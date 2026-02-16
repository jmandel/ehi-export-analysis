#!/usr/bin/env python3
"""
Parse the enrichment data-dictionary.json from the TronsHealth EHI export PDF
and produce:
  1. full-entity-inventory.json — complete machine-readable extraction
  2. summary-stats.json — aggregate statistics for the analysis
"""

import json
import os

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "results", "tronshealth-llc--tronshealth"
)
ENRICHMENT = os.path.join(RESULTS_DIR, "downloads", "enrichment")
OUT_DIR = os.path.dirname(__file__)

# Load the prior extraction
with open(os.path.join(ENRICHMENT, "data-dictionary.json")) as f:
    dd = json.load(f)

with open(os.path.join(ENRICHMENT, "extraction-stats.json")) as f:
    stats = json.load(f)

# Build full entity inventory
entities = []
total_fields = 0
fields_with_descriptions = 0
fields_with_types = 0
type_counts = {}

for entity in dd["entities"]:
    fields = []
    for field in entity["fields"]:
        desc = field.get("description", "").strip()
        dtype = field.get("dataType", "").strip()
        has_desc = bool(desc) and desc.lower() not in ["", "n/a"]
        has_type = bool(dtype)

        if dtype:
            type_counts[dtype] = type_counts.get(dtype, 0) + 1

        fields.append({
            "name": field["name"],
            "data_type": dtype if has_type else None,
            "description": desc if has_desc else None,
            "has_description": has_desc,
            "has_type": has_type,
        })

        total_fields += 1
        if has_desc:
            fields_with_descriptions += 1
        if has_type:
            fields_with_types += 1

    entities.append({
        "section_number": entity["sectionNumber"],
        "name": entity["name"],
        "field_count": len(fields),
        "fields_with_descriptions": sum(1 for f in fields if f["has_description"]),
        "fields_with_types": sum(1 for f in fields if f["has_type"]),
        "fields": fields,
    })

# Missing sections from TOC
missing_sections = [
    {"section": "3.15", "name": "Patient – Provider Note", "toc_page": 27},
    {"section": "3.18", "name": "Patient – Encounter", "toc_page": 32},
]

inventory = {
    "vendor": dd.get("vendor", "TronsHealth LLC"),
    "product": dd.get("product", "TronsHealth"),
    "document_date": dd.get("documentDate", "2024-09-11"),
    "export_format": dd.get("exportFormat", "CSV files in ZIP archive"),
    "total_entities_documented": len(entities),
    "total_entities_in_toc": len(entities) + len(missing_sections),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_with_types": fields_with_types,
    "missing_sections": missing_sections,
    "entities": entities,
}

# Write full inventory
inv_path = os.path.join(OUT_DIR, "full-entity-inventory.json")
with open(inv_path, "w") as f:
    json.dump(inventory, f, indent=2)
print(f"Wrote {inv_path}")

# Summary stats
summary = {
    "total_entities_documented": len(entities),
    "total_entities_in_toc": len(entities) + len(missing_sections),
    "missing_sections": [s["name"] for s in missing_sections],
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "pct_fields_with_descriptions": round(100 * fields_with_descriptions / total_fields, 1) if total_fields else 0,
    "fields_with_types": fields_with_types,
    "pct_fields_with_types": round(100 * fields_with_types / total_fields, 1) if total_fields else 0,
    "data_type_distribution": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
    "entity_breakdown": [
        {
            "section": e["section_number"],
            "name": e["name"],
            "fields": e["field_count"],
            "fields_described": e["fields_with_descriptions"],
            "fields_typed": e["fields_with_types"],
        }
        for e in entities
    ],
    "largest_entities": sorted(
        [{"name": e["name"], "fields": e["field_count"]} for e in entities],
        key=lambda x: -x["fields"]
    )[:5],
    "smallest_entities": sorted(
        [{"name": e["name"], "fields": e["field_count"]} for e in entities],
        key=lambda x: x["fields"]
    )[:3],
}

stats_path = os.path.join(OUT_DIR, "summary-stats.json")
with open(stats_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {stats_path}")

# Print summary
print(f"\n=== Summary ===")
print(f"Entities documented: {len(entities)} of {len(entities) + len(missing_sections)} in TOC")
print(f"Missing: {', '.join(s['name'] for s in missing_sections)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_descriptions} ({summary['pct_fields_with_descriptions']}%)")
print(f"Fields with types: {fields_with_types} ({summary['pct_fields_with_types']}%)")
print(f"\nEntity breakdown:")
for e in entities:
    print(f"  {e['section_number']:>5} {e['name']:<35} {e['field_count']:>3} fields")
print(f"\nData types: {type_counts}")
