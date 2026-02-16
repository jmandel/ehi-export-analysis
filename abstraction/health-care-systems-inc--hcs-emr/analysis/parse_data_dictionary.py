#!/usr/bin/env python3
"""Parse HCS Data Dictionary CSV into structured JSON inventory."""

import csv
import json
import sys
from collections import defaultdict

INPUT = "../downloads/HCSDataDictionary.csv"
OUTPUT_FULL = "entity-inventory-full.json"
OUTPUT_SUMMARY = "entity-inventory-summary.json"

tables = []
current_table = None

with open(INPUT, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # Table,Column,Type,Size,Description
    
    for row in reader:
        if len(row) < 5:
            # blank or short row — separator
            continue
        
        table_name, col_name, col_type, col_size, description = [c.strip() for c in row[:5]]
        
        if table_name and not col_name and not col_type:
            # Table header row
            if current_table:
                tables.append(current_table)
            current_table = {
                "table": table_name,
                "table_description": description,
                "fields": []
            }
        elif current_table and col_name:
            field = {
                "name": col_name,
                "type": col_type if col_type else None,
                "size": col_size if col_size else None,
                "description": description if description else None
            }
            # Check for foreign key references
            if description and "Reference to " in description:
                ref = description.split("Reference to ")[-1].strip()
                field["references"] = ref
            current_table["fields"].append(field)

    if current_table:
        tables.append(current_table)

# Save full inventory
with open(OUTPUT_FULL, 'w') as f:
    json.dump(tables, f, indent=2)

# Compute summary statistics
total_fields = sum(len(t["fields"]) for t in tables)
fields_with_desc = sum(1 for t in tables for fld in t["fields"] if fld["description"])
fields_with_type = sum(1 for t in tables for fld in t["fields"] if fld["type"])
fields_with_fk = sum(1 for t in tables for fld in t["fields"] if "references" in fld)

# Type distribution
type_counts = defaultdict(int)
for t in tables:
    for fld in t["fields"]:
        if fld["type"]:
            base_type = fld["type"].lower()
            type_counts[base_type] += 1

# Table size distribution
table_sizes = sorted([(t["table"], len(t["fields"])) for t in tables], key=lambda x: -x[1])

# Categorize tables by likely domain based on naming patterns
def categorize(name):
    n = name.lower()
    if any(k in n for k in ['charge', 'claim', 'payment', 'copay', 'insurance', 'eligibility', 'pbm', 'coverage']):
        return "Billing & Insurance"
    if any(k in n for k in ['admin', 'therapy']) and 'admin' in n[:6].lower():
        return "Medication Administration"
    if any(k in n for k in ['order', 'component', 'dispens', 'product', 'routed', 'packaged', 'named', 'medlist', 'medrec', 'formulary']):
        return "Orders & Pharmacy"
    if any(k in n for k in ['observation', 'condition', 'visitobservation']):
        return "Observations & Assessments"
    if any(k in n for k in ['patient']) and not any(k in n for k in ['claim', 'insurance', 'order']):
        return "Patient & Demographics"
    if any(k in n for k in ['visit']) and not any(k in n for k in ['charge', 'insurance', 'observation']):
        return "Visits & Encounters"
    if any(k in n for k in ['staff', 'practitioner']):
        return "Staff & Providers"
    if any(k in n for k in ['clinical', 'alert', 'concern', 'intervention', 'careplan', 'carelevel', 'problem', 'diagnosis']):
        return "Clinical Care"
    if any(k in n for k in ['document', 'consent', 'note', 'image', 'instruction']):
        return "Documents & Notes"
    if any(k in n for k in ['event', 'calendar', 'schedule']):
        return "Scheduling"
    if any(k in n for k in ['chat', 'message']):
        return "Communications"
    if any(k in n for k in ['immunization']):
        return "Immunizations"
    if any(k in n for k in ['near', 'safety', 'physicallocation', 'worktask']):
        return "Safety & Compliance"
    return "Other / Reference"

category_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "table_names": []})
for t in tables:
    cat = categorize(t["table"])
    category_stats[cat]["tables"] += 1
    category_stats[cat]["fields"] += len(t["fields"])
    category_stats[cat]["table_names"].append(t["table"])

summary = {
    "total_tables": len(tables),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_type,
    "fields_with_foreign_keys": fields_with_fk,
    "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "type_distribution": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
    "top_20_largest_tables": [{"table": n, "fields": c} for n, c in table_sizes[:20]],
    "categories": {k: {"tables": v["tables"], "fields": v["fields"], "table_names": v["table_names"]} 
                   for k, v in sorted(category_stats.items(), key=lambda x: -x[1]["fields"])}
}

with open(OUTPUT_SUMMARY, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"Tables: {len(tables)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['description_coverage_pct']}%)")
print(f"Fields with types: {fields_with_type}")
print(f"Fields with FK references: {fields_with_fk}")
print(f"\nTop 20 largest tables:")
for name, count in table_sizes[:20]:
    print(f"  {name}: {count} fields")
print(f"\nCategories:")
for cat, stats in sorted(category_stats.items(), key=lambda x: -x[1]["fields"]):
    print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields")
