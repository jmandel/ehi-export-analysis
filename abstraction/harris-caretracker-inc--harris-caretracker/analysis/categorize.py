#!/usr/bin/env python3
"""Categorize data classes and produce domain coverage mapping."""

import json

with open("full-entity-inventory.json") as f:
    data = json.load(f)

# Assign categories to each data class
categories = {
    "Addendum": "Clinical Documentation",
    "Advance Directives": "Clinical Documentation",
    "Alerts": "Clinical Documentation",
    "Allergies and Intolerances Pending": "Clinical",
    "Allergies and Intolerances": "Clinical",
    "Assesments": "Clinical Documentation",
    "Billing History": "Billing",
    "Care Team Members": "Care Coordination",
    "Clinical Notes": "Clinical Documentation",
    "Demographic Immunization": "Immunizations",
    "Email": "Communications",
    "FamilyHistory": "Clinical",
    "FunctionalStatus": "Clinical",
    "Goals": "Care Planning",
    "Health Concerns": "Care Planning",
    "Health Insurance": "Insurance",
    "HM Rules Ignored": "Health Maintenance",
    "HM Rules": "Health Maintenance",
    "Immunizations": "Immunizations",
    "Implantable device": "Clinical",
    "Imported Items": "Documents",
    "Injections": "Clinical",
    "Lab Tests": "Lab Results",
    "List Problem Pending": "Clinical",
    "List Problem": "Clinical",
    "Medications Pending": "Medications",
    "Medications": "Medications",
    "Next Of Kin": "Demographics",
    "Occupation and Industry History": "Demographics",
    "Orders": "Orders",
    "Patient Demographics": "Demographics",
    "Patient Generated Data": "Patient Data",
    "Patient Health Information Capture": "Clinical Documentation",
    "Patient Record Release": "Administrative",
    "Plan of Treatment": "Care Planning",
    "Procedures": "Billing",
    "Referrals": "Orders",
    "Risk Factors": "Clinical",
    "Scheduling": "Administrative",
    "Smoking Statuses": "Clinical",
    "Tracked Data": "Clinical",
    "Travel History": "Public Health",
    "User Defined Fields": "Custom Data",
    "Vital Signs": "Clinical",
}

# Add category to each data class
for dc in data["data_classes"]:
    dc["category"] = categories.get(dc["name"], "Uncategorized")

# Category summary
cat_summary = {}
for dc in data["data_classes"]:
    cat = dc["category"]
    if cat not in cat_summary:
        cat_summary[cat] = {"count": 0, "fields": 0, "classes": []}
    cat_summary[cat]["count"] += 1
    cat_summary[cat]["fields"] += dc["field_count"]
    cat_summary[cat]["classes"].append(dc["name"])

print("Category Summary")
print("=" * 70)
print(f"{'Category':<30} {'Data Classes':>12} {'Total Fields':>12}")
print("-" * 70)
for cat in sorted(cat_summary.keys()):
    s = cat_summary[cat]
    print(f"{cat:<30} {s['count']:>12} {s['fields']:>12}")
    for cls in s["classes"]:
        fc = next(dc["field_count"] for dc in data["data_classes"] if dc["name"] == cls)
        print(f"  - {cls} ({fc} fields)")
print("-" * 70)
total_classes = sum(s["count"] for s in cat_summary.values())
total_fields = sum(s["fields"] for s in cat_summary.values())
print(f"{'TOTAL':<30} {total_classes:>12} {total_fields:>12}")

# Save updated inventory
with open("full-entity-inventory.json", "w") as f:
    json.dump(data, f, indent=2)

# Save category summary
with open("category-summary.json", "w") as f:
    json.dump(cat_summary, f, indent=2)

print("\nSaved category-summary.json")
