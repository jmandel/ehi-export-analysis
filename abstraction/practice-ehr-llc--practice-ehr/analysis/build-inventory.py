#!/usr/bin/env python3
"""Build entity inventory from the Practice EHR export documentation.

Since Practice EHR provides NO data dictionary, NO schema, and NO field-level
documentation, the inventory reflects only what can be inferred from the
C-CDA standard reference and the document folder description in the PDF.
"""

import json

# The export has no vendor-specific data dictionary. We can only document
# what the C-CDA standard provides and what the documents folder contains.

entities = [
    {
        "entity": "C-CDA XML Document",
        "category": "Clinical",
        "source": "Clinical folder in ZIP",
        "format": "C-CDA XML (R2.1)",
        "fields": None,  # No field-level documentation provided
        "fields_with_descriptions": None,
        "notes": "Standard C-CDA per USCDI v1. No vendor-specific sections, templates, or extensions documented. Covers: demographics, problems, medications, allergies, labs, vitals, procedures, immunizations, care team, goals, health concerns, smoking status, assessment/plan.",
        "standard_sections_expected": [
            "Demographics (recordTarget)",
            "Problems (Problem Section)",
            "Medications (Medications Section)",
            "Allergies (Allergies and Intolerances Section)",
            "Lab Results (Results Section)",
            "Vital Signs (Vital Signs Section)",
            "Procedures (Procedures Section)",
            "Immunizations (Immunizations Section)",
            "Care Team (Care Team Section)",
            "Goals (Goals Section)",
            "Health Concerns (Health Concerns Section)",
            "Social History / Smoking Status",
            "Assessment and Plan"
        ]
    },
    {
        "entity": "Patient Documents (folder)",
        "category": "Documents",
        "source": "Documents folder in ZIP",
        "format": "Mixed (.jpg, .gif, .bmp, .png, .pdf, .txt)",
        "fields": None,
        "fields_with_descriptions": None,
        "notes": "Unstructured document dump. Includes: signed progress notes, lab results, radiology reports, scanned documents, imported documents, uploaded documents. No metadata beyond filename.",
        "document_types": [
            "Signed progress notes",
            "Available lab results",
            "Radiology reports",
            "Scanned documents",
            "Imported documents",
            "Uploaded documents"
        ]
    },
    {
        "entity": "Patient Documents Detail.xls",
        "category": "Index",
        "source": "Root of ZIP",
        "format": "XLS",
        "fields": None,
        "fields_with_descriptions": None,
        "notes": "Index file for the documents folder. Structure and columns are NOT documented in the PDF. Unknown what fields it contains."
    }
]

# Summary
summary = {
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "total_fields_with_descriptions": 0,
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_format": "C-CDA XML + document files + XLS index in ZIP",
    "categories": {
        "Clinical": {"entities": 1, "fields": "Not documented (C-CDA standard)"},
        "Documents": {"entities": 1, "fields": "Not documented (unstructured files)"},
        "Index": {"entities": 1, "fields": "Not documented"}
    },
    "notes": "Practice EHR provides NO field-level documentation, NO data dictionary, and NO schema. The export is a C-CDA (standard clinical summary) plus a folder of document files. No billing, scheduling, or administrative data is documented."
}

with open("entity-inventory-full.json", "w") as f:
    json.dump({"entities": entities, "summary": summary}, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
