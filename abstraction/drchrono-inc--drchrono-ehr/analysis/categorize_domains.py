#!/usr/bin/env python3
"""Categorize drchrono EHI export entities by domain and produce summary stats."""

import json

with open("entity-inventory-full.json") as f:
    data = json.load(f)

# Use Bulk Patient Export as most complete
bulk = data["Bulk Patient Export"]

# Domain categorization based on entity names and known data
DOMAIN_MAP = {
    "Demographics": [
        "demographics.csv", "additional_responsible_party.csv", "responsible_party_address.csv",
        "person.csv", "tribal_affiliations.csv", "uscdi_occupation_code.csv",
        "uscdi_industry_code.csv", "ethnicity_subcategories_1.csv", "race_subcategories_1.csv",
        "iz_patient_demographic.csv", "patient_occupation.csv",
    ],
    "Encounters / Visits": [
        "appointments.csv", "case_report_encounters.csv",
    ],
    "Problems / Conditions": [
        "problems.csv",
    ],
    "Medications / Prescriptions": [
        "prescription.csv", "patient_drug.csv", "prescription_message.csv",
        "cover_my_meds_pa_request.csv", "pa_request_medication.csv",
    ],
    "Allergies": [
        "allergies.csv", "allergy_snomed_code_mapping.csv",
    ],
    "Immunizations": [
        "patient_vaccination_record.csv", "patientvaccinerecord_doses.csv",
    ],
    "Vitals": [
        "system_vitals.csv", "system_vitals_author.csv", "custom_vital_value.csv",
        "custom_vital_type.csv",
    ],
    "Lab Results": [
        "lab_result.csv", "patient_lab_result_set.csv", "lab_order.csv",
        "lab_order_document.csv", "lab_order_icd10_codes.csv", "lab_result_author.csv",
        "lab_quest_cd_order_code.csv", "lab_quest_cd_order_code_aoe.csv",
    ],
    "Imaging / Diagnostic Reports": [
        "patient_imaging_order.csv",
    ],
    "Procedures": [
        "procedures.csv",
    ],
    "Clinical Notes / Documents": [
        "clinical_notes.csv", "clinical_observation.csv", "clinical_observation_snomed_details.csv",
        "custom_clinical_note_sections.csv", "note_section_comments.csv",
        "soap_note_line_item_field_value.csv", "soap_note_line_item_field_type.csv",
        "soap_note_custom_report.csv", "uploaded_documents.csv", "exported_documents",
        "clinical_note_archives.csv" if any(e["entity_name"] == "clinical_note_archives.csv" for e in bulk["entities"]) else None,
        "clinical_list.csv",
    ],
    "Care Plans / Goals": [
        "care_plans.csv", "care_plan_authors.csv", "care_plan_goals.csv",
        "care_plan_goal_attached_codes.csv", "care_plan_goal_problems.csv",
        "care_plan_interventions.csv", "care_plan_goal_interventions_codes.csv",
        "care_plan_objectives.csv",
    ],
    "Care Team": [
        "care_team_member.csv", "doctor_staff_Care_team_members.csv",
        "external_Care_team_members.csv", "patient_as_care_team_members.csv",
    ],
    "Family History": [
        "family_history.csv", "relationship.csv",
    ],
    "Functional / Mental Status": [
        "functional_statuses.csv", "functional_status_authors.csv",
        "mental_statuses.csv", "mental_status_authors.csv",
        "social_history.csv", "social_history_author.csv",
    ],
    "Insurance / Coverage": [
        "primary_hospital_insurance.csv", "auto_accident_insurance.csv",
        "auto_accident_insurance_accident.csv", "workers_comp_insurance.csv",
        "insurance_authorizations.csv",
    ],
    "Claims / Billing": [
        "claims.csv", "payments_insurance.csv", "payments_patient.csv",
        "patient_cost_estimator.csv",
    ],
    "Devices": [
        "implantable_devices.csv", "implantable_device_authors.csv",
        "patient_device_orders.csv",
    ],
    "Referrals": [
        "inbound_referrals.csv", "outbound_referrals.csv",
    ],
    "Communications / Messages": [
        "history_message.csv", "doctor_message.csv", "doctor_message_log.csv",
        "direct_message.csv", "direct_message_attachment.csv",
        "patient_message.csv", "patient_message_attachment.csv",
        "outgoing_patient_message_status.csv", "communication_log.csv",
    ],
    "Consent Forms": [
        "consent_forms.csv", "consent_form_assignments.csv",
        "consent_form_signatures.csv", "consent_form_signature_audit_logs.csv",
    ],
    "Clinical Decision Support": [
        "clinical_decision_support_rules.csv", "patient_specific_actions.csv",
    ],
    "Education": [
        "education_resource.csv", "education_resource_recommendation.csv",
        "mu_patient_education_log.csv",
    ],
    "Patient Flags": [
        "patient_flags.csv",
    ],
    "Provider / Practice": [
        "doctors.csv", "offices.csv", "practice_group.csv",
        "patient_import_ccda_file.csv", "mu_syndromic_surveillance_log.csv",
    ],
}

# Remove None values
for k in DOMAIN_MAP:
    DOMAIN_MAP[k] = [v for v in DOMAIN_MAP[k] if v is not None]

# Build lookup
entity_lookup = {e["entity_name"]: e for e in bulk["entities"]}

domain_stats = []
categorized = set()
for domain, entities in DOMAIN_MAP.items():
    total_fields = 0
    total_described = 0
    matched = []
    for ename in entities:
        if ename in entity_lookup:
            e = entity_lookup[ename]
            total_fields += e["field_count"]
            total_described += e["fields_with_description"]
            matched.append(ename)
            categorized.add(ename)
    domain_stats.append({
        "domain": domain,
        "entity_count": len(matched),
        "total_fields": total_fields,
        "fields_with_description": total_described,
        "entities": matched
    })

# Check for uncategorized
uncategorized = [e["entity_name"] for e in bulk["entities"] if e["entity_name"] not in categorized]
if uncategorized:
    print("UNCATEGORIZED entities:")
    for u in uncategorized:
        print(f"  {u}")
    print()

# Print domain summary
print(f"{'Domain':<40s} {'Entities':>8s} {'Fields':>8s} {'Described':>10s}")
print("-" * 70)
grand_entities = 0
grand_fields = 0
grand_described = 0
for ds in sorted(domain_stats, key=lambda x: -x["total_fields"]):
    print(f"{ds['domain']:<40s} {ds['entity_count']:>8d} {ds['total_fields']:>8d} {ds['fields_with_description']:>10d}")
    grand_entities += ds["entity_count"]
    grand_fields += ds["total_fields"]
    grand_described += ds["fields_with_description"]
print("-" * 70)
print(f"{'TOTAL':<40s} {grand_entities:>8d} {grand_fields:>8d} {grand_described:>10d}")

# Save
with open("domain-categorization.json", "w") as f:
    json.dump(domain_stats, f, indent=2)
