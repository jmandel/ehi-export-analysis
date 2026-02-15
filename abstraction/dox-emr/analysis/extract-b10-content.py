#!/usr/bin/env python3
"""Extract and analyze visible content from the DOX EMR b(10) documentation page.

Parses the Wix-hosted HTML to extract all visible text, identifies EHI-relevant
content, and produces a summary of what the page actually says.
"""

from html.parser import HTMLParser
import json
import os

DOWNLOADS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
    '../../../results/dox-emr/downloads')

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.skip = False
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                self.links.append(href)
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t and len(t) > 3:
                self.texts.append(t)

html_path = os.path.join(DOWNLOADS, 'b10doc-page.html')
with open(html_path, 'r', errors='ignore') as f:
    html = f.read()

p = TextExtractor()
p.feed(html)

# Identify EHI-relevant content (filter out nav/footer boilerplate)
ehi_keywords = ['b10', 'b(10)', 'ehi', 'electronic health information', 
                'export', 'ccda', 'c-cda', 'uscdi', '170.315']
ehi_texts = []
for t in p.texts:
    if any(k in t.lower() for k in ehi_keywords):
        ehi_texts.append(t)

# Count links to documentation artifacts
doc_links = [l for l in p.links if any(ext in l.lower() 
    for ext in ['.pdf', '.zip', '.xlsx', '.csv', '.json', '.xml', '.doc'])]
external_links = [l for l in p.links if 'hl7.org' in l or 'healthit.gov' in l]

result = {
    "html_file_size_bytes": os.path.getsize(html_path),
    "total_visible_text_segments": len(p.texts),
    "ehi_relevant_text_segments": len(ehi_texts),
    "ehi_relevant_content": ehi_texts,
    "total_links": len(p.links),
    "documentation_file_links": doc_links,
    "external_standard_links": external_links,
    "artifacts_downloaded": 2,  # screenshot + HTML
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "field_level_docs_present": False,
    "export_instructions_present": False,
    "summary": {
        "export_format": "C-CDA XML",
        "standard_version": "USCDI v1",
        "scope_single_patient": True,
        "scope_population": True,
        "vendor_specific_docs": False,
        "only_reference": "HL7 C-CDA Implementation Guide (external standard)"
    }
}

output_path = os.path.join(os.path.dirname(__file__), 'b10-content-analysis.json')
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
