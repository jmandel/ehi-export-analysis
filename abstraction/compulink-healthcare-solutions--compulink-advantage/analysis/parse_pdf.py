#!/usr/bin/env python3
"""Parse the Compulink EHI Export PDF and extract all structured information."""

import json
import subprocess
import re
import sys

PDF_PATH = "../../../results/compulink-healthcare-solutions--compulink-advantage/downloads/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf"

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
full_text = result.stdout

# Extract PDF metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)
metadata = {}
for line in info_result.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Parse document structure
sections = []
current_section = None
for line in full_text.split("\n"):
    # Match section headers like "1. Introduction", "2. Understanding the Files"
    m = re.match(r'^\s*(\d+)\.\s+(.+)', line)
    if m and len(m.group(2).strip()) > 3:
        if current_section:
            sections.append(current_section)
        current_section = {
            "number": m.group(1),
            "title": m.group(2).strip(),
            "content_lines": []
        }
    elif current_section:
        stripped = line.strip()
        if stripped and not stripped.startswith("ONC Cures"):
            current_section["content_lines"].append(stripped)

if current_section:
    sections.append(current_section)

# Extract explicitly mentioned table names
table_names = set()
table_patterns = [
    r'_([A-Z]+)\.csv',
    r'_([A-Z]+)\.CSV',
    r'\*_([A-Z]+)\.csv',
    r'([A-Z]+)\s+table',
]
for pattern in table_patterns:
    for m in re.finditer(pattern, full_text):
        name = m.group(1)
        if name not in ("CSV", "FLD", "ZIP", "PDF", "PNG", "JPG", "PHI", "EHI", "ONC", "EHR", "API"):
            table_names.add(name)

# Extract explicitly mentioned field names
field_names = []
for m in re.finditer(r'Name:\s*(\w+),\s*Description:\s*(.+)', full_text):
    field_names.append({
        "name": m.group(1),
        "description": m.group(2).strip()
    })

# Extract key identifiers mentioned
key_fields = []
for m in re.finditer(r'(\w+UNIQUE)\b', full_text):
    key_fields.append(m.group(1))
key_fields = sorted(set(key_fields))

# Extract file naming conventions
naming_conventions = []
for m in re.finditer(r'(P###_[^\s.]+)', full_text):
    naming_conventions.append(m.group(1))

# Count pages by content type
pages = full_text.split("\f")
page_analysis = []
for i, page in enumerate(pages, 1):
    stripped = page.strip()
    word_count = len(stripped.split())
    if word_count < 20:
        ptype = "blank/title"
    elif "Usage Terms" in stripped or "Indemnification" in stripped or "Limitation of Liability" in stripped:
        ptype = "legal/terms"
    elif "Contents" in stripped and i <= 3:
        ptype = "table_of_contents"
    else:
        ptype = "technical_content"
    page_analysis.append({
        "page": i,
        "type": ptype,
        "word_count": word_count
    })

# Build output
output = {
    "pdf_metadata": {
        "author": metadata.get("Author", ""),
        "creator": metadata.get("Creator", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": int(metadata.get("File size", "0").split()[0]),
        "encrypted": metadata.get("Encrypted", "") == "yes"
    },
    "page_analysis": page_analysis,
    "content_summary": {
        "total_pages": len(pages),
        "technical_content_pages": sum(1 for p in page_analysis if p["type"] == "technical_content"),
        "legal_pages": sum(1 for p in page_analysis if p["type"] == "legal/terms"),
        "blank_or_title_pages": sum(1 for p in page_analysis if p["type"] in ("blank/title", "table_of_contents")),
        "total_words": sum(p["word_count"] for p in page_analysis)
    },
    "document_sections": [
        {"number": s["number"], "title": s["title"]}
        for s in sections
    ],
    "export_format": {
        "delivery": "password-protected ZIP file",
        "data_files": "CSV (one per database table)",
        "image_files": "native format (PDF, PNG, JPG)",
        "field_descriptions": "FLD text files (generated per export)",
        "naming_convention_tables": "P###_TABLENAME.csv",
        "naming_convention_images": "P###_E/D###_####.ext",
        "bulk_export_prefix": "P0_"
    },
    "explicitly_mentioned_tables": sorted(table_names),
    "explicitly_mentioned_fields": field_names,
    "key_identifier_fields": key_fields,
    "relationship_structure": {
        "demographics_billing": {
            "description": "CSV files where table name does NOT start with EXAM",
            "key_field": "PATUNIQUE",
            "primary_table": "PATIENT"
        },
        "exam_data": {
            "description": "CSV files where table name starts with EXAM",
            "key_field": "EXAMUNIQUE",
            "primary_table": "EXAM",
            "sub_tables_example": "EXAMDIAG"
        },
        "demographics_images": {
            "identifier_type": "D",
            "links_via": "DOCUNIQUE in DOCUMENT table"
        },
        "exam_images": {
            "identifier_type": "E",
            "links_via": "IMAGUNIQUE in EXAMIMAG table"
        }
    },
    "fees": {
        "setup_fees": "None",
        "access_fees": "None for export function",
        "cloud_storage_note": "Possible fees for cloud-hosted clients if export exceeds contracted storage"
    },
    "contact": {
        "department": "Compulink Customer Care",
        "phone": "805.716.8677",
        "fax": "805.497.4983",
        "email": "support@compulinkadvantage.com"
    },
    "documentation_gaps": {
        "no_table_list": True,
        "no_field_level_data_dictionary": True,
        "no_data_types": True,
        "no_value_sets": True,
        "no_er_diagram": True,
        "no_sample_data": True,
        "no_schema_file": True,
        "fld_files_only_in_export": True,
        "tables_explicitly_named": len(table_names),
        "fields_explicitly_shown": len(field_names)
    }
}

with open("pdf_parse_output.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
