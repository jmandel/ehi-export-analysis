#!/usr/bin/env python3
"""
Parse the GlaceEMR Export Data Dictionary from PDF text extraction
and the enrichment JSON to produce entity-inventory-full.json and
entity-inventory-summary.json.

Uses the enrichment JSON as the parsed source (verified against PDF text).
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENRICHMENT = os.path.join(BASE, "downloads", "enrichment", "data-dictionary.json")
OUTPUT_FULL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entity-inventory-full.json")
OUTPUT_SUMMARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entity-inventory-summary.json")

with open(ENRICHMENT) as f:
    data = json.load(f)

# Build full inventory
entities = []
total_fields = 0
fields_with_desc = 0
fields_with_type = 0
fields_with_comments = 0

for schema in data["file_schemas"]:
    folder = schema["folder"]
    filename = schema["filename"]
    contents_desc = schema.get("contents_description", "")
    columns = schema["columns"]
    
    fields = []
    for col in columns:
        name = col.get("name", "")
        dtype = col.get("data_type", "")
        desc = col.get("description", "")
        comments = col.get("comments", "")
        possible_values = col.get("possible_values", [])
        is_primary_key = col.get("is_primary_key", False)
        is_foreign_key = col.get("is_foreign_key", False)
        foreign_key_ref = col.get("foreign_key_reference", "")
        
        has_desc = bool(desc and desc.strip())
        has_type = bool(dtype and dtype.strip())
        has_comments = bool(comments and comments.strip())
        
        if has_desc:
            fields_with_desc += 1
        if has_type:
            fields_with_type += 1
        if has_comments:
            fields_with_comments += 1
        total_fields += 1
        
        field_obj = {
            "name": name,
            "data_type": dtype,
            "description": desc if desc else None,
            "comments": comments if comments else None,
            "possible_values": possible_values if possible_values else None,
            "is_primary_key": is_primary_key,
            "is_foreign_key": is_foreign_key,
            "foreign_key_reference": foreign_key_ref if foreign_key_ref else None
        }
        fields.append(field_obj)
    
    entity = {
        "entity_name": filename,
        "folder": folder,
        "description": contents_desc,
        "field_count": len(fields),
        "fields": fields
    }
    entities.append(entity)

# Compute per-entity stats
for entity in entities:
    desc_count = sum(1 for f in entity["fields"] if f["description"])
    entity["fields_with_description"] = desc_count
    entity["fields_with_type"] = sum(1 for f in entity["fields"] if f["data_type"])
    fk_count = sum(1 for f in entity["fields"] if f["is_foreign_key"])
    pk_count = sum(1 for f in entity["fields"] if f["is_primary_key"])
    entity["foreign_key_count"] = fk_count
    entity["primary_key_count"] = pk_count

full_inventory = {
    "source": "GlaceEMR Export Data Dictionary v1.0 (November 27, 2023)",
    "source_file": "downloads/GlaceEMR Export Data Dictionary.pdf",
    "parsed_from": "downloads/enrichment/data-dictionary.json (verified against PDF text)",
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_description": fields_with_desc,
    "fields_with_type": fields_with_type,
    "fields_with_comments": fields_with_comments,
    "entities": entities
}

with open(OUTPUT_FULL, "w") as f:
    json.dump(full_inventory, f, indent=2)

# Build summary
emr_entities = [e for e in entities if e["folder"] == "EMR"]
pms_entities = [e for e in entities if e["folder"] == "PMS"]

# Categorize
categories = {
    "EMR - Clinical Encounters": [],
    "EMR - Medical History": [],
    "EMR - Clinical Data": [],
    "EMR - Index Files": [],
    "PMS - Demographics & Insurance": [],
    "PMS - Billing & Payments": [],
    "PMS - Administrative": [],
    "PMS - Reference/Master Lists": [],
}

history_files = ["Past_Medical_History", "Surgical_History", "Family_History",
    "Family_Relations_History", "Social_History", "Substance_Abuse_History",
    "Contraception_Sexual_History", "Pregnancy_History", "Birthing_History",
    "Menstrual_History", "Occupational_History", "Obstetric_History", "Exposure_History"]

index_files = ["Patient_Photo_Index_File", "Clinical_Document_Index_File",
    "Phone_Messages_Index_File", "Scan_And_Attachments_Index_File", "CDA_Document_Index_File"]

clinical_data_files = ["Allergies", "Assesments", "Problem_List", "Medications",
    "InactiveMedications", "Investigation", "Preventive_Screenings", "Coumadin",
    "Vaccines", "Messages", "Reminders"]

encounter_files = ["Encounters", "Vitals"]

pms_demo_ins = ["Patient_Demographics", "Patient_Insurance"]
pms_billing = ["Patient_Account_Balance", "Transactions", "Payment_Receipts", "Payment_Posting"]
pms_admin = ["Appointments"]
pms_master = ["Master_Insurance_List", "Master_POS_List", "Master_Provider_List",
    "Master_Referring_Provider_List"]

for e in entities:
    basename = e["entity_name"].split("/")[-1].replace(".csv", "")
    if e["folder"] == "EMR":
        if basename in [h for h in history_files]:
            categories["EMR - Medical History"].append(e)
        elif basename in index_files:
            categories["EMR - Index Files"].append(e)
        elif basename in clinical_data_files:
            categories["EMR - Clinical Data"].append(e)
        elif basename in encounter_files:
            categories["EMR - Clinical Encounters"].append(e)
    else:
        if basename in pms_demo_ins:
            categories["PMS - Demographics & Insurance"].append(e)
        elif basename in pms_billing:
            categories["PMS - Billing & Payments"].append(e)
        elif basename in pms_admin:
            categories["PMS - Administrative"].append(e)
        elif basename in pms_master:
            categories["PMS - Reference/Master Lists"].append(e)

category_summary = {}
for cat, ents in categories.items():
    cat_fields = sum(e["field_count"] for e in ents)
    cat_desc = sum(e["fields_with_description"] for e in ents)
    category_summary[cat] = {
        "entity_count": len(ents),
        "total_fields": cat_fields,
        "fields_with_description": cat_desc,
        "entities": [{"name": e["entity_name"], "fields": e["field_count"],
                       "described": e["fields_with_description"]} for e in ents]
    }

# Top 15 largest entities
sorted_entities = sorted(entities, key=lambda x: x["field_count"], reverse=True)
top_entities = [{
    "name": e["entity_name"],
    "field_count": e["field_count"],
    "fields_with_description": e["fields_with_description"],
    "description": e["description"][:120] if e["description"] else None
} for e in sorted_entities[:15]]

summary = {
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_description": fields_with_desc,
    "fields_with_type": fields_with_type,
    "fields_with_comments": fields_with_comments,
    "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "emr_entities": len(emr_entities),
    "emr_fields": sum(e["field_count"] for e in emr_entities),
    "pms_entities": len(pms_entities),
    "pms_fields": sum(e["field_count"] for e in pms_entities),
    "categories": category_summary,
    "top_15_largest_entities": top_entities,
    "non_csv_content": [
        {"type": "Documents/Clinical Templates", "format": "HTML + PDF", "indexed_by": "EMR/Clinical_Document_Index_File.csv"},
        {"type": "Documents/Scanned Documents", "format": "PNG/JPEG/original", "indexed_by": "EMR/Scan_And_Attachments_Index_File.csv"},
        {"type": "Documents/C-CDA v2", "format": "XML", "indexed_by": "EMR/CDA_Document_Index_File.csv"},
        {"type": "Photos", "format": "JPG", "indexed_by": "EMR/Patient_Photo_Index_File.csv"},
        {"type": "Reference", "format": "Schema files", "indexed_by": None}
    ]
}

with open(OUTPUT_SUMMARY, "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total entities: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with description: {fields_with_desc} ({round(fields_with_desc/total_fields*100,1)}%)")
print(f"Fields with type: {fields_with_type} ({round(fields_with_type/total_fields*100,1)}%)")
print(f"Fields with comments: {fields_with_comments} ({round(fields_with_comments/total_fields*100,1)}%)")
print(f"\nEMR: {len(emr_entities)} entities, {sum(e['field_count'] for e in emr_entities)} fields")
print(f"PMS: {len(pms_entities)} entities, {sum(e['field_count'] for e in pms_entities)} fields")
print(f"\nCategories:")
for cat, info in category_summary.items():
    print(f"  {cat}: {info['entity_count']} entities, {info['total_fields']} fields, {info['fields_with_description']} described")
print(f"\nTop 10 largest entities:")
for e in top_entities[:10]:
    print(f"  {e['name']}: {e['field_count']} fields ({e['fields_with_description']} described)")
print(f"\nWrote {OUTPUT_FULL}")
print(f"Wrote {OUTPUT_SUMMARY}")
