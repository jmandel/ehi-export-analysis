#!/usr/bin/env python3
"""Parse the StreamlineMD EHI Export PDF and extract structured content.

The PDF is a 2-page document with minimal content: a title page and three
bullet points describing C-CDA/PDF export using USCDI v1. There is no data
dictionary, schema, or field-level documentation to parse.

This script extracts whatever structured information exists and outputs it
as JSON for the entity inventory (which will be essentially empty).
"""

import json
import subprocess
import sys

pdf_path = "../downloads/StreamlineMD-EHR-EHI-Export.pdf"

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", pdf_path, "-"],
    capture_output=True, text=True
)
raw_text = result.stdout

# Extract metadata
info_result = subprocess.run(
    ["pdfinfo", pdf_path],
    capture_output=True, text=True
)
metadata_lines = info_result.stdout.strip().split("\n")
metadata = {}
for line in metadata_lines:
    if ":" in line:
        key, _, value = line.partition(":")
        metadata[key.strip()] = value.strip()

# Structure findings
analysis = {
    "artifact": "StreamlineMD-EHR-EHI-Export.pdf",
    "pages": int(metadata.get("Pages", "0")),
    "author": metadata.get("Author", ""),
    "creation_date": metadata.get("CreationDate", ""),
    "creator": metadata.get("Creator", ""),
    "file_size_bytes": 155440,
    "content_summary": {
        "page_1": "Title page: StreamlineMD EHR Version 15.0, 170.315 (b)(10) Electronic Health Information Export",
        "page_2": "Company description + 3 bullet points describing C-CDA/PDF export with USCDI v1"
    },
    "export_description": {
        "formats": ["C-CDA", "PDF"],
        "standard": "USCDI v1",
        "scope_options": ["Single patient", "Multiple patients", "Entire population"],
        "delivery": "File export to user-selected folder",
        "developer_intervention_required": False
    },
    "documentation_elements": {
        "data_dictionary": False,
        "field_definitions": False,
        "schema": False,
        "sample_data": False,
        "screenshots": False,
        "export_instructions": False,
        "value_sets": False,
        "relationships": False,
        "error_handling": False
    },
    "entities_defined": 0,
    "fields_defined": 0,
    "raw_text": raw_text.strip()
}

# Write analysis output
with open("pdf-analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

print(json.dumps(analysis, indent=2))
