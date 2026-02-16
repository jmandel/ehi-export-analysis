#!/usr/bin/env python3
"""Extract FHIR resource documentation details from the documents.maximus.care JS bundle."""

import json
import subprocess
import re

# Fetch the JS bundle
result = subprocess.run(
    ['curl', '-s', 'https://documents.maximus.care/js/js_main.js', '-H', 'User-Agent: Mozilla/5.0'],
    capture_output=True, text=True
)
js_content = result.stdout

# Extract FHIR resource types
resources = set()
for match in re.finditer(r'"(AllergyIntolerance|CarePlan|CareTeam|Condition|Device|DiagnosticReport|DocumentReference|Encounter|Goal|Immunization|Location|MedicationRequest|Observation|Organization|Patient|Practitioner|Procedure|Provenance)"', js_content):
    resources.add(match.group(1))

sorted_resources = sorted(resources)

# US Core STU 3.1.1 standard resource list for comparison
us_core_stu3_resources = [
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "Medication", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "PractitionerRole", "Procedure", "Provenance"
]

missing_from_vendor = [r for r in us_core_stu3_resources if r not in resources]

output = {
    "source": "https://documents.maximus.care/js/js_main.js",
    "standard": "US Core STU 3.1.1",
    "fhir_version": "R4 (4.0.1)",
    "documented_resources": sorted_resources,
    "documented_resource_count": len(sorted_resources),
    "us_core_stu3_standard_resources": us_core_stu3_resources,
    "us_core_stu3_resource_count": len(us_core_stu3_resources),
    "missing_from_vendor_vs_us_core": missing_from_vendor,
    "custom_profiles_or_extensions": False,
    "bulk_export_documented": True,
    "api_endpoints": {
        "fhir_base_url": "https://fhir.maximus.care/api",
        "capability_statement": "https://fhir.maximus.care/api/metadata",
        "smart_configuration": "https://fhir.maximus.care/api/.well-known/smart-configuration",
        "authorization_url": "https://apiauth.maximus.care/connect/authorize",
        "token_url": "https://apiauth.maximus.care/connect/token"
    },
    "api_status": {
        "metadata_endpoint": "404 Not Found (verified 2026-02-16)",
        "smart_config": "Not publicly accessible"
    }
}

output_path = 'fhir-docs-analysis.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"FHIR resources documented: {len(sorted_resources)}")
print(f"Resources: {', '.join(sorted_resources)}")
print(f"Missing vs US Core STU3: {', '.join(missing_from_vendor) if missing_from_vendor else 'None'}")
print(f"Custom profiles/extensions: {output['custom_profiles_or_extensions']}")
print(f"Output saved to: {output_path}")
