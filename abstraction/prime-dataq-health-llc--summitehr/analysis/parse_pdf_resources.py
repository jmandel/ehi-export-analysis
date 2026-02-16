#!/usr/bin/env python3
"""Parse the SummitEHR EHI Export PDF to extract resource names and produce
a full entity inventory JSON. Since the PDF contains only resource names
(no field-level detail), each entity has zero documented fields."""

import json
import subprocess
import re
import sys

PDF_PATH = "../../../results/prime-dataq-health-llc--summitehr/downloads/EHI-Export-Documentation-SummitEHR-v1.0.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Extract resources from the bulleted list (lines starting with bullet chars or whitespace + resource name)
# Resources appear after "Supported Resources" heading
resources_section = text.split("Supported Resources")[1] if "Supported Resources" in text else ""

resources = []
for line in resources_section.strip().splitlines():
    # Strip all whitespace including unicode non-breaking spaces
    line = line.strip().strip('\x0c')  # remove form feed
    # Remove any non-ASCII bullet/marker characters and whitespace
    line = re.sub(r'^[^\x20-\x7e]+\s*', '', line)
    # Remove trailing non-ASCII chars
    line = re.sub(r'[^\x20-\x7e]+$', '', line)
    line = line.strip()
    if line and not line.startswith("SummitEHR") and len(line) > 1:
        resources.append(line)

# Categorize resources by domain
domain_map = {
    "Demographics": ["Patient information", "Patient addresses", "Patient contacts", "Patient races"],
    "Encounters / Visits": ["Encounters", "Encounter built procedures", "Exam", "Appointments", "Appointment reminders", "Follow up appointments"],
    "Problems / Conditions": ["Problems", "Past medical history"],
    "Medications": ["Medications"],
    "Allergies": ["Allergies"],
    "Immunizations": ["Immunizations"],
    "Vitals": ["Patient vitals"],
    "Lab / Diagnostics": ["Lab Orders", "Lab order diagnosis", "Lab tests", "Lab test results", "Lab test result notes"],
    "Clinical Notes / Documents": ["Progress notes", "Unsigned documents", "Document Details"],
    "Care Plans / Goals": ["Care plans", "Goals", "Interventions"],
    "Social / Behavioral": ["SDOH", "Social history", "Smoking status", "Vaping status", "PHQ 9 screening", "Cognitive statuses", "Functional statuses"],
    "Family History": ["Family history", "Family history diseases"],
    "Procedures / Surgeries": ["Past surgeries"],
    "Insurance / Payments": ["Patient insurances", "Patient payments"],
    "Implantable Devices": ["Implantable devices"],
    "Care Team": ["Patient care team members", "Related person details"],
    "Other": ["Assessments", "Diet", "Patient tasks", "Pregnancy status", "Prior authentication"],
}

# Build inventory
inventory = {
    "source_file": "EHI-Export-Documentation-SummitEHR-v1.0.pdf",
    "source_pages": 4,
    "extraction_note": "PDF contains only resource names - no field-level documentation exists",
    "total_resources": len(resources),
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "resources": []
}

# Assign categories
categorized = set()
for cat, members in domain_map.items():
    for m in members:
        categorized.add(m)

for r in resources:
    cat = "Uncategorized"
    for domain, members in domain_map.items():
        if r in members:
            cat = domain
            break
    inventory["resources"].append({
        "name": r,
        "category": cat,
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "documentation_level": "name_only"
    })

# Summary by category
category_summary = {}
for r in inventory["resources"]:
    cat = r["category"]
    if cat not in category_summary:
        category_summary[cat] = {"resource_count": 0, "resources": []}
    category_summary[cat]["resource_count"] += 1
    category_summary[cat]["resources"].append(r["name"])

inventory["category_summary"] = category_summary

# Write output
with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"Total resources extracted: {len(resources)}")
print(f"\nResources by category:")
for cat, info in sorted(category_summary.items()):
    print(f"  {cat}: {info['resource_count']} ({', '.join(info['resources'])})")

print(f"\nAll resources:")
for i, r in enumerate(resources, 1):
    print(f"  {i}. {r}")

# Verify against prior report's claim of 47
if len(resources) == 47:
    print(f"\n✓ Confirmed: 47 resources (matches prior report)")
else:
    print(f"\n⚠ Count mismatch: found {len(resources)}, prior report claimed 47")
