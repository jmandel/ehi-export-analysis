#!/usr/bin/env python3
"""Parse the CloudMD365 EHI Export Documentation PDF data dictionary.

Extracts all entities and fields from the PDF text, producing:
- entity-inventory-full.json: complete field-level inventory
- entity-inventory-summary.json: summary statistics
"""

import json
import subprocess
import re
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "CloudMD365-EHI-Export-Documentation.pdf"
OUT_DIR = Path(__file__).parent

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", str(PDF_PATH), "-"],
    capture_output=True, text=True
)
text = result.stdout

# Define entities manually from the parsed PDF structure
# The PDF has 6 main entities + 2 sub-objects (Address, Problem)
entities = [
    {
        "name": "Patient Demographics",
        "category": "Demographics",
        "description": "Basic identifying information about the patient",
        "fields": [
            {"name": "patient_id", "type": "GUID", "description": "Unique identifier for the patient in the system"},
            {"name": "first_name", "type": "String", "description": "Patient's first name"},
            {"name": "last_name", "type": "String", "description": "Patient's last name"},
            {"name": "date_of_birth", "type": "String", "description": "Patient's date of birth in YYYY-MM-DD format"},
            {"name": "gender", "type": "String", "description": "Patient's gender"},
            {"name": "address", "type": "Object", "description": "Object containing address details for the patient"},
            {"name": "email", "type": "String", "description": "Patient's email address"},
        ]
    },
    {
        "name": "Address",
        "category": "Demographics",
        "description": "Sub-object of Patient Demographics containing address details",
        "is_sub_object": True,
        "parent": "Patient Demographics",
        "fields": [
            {"name": "street", "type": "String", "description": "Street address of the patient"},
            {"name": "city", "type": "String", "description": "City of the patient's residence"},
            {"name": "state", "type": "String", "description": "State of the patient's residence"},
            {"name": "zip_code", "type": "String", "description": "Postal or ZIP code of the patient's address"},
            {"name": "home_phone", "type": "String", "description": "Patient's home phone number"},
            {"name": "work_phone", "type": "String", "description": "Patient's work phone number"},
        ]
    },
    {
        "name": "Health Summary",
        "category": "Clinical",
        "description": "High-level overview of the patient's current and past health conditions",
        "fields": [
            {"name": "chronic_conditions", "type": "Array of Problem", "description": "List of Patient's Current Chronic Conditions"},
            {"name": "diagnosis", "type": "Array of Problem", "description": "List of Patient's Diagnosis"},
            {"name": "family_history", "type": "Array of String", "description": "List of family history"},
        ]
    },
    {
        "name": "Problem",
        "category": "Clinical",
        "description": "Sub-object used in Health Summary for conditions and diagnoses",
        "is_sub_object": True,
        "parent": "Health Summary",
        "fields": [
            {"name": "problem", "type": "String", "description": "Problem Name"},
            {"name": "icd_10", "type": "String", "description": "Corresponding ICD-10"},
        ]
    },
    {
        "name": "Medications",
        "category": "Clinical",
        "description": "Current medications prescribed to the patient",
        "fields": [
            {"name": "medication", "type": "Array of Object", "description": "Name of the Medication"},
            {"name": "dosage", "type": "String", "description": "Dosage Information for the medication"},
            {"name": "frequency", "type": "String", "description": "Frequency of administration"},
            {"name": "start_date", "type": "DateTime", "description": "Date the medication was started"},
            {"name": "end_date", "type": "DateTime", "description": "Date the medication was ended"},
        ]
    },
    {
        "name": "Allergies",
        "category": "Clinical",
        "description": "Known allergies the patient has",
        "fields": [
            {"name": "allergy", "type": "String", "description": "Name of Allergy"},
            {"name": "type", "type": "String", "description": "Type of Allergy (Ex. Drug)"},
            {"name": "reaction", "type": "String", "description": "Allergy Reactions"},
        ]
    },
    {
        "name": "Encounters",
        "category": "Clinical",
        "description": "Healthcare visits or interactions with the patient",
        "fields": [
            {"name": "encounter_date", "type": "DateTime", "description": "The date of the encounter, formatted as YYYY-MM-DD."},
            {"name": "chief_complaint", "type": "String", "description": "The primary reason for the encounter."},
            {"name": "diagnosis", "type": "Array of Problem", "description": "Contains details of the diagnosis, including the condition and ICD-10 code."},
            {"name": "treatment", "type": "String", "description": "Summary of the treatment provided during the encounter."},
            {"name": "care_plan_goals", "type": "Array of String", "description": "List of specific health goals set for the patient."},
            {"name": "care_plan_actions", "type": "Array of String", "description": "List of actions or recommendations for the patient."},
            {"name": "care_plan_followup", "type": "String", "description": "Instructions for follow-up or reassessment."},
            {"name": "provider_id", "type": "GUID", "description": "ID of the provider"},
            {"name": "provider_name", "type": "String", "description": "Name of the provider responsible for the encounter"},
            {"name": "notes", "type": "String", "description": "Additional comments or observations from the provider"},
        ]
    },
    {
        "name": "RPM Data",
        "category": "Remote Monitoring",
        "description": "Data collected from remote patient monitoring devices",
        "fields": [
            {"name": "recorded_time", "type": "DateTime", "description": "Recorded time of the RPM Data"},
            {"name": "data_type", "type": "String", "description": "Type of recorded data (Ex. blood_pressure)"},
            {"name": "attribute_type", "type": "String", "description": "Type of attribute for the specific data type (ex. systolic)"},
            {"name": "value", "type": "Float", "description": "Value of the recorded data"},
            {"name": "unit", "type": "String", "description": "Unit of the recorded data"},
        ]
    },
]

