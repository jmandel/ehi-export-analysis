#!/usr/bin/env python3
"""
Build the full entity inventory for Radysans EHR's (b)(10) export.
Combines C-CDA sections from the B-10 doc and FHIR resources from the G10 doc.
This is the canonical machine-readable extraction.
"""
import json

# Load parsed artifacts
with open("b10_ccda_inventory.json") as f:
    b10 = json.load(f)

with open("fhir_resource_inventory.json") as f:
    g10 = json.load(f)

# Clean up C-CDA section names
ccda_sections = []
for raw in b10["export_formats"][0]["sections"]:
    name = raw.replace("\uf0b7", "").strip()
    ccda_sections.append(name)

# Build the full inventory
inventory = {
    "vendor": "Radysans, Inc",
    "product": "Radysans EHR v5.0",
    "chpl_id": "15.04.04.2912.Rady.05.00.1.191231",
    "analysis_date": "2026-02-16",
    "export_type": "standard-based projection",
    "export_model": "C-CDA + FHIR R4 US Core (no native database export)",
    
    "ccda_export": {
        "format": "HL7 C-CDA XML",
        "standard": "USCDI v1",
        "section_count": len(ccda_sections),
        "sections": [
            {"name": s, "fields": "N/A - no field-level documentation", "description": "N/A"} 
            for s in ccda_sections
        ],
        "documentation_quality": {
            "has_field_definitions": False,
            "has_value_sets": False,
            "has_relationships": False,
            "has_sample_data": False,
            "has_schema": False,
            "detail_level": "section names only"
        }
    },
    
    "fhir_export": {
        "format": "FHIR R4 JSON",
        "standard": "US Core STU 3.1.1",
        "transport": "FHIR Bulk Data (claimed)",
        "base_url": "https://ehrwebapi.cutecharts.com/radywebapi/",
        "resource_count": g10["total_fhir_resources"],
        "resources": [],
        "documentation_quality": {
            "has_field_definitions": False,
            "has_value_sets": True,  # via standard FHIR coding
            "has_relationships": True,  # via FHIR references
            "has_sample_data": True,  # each resource has sample JSON
            "has_schema": False,  # no StructureDefinitions
            "detail_level": "sample JSON output per resource (implicit field documentation)"
        }
    },
    
    "costs_and_fees": {
        "source": "RadysansEHRCostsandLimitations.pdf",
        "data_portability_cost": "One-time fee per provider upon request of data extraction",
        "notes": "Suggests manual/vendor-assisted process rather than self-service"
    },
    
    "missing_from_export": [
        "Billing/claims data (product has full eBilling module)",
        "Insurance/coverage data (product has eligibility verification)",
        "Payment records and EOB/ERA data",
        "Appointment/scheduling data (product has enterprise scheduling)",
        "Patient registration scanned documents (photos, insurance cards)",
        "Referral management and pre-authorization tracking",
        "Transcription records (product offers transcription with long-term storage)",
        "Patient portal activity and messaging",
        "Custom forms or specialty-specific clinical data beyond USCDI"
    ],
    
    "coverage_assessment": {
        "domains_applicable": 17,
        "domains_covered": 12,
        "domains_partial": 1,
        "domains_not_covered": 4,
        "coverage_ratio": "12/17 applicable domains (clinical only; no admin/financial)"
    }
}

# Build FHIR resource details
for r in g10["resources"]:
    params = [p.replace("\uf0b7", "").strip() for p in r["parameters"]]
    inventory["fhir_export"]["resources"].append({
        "resource_type": r["resource_type"],
        "section_in_doc": r["section"],
        "endpoint_url": r["url"],
        "search_parameters": params,
        "has_sample_output": r["has_sample_output"],
        "fields": "N/A - defined by US Core profile, no vendor-specific extensions documented"
    })

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary stats
print(f"Export Type: {inventory['export_type']}")
print(f"C-CDA Sections: {inventory['ccda_export']['section_count']}")
print(f"FHIR Resources: {inventory['fhir_export']['resource_count']}")
print(f"Data Dictionary: No")
print(f"Native Database Export: No")
print(f"Field-level Documentation: No (except via FHIR sample outputs)")
print(f"Domains Covered: {inventory['coverage_assessment']['domains_covered']}/{inventory['coverage_assessment']['domains_applicable']}")
print(f"\nMissing domains:")
for m in inventory["missing_from_export"]:
    print(f"  - {m}")
