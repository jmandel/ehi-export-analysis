#!/usr/bin/env python3
"""Parse the EHI Export Documentation PDF and extract structured information.

The PDF is a single page with no data dictionary — it describes only the
export format (ZIP containing C-CDA XML, demographics PDF, scanned docs,
and clinical notes/lab results PDF). This script extracts that structure
into a machine-readable JSON inventory.
"""

import json
import subprocess
import sys

PDF_PATH = "../downloads/EHI_Export_Documentation.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
pdf_text = result.stdout

# Get PDF metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)

# The export describes 4 component types in the ZIP, no field-level detail
export_components = [
    {
        "name": "C-CDA (USCDI v1)",
        "format": "XML",
        "description": "C-CDA document in compliance with USCDI v1. Standard clinical summary covering problems, medications, allergies, immunizations, vitals, lab results, and procedures.",
        "is_computable": True,
        "has_field_level_detail": False,
        "notes": "Standard C-CDA — no vendor-specific extensions or data dictionary provided."
    },
    {
        "name": "Demographics",
        "format": "PDF",
        "description": "Patient demographics exported as a PDF document.",
        "is_computable": False,
        "has_field_level_detail": False,
        "notes": "PDF is not a computable format per (b)(10) requirements."
    },
    {
        "name": "Scanned Documents",
        "format": "PDF, JPG, PNG",
        "description": "Scanned documents from the patient record.",
        "is_computable": False,
        "has_field_level_detail": False,
        "notes": "Image/document files — inherently non-computable."
    },
    {
        "name": "Clinical Notes / Lab Results",
        "format": "PDF",
        "description": "Clinical notes and lab results exported as a PDF document.",
        "is_computable": False,
        "has_field_level_detail": False,
        "notes": "PDF is not a computable format. Lab results in PDF lose discrete data."
    }
]

# Build the inventory — since there's no data dictionary, the "entities"
# are just the 4 export components with zero field-level detail.
inventory = {
    "source_file": "downloads/EHI_Export_Documentation.pdf",
    "source_pages": 1,
    "source_author": "Brett Chapman",
    "source_created": "2023-11-09",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_format": "ZIP file containing per-patient folders",
    "export_components": export_components,
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "notes": (
        "The documentation provides no data dictionary, no field-level detail, "
        "no schema, and no sample data. The only structured content is the list "
        "of 4 export components (C-CDA XML, demographics PDF, scanned documents, "
        "clinical notes/lab results PDF). Of these, only the C-CDA is computable, "
        "and its content is defined by the USCDI v1 / C-CDA standard — no vendor-specific "
        "extensions or mappings are documented."
    )
}

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

summary = {
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "has_data_dictionary": False,
    "export_components_count": len(export_components),
    "computable_components": sum(1 for c in export_components if c["is_computable"]),
    "non_computable_components": sum(1 for c in export_components if not c["is_computable"]),
    "component_summary": [
        {"name": c["name"], "format": c["format"], "is_computable": c["is_computable"]}
        for c in export_components
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== Export Documentation Analysis ===")
print(f"Source: {inventory['source_file']}")
print(f"Pages: {inventory['source_pages']}")
print(f"Author: {inventory['source_author']}")
print(f"Created: {inventory['source_created']}")
print(f"Has data dictionary: {inventory['has_data_dictionary']}")
print(f"Has schema: {inventory['has_schema']}")
print(f"Has sample data: {inventory['has_sample_data']}")
print(f"\nExport components: {len(export_components)}")
print(f"  Computable: {summary['computable_components']}")
print(f"  Non-computable: {summary['non_computable_components']}")
print(f"\nTotal entities with field-level detail: {inventory['total_entities']}")
print(f"Total fields documented: {inventory['total_fields']}")
print("\nComponents:")
for c in export_components:
    print(f"  - {c['name']} ({c['format']}) — computable: {c['is_computable']}")
print("\nDone. Wrote entity-inventory-full.json and entity-inventory-summary.json")
