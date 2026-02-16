#!/usr/bin/env python3
"""
Parse the EHI Export section from the Patient First mandatory disclosure page.
Extracts the export categories table and produces a structured JSON inventory.
"""

import json
import re
from html.parser import HTMLParser

INPUT_FILE = "../../../results/patient-first--pas/downloads/mandatory-disclosure-page-api.json"
OUTPUT_FILE = "full-entity-inventory.json"

# Load the WordPress API JSON
with open(INPUT_FILE) as f:
    data = json.load(f)

html_content = data["content"]["rendered"]

# Extract the EHI Export section
ehi_start = html_content.find("Electronic Health Information (EHI) Export")
if ehi_start == -1:
    raise ValueError("Could not find EHI Export section")

# Find the table after the EHI section
table_start = html_content.find("<table>", ehi_start)
# Find the end of the next section (SED)
next_section = html_content.find("Safety Enhanced Design", ehi_start)
ehi_section = html_content[ehi_start:next_section] if next_section != -1 else html_content[ehi_start:]

# Extract the descriptive paragraph
p_match = re.search(r'<p>(.*?)</p>', ehi_section, re.DOTALL)
description_text = ""
if p_match:
    description_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()

# Find all paragraphs before the table
paragraphs = re.findall(r'<p>(.*?)</p>', ehi_section, re.DOTALL)
full_description = " ".join(re.sub(r'<[^>]+>', '', p).strip() for p in paragraphs)

# Parse the table
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.is_header = False
        self.current_cell = ""
        self.current_row = []
        self.rows = []
        self.headers = []
    
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_row:
            self.in_cell = True
            self.is_header = (tag == "th")
            self.current_cell = ""
    
    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if self.is_header:
                self.headers = self.current_row
            else:
                self.rows.append(self.current_row)
        elif tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
    
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data
    
    def handle_entityref(self, name):
        if self.in_cell:
            entities = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'", "nbsp": " "}
            self.current_cell += entities.get(name, f"&{name};")
    
    def handle_charref(self, name):
        if self.in_cell:
            if name.startswith('x'):
                self.current_cell += chr(int(name[1:], 16))
            else:
                self.current_cell += chr(int(name))

# Parse the EHI table specifically
table_html = ehi_section[ehi_section.find("<table>"):ehi_section.find("</table>") + len("</table>")]
parser = TableParser()
parser.feed(table_html)

# Build structured inventory
categories = []
for row in parser.rows:
    if len(row) >= 4:
        categories.append({
            "category": row[0].strip(),
            "description": row[1].strip(),
            "folder_name": row[2].strip(),
            "file_format": row[3].strip(),
        })

# Build the full inventory
inventory = {
    "source": "Patient First mandatory disclosure page (WordPress API JSON)",
    "source_url": "https://www.patientfirst.com/mandatory-disclosure-for-ehr",
    "source_file": "downloads/mandatory-disclosure-page-api.json",
    "page_last_modified": data.get("modified", "unknown"),
    "export_description": full_description,
    "export_format": "ZIP archive",
    "export_mechanism": "Manual one-time export",
    "total_categories": len(categories),
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_level_documentation": False,
    "categories": categories,
    "notes": [
        "No data dictionary or schema is provided for any export category.",
        "No sample export files are provided.",
        "No field-level documentation exists for any category.",
        "The 'Medical Records' category uses C-CDA, which is a standard with external specs.",
        "The 'Financials' category uses JSON with no schema or field definitions documented.",
        "The 'Scanned Images' folder has subfolders per document type (e.g., InsCard, PhotoID).",
        "RWT Measure #3 labels b(10) metric as 'Number of C-CDA Batch Exports Sent', conflating EHI export with C-CDA batch export."
    ]
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"Export categories found: {len(categories)}")
print(f"Table headers: {parser.headers}")
print()
for cat in categories:
    print(f"  {cat['category']:20s}  {cat['file_format']:20s}  Folder: {cat['folder_name']}")
print()
print(f"Data dictionary: NO")
print(f"Schema files: NO")
print(f"Sample data: NO")
print(f"Field-level docs: NO")
print(f"\nOutput written to {OUTPUT_FILE}")
