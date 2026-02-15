#!/usr/bin/env python3
"""Parse Schema.pdf text extraction to produce accurate table/column counts and inventory."""

import json
import re
from collections import defaultdict

schema_file = "schema-text.txt"
rows = []

with open(schema_file) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("TABLE_NAME"):
            continue
        parts = line.split()
        if len(parts) >= 3:
            table = parts[0]
            col = parts[1]
            dtype = parts[2]
            rows.append({"table": table, "column": col, "data_type": dtype})

# Build table -> columns mapping
tables = defaultdict(list)
for r in rows:
    tables[r["table"]].append({"column": r["column"], "data_type": r["data_type"]})

# Summary stats
total_tables = len(tables)
total_columns = sum(len(cols) for cols in tables.values())

print(f"Total tables: {total_tables}")
print(f"Total columns: {total_columns}")
print()

# Data types distribution
dtype_counts = defaultdict(int)
for r in rows:
    dtype_counts[r["data_type"]] += 1
print("Data type distribution:")
for dt, count in sorted(dtype_counts.items(), key=lambda x: -x[1]):
    print(f"  {dt}: {count}")
print()

# Table sizes
print("Tables by column count (descending):")
table_sizes = [(t, len(cols)) for t, cols in tables.items()]
table_sizes.sort(key=lambda x: -x[1])
for t, c in table_sizes:
    print(f"  {t}: {c} columns")
print()

# Categorize tables based on naming patterns and content
categories = {
    "Patient Demographics & Registration": [],
    "Clinical Data": [],
    "Medications": [],
    "Lab & Diagnostics": [],
    "Immunizations": [],
    "Dental": [],
    "Behavioral Health": [],
    "Pregnancy / Perinatal": [],
    "Billing & Financial": [],
    "Insurance": [],
    "Visits & Scheduling": [],
    "Documents & Imaging": [],
    "Communications": [],
    "Referrals & Care Coordination": [],
    "Administrative": [],
    "Financial Assistance": [],
    "Regulatory / Reporting": [],
    "Other": [],
}

def categorize(table_name):
    t = table_name.lower()
    if t in ("mpatient", "mpatientadditional", "mpatientregistration", "mpatientdescriptor",
             "mpatientemployment", "mpatientethnic", "mpatientrace", "mpatientfamilymember",
             "mpatientotherinformation", "mpatientpreference", "mpatientrepresentative",
             "mpatientportal", "mpatientupi", "mchart", "mpatientchartinformation"):
        return "Patient Demographics & Registration"
    elif t in ("texam", "texamhistory", "texamsurvey", "tpatientallergy", "tpatientmedicalcondition",
               "tpatientproblemlist", "tpatientclinicalinfo", "tpatienthealthmeasure",
               "mpatienthealthmeasure", "tpatientexternalhealthmeasure", "mscbaselinepatientvalue",
               "mscpatient", "tpatientworksheet", "tassessmentscore", "tpatienteducationlist",
               "tpatientclinicalmeasuredw", "tpatientform"):
        return "Clinical Data"
    elif "medication" in t or "medicine" in t or t == "trefill":
        return "Medications"
    elif "lab" in t and "label" not in t:
        return "Lab & Diagnostics"
    elif "immunization" in t:
        return "Immunizations"
    elif "dental" in t or "tooth" in t or t == "tcbeexam":
        return "Dental"
    elif "treatment" in t and "bh" in t:
        return "Behavioral Health"
    elif t == "tpatienttreatmentplan":
        return "Behavioral Health"
    elif "pregnancy" in t or "cpsp" in t:
        return "Pregnancy / Perinatal"
    elif any(w in t for w in ("billing", "hcfa", "arreceipt", "arclose", "printstatement", "purchaseorder")):
        return "Billing & Financial"
    elif "insurance" in t or "payer" in t:
        return "Insurance"
    elif t in ("tvisit", "tvisitchdp", "tevent"):
        return "Visits & Scheduling"
    elif t in ("mscandocument", "msignature"):
        return "Documents & Imaging"
    elif any(w in t for w in ("email", "sms", "fax")) and "patient" in t or t in ("temailmessage", "tsmsmessage", "tpatientfax"):
        return "Communications"
    elif "referral" in t or "case" in t:
        return "Referrals & Care Coordination"
    elif t in ("tcallqueueitem", "ttaskitem", "tpatientcontactactivity", "tpatientdisclosure",
               "mpatientreleaseauthorization", "tpatientlog", "tpatientprintobject",
               "tvideosession", "tvideosessionparticipant", "tpatientauditlog"):
        return "Administrative"
    elif t in ("mpatientneedymed", "mpatientcdp"):
        return "Financial Assistance"
    elif "oshpd" in t or "uds" in t:
        return "Regulatory / Reporting"
    elif t in ("mpatientappttypefee",):
        return "Other"
    elif t in ("mpatientnote", "tpatienttickle"):
        return "Other"
    elif t == "mpatientprogram":
        return "Other"
    else:
        return "Other"

for table_name in tables:
    cat = categorize(table_name)
    categories[cat].append(table_name)

print("Category breakdown:")
cat_stats = []
for cat, tbls in categories.items():
    if not tbls:
        continue
    field_count = sum(len(tables[t]) for t in tbls)
    cat_stats.append({
        "category": cat,
        "table_count": len(tbls),
        "field_count": field_count,
        "tables": sorted(tbls)
    })
    print(f"  {cat}: {len(tbls)} tables, {field_count} fields")
    for t in sorted(tbls):
        print(f"    - {t} ({len(tables[t])} columns)")

# Check for fields with descriptions (there are none - only name + type)
# Count self-explanatory vs cryptic fields
explanatory_keywords = {"id", "name", "date", "phone", "email", "address", "city", "state", "zip",
                       "first", "last", "middle", "gender", "dob", "ssn", "notes", "comment",
                       "description", "code", "type", "status", "active", "deleted", "created", "updated"}

cryptic_count = 0
clear_count = 0
for r in rows:
    col_lower = r["column"].lower()
    if any(kw in col_lower for kw in explanatory_keywords):
        clear_count += 1
    else:
        cryptic_count += 1

print(f"\nField clarity (heuristic):")
print(f"  Self-explanatory names: {clear_count} ({100*clear_count//total_columns}%)")
print(f"  Less obvious names: {cryptic_count} ({100*cryptic_count//total_columns}%)")
print(f"  Fields with descriptions: 0 (0%) — schema has names and types only")

# Save full inventory as JSON
inventory = []
for table_name in sorted(tables.keys()):
    cat = categorize(table_name)
    cols = tables[table_name]
    inventory.append({
        "table": table_name,
        "category": cat,
        "column_count": len(cols),
        "columns": [{"name": c["column"], "data_type": c["data_type"]} for c in cols]
    })

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Save category summary
with open("category-summary.json", "w") as f:
    json.dump(cat_stats, f, indent=2)

print(f"\nSaved full-entity-inventory.json and category-summary.json")
