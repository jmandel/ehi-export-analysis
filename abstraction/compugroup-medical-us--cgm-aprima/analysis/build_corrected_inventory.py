#!/usr/bin/env python3
"""
Create corrected full-entity-inventory.json by starting from the enrichment JSON
and applying corrections identified by comparing against the raw PDF text.

Corrections needed (enrichment dropped fields at page breaks or where names 
conflicted with section keywords):
1. Audit Trail: +1 field (Description char(2000))
2. Appointment Information: +1 field (Appointment Type Code char(25))
3. Patient Demographics: +1 field (Primary Care Provider ID char(50))
4. Patient Insurance: +1 field (Primary Insurance Name char(200))
5. Responsible Party: +1 field (Relationship Description char(50))
6. Eligibility: +2 fields (Payer Name char(100), OutNetwork Deductible money)
   Also fix: Authorize Assignment description was wrong
7. Patient Ledger: +2 fields (whoPaid char(100), lastInsurancePaymentAmount money)
   Also fix: glDate description was wrong
8. Patient Referrals: +1 field (Medical Service Provider char(200))
"""

import json
from pathlib import Path
from copy import deepcopy

ENRICHMENT_JSON = Path("/home/jmandel/hobby/ehi-export-analysis/results/compugroup-medical-us--cgm-aprima/downloads/enrichment/ehi-data-dictionary.json")
OUTPUT_DIR = Path(__file__).parent

with open(ENRICHMENT_JSON) as f:
    data = json.load(f)

DOMAIN_MAP = {
    "Audit Trail": "Administrative",
    "Contacts": "Demographics",
    "Active Medication": "Clinical",
    "Allergies": "Clinical",
    "Appointment Information": "Administrative",
    "Family History": "Clinical",
    "Immunization": "Clinical",
    "Medical History": "Clinical",
    "Patient Demographics": "Demographics",
    "Patient Insurance": "Insurance / Coverage",
    "Problem List": "Clinical",
    "Responsible Party": "Demographics",
    "Results": "Clinical",
    "Social History": "Clinical",
    "Visit Comments": "Clinical",
    "Vitals": "Clinical",
    "Eligibility": "Insurance / Coverage",
    "Employment": "Demographics",
    "Patient Ledger": "Billing / Financial",
    "Patient Referrals": "Clinical",
    "Providers": "Clinical",
    "Response Report": "Clinical Decision Support",
}

def make_field(name, dtype, desc):
    return {"column_heading": name, "data_type": dtype, "description": desc}

corrections_applied = []

for csv_file in data["csv_files"]:
    name = csv_file["name"]
    fields = csv_file["fields"]
    
    if name == "Audit Trail":
        # Insert "Description" field before "Type"
        type_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "Type")
        fields.insert(type_idx, make_field("Description", "char(2000)", "Description of the change made."))
        corrections_applied.append(f"{name}: added 'Description' field (was dropped because name matched section keyword)")
    
    elif name == "Appointment Information":
        # Insert "Appointment Type Code" before "Appointment Type Description"
        desc_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "Appointment Type Description")
        fields.insert(desc_idx, make_field("Appointment Type Code", "char(25)", "Appointment type identifier."))
        corrections_applied.append(f"{name}: added 'Appointment Type Code' field (was merged with Appointment Type Description)")
    
    elif name == "Patient Demographics":
        # Add "Primary Care Provider ID" at the end
        fields.append(make_field("Primary Care Provider ID", "char(50)", "Medical provider identifier."))
        corrections_applied.append(f"{name}: added 'Primary Care Provider ID' field (was on page boundary)")
    
    elif name == "Patient Insurance":
        # Insert "Primary Insurance Name" before "Primary Member ID"
        member_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "Primary Member ID")
        fields.insert(member_idx, make_field("Primary Insurance Name", "char(200)", "Patient insurance name."))
        corrections_applied.append(f"{name}: added 'Primary Insurance Name' field (was merged with next field)")
    
    elif name == "Responsible Party":
        # Insert "Relationship Description" after "Relationship Code"
        code_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "Relationship Code")
        fields.insert(code_idx + 1, make_field("Relationship Description", "char(50)", "Relationship description."))
        corrections_applied.append(f"{name}: added 'Relationship Description' field (was merged with Relationship Code)")
    
    elif name == "Eligibility":
        # Fix "Authorize Assignment" description (was wrong - contained "Payer Name")
        auth_field = next(f for f in fields if f["column_heading"] == "Authorize Assignment")
        auth_field["description"] = ""
        corrections_applied.append(f"{name}: fixed 'Authorize Assignment' description (was erroneously 'Payer Name')")
        
        # Insert "Payer Name" after "Authorize Assignment"
        auth_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "Authorize Assignment")
        fields.insert(auth_idx + 1, make_field("Payer Name", "char(100)", "Insurance carrier name."))
        corrections_applied.append(f"{name}: added 'Payer Name' field (was absorbed as description of previous field)")
        
        # Insert "OutNetwork Deductible" after "InNetwork Deductible"
        in_deduct_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "InNetwork Deductible")
        fields.insert(in_deduct_idx + 1, make_field("OutNetwork Deductible", "money", "Out of network deductible amount."))
        corrections_applied.append(f"{name}: added 'OutNetwork Deductible' field (was on line with merged type/desc)")
    
    elif name == "Patient Ledger":
        # Fix "glDate" description (was wrong - contained "whoPaid")
        gl_field = next(f for f in fields if f["column_heading"] == "glDate")
        gl_field["description"] = ""
        corrections_applied.append(f"{name}: fixed 'glDate' description (was erroneously 'whoPaid')")
        
        # Insert "whoPaid" after "glDate"
        gl_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "glDate")
        fields.insert(gl_idx + 1, make_field("whoPaid", "char(100)", "Superbill payer."))
        corrections_applied.append(f"{name}: added 'whoPaid' field (was absorbed as description of previous field)")
        
        # Insert "lastInsurancePaymentAmount" after "lastPatientPaymentAmount"
        lpp_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "lastPatientPaymentAmount")
        fields.insert(lpp_idx + 1, make_field("lastInsurancePaymentAmount", "money", "Amount of last insurance payment."))
        corrections_applied.append(f"{name}: added 'lastInsurancePaymentAmount' field (was on page boundary)")
    
    elif name == "Patient Referrals":
        # Insert "Medical Service Provider" after "Provider"
        prov_idx = next(i for i, f in enumerate(fields) if f["column_heading"] == "Provider")
        fields.insert(prov_idx + 1, make_field("Medical Service Provider", "char(200)", "Referring provider name."))
        corrections_applied.append(f"{name}: added 'Medical Service Provider' field (was merged with Provider)")

