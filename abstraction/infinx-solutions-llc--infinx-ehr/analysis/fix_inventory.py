#!/usr/bin/env python3
"""Fix known parsing issues in entity-inventory-full.json and regenerate summary."""

import json
import os

DIR = os.path.dirname(__file__)

with open(os.path.join(DIR, "entity-inventory-full.json")) as f:
    data = json.load(f)

# Fix 1: scheduleid and surgerymemo_id descriptions have type text bleeding in
for table in data["tables"]:
    for field in table["fields"]:
        if field["name"] == "scheduleid" and table["name"] == "schedules":
            field["description"] = "unique identifier of the item"
            field["type"] = "32 digit GUID (Globally Unique Identifier)"
        if field["name"] == "surgerymemo_id":
            field["description"] = "unique identifier of the item"
            field["type"] = "32 digit GUID (Globally Unique Identifier)"

# Fix 2: schedules table - payment_type absorbed payment_type1/2, check_num absorbed check_num1/2
# These are separate fields listed without descriptions in the PDF
for table in data["tables"]:
    if table["name"] == "schedules":
        new_fields = []
        for field in table["fields"]:
            if field["name"] == "payment_type" and "payment_type1" in field.get("description", ""):
                new_fields.append({"name": "payment_type", "description": ""})
                new_fields.append({"name": "payment_type1", "description": ""})
                new_fields.append({"name": "payment_type2", "description": ""})
            elif field["name"] == "check_num" and "check_num1" in field.get("description", ""):
                new_fields.append({"name": "check_num", "description": ""})
                new_fields.append({"name": "check_num1", "description": ""})
                new_fields.append({"name": "check_num2", "description": ""})
            else:
                new_fields.append(field)
        table["fields"] = new_fields
        table["field_count"] = len(new_fields)

# Fix 3: charges table - "charge" field has wrong type "Date as Y-m-d" (should be text/code)
for table in data["tables"]:
    if table["name"] == "charges":
        for field in table["fields"]:
            if field["name"] == "charge" and field.get("type") == "Date as Y-m-d":
                field["type"] = "text (CPT code)"

# Fix 4: patient_codes - "code" field has wrong type "date as Y-m-d" (obvious PDF misparse)
for table in data["tables"]:
    if table["name"] == "patient_codes":
        for field in table["fields"]:
            if field["name"] == "code" and "date" in field.get("type", "").lower():
                field["type"] = "text"

# Fix 5: Clean up description fragments from type text wrapping
for table in data["tables"]:
    for field in table["fields"]:
        desc = field.get("description", "")
        # Remove trailing "Identifier)" fragments
        desc = desc.replace(" Identifier)", "").replace(" Unique", "")
        field["description"] = desc.strip()

# Fix 6: charges has extra fields from continuation parse - remove "charge" duplicates
# and check for the extra field "1=set to export," which got split
for table in data["tables"]:
    if table["name"] == "charges":
        # Remove fields that look like value descriptions
        table["fields"] = [f for f in table["fields"] 
                          if not f["name"].startswith("1=") 
                          and not f["name"].startswith("2=")
                          and not f["name"].startswith("0=")]

# Recount
for table in data["tables"]:
    table["field_count"] = len(table["fields"])

# Write fixed inventory
with open(os.path.join(DIR, "entity-inventory-full.json"), "w") as f:
    json.dump(data, f, indent=2)

# Regenerate summary
total_fields = 0
fields_with_desc = 0
fields_with_type = 0
fields_with_vs = 0

tables_summary = []
for table in data["tables"]:
    tf = len(table["fields"])
    fd = sum(1 for f in table["fields"] if f.get("description", "").strip())
    ft = sum(1 for f in table["fields"] if f.get("type", "").strip())
    fv = sum(1 for f in table["fields"] if f.get("value_set"))
    total_fields += tf
    fields_with_desc += fd
    fields_with_type += ft
    fields_with_vs += fv
    tables_summary.append({
        "name": table["name"],
        "description": table["description"],
        "field_count": tf,
        "fields_with_descriptions": fd,
        "fields_with_types": ft,
    })

summary = {
    "total_tables": len(data["tables"]),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_type,
    "fields_with_value_sets": fields_with_vs,
    "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "type_coverage_pct": round(fields_with_type / total_fields * 100, 1) if total_fields else 0,
    "tables_summary": tables_summary,
}

with open(os.path.join(DIR, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print(f"Tables: {summary['total_tables']}")
print(f"Total fields: {summary['total_fields']}")
print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_coverage_pct']}%)")
print(f"Fields with types: {summary['fields_with_types']} ({summary['type_coverage_pct']}%)")
print(f"Fields with value sets: {summary['fields_with_value_sets']}")
print()
for t in tables_summary:
    print(f"  {t['name']}: {t['field_count']} fields, {t['fields_with_descriptions']} described, {t['fields_with_types']} typed")
