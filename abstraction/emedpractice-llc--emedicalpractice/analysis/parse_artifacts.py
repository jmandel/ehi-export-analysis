#!/usr/bin/env python3
"""
Parse all EHI export artifacts for eMedPractice and produce:
  - full-entity-inventory.json  (complete field-level parse)
  - export-content-summary.json (structured export page content)
  - analysis-stats.json         (aggregate statistics)
"""

import json
import os
from html.parser import HTMLParser
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent.parent / "results" / "emedpractice-llc--emedicalpractice" / "downloads"
OUTPUT_DIR = Path(__file__).parent


# --- Parse data dictionary tables from the WP API JSON ---
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.in_th = False
        self.in_h2 = False
        self.tables = []
        self.table_names = []
        self.current_table = []
        self.current_row = []
        self.current_cell = ""
        self.last_heading = ""

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
            self.table_names.append(self.last_heading)
        elif tag == "tr":
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_td = tag == "td"
            self.in_th = tag == "th"
            self.current_cell = ""
        elif tag == "h2":
            self.in_h2 = True
            self.last_heading = ""

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
            self.tables.append(self.current_table)
        elif tag == "tr":
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag in ("td", "th"):
            self.in_td = False
            self.in_th = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "h2":
            self.in_h2 = False

    def handle_data(self, data):
        if self.in_td or self.in_th:
            self.current_cell += data
        elif self.in_h2:
            self.last_heading += data


def parse_data_dictionary():
    """Parse the WP API JSON for the data dictionary page."""
    api_file = RESULTS_DIR / "ehi-data-dictionary-tables-api.json"
    with open(api_file) as f:
        data = json.load(f)

    if isinstance(data, list):
        data = data[0]

    content = data.get("content", {}).get("rendered", "")
    page_meta = {
        "created": data.get("date"),
        "modified": data.get("modified"),
        "title": data.get("title", {}).get("rendered", ""),
    }

    parser = TableParser()
    parser.feed(content)

    # De-duplicate: page renders tables twice (WordPress/Elementor artifact)
    # Tables 4-6 are exact duplicates of 1-3
    unique_tables = []
    seen_names = set()
    for i, (name, table_data) in enumerate(zip(parser.table_names, parser.tables)):
        if name not in seen_names:
            seen_names.add(name)
            unique_tables.append((name, table_data))

    entities = []
    total_fields = 0
    for name, rows in unique_tables:
        if not rows:
            continue
        header = rows[0]
        data_rows = rows[1:]

        fields = []
        for row in data_rows:
            field = {
                "name": row[0] if len(row) > 0 else "",
                "dataType": row[1] if len(row) > 1 else "",
                "defaultValue": row[2] if len(row) > 2 and row[2] else None,
                "notNull": row[3].strip() == "Not Null" if len(row) > 3 else False,
                "description": None,  # No descriptions provided
                "foreignKey": None,
                "valueSet": None,
            }
            fields.append(field)

        # Categorize based on table name
        if "patient" in name.lower():
            category = "Demographics"
        elif "insurance" in name.lower():
            category = "Insurance"
        elif "appointment" in name.lower():
            category = "Scheduling"
        else:
            category = "Other"

        entities.append({
            "tableName": name.replace(" Table Schema", "").strip(),
            "category": category,
            "fieldCount": len(fields),
            "fieldsWithDescriptions": 0,
            "fieldsWithTypes": sum(1 for f in fields if f["dataType"]),
            "fields": fields,
        })
        total_fields += len(fields)

    return entities, total_fields, page_meta


def parse_export_page():
    """Parse the WP API JSON for the export page."""
    api_file = RESULTS_DIR / "ehi-export-page-api.json"
    with open(api_file) as f:
        data = json.load(f)

    page_meta = {
        "created": data.get("date"),
        "modified": data.get("modified"),
        "title": data.get("title", {}).get("rendered", ""),
    }

    content = data.get("content", {}).get("rendered", "")

    # Check for commented-out Section 4
    import re
    comments = re.findall(r"<!--(.*?)-->", content, re.DOTALL)
    commented_sections = []
    for c in comments:
        if "Documents" in c or "Scaned" in c:
            commented_sections.append(c.strip())

    has_section_4_commented = len(commented_sections) > 0

    return {
        "page_meta": page_meta,
        "export_components": [
            {
                "section": "1. Clinical Data in CDA Format",
                "format": "C-CDA (XML)",
                "description": "Patient encounters as CDA documents; consolidated CDA file per patient; organized by chart number",
                "claims": "Includes all data elements defined in USCDI v3, in addition to other EHI the system stores",
            },
            {
                "section": "2. Patient Details Data",
                "format": "CSV",
                "description": "Demographics, insurance details, and appointments",
                "data_dictionary_link": "https://emedpractice.com/electronic-health-information-data-dictionary-tables",
            },
            {
                "section": "4. Documents (commented out)",
                "format": "PDF, JPG, PNG",
                "description": "Signed progress notes, lab results, radiology reports, scanned/uploaded documents",
                "status": "commented_out_in_html",
                "visible": False,
            },
        ],
        "commented_out_section_4": has_section_4_commented,
        "notes": [
            "Exports use encryption and secure transmission",
            "CSV exports also available via Reports section in app",
        ],
    }


