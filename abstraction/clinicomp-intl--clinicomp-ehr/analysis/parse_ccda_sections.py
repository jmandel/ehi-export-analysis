#!/usr/bin/env python3
"""Parse the EHI export HTML page to extract C-CDA sections and export format details."""

from html.parser import HTMLParser
import json

HTML_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/clinicomp-intl--clinicomp-ehr/downloads/ehi-data-export-details.html"

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
        if tag in ('br', 'p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'tr'):
            self.text_parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            self.text_parts.append(data)

with open(HTML_PATH, 'r') as f:
    html = f.read()

parser = ContentExtractor()
parser.feed(html)
text = ''.join(parser.text_parts)

# Extract C-CDA sections from the page
# The sections are listed in the page between "The C-CDA files may consist of the following sections:" 
# and "Customers can choose to export"
start_marker = "following sections:"
end_marker = "Customers can choose"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx >= 0 and end_idx >= 0:
    sections_text = text[start_idx + len(start_marker):end_idx]
    # Extract section names - they're listed as individual items
    sections = [s.strip() for s in sections_text.split('\n') if s.strip()]
    # Remove duplicates while preserving order
    seen = set()
    unique_sections = []
    for s in sections:
        if s not in seen:
            seen.add(s)
            unique_sections.append(s)
    
    print(f"C-CDA Sections listed on EHI Export page: {len(unique_sections)}")
    for i, s in enumerate(unique_sections, 1):
        print(f"  {i}. {s}")
else:
    unique_sections = []
    print("Could not find C-CDA sections in page")

# Extract export format details
export_start = text.find("Export Formats")
export_end = text.find("Explore the CliniComp")
if export_start >= 0:
    export_text = text[export_start:export_end if export_end >= 0 else export_start + 1000]
    print(f"\nExport Format Section:")
    for line in export_text.split('\n'):
        line = line.strip()
        if line:
            print(f"  {line}")

# Save results
output = {
    "ccda_sections": unique_sections,
    "ccda_section_count": len(unique_sections),
    "export_formats": [
        "C-CDA v1.0 XML",
        "HTML / web page format",
        "FHIR DocumentReference (single patient)",
        "FHIR Bulk Data EHI Export (C-CDA 2.1 XML)"
    ],
    "scope": "Single patient or all patients within selected time range"
}

with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/clinicomp-intl--clinicomp-ehr/analysis/ccda_sections.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to ccda_sections.json")
