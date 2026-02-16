#!/usr/bin/env python3
"""Parse the Aarista EHI Export Data Dictionary PDF and produce full-entity-inventory.json."""

import json
import subprocess
import re
import sys

PDF_PATH = "../../../results/aarista-technology-llc--aarista/downloads/Aarista_EHI_Export.pdf"
OUTPUT_PATH = "full-entity-inventory.json"
STATS_PATH = "summary-stats.json"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_tables(text):
    """Parse the PDF text into structured table definitions."""
    tables = []
    current_table = None
    
    # Split into lines
    lines = text.split('\n')
    
    # Table headers we expect
    table_patterns = [
        ("Single Patient - Patient Demographics", "demographics"),
        ("Single Patient - Patient Addresses", "addresses"),
        ("Single Patient - Patient Contacts", "contacts"),
        ("Single Patient - Patient Insurances", "insurances"),
        ("Single Patient - Patient Encounters – Clinical and Billing", "encounters_clinical_billing"),
        ("Practice Patients - Patient Demographics and Billing Encounters", "practice_billing"),
        ("Practice Patients - Patient Demographics and Clinical Encounters", "practice_clinical"),
    ]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for table header
        for pattern, table_id in table_patterns:
            # Normalize dashes/hyphens for matching
            normalized_line = line.replace('–', '–').replace('—', '–')
            normalized_pattern = pattern.replace('–', '–').replace('—', '–')
            if normalized_pattern in normalized_line or pattern in line:
                if current_table:
                    tables.append(current_table)
                current_table = {
                    "table_name": pattern,
                    "table_id": table_id,
                    "scope": "single_patient" if "Single Patient" in pattern else "practice",
                    "fields": []
                }
                break
        
        # Check for field lines (field name followed by data type)
        if current_table and line:
            # Match patterns like "Field Name    nvarchar(256)" or "Field Name*    nvarchar(256)"
            # Also match "n/a", "bit", "int", "date", "datetime", "float"
            field_match = re.match(
                r'^(.+?)\s{2,}(nvarchar\(.+?\)|nchar\(.+?\)|varchar\(.+?\)|int|date|datetime|float|bit|n/a|9 digits.*|2 digits.*|derived field|constant string|Date)(.*)$',
                line, re.IGNORECASE
            )
            if field_match:
                field_name = field_match.group(1).strip()
                data_type_raw = field_match.group(2).strip()
                extra = field_match.group(3).strip()
                
                # Skip header rows
                if field_name in ("Data Field", "Data Type"):
                    i += 1
                    continue
                
                required = '*' in field_name
                field_name = field_name.rstrip('*').strip()
                
                # Parse notes like "- multiple records" or ", 'mm/dd/yyyy'"
                notes = None
                multi_valued = False
                if extra:
                    notes = extra.lstrip(' -,').strip()
                    if 'multiple records' in extra.lower():
                        multi_valued = True
                
                # Also check data_type for format hints
                format_hint = None
                if "'mm/dd/yyyy'" in (data_type_raw + (extra or '')):
                    format_hint = "mm/dd/yyyy"
                
                # Separate any secondary type info
                data_type = data_type_raw
                if data_type.startswith('9 digits'):
                    data_type = "char(9)"
                    notes = "hardcoded for now" if not notes else notes
                elif data_type.startswith('2 digits'):
                    data_type = "char(2)"
                    notes = "derived from care type" if not notes else notes
                
                field = {
                    "name": field_name,
                    "data_type": data_type,
                    "required": required,
                }
                if multi_valued:
                    field["multi_valued"] = True
                if notes:
                    field["notes"] = notes
                if format_hint:
                    field["format_hint"] = format_hint
                
                current_table["fields"].append(field)
        
        i += 1
    
    if current_table:
        tables.append(current_table)
    
    return tables

def compute_stats(tables):
    total_fields = sum(len(t["fields"]) for t in tables)
    total_required = sum(sum(1 for f in t["fields"] if f.get("required")) for t in tables)
    total_multi_valued = sum(sum(1 for f in t["fields"] if f.get("multi_valued")) for t in tables)
    fields_with_notes = sum(sum(1 for f in t["fields"] if f.get("notes")) for t in tables)
    
    # No descriptions exist - only names and types
    fields_with_descriptions = 0
    
    return {
        "total_tables": len(tables),
        "total_fields": total_fields,
        "total_required_fields": total_required,
        "total_multi_valued_fields": total_multi_valued,
        "fields_with_notes": fields_with_notes,
        "fields_with_descriptions": fields_with_descriptions,
        "description_coverage_pct": 0.0,
        "tables_summary": [
            {
                "table_name": t["table_name"],
                "table_id": t["table_id"],
                "scope": t["scope"],
                "field_count": len(t["fields"]),
                "required_count": sum(1 for f in t["fields"] if f.get("required")),
                "multi_valued_count": sum(1 for f in t["fields"] if f.get("multi_valued")),
            }
            for t in tables
        ]
    }

def main():
    text = extract_text()
    tables = parse_tables(text)
    stats = compute_stats(tables)
    
    inventory = {
        "source": "Aarista_EHI_Export.pdf",
        "source_description": "Data Dictionary for Aarista EHI Export, created 2023-11-28",
        "parse_method": "pdftotext -layout + regex parsing",
        "tables": tables,
        "statistics": stats
    }
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    with open(STATS_PATH, 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    print(f"Tables found: {stats['total_tables']}")
    print(f"Total fields: {stats['total_fields']}")
    print(f"Required fields: {stats['total_required_fields']}")
    print(f"Multi-valued fields: {stats['total_multi_valued_fields']}")
    print(f"Fields with descriptions: {stats['fields_with_descriptions']} (0%)")
    print()
    for ts in stats['tables_summary']:
        print(f"  {ts['table_name']}: {ts['field_count']} fields ({ts['required_count']} required)")

if __name__ == "__main__":
    main()
