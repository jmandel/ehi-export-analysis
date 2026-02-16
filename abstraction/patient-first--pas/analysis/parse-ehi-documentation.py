#!/usr/bin/env python3
"""Parse Patient First EHI export documentation from the WordPress API JSON.

Extracts the EHI export section (paragraph + table) from the mandatory disclosure page
and produces structured JSON output for entity-inventory-full.json and summary stats.
"""

import json
import re
from html.parser import HTMLParser

# Load the WordPress API JSON
with open("../downloads/mandatory-disclosure-page-api.json") as f:
    data = json.load(f)

content = data["content"]["rendered"]

# Extract the EHI export description paragraph
ehi_match = re.search(
    r'Electronic Health Information \(EHI\) Export\s*</h\d>\s*<p>(.*?)</p>',
    content, re.DOTALL | re.IGNORECASE
)
# Broader match: look for the paragraph near "EHI Export"
if not ehi_match:
    ehi_match = re.search(
        r'EHI Export functionality(.*?)(?=<table)',
        content, re.DOTALL | re.IGNORECASE
    )

description_html = ehi_match.group(0) if ehi_match else ""
description_text = re.sub(r'<[^>]+>', '', description_html).strip()
description_text = re.sub(r'&#8217;', "'", description_text)

# Parse the export categories table
table_match = re.search(
    r'EHI Export.*?(<table.*?</table>)',
    content, re.DOTALL | re.IGNORECASE
)

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""
        elif tag == "tr":
            self.current_row = []

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

parser = TableParser()
parser.feed(table_match.group(1))

headers = parser.rows[0]
categories = []
for row in parser.rows[1:]:
    entry = {}
    for i, h in enumerate(headers):
        key = h.lower().replace(" ", "_")
        entry[key] = row[i] if i < len(row) else ""
    categories.append(entry)

# Build entity inventory
# For Patient First, the "entities" are the 7 export categories.
# There is no field-level documentation, so each entity has no fields enumerated.
entities = []
for cat in categories:
    entity = {
        "entity_name": cat.get("category", ""),
        "description": cat.get("description", ""),
        "folder_name": cat.get("folder_name", ""),
        "file_format": cat.get("file_format", ""),
        "fields": [],  # No field-level documentation exists
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "vendor_category": "EHI Export",
        "notes": "No field-level documentation provided. Only category-level description available."
    }
    entities.append(entity)

# Build full inventory
inventory = {
    "product": "PAS",
    "developer": "Patient First",
    "source_artifact": "downloads/mandatory-disclosure-page-api.json",
    "source_url": "https://www.patientfirst.com/mandatory-disclosure-for-ehr",
    "export_description": description_text,
    "documentation_level": "category-level only (no field-level documentation)",
    "total_categories": len(entities),
    "total_fields_documented": 0,
    "entities": entities
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Build summary
summary = {
    "product": "PAS",
    "developer": "Patient First",
    "total_export_categories": len(entities),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "documentation_level": "category-level only",
    "categories": [
        {
            "name": e["entity_name"],
            "description": e["description"],
            "folder": e["folder_name"],
            "format": e["file_format"],
            "field_count": 0
        }
        for e in entities
    ],
    "export_formats": list(set(e["file_format"] for e in entities)),
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_descriptions": False,
    "has_value_sets": False,
    "has_relationships": False
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Export description: {description_text[:200]}...")
print(f"\nCategories found: {len(entities)}")
for e in entities:
    print(f"  - {e['entity_name']}: {e['description']} [{e['file_format']}] -> {e['folder_name']}/")
print(f"\nField-level documentation: NONE")
print(f"Data dictionary: NO")
print(f"Schema files: NO")
print(f"Sample data: NO")
