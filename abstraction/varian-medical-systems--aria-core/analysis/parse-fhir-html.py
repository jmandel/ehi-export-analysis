#!/usr/bin/env python3
"""Parse the FHIR API documentation HTML to extract USCDI-to-FHIR mapping table."""
from html.parser import HTMLParser
import json
import re

with open("../downloads/fhir-api-documentation.html", "r", errors="replace") as f:
    html = f.read()

# Extract the USCDI mapping table
# Find lines with USCDI table content
lines = html.split("\n")
in_table = False
table_rows = []
current_row = []
current_cell = ""

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = ""
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.table_count = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
            self.table_count += 1
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_row:
            self.in_cell = True
            self.current_cell = ""
            
    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
        elif tag == "tr" and self.in_table:
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
            
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

parser = TableParser()
parser.feed(html)

print(f"Total tables found: {parser.table_count}")
print(f"Tables with content: {len(parser.tables)}")

# Find the USCDI mapping table
uscdi_table = None
for i, table in enumerate(parser.tables):
    if table and any("USCDI" in str(row) for row in table[:3]):
        uscdi_table = table
        print(f"\nUSCDI table found at index {i}, rows: {len(table)}")
        break

if uscdi_table:
    print("\nUSCDI Mapping Table:")
    for row in uscdi_table:
        print(f"  {row}")
else:
    print("\nNo explicit USCDI table found. Searching for mapping content...")
    # Look for mapping patterns in all tables
    for i, table in enumerate(parser.tables):
        if len(table) > 2:
            print(f"\nTable {i} ({len(table)} rows):")
            for row in table[:5]:
                print(f"  {row}")
            if len(table) > 5:
                print(f"  ... ({len(table) - 5} more rows)")

# Check for any b(10) or EHI references
ehi_refs = []
for line_num, line in enumerate(lines, 1):
    lower = line.lower()
    if "b)(10" in lower or "ehi" in lower.split() or "electronic health information" in lower or "designated record" in lower:
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            ehi_refs.append({"line": line_num, "text": clean[:200]})

print(f"\n=== EHI / b(10) References ===")
if ehi_refs:
    for ref in ehi_refs:
        print(f"  Line {ref['line']}: {ref['text']}")
else:
    print("  None found")

# Check for bulk export section
bulk_refs = []
for line_num, line in enumerate(lines, 1):
    lower = line.lower()
    if "bulk" in lower and ("export" in lower or "$export" in lower):
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean and len(clean) > 5:
            bulk_refs.append({"line": line_num, "text": clean[:200]})

print(f"\n=== Bulk Export References ===")
for ref in bulk_refs[:10]:
    print(f"  Line {ref['line']}: {ref['text']}")

# Save
output = {
    "total_tables": parser.table_count,
    "tables_with_content": len(parser.tables),
    "ehi_b10_references": ehi_refs,
    "bulk_export_references": bulk_refs[:10],
    "uscdi_table": uscdi_table
}
with open("fhir-html-analysis.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved to fhir-html-analysis.json")
