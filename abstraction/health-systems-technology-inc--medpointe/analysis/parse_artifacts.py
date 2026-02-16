#!/usr/bin/env python3
"""Parse all EHI export artifacts for MedPointe and produce structured inventory."""

import json
import os
from datetime import datetime

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/health-systems-technology-inc--medpointe"
DOWNLOADS_DIR = os.path.join(RESULTS_DIR, "downloads")
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/health-systems-technology-inc--medpointe/analysis"

def analyze_pdf():
    """Analyze the sole EHI export PDF document."""
    pdf_path = os.path.join(DOWNLOADS_DIR, "Providers - Exporting Computer Readable Documents.pdf")
    size = os.path.getsize(pdf_path)
    
    # PDF text was extracted; analyze its content
    pdf_text = """Exporting Documents Using the C62 File Format

There are multiple ways to export a document from a patient's chart. This can be done for a
single document of a single patient, for selected documents in a patient's chart or as a batch
process to export the documents from multiple patients' charts at the same time.

Exporting a Single Document
To export a single document, from the patient's chart, click on the document in the patient's
TOC (Table of Contents). Once viewing the document, use the right-click menu to select Export
via C62.

Exporting a Chart (or Multiple Documents in a Chart)
To export an entire chart of a single patient, open the chart within the Clinical window. From
the Overview Page, select Export Chart from the right-click menu.

This opens the Export Chart window:
From here, enter a date range (if desired) and select the type of documents you want included
in the extract. Select Export to C62 file and click OK.

Exporting Multiple Charts
To export multiple charts at the same time, from the Main Menu, click on Tools, then Clinical,
then Export, then select the patient criteria you want included in the batch (e.g., by last name
range, by date of birth, by patient classification, by provider, etc.), select the types of
documents you want included and the date range, then click OK."""

    # Document type checkboxes visible in export dialog (from PDF screenshot)
    export_dialog_document_types = [
        "Cover Sheet",
        "Notes",
        "Text Documents",
        "Scanned/Faxed Documents",
        "Include Restricted Documents"
    ]

    # Output options in export dialog
    export_output_options = [
        "Print",
        "Export to Folder",
        "Export to C62 file"
    ]

    # Export submenu items visible in right-click context menu (from PDF page 1 screenshot)
    export_submenu_items = [
        "Patient Portal: Update Chart",
        "Patient Portal: Password Reset",
        "Export Continuity of Care",
        "Export Chart",  # highlighted - this is the C62 export
        "Export Continuity of Care - Referral",
        "Export Continuity of Care - Batch",
        "Export Immunization Data",
        "Export Syndromic Data",
        "Export Medical Records"
    ]

    # Other right-click menu items visible (showing product capabilities)
    other_menu_items = [
        "Patient Communicator",
        "Send Message via Portal",
        "Send Secure E-Mail",
        "Patient Info",
        "Alert",
        "Referrals",
        "Print",
        "Activate Phone",
        "Patient Questionnaires",
        "Form Completion Library",
        "Import",
        "Export",
        "Print Med List",
        "Preventive Care Info",
        "Preventive Care Exceptions",
        "Treatment Goals",
        "Document Queue",
        "Refill Management",
        "Correspondence Set-Up",
        "Edit Form",
        "Exit Clinical Window"
    ]

    # Batch export filter criteria mentioned in text
    batch_export_criteria = [
        "Last name range",
        "Date of birth",
        "Patient classification",
        "Provider"
    ]

    return {
        "artifact": "Providers - Exporting Computer Readable Documents.pdf",
        "source_url": "https://downloads.hstcentral.com/helpdocs/Exporting%20Documents/Providers%20-%20Exporting%20Computer%20Readable%20Documents.pdf",
        "size_bytes": size,
        "pages": 2,
        "author": "Tim Schmidt",
        "created": "2023-11-16",
        "title": "Microsoft Word - Exporting Documents via C62",
        "content_analysis": {
            "export_format": "C62 (proprietary, undocumented)",
            "export_methods": [
                {
                    "name": "Single Document Export",
                    "description": "Right-click document in patient TOC, select 'Export via C62'",
                    "scope": "single_document"
                },
                {
                    "name": "Chart Export",
                    "description": "From patient Overview Page, right-click → Export Chart. Dialog allows date range, document type selection, output option selection.",
                    "scope": "single_patient_multiple_documents"
                },
                {
                    "name": "Batch Export",
                    "description": "Main Menu → Tools → Clinical → Export. Select patient criteria, document types, date range.",
                    "scope": "multiple_patients"
                }
            ],
            "export_dialog_document_types": export_dialog_document_types,
            "export_output_options": export_output_options,
            "export_submenu_items": export_submenu_items,
            "batch_export_criteria": batch_export_criteria,
            "other_menu_items_visible": other_menu_items
        },
        "documentation_gaps": {
            "no_data_dictionary": True,
            "no_schema": True,
            "no_field_definitions": True,
            "no_format_specification": True,
            "no_sample_data": True,
            "no_value_sets": True,
            "no_relationships": True,
            "no_billing_data_mentioned": True,
            "no_structured_clinical_data_mentioned": True,
            "c62_format_undocumented": True
        }
    }


