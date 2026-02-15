#!/usr/bin/env python3
"""Parse the Aarista EHI Export data dictionary PDF and produce structured inventory.

The PDF contains 7 tables across 8 pages. We extract text with pdftotext -layout
and parse field names + SQL Server data types from each table section.
"""

import json
import re
import subprocess

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/aarista-technology-llc/downloads/Aarista_EHI_Export.pdf"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/aarista-technology-llc--aarista/analysis"

result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
lines = result.stdout.split('\n')

# Table boundaries determined by manual line-by-line inspection of PDF text
table_defs = [
    {"name": "Single Patient - Patient Demographics", "start": 17, "end": 45, "category": "Demographics"},
    {"name": "Single Patient - Patient Addresses", "start": 49, "end": 61, "category": "Demographics"},
    {"name": "Single Patient - Patient Contacts", "start": 66, "end": 86, "category": "Demographics"},
    {"name": "Single Patient - Patient Insurances", "start": 89, "end": 113, "category": "Insurance"},
    {"name": "Single Patient - Patient Encounters – Clinical and Billing", "start": 116, "end": 176, "category": "Clinical & Billing"},
    {"name": "Practice Patients - Patient Demographics and Billing Encounters", "start": 183, "end": 199, "category": "Practice Billing"},
    {"name": "Practice Patients - Patient Demographics and Clinical Encounters", "start": 202, "end": 227, "category": "Practice Clinical"},
]

def parse_field_line(line):
    line = line.strip()
    if not line or 'Data Field' in line or 'Data Type' in line:
        return None
    m = re.match(r'(.+?)\s{2,}(.+)$', line)
    if m:
        name = m.group(1).strip()
        dtype = m.group(2).strip()
        return {
            "name": name.rstrip('*').strip(),
            "name_raw": name,
            "type": dtype,
            "required": '*' in name,
            "has_description": False,
            "multiple_records": 'multiple records' in dtype.lower()
        }
    return None

tables = []
for tdef in table_defs:
    fields = []
    for i in range(tdef["start"] - 1, min(tdef["end"], len(lines))):
        field = parse_field_line(lines[i])
        if field:
            fields.append(field)
    tables.append({
        "name": tdef["name"],
        "category": tdef["category"],
        "field_count": len(fields),
        "required_count": sum(1 for f in fields if f["required"]),
        "multiple_record_fields": sum(1 for f in fields if f["multiple_records"]),
        "fields": fields
    })

total_fields = sum(t["field_count"] for t in tables)
total_required = sum(t["required_count"] for t in tables)
total_multiple = sum(t["multiple_record_fields"] for t in tables)

summary = {
    "total_tables": len(tables),
    "total_fields": total_fields,
    "total_required_fields": total_required,
    "total_multiple_record_fields": total_multiple,
    "fields_with_descriptions": 0,
    "description_percentage": 0.0,
    "tables": tables
}

with open(f"{OUTPUT_DIR}/full-entity-inventory.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== Aarista EHI Export Data Dictionary Summary ===")
print(f"Total tables: {len(tables)}")
print(f"Total fields: {total_fields}")
print(f"Required fields: {total_required}")
print(f"Fields with descriptions: 0 (0%)")
print(f"Fields with 'multiple records' notation: {total_multiple}")
print()
print(f"{'Table Name':<65} {'Fields':>6} {'Req':>4} {'Category'}")
print("-" * 100)
for t in tables:
    print(f"{t['name']:<65} {t['field_count']:>6} {t['required_count']:>4} {t['category']}")
print()
print("=== Typos Found ===")
for orig, corrected in [("Mother Mainder Name","Mother Maiden Name"),("Ethnithity","Ethnicity"),
    ("Chief Comlaint","Chief Complaint"),("Historhy of Present Illness","History of Present Illness"),("L:abs","Labs")]:
    print(f"  '{orig}' -> '{corrected}'")
print()
for t in tables:
    print(f"\n--- {t['name']} ({t['field_count']} fields) ---")
    for f in t["fields"]:
        req = "*" if f["required"] else " "
        multi = " [MULTI]" if f["multiple_records"] else ""
        print(f"  {req} {f['name_raw']:<45} {f['type']}{multi}")
