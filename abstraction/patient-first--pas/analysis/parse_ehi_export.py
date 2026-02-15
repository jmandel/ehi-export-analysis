"""Parse the EHI export documentation from Patient First's mandatory disclosure page.
Extracts the export category table and produces structured output."""

import json
from html.parser import HTMLParser

# Parse API JSON (cleaner HTML)
with open("/home/jmandel/hobby/ehi-export-analysis/results/patient-first--pas/downloads/mandatory-disclosure-page-api.json") as f:
    data = json.load(f)

content = data.get("content", {}).get("rendered", "")

# Simple table parser
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.is_header = False
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == "table": self.in_table = True
        elif tag == "tr" and self.in_table: 
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_row:
            self.in_cell = True
            self.is_header = tag == "th"
            self.current_cell = ""
            
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell:
            self.current_row.append(self.current_cell.strip())
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)
            self.in_row = False
        elif tag == "table":
            self.in_table = False
            
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

# Find the EHI section and its table
ehi_idx = content.find("EHI Export")
if ehi_idx == -1:
    print("ERROR: Could not find EHI Export section")
    exit(1)

# Extract from EHI section to the next h3 (SED section)
next_section = content.find("<h3", ehi_idx + 10)
ehi_section = content[ehi_idx:next_section] if next_section > -1 else content[ehi_idx:]

parser = TableParser()
parser.feed(ehi_section)

# Structure the results
headers = parser.rows[0] if parser.rows else []
categories = []
for row in parser.rows[1:]:
    cat = {
        "category": row[0] if len(row) > 0 else "",
        "description": row[1] if len(row) > 1 else "",
        "folder_name": row[2] if len(row) > 2 else "",
        "file_format": row[3] if len(row) > 3 else "",
    }
    categories.append(cat)

result = {
    "source": "mandatory-disclosure-page-api.json",
    "section_title": "Electronic Health Information (EHI) Export",
    "export_description": "EHI Export functionality allows health systems to do a manual one-time export of health data. The export contains the electronic health information available in a patient's record in a computable file format. Some electronic health information might not be available in a computable format, such as PDF documents or images.",
    "export_format": "Compressed ZIP archive",
    "total_categories": len(categories),
    "categories": categories,
    "documentation_elements": {
        "data_dictionary": False,
        "json_schema": False,
        "sample_data": False,
        "user_guide": False,
        "api_documentation": False,
        "field_level_docs": False,
        "relationship_docs": False,
        "value_sets": False,
    }
}

print(json.dumps(result, indent=2))

with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/patient-first--pas/analysis/ehi-export-structure.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"\nSummary:")
print(f"  Categories: {len(categories)}")
print(f"  Formats: {', '.join(set(c['file_format'] for c in categories))}")
print(f"  Has data dictionary: No")
print(f"  Has sample data: No")
print(f"  Has field-level docs: No")
