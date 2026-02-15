#!/usr/bin/env python3
"""Parse the glossary HTML and the XLSX to create a categorized entity inventory."""
import json
import openpyxl
from collections import defaultdict

XLSX_PATH = "../../../results/drchrono-inc--drchrono-ehr/downloads/drchrono-ehi-export-documentation-v18.xlsx"

# Category mappings based on the glossary/reference guide organization
# and the content of each CSV file
CATEGORY_MAP = {
    # Doctor Exporter
    "doctors.csv": "Doctor Exporter",
    "custom_vital_type.csv": "Doctor Exporter",
    "education_resource.csv": "Doctor Exporter",
    "mu_syndromic_surveillance_log.csv": "Doctor Exporter",
    "offices.csv": "Doctor Exporter",
    "patient_import_ccda_file.csv": "Doctor Exporter",
    "soap_note_custom_report.csv": "Doctor Exporter",
    "soap_note_line_item_field_type.csv": "Doctor Exporter",
    
    # Practice Group Exporter
    "lab_quest_cd_order_code.csv": "Practice Group Exporter",
    "lab_quest_cd_order_code_aoe.csv": "Practice Group Exporter",
    "practice_group.csv": "Practice Group Exporter",
    
    # Patient Exporter - Demographics
    "demographics.csv": "Demographics",
    "patient_occupation.csv": "Demographics",
    "uscdi_occupation_code.csv": "Demographics",
    "uscdi_industry_code.csv": "Demographics",
    "tribal_affiliations.csv": "Demographics",
    "ethnicity_subcategories.csv": "Demographics",
    "race_subcategories.csv": "Demographics",
    
    # Patient Exporter - Responsible Parties
    "additional_responsible_party.csv": "Responsible Parties",
    "responsible_party_address.csv": "Responsible Parties",
    
    # Patient Exporter - Allergies
    "allergies.csv": "Allergies",
    "allergy_snomed_code_mapping.csv": "Allergies",
    
    # Patient Exporter - Appointments
    "appointments.csv": "Appointments",
    
    # Patient Exporter - Insurance
    "auto_accident_insurance.csv": "Insurance",
    "auto_accident_insurance_accident.csv": "Insurance",
    "primary_hospital_insurance.csv": "Insurance",
    "workers_comp_insurance.csv": "Insurance",
    "insurance_authorizations.csv": "Insurance",
    
    # Patient Exporter - Care Plans
    "care_plan.csv": "Care Plans",
    "care_plan_author.csv": "Care Plans",
    "care_plan_goal_attached_codes.csv": "Care Plans",
    "care_plan_goal_problems.csv": "Care Plans",
    "care_plan_goals.csv": "Care Plans",
    "care_plan_intervention_attached_codes.csv": "Care Plans",
    "care_plan_interventions.csv": "Care Plans",
    "care_plan_objectives.csv": "Care Plans",
    
    # Patient Exporter - Care Team
    "care_team_member.csv": "Care Team",
    "doctor_staff_care_team_members.csv": "Care Team",
    "external_care_team_members.csv": "Care Team",
    "patient_as_care_team_members.csv": "Care Team",
    
    # Patient Exporter - Claims & Billing
    "claims.csv": "Claims & Billing",
    "payments_insurance.csv": "Claims & Billing",
    "payments_patient.csv": "Claims & Billing",
    "patient_cost_estimator.csv": "Claims & Billing",
    
    # Patient Exporter - Clinical Notes
    "clinical_notes.csv": "Clinical Notes",
    "clinical_note_archives.csv": "Clinical Notes",
    "custom_clinical_note_sections.csv": "Clinical Notes",
    "note_section_comments.csv": "Clinical Notes",
    "soap_note_line_item_field_value.csv": "Clinical Notes",
    
    # Patient Exporter - Clinical Decision Support
    "clinical_decision_support_rules.csv": "Clinical Decision Support",
    "patient_specific_actions.csv": "Clinical Decision Support",
    
    # Patient Exporter - Family History
    "family_history.csv": "Family History",
    "clinical_observation.csv": "Family History",
    "clinical_observation_snomed_details.csv": "Family History",
    "person.csv": "Family History",
    "relationship.csv": "Family History",
    
    # Patient Exporter - Consent Forms
    "consent_form_assignments.csv": "Consent Forms",
    "consent_form_signatures.csv": "Consent Forms",
    "consent_form_signature_audit_logs.csv": "Consent Forms",
    
    # Patient Exporter - Communications
    "communication_log.csv": "Communications",
    "direct_message.csv": "Communications",
    "direct_message_attachment.csv": "Communications",
    "doctor_message.csv": "Communications",
    "doctor_message_log.csv": "Communications",
    "history_message.csv": "Communications",
    "outgoing_patient_message_status.csv": "Communications",
    "patient_message.csv": "Communications",
    "patient_message_attachment.csv": "Communications",
    "prescription_message.csv": "Communications",
    
    # Patient Exporter - Vitals
    "system_vitals.csv": "Vitals",
    "system_vitals_author.csv": "Vitals",
    "custom_vital_value.csv": "Vitals",
    
    # Patient Exporter - Medications
    "patient_drug.csv": "Medications",
    "prescription.csv": "Medications",
    "cover_my_meds_pa_request.csv": "Medications",
    "pa_request_medication.csv": "Medications",
    
    # Patient Exporter - Immunizations
    "patient_vaccination_record.csv": "Immunizations",
    "patientvaccinerecord_doses.csv": "Immunizations",
    "iz_patient_demographic.csv": "Immunizations",
    
    # Patient Exporter - Labs
    "lab_order.csv": "Lab Orders & Results",
    "lab_order_document.csv": "Lab Orders & Results",
    "lab_order_icd10_codes.csv": "Lab Orders & Results",
    "lab_result.csv": "Lab Orders & Results",
    "lab_result_author.csv": "Lab Orders & Results",
    "patient_lab_result_set.csv": "Lab Orders & Results",
    
    # Patient Exporter - Problems
    "problems.csv": "Problems / Diagnoses",
    
    # Patient Exporter - Social History
    "social_history.csv": "Social History",
    "social_history_author.csv": "Social History",
    
    # Patient Exporter - Functional/Mental Status
    "functional_statuses.csv": "Functional & Mental Status",
    "functional_status_authors.csv": "Functional & Mental Status",
    "mental_statuses.csv": "Functional & Mental Status",
    "mental_status_authors.csv": "Functional & Mental Status",
    
    # Patient Exporter - Devices
    "implantable_devices.csv": "Devices",
    "implantable_device_authors.csv": "Devices",
    "patient_device_orders.csv": "Devices",
    
    # Patient Exporter - Referrals
    "inbound_referrals.csv": "Referrals",
    "outbound_referrals.csv": "Referrals",
    
    # Patient Exporter - Imaging
    "patient_imaging_order.csv": "Imaging",
    
    # Patient Exporter - Documents
    "uploaded_documents.csv": "Documents",
    
    # Patient Exporter - Education
    "education_resource_recommendation.csv": "Patient Education",
    "mu_patient_education_log.csv": "Patient Education",
    
    # Patient Exporter - Case Reporting
    "case_report_encounters.csv": "Case Reporting",
    
    # Patient Exporter - Patient Flags
    "patient_flags.csv": "Patient Flags",
    
    # Patient Exporter - Clinical List (CCDA import)
    "clinical_list.csv": "Imported CCDA Data",
    
    # Patient Exporter - Consent Forms (practice level)
    "consent_forms.csv": "Consent Forms",
}

