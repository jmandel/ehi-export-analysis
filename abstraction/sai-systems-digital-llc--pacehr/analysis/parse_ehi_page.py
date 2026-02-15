"""Parse the PacEHR EHI main page HTML to extract substantive content."""
from html.parser import HTMLParser
import re

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

with open('/home/jmandel/hobby/ehi-export-analysis/results/sai-systems-digital-llc--pacehr/downloads/pacehr-ehi-main-page.html', 'r') as f:
    html = f.read()

# Extract all text
parser = TextExtractor()
parser.feed(html)

# Find the substantive EHI content (filter out navigation/footer boilerplate)
all_text = '\n'.join(parser.text_parts)

# Look for EHI-related content
ehi_keywords = ['EHI', 'Electronic Health Information', 'export', 'designated record', 'bulk', 'FHIR', 'XML', 'patient data']
lines = all_text.split('\n')
relevant = []
for i, line in enumerate(lines):
    if any(kw.lower() in line.lower() for kw in ehi_keywords):
        # Include context
        start = max(0, i-1)
        end = min(len(lines), i+2)
        for j in range(start, end):
            if lines[j] not in relevant:
                relevant.append(lines[j])

print("=== EHI-Related Content ===")
print('\n'.join(relevant))
print(f"\n=== Stats ===")
print(f"Total text segments: {len(parser.text_parts)}")
print(f"HTML file size: {len(html)} bytes")

# Also extract all links
import re
links = re.findall(r'href="([^"]*)"', html)
ehi_links = [l for l in links if any(kw in l.lower() for kw in ['ehi', 'export', 'fhir', 'cures', 'api', 'data', 'dictionary', 'schema'])]
print(f"\nRelevant links found:")
for l in ehi_links:
    print(f"  {l}")