def analyze_help_page():
    """Analyze the help documents page."""
    return {
        "artifact": "help-documents-page.png",
        "source_url": "https://hstspot.com/help-documents.php",
        "type": "screenshot",
        "page_title": "Medpointe Customer Help NOW",
        "last_published": "2020-03-27",
        "categories": {
            "Exporting Documents": {
                "file_count": 1,
                "files": ["Providers - Exporting Computer Readable Documents.pdf"]
            },
            "Tutorials": {
                "file_count": 12,
                "files": [
                    "C00-Welcome.mp4",
                    "C01-Clinical-Tour.mp4",
                    "C02-Visit-Intro.mp4",
                    "C03-HPI.mp4",
                    "C04-Document-Exam.mp4",
                    "C05-Text-Fields.mp4",
                    "C06-Exam-Wizard.mp4",
                    "C07-Plan.mp4",
                    "C08-Meds.mp4",
                    "C09-Instructions.mp4",
                    "C10-Finishing-A-Note.mp4",
                    "C11-Checkin Process.mp4"
                ]
            },
            "e-Prescribing": {
                "file_count": 7,
                "files": [
                    "Adding a New Medication.pdf",
                    "E-Prescribing Controlled Substances.pdf",
                    "EPCS Token Set-Up.pdf",
                    "Electronic Refill Requests - Provider.pdf",
                    "Electronic Refill Requests - Staff Filing.pdf",
                    "Electronic Refill Requests - Staff Follow-up.pdf",
                    "Troubleshooting MedicationScript Issues.pdf"
                ]
            }
        },
        "total_help_documents": 20,
        "ehi_export_specific_documents": 1
    }


def build_full_inventory():
    """Build the full artifact inventory with analysis."""
    pdf_analysis = analyze_pdf()
    page_analysis = analyze_help_page()

    inventory = {
        "product": "MedPointe",
        "developer": "Health Systems Technology, Inc.",
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "artifacts_reviewed": [pdf_analysis, page_analysis],
        "summary": {
            "total_artifacts": 2,
            "primary_artifact": "Providers - Exporting Computer Readable Documents.pdf",
            "total_pages_of_documentation": 2,
            "data_dictionary_present": False,
            "schema_present": False,
            "sample_data_present": False,
            "entities_documented": 0,
            "fields_documented": 0,
            "fields_with_descriptions": 0,
            "export_format": "C62 (proprietary, undocumented)",
            "document_types_in_export": 5,  # Cover Sheet, Notes, Text Documents, Scanned/Faxed, Restricted
            "export_methods": 3,  # single, chart, batch
            "export_submenu_options_visible": 9  # from screenshot
        },
        "notes": [
            "The PDF's screenshots reveal a right-click Export submenu with 9 options including "
            "'Export Medical Records', 'Export Continuity of Care', 'Export Immunization Data', "
            "and 'Export Syndromic Data' — but the documentation only describes the 'Export Chart' "
            "option with C62 format. The other export options are undocumented.",
            "The C62 format is completely undocumented — no schema, no field list, no specification. "
            "Web searches return zero results for this format in healthcare contexts.",
            "The export dialog only shows document-type categories (Cover Sheet, Notes, Text Documents, "
            "Scanned/Faxed Documents). There is no indication that structured data (diagnoses, meds, "
            "labs, vitals, billing) is included in the export.",
            "No data dictionary exists — zero entities, zero fields documented.",
            "The help page was last published 2020-03-27; the PDF was created 2023-11-16."
        ]
    }

    return inventory


if __name__ == "__main__":
    inventory = build_full_inventory()
    output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote inventory to {output_path}")
    print(f"Total artifacts: {inventory['summary']['total_artifacts']}")
    print(f"Data dictionary present: {inventory['summary']['data_dictionary_present']}")
    print(f"Entities documented: {inventory['summary']['entities_documented']}")
    print(f"Fields documented: {inventory['summary']['fields_documented']}")
    print(f"Export format: {inventory['summary']['export_format']}")
