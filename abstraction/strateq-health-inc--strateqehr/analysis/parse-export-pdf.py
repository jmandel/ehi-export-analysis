#!/usr/bin/env python3
"""Parse the StrateqEHR EHI export PDF and extract all content.

The PDF is a single page with 6 sentences — no data dictionary, no tables,
no field definitions. This script extracts the full text and produces
structured JSON output documenting exactly what's there (and what isn't).
"""

import json
import subprocess
import sys

PDF_PATH = "../downloads/Strateq-Export.pdf"

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
raw_text = result.stdout.strip()

# Extract metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)
metadata_lines = info_result.stdout.strip().split("\n")
metadata = {}
for line in metadata_lines:
    if ":" in line:
        key, _, val = line.partition(":")
        metadata[key.strip()] = val.strip()

# Parse sentences
lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
# First line is the product header
header = lines[0] if lines else ""
sentences = lines[1:] if len(lines) > 1 else []

# Categorize sentences
definitional = []
substantive = []
for s in sentences:
    # Sentences that just define file formats
    if any(s.startswith(prefix) for prefix in ["ZIP is", "PDF or Portable", "C-CDA or Consolidated"]):
        definitional.append(s)
    else:
        substantive.append(s)

output = {
    "source_file": "downloads/Strateq-Export.pdf",
    "pdf_metadata": {
        "pages": int(metadata.get("Pages", 0)),
        "page_size": metadata.get("Page size", ""),
        "created": metadata.get("CreationDate", ""),
        "producer": metadata.get("Producer", ""),
        "title": metadata.get("Title", ""),
    },
    "content": {
        "header": header,
        "total_sentences": len(sentences),
        "definitional_sentences": len(definitional),
        "substantive_sentences": len(substantive),
        "all_sentences": sentences,
        "definitional": definitional,
        "substantive": substantive,
    },
    "data_dictionary": {
        "present": False,
        "entities": 0,
        "fields": 0,
        "descriptions": 0,
    },
    "export_description": {
        "format": "ZIP containing per-encounter C-CDA ZIP archives and attached files (PDFs, images)",
        "mechanism": "Not documented",
        "scope": "Patient chart data — no specifics provided",
        "data_domains_mentioned": ["C-CDA clinical data", "attached PDFs", "attached images"],
        "data_domains_not_mentioned": [
            "billing/revenue cycle",
            "claims",
            "charges",
            "eMAR",
            "orders (detail)",
            "ED tracking",
            "dynamic form data",
            "perioperative data",
            "HIM data",
            "scheduling",
            "insurance/eligibility",
            "implantable devices",
        ],
    },
    "assessment": {
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_export_instructions": False,
        "has_screenshots": False,
        "documentation_word_count": len(raw_text.split()),
    },
}

with open("pdf-analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
