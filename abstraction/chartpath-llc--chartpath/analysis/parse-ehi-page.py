#!/usr/bin/env python3
"""Parse the ChartPath EHI export page HTML and extract structured content."""
import json
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self._in_body = False
        self._skip = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self._in_body = True
        if tag in ('script', 'style'):
            self._skip = True
            
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._skip = False
            
    def handle_data(self, data):
        if self._in_body and not self._skip:
            text = data.strip()
            if text:
                self.texts.append(text)

with open('../downloads/ehiexport-page.html', 'r') as f:
    html = f.read()

parser = TextExtractor()
parser.feed(html)

# Filter out boilerplate
content_texts = [t for t in parser.texts if t not in (
    'ChartPath_Logo', 'Copyright © 2023 ChartPath. All Rights Reserved.'
) and len(t) > 5]

# Extract the main content paragraphs
paragraphs = []
for t in content_texts:
    t = t.strip()
    if t and len(t) > 10:
        paragraphs.append(t)

result = {
    "source": "downloads/ehiexport-page.html",
    "page_title": "ChartPath Electronic Health Information Export",
    "total_substantive_paragraphs": len(paragraphs),
    "total_word_count": sum(len(p.split()) for p in paragraphs),
    "content_paragraphs": paragraphs,
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_definitions": False,
    "has_download_links": False,
    "export_format_described": {
        "container": "ZIP archive",
        "contents": [
            "Per-encounter PDF documents",
            "Per-encounter C-CDA documents",
            "Face sheet with demographics",
            "Attached files in original format"
        ]
    },
    "documentation_elements_present": {
        "data_dictionary": False,
        "field_level_definitions": False,
        "table_or_entity_listing": False,
        "value_sets_or_code_systems": False,
        "sample_export_files": False,
        "user_guide_or_instructions": False,
        "screenshots": False,
        "api_specification": False,
        "c_cda_template_details": False,
        "relationship_documentation": False
    }
}

print(json.dumps(result, indent=2))

with open('ehi-page-analysis.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\nTotal paragraphs: {result['total_substantive_paragraphs']}")
print(f"Total words: {result['total_word_count']}")
