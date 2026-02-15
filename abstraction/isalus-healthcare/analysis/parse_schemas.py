#!/usr/bin/env python3
"""Parse all JSON Schema files from the OfficeEMR EHI export schema ZIP.
Outputs a summary of entities, field counts, and field details."""

import json
import os
import sys
from pathlib import Path

SCHEMA_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/schema/OfficeEMR_B10_Schema_v1-OCT2023")

results = []
total_fields = 0
fields_with_descriptions = 0
fields_with_types = 0

for f in sorted(SCHEMA_DIR.glob("*.json")):
    try:
        with open(f) as fh:
            schema = json.load(fh)
    except json.JSONDecodeError:
        print(f"WARNING: Could not parse {f.name}", file=sys.stderr)
        continue

    # Fields are under items.properties for array schemas
    items = schema.get("items", {})
    props = items.get("properties", schema.get("properties", {}))
    field_count = len(props)
    total_fields += field_count

    desc_count = 0
    typed_count = 0
    for name, prop in props.items():
        desc = prop.get("description", "")
        if desc and desc.strip():
            desc_count += 1
            fields_with_descriptions += 1
        if "type" in prop:
            typed_count += 1
            fields_with_types += 1

    entity_name = f.stem.replace(".schema", "")
    results.append({
        "file": f.name,
        "entity": entity_name,
        "fields": field_count,
        "with_descriptions": desc_count,
        "with_types": typed_count,
        "title": schema.get("title", ""),
        "schema_description": schema.get("description", ""),
    })

# Print summary
print(f"=== JSON Schema Summary ===")
print(f"Total schema files: {len(results)}")
print(f"Total fields: {total_fields}")
print(f"Fields with non-empty descriptions: {fields_with_descriptions}")
print(f"Fields with types: {fields_with_types}")
print()

# Print per-entity table
print(f"{'Entity':<45} {'Fields':>6} {'Described':>9} {'Typed':>6}")
print("-" * 70)
for r in results:
    print(f"{r['entity']:<45} {r['fields']:>6} {r['with_descriptions']:>9} {r['with_types']:>6}")

# Save as JSON
output_path = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare/analysis/schema_summary.json")
with open(output_path, "w") as fh:
    json.dump({"summary": {"total_files": len(results), "total_fields": total_fields,
                            "fields_with_descriptions": fields_with_descriptions,
                            "fields_with_types": fields_with_types},
               "entities": results}, fh, indent=2)
print(f"\nJSON saved to {output_path}")
