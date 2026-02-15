#!/usr/bin/env python3
"""Parse the Data Elements section from the PCE API documentation PDF.
Uses page-by-page parsing since resources span known page ranges."""

import subprocess
import re
import json

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/pce-systems--pce-care-management/downloads/PIX_9_4_API_Documentation.pdf"

# Extract full text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = result.stdout

# Find the data elements section by page markers
# The Data Elements section starts at page 65 and ends before page 80 (Appendix A)
# We'll extract by looking for "Page 65 of 87" through "Page 79 of 87"

lines = full_text.split("\n")

# Collect just the data elements section
in_section = False
section_lines = []
for line in lines:
    if "Page 64 of 87" in line:
        in_section = True
    if "Page 80 of 87" in line:
        break
    if in_section:
        # Skip footer/header lines
        if "Page " in line and " of 87" in line:
            continue
        if "© 20" in line:
            continue
        if "PCE Care Management v9.4 - Web Service API Documentation" in line:
            continue
        if line.strip() == "PCE Systems":
            continue
        if re.match(r'^\s*(January|April|November)\s+\d+,\s+\d{4}\s*$', line.strip()):
            continue
        section_lines.append(line)

section_text = "\n".join(section_lines)

# Now parse: each resource starts with its name on a line, followed by
# a description line, then an "Attribute | Data Type | Description" header, then rows
resources = {}
current_resource = None
current_description = ""
in_table = False
current_attrs = []

for line in section_lines:
    stripped = line.strip()
    if not stripped:
        continue

    # Known resource headers (standalone lines that are resource names)
    known_headers = [
        "Address", "AllergyIntolerance", "CarePlan", "CareTeam", "Claim",
        "Coded Element", "Condition", "Coverage", "Device", "Diagnostic Report",
        "Document Reference", "Encounter", "Goal", "Healthcare Service",
        "Immunization", "Location", "Medication Request", "Message", "Observation",
        "Organization", "Patient", "Practitioner", "Practitioner Role", "Procedure",
        "Provenance", "Failed Response Header"
    ]

    if stripped in known_headers:
        # Save previous resource
        if current_resource is not None:
            resources[current_resource] = {
                "field_count": len(current_attrs),
                "fields": current_attrs,
                "description": current_description.strip()
            }
        current_resource = stripped
        current_description = ""
        current_attrs = []
        in_table = False
        continue

    # Detect table header
    if "Attribute" in stripped and "Data Type" in stripped and "Description" in stripped:
        in_table = True
        continue

    if not in_table:
        # Description line for the resource
        current_description += " " + stripped
        continue

    # In table: parse attribute rows
    # Rows have significant whitespace between columns
    parts = re.split(r'\s{2,}', stripped)
    if len(parts) >= 3:
        attr_name = parts[0]
        data_type = parts[1]
        description = " ".join(parts[2:])
        current_attrs.append({
            "name": attr_name,
            "type": data_type,
            "description": description
        })
    elif len(parts) == 2:
        # Could be a continuation or a split type/description
        # If first part looks like a continuation of previous attr name
        if current_attrs:
            # Check if this looks like "Element" (continuation of "Coded Element" type)
            if parts[0] in ["Element", "Element List"]:
                current_attrs[-1]["type"] += " " + parts[0]
                current_attrs[-1]["description"] += " " + parts[1]
            else:
                current_attrs[-1]["description"] += " " + stripped
    elif len(parts) == 1 and current_attrs:
        # Pure continuation line
        # Check if it's a type continuation like "Element"
        if stripped in ["Element", "Element List"]:
            current_attrs[-1]["type"] += " " + stripped
        else:
            current_attrs[-1]["description"] += " " + stripped

# Save last resource
if current_resource is not None:
    resources[current_resource] = {
        "field_count": len(current_attrs),
        "fields": current_attrs,
        "description": current_description.strip()
    }

# Summary
print("=" * 60)
print("PCE Care Management API - Data Elements Inventory")
print("=" * 60)
print(f"\nTotal resources/data elements: {len(resources)}")
total_fields = sum(r["field_count"] for r in resources.values())
print(f"Total fields across all resources: {total_fields}")

# Separate clinical/business from utility types
utility = ["Address", "Coded Element", "Failed Response Header", "Message"]
clinical_resources = {k: v for k, v in resources.items() if k not in utility}
clinical_fields = sum(r["field_count"] for r in clinical_resources.values())
print(f"\nClinical/business resources (excl utility types): {len(clinical_resources)}")
print(f"Clinical/business fields: {clinical_fields}")

described = sum(1 for r in resources.values() for f in r["fields"] if f.get("description", "").strip())
print(f"Fields with descriptions: {described}/{total_fields} ({100*described//total_fields if total_fields else 0}%)")

print("\n{:<25} {:>8} {:>12}".format("Resource", "Fields", "Described"))
print("-" * 50)
for name in ["Address", "AllergyIntolerance", "CarePlan", "CareTeam", "Claim",
    "Coded Element", "Condition", "Coverage", "Device", "Diagnostic Report",
    "Document Reference", "Encounter", "Goal", "Healthcare Service",
    "Immunization", "Location", "Medication Request", "Message", "Observation",
    "Organization", "Patient", "Practitioner", "Practitioner Role", "Procedure",
    "Provenance", "Failed Response Header"]:
    if name in resources:
        data = resources[name]
        desc_count = sum(1 for f in data["fields"] if f.get("description", "").strip())
        marker = "" if name not in utility else " (utility)"
        print(f"{name:<25} {data['field_count']:>8} {desc_count:>12}{marker}")
    else:
        print(f"{name:<25} {'MISSING':>8}")

# Save full inventory as JSON
output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/pce-systems--pce-care-management/analysis/api-data-elements-inventory.json"
with open(output_path, "w") as f:
    json.dump(resources, f, indent=2)
print(f"\nFull inventory saved to: {output_path}")
