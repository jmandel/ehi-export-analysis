#!/usr/bin/env python3
"""
Build entity-inventory-full.json and entity-inventory-summary.json
from the FHIR CapabilityStatement and USCDI mapping table.

Since there is NO dedicated (b)(10) EHI export documentation or data dictionary,
the only available structured artifacts are the (g)(10) FHIR API resources.
This script documents what IS available, which is only the FHIR API surface.
"""
import json

# Load FHIR inventory
with open("fhir-inventory.json") as f:
    fhir = json.load(f)

# Load HTML analysis for USCDI mapping
with open("fhir-html-analysis.json") as f:
    html = json.load(f)

# Extract USCDI mappings
uscdi_mappings = []
table = html["uscdi_table"]
for row in table:
    if len(row) >= 2 and row[0] != "USCDI" and not row[0].startswith("{"):
        uscdi_mappings.append({
            "uscdi_category": row[0],
            "fhir_resource": row[1]
        })

# Build entity inventory from CapabilityStatement resources
entities = []
for res in fhir["capability_statement"]["resources"]:
    # Find matching USCDI categories
    matching_uscdi = [m["uscdi_category"] for m in uscdi_mappings 
                      if m["fhir_resource"].lower().replace(" ", "") == res["type"].lower()]
    
    entities.append({
        "entity_name": res["type"],
        "source": "FHIR CapabilityStatement (g)(10) API",
        "category": "USCDI / US Core",
        "uscdi_mappings": matching_uscdi,
        "interactions": res["interactions"],
        "search_parameters": res["search_params"],
        "search_param_count": res["search_param_count"],
        "fields": "N/A - no field-level data dictionary provided",
        "field_count": None,
        "descriptions": "N/A",
        "note": "This is a FHIR resource type from the (g)(10) API, not a (b)(10) EHI export entity. No product-specific data dictionary exists."
    })

# Full inventory
full_inventory = {
    "product": "ARIA CORE",
    "version": "18.3",
    "vendor": "Varian Medical Systems (Siemens Healthineers)",
    "export_type": "No dedicated (b)(10) EHI export documentation found",
    "data_source": "FHIR R4 CapabilityStatement and USCDI mapping from (g)(10) API documentation",
    "ehi_documentation_url": "https://varian.com/aria/ehi (dead - returns 404)",
    "note": "The only available export documentation is the FHIR (g)(10) API at varian.dynamicfhir.com. No (b)(10)-specific data dictionary, schema, or export documentation was found. The FHIR API is explicitly USCDI-scoped and operates as a C-CDA pass-through.",
    "entities": entities,
    "total_entities": len(entities),
    "total_fields": None,
    "fields_with_descriptions": None,
    "uscdi_mappings": uscdi_mappings
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary
resource_types = [e["entity_name"] for e in entities]
uscdi_categories = list(set(m["uscdi_category"] for m in uscdi_mappings))

summary = {
    "product": "ARIA CORE v18.3",
    "vendor": "Varian Medical Systems (Siemens Healthineers)",
    "export_documentation_status": "NOT FOUND - registered URL returns 404",
    "registered_ehi_url": "https://varian.com/aria/ehi",
    "redirects_to": "https://cancercare.siemens-healthineers.com/aria/ehi (404)",
    "available_documentation": {
        "type": "FHIR R4 (g)(10) API only",
        "source": "https://varian.dynamicfhir.com/",
        "provider": "Dynamic Health IT (third-party)",
        "scope": "USCDI only - explicitly stated in documentation",
        "c_cda_passthrough": True,
        "c_cda_note": "Varian FHIR API assumes the use of a cumulative C-CDA with patient data"
    },
    "fhir_resource_types": len(resource_types),
    "fhir_resources": sorted(resource_types),
    "uscdi_category_count": len(uscdi_categories),
    "uscdi_categories": sorted(uscdi_categories),
    "conformance_method": "Attestation",
    "relied_upon_software": "Winzip",
    "data_dictionary": False,
    "field_level_documentation": False,
    "sample_data": False,
    "product_specific_mapping": False,
    "oncology_specific_data_in_export": False,
    "domains_covered": {
        "demographics": True,
        "encounters": True,
        "problems_conditions": True,
        "medications": True,
        "allergies": True,
        "immunizations": True,
        "vitals": True,
        "lab_results": True,
        "imaging_reports": True,
        "procedures": True,
        "clinical_notes": True,
        "care_plans_goals": True,
        "orders_referrals": False,
        "insurance_coverage": True,
        "claims_billing": False,
        "payments": False,
        "radiation_therapy_plans": False,
        "treatment_delivery_records": False,
        "cancer_staging": False,
        "chemotherapy_regimens": False,
        "toxicity_adverse_events": False,
        "disease_response": False,
        "qa_chart_checks": False,
        "medical_images_dicom": False,
        "patient_reported_outcomes": False,
        "survivorship_care_plans": False
    },
    "classification": {
        "coverage_breadth": "Minimal/stub/unclear",
        "export_approach": "Repackaged existing export",
        "rationale": "The registered (b)(10) EHI documentation URL is dead (404). The only available documentation is the FHIR (g)(10) API, which is explicitly USCDI-scoped, provided by a third party (Dynamic Health IT), and operates as a C-CDA pass-through. None of ARIA's core oncology data (radiation therapy plans, treatment delivery records, cancer staging, chemotherapy regimens, toxicity data, DICOM images) is documented in any export."
    }
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Created entity-inventory-full.json and entity-inventory-summary.json")
print(f"  FHIR resource types: {len(resource_types)}")
print(f"  USCDI categories mapped: {len(uscdi_categories)}")
print(f"  Field-level data dictionary: NO")
print(f"  (b)(10)-specific documentation: NOT FOUND")
