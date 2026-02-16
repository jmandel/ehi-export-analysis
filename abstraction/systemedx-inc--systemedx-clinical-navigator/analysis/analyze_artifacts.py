#!/usr/bin/env python3
"""
Analyze all EHI export artifacts for Systemedx Clinical Navigator.
Produces structured JSON output summarizing what was found.
"""
import json
import os
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/systemedx-inc--systemedx-clinical-navigator"
DOWNLOADS_DIR = os.path.join(RESULTS_DIR, "downloads")

class TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping script/style tags."""
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
    def handle_data(self, data):
        if not self.skip:
            stripped = data.strip()
            if stripped:
                self.text.append(stripped)

def analyze_html_page(filepath):
    """Analyze the dataExport.html page."""
    with open(filepath) as f:
        html_content = f.read()
    
    # Extract text
    extractor = TextExtractor()
    extractor.feed(html_content)
    all_text = '\n'.join(extractor.text)
    
    # Isolate EHI documentation section
    start = all_text.find('EHR data export documentation')
    doc_text = ""
    if start >= 0:
        doc_text = all_text[start:]
        footer_idx = doc_text.find('We invite you')
        if footer_idx > 0:
            doc_text = doc_text[:footer_idx].strip()
    
    # Remove trailing "Systemedx" if present
    if doc_text.endswith('Systemedx'):
        doc_text = doc_text[:-len('Systemedx')].strip()
    
    words = doc_text.split()
    
    # Identify export modes described
    export_modes = []
    if 'All Patients' in doc_text:
        export_modes.append('All Patients')
    if 'Select Patients' in doc_text:
        export_modes.append('Select Patients')
    if 'Single Patient' in doc_text:
        export_modes.append('Single Patient')
    
    # Identify output formats described
    output_formats = []
    if 'CDA XML' in doc_text:
        output_formats.append('CDA XML')
    if 'HTML' in doc_text:
        output_formats.append('CDA HTML (human-readable)')
    if 'PDF' in doc_text:
        output_formats.append('PDF (chart documents)')
    
    # Data domains explicitly mentioned
    data_mentioned = []
    if 'demographics' in doc_text.lower():
        data_mentioned.append('Patient demographics')
    if 'medications' in doc_text.lower():
        data_mentioned.append('Medications')
    if 'problems' in doc_text.lower():
        data_mentioned.append('Problems')
    # The "etc." is notable
    has_etc = 'etc.' in doc_text
    
    return {
        "file": "dataExport.html",
        "file_size_bytes": os.path.getsize(filepath),
        "total_page_text_words": len(all_text.split()),
        "ehi_documentation_text": doc_text,
        "ehi_documentation_word_count": len(words),
        "export_modes": export_modes,
        "output_formats": output_formats,
        "data_domains_explicitly_mentioned": data_mentioned,
        "uses_etc_placeholder": has_etc,
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "has_field_level_detail": False,
        "has_downloadable_artifacts": False,
        "cda_template_specified": False,
        "billing_data_mentioned": False,
        "surgical_pathway_mentioned": False,
        "folder_naming_convention": "LastName_FirstName_DOB_PatientID"
    }

def analyze_pdf(filepath):
    """Analyze the Mandatory Disclosures PDF."""
    import subprocess
    result = subprocess.run(
        ['pdftotext', '-layout', filepath, '-'],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Check if (b)(10) or data export is mentioned
    b10_mentioned = '(b)(10)' in text or 'b10' in text.lower()
    data_export_mentioned = 'data export' in text.lower() or 'ehi' in text.lower()
    
    # Count capabilities listed
    capabilities = []
    for line in text.split('\n'):
        line = line.strip()
        if line and not line.startswith('Capability') and not line.startswith('---'):
            pass  # parse capability names from first column
    
    return {
        "file": "Mandatory-Disclosures-2022.pdf",
        "file_size_bytes": os.path.getsize(filepath),
        "pages": 2,
        "b10_mentioned": b10_mentioned,
        "data_export_mentioned": data_export_mentioned,
        "content_summary": "ONC mandatory cost transparency disclosures listing fees for various certified capabilities. Does not mention (b)(10) data export or associated costs.",
        "capabilities_with_fees": [
            "Update and Setup (one-time fee)",
            "Additional Training Fee (hourly fee)",
            "Yearly Provider License (yearly per provider)",
            "Electronic Prescribing (monthly per provider + EPCS add-on)",
            "Patient Portal Access (monthly per provider)",
            "Lab Interfaces (setup + monthly support)",
            "Direct Messaging (monthly fee)",
            "Immunization Registry Submission (monthly per provider)",
            "API Access ($10,000 yearly per application)"
        ]
    }

def main():
    analysis = {
        "product": "Systemedx Clinical Navigator",
        "version": "2024.12",
        "chpl_id": 11536,
        "analysis_date": "2026-02-16",
        "artifacts_examined": []
    }
    
    # Analyze HTML page
    html_result = analyze_html_page(os.path.join(DOWNLOADS_DIR, "dataExport.html"))
    analysis["artifacts_examined"].append(html_result)
    
    # Analyze PDF
    pdf_result = analyze_pdf(os.path.join(DOWNLOADS_DIR, "Mandatory-Disclosures-2022.pdf"))
    analysis["artifacts_examined"].append(pdf_result)
    
    # Screenshot - note existence only
    screenshot_path = os.path.join(DOWNLOADS_DIR, "dataExport-screenshot.png")
    analysis["artifacts_examined"].append({
        "file": "dataExport-screenshot.png",
        "file_size_bytes": os.path.getsize(screenshot_path),
        "description": "Full-page screenshot of dataExport.html page"
    })
    
    # Summary findings
    analysis["summary"] = {
        "total_artifacts": 3,
        "informative_artifacts": 1,  # only the HTML page has EHI export info
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "has_field_level_documentation": False,
        "export_format": "CDA XML + CDA HTML + PDF documents",
        "export_mechanism": "UI-based job stream (CDAEXPORT)",
        "single_patient_export": True,
        "bulk_export": True,
        "documentation_word_count": html_result["ehi_documentation_word_count"],
        "data_domains_documented": len(html_result["data_domains_explicitly_mentioned"]),
        "b10_export_cost_documented": False,
        "classification": "Minimal/stub",
        "model_type": "Standard-based projection (CDA)",
        "entities_documented": 0,
        "fields_documented": 0
    }
    
    with open("artifact-analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
