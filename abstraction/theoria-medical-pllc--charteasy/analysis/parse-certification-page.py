#!/usr/bin/env python3
"""Parse the ChartEasy ONC certification page to extract all structured content."""

import json
import re
from html.parser import HTMLParser

html_path = "../downloads/ehr-certificate-page.html"

with open(html_path, "r") as f:
    html_content = f.read()

# Extract text content between body tags
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_script = False
        self.in_style = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_script = True
    
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_script = False
    
    def handle_data(self, data):
        if not self.in_script:
            text = data.strip()
            if text:
                self.texts.append(text)

extractor = TextExtractor()
extractor.feed(html_content)

# Extract certification criteria badges
criteria_pattern = r'170\.315\([a-z]\)\(\d+\)'
criteria = re.findall(criteria_pattern, html_content)
criteria = sorted(set(criteria))

# Extract all links
link_pattern = r'href="([^"]*)"'
links = re.findall(link_pattern, html_content)
pdf_links = [l for l in links if l.endswith('.pdf')]
external_links = [l for l in links if l.startswith('http')]

# Extract the b(10) statement
b10_pattern = r'Support for EHI Export.*?Should you have any questions or require further information, please don&#x27;t hesitate to reach out to our team\.'
b10_match = re.search(b10_pattern, html_content, re.DOTALL)
b10_text = ""
if b10_match:
    # Clean HTML tags
    b10_text = re.sub(r'<[^>]+>', ' ', b10_match.group())
    b10_text = re.sub(r'\s+', ' ', b10_text).strip()
    b10_text = b10_text.replace("&#x27;", "'")

result = {
    "page_file": "downloads/ehr-certificate-page.html",
    "page_size_bytes": len(html_content),
    "certification_criteria_count": len(criteria),
    "certification_criteria": criteria,
    "pdf_links": pdf_links,
    "pdf_link_count": len(pdf_links),
    "external_links": external_links,
    "b10_statement": {
        "found": bool(b10_text),
        "word_count": len(b10_text.split()) if b10_text else 0,
        "text": b10_text,
        "export_formats_mentioned": ["PDF", "CCDA"],
        "export_mechanisms": [
            "ChartEasy Patient Portal (web and iOS)",
            "Email request to records@theoriamedical.com"
        ],
        "data_dictionary_present": False,
        "schema_present": False,
        "sample_data_present": False,
        "field_level_documentation": False,
    },
    "documentation_artifacts": {
        "data_dictionary": None,
        "schema_files": None,
        "sample_exports": None,
        "format_specifications": None,
        "api_documentation": None,
    },
    "all_text_content": extractor.texts,
}

print(json.dumps(result, indent=2))
