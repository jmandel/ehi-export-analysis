"""
Parse all FHIR resource HTML documentation pages from One Medical's API docs.
Extracts field-level detail for each resource type and outputs entity-inventory-full.json.
"""
import json
import os
import sys
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
FHIR_RESOURCES_DIR = DOWNLOADS / "fhir" / "resources"

class TableExtractor(HTMLParser):
    """Extract all HTML tables as lists of rows (lists of cell text)."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = ''
        self.tables = []
        self.current_table = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
        if tag == 'table':
            self.in_table = True
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.current_cell = ''
        elif tag == 'br' and self.in_cell:
            self.current_cell += '\n'

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False
        if tag == 'table':
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
        elif tag == 'tr':
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag in ('td', 'th'):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_cell:
            self.current_cell += data


def parse_resource_html(filepath):
    """Parse a single FHIR resource HTML file and return structured field data."""
    with open(filepath, 'r') as f:
        html = f.read()

    parser = TableExtractor()
    parser.feed(html)

    resource_name = filepath.stem
    fields = []

    for table in parser.tables:
        if not table:
            continue
        header = [h.lower().strip() for h in table[0]]
        if 'field name' not in header:
            continue

        name_idx = header.index('field name')
        type_idx = header.index('field type') if 'field type' in header else None
        card_idx = None
        desc_idx = None
        for i, h in enumerate(header):
            if 'cardinality' in h:
                card_idx = i
            if 'description' in h:
                desc_idx = i

        for row in table[1:]:
            if len(row) <= name_idx:
                continue
            field = {
                "name": row[name_idx].strip(),
                "type": row[type_idx].strip() if type_idx is not None and len(row) > type_idx else "",
                "cardinality": row[card_idx].strip() if card_idx is not None and len(row) > card_idx else "",
                "description": row[desc_idx].strip() if desc_idx is not None and len(row) > desc_idx else "",
            }
            # Clean up description
            field["has_description"] = bool(field["description"])
            fields.append(field)

    return {
        "entity": resource_name,
        "source_file": str(filepath.relative_to(DOWNLOADS.parent)),
        "field_count": len(fields),
        "fields": fields
    }


def parse_ehi_overview():
    """Parse the EHI export overview to get the list of resource types and C-CDA sections."""
    overview_path = DOWNLOADS / "ehi-export-overview.html"
    with open(overview_path) as f:
        html = f.read()

    parser = TableExtractor()
    parser.feed(html)

    fhir_resources = []
    ccda_sections = []

    for table in parser.tables:
        if not table:
            continue
        header = table[0]
        if len(header) == 1:
            h = header[0].lower().strip()
            if 'resource' in h:
                fhir_resources = [row[0].strip() for row in table[1:] if row]
            elif 'c-cda' in h or 'section' in h:
                ccda_sections = [row[0].strip() for row in table[1:] if row]

    return fhir_resources, ccda_sections


def parse_ccda_sections():
    """Parse the C-CDA documentation page for section details."""
    ccda_path = DOWNLOADS / "ccda" / "patient-continuity-of-care-document.html"
    if not ccda_path.exists():
        return []

    with open(ccda_path) as f:
        html = f.read()

    parser = TableExtractor()
    parser.feed(html)

    sections = []
    for table in parser.tables:
        if not table:
            continue
        header = [h.lower().strip() for h in table[0]]
        for row in table[1:]:
            if row:
                sections.append({
                    "header": header,
                    "values": row
                })

    return sections


def main():
    # Parse EHI overview
    ehi_fhir_resources, ehi_ccda_sections = parse_ehi_overview()
    print(f"EHI Export FHIR resources: {len(ehi_fhir_resources)}")
    print(f"  {ehi_fhir_resources}")
    print(f"EHI Export C-CDA sections: {len(ehi_ccda_sections)}")
    print(f"  {ehi_ccda_sections}")

    # Parse all FHIR resource pages
    entities = []
    total_fields = 0
    total_described = 0

    resource_files = sorted(FHIR_RESOURCES_DIR.glob("*.html"))
    print(f"\nParsing {len(resource_files)} FHIR resource documentation pages...")

    for rf in resource_files:
        entity = parse_resource_html(rf)
        entities.append(entity)
        total_fields += entity["field_count"]
        described = sum(1 for f in entity["fields"] if f["has_description"])
        total_described += described
        print(f"  {entity['entity']}: {entity['field_count']} fields ({described} described)")

    # Build full inventory
    inventory = {
        "product": "1Life (One Medical)",
        "export_format": "FHIR R4 JSON + C-CDA 2.1 XML",
        "ehi_export_fhir_resources": ehi_fhir_resources,
        "ehi_export_ccda_sections": ehi_ccda_sections,
        "documented_fhir_resources": [e["entity"] for e in entities],
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_fields_with_descriptions": total_described,
        "description_coverage_pct": round(total_described / total_fields * 100, 1) if total_fields else 0,
        "entities": entities
    }

    # Also note resources in EHI export but NOT in FHIR docs (and vice versa)
    ehi_set = set(r.lower().replace(" ", "") for r in ehi_fhir_resources)
    doc_set = set(e["entity"].lower() for e in entities)

    in_ehi_not_doc = [r for r in ehi_fhir_resources if r.lower().replace(" ", "") not in doc_set]
    in_doc_not_ehi = [e["entity"] for e in entities if e["entity"].lower() not in ehi_set]

    inventory["in_ehi_export_but_no_doc_page"] = in_ehi_not_doc
    inventory["in_doc_but_not_ehi_export"] = in_doc_not_ehi

    # Write full inventory
    output_path = Path(__file__).parent / "entity-inventory-full.json"
    with open(output_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f"\nWrote {output_path}")

    # Write summary
    summary = {
        "product": inventory["product"],
        "export_format": inventory["export_format"],
        "total_fhir_resource_types_in_ehi": len(ehi_fhir_resources),
        "total_ccda_sections_in_ehi": len(ehi_ccda_sections),
        "total_documented_resource_types": len(entities),
        "total_fields_across_all_resources": total_fields,
        "total_fields_with_descriptions": total_described,
        "description_coverage_pct": inventory["description_coverage_pct"],
        "entities_summary": [
            {
                "entity": e["entity"],
                "field_count": e["field_count"],
                "fields_with_descriptions": sum(1 for f in e["fields"] if f["has_description"])
            }
            for e in entities
        ],
        "in_ehi_export_but_no_doc_page": in_ehi_not_doc,
        "in_doc_but_not_ehi_export": in_doc_not_ehi
    }

    summary_path = Path(__file__).parent / "entity-inventory-summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {summary_path}")

    # Print summary table
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"EHI Export FHIR resources listed:  {len(ehi_fhir_resources)}")
    print(f"EHI Export C-CDA sections listed:  {len(ehi_ccda_sections)}")
    print(f"FHIR resource doc pages parsed:    {len(entities)}")
    print(f"Total fields documented:           {total_fields}")
    print(f"Fields with descriptions:          {total_described} ({inventory['description_coverage_pct']}%)")
    print(f"In EHI but no doc page:            {in_ehi_not_doc}")
    print(f"In doc but not EHI list:           {in_doc_not_ehi}")


if __name__ == "__main__":
    main()
