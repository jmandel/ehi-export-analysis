#!/usr/bin/env python3
"""Parse the ReLiMed Patient Export File Format PDF (via pdftotext) 
and extract structured inventory of worksheets and per-patient file types."""

import json, re, subprocess

# Extract PDF text
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/Patient_Export_Data_File_Format.pdf", "-"],
    capture_output=True, text=True
)
text = result.stdout

# ---- XLSX Worksheets ----
worksheets = [
    "Locations",
    "License Providers",
    "Referring Providers",
    "Master Insurances",
    "Resources/staff members",
    "Patient Employers",
    "Patient Demographics",
    "Patient Guarantors",
    "Patient Contacts",
    "Patient Pharmacies",
    "Patient Insurances",
    "Past Appointments",
    "Patient Notes",
    "Patient Alerts (Billing etc.)",
    "Patient Medications",
    "Patient Allergies",
    "Patient Diagnosis",
    "Future Appointments",
]

# ---- Per-patient file types ----
per_patient_files = [
    {"pattern": "CCD.xml", "format": "XML", "description": "Used for viewing/importing patient information within supported EMR systems."},
    {"pattern": "CCD.html", "format": "HTML", "description": "A human readable version of the CCD"},
    {"pattern": "Demographics_*_MedicalHistory.pdf", "format": "PDF", "description": "A report that contains a snapshot summary of the patient's demographic and insurance information."},
    {"pattern": "MedicalHx_*_MedicalHistory.pdf", "format": "PDF", "description": "A report that contains a snapshot summary of the patient's active medications, chronic problems, and active allergies."},
    {"pattern": "Encounter_<yyyyMMdd>_<hhmm>_<type>.pdf", "format": "PDF", "description": "One or more files that contain the generated summary for the associated encounter."},
    {"pattern": "Document_<type>_<name>.pdf", "format": "PDF", "description": "One or more files that contain a document that was uploaded to the patient's chart."},
    {"pattern": "LabResult_<yyyyMMdd>_<hhmm>_<guid>.pdf", "format": "PDF", "description": "One or more files that contain the e-lab results that were received for the patient."},
    {"pattern": "Form_<yyyyMMdd>_<hhmm>_<type>_<name>.rtf", "format": "RTF", "description": "One or more files that contain a custom user form that was generated for the patient."},
]

# ---- Single patient export selectable sections (from UI screenshot description) ----
single_patient_sections = [
    "Encounters",
    "Active Medications",
    "Chronic Problems",
    "Allergies",
    "Documents",
    "eLab Results",
    "Patient Forms",
    "CCD",
    "Claims",
    "Insurance Information",
    "Active Allergies (Medical History)",
    "Active Medications (Medical History)",
    "Chronic Problems (Medical History)",
    "Restricted Encounter Types",
    "Restricted Document Types",
]

# ---- Build entity inventory ----
entities = []

for ws in worksheets:
    entities.append({
        "entity_name": ws,
        "source": "patient-data-export.xlsx (bulk export)",
        "format": "XLSX worksheet",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "description": f"Worksheet in the bulk export XLSX workbook. No field-level documentation provided.",
        "category": categorize(ws) if False else None,
    })

# Categorize
def categorize(name):
    admin = ["Locations", "License Providers", "Referring Providers", "Master Insurances", "Resources/staff members"]
    scheduling = ["Past Appointments", "Future Appointments"]
    clinical = ["Patient Notes", "Patient Medications", "Patient Allergies", "Patient Diagnosis", "Patient Alerts (Billing etc.)"]
    demographics = ["Patient Demographics", "Patient Guarantors", "Patient Contacts", "Patient Employers", "Patient Pharmacies", "Patient Insurances"]
    if name in admin: return "Practice/Administrative"
    if name in scheduling: return "Scheduling"
    if name in clinical: return "Clinical"
    if name in demographics: return "Patient Demographics & Relationships"
    return "Unknown"

# Re-categorize
for e in entities:
    e["category"] = categorize(e["entity_name"])

for pf in per_patient_files:
    entities.append({
        "entity_name": pf["pattern"],
        "source": "Medical Records folder (per-patient files)",
        "format": pf["format"],
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "description": pf["description"],
        "category": "Per-Patient Documents",
    })

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

# Summary
summary = {
    "product": "ReLiMed EMR",
    "source_artifact": "Patient_Export_Data_File_Format.pdf (4 pages)",
    "total_entities": len(entities),
    "xlsx_worksheets": len(worksheets),
    "per_patient_file_types": len(per_patient_files),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "field_level_documentation": False,
    "sample_data_provided": False,
    "schema_provided": False,
    "categories": {},
    "export_mechanisms": {
        "single_patient": {
            "format": "PDF",
            "access": "Self-service via Patient Chart → Patient Export",
            "privilege_required": "Medical Record Request",
            "selectable_sections": single_patient_sections,
        },
        "bulk_export": {
            "format": "XLSX workbook + per-patient files (PDF, RTF, XML, HTML) in ZIP",
            "access": "Vendor-assisted (contact ReLi Med support)",
            "delivery": "Password-protected ZIP via SFTP",
            "worksheets": worksheets,
            "per_patient_file_types": [p["pattern"] for p in per_patient_files],
        }
    }
}

# Category breakdown
cats = {}
for e in entities:
    c = e["category"]
    if c not in cats:
        cats[c] = {"entity_count": 0, "total_fields": 0}
    cats[c]["entity_count"] += 1
    cats[c]["total_fields"] += e["field_count"]
summary["categories"] = cats

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
