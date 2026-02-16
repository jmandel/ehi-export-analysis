#!/usr/bin/env python3
"""
Extract all structured evidence from the Zoobook EHI Export Documentation PDF.
Since this PDF is a 5-page user guide with screenshots (not a data dictionary),
we extract: visible module names, navigation tabs, settings items, user roles,
and sample export records visible in screenshots.
"""

import json
import subprocess
import sys

PDF_PATH = "../../../results/zoobook-systems-llc--zoobook-ehr/downloads/EHIexportDocumentation.pdf"

# Get PDF metadata
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
pdf_info_lines = result.stdout.strip().split("\n")
pdf_metadata = {}
for line in pdf_info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_metadata[key.strip()] = val.strip()

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = result.stdout

# All evidence extracted from screenshots and text (verified against rendered PNG pages)
evidence = {
    "pdf_metadata": {
        "pages": int(pdf_metadata.get("Pages", 0)),
        "author": pdf_metadata.get("Author", ""),
        "creator": pdf_metadata.get("Creator", ""),
        "creation_date": pdf_metadata.get("CreationDate", ""),
        "file_size_bytes": 389047,
    },
    "document_title": "§170.315(b)(10) Electronic Health Information Export Documentation",
    "document_type": "UI walkthrough / user guide with annotated screenshots",
    "contains_data_dictionary": False,
    "contains_schema": False,
    "contains_sample_data_files": False,
    "contains_format_specification": False,

    "navigation_tabs_visible": [
        "Dashboard", "Call Center", "Clients", "Employees", "Appointments",
        "Lab Results", "Group Curriculum", "Billing", "Client Invoicing/Payment",
        "Payroll", "Quality", "Reports", "Meetings/Group Supervision",
        "Policies", "Contacts", "Marketing"
    ],

    "settings_menu_items": {
        "General": [
            "Amendment Settings", "Bed Management Settings", "Billing Settings",
            "Business Rules Management", "Clinical Decision Support Settings",
            "Companies", "Data Export Settings", "DropDown Manager", "EHI Export",
            "Email Templates", "Enhancement Packages", "Form Builder",
            "Job Descriptions", "Notifications Manager", "Prescriber List",
            "Real-time Notifications", "Referrals/Payers",
            "Urine Screen Code Management", "Vacation and Leaves Settings"
        ],
        "Logs": ["Email Logs", "Fax Messages", "SMS Send Logs"],
        "Security": ["(partially visible in screenshot)"]
    },

    "export_filter_fields": ["Date Range (Date From / Date To)", "Clients", "Modules"],

    "export_record_columns": [
        "Client IDs", "Full Name", "Module IDs", "Module Name",
        "URL", "Start Date", "End Date", "Created By",
        "Expiration Date", "Download Button"
    ],

    "sample_export_records_visible": [
        {
            "client_id": "223837",
            "full_name": "QAtest, TeoTest1",
            "module_id": "253",
            "module_name": "Psychiatric Progress Note",
            "start_date": "11/24/2023",
            "end_date": "11/30/2023",
            "created_by": "Pamela",
            "expiration_date": "11/30/2023 10:47:49 AM"
        },
        {
            "client_id": "132370, 223954",
            "full_name": "Miller, Paul, Tezt, Premiz MI",
            "module_id": "246",
            "module_name": "Mental Health Assessment",
            "start_date": "11/19/2023",
            "end_date": "11/29/2023",
            "created_by": "Pamela",
            "expiration_date": "11/30/2023 10:42:15 AM"
        }
    ],

    "modules_total_selected": 172,
    "modules_visible_in_screenshot": [
        {"id": "836", "name": "Client Notes To File", "checked": False, "note": "Excluded from export in screenshot"},
        {"id": "842", "name": "PHI Disclosure Log", "checked": True},
        {"id": "853", "name": "CPST Note", "checked": True},
        {"id": "1841", "name": "Counseling Monthly Individual Progress Report", "checked": True},
        {"id": "811", "name": "Comprehensive Psychosocial Evaluation", "checked": True},
        {"id": "883", "name": "Pre-Admission Documents", "checked": True}
    ],

    "user_roles_visible": [
        "Administrative Staff", "Administrator", "Assistant Clinical Director",
        "Billers", "Clerical", "Client", "Counselor", "Director", "Driver",
        "Hr Staff", "Intake", "Intern/Trainee", "Manager", "Medical Staff",
        "Provisional User", "Receptionist", "Sample Collector",
        "Super Administrator", "Supervisor", "Support"
    ],

    "security_settings_visible": [
        "Client File Restrictions", "Company Roles Management",
        "Company Wide Settings", "FHIR Settings", "Module Management",
        "Provisional Account Management"
    ],

    "export_delivery_methods": ["Download Button", "Public URL"],

    "disclosures_page_rwt_objectives": {
        "objective_1": "EHI Export Functionality Accuracy — target ≥98% error-free exports",
        "objective_2": "Export Usability Efficiency — target ≤2 minutes per export",
        "objective_3": "Role-Based Access Control — 100% authorized / 0% unauthorized",
        "objective_4": "Date Range Configuration Accuracy — target 98% correct application",
        "objective_5": "Batch Export Efficiency — target ≤1.5x individual export time",
        "objective_6": "Transmission Reliability and Storage Options — target ≥99% success"
    }
}

# Compute summary statistics
summary = {
    "total_modules_claimed": 172,
    "modules_with_names_visible": len(evidence["modules_visible_in_screenshot"]),
    "modules_with_descriptions": 0,
    "modules_with_field_details": 0,
    "total_fields_documented": 0,
    "export_format_documented": False,
    "data_dictionary_present": False,
    "sample_data_files_present": False,
    "user_roles_count": len(evidence["user_roles_visible"]),
    "navigation_tabs_count": len(evidence["navigation_tabs_visible"]),
    "pdf_pages": evidence["pdf_metadata"]["pages"]
}

output = {
    "extraction_date": "2026-02-16",
    "source_artifact": "downloads/EHIexportDocumentation.pdf",
    "evidence": evidence,
    "summary": summary
}

with open("pdf-evidence.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(summary, indent=2))
print(f"\nSaved full evidence to pdf-evidence.json")