# Build corrected inventory
entities = []
total_fields = 0
fields_with_descriptions = 0
fields_with_types = 0

for csv_file in data["csv_files"]:
    name = csv_file["name"]
    category = DOMAIN_MAP.get(name, "Unknown")
    fields = []
    
    for field in csv_file["fields"]:
        col_name = field.get("column_heading", "")
        data_type = field.get("data_type", "")
        description = field.get("description", "")
        
        has_desc = bool(description and description.strip())
        has_type = bool(data_type and data_type.strip())
        
        total_fields += 1
        if has_desc:
            fields_with_descriptions += 1
        if has_type:
            fields_with_types += 1
        
        fields.append({
            "name": col_name,
            "type": data_type,
            "description": description,
            "has_description": has_desc,
            "has_type": has_type,
        })
    
    entities.append({
        "entity_name": name,
        "file_name": csv_file.get("file_name", ""),
        "entity_description": csv_file.get("description", ""),
        "category": category,
        "field_count": len(fields),
        "fields": fields,
    })

inventory = {
    "source": "cgm-aprima-electronic-health-information-export-user-guide.pdf",
    "extraction_method": "Enrichment JSON with manual corrections verified against raw PDF text",
    "corrections_applied": corrections_applied,
    "product": "CGM APRIMA",
    "export_format": "CSV files in ZIP archive (plus USCDI XML, Complete Patient Chart PDF, images)",
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_without_descriptions": total_fields - fields_with_descriptions,
    "fields_with_types": fields_with_types,
    "description_coverage_pct": round(fields_with_descriptions / total_fields * 100, 1) if total_fields else 0,
    "type_coverage_pct": round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
    "entities": entities,
}

with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Category breakdown
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
    categories[cat]["entity_count"] += 1
    categories[cat]["field_count"] += e["field_count"]
    categories[cat]["entities"].append({"name": e["entity_name"], "fields": e["field_count"]})

with open(OUTPUT_DIR / "category-breakdown.json", "w") as f:
    json.dump(categories, f, indent=2)

# Print summary
print(f"Total CSV files: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_descriptions} ({inventory['description_coverage_pct']}%)")
print(f"Fields without descriptions: {total_fields - fields_with_descriptions}")
print(f"Fields with types: {fields_with_types} ({inventory['type_coverage_pct']}%)")
print()
print("Corrections applied:")
for c in corrections_applied:
    print(f"  - {c}")
print()
print("Category breakdown:")
for cat, info in sorted(categories.items()):
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    for e in info["entities"]:
        print(f"    - {e['name']} ({e['fields']} fields)")
print()
print("Entities by size (descending):")
for e in sorted(entities, key=lambda x: x["field_count"], reverse=True):
    print(f"  {e['entity_name']}: {e['field_count']} fields ({e['category']})")
print()
print("Fields without descriptions:")
for e in entities:
    for f in e["fields"]:
        if not f["has_description"]:
            print(f"  {e['entity_name']}.{f['name']}")
