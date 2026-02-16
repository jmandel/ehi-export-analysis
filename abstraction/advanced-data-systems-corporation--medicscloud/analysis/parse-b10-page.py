"""Parse the B10_MedicsCloud.html page and extract all structured content."""

from html.parser import HTMLParser
import json
import os

html_path = os.path.join(os.path.dirname(__file__), "..", "downloads", "B10_MedicsCloud.html")

with open(html_path, "r") as f:
    html_content = f.read()

# Simple extraction
class B10Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = {
            "file": "B10_MedicsCloud.html",
            "file_size_bytes": len(html_content.encode()),
            "title": None,
            "headings": [],
            "paragraphs": [],
            "links": [],
            "lists": [],
            "current_tag": None,
            "current_text": "",
        }
        self._in_tag = None

    def handle_starttag(self, tag, attrs):
        self._in_tag = tag
        self.results["current_text"] = ""
        if tag == "a":
            href = dict(attrs).get("href", "").strip()
            self.results["links"].append({"href": href, "text": ""})

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self._in_tag in ("h1", "h2"):
            self.results["headings"].append({"level": self._in_tag, "text": text})
        if self._in_tag == "p":
            self.results["paragraphs"].append(text)
        if self._in_tag == "a" and self.results["links"]:
            self.results["links"][-1]["text"] = text
        if self._in_tag == "li":
            self.results["lists"].append(text)

parser = B10Parser()
parser.handle_starttag = parser.handle_starttag
parser.feed(html_content)

# Clean up internal state
del parser.results["current_tag"]
del parser.results["current_text"]

output = {
    "source_file": "downloads/B10_MedicsCloud.html",
    "file_size_bytes": len(html_content.encode()),
    "total_headings": len(parser.results["headings"]),
    "total_paragraphs": len(parser.results["paragraphs"]),
    "total_links": len(parser.results["links"]),
    "headings": parser.results["headings"],
    "paragraphs": parser.results["paragraphs"],
    "links": parser.results["links"],
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False,
    "has_api_docs": False,
    "export_formats_mentioned": ["HL7 CCDA XML", "HL7 FHIR R4 US Core STU3.1.1"],
    "standards_referenced": ["USCDI v1", "HL7 C-CDA", "FHIR v4.0.1", "US Core v3.1.1"],
    "export_scope_mentioned": ["single patient", "patient population"],
    "vendor_specific_content": "None - documentation consists of one paragraph and two links to external standards",
}

output_path = os.path.join(os.path.dirname(__file__), "b10-page-parsed.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
