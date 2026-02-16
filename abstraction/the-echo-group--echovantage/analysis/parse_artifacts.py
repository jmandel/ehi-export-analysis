#!/usr/bin/env python3
"""Parse all EHI export artifacts for EchoVantage and produce structured outputs."""

import json
import re
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')
OUTPUT_DIR = os.path.dirname(__file__)

def parse_pdf():
    """Extract and structure the PDF content."""
    pdf_path = os.path.join(DOWNLOADS, 'Electronic-Health-Information-Export_EchoVantage.pdf')
    result = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], capture_output=True, text=True)
    text = result.stdout.strip()
    
    info = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
    
    return {
        "file": "Electronic-Health-Information-Export_EchoVantage.pdf",
        "pages": 1,
        "size_bytes": os.path.getsize(pdf_path),
        "author": "Catherine Baker",
        "created": "2025-08-15",
        "raw_text": text,
        "sections": {
            "title": "Electronic Health Information (EHI) Export",
            "subtitle": "File Formats",
            "description": "These are standardized computable formats. The export(s) will include one or more of the formats below depending on set-up and use of the system by the agency.",
            "single_patient_formats": [
                {
                    "format": "CCD/C-CDA",
                    "description": "Consolidated Clinical Document Architecture which will contain data required by the USCDI v1 standards."
                },
                {
                    "format": "JSON",
                    "description": "JavaScript Object Notation. JSON is a lightweight format for storing and transporting data. JSON is in plain text, which is readable by a person, but is meant to be parsed and understood by an application or web page."
                },
                {
                    "format": "PDF",
                    "description": "Portable Document Format, is a file format to present documents, including text formatting and image."
                }
            ],
            "patient_population_formats": [
                {
                    "format": ".bak file",
                    "description": "This is a full MSSQL Server database backup of all data for an agency that can be restored."
                }
            ]
        }
    }

def parse_html():
    """Extract the EHI export section from the ONC page."""
    html_path = os.path.join(DOWNLOADS, 'onc-echo-page.html')
    with open(html_path) as f:
        html = f.read()
    
    # Strip scripts and styles
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    
    # Extract links
    links = re.findall(r'href="([^"]*)"', html)
    ehi_links = [l for l in links if any(k in l.lower() for k in ['ehi', 'export', 'electronic-health'])]
    fhir_links = [l for l in links if 'fhir' in l.lower() or 'api' in l.lower()]
    
    # Extract EHI section text
    text_clean = re.sub(r'<[^>]+>', '\n', text)
    text_clean = re.sub(r'\n{3,}', '\n\n', text_clean)
    text_clean = re.sub(r'[ \t]+', ' ', text_clean)
    
    lines = text_clean.split('\n')
    ehi_section = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if 'Electronic Health Information' in stripped:
            in_section = True
        if in_section:
            ehi_section.append(stripped)
        if in_section and ('FHIR API' in stripped or 'Real World Testing' in stripped):
            break
    
    return {
        "file": "onc-echo-page.html",
        "size_bytes": os.path.getsize(html_path),
        "ehi_related_links": ehi_links,
        "fhir_related_links": fhir_links[:5],
        "ehi_section_text": '\n'.join(ehi_section),
        "export_modes": {
            "single_patient": {
                "mechanism": "User-initiated, no developer assistance needed",
                "formats": ["CCD/C-CDA", "JSON", "PDF"],
                "scope": "USCDI v1"
            },
            "patient_population": {
                "mechanism": "Support ticket via Salesforce",
                "formats": ["MSSQL .bak database backup"],
                "scope": "All data for an agency",
                "caveats": [
                    "Content varies by software applications in use",
                    "Content varies by software version",
                    "Content varies by documentation practices",
                    "Content varies by configuration decisions",
                    "May include materials not sourced from the application"
                ]
            }
        }
    }

