#!/usr/bin/env python3
"""
Parse the Amazing Charts EHI Export PDF data dictionary from raw pdftotext output.
Produces entity-inventory-full.json and entity-inventory-summary.json.

Usage: python parse-data-dictionary.py
"""

import json
import re
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(SCRIPT_DIR, "..", "downloads",
                        "Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf")

# Extract text from PDF
raw = subprocess.check_output(["pdftotext", "-layout", PDF_PATH, "-"],
                              text=True)

# All 44 known data class names from the PDF (visual inspection)
KNOWN_NAMES = [
    "Addendum",
    "Advance Directives",
    "Alerts",
    "Allergies and Intolerances Pending",
    "Allergies and Intolerances",
    "Assesments",
    "Billing History",
    "Care Team Members",
    "Clinical Notes",
    "Demographic Immunization",
    "Email",
    "FamilyHistory",
    "FunctionalStatus",
    "Goals",
    "Health Concerns",
    "Health Insurance",
    "HM Rules Ignored",
    "HM Rules",
    "Immunizations",
    "Implantable device",
    "Imported Items",
    "Injections",
    "Lab Tests",
    "List Problem Pending",
    "List Problem",
    "Medications Pending",
    "Medications",
    "Next Of Kin",
    "Occupation and Industry History",
    "Orders",
    "Patient Demographics",
    "Patient Generated Data",
    "Patient Health Information Capture",
    "Patient Record Release",
    "Plan of Treatment",
    "Procedures",
    "Referrals",
    "Risk Factors",
    "Scheduling",
    "Smoking Statuses",
    "Tracked Data",
    "Travel History",
    "User Defined Fields",
    "Vital Signs",
]

# Clean text: remove page headers/footers/numbers
lines = raw.split("\n")
clean = []
header_re = re.compile(r"^Amazing Charts EHI Export:.*v1\.0$")
for line in lines:
    t = line.strip()
    if not t:
        continue
    if header_re.match(t):
        continue
    if re.match(r"^\d+$", t):
        continue
    clean.append(t)

# Find table start - look for "Data Class Name" header line
table_start = None
for i, line in enumerate(clean):
    if line.strip().startswith("Data Class Name"):
        table_start = i + 1
        break

if table_start is None:
    raise ValueError("Could not find 'Data Class Name' header")

# For indentation-based parsing, we need the raw lines (with whitespace)
# Re-find table start in original lines
raw_table_start = None
for i, line in enumerate(lines):
    if line.strip().startswith("Data Class Name") and "Column Headings" in line:
        raw_table_start = i + 1
        break

data_lines_raw = lines[raw_table_start:] if raw_table_start else []

# Sort names longest first to avoid partial matches
sorted_names = sorted(KNOWN_NAMES, key=len, reverse=True)

# The PDF layout has data class names at left margin (indent 0-1) followed by columns.
# Continuation lines (wrapped columns) are indented 25+ chars.
# Some data class names span two lines (e.g., "Allergies and Intolerances" + "Pending",
# "Occupation and Industry" + "History", "Patient Health Information" + "Capture").
# Strategy: use indentation + known name matching to distinguish entries from continuations.

# Multi-line name second parts that appear at low indent
MULTILINE_SECOND_PARTS = {"Pending", "History", "Capture"}

entries = []  # list of {"name": str, "raw_col_text": str}

for line in data_lines_raw:
    if not line.strip():
        continue
    indent = len(line) - len(line.lstrip())
    stripped = line.strip()
    
    # Skip page headers and page numbers
    if header_re.match(stripped) or re.match(r"^\d+$", stripped):
        continue
    
    matched_name = None
    if indent <= 5:
        # Check if this is the second part of a multi-line data class name
        first_word = stripped.split()[0] if stripped.split() else ""
        if entries and first_word in MULTILINE_SECOND_PARTS:
            # Check if combining with previous entry's name gives a known name
            combined = entries[-1]["name"] + " " + first_word
            if combined in KNOWN_NAMES:
                # Update the previous entry's name and add any columns from this line
                entries[-1]["name"] = combined
                rest = stripped[len(first_word):].strip()
                if rest:
                    entries[-1]["raw_col_text"] += " " + rest
                continue
        
        for name in sorted_names:
            if stripped.lower().startswith(name.lower()):
                rest = stripped[len(name):]
                if not rest or rest[0] in (' ', '\t', ','):
                    matched_name = name
                    col_text = rest.strip()
                    break
    
    if matched_name:
        entries.append({"name": matched_name, "raw_col_text": col_text})
    elif entries:
        entries[-1]["raw_col_text"] += " " + stripped

# Now parse columns from raw text
data_classes = []
parse_failures = []

