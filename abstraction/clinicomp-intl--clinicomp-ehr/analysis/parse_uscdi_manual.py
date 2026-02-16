#!/usr/bin/env python3
"""Parse CliniComp USCDI PDF data dictionary into structured JSON.
Uses pdftotext -layout output and manually handles the known 20 USCDI objects."""

import json
import re
import subprocess

PDF_PATH = "../downloads/250-70079_CliniComp_EHR_ONC-API_USCDI.pdf"

def extract_text():
    result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
    return result.stdout

# Manually define all fields from the PDF based on careful reading.
# This is more reliable than trying to parse the fixed-width PDF tables.
ENTITIES = [
    {
        "entity_name": "Patient Name",
        "ccds_object": "CCDS.Patient_Name",
        "section": "5.6.1",
        "category": "Demographics",
        "fields": [
            {"name": "Patient Name", "type": "String", "nullable": True, "description": "Patient name", "ehr_major_it": "0517 PatientName.adm"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Sex",
        "ccds_object": "CCDS.Sex",
        "section": "5.6.2",
        "category": "Demographics",
        "fields": [
            {"name": "Sex", "type": "String", "nullable": True, "description": "Gender", "ehr_major_it": "0529 Sex.adm"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Date of Birth",
        "ccds_object": "CCDS.Date_of_Birth",
        "section": "5.6.3",
        "category": "Demographics",
        "fields": [
            {"name": "Date of Birth", "type": "String", "nullable": True, "description": "Date of birth", "ehr_major_it": "0519 BirthDate.adm"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Race",
        "ccds_object": "CCDS.Race",
        "section": "5.6.4",
        "category": "Demographics",
        "fields": [
            {"name": "Race", "type": "String", "nullable": True, "description": "Race", "ehr_major_it": "0962 Race.adm or 19966 Race.adm.lg"},
            {"name": "Secondary Race", "type": "String", "nullable": True, "description": "Secondary Race", "ehr_major_it": "19685 SecondaryRace.adm"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Ethnicity",
        "ccds_object": "CCDS.Ethnicity",
        "section": "5.6.5",
        "category": "Demographics",
        "fields": [
            {"name": "Ethnic Background", "type": "String", "nullable": True, "description": "Ethnic Background", "ehr_major_it": "15288 Ethnic Background"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Preferred Language",
        "ccds_object": "CCDS.Preferred_Language",
        "section": "5.6.6",
        "category": "Demographics",
        "fields": [
            {"name": "Preferred Language", "type": "String", "nullable": True, "description": "Primary Language", "ehr_major_it": "1531 Language.adm or 19967 Language.adm.lg"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Smoking Status",
        "ccds_object": "CCDS.Smoking_Status",
        "section": "5.6.7",
        "category": "Clinical",
        "fields": [
            {"name": "ElementDescription", "type": "String", "nullable": False, "description": "Specify a current or historical smoking", "ehr_major_it": "6740 (null or blank for current, otherwise historical)"},
            {"name": "Description", "type": "String", "nullable": True, "description": "General description", "ehr_major_it": "4770 Tobacco"},
            {"name": "StartDate", "type": "String", "nullable": True, "description": "Start date", "ehr_major_it": "21283 SmokeStart"},
            {"name": "EndDate", "type": "String", "nullable": True, "description": "End date", "ehr_major_it": "6740 SmokeDT"},
            {"name": "SNOMED-CT", "type": "String", "nullable": True, "description": "SNOMED-CT", "ehr_major_it": "19850 Smoking Status Code"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Problems",
        "ccds_object": "CCDS.Problems",
        "section": "5.6.8",
        "category": "Clinical",
        "fields": [
            {"name": "Problem Name", "type": "String", "nullable": True, "description": "Problem Name", "ehr_major_it": "20925 Probs_name.MGDB"},
            {"name": "Onset Date", "type": "String", "nullable": True, "description": "Onset Date", "ehr_major_it": "20976 CQM ProblemOnset.MGDB"},
            {"name": "Resolved Date", "type": "String", "nullable": True, "description": "Resolved Date", "ehr_major_it": "20977 CQM ProblemResolve.MGDB"},
            {"name": "Diagnose Date", "type": "String", "nullable": True, "description": "Diagnose Date", "ehr_major_it": "20933 Probs_diagnosedDT.MGDB"},
            {"name": "SNOMED-CT", "type": "String", "nullable": True, "description": "SNOMED-CT", "ehr_major_it": "20928 Probs SNOMEDcode.MGDB"},
            {"name": "Status", "type": "String", "nullable": True, "description": "Status", "ehr_major_it": "20929 Probs_status.MGDB"},
            {"name": "AcuteChronic", "type": "String", "nullable": True, "description": "Acute Chronic", "ehr_major_it": "20930 Probs_severity.MGDB"},
            {"name": "ICD9 Code", "type": "String", "nullable": True, "description": "ICD9 Code", "ehr_major_it": "20926 Probs icd9code.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Medication",
        "ccds_object": "CCDS.Medications",
        "section": "5.6.9",
        "category": "Clinical",
        "fields": [
            {"name": "RxNorm", "type": "String", "nullable": True, "description": "RxNorm Code", "ehr_major_it": "19079 meds_flow_rxnorm"},
            {"name": "MedicationName", "type": "String", "nullable": True, "description": "Medication Name", "ehr_major_it": "2225 meds_flow_definition"},
            {"name": "StartDate", "type": "String", "nullable": True, "description": "Start Date", "ehr_major_it": "2225 meds_flow_definition"},
            {"name": "EndDate", "type": "String", "nullable": True, "description": "End Date", "ehr_major_it": "2225 meds_flow_definition"},
            {"name": "Route", "type": "String", "nullable": True, "description": "Route", "ehr_major_it": "2228 meds_flow_route"},
            {"name": "Frequency", "type": "String", "nullable": True, "description": "Frequency", "ehr_major_it": "2226 meds_flow_frequency"},
            {"name": "Dose", "type": "String", "nullable": True, "description": "Dose and unit", "ehr_major_it": "2229 meds_flow_dose"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
        ]
    },
    {
        "entity_name": "Medication Allergies",
        "ccds_object": "CCDS.Medication_Allergies",
        "section": "5.6.10",
        "category": "Clinical",
        "fields": [
            {"name": "Type", "type": "String", "nullable": True, "description": "Allergy type", "ehr_major_it": "11482-11603 (multiple slots)"},
            {"name": "Name", "type": "String", "nullable": True, "description": "Allergy name", "ehr_major_it": "11483-11604+ (multiple slots)"},
            {"name": "OnsetDate", "type": "String", "nullable": True, "description": "Allergy onset date", "ehr_major_it": "Observation time of 11486-11607"},
            {"name": "Symptom", "type": "String", "nullable": True, "description": "Symptoms", "ehr_major_it": "11485-11606 (multiple slots)"},
            {"name": "Severity", "type": "String", "nullable": True, "description": "Severity", "ehr_major_it": "11484-11605 (multiple slots)"},
            {"name": "Description", "type": "String", "nullable": True, "description": "Allergy description", "ehr_major_it": "6089 (vdata)"},
            {"name": "Algyid", "type": "String", "nullable": True, "description": "Allergy id", "ehr_major_it": "6089 (vdata)"},
            {"name": "RxNorm", "type": "String", "nullable": True, "description": "RxNorm code", "ehr_major_it": "6089 (vdata)"},
            {"name": "Inactive", "type": "String", "nullable": True, "description": "Inactive status", "ehr_major_it": "6089 (vdata)"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
        ]
    },
    {
        "entity_name": "Laboratory Tests",
        "ccds_object": "CCDS.Laboratory_Tests",
        "section": "5.6.11",
        "category": "Clinical",
        "fields": [
            {"name": "Test Name", "type": "String", "nullable": True, "description": "Test Name", "ehr_major_it": "12637 labresult_extrainfo (vdata)"},
            {"name": "Test Source", "type": "String", "nullable": True, "description": "Test Source", "ehr_major_it": "12637 labresult_extrainfo (vdata)"},
            {"name": "Observation Date Time", "type": "String", "nullable": True, "description": "Observation Date Time", "ehr_major_it": "12637 labresult_extrainfo (vdata)"},
            {"name": "Laboratory Name", "type": "String", "nullable": True, "description": "Laboratory Name", "ehr_major_it": "21108 labresult_laboratory (vdata)"},
            {"name": "Laboratory Address", "type": "String", "nullable": True, "description": "Laboratory Address", "ehr_major_it": "21108 labresult_laboratory (vdata)"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Laboratory Values",
        "ccds_object": "CCDS.Laboratory_Values",
        "section": "5.6.12",
        "category": "Clinical",
        "fields": [
            {"name": "LOINC Code", "type": "String", "nullable": True, "description": "LOINC Code", "ehr_major_it": "14074 labresult_ID"},
            {"name": "Name", "type": "String", "nullable": True, "description": "Lab results Name", "ehr_major_it": "12629 labresult_name"},
            {"name": "Value", "type": "String", "nullable": True, "description": "Lab results Value", "ehr_major_it": "12630 labresult_value"},
            {"name": "Unit", "type": "String", "nullable": True, "description": "Lab results Units", "ehr_major_it": "12631 labresult_unit"},
            {"name": "Range", "type": "String", "nullable": True, "description": "Lab results Range", "ehr_major_it": "12632 labresult_range"},
            {"name": "Observation Date Time", "type": "String", "nullable": True, "description": "Observation Date Time", "ehr_major_it": "12637 labresult_extrainfo (vdata)"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Vital Signs",
        "ccds_object": "CCDS.Vital_Signs",
        "section": "5.6.13",
        "category": "Clinical",
        "fields": [
            {"name": "Vitals Name", "type": "String", "nullable": False, "description": "Vitals Name", "ehr_major_it": "N/A"},
            {"name": "Timing Information", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
            {"name": "Value", "type": "String", "nullable": True, "description": "Value", "ehr_major_it": "0096, 0097, 0276, 0275, 0159, 0270, 0012, 0278, 0165"},
            {"name": "Unit", "type": "String", "nullable": False, "description": "Unit", "ehr_major_it": "N/A"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Implantable Device",
        "ccds_object": "CCDS.Implantable_Device",
        "section": "5.6.14",
        "category": "Clinical",
        "fields": [
            {"name": "UDI", "type": "String", "nullable": True, "description": "UDI", "ehr_major_it": "27836 ImplantableDeviceUDI"},
            {"name": "AssigningAuthority", "type": "String", "nullable": False, "description": "AssigningAuthority", "ehr_major_it": "N/A"},
            {"name": "SNOMED-CT", "type": "String", "nullable": True, "description": "SNOMED-CT", "ehr_major_it": "27837 ImplantableDeviceSNOMED"},
            {"name": "Device Name", "type": "String", "nullable": True, "description": "Device Name", "ehr_major_it": "27834 GMDN PT"},
            {"name": "Device ID", "type": "String", "nullable": True, "description": "Device ID", "ehr_major_it": "27841 ImplantableDeviceHTCP"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Procedures",
        "ccds_object": "CCDS.Procedures",
        "section": "5.6.15",
        "category": "Clinical",
        "fields": [
            {"name": "Procedure Name", "type": "String", "nullable": True, "description": "Procedure Name", "ehr_major_it": "19074 procds_name.MGDB"},
            {"name": "Date Procedure Performed", "type": "String", "nullable": True, "description": "Date Procedure Performed", "ehr_major_it": "19078 procds_dateperformed.MGDB"},
            {"name": "Status", "type": "String", "nullable": True, "description": "Status", "ehr_major_it": "19077 procds_status.MGDB"},
            {"name": "Target Site", "type": "String", "nullable": True, "description": "Target Site", "ehr_major_it": "19877 procds_targetsite.MGDB"},
            {"name": "CCI Code", "type": "String", "nullable": True, "description": "CCI Code", "ehr_major_it": "19076 procds_ccicode.MGDB"},
            {"name": "ICD9 Code", "type": "String", "nullable": True, "description": "ICD9 Code", "ehr_major_it": "19075 procds_icd9code.MGDB"},
            {"name": "SNOMED-CT", "type": "String", "nullable": True, "description": "SNOMED-CT", "ehr_major_it": "19895 procds_SNOMEDcode.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Care Team Members",
        "ccds_object": "CCDS.Care_Team_Members",
        "section": "5.6.16",
        "category": "Clinical",
        "fields": [
            {"name": "Followup Team", "type": "String", "nullable": True, "description": "Followup Team", "ehr_major_it": "19888 FollowupTeam.MGDB"},
            {"name": "Facility", "type": "String", "nullable": True, "description": "Facility", "ehr_major_it": "19889 FollowupFacility.MGDB"},
            {"name": "Address", "type": "String", "nullable": True, "description": "Address", "ehr_major_it": "19890 FollowupFacilAddr.MGDB"},
            {"name": "Phone", "type": "String", "nullable": True, "description": "Phone", "ehr_major_it": "19891 FollowupFacilPhone.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Immunizations",
        "ccds_object": "CCDS.Immunizations",
        "section": "5.6.17",
        "category": "Clinical",
        "fields": [
            {"name": "CVX Code", "type": "String", "nullable": True, "description": "CVX Code", "ehr_major_it": "19126 CVX Code.MGDB"},
            {"name": "Vaccine Name", "type": "String", "nullable": True, "description": "CPT Description", "ehr_major_it": "19125 CPT Description.MGDB"},
            {"name": "Vaccine Admin Date", "type": "String", "nullable": True, "description": "Vaccine Admin Date", "ehr_major_it": "20213 VaccineAdminDate.MGDB"},
            {"name": "Immunizations Status", "type": "String", "nullable": True, "description": "Immunizations Status", "ehr_major_it": "26032 Immunizations Status.MGDB"},
            {"name": "Lot Number", "type": "String", "nullable": True, "description": "Lot Number", "ehr_major_it": "19130 Vaccine Lot Number.MGDB"},
            {"name": "Manufacturer Name", "type": "String", "nullable": True, "description": "Manufacturer Name", "ehr_major_it": "19131 Manufacturer Name.MGDB"},
            {"name": "Additional Notes", "type": "String", "nullable": True, "description": "Additional Notes", "ehr_major_it": "19998 Vaccine Admin Note.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Health Concerns",
        "ccds_object": "CCDS.Health_Concerns",
        "section": "5.6.18",
        "category": "Clinical",
        "fields": [
            {"name": "Health Concerns", "type": "String", "nullable": True, "description": "Health Concerns", "ehr_major_it": "27889 HealthConcerns.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Assessment Treatment",
        "ccds_object": "CCDS.Assessment_Treatment",
        "section": "5.6.19",
        "category": "Clinical",
        "fields": [
            {"name": "Assessment", "type": "String", "nullable": True, "description": "Assessment", "ehr_major_it": "27888 Assessment.MGDB"},
            {"name": "Treatment", "type": "String", "nullable": True, "description": "Treatment", "ehr_major_it": "27890 Treatment.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Tkey", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
    {
        "entity_name": "Goals",
        "ccds_object": "CCDS.Goals",
        "section": "5.6.20",
        "category": "Clinical",
        "fields": [
            {"name": "Care Plan Goal", "type": "String", "nullable": True, "description": "Care Plan Goal", "ehr_major_it": "19924 CarePlanGoal.MGDB"},
            {"name": "Care Plan Instructions", "type": "String", "nullable": True, "description": "Care Plan Instructions", "ehr_major_it": "19925 CarePlanInst.MGDB"},
            {"name": "Care Plan Code", "type": "String", "nullable": True, "description": "Care Plan Code", "ehr_major_it": "19926 CarePlanCode.MGDB"},
            {"name": "Care Plan System", "type": "String", "nullable": True, "description": "Care Plan System", "ehr_major_it": "19927 CarePlanSystem.MGDB"},
            {"name": "MRN", "type": "String", "nullable": False, "description": "MRN of patient", "ehr_major_it": "0518 PatientSSN.adm"},
            {"name": "Nit", "type": "String", "nullable": False, "description": "Minor IT", "ehr_major_it": "N/A"},
            {"name": "Key", "type": "String", "nullable": False, "description": "Key in date format", "ehr_major_it": "N/A"},
        ]
    },
]

CCDA_SECTIONS = [
    "Admission Diagnosis", "Encounter Data", "Implantable Devices", "Problems",
    "Social History", "Allergies", "Discharge Medications", "Immunization",
    "Procedures", "Smoking Status", "Assessment", "Hospital Discharge Instructions",
    "Functional Status", "Plan of Care", "Reason for Referral", "Care Team",
    "Health Concerns", "Medications", "Vital Signs", "Cognitive Status",
    "Goals", "Results", "Laboratory Tests", "Payers"
]

def main():
    for e in ENTITIES:
        e["field_count"] = len(e["fields"])
    
    total_fields = sum(e["field_count"] for e in ENTITIES)
    fields_with_desc = sum(
        1 for e in ENTITIES for f in e["fields"]
        if f.get("description") and f["description"] not in ("", "N/A")
    )
    meta_fields = sum(
        1 for e in ENTITIES for f in e["fields"]
        if f["name"].lower() in ("mrn", "nit", "tkey", "key")
    )
    substantive_fields = total_fields - meta_fields
    
    # Build full inventory
    inventory = {
        "source": "250-70079_CliniComp_EHR_ONC-API_USCDI.pdf",
        "source_version": "Rev D, 11 Jan 2024",
        "total_entities": len(ENTITIES),
        "total_fields": total_fields,
        "substantive_fields": substantive_fields,
        "metadata_fields_mrn_nit_tkey": meta_fields,
        "entities": ENTITIES,
        "ccda_sections": CCDA_SECTIONS,
        "ccda_section_count": len(CCDA_SECTIONS)
    }
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Summary
    summary = {
        "total_entities": len(ENTITIES),
        "total_fields": total_fields,
        "substantive_fields": substantive_fields,
        "metadata_fields": meta_fields,
        "fields_with_descriptions": fields_with_desc,
        "description_coverage_pct": round(fields_with_desc / max(1, total_fields) * 100, 1),
        "all_fields_typed": True,  # All fields are String type
        "all_fields_nullable_documented": True,
        "entity_summary": [
            {
                "entity_name": e["entity_name"],
                "ccds_object": e["ccds_object"],
                "category": e["category"],
                "field_count": e["field_count"],
                "substantive_fields": e["field_count"] - sum(1 for f in e["fields"] if f["name"].lower() in ("mrn", "nit", "tkey", "key")),
            }
            for e in ENTITIES
        ],
        "ccda_sections": CCDA_SECTIONS,
        "ccda_section_count": len(CCDA_SECTIONS),
        "categories": {
            "Demographics": {
                "entities": [e["entity_name"] for e in ENTITIES if e["category"] == "Demographics"],
                "count": sum(1 for e in ENTITIES if e["category"] == "Demographics"),
                "total_fields": sum(e["field_count"] for e in ENTITIES if e["category"] == "Demographics"),
            },
            "Clinical": {
                "entities": [e["entity_name"] for e in ENTITIES if e["category"] == "Clinical"],
                "count": sum(1 for e in ENTITIES if e["category"] == "Clinical"),
                "total_fields": sum(e["field_count"] for e in ENTITIES if e["category"] == "Clinical"),
            },
            "Billing": {"entities": [], "count": 0, "total_fields": 0},
            "Orders": {"entities": [], "count": 0, "total_fields": 0},
            "Notes/Documents": {"entities": [], "count": 0, "total_fields": 0},
            "Specialty": {"entities": [], "count": 0, "total_fields": 0},
        }
    }
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Total entities: {len(ENTITIES)}")
    print(f"Total fields: {total_fields}")
    print(f"  Substantive: {substantive_fields}")
    print(f"  Metadata (MRN/nit/tkey): {meta_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({round(fields_with_desc/total_fields*100,1)}%)")
    print(f"C-CDA sections: {len(CCDA_SECTIONS)}")
    print()
    print("By category:")
    for cat in ("Demographics", "Clinical"):
        ents = [e for e in ENTITIES if e["category"] == cat]
        flds = sum(e["field_count"] for e in ents)
        print(f"  {cat}: {len(ents)} entities, {flds} fields")
    print()
    for e in ENTITIES:
        sub = e["field_count"] - sum(1 for f in e["fields"] if f["name"].lower() in ("mrn", "nit", "tkey", "key"))
        print(f"  {e['entity_name']:25s} {e['field_count']:3d} fields ({sub} substantive)")

if __name__ == "__main__":
    main()
