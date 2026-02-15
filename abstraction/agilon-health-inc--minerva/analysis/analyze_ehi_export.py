#!/usr/bin/env python3
"""
Analyze the Minerva EHI Export documentation PDF.
Extracts and compares FHIR resource types from:
1. The "Supported Resources" list in the API documentation (page 8)
2. The ZIP file screenshot showing actual exported files (page 6)
"""

import json

# From PDF page 8 - explicitly listed "Supported Resources" for bulk export API
api_supported_resources = sorted([
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "Medication", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "PractitionerRole", "Procedure", "Provenance"
])

# From PDF page 6 - ZIP file contents screenshot (single-patient UI export)
# Visible files in the screenshot
zip_file_resources = sorted([
    "AllergyIntolerance", "CareTeam", "ClinicalImpression",
    "DiagnosticReport", "DocumentReference", "Encounter", "Location",
    "Medication", "MedicationRequest", "Observation", "Patient",
    "Practitioner", "Procedure", "Provenance"
])

# Analysis
print("=" * 70)
print("MINERVA EHI EXPORT - FHIR RESOURCE ANALYSIS")
print("=" * 70)

print(f"\n## API Supported Resources (from PDF p.8)")
print(f"Count: {len(api_supported_resources)}")
for r in api_supported_resources:
    print(f"  - {r}")

print(f"\n## ZIP File Resources (from PDF p.6 screenshot)")
print(f"Count: {len(zip_file_resources)}")
for r in zip_file_resources:
    print(f"  - {r}")

# Discrepancies
in_api_not_zip = sorted(set(api_supported_resources) - set(zip_file_resources))
in_zip_not_api = sorted(set(zip_file_resources) - set(api_supported_resources))

print(f"\n## Discrepancies")
print(f"\nIn API list but NOT in ZIP screenshot ({len(in_api_not_zip)}):")
for r in in_api_not_zip:
    print(f"  - {r}")

print(f"\nIn ZIP screenshot but NOT in API list ({len(in_zip_not_api)}):")
for r in in_zip_not_api:
    print(f"  - {r}")

# Domain coverage analysis
print("\n" + "=" * 70)
print("DOMAIN COVERAGE MAPPING")
print("=" * 70)

# Map FHIR resources to EHI domains
domain_mapping = {
    "Demographics": ["Patient"],
    "Encounters / visits": ["Encounter"],
    "Problems / conditions / diagnoses": ["Condition", "ClinicalImpression"],
    "Medications / prescriptions": ["Medication", "MedicationRequest"],
    "Allergies": ["AllergyIntolerance"],
    "Immunizations": ["Immunization"],
    "Vitals": ["Observation"],  # Observation covers vitals + labs
    "Lab results": ["Observation", "DiagnosticReport"],
    "Imaging / diagnostic reports": ["DiagnosticReport", "DocumentReference"],
    "Procedures": ["Procedure"],
    "Clinical notes / documents": ["DocumentReference"],
    "Care plans / goals": ["CarePlan", "Goal", "CareTeam"],
    "Orders / referrals": [],  # No ServiceRequest
    "Insurance / coverage": [],  # No Coverage resource
    "Claims / billing": [],  # No Claim resource
    "Payments": [],  # No PaymentReconciliation
    "Consents / directives": [],  # No Consent resource
    "Patient communications / portal messages": [],  # No Communication resource
}

all_resources = set(api_supported_resources) | set(zip_file_resources)

print(f"\nTotal unique FHIR resources across both lists: {len(all_resources)}")
print(f"\nDomain coverage:")
for domain, resources in domain_mapping.items():
    covered = [r for r in resources if r in all_resources]
    if covered:
        status = "✅ Covered" if len(covered) == len(resources) else "⚠️ Partial"
        print(f"  {status}: {domain} → {', '.join(covered)}")
    else:
        print(f"  ❌ Not covered: {domain}")

# Missing FHIR resource types that would improve coverage
print("\n## Notable FHIR Resources NOT in Export")
missing_important = [
    ("Coverage", "Insurance information"),
    ("Claim / ExplanationOfBenefit", "Billing/claims data"),
    ("Communication", "Patient-provider messaging"),
    ("Appointment / Schedule", "Appointment data"),
    ("Consent", "Patient consent records"),
    ("ServiceRequest", "Orders and referrals"),
    ("QuestionnaireResponse", "Patient-reported data"),
    ("RelatedPerson", "Patient family/contacts"),
]
for resource, desc in missing_important:
    print(f"  - {resource}: {desc}")

# Export to JSON for reference
output = {
    "api_supported_resources": api_supported_resources,
    "zip_screenshot_resources": zip_file_resources,
    "all_unique_resources": sorted(all_resources),
    "in_api_not_zip": in_api_not_zip,
    "in_zip_not_api": in_zip_not_api,
    "total_api_resources": len(api_supported_resources),
    "total_zip_resources": len(zip_file_resources),
    "total_unique": len(all_resources),
}

with open("resource_inventory.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved resource_inventory.json")

# PDF analysis summary
print("\n" + "=" * 70)
print("PDF DOCUMENT SUMMARY")
print("=" * 70)
print(f"File: Mphrx-EHI-export-documentation.pdf")
print(f"Pages: 12")
print(f"Created: June 4, 2021")
print(f"Author: admin (MphRx)")
print(f"Tool: Microsoft Word for Microsoft 365")
print(f"Format: Letter (792x612 pts), landscape orientation")
print(f"File size: 638,720 bytes (624 KB)")
print(f"\nContent breakdown:")
print(f"  Page 1: Title page")
print(f"  Page 2: Table of contents")
print(f"  Page 3: Summary & intended users (2 sentences total)")
print(f"  Pages 4-6: Single patient UI export (screenshots)")
print(f"  Pages 7-11: Bulk FHIR API export (technical details)")
print(f"  Page 12: Download instructions & notes")
print(f"\nKey characteristics:")
print(f"  - Export format: NDJSON (one file per FHIR resource type)")
print(f"  - Single patient: UI button (Admin/Clinical Admin)")
print(f"  - Bulk export: FHIR $export API (SMART Backend Services auth)")
print(f"  - File splitting: New file per 10,000 records per resource")
print(f"  - Download expiry: URLs expire after 48 hours")
print(f"  - No data dictionary beyond FHIR resource references")
print(f"  - No sample data content shown (just file names)")
print(f"  - No vendor extensions documented")
print(f"  - References HL7 FHIR ndjson spec for format details")
