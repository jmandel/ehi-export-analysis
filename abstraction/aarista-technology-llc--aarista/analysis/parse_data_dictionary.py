#!/usr/bin/env python3
"""Parse the Aarista EHI Export Data Dictionary PDF into structured JSON."""

import json
import re
import subprocess
import sys

def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_tables(text):
    """Parse the data dictionary tables from extracted PDF text."""
    entities = []
    current_entity = None
    current_fields = []
    
    lines = text.split("\n")
    
    # Table headers we expect to find
    table_headers = [
        "Single Patient - Patient Demographics",
        "Single Patient - Patient Addresses",
        "Single Patient - Patient Contacts",
        "Single Patient - Patient Insurances",
        "Single Patient - Patient Encounters – Clinical and Billing",
        "Practice Patients - Patient Demographics and Billing Encounters",
        "Practice Patients - Patient Demographics and Clinical Encounters",
    ]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this line starts a new table
        matched_header = None
        for header in table_headers:
            # Normalize dashes for matching
            normalized_line = line.replace("–", "-").replace("—", "-")
            normalized_header = header.replace("–", "-").replace("—", "-")
            if normalized_header.lower() in normalized_line.lower():
                matched_header = header
                break
        
        if matched_header:
            # Save previous entity
            if current_entity and current_fields:
                entities.append({
                    "name": current_entity,
                    "fields": current_fields
                })
            current_entity = matched_header
            current_fields = []
            i += 1
            continue
        
        # Skip header rows and empty lines
        if not line or "Data Field" in line or "Data Type" in line:
            i += 1
            continue
        
        # Try to parse a field line: field name followed by data type
        if current_entity:
            # Match patterns like "First Name*    nvarchar(256)"
            # or "SSN    nvarchar(9)"
            # or "Policy Holder    derived field"
            field_match = re.match(
                r'^(.+?)\s{2,}(\S.+)$', line
            )
            if field_match:
                field_name = field_match.group(1).strip()
                data_type = field_match.group(2).strip()
                
                # Skip if it looks like a sub-header
                if field_name in ["Data Field", "Data Type"]:
                    i += 1
                    continue
                
                required = "*" in field_name
                field_name = field_name.replace("*", "").strip()
                
                # Check for notes like "- multiple records"
                notes = None
                if " - " in data_type:
                    parts = data_type.split(" - ", 1)
                    data_type = parts[0].strip()
                    notes = parts[1].strip()
                
                current_fields.append({
                    "name": field_name,
                    "type": data_type,
                    "required": required,
                    "description": "",  # No descriptions in this dictionary
                    "notes": notes
                })
            
        i += 1
    
    # Save last entity
    if current_entity and current_fields:
        entities.append({
            "name": current_entity,
            "fields": current_fields
        })
    
    return entities

def main():
    pdf_path = "../downloads/Aarista_EHI_Export.pdf"
    text = extract_pdf_text(pdf_path)
    entities = parse_tables(text)
    
    # Also handle the Communication sub-table within Addresses
    # The PDF has a sub-table for Communication Type/Phone/Email within Addresses
    # Let's check if it got merged into Addresses or missed
    
    # Build full inventory
    inventory = {
        "source": "Aarista_EHI_Export.pdf",
        "source_description": "EHI Export Data Dictionary, 8-page PDF, created 2023-11-28",
        "export_modes": [
            "Single Patient - individual patient export",
            "Practice Patients - bulk export for all patients in a practice"
        ],
        "entities": []
    }
    
    total_fields = 0
    for entity in entities:
        total_fields += len(entity["fields"])
        inventory["entities"].append(entity)
    
    inventory["summary"] = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": sum(1 for e in entities for f in e["fields"] if f["type"] and f["type"] != "n/a"),
        "fields_required": sum(1 for e in entities for f in e["fields"] if f["required"]),
    }
    
    # Write full inventory
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Write summary
    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": inventory["summary"]["fields_with_types"],
        "fields_required": inventory["summary"]["fields_required"],
        "entities_summary": []
    }
    for entity in entities:
        summary["entities_summary"].append({
            "name": entity["name"],
            "field_count": len(entity["fields"]),
            "required_fields": sum(1 for f in entity["fields"] if f["required"]),
            "fields_with_types": sum(1 for f in entity["fields"] if f["type"] and f["type"] != "n/a"),
        })
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary to stdout
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: 0 (no descriptions provided)")
    print(f"Fields with types: {inventory['summary']['fields_with_types']}")
    print(f"Required fields: {inventory['summary']['fields_required']}")
    print()
    for entity in entities:
        print(f"  {entity['name']}: {len(entity['fields'])} fields")

if __name__ == "__main__":
    main()
