#!/usr/bin/env python3
"""Parse the actual HTML entity pages to independently verify field counts and descriptions."""

import re
import os
import json
from html.parser import HTMLParser

DOWNLOADS = "../../../results/allegiancemd-software-inc/downloads"

class FieldExtractor(HTMLParser):
    """Extract field rows from Javadoc-style entity HTML pages."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.in_th = False
        self.current_row = []
        self.rows = []
        self.current_text = ""
        self.table_count = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table_count += 1
            self.in_table = True
        elif tag == "td":
            self.in_td = True
            self.current_text = ""
        elif tag == "th":
            self.in_th = True
            self.current_text = ""
        elif tag == "tr":
            self.current_row = []
    
    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif tag == "td":
            self.in_td = False
            self.current_row.append(self.current_text.strip())
        elif tag == "th":
            self.in_th = False
        elif tag == "tr":
            if len(self.current_row) >= 2:
                self.rows.append(self.current_row)
    
    def handle_data(self, data):
        if self.in_td:
            self.current_text += data

results = {}
for fname in sorted(os.listdir(DOWNLOADS)):
    if not fname.endswith("Entity.html"):
        continue
    
    filepath = os.path.join(DOWNLOADS, fname)
    with open(filepath) as f:
        content = f.read()
    
    parser = FieldExtractor()
    parser.feed(content)
    
    entity_name = fname.replace(".html", "")
    
    # Filter to field rows (skip header rows and summary rows)
    field_rows = [r for r in parser.rows if r[0] not in ("Modifier and Type", "Type", "")]
    
    # Count fields with non-empty descriptions
    fields_with_desc = sum(1 for r in field_rows if len(r) >= 3 and r[2].strip())
    
    results[entity_name] = {
        "file": fname,
        "file_size": os.path.getsize(filepath),
        "field_count_from_html": len(field_rows),
        "fields_with_descriptions": fields_with_desc,
    }

# Compare with JSON data dictionary
with open(os.path.join(DOWNLOADS, "entity-data-dictionary.json")) as f:
    json_dict = json.load(f)

print(f"{'Entity':<45} {'HTML':>5} {'JSON':>5} {'Match':>6}")
print("-" * 65)
total_html = 0
total_json = 0
mismatches = []
for entity in sorted(json_dict.keys()):
    json_count = len(json_dict[entity])
    html_count = results.get(entity, {}).get("field_count_from_html", "N/A")
    match = "✓" if html_count == json_count else "✗"
    if html_count != json_count:
        mismatches.append(entity)
    total_html += html_count if isinstance(html_count, int) else 0
    total_json += json_count
    print(f"{entity:<45} {html_count:>5} {json_count:>5} {match:>6}")

print("-" * 65)
print(f"{'TOTAL':<45} {total_html:>5} {total_json:>5}")
if mismatches:
    print(f"\nMismatches found in: {', '.join(mismatches)}")
else:
    print("\nAll counts match between HTML and JSON sources.")

# Save verification results
with open("html_verification.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nVerification results saved to html_verification.json")
