#!/usr/bin/env python3
"""Parse the EHI export HTML page and extract structured data categories and items."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent.parent.parent / "results" / "avon-health--avon-emr" / "downloads"
OUTPUT_DIR = Path(__file__).resolve().parent

class StructuredExtractor(HTMLParser):
    """Extract headings and list items to reconstruct the data categories."""
    def __init__(self):
        super().__init__()
        self.elements = []
        self.current_tag = None
        self.current_text = ""
        self.skip_tags = {"script", "style", "noscript"}
        self.skip = False
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
        self.tag_stack.append(tag)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "li", "p"):
            self.current_tag = tag
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
        if tag == self.current_tag and self.current_text.strip():
            self.elements.append({"tag": tag, "text": self.current_text.strip()})
            self.current_tag = None
            self.current_text = ""
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

    def handle_data(self, data):
        if not self.skip and self.current_tag:
            self.current_text += data


html_path = DOWNLOADS / "ehi-export.html"
with open(html_path, "r") as f:
    content = f.read()

parser = StructuredExtractor()
parser.feed(content)

# Find the "Data Categories Included" section and extract categories
in_data_categories = False
current_category = None
categories = []
all_items = []

for elem in parser.elements:
    if "Data Categories Included" in elem["text"]:
        in_data_categories = True
        continue
    if not in_data_categories:
        continue
    # Stop at navigation elements
    if elem["text"] in ("Next", "Getting started", "→") or "What is Electronic Health" in elem["text"]:
        break
    if elem["tag"] == "h4":
        current_category = elem["text"]
        categories.append({"category": current_category, "items": []})
    elif elem["tag"] == "li" and current_category:
        item_text = elem["text"]
        categories[-1]["items"].append(item_text)
        all_items.append({
            "category": current_category,
            "item": item_text
        })

# Build the full inventory
inventory = {
    "source": "ehi-export.html",
    "source_url": "https://guides.avonhealth.com/docs/ehi-export",
    "export_format": "ZIP containing CSV files, PDF documents, PNG images",
    "single_patient_export": True,
    "population_export": True,
    "population_export_method": "Email request to support@avonhealth.com",
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "has_field_level_documentation": False,
    "total_categories": len(categories),
    "total_data_items": len(all_items),
    "categories": categories,
    "flat_items": all_items
}

# Write full inventory
output_path = OUTPUT_DIR / "full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"Total categories: {len(categories)}")
for cat in categories:
    print(f"  {cat['category']}: {len(cat['items'])} items")
print(f"Total data items listed: {len(all_items)}")
print(f"\nAll items:")
for item in all_items:
    print(f"  [{item['category']}] {item['item']}")

# Summary stats
stats = {
    "total_categories": len(categories),
    "total_data_items": len(all_items),
    "categories_breakdown": {c["category"]: len(c["items"]) for c in categories},
    "has_field_names": False,
    "has_field_types": False,
    "has_field_descriptions": False,
    "has_relationships": False,
    "has_value_sets": False,
    "has_sample_data": False,
    "documentation_level": "category-level only (no field-level detail)"
}
stats_path = OUTPUT_DIR / "summary-stats.json"
with open(stats_path, "w") as f:
    json.dump(stats, f, indent=2)

print(f"\nOutput written to: {output_path}")
print(f"Stats written to: {stats_path}")
