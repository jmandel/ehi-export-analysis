#!/usr/bin/env python3
"""Parse the B10_MedicsCloud.html page and extract structured content."""

from html.parser import HTMLParser
import json
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/advanced-data-systems-corporation--medicscloud/downloads"
HTML_PATH = os.path.join(DOWNLOADS, "B10_MedicsCloud.html")

class B10Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_chunks = []
        self.links = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.links.append(value.strip())

    def handle_data(self, data):
        stripped = data.strip()
        if stripped:
            self.text_chunks.append(stripped)

with open(HTML_PATH, "r") as f:
    html = f.read()

parser = B10Parser()
parser.feed(html)

# Extract key content
result = {
    "file": "B10_MedicsCloud.html",
    "file_size_bytes": len(html.encode("utf-8")),
    "vendor": "Advanced Data Systems Corporation",
    "product": "MedicsCloud, Version 11.0",
    "section_title": "§ 170.315 (b)(10) Electronic Health Information export",
    "substantive_text": (
        "MedicsCloud authorized users can generate the Electronic Health "
        "Information Export (EHI) for a single patient and also the patient "
        "population in both HL7 CCDA xml format that comply with USCDI v1 "
        "requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."
    ),
    "external_links": parser.links,
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "field_count": 0,
    "entity_count": 0,
    "export_formats": ["HL7 C-CDA XML", "HL7 FHIR R4 US Core STU3.1.1"],
    "uscdi_version": "v1",
    "total_text_elements": len(parser.text_chunks),
    "total_links": len(parser.links),
    "analysis": {
        "documentation_type": "single_page_stub",
        "has_vendor_specific_content": False,
        "references_only_external_standards": True,
        "export_mechanism": "unclear - says 'authorized users can generate'",
        "single_patient": True,
        "bulk_population": True,
    },
}

output_path = os.path.join(os.path.dirname(__file__), "parsed_b10_page.json")
with open(output_path, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
