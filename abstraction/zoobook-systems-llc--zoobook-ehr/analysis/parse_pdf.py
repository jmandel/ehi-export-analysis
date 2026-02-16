#!/usr/bin/env python3
"""
Parse the Zoobook EHI Export Documentation PDF and extract all structured information.
The PDF is a 5-page UI walkthrough with screenshots — there is no data dictionary
or schema to parse. This script extracts what little structured info exists:
module names visible in screenshots, export record columns, and user roles.
"""

import json
import subprocess
import re

PDF_PATH = "../downloads/EHIexportDocumentation.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout

# Extract PDF metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)

# Parse known structured elements from the PDF and screenshots

# Visible module names from the business rules screenshot (page 4)
visible_modules = [
    {"id": 836, "name": "Client Notes To File", "selected": False},
    {"id": 842, "name": "PHI Disclosure Log", "selected": True},
    {"id": 853, "name": "CPST Note", "selected": True},
    {"id": 1841, "name": "Counseling Monthly Individual Progress Report", "selected": True},
    {"id": 811, "name": "Comprehensive Psychosocial Evaluation", "selected": True},
    {"id": 883, "name": "Pre-Admission Documents", "selected": True},
]

# Module names visible from page 2 export records table
export_sample_modules = [
    "Psychiatric Progress Note",
    "Mental Health Assessment",
]

# Export record listing columns (page 3) — these describe the UI, not the exported data
export_listing_columns = [
    {"name": "Client ID", "description": "Unique identifier assigned to each client"},
    {"name": "Full Name", "description": "Complete name of the client"},
    {"name": "Module Name", "description": "Specific module from which data is exported"},
    {"name": "URL", "description": "Public URL for downloading the EHI export"},
    {"name": "Start Date", "description": "Commencement date of the record"},
    {"name": "End Date", "description": "Final date of the data record"},
    {"name": "Created By", "description": "Employee who generated the record"},
    {"name": "Expiration Date", "description": "When the record expires or becomes unavailable"},
    {"name": "Download Button", "description": "UI element to download the EHI record file"},
]

# User roles visible in access control screenshot (page 5)
user_roles = [
    "Administrative Staff", "Administrator", "Assistant Clinical Director",
    "Billers", "Clerical", "Client", "Counselor", "Director", "Driver",
    "Hr Staff", "Intake", "Intern/Trainee", "Manager", "Medical Staff",
    "Provisional User", "Receptionist", "Sample Collector",
    "Super Administrator", "Supervisor", "Support",
]

# Navigation bar modules visible in page 1 screenshot
nav_bar_modules = [
    "Dashboard", "Call Center", "Clients", "Employees", "Appointments",
    "Lab Results", "Group Curriculum", "Billing", "Client Invoice/Payment",
    "Payroll", "Quality", "Reports", "Meetings/Group Supervision",
    "Policies", "Contracts", "Marketing",
]

# Settings menu items visible in page 1 screenshot
settings_menu_items = {
    "General": [
        "Amendment Settings", "Bed Management Settings", "Billing Settings",
        "Business Rules Management", "Clinical Decision Support Settings",
        "Companies", "Data Export Settings", "DropDown Manager", "EHI Export",
        "Email Templates", "Enhancement Packages", "Form Builder",
        "Job Descriptions", "Notifications Manager", "Prescriber List",
        "Real-time Notifications", "Referrals/Payers",
        "Urine Screen Code Management", "Vacation and Leaves Settings",
    ],
    "Logs": [
        "Email Logs", "Fax Messages", "SMS Send Logs",
    ],
    "Security": [],  # truncated in screenshot
}

output = {
    "pdf_metadata": {
        "pages": 5,
        "file_size_bytes": 389047,
        "created": "2023-11-28",
        "creator": "Microsoft Word 2016",
        "author": "ACER",
    },
    "document_type": "UI walkthrough / user guide",
    "contains_data_dictionary": False,
    "contains_schema": False,
    "contains_sample_data": False,
    "contains_format_specification": False,
    "total_modules_available": 172,
    "visible_modules_in_business_rules": visible_modules,
    "export_sample_modules": export_sample_modules,
    "export_listing_columns": export_listing_columns,
    "user_roles": user_roles,
    "nav_bar_modules": nav_bar_modules,
    "settings_menu_items": settings_menu_items,
    "export_filters": ["Date Range", "Clients", "Modules"],
    "export_delivery": ["Download Button", "Public URL"],
    "notes": [
        "The PDF documents the export UI process, not the exported data itself.",
        "172 modules are listed as available for export, but only 6 are visible by name.",
        "No export format (CSV, JSON, PDF, etc.) is specified anywhere.",
        "No field-level documentation exists for any module.",
        "The 'Column Definition' section describes the export records listing UI, not the actual exported data content.",
        "Administrators can selectively exclude modules from the export via Business Rules.",
        "Role-based access controls which user roles can perform exports.",
    ],
}

with open("pdf_extraction.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
