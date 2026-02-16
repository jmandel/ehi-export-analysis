#!/usr/bin/env python3
"""Parse all Agastha EHI export artifacts and produce entity-inventory-full.json and summary."""

import json
import re
import subprocess

# 1. Extract FHIR resources from the B10 PDF
pdf_text = subprocess.run(
    ["pdftotext", "-layout", "../downloads/Agastha-B10-Documentation.pdf", "-"],
    capture_output=True, text=True
).stdout

# Parse resource list from PDF text
# The PDF lists resources between "the resources using FHIR are:" and "All the other resources"
resource_section = re.search(
    r'resources using FHIR are:\s*(.*?)All the other resources',
    pdf_text, re.DOTALL
)

b10_resources = []
if resource_section:
    lines = resource_section.group(1).strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('•'):
            # Convert display name to FHIR resource type
            b10_resources.append(line)

# Clean up resource names
b10_resource_types = []
for r in b10_resources:
    r = r.strip()
    # Remove Unicode bullet characters
    r = r.replace('\uf0a7', '').strip()
    if r:
        # Convert "Allergy Intolerance" -> "AllergyIntolerance" etc.
        camel = r.replace(' ', '')
        b10_resource_types.append(camel)

print(f"B10 PDF FHIR resources: {len(b10_resource_types)}")
for r in b10_resource_types:
    print(f"  {r}")

# 2. Parse resource descriptions from PDF
desc_section = re.search(r'Resource Description\s*Name\s+Description\s*(.*?)Support', pdf_text, re.DOTALL)
resource_descriptions = {}
if desc_section:
    text = desc_section.group(1)
    # Parse two-column table: Name followed by multi-line description
    current_name = None
    current_desc = []
    for line in text.split('\n'):
        line = line.rstrip()
        if not line.strip():
            continue
        # Check if line starts with a known resource name (left-aligned, short word)
        # Resource names start at the left margin
        match = re.match(r'^(\w[\w ]{0,25}?)\s{3,}(.+)$', line)
        if match:
            if current_name:
                resource_descriptions[current_name] = ' '.join(current_desc).strip()
            current_name = match.group(1).strip().replace(' ', '')
            current_desc = [match.group(2).strip()]
        elif current_name:
            current_desc.append(line.strip())
    if current_name:
        resource_descriptions[current_name] = ' '.join(current_desc).strip()

print(f"\nResource descriptions parsed: {len(resource_descriptions)}")

# 3. Parse apiR4.html for additional resources
with open('../downloads/apiR4.html') as f:
    api_content = f.read()

api_resources = re.findall(r'data-toggle="list"[^>]*>([^<]+)</a>', api_content)
api_fhir_resources = []
for r in api_resources:
    r = r.strip()
    if r and not any(skip in r.lower() for skip in ['well-known', 'authorization', 'token', 'openid', 'jwks', 'revocation', '.']):
        api_fhir_resources.append(r)

print(f"\napiR4.html FHIR resources: {len(api_fhir_resources)}")
for r in api_fhir_resources:
    print(f"  {r}")

# Identify resources in API but not in B10
b10_set = set(b10_resource_types)
api_set = set(api_fhir_resources)
in_api_not_b10 = api_set - b10_set
in_b10_not_api = b10_set - api_set
print(f"\nIn apiR4 but NOT in B10 PDF: {in_api_not_b10}")
print(f"In B10 PDF but NOT in apiR4: {in_b10_not_api}")

# 4. Build entity inventory
# Standard FHIR resource descriptions (generic) for ones where we couldn't parse from PDF
standard_fhir_descriptions = {
    "AllergyIntolerance": "Risk of harmful or undesirable physiological response specific to an individual.",
    "CarePlan": "Intention of how practitioners intend to deliver care for a patient.",
    "CareTeam": "People and organizations who plan to participate in care coordination.",
    "Condition": "A clinical condition, problem, diagnosis, or other clinical concept.",
    "Device": "Properties, administrative info, and type of a physical unit.",
    "DiagnosticReport": "Findings and interpretation of diagnostic tests.",
    "DocumentReference": "A reference to a document of any kind for any purpose.",
    "Encounter": "An interaction between a patient and healthcare provider(s).",
    "Goal": "Intended objective(s) for patient care.",
    "Immunization": "Event of a patient being administered a vaccine.",
    "Location": "Details and position information for a place where services are provided.",
    "Medication": "Identification and definition of a medication, including ingredients.",
    "MedicationRequest": "An order or request for supply and administration of medication.",
    "Observation": "Measurements and simple assertions made about a patient.",
    "Organization": "A formally or informally recognized grouping of people or organizations.",
    "Patient": "Demographics and administrative information about an individual receiving care.",
    "Practitioner": "Roles/Locations/specialties/services that a practitioner may perform.",
    "Procedure": "An action performed on or for a patient.",
    "Provenance": "Record describing entities and processes involved in producing a resource.",
    "RelatedPerson": "Person involved in a patient's health or care but not the target of healthcare.",
    "ServiceRequest": "A record of a request for service such as diagnostic investigations or treatments.",
    # Additional from apiR4
    "Appointment": "A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s).",
    "ChargeItem": "The resource ChargeItem describes the provision of healthcare provider products.",
    "Coverage": "Financial instrument which may be used to reimburse or pay for health care products and services.",
    "FamilyMemberHistory": "Significant health conditions for a person related to the patient.",
}

