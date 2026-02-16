#!/usr/bin/env python3
"""
Builds full-entity-inventory.json and summary statistics from the
enrichment data-dictionary.json for PrognoCIS EHI export.

Input:  ../../results/bizmatics-inc--prognocis/downloads/enrichment/data-dictionary.json
Output: full-entity-inventory.json, summary-stats.json
"""

import json
import os

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..",
    "results", "bizmatics-inc--prognocis", "downloads"
)

dd_path = os.path.join(RESULTS_DIR, "enrichment", "data-dictionary.json")
with open(dd_path) as f:
    dd = json.load(f)

# Assign categories based on element number ranges from the PDF structure
def assign_category(elem):
    n = elem["number"]
    if 1 <= n <= 7:
        return "Reference / Provider Data"
    elif 8 <= n <= 37:
        return "Patient Clinical & Administrative Data"
    elif 38 <= n <= 42:
        return "Patient Case & Administrative Data"
    elif 43 <= n <= 47:
        return "Billing Data"
    return "Unknown"

# More granular domain mapping
def assign_domain(name):
    domain_map = {
        "Insurance Master": "Insurance / Coverage",
        "Medics": "Reference Data",
        "Referring Doctor": "Reference Data",
        "Adjusters": "Insurance / Coverage",
        "Attorneys": "Insurance / Coverage",
        "Employers": "Reference Data",
        "Guarantor": "Demographics",
        "Patient Demographics": "Demographics",
        "Patient Insurance": "Insurance / Coverage",
        "Vaccination": "Immunizations",
        "Health Maintenance": "Care Plans / Goals",
        "Family History": "Problems / Conditions",
        "Past Medical Hist": "Problems / Conditions",
        "Surgery": "Procedures",
        "Allergy": "Allergies",
        "Current Medication": "Medications / Prescriptions",
        "Social History": "Clinical Observations",
        "Legal Documents": "Clinical Notes / Documents",
        "Other Documents": "Clinical Notes / Documents",
        "Enc Attach Docs": "Clinical Notes / Documents",
        "Old Progress Notes": "Clinical Notes / Documents",
        "Messages": "Patient Communications",
        "Future Appointments": "Encounters / Visits",
        "Vitals": "Vitals",
        "Diagnosis Code": "Problems / Conditions",
        "CPT Codes": "Procedures",
        "HCPC Codes": "Procedures",
        "CCD": "Clinical Notes / Documents",
        "Prescriptions": "Medications / Prescriptions",
        "Lab Results": "Lab Results",
        "Rad Results": "Imaging / Diagnostic Reports",
        "Procedure Orders": "Orders / Referrals",
        "Consults": "Orders / Referrals",
        "Enc Progress Notes": "Encounters / Visits",
        "Procedure Notes": "Clinical Notes / Documents",
        "Letters": "Clinical Notes / Documents",
        "All Vitals": "Vitals",
        "Lab Test Result Values": "Lab Results",
        "Patient Cases": "Insurance / Coverage",
        "Patient Notes": "Clinical Notes / Documents",
        "Patient Alert": "Clinical Notes / Documents",
        "Past Appointments": "Encounters / Visits",
        "Billing Ledger": "Claims / Billing",
        "Billing Claims": "Claims / Billing",
        "Billing Charges": "Claims / Billing",
        "Patient Advance": "Payments",
        "Statements": "Claims / Billing",
    }
    return domain_map.get(name, "Unknown")

# Build full entity inventory
entities = []
for elem in dd["data_elements"]:
    fields = []
    for i, field_name in enumerate(elem["fields"]):
        fields.append({
            "index": i,
            "name": field_name.rstrip("."),
            "type": None,       # Not provided in source
            "description": None, # Not provided in source (only field names)
            "nullable": None,
            "max_length": None,
            "foreign_key": None,
            "value_set": None,
            "default": None,
            "example": None,
        })

    entities.append({
        "number": elem["number"],
        "name": elem["name"],
        "description": elem["description"],
        "vendor_category": assign_category(elem),
        "ehi_domain": assign_domain(elem["name"]),
        "field_count": len(elem["fields"]),
        "fields_with_descriptions": 0,  # Source has no per-field descriptions
        "fields_with_types": 0,          # Source has no type info
        "has_file_attachments": elem["hasFileColumn"],
        "file_example": elem.get("fileExample"),
        "notes": elem.get("notes", []),
        "fields": fields,
    })

inventory = {
    "source": "b-10-EHI-Export_PrognoCIS-Support.pdf",
    "product": "PrognoCIS",
    "version": "Denali 3.1",
    "extraction_date": "2026-02-16",
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities_with_field_lists": sum(1 for e in entities if e["field_count"] > 0),
    "entities_without_field_lists": sum(1 for e in entities if e["field_count"] == 0),
    "entities_with_file_attachments": sum(1 for e in entities if e["has_file_attachments"]),
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "entities": entities,
}

# Write full inventory
out_path = os.path.join(os.path.dirname(__file__), "full-entity-inventory.json")
with open(out_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Build summary statistics
by_category = {}
by_domain = {}
for e in entities:
    cat = e["vendor_category"]
    dom = e["ehi_domain"]
    by_category.setdefault(cat, {"entities": 0, "fields": 0, "names": []})
    by_category[cat]["entities"] += 1
    by_category[cat]["fields"] += e["field_count"]
    by_category[cat]["names"].append(e["name"])

    by_domain.setdefault(dom, {"entities": 0, "fields": 0, "names": []})
    by_domain[dom]["entities"] += 1
    by_domain[dom]["fields"] += e["field_count"]
    by_domain[dom]["names"].append(e["name"])

# Top entities by field count
top_entities = sorted(entities, key=lambda e: e["field_count"], reverse=True)[:15]

summary = {
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities_with_field_lists": sum(1 for e in entities if e["field_count"] > 0),
    "entities_without_field_lists": [e["name"] for e in entities if e["field_count"] == 0],
    "entities_with_file_attachments": sum(1 for e in entities if e["has_file_attachments"]),
    "by_vendor_category": by_category,
    "by_ehi_domain": by_domain,
    "top_15_by_field_count": [
        {"name": e["name"], "fields": e["field_count"], "category": e["vendor_category"]}
        for e in top_entities
    ],
}

summary_path = os.path.join(os.path.dirname(__file__), "summary-stats.json")
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Full inventory: {len(entities)} entities, {sum(e['field_count'] for e in entities)} fields")
print(f"Entities with field lists: {sum(1 for e in entities if e['field_count'] > 0)}")
print(f"Entities without field lists: {[e['name'] for e in entities if e['field_count'] == 0]}")
print(f"\nBy vendor category:")
for cat, info in sorted(by_category.items()):
    print(f"  {cat}: {info['entities']} entities, {info['fields']} fields")
print(f"\nTop 10 by field count:")
for e in top_entities[:10]:
    print(f"  {e['name']}: {e['field_count']} fields")
print(f"\nOutput: {out_path}")
print(f"Summary: {summary_path}")
