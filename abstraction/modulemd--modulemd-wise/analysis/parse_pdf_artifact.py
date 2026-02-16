#!/usr/bin/env python3
"""Parse the B10 Data Export Process Flow PDF and extract structured information.

This is the only artifact available for ModuleMD WISE's (b)(10) export.
The PDF is a 9-page process guide with screenshots — no data dictionary,
no schema, no field-level documentation. This script documents what IS
present and produces a structured JSON output.
"""

import json
import subprocess
import os

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/modulemd--modulemd-wise/downloads/B10-Data-Export-Process-Flow-Document_compressed.pdf"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Extract PDF metadata
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
pdf_info = {}
for line in result.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_info[key.strip()] = val.strip()

# Extract full text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = result.stdout

# Build structured artifact analysis
artifact = {
    "artifact_file": "B10-Data-Export-Process-Flow-Document_compressed.pdf",
    "pdf_metadata": {
        "pages": int(pdf_info.get("Pages", 0)),
        "title": pdf_info.get("Title", ""),
        "author": pdf_info.get("Author", ""),
        "creator": pdf_info.get("Creator", ""),
        "creation_date": pdf_info.get("CreationDate", ""),
        "file_size": pdf_info.get("File size", ""),
    },
    "document_type": "Process flow guide with screenshots",
    "content_summary": {
        "total_pages": 9,
        "content_pages": 8,  # page 9 is just "Confidential" marker
        "pages": [
            {
                "page": 1,
                "content": "Title page and introduction. States export format is C-CDA or CSV. Navigation path: Administration >> Practice Setup >> Data Export.",
                "key_quote": "The documentation for the export format consists of information on the structure and syntax for how the EHI will be exported by the product such as, for example, Consolidated-Clinical Document Architecture (C-CDA) document(s) or data dictionary for comma separated values (csv) file(s)."
            },
            {
                "page": 2,
                "content": "Patient selection UI. Shows search by Name or Account Number. Single or multiple patient selection."
            },
            {
                "page": 3,
                "content": "Multiple patient selection screen. 'Select All Patients' checkbox for bulk export."
            },
            {
                "page": 4,
                "content": "Export form fields: Archive Name, File Type (dropdown - value not shown), Encryption Key, Comments, Submit button. Backend program scheduled daily to process exports.",
                "notable": "File Type dropdown is visible but empty/value not documented. No indication of what file type options exist."
            },
            {
                "page": 5,
                "content": "Step 1: Request submitted, status 'New' on Data Export Screen. Table columns: Archive Name, Date Generated, Created By, Status, Expiry Date."
            },
            {
                "page": 6,
                "content": "Steps 2-3: Status progression from 'InProgress' to 'Completed'. Download option visible only to requestor. Expiry dates shown.",
                "notable": "Practice Setup tabs visible: General, Billing, Schedule, EMR, Allergy, Meaningful Use, Menu Privileges, Data Export"
            },
            {
                "page": 7,
                "content": "Download section. Shows ZIP files (QAT_1.zip, QAT_2.zip, QAT_3.zip). Patient folder structure. Text: 'Download the Folder and Select the Patient folder to view C-CDA in XML files'.",
                "notable": "Export output confirmed as C-CDA XML files organized in per-patient folders within ZIP archives."
            },
            {
                "page": 8,
                "content": "Shows ClinicalSummary XML file in patient folder. Patient Portal document download option.",
                "notable": "File named 'QAT-1-11142023_ClinicalSummary' (XML Document). Patient Portal also provides C-CDA download under Documents."
            },
            {
                "page": 9,
                "content": "'|| Confidential ||' marker only."
            }
        ]
    },
    "export_characteristics": {
        "format": "C-CDA XML (ClinicalSummary)",
        "format_evidence": "Page 7: 'view C-CDA in XML files'; Page 8: filename 'QAT-1-11142023_ClinicalSummary' (XML Document)",
        "csv_mentioned": True,
        "csv_evidence": "Page 1 mentions CSV as possible format, but all screenshots and instructions show only C-CDA XML output",
        "csv_documented": False,
        "packaging": "ZIP archives containing per-patient folders with XML files",
        "patient_selection": ["Single patient", "Multiple patients", "All patients"],
        "bulk_capable": True,
        "mechanism": "UI-driven: Administration >> Practice Setup >> Data Export",
        "processing": "Backend batch program scheduled daily",
        "access_control": "Download visible only to requestor; downloads have expiry dates",
        "encryption": "Optional encryption key/password",
        "patient_portal_access": True,
        "patient_portal_note": "Single patients can download C-CDA from Patient Portal >> Documents"
    },
    "documentation_assessment": {
        "has_data_dictionary": False,
        "has_schema": False,
        "has_field_documentation": False,
        "has_sample_data": False,
        "has_entity_list": False,
        "has_relationship_documentation": False,
        "has_value_sets": False,
        "document_purpose": "Step-by-step UI walkthrough for initiating an export",
        "what_is_missing": [
            "Data dictionary or schema for exported content",
            "Field-level documentation",
            "Description of what clinical data elements are included in the C-CDA",
            "Documentation of CSV export option (mentioned but never shown)",
            "Entity/table listing",
            "Sample export files",
            "Relationship documentation",
            "Value set definitions"
        ]
    }
}

# Write output
output_path = os.path.join(OUTPUT_DIR, "pdf-artifact-analysis.json")
with open(output_path, "w") as f:
    json.dump(artifact, f, indent=2)
print(f"Wrote artifact analysis to {output_path}")

# Print summary
print(f"\nPDF: {artifact['artifact_file']}")
print(f"Pages: {artifact['pdf_metadata']['pages']}")
print(f"Author: {artifact['pdf_metadata']['author']}")
print(f"Type: {artifact['document_type']}")
print(f"Export format: {artifact['export_characteristics']['format']}")
print(f"Has data dictionary: {artifact['documentation_assessment']['has_data_dictionary']}")
print(f"Has schema: {artifact['documentation_assessment']['has_schema']}")
print(f"Has field docs: {artifact['documentation_assessment']['has_field_documentation']}")
print(f"Has sample data: {artifact['documentation_assessment']['has_sample_data']}")
print(f"Missing items: {len(artifact['documentation_assessment']['what_is_missing'])}")
