#!/usr/bin/env python3
"""Parse the UMC disclosure page HTML to extract all EHI-related content."""

from html.parser import HTMLParser
import json
import re

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_td = False
        self.in_p = False
        self.tables = []
        self.current_row = []
        self.in_table = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
            self.current_row.append('')
        if tag == 'p':
            self.in_p = True
        if tag == 'table':
            self.in_table = True
            self.tables.append([])

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
        if tag == 'p':
            self.in_p = False
        if tag == 'tr' and self.in_table:
            if self.current_row:
                self.tables[-1].append(self.current_row)
            self.current_row = []
        if tag == 'table':
            self.in_table = False

    def handle_data(self, data):
        stripped = data.strip()
        if stripped:
            self.text_parts.append(stripped)
            if self.in_td and self.current_row:
                self.current_row[-1] += stripped

with open('../downloads/cost-disclosure-and-transparency.html', 'r') as f:
    html = f.read()

parser = TextExtractor()
parser.feed(html)

# Find the EHI export footnote
ehi_texts = [t for t in parser.text_parts if 'EHI' in t or 'b)(10)' in t or 'Electronic Health Information' in t]

# Find all certification criteria mentioned
criteria = [t for t in parser.text_parts if t.startswith('§170.315')]

# Find any links in the page
import re
links = re.findall(r'href="(https?://[^"]+)"', html)
unique_links = sorted(set(links))

results = {
    "ehi_export_texts": ehi_texts,
    "certification_criteria_listed": criteria,
    "external_links": unique_links,
    "total_text_segments": len(parser.text_parts),
    "tables_found": len(parser.tables),
}

with open('disclosure-page-extract.json', 'w') as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
