#!/usr/bin/env python3
"""
Parse the WRS Health EHI Export PDF to extract the documented export file structure.
Since there is no field-level data dictionary, this script captures the file-level
inventory that the vendor provides and produces a structured JSON representation.
"""

import json

# The PDF documents these export components (extracted from pdftotext output and visual inspection)
export_structure = {
    "export_name": "ehi_documents.zip",
    "format": "ZIP archive",
    "vendor": "WRS Health",
    "product": "WRS Health Web EHR and Practice Management System",
    "version": "7.0",
    "document_version": "1.0",
    "document_date": "2023-10-14",
    "source_pdf": "170.315-b10-EHI-Export.pdf",
    "source_pdf_pages": 8,
    "source_pdf_size_bytes": 1122095,
    "components": [
        {
            "name": "BillingReport.csv",
            "format": "CSV",
            "category": "Billing",
            "description": "Financial transactions with provider. Includes patient information, transaction dates, charges, claims and the description of transactions made with status.",
            "field_documentation": "none",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "patient information",
                "transaction dates",
                "charges",
                "claims",
                "description of transactions",
                "status"
            ]
        },
        {
            "name": "CCDA.xml",
            "format": "XML (C-CDA)",
            "category": "Clinical",
            "description": "XML file export of patient's clinical data. HL7 CCDA compliant with USCDI Version 1 requirements.",
            "field_documentation": "none (refers to HL7 specification)",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "clinical data (USCDI v1)",
                "allergies",
                "encounters",
                "lab results",
                "procedures"
            ],
            "standard_reference": "HL7 C-CDA, USCDI v1"
        },
        {
            "name": "demographics.csv",
            "format": "CSV",
            "category": "Demographics",
            "description": "Patient's key information, identification details, contact information, insurance information etc.",
            "field_documentation": "none",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "key information",
                "identification details",
                "contact information",
                "insurance information"
            ]
        },
        {
            "name": "schedule.csv",
            "format": "CSV",
            "category": "Scheduling/Encounters",
            "description": "Record of the patient's encounters with specific information including appointment date, provider, location, appointment type, workflow, notes and date on which notes are recorded.",
            "field_documentation": "none",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "appointment date",
                "provider",
                "location",
                "appointment type",
                "workflow",
                "notes",
                "date on which notes are recorded"
            ]
        },
        {
            "name": "PatientDocumentFiles.csv",
            "format": "CSV",
            "category": "Index/Mapping",
            "description": "CSV mapping file that contains the list of patient documents. Outlines contents of supporting attachments in the Documents folder.",
            "field_documentation": "none",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "list of patient documents",
                "document mapping"
            ]
        },
        {
            "name": "Documents/",
            "format": "Mixed (PDF, DOCX, XLS, XML, HTML, DAT, JPG, GIF, PNG)",
            "category": "Documents/Attachments",
            "description": "Folder containing patient's supporting documents or attachments when available - attachments, lab results, any documents uploaded to the patient's account.",
            "field_documentation": "N/A (raw files)",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "attachments",
                "lab results",
                "uploaded documents"
            ],
            "filename_convention": "References patient's name, patient ID"
        },
        {
            "name": "Notes/",
            "format": "HTML (with CSS/JS/images)",
            "category": "Clinical Notes",
            "description": "Encounter notes created during patient visits. Each note in HTML format with CSS, images, and JavaScript for readable formatting.",
            "field_documentation": "N/A (rendered HTML)",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "encounter notes",
                "visit notes",
                "specialty notes (ENT, dermatology, internal medicine)"
            ],
            "filename_convention": "References patient name, patient ID, date of encounter, note type",
            "observed_note_types_in_screenshots": [
                "VISIT_NOTE_II",
                "ENT_NOTE",
                "DERMATOLOGY_NOTE",
                "INTERNAL_MEDICINE_NOTE"
            ]
        },
        {
            "name": "Notes/PatientNoteFiles.csv",
            "format": "CSV",
            "category": "Index/Mapping",
            "description": "CSV mapping file that contains a list of patient notes generated during the export.",
            "field_documentation": "none",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "list of patient notes"
            ]
        },
        {
            "name": "Notes/NOTES.LOG",
            "format": "Text",
            "category": "Export Metadata",
            "description": "Data file containing logs of successfully exported notes as well as any notes that encountered errors during the export process.",
            "field_documentation": "N/A",
            "fields_listed": 0,
            "fields_described": 0,
            "documented_content_hints": [
                "export success logs",
                "export error logs"
            ]
        }
    ]
}

# Compute summary statistics
total_components = len(export_structure["components"])
csv_files = [c for c in export_structure["components"] if c["format"] == "CSV"]
structured_data_files = [c for c in export_structure["components"] if c["format"] == "CSV" and c["category"] not in ("Index/Mapping", "Export Metadata")]
total_fields_documented = sum(c["fields_listed"] for c in export_structure["components"])
total_fields_described = sum(c["fields_described"] for c in export_structure["components"])

summary = {
    "total_export_components": total_components,
    "csv_files_count": len(csv_files),
    "structured_data_files_count": len(structured_data_files),
    "total_fields_documented": total_fields_documented,
    "total_fields_with_descriptions": total_fields_described,
    "has_field_level_data_dictionary": False,
    "has_schema_files": False,
    "has_sample_data": False,
    "has_value_sets": False,
    "has_relationship_documentation": False,
    "export_formats": ["CSV", "XML (C-CDA)", "HTML", "Mixed document formats"],
    "data_categories_in_export": [
        "Billing (BillingReport.csv)",
        "Demographics (demographics.csv)",
        "Scheduling/Encounters (schedule.csv)",
        "Clinical summary (CCDA.xml - USCDI v1)",
        "Clinical Notes (HTML encounter notes)",
        "Documents/Attachments (raw files)"
    ],
    "documentation_quality": {
        "file_level_descriptions": True,
        "field_level_descriptions": False,
        "data_types": False,
        "value_sets": False,
        "foreign_keys": False,
        "sample_data": False,
        "machine_readable_schema": False
    }
}

export_structure["summary"] = summary

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/wrs-health--wrs-health-web-ehr-and-practice-management-system/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(export_structure, f, indent=2)

print(json.dumps(summary, indent=2))
print(f"\nFull inventory written to: {output_path}")
