#!/usr/bin/env python3
"""Parse Harris CareTracker EHI Export PDF data dictionary into structured JSON.

Reads the PDF text extracted via pdftotext and parses the table of Data Classes
and their Column Headings into a complete entity-inventory-full.json.
"""

import json
import re
import subprocess
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "downloads",
                        "CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf")
OUT_DIR = os.path.dirname(__file__)


def main():
    result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"],
                            capture_output=True, text=True)
    text = result.stdout
    lines = text.split("\n")

    entities = []
    current_entity = None
    current_fields_text = ""
    in_table = False

    def save_current():
        nonlocal current_entity, current_fields_text
        if current_entity and current_fields_text:
            # Parse fields from comma-separated text
            cleaned = re.sub(r'\s+', ' ', current_fields_text).strip()
            # Remove trailing commas
            cleaned = cleaned.rstrip(',')
            raw_fields = [f.strip() for f in cleaned.split(',') if f.strip()]
            fields = []
            for f in raw_fields:
                fields.append({
                    "name": f,
                    "type": None,
                    "description": None
                })
            entities.append({
                "entity_name": current_entity,
                "field_count": len(fields),
                "fields": fields
            })
        current_entity = None
        current_fields_text = ""

    for line in lines:
        stripped = line.rstrip()
        if "CareTracker EHI Export: Folder Organization" in stripped:
            continue
        if re.match(r'^\s*\d+\s*$', stripped):
            continue
        if not stripped.strip():
            continue
        if "Data Class Name" in stripped and "Column Headings" in stripped:
            in_table = True
            continue
        if not in_table:
            continue

        leading_spaces = len(stripped) - len(stripped.lstrip())

        # New entity: text starts at left margin with fields after gap
        match = re.match(r'^(\s{0,29}\S.*?)\s{3,}(\w+.*)', stripped)
        if match and leading_spaces < 30:
            save_current()
            current_entity = match.group(1).strip()
            current_fields_text = match.group(2).strip()
        elif leading_spaces < 5 and current_entity:
            # Continuation of entity name (multi-line name like "Allergies and Intolerances\n Pending")
            # But only if the line doesn't look like field names
            txt = stripped.strip()
            if ',' not in txt and len(txt.split()) <= 4:
                current_entity += " " + txt
            else:
                current_fields_text += " " + txt
        elif leading_spaces >= 5:
            # Continuation of fields
            current_fields_text += " " + stripped.strip()

    save_current()

    # Post-process: fix known entity names
    # The PDF shows "Allergies and Intolerances Pending" and "Allergies and Intolerances" as separate
    # Also "Occupation and Industry History" spans two lines

    # Build full inventory
    total_fields = sum(e["field_count"] for e in entities)

    inventory = {
        "product": "Harris CareTracker",
        "source": "CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf",
        "version": "v1.0",
        "export_formats": ["CSV", "JSON", "XML"],
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "entities": entities
    }

    # Write full inventory
    with open(os.path.join(OUT_DIR, "entity-inventory-full.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    # Write summary
    summary = {
        "product": inventory["product"],
        "source": inventory["source"],
        "version": inventory["version"],
        "export_formats": inventory["export_formats"],
        "total_entities": inventory["total_entities"],
        "total_fields": inventory["total_fields"],
        "fields_with_descriptions": inventory["fields_with_descriptions"],
        "fields_with_types": inventory["fields_with_types"],
        "pct_fields_with_descriptions": "0%",
        "entity_summary": [
            {
                "entity_name": e["entity_name"],
                "field_count": e["field_count"]
            }
            for e in entities
        ]
    }

    with open(os.path.join(OUT_DIR, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: 0 (PDF only provides column headings, no descriptions)")
    print(f"Fields with types: 0 (PDF only provides column headings, no types)")
    print()
    for e in entities:
        print(f"  {e['entity_name']}: {e['field_count']} fields")

if __name__ == "__main__":
    main()
