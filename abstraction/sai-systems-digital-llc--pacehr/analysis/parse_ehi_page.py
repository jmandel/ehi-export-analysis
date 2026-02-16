#!/usr/bin/env python3
"""Parse the main EHI export page to extract substantive content and word counts."""

import json
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/sai-systems-digital-llc--pacehr/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/sai-systems-digital-llc--pacehr/analysis"

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip = False
        self.skip_tags = {'script', 'style', 'head'}
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.text_parts.append(t)

with open(f"{DOWNLOADS}/pacehr-ehi-main-page.html") as f:
    content = f.read()

parser = TextExtractor()
parser.feed(content)

# Filter for substantive text (skip nav, footer boilerplate)
all_text = parser.text_parts

# Find the EHI-specific content by looking for key phrases
ehi_content_start = None
ehi_content_end = None
for i, t in enumerate(all_text):
    if "Electronic Health Information (EHI) All Data Export" in t and ehi_content_start is None:
        ehi_content_start = i
    if "Saisystems Health PALTC Practice Support" in t and i > 10:
        ehi_content_end = i
        break

substantive = all_text[ehi_content_start:ehi_content_end] if ehi_content_start else []
substantive_text = " ".join(substantive)
word_count = len(substantive_text.split())

output = {
    "source_file": "pacehr-ehi-main-page.html",
    "file_size_bytes": len(content),
    "total_text_fragments": len(all_text),
    "substantive_content_fragments": len(substantive),
    "substantive_word_count": word_count,
    "substantive_content": substantive,
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_definitions": False,
    "has_export_instructions": False,
    "has_screenshots": False,
    "links_to_fhir_api": True,
    "claims_xml_format": True,
    "claims_bulk_export": True,
    "claims_single_patient_export": True,
    "mentions_billing": True,  # in the EHI definition
    "documents_billing_export": False  # but not in the technical docs
}

with open(f"{OUTPUT}/ehi-page-analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"EHI Main Page Analysis")
print(f"  File size: {len(content):,} bytes")
print(f"  Substantive content: {len(substantive)} text fragments, {word_count} words")
print(f"  Data dictionary: No")
print(f"  Schema files: No")
print(f"  Sample data: No")
print(f"  Field definitions: No")
print(f"  Export instructions: No")
print(f"\nSubstantive content:")
for line in substantive:
    print(f"  {line}")