# Categorize each data class
CATEGORIES = {
    "Addendum": "Clinical Notes",
    "Advance Directives": "Care Planning",
    "Alerts": "Communication",
    "Allergies and Intolerances Pending": "Allergies",
    "Allergies and Intolerances": "Allergies",
    "Assesments": "Clinical Notes",
    "Billing History": "Billing",
    "Care Team Members": "Care Planning",
    "Clinical Notes": "Clinical Notes",
    "Demographic Immunization": "Immunizations",
    "Email": "Communication",
    "FamilyHistory": "History",
    "FunctionalStatus": "Care Planning",
    "Goals": "Care Planning",
    "Health Concerns": "Care Planning",
    "Health Insurance": "Insurance",
    "HM Rules Ignored": "Immunizations / Health Maintenance",
    "HM Rules": "Immunizations / Health Maintenance",
    "Immunizations": "Immunizations",
    "Implantable device": "Devices",
    "Imported Items": "Documents",
    "Injections": "Medications",
    "Lab Tests": "Labs",
    "List Problem Pending": "Problems",
    "List Problem": "Problems",
    "Medications Pending": "Medications",
    "Medications": "Medications",
    "Next Of Kin": "Demographics",
    "Occupation and Industry History": "History",
    "Orders": "Orders",
    "Patient Demographics": "Demographics",
    "Patient Generated Data": "Documents",
    "Patient Health Information Capture": "Documents",
    "Patient Record Release": "Administrative",
    "Plan of Treatment": "Clinical Notes",
    "Procedures": "Procedures",
    "Referrals": "Orders",
    "Risk Factors": "History",
    "Scheduling": "Administrative",
    "Smoking Statuses": "History",
    "Tracked Data": "Clinical Data",
    "Travel History": "History",
    "User Defined Fields": "Administrative",
    "Vital Signs": "Vitals",
}

for entry in entries:
    col_text = entry["raw_col_text"].strip()

    if not col_text:
        parse_failures.append({"name": entry["name"], "reason": "No column text found"})
        data_classes.append({
            "name": entry["name"],
            "category": CATEGORIES.get(entry["name"], "Unknown"),
            "fields": [],
            "field_count": 0,
            "parse_error": True,
            "parse_error_reason": "No column text found after name in PDF",
        })
        continue

    cols = [c.strip() for c in col_text.split(",") if c.strip()]
    cols = [re.sub(r"\s+", " ", c) for c in cols]

    fields = []
    for col in cols:
        fields.append({
            "name": col,
            "type": None,
            "description": None,
            "nullable": None,
            "max_length": None,
            "foreign_key": None,
            "value_set": None,
        })

    data_classes.append({
        "name": entry["name"],
        "category": CATEGORIES.get(entry["name"], "Unknown"),
        "fields": fields,
        "field_count": len(fields),
    })

# Compute totals
total_fields = sum(dc["field_count"] for dc in data_classes)
fields_with_desc = sum(
    1 for dc in data_classes for f in dc["fields"] if f.get("description")
)
fields_with_type = sum(
    1 for dc in data_classes for f in dc["fields"] if f.get("type")
)

# Full inventory
full_inventory = {
    "source": "Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf",
    "version": "v1.0",
    "export_formats": ["csv", "json", "xml"],
    "extraction_date": "2026-02-16",
    "total_data_classes": len(data_classes),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_type,
    "expected_data_classes": len(KNOWN_NAMES),
    "parse_failures": parse_failures,
    "data_classes": data_classes,
}

out_full = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
with open(out_full, "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary
category_summary = {}
for dc in data_classes:
    cat = dc["category"]
    if cat not in category_summary:
        category_summary[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
    category_summary[cat]["entity_count"] += 1
    category_summary[cat]["field_count"] += dc["field_count"]
    category_summary[cat]["entities"].append(dc["name"])

# Top entities by field count
top_entities = sorted(data_classes, key=lambda x: x["field_count"], reverse=True)[:15]

summary = {
    "total_data_classes": len(data_classes),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "pct_with_descriptions": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "fields_with_types": fields_with_type,
    "pct_with_types": round(fields_with_type / total_fields * 100, 1) if total_fields else 0,
    "parse_failures": len(parse_failures),
    "categories": category_summary,
    "top_15_entities": [
        {"name": e["name"], "category": e["category"], "field_count": e["field_count"]}
        for e in top_entities
    ],
}

out_summary = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")
with open(out_summary, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Data classes: {len(data_classes)}/{len(KNOWN_NAMES)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['pct_with_descriptions']}%)")
print(f"Fields with types: {fields_with_type} ({summary['pct_with_types']}%)")
print(f"Parse failures: {len(parse_failures)}")
for pf in parse_failures:
    print(f"  {pf['name']}: {pf['reason']}")
print(f"\nOutput: {out_full}")
print(f"Output: {out_summary}")
print(f"\nTop 15 entities by field count:")
for e in top_entities:
    print(f"  {e['name']}: {e['field_count']} fields ({e['category']})")
print(f"\nCategories:")
for cat, info in sorted(category_summary.items()):
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
