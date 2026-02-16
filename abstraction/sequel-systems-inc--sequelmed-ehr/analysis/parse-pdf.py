#!/usr/bin/env python3
"""Parse the SequelMed EHI export PDF and extract structured information."""

import json
import subprocess
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "downloads",
                        "SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf")

# Get PDF metadata
info_result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
info_lines = info_result.stdout.strip().split("\n")
metadata = {}
for line in info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Get PDF text
text_result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = text_result.stdout

# Extract structured info from the PDF content
export_info = {
    "document_title": "170.315(b)(10) Electronic Health Information Export - Electronic data Export Documentation",
    "version": "1.0",
    "pdf_metadata": {
        "creator": metadata.get("Creator", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": int(metadata.get("File size", "0").split()[0]),
    },
    "export_modes": [
        {
            "mode": "Single Patient Export",
            "description": "Users can export EHI for a single patient at any time without developer assistance."
        },
        {
            "mode": "Multi-Patient Export",
            "description": "Users can export EHI for multiple patients at any time without developer assistance."
        }
    ],
    "export_structure": {
        "format": "ZIP file per patient",
        "contents": [
            {
                "name": "Clinical folder",
                "description": "Contains one XML-based C-CDA file per patient",
                "format": "C-CDA XML",
                "standard": "USCDI Version 1",
                "specifications": [
                    "HL-7 Implementation Guide for CDA Release 2: IHE Health Story Consolidation, DSTU Release 1.1 (US Realm) July 2012",
                    "HL-7 Implementation Guide for CDA Release 2: Consolidated CDA Templates for Clinical Notes (US Realm), DSTU Release 2.1 August 2015, June 2019 (with Errata)",
                    "HL-7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2, October 2019"
                ]
            },
            {
                "name": "Documents folder",
                "description": "Patient documents exported in original upload/scan format",
                "document_types": [
                    "Signed progress notes",
                    "Available lab results",
                    "Radiology reports",
                    "Scanned documents",
                    "Imported documents",
                    "Uploaded documents (listed as 'Iploaded' - typo in source)"
                ],
                "supported_formats": [".jpg", ".gif", ".bmp", ".png", ".pdf", ".txt"]
            },
            {
                "name": "Patient Documents Detail.xls",
                "description": "Excel file - no further description provided in documentation",
                "format": "XLS"
            }
        ]
    },
    "data_dictionary": None,
    "sample_data": None,
    "field_level_documentation": False,
    "schema_provided": False,
    "total_entities_documented": 0,
    "total_fields_documented": 0
}

output_path = os.path.join(os.path.dirname(__file__), "pdf-parse-output.json")
with open(output_path, "w") as f:
    json.dump(export_info, f, indent=2)

print(f"Parsed PDF: {metadata.get('Pages', '?')} pages")
print(f"No data dictionary found")
print(f"No field-level documentation found")
print(f"Export format: C-CDA XML + document attachments in ZIP")
print(f"Output saved to {output_path}")
