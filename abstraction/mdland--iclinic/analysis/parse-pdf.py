#!/usr/bin/env python3
"""Parse the ehiexport.pdf and extract structured information about the EHI export documentation."""

import subprocess
import json

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/ehiexport.pdf", "-"],
    capture_output=True, text=True
)
pdf_text = result.stdout

# Extract PDF metadata
info_result = subprocess.run(
    ["pdfinfo", "../downloads/ehiexport.pdf"],
    capture_output=True, text=True
)
pdf_info = {}
for line in info_result.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_info[key.strip()] = val.strip()

# Document what the PDF contains
analysis = {
    "file": "ehiexport.pdf",
    "source_url": "https://mdland.net/static/docs/ehiexport.pdf",
    "metadata": {
        "author": pdf_info.get("Author", ""),
        "creator": pdf_info.get("Creator", ""),
        "creation_date": pdf_info.get("CreationDate", ""),
        "pages": int(pdf_info.get("Pages", 0)),
        "file_size_bytes": int(pdf_info.get("File size", "0").replace(" bytes", "")),
    },
    "content_summary": {
        "regulation_reference": "§170.315(b)(10)",
        "export_format": "XML in password-protected ZIP",
        "format_standard_reference": "https://www.w3.org/TR/xml/",
        "export_scope_options": [
            "All Patients",
            "All Active Patients",
            "Patient with Encounter",
            "Patient with DOB",
            "Specify Patient [Single Patient]"
        ],
        "export_mechanism": "UI-driven (Settings → Advanced → Patient Data Export)",
        "processing": "Server-side by MDLand IT (10 minutes to hours)",
        "access_control": "Restricted to authorized users via Advanced Settings",
        "workflow_steps": 4,
    },
    "documentation_gaps": {
        "has_data_dictionary": False,
        "has_xml_schema": False,
        "has_xsd_or_dtd": False,
        "has_sample_data": False,
        "has_field_definitions": False,
        "has_entity_list": False,
        "has_relationship_docs": False,
        "has_value_sets": False,
        "has_data_type_docs": False,
        "has_namespace_docs": False,
    },
    "entities": [],
    "fields": [],
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
}

# Save analysis
with open("pdf-analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

print(f"PDF: {analysis['metadata']['pages']} pages, {analysis['metadata']['file_size_bytes']} bytes")
print(f"Author: {analysis['metadata']['author']}")
print(f"Created: {analysis['metadata']['creation_date']}")
print(f"Export format: {analysis['content_summary']['export_format']}")
print(f"Data dictionary: {'Yes' if analysis['documentation_gaps']['has_data_dictionary'] else 'No'}")
print(f"XML schema: {'Yes' if analysis['documentation_gaps']['has_xml_schema'] else 'No'}")
print(f"Sample data: {'Yes' if analysis['documentation_gaps']['has_sample_data'] else 'No'}")
print(f"Entities documented: {analysis['total_entities']}")
print(f"Fields documented: {analysis['total_fields']}")
