"""
Build entity-inventory-full.json and entity-inventory-summary.json from the HTML page.
Parses the C-CDA data dictionary table directly from the HTML.
"""
import json
import re
from html.parser import HTMLParser

HTML_PATH = "../downloads/ehi-export-page.html"

class TableExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = None
        self.current_cell = None
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.in_style = False
        self.in_script = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'style': self.in_style = True
        if tag == 'script': self.in_script = True
        if tag == 'table':
            self.in_table = True
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            attrs_dict = dict(attrs)
            self.current_cell = {
                'text': '',
                'tag': tag,
                'rowspan': int(attrs_dict.get('rowspan', 1)),
                'colspan': int(attrs_dict.get('colspan', 1))
            }
            
    def handle_endtag(self, tag):
        if tag == 'style': self.in_style = False
        if tag == 'script': self.in_script = False
        if tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            self.current_cell['text'] = ' '.join(self.current_cell['text'].split())
            self.current_row.append(self.current_cell)
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag == 'table' and self.in_table:
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
                
    def handle_data(self, data):
        if self.in_cell and not self.in_style and not self.in_script:
            self.current_cell['text'] += data

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html_content = f.read()

ext = TableExtractor()
ext.feed(html_content)

assert len(ext.tables) == 1, f"Expected 1 table, found {len(ext.tables)}"
table = ext.tables[0]

# Header row
headers = [c['text'] for c in table[0]]
print(f"Headers: {headers}")
print(f"Total rows (including header): {len(table)}")

# Process rows, handling rowspan for Section Name column
# The first column (Section Name) uses rowspan to group elements
data_rows = table[1:]  # Skip header

# Resolve rowspans: build a normalized grid
grid = []
pending_spans = {}  # col_idx -> (value, remaining_count)

for row_cells in data_rows:
    normalized_row = []
    cell_idx = 0
    col_idx = 0
    
    while col_idx < 4:  # 4 columns
        # Check if there's a pending rowspan for this column
        if col_idx in pending_spans:
            val, remaining = pending_spans[col_idx]
            normalized_row.append(val)
            if remaining <= 1:
                del pending_spans[col_idx]
            else:
                pending_spans[col_idx] = (val, remaining - 1)
            col_idx += 1
        elif cell_idx < len(row_cells):
            cell = row_cells[cell_idx]
            normalized_row.append(cell['text'])
            if cell['rowspan'] > 1:
                pending_spans[col_idx] = (cell['text'], cell['rowspan'] - 1)
            cell_idx += 1
            col_idx += 1
        else:
            normalized_row.append('')
            col_idx += 1
    
    grid.append(normalized_row)

# Build entity inventory organized by section
sections = {}
for row in grid:
    section_name = row[0]
    data_element = row[1]
    entry_xpath = row[2]
    code_system = row[3]
    
    if section_name not in sections:
        sections[section_name] = {
            "section_name": section_name,
            "fields": []
        }
    
    sections[section_name]["fields"].append({
        "data_element": data_element,
        "entry_xpath": entry_xpath,
        "code_system": code_system if code_system else None,
        "has_code_system": bool(code_system and code_system.strip() and code_system.strip() != "NA"),
        "description": None,  # No descriptions provided by vendor
        "data_type": None,    # No data types provided by vendor
    })

# Build full inventory
full_inventory = {
    "source": "https://ehryourway.com/electronic-health-information-export/",
    "export_format": "C-CDA Release 2.1 (August 2015)",
    "export_packaging": "ZIP archive (C-CDA XML + human-readable PDF + attachment PDFs)",
    "export_modes": ["Single Patient Export", "Bulk Export (multiple patients)"],
    "total_sections": len(sections),
    "total_fields": sum(len(s["fields"]) for s in sections.values()),
    "fields_with_code_system": sum(
        1 for s in sections.values() for f in s["fields"] if f["has_code_system"]
    ),
    "fields_with_description": 0,
    "fields_with_data_type": 0,
    "entities": []
}

