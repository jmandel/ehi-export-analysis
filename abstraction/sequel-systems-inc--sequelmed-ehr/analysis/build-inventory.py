#!/usr/bin/env python3
"""
Build entity inventory from the SequelMed EHI export documentation.

Since the documentation provides NO data dictionary, NO field-level detail,
and NO schema, we can only document the export at the file/folder level
as described in the PDF. The C-CDA content is governed by external HL7
specifications (not product-specific documentation).
"""

import json
import os

# The export contains three components, none with field-level documentation
entities = [
    {
        "entity_name": "C-CDA Clinical Document",
        "source_file": "Clinical folder (ZIP contents)",
        "format": "C-CDA XML (CDA R2, Consolidated CDA Templates R2.1)",
        "vendor_category": "Clinical Data",
        "description": "One XML-based C-CDA file per patient. Vendor states compliance with USCDI Version 1. No product-specific field mapping, extensions, or constraints documented.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "C-CDA is an external standard; the vendor provides no documentation of which C-CDA sections/templates are populated or what product-specific data maps to which C-CDA elements. A standard C-CDA R2.1 would typically include: Allergies, Encounters, Immunizations, Medications, Problems, Procedures, Results, Vital Signs, Plan of Treatment, Goals, Health Concerns, Assessment, Social History, and Functional Status sections."
    },
    {
        "entity_name": "Patient Documents",
        "source_file": "Documents folder (ZIP contents)",
        "format": "Original upload format (.jpg, .gif, .bmp, .png, .pdf, .txt)",
        "vendor_category": "Patient Documents",
        "description": "Patient documents exported in their original upload/scan format. Includes signed progress notes, lab results, radiology reports, scanned documents, imported documents, and uploaded documents.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "document_types": [
            "Signed progress notes",
            "Available lab results",
            "Radiology reports",
            "Scanned documents",
            "Imported documents",
            "Uploaded documents"
        ],
        "notes": "Unstructured files with no metadata documentation. No field-level detail about document properties (dates, authors, types, etc.)."
    },
    {
        "entity_name": "Patient Documents Detail",
        "source_file": "Patient Documents Detail.xls (ZIP contents)",
        "format": "XLS (Excel)",
        "vendor_category": "Patient Documents",
        "description": "Excel file included in export. No documentation of its contents, columns, or purpose is provided anywhere in the vendor's documentation.",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "Completely undocumented. Likely a document manifest but this is speculative."
    }
]

# Summary
summary = {
    "product": "SequelMed EHR V12",
    "vendor": "Sequel Systems, Inc.",
    "documentation_source": "SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf (4 pages, 96,891 bytes)",
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "export_format": "ZIP per patient containing C-CDA XML + document files + XLS",
    "categories": {
        "Clinical Data": {
            "entity_count": 1,
            "field_count": 0,
            "description": "C-CDA XML file - no product-specific field documentation"
        },
        "Patient Documents": {
            "entity_count": 2,
            "field_count": 0,
            "description": "Document files + undocumented XLS manifest"
        }
    },
    "notes": "The vendor provides NO data dictionary, NO field-level documentation, NO schema, and NO sample data. The entire export documentation is ~1.5 pages of actual content describing the export at the file/folder level only. The clinical data component relies entirely on the external C-CDA specification with no product-specific mapping."
}

# Write full inventory
full_path = os.path.join(os.path.dirname(__file__), "entity-inventory-full.json")
with open(full_path, "w") as f:
    json.dump({"entities": entities, "summary": summary}, f, indent=2)

# Write summary
summary_path = os.path.join(os.path.dirname(__file__), "entity-inventory-summary.json")
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total entities: {len(entities)}")
print(f"Total fields documented: 0")
print(f"Data dictionary: None")
print(f"Written: {full_path}")
print(f"Written: {summary_path}")
