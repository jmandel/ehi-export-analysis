#!/usr/bin/env python3
"""Analyze the sample patient export files. Count records, fields, and data coverage."""

import json
from pathlib import Path

SAMPLE_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/sample-export")

results = []
total_records = 0

for f in sorted(SAMPLE_DIR.glob("*.json")):
    try:
        with open(f, encoding='utf-8-sig') as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, UnicodeDecodeError):
        results.append({"file": f.name, "error": "parse_error"})
        continue

    entity_name = f.stem
    if isinstance(data, list):
        record_count = len(data)
        total_records += record_count
        # Analyze first record for field coverage
        if record_count > 0:
            first = data[0]
            field_count = len(first.keys()) if isinstance(first, dict) else 0
            populated = sum(1 for v in first.values() if v is not None and v != "" and v != []) if isinstance(first, dict) else 0
        else:
            field_count = 0
            populated = 0
    elif isinstance(data, dict):
        record_count = 1
        total_records += 1
        field_count = len(data.keys())
        populated = sum(1 for v in data.values() if v is not None and v != "" and v != [])
    else:
        record_count = 0
        field_count = 0
        populated = 0

    results.append({
        "file": f.name,
        "entity": entity_name,
        "records": record_count,
        "fields_in_first_record": field_count,
        "populated_fields": populated,
    })

print(f"=== Sample Export Summary ===")
print(f"Total files: {len(results)}")
print(f"Total records across all files: {total_records}")
print()
print(f"{'Entity':<45} {'Records':>8} {'Fields':>7} {'Populated':>10}")
print("-" * 75)
for r in results:
    if "error" in r:
        print(f"{r['file']:<45} ERROR")
    else:
        print(f"{r['entity']:<45} {r['records']:>8} {r['fields_in_first_record']:>7} {r['populated_fields']:>10}")

# Save as JSON
output_path = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare/analysis/sample_export_summary.json")
with open(output_path, "w") as fh:
    json.dump({"total_files": len(results), "total_records": total_records, "entities": results}, fh, indent=2)
print(f"\nJSON saved to {output_path}")
