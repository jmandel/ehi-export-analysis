"""
Parse the v9-data-dictionary.json with categories from v9-index.html.
Produces full entity inventory, category summary, and stats.
"""
import json
import re
from collections import Counter

DD_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/practice-fusion--practice-fusion-ehr/downloads/v9-data-dictionary.json"
INDEX_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/practice-fusion--practice-fusion-ehr/downloads/v9-index.html"
OUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/practice-fusion--practice-fusion-ehr/analysis"

with open(DD_PATH) as f:
    dd = json.load(f)

# Extract categories from index HTML using h3 headings
with open(INDEX_PATH) as f:
    html = f.read()

sections = re.split(r'<h3[^>]*>(.*?)</h3>', html, flags=re.DOTALL)
categories = {}
table_to_category = {}
for i in range(1, len(sections), 2):
    cat_name = re.sub(r'<[^>]+>', '', sections[i]).strip()
    content = sections[i+1] if i+1 < len(sections) else ''
    links = re.findall(r'href="/ehi-export-documentation/v9/([^/"]+)/?\"', content)
    links = [l for l in links if l != 'index']
    tsv_names = [l + '.tsv' for l in links]
    categories[cat_name] = tsv_names
    for t in tsv_names:
        table_to_category[t] = cat_name

# Basic stats
total_tables = len(dd)
total_fields = sum(t["field_count"] for t in dd.values())
fields_with_desc = 0
fields_without_desc = 0
type_counts = Counter()

for tdata in dd.values():
    for field in tdata["fields"]:
        desc = field.get("description", "").strip()
        if desc:
            fields_with_desc += 1
        else:
            fields_without_desc += 1
        type_counts[field.get("data_type", "unknown")] += 1

# Print stats
print(f"=== Practice Fusion v9 Data Dictionary Stats ===")
print(f"Total tables: {total_tables}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({100*fields_with_desc/total_fields:.1f}%)")
print(f"Fields without descriptions: {fields_without_desc} ({100*fields_without_desc/total_fields:.1f}%)")
print()

print("=== Data Type Distribution ===")
for dtype, count in type_counts.most_common():
    print(f"  {dtype}: {count}")
print()

# Category stats
print("=== Category Breakdown ===")
print(f"{'Category':<30} {'Tables':>6} {'Fields':>6} {'Described':>9} {'%':>6}")
print("-" * 60)
category_stats = {}
for cat, tables in categories.items():
    field_count = sum(dd[t]["field_count"] for t in tables if t in dd)
    described = sum(
        1 for t in tables if t in dd
        for f in dd[t]["fields"] if f.get("description", "").strip()
    )
    pct = round(100 * described / field_count, 1) if field_count > 0 else 0
    category_stats[cat] = {
        "tables": len(tables),
        "fields": field_count,
        "described": described,
        "pct_described": pct
    }
    print(f"  {cat:<28} {len(tables):>6} {field_count:>6} {described:>9} {pct:>5.1f}%")

print("-" * 60)
print(f"  {'TOTAL':<28} {total_tables:>6} {total_fields:>6} {fields_with_desc:>9} {100*fields_with_desc/total_fields:.1f}%")
print()

# Build full inventory
inventory = []
for tname, tdata in sorted(dd.items()):
    cat = table_to_category.get(tname, "Uncategorized")
    desc_count = sum(1 for f in tdata["fields"] if f.get("description", "").strip())
    typed_count = sum(1 for f in tdata["fields"] if f.get("data_type", "").strip())
    inventory.append({
        "table": tname,
        "category": cat,
        "field_count": tdata["field_count"],
        "fields_described": desc_count,
        "fields_typed": typed_count,
        "pct_described": round(100 * desc_count / tdata["field_count"], 1) if tdata["field_count"] > 0 else 0,
        "fields": [
            {
                "name": f["field_name"],
                "type": f.get("data_type", ""),
                "description": f.get("description", "")
            }
            for f in tdata["fields"]
        ]
    })

inventory.sort(key=lambda x: (x["category"], x["table"]))

with open(f"{OUT_DIR}/full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

with open(f"{OUT_DIR}/category-summary.json", "w") as f:
    json.dump(category_stats, f, indent=2)

# Top tables
print("=== Top 20 Largest Tables ===")
by_size = sorted(inventory, key=lambda x: x["field_count"], reverse=True)
for t in by_size[:20]:
    print(f"  {t['table']}: {t['field_count']} fields ({t['category']})")

# Tables with incomplete descriptions
print()
print("=== Tables with <100% Descriptions ===")
incomplete = [t for t in inventory if t["pct_described"] < 100]
if incomplete:
    for t in incomplete:
        print(f"  {t['table']}: {t['fields_described']}/{t['field_count']} ({t['pct_described']}%)")
        for f in t["fields"]:
            if not f["description"]:
                print(f"    Missing desc: {f['name']} ({f['type']})")
else:
    print("  All tables have 100% field descriptions")

# Check for tables with description field (table-level)
print()
print("=== Table-Level Descriptions ===")
has_table_desc = sum(1 for tdata in dd.values() if tdata.get("description", "").strip())
print(f"Tables with table-level description: {has_table_desc}/{total_tables}")

print()
print(f"Saved full-entity-inventory.json ({len(inventory)} tables)")
print(f"Saved category-summary.json ({len(category_stats)} categories)")
