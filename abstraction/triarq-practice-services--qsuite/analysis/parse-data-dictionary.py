#!/usr/bin/env python3
"""
Parse raw EHI export data dictionary from ehiexportdocs-raw.json and resourceList-raw.json.
Produces entity-inventory-full.json and entity-inventory-summary.json.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")

# Load raw data
with open(os.path.join(DOWNLOADS, "ehiexportdocs-raw.json")) as f:
    fields_raw = json.load(f)

with open(os.path.join(DOWNLOADS, "resourceList-raw.json")) as f:
    resources_raw = json.load(f)

# Build resource lookup
resource_lookup = {r["module"]: r.get("description", "") for r in resources_raw}

# Group fields by module
modules = {}
for f in fields_raw:
    mod = f["module"]
    if mod not in modules:
        modules[mod] = []
    modules[mod].append({
        "name": f["field"],
        "type": f["type"],
        "description": f.get("description", ""),
        "raw_id": f["id"]
    })

# Build full inventory
entities = []
for mod_name, fields in sorted(modules.items()):
    # Determine if this module has a resource description
    res_desc = resource_lookup.get(mod_name, "")
    
    # Classify description quality per field
    fields_with_desc = 0
    fields_trivial_desc = 0
    for fld in fields:
        desc = fld["description"].strip()
        name = fld["name"].strip()
        # "trivial" = description is basically just the field name with spaces
        name_normalized = name.lower().replace("_", "").replace(" ", "")
        desc_normalized = desc.lower().replace("_", "").replace(" ", "")
        if not desc:
            pass
        elif desc_normalized == name_normalized:
            fields_trivial_desc += 1
            fields_with_desc += 1
        else:
            fields_with_desc += 1

    # Categorize entity
    billing_keywords = {"charges", "payments", "adjustment", "denials", "refunds", 
                        "reserves", "insurances", "eligibility", "guarantor",
                        "prior authorization", "patient cases"}
    clinical_keywords = {"allergy", "medication", "immunization", "vitals", "ob vitals",
                        "problems", "history", "medical devices"}
    admin_keywords = {"demographic", "appointments", "referrals", "pharmacy",
                     "patient alert", "patient-provider messages", "audit trail",
                     "other care teams", "primary care physician", "dms document"}
    
    mod_lower = mod_name.lower()
    if any(k in mod_lower for k in billing_keywords):
        category = "Billing & Financial"
    elif any(k in mod_lower for k in clinical_keywords):
        category = "Clinical"
    elif any(k in mod_lower for k in admin_keywords):
        category = "Administrative"
    else:
        category = "Other"

    entities.append({
        "entity": mod_name,
        "description": res_desc,
        "category": category,
        "field_count": len(fields),
        "fields_with_description": fields_with_desc,
        "fields_trivial_description": fields_trivial_desc,
        "fields": fields
    })

# Non-CSV export file types (from enrichment data-dictionary)
with open(os.path.join(DOWNLOADS, "enrichment", "data-dictionary.json")) as f:
    enrichment = json.load(f)

export_file_types = enrichment.get("exportFileTypes", [])

# Build full inventory
full_inventory = {
    "product": "QSuite (Manistee)",
    "developer": "TRIARQ Practice Services",
    "source": "https://ehi.myqone.com/",
    "extraction_date": "2026-02-16",
    "csv_entities": entities,
    "non_csv_exports": export_file_types,
    "totals": {
        "csv_entity_count": len(entities),
        "csv_field_count": sum(e["field_count"] for e in entities),
        "non_csv_format_count": len(export_file_types),
        "non_csv_document_types": sum(len(e.get("documentTypes", [])) for e in export_file_types)
    }
}

# Summary
type_counts = {}
for f in fields_raw:
    t = f["type"]
    type_counts[t] = type_counts.get(t, 0) + 1

# Description quality
total = len(fields_raw)
empty_desc = sum(1 for f in fields_raw if not f.get("description", "").strip())
trivial_desc = sum(1 for f in fields_raw 
                   if f.get("description", "").strip() and
                   f["description"].strip().lower().replace(" ", "") == 
                   f["field"].strip().lower().replace(" ", ""))
meaningful_desc = total - empty_desc - trivial_desc

category_summary = {}
for e in entities:
    cat = e["category"]
    if cat not in category_summary:
        category_summary[cat] = {"entity_count": 0, "field_count": 0}
    category_summary[cat]["entity_count"] += 1
    category_summary[cat]["field_count"] += e["field_count"]

summary = {
    "product": "QSuite (Manistee)",
    "csv_entities": len(entities),
    "csv_fields_total": total,
    "field_types": type_counts,
    "description_quality": {
        "total_fields": total,
        "fields_with_description": total - empty_desc,
        "fields_empty_description": empty_desc,
        "fields_trivial_description": trivial_desc,
        "fields_meaningful_description": meaningful_desc,
        "pct_with_any_description": round(100 * (total - empty_desc) / total, 1),
        "pct_meaningful_description": round(100 * meaningful_desc / total, 1)
    },
    "categories": category_summary,
    "entity_sizes": [{"entity": e["entity"], "fields": e["field_count"], "category": e["category"]} 
                     for e in sorted(entities, key=lambda x: -x["field_count"])],
    "non_csv_exports": {
        "formats": len(export_file_types),
        "total_document_types": sum(len(e.get("documentTypes", [])) for e in export_file_types),
        "breakdown": {e["format"]: len(e.get("documentTypes", [])) for e in export_file_types}
    }
}

# Write outputs
out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, "entity-inventory-full.json"), "w") as f:
    json.dump(full_inventory, f, indent=2)
    
with open(os.path.join(out_dir, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("Done.")
print(f"CSV entities: {len(entities)}")
print(f"CSV fields: {total}")
print(f"Description quality: {meaningful_desc}/{total} meaningful ({round(100*meaningful_desc/total,1)}%)")
print(f"Non-CSV exports: {len(export_file_types)} formats, {summary['non_csv_exports']['total_document_types']} document types")
print(f"\nBy category:")
for cat, info in sorted(category_summary.items()):
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
