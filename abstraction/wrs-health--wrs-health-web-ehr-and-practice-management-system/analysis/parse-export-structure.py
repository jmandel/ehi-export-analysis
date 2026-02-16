#!/usr/bin/env python3
"""Parse the WRS Health EHI Export PDF documentation and extract the export structure.

The PDF describes a ZIP file with CSV files, a C-CDA XML, HTML notes, and document
attachments. There is NO field-level data dictionary — only file-level descriptions.
This script produces the entity inventory from what's documented.
"""

import json

# Export components as described in the PDF (pages 5-7)
# No column-level detail is provided for any CSV file.
export_entities = [
    {
        "entity_name": "BillingReport.csv",
        "format": "CSV",
        "category": "Billing",
        "description": "Financial transactions with the provider. Includes patient information, transaction dates, charges, claims, and the description of transactions made with status.",
        "fields": [],
        "field_count": None,  # No field-level documentation
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "No column names, types, or value sets documented. Only a prose description of general content."
    },
    {
        "entity_name": "CCDA.xml",
        "format": "XML (C-CDA / USCDI v1)",
        "category": "Clinical",
        "description": "XML file export of a patient's clinical data. Complies with HL7 C-CDA and USCDI Version 1 requirements. Specifications obtainable from HL7 website.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "Standard C-CDA per USCDI v1. No vendor-specific extensions or additional mappings documented. No profile detail beyond the reference to HL7 spec."
    },
    {
        "entity_name": "demographics.csv",
        "format": "CSV",
        "category": "Demographics",
        "description": "Patient's key information, identification details, contact information, insurance information.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "No column names, types, or value sets documented."
    },
    {
        "entity_name": "schedule.csv",
        "format": "CSV",
        "category": "Scheduling / Encounters",
        "description": "Record of patient's encounters with specific information including appointment date, provider, location, appointment type, workflow, notes, and date on which notes are recorded.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "No column names, types, or value sets documented. Mentions ~7 conceptual data points in prose."
    },
    {
        "entity_name": "PatientDocumentFiles.csv",
        "format": "CSV",
        "category": "Documents",
        "description": "Mapping file listing patient documents/attachments contained in the Documents folder.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "No column names or types documented."
    },
    {
        "entity_name": "Documents/",
        "format": "Various (PDF, DOCX, XLS, XML, HTML, DAT, JPG, GIF, PNG, etc.)",
        "category": "Documents",
        "description": "Folder containing patient's supporting documents/attachments, lab results, and documents uploaded by the practice. Filename convention references patient name and patient ID.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "Raw file attachments. No structured data dictionary."
    },
    {
        "entity_name": "Notes/ (HTML encounter notes)",
        "format": "HTML + CSS/JS/images",
        "category": "Clinical Notes",
        "description": "Encounter notes from patient visits. Each note is an HTML file with accompanying CSS, images, and JavaScript for readable formatting. Filename references patient name, ID, date, and note type.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "Rendered HTML notes — narrative clinical content, not structured/computable data."
    },
    {
        "entity_name": "Notes/PatientNoteFiles.csv",
        "format": "CSV",
        "category": "Clinical Notes",
        "description": "Mapping file listing all patient notes generated during the export.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "No column names or types documented."
    },
    {
        "entity_name": "Notes/NOTES.LOG",
        "format": "Text log",
        "category": "Clinical Notes",
        "description": "Log of successfully exported notes and any notes that encountered errors during export.",
        "fields": [],
        "field_count": None,
        "fields_described": 0,
        "has_field_names": False,
        "has_field_types": False,
        "notes": "Export process log, not patient data."
    }
]

# Full inventory
full_inventory = {
    "product": "WRS Health Web EHR and Practice Management System",
    "version": "7.0",
    "documentation_version": "1.0",
    "documentation_date": "2023-10-14",
    "source_artifact": "downloads/170.315-b10-EHI-Export.pdf",
    "total_export_components": len(export_entities),
    "structured_data_files": 5,  # BillingReport, CCDA, demographics, schedule, PatientDocumentFiles
    "csv_files": 4,  # BillingReport, demographics, schedule, PatientDocumentFiles (+ PatientNoteFiles)
    "total_documented_fields": 0,
    "fields_with_names": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "notes": "The PDF provides ONLY file-level descriptions. No column names, data types, value sets, or field-level documentation exists for any of the CSV files. The C-CDA is referenced as standard USCDI v1 with no vendor-specific detail.",
    "entities": export_entities
}

# Summary
summary = {
    "product": full_inventory["product"],
    "total_export_components": full_inventory["total_export_components"],
    "structured_data_files": full_inventory["structured_data_files"],
    "total_documented_fields": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "categories": {},
    "format_breakdown": {}
}

for e in export_entities:
    cat = e["category"]
    fmt = e["format"].split(" ")[0]  # First word
    summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
    summary["format_breakdown"][fmt] = summary["format_breakdown"].get(fmt, 0) + 1

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Generated entity-inventory-full.json and entity-inventory-summary.json")
print(f"  Total export components: {len(export_entities)}")
print(f"  Structured data files: {full_inventory['structured_data_files']}")
print(f"  Documented fields: 0 (no data dictionary)")
print(f"  Categories: {summary['categories']}")
