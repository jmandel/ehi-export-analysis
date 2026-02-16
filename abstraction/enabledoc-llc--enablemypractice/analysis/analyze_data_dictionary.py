#!/usr/bin/env python3
"""
Parse the enrichment data-dictionary.json and produce:
1. full-entity-inventory.json — complete machine-readable extraction
2. summary-stats.json — aggregate statistics
3. Print summary to stdout for inclusion in analysis.md
"""
import json
import sys
from pathlib import Path

ENRICHMENT = Path(__file__).resolve().parent.parent.parent.parent / "results/enabledoc-llc--enablemypractice/downloads/enrichment/data-dictionary.json"
OUT_DIR = Path(__file__).resolve().parent

with open(ENRICHMENT) as f:
    data = json.load(f)

entities = data["excelEntities"]
value_sets = data["valueSets"]
export_formats = data["exportFormats"]
excel_tabs = data["excelTabNames"]

# Build full entity inventory
inventory = []
total_fields = 0
total_described = 0
total_typed = 0
total_required = 0
total_preferred = 0
total_optional = 0

for entity in entities:
    fields = entity.get("fields", [])
    field_list = []
    for f in fields:
        desc = f.get("description", "").strip()
        dtype = f.get("dataType", "").strip()
        req = f.get("requirement", "").strip()
        
        req_val = f.get("required", "").strip()
        
        field_obj = {
            "name": f.get("name", ""),
            "description": desc if desc else None,
            "dataType": dtype if dtype and dtype != "unknown" else None,
            "requirement": req_val if req_val else None,
            "valueSet": f.get("valueSet") if f.get("valueSet") else None,
            "referenceSection": f.get("referenceSection") if f.get("referenceSection") else None,
        }
        field_list.append(field_obj)
        
        total_fields += 1
        if desc:
            total_described += 1
        if dtype and dtype != "unknown":
            total_typed += 1
        if req_val:
            r = req_val.lower()
            if r == "required":
                total_required += 1
            elif r == "preferred":
                total_preferred += 1
            elif r == "optional":
                total_optional += 1

    entity_obj = {
        "name": entity["name"],
        "fieldCount": len(fields),
        "fieldsWithDescriptions": sum(1 for f in fields if f.get("description", "").strip()),
        "fieldsWithTypes": sum(1 for f in fields if f.get("dataType", "").strip() and f.get("dataType", "") != "unknown"),
        "fields": field_list,
    }
    inventory.append(entity_obj)

# Value sets
vs_inventory = []
total_vs_values = 0
for vs in value_sets:
    vals = vs.get("values", [])
    total_vs_values += len(vals)
    vs_inventory.append({
        "name": vs["name"],
        "valueCount": len(vals),
        "values": vals,
    })

# Full inventory
full_inventory = {
    "source": "Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf",
    "exportFormats": [fmt.get("name", "") for fmt in export_formats],
    "excelTabNames": excel_tabs,
    "entityCount": len(inventory),
    "totalFields": total_fields,
    "totalFieldsWithDescriptions": total_described,
    "totalFieldsWithTypes": total_typed,
    "fieldRequirements": {
        "required": total_required,
        "preferred": total_preferred,
        "optional": total_optional,
        "unspecified": total_fields - total_required - total_preferred - total_optional,
    },
    "valueSetCount": len(vs_inventory),
    "totalValueSetValues": total_vs_values,
    "entities": inventory,
    "valueSets": vs_inventory,
}

with open(OUT_DIR / "full-entity-inventory.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary stats
summary = {
    "entityCount": len(inventory),
    "totalFields": total_fields,
    "totalFieldsWithDescriptions": total_described,
    "descriptionPercentage": round(total_described / total_fields * 100, 1) if total_fields > 0 else 0,
    "totalFieldsWithTypes": total_typed,
    "typePercentage": round(total_typed / total_fields * 100, 1) if total_fields > 0 else 0,
    "fieldRequirements": {
        "required": total_required,
        "preferred": total_preferred,
        "optional": total_optional,
    },
    "valueSetCount": len(vs_inventory),
    "totalValueSetValues": total_vs_values,
    "exportFormats": [fmt.get("name", "") for fmt in export_formats],
    "excelTabCount": len(excel_tabs),
    "entitiesWithoutFieldDefs": [t for t in excel_tabs if t not in [e["name"] for e in entities]],
    "entitySummary": [
        {"name": e["name"], "fields": e["fieldCount"], "described": e["fieldsWithDescriptions"], "typed": e["fieldsWithTypes"]}
        for e in inventory
    ],
}

with open(OUT_DIR / "summary-stats.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=" * 70)
print("ENABLEDOC EHI EXPORT DATA DICTIONARY ANALYSIS")
print("=" * 70)
print(f"Source: {full_inventory['source']}")
print(f"Export formats: {', '.join(full_inventory['exportFormats'])}")
print(f"Excel tabs listed: {len(excel_tabs)}")
print(f"Entities with field definitions: {len(inventory)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {total_described} ({summary['descriptionPercentage']}%)")
print(f"Fields with data types: {total_typed} ({summary['typePercentage']}%)")
print(f"Field requirements: {total_required} required, {total_preferred} preferred, {total_optional} optional")
print(f"Value sets: {len(vs_inventory)} ({total_vs_values} total coded values)")
print()

# Tabs without field defs
tabs_without = summary["entitiesWithoutFieldDefs"]
if tabs_without:
    print(f"Excel tabs WITHOUT field definitions: {', '.join(tabs_without)}")
else:
    print("All Excel tabs have field definitions.")

# Check for matching: excel tab names vs entity names
entity_names = [e["name"] for e in entities]
print(f"\nEntity names: {entity_names}")
print(f"Excel tab names: {excel_tabs}")

# Show entity table
print("\n" + "-" * 70)
print(f"{'Entity':<30} {'Fields':>6} {'Described':>10} {'Typed':>6}")
print("-" * 70)
for e in sorted(inventory, key=lambda x: -x["fieldCount"]):
    print(f"{e['name']:<30} {e['fieldCount']:>6} {e['fieldsWithDescriptions']:>10} {e['fieldsWithTypes']:>6}")
print("-" * 70)
print(f"{'TOTAL':<30} {total_fields:>6} {total_described:>10} {total_typed:>6}")