wb = openpyxl.load_workbook(XLSX_PATH, read_only=True)

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    data = rows[1:]
    
    # Build categorized inventory
    entities = {}
    for row in data:
        export_name = str(row[0]).strip() if row[0] else None
        if not export_name:
            continue
        if export_name not in entities:
            entities[export_name] = {"fields": 0, "described": 0}
        entities[export_name]["fields"] += 1
        if row[2] and str(row[2]).strip():
            entities[export_name]["described"] += 1
    
    # Category summary
    category_stats = defaultdict(lambda: {"entities": 0, "fields": 0, "described": 0, "entity_list": []})
    uncategorized = []
    
    for entity_name, info in sorted(entities.items()):
        cat = CATEGORY_MAP.get(entity_name, None)
        if cat is None:
            uncategorized.append(entity_name)
            cat = "Uncategorized"
        category_stats[cat]["entities"] += 1
        category_stats[cat]["fields"] += info["fields"]
        category_stats[cat]["described"] += info["described"]
        category_stats[cat]["entity_list"].append(entity_name)
    
    print(f"\n=== {sheet_name} - Category Summary ===")
    print(f"{'Category':<30} {'Entities':>8} {'Fields':>8} {'Described':>10}")
    print("-" * 60)
    for cat in sorted(category_stats.keys()):
        s = category_stats[cat]
        print(f"{cat:<30} {s['entities']:>8} {s['fields']:>8} {s['described']:>10}")
    
    if uncategorized:
        print(f"\nUncategorized entities: {uncategorized}")

# Also check what fields lack descriptions in bulk export
ws = wb["Bulk Patient Export"]
rows = list(ws.iter_rows(values_only=True))
data = rows[1:]
missing_desc = []
for row in data:
    if not row[2] or not str(row[2]).strip():
        missing_desc.append((str(row[0]).strip() if row[0] else "?", str(row[1]).strip() if row[1] else "?"))

print(f"\n=== Fields WITHOUT descriptions in Bulk Export ({len(missing_desc)} total) ===")
for entity, field in missing_desc:
    print(f"  {entity} -> {field}")

wb.close()
