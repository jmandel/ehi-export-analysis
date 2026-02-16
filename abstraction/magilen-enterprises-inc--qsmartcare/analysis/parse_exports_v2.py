#!/usr/bin/env python3
"""
Build a complete entity/field inventory from QSmartCare's EHI export samples.
Since the vendor provides no formal data dictionary, we reconstruct from:
  1. Sample JSON export
  2. Sample PDF export (has more sections than JSON)
"""

import json
import subprocess
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent / "downloads"
ANALYSIS = Path(__file__).resolve().parent

# ── 1. Parse JSON sample ──────────────────────────────────────────────
with open(DOWNLOADS / "sample-ehi-export.json") as f:
    raw_json = json.load(f)

obj = raw_json["object"]["organization"]

def extract_fields(data, prefix=""):
    fields = []
    if isinstance(data, dict):
        for k, v in data.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                fields.extend(extract_fields(v, path))
            elif isinstance(v, list):
                if v and isinstance(v[0], dict):
                    for sf in extract_fields(v[0], path + "[]"):
                        sf["is_array"] = True
                        fields.append(sf)
                else:
                    fields.append({"name": path, "sample_value": str(v), "type": "array", "is_array": True})
            else:
                fields.append({"name": path, "sample_value": str(v) if v is not None else None,
                               "type": type(v).__name__, "is_array": False})
    return fields

json_entities = []
for key, val in obj.items():
    if key == "resourceType":
        continue
    if isinstance(val, dict):
        rt = val.get("resourceType")
        flds = extract_fields(val)
    else:
        rt = None
        flds = [{"name": "value", "sample_value": str(val), "type": type(val).__name__, "is_array": False}]
    json_entities.append({
        "entity_name": key,
        "source": "JSON",
        "resourceType": rt,
        "fields": [{"name": f["name"], "type": f.get("type","string"), "sample_value": f.get("sample_value"),
                     "description": None, "is_array": f.get("is_array", False)} for f in flds]
    })

# ── 2. Manually define PDF sections with their fields ────────────────
# (From careful reading of the extracted PDF text)

