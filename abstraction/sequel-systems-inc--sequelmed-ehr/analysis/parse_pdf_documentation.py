#!/usr/bin/env python3
"""
Parse the SequelMed EHR B10 Electronic Health Information Export PDF.
Extracts structured information about the export documentation.

Input: The single PDF artifact (SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf)
Output: JSON summary of what the documentation describes, saved to pdf-analysis.json
"""

import json
import subprocess
import os

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
RESULTS_DIR = os.path.join(REPO_ROOT, "results", "sequel-systems-inc--sequelmed-ehr")
PDF_PATH = os.path.join(RESULTS_DIR, "downloads", "SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Extract PDF metadata
pdfinfo = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
info_lines = pdfinfo.stdout.strip().split("\n")
metadata = {}
for line in info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Extract PDF text
pdftext = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = pdftext.stdout

# Build structured analysis
analysis = {
    "pdf_file": "SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf",
    "pdf_metadata": {
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": int(metadata.get("File size", "0").replace(" bytes", "")),
        "creator": metadata.get("Creator", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "pdf_version": metadata.get("PDF version", ""),
    },
    "document_title": "170.315(b)(10) Electronic Health Information Export — Electronic data Export Documentation",
    "version": "1.0",
    "export_modes": [
        {
            "mode": "Single patient",
            "description": "SequelMed EHR allows users to export EHI for a single patient at any time without developer assistance."
        },
        {
            "mode": "Multi-patient",
            "description": "SequelMed EHR allows users to export EHI for multiple patients at any time without developer assistance."
        }
    ],
    "export_structure": {
        "format": "Single compressed ZIP file per patient",
        "contents": [
            {
                "name": "Clinical folder",
                "description": "Contains one XML-based C-CDA file for the patient",
                "format": "C-CDA XML",
                "standard_compliance": "US Core Data for Interoperability (USCDI) Version 1",
                "referenced_specs": [
                    "HL7 Implementation Guide for CDA Release 2: IHE Health Story Consolidation, DSTU Release 1.1 (US Realm) July 2012",
                    "HL7 Implementation Guide for CDA Release 2: Consolidated CDA Templates for Clinical Notes (US Realm), DSTU Release 2.1 August 2015, June 2019 (with Errata)",
                    "HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2, October 2019"
                ]
            },
            {
                "name": "Documents folder",
                "description": "Patient documents exported in their original upload/scan format",
                "document_types": [
                    "Signed progress notes",
                    "Available lab results",
                    "Radiology reports",
                    "Scanned documents",
                    "Imported documents",
                    "Uploaded documents (listed as 'Iploaded' — typo in original)"
                ],
                "supported_formats": [".jpg", ".gif", ".bmp", ".png", ".pdf", ".txt"]
            },
            {
                "name": "Patient Documents Detail.xls",
                "description": "Excel file — no further explanation provided in documentation",
                "format": "XLS",
                "documentation_quality": "Completely undocumented; contents unknown"
            }
        ]
    },
    "data_dictionary": None,
    "sample_data": None,
    "schema_files": None,
    "field_level_documentation": False,
    "screenshots": False,
    "documentation_issues": [
        "No data dictionary or field-level documentation",
        "No schema files",
        "No sample data",
        "No screenshots of export interface",
        "Patient Documents Detail.xls is listed but never described",
        "Typo: 'Iploaded' instead of 'Uploaded' on page 3",
        "Typo: 'USCD' instead of 'USCDI' on page 2",
        "No explanation of what data is included in or excluded from the C-CDA",
        "No explanation of scope or completeness"
    ],
    "content_pages": {
        "total_pages": 4,
        "cover_page": 1,
        "content_pages": 3,
        "estimated_substantive_content_pages": 1.5
    }
}

# Count lines of actual content (non-blank, non-page-number)
content_lines = [
    line.strip() for line in full_text.split("\n")
    if line.strip() and not line.strip().startswith("Page |")
]
analysis["content_line_count"] = len(content_lines)
analysis["full_text_extracted"] = full_text

output_path = os.path.join(OUTPUT_DIR, "pdf-analysis.json")
with open(output_path, "w") as f:
    json.dump(analysis, f, indent=2)

print(f"PDF Analysis saved to {output_path}")
print(f"Pages: {analysis['pdf_metadata']['pages']}")
print(f"Content lines: {analysis['content_line_count']}")
print(f"Export components: {len(analysis['export_structure']['contents'])}")
print(f"Documentation issues: {len(analysis['documentation_issues'])}")
print(f"Data dictionary: {'Yes' if analysis['data_dictionary'] else 'No'}")
print(f"Sample data: {'Yes' if analysis['sample_data'] else 'No'}")
print(f"Field-level docs: {'Yes' if analysis['field_level_documentation'] else 'No'}")
