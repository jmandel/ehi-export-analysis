"""
Parse all Braintree EHI export artifacts and produce structured inventory.

The b(10) documentation is 6 bullet points on a webpage with no data dictionary,
so we extract what we can: the export format descriptions and the g(10) FHIR 
resource list (to compare what's available via API vs what b(10) claims to export).
"""

import json
import re
import os
from html.parser import HTMLParser

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')
ANALYSIS = os.path.dirname(__file__)


def extract_b10_section(html_path):
    """Extract the b(10) EHI export section from the certification page."""
    with open(html_path, 'r') as f:
        content = f.read()
    
    # Find b(10) section
    idx = content.lower().find('b(10)')
    if idx < 0:
        return None
    
    # Get surrounding context
    start = max(0, idx - 200)
    end = min(len(content), idx + 2000)
    chunk = content[start:end]
    
    # Clean HTML
    clean = re.sub(r'<[^>]+>', '\n', chunk)
    clean = re.sub(r'\n\s*\n', '\n', clean).strip()
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    
    # Extract bullet points
    bullets = []
    capture = False
    for line in lines:
        if 'Key Information' in line:
            capture = True
            continue
        if capture:
            # Stop at CQMs or next section
            if 'CQM' in line or 'Version' in line or 'Quality Measure' in line:
                break
            if line.startswith('While') or line.startswith('The ') or len(line) > 20:
                bullets.append(line)
    
    return {
        "section_title": "Electronic Health Information export b(10)",
        "intro_text": "Braintree understands the importance of ensuring patients have timely, secure and easy access to electronic health information (\"EHI\") to empower them in managing their own health and well-being.",
        "export_formats": bullets
    }


def extract_fhir_resources(pdf_text_path):
    """Extract FHIR resource types from the g(10) API documentation."""
    import subprocess
    result = subprocess.run(
        ['pdftotext', '-layout', os.path.join(DOWNLOADS, 'Braintree-FHIR-API-Documentation-1.pdf'), '-'],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Find "Request :" lines which indicate supported resources
    resources = set()
    for line in text.split('\n'):
        match = re.match(r'Request\s*:\s*(.+)', line.strip())
        if match:
            resource_name = match.group(1).strip()
            # Clean trailing dots/page numbers
            resource_name = re.sub(r'[\s.]+\d+$', '', resource_name).strip()
            resource_name = resource_name.rstrip('.')
            if resource_name:
                resources.add(resource_name)
    
    return sorted(resources)


def build_export_inventory():
    """Build the complete inventory of what we know about the export."""
    
    b10 = extract_b10_section(os.path.join(DOWNLOADS, 'certification-page.html'))
    fhir_resources = extract_fhir_resources(None)
    
    # The b(10) export describes these categories (from the 6 bullet points):
    export_categories = [
        {
            "entity": "patient_demographics",
            "format": "CCDA XML",
            "description": "The patient demographics are exported in CCDA xml format.",
            "category": "Demographics",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None
        },
        {
            "entity": "consent_forms",
            "format": "HTML",
            "description": "The consents form of the patient are exported in HTML format.",
            "category": "Consents",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None
        },
        {
            "entity": "clinical_billing_reports",
            "format": "PDF (described as 'computable format')",
            "description": "The clinical and billing report and encounter documentation of the patient is exported in PDF format. The PDF provided are in computable format.",
            "category": "Clinical / Billing",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None
        },
        {
            "entity": "patient_attachments",
            "format": "Original upload format",
            "description": "The patient attachments are exported in the original format as uploaded into EMR.",
            "category": "Attachments",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None
        },
        {
            "entity": "patient_images",
            "format": "DICOM",
            "description": "The patient images are exported into DICOM format.",
            "category": "Imaging",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None
        },
        {
            "entity": "images_documents_reports",
            "format": "HTML/PDF",
            "description": "While certain EHI, such as images, documents, reports are exported in human-readable html/pdf format where applicable.",
            "category": "Documents / Reports",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None
        }
    ]
    
    inventory = {
        "product": "BRAINTREE (BMW Platform)",
        "version": "10.5.1.1",
        "documentation_source": "https://www.braintreehealth.com/braintree-onc-certification-btree/",
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "b10_documentation": b10,
        "export_categories": export_categories,
        "g10_fhir_resources": fhir_resources,
        "total_entities_documented": len(export_categories),
        "total_fields_documented": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0
    }
    
    return inventory


def build_summary(inventory):
    """Build summary statistics from the inventory."""
    return {
        "product": inventory["product"],
        "version": inventory["version"],
        "has_data_dictionary": inventory["has_data_dictionary"],
        "has_sample_data": inventory["has_sample_data"],
        "has_schema": inventory["has_schema"],
        "total_entities": inventory["total_entities_documented"],
        "total_fields": inventory["total_fields_documented"],
        "fields_with_descriptions": inventory["fields_with_descriptions"],
        "pct_fields_with_descriptions": "N/A",
        "export_formats": ["CCDA XML", "HTML", "PDF", "DICOM", "Original format"],
        "g10_resource_count": len(inventory["g10_fhir_resources"]),
        "g10_resources": inventory["g10_fhir_resources"],
        "categories": [c["category"] for c in inventory["export_categories"]],
        "documentation_quality": "Very poor - 6 bullet points, no field-level detail"
    }


if __name__ == '__main__':
    inventory = build_export_inventory()
    
    with open(os.path.join(ANALYSIS, 'entity-inventory-full.json'), 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote entity-inventory-full.json")
    print(f"  Entities: {inventory['total_entities_documented']}")
    print(f"  Fields: {inventory['total_fields_documented']}")
    print(f"  FHIR resources (g10): {len(inventory['g10_fhir_resources'])}")
    
    summary = build_summary(inventory)
    with open(os.path.join(ANALYSIS, 'entity-inventory-summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")
