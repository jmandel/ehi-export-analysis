#!/usr/bin/env python3
"""Parse the Avon Health EHI export HTML page and extract structured data categories/fields."""

from html.parser import HTMLParser
import json
import re

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
        if tag in ('br', 'p', 'div', 'h1', 'h2', 'h3', 'h4', 'li'):
            self.text_parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            self.text_parts.append(data)

with open('downloads/ehi-export.html') as f:
    html = f.read()

e = TextExtractor()
e.feed(html)
full_text = ''.join(e.text_parts)

# Extract the data categories section
categories = []
current_category = None

lines = full_text.split('\n')
in_data_section = False
for line in lines:
    line = line.strip()
    if not line:
        continue
    if 'Data Categories Included' in line:
        in_data_section = True
        continue
    if in_data_section:
        # Stop at "Next" or navigation
        if line.startswith('Next') or line in ('Getting started', '→', 'On this page'):
            break
        # Category headers (Demographics, Clinical Information, etc.)
        if line in ('Demographics', 'Clinical Information', 'Administrative and Billing Information', 'Other Documents'):
            current_category = {"name": line, "fields": []}
            categories.append(current_category)
        elif current_category is not None:
            # Clean up field text
            field = line.strip()
            if field and not field.startswith('The export includes'):
                current_category["fields"].append(field)

# Build the entity inventory
entities = []
total_fields = 0
for cat in categories:
    entity = {
        "entity_name": cat["name"],
        "category": cat["name"],
        "fields": [],
        "field_count": len(cat["fields"])
    }
    for f in cat["fields"]:
        entity["fields"].append({
            "name": f,
            "type": None,
            "description": None,
            "has_description": False
        })
    entities.append(entity)
    total_fields += len(cat["fields"])

# Output full inventory
inventory = {
    "source": "downloads/ehi-export.html",
    "source_url": "https://guides.avonhealth.com/docs/ehi-export",
    "extraction_notes": "This is NOT a data dictionary. The vendor provides only category names with high-level bullet-point field labels. No CSV column names, data types, descriptions, relationships, or value sets are documented.",
    "total_categories": len(entities),
    "total_fields_listed": total_fields,
    "fields_with_types": 0,
    "fields_with_descriptions": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "entities": entities
}

with open('analysis/entity-inventory-full.json', 'w') as f:
    json.dump(inventory, f, indent=2)

# Summary
summary = {
    "source": inventory["source"],
    "has_data_dictionary": False,
    "total_categories": len(entities),
    "total_fields_listed": total_fields,
    "fields_with_types": 0,
    "fields_with_descriptions": 0,
    "pct_fields_with_descriptions": 0,
    "categories": []
}
for ent in entities:
    summary["categories"].append({
        "name": ent["entity_name"],
        "field_count": ent["field_count"],
        "fields": [f["name"] for f in ent["fields"]]
    })

with open('analysis/entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Categories: {len(entities)}")
print(f"Total fields listed: {total_fields}")
print(f"Fields with types: 0")
print(f"Fields with descriptions: 0")
print()
for cat in categories:
    print(f"  {cat['name']}: {len(cat['fields'])} items")
    for f in cat['fields']:
        print(f"    - {f}")
