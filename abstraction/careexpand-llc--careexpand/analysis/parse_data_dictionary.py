#!/usr/bin/env python3
"""
Parse the Careexpand EHI export data dictionary from the data-dictionary-table.png image.
The image contains a table with 17 fields. Since the data dictionary is an image (not structured data),
we transcribe it manually based on visual inspection.

Source: downloads/data-dictionary-table.png
"""

import json

# Transcribed from the data-dictionary-table.png image
fields = [
    {"field": "patient_name", "description": "Full name of the patient", "data_type": "String", "required": True},
    {"field": "dob", "description": "Date of birth of the patient", "data_type": "Date (YYYY-MM-DD)", "required": True},
    {"field": "gender", "description": "Patient's gender", "data_type": "String (M/F/Other)", "required": True},
    {"field": "race", "description": "Race of the patient", "data_type": "String", "required": False},
    {"field": "ethnicity", "description": "Ethnicity of the patient", "data_type": "String", "required": False},
    {"field": "language", "description": "Preferred language of communication", "data_type": "String", "required": False},
    {"field": "address", "description": "Patient's home address", "data_type": "String", "required": False},
    {"field": "phone", "description": "Contact number", "data_type": "String", "required": False},
    {"field": "emergency_contact", "description": "Emergency contact name and phone", "data_type": "String", "required": False},
    {"field": "smoking_status", "description": "Patient's smoking habits", "data_type": "String", "required": False},
    {"field": "problem_list", "description": "List of active and past medical problems", "data_type": "Array (Structured)", "required": True},
    {"field": "medications", "description": "Active and past medications", "data_type": "Array (Structured)", "required": True},
    {"field": "allergies", "description": "Patient allergies", "data_type": "Array (Structured)", "required": False},
    {"field": "lab_results", "description": "Laboratory test results", "data_type": "Array (Structured)", "required": False},
    {"field": "procedures", "description": "Medical procedures performed", "data_type": "Array (Structured)", "required": False},
    {"field": "encounters", "description": "Clinical encounters and visits", "data_type": "Array (Structured)", "required": False},
    {"field": "vital_signs", "description": "Blood pressure, heart rate, temperature, etc.", "data_type": "Array (Structured)", "required": False},
]

# Build entity inventory
entity_inventory = {
    "source": "downloads/data-dictionary-table.png (image transcription) and downloads/b10-ehi-export-ccda.md",
    "export_format": "C-CDA 2.1 XML",
    "api_endpoint": "POST /patient/:idPatient/getPatientCCDAData",
    "authentication": "JWT Bearer Token",
    "entities": [
        {
            "name": "C-CDA Patient Export",
            "description": "Single C-CDA 2.1 XML document containing all patient EHI data",
            "category": "Clinical (C-CDA)",
            "fields": fields
        }
    ],
    "summary": {
        "total_entities": 1,
        "total_fields": len(fields),
        "fields_with_descriptions": sum(1 for f in fields if f.get("description")),
        "fields_with_types": sum(1 for f in fields if f.get("data_type")),
        "fields_required": sum(1 for f in fields if f.get("required")),
        "fields_optional": sum(1 for f in fields if not f.get("required")),
        "demographic_fields": sum(1 for f in fields if f["data_type"] == "String" or "Date" in f["data_type"]),
        "clinical_fields": sum(1 for f in fields if "Array" in f["data_type"]),
    }
}

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(entity_inventory, f, indent=2)

# Write summary
summary = {
    "product": "Careexpand",
    "export_format": "C-CDA 2.1 XML",
    "total_entities": 1,
    "total_fields": len(fields),
    "fields_with_descriptions": entity_inventory["summary"]["fields_with_descriptions"],
    "pct_fields_with_descriptions": round(100 * entity_inventory["summary"]["fields_with_descriptions"] / len(fields), 1),
    "fields_with_types": entity_inventory["summary"]["fields_with_types"],
    "pct_fields_with_types": round(100 * entity_inventory["summary"]["fields_with_types"] / len(fields), 1),
    "demographic_fields": entity_inventory["summary"]["demographic_fields"],
    "clinical_fields": entity_inventory["summary"]["clinical_fields"],
    "domains_covered": [
        "Demographics (10 fields)",
        "Problems/Conditions (1 field: problem_list)",
        "Medications (1 field: medications)",
        "Allergies (1 field: allergies)",
        "Lab Results (1 field: lab_results)",
        "Procedures (1 field: procedures)",
        "Encounters (1 field: encounters)",
        "Vital Signs (1 field: vital_signs)",
    ],
    "domains_missing_vs_product_capabilities": [
        "Billing / claims / charges",
        "Insurance / coverage details",
        "Care plans / goals",
        "Orders / referrals",
        "Clinical notes / documents",
        "Immunizations",
        "Patient communications / portal messages",
        "Telemedicine session records",
        "Remote patient monitoring data",
        "E-prescribing details",
        "Scheduling / appointments (if used for care decisions)",
    ],
    "note": "The data dictionary is provided as a PNG image, not as structured/machine-readable data. "
            "The 17 fields map directly to standard C-CDA sections. No vendor-specific extensions, "
            "custom forms, or non-USCDI data domains are documented."
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total fields: {len(fields)}")
print(f"Fields with descriptions: {entity_inventory['summary']['fields_with_descriptions']}/{len(fields)} ({summary['pct_fields_with_descriptions']}%)")
print(f"Fields with types: {entity_inventory['summary']['fields_with_types']}/{len(fields)} ({summary['pct_fields_with_types']}%)")
print(f"Required fields: {entity_inventory['summary']['fields_required']}")
print(f"Optional fields: {entity_inventory['summary']['fields_optional']}")
print(f"Demographic fields: {entity_inventory['summary']['demographic_fields']}")
print(f"Clinical (array) fields: {entity_inventory['summary']['clinical_fields']}")
print(f"\nDomains covered: {len(summary['domains_covered'])}")
print(f"Domains missing (relative to product): {len(summary['domains_missing_vs_product_capabilities'])}")
