#!/usr/bin/env python3
"""Parse the Strateq-Export.pdf and produce a structured JSON inventory of its content."""

import json
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
DOWNLOADS = os.path.join(REPO_ROOT, "results/strateq-health-inc--strateqehr/downloads")
PDF_PATH = os.path.join(DOWNLOADS, "Strateq-Export.pdf")
OUTPUT_DIR = SCRIPT_DIR

# Extract PDF metadata
info = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True).stdout
text = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True).stdout

# Parse pdfinfo
meta = {}
for line in info.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip()

# Parse text into paragraphs
paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]

# Build inventory
inventory = {
    "source_file": "Strateq-Export.pdf",
    "source_url": "https://strateqhealth.com/wp-content/uploads/2023/12/Strateq-Export.pdf",
    "pdf_metadata": {
        "title": meta.get("Title", ""),
        "pages": int(meta.get("Pages", "0")),
        "creation_date": meta.get("CreationDate", ""),
        "file_size_bytes": int(meta.get("File size", "0").replace(" bytes", "")),
        "page_size": meta.get("Page size", ""),
        "producer": meta.get("Producer", ""),
    },
    "content": {
        "total_paragraphs": len(paragraphs),
        "total_sentences": sum(p.count(".") for p in paragraphs),
        "paragraphs": paragraphs,
    },
    "export_description": {
        "product_name": "StrateqEHR",
        "product_version": "5",
        "export_format": "ZIP archive",
        "export_contents": [
            "Per-encounter C-CDA documents (in ZIP sub-archives)",
            "Attached files (PDF, images)",
        ],
        "data_dictionary_present": False,
        "field_definitions_present": False,
        "schema_present": False,
        "sample_data_present": False,
        "export_instructions_present": False,
        "entity_count": 0,
        "field_count": 0,
        "fields_with_descriptions": 0,
    },
    "analysis_notes": [
        "3 of 6 sentences are generic definitions of file formats (ZIP, PDF, C-CDA)",
        "No data dictionary, schema, or field-level documentation of any kind",
        "Export is C-CDA based — a clinical summary standard, not a native database export",
        "No mention of billing, revenue cycle, orders, eMAR, or other non-clinical data",
        "No information about how to initiate the export or access constraints",
        "Document created from 'Microsoft Word - Export.docx' — appears hastily produced",
    ],
}

# This serves as the full-entity-inventory since there are no entities documented
output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Wrote inventory to {output_path}")
print(f"PDF pages: {inventory['pdf_metadata']['pages']}")
print(f"Paragraphs: {inventory['content']['total_paragraphs']}")
print(f"Entities documented: {inventory['export_description']['entity_count']}")
print(f"Fields documented: {inventory['export_description']['field_count']}")
