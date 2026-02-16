#!/usr/bin/env python3
"""
Generate full-entity-inventory.json for SequelMed EHR export.

Since SequelMed provides NO data dictionary, NO schema, and NO field-level
documentation, this inventory reflects only what can be inferred from the
export documentation PDF. The export consists of:
  1. A C-CDA XML file (standard clinical summary)
  2. A Documents folder (unstructured files)
  3. A Patient Documents Detail.xls (undocumented)

We document what's known about each component and flag what's missing.
"""

import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# C-CDA sections that would typically be present per USCDI V1 / C-CDA R2.1
# These are standard C-CDA sections — SequelMed claims USCDI V1 compliance
# but provides NO documentation of which sections they actually populate.
STANDARD_CCDA_SECTIONS = [
    {"section": "Patient Demographics", "loinc": "N/A", "note": "Header-level: name, DOB, gender, race, ethnicity, address, phone, language"},
    {"section": "Allergies and Intolerances", "loinc": "48765-2", "note": "Standard USCDI V1 element"},
    {"section": "Medications", "loinc": "10160-0", "note": "Standard USCDI V1 element"},
    {"section": "Problems", "loinc": "11450-4", "note": "Standard USCDI V1 element"},
    {"section": "Procedures", "loinc": "47519-4", "note": "Standard USCDI V1 element"},
    {"section": "Results (Labs)", "loinc": "30954-2", "note": "Standard USCDI V1 element"},
    {"section": "Vital Signs", "loinc": "8716-3", "note": "Standard USCDI V1 element"},
    {"section": "Immunizations", "loinc": "11369-6", "note": "Standard USCDI V1 element"},
    {"section": "Plan of Treatment", "loinc": "18776-5", "note": "Common C-CDA section"},
    {"section": "Goals", "loinc": "61146-7", "note": "USCDI V1 element"},
    {"section": "Health Concerns", "loinc": "75310-3", "note": "USCDI V1 element"},
    {"section": "Assessment and Plan", "loinc": "51847-2", "note": "Common C-CDA section"},
    {"section": "Encounter Diagnoses", "loinc": "29308-4", "note": "Common C-CDA section"},
    {"section": "Social History (Smoking Status)", "loinc": "29762-2", "note": "USCDI V1 element"},
    {"section": "Functional Status", "loinc": "47420-5", "note": "Optional C-CDA section"},
    {"section": "Mental Status", "loinc": "10190-7", "note": "Optional C-CDA section"},
    {"section": "Reason for Referral", "loinc": "42349-1", "note": "Optional C-CDA section"},
]

inventory = {
    "vendor": "Sequel Systems, Inc.",
    "product": "SequelMed EHR V12",
    "export_documentation_version": "1.0",
    "inventory_generated": "2026-02-16",
    "source_artifact": "SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf",
    "data_dictionary_available": False,
    "schema_available": False,
    "sample_data_available": False,
    "notes": [
        "SequelMed provides NO data dictionary, NO field-level documentation, and NO schema.",
        "This inventory represents what can be INFERRED from the 4-page PDF documentation.",
        "The export is a C-CDA XML + unstructured documents — no native database tables are exported.",
        "C-CDA sections listed below are standard sections that SHOULD be present per USCDI V1 compliance claim, but SequelMed does not document which sections they actually include.",
        "No vendor-specific fields, extensions, or custom data elements are documented."
    ],
    "export_components": [
        {
            "component": "C-CDA XML File",
            "location": "Clinical folder",
            "format": "XML (C-CDA R2.1)",
            "standard": "HL7 C-CDA R2.1, USCDI V1",
            "vendor_documented_fields": 0,
            "vendor_documented_entities": 0,
            "inferred_sections": STANDARD_CCDA_SECTIONS,
            "inferred_section_count": len(STANDARD_CCDA_SECTIONS),
            "documentation_quality": "Zero vendor-specific documentation. Only references to external HL7 specs."
        },
        {
            "component": "Patient Documents",
            "location": "Documents folder",
            "format": "Mixed (.jpg, .gif, .bmp, .png, .pdf, .txt)",
            "document_types_listed": [
                "Signed progress notes",
                "Available lab results",
                "Radiology reports",
                "Scanned documents",
                "Imported documents",
                "Uploaded documents"
            ],
            "vendor_documented_fields": 0,
            "documentation_quality": "Document types listed but no metadata schema, no naming convention, no structure documented."
        },
        {
            "component": "Patient Documents Detail.xls",
            "location": "Root of ZIP",
            "format": "XLS (Excel)",
            "vendor_documented_fields": 0,
            "documentation_quality": "Mentioned by name only. No description of columns, rows, or purpose."
        }
    ],
    "summary_statistics": {
        "total_vendor_documented_entities": 0,
        "total_vendor_documented_fields": 0,
        "total_fields_with_descriptions": 0,
        "total_fields_with_types": 0,
        "total_inferred_ccda_sections": len(STANDARD_CCDA_SECTIONS),
        "export_components": 3,
        "documentation_pages": 4,
        "substantive_content_pages": 1.5
    }
}

output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Full entity inventory saved to {output_path}")
print(f"Vendor-documented entities: {inventory['summary_statistics']['total_vendor_documented_entities']}")
print(f"Vendor-documented fields: {inventory['summary_statistics']['total_vendor_documented_fields']}")
print(f"Inferred C-CDA sections: {inventory['summary_statistics']['total_inferred_ccda_sections']}")
print(f"Export components: {inventory['summary_statistics']['export_components']}")
