#!/usr/bin/env python3
"""
Parse all HTML artifacts from CHN Tech Solutions EHI export documentation.
Uses regex on raw HTML to reliably extract scopes and section lists.
Outputs entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import re
from pathlib import Path

DOWNLOADS = Path("../downloads")

# --- Extract scopes from REST API page using regex ---
rest_html = (DOWNLOADS / "rest-api-page.html").read_text()

all_scopes = set(re.findall(
    r'((?:patient|user|system)/[A-Za-z_.*$]+\.(?:read|write|\$docref|\$export|\$bulkdata-status))',
    rest_html
))

# Categorize scopes
fhir_patient_scopes = sorted([s for s in all_scopes if s.startswith("patient/") and s.split("/")[1][0].isupper()])
fhir_system_scopes = sorted([s for s in all_scopes if s.startswith("system/")])
fhir_user_scopes = sorted([s for s in all_scopes if s.startswith("user/") and s.split("/")[1][0].isupper()])
oemr_user_scopes = sorted([s for s in all_scopes if s.startswith("user/") and s.split("/")[1][0].islower()])
portal_patient_scopes = sorted([s for s in all_scopes if s.startswith("patient/") and s.split("/")[1][0].islower()])

# Extract FHIR resource types
fhir_resources = set()
for scope in fhir_patient_scopes + fhir_system_scopes + fhir_user_scopes:
    resource = scope.split("/")[1].split(".")[0]
    if resource not in ("*",):
        fhir_resources.add(resource)

# Extract OpenEMR native data types
oemr_data_types = set()
for scope in oemr_user_scopes:
    dtype = scope.split("/")[1].split(".")[0]
    oemr_data_types.add(dtype)

# --- CCD sections from FHIR API page ---
date_filterable_sections = [
    "History of Procedures",
    "Relevant DX Tests / LAB Data",
    "Functional Status",
    "Progress Notes",
    "Procedure Notes",
    "Laboratory Report Narrative",
    "Encounters",
    "Assessments",
    "Treatment Plan",
    "Goals",
    "Health Concerns",
    "Document Reason for Referral",
    "Mental Status",
]

full_record_sections = [
    "Demographics",
    "Allergies, Adverse Reactions, Alerts",
    "History of Medication Use",
    "Problem List",
    "Immunizations",
    "Social History",
    "Medical Equipment",
    "Vital Signs",
]

# --- Build entity inventory ---
entities = []

for section in date_filterable_sections:
    entities.append({
        "entity_name": f"CCD Section: {section}",
        "category": "C-CDA CCD Export (Date-Filterable)",
        "source": "fhir-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"CCD section '{section}' - filtered by encounter date range",
        "notes": "No field-level documentation; relies on C-CDA R2.1 standard templates"
    })

for section in full_record_sections:
    entities.append({
        "entity_name": f"CCD Section: {section}",
        "category": "C-CDA CCD Export (Full Record)",
        "source": "fhir-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"CCD section '{section}' - always includes complete patient history",
        "notes": "No field-level documentation; relies on C-CDA R2.1 standard templates"
    })

for resource in sorted(fhir_resources):
    entities.append({
        "entity_name": f"FHIR Resource: {resource}",
        "category": "FHIR API Resources",
        "source": "rest-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"FHIR R4 {resource} resource via US Core 3.1 API",
        "notes": "Standard US Core profiles; no vendor-specific field documentation"
    })

for dtype in sorted(oemr_data_types):
    entities.append({
        "entity_name": f"OpenEMR API: {dtype}",
        "category": "OpenEMR Native REST API (NOT in b(10) export)",
        "source": "rest-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"OpenEMR native REST API endpoint for '{dtype}' data",
        "notes": "Available via REST API but NOT documented as part of (b)(10) EHI export"
    })

inventory = {
    "product": "Integrated Care EHR",
    "vendor": "CHN Tech Solutions LLC",
    "export_format": "C-CDA CCD (XML) via FHIR $docref operation",
    "data_dictionary_available": False,
    "sample_data_available": False,
    "entities": entities,
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "ccd_sections": {
        "date_filterable": date_filterable_sections,
        "full_record": full_record_sections,
        "total_sections": len(date_filterable_sections) + len(full_record_sections)
    },
    "fhir_resources": sorted(fhir_resources),
    "fhir_resource_count": len(fhir_resources),
    "oemr_data_types": sorted(oemr_data_types),
    "oemr_data_type_count": len(oemr_data_types),
    "scopes": {
        "fhir_patient": fhir_patient_scopes,
        "fhir_system": fhir_system_scopes,
        "fhir_user": fhir_user_scopes,
        "oemr_user": oemr_user_scopes,
        "portal_patient": portal_patient_scopes,
    },
    "scope_counts": {
        "fhir_patient": len(fhir_patient_scopes),
        "fhir_system": len(fhir_system_scopes),
        "fhir_user": len(fhir_user_scopes),
        "oemr_user": len(oemr_user_scopes),
        "portal_patient": len(portal_patient_scopes),
    }
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# --- Summary ---
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entity_count": 0, "total_fields": 0}
    categories[cat]["entity_count"] += 1

summary = {
    "product": "Integrated Care EHR",
    "vendor": "CHN Tech Solutions LLC",
    "export_mechanism": "C-CDA CCD via FHIR $docref operation",
    "data_dictionary": "None - no field-level documentation provided",
    "total_ccd_sections": inventory["ccd_sections"]["total_sections"],
    "ccd_date_filterable_sections": len(date_filterable_sections),
    "ccd_full_record_sections": len(full_record_sections),
    "fhir_resource_types": inventory["fhir_resource_count"],
    "oemr_native_data_types": inventory["oemr_data_type_count"],
    "category_breakdown": categories,
    "data_types_in_rest_api_but_not_in_ccd": sorted(oemr_data_types - {
        "allergy", "encounter", "immunization", "medication", "patient",
        "practitioner", "procedure", "vital"
    }),
    "key_gaps_vs_rest_api": [
        "dental_issue - dental data accessible via API but not in CCD",
        "insurance / insurance_company / insurance_type - insurance data not in CCD",
        "soap_note - SOAP notes not individually exported",
        "surgery - surgery records not in CCD",
        "transaction - financial transactions not in CCD",
        "prescription - prescription details beyond medication list not in CCD",
        "document - uploaded documents not exported",
        "drug - drug reference data not in CCD",
        "message - patient messages not in CCD",
        "appointment - appointment data not in CCD",
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print results
print("=== Entity Inventory Summary ===")
print(f"Total CCD sections: {inventory['ccd_sections']['total_sections']}")
print(f"  Date-filterable: {len(date_filterable_sections)}")
print(f"  Full record: {len(full_record_sections)}")
print(f"\nFHIR Resources: {inventory['fhir_resource_count']}")
print(f"  {', '.join(sorted(fhir_resources))}")
print(f"\nOpenEMR native data types: {inventory['oemr_data_type_count']}")
print(f"  {', '.join(sorted(oemr_data_types))}")
print(f"\nScope counts:")
for k, v in inventory["scope_counts"].items():
    print(f"  {k}: {v}")
print(f"\nData types in REST API but not clearly in CCD export:")
for gap in summary["data_types_in_rest_api_but_not_in_ccd"]:
    print(f"  - {gap}")
print(f"\nField-level documentation: NONE")
print(f"Sample data: NONE")
