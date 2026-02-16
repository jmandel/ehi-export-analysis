#!/usr/bin/env python3
"""Parse the Tebra FHIR API User Guide to extract FHIR resources and their details."""

import json
import re

with open("fhir_api_guide_text.txt") as f:
    text = f.read()

# Extract USCDI/FHIR resource mapping table
fhir_resources = []

# From the Function Names & Resources table
resource_mappings = [
    {"uscdi_class": "Allergies and Intolerances", "us_core_profile": "US Core AllergyIntolerance Profile", "fhir_resource": "AllergyIntolerance", "scope": "Search, Read"},
    {"uscdi_class": "Assessment and Plan of Treatment", "us_core_profile": "US Core CarePlan Profile", "fhir_resource": "CarePlan", "scope": "Search, Read"},
    {"uscdi_class": "Care Team Members", "us_core_profile": "US Core CareTeam Profile", "fhir_resource": "CareTeam", "scope": "Search, Read"},
    {"uscdi_class": "Clinical Notes", "us_core_profile": "US Core DocumentReference Profile", "fhir_resource": "DocumentReference", "scope": "Search, Read"},
    {"uscdi_class": "Clinical Notes (Diagnostic)", "us_core_profile": "US Core DiagnosticReport Profile for Report and Note Exchange", "fhir_resource": "DiagnosticReport", "scope": "Search, Read"},
    {"uscdi_class": "Goals", "us_core_profile": "US Core Goal Profile", "fhir_resource": "Goal", "scope": "Search, Read"},
    {"uscdi_class": "Health Concerns", "us_core_profile": "US Core Condition Profile", "fhir_resource": "Condition", "scope": "Search, Read"},
    {"uscdi_class": "Immunizations", "us_core_profile": "US Core Immunizations Profile", "fhir_resource": "Immunization", "scope": "Search, Read"},
    {"uscdi_class": "Laboratory", "us_core_profile": "US Core Laboratory Result Observation Profile / US Core DiagnosticReport Profile", "fhir_resource": "Observation, DiagnosticReport", "scope": "Search, Read"},
    {"uscdi_class": "Medications", "us_core_profile": "US Core Medication Profile / US Core Medication Request Profile", "fhir_resource": "Medication, MedicationRequest", "scope": "Search, Read"},
    {"uscdi_class": "Patient Demographics", "us_core_profile": "US Core Patient Profile", "fhir_resource": "Patient", "scope": "Search, Read"},
    {"uscdi_class": "Problems", "us_core_profile": "US Core Condition Profile", "fhir_resource": "Condition", "scope": "Search, Read"},
    {"uscdi_class": "Procedures", "us_core_profile": "US Core Procedure Profile", "fhir_resource": "Procedure", "scope": "Search, Read"},
    {"uscdi_class": "Provenance", "us_core_profile": "US Core Provenance Profile", "fhir_resource": "Provenance", "scope": "Search, Read"},
    {"uscdi_class": "Smoking Status", "us_core_profile": "US Core Smoking Status Observation Profile", "fhir_resource": "Observation", "scope": "Search, Read"},
    {"uscdi_class": "Implantable Device", "us_core_profile": "US Core Implantable Device Profile", "fhir_resource": "Device", "scope": "Search, Read"},
    {"uscdi_class": "Vitals", "us_core_profile": "FHIR Core / US Core Profiles", "fhir_resource": "Observation", "scope": "Search, Read"},
]

# Unique FHIR resources
unique_resources = sorted(set(r["fhir_resource"] for r in resource_mappings))

output = {
    "api_type": "FHIR R4 (via SmileCDR)",
    "base_url": "https://fhir.prd.cloud.tebra.com/fhir-request",
    "standard": "HL7 FHIR US Core Implementation Guide STU3 Release 3.1.1",
    "uscdi_version": "v1",
    "total_unique_fhir_resources": len(set(r.replace(", ", ",").split(",")[0] for r in unique_resources)),
    "uscdi_data_classes": len(resource_mappings),
    "resource_mappings": resource_mappings,
    "unique_fhir_resources": unique_resources,
    "additional_resources": ["Encounter", "Location", "Organization", "Practitioner", "PractitionerRole"]
}

with open("fhir_api_inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
print(f"\nUnique FHIR Resources: {len(unique_resources)}")
print(f"Additional (non-USCDI) resources: {output['additional_resources']}")
