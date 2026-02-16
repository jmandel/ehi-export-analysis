"""Parse the FHIR Documentation HTML to extract all resource types and API details."""
import re
from html.parser import HTMLParser
import json

class FHIRDocParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []
        self.current_resource = None
        self.in_h2 = False
        self.in_h3 = False
        self.in_h5 = False
        self.in_span = False
        self.in_li = False
        self.in_code = False
        self.current_text = ""
        self.section_id = None
        self.all_ids = []
        self.h2_texts = []
        self.h3_texts = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div':
            id_val = attrs_dict.get('id', '')
            if id_val:
                self.all_ids.append(id_val)
                self.section_id = id_val
        if tag == 'h2':
            self.in_h2 = True
            self.current_text = ""
        elif tag == 'h3':
            self.in_h3 = True
            self.current_text = ""
        elif tag == 'h5':
            self.in_h5 = True
            self.current_text = ""
            
    def handle_endtag(self, tag):
        if tag == 'h2':
            self.in_h2 = False
            self.h2_texts.append(self.current_text.strip())
        elif tag == 'h3':
            self.in_h3 = False
            self.h3_texts.append(self.current_text.strip())
        elif tag == 'h5':
            self.in_h5 = False
            
    def handle_data(self, data):
        if self.in_h2 or self.in_h3 or self.in_h5:
            self.current_text += data

with open('/home/jmandel/hobby/ehi-export-analysis/results/cursahealth-llc--cursahealth-ehr/downloads/FHIR-Documentation.html', 'r') as f:
    html = f.read()

parser = FHIRDocParser()
parser.feed(html)

print("=== H2 headings ===")
for h in parser.h2_texts:
    print(f"  {h}")

print(f"\n=== H3 headings ({len(parser.h3_texts)}) ===")
for h in parser.h3_texts:
    print(f"  {h}")

print(f"\n=== Section IDs ({len(parser.all_ids)}) ===")
for i in parser.all_ids:
    print(f"  {i}")

# Also extract resource names using regex on section IDs
resource_ids = [i for i in parser.all_ids if i not in ('root', 'navbarSupportedContent', 'Client_Registration', 'Authorization', 'Scopes')]
print(f"\n=== Likely resource section IDs ({len(resource_ids)}) ===")
for r in resource_ids:
    print(f"  {r}")

# Extract API endpoints using regex
endpoints = re.findall(r'(GET|POST|PUT|DELETE)\s+.*?(/[^\s<"]+)', html)
print(f"\n=== API endpoints ({len(endpoints)}) ===")
for method, path in endpoints[:50]:
    print(f"  {method} {path}")

