#!/usr/bin/env python3
"""
Parse all structured artifacts from Braintree Health's EHI export documentation.
Produces full-entity-inventory.json and summary statistics.
"""

import json
import re
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/braintree-health--braintree/downloads")
OUTPUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/braintree-health--braintree/analysis")

def parse_b10_section(html_path):
    """Extract the b(10) EHI export section from the certification page HTML."""
    with open(html_path, 'r') as f:
        html = f.read()
    
    # Find the b(10) section
    start = html.find('Electronic Health Information export b(10)')
    if start == -1:
        return None
    
    # Get the section until CQMs
    end = html.find('CQMs:', start)
    if end == -1:
        end = start + 3000
    chunk = html[start:end]
    
    # Extract list items
    items = re.findall(r'<li>(.*?)</li>', chunk, re.DOTALL)
    items = [re.sub(r'<[^>]+>', '', item).strip() for item in items]
    
    # Extract the intro paragraph
    paras = re.findall(r'<p>(.*?)</p>', chunk, re.DOTALL)
    paras = [re.sub(r'<[^>]+>', '', p).strip() for p in paras]
    
    return {
        "section_title": "Electronic Health Information export b(10)",
        "introductory_text": paras,
        "export_format_bullets": items,
        "total_bullet_points": len(items),
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_linked_documents": False,
        "has_export_instructions": False,
    }

def parse_fhir_resources(pdf_text_path):
    """Parse FHIR resource list from the extracted PDF text."""
    with open(pdf_text_path, 'r') as f:
        text = f.read()
    
    # Extract the resource table
    start = text.find('Following resources are supported')
    end = text.find('Request : Patient', start)
    if start == -1 or end == -1:
        return []
    
    chunk = text[start:end]
    lines = [l.strip() for l in chunk.split('\n') if l.strip() and l.strip() != 'FHIR Resource']
    lines = [l for l in lines if l != 'Following resources are supported']
    
    resources = []
    for line in lines:
        # Parse "Name - Profile" or just "Name"
        parts = line.split(' - ', 1)
        name = parts[0].strip()
        profile = parts[1].strip() if len(parts) > 1 else None
        if name:
            resources.append({
                "name": name,
                "profile": profile,
                "standard": "US Core / USCDI v1"
            })
    
    return resources

def parse_fhir_request_sections(pdf_text_path):
    """Parse individual FHIR request sections to count documented fields."""
    with open(pdf_text_path, 'r') as f:
        text = f.read()
    
    # Find all Request sections
    sections = re.findall(r'Request\s*:\s*(.*?)(?=Request\s*:|Profile audience|$)', text, re.DOTALL)
    
    results = []
    for section_text in sections:
        title_match = re.match(r'(.+?)(?:\n|\.)', section_text)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        # Count JSON field names in sample responses
        json_fields = re.findall(r'"(\w+)"\s*:', section_text)
        unique_fields = list(set(json_fields))
        
        results.append({
            "resource": title,
            "sample_fields_count": len(unique_fields),
            "sample_fields": sorted(unique_fields)[:20],  # first 20 for reference
        })
    
    return results

