#!/usr/bin/env python3
"""Parse the Aarista EHI Export Data Dictionary PDF and produce structured inventory."""

import json
import subprocess
import re

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/aarista-technology-llc/downloads/Aarista_EHI_Export.pdf"

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Split into lines
lines = text.split('\n')

# Parse tables by identifying headers and field rows
tables = []
current_table = None

for line in lines:
    stripped = line.strip()
    
    # Detect table headers (lines like "Single Patient - Patient Demographics")
    if re.match(r'^(Single Patient|Practice Patients)\s*-\s*', stripped):
        if current_table:
            tables.append(current_table)
        current_table = {
            "name": stripped,
            "fields": [],
            "has_descriptions": False,
            "has_types": True,
        }
        continue
    
    if current_table is None:
        continue
    
    # Skip header rows and empty lines
    if stripped in ("", "Data Field", "Data Type") or stripped.startswith("Data Field"):
        continue
    if stripped.startswith("EHI Export") or stripped.startswith("The Electronic"):
        continue
    
    # Match field lines: field name followed by data type
    # Types: nvarchar, nchar, int, date, datetime, float, bit, varchar, derived, constant, n/a
    field_match = re.match(
        r'^(.+?)\s{2,}(nvarchar\(.+?\)|nchar\(.+?\)|int|date(?:time)?|float|bit|varchar\(.+?\)|derived\s+field|constant\s+string|n/a|9\s+digits.*|2\s+digits.*)',
        stripped,
        re.IGNORECASE
    )
    
    if field_match:
        field_name = field_match.group(1).strip().rstrip('*')
        is_required = '*' in field_match.group(1)
        data_type = field_match.group(2).strip()
        
        # Check for "multiple records" annotation
        multi = "multiple records" in stripped.lower()
        
        current_table["fields"].append({
            "name": field_name,
            "type": data_type,
            "required": is_required,
            "multiple_records": multi,
        })

if current_table:
    tables.append(current_table)

# Categorize tables
categories = {
    "Single Patient - Patient Demographics": "Demographics",
    "Single Patient - Patient Addresses": "Demographics",
    "Single Patient - Patient Contacts": "Demographics",
    "Single Patient - Patient Insurances": "Insurance",
    "Single Patient - Patient Encounters – Clinical and Billing": "Clinical & Billing",
    "Practice Patients - Patient Demographics and Billing Encounters": "Billing",
    "Practice Patients - Patient Demographics and Clinical Encounters": "Clinical",
}

# Build summary
total_fields = 0
for t in tables:
    t["field_count"] = len(t["fields"])
    t["category"] = categories.get(t["name"], "Unknown")
    total_fields += t["field_count"]

summary = {
    "total_tables": len(tables),
    "total_fields": total_fields,
    "fields_with_descriptions": 0,  # None have descriptions beyond field names
    "fields_with_types": total_fields,  # All have SQL types
    "description_percentage": 0.0,
    "tables": []
}

for t in tables:
    table_info = {
        "name": t["name"],
        "category": t["category"],
        "field_count": t["field_count"],
        "fields_with_descriptions": 0,
        "has_types": True,
        "fields": t["fields"]
    }
    summary["tables"].append(table_info)

# Output
output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/aarista-technology-llc--aarista/analysis/full-entity-inventory.json"
with open(output_path, 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total tables: {summary['total_tables']}")
print(f"Total fields: {summary['total_fields']}")
print(f"Fields with descriptions: {summary['fields_with_descriptions']} (0%)")
print(f"Fields with types: {summary['fields_with_types']} (100%)")
print()

for t in summary["tables"]:
    multi_count = sum(1 for f in t["fields"] if f.get("multiple_records"))
    required_count = sum(1 for f in t["fields"] if f.get("required"))
    print(f"  {t['name']}")
    print(f"    Category: {t['category']}")
    print(f"    Fields: {t['field_count']}")
    print(f"    Required fields: {required_count}")
    print(f"    Multi-record fields: {multi_count}")
    print()

# Count typos
typos = {
    "Ethnithity": "Ethnicity",
    "Mother Mainder Name": "Mother Maiden Name", 
    "Chief Comlaint": "Chief Complaint",
    "Historhy of Present Illness": "History of Present Illness",
    "L:abs": "Labs",
}
print(f"Typos found: {len(typos)}")
for wrong, right in typos.items():
    print(f"  '{wrong}' → '{right}'")
