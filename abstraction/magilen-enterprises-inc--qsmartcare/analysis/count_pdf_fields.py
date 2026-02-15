"""
Count distinct data fields per section in the PDF export.
Uses the extracted PDF text to identify column headers and field labels.
"""

import re

OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/magilen-enterprises-inc--qsmartcare/analysis"

with open(f"{OUTPUT_DIR}/pdf_text.txt", "r") as f:
    pdf_text = f.read()

# Manual inventory based on PDF inspection
pdf_sections = {
    "DEMOGRAPHIC INFO": {
        "fields": ["First Name", "Last Name", "Middle Name", "Previous Name", "Suffix", "Sex",
                   "Dob", "Marital Status", "Pref Language", "PCare Provider", "Race", "Ethnicity",
                   "Current Address", "Previous Address", "Ssn", "Granular Race", "Phone", "Mobile",
                   "Email", "Fax", "City", "State", "Address", "ZipCode"],
        "count": 24,
        "in_json": True,
    },
    "ORGANIZATION INFO": {
        "fields": ["Name", "Alias Name", "Phone No", "Fax No", "Repository"],
        "count": 5,
        "in_json": True,
    },
    "ORGANIZATION ADDRESS INFO": {
        "fields": ["Street Address", "City", "State", "Postal Code", "Country", "Website"],
        "count": 6,
        "in_json": True,
    },
    "LOCATION INFO": {
        "fields": ["Name", "Phone No", "Street Address", "City", "State", "Postal Code", "Country"],
        "count": 7,
        "in_json": True,
    },
    "CARE TEAM INFO": {
        "fields": ["First Name", "Last Name", "Phone No", "Role"],
        "count": 4,
        "in_json": True,
    },
    "ENCOUNTERS INFO": {
        "fields": ["Consult For", "Chief Complaints", "DOS", "Smoking Status"],
        "count": 4,
        "in_json": True,
    },
    "HISTORY OF PRESENT ILLNESS INFO": {
        "fields": ["History of Present Illness"],
        "count": 1,
        "in_json": True,
    },
    "Social History": {
        "fields": ["Social History (free text)"],
        "count": 1,
        "in_json": True,
    },
    "Family History": {
        "fields": ["Family History (free text)"],
        "count": 1,
        "in_json": False,
    },
    "ASSESSMENT AND PLAN OF TREATMENT INFO": {
        "fields": ["Assessment", "Plan Of Treatment"],
        "count": 2,
        "in_json": True,
    },
    "PATIENT RELATIONSHIP INFO": {
        "fields": ["Name", "Relationship"],
        "count": 2,
        "in_json": False,
    },
    "INSURANCE INFO": {
        "fields": ["Primary Insurance", "Secondary Insurance"],
        "count": 2,
        "in_json": False,
    },
    "SPOUSE INFO": {
        "fields": ["Name", "Occupation", "Workplace", "Work Phone", "Organization Name"],
        "count": 5,
        "in_json": False,
    },
    "PAST MEDICAL HISTORY INFO": {
        "fields": ["Diagnosis Code", "Diagnosis Name", "Start Date", "End Date", "Status"],
        "count": 5,
        "in_json": False,
    },
    "ANTICOAGULANT INFO": {
        "fields": ["Anticoagulant Name"],
        "count": 1,
        "in_json": False,
    },
    "PATIENT WOUND INFO": {
        "fields": ["Wound number", "Wound DOS", "Wound Location", "Wound Side", "Sub Location",
                   "Vertical Plane", "Horizontal Plane", "Status"],
        "count": 8,
        "in_json": True,
    },
    "IMPLANTABLE DEVICE INFO": {
        "fields": ["Unique Device Identifiers", "Company Name", "Brand Name", "Version/Model",
                   "MRI Safety Info", "Labeled Contains NRL", "GMDN PT Name", "Manufactured Date",
                   "Expiration Date", "FDA Product Code", "FDA Product Name", "Status"],
        "count": 12,
        "in_json": True,
    },
    "ALLERGY INFO": {
        "fields": ["Allergies", "Allergy Reaction", "Updated", "Start Date", "End Date",
                   "Severity", "Reaction Severity", "Types of Allergies", "Status"],
        "count": 9,
        "in_json": True,
    },
    "MEDICATION INFO": {
        "fields": ["Medication", "Medication Type", "Dosage", "Route", "Frequency",
                   "RxNorm Code", "Status"],
        "count": 7,
        "in_json": True,
    },
    "DIAGNOSIS INFO": {
        "fields": ["Diagnosis Code", "Diagnosis Name", "Start Date", "End Date", "Status"],
        "count": 5,
        "in_json": True,
    },
    "LAB INFO": {
        "fields": ["Date", "Path", "Lab Name", "Lab Location"],
        "count": 4,
        "in_json": False,
    },
    "BLOOD PRESSURE INFO": {
        "fields": ["Date", "Systolic", "Diastolic"],
        "count": 3,
        "in_json": True,
    },
    "BLOOD SUGAR INFO": {
        "fields": ["Date", "Fasting", "Random", "HbA1c"],
        "count": 4,
        "in_json": False,
    },
    "BMI INFO": {
        "fields": ["Date", "Height", "Weight", "HbA1c (BMI)"],
        "count": 4,
        "in_json": True,
    },
    "PULSE INFO": {
        "fields": ["Date", "Pulse"],
        "count": 2,
        "in_json": True,
    },
    "PULSE OXIMETRY INFO": {
        "fields": ["Date", "Pulse Oximetry"],
        "count": 2,
        "in_json": False,
    },
    "BODY TEMPERATURE INFO": {
        "fields": ["Date", "Temperature"],
        "count": 2,
        "in_json": True,
    },
    "HEART RATE INFO": {
        "fields": ["Date", "Heart Rate"],
        "count": 2,
        "in_json": True,
    },
    "RESPIRATORY RATE INFO": {
        "fields": ["Date", "Respiratory Rate"],
        "count": 2,
        "in_json": True,
    },
    "OXYGEN CONCENTRATION INFO": {
        "fields": ["Date", "Oxygen Concentration"],
        "count": 2,
        "in_json": False,
    },
    "PAST SURGICAL HISTORIES": {
        "fields": ["Procedure Code", "Procedure Name", "Start Date", "End Date", "OutCome", "Status"],
        "count": 6,
        "in_json": True,
    },
    "IMMUNIZATION": {
        "fields": ["Vaccine Code", "Code System", "Vaccine Name", "Date", "Status", "Additional Notes"],
        "count": 6,
        "in_json": True,
    },
    "FUNCTIONAL STATUS": {
        "fields": ["Code", "Code System", "Name", "Date"],
        "count": 4,
        "in_json": False,
    },
    "COGNITIVE STATUS": {
        "fields": ["Code", "Code System", "Name", "Date"],
        "count": 4,
        "in_json": False,
    },
}

