#!/usr/bin/env python3
"""
Parse the Patient EHI Data Export Overview PDF to extract the 22 C-CDA sections
listed as part of the EHI export. Produces entity-inventory-full.json and
entity-inventory-summary.json.

Since the export is C-CDA-based with no data dictionary, each "section" is
treated as an entity with no field-level detail available.
"""

import json
import subprocess
import re
import sys

PDF_PATH = "../downloads/Patient-EHI-Data-Export-Overview.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout

# Parse bullet items (lines starting with •)
sections = []
for line in text.split("\n"):
    line = line.strip()
    if line.startswith("•"):
        section_name = line.lstrip("•").strip()
        if section_name:
            sections.append(section_name)

# Map C-CDA sections to USCDI/clinical categories
SECTION_CATEGORY = {
    "ALLERGIES": "Clinical",
    "ASSESSMENT": "Clinical",
    "CONSULT NOTE": "Clinical Notes",
    "DIAGNOSTIC IMAGING STUDY": "Diagnostics",
    "ENCOUNTERS": "Clinical",
    "FUNCTIONAL STATUS": "Clinical",
    "GOALS": "Clinical",
    "HEALTH CONCERN": "Clinical",
    "HISTORY AND PHYSICAL": "Clinical Notes",
    "IMMUNIZATIONS": "Clinical",
    "LABORATORY REPORT NARRATIVE": "Diagnostics",
    "MEDICAL EQUIPMENT": "Clinical",
    "MEDICATIONS": "Clinical",
    "MENTAL STATUS": "Clinical",
    "PLAN OF CARE": "Clinical",
    "PROBLEM LIST": "Clinical",
    "PROCEDURES": "Clinical",
    "PROGRESS NOTE": "Clinical Notes",
    "REASON FOR REFERRAL": "Clinical",
    "RESULTS": "Diagnostics",
    "SOCIAL HISTORY": "Clinical",
    "VITAL SIGNS": "Clinical",
}

# Build entity inventory
entities = []
for section in sections:
    entities.append({
        "entity_name": section,
        "category": SECTION_CATEGORY.get(section, "Unknown"),
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "source": "Patient-EHI-Data-Export-Overview.pdf",
        "notes": "C-CDA section listed in export overview. No field-level documentation provided."
    })

# Full inventory
full_inventory = {
    "product": "Criterions EHR",
    "version": "4.0",
    "export_format": "C-CDA (XML)",
    "source_artifact": "Patient-EHI-Data-Export-Overview.pdf",
    "total_entities": len(entities),
    "total_fields": 0,
    "total_fields_with_descriptions": 0,
    "total_fields_with_types": 0,
    "note": "Export is C-CDA based. Only section names are documented; no field-level data dictionary exists.",
    "entities": entities
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary inventory
category_breakdown = {}
for e in entities:
    cat = e["category"]
    if cat not in category_breakdown:
        category_breakdown[cat] = {"entity_count": 0, "field_count": 0}
    category_breakdown[cat]["entity_count"] += 1
    category_breakdown[cat]["field_count"] += e["field_count"]

summary = {
    "product": "Criterions EHR",
    "version": "4.0",
    "export_format": "C-CDA (XML)",
    "total_entities": len(entities),
    "total_fields": 0,
    "total_fields_with_descriptions": 0,
    "total_fields_with_types": 0,
    "category_breakdown": category_breakdown,
    "section_names": sections,
    "data_dictionary_available": False,
    "sample_data_available": False,
    "machine_readable_schema": False,
    "note": "No data dictionary exists. Export documentation lists 22 C-CDA section names only."
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Parsed {len(sections)} C-CDA sections from PDF:")
for s in sections:
    print(f"  - {s} [{SECTION_CATEGORY.get(s, 'Unknown')}]")
print(f"\nCategory breakdown:")
for cat, info in sorted(category_breakdown.items()):
    print(f"  {cat}: {info['entity_count']} sections")
print(f"\nOutput: entity-inventory-full.json, entity-inventory-summary.json")
