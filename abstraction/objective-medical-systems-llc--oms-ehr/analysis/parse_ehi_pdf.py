#!/usr/bin/env python3
"""Parse the OMS EHR EHI Export Data Format PDF and produce a structured JSON inventory."""

import json
import subprocess
import re

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/objective-medical-systems-llc--oms-ehr/downloads/EHI-Export-Data-Format.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
raw_text = result.stdout

# Parse the table rows from the PDF text
# The table has two columns: Function and Doc Type
export_categories = []
lines = raw_text.strip().split("\n")
in_table = False
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("Function"):
        in_table = True
        continue
    if line.startswith("Note:"):
        break
    if in_table and line:
        # Split on multiple spaces (table columns)
        parts = re.split(r'\s{2,}', line)
        if len(parts) >= 2:
            export_categories.append({
                "function": parts[0].strip(),
                "doc_type": parts[1].strip()
            })
        elif len(parts) == 1 and parts[0]:
            export_categories.append({
                "function": parts[0].strip(),
                "doc_type": "unknown"
            })

# Build the full inventory
inventory = {
    "source_file": "EHI-Export-Data-Format.pdf",
    "source_url": "https://objectivemedicalsystems.com/wp-content/uploads/2025/09/EHI-Export-Data-Format.pdf",
    "pdf_pages": 2,
    "pdf_creation_date": "2023-11-16",
    "pdf_author": "Anand Aravind",
    "document_title": "§170.315(b)(10) Electronic Health Information Export Data Format",
    "total_export_categories": len(export_categories),
    "total_fields_documented": 0,  # No field-level documentation exists
    "has_data_dictionary": False,
    "has_field_descriptions": False,
    "has_field_types": False,
    "has_relationships": False,
    "has_value_sets": False,
    "has_sample_data": False,
    "export_categories": export_categories,
    "note": "Documents sourced from outside will be exported in the same format it was received.",
    "assessment": {
        "documentation_type": "minimal format listing",
        "detail_level": "category-level only, no field-level documentation",
        "total_entities_with_field_detail": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "description_percentage": 0
    }
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/objective-medical-systems-llc--oms-ehr/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(json.dumps(inventory, indent=2))
print(f"\nSaved to {output_path}")
