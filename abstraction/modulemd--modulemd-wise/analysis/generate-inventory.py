#!/usr/bin/env python3
"""
Generate entity-inventory-full.json and entity-inventory-summary.json.

Since ModuleMD WISE provides NO data dictionary, NO schema, and NO field-level
documentation, the inventory reflects only what can be inferred from the PDF
screenshots: the export produces C-CDA ClinicalSummary XML files. We document
the standard C-CDA ClinicalSummary sections as the probable content, clearly
flagged as inferred.
"""

import json

# Standard C-CDA ClinicalSummary sections (CCD template)
# These are the sections typically present in a CCD/ClinicalSummary document.
# We flag all as "inferred" since ModuleMD provides no documentation of which
# sections their C-CDA actually includes.
ccda_sections = [
    {"section": "Allergies and Intolerances", "loinc": "48765-2", "status": "inferred"},
    {"section": "Medications", "loinc": "10160-0", "status": "inferred"},
    {"section": "Problem List", "loinc": "11450-4", "status": "inferred"},
    {"section": "Procedures", "loinc": "47519-4", "status": "inferred"},
    {"section": "Results", "loinc": "30954-2", "status": "inferred"},
    {"section": "Vital Signs", "loinc": "8716-3", "status": "inferred"},
    {"section": "Immunizations", "loinc": "11369-6", "status": "inferred"},
    {"section": "Social History", "loinc": "29762-2", "status": "inferred"},
    {"section": "Plan of Treatment", "loinc": "18776-5", "status": "inferred"},
    {"section": "Goals", "loinc": "61146-7", "status": "inferred"},
    {"section": "Health Concerns", "loinc": "75310-3", "status": "inferred"},
    {"section": "Encounters", "loinc": "46240-8", "status": "inferred"},
    {"section": "Reason for Referral", "loinc": "42349-1", "status": "inferred"},
    {"section": "Family History", "loinc": "10157-6", "status": "inferred"},
    {"section": "Medical Equipment", "loinc": "46264-8", "status": "inferred"},
    {"section": "Functional Status", "loinc": "47420-5", "status": "inferred"},
    {"section": "Mental Status", "loinc": "10190-7", "status": "inferred"},
    {"section": "Assessment", "loinc": "51848-0", "status": "inferred"},
]

entity_inventory_full = {
    "product": "ModuleMD WISE™",
    "version": "10.0",
    "export_format": "C-CDA XML (ClinicalSummary)",
    "data_dictionary_provided": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "inventory_source": "Inferred from C-CDA ClinicalSummary standard; NO vendor-specific documentation available",
    "confidence": "low — no vendor documentation confirms which sections or fields are included",
    "entities": [
        {
            "name": "C-CDA ClinicalSummary Document",
            "description": "A single C-CDA XML document per patient containing standard clinical summary sections",
            "format": "XML (C-CDA 2.1 assumed)",
            "fields_documented": 0,
            "fields_inferred": len(ccda_sections),
            "vendor_category": "N/A — no vendor categorization provided",
            "sections": ccda_sections,
        }
    ],
    "totals": {
        "entities_documented": 0,
        "entities_inferred": 1,
        "fields_documented": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "sections_inferred": len(ccda_sections),
    },
}

entity_inventory_summary = {
    "product": "ModuleMD WISE™",
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "pct_fields_with_descriptions": "N/A",
    "data_dictionary_exists": False,
    "export_format": "C-CDA XML (ClinicalSummary)",
    "vendor_categories": [],
    "notes": [
        "No data dictionary provided by vendor",
        "No schema or field-level documentation",
        "No sample data files",
        "Export format is C-CDA ClinicalSummary XML, inferred from file naming in screenshots",
        "Standard C-CDA sections are assumed but unconfirmed",
        "Zero documented entities or fields — all content is inferred from export format",
    ],
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(entity_inventory_full, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(entity_inventory_summary, f, indent=2)

print("=== SUMMARY ===")
print(json.dumps(entity_inventory_summary, indent=2))
