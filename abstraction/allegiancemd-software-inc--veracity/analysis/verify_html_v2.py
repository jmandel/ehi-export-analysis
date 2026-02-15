#!/usr/bin/env python3
"""Parse Javadoc HTML entity pages using the actual div-based structure to verify field counts."""

import re
import os
import json

DOWNLOADS = "../../../results/allegiancemd-software-inc/downloads"

results = {}
for fname in sorted(os.listdir(DOWNLOADS)):
    if not fname.endswith("Entity.html"):
        continue
    
    filepath = os.path.join(DOWNLOADS, fname)
    with open(filepath) as f:
        content = f.read()
    
    entity_name = fname.replace(".html", "")
    
    # Extract field names from member-name-link anchors
    field_names = re.findall(r'class="member-name-link">(\w+)</a>', content)
    
    # Extract descriptions from div.block elements
    descriptions = re.findall(r'<div class="block">\s*(.*?)\s*</div>', content, re.DOTALL)
    descriptions = [d.strip() for d in descriptions]
    non_empty_desc = [d for d in descriptions if d]
    
    # Extract types from col-first divs
    types = re.findall(r'<code>\s*(?:<a[^>]*>)?(\w+(?:\[])?)(?:</a>)?(?:&lt;.*?&gt;)?\s*</code>', content)
    
    results[entity_name] = {
        "file": fname,
        "file_size": os.path.getsize(filepath),
        "field_count": len(field_names),
        "fields_with_descriptions": len(non_empty_desc),
        "field_names": field_names,
    }

# Compare with JSON data dictionary
with open(os.path.join(DOWNLOADS, "entity-data-dictionary.json")) as f:
    json_dict = json.load(f)

print(f"{'Entity':<45} {'HTML':>5} {'JSON':>5} {'Match':>6} {'Desc':>5}")
print("-" * 70)
total_html = 0
total_json = 0
total_desc_html = 0
mismatches = []
for entity in sorted(json_dict.keys()):
    json_count = len(json_dict[entity])
    html_data = results.get(entity, {})
    html_count = html_data.get("field_count", "N/A")
    desc_count = html_data.get("fields_with_descriptions", 0)
    match = "✓" if html_count == json_count else "✗"
    if html_count != json_count:
        mismatches.append((entity, html_count, json_count))
    total_html += html_count if isinstance(html_count, int) else 0
    total_json += json_count
    total_desc_html += desc_count
    print(f"{entity:<45} {html_count:>5} {json_count:>5} {match:>6} {desc_count:>5}")

print("-" * 70)
print(f"{'TOTAL':<45} {total_html:>5} {total_json:>5} {'':>6} {total_desc_html:>5}")

if mismatches:
    print(f"\nMismatches ({len(mismatches)}):")
    for entity, h, j in mismatches:
        print(f"  {entity}: HTML={h}, JSON={j}")
else:
    print("\nAll counts match between HTML and JSON sources. ✓")
