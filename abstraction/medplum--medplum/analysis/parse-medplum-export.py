#!/usr/bin/env python3
"""
Parse Medplum FHIR export documentation artifacts to produce:
  - entity-inventory-full.json: Complete resource/field inventory
  - entity-inventory-summary.json: Summary statistics
  
Sources:
  - downloads/capability-statement.json (FHIR CapabilityStatement)
  - downloads/openapi.json (OpenAPI 3.1 spec with all FHIR schemas)
  - downloads/patienteverything.ts (source code for $patient-everything)
"""

import json
import os
import sys
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..")
DOWNLOADS = os.path.join(BASE, "downloads")
OUTPUT_DIR = os.path.dirname(__file__)

# FHIR R4 Patient Compartment definition
# https://hl7.org/fhir/R4/compartmentdefinition-patient.html
PATIENT_COMPARTMENT_RESOURCES = {
    "Account", "AdverseEvent", "AllergyIntolerance", "Appointment",
    "AppointmentResponse", "AuditEvent", "Basic", "BodyStructure",
    "CarePlan", "CareTeam", "ChargeItem", "Claim", "ClaimResponse",
    "ClinicalImpression", "Communication", "CommunicationRequest",
    "Composition", "Condition", "Consent", "Coverage",
    "CoverageEligibilityRequest", "CoverageEligibilityResponse",
    "DetectedIssue", "DeviceRequest", "DeviceUseStatement",
    "DiagnosticReport", "DocumentManifest", "DocumentReference",
    "Encounter", "EnrollmentRequest", "EpisodeOfCare",
    "ExplanationOfBenefit", "FamilyMemberHistory", "Flag", "Goal",
    "Group", "GuidanceResponse", "ImagingStudy", "Immunization",
    "ImmunizationEvaluation", "ImmunizationRecommendation", "Invoice",
    "List", "MeasureReport", "Media", "MedicationAdministration",
    "MedicationDispense", "MedicationRequest", "MedicationStatement",
    "MolecularSequence", "NutritionOrder", "Observation", "Patient",
    "Person", "Procedure", "Provenance", "QuestionnaireResponse",
    "RelatedPerson", "RequestGroup", "ResearchSubject", "RiskAssessment",
    "Schedule", "ServiceRequest", "Specimen", "SupplyDelivery",
    "SupplyRequest", "Task", "VisionPrescription"
}

# Additional resource types resolved by $patient-everything (from source code)
RESOLVED_REFERENCE_TYPES = {
    "Organization", "Location", "Practitioner", "PractitionerRole",
    "Medication", "Device"
}