total_fields = sum(s["count"] for s in pdf_sections.values())
total_sections = len(pdf_sections)
in_json = sum(1 for s in pdf_sections.values() if s["in_json"])
not_in_json = sum(1 for s in pdf_sections.values() if not s["in_json"])

print(f"PDF Section Inventory")
print(f"{'='*60}")
print(f"Total sections: {total_sections}")
print(f"Total fields: {total_fields}")
print(f"Sections also in JSON: {in_json}")
print(f"Sections PDF-only: {not_in_json}")
print()

print(f"{'Section':<40s} {'Fields':>6s} {'In JSON?':>10s}")
print("-" * 60)
for name, info in pdf_sections.items():
    print(f"{name:<40s} {info['count']:>6d} {'Yes' if info['in_json'] else 'NO':>10s}")
print("-" * 60)
print(f"{'TOTAL':<40s} {total_fields:>6d}")

import json
with open(f"{OUTPUT_DIR}/pdf-field-inventory.json", "w") as f:
    json.dump({
        "total_sections": total_sections,
        "total_fields": total_fields,
        "sections_in_json": in_json,
        "sections_pdf_only": not_in_json,
        "sections": {k: {"fields": v["fields"], "count": v["count"], "in_json": v["in_json"]} for k, v in pdf_sections.items()}
    }, f, indent=2)

print(f"\n✅ Saved to {OUTPUT_DIR}/pdf-field-inventory.json")
