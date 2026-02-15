#!/usr/bin/env python3
"""
Parse the CSV data dictionaries from the Medgen Backup Utility PDF (pp. 72-77).
Extracted from pdftotext output of MedgenBackupUtility.pdf.

Counts fields, checks whether descriptions are meaningful (vs just repeating the column name).
"""

import json

# Data dictionaries extracted from PDF text (pp. 72-77)
csv_files = {
    "patients.csv": {
        "title": "Patient Demographics & Insurance",
        "fields": [
            {"pos": 1, "name": "Id_code", "desc": "Medgen Patient Identifier"},
            {"pos": 2, "name": "last_name", "desc": "Patient Last Name"},
            {"pos": 3, "name": "First_name", "desc": "Patient First Name"},
            {"pos": 4, "name": "Middle_int", "desc": "Patient Middle Initial"},
            {"pos": 5, "name": "Addres1", "desc": "Patient Street Address"},
            {"pos": 6, "name": "Addres2", "desc": "Patient Suite or Apt Number"},
            {"pos": 7, "name": "City", "desc": "Patient City"},
            {"pos": 8, "name": "State", "desc": "Patient State"},
            {"pos": 9, "name": "Zip", "desc": "Patient Zip"},
            {"pos": 10, "name": "DOB", "desc": "Patient DOB (MM/DD/YYYY)"},
            {"pos": 11, "name": "Sex", "desc": "Patient Birth Gender"},
            {"pos": 12, "name": "SSN", "desc": "Patient Social Security Number"},
            {"pos": 13, "name": "Phone", "desc": "Patient Home Phone Number"},
            {"pos": 14, "name": "Work_phone", "desc": "Patient Work Phone Number"},
            {"pos": 15, "name": "Cellno", "desc": "Patient Cell Phone Number"},
            {"pos": 16, "name": "email", "desc": "Patient Email"},
            {"pos": 17, "name": "INS1", "desc": "Patient Primary Medgen Insurance Code"},
            {"pos": 18, "name": "NAME1", "desc": "Patient Primary Insurance Name"},
            {"pos": 19, "name": "INSPOLICY1", "desc": "Patient Primary Insurance Policy Number"},
            {"pos": 20, "name": "INS2", "desc": "Patient Secondary Medgen Insurance Code"},
            {"pos": 21, "name": "NAME2", "desc": "Patient Secondary Insurance Name"},
            {"pos": 22, "name": "INSPOLICY2", "desc": "Patient Secondary Insurance Policy Number"},
        ]
    },
    "appointments.csv": {
        "title": "Patient Appointments",
        "fields": [
            {"pos": 1, "name": "Apptno", "desc": "Medgen Appointment Identifier"},
            {"pos": 2, "name": "Appt_date", "desc": "Appointment Date (MM/DD/YYYY)"},
            {"pos": 3, "name": "Start_time", "desc": "Appointment Start Time (HHMM)"},
            {"pos": 4, "name": "Duration", "desc": "Appointment Duration"},
            {"pos": 5, "name": "Id_code", "desc": "Medgen Patient Identifier"},
            {"pos": 6, "name": "Last_name", "desc": "Patient Last Name"},
            {"pos": 7, "name": "First_name", "desc": "Patient First Name"},
            {"pos": 8, "name": "Dob", "desc": "Patient DOB (MM/DD/YYYY)"},
            {"pos": 9, "name": "Apptreason", "desc": "Appointment Reason Description"},
            {"pos": 10, "name": "Notes", "desc": "Appointment Notes"},
            {"pos": 11, "name": "Provider", "desc": "Appointment Provider Medgen Identifier"},
            {"pos": 12, "name": "Officeid", "desc": "Appointment Office Medgen Identifier"},
        ]
    },
    "pharmacy.csv": {
        "title": "Patient Pharmacies",
        "fields": [
            {"pos": 1, "name": "Id_code", "desc": "Medgen Patient Identifier"},
            {"pos": 2, "name": "NCPDPID", "desc": "Pharmacy NCPDPID"},
            {"pos": 3, "name": "Name", "desc": "Pharmacy Name"},
            {"pos": 4, "name": "Address", "desc": "Pharmacy Address"},
            {"pos": 5, "name": "City", "desc": "Pharmacy City"},
            {"pos": 6, "name": "State", "desc": "Pharmacy State"},
            {"pos": 7, "name": "Zip", "desc": "Pharmacy Zip"},
        ]
    },
    "comments.csv": {
        "title": "Patient Comments",
        "fields": [
            {"pos": 1, "name": "Id_code", "desc": "Medgen Patient Identifier"},
            {"pos": 2, "name": "Comment_no", "desc": "Medgen Comment Identifier"},
            {"pos": 3, "name": "Comdate", "desc": "Comment Date (MM/DD/YYYY)"},
            {"pos": 4, "name": "Alert", "desc": "Comment Alert Flag (0/1)"},
            {"pos": 5, "name": "Color", "desc": "Comment Color"},
            {"pos": 6, "name": "Comment", "desc": "Comment"},
        ]
    },
    "Transactions.csv": {
        "title": "Patient Charges & Transactions",
        "fields": [
            {"pos": 1, "name": "Claim No", "desc": "Claim No"},
            {"pos": 2, "name": "Accession", "desc": "Accession"},
            {"pos": 3, "name": "Patient ID", "desc": "Patient ID"},
            {"pos": 4, "name": "Patient Name", "desc": "Patient Name"},
            {"pos": 5, "name": "DOB", "desc": "DOB"},
            {"pos": 6, "name": "STATE", "desc": "STATE"},
            {"pos": 7, "name": "DOS", "desc": "DOS"},
            {"pos": 8, "name": "InitialIns", "desc": "InitialIns"},
            {"pos": 9, "name": "Current Bill Type", "desc": "Current Bill Type"},
            {"pos": 10, "name": "Procdure Code", "desc": "Procdure Code"},
            {"pos": 11, "name": "Modifier 1", "desc": "Modifier 1"},
            {"pos": 12, "name": "Modifier 2", "desc": "Modifier 2"},
            {"pos": 13, "name": "Modifier 3", "desc": "Modifier 3"},
            {"pos": 14, "name": "Modifier 4", "desc": "Modifier 4"},
            {"pos": 15, "name": "Proc Charge", "desc": "Proc Charge"},
            {"pos": 16, "name": "Paid", "desc": "Paid"},
            {"pos": 17, "name": "Deductible", "desc": "Deductible"},
            {"pos": 18, "name": "Coinsurance", "desc": "Coinsurance"},
            {"pos": 19, "name": "Copay", "desc": "Copay"},
            {"pos": 20, "name": "Adjustment", "desc": "Adjustment"},
            {"pos": 21, "name": "Balance", "desc": "Balance"},
            {"pos": 22, "name": "Primary Balance", "desc": "Primary Balance"},
            {"pos": 23, "name": "Other Balance", "desc": "Other Balance"},
            {"pos": 24, "name": "Patient Balance", "desc": "Patient Balance"},
            {"pos": 25, "name": "DIAG1", "desc": "DIAG1"},
            {"pos": 26, "name": "DIAG2", "desc": "DIAG2"},
            {"pos": 27, "name": "DIAG3", "desc": "DIAG3"},
            {"pos": 28, "name": "DIAG4", "desc": "DIAG4"},
            {"pos": 29, "name": "DIAG5", "desc": "DIAG5"},
            {"pos": 30, "name": "DIAG6", "desc": "DIAG6"},
            {"pos": 31, "name": "DIAG7", "desc": "DIAG7"},
            {"pos": 32, "name": "DIAG8", "desc": "DIAG8"},
            {"pos": 33, "name": "DIAG9", "desc": "DIAG9"},
            {"pos": 34, "name": "DIAG10", "desc": "DIAG10"},
            {"pos": 35, "name": "DIAG11", "desc": "DIAG11"},
            {"pos": 36, "name": "DIAG12", "desc": "DIAG12"},
            {"pos": 37, "name": "ActionNote", "desc": "ActionNote"},
            {"pos": 38, "name": "ActionNoteDate", "desc": "ActionNoteDate"},
            {"pos": 39, "name": "ActionNoteType", "desc": "ActionNoteType"},
            {"pos": 40, "name": "FollowupDate", "desc": "FollowupDate"},
            {"pos": 41, "name": "Claim Status", "desc": "Claim Status"},
            {"pos": 42, "name": "Claim Action", "desc": "Claim Action"},
            {"pos": 43, "name": "Claim Sub Status", "desc": "Claim Sub Status"},
            {"pos": 44, "name": "DateEntered", "desc": "DateEntered"},
            {"pos": 45, "name": "FirstBillDate", "desc": "FirstBillDate"},
            {"pos": 46, "name": "LastBillDate", "desc": "LastBillDate"},
            {"pos": 47, "name": "ClaimPostedDate", "desc": "ClaimPostedDate"},
            {"pos": 48, "name": "Office", "desc": "Office"},
            {"pos": 49, "name": "PayInsurance", "desc": "PayInsurance"},
            {"pos": 50, "name": "Amount", "desc": "Amount"},
            {"pos": 51, "name": "CHECKCREDITNUMBER", "desc": "CHECKCREDITNUMBER"},
            {"pos": 52, "name": "CheckDate", "desc": "CheckDate"},
            {"pos": 53, "name": "PaymentPostedDate", "desc": "PaymentPostedDate"},
            {"pos": 54, "name": "ThirdParty", "desc": "ThirdParty"},
            {"pos": 55, "name": "ThirdPartyName", "desc": "ThirdPartyName"},
            {"pos": 56, "name": "RefProvid", "desc": "RefProvid"},
            {"pos": 57, "name": "RefProvName", "desc": "RefProvName"},
            {"pos": 58, "name": "Hold", "desc": "Hold"},
            {"pos": 59, "name": "LastUpdated", "desc": "LastUpdated"},
            {"pos": 60, "name": "PriInsCode", "desc": "PriInsCode"},
            {"pos": 61, "name": "PriInsName", "desc": "PriInsName"},
            {"pos": 62, "name": "PriInsClass", "desc": "PriInsClass"},
            {"pos": 63, "name": "PriInsPolicy1", "desc": "PriInsPolicy1"},
            {"pos": 64, "name": "PriInsGroupName", "desc": "PriInsGroupName"},
            {"pos": 65, "name": "PriInsNotes", "desc": "PriInsNotes"},
            {"pos": 66, "name": "PriEffDate", "desc": "PriEffDate"},
            {"pos": 67, "name": "PriTermDate", "desc": "PriTermDate"},
            {"pos": 68, "name": "SecInsCode", "desc": "SecInsCode"},
            {"pos": 69, "name": "SecInsName", "desc": "SecInsName"},
            {"pos": 70, "name": "SecInsClass", "desc": "SecInsClass"},
            {"pos": 71, "name": "SecInsPolicy1", "desc": "SecInsPolicy1"},
            {"pos": 72, "name": "SecInsGroupName", "desc": "SecInsGroupName"},
            {"pos": 73, "name": "SecInsNotes", "desc": "SecInsNotes"},
            {"pos": 74, "name": "SecEffDate", "desc": "SecEffDate"},
            {"pos": 75, "name": "SecTermDate", "desc": "SecTermDate"},
            {"pos": 76, "name": "DeptCode", "desc": "DeptCode"},
            {"pos": 77, "name": "POS", "desc": "POS"},
            {"pos": 78, "name": "PROVIDER", "desc": "PROVIDER"},
            {"pos": 79, "name": "Sex", "desc": "Sex"},
            {"pos": 80, "name": "Days Since Status Change", "desc": "Days Since Status Change"},
            {"pos": 81, "name": "Payer Ref Number", "desc": "Payer Ref Number"},
            {"pos": 82, "name": "Test Code", "desc": "Test Code"},
            {"pos": 83, "name": "ProcName", "desc": "ProcName"},
            {"pos": 84, "name": "Procedure Notes", "desc": "Procedure Notes"},
            {"pos": 85, "name": "Adj Reason", "desc": "Adj Reason"},
            {"pos": 86, "name": "Tran Comment", "desc": "Tran Comment"},
            {"pos": 87, "name": "Primary Payer Family", "desc": "Primary Payer Family"},
            {"pos": 88, "name": "Secondary Payer Family", "desc": "Secondary Payer Family"},
            {"pos": 89, "name": "Service Facility", "desc": "Service Facility"},
            {"pos": 90, "name": "Units", "desc": "Units"},
            {"pos": 91, "name": "PreAuthNo", "desc": "PreAuthNo"},
            {"pos": 92, "name": "Address1", "desc": "Address1"},
            {"pos": 93, "name": "Address2", "desc": "Address2"},
            {"pos": 94, "name": "City", "desc": "City"},
            {"pos": 95, "name": "Zip", "desc": "Zip"},
            {"pos": 96, "name": "Phone", "desc": "Phone"},
            {"pos": 97, "name": "Item No", "desc": "Item No"},
            {"pos": 98, "name": "PrimaryPlanId", "desc": "PrimaryPlanId"},
            {"pos": 99, "name": "SecondaryPlanId", "desc": "SecondaryPlanId"},
            {"pos": 100, "name": "TransactionID", "desc": "TransactionID"},
            {"pos": 101, "name": "PaidToPatient", "desc": "PaidToPatient"},
            {"pos": 102, "name": "OfficeName", "desc": "OfficeName"},
            {"pos": 103, "name": "ProviderLastName", "desc": "ProviderLastName"},
            {"pos": 104, "name": "ProviderFirstName", "desc": "ProviderFirstName"},
            {"pos": 105, "name": "PatientEmail", "desc": "PatientEmail"},
            {"pos": 106, "name": "PatientCellNo", "desc": "PatientCellNo"},
            {"pos": 107, "name": "PayInsuranceName", "desc": "PayInsuranceName"},
            {"pos": 108, "name": "SALES_GROUP_1", "desc": "SALES_GROUP_1"},
            {"pos": 109, "name": "SALES_GROUP_2", "desc": "SALES_GROUP_2"},
            {"pos": 110, "name": "SALES_GROUP_3", "desc": "SALES_GROUP_3"},
            {"pos": 111, "name": "SALES_GROUP_4", "desc": "SALES_GROUP_4"},
            {"pos": 112, "name": "ClientNote", "desc": "ClientNote"},
            {"pos": 113, "name": "ClientNoteDate", "desc": "ClientNoteDate"},
            {"pos": 114, "name": "ClientNoteType", "desc": "ClientNoteType"},
        ]
    }
}

