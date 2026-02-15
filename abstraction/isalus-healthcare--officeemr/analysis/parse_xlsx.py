"""
Parse the XLSX data dictionary more thoroughly, extracting:
- Entity name, field name, description, example, category (Clinical/PM)
- Build entity-level and category-level summaries
"""
import json, openpyxl
from pathlib import Path
from collections import defaultdict

BASE = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare--officeemr/downloads")
OUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare--officeemr/analysis")

xlsx_path = BASE / "data-elements" / "iSalus_EHI_ExportDataElements_published_version1_Oct2023_pristine.xlsx"
wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)

ws = wb['Export Field Listing']
rows = list(ws.iter_rows(values_only=True))
headers = rows[0]
# Headers: ('Export Name', 'Field Items', 'FIELD Position in Export', 'FIELD', 'Description', 'Example:', 'Data Type')

entities = defaultdict(lambda: {"fields": [], "category": ""})
all_fields = []

for row in rows[1:]:
    export_name = str(row[0]).strip() if row[0] else ""
    field_name = str(row[3]).strip() if row[3] else ""
    description = str(row[4]).strip() if row[4] else ""
    example = str(row[5]).strip() if row[5] else ""
    category = str(row[6]).strip() if row[6] else ""
    
    if not field_name or field_name == "None":
        continue
    
    entity_key = export_name.replace(".json", "").strip()
    has_desc = bool(description and description != "None")
    has_example = bool(example and example != "None")
    
    field_entry = {
        "field": field_name,
        "description": description if has_desc else "",
        "example": example if has_example else "",
        "has_description": has_desc,
        "has_example": has_example,
        "category": category
    }
    
    entities[entity_key]["fields"].append(field_entry)
    entities[entity_key]["category"] = category
    all_fields.append({**field_entry, "entity": entity_key})

wb.close()

# Build entity summary
entity_summary = []
for name, data in sorted(entities.items()):
    total = len(data["fields"])
    with_desc = sum(1 for f in data["fields"] if f["has_description"])
    with_example = sum(1 for f in data["fields"] if f["has_example"])
    entity_summary.append({
        "entity": name,
        "category": data["category"],
        "field_count": total,
        "fields_with_descriptions": with_desc,
        "fields_with_examples": with_example,
        "description_pct": round(with_desc / total * 100) if total > 0 else 0,
        "fields": [f["field"] for f in data["fields"]]
    })

# Category summary
categories = defaultdict(lambda: {"entities": 0, "fields": 0, "with_desc": 0, "with_example": 0, "entity_names": []})
for e in entity_summary:
    cat = e["category"] or "Unknown"
    categories[cat]["entities"] += 1
    categories[cat]["fields"] += e["field_count"]
    categories[cat]["with_desc"] += e["fields_with_descriptions"]
    categories[cat]["with_example"] += e["fields_with_examples"]
    categories[cat]["entity_names"].append(e["entity"])

# Save outputs
with open(OUT / "xlsx-entity-summary.json", "w") as fh:
    json.dump(entity_summary, fh, indent=2)

with open(OUT / "xlsx-category-summary.json", "w") as fh:
    json.dump(dict(categories), fh, indent=2)

# Print results
print("=" * 70)
print("XLSX DATA DICTIONARY ANALYSIS")
print("=" * 70)
print(f"Total entities: {len(entity_summary)}")
print(f"Total fields: {len(all_fields)}")
print(f"Fields with descriptions: {sum(1 for f in all_fields if f['has_description'])} ({sum(1 for f in all_fields if f['has_description'])/len(all_fields)*100:.0f}%)")
print(f"Fields with examples: {sum(1 for f in all_fields if f['has_example'])} ({sum(1 for f in all_fields if f['has_example'])/len(all_fields)*100:.0f}%)")

print(f"\n{'Category':<20} {'Entities':>10} {'Fields':>10} {'Described':>10} {'Examples':>10}")
print("-" * 65)
for cat, stats in sorted(categories.items()):
    print(f"{cat:<20} {stats['entities']:>10} {stats['fields']:>10} {stats['with_desc']:>10} {stats['with_example']:>10}")

print(f"\n{'Entity':<45} {'Cat':<10} {'Fields':>8} {'Desc':>6} {'Ex':>6}")
print("-" * 80)
for e in sorted(entity_summary, key=lambda x: -x["field_count"]):
    print(f"{e['entity']:<45} {e['category']:<10} {e['field_count']:>8} {e['fields_with_descriptions']:>6} {e['fields_with_examples']:>6}")
