#!/usr/bin/env python3
"""Final cleanup of entity-inventory-full.json: remove duplicate/false fields from PDF wrapping artifacts."""

import json, os

DIR = os.path.dirname(__file__)
with open(os.path.join(DIR, "entity-inventory-full.json")) as f:
    data = json.load(f)

# Fix charges table - remove false fields from line wrapping
for table in data["tables"]:
    if table["name"] == "charges":
        # Known correct fields for charges (from PDF, 21 real fields):
        correct_fields = [
            {"name": "charges_id", "description": "identifier of this particular log/row in the table", "type": "32 digit GUID (Globally Unique Identifier)"},
            {"name": "scheduleid", "description": "identifier of patient's visit", "type": "32 digit GUID"},
            {"name": "patientid", "description": "identifier of the patient", "type": "32 digit GUID"},
            {"name": "date", "description": "Date of charge", "type": "date as Y-m-d"},
            {"name": "userid", "description": "identifier of user that added the charge", "type": "32 digit GUID"},
            {"name": "charge", "description": "charge code as CPT", "type": "text"},
            {"name": "chargeHeading", "description": "charge heading on superbill", "type": "text"},
            {"name": "chargeDesc", "description": "charge description", "type": "text"},
            {"name": "chargeText", "description": "text associated with charge", "type": "text"},
            {"name": "numUnits", "description": "number of units for charge", "type": "integer"},
            {"name": "fee", "description": "fee associated with charge", "type": "Number"},
            {"name": "verified", "description": "if charge verified", "type": "integer", "value_set": {"0": "no", "1": "yes"}},
            {"name": "caseType", "description": "case type", "type": "text", "value_set": {"New": "New", "Pending": "Pending", "Processed": "Processed"}},
            {"name": "charge_batch_number", "description": "Batch number associated with charge", "type": "integer"},
            {"name": "isExported", "description": "if charge exported", "type": "integer", "value_set": {"0": "not exported", "1": "set to export", "2": "exported"}},
            {"name": "exported_datetime", "description": "Date charge was exported", "type": "timestamp as Y-m-d H:i:s"},
            {"name": "export_error", "description": "Error message associated with export", "type": "text"},
            {"name": "billing_desc", "description": "Billing description of charge", "type": "text"},
            {"name": "sort_order", "description": "Sort order of charge", "type": "integer"},
            {"name": "charge_location_guid", "description": "identifier of location for charge", "type": "32 digit GUID"},
            {"name": "time_last_modified", "description": "Date time item last modified", "type": "timestamp as Y-m-d H:i:s"},
        ]
        table["fields"] = correct_fields
        table["field_count"] = len(correct_fields)

# Fix patient_codes - units type is wrong (says "32 digit GUID", should be text)  
for table in data["tables"]:
    if table["name"] == "patient_codes":
        for field in table["fields"]:
            if field["name"] == "units":
                field["type"] = "text"

# Fix patient_forms_data - remove any false fields  
for table in data["tables"]:
    if table["name"] == "patient_forms_data":
        # Remove empty-name or continuation-artifact fields
        table["fields"] = [f for f in table["fields"] if f["name"] and not f["name"].startswith("array")]
        table["field_count"] = len(table["fields"])

# Fix ptinr_log - remove any continuation artifacts
for table in data["tables"]:
    if table["name"] == "ptinr_log":
        seen = set()
        clean = []
        for f in table["fields"]:
            if f["name"] not in seen:
                seen.add(f["name"])
                clean.append(f)
        table["fields"] = clean
        table["field_count"] = len(clean)

# Fix patient_advforms - remove duplicates
for table in data["tables"]:
    if table["name"] == "patient_advforms":
        seen = set()
        clean = []
        for f in table["fields"]:
            if f["name"] not in seen:
                seen.add(f["name"])
                clean.append(f)
        table["fields"] = clean
        table["field_count"] = len(clean)

# Remove any fields with empty name across all tables
for table in data["tables"]:
    table["fields"] = [f for f in table["fields"] if f.get("name", "").strip()]
    table["field_count"] = len(table["fields"])

# Recount totals
total = sum(t["field_count"] for t in data["tables"])

with open(os.path.join(DIR, "entity-inventory-full.json"), "w") as f:
    json.dump(data, f, indent=2)

# Regenerate summary
summary = {
    "total_tables": len(data["tables"]),
    "total_fields": total,
    "fields_with_descriptions": sum(1 for t in data["tables"] for f in t["fields"] if f.get("description", "").strip()),
    "fields_with_types": sum(1 for t in data["tables"] for f in t["fields"] if f.get("type", "").strip()),
    "fields_with_value_sets": sum(1 for t in data["tables"] for f in t["fields"] if f.get("value_set")),
    "tables_summary": []
}
summary["description_coverage_pct"] = round(summary["fields_with_descriptions"] / total * 100, 1)
summary["type_coverage_pct"] = round(summary["fields_with_types"] / total * 100, 1)

for table in data["tables"]:
    summary["tables_summary"].append({
        "name": table["name"],
        "description": table["description"],
        "field_count": table["field_count"],
        "fields_with_descriptions": sum(1 for f in table["fields"] if f.get("description", "").strip()),
        "fields_with_types": sum(1 for f in table["fields"] if f.get("type", "").strip()),
    })

with open(os.path.join(DIR, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print(f"Tables: {summary['total_tables']}")
print(f"Total fields: {summary['total_fields']}")
print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_coverage_pct']}%)")
print(f"Fields with types: {summary['fields_with_types']} ({summary['type_coverage_pct']}%)")
print(f"Fields with value sets: {summary['fields_with_value_sets']}")
print()
for t in summary["tables_summary"]:
    print(f"  {t['name']}: {t['field_count']} fields, {t['fields_with_descriptions']} described, {t['fields_with_types']} typed")
