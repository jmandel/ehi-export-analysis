"""
Generate a markdown entity inventory table from the data dictionary JSON,
using the INDEX sheet for correct category/module assignment.
"""
import json
import xlrd

RESULTS = "/home/jmandel/hobby/ehi-export-analysis/results/qualifacts-systems-llc--insync-emr-pm"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/qualifacts-systems-llc--insync-emr-pm/analysis"

with open(f"{RESULTS}/downloads/enrichment/data-dictionary.json") as f:
    data = json.load(f)

# Build index mapping from XLS INDEX sheet for correct category/module
wb = xlrd.open_workbook(f"{RESULTS}/downloads/InSync_EHI_Export_Data_Dictionary.xls")
ws = wb.sheet_by_name('INDEX')
index_map = {}
for r in range(3, ws.nrows):  # skip header rows
    row_num = ws.cell_value(r, 0)
    name = ws.cell_value(r, 1).strip()
    cat = ws.cell_value(r, 2).strip()
    mod = ws.cell_value(r, 3).strip()
    if name and name != 'Changelogs':
        index_map[name.lower()] = {"category": cat, "module": mod}

# Build corrected inventory
inventory = []
for s in data['sections']:
    # Try to match to INDEX
    sname = s['section_name'].strip()
    idx = index_map.get(sname.lower(), {})
    cat = idx.get("category", s.get("category", ""))
    mod = idx.get("module", s.get("module", ""))
    
    field_count = len(s['fields'])
    desc_count = sum(1 for f in s['fields'] if f.get('description', '').strip())
    type_count = sum(1 for f in s['fields'] if f.get('data_type', '').strip())
    
    inventory.append({
        "section": sname,
        "category": cat,
        "module": mod,
        "fields": field_count,
        "described": desc_count,
        "typed": type_count
    })

# Sort by category then section name
inventory.sort(key=lambda x: (x['category'], x['section']))

# Print markdown table
print("| # | Entity/Section | Fields | Described | Typed | Category | Module |")
print("|---|---|---|---|---|---|---|")
for i, item in enumerate(inventory, 1):
    print(f"| {i} | {item['section']} | {item['fields']} | {item['described']} | {item['typed']} | {item['category']} | {item['module']} |")

# Also print category summary
print("\n\n### Category Summary\n")
from collections import defaultdict
cat_summary = defaultdict(lambda: {"sections": 0, "fields": 0})
for item in inventory:
    cat = item['category'] or "(unclassified)"
    cat_summary[cat]["sections"] += 1
    cat_summary[cat]["fields"] += item["fields"]

print("| Category | Sections | Total Fields |")
print("|---|---|---|")
for cat, stats in sorted(cat_summary.items(), key=lambda x: -x[1]["fields"]):
    print(f"| {cat} | {stats['sections']} | {stats['fields']} |")

# Module summary
print("\n\n### Module Summary\n")
mod_summary = defaultdict(lambda: {"sections": 0, "fields": 0})
for item in inventory:
    mod = item['module'] or "(unclassified)"
    mod_summary[mod]["sections"] += 1
    mod_summary[mod]["fields"] += item["fields"]

print("| Module | Sections | Total Fields |")
print("|---|---|---|")
for mod, stats in sorted(mod_summary.items(), key=lambda x: -x[1]["fields"]):
    print(f"| {mod} | {stats['sections']} | {stats['fields']} |")

# Save corrected inventory as JSON
with open(f"{OUTPUT}/corrected-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)
