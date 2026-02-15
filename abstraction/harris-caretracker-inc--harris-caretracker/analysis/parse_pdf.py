#!/usr/bin/env python3
"""Parse the CareTracker EHI Export PDF text to extract data classes and field counts."""

import json
import re

with open("pdf-text.txt", "r") as f:
    text = f.read()

# Remove page headers/footers
text = re.sub(r'CareTracker EHI Export: Folder Organization and Data Format Specification – v1\.0\n', '', text)
text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

# Find all data class entries - they start with a capitalized name followed by fields
# The data classes section starts after "Below is a listing..."
start = text.find("Below is a listing")
header_line = text.find("Data Class Name", start)
data_section = text[text.find("\n", header_line):]

# Parse data classes by finding lines that start with a class name
# A data class line starts with 1-2 spaces and a capitalized word, followed by fields
lines = data_section.split('\n')

data_classes = []
current_class = None
current_fields_text = ""

for line in lines:
    # Check if this is a new data class line (starts with space + capitalized word, has fields after)
    match = re.match(r'^\s{1,2}([A-Z][A-Za-z\s/]+?)\s{2,}(Pat\w+|Last\w+|Description|PatientID|Patientid|PatientId|PatId)\b', line)
    if match:
        # Save previous class
        if current_class:
            fields = [f.strip() for f in re.split(r',\s*', current_fields_text.strip()) if f.strip()]
            data_classes.append({"name": current_class, "fields": fields, "field_count": len(fields)})
        
        current_class = match.group(1).strip()
        # Fields start from the first field identifier
        field_start = line.find(match.group(2))
        current_fields_text = line[field_start:]
    elif current_class:
        # Continuation line - append to current fields
        stripped = line.strip()
        if stripped and not stripped.startswith('Data Class'):
            current_fields_text += ", " + stripped

# Don't forget the last class
if current_class:
    fields = [f.strip() for f in re.split(r',\s*', current_fields_text.strip()) if f.strip()]
    data_classes.append({"name": current_class, "fields": fields, "field_count": len(fields)})

# Clean up field names (remove trailing commas, empty strings)
for dc in data_classes:
    dc["fields"] = [f.rstrip(',').strip() for f in dc["fields"] if f.rstrip(',').strip()]
    dc["field_count"] = len(dc["fields"])

# Fix known multi-line name issues from PDF layout
# 1. First "Allergies and Intolerances" should be "Allergies and Intolerances Pending"
#    and field 7 "Pending ... AddedByFirstName" should be split
for dc in data_classes:
    if dc["name"] == "Allergies and Intolerances" and "PendingFlag" in dc["fields"]:
        dc["name"] = "Allergies and Intolerances Pending"
        # Fix the merged field
        dc["fields"] = [f.split()[-1] if "Pending" in f and "AddedBy" in f else f for f in dc["fields"]]
        dc["field_count"] = len(dc["fields"])
    
    # 2. "Occupation and Industry" should be "Occupation and Industry History"
    if dc["name"] == "Occupation and Industry":
        dc["name"] = "Occupation and Industry History"
        dc["fields"] = [f.split()[-1] if "History" in f and "Census" in f else f for f in dc["fields"]]
        dc["field_count"] = len(dc["fields"])
    
    # 3. "Patient Health Information" should be "Patient Health Information Capture"
    if dc["name"] == "Patient Health Information":
        dc["name"] = "Patient Health Information Capture"
        dc["fields"] = [f.split()[-1] if "Capture" in f and "Directive" in f else f for f in dc["fields"]]
        dc["field_count"] = len(dc["fields"])

# Print summary
total_fields = sum(dc["field_count"] for dc in data_classes)
print(f"Total data classes: {len(data_classes)}")
print(f"Total fields: {total_fields}")
print()

# Print table
print(f"{'Data Class':<35} {'Fields':>6}")
print("-" * 45)
for dc in data_classes:
    print(f"{dc['name']:<35} {dc['field_count']:>6}")
print("-" * 45)
print(f"{'TOTAL':<35} {total_fields:>6}")

# Save full inventory as JSON
with open("full-entity-inventory.json", "w") as f:
    json.dump({
        "summary": {
            "total_data_classes": len(data_classes),
            "total_fields": total_fields,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
        },
        "data_classes": data_classes
    }, f, indent=2)
print(f"\nSaved full inventory to full-entity-inventory.json")
