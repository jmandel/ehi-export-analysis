#!/usr/bin/env python3
"""Parse the SummitEHR EHI Export Documentation PDF to extract supported resources
and produce entity-inventory-full.json and entity-inventory-summary.json."""

import json
import subprocess
import re

PDF_PATH = "../downloads/EHI-Export-Documentation-SummitEHR-v1.0.pdf"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout

# Extract resource names from the bulleted list after "Supported Resources"
in_resources = False
resources = []
for line in text.split("\n"):
    stripped = line.strip()
    if "Supported Resources" in stripped:
        in_resources = True
        continue
    if in_resources and stripped:
        # Lines starting with bullet-like chars or resource names
        # Remove bullet markers and extra whitespace
        name = re.sub(r'^[\u2022\u25cf\-\*•\uf0b7]\s*', '', stripped).strip().rstrip('\uf020')
        # Skip non-resource lines
        if name and not name.startswith("SummitEHR") and len(name) < 100:
            resources.append(name)

print(f"Found {len(resources)} resources")

# Categorize resources into domains
domain_map = {
    "Demographics": ["Patient information", "Patient addresses", "Patient contacts", "Patient races", "Related person details"],
    "Encounters / Visits": ["Encounters", "Encounter built procedures", "Exam", "Appointments", "Appointment reminders", "Follow up appointments"],
    "Problems / Conditions": ["Problems", "Past medical history"],
    "Medications / Prescriptions": ["Medications"],
    "Allergies": ["Allergies"],
    "Immunizations": ["Immunizations"],
    "Vitals": ["Patient vitals"],
    "Lab Results": ["Lab Orders", "Lab order diagnosis", "Lab tests", "Lab test results", "Lab test result notes"],
    "Procedures": ["Encounter built procedures", "Past surgeries"],
    "Clinical Notes / Documents": ["Progress notes", "Unsigned documents", "Document Details"],
    "Care Plans / Goals": ["Care plans", "Goals", "Interventions"],
    "Assessments / Screening": ["Assessments", "PHQ 9 screening", "Cognitive statuses", "Functional statuses"],
    "Social / Behavioral": ["SDOH", "Social history", "Smoking status", "Vaping status", "Pregnancy status"],
    "Family History": ["Family history", "Family history diseases"],
    "Implantable Devices": ["Implantable devices"],
    "Insurance / Coverage": ["Patient insurances"],
    "Payments": ["Patient payments"],
    "Care Team": ["Patient care team members"],
    "Diet / Nutrition": ["Diet"],
    "Tasks / Workflow": ["Patient tasks"],
    "Prior Authorization": ["Prior authentication"],
}

# Build entity inventory
entities = []
for resource in resources:
    # Find which domain this belongs to
    domain = "Other"
    for d, members in domain_map.items():
        if resource in members:
            domain = d
            break
    
    entities.append({
        "entity_name": resource,
        "domain": domain,
        "fields": [],  # No field-level documentation available
        "field_count": None,  # Unknown - no data dictionary
        "has_field_documentation": False,
        "notes": "Resource listed in PDF documentation; no field-level details provided"
    })

# entity-inventory-full.json
full_inventory = {
    "product": "summitEHR",
    "version": "1.0",
    "source_artifact": "EHI-Export-Documentation-SummitEHR-v1.0.pdf",
    "extraction_notes": "PDF lists 47 resource names only. No field-level data dictionary exists. Field counts, types, descriptions, and relationships are completely undocumented.",
    "total_entities": len(entities),
    "total_fields": None,  # Unknown
    "fields_with_descriptions": 0,
    "entities": entities
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# entity-inventory-summary.json
domain_summary = {}
for e in entities:
    d = e["domain"]
    if d not in domain_summary:
        domain_summary[d] = {"entity_count": 0, "entities": []}
    domain_summary[d]["entity_count"] += 1
    domain_summary[d]["entities"].append(e["entity_name"])

summary = {
    "product": "summitEHR",
    "total_entities": len(entities),
    "total_fields": "Unknown - no field-level documentation",
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "export_format": "TSV (Tab-Separated Values)",
    "domain_breakdown": domain_summary,
    "documentation_quality": {
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_data_types": False,
        "has_value_sets": False,
        "has_relationships": False,
        "has_sample_data": False,
        "has_machine_readable_schema": False,
        "documentation_pages": 4,
        "documentation_level": "resource-name-only"
    }
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nTotal entities: {len(entities)}")
print(f"\nDomain breakdown:")
for d, info in sorted(domain_summary.items()):
    print(f"  {d}: {info['entity_count']} entities - {', '.join(info['entities'])}")

print(f"\nSaved entity-inventory-full.json and entity-inventory-summary.json")
