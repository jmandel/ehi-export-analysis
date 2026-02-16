#!/usr/bin/env python3
"""Parse the Practice EHR B10 PDF and extract structured information."""

import subprocess
import json
import re

PDF_PATH = "../downloads/Practice-EHR-B10-Electronic-Health-Information-Export.pdf"

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout

# Extract metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)
metadata = {}
for line in info_result.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Parse document structure
export_components = {
    "clinical_folder": {
        "format": "C-CDA XML",
        "standard": "USCDI v1",
        "description": "One XML-based C-CDA file per patient",
        "hl7_specs_referenced": [
            "HL7 CDA R2 IHE Health Story Consolidation, DSTU Release 1.1 (July 2012)",
            "HL7 CDA R2 Consolidated CDA Templates, DSTU Release 2.1 (Aug 2015, Jun 2019 Errata)",
            "HL7 CDA R2 C-CDA Templates R2.1 Companion Guide, Release 2 (Oct 2019)"
        ]
    },
    "documents_folder": {
        "format": "Original upload/scan formats",
        "file_types": [".jpg", ".gif", ".bmp", ".png", ".pdf", ".txt"],
        "document_types": [
            "Signed progress notes",
            "Available lab results",
            "Radiology reports",
            "Scanned documents",
            "Imported documents",
            "Uploaded documents"
        ]
    },
    "index_file": {
        "name": "Patient Documents Detail.xls",
        "format": "XLS",
        "description": "Index of patient documents (structure not documented)"
    }
}

export_modes = {
    "single_patient": "Export EHI for one patient at any time without developer assistance",
    "multi_patient": "Export EHI for multiple patients at any time without developer assistance"
}

# C-CDA USCDI v1 data classes (what a standard C-CDA covers)
ccda_uscdi_v1_coverage = [
    "Patient demographics",
    "Problems / diagnoses",
    "Medications",
    "Allergies",
    "Lab results (structured)",
    "Vital signs",
    "Procedures",
    "Immunizations",
    "Care team",
    "Goals",
    "Health concerns",
    "Smoking status",
    "Assessment and plan"
]

analysis = {
    "pdf_metadata": metadata,
    "pdf_pages": int(metadata.get("Pages", 0)),
    "pdf_size_bytes": 116552,
    "version": "1.0",
    "date": "November 2023",
    "export_modes": export_modes,
    "export_components": export_components,
    "ccda_uscdi_v1_coverage": ccda_uscdi_v1_coverage,
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "field_level_documentation": False,
    "typos_found": ["USCD (should be USCDI)", "Iploaded (should be Uploaded)"],
    "raw_text": text
}

with open("pdf-analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

print(f"PDF pages: {analysis['pdf_pages']}")
print(f"Data dictionary: {analysis['data_dictionary_present']}")
print(f"Schema: {analysis['schema_present']}")
print(f"Sample data: {analysis['sample_data_present']}")
print(f"Export components: {len(export_components)}")
print(f"C-CDA covers {len(ccda_uscdi_v1_coverage)} USCDI v1 data classes")
print("Saved to pdf-analysis.json")