# C-CDA sections from the PDF
ccda_sections = [
    {"name": "Allergy Intolerance", "uscdi_class": "Allergies & Intolerance", "data_elements": ["Drug allergies", "Reactions"], "pages": "20-24"},
    {"name": "CarePlan", "uscdi_class": "CarePlan", "data_elements": ["Health concerns", "Interventions", "Goals", "Outcomes"], "pages": "25-26"},
    {"name": "CareTeam", "uscdi_class": "Care Team", "data_elements": ["Member Name", "Member Identifier", "Member Role", "Location", "Telecom"], "pages": "27-30"},
    {"name": "Problems", "uscdi_class": "Problems", "data_elements": ["Problems", "Health Concerns", "Date of diagnosis", "Date of resolution"], "pages": "31-33"},
    {"name": "Medication", "uscdi_class": "Medication", "data_elements": ["Medication", "Dose", "Indication", "Fill status"], "pages": "34-36"},
    {"name": "Immunization", "uscdi_class": "Immunization", "data_elements": ["Vaccination status", "Code"], "pages": "37-38"},
    {"name": "Functional Status", "uscdi_class": "Functional Status", "data_elements": ["Health Concerns", "Functional Status", "Smoking status"], "pages": "39-41"},
    {"name": "Cognitive Status", "uscdi_class": "Cognitive Status", "data_elements": ["Physical", "Cognitive", "Intellectual", "Psychiatric disabilities"], "pages": "42-44"},
    {"name": "Result Section Data", "uscdi_class": "Results", "data_elements": ["Tests", "Values/Results"], "pages": "45-48"},
    {"name": "Vital Signs", "uscdi_class": "Vital Signs", "data_elements": ["Systolic BP", "Diastolic BP", "Heart Rate", "Respiratory Rate", "Temperature", "Height", "Weight", "Pulse Oximetry", "O2 Concentration"], "pages": "49-53"},
    {"name": "Social History", "uscdi_class": "Social History", "data_elements": ["Name", "DOB", "Birth sex", "Address", "Telecom", "Smoking status"], "pages": "54-57"},
    {"name": "Implant or Device", "uscdi_class": "Implant/Device", "data_elements": ["Device (UDI)"], "pages": "58-59"},
    {"name": "History of Encounter", "uscdi_class": "Encounters", "data_elements": ["Encounter Type", "Encounter Diagnosis", "Encounter Time", "Location"], "pages": "60-63"},
    {"name": "Goals", "uscdi_class": "Goals", "data_elements": ["Patient Goals"], "pages": "64-65"},
    {"name": "Procedure", "uscdi_class": "Procedure", "data_elements": ["Procedures"], "pages": "66-67"},
    {"name": "Clinical Notes", "uscdi_class": "Clinical Notes", "data_elements": ["Consultation note", "Discharge summary", "Procedure note", "Progress note", "Test Reports"], "pages": "68-70"},
]


