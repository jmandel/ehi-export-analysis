#!/usr/bin/env python3
"""
Produce final entity inventory using enrichment data (which counts all nested fields)
and verify against our schema parse. Also produce summary statistics.
"""

import json
from pathlib import Path

ENRICHMENT = Path("/home/jmandel/hobby/ehi-export-analysis/results/sevocity-a-division-of-conceptual-mindworks-inc--sevocity/downloads/enrichment/sevocity-fhir-api-extracted.json")
OUTPUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/sevocity-a-division-of-conceptual-mindworks-inc--sevocity/analysis")

def classify_resource(rtype):
    categories = {
        "PATIENT": "Demographics",
        "RELATEDPERSON": "Demographics",
        "ENCOUNTER": "Encounters / Visits",
        "APPOINTMENT": "Encounters / Visits",
        "CONDITION": "Problems / Conditions",
        "ALLERGYINTOLERANCE": "Allergies",
        "MEDICATION": "Medications",
        "MEDICATIONREQUEST": "Medications",
        "MEDICATIONSTATEMENT": "Medications",
        "MEDICATIONDISPENSE": "Medications",
        "IMMUNIZATION": "Immunizations",
        "OBSERVATION": "Vitals / Labs / Social History",
        "DIAGNOSTICREPORT": "Lab / Diagnostic Reports",
        "PROCEDURE": "Procedures",
        "CAREPLAN": "Care Plans / Goals",
        "GOAL": "Care Plans / Goals",
        "CARETEAM": "Care Plans / Goals",
        "DOCUMENTREFERENCE": "Clinical Notes / Documents",
        "COVERAGE": "Insurance / Coverage",
        "SERVICEREQUEST": "Orders / Referrals",
        "QUESTIONNAIRE": "Clinical Assessments",
        "QUESTIONNAIRERESPONSE": "Clinical Assessments",
        "PROVENANCE": "Provenance",
        "ORGANIZATION": "Administrative",
        "PRACTITIONER": "Administrative",
        "READPRACTITIONER": "Administrative",
        "LOCATION": "Administrative",
        "ENDPOINT": "Administrative",
        "DEVICE": "Devices",
    }
    return categories.get(rtype.upper(), "Other")

CERTIFIED_G10 = {
    "ALLERGYINTOLERANCE", "CAREPLAN", "CARETEAM", "CONDITION", "COVERAGE",
    "DEVICE", "DIAGNOSTICREPORT", "DOCUMENTREFERENCE", "ENCOUNTER",
    "ENDPOINT", "GOAL", "IMMUNIZATION", "LOCATION", "MEDICATION",
    "MEDICATIONDISPENSE", "MEDICATIONREQUEST", "OBSERVATION",
    "ORGANIZATION", "PATIENT", "PRACTITIONER", "READPRACTITIONER",
    "PROCEDURE", "PROVENANCE"
}

with open(ENRICHMENT) as f:
    enrichment = json.load(f)

# Extract READ-variant resources only (these represent the export data)
read_resources = []
for r in enrichment["resources"]:
    rt = r.get("resourceType", "")
    variant = r.get("variant", "")
    if variant == "read" and rt not in ("FHIR-JSON-RESOURCE", "METADATA"):
        # Normalize practitioner
        canonical_name = rt.upper() if rt != "ReadPractitioner" else "PRACTITIONER"
        read_resources.append({
            "resourceType": canonical_name,
            "original_name": rt,
            "field_count": r["fieldCount"],
            "category": classify_resource(rt),
            "certified_g10": canonical_name in CERTIFIED_G10,
            "fields": r.get("fields", [])
        })

# Summary
total_resources = len(read_resources)
total_fields = sum(r["field_count"] for r in read_resources)
certified_count = sum(1 for r in read_resources if r["certified_g10"])

categories = {}
for r in read_resources:
    cat = r["category"]
    if cat not in categories:
        categories[cat] = {"resources": [], "field_count": 0}
    categories[cat]["resources"].append(r["resourceType"])
    categories[cat]["field_count"] += r["field_count"]

# Print table for analysis.md
print("| Resource Type | Fields | Category | (g)(10) |")
print("|---|---|---|---|")
for r in sorted(read_resources, key=lambda x: (-x["field_count"])):
    cert = "Yes" if r["certified_g10"] else "No"
    print(f"| {r['resourceType']} | {r['field_count']} | {r['category']} | {cert} |")

print()
print(f"Total resource types (READ variants): {total_resources}")
print(f"Total fields across all resources: {total_fields}")
print(f"Certified (g)(10): {certified_count}")
print(f"Non-certified: {total_resources - certified_count}")

print()
print("Category breakdown:")
print("| Category | Resources | Total Fields |")
print("|---|---|---|")
for cat in sorted(categories.keys()):
    info = categories[cat]
    print(f"| {cat} | {len(info['resources'])} ({', '.join(info['resources'])}) | {info['field_count']} |")

# Save updated inventory
inventory = {
    "extraction_date": "2026-02-16",
    "source": "Sevocity FHIR OpenAPI 3.0.1 Specification (enrichment extraction)",
    "spec_version": "1.0.0",
    "fhir_version": "R4",
    "us_core_version": "STU6.1.0",
    "field_counting_method": "All fields at all nesting levels (not just leaf fields)",
    "resources": read_resources,
    "summary": {
        "total_resource_types": total_resources,
        "total_fields": total_fields,
        "certified_g10": certified_count,
        "non_certified": total_resources - certified_count,
        "categories": {cat: {"resource_count": len(info["resources"]), "field_count": info["field_count"], "resources": info["resources"]} for cat, info in categories.items()},
        "fields_with_descriptions": 0,
        "description_note": "OpenAPI schemas provide type information only; no field-level descriptions/documentation"
    }
}

with open(OUTPUT / "full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"\nSaved to {OUTPUT / 'full-entity-inventory.json'}")
