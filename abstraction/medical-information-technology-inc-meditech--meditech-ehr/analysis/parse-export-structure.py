#!/usr/bin/env python3
"""
Parses MEDITECH EHI Export HTML documentation and PDF data dictionaries
to produce a complete entity inventory for analysis.

For Expanse 2.2 Ambulatory (Configuration 1): document/report-based export
For legacy platforms (Configuration 2): CSV-based export with field-level data dictionaries
"""

import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")


class TableParser(HTMLParser):
    """Extract tables from HTML."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.cur_table = None
        self.cur_row = None
        self.cur_cell = []
        self.in_cell = False
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
        elif tag == 'table':
            self.cur_table = []
        elif tag == 'tr' and self.cur_table is not None:
            self.cur_row = []
        elif tag in ('td', 'th') and self.cur_row is not None:
            self.cur_cell = []
            self.in_cell = True
        elif tag == 'br' and self.in_cell:
            self.cur_cell.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False
        elif tag == 'table' and self.cur_table is not None:
            self.tables.append(self.cur_table)
            self.cur_table = None
        elif tag == 'tr' and self.cur_row is not None:
            if self.cur_table is not None:
                self.cur_table.append(self.cur_row)
            self.cur_row = None
        elif tag in ('td', 'th') and self.in_cell:
            text = ''.join(self.cur_cell).strip()
            if self.cur_row is not None:
                self.cur_row.append(text)
            self.in_cell = False

    def handle_data(self, data):
        if not self.skip and self.in_cell:
            self.cur_cell.append(data)


def parse_html_tables(filepath):
    content = Path(filepath).read_text()
    p = TableParser()
    p.feed(content)
    return p.tables


def extract_config1_info():
    """Parse Config 1 HTML: product sections, section details."""
    tables = parse_html_tables(DOWNLOADS / "ehiexportconfig1.html")

    # Table 2: Product Version -> Included Sections
    product_sections = {}
    if len(tables) > 2:
        for row in tables[2][1:]:
            if len(row) >= 2:
                sections = [s.strip() for s in row[1].split('\n') if s.strip()]
                product_sections[row[0].strip()] = sections

    # Table 3: Section -> Details
    section_details = {}
    if len(tables) > 3:
        for row in tables[3][1:]:
            if len(row) >= 2:
                section_details[row[0].strip()] = row[1].strip()

    return product_sections, section_details


def extract_config2_info():
    """Parse Config 2 HTML: sections and details."""
    tables = parse_html_tables(DOWNLOADS / "ehiexportconfig2.html")

    section_details = {}
    for table in tables:
        if not table:
            continue
        header = [c.lower().strip() for c in table[0]]
        if 'section' in header and 'details' in header:
            for row in table[1:]:
                if len(row) >= 2:
                    section_details[row[0].strip()] = row[1].strip()
    return section_details


def parse_csv_data_dictionaries():
    """Parse all three PDF data dictionaries using pdftotext."""
    pdfs = [
        ("csacuteandambehiexportdrsolutionmerged.pdf", "Client/Server Acute & Ambulatory"),
        ("mgehiexportdrsolutionmerged.pdf", "MAGIC Acute & Ambulatory"),
        ("608ehiexportcsv.pdf", "MPM 6.08 Ambulatory"),
    ]

    all_platforms = []

    for pdf_file, platform_name in pdfs:
        pdf_path = DOWNLOADS / pdf_file
        text = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True
        ).stdout

        tables = []
        errors = []
        current_table = None

        for i, line in enumerate(text.split('\n'), 1):
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed in ('Field', 'MEDITECH') or \
               'EHI Export Data in CSV File' in trimmed or \
               trimmed.startswith('Last Updated:') or \
               trimmed.startswith('EHI Export Patient Data') or \
               trimmed.startswith('Platform:') or \
               trimmed.startswith('The tables/columns below') or \
               re.match(r'^\d+$', trimmed) or \
               (trimmed.startswith('Field') and 'Table' in trimmed and 'Column' in trimmed):
                continue

            has_multiple_cols = bool(re.search(r'\S\s{2,}\S', line))

            if not has_multiple_cols and '  ' not in trimmed and len(trimmed) > 0:
                current_table = {"tableName": trimmed, "fields": []}
                tables.append(current_table)
                continue

            if has_multiple_cols and current_table:
                parts = re.split(r'\s{2,}', trimmed)
                if len(parts) >= 3:
                    current_table["fields"].append({
                        "field": parts[0].strip(),
                        "table": parts[1].strip(),
                        "column": ' '.join(parts[2:]).strip(),
                    })
                elif len(parts) == 2:
                    current_table["fields"].append({
                        "field": parts[0].strip(),
                        "table": parts[1].strip(),
                        "column": "",
                    })
                    errors.append(f"Line {i}: Only 2 columns: {trimmed}")

        total_fields = sum(len(t["fields"]) for t in tables)
        all_platforms.append({
            "platform": platform_name,
            "sourceFile": pdf_file,
            "lastUpdated": "October 2023",
            "tables": tables,
            "totalFields": total_fields,
            "totalTables": len(tables),
            "parseErrors": errors,
        })
        print(f"  {platform_name}: {len(tables)} tables, {total_fields} fields, {len(errors)} errors")

    return all_platforms


def categorize_table_name(name):
    """Categorize a CSV table name by its prefix into a domain."""
    prefixes = {
        'Adm': 'Registration/Demographics',
        'Apr': 'Ambulatory/Practice',
        'Arm': 'Authorization/Referral Management',
        'Bbk': 'Blood Bank',
        'Bdf': 'Bed Management',
        'Chg': 'Charges/Billing',
        'Dic': 'Dictation',
        'Dgn': 'Diagnosis',
        'Dme': 'Durable Medical Equipment',
        'Doc': 'Documentation',
        'Drg': 'DRG/Coding',
        'Dsp': 'Discharge Planning',
        'Edm': 'ED Management',
        'Edu': 'Education',
        'Edc': 'Education',
        'Enc': 'Encounters',
        'Eps': 'E-Prescribing',
        'FDB': 'Drug Database',
        'Gen': 'General',
        'Hst': 'History',
        'Hub': 'Interoperability/Hub',
        'Imm': 'Immunizations',
        'Img': 'Imaging/Radiology',
        'Ins': 'Insurance',
        'Its': 'Interfaces/Transactions',
        'Lab': 'Laboratory',
        'Med': 'Medications',
        'Mic': 'Microbiology',
        'Mri': 'Medical Records/HIM',
        'Nrs': 'Nursing',
        'Nur': 'Nursing',
        'Obs': 'Obstetrics',
        'Oe': 'Order Entry/CPOE',
        'Oep': 'Order Entry/CPOE',
        'Ord': 'Orders',
        'Orp': 'Order Processing',
        'Pat': 'Patient',
        'Pbr': 'Provider/Physician',
        'Pcm': 'Care Management',
        'Pcp': 'Primary Care',
        'Pha': 'Pharmacy',
        'Phm': 'Patient Portal',
        'Pth': 'Pathology',
        'Rad': 'Radiology',
        'Reg': 'Registration',
        'Res': 'Results',
        'Rls': 'Release',
        'Rxm': 'Pharmacy/Medication Management',
        'Sch': 'Scheduling',
        'Scn': 'Scanning',
        'Srv': 'Service',
        'Sur': 'Surgery',
        'Text': 'Text/Documents',
        'Tsk': 'Tasks',
        'Trg': 'Triggers',
        'Utl': 'Utilization',
        'Vst': 'Visits',
    }
    for prefix, category in sorted(prefixes.items(), key=lambda x: -len(x[0])):
        if name.startswith(prefix):
            return category
    return 'Other'


def build_entity_inventory():
    """Build the complete entity inventory."""
    print("=== Parsing Configuration 1 (Expanse) ===")
    product_sections, section_details = extract_config1_info()

    expanse_sections = product_sections.get("MEDITECH Expanse 2.2", [])
    print(f"  Expanse 2.2 sections: {expanse_sections}")
    print(f"  Section details found: {len(section_details)}")

    print("\n=== Parsing Configuration 2 ===")
    config2_section_details = extract_config2_info()
    print(f"  Section details found: {len(config2_section_details)}")

    print("\n=== Parsing CSV Data Dictionaries ===")
    csv_platforms = parse_csv_data_dictionaries()

    # Build entities for Expanse 2.2 (Config 1)
    expanse_entities = []
    format_map = {
        "Electronic Chart": "Mixed (PDF, images: PNG/JPG/TIF/BMP)",
        "Structured Clinical Documents": "C-CDA XML",
        "FHIR Resource Bundle": "FHIR R4 JSON (US Core STU 3.1.1)",
        "Ambulatory Results": "PDF",
        "Authorization & Referral Management Reports": "PDF",
        "Financial Reports": "Text (TXT)",
        "Immunization History": "PDF",
        "Population Health": "PDF",
        "Utilization Review": "PDF",
        "Historical Ambulatory Data": "Mixed (PDF, images, text)",
    }

    for section_name in expanse_sections:
        details = section_details.get(section_name, "")
        entity = {
            "entity_name": section_name,
            "format": format_map.get(section_name, "unknown"),
            "details": details,
            "fields": [],
            "field_count": 0,
            "has_field_level_dictionary": False,
            "configuration": "Configuration 1",
            "platform": "MEDITECH Expanse 2.2",
        }
        expanse_entities.append(entity)

    # Build entities for CSV data dictionaries (Config 2)
    config2_entities = []
    for platform in csv_platforms:
        for table in platform["tables"]:
            entity = {
                "entity_name": table["tableName"],
                "format": "CSV",
                "category": categorize_table_name(table["tableName"]),
                "details": f"CSV data table with {len(table['fields'])} field-column mappings",
                "fields": table["fields"],
                "field_count": len(table["fields"]),
                "has_field_level_dictionary": True,
                "configuration": "Configuration 2",
                "platform": platform["platform"],
            }
            config2_entities.append(entity)

    # Full inventory
    inventory = {
        "extraction_date": "2026-02-16",
        "product_analyzed": "MEDITECH Expanse 2.2 Ambulatory",
        "applicable_configuration": "Configuration 1",
        "note": "Configuration 1 (Expanse) has NO field-level data dictionary. The CSV data dictionaries in the PDFs apply only to Configuration 2 (legacy platforms: Client/Server, MAGIC, 6.08 Ambulatory).",
        "configurations": {
            "configuration_1": {
                "description": "Document/report-based export with FHIR and C-CDA. No field-level data dictionary provided.",
                "applicable_platforms": [
                    "Expanse 2.2 (Acute & Ambulatory)",
                    "Expanse 2.1 (Acute & Ambulatory)",
                    "6.15 (Acute & Ambulatory)",
                    "6.08 (Acute only)",
                    "Client/Server (Acute only)",
                    "MAGIC (Acute only)",
                ],
                "prerequisites": ["HIM", "SCN (Scanning and Archiving with eChart)", "PHM (Patient Portal, optional)"],
                "all_product_sections": product_sections,
                "section_details": section_details,
                "expanse_2_2_entities": expanse_entities,
                "total_sections_expanse_2_2": len(expanse_sections),
                "has_field_level_data_dictionary": False,
            },
            "configuration_2": {
                "description": "CSV-based export with field-level data dictionaries (NOT applicable to Expanse 2.2 Ambulatory)",
                "applicable_platforms": [
                    "MPM 6.08 (Ambulatory only)",
                    "Client/Server (Acute & Ambulatory)",
                    "MAGIC (Acute & Ambulatory)",
                ],
                "prerequisites": ["MRI (Medical Records)", "DR (Data Repository)"],
                "section_details": config2_section_details,
                "platforms": [{
                    "platform": p["platform"],
                    "sourceFile": p["sourceFile"],
                    "totalTables": p["totalTables"],
                    "totalFields": p["totalFields"],
                    "parseErrors": p["parseErrors"],
                } for p in csv_platforms],
                "entities": config2_entities,
                "total_tables_across_platforms": sum(p["totalTables"] for p in csv_platforms),
                "total_fields_across_platforms": sum(p["totalFields"] for p in csv_platforms),
                "has_field_level_data_dictionary": True,
            },
        },
    }

    return inventory


def build_summary(inventory):
    """Build summary statistics."""
    config1 = inventory["configurations"]["configuration_1"]
    config2 = inventory["configurations"]["configuration_2"]

    # Categorize Config 2 tables by domain
    domain_stats = {}
    for entity in config2["entities"]:
        cat = entity.get("category", "Other")
        domain_stats.setdefault(cat, {"tables": 0, "fields": 0, "platforms": set()})
        domain_stats[cat]["tables"] += 1
        domain_stats[cat]["fields"] += entity["field_count"]
        domain_stats[cat]["platforms"].add(entity["platform"])

    domain_stats_out = {}
    for cat in sorted(domain_stats.keys(), key=lambda c: -domain_stats[c]["fields"]):
        domain_stats_out[cat] = {
            "tables": domain_stats[cat]["tables"],
            "fields": domain_stats[cat]["fields"],
            "platforms": sorted(domain_stats[cat]["platforms"]),
        }

    summary = {
        "product_analyzed": "MEDITECH Expanse 2.2 Ambulatory",
        "applicable_configuration": "Configuration 1",
        "configuration_1_summary": {
            "total_sections": config1["total_sections_expanse_2_2"],
            "section_list": [e["entity_name"] for e in config1["expanse_2_2_entities"]],
            "section_formats": {e["entity_name"]: e["format"] for e in config1["expanse_2_2_entities"]},
            "has_field_level_data_dictionary": False,
            "note": "No structured data dictionary. Export is document/report-based with FHIR and C-CDA.",
        },
        "configuration_2_summary": {
            "note": "NOT applicable to Expanse 2.2, but shown for reference (legacy platforms only)",
            "total_tables_across_platforms": config2["total_tables_across_platforms"],
            "total_fields_across_platforms": config2["total_fields_across_platforms"],
            "has_field_level_data_dictionary": True,
            "platforms": config2["platforms"],
            "domain_categories": domain_stats_out,
        },
    }

    return summary


def main():
    inventory = build_entity_inventory()

    with open(OUTPUT / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nSaved entity-inventory-full.json")

    summary = build_summary(inventory)
    with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved entity-inventory-summary.json")

    # Print key stats
    c1 = inventory["configurations"]["configuration_1"]
    c2 = inventory["configurations"]["configuration_2"]
    print(f"\n=== KEY STATS ===")
    print(f"Configuration 1 (Expanse 2.2): {c1['total_sections_expanse_2_2']} sections, NO field-level data dictionary")
    print(f"Configuration 2 (Legacy): {c2['total_tables_across_platforms']} tables, {c2['total_fields_across_platforms']} fields across 3 platforms")
    print(f"\nExpanse 2.2 Export Sections:")
    for e in c1["expanse_2_2_entities"]:
        print(f"  - {e['entity_name']} [{e['format']}]")

    print(f"\nConfig 2 Domain Categories:")
    for cat, stats in summary["configuration_2_summary"]["domain_categories"].items():
        print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields")


if __name__ == "__main__":
    main()
