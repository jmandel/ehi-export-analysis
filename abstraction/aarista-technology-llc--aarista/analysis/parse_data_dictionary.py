#!/usr/bin/env python3
"""Parse the Aarista EHI Export Data Dictionary PDF and produce structured counts."""

import json
import re
import subprocess

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/aarista-technology-llc/downloads/Aarista_EHI_Export.pdf"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_tables(text):
    """Parse the PDF text into structured tables with fields."""
    tables = []
    current_table = None
    
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Detect table headers
        if stripped.startswith("Single Patient -") or stripped.startswith("Practice Patients -"):
            if current_table:
                tables.append(current_table)
            current_table = {
                "name": stripped,
                "fields": [],
                "category": "Single Patient" if stripped.startswith("Single Patient") else "Practice (Bulk)"
            }
            continue
        
        # Skip header rows and non-field lines
        if stripped in ("Data Field", "Data Type", "Data Field                          Data Type"):
            continue
        if stripped.startswith("Data Field") and "Data Type" in stripped:
            continue
        if stripped.startswith("EHI Export") or stripped.startswith("The Electronic"):
            continue
        if stripped.startswith("•") or stripped.startswith("Data Dictionary"):
            continue
        
        # Parse field lines: field name followed by data type
        if current_table is not None:
            # Match lines with field name and data type
            match = re.match(r'^(.+?)\s{2,}(.+)$', stripped)
            if match:
                field_name = match.group(1).strip().rstrip("*")
                data_type = match.group(2).strip()
                # Only include if data_type looks like a SQL type
                if any(t in data_type.lower() for t in ["varchar", "nchar", "int", "date", "float", "bit", "digits", "derived", "n/a", "constant"]):
                    required = "*" in match.group(1)
                    has_multiple = "multiple records" in data_type.lower()
                    current_table["fields"].append({
                        "name": field_name,
                        "type": data_type,
                        "required": required,
                        "has_multiple_records": has_multiple,
                        "has_description": False  # No descriptions in this PDF
                    })
    
    if current_table:
        tables.append(current_table)
    
    return tables

def main():
    text = extract_text()
    tables = parse_tables(text)
    
    # Summary stats
    total_fields = sum(len(t["fields"]) for t in tables)
    total_required = sum(sum(1 for f in t["fields"] if f["required"]) for t in tables)
    total_multi = sum(sum(1 for f in t["fields"] if f["has_multiple_records"]) for t in tables)
    
    print("=" * 70)
    print("AARISTA EHI EXPORT DATA DICTIONARY - PARSED SUMMARY")
    print("=" * 70)
    print(f"\nTotal tables: {len(tables)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: 0 (0%)")
    print(f"Required fields: {total_required}")
    print(f"Multi-record fields: {total_multi}")
    print()
    
    for t in tables:
        print(f"\n--- {t['name']} ---")
        print(f"  Category: {t['category']}")
        print(f"  Fields: {len(t['fields'])}")
        req = sum(1 for f in t['fields'] if f['required'])
        print(f"  Required: {req}")
        for f in t['fields']:
            marker = "*" if f["required"] else " "
            multi = " [MULTI]" if f["has_multiple_records"] else ""
            print(f"    {marker} {f['name']:<40} {f['type']}{multi}")
    
    # Save as JSON
    output = {
        "summary": {
            "total_tables": len(tables),
            "total_fields": total_fields,
            "fields_with_descriptions": 0,
            "description_percentage": 0,
            "required_fields": total_required,
            "multi_record_fields": total_multi
        },
        "tables": tables
    }
    
    with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/aarista-technology-llc--aarista/analysis/parsed_data_dictionary.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n\nJSON output saved to analysis/parsed_data_dictionary.json")

if __name__ == "__main__":
    main()
