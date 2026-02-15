#!/usr/bin/env python3
"""Analyze the ModuleMD WISE B10 Data Export PDF.

Extracts text, metadata, and key findings from the single EHI export artifact.
"""
import subprocess
import json
import os

PDF_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../results/modulemd--modulemd-wise/downloads/"
    "B10-Data-Export-Process-Flow-Document_compressed.pdf"
)
OUTPUT_DIR = os.path.dirname(__file__)

# Get PDF metadata
meta_raw = subprocess.run(
    ["pdfinfo", PDF_PATH], capture_output=True, text=True
).stdout
metadata = {}
for line in meta_raw.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Extract full text
text = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
).stdout

# Page-by-page analysis (based on manual inspection of rendered pages)
pages = [
    {
        "page": 1,
        "content": "Title page + intro text",
        "key_findings": [
            "Mentions both C-CDA and CSV as possible export formats",
            "Navigation: Administration >> Practice Setup >> Data Export",
            "Exact quote: 'export format consists of information on the structure and syntax "
            "for how the EHI will be exported by the product such as, for example, "
            "Consolidated-Clinical Document Architecture (C-CDA) document(s) or data dictionary "
            "for comma separated values (csv) file(s)'"
        ]
    },
    {
        "page": 2,
        "content": "Patient selection UI",
        "key_findings": [
            "Single or multiple patient selection by Name or Account Number",
            "+New Export button initiates process"
        ]
    },
    {
        "page": 3,
        "content": "Bulk patient selection",
        "key_findings": [
            "Select All Patients checkbox enables bulk export"
        ]
    },
    {
        "page": 4,
        "content": "Export configuration options",
        "key_findings": [
            "Archive Name field",
            "File Type dropdown (values NOT enumerated in document)",
            "Encryption Key field for password protection",
            "Comments field",
            "Submit button triggers daily backend batch processing"
        ]
    },
    {
        "page": 5,
        "content": "Export status workflow",
        "key_findings": [
            "3-step pipeline: New → InProgress → Completed",
            "Backend program scheduled daily",
            "Shows multiple exports (DevAsthma7_122 through DevAsthma7_127) with InProgress status"
        ]
    },
    {
        "page": 6,
        "content": "Completed exports with download",
        "key_findings": [
            "Completed exports show expiry dates (12/19-12/20/2023)",
            "Download icon visible only for requestor",
            "Navigation tabs visible: General, Billing, Schedule, EMR, Allergy, "
            "Meaningful Use, Menu Privileges, Data Export"
        ]
    },
    {
        "page": 7,
        "content": "Downloaded file contents",
        "key_findings": [
            "Shows ZIP files in download (QAT_1.zip, QAT_2.zip, QAT_3.zip)",
            "Instructions say 'Download the Folder and Select the Patient folder "
            "to view C-CDA in XML files'",
            "Visible filename: QAT-1-11142023_ClinicalSummary — confirms C-CDA XML per patient"
        ]
    },
    {
        "page": 8,
        "content": "Patient Portal access",
        "key_findings": [
            "Single patients can download C-CDA from Patient Portal",
            "Documents section shows C-CDA hyperlink",
            "Visible filename: DevAsthma7-6-11172023_ClinicalSummary"
        ]
    },
    {
        "page": 9,
        "content": "Confidentiality marker only",
        "key_findings": ["'|| Confidential ||' — no substantive content"]
    }
]

# Build output
output = {
    "pdf_file": "B10-Data-Export-Process-Flow-Document_compressed.pdf",
    "file_size_bytes": 448021,
    "metadata": metadata,
    "total_pages": 9,
    "substantive_pages": 8,  # page 9 is just a footer
    "page_analysis": pages,
    "export_format_evidence": {
        "confirmed": "C-CDA XML (Clinical Summary per patient in ZIP folders)",
        "mentioned_but_undocumented": "CSV with data dictionary (mentioned on page 1 intro text only)",
        "file_type_dropdown": "Shown on page 4 but values never enumerated"
    },
    "export_mechanics": {
        "access_path": "Administration >> Practice Setup >> Data Export",
        "patient_selection": "Single, multiple (by name/account#), or all patients",
        "processing": "Daily backend batch job",
        "pipeline": "New → InProgress → Completed",
        "delivery": "URL download with expiry date",
        "encryption": "Optional encryption key",
        "access_control": "Download visible only to requestor",
        "patient_portal": "Single patients can download C-CDA from portal"
    },
    "data_dictionary": None,
    "sample_data": None,
    "schema": None,
    "missing_from_documentation": [
        "No data dictionary",
        "No field-level documentation",
        "No schema or data model description",
        "No sample data files",
        "File Type dropdown values not enumerated",
        "No description of what data fields are included in C-CDA exports",
        "No description of what data fields would be in CSV exports (if they exist)",
        "No documentation of relationships between data elements",
        "No value sets or code systems documented"
    ]
}

# Save output
output_path = os.path.join(OUTPUT_DIR, "pdf_analysis_output.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

# Print summary
print(f"PDF: {output['pdf_file']}")
print(f"Size: {output['file_size_bytes']} bytes")
print(f"Pages: {output['total_pages']} ({output['substantive_pages']} substantive)")
print(f"Author: {metadata.get('Author', 'unknown')}")
print(f"Created: {metadata.get('CreationDate', 'unknown')}")
print(f"\nConfirmed format: {output['export_format_evidence']['confirmed']}")
print(f"Mentioned but undoc: {output['export_format_evidence']['mentioned_but_undocumented']}")
print(f"\nMissing documentation items: {len(output['missing_from_documentation'])}")
for item in output['missing_from_documentation']:
    print(f"  - {item}")