for section_name, section_data in sections.items():
    entity = {
        "entity_name": section_name,
        "category": classify_section(section_name) if False else None,
        "field_count": len(section_data["fields"]),
        "fields_with_code_system": sum(1 for f in section_data["fields"] if f["has_code_system"]),
        "fields": section_data["fields"]
    }
    full_inventory["entities"].append(entity)

# Classify sections into categories
def classify(name):
    clinical_notes = {"History and Physical Exam Note", "Progress Notes", "Procedure Notes",
                      "Laboratory Notes", "Consultation Notes", "Discharge Summary",
                      "Imaging Narrative", "Pathology Report"}
    if name in clinical_notes:
        return "Clinical Notes"
    if name == "Demographics":
        return "Demographics"
    if name in ("Encounter", "Reason for Visit"):
        return "Encounters"
    if name == "Medication Allergies":
        return "Allergies"
    if name == "Medication Information":
        return "Medications"
    if name == "Problem or Conditions":
        return "Problems"
    if name == "Results":
        return "Lab Results"
    if name == "Social History":
        return "Social History"
    if name == "Vitals":
        return "Vitals"
    if name == "Immunizations":
        return "Immunizations"
    if name == "Procedures":
        return "Procedures"
    if name in ("Assessment", "Reason for Referral", "Plan of Treatment"):
        return "Assessment & Plan"
    if name in ("Functional Status", "Mental Status"):
        return "Health Status"
    if name == "Medical Equipment":
        return "Medical Devices"
    if name in ("Goals", "Health Concerns"):
        return "Goals & Concerns"
    if name == "Care Team":
        return "Care Team"
    return "Other"

for entity in full_inventory["entities"]:
    entity["category"] = classify(entity["entity_name"])

# Build summary
category_summary = {}
for entity in full_inventory["entities"]:
    cat = entity["category"]
    if cat not in category_summary:
        category_summary[cat] = {"section_count": 0, "field_count": 0, "sections": []}
    category_summary[cat]["section_count"] += 1
    category_summary[cat]["field_count"] += entity["field_count"]
    category_summary[cat]["sections"].append(entity["entity_name"])

summary = {
    "total_sections": full_inventory["total_sections"],
    "total_fields": full_inventory["total_fields"],
    "fields_with_code_system": full_inventory["fields_with_code_system"],
    "fields_with_description": 0,
    "fields_with_data_type": 0,
    "pct_fields_with_description": "0%",
    "pct_fields_with_code_system": f"{full_inventory['fields_with_code_system'] / full_inventory['total_fields'] * 100:.1f}%",
    "categories": category_summary,
    "missing_domains": [
        "Billing / Claims / Revenue Cycle",
        "Insurance / Coverage / Eligibility",
        "Payments / Adjustments",
        "Behavioral Health Assessments (PHQ-9, GAD-7, etc.)",
        "Treatment Plans with Outcome Tracking",
        "Custom Forms / Intake Forms",
        "Substance Abuse Treatment Data",
        "PDMP Query Results",
        "Patient Communications / Portal Messages",
        "Uploaded Documents (structured metadata)",
        "Consent Forms",
        "Prior Authorizations",
    ],
    "uscdi_alignment": "The 28 C-CDA sections map closely to USCDI v3 data classes. This export covers the standard clinical exchange surface without extending beyond it."
}

with open('entity-inventory-full.json', 'w') as f:
    json.dump(full_inventory, f, indent=2)

with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\nTotal sections: {full_inventory['total_sections']}")
print(f"Total fields: {full_inventory['total_fields']}")
print(f"Fields with code system: {full_inventory['fields_with_code_system']}")
print(f"Fields with descriptions: 0 (none provided)")
print(f"Fields with data types: 0 (none provided)")
print(f"\nCategories:")
for cat, data in sorted(category_summary.items()):
    print(f"  {cat}: {data['section_count']} sections, {data['field_count']} fields - {data['sections']}")

print("\nSaved entity-inventory-full.json and entity-inventory-summary.json")
