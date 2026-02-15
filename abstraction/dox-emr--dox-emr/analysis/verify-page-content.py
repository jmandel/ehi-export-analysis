#!/usr/bin/env python3
"""
Verify DOX EMR b10doc page content by extracting visible text from the downloaded HTML.
Confirms what the page actually says vs what prior reports claim.
"""
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t and len(t) > 10:
                self.texts.append(t)

html_path = "/home/jmandel/hobby/ehi-export-analysis/results/dox-emr--dox-emr/downloads/b10doc-page.html"
with open(html_path) as f:
    html = f.read()

parser = TextExtractor()
parser.feed(html)

# Filter to substantive text (skip nav/framework items)
print("=== Extracted visible text from b10doc-page.html ===")
print(f"File size: {len(html):,} bytes")
print()

# Identify the key content area
content_keywords = ['b10', 'EHI', 'CCDA', 'USCDI', '170.315', 'export', 'hl7']
print("--- Key EHI-related content ---")
for t in parser.texts:
    if any(k.lower() in t.lower() for k in content_keywords):
        print(f"  {t}")

print()
print("--- All extracted text (>10 chars) ---")
for i, t in enumerate(parser.texts):
    print(f"  [{i}] {t}")

# Count links
import re
links = re.findall(r'href="([^"]*)"', html)
downloadable = [l for l in links if any(l.endswith(ext) for ext in ['.pdf', '.zip', '.xlsx', '.csv', '.json', '.doc', '.docx', '.xml'])]
print(f"\nTotal links found: {len(links)}")
print(f"Downloadable file links: {len(downloadable)}")
if downloadable:
    for l in downloadable:
        print(f"  {l}")
else:
    print("  (none)")
