#!/usr/bin/env python3
"""
Parse the EHI export structure from the PDF documentation.

The PDF describes 7 file components in the export ZIP but provides NO field-level
data dictionary. We extract what's described at the file/component level.

Source: downloads/Electronic_Health_Information_Export.pdf (10 pages)
"""

import json
import subprocess
import re

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "downloads/Electronic_Health_Information_Export.pdf", "-"],
    capture_output=True, text=True, cwd=".."
)
pdf_text = result.stdout

# The export components as described in the PDF (pages 5-6)
# These are identical for single-patient and multi-patient exports
export_components = [
    {
        "entity_name": "Documents",
        "format": "CDA XML (folder)",
        "description": "CDA XML DOC Export file containing the 'Documents' folder containing patient's supporting documents or attachments when available.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Clinical Documents",
        "notes": "Folder of CDA XML files; no field-level schema provided"
    },
    {
        "entity_name": "Notes",
        "format": "CDA XML (folder)",
        "description": "CDA XML DOC Export file folder containing all the notes recorded during the patient's previous medical visits/encounters.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Clinical Documents",
        "notes": "Folder of CDA XML files; no field-level schema provided"
    },
    {
        "entity_name": "BillingReport",
        "format": "CSV",
        "description": "CSV file containing the patient's financial transactions with their provider. The information includes the patient information, transaction dates, charges, claims and the description of transactions made with status.",
        "fields": [
            {"name": "patient information", "type": "unknown", "description": "Patient identifying information", "source": "prose description"},
            {"name": "transaction dates", "type": "unknown", "description": "Dates of financial transactions", "source": "prose description"},
            {"name": "charges", "type": "unknown", "description": "Charge amounts", "source": "prose description"},
            {"name": "claims", "type": "unknown", "description": "Claims data", "source": "prose description"},
            {"name": "description of transactions", "type": "unknown", "description": "Description of transactions made", "source": "prose description"},
            {"name": "status", "type": "unknown", "description": "Transaction status", "source": "prose description"},
        ],
        "field_count": 6,
        "fields_with_descriptions": 6,
        "fields_with_types": 0,
        "category": "Billing",
        "notes": "Fields inferred from prose description only; no CSV header or schema provided"
    },
    {
        "entity_name": "CCDA",
        "format": "XML (HL7 C-CDA)",
        "description": "XML file export of a patient's clinical data. The system allows exports of HL7 CCDA which complies with United States Core Data for Interoperability (USCDI), Version 1 requirements. The specifications for the CCDA can be obtained from the HL7 website.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Clinical Summary",
        "notes": "Standard C-CDA; vendor defers to HL7 spec for field definitions. Covers USCDI v1 data classes (problems, medications, allergies, labs, vitals, procedures, immunizations, etc.)"
    },
    {
        "entity_name": "demographics",
        "format": "CSV",
        "description": "CSV file that contains the patient's key information, identification details, contact information, insurance information etc.",
        "fields": [
            {"name": "key information", "type": "unknown", "description": "Patient key/identifying information", "source": "prose description"},
            {"name": "identification details", "type": "unknown", "description": "Patient identification details", "source": "prose description"},
            {"name": "contact information", "type": "unknown", "description": "Patient contact information", "source": "prose description"},
            {"name": "insurance information", "type": "unknown", "description": "Patient insurance information", "source": "prose description"},
        ],
        "field_count": 4,
        "fields_with_descriptions": 4,
        "fields_with_types": 0,
        "category": "Demographics",
        "notes": "Fields inferred from prose description only; no CSV header or schema provided"
    },
    {
        "entity_name": "PatientDocumentFiles",
        "format": "CSV",
        "description": "CSV mapping file that contains the list of patient's documents. This file outlines the contents of the patient's supporting attachments contained in the 'Documents' folder.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Clinical Documents",
        "notes": "Mapping/index file for the Documents folder; no field-level schema provided"
    },
    {
        "entity_name": "Schedule",
        "format": "CSV",
        "description": "CSV file that contains a record of the patient's encounters with specific information including appointment date, provider, location, appointment type, workflow, notes and date on which notes are recorded.",
        "fields": [
            {"name": "appointment date", "type": "unknown", "description": "Date of appointment/encounter", "source": "prose description"},
            {"name": "provider", "type": "unknown", "description": "Provider for the encounter", "source": "prose description"},
            {"name": "location", "type": "unknown", "description": "Location of the encounter", "source": "prose description"},
            {"name": "appointment type", "type": "unknown", "description": "Type of appointment", "source": "prose description"},
            {"name": "workflow", "type": "unknown", "description": "Workflow information", "source": "prose description"},
            {"name": "notes", "type": "unknown", "description": "Notes associated with the encounter", "source": "prose description"},
            {"name": "date on which notes are recorded", "type": "unknown", "description": "Date notes were recorded", "source": "prose description"},
        ],
        "field_count": 7,
        "fields_with_descriptions": 7,
        "fields_with_types": 0,
        "category": "Encounters/Scheduling",
        "notes": "Fields inferred from prose description only; no CSV header or schema provided"
    },
]

