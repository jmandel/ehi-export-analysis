#!/usr/bin/env python3
"""
Analyze the inteliMD b10-ehi-export.pdf artifact.
Extracts structured information from the PDF text content.
"""
import json
import subprocess
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/intelimd-pllc--intelimd/downloads/b10-ehi-export.pdf"

# Get PDF metadata
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
info_lines = result.stdout.strip().split("\n")
metadata = {}
for line in info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = result.stdout

# Analyze document structure
sections = []
current_section = None
for line in full_text.split("\n"):
    stripped = line.strip()
    # Detect section headers (bold/large text in PDF shows as standalone lines)
    if stripped in ["Overview", "Purpose and Scope", "Error Codes",
                    "Patient EHI C-CDA XML"]:
        if current_section:
            sections.append(current_section)
        current_section = {"title": stripped, "lines": []}
    elif stripped.startswith("Single Patient") or stripped.startswith("Bulk Export"):
        if current_section:
            sections.append(current_section)
        current_section = {"title": stripped, "lines": []}
    elif current_section:
        if stripped:
            current_section["lines"].append(stripped)

if current_section:
    sections.append(current_section)

# Summarize
analysis = {
    "artifact": "b10-ehi-export.pdf",
    "source_url": "https://www.intelimd.com/assets/docs/b10-ehi-export.pdf",
    "pdf_metadata": {
        "title": metadata.get("Title", ""),
        "producer": metadata.get("Producer", ""),
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": int(metadata.get("File size", "0").split()[0]),
        "pdf_version": metadata.get("PDF version", ""),
    },
    "document_sections": [
        {"title": s["title"], "line_count": len(s["lines"])} for s in sections
    ],
    "export_format": {
        "primary": "C-CDA XML",
        "secondary": "PDF (single patient only)",
        "bulk": "ZIP of C-CDA XML files",
    },
    "export_mechanism": {
        "access_level": "superadmin",
        "authentication": "OTP verification to registered mobile number",
        "single_patient": "UI button on patient profile (eye icon → C-CDA or PDF download)",
        "bulk": "'Download Records' button generates ZIP of all patients' C-CDA files",
    },
    "data_domains_mentioned": [
        "demographics",
        "clinical notes",
        "medications",
        "lab results",
        "medical history",
        "test results",
        "treatment plans",
    ],
    "documentation_gaps": {
        "data_dictionary": False,
        "schema_documentation": False,
        "sample_data": False,
        "field_level_specs": False,
        "ccda_template_oids": False,
        "ccda_sections_listed": False,
        "value_sets": False,
        "relationships": False,
        "completeness_mapping": False,
        "api_documentation": False,
    },
    "error_codes": [
        {"status": 400, "description": "Invalid search parameter"},
        {"status": 500, "description": "Internal Server Error"},
        {"status": 401, "description": "Unauthorized access"},
    ],
    "product_info": {
        "developer": "inteliMD PLLC",
        "product": "inteliMD",
        "version": "v1.1",
        "certificate": "15.05.05.3211.INTL.01.00.1.241127",
        "certification_date": "Nov 27, 2024",
        "criteria": "§170.315(b)(10)",
    },
    "sidebar_menu_items_visible_in_screenshots": [
        "Registered Business",
        "Registered Patients",
        "Form Template",
        "Inquiries",
        "Logs",
        "Audit Logs",
        "Legal Documents",
        "Global Speciality Illness",
        "Manage Medication",
        "Courses",
        "Manage CSR",
        "Billed Inactive",
        "Deactivated Business",
        "Medication Improvement",
        "Manage Tickets",
        "CDS Rules",
        "Code Logs",
    ],
    "patient_chart_summary_fields_visible": [
        "Patient (name)",
        "Date Of Birth",
        "Sex",
        "Race",
        "Ethnicity",
        "Contact Info",
        "Patient IDs",
        "Document Id",
        "Document Created",
        "Performer",
        "Author",
    ],
    "patient_list_columns_visible": [
        "S.No",
        "Patient Name",
        "Contact Details",
        "MRN",
        "SSN",
        "Registered Date",
        "Action",
    ],
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/intelimd-pllc--intelimd/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(analysis, f, indent=2)

print(json.dumps(analysis, indent=2))