# Domain categorization for FHIR resource types
DOMAIN_MAP = {
    # Demographics
    "Patient": "Demographics",
    "Person": "Demographics",
    "RelatedPerson": "Demographics",
    
    # Encounters
    "Encounter": "Encounters / Visits",
    "EpisodeOfCare": "Encounters / Visits",
    
    # Problems / Conditions
    "Condition": "Problems / Conditions",
    "ClinicalImpression": "Problems / Conditions",
    
    # Medications
    "Medication": "Medications / Prescriptions",
    "MedicationRequest": "Medications / Prescriptions",
    "MedicationAdministration": "Medications / Prescriptions",
    "MedicationDispense": "Medications / Prescriptions",
    "MedicationStatement": "Medications / Prescriptions",
    
    # Allergies
    "AllergyIntolerance": "Allergies",
    
    # Immunizations
    "Immunization": "Immunizations",
    "ImmunizationEvaluation": "Immunizations",
    "ImmunizationRecommendation": "Immunizations",
    
    # Vitals/Labs/Observations
    "Observation": "Observations (Vitals, Labs, etc.)",
    
    # Diagnostic
    "DiagnosticReport": "Diagnostic Reports / Imaging",
    "ImagingStudy": "Diagnostic Reports / Imaging",
    "Media": "Diagnostic Reports / Imaging",
    "MolecularSequence": "Diagnostic Reports / Imaging",
    "Specimen": "Diagnostic Reports / Imaging",
    
    # Procedures
    "Procedure": "Procedures",
    
    # Documents / Notes
    "Composition": "Clinical Notes / Documents",
    "DocumentReference": "Clinical Notes / Documents",
    "DocumentManifest": "Clinical Notes / Documents",
    
    # Care Plans / Goals
    "CarePlan": "Care Plans / Goals",
    "CareTeam": "Care Plans / Goals",
    "Goal": "Care Plans / Goals",
    "NutritionOrder": "Care Plans / Goals",
    
    # Orders / Referrals
    "ServiceRequest": "Orders / Referrals",
    "DeviceRequest": "Orders / Referrals",
    "RequestGroup": "Orders / Referrals",
    "Task": "Orders / Referrals",
    "GuidanceResponse": "Orders / Referrals",
    "SupplyRequest": "Orders / Referrals",
    "SupplyDelivery": "Orders / Referrals",
    
    # Insurance / Coverage
    "Coverage": "Insurance / Coverage",
    "CoverageEligibilityRequest": "Insurance / Coverage",
    "CoverageEligibilityResponse": "Insurance / Coverage",
    "EnrollmentRequest": "Insurance / Coverage",
    
    # Claims / Billing
    "Claim": "Claims / Billing",
    "ClaimResponse": "Claims / Billing",
    "ExplanationOfBenefit": "Claims / Billing",
    "ChargeItem": "Claims / Billing",
    "Invoice": "Claims / Billing",
    "Account": "Claims / Billing",
    
    # Consents
    "Consent": "Consents / Directives",
    
    # Communications
    "Communication": "Patient Communications",
    "CommunicationRequest": "Patient Communications",
    
    # Devices
    "Device": "Medical Devices",
    "DeviceUseStatement": "Medical Devices",
    
    # Family History
    "FamilyMemberHistory": "Family Health History",
    
    # Risk / Assessment
    "RiskAssessment": "Risk Assessments",
    
    # Questionnaires
    "QuestionnaireResponse": "Questionnaires / Forms",
    
    # Provenance
    "Provenance": "Provenance / Audit",
    "AuditEvent": "Provenance / Audit",
    
    # Other clinical
    "AdverseEvent": "Adverse Events",
    "DetectedIssue": "Clinical Decision Support",
    "Flag": "Alerts / Flags",
    "Basic": "Other",
    "BodyStructure": "Other Clinical",
    "List": "Other Clinical",
    "MeasureReport": "Quality Measures",
    "Schedule": "Scheduling",
    "Appointment": "Scheduling",
    "AppointmentResponse": "Scheduling",
    "Group": "Group / Population",
    "VisionPrescription": "Vision",
    "ResearchSubject": "Research",
    
    # Referenced types (not in compartment but resolved)
    "Organization": "Provider Directory",
    "Location": "Provider Directory",
    "Practitioner": "Provider Directory",
    "PractitionerRole": "Provider Directory",
}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def extract_openapi_fields(schema_name, schemas):
    """Extract fields from an OpenAPI schema definition."""
    schema = schemas.get(schema_name, {})
    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))
    
    fields = []
    for name, prop in properties.items():
        field = {
            "name": name,
            "type": resolve_type(prop, schemas),
            "description": prop.get("description", ""),
            "required": name in required_fields,
            "isArray": prop.get("type") == "array",
        }
        fields.append(field)
    
    return fields


def resolve_type(prop, schemas):
    """Resolve the type string from an OpenAPI property."""
    if "$ref" in prop:
        return prop["$ref"].split("/")[-1]
    if "type" in prop:
        if prop["type"] == "array":
            items = prop.get("items", {})
            if "$ref" in items:
                return items["$ref"].split("/")[-1] + "[]"
            return (items.get("type", "unknown") + "[]")
        return prop["type"]
    # oneOf / anyOf
    if "oneOf" in prop:
        types = []
        for opt in prop["oneOf"]:
            if "$ref" in opt:
                types.append(opt["$ref"].split("/")[-1])
            elif "type" in opt:
                types.append(opt["type"])
        return " | ".join(types)
    return "unknown"


