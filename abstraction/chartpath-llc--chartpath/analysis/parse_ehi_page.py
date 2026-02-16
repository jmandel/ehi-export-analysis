#!/usr/bin/env python3
"""Parse the ChartPath EHI export page HTML and extract all substantive content.

Outputs a JSON structure with the page metadata, extracted text content,
and basic statistics about the documentation.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/chartpath-llc--chartpath/downloads")

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self.current_tag = None
        self.skip = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in ('script', 'style', 'noscript'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
        self.current_tag = None

    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t and len(t) > 2:
                self.text_blocks.append({"tag": self.current_tag or "text", "text": t})


def analyze_ehi_page():
    html_path = DOWNLOADS / "ehiexport-page.html"
    html_content = html_path.read_text()

    ext = TextExtractor()
    ext.feed(html_content)

    # Filter to meaningful text (exclude boilerplate)
    substantive = [b for b in ext.text_blocks if b["tag"] in ("p", "h1", "h2", "h3", "span", None, "text")]
    substantive_text = [b["text"] for b in substantive if len(b["text"]) > 10]

    # Count sentences and words
    full_text = " ".join(substantive_text)
    sentences = [s.strip() for s in re.split(r'[.!?]+', full_text) if s.strip()]
    words = full_text.split()

    # Check for links
    links = re.findall(r'href="([^"]*)"', html_content)
    external_links = [l for l in links if l.startswith("http") and "hubspot" not in l.lower() and "chartpath" not in l.lower()]
    download_links = [l for l in links if any(ext in l.lower() for ext in ['.pdf', '.csv', '.json', '.xml', '.zip', '.xlsx'])]

    result = {
        "source_file": "ehiexport-page.html",
        "source_url": "https://info.chartpath.com/ehiexport",
        "page_title": "ChartPath Electronic Health Information Export",
        "file_size_bytes": len(html_content),
        "substantive_text_blocks": substantive_text,
        "statistics": {
            "total_sentences": len(sentences),
            "total_words": len(words),
            "external_links": len(external_links),
            "download_links": len(download_links),
            "has_data_dictionary": False,
            "has_schema": False,
            "has_sample_data": False,
            "has_field_definitions": False,
            "has_table_definitions": False,
            "has_user_guide": False,
        },
        "export_description": {
            "format": "ZIP archive containing sub-ZIPs",
            "contents": [
                "Per-encounter PDFs (in a sub-ZIP)",
                "Per-encounter C-CDA documents (in a sub-ZIP)",
                "Attached files in original format (in a sub-ZIP)",
                "Face sheet document with patient demographics"
            ],
            "mentioned_data_domains": [
                "Patient demographics (face sheet)",
                "Encounter data (PDF + C-CDA per encounter)",
                "File attachments"
            ],
            "unmentioned_domains": [
                "Billing/claims/charges",
                "Medications/prescriptions (beyond C-CDA)",
                "Problem/diagnosis lists (beyond C-CDA)",
                "Screening/assessment scores",
                "Census/facility assignment data",
                "Orders",
                "Implantable device data",
                "Care coordination data",
                "Structured lab results",
                "Immunizations (beyond C-CDA)",
                "Vitals (beyond C-CDA)",
                "Allergies (beyond C-CDA)"
            ]
        }
    }

    return result


def analyze_cehrt_page():
    html_path = DOWNLOADS / "2015-cehrt-page.html"
    html_content = html_path.read_text()

    # Extract CTA button labels
    cta_buttons = re.findall(r'alt="([^"]*)"', html_content)
    cta_buttons = [b for b in cta_buttons if b and len(b) > 3 and b != "ChartPath_Logo"]

    # Extract FHIR document links
    fhir_links = []
    for m in re.finditer(r'href="(https://hubs\.ly/[^"]+)"', html_content):
        fhir_links.append(m.group(1))
    for m in re.finditer(r'href="(https://app\.hubspot\.com/documents/[^"]*)"', html_content):
        fhir_links.append(m.group(1).replace("&amp;", "&"))

    return {
        "source_file": "2015-cehrt-page.html",
        "source_url": "https://chartpath.com/2015-cehrt",
        "file_size_bytes": len(html_content),
        "cta_buttons": cta_buttons,
        "fhir_document_links": fhir_links,
        "ehi_export_link_target": "https://info.chartpath.com/ehiexport (via HubSpot CTA redirect)",
        "certification_details": {
            "product": "ChartPath",
            "version": "1.29",
            "certification_date": "December 27, 2019",
            "certificate_number": "15.04.04.2996.Char.12.01.1.191227"
        }
    }


if __name__ == "__main__":
    output = {
        "analysis_date": "2026-02-16",
        "ehi_export_page": analyze_ehi_page(),
        "cehrt_page": analyze_cehrt_page(),
        "artifacts_summary": {
            "total_files": 4,
            "files": [
                {"name": "ehiexport-page.html", "type": "HTML", "description": "EHI export documentation page - 7 sentences"},
                {"name": "ehiexport-page-screenshot.png", "type": "PNG", "description": "Screenshot of EHI export page"},
                {"name": "2015-cehrt-page.html", "type": "HTML", "description": "2015 CEHRT mandatory disclosures page"},
                {"name": "2015-cehrt-screenshot.png", "type": "PNG", "description": "Screenshot of CEHRT page"}
            ]
        }
    }

    output_path = Path(__file__).parent / "parsed_ehi_documentation.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))
