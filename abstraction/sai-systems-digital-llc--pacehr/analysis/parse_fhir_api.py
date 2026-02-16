"""Parse the FHIR API documentation page to extract all documented resources and their data elements."""
import re
from html.parser import HTMLParser
import json

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'):
            self.skip = True
        if tag in ('br', 'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr', 'td', 'th'):
            self.text.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

with open('../downloads/cures-update-fhir-api-docs.html') as f:
    html = f.read()

p = TextExtractor()
p.feed(html)
text = ''.join(p.text)

# Split into lines and clean
lines = [l.strip() for l in text.split('\n') if l.strip()]

# Find FHIR Resource sections
resources = []
current_resource = None
current_elements = []

for i, line in enumerate(lines):
    if line.startswith('FHIR Resource'):
        if current_resource:
            resources.append({'resource': current_resource, 'elements': current_elements})
        # Next non-empty line is the resource name
        # Look at the rest of this line and subsequent lines
        rest = line.replace('FHIR Resource:', '').replace('FHIR Resource', '').strip()
        if rest:
            current_resource = rest
        else:
            # Check next line
            if i+1 < len(lines):
                current_resource = lines[i+1]
        current_elements = []
    elif line.startswith('(USCDI') and current_resource:
        # This is a USCDI element tag, the previous line is the element name
        if current_elements:
            current_elements[-1]['uscdi'] = line
        elif i > 0:
            current_elements.append({'name': lines[i-1], 'uscdi': line})

# Capture last resource
if current_resource:
    resources.append({'resource': current_resource, 'elements': current_elements})

# Now let's do a more thorough parse - find USCDI data elements per resource
# Look for patterns like element names followed by (USCDI vX)
print("=== FHIR Resources Documented ===")
for r in resources:
    print(f"\n{r['resource']}:")
    for e in r['elements']:
        print(f"  - {e['name']} {e.get('uscdi','')}")

# Also count all unique resource types from endpoint paths
endpoint_resources = set()
for line in lines:
    m = re.match(r'^/(\w+)/', line)
    if m:
        endpoint_resources.add(m.group(1))

print(f"\n=== Endpoint Resource Types ({len(endpoint_resources)}) ===")
for r in sorted(endpoint_resources):
    print(f"  {r}")

# Build the full inventory
print("\n\n=== Full text around FHIR resources ===")
for i, line in enumerate(lines):
    if 'FHIR Resource' in line:
        start = max(0, i)
        end = min(len(lines), i+30)
        print(f"\n--- Section at line {i} ---")
        for j in range(start, end):
            print(f"  {j}: {lines[j]}")
