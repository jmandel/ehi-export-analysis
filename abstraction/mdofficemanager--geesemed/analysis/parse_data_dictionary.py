#!/usr/bin/env python3
"""Parse the GeeseMed b(10) PDF data dictionary into structured JSON.

Reads the pdftotext output and extracts every CCD section and its fields,
including template IDs and descriptions where present.
"""

import json
import re

# The full text extracted from the PDF (pages 6-8 data dictionary section)
# We'll parse it directly from the pdftotext output file

with open("/tmp/geesemed_b10.txt", "r") as f:
    text = f.read()

# Extract only the data dictionary portion (after "Sections in CCD:")
dd_start = text.find("Sections in CCD:")
dd_text = text[dd_start:]

sections = []
current_section = None

lines = dd_text.split("\n")
for line in lines:
    line_stripped = line.strip()
    if not line_stripped or line_stripped.startswith("The material") or \
       line_stripped.startswith("Copyrights") or line_stripped.startswith("Standard Referenced") or \
       line_stripped.startswith("§ 170.205") or line_stripped.startswith("Sections in CCD") or \
       line_stripped.startswith("§170.315") or \
       line_stripped.startswith("may not be reproduced") or \
       line_stripped.startswith("Future Appointments, lab orders") or \
       line_stripped == "Data Elements                                                                                Description":
        continue

    # Check for section header (contains Template ID or is a known header without one)
    template_match = re.search(r'\(Template ID:\s*([\d.]+)\)', line_stripped)

    # Known section headers without template IDs
    headerless_sections = [
        "Patient Demographics/Information",
        "Provider's name and office contact information",
        "Participant",
        "Laboratory Tests",
        "Laboratory Information",
    ]

    is_header = False
    if template_match:
        section_name = line_stripped.split("(Template ID")[0].strip()
        template_id = template_match.group(1)
        current_section = {
            "section": section_name,
            "template_id": template_id,
            "fields": []
        }
        sections.append(current_section)
        is_header = True
    elif line_stripped in headerless_sections:
        current_section = {
            "section": line_stripped,
            "template_id": None,
            "fields": []
        }
        sections.append(current_section)
        is_header = True

    if not is_header and current_section is not None:
        # Parse field line - may have description separated by whitespace
        # Use the layout: field name on left, description on right (separated by lots of spaces)
        parts = re.split(r'\s{3,}', line_stripped)
        field_name = parts[0].strip() if parts else line_stripped.strip()
        description = parts[1].strip() if len(parts) > 1 else None

        if field_name:
            field_obj = {"name": field_name}
            if description:
                field_obj["description"] = description
            current_section["fields"].append(field_obj)

# Build full inventory
inventory = {
    "source": "GeeseMed_b10_Health-Info.Export_11202023.pdf",
    "format": "C-CDA (HL7 CDA R2, Consolidated CDA Templates DSTU 2.1)",
    "sections": sections,
    "summary": {}
}

total_fields = sum(len(s["fields"]) for s in sections)
fields_with_desc = sum(
    1 for s in sections for f in s["fields"] if f.get("description")
)
fields_without_desc = total_fields - fields_with_desc

inventory["summary"] = {
    "total_sections": len(sections),
    "total_fields": total_fields,
    "fields_with_description": fields_with_desc,
    "fields_without_description": fields_without_desc,
    "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
    "sections_with_template_id": sum(1 for s in sections if s.get("template_id")),
    "sections_without_template_id": sum(1 for s in sections if not s.get("template_id")),
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/mdofficemanager--geesemed/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== GeeseMed CCD Data Dictionary Parse Results ===")
print(f"Total sections: {inventory['summary']['total_sections']}")
print(f"Total fields: {inventory['summary']['total_fields']}")
print(f"Fields with description: {inventory['summary']['fields_with_description']}")
print(f"Fields without description: {inventory['summary']['fields_without_description']}")
print(f"Description coverage: {inventory['summary']['description_coverage_pct']}%")
print(f"Sections with template ID: {inventory['summary']['sections_with_template_id']}")
print(f"Sections without template ID: {inventory['summary']['sections_without_template_id']}")
print()
print("=== Sections Detail ===")
for s in sections:
    tid = f" ({s['template_id']})" if s['template_id'] else ""
    desc_count = sum(1 for f in s["fields"] if f.get("description"))
    print(f"  {s['section']}{tid}: {len(s['fields'])} fields ({desc_count} described)")

print(f"\nFull inventory written to: {output_path}")
