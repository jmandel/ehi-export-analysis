#!/usr/bin/env python3
"""
Parse the enrichment data-dictionary.json from the PDF extraction
and produce a full-entity-inventory.json plus summary statistics.

Input: results/downloads/enrichment/data-dictionary.json (previously extracted from PDF)
Output: full-entity-inventory.json, summary-stats.json
"""

import json
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 
    "../../../results/eyefinity-inc--ehr-powered-by-ema-in-eyefinity-encompass")
ANALYSIS_DIR = os.path.dirname(__file__)

# Load the parsed data dictionary
with open(os.path.join(RESULTS_DIR, "downloads/enrichment/data-dictionary.json")) as f:
    raw_tables = json.load(f)

# Build full entity inventory
entities = []
for t in raw_tables:
    table_name = t.get("table_name", "")
    grouping = t.get("grouping", "")
    description = t.get("description", "")
    columns = t.get("columns", [])
    longitudinal = t.get("longitudinal_tracking", "")
    
    # Skip any malformed entries (the first entry is sometimes a parse artifact)
    if not table_name or table_name == "excluded":
        continue
    
    fields = []
    for col in columns:
        if isinstance(col, str):
            fields.append({
                "name": col,
                "type": None,  # Not provided in this data dictionary
                "description": None,  # Only table-level descriptions exist
                "nullable": None,
                "max_length": None,
                "foreign_key": None,
                "value_set": None
            })
        elif isinstance(col, dict):
            fields.append(col)
    
    entities.append({
        "grouping": grouping,
        "table_name": table_name,
        "description": description,
        "longitudinal_tracking": longitudinal,
        "field_count": len(fields),
        "fields": fields
    })

# Compute summary statistics
total_tables = len(entities)
total_fields = sum(e["field_count"] for e in entities)
tables_with_descriptions = sum(1 for e in entities if e["description"] and len(e["description"].strip()) > 0)
fields_with_descriptions = 0  # No field-level descriptions exist
fields_with_types = 0  # No data types provided

# Group statistics
grouping_stats = {}
for e in entities:
    g = e["grouping"]
    if g not in grouping_stats:
        grouping_stats[g] = {"tables": 0, "fields": 0, "table_names": []}
    grouping_stats[g]["tables"] += 1
    grouping_stats[g]["fields"] += e["field_count"]
    grouping_stats[g]["table_names"].append(e["table_name"])

# Top entities by field count
top_entities = sorted(entities, key=lambda x: x["field_count"], reverse=True)[:20]

# Longitudinal tracking breakdown
tracking_counts = {}
for e in entities:
    lt = e["longitudinal_tracking"] or "Unknown"
    tracking_counts[lt] = tracking_counts.get(lt, 0) + 1

# Write full inventory
inventory_path = os.path.join(ANALYSIS_DIR, "full-entity-inventory.json")
with open(inventory_path, "w") as f:
    json.dump({
        "source": "Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf",
        "extraction_method": "pdftotext -> Bun TypeScript parser -> Python inventory builder",
        "total_entities": total_tables,
        "total_fields": total_fields,
        "entities": entities
    }, f, indent=2)

# Write summary stats
summary = {
    "total_tables": total_tables,
    "total_fields": total_fields,
    "tables_with_descriptions": tables_with_descriptions,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_with_types": fields_with_types,
    "pct_tables_with_descriptions": round(tables_with_descriptions / total_tables * 100, 1) if total_tables > 0 else 0,
    "pct_fields_with_descriptions": 0.0,
    "declared_but_empty_groupings": ["Lookup", "MIPS", "Medical Lookup"],
    "longitudinal_tracking": tracking_counts,
    "grouping_summary": [
        {
            "grouping": g,
            "tables": grouping_stats[g]["tables"],
            "fields": grouping_stats[g]["fields"],
            "table_names": grouping_stats[g]["table_names"]
        }
        for g in sorted(grouping_stats.keys())
    ],
    "top_20_entities_by_field_count": [
        {
            "table_name": e["table_name"],
            "grouping": e["grouping"],
            "field_count": e["field_count"],
            "description": e["description"]
        }
        for e in top_entities
    ]
}

stats_path = os.path.join(ANALYSIS_DIR, "summary-stats.json")
with open(stats_path, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Full entity inventory: {inventory_path}")
print(f"  Entities: {total_tables}")
print(f"  Fields: {total_fields}")
print(f"  Tables with descriptions: {tables_with_descriptions}/{total_tables} ({summary['pct_tables_with_descriptions']}%)")
print(f"  Fields with descriptions: {fields_with_descriptions}/{total_fields} (0%)")
print(f"  Fields with types: {fields_with_types}/{total_fields} (0%)")
print()
print("Grouping breakdown:")
for gs in summary["grouping_summary"]:
    print(f"  {gs['grouping']}: {gs['tables']} tables, {gs['fields']} fields")
print()
print("Longitudinal tracking:")
for k, v in sorted(tracking_counts.items()):
    print(f"  {k}: {v} tables")
print()
print("Top 20 entities by field count:")
for e in top_entities:
    print(f"  {e['table_name']} ({e['grouping']}): {e['field_count']} fields")