def is_meaningful_description(name, desc):
    """Check if the description adds information beyond the column name."""
    # Normalize for comparison
    name_norm = name.lower().replace("_", " ").replace("-", " ").strip()
    desc_norm = desc.lower().replace("_", " ").replace("-", " ").strip()
    return name_norm != desc_norm


# Analyze
print("=" * 70)
print("MEDGEN BACKUP UTILITY - CSV DATA DICTIONARY ANALYSIS")
print("=" * 70)

total_fields = 0
total_meaningful = 0

for filename, data in csv_files.items():
    n_fields = len(data["fields"])
    meaningful = sum(1 for f in data["fields"] if is_meaningful_description(f["name"], f["desc"]))
    total_fields += n_fields
    total_meaningful += meaningful
    
    print(f"\n{filename} ({data['title']})")
    print(f"  Fields: {n_fields}")
    print(f"  With meaningful descriptions: {meaningful}/{n_fields} ({100*meaningful/n_fields:.0f}%)")
    print(f"  Data types documented: No")
    print(f"  Value sets documented: No")
    
    # Show fields where description just repeats name
    repeats = [f for f in data["fields"] if not is_meaningful_description(f["name"], f["desc"])]
    if repeats:
        print(f"  Fields where description = column name: {len(repeats)}")

