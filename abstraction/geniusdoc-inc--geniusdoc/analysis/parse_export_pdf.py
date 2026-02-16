#!/usr/bin/env python3
"""Parse the GeniusDoc EHI export PDF and produce structured JSON output.

The PDF is a 2-page document (page 2 blank) with 6 export categories.
Since there's no data dictionary, field names, or schema, we extract
the category-level information that exists.
"""

import json
import subprocess
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/geniusdoc-inc--geniusdoc/downloads/GeniusDoc_Data_Export.pdf"

# Extract PDF metadata
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
pdf_info_lines = result.stdout.strip().split("\n")
pdf_metadata = {}
for line in pdf_info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_metadata[key.strip()] = val.strip()

# Extract PDF text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
pdf_text = result.stdout.strip()

# Parse the 6 export categories from the text
categories = [
    {
        "number": 1,
        "name": "Demographics and Insurance",
        "format": "Excel",
        "description": "Comprehensive patient demographics and insurance details.",
        "fields_documented": 0,
        "field_names_listed": False,
        "types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
    },
    {
        "number": 2,
        "name": "Medications and Allergies",
        "format": "Excel",
        "description": "Patient medications and allergies details.",
        "fields_documented": 0,
        "field_names_listed": False,
        "types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
    },
    {
        "number": 3,
        "name": "Problems",
        "format": "Excel",
        "description": "The active patient diagnosis.",
        "fields_documented": 0,
        "field_names_listed": False,
        "types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
        "notes": "Only 'active' diagnoses mentioned — resolved/historical diagnoses not mentioned.",
    },
    {
        "number": 4,
        "name": "Lab Results",
        "format": "Excel",
        "description": "Structured patient lab results.",
        "fields_documented": 0,
        "field_names_listed": False,
        "types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
    },
    {
        "number": 5,
        "name": "Visit Summaries",
        "format": "PDF, CDA (HL7), Excel (reference link document)",
        "description": "All the details of each encounter. Exported in PDF and CDA format. A reference link document is provided in Excel.",
        "fields_documented": 0,
        "field_names_listed": False,
        "types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
        "notes": "CDA format mentioned but no CDA template or profile specified.",
    },
    {
        "number": 6,
        "name": "Documents",
        "format": "Original file formats, Excel (reference/index file)",
        "description": "All scanned or imported documents in the patient chart. A reference file provides document index, file information, folder names and patient details.",
        "fields_documented": 0,
        "field_names_listed": False,
        "types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
    },
]

output = {
    "vendor": "GeniusDoc, Inc.",
    "product": "GeniusDoc 12.0",
    "artifact": "GeniusDoc_Data_Export.pdf",
    "artifact_metadata": {
        "pages": int(pdf_metadata.get("Pages", 0)),
        "file_size_bytes": int(pdf_metadata.get("File size", "0").replace(" bytes", "")),
        "author": pdf_metadata.get("Author", ""),
        "creator": pdf_metadata.get("Creator", ""),
        "creation_date": pdf_metadata.get("CreationDate", ""),
        "content_pages": 1,  # Page 2 is blank
    },
    "export_categories": categories,
    "summary_statistics": {
        "total_categories": len(categories),
        "total_fields_documented": 0,
        "total_field_names_listed": 0,
        "categories_with_field_detail": 0,
        "categories_with_type_info": 0,
        "categories_with_relationships": 0,
        "categories_with_value_sets": 0,
        "categories_with_sample_data": 0,
        "formats_used": ["Excel", "PDF", "CDA (HL7)"],
    },
    "documentation_assessment": {
        "has_data_dictionary": False,
        "has_field_names": False,
        "has_field_types": False,
        "has_field_descriptions": False,
        "has_relationships": False,
        "has_value_sets": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_export_instructions": False,
        "has_export_process_description": False,
        "documentation_level": "category-level only",
    },
    "raw_text": pdf_text,
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/geniusdoc-inc--geniusdoc/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Wrote structured output to {output_path}")
print(f"\nSummary:")
print(f"  PDF pages: {output['artifact_metadata']['pages']} ({output['artifact_metadata']['content_pages']} with content)")
print(f"  Export categories: {output['summary_statistics']['total_categories']}")
print(f"  Fields documented: {output['summary_statistics']['total_fields_documented']}")
print(f"  Field names listed: {output['summary_statistics']['total_field_names_listed']}")
print(f"  Formats: {', '.join(output['summary_statistics']['formats_used'])}")
print(f"  Has data dictionary: {output['documentation_assessment']['has_data_dictionary']}")
print(f"  Has schema: {output['documentation_assessment']['has_schema']}")
print(f"  Has sample data: {output['documentation_assessment']['has_sample_data']}")