def main():
    # Load sources
    cs = load_json(os.path.join(DOWNLOADS, "capability-statement.json"))
    oa = load_json(os.path.join(DOWNLOADS, "openapi.json"))
    
    schemas = oa.get("components", {}).get("schemas", {})
    
    # Get server resource types from CapabilityStatement
    rest = cs.get("rest", [{}])[0]
    server_resources = {r["type"]: r for r in rest.get("resource", [])}
    
    # Build resource inventory
    all_resources = []
    
    # Process all resource types from OpenAPI schemas
    # FHIR resource types have resourceType property
    resource_type_names = set()
    for name, schema in schemas.items():
        props = schema.get("properties", {})
        if "resourceType" in props:
            resource_type_names.add(name)
    
    # Also include all from CapabilityStatement
    for rt in server_resources:
        resource_type_names.add(rt)
    
    for rt_name in sorted(resource_type_names):
        fields = extract_openapi_fields(rt_name, schemas)
        
        in_compartment = rt_name in PATIENT_COMPARTMENT_RESOURCES
        is_resolved_ref = rt_name in RESOLVED_REFERENCE_TYPES
        in_export = in_compartment or is_resolved_ref
        
        # Get search params and interactions from CS
        cs_resource = server_resources.get(rt_name, {})
        search_params = []
        for sp in cs_resource.get("searchParam", []):
            search_params.append({
                "name": sp.get("name", ""),
                "type": sp.get("type", ""),
                "documentation": sp.get("documentation", "")
            })
        
        interactions = [i["code"] for i in cs_resource.get("interaction", [])]
        
        # Count described fields
        described = sum(1 for f in fields if f.get("description", "").strip())
        
        resource = {
            "resourceType": rt_name,
            "description": schemas.get(rt_name, {}).get("description", ""),
            "fields": fields,
            "fieldCount": len(fields),
            "fieldsWithDescriptions": described,
            "searchParams": search_params,
            "interactions": interactions,
            "inPatientCompartment": in_compartment,
            "isResolvedReference": is_resolved_ref,
            "inExport": in_export,
            "domain": DOMAIN_MAP.get(rt_name, "Other / Definitional"),
        }
        all_resources.append(resource)
    
    # Write full inventory
    with open(os.path.join(OUTPUT_DIR, "entity-inventory-full.json"), "w") as f:
        json.dump(all_resources, f, indent=2)
    
    # Build summary
    export_resources = [r for r in all_resources if r["inExport"]]
    compartment_resources = [r for r in all_resources if r["inPatientCompartment"]]
    
    total_fields = sum(r["fieldCount"] for r in all_resources)
    total_described = sum(r["fieldsWithDescriptions"] for r in all_resources)
    export_fields = sum(r["fieldCount"] for r in export_resources)
    export_described = sum(r["fieldsWithDescriptions"] for r in export_resources)
    
    # Domain breakdown
    domain_breakdown = defaultdict(lambda: {"resources": [], "resourceCount": 0, "fieldCount": 0, "inExport": False})
    for r in export_resources:
        d = r["domain"]
        domain_breakdown[d]["resources"].append(r["resourceType"])
        domain_breakdown[d]["resourceCount"] += 1
        domain_breakdown[d]["fieldCount"] += r["fieldCount"]
        domain_breakdown[d]["inExport"] = True
    
    # Category summary for export resources
    domain_summary = {}
    for domain, info in sorted(domain_breakdown.items()):
        domain_summary[domain] = {
            "resourceCount": info["resourceCount"],
            "fieldCount": info["fieldCount"],
            "resources": sorted(info["resources"])
        }
    
    # Top resources by field count (in export)
    top_resources = sorted(export_resources, key=lambda r: r["fieldCount"], reverse=True)[:20]
    top_summary = [{"resourceType": r["resourceType"], "fieldCount": r["fieldCount"], 
                     "fieldsWithDescriptions": r["fieldsWithDescriptions"], "domain": r["domain"]}
                    for r in top_resources]
    
    summary = {
        "total_resource_types": len(all_resources),
        "total_fields_all": total_fields,
        "total_fields_described_all": total_described,
        "description_pct_all": round(total_described / total_fields * 100, 1) if total_fields else 0,
        "in_export": {
            "total_resource_types": len(export_resources),
            "in_patient_compartment": len(compartment_resources),
            "resolved_references": len([r for r in all_resources if r["isResolvedReference"]]),
            "total_fields": export_fields,
            "total_fields_described": export_described,
            "description_pct": round(export_described / export_fields * 100, 1) if export_fields else 0,
        },
        "domain_breakdown": domain_summary,
        "top_20_resources_by_field_count": top_summary,
        "not_in_export_count": len(all_resources) - len(export_resources),
        "not_in_export_examples": [r["resourceType"] for r in all_resources if not r["inExport"]][:30],
    }
    
    with open(os.path.join(OUTPUT_DIR, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary to stdout
    print(f"=== Medplum EHI Export Inventory ===")
    print(f"Total resource types in platform: {len(all_resources)}")
    print(f"Total fields across all types: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({summary['description_pct_all']}%)")
    print()
    print(f"=== Export ($patient-everything) ===")
    print(f"Resource types in export: {len(export_resources)}")
    print(f"  In Patient Compartment: {len(compartment_resources)}")
    print(f"  Resolved references: {summary['in_export']['resolved_references']}")
    print(f"Fields in export resources: {export_fields}")
    print(f"Fields with descriptions: {export_described} ({summary['in_export']['description_pct']}%)")
    print()
    print(f"=== Domain Breakdown (export resources) ===")
    for domain, info in sorted(domain_summary.items()):
        print(f"  {domain}: {info['resourceCount']} resources, {info['fieldCount']} fields")
        for r in info['resources']:
            print(f"    - {r}")
    print()
    print(f"=== Top 20 Resources by Field Count ===")
    for r in top_summary:
        print(f"  {r['resourceType']}: {r['fieldCount']} fields ({r['fieldsWithDescriptions']} described) [{r['domain']}]")


if __name__ == "__main__":
    main()