def build_inventory():
    """
    Build entity inventory. Since there is no data dictionary, schema, or 
    field-level documentation, the inventory reflects only what the documentation describes.
    """
    # No data dictionary exists - the entire EHI documentation is a 1-page PDF
    # listing export formats with no entity/table/field details
    inventory = {
        "metadata": {
            "product": "EchoVantage",
            "vendor": "The Echo Group (Ensora Health)",
            "source": "Electronic-Health-Information-Export_EchoVantage.pdf + onc-echo-page.html",
            "has_data_dictionary": False,
            "has_schema": False,
            "has_sample_data": False,
            "has_field_definitions": False,
            "entity_count": 0,
            "field_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "note": "No data dictionary, schema, or field-level documentation provided. "
                    "The only EHI export documentation is a 1-page PDF listing export formats "
                    "(CCD/C-CDA, JSON, PDF for single patient; MSSQL .bak for population) "
                    "with no detail about what data elements are included."
        },
        "entities": [],
        "export_formats_documented": [
            {
                "name": "CCD/C-CDA (Single Patient)",
                "scope": "USCDI v1 data elements",
                "entity_detail": "None provided",
                "field_detail": "None provided"
            },
            {
                "name": "JSON (Single Patient)",
                "scope": "Not specified",
                "entity_detail": "None provided",
                "field_detail": "None provided"
            },
            {
                "name": "PDF (Single Patient)",
                "scope": "Not specified",
                "entity_detail": "None provided",
                "field_detail": "None provided"
            },
            {
                "name": "MSSQL .bak (Patient Population)",
                "scope": "Full database backup for agency",
                "entity_detail": "None provided - no documentation of database schema",
                "field_detail": "None provided"
            }
        ]
    }
    return inventory

def build_summary(inventory):
    """Build summary statistics from inventory."""
    return {
        "product": "EchoVantage",
        "vendor": "The Echo Group (Ensora Health)",
        "total_entities": inventory["metadata"]["entity_count"],
        "total_fields": inventory["metadata"]["field_count"],
        "fields_with_descriptions": inventory["metadata"]["fields_with_descriptions"],
        "fields_with_types": inventory["metadata"]["fields_with_types"],
        "pct_described": "N/A",
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "export_formats": ["CCD/C-CDA", "JSON", "PDF", "MSSQL .bak"],
        "single_patient_scope": "USCDI v1 (per vendor documentation)",
        "population_scope": "Full MSSQL database backup (undocumented schema)",
        "documentation_artifacts": [
            {
                "file": "Electronic-Health-Information-Export_EchoVantage.pdf",
                "pages": 1,
                "content": "Format descriptions only, no data dictionary"
            },
            {
                "file": "onc-echo-page.html",
                "content": "EHI export section with export mode descriptions"
            }
        ],
        "assessment": {
            "documentation_quality": "Minimal - no field-level documentation exists",
            "coverage_breadth": "Unclear - single patient export explicitly limited to USCDI v1; population export is full database backup but undocumented",
            "approach": "Hybrid: repackaged C-CDA for single patient, database dump for population"
        }
    }

if __name__ == '__main__':
    # Parse all artifacts
    pdf_data = parse_pdf()
    html_data = parse_html()
    inventory = build_inventory()
    summary = build_summary(inventory)
    
    # Save outputs
    with open(os.path.join(OUTPUT_DIR, 'pdf-parsed.json'), 'w') as f:
        json.dump(pdf_data, f, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, 'html-parsed.json'), 'w') as f:
        json.dump(html_data, f, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, 'entity-inventory-full.json'), 'w') as f:
        json.dump(inventory, f, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, 'entity-inventory-summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("=== EchoVantage EHI Export Artifact Analysis ===")
    print(f"PDF: 1 page, {pdf_data['size_bytes']} bytes")
    print(f"  - Single patient formats: {', '.join(f['format'] for f in pdf_data['sections']['single_patient_formats'])}")
    print(f"  - Population formats: {', '.join(f['format'] for f in pdf_data['sections']['patient_population_formats'])}")
    print(f"HTML page: {html_data['size_bytes']} bytes")
    print(f"  - EHI links found: {len(html_data['ehi_related_links'])}")
    print(f"Data dictionary: NOT PROVIDED")
    print(f"Schema documentation: NOT PROVIDED")
    print(f"Sample data: NOT PROVIDED")
    print(f"Entities documented: 0")
    print(f"Fields documented: 0")
    print("Files saved: pdf-parsed.json, html-parsed.json, entity-inventory-full.json, entity-inventory-summary.json")