pdf_sections = [
    {
        "entity_name": "Demographics",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "First Name"}, {"name": "Last Name"}, {"name": "Middle Name"},
            {"name": "Previous Name"}, {"name": "Suffix"}, {"name": "Sex"},
            {"name": "Dob"}, {"name": "Marital Status"}, {"name": "Pref Language"},
            {"name": "PCare Provider"}, {"name": "Race"}, {"name": "Ethnicity"},
            {"name": "Current Address"}, {"name": "Previous Address"}, {"name": "Ssn"},
            {"name": "Granular Race"}, {"name": "Phone"}, {"name": "Mobile"},
            {"name": "Email"}, {"name": "Fax"}, {"name": "City"}, {"name": "State"},
            {"name": "Address"}, {"name": "ZipCode"},
        ]
    },
    {
        "entity_name": "Organization",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Name"}, {"name": "Alias Name"}, {"name": "Phone No"},
            {"name": "Fax No"}, {"name": "Repository"},
        ]
    },
    {
        "entity_name": "Organization Address",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Street Address"}, {"name": "City"}, {"name": "State"},
            {"name": "Postal Code"}, {"name": "Country"}, {"name": "Website"},
        ]
    },
    {
        "entity_name": "Location",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Name"}, {"name": "Phone No"}, {"name": "Street Address"},
            {"name": "City"}, {"name": "State"}, {"name": "Postal Code"},
            {"name": "Country"},
        ]
    },
    {
        "entity_name": "Care Team",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "First Name"}, {"name": "Last Name"}, {"name": "Phone No"},
            {"name": "Role"},
        ]
    },
    {
        "entity_name": "Encounters",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Consult For"}, {"name": "Chief Complaints"}, {"name": "DOS"},
            {"name": "Smoking Status"},
        ]
    },
    {
        "entity_name": "History of Present Illness",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "History of Present Illness"},
        ]
    },
    {
        "entity_name": "Social History",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Social History"},
        ]
    },
    {
        "entity_name": "Family History",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Family History"},
        ]
    },
    {
        "entity_name": "Assessment and Plan of Treatment",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Assessment"}, {"name": "Plan Of Treatment"},
        ]
    },
    {
        "entity_name": "Patient Relationship",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Name"}, {"name": "Relationship"},
        ]
    },
    {
        "entity_name": "Insurance",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Primary Insurance"}, {"name": "Secondary Insurance"},
        ]
    },
    {
        "entity_name": "Spouse",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Name"}, {"name": "Occupation"}, {"name": "Workplace"},
            {"name": "Work Phone"}, {"name": "Organization Name"},
        ]
    },
    {
        "entity_name": "Past Medical History",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Diagnosis Code"}, {"name": "Diagnosis Name"},
            {"name": "Start Date"}, {"name": "End Date"}, {"name": "Status"},
        ]
    },
    {
        "entity_name": "Anticoagulant",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Anticoagulant Name"},
        ]
    },
    {
        "entity_name": "Patient Wound",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Wound number"}, {"name": "Wound DOS"}, {"name": "Wound Location"},
            {"name": "Wound Side"}, {"name": "Sub Location"}, {"name": "Vertical Plane"},
            {"name": "Horizontal Plane"}, {"name": "Status"},
        ]
    },
    {
        "entity_name": "Implantable Device",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Unique Device Identifiers"}, {"name": "Company Name"},
            {"name": "Brand Name"}, {"name": "Version/Model"}, {"name": "MRI Safety"},
            {"name": "Labeled Contains NRL"}, {"name": "GMDN PT Name"},
            {"name": "Manufactured Date"}, {"name": "Expiration Date"},
            {"name": "FDA Product Code"}, {"name": "FDA Product Name"}, {"name": "Status"},
        ]
    },
    {
        "entity_name": "Medications",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Medication Name"}, {"name": "Indication"}, {"name": "Dosage"},
            {"name": "Frequency"}, {"name": "Status"},
        ]
    },
    {
        "entity_name": "Diagnosis",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Diagnosis Code"}, {"name": "Diagnosis Name"},
            {"name": "Start Date"}, {"name": "End Date"}, {"name": "Status"},
        ]
    },
    {
        "entity_name": "Lab",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Path"}, {"name": "Lab Name"},
            {"name": "Lab Location"},
        ]
    },
    {
        "entity_name": "Blood Pressure",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Systolic"}, {"name": "Diastolic"},
        ]
    },
    {
        "entity_name": "Blood Sugar",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Fasting"}, {"name": "Random"}, {"name": "HbA1c"},
        ]
    },
    {
        "entity_name": "BMI",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Height"}, {"name": "Weight"}, {"name": "BMI"},
        ]
    },
    {
        "entity_name": "Pulse",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Pulse"},
        ]
    },
    {
        "entity_name": "Pulse Oximetry",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Pulse Oximetry"},
        ]
    },
    {
        "entity_name": "Body Temperature",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Temperature"},
        ]
    },
    {
        "entity_name": "Heart Rate",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Heart Rate"},
        ]
    },
    {
        "entity_name": "Respiratory Rate",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Respiratory Rate"},
        ]
    },
    {
        "entity_name": "Oxygen Concentration",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Date"}, {"name": "Oxygen Concentration"},
        ]
    },
    {
        "entity_name": "Past Surgical Histories",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Procedure Code"}, {"name": "Procedure Name"},
            {"name": "Start Date"}, {"name": "End Date"}, {"name": "OutCome"},
            {"name": "Status"},
        ]
    },
    {
        "entity_name": "Immunization",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Vaccine Code"}, {"name": "Code System"}, {"name": "Vaccine Name"},
            {"name": "Date"}, {"name": "Status"}, {"name": "Additional Notes"},
        ]
    },
    {
        "entity_name": "Functional Status",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Code"}, {"name": "Code System"}, {"name": "Name"}, {"name": "Date"},
        ]
    },
    {
        "entity_name": "Cognitive Status",
        "source": "PDF",
        "resourceType": None,
        "fields": [
            {"name": "Code"}, {"name": "Code System"}, {"name": "Name"}, {"name": "Date"},
        ]
    },
]

# Add default fields
for sec in pdf_sections:
    for f in sec["fields"]:
        f.setdefault("type", "string")
        f.setdefault("sample_value", None)
        f.setdefault("description", None)
        f.setdefault("is_array", False)

# ── 3. Merge JSON + PDF into unified inventory ───────────────────────
# Use PDF as authoritative for structure since it has more sections
# But note where JSON provides machine-readable equivalents

entities = []
for sec in pdf_sections:
    sec["field_count"] = len(sec["fields"])
    entities.append(sec)

# Note JSON-only sections (assessments has no PDF equivalent explicitly)
json_only = ["assessments"]
for jname in json_only:
    je = next((e for e in json_entities if e["entity_name"] == jname), None)
    if je:
        je["field_count"] = len(je["fields"])
        entities.append(je)

# ── 4. Write outputs ────────────────────────────────────────────────
with open(ANALYSIS / "entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

total_entities = len(entities)
total_fields = sum(len(e["fields"]) for e in entities)
fields_with_desc = sum(1 for e in entities for f in e["fields"] if f.get("description"))
fields_with_sample = sum(1 for e in entities for f in e["fields"] if f.get("sample_value"))

summary = {
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "pct_described": 0.0,
    "fields_with_sample_values": fields_with_sample,
    "pct_with_samples": round(fields_with_sample / total_fields * 100, 1) if total_fields else 0,
    "note": "No formal data dictionary exists. Fields reconstructed from sample PDF (33 sections) and JSON export.",
    "json_export_sections": [e["entity_name"] for e in json_entities],
    "pdf_export_sections": [e["entity_name"] for e in pdf_sections],
    "entity_summary": [
        {"name": e["entity_name"], "source": e["source"], "field_count": len(e["fields"])}
        for e in entities
    ]
}

with open(ANALYSIS / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total entities (sections): {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} (0%)")
print(f"Fields with sample values: {fields_with_sample}")
print()
for e in entities:
    print(f"  {e['entity_name']:40s} [{e['source']:4s}] {len(e['fields']):3d} fields")
