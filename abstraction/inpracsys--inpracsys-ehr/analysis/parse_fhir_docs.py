"""Parse the InPracSys FHIR API documentation HTML page to extract
all documented resource types and their fields into a structured JSON inventory."""

import json
import re
from html.parser import HTMLParser

with open("downloads/fhir-api-documentation-page.html", "r") as f:
    html = f.read()

# The page uses WordPress with Flavor theme. Content sections are in
# div elements with specific IDs corresponding to the left-nav links.
# Each resource section has tables documenting fields.

# Strategy: find all <table> elements, extract headers and rows,
# and associate them with the nearest preceding heading.

class TableExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = None
        self.current_cell = None
        self.in_cell = False
        self.in_heading = False
        self.current_heading = ""
        self.headings = []
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.in_heading = True
            self.current_heading = ""
        elif tag == 'table':
            self.current_table = {"heading": self.headings[-1] if self.headings else "", "rows": [], "headers": []}
        elif tag == 'tr' and self.current_table is not None:
            self.current_row = []
        elif tag in ('td', 'th') and self.current_row is not None:
            self.current_cell = ""
            self.in_cell = True

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.in_heading = False
            cleaned = self.current_heading.strip()
            if cleaned:
                self.headings.append(cleaned)
        elif tag == 'table' and self.current_table is not None:
            self.tables.append(self.current_table)
            self.current_table = None
        elif tag == 'tr' and self.current_row is not None and self.current_table is not None:
            if not self.current_table["headers"] and self.current_row:
                # Check if this looks like a header row (first row)
                self.current_table["headers"] = self.current_row
            else:
                self.current_table["rows"].append(self.current_row)
            self.current_row = None
        elif tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            if self.current_row is not None:
                self.current_row.append(self.current_cell.strip())
            self.current_cell = None

    def handle_data(self, data):
        if self.in_heading:
            self.current_heading += data
        if self.in_cell and self.current_cell is not None:
            self.current_cell += data

extractor = TableExtractor()
extractor.feed(html)

# Now organize the tables by resource type
# We need to identify which tables are field definition tables
# (vs. parameter tables or sample data tables)

resources = {}
for table in extractor.tables:
    heading = table["heading"]
    headers = [h.lower().strip() for h in table["headers"]]
    
    # Skip tables that don't look like field definitions
    # Field definition tables typically have columns like: Name, Card., Type, Description
    is_field_table = False
    for h in headers:
        if 'name' in h or 'element' in h or 'field' in h:
            is_field_table = True
            break
    
    if not is_field_table:
        continue
    
    # Map heading to resource name
    resource_name = heading
    
    if resource_name not in resources:
        resources[resource_name] = {
            "name": resource_name,
            "fields": [],
            "table_headers": table["headers"]
        }
    
    for row in table["rows"]:
        if len(row) >= 2:
            field = {"name": row[0]}
            # Try to map columns based on headers
            for i, val in enumerate(row[1:], 1):
                if i < len(headers):
                    col_name = headers[i]
                    if 'card' in col_name:
                        field["cardinality"] = val
                    elif 'type' in col_name:
                        field["type"] = val
                    elif 'desc' in col_name or 'definition' in col_name:
                        field["description"] = val
                    elif 'value' in col_name:
                        field["value_set"] = val
                    else:
                        field[col_name] = val
                else:
                    field[f"col_{i}"] = val
            resources[resource_name]["fields"].append(field)

# Print summary
print(f"Found {len(extractor.tables)} tables total")
print(f"Found {len(resources)} resource sections with field definitions")
print()

total_fields = 0
for name, res in resources.items():
    n = len(res["fields"])
    total_fields += n
    print(f"  {name}: {n} fields")

print(f"\nTotal fields: {total_fields}")

# Save full inventory
with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(resources, f, indent=2)

print("\nSaved to analysis/entity-inventory-full.json")
