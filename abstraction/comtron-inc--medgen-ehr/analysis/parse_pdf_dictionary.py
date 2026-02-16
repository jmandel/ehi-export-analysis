#!/usr/bin/env python3
"""Parse the Medgen Backup Utility PDF data dictionary into structured JSON.

Extracts:
1. C-CDA sections with their USCDI data classes and data elements
2. CSV file specifications with column-level data dictionaries
"""

import json
import re
import sys

# Read the extracted PDF text
with open("MedgenBackupUtility.txt", "r") as f:
    text = f.read()

entities = []

# ============================================================
# Parse C-CDA sections from the PDF
# ============================================================

ccda_sections = [
    {
        "name": "Allergy Intolerance",
        "uscdi_class": "Allergies & Intolerance",
        "data_elements": [
            {"name": "Timestamp", "description": "Time the concern was authored in the patient's chart"},
            {"name": "AllergyType", "description": "Code representing allergy type (e.g., drug allergy 416098002, food allergy 414285001)"},
            {"name": "AllergyCoded", "description": "Coded allergy substance using RxNorm for drugs, SNOMED CT for drug classes"},
            {"name": "AllergyStatus", "description": "Status of the allergy (active or inactive)"},
            {"name": "AllergyReaction", "description": "Reaction type (e.g., hives)"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.6",
        "loinc_code": "48765-2",
    },
    {
        "name": "CarePlan",
        "uscdi_class": "CarePlan",
        "data_elements": [
            {"name": "Code", "description": "Code specifying whether the item is a goal or a plan of care"},
            {"name": "GoalOrCarePlanText", "description": "Goal or care plan text"},
            {"name": "ProblemName", "description": "Problem name for problem-based instructions"},
            {"name": "HealthConcerns", "description": "Patient's general health status"},
            {"name": "Authenticator", "description": "Participant who attests to accuracy"},
            {"name": "CarePlanReview", "description": "Care Plan review date (past or future)"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.1.15",
    },
    {
        "name": "CareTeam",
        "uscdi_class": "Care Team",
        "data_elements": [
            {"name": "CareTeamMemberName", "description": "Care Team Member Name"},
            {"name": "MemberIdentifier", "description": "Member Identifier"},
            {"name": "MemberRole", "description": "Member Role"},
            {"name": "Location", "description": "Location"},
            {"name": "Telecom", "description": "Telecom"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.500",
        "loinc_code": "85847-2",
    },
    {
        "name": "Problems",
        "uscdi_class": "Problems",
        "data_elements": [
            {"name": "Problems", "description": "Active problems"},
            {"name": "ProblemHealthConcerns", "description": "Problem/Health Concerns"},
            {"name": "DateOfDiagnosis", "description": "Date of diagnosis"},
            {"name": "DateOfResolution", "description": "Date of resolution"},
            {"name": "ProblemStatus", "description": "Concern status (active/completed)"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.5.1",
    },
    {
        "name": "Medication",
        "uscdi_class": "Medication",
        "data_elements": [
            {"name": "Medication", "description": "Medication at prescription level (e.g., 500mg oral tablet)"},
            {"name": "Dose", "description": "Dose quantity"},
            {"name": "Indication", "description": "Indication for medication"},
            {"name": "FillStatus", "description": "Fill status (repeatNumber)"},
            {"name": "Status", "description": "Status code"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.1.1",
    },
    {
        "name": "Immunization",
        "uscdi_class": "Immunization",
        "data_elements": [
            {"name": "VaccinationStatus", "description": "Vaccination status code"},
            {"name": "VaccinationCode", "description": "Vaccine code"},
            {"name": "VaccineDate", "description": "Vaccine administration date"},
            {"name": "DoseQuantity", "description": "Vaccine quantity"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.2",
        "loinc_code": "11369-6",
    },
    {
        "name": "Functional Status",
        "uscdi_class": "Functional Status",
        "data_elements": [
            {"name": "HealthConcerns", "description": "Health Concerns"},
            {"name": "FunctionalStatus", "description": "Functional Status observation"},
            {"name": "SmokingStatus", "description": "Smoking status"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.14",
        "loinc_code": "47420-5",
    },
    {
        "name": "Cognitive Status",
        "uscdi_class": "Cognitive Status",
        "data_elements": [
            {"name": "Physical", "description": "Physical disabilities"},
            {"name": "Cognitive", "description": "Cognitive status"},
            {"name": "Intellectual", "description": "Intellectual disabilities"},
            {"name": "PsychiatricDisabilities", "description": "Psychiatric disabilities"},
            {"name": "Status", "description": "Status observation"},
            {"name": "CognitiveProblem", "description": "Cognitive problem observation"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.56",
        "loinc_code": "10190-7",
    },
    {
        "name": "Result Section Data",
        "uscdi_class": "Laboratory / Clinical Tests",
        "data_elements": [
            {"name": "Tests", "description": "Result Organizer with ordered test and date/time"},
            {"name": "ValuesResults", "description": "Test values, reference ranges, interpretations"},
            {"name": "LabLocation", "description": "Lab location"},
            {"name": "Status", "description": "Test status (e.g., negative)"},
            {"name": "Timestamps", "description": "Test timestamps"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.3.1",
        "loinc_code": "30954-2",
    },
    {
        "name": "Vital Signs",
        "uscdi_class": "Vital Signs",
        "data_elements": [
            {"name": "SystolicBloodPressure", "description": "Systolic Blood Pressure"},
            {"name": "DiastolicBloodPressure", "description": "Diastolic Blood Pressure"},
            {"name": "HeartRate", "description": "Heart Rate"},
            {"name": "RespiratoryRate", "description": "Respiratory Rate"},
            {"name": "BodyTemperature", "description": "Body Temperature"},
            {"name": "BodyHeight", "description": "Body Height"},
            {"name": "BodyWeight", "description": "Body Weight"},
            {"name": "PulseOximetry", "description": "Pulse Oximetry"},
            {"name": "InhaledOxygenConcentration", "description": "Inhaled Oxygen Concentration"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.4",
        "loinc_code": "8716-3",
    },
    {
        "name": "Social History",
        "uscdi_class": "Social History / Patient Demographics",
        "data_elements": [
            {"name": "FirstName", "description": "First Name"},
            {"name": "LastName", "description": "Last Name"},
            {"name": "FamilyName", "description": "Family Name"},
            {"name": "DateOfBirth", "description": "Date of birth"},
            {"name": "BirthSex", "description": "Birth sex"},
            {"name": "Address", "description": "Address"},
            {"name": "TelecomNumber", "description": "Telecom Number"},
            {"name": "SmokingStatus", "description": "Smoking Status"},
            {"name": "Gender", "description": "Gender"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.17",
        "loinc_code": "29762-2",
    },
    {
        "name": "Implant or Device",
        "uscdi_class": "Medical Devices",
        "data_elements": [
            {"name": "Device", "description": "Device (e.g., pacemaker, implant with UDI)"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.33",
        "loinc_code": "55122-6",
    },
    {
        "name": "History of Encounter",
        "uscdi_class": "Encounters",
        "data_elements": [
            {"name": "EncounterType", "description": "Encounter Type (CPT for ambulatory)"},
            {"name": "EncounterDiagnosis", "description": "Encounter Diagnosis"},
            {"name": "EncounterTime", "description": "Encounter Time (admission/discharge for hospitalization)"},
            {"name": "Location", "description": "Location"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.4.80",
        "loinc_code": "29308-4",
    },
    {
        "name": "Goals",
        "uscdi_class": "Goals",
        "data_elements": [
            {"name": "PatientGoals", "description": "Patient-defined goals (alleviation of health concerns, desired outcomes, function, symptom management, comfort)"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.60",
        "loinc_code": "61146-7",
    },
    {
        "name": "Procedure",
        "uscdi_class": "Procedures",
        "data_elements": [
            {"name": "Procedures", "description": "Procedure details including site preparation, sedation, measurements, times, medications, blood loss, specimens, implants"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.27",
        "loinc_code": "29554-3",
    },
    {
        "name": "Clinical Notes",
        "uscdi_class": "Clinical Notes",
        "data_elements": [
            {"name": "ConsultationNote", "description": "Consultation note"},
            {"name": "DischargeSummary", "description": "Discharge summary"},
            {"name": "ProcedureNote", "description": "Procedure note"},
            {"name": "ProgressNote", "description": "Progress note"},
            {"name": "TestReports", "description": "Test Reports"},
        ],
        "template_id": "2.16.840.1.113883.10.20.22.2.65",
    },
]

# Add C-CDA sections as entities
for section in ccda_sections:
    fields = []
    for elem in section["data_elements"]:
        fields.append({
            "name": elem["name"],
            "type": "XML element (C-CDA)",
            "description": elem["description"],
            "nullable": None,
        })
    entities.append({
        "name": f"C-CDA: {section['name']}",
        "category": "C-CDA Clinical Data",
        "source_format": "C-CDA XML",
        "field_count": len(fields),
        "fields": fields,
        "uscdi_class": section.get("uscdi_class", ""),
        "template_id": section.get("template_id", ""),
        "loinc_code": section.get("loinc_code", ""),
    })

# ============================================================
# Parse CSV file specifications
# ============================================================

csv_files = [
    {
        "name": "patients.csv",
        "display_name": "Patient Demographics & Insurance",
        "category": "CSV Supplementary Data",
        "fields": [
            {"position": 1, "name": "Id_code", "description": "Medgen Patient Identifier"},
            {"position": 2, "name": "last_name", "description": "Patient Last Name"},
            {"position": 3, "name": "First_name", "description": "Patient First Name"},
            {"position": 4, "name": "Middle_int", "description": "Patient Middle Initial"},
            {"position": 5, "name": "Addres1", "description": "Patient Street Address"},
            {"position": 6, "name": "Addres2", "description": "Patient Suite or Apt Number"},
            {"position": 7, "name": "City", "description": "Patient City"},
            {"position": 8, "name": "State", "description": "Patient State"},
            {"position": 9, "name": "Zip", "description": "Patient Zip"},
            {"position": 10, "name": "DOB", "description": "Patient DOB (MM/DD/YYYY)"},
            {"position": 11, "name": "Sex", "description": "Patient Birth Gender"},
            {"position": 12, "name": "SSN", "description": "Patient Social Security Number"},
            {"position": 13, "name": "Phone", "description": "Patient Home Phone Number"},
            {"position": 14, "name": "Work_phone", "description": "Patient Work Phone Number"},
            {"position": 15, "name": "Cellno", "description": "Patient Cell Phone Number"},
            {"position": 16, "name": "email", "description": "Patient Email"},
            {"position": 17, "name": "INS1", "description": "Patient Primary Medgen Insurance Code"},
            {"position": 18, "name": "NAME1", "description": "Patient Primary Insurance Name"},
            {"position": 19, "name": "INSPOLICY1", "description": "Patient Primary Insurance Policy Number"},
            {"position": 20, "name": "INS2", "description": "Patient Secondary Medgen Insurance Code"},
            {"position": 21, "name": "NAME2", "description": "Patient Secondary Insurance Name"},
            {"position": 22, "name": "INSPOLICY2", "description": "Patient Secondary Insurance Policy Number"},
        ],
    },
    {
        "name": "appointments.csv",
        "display_name": "Patient Appointments",
        "category": "CSV Supplementary Data",
        "fields": [
            {"position": 1, "name": "Apptno", "description": "Medgen Appointment Identifier"},
            {"position": 2, "name": "Appt_date", "description": "Appointment Date (MM/DD/YYYY)"},
            {"position": 3, "name": "Start_time", "description": "Appointment Start Time (HHMM)"},
            {"position": 4, "name": "Duration", "description": "Appointment Duration"},
            {"position": 5, "name": "Id_code", "description": "Medgen Patient Identifier"},
            {"position": 6, "name": "Last_name", "description": "Patient Last Name"},
            {"position": 7, "name": "First_name", "description": "Patient First Name"},
            {"position": 8, "name": "Dob", "description": "Patient DOB (MM/DD/YYYY)"},
            {"position": 9, "name": "Apptreason", "description": "Appointment Reason Description"},
            {"position": 10, "name": "Notes", "description": "Appointment Notes"},
            {"position": 11, "name": "Provider", "description": "Appointment Provider Medgen Identifier"},
            {"position": 12, "name": "Officeid", "description": "Appointment Office Medgen Identifier"},
        ],
    },
    {
        "name": "pharmacy.csv",
        "display_name": "Patient Pharmacies",
        "category": "CSV Supplementary Data",
        "fields": [
            {"position": 1, "name": "Id_code", "description": "Medgen Patient Identifier"},
            {"position": 2, "name": "NCPDPID", "description": "Pharmacy NCPDPID"},
            {"position": 3, "name": "Name", "description": "Pharmacy Name"},
            {"position": 4, "name": "Address", "description": "Pharmacy Address"},
            {"position": 5, "name": "City", "description": "Pharmacy City"},
            {"position": 6, "name": "State", "description": "Pharmacy State"},
            {"position": 7, "name": "Zip", "description": "Pharmacy Zip"},
        ],
    },
    {
        "name": "comments.csv",
        "display_name": "Patient Comments",
        "category": "CSV Supplementary Data",
        "fields": [
            {"position": 1, "name": "Id_code", "description": "Medgen Patient Identifier"},
            {"position": 2, "name": "Comment_no", "description": "Medgen Comment Identifier"},
            {"position": 3, "name": "Comdate", "description": "Comment Date (MM/DD/YYYY)"},
            {"position": 4, "name": "Alert", "description": "Comment Alert Flag (0/1)"},
            {"position": 5, "name": "Color", "description": "Comment Color"},
            {"position": 6, "name": "Comment", "description": "Comment"},
        ],
    },
    {
        "name": "Transactions.csv",
        "display_name": "Patient Charges & Transactions",
        "category": "CSV Supplementary Data - Billing",
        "fields": [
            {"position": 1, "name": "Claim No", "description": "Claim No"},
            {"position": 2, "name": "Accession", "description": "Accession"},
            {"position": 3, "name": "Patient ID", "description": "Patient ID"},
            {"position": 4, "name": "Patient Name", "description": "Patient Name"},
            {"position": 5, "name": "DOB", "description": "DOB"},
            {"position": 6, "name": "STATE", "description": "STATE"},
            {"position": 7, "name": "DOS", "description": "DOS"},
            {"position": 8, "name": "InitialIns", "description": "InitialIns"},
            {"position": 9, "name": "Current Bill Type", "description": "Current Bill Type"},
            {"position": 10, "name": "Procdure Code", "description": "Procdure Code"},
            {"position": 11, "name": "Modifier 1", "description": "Modifier 1"},
            {"position": 12, "name": "Modifier 2", "description": "Modifier 2"},
            {"position": 13, "name": "Modifier 3", "description": "Modifier 3"},
            {"position": 14, "name": "Modifier 4", "description": "Modifier 4"},
            {"position": 15, "name": "Proc Charge", "description": "Proc Charge"},
            {"position": 16, "name": "Paid", "description": "Paid"},
            {"position": 17, "name": "Deductible", "description": "Deductible"},
            {"position": 18, "name": "Coinsurance", "description": "Coinsurance"},
            {"position": 19, "name": "Copay", "description": "Copay"},
            {"position": 20, "name": "Adjustment", "description": "Adjustment"},
            {"position": 21, "name": "Balance", "description": "Balance"},
            {"position": 22, "name": "Primary Balance", "description": "Primary Balance"},
            {"position": 23, "name": "Other Balance", "description": "Other Balance"},
            {"position": 24, "name": "Patient Balance", "description": "Patient Balance"},
            {"position": 25, "name": "DIAG1", "description": "DIAG1"},
            {"position": 26, "name": "DIAG2", "description": "DIAG2"},
            {"position": 27, "name": "DIAG3", "description": "DIAG3"},
            {"position": 28, "name": "DIAG4", "description": "DIAG4"},
            {"position": 29, "name": "DIAG5", "description": "DIAG5"},
            {"position": 30, "name": "DIAG6", "description": "DIAG6"},
            {"position": 31, "name": "DIAG7", "description": "DIAG7"},
            {"position": 32, "name": "DIAG8", "description": "DIAG8"},
            {"position": 33, "name": "DIAG9", "description": "DIAG9"},
            {"position": 34, "name": "DIAG10", "description": "DIAG10"},
            {"position": 35, "name": "DIAG11", "description": "DIAG11"},
            {"position": 36, "name": "DIAG12", "description": "DIAG12"},
            {"position": 37, "name": "ActionNote", "description": "ActionNote"},
            {"position": 38, "name": "ActionNoteDate", "description": "ActionNoteDate"},
            {"position": 39, "name": "ActionNoteType", "description": "ActionNoteType"},
            {"position": 40, "name": "FollowupDate", "description": "FollowupDate"},
            {"position": 41, "name": "Claim Status", "description": "Claim Status"},
            {"position": 42, "name": "Claim Action", "description": "Claim Action"},
            {"position": 43, "name": "Claim Sub Status", "description": "Claim Sub Status"},
            {"position": 44, "name": "DateEntered", "description": "DateEntered"},
            {"position": 45, "name": "FirstBillDate", "description": "FirstBillDate"},
            {"position": 46, "name": "LastBillDate", "description": "LastBillDate"},
            {"position": 47, "name": "ClaimPostedDate", "description": "ClaimPostedDate"},
            {"position": 48, "name": "Office", "description": "Office"},
            {"position": 49, "name": "PayInsurance", "description": "PayInsurance"},
            {"position": 50, "name": "Amount", "description": "Amount"},
            {"position": 51, "name": "CHECKCREDITNUMBER", "description": "CHECKCREDITNUMBER"},
            {"position": 52, "name": "CheckDate", "description": "CheckDate"},
            {"position": 53, "name": "PaymentPostedDate", "description": "PaymentPostedDate"},
            {"position": 54, "name": "ThirdParty", "description": "ThirdParty"},
            {"position": 55, "name": "ThirdPartyName", "description": "ThirdPartyName"},
            {"position": 56, "name": "RefProvid", "description": "RefProvid"},
            {"position": 57, "name": "RefProvName", "description": "RefProvName"},
            {"position": 58, "name": "Hold", "description": "Hold"},
            {"position": 59, "name": "LastUpdated", "description": "LastUpdated"},
            {"position": 60, "name": "PriInsCode", "description": "PriInsCode"},
            {"position": 61, "name": "PriInsName", "description": "PriInsName"},
            {"position": 62, "name": "PriInsClass", "description": "PriInsClass"},
            {"position": 63, "name": "PriInsPolicy1", "description": "PriInsPolicy1"},
            {"position": 64, "name": "PriInsGroupName", "description": "PriInsGroupName"},
            {"position": 65, "name": "PriInsNotes", "description": "PriInsNotes"},
            {"position": 66, "name": "PriEffDate", "description": "PriEffDate"},
            {"position": 67, "name": "PriTermDate", "description": "PriTermDate"},
            {"position": 68, "name": "SecInsCode", "description": "SecInsCode"},
            {"position": 69, "name": "SecInsName", "description": "SecInsName"},
            {"position": 70, "name": "SecInsClass", "description": "SecInsClass"},
            {"position": 71, "name": "SecInsPolicy1", "description": "SecInsPolicy1"},
            {"position": 72, "name": "SecInsGroupName", "description": "SecInsGroupName"},
            {"position": 73, "name": "SecInsNotes", "description": "SecInsNotes"},
            {"position": 74, "name": "SecEffDate", "description": "SecEffDate"},
            {"position": 75, "name": "SecTermDate", "description": "SecTermDate"},
            {"position": 76, "name": "DeptCode", "description": "DeptCode"},
            {"position": 77, "name": "POS", "description": "POS"},
            {"position": 78, "name": "PROVIDER", "description": "PROVIDER"},
            {"position": 79, "name": "Sex", "description": "Sex"},
            {"position": 80, "name": "Days Since Status Change", "description": "Days Since Status Change"},
            {"position": 81, "name": "Payer Ref Number", "description": "Payer Ref Number"},
            {"position": 82, "name": "Test Code", "description": "Test Code"},
            {"position": 83, "name": "ProcName", "description": "ProcName"},
            {"position": 84, "name": "Procedure Notes", "description": "Procedure Notes"},
            {"position": 85, "name": "Adj Reason", "description": "Adj Reason"},
            {"position": 86, "name": "Tran Comment", "description": "Tran Comment"},
            {"position": 87, "name": "Primary Payer Family", "description": "Primary Payer Family"},
            {"position": 88, "name": "Secondary Payer Family", "description": "Secondary Payer Family"},
            {"position": 89, "name": "Service Facility", "description": "Service Facility"},
            {"position": 90, "name": "Units", "description": "Units"},
            {"position": 91, "name": "PreAuthNo", "description": "PreAuthNo"},
            {"position": 92, "name": "Address1", "description": "Address1"},
            {"position": 93, "name": "Address2", "description": "Address2"},
            {"position": 94, "name": "City", "description": "City"},
            {"position": 95, "name": "Zip", "description": "Zip"},
            {"position": 96, "name": "Phone", "description": "Phone"},
            {"position": 97, "name": "Item No", "description": "Item No"},
            {"position": 98, "name": "PrimaryPlanId", "description": "PrimaryPlanId"},
            {"position": 99, "name": "SecondaryPlanId", "description": "SecondaryPlanId"},
            {"position": 100, "name": "TransactionID", "description": "TransactionID"},
            {"position": 101, "name": "PaidToPatient", "description": "PaidToPatient"},
            {"position": 102, "name": "OfficeName", "description": "OfficeName"},
            {"position": 103, "name": "ProviderLastName", "description": "ProviderLastName"},
            {"position": 104, "name": "ProviderFirstName", "description": "ProviderFirstName"},
            {"position": 105, "name": "PatientEmail", "description": "PatientEmail"},
            {"position": 106, "name": "PatientCellNo", "description": "PatientCellNo"},
            {"position": 107, "name": "PayInsuranceName", "description": "PayInsuranceName"},
            {"position": 108, "name": "SALES_GROUP_1", "description": "SALES_GROUP_1"},
            {"position": 109, "name": "SALES_GROUP_2", "description": "SALES_GROUP_2"},
            {"position": 110, "name": "SALES_GROUP_3", "description": "SALES_GROUP_3"},
            {"position": 111, "name": "SALES_GROUP_4", "description": "SALES_GROUP_4"},
            {"position": 112, "name": "ClientNote", "description": "ClientNote"},
            {"position": 113, "name": "ClientNoteDate", "description": "ClientNoteDate"},
            {"position": 114, "name": "ClientNoteType", "description": "ClientNoteType"},
        ],
    },
]

for csv_file in csv_files:
    fields = []
    for f in csv_file["fields"]:
        desc = f["description"]
        # Check if description is just the field name repeated
        has_real_description = desc.lower().strip() != f["name"].lower().strip()
        fields.append({
            "name": f["name"],
            "position": f["position"],
            "type": "CSV column",
            "description": desc,
            "has_meaningful_description": has_real_description,
            "nullable": None,
        })
    entities.append({
        "name": csv_file["name"],
        "display_name": csv_file["display_name"],
        "category": csv_file["category"],
        "source_format": "CSV",
        "field_count": len(fields),
        "fields": fields,
    })

# Also add the Patient Documents entity
entities.append({
    "name": "Patient Documents (ZIP)",
    "display_name": "Patient Documents Download",
    "category": "Document Export",
    "source_format": "ZIP containing PDFs and other documents",
    "field_count": 0,
    "fields": [],
    "notes": "Documents exported as ZIP archives per patient. File naming pattern: docnumber_date_idcode_firstname_lastname_dob_providerid_description.filetype",
})

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

# ============================================================
# Generate summary statistics
# ============================================================

total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)

# Count fields with meaningful descriptions
ccda_fields = sum(e["field_count"] for e in entities if e["source_format"] == "C-CDA XML")
csv_fields = sum(e["field_count"] for e in entities if e["source_format"] == "CSV")

# For CSV files, count fields where description != field name
csv_fields_with_desc = 0
csv_fields_name_only = 0
for e in entities:
    if e["source_format"] == "CSV":
        for field in e["fields"]:
            if field.get("has_meaningful_description", True):
                csv_fields_with_desc += 1
            else:
                csv_fields_name_only += 1

# All C-CDA fields have descriptions
ccda_fields_with_desc = ccda_fields

total_fields_with_desc = ccda_fields_with_desc + csv_fields_with_desc

# Category breakdown
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entity_count": 0, "field_count": 0}
    categories[cat]["entity_count"] += 1
    categories[cat]["field_count"] += e["field_count"]

summary = {
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_meaningful_descriptions": total_fields_with_desc,
    "fields_description_is_just_name": csv_fields_name_only,
    "description_percentage": round(total_fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
    "ccda_sections": len([e for e in entities if e["source_format"] == "C-CDA XML"]),
    "ccda_fields": ccda_fields,
    "csv_files": len([e for e in entities if e["source_format"] == "CSV"]),
    "csv_fields": csv_fields,
    "document_export": 1,
    "categories": categories,
    "csv_file_details": [
        {"file": csv["name"], "display_name": csv["display_name"], "field_count": len(csv["fields"])}
        for csv in csv_files
    ],
    "transactions_csv_description_quality": {
        "total_fields": 114,
        "fields_with_meaningful_description": csv_fields_with_desc - sum(
            1 for e in entities if e["source_format"] == "CSV" and e["name"] != "Transactions.csv"
            for f in e["fields"] if f.get("has_meaningful_description", True)
        ),
        "fields_where_description_equals_name": csv_fields_name_only,
        "note": "Most Transactions.csv field descriptions simply repeat the field name with no additional context"
    },
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with meaningful descriptions: {total_fields_with_desc} ({summary['description_percentage']}%)")
print(f"C-CDA sections: {summary['ccda_sections']} ({ccda_fields} data elements)")
print(f"CSV files: {summary['csv_files']} ({csv_fields} fields)")
print(f"\nCategory breakdown:")
for cat, info in categories.items():
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
print(f"\nCSV file details:")
for csv in csv_files:
    print(f"  {csv['name']}: {len(csv['fields'])} fields")
print(f"\nTransactions.csv: {csv_fields_name_only} of 114 fields have description = field name")
