#!/usr/bin/env python3
"""
Parse the pre-extracted data-dictionary.json and produce:
1. full-entity-inventory.json - complete machine-readable inventory
2. summary-stats.json - aggregate statistics for analysis.md
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

DATA_DICT = Path("/home/jmandel/hobby/ehi-export-analysis/results/modernizing-medicine-gastroenterology-llc--ggastro/downloads/enrichment/data-dictionary.json")
OUT_DIR = Path(__file__).parent

with open(DATA_DICT) as f:
    dd = json.load(f)

tables = dd["tables"]
relationships = dd["relationships"]
translations = dd["translations"]
glossary = dd["glossary"]

# --- Domain classification ---
# Map table name prefixes to human-readable domains
DOMAIN_RULES = [
    ("Billing", "Billing & Claims"),
    ("Insurance", "Billing & Claims"),
    ("Eligibility", "Billing & Claims"),
    ("Guarantor", "Billing & Claims"),
    ("CreditCard", "Billing & Claims"),
    ("NdcIdLog", "Billing & Claims"),
    ("CodingAdvisor", "Billing & Claims"),
    ("CodingTool", "Billing & Claims"),
    ("Mips", "Quality Reporting"),
    ("Finding", "Endoscopy / Procedures"),
    ("Intervention", "Endoscopy / Procedures"),
    ("Procedure", "Endoscopy / Procedures"),
    ("Aldrete", "Endoscopy / Procedures"),
    ("Anesthesia", "Endoscopy / Procedures"),
    ("Asc", "Endoscopy / Procedures"),
    ("Aga", "Endoscopy / Procedures"),
    ("Giquic", "Endoscopy / Procedures"),
    ("Limitation", "Endoscopy / Procedures"),
    ("Npo", "Endoscopy / Procedures"),
    ("Oxygen", "Endoscopy / Procedures"),
    ("Pain", "Endoscopy / Procedures"),
    ("Preparation", "Endoscopy / Procedures"),
    ("Nursing", "Endoscopy / Procedures"),
    ("Instrument", "Endoscopy / Procedures"),
    ("Infusion", "Endoscopy / Procedures"),
    ("Iv", "Endoscopy / Procedures"),
    ("Discharge", "Endoscopy / Procedures"),
    ("Administered", "Endoscopy / Procedures"),
    ("Addendum", "Endoscopy / Procedures"),
    ("Blood", "Endoscopy / Procedures"),
    ("PhysicianStanding", "Endoscopy / Procedures"),
    ("Cardiology", "Endoscopy / Procedures"),
    ("Carotid", "Endoscopy / Procedures"),
    ("Nuclear", "Endoscopy / Procedures"),
    ("Stress", "Endoscopy / Procedures"),
    ("Heart", "Endoscopy / Procedures"),
    ("Tte", "Endoscopy / Procedures"),
    ("Service", "Encounters / Services"),
    ("Appointment", "Scheduling"),
    ("Recall", "Scheduling"),
    ("Pending", "Scheduling"),
    ("Inbound", "Scheduling"),
    ("LocationsPerAppointment", "Scheduling"),
    ("Resource", "Scheduling"),
    ("Rounding", "Scheduling"),
    ("Patient", "Patient / Demographics"),
    ("Person", "Patient / Demographics"),
    ("Relative", "Patient / Demographics"),
    ("EmergencyContact", "Patient / Demographics"),
    ("Employment", "Patient / Demographics"),
    ("SupportPerson", "Patient / Demographics"),
    ("Phone", "Patient / Demographics"),
    ("UsaAddress", "Patient / Demographics"),
    ("Email", "Patient / Demographics"),
    ("Medication", "Medications"),
    ("Prescription", "Medications"),
    ("Renewal", "Medications"),
    ("Pharmacy", "Medications"),
    ("EligibilityFormulary", "Medications"),
    ("Order", "Orders / Referrals"),
    ("External", "Orders / Referrals"),
    ("Imaging", "Imaging / Documents"),
    ("Chart", "Imaging / Documents"),
    ("Document", "Imaging / Documents"),
    ("DocRetrieve", "Imaging / Documents"),
    ("General", "Imaging / Documents"),
    ("Interface", "Lab Interfaces"),
    ("Vital", "Vitals"),
    ("Physical", "Vitals"),
    ("Functional", "Clinical Assessments"),
    ("Extra", "Clinical Assessments"),
    ("Guideline", "Clinical Assessments"),
    ("Impression", "Clinical Assessments"),
    ("MedicalHistory", "Clinical Assessments"),
    ("Pif", "Clinical Assessments"),
    ("Questionnaire", "Clinical Assessments"),
    ("Direct", "Messaging / Communications"),
    ("Fax", "Messaging / Communications"),
    ("Letter", "Messaging / Communications"),
    ("Task", "Messaging / Communications"),
    ("Telehealth", "Telehealth"),
    ("Portal", "Patient Portal"),
    ("Balance", "Patient Portal"),
    ("BulkAction", "Administrative"),
    ("Export", "Administrative"),
    ("Hl7", "Administrative"),
    ("Ldm", "Administrative"),
    ("Syndromic", "Administrative"),
    ("User", "Administrative"),
    ("Activity", "Administrative"),
    ("Cvx", "Immunizations"),
    ("Referr", "Orders / Referrals"),
    ("Provider", "Patient / Demographics"),
    ("ReportCustom", "Quality Reporting"),
]

def classify_table(name):
    for prefix, domain in DOMAIN_RULES:
        if name.startswith(prefix):
            return domain
    return "Other"

# Build inventory
inventory = []
for t in tables:
    fields_detail = []
    for f in t.get("fields", []):
        fields_detail.append({
            "index": f["index"],
            "name": f["name"],
            "type": f.get("type", ""),
            "length": f.get("length"),
            "format_or_translation": f.get("format_or_translation"),
        })
    
    domain = classify_table(t["name"])
    inventory.append({
        "table": t["name"],
        "domain": domain,
        "field_count": len(fields_detail),
        "fields": fields_detail,
    })

# Save full inventory
with open(OUT_DIR / "full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# --- Summary statistics ---
domain_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "table_names": []})
for item in inventory:
    d = item["domain"]
    domain_stats[d]["tables"] += 1
    domain_stats[d]["fields"] += item["field_count"]
    domain_stats[d]["table_names"].append(item["table"])

# Field type distribution
type_counts = Counter()
fields_with_type = 0
fields_with_length = 0
fields_with_format = 0
for t in tables:
    for f in t.get("fields", []):
        tp = f.get("type", "")
        if tp:
            type_counts[tp] += 1
            fields_with_type += 1
        if f.get("length"):
            fields_with_length += 1
        if f.get("format_or_translation"):
            fields_with_format += 1

# Translation stats
total_translation_entries = sum(len(t.get("entries", [])) for t in translations)

summary = {
    "total_tables": len(tables),
    "total_fields": sum(len(t.get("fields", [])) for t in tables),
    "total_relationships": len(relationships),
    "total_translation_tables": len(translations),
    "total_translation_entries": total_translation_entries,
    "glossary_terms": len(glossary),
    "fields_with_type": fields_with_type,
    "fields_with_length": fields_with_length,
    "fields_with_format_or_translation": fields_with_format,
    "fields_with_description": 0,  # No descriptions in this data dictionary
    "type_distribution": dict(type_counts.most_common()),
    "domain_breakdown": {
        d: {"tables": s["tables"], "fields": s["fields"]}
        for d, s in sorted(domain_stats.items(), key=lambda x: -x[1]["fields"])
    },
    "domain_breakdown_with_tables": {
        d: {"tables": s["tables"], "fields": s["fields"], "table_names": s["table_names"]}
        for d, s in sorted(domain_stats.items(), key=lambda x: -x[1]["fields"])
    },
    "top_20_tables": [
        {"table": item["table"], "fields": item["field_count"], "domain": item["domain"]}
        for item in sorted(inventory, key=lambda x: -x["field_count"])[:20]
    ],
}

with open(OUT_DIR / "summary-stats.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print key stats
print(f"Total tables: {summary['total_tables']}")
print(f"Total fields: {summary['total_fields']}")
print(f"Fields with type: {summary['fields_with_type']}")
print(f"Fields with length: {summary['fields_with_length']}")
print(f"Fields with format/translation: {summary['fields_with_format_or_translation']}")
print(f"Fields with description: {summary['fields_with_description']}")
print(f"Relationships: {summary['total_relationships']}")
print(f"Translation tables: {summary['total_translation_tables']}")
print()
print("Domain breakdown:")
for d, s in sorted(summary["domain_breakdown"].items(), key=lambda x: -x[1]["fields"]):
    print(f"  {d}: {s['tables']} tables, {s['fields']} fields")
