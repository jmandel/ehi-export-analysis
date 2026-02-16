#!/usr/bin/env python3
"""
Parse Patagonia Health EHI export artifacts and produce entity inventories.

Since Patagonia Health provides NO data dictionary, NO schema, and NO field-level
documentation for their (b)(10) export, this script documents what IS available:
- C-CDA 2.1 clinical sections (from the proprietary API docs)
- FHIR R4 resources (from the SmartOnFHIR API docs) — these are (g)(10), NOT (b)(10)
- Billing export (CSV/XLSX) — no field documentation exists

The "entities" here represent sections/resources documented in the vendor's API PDFs,
NOT a product-specific data dictionary.
"""

import json
import subprocess
import re
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')

# ---- C-CDA sections from Patient Health Data API v1.1 ----
ccda_sections = [
    {"name": "demographics", "display": "Patient Demographics"},
    {"name": "careteam", "display": "Care Team"},
    {"name": "allergies", "display": "Allergies and Intolerances"},
    {"name": "assessments", "display": "Assessment"},
    {"name": "encounters", "display": "Encounters"},
    {"name": "functionalstatus", "display": "Functional Status"},
    {"name": "goals", "display": "Goals"},
    {"name": "healthconcerns", "display": "Health Concerns"},
    {"name": "immunizations", "display": "Immunizations"},
    {"name": "medicalequipment", "display": "Medical Equipment"},
    {"name": "medications", "display": "Medications"},
    {"name": "mentalstatus", "display": "Mental Status"},
    {"name": "planoftreatment", "display": "Plan of Treatment"},
    {"name": "problem", "display": "Problem"},
    {"name": "procedures", "display": "Procedures"},
    {"name": "reasonforreferral", "display": "Reason for Referral"},
    {"name": "results", "display": "Results"},
    {"name": "socialhistory", "display": "Social History"},
    {"name": "vitalsigns", "display": "Vital Signs"},
]

# ---- FHIR R4 resources from SmartOnFHIR API Documentation ----
fhir_resources = [
    "Patient", "AllergyIntolerance", "CarePlan", "CareTeam",
    "Condition", "Device", "DiagnosticReport", "DocumentReference",
    "Goal", "Immunization", "Medication", "MedicationDispense",
    "Observation", "Organization", "Procedure", "Provenance",
    "ServiceRequest", "Coverage", "Specimen", "RelatedPerson",
]

# Build entity inventory
entities = []

# Clinical export entities (C-CDA sections)
for section in ccda_sections:
    entities.append({
        "entity_name": f"ccda_section_{section['name']}",
        "display_name": section["display"],
        "source": "EHI Export (C-CDA 2.1)",
        "category": "Clinical (C-CDA)",
        "format": "C-CDA 2.1 XML",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation provided. C-CDA standard sections only."
    })

# Billing export entity (no field documentation)
entities.append({
    "entity_name": "billing_claims",
    "display_name": "Claims Data",
    "source": "EHI Export (Billing)",
    "category": "Billing",
    "format": "CSV / XLSX / PDF",
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "notes": "No field-level documentation. Exported via Dashboard > Billing > Reports > Claim > Detail."
})

entities.append({
    "entity_name": "billing_patient_financial",
    "display_name": "Patient Financial Export",
    "source": "EHI Export (Billing)",
    "category": "Billing",
    "format": "CSV / XLSX",
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "notes": "No field-level documentation. Exported via Dashboard > Billing > Search > Claims."
})

# FHIR resources (NOT part of b(10), but documented for reference)
for resource in fhir_resources:
    entities.append({
        "entity_name": f"fhir_{resource.lower()}",
        "display_name": resource,
        "source": "SmartOnFHIR API (g)(10) — NOT (b)(10)",
        "category": "FHIR API (g)(10)",
        "format": "FHIR R4 JSON",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "Standard USCDI FHIR resource. This is the (g)(10) API, not the (b)(10) EHI export."
    })

# Write full inventory
full_inventory = {
    "product": "Patagonia Health EHR",
    "version": "6",
    "analysis_date": "2026-02-16",
    "data_dictionary_available": False,
    "notes": "Patagonia Health provides NO data dictionary, NO schema, and NO field-level documentation for their (b)(10) EHI export. The export consists of C-CDA 2.1 XML for clinical data and CSV/XLSX for billing data, but no documentation describes what fields are included in either format.",
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "ehi_export_entities": len(ccda_sections) + 2,  # ccda sections + 2 billing
    "fhir_api_entities_for_reference": len(fhir_resources),
    "entities": entities
}

output_path = os.path.join(os.path.dirname(__file__), 'entity-inventory-full.json')
with open(output_path, 'w') as f:
    json.dump(full_inventory, f, indent=2)
print(f"Wrote {output_path}")

# Write summary
summary = {
    "product": "Patagonia Health EHR",
    "version": "6",
    "analysis_date": "2026-02-16",
    "data_dictionary_exists": False,
    "sample_data_exists": False,
    "machine_readable_schema_exists": False,
    "ehi_export": {
        "clinical_format": "C-CDA 2.1 Release 2 (USCDI v1)",
        "billing_format": "CSV / XLSX / PDF",
        "clinical_sections": len(ccda_sections),
        "billing_entities": 2,
        "total_entities": len(ccda_sections) + 2,
        "total_documented_fields": 0,
        "field_descriptions": 0,
        "field_types_documented": 0,
    },
    "fhir_api_g10": {
        "note": "NOT part of (b)(10) export — included for reference only",
        "resource_types": len(fhir_resources),
        "resources": fhir_resources,
    },
    "ccda_sections": [s["display"] for s in ccda_sections],
    "category_breakdown": {
        "Clinical (C-CDA)": {"entity_count": len(ccda_sections), "field_count": 0},
        "Billing": {"entity_count": 2, "field_count": 0},
        "FHIR API (g)(10) — NOT b(10)": {"entity_count": len(fhir_resources), "field_count": 0},
    }
}

summary_path = os.path.join(os.path.dirname(__file__), 'entity-inventory-summary.json')
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {summary_path}")

# Print summary stats
print(f"\n=== Summary Statistics ===")
print(f"Data dictionary: NO")
print(f"EHI Export entities: {len(ccda_sections) + 2} ({len(ccda_sections)} C-CDA sections + 2 billing entities)")
print(f"Documented fields: 0 (no field-level documentation)")
print(f"FHIR API (g)(10) resources (for reference): {len(fhir_resources)}")
print(f"Sample data provided: No")
