#!/usr/bin/env python3
"""Parse the B10_EHI_Export.pdf data dictionary into structured JSON.

Reads the pdftotext output and extracts the Section/Elements table from pages 5-7.
"""

import json
import subprocess
import re

def parse_dictionary():
    result = subprocess.run(
        ["pdftotext", "-layout", "../downloads/B10_EHI_Export.pdf", "-"],
        capture_output=True, text=True
    )
    text = result.stdout

    # Find the data dictionary table starting after "Export Format" heading
    lines = text.split("\n")
    
    entities = []
    current_section = None
    in_table = False
    
    # The table has Section and Elements columns
    for line in lines:
        stripped = line.strip()
        
        # Skip headers, footers, empty lines
        if not stripped:
            continue
        if "2184 Morris Ave" in stripped or "Phone:" in stripped or "Email:" in stripped:
            continue
        if "Web:" in stripped or "Support:" in stripped:
            continue
        if "(b)(10) Electronic Health Information" in stripped:
            continue
        if "§ 170.205" in stripped:
            in_table = True
            continue
        if stripped == "Section" and "Elements" in line:
            in_table = True
            continue
            
        if not in_table:
            continue

        # Detect section names vs element names based on indentation
        # Section names appear at left margin, elements are indented
        indent = len(line) - len(line.lstrip())
        
        # Check if this is a section name (less indented) or element (more indented)
        if indent < 15 and stripped and not stripped.startswith("Section"):
            # New section
            if current_section:
                entities.append(current_section)
            current_section = {
                "section": stripped,
                "elements": []
            }
        elif indent >= 15 and current_section and stripped:
            current_section["elements"].append(stripped)
    
    if current_section:
        entities.append(current_section)
    
    # Fix: "Medical Equipments" splits across lines in PDF layout
    # Merge "Medical" (0 elements) + "Equipments" (with elements) into "Medical Equipments"
    merged = []
    skip_next = False
    for i, e in enumerate(entities):
        if skip_next:
            skip_next = False
            continue
        if e["section"] == "Medical" and len(e["elements"]) == 0 and i + 1 < len(entities) and entities[i+1]["section"] == "Equipments":
            merged.append({
                "section": "Medical Equipments",
                "elements": entities[i+1]["elements"]
            })
            skip_next = True
        else:
            merged.append(e)
    
    return merged

def build_full_inventory(entities):
    """Build entity-inventory-full.json format."""
    inventory = []
    for entity in entities:
        fields = []
        for elem in entity["elements"]:
            fields.append({
                "name": elem,
                "type": None,
                "description": None,
                "nullable": None,
                "max_length": None,
                "foreign_key": None,
                "value_set": None,
                "coded_values": None,
                "default_value": None,
                "example_data": None
            })
        inventory.append({
            "entity": entity["section"],
            "category": "C-CDA Section",
            "field_count": len(fields),
            "fields": fields
        })
    return inventory

def build_summary(inventory):
    """Build entity-inventory-summary.json."""
    total_entities = len(inventory)
    total_fields = sum(e["field_count"] for e in inventory)
    fields_with_descriptions = sum(
        1 for e in inventory for f in e["fields"] if f["description"]
    )
    
    entity_summary = []
    for e in inventory:
        entity_summary.append({
            "entity": e["entity"],
            "field_count": e["field_count"],
            "fields_with_descriptions": sum(1 for f in e["fields"] if f["description"]),
            "fields_with_types": sum(1 for f in e["fields"] if f["type"]),
        })
    
    return {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "fields_with_types": 0,
        "pct_fields_with_descriptions": 0.0,
        "pct_fields_with_types": 0.0,
        "categories": {"C-CDA Section": {
            "entity_count": total_entities,
            "field_count": total_fields
        }},
        "entities": entity_summary
    }

if __name__ == "__main__":
    entities = parse_dictionary()
    
    print(f"Parsed {len(entities)} sections:")
    for e in entities:
        print(f"  {e['section']}: {len(e['elements'])} elements")
    
    total_elements = sum(len(e["elements"]) for e in entities)
    print(f"\nTotal elements: {total_elements}")
    
    inventory = build_full_inventory(entities)
    summary = build_summary(inventory)
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nWrote entity-inventory-full.json ({len(inventory)} entities)")
    print(f"Wrote entity-inventory-summary.json")
    print(f"\nSummary:")
    print(f"  Total entities: {summary['total_entities']}")
    print(f"  Total fields: {summary['total_fields']}")
    print(f"  Fields with descriptions: {summary['fields_with_descriptions']} (0%)")
    print(f"  Fields with types: 0 (0%)")
