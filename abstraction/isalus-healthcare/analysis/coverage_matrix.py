#!/usr/bin/env python3
"""Cross-reference schema files, sample export files, and XLSX data dictionary.
Produces a unified coverage matrix."""

import json
import os
from pathlib import Path

SCHEMA_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/schema/OfficeEMR_B10_Schema_v1-OCT2023")
SAMPLE_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/sample-export")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare/analysis")

# Gather all entity names from each source
schema_entities = set()
for f in SCHEMA_DIR.glob("*.json"):
    name = f.stem.replace(".schema", "")
    if name != "readme":
        schema_entities.add(name)

sample_entities = set()
sample_records = {}
for f in SAMPLE_DIR.glob("*.json"):
    name = f.stem
    if name == "readme":
        continue
    sample_entities.add(name)
    try:
        with open(f, encoding='utf-8-sig') as fh:
            data = json.load(fh)
        if isinstance(data, list):
            sample_records[name] = len(data)
        else:
            sample_records[name] = 1
    except:
        sample_records[name] = -1

# All entities
all_entities = sorted(schema_entities | sample_entities)

print(f"{'Entity':<45} {'Schema':>7} {'Sample':>7} {'Records':>8}")
print("-" * 72)
for e in all_entities:
    has_schema = "Yes" if e in schema_entities else "No"
    has_sample = "Yes" if e in sample_entities else "No"
    records = str(sample_records.get(e, "-"))
    print(f"{e:<45} {has_schema:>7} {has_sample:>7} {records:>8}")

print()
print(f"Schema-only entities (no sample data): {sorted(schema_entities - sample_entities)}")
print(f"Sample-only entities (no schema): {sorted(sample_entities - schema_entities)}")

# Domain classification
domain_map = {
    "demographics": "Demographics",
    "emergency_contact": "Demographics",
    "responsible_party": "Demographics",
    "insurance": "Insurance/Coverage",
    "eligibility": "Insurance/Coverage",
    "appointment": "Encounters/Visits",
    "template_encounter": "Encounters/Visits",
    "template_encounter_assessment": "Encounters/Visits",
    "template_encounter_exam": "Encounters/Visits",
    "template_encounter_history": "Encounters/Visits",
    "template_encounter_hpi": "Encounters/Visits",
    "template_encounter_order_fulfillment": "Encounters/Visits",
    "template_encounter_ros": "Encounters/Visits",
    "template_encounter_treatment_plan": "Encounters/Visits",
    "extension_encounter": "Encounters/Visits",
    "phone_encounter": "Encounters/Visits",
    "problem_list": "Problems/Diagnoses",
    "problem_list_note": "Problems/Diagnoses",
    "health_concern": "Problems/Diagnoses",
    "medication": "Medications",
    "optimize_rx": "Medications",
    "pharmacy": "Medications",
    "epa": "Medications",
    "allergy": "Allergies",
    "allergy_symptom": "Allergies",
    "immunization": "Immunizations",
    "immunization_registry": "Immunizations",
    "vital": "Vitals",
    "lab_result": "Lab Results",
    "order": "Orders/Referrals",
    "order_finding": "Orders/Referrals",
    "referral_tracking": "Orders/Referrals",
    "progress_note": "Clinical Notes",
    "letter": "Clinical Notes",
    "image_document": "Documents",
    "image_xref": "Documents",
    "hie": "Documents",
    "care_plan_goal": "Care Plans/Goals",
    "care_team": "Care Plans/Goals",
    "goal": "Care Plans/Goals",
    "goal_comment": "Care Plans/Goals",
    "goal_intervention": "Care Plans/Goals",
    "goal_objective": "Care Plans/Goals",
    "goal_problem": "Care Plans/Goals",
    "implantable_device": "Devices",
    "claim": "Billing/Claims",
    "claim_procedure": "Billing/Claims",
    "denial": "Billing/Claims",
    "statement": "Billing/Claims",
    "fee_schedule": "Billing/Claims",
    "sliding_fee": "Billing/Claims",
    "preschool_billing": "Billing/Claims",
    "price_estimate": "Billing/Claims",
    "price_estimate_line": "Billing/Claims",
    "payment": "Payments",
    "prior_authorization": "Authorizations",
    "prior_authorization_code": "Authorizations",
    "prior_authorization_rendering": "Authorizations",
    "consent": "Consents",
    "communication": "Communications",
    "communication_recipient": "Communications",
    "portal_message": "Communications",
    "comment": "Communications",
    "education": "Patient Education",
    "accident": "Accident/Injury",
    "pregnancy": "Specialty/Pregnancy",
    "pregnancy_visit": "Specialty/Pregnancy",
    "dialysis_setup": "Specialty/Dialysis",
    "dialysis_visit": "Specialty/Dialysis",
    "case_management": "Specialty/Case Mgmt",
    "case_management_ckcc_note": "Specialty/Case Mgmt",
    "ckcc_status": "Specialty/Case Mgmt",
    "chronic_care_management": "Specialty/Chronic Care",
    "md_revolution_status": "Specialty/RPM",
    "chart_share": "Chart Sharing",
    "chart_share_detail_all": "Chart Sharing",
    "chart_share_detail_individual": "Chart Sharing",
    "chart_share_detail_individual_1": "Chart Sharing",
    "chart_share_note": "Chart Sharing",
    "extension_results": "Lab Results",
}

# Summary by domain
from collections import defaultdict
domain_entities = defaultdict(list)
for e in all_entities:
    domain = domain_map.get(e, "Other/Unknown")
    domain_entities[domain].append(e)

print("\n=== Domain Coverage ===")
for domain in sorted(domain_entities.keys()):
    entities = domain_entities[domain]
    print(f"\n{domain}:")
    for e in entities:
        has_schema = "✓" if e in schema_entities else "✗"
        has_sample = "✓" if e in sample_entities else "✗"
        records = sample_records.get(e, 0)
        print(f"  {has_schema} schema {has_sample} sample ({records:>4} records) {e}")

# Save
output = {
    "total_schema_entities": len(schema_entities),
    "total_sample_entities": len(sample_entities),
    "total_unique_entities": len(all_entities),
    "schema_only": sorted(schema_entities - sample_entities),
    "sample_only": sorted(sample_entities - schema_entities),
    "domain_coverage": {d: entities for d, entities in sorted(domain_entities.items())}
}
with open(OUTPUT_DIR / "coverage_matrix.json", "w") as fh:
    json.dump(output, fh, indent=2)
print(f"\nSaved to {OUTPUT_DIR / 'coverage_matrix.json'}")
