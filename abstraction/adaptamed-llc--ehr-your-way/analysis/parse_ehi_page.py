#!/usr/bin/env python3
"""
Parse the EHR Your Way EHI export HTML page.
Extracts the C-CDA data dictionary table and computes summary statistics.
Outputs full-entity-inventory.json and summary-stats.json.
"""

import json
import sys
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/adaptamed-llc--ehr-your-way/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/adaptamed-llc--ehr-your-way/analysis"

class TableExtractor(HTMLParser):
    """Extract all <table> content from HTML."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = ""
        self.skip = False
        self.skip_tags = {'script', 'style'}

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
        elif tag == 'table':
            self.in_table = True
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
        elif tag == 'table':
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
            self.current_cell = ""

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_cell:
            self.current_cell += data


with open(f"{RESULTS_DIR}/ehi-export-page.html", "r") as f:
    html = f.read()

extractor = TableExtractor()
extractor.feed(html)

# Find the C-CDA data dictionary table (has "Section Name" header)
ccda_table = None
for table in extractor.tables:
    if table and len(table[0]) >= 4:
        headers = [h.strip().lower() for h in table[0]]
        if 'section name' in headers:
            ccda_table = table
            break

if not ccda_table:
    print("ERROR: Could not find C-CDA data dictionary table")
    sys.exit(1)

headers = [h.strip() for h in ccda_table[0]]
print(f"Table headers: {headers}")
print(f"Total rows (including header): {len(ccda_table)}")
print(f"Data rows: {len(ccda_table) - 1}")

# Parse each row into structured data
sections = {}
all_elements = []

for row in ccda_table[1:]:
    if len(row) < 4:
        continue
    section_name = row[0].strip()
    data_element = row[1].strip()
    entry_xpath = row[2].strip()
    code_system = row[3].strip()

    element = {
        "section": section_name,
        "data_element": data_element,
        "entry_xpath": entry_xpath,
        "code_system": code_system if code_system else None,
        "has_code_system": bool(code_system and code_system != "NA"),
        "has_xpath": bool(entry_xpath),
    }
    all_elements.append(element)

    if section_name not in sections:
        sections[section_name] = []
    sections[section_name].append(element)

# Build full entity inventory
inventory = {
    "source": "https://ehryourway.com/electronic-health-information-export/",
    "export_format": "C-CDA Release 2.1 (HL7 CDA R2, DSTU 2.1, August 2015)",
    "export_packaging": "ZIP archive (C-CDA XML + human-readable PDF + attachments)",
    "export_modes": ["Single Patient Export", "Bulk Export (multiple patients)"],
    "model_type": "standard_projection",
    "standard": "C-CDA",
    "total_sections": len(sections),
    "total_data_elements": len(all_elements),
    "elements_with_code_system": sum(1 for e in all_elements if e["has_code_system"]),
    "elements_with_xpath": sum(1 for e in all_elements if e["has_xpath"]),
    "sections": {}
}

for section_name, elements in sections.items():
    inventory["sections"][section_name] = {
        "element_count": len(elements),
        "elements_with_code_system": sum(1 for e in elements if e["has_code_system"]),
        "elements": elements
    }

# Summary stats
summary = {
    "total_sections": len(sections),
    "total_data_elements": len(all_elements),
    "elements_with_code_system": sum(1 for e in all_elements if e["has_code_system"]),
    "elements_without_code_system": sum(1 for e in all_elements if not e["has_code_system"]),
    "elements_with_xpath": sum(1 for e in all_elements if e["has_xpath"]),
    "has_data_types": False,
    "has_descriptions": False,
    "has_value_sets": False,
    "has_cardinality": False,
    "has_relationships": False,
    "has_sample_data": False,
    "section_breakdown": []
}

for section_name, elements in sections.items():
    summary["section_breakdown"].append({
        "section": section_name,
        "element_count": len(elements),
        "with_code_system": sum(1 for e in elements if e["has_code_system"]),
    })

# Categorize sections by clinical domain type
clinical_sections = [
    "Encounter", "Medication Allergies", "Medication Information",
    "Problem or Conditions", "Results", "Social History", "Vitals",
    "Immunizations", "Procedures", "Assessment", "Plan of Treatment",
    "Functional Status", "Mental Status", "Medical Equipment",
    "Goals", "Health Concerns", "Care Team", "Reason for Visit",
    "Reason for Referral"
]
note_sections = [
    "History and Physical Exam Note", "Progress Notes", "Procedure Notes",
    "Laboratory Notes", "Consultation Notes", "Discharge Summary",
    "Imaging Narrative", "Pathology Report"
]
demographic_sections = ["Demographics"]

summary["domain_grouping"] = {
    "demographics": {
        "sections": [s for s in demographic_sections if s in sections],
        "total_elements": sum(len(sections[s]) for s in demographic_sections if s in sections)
    },
    "clinical": {
        "sections": [s for s in clinical_sections if s in sections],
        "total_elements": sum(len(sections[s]) for s in clinical_sections if s in sections)
    },
    "clinical_notes": {
        "sections": [s for s in note_sections if s in sections],
        "total_elements": sum(len(sections[s]) for s in note_sections if s in sections)
    }
}

# Write outputs
with open(f"{OUTPUT_DIR}/full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)
print(f"\nWrote full-entity-inventory.json")

with open(f"{OUTPUT_DIR}/summary-stats.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote summary-stats.json")

# Print summary
print(f"\n=== SUMMARY ===")
print(f"Total sections: {len(sections)}")
print(f"Total data elements: {len(all_elements)}")
print(f"Elements with code system OIDs: {summary['elements_with_code_system']}")
print(f"Elements without code system: {summary['elements_without_code_system']}")
print(f"\nDocumentation characteristics:")
print(f"  Data types documented: NO")
print(f"  Descriptions documented: NO (only element names)")
print(f"  Value sets enumerated: NO (only OIDs)")
print(f"  Cardinality documented: NO")
print(f"  Relationships documented: NO")
print(f"  Sample data provided: NO")

print(f"\n=== SECTION BREAKDOWN ===")
for s in summary["section_breakdown"]:
    print(f"  {s['section']}: {s['element_count']} elements ({s['with_code_system']} with code systems)")

print(f"\n=== DOMAIN GROUPING ===")
for domain, info in summary["domain_grouping"].items():
    print(f"  {domain}: {len(info['sections'])} sections, {info['total_elements']} elements")
