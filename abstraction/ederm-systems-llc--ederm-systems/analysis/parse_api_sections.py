"""
Parse the eDerm API Documentation PDF to extract the data sections/parameters
available in the GetPatientData API, and the C-CDA sections in the sample response.
Produces entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import subprocess
import re

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/eDerm-API-Documentation-G8-G9.pdf", "-"],
    capture_output=True, text=True
)
pdf_text = result.stdout

# The API parameters for GetPatientData (from the table at end of PDF)
api_parameters = [
    {"parameter": "patientname", "ccda_element": "Patient Name", "category": "Demographics"},
    {"parameter": "patientgender", "ccda_element": "Sex", "category": "Demographics"},
    {"parameter": "patientdob", "ccda_element": "Date of Birth", "category": "Demographics"},
    {"parameter": "patientrace", "ccda_element": "Race", "category": "Demographics"},
    {"parameter": "patientethnicity", "ccda_element": "Ethnicity", "category": "Demographics"},
    {"parameter": "patientpreferredlanguage", "ccda_element": "Preferred Language", "category": "Demographics"},
    {"parameter": "smokingstatus", "ccda_element": "Smoking Status", "category": "Social History"},
    {"parameter": "problems", "ccda_element": "Problems", "category": "Clinical"},
    {"parameter": "medications", "ccda_element": "Medications", "category": "Clinical"},
    {"parameter": "medicationallergies", "ccda_element": "Medication Allergies", "category": "Clinical"},
    {"parameter": "labtest", "ccda_element": "Laboratory Tests", "category": "Clinical"},
    {"parameter": "labresults", "ccda_element": "Laboratory Values Results", "category": "Clinical"},
    {"parameter": "vitalsigns", "ccda_element": "Vital Signs", "category": "Clinical"},
    {"parameter": "procedures", "ccda_element": "Procedures", "category": "Clinical"},
    {"parameter": "careteammembers", "ccda_element": "Care Team Members", "category": "Clinical"},
    {"parameter": "immunizations", "ccda_element": "Immunizations", "category": "Clinical"},
    {"parameter": "udiforpatientdevices", "ccda_element": "Unique Device Identifiers (procedures)", "category": "Clinical"},
    {"parameter": "assessment", "ccda_element": "Assessment and Plan", "category": "Clinical"},
    {"parameter": "goals", "ccda_element": "Goals", "category": "Clinical"},
    {"parameter": "healthconcerns", "ccda_element": "Health Concerns", "category": "Clinical"},
]

# C-CDA sections visible in the sample response (from examining the embedded XML)
ccda_sections_in_sample = [
    "Chief Complaint and Reason for Visit",
    "Allergies and Adverse Reactions",
    "Immunizations",
    "Medications",
    "Problems",
    "Procedures",
    "Results (Laboratory)",
    "Plan of Treatment",
    "Social History (Smoking Status)",
    "Vital Signs",
    "Goals",
    "Health Concerns",
    "Assessment Section",
    "Mental Status",
    "Functional Status",
    "Referrals",
]

# Build entity inventory
entities = []

# The single "entity" is the C-CDA document returned by GetPatientData
entity = {
    "entity_name": "GetPatientData C-CDA Response",
    "description": "C-CDA 2.1 document returned by the eDerm proprietary REST API. This is NOT a (b)(10) EHI export — it is the (g)(9)/(g)(10) clinical summary API.",
    "format": "C-CDA 2.1 (XML)",
    "category": "Clinical Summary (USCDI scope only)",
    "fields": [],
    "ccda_sections_in_sample": ccda_sections_in_sample,
    "notes": "API returns standard C-CDA sections toggleable via boolean parameters. No field-level data dictionary. No vendor-specific extensions documented."
}

for param in api_parameters:
    entity["fields"].append({
        "name": param["parameter"],
        "type": "boolean (API toggle)",
        "description": f"Toggles inclusion of {param['ccda_element']} in the C-CDA response",
        "ccda_element": param["ccda_element"],
        "category": param["category"],
        "has_description": True,
        "has_type": True,
    })

entities.append(entity)

# Also document the other API endpoints
entities.append({
    "entity_name": "SearchPatient",
    "description": "Patient search API returning basic demographics (MRN, Id, FirstName, LastName, DoB, Gender)",
    "format": "JSON",
    "category": "API Endpoint",
    "fields": [
        {"name": "firstname", "type": "string", "description": "Search input: patient first name", "has_description": True, "has_type": True},
        {"name": "lastname", "type": "string", "description": "Search input: patient last name", "has_description": True, "has_type": True},
        {"name": "dob", "type": "string (MM/DD/YYYY)", "description": "Search input: date of birth", "has_description": True, "has_type": True},
        {"name": "gender", "type": "string", "description": "Search input: gender (M/F)", "has_description": True, "has_type": True},
    ],
    "response_fields": [
        {"name": "MRN", "type": "string", "description": "Medical Record Number"},
        {"name": "Id", "type": "string", "description": "Internal patient ID"},
        {"name": "FirstName", "type": "string", "description": "Patient first name"},
        {"name": "LastName", "type": "string", "description": "Patient last name"},
        {"name": "DoB", "type": "string (YYYYMMDD)", "description": "Date of birth"},
        {"name": "Gender", "type": "string", "description": "Gender code"},
    ],
    "notes": "Search endpoint, not an export mechanism"
})

entities.append({
    "entity_name": "GetPatientEncounters",
    "description": "Lists encounters for a patient with visit date and provider name",
    "format": "JSON",
    "category": "API Endpoint",
    "fields": [
        {"name": "patientid", "type": "string", "description": "Internal patient ID", "has_description": True, "has_type": True},
        {"name": "ccdafromdatetime", "type": "string (datetime)", "description": "Start date filter", "has_description": True, "has_type": True},
        {"name": "ccdatodatetime", "type": "string (datetime)", "description": "End date filter", "has_description": True, "has_type": True},
    ],
    "response_fields": [
        {"name": "PatientId", "type": "string", "description": "Patient ID"},
        {"name": "VisitBeginDateTime", "type": "string (datetime)", "description": "Visit date/time"},
        {"name": "ProviderFullName", "type": "string", "description": "Provider name"},
    ],
    "notes": "Returns minimal encounter metadata only"
})

# Full inventory
full_inventory = {
    "vendor": "eDerm Systems LLC",
    "product": "eDerm Systems",
    "version": "2.8.0",
    "source_artifact": "downloads/eDerm-API-Documentation-G8-G9.pdf",
    "source_type": "API documentation PDF (26 pages)",
    "is_ehi_export": False,
    "is_g10_api": True,
    "notes": "No (b)(10) EHI export documentation exists. This inventory documents the only available API, which is the (g)(9)/(g)(10) C-CDA clinical summary API. There is no data dictionary, no export schema, and no documentation of any kind describing a full EHI export.",
    "entities": entities,
    "total_api_parameters": len(api_parameters),
    "total_ccda_sections_in_sample": len(ccda_sections_in_sample),
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary
summary = {
    "vendor": "eDerm Systems LLC",
    "product": "eDerm Systems",
    "version": "2.8.0",
    "ehi_export_exists": False,
    "what_exists_instead": "Proprietary REST API returning C-CDA 2.1 documents (USCDI clinical summary scope)",
    "total_entities_documented": 3,  # GetPatientData, SearchPatient, GetPatientEncounters
    "total_api_toggle_parameters": len(api_parameters),
    "total_ccda_sections_in_sample": len(ccda_sections_in_sample),
    "data_dictionary_exists": False,
    "field_level_documentation": False,
    "sample_data_provided": True,  # embedded C-CDA sample in the PDF
    "sample_data_format": "C-CDA 2.1 XML (embedded in PDF as escaped string)",
    "categories": {
        "Demographics": {"parameters": 6, "description": "Patient name, sex, DOB, race, ethnicity, preferred language"},
        "Social History": {"parameters": 1, "description": "Smoking status only"},
        "Clinical": {"parameters": 13, "description": "Problems, medications, allergies, labs, vitals, procedures, care team, immunizations, devices, assessment/plan, goals, health concerns"},
    },
    "domains_covered_by_api": [
        "Demographics (basic)",
        "Problems/Conditions",
        "Medications",
        "Allergies",
        "Lab Tests/Results",
        "Vital Signs",
        "Procedures",
        "Immunizations",
        "Implantable Devices",
        "Care Team",
        "Assessment and Plan",
        "Goals",
        "Health Concerns",
        "Smoking Status",
    ],
    "domains_NOT_covered": [
        "Clinical Photography (core dermatology feature)",
        "Pathology Lifecycle / Biopsy Tracking",
        "Cancer Patient Tracking",
        "Billing / Claims / Revenue Cycle (full RCM module exists)",
        "Insurance Information and Verification",
        "Scheduling / Appointments",
        "Phone Messages",
        "Scanned Documents",
        "Consent Forms",
        "Dermatology-specific Charting (One-Touch, 3D anatomical maps)",
        "Smart Coder Output",
        "Encounter Notes (beyond C-CDA generic sections)",
    ],
    "fhir_server_status": "Dead (SSL cert expired Feb 10 2026, FHIR app undeployed, returns 404)",
    "classification": {
        "coverage_breadth": "Minimal/stub/unclear",
        "export_approach": "Repackaged existing export",
    }
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities documented: {len(entities)}")
print(f"API parameters: {len(api_parameters)}")
print(f"C-CDA sections in sample: {len(ccda_sections_in_sample)}")
print("Written: entity-inventory-full.json, entity-inventory-summary.json")
