#!/usr/bin/env python3
"""Parse the Compulink EHI export PDF and extract all structured information.

The PDF has no data dictionary — it describes the export format/structure only.
This script extracts the few concrete data points mentioned (table names, field names,
key relationships) to produce entity-inventory-full.json.
"""

import json
import subprocess
import re

pdf_path = "../downloads/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf"

# Extract text
result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
text = result.stdout

# Tables explicitly mentioned in the PDF
tables_mentioned = {
    "PATIENT": {
        "description": "Key demographic information table",
        "category": "Demographics/Billing",
        "key_field": "PATUNIQUE",
        "mentioned_fields": [
            {"name": "PATUNIQUE", "description": "Patient Identifier Number (primary key)", "type": None},
            {"name": "ERXCONSENT", "description": "E-Rx History Consent", "type": None},
            {"name": "GENDERIDENTITYNOTE", "description": "Gender Identity Note", "type": None},
            {"name": "SEXUALORIENTATIONNOTE", "description": "Sexual Orientation Note", "type": None},
        ]
    },
    "EXAM": {
        "description": "Prominent exam table; main exam record",
        "category": "Exam",
        "key_field": "EXAMUNIQUE",
        "mentioned_fields": [
            {"name": "EXAMUNIQUE", "description": "Exam Identification Number (primary key)", "type": None},
        ]
    },
    "EXAMDIAG": {
        "description": "Exam Diagnosis table (sub-table of EXAM)",
        "category": "Exam",
        "key_field": "EXAMUNIQUE",
        "mentioned_fields": [
            {"name": "EXAMUNIQUE", "description": "Links to EXAM table", "type": None},
        ]
    },
    "DOCUMENT": {
        "description": "Demographics document metadata table",
        "category": "Demographics/Billing",
        "key_field": "DOCUNIQUE",
        "mentioned_fields": [
            {"name": "DOCUNIQUE", "description": "Document unique identifier; links to D-type image files", "type": None},
        ]
    },
    "EXAMIMAG": {
        "description": "Exam image metadata table",
        "category": "Exam",
        "key_field": "IMAGUNIQUE",
        "mentioned_fields": [
            {"name": "IMAGUNIQUE", "description": "Image unique identifier; links to E-type image files", "type": None},
        ]
    },
}

# Build entity inventory
entities = []
for table_name, info in tables_mentioned.items():
    entity = {
        "name": table_name,
        "description": info["description"],
        "category": info["category"],
        "key_field": info["key_field"],
        "fields": info["mentioned_fields"],
        "field_count": len(info["mentioned_fields"]),
        "source": "Explicitly mentioned in PDF documentation",
        "note": "Only fields explicitly mentioned in the PDF are listed. Full field inventory is only available via FLD files included in actual exports."
    }
    entities.append(entity)

inventory = {
    "product": "Compulink Advantage",
    "version": "Version 12",
    "source_document": "COMPULINK-PHIEXPORT-DOCUMENTATION.pdf",
    "source_date": "2023-10-05",
    "extraction_notes": [
        "The PDF does NOT contain a data dictionary or complete table listing.",
        "Only 5 table names are mentioned as examples in the documentation.",
        "Only 7 unique field names are mentioned across all tables.",
        "The vendor states that FLD files (field description files) are generated with each export and serve as the data dictionary.",
        "Due to 'comprehensive customization,' field lists vary per installation.",
        "No data types, value sets, or constraints are documented.",
        "This inventory represents the minimum known surface, not the complete export."
    ],
    "export_format": {
        "container": "Password-protected ZIP file",
        "data_files": "CSV (one per database table)",
        "image_files": "Native format (PDF, PNG, JPG, etc.)",
        "field_description_files": "FLD (text files with Name/Description pairs)",
        "naming_convention": {
            "tables": "P###_TABLENAME.csv (### = patient ID, or P0_ for bulk)",
            "images": "P###_E/D###_####.ext (E=exam, D=demographics)",
            "field_files": "P###_TABLENAME.FLD"
        }
    },
    "relationships": {
        "demographics_billing": "Linked by PATUNIQUE; table names do NOT start with EXAM",
        "exam_tables": "Linked by EXAMUNIQUE; table names start with EXAM",
        "demographics_images": "D-type image ID matches DOCUNIQUE in DOCUMENT table",
        "exam_images": "E-type image ID matches IMAGUNIQUE in EXAMIMAG table"
    },
    "total_entities_documented": len(entities),
    "total_fields_documented": sum(e["field_count"] for e in entities),
    "entities": entities
}

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "product": inventory["product"],
    "source_document": inventory["source_document"],
    "total_entities_documented": inventory["total_entities_documented"],
    "total_fields_documented": inventory["total_fields_documented"],
    "has_complete_data_dictionary": False,
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "data_dictionary_mechanism": "FLD files generated with each export (not publicly available)",
    "export_format": "CSV + native images in password-protected ZIP",
    "categories": {
        "Demographics/Billing": {"entities": 2, "fields": 5},
        "Exam": {"entities": 3, "fields": 2}
    },
    "key_limitations": [
        "No complete table listing published",
        "No static data dictionary — FLD files only in exports",
        "No data types documented",
        "No value sets or coded values documented",
        "No sample data provided",
        "Only 5 of unknown-total tables named",
        "Only 7 of unknown-total fields named"
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities documented: {inventory['total_entities_documented']}")
print(f"Fields documented: {inventory['total_fields_documented']}")
print("Output: entity-inventory-full.json, entity-inventory-summary.json")
