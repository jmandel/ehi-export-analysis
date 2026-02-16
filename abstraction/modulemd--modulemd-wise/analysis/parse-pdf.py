#!/usr/bin/env python3
"""
Parse the B10 Data Export Process Flow PDF and extract all structured
information visible in screenshots and text. Since there is no data
dictionary, this script documents what the PDF actually contains and
produces the entity inventory (minimal, since no schema is provided).
"""

import json
import subprocess
import re

PDF_PATH = "../downloads/B10-Data-Export-Process-Flow-Document_compressed.pdf"

# Extract PDF metadata
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
metadata_lines = result.stdout.strip().split("\n")
metadata = {}
for line in metadata_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = result.stdout

# Document structure analysis
pdf_analysis = {
    "source_file": "B10-Data-Export-Process-Flow-Document_compressed.pdf",
    "metadata": {
        "author": metadata.get("Author", ""),
        "creator": metadata.get("Creator", ""),
        "producer": metadata.get("Producer", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": 448021,
    },
    "document_type": "Process flow / user guide with annotated screenshots",
    "content_summary": {
        "pages": 9,
        "screenshots_count": 14,  # counted from rendered pages
        "has_data_dictionary": False,
        "has_schema": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_format_specification": False,
        "has_value_sets": False,
    },
    "export_mechanics": {
        "navigation_path": "Administration >> Practice Setup >> Data Export",
        "export_creation": "+New Export button",
        "patient_selection": ["Single patient (by name or account number)", "Multiple patients", "Select All Patients"],
        "configuration_options": {
            "archive_name": "User-defined name for the export file",
            "file_type": "Dropdown (options not documented/visible)",
            "encryption_key": "Password to secure data files",
            "comments": "Rich text comments box",
        },
        "processing_pipeline": [
            {"step": 1, "status": "New", "description": "Request submitted"},
            {"step": 2, "status": "InProgress", "description": "Data generated into folders"},
            {"step": 3, "status": "Completed", "description": "Data copied to cloud, URL generated with expiry date"},
        ],
        "scheduling": "Backend program runs daily to process export requests",
        "access_control": "Download option visible only to requestor who submitted the request",
        "download_expiry": True,
        "patient_portal_access": "Single patients can download C-CDA files via Patient Portal >> Documents",
    },
    "export_output": {
        "format": "C-CDA XML",
        "file_structure": "ZIP archive containing patient folders, each with C-CDA XML file(s)",
        "file_naming_examples": [
            "QAT-1-11142023_ClinicalSummary (XML Document, from page 8 file explorer)",
            "DevAsthma7-6-11172023_ClinicalSummary.xml (from Patient Portal, page 8-9)",
        ],
        "archive_naming_examples": [
            "DevAsthma7_130",
            "DevAsthma7_129",
            "DevAsthma7_128",
        ],
    },
    "screenshots_observed_ui_elements": {
        "practice_setup_tabs": [
            "General", "Billing", "Schedule", "EMR", "Allergy",
            "Meaningful Use", "Menu Privileges", "Password Expiration",
            "Register IP Address", "Data Export"
        ],
        "top_menu_areas": [
            "Clinical Management (Finalize Notes, Documents, Schedule, Reception, Diagnostic Order)",
            "Administration (Manager, Practice Setup, Encrypt CCD)",
        ],
        "patient_portal_sections": [
            "Dashboard", "Messages", "Clinical", "Financials",
            "Patient Forms", "Educational Resources", "Documents"
        ],
    },
    "browser_downloads_sidebar_page7": {
        "note": "The page 7 screenshot shows a browser Downloads sidebar with files beyond the export ZIPs",
        "files_visible": [
            "QAT_1.zip (61.2 KB, part of export)",
            "QAT_2.zip (part of export)",
            "QAT_3 (1).zip (part of export)",
            "QAT_3.zip (part of export)",
            "Patients Referred through message.xlsx (unclear if part of export or incidental download)",
            "BilledStatements_4768_10-11 23_14.52.pdf (unclear if part of export or incidental download)",
        ],
        "interpretation": "The XLSX and PDF files may be incidental browser downloads, not part of the (b)(10) export. The document text explicitly describes the export output as 'C-CDA in XML files' organized by patient folder.",
    },
}

# Save analysis
with open("pdf-analysis.json", "w") as f:
    json.dump(pdf_analysis, f, indent=2)

print(json.dumps(pdf_analysis, indent=2))
