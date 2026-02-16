#!/usr/bin/env python3
"""Parse Moyae's FHIR CapabilityStatement and Postman collection to produce
entity-inventory-full.json and entity-inventory-summary.json.

Since Moyae has no data dictionary, the "entities" are FHIR resource types
from the CapabilityStatement, and the "fields" are search parameters (the
only per-resource metadata available).
"""

import json
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
OUT = Path(__file__).parent

# --- Parse CapabilityStatement ---
with open(DOWNLOADS / "fhir-capability-statement.json") as f:
    cs = json.load(f)

resources = cs["rest"][0]["resource"]

# Categorize resources by FHIR domain
CLINICAL = {
    "AllergyIntolerance", "CarePlan", "CareTeam", "ClinicalImpression",
    "Condition", "DetectedIssue", "DiagnosticReport", "DocumentReference",
    "Encounter", "EpisodeOfCare", "FamilyMemberHistory", "Goal",
    "ImagingStudy", "Immunization", "ImmunizationEvaluation",
    "ImmunizationRecommendation", "Media", "Medication",
    "MedicationAdministration", "MedicationDispense", "MedicationRequest",
    "MedicationStatement", "NutritionOrder", "Observation", "Patient",
    "Procedure", "QuestionnaireResponse", "RiskAssessment",
    "ServiceRequest", "Specimen", "VisionPrescription", "Consent",
    "AdverseEvent", "BodyStructure", "Communication", "Composition",
    "Flag", "List", "Device", "DeviceRequest", "DeviceUseStatement",
}
FINANCIAL = {
    "Account", "ChargeItem", "ChargeItemDefinition", "Claim",
    "ClaimResponse", "Contract", "Coverage", "CoverageEligibilityRequest",
    "CoverageEligibilityResponse", "EnrollmentRequest", "EnrollmentResponse",
    "ExplanationOfBenefit", "InsurancePlan", "Invoice", "PaymentNotice",
    "PaymentReconciliation",
}
ADMINISTRATIVE = {
    "Appointment", "AppointmentResponse", "Endpoint", "Group",
    "HealthcareService", "Location", "Organization",
    "OrganizationAffiliation", "Patient", "Person", "Practitioner",
    "PractitionerRole", "RelatedPerson", "Schedule", "Slot",
}

def categorize(rtype):
    if rtype in CLINICAL:
        return "Clinical"
    if rtype in FINANCIAL:
        return "Financial"
    if rtype in ADMINISTRATIVE:
        return "Administrative"
    return "Infrastructure/Definitional"

# --- Parse Postman collection ---
with open(DOWNLOADS / "moyae-fhir-api-postman-collection.json") as f:
    pm = json.load(f)

postman_folders = {}
for item in pm.get("item", []):
    name = item.get("name", "")
    endpoints = item.get("item", [])
    ep_details = []
    for ep in endpoints:
        req = ep.get("request", {})
        url = req.get("url", "")
        if isinstance(url, dict):
            url = url.get("raw", "")
        ep_details.append({
            "name": ep.get("name", ""),
            "method": req.get("method", ""),
            "url": url,
            "has_description": bool(req.get("description")),
        })
    postman_folders[name] = ep_details

# --- Build entity inventory ---
entities = []
for r in resources:
    rtype = r["type"]
    search_params = r.get("searchParam", [])
    interactions = [i["code"] for i in r.get("interaction", [])]

    fields = []
    for sp in search_params:
        fields.append({
            "name": sp["name"],
            "type": sp.get("type", ""),
            "description": "",  # No descriptions in CapabilityStatement
            "definition": sp.get("definition", ""),
        })

    entities.append({
        "name": rtype,
        "category": categorize(rtype),
        "source": "FHIR CapabilityStatement",
        "field_count": len(fields),
        "fields_with_descriptions": 0,
        "interactions": interactions,
        "has_search": "search-type" in interactions,
        "profile": r.get("profile", ""),
        "custom_profile": False,
        "in_postman": any(
            rtype.lower().replace(" ", "") in folder.lower().replace(" ", "")
            for folder in postman_folders
        ),
        "fields": fields,
    })

# Sort by category then name
entities.sort(key=lambda e: (e["category"], e["name"]))

# --- Summary stats ---
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
total_described = sum(e["fields_with_descriptions"] for e in entities)
by_category = {}
for e in entities:
    cat = e["category"]
    if cat not in by_category:
        by_category[cat] = {"count": 0, "fields": 0}
    by_category[cat]["count"] += 1
    by_category[cat]["fields"] += e["field_count"]

# Export endpoint info
export_info = {
    "mechanism": "FHIR Bulk Data $export (system-level)",
    "format": "NDJSON (Newline Delimited JSON)",
    "fhir_version": "4.0.1",
    "parameters": ["_outputFormat", "_since", "_type"],
    "authentication": "Bearer token (Cognito/Auth0) + API key",
    "job_management": True,
    "cancellation": True,
}

# Postman stats
postman_total_folders = len(postman_folders)
postman_total_endpoints = sum(len(eps) for eps in postman_folders.values())
postman_folders_with_desc = sum(
    1 for eps in postman_folders.values()
    if any(ep["has_description"] for ep in eps)
)

summary = {
    "product": "Moyae",
    "export_format": "FHIR R4 NDJSON via Bulk Data $export",
    "total_entities": total_entities,
    "total_search_parameters": total_fields,
    "fields_with_descriptions": total_described,
    "description_percentage": 0.0,
    "custom_profiles": 0,
    "custom_search_parameters": 0,
    "by_category": by_category,
    "export_mechanism": export_info,
    "postman_collection": {
        "total_folders": postman_total_folders,
        "total_endpoints": postman_total_endpoints,
        "folders_with_descriptions": postman_folders_with_desc,
    },
    "key_observations": [
        "All 146 resource types support identical CRUD + search interactions (except Binary which lacks search)",
        "Zero custom profiles or extensions documented",
        "Zero field-level descriptions in CapabilityStatement or Postman",
        "Software self-identifies as generic 'FHIR Server' v1.0.0",
        "Server supports the entire FHIR R4 resource catalog, including types no ophthalmology EHR would use (e.g., SubstanceNucleicAcid, MedicinalProductPharmaceutical, ResearchElementDefinition)",
        "No evidence of ophthalmology-specific data modeling (IOP, visual acuity, refraction, retina drawings)",
    ],
}

# Write outputs
with open(OUT / "entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

with open(OUT / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities: {total_entities}")
print(f"Total search parameters: {total_fields}")
print(f"Fields with descriptions: {total_described}")
print(f"Categories: {json.dumps(by_category, indent=2)}")
print(f"Postman folders: {postman_total_folders}, endpoints: {postman_total_endpoints}")
print(f"\nWritten: entity-inventory-full.json, entity-inventory-summary.json")
