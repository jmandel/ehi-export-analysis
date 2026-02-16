#!/usr/bin/env python3
"""
Parse the ReLiMed Patient Export File Format PDF and produce a structured
JSON inventory of everything documented about the export.

Source: downloads/Patient_Export_Data_File_Format.pdf (4 pages, 189,921 bytes)
Created: Oct 18, 2023 by Lisa Davies via Microsoft Word for Microsoft 365
"""

import json

# Everything below is manually extracted from the PDF text and screenshots.
# The PDF has NO field-level data dictionary — only worksheet/file names
# with brief descriptions. This script captures every piece of structured
# information present in the documentation.

export_doc = {
    "source_file": "Patient_Export_Data_File_Format.pdf",
    "source_url": "https://hf-files-oregon.s3.amazonaws.com/hdprelimed_kb_attachments/2023/10-18/b1891224-a7cc-4e26-a531-433712c1d9cc/Patient_Export_Data_File_Format.pdf",
    "pages": 4,
    "size_bytes": 189921,
    "created": "2023-10-18",
    "author": "Lisa Davies",
    "tool": "Microsoft Word for Microsoft 365",

    "single_patient_export": {
        "access": "Patient Chart -> Patient Export menu option",
        "privilege_required": "Medical Record Request",
        "output_format": "PDF",
        "output_options": ["Save", "Print", "Fax"],
        "selectable_categories": [
            {"name": "Encounters", "description": "Encounter records with date, type, status, provider columns"},
            {"name": "Active Medications", "description": "Active medication records"},
            {"name": "Chronic Problems", "description": "Chronic problem records"},
            {"name": "Allergies", "description": "Allergy records"},
            {"name": "Documents", "description": "Documents uploaded to patient chart"},
            {"name": "eLab Results", "description": "Electronic lab results"},
            {"name": "Patient Forms", "description": "Custom user forms"},
            {"name": "CCD", "description": "Continuity of Care Document"},
            {"name": "Claims", "description": "Claim records"}
        ],
        "export_options": {
            "Insurance": "Include Insurance Information (checkbox)",
            "Medical History": "Include Active Allergies, Include Active Medications, Include Chronic Problems (checkboxes)",
            "Restricted": "Include Encounter Types, Include Document Types (checkboxes)"
        },
        "date_filter": "From Date / To Date with Apply button",
        "tabs": ["Clinical Data", "Additional Notes", "Additional Files"],
        "screenshot_details": {
            "test_patient": "ReLiMed Test | 1596 | M | 02/18/1972 (51 yrs)",
            "encounter_types_visible": [
                "Billing Only",
                "Follow Up",
                "Assessment/Testing",
                "Initial Evaluation FTF 60 min",
                "No Show - Charge"
            ],
            "encounter_statuses_visible": ["Open", "Closed"],
            "encounter_columns": ["Documentation", "A", "S", "checkbox", "Date", "Type", "Status", "Provider"]
        }
    },

    "bulk_export": {
        "access": "Provided by ReLi Med Solutions support team upon request",
        "self_service": False,
        "delivery": "Password-protected ZIP file on SFTP server",
        "security": {
            "sftp_password": "Separate password sent via secure email",
            "zip_password": "Separate password sent via secure email (different from SFTP)",
            "rationale": "Allows non-HIPAA compliant user to assist with download without patient data exposure"
        },
        "sftp_client_recommended": "FileZilla 3.55.1",

        "xlsx_workbook": {
            "filename": "patient-data-export.xlsx",
            "worksheets": [
                {"name": "Locations", "description": "Practice location data", "category": "Practice/Reference"},
                {"name": "License Providers", "description": "Licensed provider information", "category": "Practice/Reference"},
                {"name": "Referring Providers", "description": "Referring provider information", "category": "Practice/Reference"},
                {"name": "Master Insurances", "description": "Insurance plan definitions", "category": "Practice/Reference"},
                {"name": "Resources/staff members", "description": "Staff/resource data", "category": "Practice/Reference"},
                {"name": "Patient Employers", "description": "Employer information", "category": "Patient Administrative"},
                {"name": "Patient Demographics", "description": "Patient demographic data", "category": "Patient Administrative"},
                {"name": "Patient Guarantors", "description": "Guarantor information", "category": "Patient Administrative"},
                {"name": "Patient Contacts", "description": "Contact persons", "category": "Patient Administrative"},
                {"name": "Patient Pharmacies", "description": "Pharmacy preferences", "category": "Patient Administrative"},
                {"name": "Patient Insurances", "description": "Patient-specific insurance", "category": "Insurance"},
                {"name": "Past Appointments", "description": "Historical appointments", "category": "Scheduling"},
                {"name": "Patient Notes", "description": "Clinical notes", "category": "Clinical"},
                {"name": "Patient Alerts (Billing etc.)", "description": "Billing and other alerts", "category": "Administrative"},
                {"name": "Patient Medications", "description": "Medication records", "category": "Clinical"},
                {"name": "Patient Allergies", "description": "Allergy records", "category": "Clinical"},
                {"name": "Patient Diagnosis", "description": "Diagnosis records", "category": "Clinical"},
                {"name": "Future Appointments", "description": "Scheduled future appointments", "category": "Scheduling"}
            ],
            "total_worksheets": 18,
            "field_level_documentation": False,
            "column_names_documented": False,
            "data_types_documented": False,
            "relationships_documented": False,
            "value_sets_documented": False,
            "sample_data_provided": False
        },

        "medical_records_folder": {
            "folder_name": "Medical Records",
            "organization": "Sub-folder per patient, organized by MR Number",
            "file_types": [
                {
                    "filename_pattern": "CCD.xml",
                    "format": "XML",
                    "description": "Used for viewing/importing patient information within supported EMR systems",
                    "category": "Clinical Summary"
                },
                {
                    "filename_pattern": "CCD.html",
                    "format": "HTML",
                    "description": "A human readable version of the CCD",
                    "category": "Clinical Summary"
                },
                {
                    "filename_pattern": "Demographics_*_MedicalHistory.pdf",
                    "format": "PDF",
                    "description": "A report that contains a snapshot summary of the patient's demographic and insurance information",
                    "category": "Demographics"
                },
                {
                    "filename_pattern": "MedicalHx_*_MedicalHistory.pdf",
                    "format": "PDF",
                    "description": "A report that contains a snapshot summary of the patient's active medications, chronic problems, and active allergies",
                    "category": "Clinical Summary"
                },
                {
                    "filename_pattern": "Encounter_<yyyyMMdd>_<hhmm>_<type>.pdf",
                    "format": "PDF",
                    "description": "One or more files that contain the generated summary for the associated encounter",
                    "category": "Encounters"
                },
                {
                    "filename_pattern": "Document_<type>_<name>.pdf",
                    "format": "PDF",
                    "description": "One or more files that contain a document that was uploaded to the patient's chart",
                    "category": "Documents"
                },
                {
                    "filename_pattern": "LabResult_<yyyyMMdd>_<hhmm>_<guid>.pdf",
                    "format": "PDF",
                    "description": "One or more files that contain the e-lab results that were received for the patient",
                    "category": "Lab Results"
                },
                {
                    "filename_pattern": "Form_<yyyyMMdd>_<hhmm>_<type>_<name>.rtf",
                    "format": "RTF",
                    "description": "One or more files that contain a custom user form that was generated for the patient",
                    "category": "Custom Forms"
                }
            ],
            "total_file_types": 8
        }
    }
}

