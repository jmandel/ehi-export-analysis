#!/usr/bin/env python3
"""
Analyze the GlaceEMR Data Dictionary JSON to produce:
- full-entity-inventory.json (complete field-level extraction)
- summary statistics
- category breakdowns
"""

import json
import sys
from pathlib import Path

DD_PATH = Path(__file__).parent / "../../../results/glenwood-systems-llc--glaceemr/downloads/enrichment/data-dictionary.json"
OUT_DIR = Path(__file__).parent

def main():
    with open(DD_PATH) as f:
        dd = json.load(f)

    entities = []
    total_fields = 0
    fields_with_desc = 0
    fields_with_type = 0
    fields_with_fk = 0
    fields_with_possible_values = 0

    for schema in dd["file_schemas"]:
        filename = schema["filename"]
        folder = schema["folder"]
        columns = schema.get("columns", [])

        entity = {
            "filename": filename,
            "folder": folder,
            "contents_description": schema.get("contents_description", ""),
            "field_count": len(columns),
            "fields": []
        }

        entity_desc_count = 0
        entity_type_count = 0

        for col in columns:
            field = {
                "name": col.get("name", ""),
                "data_type": col.get("data_type", ""),
                "description": col.get("description", ""),
                "comments": col.get("comments", ""),
            }
            # Capture optional fields
            if col.get("is_primary_key"):
                field["is_primary_key"] = True
            if col.get("is_foreign_key"):
                field["is_foreign_key"] = True
                field["foreign_key_ref"] = col.get("foreign_key_ref", "")
                fields_with_fk += 1
            if col.get("possible_values"):
                field["possible_values"] = col["possible_values"]
                fields_with_possible_values += 1

            has_desc = bool(field["description"].strip()) or bool(field["comments"].strip())
            if has_desc:
                fields_with_desc += 1
                entity_desc_count += 1
            if field["data_type"].strip():
                fields_with_type += 1
                entity_type_count += 1

            entity["fields"].append(field)

        entity["fields_with_descriptions"] = entity_desc_count
        entity["fields_with_types"] = entity_type_count
        entities.append(entity)
        total_fields += len(columns)

    # Build category breakdown
    categories = {}
    for e in entities:
        cat = e["folder"]
        if cat not in categories:
            categories[cat] = {"entity_count": 0, "field_count": 0, "fields_with_desc": 0}
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e["field_count"]
        categories[cat]["fields_with_desc"] += e["fields_with_descriptions"]

    inventory = {
        "source": "GlaceEMR Export Data Dictionary v1.0 (2023-11-27)",
        "summary": {
            "total_entities": len(entities),
            "total_fields": total_fields,
            "fields_with_descriptions": fields_with_desc,
            "fields_with_types": fields_with_type,
            "fields_with_foreign_keys": fields_with_fk,
            "fields_with_possible_values": fields_with_possible_values,
            "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        },
        "category_breakdown": categories,
        "entities": entities
    }

    # Write full inventory
    out_path = OUT_DIR / "full-entity-inventory.json"
    with open(out_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote {out_path}")

    # Print summary
    print(f"\n=== GlaceEMR Data Dictionary Summary ===")
    print(f"Total entities (CSV files): {len(entities)}")
    print(f"Total fields (columns):     {total_fields}")
    print(f"Fields with descriptions:   {fields_with_desc} ({inventory['summary']['description_coverage_pct']}%)")
    print(f"Fields with data types:     {fields_with_type}")
    print(f"Fields with foreign keys:   {fields_with_fk}")
    print(f"Fields with possible values:{fields_with_possible_values}")

    print(f"\n=== Category Breakdown ===")
    for cat, info in categories.items():
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields, {info['fields_with_desc']} with descriptions")

    print(f"\n=== Entity Details ===")
    for e in entities:
        desc_pct = round(e["fields_with_descriptions"] / e["field_count"] * 100) if e["field_count"] else 0
        print(f"  {e['filename']:50s} {e['field_count']:3d} fields  ({desc_pct}% described)")

    # Write summary to text file too
    summary_path = OUT_DIR / "summary-stats.txt"
    with open(summary_path, "w") as f:
        f.write(f"GlaceEMR Data Dictionary Summary\n")
        f.write(f"================================\n\n")
        f.write(f"Total entities: {len(entities)}\n")
        f.write(f"Total fields: {total_fields}\n")
        f.write(f"Fields with descriptions: {fields_with_desc} ({inventory['summary']['description_coverage_pct']}%)\n")
        f.write(f"Fields with data types: {fields_with_type}\n")
        f.write(f"Fields with foreign keys: {fields_with_fk}\n")
        f.write(f"Fields with possible values: {fields_with_possible_values}\n\n")
        f.write(f"Category Breakdown:\n")
        for cat, info in categories.items():
            f.write(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields\n")
        f.write(f"\nEntity Details:\n")
        for e in entities:
            desc_pct = round(e["fields_with_descriptions"] / e["field_count"] * 100) if e["field_count"] else 0
            f.write(f"  {e['filename']:50s} {e['field_count']:3d} fields  ({desc_pct}% described)\n")
    print(f"\nWrote {summary_path}")

if __name__ == "__main__":
    main()
