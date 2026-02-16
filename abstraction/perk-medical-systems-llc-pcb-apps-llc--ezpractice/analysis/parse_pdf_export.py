#!/usr/bin/env python3
"""Parse the EHI Export PDF and extract structured data about the export format."""

import json
import subprocess
import re

PDF_PATH = "../../../results/perk-medical-systems-llc-pcb-apps-llc--ezpractice/downloads/EHI Export.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
pdf_text = result.stdout

# Extract PDF metadata
info_result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)

# Parse the CSV column table from the PDF text
# The table describes the adhoc patient notes CSV format
csv_columns = []
# Look for the column definitions in the text
col_pattern = re.compile(r'^\s+(\d+)\s+([\w\s]+?)\s{2,}(.+?)$', re.MULTILINE)
for match in col_pattern.finditer(pdf_text):
    col_num = match.group(1).strip()
    col_name = match.group(2).strip()
    desc = match.group(3).strip()
    csv_columns.append({
        "column_number_as_printed": int(col_num),
        "column_name": col_name,
        "description": desc
    })

# Build structured output
export_doc = {
    "source_file": "EHI Export.pdf",
    "pages": 7,
    "created": "2023-12-20",
    "product": "ezPractice V15.1",
    "chpl_id": "15.07.04.2154.Ezpr.15.01.1.230208",
    "product_portfolio": [
        "Certified Health Information Technology – EHR",
        "Practice Management",
        "Patient Portal",
        "Health Information Exchange"
    ],
    "services": [
        "Revenue Cycle Management",
        "Professional Services"
    ],
    "export_mechanism": {
        "format": "ZIP file(s)",
        "scope": "Single patient or full collection of patients",
        "self_service": True,
        "vendor_assisted": True,
        "fees": "No fees for self-service; vendor-assisted may incur fees"
    },
    "file_naming_convention": {
        "pattern1": "PID_INTERNALNUMBERING.EXT",
        "pattern2": "PID_INTERNALNUMBERING_TYPE.EXT",
        "fields": {
            "PID": "Patient ID (unique number)",
            "INTERNALNUMBERING": "Internal control number (can be ignored)",
            "TYPE": "Content descriptor: 'Claim Data', 'Echart', or 'patNotes'",
            "EXT": "File extension: XML (with HTML pair) or CSV"
        }
    },
    "export_categories": [
        {
            "name": "Patient Demographics and Clinical Data",
            "format": "HL7 C-CDA R2.1",
            "file_extension": "XML + HTML pair",
            "type_value": None,
            "documentation_level": "Defers to C-CDA R2.1 specification",
            "references": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1380194/",
                "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447"
            ],
            "field_count": 0,
            "field_descriptions": 0,
            "notes": "No ezPractice-specific field documentation; relies entirely on C-CDA standard"
        },
        {
            "name": "Adhoc Patient Notes",
            "format": "CSV",
            "file_extension": "CSV",
            "type_value": "patNotes",
            "documentation_level": "Field-level descriptions provided",
            "field_count": 7,
            "field_descriptions": 7,
            "fields": csv_columns,
            "notes": "Column numbering in PDF is incorrect (3 appears twice); actual columns are 7"
        },
        {
            "name": "Scanned Records",
            "format": "HL7 CDA with Base64 encoding",
            "file_extension": "XML",
            "type_value": "Echart",
            "documentation_level": "Defers to HL7 CDA specification",
            "references": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1380194",
                "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447"
            ],
            "field_count": 0,
            "field_descriptions": 0,
            "notes": "Contains Base64-encoded scanned/uploaded documents; may be large"
        },
        {
            "name": "Claim Data",
            "format": "Unknown",
            "file_extension": "Unknown",
            "type_value": "Claim Data",
            "documentation_level": "Mentioned in filename convention only; no format documentation",
            "field_count": 0,
            "field_descriptions": 0,
            "notes": "TYPE value 'Claim Data' listed in naming convention but completely undocumented"
        }
    ],
    "total_documented_fields": 7,
    "total_fields_with_descriptions": 7,
    "data_dictionary_present": False,
    "sample_data_present": False,
    "machine_readable_schema": False,
    "documented_file_types_mentioned": ["Claim Data", "Echart", "patNotes"]
}

# Write outputs
with open("full-entity-inventory.json", "w") as f:
    json.dump(export_doc, f, indent=2)

# Summary stats
stats = {
    "pdf_pages": 7,
    "substantive_pages": "~3 (pages 4-6)",
    "export_categories": len(export_doc["export_categories"]),
    "categories_with_field_documentation": 1,
    "total_documented_fields": 7,
    "total_fields_with_descriptions": 7,
    "description_rate": "100% (of the 7 documented fields)",
    "undocumented_categories": ["Patient Demographics/Clinical (defers to C-CDA)", "Scanned Records (defers to CDA)", "Claim Data (no documentation at all)"],
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "export_format": "Mixed: C-CDA R2.1 XML + CSV + CDA XML",
    "export_scope": "Single patient or bulk",
    "fees": "None for self-service"
}

with open("summary-stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("=== EHI Export PDF Analysis ===")
print(f"Pages: {export_doc['pages']}")
print(f"Export categories: {len(export_doc['export_categories'])}")
print(f"Total documented fields: {export_doc['total_documented_fields']}")
print(f"Fields with descriptions: {export_doc['total_fields_with_descriptions']}")
print(f"Data dictionary: {export_doc['data_dictionary_present']}")
print(f"Sample data: {export_doc['sample_data_present']}")
print(f"Machine-readable schema: {export_doc['machine_readable_schema']}")
print()
print("Export categories:")
for cat in export_doc["export_categories"]:
    print(f"  - {cat['name']}: {cat['format']} ({cat['field_count']} fields documented)")
print()
print("Product portfolio mentions:")
for p in export_doc["product_portfolio"]:
    print(f"  - {p}")
print()
print("CSV columns parsed from PDF:")
for col in csv_columns:
    print(f"  #{col['column_number_as_printed']}: {col['column_name']} - {col['description']}")
