#!/usr/bin/env python3
"""Parse all EHI export artifacts for Procentive and produce inventory files.

Since Procentive provides no data dictionary, schema, or field-level documentation,
this script extracts what we can from the FHIR CapabilityStatement and the ONC page
to document what's available.
"""

import json
import re
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
OUTPUT = Path(__file__).parent

# 1. Parse FHIR CapabilityStatement
with open(DOWNLOADS / "fhir-capability-statement.json") as f:
    cs = json.load(f)

rest = cs.get("rest", [{}])[0]
resources = rest.get("resource", [])

def classify_resource(rtype):
    mapping = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Allergies",
        "CarePlan": "Care Plans",
        "CareTeam": "Care Team",
        "Condition": "Problems/Conditions",
        "Device": "Devices",
        "DiagnosticReport": "Diagnostics",
        "DocumentReference": "Documents",
        "Encounter": "Encounters",
        "Goal": "Goals",
        "Immunization": "Immunizations",
        "MedicationRequest": "Medications",
        "Observation": "Clinical Observations",
        "Procedure": "Procedures",
        "Provenance": "Provenance",
        "Location": "Facility",
        "Organization": "Organization",
        "Practitioner": "Provider",
        "PractitionerRole": "Provider",
        "Group": "Administrative",
        "Binary": "Documents",
        "ClinicalImpression": "Clinical Observations",
        "Composition": "Documents",
    }
    return mapping.get(rtype, "Other")

fhir_resources = []
for r in resources:
    rtype = r.get("type", "?")
    interactions = [i["code"] for i in r.get("interaction", [])]
    operations = [o["name"] for o in r.get("operation", [])]
    search_params = [s["name"] for s in r.get("searchParam", [])]
    profiles = r.get("supportedProfile", []) or []
    if r.get("profile"):
        profiles.insert(0, r["profile"])
    fhir_resources.append({
        "type": rtype,
        "interactions": interactions,
        "operations": operations,
        "search_params": search_params,
        "profiles": profiles,
    })

# 2. Parse ONC page for EHI export description
with open(DOWNLOADS / "onc-procentive-page.html") as f:
    onc_html = f.read()

text = re.sub(r'<style[^>]*>.*?</style>', '', onc_html, flags=re.DOTALL)
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', text)
text = re.sub(r'\n\s*\n', '\n', text)
text = re.sub(r'[ \t]+', ' ', text)
lines = [l.strip() for l in text.split('\n') if l.strip()]

# Extract EHI section
ehi_section = []
in_ehi = False
for line in lines:
    if "Electronic Health Information (EHI) Export" in line:
        in_ehi = True
    if in_ehi:
        ehi_section.append(line)
        if "FHIR Endpoints" in line or "ONC Real World Testing" in line:
            break

# 3. Parse PDF content
import subprocess
pdf_text = subprocess.run(
    ["pdftotext", "-layout", str(DOWNLOADS / "PDF-for-Website-on-Formats-1.pdf"), "-"],
    capture_output=True, text=True
).stdout.strip()

# 4. Build the entity inventory
# Since there is NO data dictionary, we document what the FHIR API exposes
# (which is the only documented export mechanism)
entities = []
for r in fhir_resources:
    entities.append({
        "entity_name": r["type"],
        "source": "FHIR CapabilityStatement",
        "fields": [],  # No field-level documentation provided
        "field_count": 0,
        "fields_with_descriptions": 0,
        "interactions": r["interactions"],
        "operations": r["operations"],
        "search_params": r["search_params"],
        "profiles": r["profiles"],
        "category": classify_resource(r["type"]),
    })

def classify_resource(rtype):
    mapping = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Allergies",
        "CarePlan": "Care Plans",
        "CareTeam": "Care Team",
        "Condition": "Problems/Conditions",
        "Device": "Devices",
        "DiagnosticReport": "Diagnostics",
        "DocumentReference": "Documents",
        "Encounter": "Encounters",
        "Goal": "Goals",
        "Immunization": "Immunizations",
        "MedicationRequest": "Medications",
        "Observation": "Clinical Observations",
        "Procedure": "Procedures",
        "Provenance": "Provenance",
        "Location": "Facility",
        "Organization": "Organization",
        "Practitioner": "Provider",
        "PractitionerRole": "Provider",
        "Group": "Administrative",
        "Binary": "Documents",
        "ClinicalImpression": "Clinical Observations",
        "Composition": "Documents",
    }
    return mapping.get(rtype, "Other")

# Re-run with function defined first
entities = []
for r in fhir_resources:
    entities.append({
        "entity_name": r["type"],
        "source": "FHIR CapabilityStatement",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "interactions": r["interactions"],
        "operations": r["operations"],
        "search_params": r["search_params"],
        "profiles": r["profiles"],
        "category": classify_resource(r["type"]),
    })

# Full inventory
full_inventory = {
    "product": "Procentive",
    "vendor": "Ensora Health (formerly Therapy Brands / Procentive)",
    "export_documentation_source": "ONC page + PDF + FHIR CapabilityStatement",
    "has_data_dictionary": False,
    "has_field_level_documentation": False,
    "has_sample_data": False,
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "entities": entities,
    "ehi_export_description": ehi_section,
    "pdf_content": pdf_text,
    "fhir_resource_types": [r["type"] for r in fhir_resources],
}

with open(OUTPUT / "entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"count": 0, "resources": []}
    categories[cat]["count"] += 1
    categories[cat]["resources"].append(e["entity_name"])

summary = {
    "product": "Procentive",
    "total_fhir_resource_types": len(entities),
    "total_fields_documented": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "export_formats_mentioned": ["XML", "CSV", "PDF"],
    "fhir_resource_count": len(fhir_resources),
    "categories": categories,
    "documentation_artifacts": {
        "pdf_file_formats": {
            "pages": 1,
            "content": "Generic descriptions of XML, CSV, PDF formats. No field definitions.",
        },
        "onc_page": {
            "ehi_section_lines": len(ehi_section),
            "content_summary": "Single/population export mentioned. Formats link to PDF. No data dictionary.",
        },
        "fhir_capability_statement": {
            "resource_types": len(fhir_resources),
            "content_summary": "Standard USCDI FHIR resources. No vendor extensions documented.",
        },
        "fhir_api_documentation": {
            "content_summary": "USCDI-to-FHIR mapping. Explicitly states 'Available data via the API interface is limited by the data defined by the USCDI.'",
        },
    },
}

with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities: {len(entities)}")
print(f"Fields documented: 0")
print(f"Categories: {list(categories.keys())}")
print(f"FHIR resources: {[r['type'] for r in fhir_resources]}")
print(f"\nEHI section from ONC page:")
for line in ehi_section:
    print(f"  {line}")
print(f"\nPDF content:")
print(pdf_text)
print("\nDone. Output saved to entity-inventory-full.json and entity-inventory-summary.json")