print(f"\n{'='*70}")
print(f"TOTALS ACROSS ALL CSV FILES")
print(f"  Total CSV files: {len(csv_files)}")
print(f"  Total fields: {total_fields}")
print(f"  With meaningful descriptions: {total_meaningful}/{total_fields} ({100*total_meaningful/total_fields:.0f}%)")
print(f"  With just name-repeating descriptions: {total_fields - total_meaningful}/{total_fields} ({100*(total_fields-total_meaningful)/total_fields:.0f}%)")

print(f"\n{'='*70}")
print(f"C-CDA SECTIONS DOCUMENTED")
print(f"  Total sections: {len(ccda_sections)}")
total_elements = sum(len(s["data_elements"]) for s in ccda_sections)
print(f"  Total data elements listed: {total_elements}")
for s in ccda_sections:
    print(f"  - {s['name']} ({s['uscdi_class']}): {len(s['data_elements'])} elements (pp. {s['pages']})")

print(f"\n{'='*70}")
print(f"COMBINED EXPORT SUMMARY")
print(f"  Export components: C-CDA XML + Patient Document ZIPs + 5 CSV files")
print(f"  C-CDA sections: {len(ccda_sections)}")
print(f"  CSV files: {len(csv_files)}")
print(f"  CSV total fields: {total_fields}")
print(f"  CSV fields with meaningful descriptions: {total_meaningful} ({100*total_meaningful/total_fields:.0f}%)")

# Save as JSON for reference
output = {
    "csv_files": {},
    "ccda_sections": ccda_sections,
    "summary": {
        "total_csv_files": len(csv_files),
        "total_csv_fields": total_fields,
        "csv_fields_with_meaningful_descriptions": total_meaningful,
        "csv_fields_with_repeated_names": total_fields - total_meaningful,
        "ccda_sections": len(ccda_sections),
        "ccda_data_elements": total_elements,
    }
}

for filename, data in csv_files.items():
    output["csv_files"][filename] = {
        "title": data["title"],
        "field_count": len(data["fields"]),
        "fields": data["fields"],
        "meaningful_descriptions": sum(1 for f in data["fields"] if is_meaningful_description(f["name"], f["desc"])),
    }

with open("full-entity-inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved full inventory to full-entity-inventory.json")
