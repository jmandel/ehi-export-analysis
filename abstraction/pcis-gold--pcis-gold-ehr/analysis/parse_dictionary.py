#!/usr/bin/env python3
"""
Parse the PCIS GOLD EHI Export Data Table Definitions HTML page.
Extracts all table definitions with fields into JSON.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

HTML_PATH = Path(__file__).parent.parent / "downloads" / "ehi-export-data-table-definitions.html"
html = HTML_PATH.read_text(encoding="utf-8")

# Strategy: use regex to find each h2 section, then parse the table within it.
# Each table definition: <h2 id="linkXxx">TableName</h2>...<p>Description</p>...<table>...</table>

# Split HTML into sections by h2 tags
sections = re.split(r'(?=<h2\s)', html)

tables = []
for section in sections:
    # Match table name from h2
    h2_match = re.match(r'<h2\s+id="link[^"]*">([^<]+)</h2>', section)
    if not h2_match:
        continue
    table_name = h2_match.group(1).strip()
    
    # Skip the "Data Table Index" header
    if table_name == "Data Table Index":
        continue
    
    # Extract table description from <p> tag between h2 and table
    desc_match = re.search(r'</a>\s*<p>(.*?)</p>', section, re.DOTALL)
    table_desc = desc_match.group(1).strip() if desc_match else ""
    # Clean HTML tags from description
    table_desc = re.sub(r'<[^>]+>', '', table_desc).strip()
    
    # Extract field rows from the table
    fields = []
    # Find all <tr> blocks with <td> elements
    rows = re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>', section, re.DOTALL)
    for name, ftype, fdesc in rows:
        # Clean HTML from values
        name = re.sub(r'<[^>]+>', '', name).strip()
        ftype = re.sub(r'<[^>]+>', '', ftype).strip()
        fdesc = re.sub(r'<[^>]+>', '', fdesc).strip()
        # Decode HTML entities
        for ent, char in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&#39;', "'")]:
            name = name.replace(ent, char)
            ftype = ftype.replace(ent, char)
            fdesc = fdesc.replace(ent, char)
        fields.append({
            "name": name,
            "type": ftype,
            "description": fdesc
        })
    
    tables.append({
        "table_name": table_name,
        "table_description": table_desc,
        "field_count": len(fields),
        "fields": fields
    })

# Compute stats
total_fields = sum(t["field_count"] for t in tables)
fields_with_desc = sum(1 for t in tables for f in t["fields"] if f["description"])
fields_with_type = sum(1 for t in tables for f in t["fields"] if f["type"])

# Categorize tables by prefix/naming pattern
def categorize(name):
    nl = name.lower()
    
    # Exact matches first
    exact = {
        "Patients": "Demographics",
        "T_Patients": "Demographics",
        "T_Persons": "Demographics",
        "T_PatientAddress": "Demographics",
        "T_PatientPhones": "Demographics",
        "T_PatientEmergencyContact": "Demographics",
        "T_PatientNextOfKin": "Demographics",
        "T_PatientEthnicity": "Demographics",
        "T_PatientRaces": "Demographics",
        "T_PatientIndustries": "Demographics",
        "T_PatientOccupations": "Demographics",
        "T_PatientProviders": "Demographics",
        "T_CommunicationPreferences": "Demographics",
        "T_Employer": "Demographics",
        "T_Relationships": "Demographics",
        "T_PhoneTypes": "Demographics",
        "MiscAddress": "Demographics",
        "PatientHIPAA": "Demographics/Consent",
        "T_PatientHistory": "Patient History",
        "T_PatientHistoryLinks": "Patient History",
        "T_PatientPMH": "Patient History",
        "T_SmokingStatus": "Patient History",
        "T_PatientCognitiveStatus": "Health Assessments",
        "T_PatientFunctionalStatus": "Health Assessments",
        "Visits": "Visits/Encounters",
        "Visits_Reps": "Visits/Encounters",
        "T_Visits": "Visits/Encounters",
        "T_VisitsNonRegPatient": "Visits/Encounters",
        "T_VisitTypes": "Visits/Encounters",
        "T_VisitStatus": "Visits/Encounters",
        "T_VisitCancelCodes": "Visits/Encounters",
        "T_VisitPatientInfo": "Visits/Encounters",
        "T_VisitStr": "Visits/Encounters",
        "T_VisitCompletionHistory": "Visits/Encounters",
        "T_VisitCompletionPeople": "Visits/Encounters",
        "T_VisitEMRStatus": "Visits/Encounters",
        "T_EMRStatusDefs": "Visits/Encounters",
        "Trans": "Billing/Transactions",
        "Trans_Reps": "Billing/Transactions",
        "Statements": "Billing/Statements",
        "Statements_Reps": "Billing/Statements",
        "PaymentPlans": "Billing/Payments",
        "TaskHeader": "Tasks/Workflow",
        "TaskDetail": "Tasks/Workflow",
        "T_Status": "Tasks/Workflow",
        "T_Departments": "Organization",
        "T_Facility": "Organization",
        "T_Providers": "Organization",
        "T_Specialties": "Organization",
        "Panels": "Lab Panels",
        "PatientPanels": "Lab Panels",
        "T_LabRecOrder": "Laboratory",
        "T_LabRecItem": "Laboratory",
        "T_LabRecOrderItem": "Laboratory",
        "T_LabRecOrderItemCodes": "Laboratory",
        "T_PatientMedication": "Medications",
        "T_PatientMedicationDxCodes": "Medications",
        "T_PatientMedicationSigChange": "Medications",
        "T_PatientERxDetails": "Medications/E-Prescribing",
        "T_PatientErxCancelDetails": "Medications/E-Prescribing",
        "T_PatientErxChange": "Medications/E-Prescribing",
        "T_PatientPrintRxDetails": "Medications/E-Prescribing",
        "T_PatientRxHistory": "Medications/E-Prescribing",
        "T_PatientPharmacy": "Medications/E-Prescribing",
        "T_tblPharmacy": "Medications/E-Prescribing",
        "T_PatientAllergy": "Patient Allergies",
        "T_PatientAllergyReactions": "Patient Allergies",
        "T_PatientAlertAllergies": "Patient Allergies",
        "T_PCIS_Allergy": "Patient Allergies",
        "T_AllergyType": "Patient Allergies",
        "T_PatientAlerts": "Patient Alerts",
        "T_PatientAlertCategory": "Patient Alerts",
        "T_PatientAlertTypes": "Patient Alerts",
        "T_PatientAlertsEditUsers": "Patient Alerts",
        "T_PatientAlertsPrivate": "Patient Alerts",
        "T_PatientImmunizations": "Immunizations",
        "T_PatientImmunizationEvaluatedForecast": "Immunizations",
        "T_PatientImmunizationEvaluatedHistory": "Immunizations",
        "T_PatientImmunizationEvaluatedReport": "Immunizations",
        "T_PatientImmunizationRegistryInfo": "Immunizations",
        "T_PatientImmunizationVIS": "Immunizations",
        "T_Immunizations": "Immunizations",
        "T_ImmunManufacturer": "Immunizations",
        "T_VFCEligibilityQuestions": "Immunizations",
        "T_VFCPatientEligibility": "Immunizations",
        "T_PatientImplantableDevice": "Implantable Devices",
        "T_PatientCancerEvent": "Cancer/Oncology",
        "T_PatientCancerEventPlannedMeds": "Cancer/Oncology",
        "T_FamilyHistRelConditions": "Family History",
        "T_FamilyHistRelativeConditions": "Family History",
        "T_FamilyHistoryCondition": "Family History",
        "T_FamilyHistoryMisc": "Family History",
        "T_FamilyHistoryPerson": "Family History",
        "T_FamilyHistoryRelationships": "Family History",
        "T_PatientFamilyHistRelative": "Family History",
        "T_PatientFamilyHistory": "Family History",
        "T_PatientFamilyHistoryRelatives": "Family History",
        "T_OBData": "OB/GYN",
        "T_VisitNote": "Clinical Notes",
        "T_VisitNoteAddendum": "Clinical Notes",
        "T_VisitNoteAmendment": "Clinical Notes",
        "T_VisitNotesSection": "Clinical Notes",
        "T_VisitSection": "Clinical Notes",
        "T_VisitDataSectionText": "Clinical Notes",
        "T_VisitHPIData": "Clinical Notes",
        "T_VisitPEData": "Clinical Notes",
        "T_VisitTreeData": "Clinical Notes",
        "T_VisitInkData": "Clinical Notes",
        "T_VisitSketchImage": "Clinical Notes",
        "T_ScribbleAddenda": "Clinical Notes",
        "T_ScribblePageData": "Clinical Notes",
        "T_HPIPhrase": "Clinical Notes",
        "T_VisitMiscFields": "Clinical Notes",
        "T_VisitIncludePatientNote": "Clinical Notes",
        "PatientNotes": "Patient Notes",
        "PatientNotes_Reps": "Patient Notes",
        "T_Annotation": "Patient Notes",
        "T_PatientLetter": "Patient Communications",
        "T_PatientPortalInfo": "Patient Portal",
        "T_PatientPortalMessages": "Patient Portal",
        "T_Faxes": "Fax/Communications",
        "T_FaxStatus": "Fax/Communications",
        "T_VisitDiags": "Visit Diagnoses/Procedures",
        "T_VisitProcDiag": "Visit Diagnoses/Procedures",
        "T_VisitProcMod": "Visit Diagnoses/Procedures",
        "T_VisitOrderExtraData": "Visit Diagnoses/Procedures",
        "T_VisitCheckOutMessages": "Visit Checkout",
        "T_VisitCheckOutSentProcTasks": "Visit Checkout",
        "T_VisitCheckOutTasks": "Visit Checkout",
        "T_VisitRHO_CompletedNote": "Visit Checkout",
        "T_VisitRadOutboundInfo": "Imaging/Radiology",
        "T_OrderTracking": "Order Tracking",
        "T_OrderTrackingComment": "Order Tracking",
        "T_OrderTrackingLinks": "Order Tracking",
        "T_OrderTrackingStatus": "Order Tracking",
        "T_OrderTrackingStatusDefs": "Order Tracking",
        "T_PatientReferrals": "Referrals",
        "T_PatientReferralComments": "Referrals",
        "T_PatientReferralLinks": "Referrals",
        "T_PatientReferralStatus": "Referrals",
        "T_PatientReferralStatusDefs": "Referrals",
        "T_ReferralTypes": "Referrals",
        "Referrals": "Referrals",
        "Referrals_Reps": "Referrals",
        "T_RenewalRequests": "Medication Renewals",
        "T_RenewalRequestComments": "Medication Renewals",
        "T_PatientCCDA": "Care Coordination",
        "T_PatientTransitionsOfCare": "Care Coordination",
        "TOC_Attachments": "Care Coordination",
        "TOC_Entries": "Care Coordination",
        "TOC_EntryComments": "Care Coordination",
        "T_BlobData": "Documents/Files",
        "T_BlobData_Category": "Documents/Files",
        "T_VisitAttachments": "Documents/Files",
        "T_PatientEducationDocuments": "Documents/Files",
        "T_ExternalLinks": "Documents/Files",
        "T_ClinicalLinks": "Clinical Links",
        "T_AmendmentMessages": "Amendments",
        "T_ChangeRequestComments": "Amendments",
        "T_PatientRecordRequests": "Record Requests",
        "RecordRequest_Methods": "Record Requests",
        "PatientFormResponse": "Custom Forms",
        "PatientFormResponseQuestions": "Custom Forms",
        "ScreeningDef": "Screening/Assessments",
        "ScreeningQuestionChoice": "Screening/Assessments",
        "ScreeningQuestionDef": "Screening/Assessments",
        "T_EyeItem": "Eye/Ophthalmology",
        "T_EyeItemData": "Eye/Ophthalmology",
        "T_EyeRefraction": "Eye/Ophthalmology",
        "T_PatientContactLens": "Eye/Ophthalmology",
        "T_PatientEyeDilation": "Eye/Ophthalmology",
        "T_PatientEyeIOP": "Eye/Ophthalmology",
        "T_PatientEyeRefraction": "Eye/Ophthalmology",
        "T_PatientEyeVisualAcuity": "Eye/Ophthalmology",
        "T_PatientEyesRx": "Eye/Ophthalmology",
        "T_PatientIOP": "Eye/Ophthalmology",
        "T_PatientIOPLinks": "Eye/Ophthalmology",
        "T_PatientKeratometry": "Eye/Ophthalmology",
        "T_PatientRefraction": "Eye/Ophthalmology",
        "T_PatientVisualAcuity": "Eye/Ophthalmology",
        "T_OcularHistory": "Eye/Ophthalmology",
        "T_VisitContactLens": "Eye/Ophthalmology",
        "T_VisitDilation": "Eye/Ophthalmology",
        "T_VisitEyeCurrentRx": "Eye/Ophthalmology",
        "T_VisitIOP": "Eye/Ophthalmology",
        "T_VisitKeratometry": "Eye/Ophthalmology",
        "T_VisitOcularHistory": "Eye/Ophthalmology",
        "T_VisitRefraction": "Eye/Ophthalmology",
        "T_VisitVisualAcuity": "Eye/Ophthalmology",
        "T_VisitImplantableDeviceIncludeInNote": "Implantable Devices",
        "T_VisitVitalMod": "Vitals",
        "T_Vital": "Vitals",
        "T_VitalAlternateName": "Vitals",
        "T_VitalBCodes": "Vitals",
        "T_VitalCondition": "Vitals",
        "T_VitalConditionGroup": "Vitals",
        "T_VitalConditionGroupBCodes": "Vitals",
        "T_VitalConstants": "Vitals",
        "T_VitalIsVisible": "Vitals",
        "T_VitalModifier": "Vitals",
        "T_VitalTemplateBCodes": "Vitals",
        "T_VitalTemplateCondition": "Vitals",
        "T_VitalTemplateConditionGroup": "Vitals",
        "T_VitalTemplateConditionGroupBCodes": "Vitals",
        "T_VitalTemplateVisibleUnits": "Vitals",
        "T_VitalUnitTypes": "Vitals",
        "T_UnitType": "Vitals",
        "T_UnitofMeasure": "Vitals",
        "T_RecallCodes": "Recalls",
        "T_RecallLocations": "Recalls",
        "T_RecallNote": "Recalls",
        "T_RecallPatient": "Recalls",
        "T_Flowsheets": "Flowsheets",
        "T_FlowsheetColumns": "Flowsheets",
        "T_FlowsheetComments": "Flowsheets",
        "T_FlowsheetHistory": "Flowsheets",
        "T_HRIApprovedItems": "Health Record Items",
        "T_HRIComments": "Health Record Items",
        "T_HRICustomFieldDefinitions": "Health Record Items",
        "T_HRICustomFields": "Health Record Items",
        "T_HRIGroupItems": "Health Record Items",
        "T_HRIGroups": "Health Record Items",
        "T_HRINonClinicalItems": "Health Record Items",
    }
    if name in exact:
        return exact[name]
    
    # Prefix-based
    prefixes = {
        "Allergy_": "Allergy/Immunotherapy",
        "Lab_": "Laboratory",
        "eTask_": "E-Tasking/Messaging",
        "Demo_": "Demographics",
        "ColBased_": "Custom Forms/Columns",
        "EOB": "Billing/EOB",
        "Estimate": "Billing/Estimates",
        "EHI_": "EHI Export Metadata",
        "Acct": "Accounts",
        "Account": "Accounts",
        "PAR_": "Prior Authorization",
        "POS_": "Point of Service",
        "Portal_": "Patient Portal",
        "InfoRelease": "Information Release",
        "MidmarkReport": "Midmark Integration",
        "Dunning": "Billing/Collections",
        "Allocated": "Billing/Payments",
        "Claim": "Claims/Billing",
        "Problem_": "Problems",
    }
    for prefix, category in prefixes.items():
        if name.startswith(prefix):
            return category
    
    # Keyword fallback
    if "order" in nl:
        return "Orders"
    if "diagnos" in nl or "diag" in nl:
        return "Diagnoses"
    if "procedure" in nl or "proc" in nl:
        return "Procedures"
    if "recall" in nl:
        return "Recalls"
    if "insur" in nl:
        return "Insurance"
    
    return "Other"

for t in tables:
    t["category"] = categorize(t["table_name"])

# Category summary
from collections import Counter, defaultdict
cat_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "table_names": []})
for t in tables:
    cat = t["category"]
    cat_stats[cat]["tables"] += 1
    cat_stats[cat]["fields"] += t["field_count"]
    cat_stats[cat]["table_names"].append(t["table_name"])

summary = {
    "total_tables": len(tables),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_type,
    "pct_with_descriptions": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "pct_with_types": round(fields_with_type / total_fields * 100, 1) if total_fields else 0,
    "categories": {k: v for k, v in sorted(cat_stats.items(), key=lambda x: -x[1]["fields"])},
    "tables_by_field_count_top20": sorted(
        [{"table": t["table_name"], "fields": t["field_count"], "category": t["category"]} for t in tables],
        key=lambda x: -x["fields"]
    )[:20]
}

# Write outputs
out_dir = Path(__file__).parent
with open(out_dir / "entity-inventory-full.json", "w") as f:
    json.dump(tables, f, indent=2)

with open(out_dir / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Tables: {len(tables)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['pct_with_descriptions']}%)")
print(f"Fields with types: {fields_with_type} ({summary['pct_with_types']}%)")
print(f"\nCategories ({len(cat_stats)}):")
for cat, stats in sorted(cat_stats.items(), key=lambda x: -x[1]["fields"]):
    print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields")
print(f"\nTop 20 tables by field count:")
for item in summary["tables_by_field_count_top20"]:
    print(f"  {item['table']}: {item['fields']} fields ({item['category']})")
