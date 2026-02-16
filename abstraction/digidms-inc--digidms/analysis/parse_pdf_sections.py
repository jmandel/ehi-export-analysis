#!/usr/bin/env python3
"""Parse the B10_EHI_Export.pdf text to extract C-CDA sections and fields.

Reads pdftotext output and structures the section/element table into JSON.
"""

import subprocess
import json
import re

PDF_PATH = "../../../results/digidms-inc--digidms/downloads/B10_EHI_Export.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
raw_text = result.stdout

# Find the Export Format section table
# The table has "Section" and "Elements" columns
lines = raw_text.split('\n')

# State machine to parse section/element pairs
sections = []
current_section = None
in_table = False

for line in lines:
    stripped = line.strip()
    
    # Skip headers, footers, empty lines
    if not stripped:
        continue
    if "2184 Morris Ave" in stripped:
        continue
    if "Phone:" in stripped or "Email:" in stripped or "Web:" in stripped or "Support:" in stripped:
        continue
    if "(b)(10) Electronic Health Information" in stripped:
        continue
    if "Export Format" in stripped or "§ 170.205" in stripped:
        in_table = True
        continue
    if stripped in ("Section", "Elements", "Section                Elements"):
        in_table = True
        continue
    
    if not in_table:
        continue
    
    # Detect section headers vs elements by indentation
    # Section names are left-aligned, elements are indented
    if line.startswith('                       ') and current_section:
        # This is an element (indented)
        current_section["elements"].append(stripped)
    elif stripped and not stripped.startswith('(') and stripped not in (
        "Overview", "Export Options", "Product Name and Version: DigiDMS and 22.0",
    ):
        # Check if this looks like a section name
        indent = len(line) - len(line.lstrip())
        if indent < 20:  # Section names have less indentation
            # Known multi-word section names that span lines
            multiword_continuations = {"Equipments"}
            if current_section and not current_section["elements"] and stripped in multiword_continuations:
                current_section["name"] += " " + stripped
            else:
                current_section = {"name": stripped, "elements": []}
                sections.append(current_section)

# Clean up section names
for s in sections:
    s["name"] = re.sub(r'\s+', ' ', s["name"]).strip()

# Build full inventory
inventory = {
    "source_file": "B10_EHI_Export.pdf",
    "source_type": "PDF document",
    "export_format": "C-CDA (HL7 CDA R2 Consolidated CDA)",
    "export_standard": "§ 170.205(a)(4) HL7 Implementation Guide for CDA Release 2: Consolidated CDA",
    "product_version_in_doc": "DigiDMS 22.0",
    "total_sections": 0,
    "total_fields": 0,
    "sections": []
}

for s in sections:
    section_entry = {
        "section_name": s["name"],
        "field_count": len(s["elements"]),
        "fields": []
    }
    for elem in s["elements"]:
        section_entry["fields"].append({
            "name": elem,
            "type": None,  # Not documented
            "description": None,  # Not documented
            "value_set": None,  # Not documented
        })
    inventory["sections"].append(section_entry)
    inventory["total_fields"] += len(s["elements"])

inventory["total_sections"] = len(inventory["sections"])

# Summary stats
stats = {
    "total_sections": inventory["total_sections"],
    "total_fields": inventory["total_fields"],
    "fields_with_types": 0,
    "fields_with_descriptions": 0,
    "fields_with_value_sets": 0,
    "sections_summary": []
}

for s in inventory["sections"]:
    stats["sections_summary"].append({
        "name": s["section_name"],
        "fields": s["field_count"]
    })

print("=== PARSING RESULTS ===")
print(f"Total C-CDA sections: {stats['total_sections']}")
print(f"Total fields/elements: {stats['total_fields']}")
print(f"Fields with types documented: {stats['fields_with_types']}")
print(f"Fields with descriptions: {stats['fields_with_descriptions']}")
print(f"Fields with value sets: {stats['fields_with_value_sets']}")
print()
print("=== SECTIONS ===")
for s in stats["sections_summary"]:
    print(f"  {s['name']}: {s['fields']} fields")

# Write full inventory JSON
with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"\nFull inventory written to full-entity-inventory.json")

# Write summary stats
with open("summary-stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print(f"Summary stats written to summary-stats.json")
