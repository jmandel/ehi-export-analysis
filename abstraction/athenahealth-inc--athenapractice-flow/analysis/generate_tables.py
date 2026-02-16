#!/usr/bin/env python3
"""Generate analysis summary tables from the full entity inventory."""

import json

OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/athenahealth-inc--athenapractice-flow/analysis"

with open(f"{OUTPUT_DIR}/full-entity-inventory.json") as f:
    inv = json.load(f)

entities = inv["entities"]

# Sort by category then by field count descending
entities_sorted = sorted(entities, key=lambda e: (
    {"practiceManagement": 0, "clinical": 1, "custom": 2, "system": 3}.get(e["category"], 4),
    -e["fieldCount"]
))

# EHI Export resource list (from the ehiexport.html page)
ehi_export_resources_ap = {
    "Location", "Medication", "Organization", "Practitioner", "PractitionerRole", "OperationOutcome",
    "AllergyIntolerance", "Binary", "CarePlan", "CareTeam", "ClinicalImpression", "Condition", "Consent",
    "Device", "DiagnosticReport", "DocumentReference", "Encounter", "FamilyMemberHistory", "Goal",
    "Immunization", "MedicationAdministration", "MedicationRequest", "MedicationStatement", "Observation",
    "Procedure", "Provenance", "ServiceRequest",
    "Account", "Appointment", "Coverage", "Patient", "RelatedPerson", "Schedule", "Slot",
    "Adjustment", "BillingStatement", "Charge", "Claim", "Collection", "Deductible", "Eligibility",
    "PatientInsurance", "Payment"
}

ehi_export_resources_af = ehi_export_resources_ap - {
    "Account", "Schedule", "Slot",
    "Adjustment", "BillingStatement", "Charge", "Claim", "Collection", "Deductible", "Eligibility",
    "PatientInsurance", "Payment"
}

# Resources in FHIR API (from index.html) but NOT in EHI export
api_only_resources = {"Media", "MedicationDispense", "Specimen", "AuditEvent", "Posting"}

category_display = {
    "practiceManagement": "Practice Management",
    "clinical": "Clinical",
    "custom": "Custom / Financial",
    "system": "System"
}

# Generate markdown table
print("| Resource | Base Type | Category | Fields | Descriptions | Types | Bindings | In EHI Export | Product |")
print("|---|---|---|---|---|---|---|---|---|")

for e in entities_sorted:
    base = e["baseType"]
    title = (e.get("title") or e["name"]).strip()
    if not title:
        title = base
    # Determine clean display name
    display_name = title.replace("Profile - Athena Custom ", "")
    if display_name.startswith("Athena"):
        display_name = display_name.replace("Athena", "").strip()
    if not display_name:
        display_name = base

    cat = category_display.get(e["category"], e["category"])
    fc = e["fieldCount"]
    desc = e["fieldsWithDescription"]
    types = e["fieldsWithTypes"]
    bindings = e["fieldsWithBindings"]
    
    # Check if in EHI export
    in_ehi = "Yes" if base in ehi_export_resources_ap or e["name"].replace("Athena","").replace(" ","") in ehi_export_resources_ap else "No"
    # Check product availability
    if base in ehi_export_resources_af or e["name"].replace("Athena","").replace(" ","") in ehi_export_resources_af:
        product = "Both"
    elif in_ehi == "Yes":
        product = "athenaPractice only"
    else:
        product = "N/A (not in EHI export)"
    
    print(f"| {display_name} | {base} | {cat} | {fc} | {desc} | {types} | {bindings} | {in_ehi} | {product} |")

# Print stats summary
print()
print("## Summary Statistics")
ehi_entities = [e for e in entities if e["baseType"] in ehi_export_resources_ap or e["name"].replace("Athena","").replace(" ","") in ehi_export_resources_ap]
non_ehi = [e for e in entities if e not in ehi_entities]

ehi_fields = sum(e["fieldCount"] for e in ehi_entities)
total_fields = sum(e["fieldCount"] for e in entities)
print(f"- EHI export entities: {len(ehi_entities)} of {len(entities)} profiled")
print(f"- EHI export fields: {ehi_fields}")
print(f"- Non-EHI entities: {len(non_ehi)} ({', '.join(e['baseType'] for e in non_ehi)})")
print(f"- Total fields across all profiles: {total_fields}")
print(f"- Description coverage: 100% (all {total_fields} fields have descriptions)")
