#!/usr/bin/env python3
"""Parse the OMS EHR EHI Export Data Format PDF and produce structured JSON inventory."""

import json
import subprocess
import re
import sys
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "EHI-Export-Data-Format.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", str(PDF_PATH), "-"],
    capture_output=True, text=True
)
text = result.stdout

# Extract PDF metadata
info = subprocess.run(
    ["pdfinfo", str(PDF_PATH)],
    capture_output=True, text=True
)
metadata_lines = info.stdout.strip().split("\n")
pdf_metadata = {}
for line in metadata_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_metadata[key.strip()] = val.strip()

# Parse the table from page 2
# The table has two columns: Function and Doc Type
entries = []
# Pattern: function name followed by doc type(s)
table_rows = [
    ("CCDA", "XML, HTML"),
    ("Notes", "HTML"),
    ("C3 Notes", "HTML"),
    ("Labs", "XML, HTML"),
    ("Labs Scanned", "PDF"),
    ("Diagnostics", "Discrete fields, PDF"),
    ("Scanned documents", "PDF"),
    ("Smart Forms", "HTML"),
    ("Messages", "Discrete fields"),
]

# Verify each row appears in the extracted text
for func, doc_type in table_rows:
    if func not in text:
        print(f"WARNING: '{func}' not found in PDF text", file=sys.stderr)

for func, doc_type in table_rows:
    formats = [f.strip() for f in doc_type.split(",")]
    entries.append({
        "entity_name": func,
        "export_formats": formats,
        "fields": [],  # No fields documented
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": None,
    })

# Build the full inventory
inventory = {
    "source_file": "downloads/EHI-Export-Data-Format.pdf",
    "source_url": "https://objectivemedicalsystems.com/wp-content/uploads/2025/09/EHI-Export-Data-Format.pdf",
    "pdf_metadata": {
        "author": pdf_metadata.get("Author", ""),
        "creator": pdf_metadata.get("Creator", ""),
        "creation_date": pdf_metadata.get("CreationDate", ""),
        "modification_date": pdf_metadata.get("ModDate", ""),
        "pages": int(pdf_metadata.get("Pages", 0)),
    },
    "document_note": "Documents sourced from outside will be exported in the same format it was received.",
    "total_entities": len(entries),
    "total_fields": 0,
    "total_fields_with_descriptions": 0,
    "total_fields_with_types": 0,
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False,
    "entities": entries,
}

# Write full inventory
out_path = Path(__file__).parent / "entity-inventory-full.json"
with open(out_path, "w") as f:
    json.dump(inventory, f, indent=2)
print(f"Wrote {out_path}")

# Write summary
summary = {
    "source_file": inventory["source_file"],
    "total_entities": inventory["total_entities"],
    "total_fields": inventory["total_fields"],
    "total_fields_with_descriptions": inventory["total_fields_with_descriptions"],
    "total_fields_with_types": inventory["total_fields_with_types"],
    "has_data_dictionary": inventory["has_data_dictionary"],
    "has_field_definitions": inventory["has_field_definitions"],
    "has_sample_data": inventory["has_sample_data"],
    "has_schema": inventory["has_schema"],
    "format_breakdown": {},
    "entities_by_format": {},
}

for e in entries:
    for fmt in e["export_formats"]:
        summary["format_breakdown"][fmt] = summary["format_breakdown"].get(fmt, 0) + 1
        if fmt not in summary["entities_by_format"]:
            summary["entities_by_format"][fmt] = []
        summary["entities_by_format"][fmt].append(e["entity_name"])

summary_path = Path(__file__).parent / "entity-inventory-summary.json"
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {summary_path}")

# Print summary stats
print(f"\n=== Summary ===")
print(f"Total export categories: {len(entries)}")
print(f"Total documented fields: 0 (no field-level documentation)")
print(f"Format breakdown:")
for fmt, count in summary["format_breakdown"].items():
    print(f"  {fmt}: {count} categories")
print(f"Has data dictionary: No")
print(f"Has sample data: No")
