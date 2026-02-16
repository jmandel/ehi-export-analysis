#!/usr/bin/env python3
"""Parse the GeeseMed (b)(10) PDF data dictionary and produce structured JSON inventory."""

import json
import re
import subprocess
import sys

PDF_PATH = "../downloads/GeeseMed_b10_Health-Info.Export_11202023.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout

# Parse the "Sections in CCD" table from pages 6-8
# Each section starts with a header line, then field rows with Data Element + Description columns

sections = []
current_section = None
in_table = False

for line in text.split("\n"):
    line_stripped = line.strip()
    if not line_stripped:
        continue

    # Detect section headers (lines with Template ID or known section names)
    template_match = re.search(r'^(.+?)\s*\(Template ID:\s*([\d.]+)\)', line_stripped)
    if template_match:
        if current_section:
            sections.append(current_section)
        current_section = {
            "section": template_match.group(1).strip(),
            "template_id": template_match.group(2).strip(),
            "fields": []
        }
        in_table = True
        continue

    # Known section headers without template IDs
    if line_stripped in ["Patient Demographics/Information", "Provider's name and office contact information",
                         "Participant", "Laboratory Tests", "Laboratory Information"]:
        if current_section:
            sections.append(current_section)
        current_section = {
            "section": line_stripped,
            "template_id": None,
            "fields": []
        }
        in_table = True
        continue

    # Skip non-data lines
    if any(skip in line_stripped for skip in [
        "Data Elements", "Description", "Copyrights", "material presented",
        "may not be reproduced", "Standard Referenced", "§ 170.205",
        "Realm)", "Sections in CCD", "GeeseMed EHR", "MDOfficeManager"
    ]):
        continue

    # Parse field rows - they have a data element name and optionally a description
    if current_section and in_table:
        # Split on multiple spaces to separate element from description
        parts = re.split(r'\s{3,}', line_stripped)
        if parts and parts[0]:
            field_name = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            # Skip if this looks like a continuation/noise
            if field_name and not field_name.startswith("©"):
                current_section["fields"].append({
                    "name": field_name,
                    "description": description,
                    "type": None,  # Not provided in documentation
                    "values": None  # Not provided
                })

if current_section:
    sections.append(current_section)

# Build entity inventory
entities = []
total_fields = 0
fields_with_descriptions = 0

for section in sections:
    entity = {
        "entity": section["section"],
        "template_id": section["template_id"],
        "category": "C-CDA Section",
        "field_count": len(section["fields"]),
        "fields": section["fields"]
    }
    total_fields += len(section["fields"])
    for f in section["fields"]:
        if f["description"] and f["description"] != f["name"]:
            fields_with_descriptions += 1
    entities.append(entity)

inventory = {
    "product": "GeeseMed",
    "version": "7.1",
    "source": "GeeseMed_b10_Health-Info.Export_11202023.pdf",
    "export_format": "C-CDA (HL7 CDA R2, Consolidated CDA Templates DSTU 2.1)",
    "total_sections": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_without_descriptions": total_fields - fields_with_descriptions,
    "entities": entities
}

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "product": inventory["product"],
    "version": inventory["version"],
    "source": inventory["source"],
    "export_format": inventory["export_format"],
    "total_sections": inventory["total_sections"],
    "total_fields": inventory["total_fields"],
    "fields_with_descriptions": inventory["fields_with_descriptions"],
    "fields_without_descriptions": inventory["fields_without_descriptions"],
    "description_percentage": round(fields_with_descriptions / total_fields * 100, 1) if total_fields else 0,
    "sections_summary": [
        {
            "section": e["entity"],
            "template_id": e["template_id"],
            "field_count": e["field_count"],
            "fields_described": sum(1 for f in e["fields"] if f["description"] and f["description"] != f["name"])
        }
        for e in entities
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Sections: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_descriptions} ({summary['description_percentage']}%)")
print(f"Fields without descriptions: {total_fields - fields_with_descriptions}")
print()
for e in entities:
    desc_count = sum(1 for f in e["fields"] if f["description"] and f["description"] != f["name"])
    print(f"  {e['entity']}: {e['field_count']} fields ({desc_count} described)")
