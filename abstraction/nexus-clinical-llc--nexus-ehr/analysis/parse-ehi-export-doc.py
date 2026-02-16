#!/usr/bin/env python3
"""Parse the EHI Export Documentation PDF and extract structured export components.

The PDF describes 5 export components for both individual and population exports.
Since there's no data dictionary, we extract the described export structure.
"""
import json
import subprocess
import re

pdf_path = "../downloads/EHI-Export-Documentation.pdf"

# Extract text
result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
text = result.stdout

# Define the export components as described in the PDF
export_components = [
    {
        "id": "clinical_data_ccda",
        "name": "Clinical Data (C-CDA)",
        "format": "C-CDA R2.1",
        "standard_reference": "https://www.hl7.org/ccdasearch/",
        "compliance": "USCDI V1",
        "description": "Clinical data exported in C-CDA R2.1 format, compliant with USCDI V1.",
        "individual_export": True,
        "population_export": True,
        "population_note": "C-CDA files exported for each patient in the population",
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    },
    {
        "id": "billing_claims",
        "name": "Patient Billing - Claims",
        "format": "CSV",
        "description": "Claims data exported as CSV file.",
        "individual_export": True,
        "population_export": True,
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    },
    {
        "id": "billing_insurance_payments",
        "name": "Patient Billing - Insurance Payment Details",
        "format": "CSV",
        "description": "Insurance payment details exported as CSV file.",
        "individual_export": True,
        "population_export": True,
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    },
    {
        "id": "billing_patient_payments",
        "name": "Patient Billing - Patient Payment Details",
        "format": "CSV",
        "description": "Patient payment details exported as CSV file.",
        "individual_export": True,
        "population_export": True,
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    },
    {
        "id": "documents",
        "name": "Patient Documents",
        "format": "Native (PDF, DOC, HTML, JPG, etc.)",
        "description": "Documents exported in original format.",
        "individual_export": True,
        "population_export": False,
        "population_note": "Population export provides document index CSV with document ID, patient ID, classification, name, created date. Separate utility program exports actual documents.",
        "document_types": [
            "Chart Notes (PDF)",
            "Scanned Documents (PDF)",
            "Imported Faxes (PDF)",
            "Software-generated Documents and Forms (PDF)",
            "PE Images (image format)",
            "Other imported documents (original format)"
        ],
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    },
    {
        "id": "future_appointments",
        "name": "Future Appointments",
        "format": "CSV",
        "description": "Appointments scheduled for future dates exported in CSV format.",
        "individual_export": True,
        "population_export": True,
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    },
    {
        "id": "demographics_insurance",
        "name": "Patient Demographics and Insurance",
        "format": "CSV",
        "description": "Contact details, address, emergency contact, primary/secondary insurance, and responsible party information in CSV format.",
        "individual_export": True,
        "population_export": True,
        "fields_documented": False,
        "field_count": None,
        "data_dictionary": False
    }
]

# Build entity inventory - since there's no data dictionary, we create
# entities from the described components with inferred fields
entities = []

# C-CDA USCDI V1 sections (standard C-CDA R2.1 sections per USCDI V1)
ccda_sections = [
    "Patient Demographics", "Problems", "Medications", "Medication Allergies",
    "Laboratory Tests/Values/Results", "Vital Signs", "Procedures",
    "Care Team Members", "Immunizations", "Unique Device Identifiers",
    "Assessment and Plan of Treatment", "Goals", "Health Concerns",
    "Smoking Status", "Clinical Notes"
]

entities.append({
    "entity_name": "Clinical Data (C-CDA R2.1)",
    "format": "C-CDA R2.1",
    "category": "Clinical",
    "sections": ccda_sections,
    "section_count": len(ccda_sections),
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "note": "No field-level documentation provided. C-CDA R2.1 structure implied by USCDI V1 compliance claim."
})

# CSV components - no fields documented
csv_components = [
    {"name": "Claims", "category": "Billing"},
    {"name": "Insurance Payment Details", "category": "Billing"},
    {"name": "Patient Payment Details", "category": "Billing"},
    {"name": "Patient Demographics and Insurance", "category": "Demographics"},
    {"name": "Future Appointments", "category": "Administrative"},
]

for comp in csv_components:
    entities.append({
        "entity_name": comp["name"],
        "format": "CSV",
        "category": comp["category"],
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "note": "No field-level documentation provided. CSV column names and structure undocumented."
    })

# Document export
entities.append({
    "entity_name": "Patient Documents",
    "format": "Native files (PDF, DOC, HTML, JPG, etc.)",
    "category": "Documents",
    "document_types": [
        "Chart Notes (PDF)",
        "Scanned Documents (PDF)",
        "Imported Faxes (PDF)",
        "Software-generated Documents and Forms (PDF)",
        "PE Images (image format)",
        "Other imported documents (original format)"
    ],
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "note": "Documents exported as-is in native format. Population export includes document index CSV."
})

# Summary
summary = {
    "vendor": "Nexus Clinical LLC",
    "product": "Nexus EHR",
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "total_fields_with_descriptions": 0,
    "total_fields_with_types": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "export_formats": ["C-CDA R2.1", "CSV", "Native document files"],
    "categories": {
        "Clinical": {"entity_count": 1, "field_count": 0, "note": "C-CDA R2.1 with USCDI V1 sections"},
        "Billing": {"entity_count": 3, "field_count": 0, "note": "Claims, insurance payments, patient payments as CSV"},
        "Demographics": {"entity_count": 1, "field_count": 0, "note": "Demographics and insurance as CSV"},
        "Documents": {"entity_count": 1, "field_count": 0, "note": "Native format document files"},
        "Administrative": {"entity_count": 1, "field_count": 0, "note": "Future appointments as CSV"}
    },
    "documentation_quality": {
        "field_level_detail": "none",
        "relationship_documentation": "none",
        "value_set_documentation": "none",
        "sample_data_provided": False,
        "total_documentation_pages": 2
    }
}

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump({"export_components": export_components, "entities": entities}, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== EHI Export Documentation Analysis ===")
print(f"PDF pages: 2")
print(f"Total export components: {len(export_components)}")
print(f"Total entities: {len(entities)}")
print(f"Total documented fields: 0 (no data dictionary)")
print(f"Export formats: C-CDA R2.1, CSV, Native document files")
print(f"\nCategories:")
for cat, info in summary["categories"].items():
    print(f"  {cat}: {info['entity_count']} entities - {info['note']}")
print(f"\nKey observations:")
print(f"  - No data dictionary or field-level documentation exists")
print(f"  - Clinical data uses C-CDA R2.1 (USCDI V1 compliance)")
print(f"  - Billing data exported separately as CSV (beyond C-CDA)")
print(f"  - Documents exported in native format")
print(f"  - Both individual and population export supported")
