"""
Build the final cross-referenced entity inventory from:
1. All 80 JSON schema files (67 .schema.json + 13 .json)
2. PDF data dictionary (uncorrupted source of truth for descriptions)
3. 58 sample export files
"""
import json, re, glob as globmod
from pathlib import Path
from collections import defaultdict

BASE = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare--officeemr/downloads")
OUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare--officeemr/analysis")

# ── 1. Schema files ──
schema_dir = BASE / "schema" / "OfficeEMR_B10_Schema_v1-OCT2023"
schema_data = {}
for f in sorted(schema_dir.glob("*.json")):
    name = f.stem.replace(".schema", "")
    try:
        with open(f) as fh:
            content = fh.read()
        # Fix known JSON errors (double commas)
        content = content.replace('"",', '""')
        s = json.loads(content)
        items = s.get("items", s)
        props = items.get("properties", {})
        schema_data[name] = {
            "field_count": len(props),
            "fields": sorted(props.keys()),
            "types": {k: v.get("type", "unknown") for k, v in props.items()}
        }
    except Exception as e:
        # Fallback: count by grep
        with open(f) as fh:
            lines = fh.readlines()
        field_count = sum(1 for l in lines if '"description"' in l) - 1  # subtract root description
        schema_data[name] = {"field_count": max(field_count, 0), "fields": [], "types": {}}

# ── 2. PDF data dictionary ──
pdf_dict = json.load(open(OUT / "pdf-data-dictionary.json"))
pdf_entities = defaultdict(lambda: {"fields": [], "category": ""})
for entry in pdf_dict:
    e = entry["entity"]
    pdf_entities[e]["fields"].append(entry["field"])
    pdf_entities[e]["category"] = entry["category"]

# ── 3. Sample export ──
sample_dir = BASE / "sample-export"
sample_data = {}
for f in sorted(sample_dir.glob("*.json")):
    name = f.stem
    try:
        with open(f, encoding='utf-8-sig') as fh:
            data = json.load(fh)
        if isinstance(data, list):
            records = len(data)
            if records > 0 and isinstance(data[0], dict):
                fields = set()
                for rec in data:
                    fields.update(rec.keys())
                sample_data[name] = {"records": records, "fields": len(fields)}
            else:
                sample_data[name] = {"records": records, "fields": 0}
        elif isinstance(data, dict):
            sample_data[name] = {"records": 1, "fields": len(data)}
        else:
            sample_data[name] = {"records": 0, "fields": 0}
    except:
        sample_data[name] = {"records": 0, "fields": 0}

# ── Build combined inventory ──
all_names = sorted(set(list(schema_data.keys()) + list(pdf_entities.keys()) + list(sample_data.keys())))
# Exclude readme
all_names = [n for n in all_names if n != "readme"]

inventory = []
for name in all_names:
    s = schema_data.get(name, {})
    p = pdf_entities.get(name, {"fields": [], "category": ""})
    d = sample_data.get(name, {})
    
    inventory.append({
        "entity": name,
        "category": p.get("category", "Unknown"),
        "schema_fields": s.get("field_count", 0),
        "pdf_fields": len(p["fields"]),
        "sample_records": d.get("records", 0),
        "sample_fields": d.get("fields", 0),
        "in_schema": name in schema_data,
        "in_pdf": name in pdf_entities,
        "in_sample": name in sample_data
    })

# Save
with open(OUT / "full-entity-inventory.json", "w") as fh:
    json.dump(inventory, fh, indent=2)

# ── Category summary ──
categories = defaultdict(lambda: {"entities": 0, "total_schema_fields": 0, "total_pdf_fields": 0, "entity_names": []})
for e in inventory:
    cat = e["category"] or "Unknown"
    categories[cat]["entities"] += 1
    categories[cat]["total_schema_fields"] += e["schema_fields"]
    categories[cat]["total_pdf_fields"] += e["pdf_fields"]
    categories[cat]["entity_names"].append(e["entity"])

with open(OUT / "category-summary.json", "w") as fh:
    json.dump(dict(categories), fh, indent=2)

# ── Print results ──
total_schema = sum(e["schema_fields"] for e in inventory)
total_pdf = sum(e["pdf_fields"] for e in inventory)
total_sample_records = sum(e["sample_records"] for e in inventory)

print("=" * 80)
print("FINAL ENTITY INVENTORY")
print("=" * 80)
print(f"Total entities (excl readme): {len(inventory)}")
print(f"Total schema fields: {total_schema}")
print(f"Total PDF-documented fields: {total_pdf}")
print(f"Total sample records: {total_sample_records}")
print(f"Entities in schema: {sum(1 for e in inventory if e['in_schema'])}")
print(f"Entities in PDF dict: {sum(1 for e in inventory if e['in_pdf'])}")
print(f"Entities in sample: {sum(1 for e in inventory if e['in_sample'])}")
print(f"Entities in all three: {sum(1 for e in inventory if e['in_schema'] and e['in_pdf'] and e['in_sample'])}")

print(f"\n{'Category':<25} {'Entities':>10} {'Schema F':>10} {'PDF F':>10}")
print("-" * 60)
for cat, stats in sorted(categories.items()):
    print(f"{cat:<25} {stats['entities']:>10} {stats['total_schema_fields']:>10} {stats['total_pdf_fields']:>10}")

print(f"\n{'Entity':<45} {'Cat':<20} {'SchF':>6} {'PdfF':>6} {'SmpR':>6}")
print("-" * 90)
for e in sorted(inventory, key=lambda x: -x["schema_fields"]):
    print(f"{e['entity']:<45} {e['category']:<20} {e['schema_fields']:>6} {e['pdf_fields']:>6} {e['sample_records']:>6}")
