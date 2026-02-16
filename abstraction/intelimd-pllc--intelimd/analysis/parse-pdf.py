#!/usr/bin/env python3
"""
Parse the inteliMD b10-ehi-export.pdf and extract all structured information.
Since there is no data dictionary, this script documents what IS present:
- PDF metadata
- Sections and their content
- UI elements visible in screenshots (sidebar navigation, profile fields)
- Any data fields mentioned
"""
import json
import subprocess
import re

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/b10-ehi-export.pdf", "-"],
    capture_output=True, text=True
)
text = result.stdout

# PDF info
info_result = subprocess.run(
    ["pdfinfo", "../downloads/b10-ehi-export.pdf"],
    capture_output=True, text=True
)

# Parse sections from the PDF text
sections = []
current_section = None
for line in text.split('\n'):
    stripped = line.strip()
    # Detect section headers (lines that are standalone and look like titles)
    if stripped and len(stripped) < 80 and not stripped.startswith('·'):
        if stripped in [
            "Overview", "Purpose and Scope", 
            "Single Patient's export data from UI",
            "Bulk Export of All Patients Individual Data",
            "Patient EHI C-CDA XML", "Error Codes",
            "Initiate the Bulk Export:", "Countdown and Automatic Download:"
        ]:
            if current_section:
                sections.append(current_section)
            current_section = {"heading": stripped, "content": ""}
        elif current_section:
            current_section["content"] += line + "\n"
    elif current_section:
        current_section["content"] += line + "\n"

if current_section:
    sections.append(current_section)

# Data types explicitly mentioned in the document
mentioned_data_types = [
    "demographics",
    "clinical notes", 
    "medications",
    "lab results",
    "medical history",
    "test results",
    "treatment plans",
    "health records"
]

# Fields visible in the Profile Summary screenshot (from PDF page 3)
profile_summary_fields = [
    {"field": "Patient", "example": "Reyansh Saini"},
    {"field": "Date Of Birth", "example": "November 9, 1972"},
    {"field": "Sex", "example": "Male"},
    {"field": "Race", "example": "(empty)"},
    {"field": "Ethnicity", "example": "(empty)"},
    {"field": "Contact Info", "example": "Primary Home: A S Eventech IT Pahe, Dehardun, AK 24800, US"},
    {"field": "Patient IDs", "example": "0000001142 1.3.6.1.4.1.36517.1"},
    {"field": "Document Id", "example": "PatientSummary-Header-0000001142"},
    {"field": "Document Created", "example": "November 23, 2023, 10:11:00 +0530"},
    {"field": "Performer", "example": "Abhinav Mishra"},
    {"field": "Author", "example": "Abhinav Mishra, Mean Healthcare"},
    {"field": "Contact Info (Work)", "example": "Work Place: A S Eventech IT Park"}
]

# Patient list columns visible in screenshot
patient_list_columns = [
    "S.No", "Patient Name", "Contact Details", "MRN", "SSN", "Registered Date", "Action"
]

# Sidebar navigation items visible in screenshots
sidebar_items = [
    "Registered Business",
    "Registered Patients",
    "Form Template",
    "Inquiries",
    "Logs",
    "Audit Logs",
    "Legal Documents",
    "Global Specialty Illness",
    "Manage Medication",
    "Courses",
    "Manage CSR",
    "Billed Inactive",
    "Deactivated Business",
    "Medication Improvement",
    "Manage Tickets",
    "CDS Rules",
    "Code Logs"
]

# Export formats documented
export_formats = [
    {"format": "C-CDA XML", "scope": "single patient or bulk (ZIP)", "documented_content": "medical history, test results, treatment plans, other relevant health records"},
    {"format": "PDF", "scope": "single patient only", "documented_content": "not specified"}
]

# Error codes
error_codes = [
    {"status": 400, "description": "Invalid search parameter"},
    {"status": 500, "description": "Internal Server Error"},
    {"status": 401, "description": "Unauthorized access"}
]

analysis = {
    "pdf_metadata": {
        "title": "170.315(b)(10) Electronic Health Information export",
        "producer": "Skia/PDF m144 Google Docs Renderer",
        "pages": 5,
        "file_size_bytes": 432456
    },
    "sections": [s["heading"] for s in sections],
    "mentioned_data_types": mentioned_data_types,
    "profile_summary_fields": profile_summary_fields,
    "patient_list_columns": patient_list_columns,
    "sidebar_navigation_items": sidebar_items,
    "export_formats": export_formats,
    "error_codes": error_codes,
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_definitions": False,
    "has_ccda_section_mapping": False,
    "has_value_sets": False,
    "has_relationships": False,
    "product_info": {
        "developer": "inteliMD PLLC",
        "product": "inteliMD",
        "version": "v1.1",
        "certificate_number": "15.05.05.3211.INTL.01.00.1.241127",
        "certification_date": "Nov 27, 2024",
        "criteria": "§170.315(b)(10)"
    }
}

with open("pdf-analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

print(json.dumps(analysis, indent=2))
