#!/usr/bin/env python3
"""
Parse the enrichment data from 1Life (One Medical) EHI export documentation.
Produces full-entity-inventory.json and summary statistics.
"""
import json
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 
    "../../../results/1life-healthcare-inc--1life/downloads")
OUTPUT_DIR = os.path.dirname(__file__)

# Load the pre-extracted FHIR resources
with open(os.path.join(RESULTS_DIR, "enrichment/fhir-resources.json")) as f:
    fhir_resources = json.load(f)

with open(os.path.join(RESULTS_DIR, "enrichment/ehi-export-summary.json")) as f:
    ehi_summary = json.load(f)

# Build full entity inventory
inventory = {
    "metadata": {
        "vendor": "1Life Healthcare, Inc (One Medical)",
        "product": "1Life",
        "export_format": "FHIR R4 JSON Bundle + C-CDA v2.1 XML (ZIP)",
        "source": "https://apidocs.onemedical.io/ehi_export/overview/",
        "extraction_date": "2026-02-16"
    },
    "ehi_export_fhir_resource_types": [
        "AllergyIntolerance", "CareTeam", "Communication", "Condition",
        "Consent", "Device", "DiagnosticReport", "DocumentReference",
        "Encounter", "Goal", "Immunization", "MedicationRequest",
        "Observation", "Patient", "Procedure", "ServiceRequest"
    ],
    "ehi_export_ccda_sections": ehi_summary["ehiExport"]["formats"]["xml"]["ccdaSections"],
    "documented_fhir_resources": [],
    "undocumented_ehi_resources": [],
    "summary": {}
}

# Categorize each FHIR resource by clinical domain
DOMAIN_MAP = {
    "Patient": "Demographics",
    "Organization": "Demographics (Supporting)",
    "Location": "Demographics (Supporting)",
    "Practitioner": "Demographics (Supporting)",
    "Provenance": "Demographics (Supporting)",
    "Encounter": "Encounters / Visits",
    "Condition": "Problems / Conditions / Diagnoses",
    "MedicationRequest": "Medications / Prescriptions",
    "Medication": "Medications / Prescriptions",
    "AllergyIntolerance": "Allergies",
    "Immunization": "Immunizations",
    "Observation": "Vitals / Labs / Social History",
    "DiagnosticReport": "Lab Results / Diagnostic Reports",
    "DocumentReference": "Clinical Notes / Documents",
    "Procedure": "Procedures",
    "CarePlan": "Care Plans / Goals",
    "CareTeam": "Care Plans / Goals",
    "ServiceRequest": "Orders / Referrals",
    "Coverage": "Insurance / Coverage",
    "Device": "Medical Equipment / Devices",
    "Questionnaire": "Questionnaires / Assessments",
    "QuestionnaireResponse": "Questionnaires / Assessments",
}

total_fields = 0
total_with_descriptions = 0
total_with_types = 0

ehi_listed = set(inventory["ehi_export_fhir_resource_types"])
documented_names = set()

for resource in fhir_resources:
    rt = resource["resourceType"]
    # Normalize capitalization
    rt_normalized = rt[0].upper() + rt[1:]
    # Fix known casing issues
    casing_fixes = {
        "Allergyintolerance": "AllergyIntolerance",
        "Careplan": "CarePlan",
        "Careteam": "CareTeam",
        "Diagnosticreport": "DiagnosticReport",
        "Documentreference": "DocumentReference",
        "Medicationrequest": "MedicationRequest",
        "Questionnaireresponse": "QuestionnaireResponse",
        "Servicerequest": "ServiceRequest",
    }
    rt_fixed = casing_fixes.get(rt_normalized, rt_normalized)
    documented_names.add(rt_fixed)
    
    fields = []
    for table in resource.get("tables", []):
        for field in table.get("fields", []):
            desc = field.get("description", "").strip()
            ftype = field.get("type", "").strip()
            has_desc = len(desc) > 0
            has_type = len(ftype) > 0
            
            total_fields += 1
            if has_desc:
                total_with_descriptions += 1
            if has_type:
                total_with_types += 1
                
            fields.append({
                "name": field.get("name", ""),
                "type": ftype if ftype else None,
                "cardinality": field.get("cardinality", ""),
                "description": desc if desc else None,
            })
    
    in_ehi = rt_fixed in ehi_listed
    domain = DOMAIN_MAP.get(rt_fixed, "Other")
    
    inventory["documented_fhir_resources"].append({
        "resourceType": rt_fixed,
        "domain": domain,
        "fieldCount": len(fields),
        "fieldsWithDescriptions": sum(1 for f in fields if f["description"]),
        "fieldsWithTypes": sum(1 for f in fields if f["type"]),
        "inEhiExport": in_ehi,
        "sourceUrl": resource.get("sourceUrl", ""),
        "fields": fields
    })

