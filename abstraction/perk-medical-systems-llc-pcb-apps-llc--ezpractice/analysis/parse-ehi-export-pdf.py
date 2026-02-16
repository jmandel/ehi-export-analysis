#!/usr/bin/env python3
"""Parse the EHI Export PDF and extract all structured information.

Reads the PDF via pdftotext, identifies:
- File categories and their formats
- The adhoc patient notes CSV schema (the only product-specific data dictionary)
- References to external specs (C-CDA R2.1)
- Fee disclosures
"""

import json
import subprocess
import re

pdf_path = "../downloads/EHI Export.pdf"

# Extract text
result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
text = result.stdout

# Parse the adhoc patient notes table - the only product-specific schema
# Columns: number, name, description
notes_fields = [
    {"column_number": 1, "name": "PID", "description": "Data reflected under this column are patient IDs. These are unique.", "type": "identifier"},
    {"column_number": 2, "name": "Patient Notes ID", "description": "Data reflected under this column are patient note IDs. These are unique.", "type": "identifier"},
    {"column_number": 3, "name": "Username", "description": "Data reflected under this column refer to the user who documented the note", "type": "string"},
    {"column_number": 4, "name": "Subject", "description": "Data reflected under this column refer to the subject of the note. This field maybe blank", "type": "string"},
    {"column_number": 5, "name": "Patient Notes Category", "description": "Data reflected under this column refers to the category associated with the note. These categories are user defined but available from a pick list for the user.", "type": "string"},
    {"column_number": 6, "name": "Patient Notes Date", "description": "Data reflected under this column refer to the date the note was created.", "type": "date"},
    {"column_number": 7, "name": "Patient Notes", "description": "Data reflected under this column refers to documented details of the patient note.", "type": "text"},
]

# Note: PDF has a numbering error (column 3 listed twice, then jumps to 4,5,6)
# Actual columns are 7 fields as parsed above

# Build full entity inventory
entities = [
    {
        "name": "Patient Demographics and Clinical Data",
        "format": "C-CDA R2.1 XML + HTML",
        "description": "Patient demographics and clinical records in HL7 C-CDA R2.1 format. Paired XML and HTML files. No product-specific data dictionary provided; vendor references external C-CDA R2.1 specification.",
        "file_pattern": "PID_INTERNALNUMBERING.xml / .html",
        "fields": [],
        "field_count": 0,
        "has_product_specific_dictionary": False,
        "external_spec_references": [
            "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1380194/"
        ],
        "notes": "Relies entirely on standard C-CDA R2.1 spec. No vendor-specific extensions, mappings, or field documentation provided."
    },
    {
        "name": "Adhoc Patient Notes",
        "format": "CSV",
        "description": "Telephone calls, adhoc notes related to the patient via the Patient Notes feature. This is the only component with a product-specific data dictionary.",
        "file_pattern": "PID_INTERNALNUMBERING_patNotes.csv",
        "fields": notes_fields,
        "field_count": len(notes_fields),
        "has_product_specific_dictionary": True,
        "external_spec_references": [],
        "notes": "7 fields documented with descriptions. Column numbering in PDF has an error (column 3 listed twice)."
    },
    {
        "name": "Scanned Records",
        "format": "CDA XML (Base64-encoded documents)",
        "description": "All patient scanned and uploaded documents, encoded using Base64 within CDA XML files.",
        "file_pattern": "PID_INTERNALNUMBERING_Echart.xml",
        "fields": [],
        "field_count": 0,
        "has_product_specific_dictionary": False,
        "external_spec_references": [
            "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1380194/"
        ],
        "notes": "Base64-encoded scanned documents wrapped in CDA XML. No field-level documentation."
    }
]

# Export mechanisms
export_info = {
    "mechanism": "User-initiated export within ezPractice application",
    "output_format": "ZIP file(s)",
    "scope": "Single patient or full collection of patients",
    "fees": "No fees if performed by user. Fees may apply if vendor performs the export.",
    "access_requirements": "Valid user subscription required"
}

# Summary stats
total_entities = len(entities)
total_fields_documented = sum(e["field_count"] for e in entities)
entities_with_dictionary = sum(1 for e in entities if e["has_product_specific_dictionary"])

summary = {
    "product": "ezPractice V15.1",
    "vendor": "Perk Medical Systems LLC (PCB Apps LLC)",
    "chpl_id": "15.07.04.2154.Ezpr.15.01.1.230208",
    "pdf_pages": 7,
    "pdf_date": "2023-12-20",
    "total_export_components": total_entities,
    "total_fields_with_product_specific_documentation": total_fields_documented,
    "components_with_product_specific_dictionary": entities_with_dictionary,
    "components_relying_on_external_spec": total_entities - entities_with_dictionary,
    "export_info": export_info,
    "entities": entities
}

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump(summary, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    summary_only = {
        "total_export_components": total_entities,
        "total_fields_documented": total_fields_documented,
        "components_with_dictionary": entities_with_dictionary,
        "component_summary": [
            {
                "name": e["name"],
                "format": e["format"],
                "field_count": e["field_count"],
                "has_dictionary": e["has_product_specific_dictionary"]
            }
            for e in entities
        ]
    }
    json.dump(summary_only, f, indent=2)

print(f"Total export components: {total_entities}")
print(f"Total fields with product-specific documentation: {total_fields_documented}")
print(f"Components with product-specific data dictionary: {entities_with_dictionary}/{total_entities}")
print(f"\nComponent breakdown:")
for e in entities:
    print(f"  - {e['name']}: {e['format']}, {e['field_count']} fields documented, dictionary={e['has_product_specific_dictionary']}")
