"""
Parse and analyze the InSync EHI Export Data Dictionary.
Produces summary statistics, category breakdowns, and full entity inventory.
"""
import json
import os

RESULTS = "/home/jmandel/hobby/ehi-export-analysis/results/qualifacts-systems-llc--insync-emr-pm"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/qualifacts-systems-llc--insync-emr-pm/analysis"

with open(os.path.join(RESULTS, "downloads/enrichment/data-dictionary.json")) as f:
    data = json.load(f)

sections = data["sections"]

# Summary stats
total_sections = len(sections)
total_fields = sum(len(s["fields"]) for s in sections)

# Count fields with non-trivial descriptions
def is_trivial_description(col_name, desc):
    """Check if description just restates the column name."""
    if not desc or not desc.strip():
        return True
    # Normalize both
    cn = col_name.lower().replace("_", " ").replace("-", " ").strip()
    d = desc.lower().replace("_", " ").replace("-", " ").strip()
    # If description is just the column name with spaces
    if cn == d:
        return True
    # Remove common filler words
    cn_words = set(cn.split())
    d_words = set(d.split())
    if cn_words == d_words:
        return True
    return False

fields_with_any_desc = 0
fields_with_nontrivial_desc = 0
fields_with_remarks = 0
fields_with_types = 0

for s in sections:
    for f in s["fields"]:
        desc = f.get("description", "")
        if desc and desc.strip():
            fields_with_any_desc += 1
        if not is_trivial_description(f["column_name"], desc):
            fields_with_nontrivial_desc += 1
        if f.get("remarks", "").strip():
            fields_with_remarks += 1
        if f.get("data_type", "").strip():
            fields_with_types += 1

# Category/module breakdown
from collections import defaultdict
cat_stats = defaultdict(lambda: {"sections": 0, "fields": 0, "section_names": []})
for s in sections:
    cat = s.get("category", "").strip() or "(unclassified)"
    cat_stats[cat]["sections"] += 1
    cat_stats[cat]["fields"] += len(s["fields"])
    cat_stats[cat]["section_names"].append(s["section_name"])

module_stats = defaultdict(lambda: {"sections": 0, "fields": 0})
for s in sections:
    mod = s.get("module", "").strip() or "(unclassified)"
    module_stats[mod]["sections"] += 1
    module_stats[mod]["fields"] += len(s["fields"])

# Full inventory sorted by field count descending
inventory = []
for s in sections:
    desc_count = sum(1 for f in s["fields"] if f.get("description", "").strip())
    nontrivial_count = sum(1 for f in s["fields"]
                          if not is_trivial_description(f["column_name"], f.get("description", "")))
    types_count = sum(1 for f in s["fields"] if f.get("data_type", "").strip())
    inventory.append({
        "section_name": s["section_name"],
        "sheet_name": s["sheet_name"],
        "category": s.get("category", ""),
        "module": s.get("module", ""),
        "field_count": len(s["fields"]),
        "fields_with_description": desc_count,
        "fields_with_nontrivial_description": nontrivial_count,
        "fields_with_types": types_count,
        "description": s.get("description", ""),
        "field_names": [f["column_name"] for f in s["fields"]]
    })
inventory.sort(key=lambda x: x["field_count"], reverse=True)

# Data types distribution
type_counts = defaultdict(int)
for s in sections:
    for f in s["fields"]:
        dt = f.get("data_type", "").strip() or "(none)"
        type_counts[dt] += 1

# Output results
results = {
    "summary": {
        "total_sections": total_sections,
        "total_fields": total_fields,
        "fields_with_any_description": fields_with_any_desc,
        "fields_with_nontrivial_description": fields_with_nontrivial_desc,
        "fields_with_remarks": fields_with_remarks,
        "fields_with_types": fields_with_types,
        "pct_described": round(fields_with_any_desc / total_fields * 100, 1),
        "pct_nontrivial_desc": round(fields_with_nontrivial_desc / total_fields * 100, 1),
        "pct_typed": round(fields_with_types / total_fields * 100, 1),
    },
    "category_breakdown": {k: {"sections": v["sections"], "fields": v["fields"],
                                "section_names": v["section_names"]}
                           for k, v in sorted(cat_stats.items(), key=lambda x: -x[1]["fields"])},
    "module_breakdown": {k: v for k, v in sorted(module_stats.items(), key=lambda x: -x[1]["fields"])},
    "data_type_distribution": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
    "inventory": inventory
}

with open(os.path.join(OUTPUT, "full-entity-inventory.json"), "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=== InSync EHI Export Data Dictionary Analysis ===\n")
print(f"Total sections: {total_sections}")
print(f"Total fields: {total_fields}")
print(f"Fields with any description: {fields_with_any_desc} ({results['summary']['pct_described']}%)")
print(f"Fields with non-trivial description: {fields_with_nontrivial_desc} ({results['summary']['pct_nontrivial_desc']}%)")
print(f"Fields with remarks: {fields_with_remarks}")
print(f"Fields with data types: {fields_with_types} ({results['summary']['pct_typed']}%)")

print("\n--- Category Breakdown ---")
for cat, stats in results["category_breakdown"].items():
    print(f"  {cat}: {stats['sections']} sections, {stats['fields']} fields")

print("\n--- Module Breakdown ---")
for mod, stats in results["module_breakdown"].items():
    print(f"  {mod}: {stats['sections']} sections, {stats['fields']} fields")

print("\n--- Data Type Distribution ---")
for dt, count in results["data_type_distribution"].items():
    print(f"  {dt}: {count}")

print("\n--- Top 20 Largest Sections ---")
for item in inventory[:20]:
    print(f"  {item['section_name']}: {item['field_count']} fields (cat={item['category']}, mod={item['module']})")

print("\n--- Sections with 0 non-trivial descriptions ---")
for item in inventory:
    if item["fields_with_nontrivial_description"] == 0:
        print(f"  {item['section_name']}: {item['field_count']} fields")
