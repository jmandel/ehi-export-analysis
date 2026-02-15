"""Parse the FHIR API documentation page to extract resource types, endpoints, and field details."""
from html.parser import HTMLParser
import re

with open('/home/jmandel/hobby/ehi-export-analysis/results/sai-systems-digital-llc--pacehr/downloads/cures-update-fhir-api-docs.html', 'r') as f:
    html = f.read()

# Extract headings to find resource sections
headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.DOTALL|re.IGNORECASE)
headings_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]

print("=== All Headings ===")
for h in headings_clean:
    if h:
        print(f"  - {h}")

# Find FHIR resource references
fhir_resources = re.findall(r'(?:hl7\.org/fhir/|fhir\.org/)(?:STU3/|R4/|DSTU2/)?([A-Z][a-zA-Z]+)', html)
unique_resources = sorted(set(fhir_resources))
print(f"\n=== FHIR Resources Referenced ({len(unique_resources)}) ===")
for r in unique_resources:
    print(f"  - {r}")

# Find API endpoints
endpoints = re.findall(r'(?:GET|POST|PUT|DELETE)\s+[/\w{}\-]+', html)
print(f"\n=== API Endpoints ({len(endpoints)}) ===")
for e in sorted(set(endpoints)):
    print(f"  - {e}")

# Find table-like structures for USCDI mappings  
# Look for USCDI data element mentions
uscdi_elements = re.findall(r'(?:USCDI|US Core)\s*(?:v\d+)?\s*(?:Data\s*(?:Class|Element))?\s*[:\-]?\s*([^<\n]{5,80})', html, re.IGNORECASE)
if uscdi_elements:
    print(f"\n=== USCDI Element References ===")
    for e in uscdi_elements[:20]:
        print(f"  - {e.strip()}")

# Count search parameters documented
search_params = re.findall(r'[?&](\w+)=', html)
unique_params = sorted(set(search_params))
print(f"\n=== Search Parameters ({len(unique_params)}) ===")
for p in unique_params:
    print(f"  - {p}")

# Check for any data dictionary / field definitions
tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL|re.IGNORECASE)
print(f"\n=== HTML Tables Found: {len(tables)} ===")
for i, t in enumerate(tables):
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.DOTALL|re.IGNORECASE)
    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', t, re.DOTALL|re.IGNORECASE)
    cells_clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells[:10]]
    print(f"  Table {i+1}: {len(rows)} rows, first cells: {cells_clean}")

# Save the full text for reference
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_script = False
        self.in_style = False
    def handle_starttag(self, tag, attrs):
        if tag == 'script': self.in_script = True
        if tag == 'style': self.in_style = True
    def handle_endtag(self, tag):
        if tag == 'script': self.in_script = False
        if tag == 'style': self.in_style = False
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            text = data.strip()
            if text:
                self.text_parts.append(text)

parser = TextExtractor()
parser.feed(html)
full_text = '\n'.join(parser.text_parts)
with open('fhir_api_docs_text.txt', 'w') as f:
    f.write(full_text)
print(f"\nFull text saved to fhir_api_docs_text.txt ({len(full_text)} chars)")
