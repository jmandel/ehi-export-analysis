#!/usr/bin/env python3
"""Parse the StreamlineMD EHI Export PDF and produce structured JSON output."""

import json
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/streamlinemd-llc--streamlinemd-ehr/downloads/StreamlineMD-EHR-EHI-Export.pdf"
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "pdf-extraction.json")

# Get PDF metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH], capture_output=True, text=True
)
metadata = {}
for line in info_result.stdout.strip().split("\n"):
    if ":" in line:
        key, _, val = line.partition(":")
        metadata[key.strip()] = val.strip()

# Extract text
text_result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True
)
full_text = text_result.stdout

# Parse into pages
pages = full_text.split("\f")
pages = [p.strip() for p in pages if p.strip()]

# Identify bullet points on page 2
bullet_points = []
current_bullet = []
for line in pages[1].split("\n") if len(pages) > 1 else []:
    stripped = line.strip()
    if stripped.startswith("•"):
        if current_bullet:
            bullet_points.append(" ".join(current_bullet))
        current_bullet = [stripped.lstrip("• ").strip()]
    elif current_bullet and stripped:
        current_bullet.append(stripped)
if current_bullet:
    bullet_points.append(" ".join(current_bullet))

output = {
    "source_file": "StreamlineMD-EHR-EHI-Export.pdf",
    "source_url": "https://streamlinemd.com/wp-content/uploads/2023/10/StreamlineMD-EHR-EHI-Export.pdf",
    "pdf_metadata": {
        "author": metadata.get("Author", ""),
        "creator": metadata.get("Creator", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": int(metadata.get("File size", "0").split()[0]),
    },
    "content_summary": {
        "page_1": "Title page: StreamlineMD EHR Version 15.0, 170.315 (b)(10) Electronic Health Information Export",
        "page_2": "Company summary + 3 bullet points describing C-CDA/PDF export using USCDI v1",
    },
    "export_description": {
        "formats": ["C-CDA", "PDF"],
        "standard": "USCDI v1",
        "scope_options": ["single patient", "multiple patients", "entire population"],
        "delivery_method": "file export to user-selected folder",
        "developer_intervention_required": False,
    },
    "bullet_points": bullet_points,
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "field_level_documentation": False,
    "entities_documented": 0,
    "fields_documented": 0,
    "full_text": full_text,
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"Output written to {OUTPUT_PATH}")
print(f"Pages: {output['pdf_metadata']['pages']}")
print(f"Bullet points found: {len(bullet_points)}")
print(f"Data dictionary: {output['data_dictionary_present']}")
print(f"Entities documented: {output['entities_documented']}")
print(f"Fields documented: {output['fields_documented']}")