# Additional optional components mentioned on page 7
optional_components = [
    {
        "entity_name": "Custom Patient Data Tables",
        "format": "Embedded in CDA XML",
        "description": "Custom (user-created) Patient Data Tables are included as part of the CDA whenever the export is done using the Batch CDA option, unless the custom Patient Data Table is set to be excluded as FHR.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Custom Data",
        "notes": "Variable content depending on facility configuration; included in CDA by default"
    },
    {
        "entity_name": "Chart Documents",
        "format": "Mixed (TIF, other)",
        "description": "Optionally included chart documents and attachments. Includes option to show sticky notes on TIF documents.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Clinical Documents",
        "notes": "Optional inclusion via checkbox; scanned documents and images"
    },
]

all_components = export_components + optional_components

# Build the full inventory
inventory = {
    "source": "downloads/Electronic_Health_Information_Export.pdf",
    "source_pages": 10,
    "source_version": "2.0",
    "source_date": "October 24, 2023",
    "export_format": "ZIP containing C-CDA XML + CSV files + document folders",
    "has_data_dictionary": False,
    "has_field_level_schema": False,
    "has_sample_data": False,
    "total_entities": len(all_components),
    "total_fields_documented": sum(c["field_count"] for c in all_components),
    "fields_from_prose_only": True,
    "entities": all_components,
}

# Write full inventory
with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "total_entities": inventory["total_entities"],
    "total_fields_documented": inventory["total_fields_documented"],
    "fields_with_descriptions": sum(c["fields_with_descriptions"] for c in all_components),
    "fields_with_types": sum(c["fields_with_types"] for c in all_components),
    "has_data_dictionary": False,
    "has_field_level_schema": False,
    "has_sample_data": False,
    "all_field_types_unknown": True,
    "categories": {},
    "formats": {},
}

for c in all_components:
    cat = c["category"]
    if cat not in summary["categories"]:
        summary["categories"][cat] = {"entity_count": 0, "field_count": 0}
    summary["categories"][cat]["entity_count"] += 1
    summary["categories"][cat]["field_count"] += c["field_count"]
    
    fmt = c["format"]
    if fmt not in summary["formats"]:
        summary["formats"][fmt] = 0
    summary["formats"][fmt] += 1

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== Entity Inventory Summary ===")
print(f"Total entities/components: {inventory['total_entities']}")
print(f"Total fields documented (from prose): {inventory['total_fields_documented']}")
print(f"Has data dictionary: {inventory['has_data_dictionary']}")
print(f"Has field-level schema: {inventory['has_field_level_schema']}")
print(f"Has sample data: {inventory['has_sample_data']}")
print()
print("By category:")
for cat, info in summary["categories"].items():
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
print()
print("By format:")
for fmt, count in summary["formats"].items():
    print(f"  {fmt}: {count} entities")
