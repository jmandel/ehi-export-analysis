#!/usr/bin/env python3
"""Parse the Simplify EMR EHI export documentation and produce a structured inventory.

The entire EHI export documentation is a single 831-byte text file describing
folder structure. There is no data dictionary, no field definitions, no schema.
The export consists of C-CDA XML + PDF/HTML encounter notes and documents.

This script extracts what structure exists and produces full-entity-inventory.json.
"""

import json
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/genensys-llc--simplify-emr"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/genensys-llc--simplify-emr/analysis"

# Read the raw text
with open(os.path.join(RESULTS_DIR, "downloads/ehi-export-doc.txt")) as f:
    raw_text = f.read()

text_size = len(raw_text)

# Read file sizes
artifacts = []
downloads_dir = os.path.join(RESULTS_DIR, "downloads")
for fname in sorted(os.listdir(downloads_dir)):
    fpath = os.path.join(downloads_dir, fname)
    if os.path.isfile(fpath):
        artifacts.append({
            "filename": fname,
            "size_bytes": os.path.getsize(fpath),
        })

# The export structure as documented
# USCDI v1 C-CDA covers a known set of data classes - enumerate them
uscdi_v1_data_classes = [
    "Patient Demographics/Information",
    "Allergies and Intolerances",
    "Assessment and Plan of Treatment",
    "Care Team Members",
    "Clinical Notes",
    "Goals",
    "Health Concerns",
    "Immunizations",
    "Laboratory (Results/Reports)",
    "Medications",
    "Problems (Conditions/Diagnoses)",
    "Procedures",
    "Provenance",
    "Smoking Status",
    "Unique Device Identifier(s) for Implantable Devices",
    "Vital Signs",
]

# Build the inventory
inventory = {
    "source_file": "downloads/ehi-export-doc.txt",
    "source_size_bytes": text_size,
    "source_format": "plain text (exported from Google Doc)",
    "pdf_pages": 2,
    "pdf_title": "Simplify EMR b(10) Export Format",
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False,
    "export_modes": [
        {
            "name": "All Patient Mode",
            "description": "ZIP file containing one folder per patient in single-patient format",
            "output_format": "ZIP file",
            "naming_convention": "Patient_export_{date}.zip",
        },
        {
            "name": "Single Patient Mode",
            "description": "Folder containing C-CDA XML, encounter notes subfolder, and patient documents subfolder",
            "output_format": "folder",
            "naming_convention": "Lastname_FirstName_patientId_Date",
        },
    ],
    "export_components": [
        {
            "name": "C-CDA XML",
            "type": "standard_document",
            "standard": "USCDI v1 C-CDA",
            "format": "XML",
            "naming_convention": "Lastname_FirstName_ccda.xml",
            "description": "CCDA File Conformant to USCDI v1",
            "reference": "USCDI-Version-1-July-2020-Errata-Final_0.pdf",
            "data_classes_covered": uscdi_v1_data_classes,
            "field_count": "N/A - no vendor-specific field documentation",
            "fields_documented": 0,
        },
        {
            "name": "Encounters",
            "type": "document_dump",
            "format": "PDF or HTML",
            "naming_convention": "{encounterId}_{date}.pdf or .html",
            "description": "All Visit Notes in PDF or HTML Format (0 to many)",
            "cardinality": "0 to many per patient",
            "field_count": "N/A - unstructured documents",
            "fields_documented": 0,
        },
        {
            "name": "Patient Documents",
            "type": "document_dump",
            "format": "PDF or HTML",
            "naming_convention": "{documentId}_{date}.pdf or .html",
            "description": "Other Documents in PDF Format or HTML Format (0 to many)",
            "cardinality": "0 to many per patient",
            "field_count": "N/A - unstructured documents",
            "fields_documented": 0,
        },
    ],
    "artifacts_reviewed": artifacts,
    "summary_statistics": {
        "total_entities": 3,  # C-CDA, Encounters folder, Documents folder
        "total_fields_documented": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "data_dictionary_present": False,
        "sample_data_present": False,
        "schema_present": False,
        "documentation_text_bytes": text_size,
        "documentation_pages": 2,
        "export_format": "C-CDA XML + PDF/HTML documents",
        "model_type": "standard projection (USCDI v1 C-CDA) + document dump",
    },
    "raw_documentation_text": raw_text,
}

output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Wrote inventory to {output_path}")
print(f"Source text size: {text_size} bytes")
print(f"PDF pages: 2")
print(f"Export components: {len(inventory['export_components'])}")
print(f"Data dictionary: No")
print(f"Field definitions: None")
print(f"Sample data: None")
print(f"USCDI v1 data classes referenced: {len(uscdi_v1_data_classes)}")
print(f"\nArtifacts reviewed:")
for a in artifacts:
    print(f"  {a['filename']}: {a['size_bytes']} bytes")