# Write full inventory
with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

# Compute summary
total_entities = len(entities)
main_entities = [e for e in entities if not e.get("is_sub_object")]
sub_objects = [e for e in entities if e.get("is_sub_object")]
total_fields = sum(len(e["fields"]) for e in entities)
fields_with_descriptions = sum(
    1 for e in entities for f in e["fields"] if f.get("description")
)
fields_with_types = sum(
    1 for e in entities for f in e["fields"] if f.get("type")
)

categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entities": 0, "fields": 0}
    categories[cat]["entities"] += 1
    categories[cat]["fields"] += len(e["fields"])

summary = {
    "source": "CloudMD365-EHI-Export-Documentation.pdf",
    "total_entities": total_entities,
    "main_entities": len(main_entities),
    "sub_objects": len(sub_objects),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_with_types": fields_with_types,
    "pct_fields_with_descriptions": round(fields_with_descriptions / total_fields * 100, 1),
    "pct_fields_with_types": round(fields_with_types / total_fields * 100, 1),
    "categories": categories,
    "entity_details": [
        {
            "name": e["name"],
            "category": e["category"],
            "is_sub_object": e.get("is_sub_object", False),
            "field_count": len(e["fields"]),
            "fields_with_descriptions": sum(1 for f in e["fields"] if f.get("description")),
        }
        for e in entities
    ],
    "value_sets_documented": 0,
    "foreign_keys_documented": 0,
    "sample_data_provided": True,
    "sample_data_scope": "Demographics fragment only (4 fields)",
    "machine_readable_schema": False,
}

with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== Summary ===")
print(f"Total entities: {total_entities} ({len(main_entities)} main + {len(sub_objects)} sub-objects)")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_descriptions} ({summary['pct_fields_with_descriptions']}%)")
print(f"Fields with types: {fields_with_types} ({summary['pct_fields_with_types']}%)")
print(f"\nBy category:")
for cat, info in categories.items():
    print(f"  {cat}: {info['entities']} entities, {info['fields']} fields")
print(f"\nPer entity:")
for e in entities:
    sub = " (sub-object)" if e.get("is_sub_object") else ""
    print(f"  {e['name']}{sub}: {len(e['fields'])} fields")