def compute_stats(entities, total_fields, export_info):
    """Compute aggregate statistics."""
    fields_with_descriptions = sum(e["fieldsWithDescriptions"] for e in entities)
    fields_with_types = sum(e["fieldsWithTypes"] for e in entities)

    # Count coded fields (int fields that appear to be FKs or coded values)
    coded_fields = []
    for e in entities:
        for f in e["fields"]:
            if f["dataType"] == "int" and f["name"] not in ("ChartNo",):
                coded_fields.append(f"{e['tableName']}.{f['name']}")
            elif f["dataType"] == "varchar" and f["name"] in (
                "status", "MaritalStatus", "Race", "Ethnicity", "Gender", "PatientRel", "PatientRel1"
            ):
                coded_fields.append(f"{e['tableName']}.{f['name']}")

    # Data type distribution
    type_counts = {}
    for e in entities:
        for f in e["fields"]:
            dt = f["dataType"]
            type_counts[dt] = type_counts.get(dt, 0) + 1

    # Category breakdown
    category_breakdown = {}
    for e in entities:
        cat = e["category"]
        if cat not in category_breakdown:
            category_breakdown[cat] = {"tables": 0, "fields": 0}
        category_breakdown[cat]["tables"] += 1
        category_breakdown[cat]["fields"] += e["fieldCount"]

    return {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "fields_with_descriptions_pct": 0.0,
        "fields_with_types": fields_with_types,
        "fields_with_types_pct": round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
        "coded_fields_without_value_sets": coded_fields,
        "coded_fields_count": len(coded_fields),
        "data_type_distribution": type_counts,
        "category_breakdown": category_breakdown,
        "data_type_typo": "InsuredDOB typed as 'datet' (likely typo for 'date')",
        "duplicate_tables_in_html": "Data dictionary page renders all 3 tables twice (6 HTML tables total); tables 4-6 are exact duplicates of 1-3",
        "export_formats": ["C-CDA (XML)", "CSV"],
        "sample_data_provided": False,
        "machine_readable_schema": False,
        "export_instructions": False,
        "has_commented_out_section": export_info["commented_out_section_4"],
    }


def main():
    entities, total_fields, dd_meta = parse_data_dictionary()
    export_info = parse_export_page()
    stats = compute_stats(entities, total_fields, export_info)

    # Write full entity inventory
    inventory = {
        "source": "https://emedpractice.com/electronic-health-information-data-dictionary-tables/",
        "data_dictionary_created": dd_meta["created"],
        "data_dictionary_modified": dd_meta["modified"],
        "total_entities": len(entities),
        "total_fields": total_fields,
        "entities": entities,
    }
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)

    # Write export content summary
    with open(OUTPUT_DIR / "export-content-summary.json", "w") as f:
        json.dump(export_info, f, indent=2)

    # Write stats
    with open(OUTPUT_DIR / "analysis-stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # Print summary
    print(f"Entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {stats['fields_with_descriptions']} (0%)")
    print(f"Fields with types: {stats['fields_with_types']} ({stats['fields_with_types_pct']}%)")
    print(f"Coded fields w/o value sets: {stats['coded_fields_count']}")
    print(f"Data types: {stats['data_type_distribution']}")
    print(f"Category breakdown: {json.dumps(stats['category_breakdown'], indent=2)}")
    print(f"Data type typo: {stats['data_type_typo']}")
    print(f"Commented-out Section 4: {stats['has_commented_out_section']}")
    print(f"\nFiles written:")
    print(f"  full-entity-inventory.json")
    print(f"  export-content-summary.json")
    print(f"  analysis-stats.json")


if __name__ == "__main__":
    main()