def build_export_inventory():
    """Build the complete inventory of what the b(10) export documents."""
    
    b10 = parse_b10_section(DOWNLOADS / "certification-page.html")
    
    # Parse FHIR PDF for context
    import subprocess
    result = subprocess.run(
        ['pdftotext', '-layout', str(DOWNLOADS / 'Braintree-FHIR-API-Documentation-1.pdf'), '-'],
        capture_output=True, text=True
    )
    pdf_text_path = OUTPUT / "fhir_pdf_text.txt"
    with open(pdf_text_path, 'w') as f:
        f.write(result.stdout)
    
    fhir_resources = parse_fhir_resources(pdf_text_path)
    fhir_sections = parse_fhir_request_sections(pdf_text_path)
    
    # Build the b(10) export content entities based on the 6 bullet points
    b10_entities = [
        {
            "entity_name": "General EHI (images, documents, reports)",
            "export_format": "HTML/PDF",
            "description": "While certain EHI, such as images, documents, reports are exported in human-readable html/pdf format where applicable.",
            "fields": [],
            "fields_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": "General",
            "documentation_detail": "none - no field-level detail provided"
        },
        {
            "entity_name": "Patient Demographics",
            "export_format": "C-CDA XML",
            "description": "The patient demographics are exported in CCDA xml format.",
            "fields": [],
            "fields_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": "Demographics",
            "documentation_detail": "none - format specified (C-CDA) but no field enumeration"
        },
        {
            "entity_name": "Consent Forms",
            "export_format": "HTML",
            "description": "The consents form of the patient are exported in HTML format.",
            "fields": [],
            "fields_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": "Consents",
            "documentation_detail": "none - format specified only"
        },
        {
            "entity_name": "Clinical and Billing Report / Encounter Documentation",
            "export_format": "PDF (computable format)",
            "description": "The clinical and billing report and encounter documentation of the patient is exported in PDF format. The PDF provided are in computable format.",
            "fields": [],
            "fields_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": "Clinical / Billing",
            "documentation_detail": "none - format specified, 'computable format' claim unexplained"
        },
        {
            "entity_name": "Patient Attachments",
            "export_format": "Original upload format",
            "description": "The patient attachments are exported in the original format as uploaded into EMR.",
            "fields": [],
            "fields_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": "Attachments",
            "documentation_detail": "none - format specified only"
        },
        {
            "entity_name": "Patient Images",
            "export_format": "DICOM",
            "description": "The patient images are exported into DICOM format.",
            "fields": [],
            "fields_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": "Imaging",
            "documentation_detail": "none - format specified only; DICOM is appropriate for imaging"
        }
    ]
    
    inventory = {
        "vendor": "Braintree Health",
        "product": "BRAINTREE (BMW Platform)",
        "version": "10.5.1.1",
        "chpl_id": 10727,
        "analysis_date": "2026-02-16",
        "b10_documentation": {
            "source": "certification-page.html (inline text on ONC certification page)",
            "source_url": "https://www.braintreehealth.com/braintree-onc-certification-btree/",
            "section_heading": "Electronic Health Information export b(10)",
            "total_bullet_points": 6,
            "has_data_dictionary": False,
            "has_sample_data": False,
            "has_schema": False,
            "has_linked_documents": False,
            "has_export_instructions": False,
            "has_field_definitions": False,
            "has_value_sets": False,
            "has_relationships": False,
            "introductory_text": b10["introductory_text"] if b10 else [],
            "export_format_bullets": b10["export_format_bullets"] if b10 else [],
        },
        "b10_export_entities": b10_entities,
        "b10_summary": {
            "total_entities": len(b10_entities),
            "total_fields_documented": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "export_formats": ["C-CDA XML", "HTML", "PDF (computable)", "DICOM", "Original upload format"],
            "categories": {
                "General": 1,
                "Demographics": 1,
                "Consents": 1,
                "Clinical / Billing": 1,
                "Attachments": 1,
                "Imaging": 1,
            }
        },
        "g10_fhir_api": {
            "source": "Braintree-FHIR-API-Documentation-1.pdf",
            "pages": 76,
            "note": "This is g(10) documentation, NOT b(10). Included for context on what clinical data the system stores.",
            "resources": fhir_resources,
            "resource_count": len(fhir_resources),
            "request_sections": fhir_sections,
        },
        "other_artifacts": {
            "fhir_base_url_pdf": {
                "source": "Braintree-fhir-doc.pdf",
                "pages": 1,
                "content": "Lists test and production FHIR server endpoints",
                "relevance_to_b10": "none"
            },
            "transparency_htm": {
                "source": "transparency.htm",
                "content": "Excel-exported HTML frameset for cost disclosures",
                "relevance_to_b10": "none"
            }
        }
    }
    
    return inventory

def main():
    inventory = build_export_inventory()
    
    # Save full inventory
    with open(OUTPUT / "full-entity-inventory.json", 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    print("=== Braintree Health EHI Export Analysis ===")
    print()
    print("b(10) Export Documentation:")
    print(f"  Source: Inline text on certification page (6 bullet points)")
    print(f"  Entities described: {inventory['b10_summary']['total_entities']}")
    print(f"  Fields documented: {inventory['b10_summary']['total_fields_documented']}")
    print(f"  Data dictionary: No")
    print(f"  Sample data: No")
    print(f"  Schema: No")
    print(f"  Export instructions: No")
    print(f"  Export formats: {', '.join(inventory['b10_summary']['export_formats'])}")
    print()
    print("b(10) Export Entities:")
    for entity in inventory['b10_export_entities']:
        print(f"  - {entity['entity_name']} → {entity['export_format']}")
    print()
    print("g(10) FHIR API (for context, NOT part of b(10)):")
    print(f"  Resources: {inventory['g10_fhir_api']['resource_count']}")
    for r in inventory['g10_fhir_api']['resources']:
        profile = f" ({r['profile']})" if r['profile'] else ""
        print(f"    - {r['name']}{profile}")
    print()
    print("Artifacts reviewed:")
    print(f"  certification-page.html: 71,326 bytes - primary b(10) source")
    print(f"  Braintree-FHIR-API-Documentation-1.pdf: 803,598 bytes, 76 pages - g(10) only")
    print(f"  Braintree-fhir-doc.pdf: 166,453 bytes, 1 page - FHIR endpoints only")
    print(f"  transparency.htm: 9,971 bytes - cost disclosure, not relevant")
    print(f"  ehi-export-section-screenshot.png: 244,687 bytes - screenshot of b(10) section")
    print(f"  certification-page-full.png: 938,405 bytes - full page screenshot")

if __name__ == "__main__":
    main()
