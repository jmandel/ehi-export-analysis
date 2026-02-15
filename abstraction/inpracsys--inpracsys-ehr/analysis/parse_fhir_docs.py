"""Parse the InPracSys FHIR API documentation HTML to extract resource types, fields, and structure."""

from html.parser import HTMLParser
import json
import re

class FHIRDocParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.current_cell_text = ""
        self.tables = []
        self.current_table = []
        self.in_h2 = False
        self.in_h3 = False
        self.in_h4 = False
        self.current_heading = ""
        self.headings = []
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag in ('h1', 'h2', 'h3', 'h4'):
            setattr(self, f'in_{tag}' if tag != 'h1' else 'in_h2', True)
            self.current_heading = ""
        if tag == 'table':
            self.in_table = True
            self.current_table = []
        if tag == 'tr':
            self.in_row = True
            self.current_row = []
        if tag in ('td', 'th'):
            self.in_cell = True
            self.current_cell_text = ""

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.headings.append({"level": tag, "text": self.current_heading.strip()})
            setattr(self, f'in_{tag}' if tag != 'h1' else 'in_h2', False)
        if tag in ('td', 'th'):
            self.in_cell = False
            self.current_row.append(self.current_cell_text.strip())
        if tag == 'tr':
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        if tag == 'table':
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_text += data
        if any(getattr(self, f'in_{h}', False) for h in ('h2', 'h3', 'h4')):
            self.current_heading += data


with open("/home/jmandel/hobby/ehi-export-analysis/results/inpracsys--inpracsys-ehr/downloads/fhir-api-documentation-page.html") as f:
    html = f.read()

parser = FHIRDocParser()
parser.feed(html)

print("=== HEADINGS ===")
for h in parser.headings:
    print(f"  {h['level']}: {h['text'][:120]}")

print(f"\n=== TABLES: {len(parser.tables)} total ===")

# Analyze tables for field definitions
resource_tables = []
for i, table in enumerate(parser.tables):
    if len(table) > 1:
        header = table[0]
        # Look for field definition tables (usually have columns like Element, Card., Type, Description)
        header_lower = [h.lower() for h in header]
        is_field_table = any(k in ' '.join(header_lower) for k in ['element', 'card', 'type', 'description', 'field'])
        if is_field_table or len(header) >= 3:
            print(f"\nTable {i}: {len(table)-1} data rows, header: {header[:6]}")
            # Count fields
            resource_tables.append({
                "table_index": i,
                "header": header,
                "row_count": len(table) - 1,
                "sample_rows": table[1:3]
            })

# Parse more carefully: find sections that correspond to FHIR resources
print("\n=== RESOURCE ANALYSIS ===")

# Look for patterns like endpoint URLs in the HTML
import re
endpoints = re.findall(r'(?:GET|POST)\s+(/\w+(?:/\w+)*)', html)
unique_endpoints = sorted(set(endpoints))
print(f"\nEndpoints found: {len(unique_endpoints)}")
for ep in unique_endpoints:
    print(f"  {ep}")

# Find all resource type references
resource_types = re.findall(r'"resourceType"\s*:\s*"(\w+)"', html)
unique_resources = sorted(set(resource_types))
print(f"\nFHIR resource types in samples: {len(unique_resources)}")
for rt in unique_resources:
    print(f"  {rt}")

# Save full analysis
output = {
    "heading_count": len(parser.headings),
    "table_count": len(parser.tables),
    "headings": parser.headings,
    "resource_tables": resource_tables,
    "endpoints": unique_endpoints,
    "resource_types_in_samples": unique_resources
}

with open("fhir_doc_structure.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nFull structure saved to fhir_doc_structure.json")
