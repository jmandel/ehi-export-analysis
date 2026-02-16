#!/usr/bin/env python3
"""Parse FHIR CapabilityStatement and SMART guide to produce entity inventory.

Since iPatientCare's (b)(10) export is just their FHIR (g)(10) API + C-CDA,
the 'entities' are the FHIR resource types from their CapabilityStatement.
There is no vendor-specific data dictionary.
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CS_PATH = os.path.join(BASE, "downloads", "fhir-capability-statement.json")

with open(CS_PATH) as f:
    cs = json.load(f)

rest = cs["rest"][0]
resources = rest["resource"]

entities = []
for r in resources:
    rtype = r["type"]
    profiles = r.get("supportedProfile", [])
    interactions = [i["code"] for i in r.get("interaction", [])]
    search_params = [s["name"] for s in r.get("searchParam", [])]
    
    entity = {
        "entity_name": rtype,
        "category": "FHIR US Core / USCDI",
        "fields": [],
        "profile_count": len(profiles),
        "profiles": profiles,
        "interactions": interactions,
        "search_params": search_params,
        "source": "fhir-capability-statement.json",
        "notes": "Standard US Core resource; no vendor-specific extensions or data dictionary provided"
    }
    
    # Fields are not documented per-entity; we note this
    # The SMART guide shows example JSON but no field-level data dictionary
    entities.append(entity)

# Sort by name
entities.sort(key=lambda e: e["entity_name"])

# Full inventory
inventory = {
    "product": "iPatientCare",
    "vendor": "AssureCare LLC",
    "export_type": "Repackaged (g)(10) FHIR Bulk Data + C-CDA",
    "data_dictionary_provided": False,
    "total_entities": len(entities),
    "total_fields": "N/A - no field-level data dictionary",
    "fields_with_descriptions": "N/A",
    "source_artifacts": [
        "170.315b10-Electronic-Health-Information-Export-v1.0.0.2.pdf (3 pages)",
        "SMART-on-FHIR-API-Authentication-and-Access-Guide-1.0.0.3.pdf (118 pages)",
        "fhir-capability-statement.json",
        "fhir-endpoints-bundle.json",
        "smart-configuration.json"
    ],
    "entities": entities
}

# Write full inventory
out_path = os.path.join(BASE, "analysis", "entity-inventory-full.json")
with open(out_path, "w") as f:
    json.dump(inventory, f, indent=2)
print(f"Wrote {out_path} with {len(entities)} entities")

# Summary
summary = {
    "product": "iPatientCare",
    "vendor": "AssureCare LLC",
    "total_entities": len(entities),
    "total_fields": "N/A",
    "fields_with_descriptions": "N/A",
    "has_data_dictionary": False,
    "export_formats": ["C-CDA XML (USCDI v1)", "FHIR R4 Bulk Data (US Core STU 6.1.0)"],
    "entity_categories": {
        "FHIR US Core / USCDI": len(entities)
    },
    "resource_types": [e["entity_name"] for e in entities],
    "resources_with_profiles": sum(1 for e in entities if e["profile_count"] > 0),
    "total_profiles": sum(e["profile_count"] for e in entities),
    "coverage_assessment": {
        "demographics": True,
        "encounters": True,
        "problems_conditions": True,
        "medications": True,
        "allergies": True,
        "immunizations": True,
        "vitals": True,
        "lab_results": True,
        "imaging_diagnostic": True,
        "procedures": True,
        "clinical_notes": True,
        "care_plans_goals": True,
        "orders_referrals": True,
        "insurance_coverage": True,
        "claims_billing": False,
        "payments": False,
        "consents_directives": False,
        "patient_communications": False,
        "custom_forms": False,
        "documents_scanned": False
    }
}

sum_path = os.path.join(BASE, "analysis", "entity-inventory-summary.json")
with open(sum_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {sum_path}")

# Print summary stats
print(f"\n=== Summary ===")
print(f"Total FHIR resource types: {len(entities)}")
print(f"Resources with US Core profiles: {summary['resources_with_profiles']}")
print(f"Total supported profiles: {summary['total_profiles']}")
print(f"Data dictionary: None provided")
print(f"Export formats: {', '.join(summary['export_formats'])}")
print(f"\nResource types:")
for e in entities:
    print(f"  {e['entity_name']} ({e['profile_count']} profiles, {len(e['interactions'])} interactions, {len(e['search_params'])} search params)")
