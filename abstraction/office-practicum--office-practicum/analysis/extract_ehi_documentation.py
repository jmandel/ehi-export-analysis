#!/usr/bin/env python3
"""
Extract and analyze all EHI export documentation from Office Practicum artifacts.
Produces structured JSON output for the analysis.
"""

import json
import os
import re
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/office-practicum--office-practicum/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/office-practicum--office-practicum/analysis"


class TextExtractor(HTMLParser):
    """Simple HTML to text extractor."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False
        if tag in ('p', 'br', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'):
            self.text.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

    def get_text(self):
        return ''.join(self.text)


def extract_ehi_section(html_content):
    """Extract the EHI export section from an HTML page."""
    idx = html_content.find('Electronic Health Information Export')
    if idx == -1:
        return None

    # Find the enclosing div section (roughly 2000 chars should cover it)
    start = max(0, idx - 100)
    end = min(len(html_content), idx + 2000)
    snippet = html_content[start:end]

    extractor = TextExtractor()
    extractor.feed(snippet)
    text = extractor.get_text().strip()

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()


def count_ehi_words(text):
    """Count words in the EHI documentation text."""
    words = text.split()
    return len(words)


def analyze_artifacts():
    results = {
        "product": "Office Practicum",
        "developer": "Connexin Software, Inc. (d/b/a Office Practicum)",
        "analysis_date": "2026-02-16",
        "artifacts": [],
        "ehi_documentation": {},
        "data_dictionary": None,
        "sample_data": None,
        "schema": None,
    }

    # 1. Analyze onc-certification-page.html
    cert_path = os.path.join(RESULTS_DIR, "onc-certification-page.html")
    with open(cert_path, 'r', encoding='utf-8') as f:
        cert_html = f.read()

    cert_size = os.path.getsize(cert_path)
    ehi_text_cert = extract_ehi_section(cert_html)
    cert_word_count = count_ehi_words(ehi_text_cert) if ehi_text_cert else 0

    results["artifacts"].append({
        "filename": "onc-certification-page.html",
        "source_url": "https://www.officepracticum.com/op/population-health/onc-certification",
        "size_bytes": cert_size,
        "type": "HTML page",
        "description": "Registered URL for ONC certification. Contains EHI export section.",
        "ehi_content_found": ehi_text_cert is not None,
        "ehi_word_count": cert_word_count,
        "informative_rating": "primary — contains the entirety of EHI export documentation"
    })

    # 2. Analyze disclosures page
    disc_path = os.path.join(RESULTS_DIR, "onc-certification-info-disclosures.html")
    with open(disc_path, 'r', encoding='utf-8') as f:
        disc_html = f.read()

    disc_size = os.path.getsize(disc_path)
    ehi_text_disc = extract_ehi_section(disc_html)
    disc_word_count = count_ehi_words(ehi_text_disc) if ehi_text_disc else 0

    results["artifacts"].append({
        "filename": "onc-certification-info-disclosures.html",
        "source_url": "https://www.officepracticum.com/onc-certification-info",
        "size_bytes": disc_size,
        "type": "HTML page",
        "description": "Mandatory disclosures page with accordion sections. EHI section identical to registered URL.",
        "ehi_content_found": ehi_text_disc is not None,
        "ehi_word_count": disc_word_count,
        "text_matches_certification_page": ehi_text_cert == ehi_text_disc if ehi_text_cert and ehi_text_disc else None,
        "informative_rating": "duplicate — identical EHI text as certification page"
    })

    # 3. PDF analysis
    pdf_path = os.path.join(RESULTS_DIR, "OP_RWT_Results_Report_2025.pdf")
    pdf_size = os.path.getsize(pdf_path)

    results["artifacts"].append({
        "filename": "OP_RWT_Results_Report_2025.pdf",
        "source_url": "https://hub.officepracticum.com/hubfs/OP%20Website/OP_RWT_Results_Report_2025.pdf",
        "size_bytes": pdf_size,
        "type": "PDF (10 pages)",
        "description": "2025 Real World Testing Results Report. Page 7 covers EHI Export: 2,861 single-patient exports, 20 bulk exports across 5 practices in Q4 2025.",
        "ehi_content_found": True,
        "ehi_technical_detail": False,
        "rwt_data": {
            "reporting_period": "Q4 2025",
            "testing_methodology": "Logging",
            "practices_tested": 5,
            "single_patient_exports": 2861,
            "bulk_exports": 20,
            "key_finding": "Significant increase in utilization since last year. Satisfaction is high. Functionality working as expected.",
            "action_needed": "None"
        },
        "informative_rating": "supplementary — confirms feature exists and is used, but no technical detail about export contents"
    })

    # 4. Screenshots
    screenshots = [
        "screenshot-registered-url-onccert.png",
        "screenshot-registered-url-ehi-section.png",
        "screenshot-disclosures-page-top.png",
        "screenshot-ehi-export-accordion-expanded.png",
    ]
    for ss in screenshots:
        ss_path = os.path.join(RESULTS_DIR, ss)
        results["artifacts"].append({
            "filename": ss,
            "size_bytes": os.path.getsize(ss_path),
            "type": "PNG screenshot",
            "description": f"Visual capture of web page content.",
            "informative_rating": "corroborative — visual confirmation of HTML content"
        })

    # EHI documentation summary
    results["ehi_documentation"] = {
        "full_text": ehi_text_cert,
        "word_count": cert_word_count,
        "sections": [
            {
                "heading": "Single Patient Export",
                "content": "Office Practicum allows a user to export electronic health information (EHI) for a single patient at any time via a Database Viewer stored SQL query built into OP named \"Single patient EHI export\" without developer assistance. The exported files are in .csv file format explained below"
            },
            {
                "heading": "Multi-Patient Export",
                "content": "Office Practicum can export all the data for a patient population in .csv file format explained below:"
            },
            {
                "heading": "CSV",
                "content": "A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values. Each line of the file is a data record. Each record consists of one or more fields, separated by commas. The use of the comma as a field separator is the source of the name for this file format."
            }
        ],
        "mentions_data_dictionary": False,
        "mentions_schema": False,
        "mentions_table_names": False,
        "mentions_field_names": False,
        "mentions_data_types": False,
        "mentions_sample_data": False,
        "mentions_relationships": False,
        "mentions_value_sets": False,
        "downloadable_files": 0,
        "links_to_technical_docs": 0,
    }

    # Summary stats
    results["summary"] = {
        "total_artifacts": len(results["artifacts"]),
        "total_ehi_documentation_words": cert_word_count,
        "data_dictionary_present": False,
        "schema_present": False,
        "sample_data_present": False,
        "entities_documented": 0,
        "fields_documented": 0,
        "export_format": "CSV",
        "export_mechanism": "Database Viewer stored SQL query ('Single patient EHI export')",
        "single_patient_export": True,
        "bulk_export": True,
        "classification": "Minimal/stub",
    }

    return results


if __name__ == "__main__":
    results = analyze_artifacts()
    output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Analysis written to {output_path}")
    print(f"\nSummary:")
    print(f"  Total artifacts: {results['summary']['total_artifacts']}")
    print(f"  EHI documentation word count: {results['summary']['total_ehi_documentation_words']}")
    print(f"  Data dictionary: {'Yes' if results['summary']['data_dictionary_present'] else 'No'}")
    print(f"  Schema: {'Yes' if results['summary']['schema_present'] else 'No'}")
    print(f"  Sample data: {'Yes' if results['summary']['sample_data_present'] else 'No'}")
    print(f"  Entities documented: {results['summary']['entities_documented']}")
    print(f"  Fields documented: {results['summary']['fields_documented']}")
    print(f"  Export format: {results['summary']['export_format']}")
    print(f"  Classification: {results['summary']['classification']}")
