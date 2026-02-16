"""
Parse the MDRhythm B10 Data Export Instructions PDF and the ONC compliance page
to extract structured information about the EHI export.
Produces entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import subprocess
import re

# Extract B10 PDF text
result = subprocess.run(
    ["pdftotext", "-layout", "downloads/MDRhythm B10 Data Export Instructions.pdf", "-"],
    capture_output=True, text=True
)
b10_text = result.stdout

# The B10 export explicitly lists these 6 data categories
b10_categories = [
    "Patient Demographics",
    "Allergy Details",
    "Current Medication Details and Medication History",
    "Diagnosis and Problem Information",
    "Visit Note Information",
    "Vitals Information",
]

# From the sample export screenshot (page 2-3), we can see these fields:
# Visit Details header: Patient name, Provider name, Sex, DOB, Visit Date
# Subjective section: Allergies list, Medical History list, Meds Review
# Objective section: Vitals (BP, Respiration, Temperature, Pulse, Height, Weight, BMI), Physical Exam
# Assessment section: Diagnosis Codes, Procedure Codes
# Plan section: Diagnostic Tests, Current Medications table, Medication by Others table, Plan of Care

# Build entity inventory from what the B10 documentation explicitly states
entities = []

# 1. Patient Demographics
entities.append({
    "entity_name": "Patient Demographics",
    "category": "Demographics",
    "fields": [
        {"name": "Patient Name", "type": "text", "description": "Patient's full name (visible in sample export header)"},
        {"name": "Sex", "type": "text", "description": "Patient's sex/gender"},
        {"name": "DOB", "type": "date", "description": "Date of birth"},
    ],
    "notes": "Only name, sex, and DOB visible in sample. No address, contact, insurance, or other demographic fields documented.",
    "field_count": 3,
    "source": "B10 PDF page 2 sample export screenshot"
})

# 2. Allergy Details
entities.append({
    "entity_name": "Allergy Details",
    "category": "Allergies",
    "fields": [
        {"name": "Allergy", "type": "text", "description": "Name of allergen (e.g., 'Amoxicillin, Apples, Beer, Shampoo' in sample)"},
    ],
    "notes": "Sample shows allergen names only as a comma-separated list. No severity, reaction type, onset date, or status fields visible.",
    "field_count": 1,
    "source": "B10 PDF page 2 sample export screenshot"
})

# 3. Current Medication Details and Medication History
entities.append({
    "entity_name": "Current Medication Details",
    "category": "Medications",
    "fields": [
        {"name": "Medication", "type": "text", "description": "Medication name and strength"},
        {"name": "SIG/Directions", "type": "text", "description": "Dosing instructions"},
        {"name": "Supply", "type": "text", "description": "Supply quantity"},
        {"name": "Count", "type": "text", "description": "Count/quantity"},
        {"name": "Refills", "type": "text", "description": "Number of refills"},
        {"name": "Date", "type": "date", "description": "Date prescribed or started"},
        {"name": "Status", "type": "text", "description": "Active/Inactive status"},
    ],
    "notes": "Sample shows a table with columns: Medication, SIG/Directions, Supply, Count, Refills, Date, Status. Separate section for 'Medication by Others' with same columns.",
    "field_count": 7,
    "source": "B10 PDF page 2-3 sample export screenshot"
})

# 4. Diagnosis and Problem Information
entities.append({
    "entity_name": "Diagnosis and Problem Information",
    "category": "Diagnoses/Problems",
    "fields": [
        {"name": "Medical History", "type": "text", "description": "List of medical history items with dates"},
        {"name": "Diagnosis Codes", "type": "text", "description": "Diagnosis codes with descriptions in the Assessment section"},
    ],
    "notes": "Sample shows Medical History as a list (e.g. 'Acute and subacute liver necrosis', 'Anxiety started 1/27/2016 test 1') and Diagnosis Codes in Assessment with ICD codes and descriptions.",
    "field_count": 2,
    "source": "B10 PDF page 2 sample export screenshot"
})

# 5. Visit Note Information
entities.append({
    "entity_name": "Visit Note Information",
    "category": "Clinical Notes",
    "fields": [
        {"name": "Visit Date", "type": "date", "description": "Date of the visit"},
        {"name": "Provider Name", "type": "text", "description": "Name of provider for the visit"},
        {"name": "Subjective", "type": "text", "description": "SOAP note subjective section"},
        {"name": "Objective", "type": "text", "description": "SOAP note objective section"},
        {"name": "Assessment", "type": "text", "description": "SOAP note assessment section"},
        {"name": "Plan", "type": "text", "description": "SOAP note plan section"},
        {"name": "Procedure Codes", "type": "text", "description": "CPT/procedure codes listed in Assessment"},
        {"name": "Plan of Care", "type": "text", "description": "Care plan items (e.g., nutrition, exercise, dietary management)"},
        {"name": "Goals", "type": "text", "description": "Health goals"},
        {"name": "Health Concerns", "type": "text", "description": "Health concerns"},
        {"name": "Electronic Signature", "type": "text", "description": "Electronically signed by provider name and timestamp"},
    ],
    "notes": "Each visit note appears with SOAP structure. Sample shows provider 'Max Burger, MD', visit date 11/07/2022. Includes diagnosis codes, procedure codes, diagnostic tests, and plan of care within the note.",
    "field_count": 11,
    "source": "B10 PDF page 2-3 sample export screenshot"
})

# 6. Vitals Information
entities.append({
    "entity_name": "Vitals Information",
    "category": "Vitals",
    "fields": [
        {"name": "BP", "type": "text", "description": "Blood pressure (e.g., '130/76 mmHg')"},
        {"name": "Arm Sitting", "type": "text", "description": "BP measurement position"},
        {"name": "Respiration", "type": "numeric", "description": "Respiratory rate"},
        {"name": "Temperature", "type": "numeric", "description": "Body temperature in °F"},
        {"name": "Pulse", "type": "numeric", "description": "Heart rate"},
        {"name": "Height", "type": "text", "description": "Height with percentile"},
        {"name": "Weight", "type": "numeric", "description": "Weight in lbs"},
        {"name": "BMI", "type": "numeric", "description": "Body Mass Index"},
    ],
    "notes": "Sample shows: 'BP: 130/76 mmHg L Arm Sitting, Respiration: 14 Unlabored, Temperature: 98.4 °F, Pulse: 98 Regular /min, Height: 5-9.0\" (46%), Weight: 160 Lbs, BMI: 23.63 (70%)'",
    "field_count": 8,
    "source": "B10 PDF page 2 sample export screenshot"
})

# Total field count
total_fields = sum(e["field_count"] for e in entities)
total_entities = len(entities)

# All fields have descriptions (from sample screenshot observation)
fields_with_descriptions = total_fields  # We described all based on the sample

inventory = {
    "product": "MDRhythm Version 8",
    "vendor": "TechSoft, Inc.",
    "export_format": "PDF",
    "export_mechanism": "Web portal (https://patientdata.mdronline.net) - practice login, select patients, click 'Export EHR'",
    "max_patients_per_export": 5,
    "documentation_source": "MDRhythm B10 Data Export Instructions.pdf (3 pages)",
    "data_dictionary_provided": False,
    "sample_data_provided": True,
    "sample_data_format": "Screenshot of PDF export in B10 instructions document",
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "entities": entities,
    "b10_documented_categories": b10_categories,
    "fhir_api_resources": [
        "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
        "Device", "DiagnosticReport", "DocumentReference", "Encounter",
        "Goal", "Immunization", "Location", "Medication", "MedicationRequest",
        "Observation", "Organization", "Patient", "Practitioner",
        "PractitionerRole", "Procedure", "Provenance"
    ],
    "fhir_api_resource_count": 20,
    "notes": [
        "The B10 export is a PDF file, not structured/machine-readable data.",
        "No data dictionary is provided - only a 3-page PDF with instructions and one sample export screenshot.",
        "The export covers 6 clinical data categories only.",
        "No billing, insurance, scheduling, pharmacy/inventory, document management, or administrative data is included.",
        "The FHIR API (g)(10) covers 20 USCDI resource types - all clinical, no billing or operational data.",
        "The B10 export appears to be a subset of what's available via the FHIR API, rendered as PDF.",
        "Maximum 5 patients per export batch.",
    ]
}

# Write full inventory
with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "product": inventory["product"],
    "vendor": inventory["vendor"],
    "export_format": inventory["export_format"],
    "total_entities": inventory["total_entities"],
    "total_fields": inventory["total_fields"],
    "fields_with_descriptions": inventory["fields_with_descriptions"],
    "data_dictionary_provided": inventory["data_dictionary_provided"],
    "b10_documented_categories": inventory["b10_documented_categories"],
    "category_breakdown": {},
    "missing_domains": [
        "Insurance / Coverage",
        "Claims / Billing",
        "Payments",
        "Scheduling / Appointments",
        "Pharmacy / Inventory",
        "Document Management (scans, faxes)",
        "Patient Portal Messages",
        "Immunizations",
        "Lab Results (structured)",
        "Imaging / Diagnostic Reports",
        "Care Plans / Goals (structured)",
        "Procedures (structured)",
        "Care Team",
        "Devices / UDI",
        "Referrals / Orders",
        "Consents / Directives",
    ],
    "covered_domains": [
        "Demographics (minimal - name, sex, DOB only)",
        "Allergies (names only)",
        "Medications (current + history, tabular)",
        "Diagnoses / Problems (medical history + diagnosis codes)",
        "Clinical Notes (SOAP visit notes)",
        "Vitals (within visit notes)",
    ]
}

for e in entities:
    cat = e["category"]
    if cat not in summary["category_breakdown"]:
        summary["category_breakdown"][cat] = {"entity_count": 0, "field_count": 0}
    summary["category_breakdown"][cat]["entity_count"] += 1
    summary["category_breakdown"][cat]["field_count"] += e["field_count"]

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_descriptions}")
print(f"B10 categories: {len(b10_categories)}")
print(f"FHIR API resources: {inventory['fhir_api_resource_count']}")
print("\nCategory breakdown:")
for cat, info in summary["category_breakdown"].items():
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
print("\nFiles written: entity-inventory-full.json, entity-inventory-summary.json")
