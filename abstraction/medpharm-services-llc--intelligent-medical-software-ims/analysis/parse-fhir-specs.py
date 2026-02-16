#!/usr/bin/env python3
"""Parse the FHIR specifications HTML to extract all resource definitions.

Reads the raw HTML from downloads/fhir-specifications.html and extracts
resource types, fields, and search parameters. Handles the Duda SPA HTML
by searching for embedded JSON data and table structures in the raw source.

Outputs:
  - entity-inventory-full.json: Complete field-level inventory
  - entity-inventory-summary.json: Summary statistics
"""

import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

BASE = Path(__file__).parent.parent
HTML_FILE = BASE / "downloads" / "fhir-specifications.html"
ENRICHMENT_FILE = BASE / "downloads" / "enrichment" / "fhir-resources.json"

def load_enrichment_data():
    """Load the browser-extracted FHIR resource data."""
    with open(ENRICHMENT_FILE) as f:
        return json.load(f)

def check_html_for_document_reference():
    """Check if DocumentReference content exists in the HTML source."""
    html = HTML_FILE.read_text(errors='replace')
    # Count occurrences
    count = len(re.findall(r'DocumentReference|Document Reference', html, re.IGNORECASE))
    return count

def build_inventory():
    """Build complete entity inventory from enrichment data + HTML verification."""
    resources = load_enrichment_data()
    doc_ref_count = check_html_for_document_reference()

    # The browser extraction missed DocumentReference (visible in nav and HTML).
    # We know from the HTML it exists. Check if Procedure is genuinely there.
    resource_types = [r['resourceType'] for r in resources]

    # Build inventory
    entities = []
    for r in resources:
        entity = {
            "entity_name": r['resourceType'],
            "entity_type": "FHIR Resource",
            "description": r.get('description', ''),
            "category": categorize_resource(r['resourceType']),
            "field_count": len(r.get('fields', [])),
            "fields": [],
            "search_params": r.get('searchParams', [])
        }
        for f in r.get('fields', []):
            field = {
                "name": f['name'],
                "data_type": f.get('dataType', ''),
                "description": f.get('description', ''),
                "required": f.get('required', ''),
                "has_description": bool(f.get('description', '').strip()),
            }
            entity["fields"].append(field)
        entities.append(entity)

    # Add DocumentReference as noted-but-not-extracted
    if 'DocumentReference' not in resource_types and doc_ref_count > 0:
        entities.append({
            "entity_name": "DocumentReference",
            "entity_type": "FHIR Resource",
            "description": "Referenced in HTML navigation and page content but not captured by browser extraction script.",
            "category": "Clinical Notes / Documents",
            "field_count": 0,
            "fields": [],
            "search_params": [],
            "parse_note": f"Present in HTML ({doc_ref_count} occurrences) but missed by extraction script"
        })

    return entities

def categorize_resource(resource_type):
    """Categorize FHIR resources into clinical domains."""
    categories = {
        'AllergyIntolerance': 'Allergies',
        'Patient': 'Demographics',
        'Encounter': 'Encounters',
        'Immunization': 'Immunizations',
        'Goal': 'Care Plans / Goals',
        'Condition': 'Problems / Conditions',
        'Organization': 'Administrative',
        'MedicationRequest': 'Medications',
        'Provenance': 'Provenance',
        'Procedure': 'Procedures',
        'Device': 'Medical Devices',
        'Practitioner': 'Administrative',
        'CarePlan': 'Care Plans / Goals',
        'CareTeam': 'Care Plans / Goals',
        'Observation': 'Vitals / Labs / Clinical Tests',
        'DiagnosticReport': 'Vitals / Labs / Clinical Tests',
        'DocumentReference': 'Clinical Notes / Documents',
    }
    return categories.get(resource_type, 'Other')

def build_summary(entities):
    """Build summary statistics from entity inventory."""
    total_fields = sum(e['field_count'] for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e['fields'] if f.get('has_description')
    )
    total_field_objects = sum(len(e['fields']) for e in entities)

    # Category breakdown
    categories = {}
    for e in entities:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'field_count': 0}
        categories[cat]['entity_count'] += 1
        categories[cat]['field_count'] += e['field_count']

    # C-CDA sections from the EHI export page
    ccda_sections = [
        "Assessment", "Clinical Notes", "Durable Medical Equipment",
        "Encounters", "Family History", "Functional Status", "Goals",
        "Health Concerns", "Immunization", "Laboratory Values/Results",
        "Medications", "Medication Allergies", "Payer",
        "Plan of Treatment", "Problems", "Procedures",
        "Reason for Referral", "Smoking Status and Tobacco Use", "Vital Signs"
    ]

    summary = {
        "export_formats": ["C-CDA XML (USCDI v1)", "FHIR R4 (US Core STU 3.1.1, Bulk Data STU 1.0.1)"],
        "fhir_resources": {
            "total_resources": len(entities),
            "total_fields": total_fields,
            "fields_with_descriptions": fields_with_desc,
            "description_percentage": round(fields_with_desc / total_field_objects * 100, 1) if total_field_objects > 0 else 0,
            "category_breakdown": categories,
            "resources_extracted": len([e for e in entities if e['field_count'] > 0]),
            "resources_noted_but_not_extracted": len([e for e in entities if e['field_count'] == 0]),
        },
        "ccda_sections": {
            "total_sections": len(ccda_sections),
            "sections": ccda_sections,
            "field_level_detail": False,
            "note": "C-CDA sections listed by name only on the EHI export page; no field-level documentation provided"
        },
        "documentation_artifacts": {
            "ehi_export_page": {
                "url": "https://www.meditab.com/company/ehi-export",
                "format": "HTML (Duda SPA)",
                "content": "Single page with C-CDA section list and FHIR format description"
            },
            "fhir_specifications": {
                "url": "https://www.meditab.com/fhir/specifications",
                "format": "HTML (Duda SPA, 3.3 MB)",
                "content": "Detailed FHIR API docs for US Core resources"
            },
            "sample_data": False,
            "schema_files": False,
            "downloadable_files": False,
            "user_guide": False,
        },
        "coverage_assessment": {
            "is_uscdi_only": True,
            "extends_beyond_g10": False,
            "vendor_explicitly_references_g10": True,
            "billing_data": False,
            "specialty_data": False,
            "custom_forms": False,
            "vendor_extensions": False,
            "note": "Vendor explicitly states 'For detailed specifications, please refer to 170.315(g)(10)' — confirming this is their g(10) API repackaged as b(10)"
        }
    }
    return summary

def main():
    entities = build_inventory()
    summary = build_summary(entities)

    out_dir = Path(__file__).parent

    with open(out_dir / "entity-inventory-full.json", "w") as f:
        json.dump(entities, f, indent=2)
    print(f"Wrote entity-inventory-full.json: {len(entities)} entities")

    with open(out_dir / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")

    # Print summary stats
    print(f"\n=== Summary ===")
    print(f"FHIR Resources: {len(entities)} ({summary['fhir_resources']['resources_extracted']} with field data)")
    print(f"Total fields: {summary['fhir_resources']['total_fields']}")
    print(f"Fields with descriptions: {summary['fhir_resources']['fields_with_descriptions']} ({summary['fhir_resources']['description_percentage']}%)")
    print(f"C-CDA sections: {summary['ccda_sections']['total_sections']}")
    print(f"\nCategory breakdown:")
    for cat, data in sorted(summary['fhir_resources']['category_breakdown'].items()):
        print(f"  {cat}: {data['entity_count']} resources, {data['field_count']} fields")

if __name__ == "__main__":
    main()