entities = []
all_resource_names = sorted(set(b10_resource_types + api_fhir_resources))

for resource in all_resource_names:
    in_b10 = resource in b10_set
    in_api = resource in api_set
    
    desc = resource_descriptions.get(resource, standard_fhir_descriptions.get(resource, ""))
    
    # Determine category based on resource type
    if resource in ("Patient", "RelatedPerson", "Practitioner", "Organization", "Location"):
        category = "Administrative/Demographics"
    elif resource in ("Encounter", "Appointment"):
        category = "Encounters/Scheduling"
    elif resource in ("Condition",):
        category = "Clinical - Problems"
    elif resource in ("AllergyIntolerance",):
        category = "Clinical - Allergies"
    elif resource in ("Medication", "MedicationRequest"):
        category = "Clinical - Medications"
    elif resource in ("Observation",):
        category = "Clinical - Observations"
    elif resource in ("Immunization",):
        category = "Clinical - Immunizations"
    elif resource in ("Procedure",):
        category = "Clinical - Procedures"
    elif resource in ("DiagnosticReport",):
        category = "Clinical - Diagnostics"
    elif resource in ("DocumentReference",):
        category = "Clinical - Documents"
    elif resource in ("CarePlan", "CareTeam", "Goal"):
        category = "Clinical - Care Planning"
    elif resource in ("ServiceRequest",):
        category = "Clinical - Orders"
    elif resource in ("Device",):
        category = "Clinical - Devices"
    elif resource in ("Provenance",):
        category = "Infrastructure"
    elif resource in ("Coverage", "ChargeItem"):
        category = "Financial/Billing"
    elif resource in ("FamilyMemberHistory",):
        category = "Clinical - Family History"
    else:
        category = "Other"

    entity = {
        "entity_name": resource,
        "fhir_resource_type": resource,
        "description": desc,
        "description_source": "FHIR R4 specification (verbatim copy in vendor PDF)" if desc else "none",
        "in_b10_pdf": in_b10,
        "in_api_r4_docs": in_api,
        "category": category,
        "fields": [],  # No field-level documentation provided
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "vendor_specific_detail": "none",
        "notes": ""
    }
    
    if in_b10 and not in_api:
        entity["notes"] = "Listed in B10 PDF but not documented in apiR4.html"
    elif in_api and not in_b10:
        entity["notes"] = "Documented in apiR4.html (g)(10) API but NOT listed in B10 PDF"
    
    entities.append(entity)

# Add note about "all other resources" claim
inventory = {
    "product": "Agastha Enterprise Healthcare Software",
    "export_format": "FHIR R4 JSON (21 listed resources) + unspecified 'standard JSON format' for other resources",
    "documentation_source": "Agastha-B10-Documentation.pdf (7 pages), dataExport.html, apiR4.html",
    "total_entities_documented_b10": len(b10_resource_types),
    "total_entities_documented_api": len(api_fhir_resources),
    "total_unique_entities": len(entities),
    "total_fields_documented": 0,
    "field_level_documentation": False,
    "vendor_specific_mappings": False,
    "sample_data_provided": False,
    "undocumented_export_claim": "PDF states 'All the other resources are currently exported using the standard JSON format' but provides zero documentation about what those resources are.",
    "entities": entities
}

with open('entity-inventory-full.json', 'w') as f:
    json.dump(inventory, f, indent=2)

print(f"\nWrote entity-inventory-full.json with {len(entities)} entities")

# 5. Build summary
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"count": 0, "in_b10": 0, "in_api": 0, "entities": []}
    categories[cat]["count"] += 1
    categories[cat]["entities"].append(e["entity_name"])
    if e["in_b10_pdf"]:
        categories[cat]["in_b10"] += 1
    if e["in_api_r4_docs"]:
        categories[cat]["in_api"] += 1

summary = {
    "product": "Agastha Enterprise Healthcare Software",
    "analysis_date": "2026-02-16",
    "total_entities": len(entities),
    "entities_in_b10_pdf": len(b10_resource_types),
    "entities_in_api_r4": len(api_fhir_resources),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "field_level_documentation_exists": False,
    "vendor_specific_mappings_exist": False,
    "categories": categories,
    "missing_domains": [
        "Billing/Claims (Claim, ClaimResponse, ExplanationOfBenefit) - product has billing module",
        "Pharmacy management data (inventory, procurement, sales) - product has pharmacy module",
        "Lab management data (specimen tracking, barcodes, device connectivity) - product has LIS module",
        "Patient portal data (secure messages, portal interactions) - product has patient portal",
        "Telehealth data (virtual visit records, remote monitoring) - product has telehealth module",
        "E-prescribing details (EPCS records, transmission logs) - product has e-prescribing module",
        "Custom/specialty clinical data (oncology, neurology, mental health assessments) - product serves these specialties",
    ],
    "notes": [
        "ChargeItem and Coverage appear in apiR4.html but NOT in B10 PDF - partial financial coverage in API only",
        "FamilyMemberHistory and Appointment appear in apiR4.html but NOT in B10 PDF",
        "No field-level documentation exists anywhere - only resource-level FHIR definitions copied from spec",
        "PDF states 'all other resources exported in standard JSON format' but provides no documentation of what those are"
    ]
}

with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"Wrote entity-inventory-summary.json")
print(f"\nCategories:")
for cat, info in sorted(categories.items()):
    print(f"  {cat}: {info['count']} entities (B10: {info['in_b10']}, API: {info['in_api']})")