# Identify undocumented EHI resources (listed on EHI page but no doc page)
for rt in ehi_listed:
    if rt not in documented_names:
        inventory["undocumented_ehi_resources"].append(rt)

# Summary statistics
inventory["summary"] = {
    "documented_resource_count": len(fhir_resources),
    "ehi_listed_resource_count": len(ehi_listed),
    "undocumented_ehi_resources": sorted(inventory["undocumented_ehi_resources"]),
    "supporting_resources_not_in_ehi": sorted(documented_names - ehi_listed),
    "total_fields": total_fields,
    "fields_with_descriptions": total_with_descriptions,
    "fields_with_types": total_with_types,
    "description_coverage_pct": round(total_with_descriptions / total_fields * 100, 1) if total_fields else 0,
    "type_coverage_pct": round(total_with_types / total_fields * 100, 1) if total_fields else 0,
    "ccda_section_count": len(inventory["ehi_export_ccda_sections"]),
    "extensions_count": len(ehi_summary.get("extensions", [])),
    "custom_terminology_codes": len(ehi_summary.get("terminology", [])),
}

# Domain breakdown
domain_breakdown = {}
for r in inventory["documented_fhir_resources"]:
    d = r["domain"]
    if d not in domain_breakdown:
        domain_breakdown[d] = {"resources": 0, "fields": 0, "in_ehi": 0}
    domain_breakdown[d]["resources"] += 1
    domain_breakdown[d]["fields"] += r["fieldCount"]
    if r["inEhiExport"]:
        domain_breakdown[d]["in_ehi"] += 1

inventory["summary"]["domain_breakdown"] = domain_breakdown

# Write full inventory
output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== 1Life EHI Export Inventory Summary ===")
print(f"Documented FHIR resources: {inventory['summary']['documented_resource_count']}")
print(f"EHI export listed resources: {inventory['summary']['ehi_listed_resource_count']} (unique, after dedup)")
print(f"Undocumented EHI resources: {inventory['summary']['undocumented_ehi_resources']}")
print(f"Supporting resources (documented but not in EHI list): {inventory['summary']['supporting_resources_not_in_ehi']}")
print(f"Total fields: {inventory['summary']['total_fields']}")
print(f"Fields with descriptions: {inventory['summary']['fields_with_descriptions']} ({inventory['summary']['description_coverage_pct']}%)")
print(f"Fields with types: {inventory['summary']['fields_with_types']} ({inventory['summary']['type_coverage_pct']}%)")
print(f"C-CDA sections: {inventory['summary']['ccda_section_count']}")
print(f"FHIR extensions: {inventory['summary']['extensions_count']}")
print(f"Custom terminology codes: {inventory['summary']['custom_terminology_codes']}")

print("\n=== Domain Breakdown ===")
for domain, info in sorted(domain_breakdown.items()):
    print(f"  {domain}: {info['resources']} resources, {info['fields']} fields ({info['in_ehi']} in EHI export)")

print(f"\n=== Per-Resource Field Counts ===")
for r in sorted(inventory["documented_fhir_resources"], key=lambda x: -x["fieldCount"]):
    ehi_marker = "✓" if r["inEhiExport"] else " "
    print(f"  [{ehi_marker}] {r['resourceType']:25s} {r['fieldCount']:3d} fields  ({r['fieldsWithDescriptions']} described, {r['fieldsWithTypes']} typed)")

print(f"\nFull inventory written to: {output_path}")