# Summary statistics
stats = {
    "total_xlsx_worksheets": export_doc["bulk_export"]["xlsx_workbook"]["total_worksheets"],
    "total_per_patient_file_types": export_doc["bulk_export"]["medical_records_folder"]["total_file_types"],
    "total_documented_fields": 0,  # No field-level documentation exists
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "fields_with_value_sets": 0,
    "data_dictionary_present": False,
    "sample_data_present": False,
    "machine_readable_schema_present": False,

    "worksheet_categories": {
        "Practice/Reference": {
            "count": 5,
            "worksheets": ["Locations", "License Providers", "Referring Providers", "Master Insurances", "Resources/staff members"]
        },
        "Patient Administrative": {
            "count": 5,
            "worksheets": ["Patient Employers", "Patient Demographics", "Patient Guarantors", "Patient Contacts", "Patient Pharmacies"]
        },
        "Insurance": {
            "count": 1,
            "worksheets": ["Patient Insurances"]
        },
        "Scheduling": {
            "count": 2,
            "worksheets": ["Past Appointments", "Future Appointments"]
        },
        "Clinical": {
            "count": 3,
            "worksheets": ["Patient Notes", "Patient Medications", "Patient Allergies", "Patient Diagnosis"]
        },
        "Administrative": {
            "count": 1,
            "worksheets": ["Patient Alerts (Billing etc.)"]
        }
    },

    "single_patient_selectable_categories": 9,
    "single_patient_output_format": "PDF (non-structured)",
    "bulk_export_self_service": False,
    "documentation_pages": 4
}

# Save full inventory
output = {
    "export_documentation": export_doc,
    "summary_statistics": stats
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print("=== ReLiMed EMR Export Documentation Summary ===")
print(f"Source: {export_doc['source_file']} ({export_doc['pages']} pages, {export_doc['size_bytes']:,} bytes)")
print(f"Created: {export_doc['created']} by {export_doc['author']}")
print()
print("--- Single Patient Export ---")
print(f"  Format: PDF")
print(f"  Access: Self-service via Patient Chart menu")
print(f"  Selectable categories: {len(export_doc['single_patient_export']['selectable_categories'])}")
for cat in export_doc['single_patient_export']['selectable_categories']:
    print(f"    - {cat['name']}")
print()
print("--- Bulk (All Patient) Export ---")
print(f"  Access: Vendor-assisted (contact support)")
print(f"  Delivery: Password-protected ZIP via SFTP")
print(f"  XLSX Worksheets: {export_doc['bulk_export']['xlsx_workbook']['total_worksheets']}")
for ws in export_doc['bulk_export']['xlsx_workbook']['worksheets']:
    print(f"    - {ws['name']} ({ws['category']})")
print(f"  Per-patient file types: {export_doc['bulk_export']['medical_records_folder']['total_file_types']}")
for ft in export_doc['bulk_export']['medical_records_folder']['file_types']:
    print(f"    - {ft['filename_pattern']} ({ft['format']})")
print()
print("--- Documentation Quality ---")
print(f"  Field-level documentation: NO")
print(f"  Column names documented: NO")
print(f"  Data types documented: NO")
print(f"  Relationships documented: NO")
print(f"  Value sets documented: NO")
print(f"  Sample data provided: NO")
print(f"  Machine-readable schema: NO")
print()
print("Output saved to: full-entity-inventory.json")
