#!/usr/bin/env python3
"""
Parses all CharmHealth EHI export artifacts and produces:
- entity-inventory-full.json: Complete extraction of all FHIR resources with fields
- entity-inventory-summary.json: Summary statistics
- billing-reports-inventory.json: Billing report types documented
"""

import json
import re
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')
OUTPUT_DIR = os.path.dirname(__file__)


def parse_fhir_api():
    """Parse FHIR API documentation to extract all resources and their fields."""
    data = json.load(open(os.path.join(DOWNLOADS, 'enrichment', 'fhir-api-extracted.json')))
    
    entities = []
    
    for resource in data['resources']:
        name = resource['name']
        profile = resource.get('usCorProfile', '')
        is_us_core = 'us-core' in str(profile).lower()
        description = resource.get('description', '')
        
        # Extract fields from response examples
        fields = extract_fields_from_examples(resource)
        
        # Extract search parameters as additional metadata
        search_params = []
        for op in resource.get('operations', []):
            for param in op.get('parameters', []):
                search_params.append({
                    'name': param.get('name', ''),
                    'type': param.get('type', ''),
                    'required': param.get('required', 'optional'),
                    'description': param.get('description', ''),
                    'operation': op.get('name', '')
                })
        
        entity = {
            'name': name,
            'category': categorize_resource(name),
            'source': 'FHIR R4 API',
            'profile': 'US Core' if is_us_core else 'FHIR R4 Base',
            'description': description,
            'operations': [op.get('name', '') for op in resource.get('operations', [])],
            'fields': fields,
            'field_count': len(fields),
            'search_parameters': search_params,
            'search_parameter_count': len(search_params),
            'has_examples': any(op.get('responseExample') for op in resource.get('operations', []))
        }
        entities.append(entity)
    
    return entities, data.get('bulkExport', {}), data.get('ccda', {})


def extract_fields_from_examples(resource):
    """Extract field names and types from FHIR response examples."""
    fields = []
    seen = set()
    
    for op in resource.get('operations', []):
        example = op.get('responseExample', '')
        if not example:
            continue
        
        # Try to find JSON in the response example
        # The format is typically "HTTP/1.1 200 OK { ... }"
        json_match = re.search(r'\{[\s\S]*\}', example)
        if not json_match:
            continue
        
        try:
            parsed = json.loads(json_match.group())
        except json.JSONDecodeError:
            # Try to fix common issues
            try:
                # Sometimes examples have trailing commas or incomplete JSON
                fixed = json_match.group().rstrip()
                parsed = json.loads(fixed)
            except:
                continue
        
        # Navigate to the actual resource (may be in Bundle.entry[0].resource)
        actual_resource = parsed
        if parsed.get('resourceType') == 'Bundle':
            entries = parsed.get('entry', [])
            if entries:
                actual_resource = entries[0].get('resource', parsed)
        
        # Extract fields recursively
        extract_json_fields(actual_resource, '', fields, seen)
    
    return fields


def extract_json_fields(obj, prefix, fields, seen, depth=0):
    """Recursively extract fields from a JSON object."""
    if depth > 5 or not isinstance(obj, dict):
        return
    
    for key, value in obj.items():
        full_path = f'{prefix}.{key}' if prefix else key
        
        if full_path in seen:
            continue
        seen.add(full_path)
        
        field_type = infer_type(value)
        
        fields.append({
            'name': full_path,
            'type': field_type,
            'description': '',  # FHIR examples don't include descriptions
            'example_value': truncate_value(value),
            'has_description': False
        })
        
        if isinstance(value, dict):
            extract_json_fields(value, full_path, fields, seen, depth + 1)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            extract_json_fields(value[0], full_path + '[]', fields, seen, depth + 1)


def infer_type(value):
    if isinstance(value, str):
        return 'string'
    elif isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, float):
        return 'number'
    elif isinstance(value, list):
        return 'array'
    elif isinstance(value, dict):
        return 'object'
    return 'unknown'


def truncate_value(value):
    s = str(value)
    return s[:100] + '...' if len(s) > 100 else s


def categorize_resource(name):
    """Categorize a FHIR resource by clinical domain."""
    categories = {
        'Patient': 'Demographics',
        'RelatedPerson': 'Demographics',
        'Practitioner': 'Provider',
        'Organization': 'Provider',
        'Location': 'Provider',
        'Encounter': 'Encounters',
        'Appointment': 'Scheduling',
        'Condition': 'Problems/Diagnoses',
        'AllergyIntolerance': 'Allergies',
        'Medication': 'Medications',
        'MedicationRequest': 'Medications',
        'MedicationAdministration': 'Medications',
        'Immunization': 'Immunizations',
        'Observation': 'Observations/Vitals/Labs',
        'DiagnosticReport': 'Diagnostics',
        'Procedure': 'Procedures',
        'CarePlan': 'Care Plans',
        'CareTeam': 'Care Team',
        'Goal': 'Goals',
        'DocumentReference': 'Documents',
        'Device': 'Devices',
        'FamilyMemberHistory': 'Family History',
        'Provenance': 'Provenance',
        'QuestionnaireResponse': 'Questionnaires/Forms',
    }
    return categories.get(name, 'Other')


def parse_billing_reports():
    """Parse billing reports HTML to extract report types and their fields."""
    html = open(os.path.join(DOWNLOADS, 'billing-reports.html')).read()
    
    reports = []
    
    # Extract report sections with headings
    headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.DOTALL)
    
    # Extract specific report types mentioned as exportable
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    # Find all mentions of CSV export
    csv_mentions = [m.start() for m in re.finditer(r'CSV|Export as CSV|export.*csv', text, re.IGNORECASE)]
    
    report_types = [
        'Receipts List', 'Procedures List', 'Product Sales List',
        'Procedures by Patient', 'Product Sales By Patient',
        'Receipts by Patient', 'Receipts By Payment Method',
        'Receipts and Refund Report', 'Refunds Report',
        'Payment Collection by Provider', 'Product Sales List',
        'Tax Report (Based on Invoice)', 'Tax Report (Based on Collection)',
        'A/R Aging Report by Patient', 'A/R Aging Report by Provider',
        'Patient Card on File Report', 'Recurring Profile Report',
        'Recurring Profile - Invoice Line Item Report',
        'Encounter Summary Report', 'Write-off / Adjustment Report',
        'Patient Invoice Sent Report', 'EOBs List', 'ERAs (e-Claim) List',
        'Electronic Claim Submission Report'
    ]
    
    for rt in report_types:
        reports.append({
            'name': rt,
            'source': 'Billing Reports (CSV)',
            'category': 'Billing',
            'format': 'CSV',
            'description': f'Exportable billing report: {rt}',
            'fields': [],
            'field_count': 0,
            'has_field_documentation': False
        })
    
    return reports, len(csv_mentions)


def parse_claims_reports():
    """Parse claims HTML to extract claim report types."""
    html = open(os.path.join(DOWNLOADS, 'claims.html')).read()
    
    reports = []
    
    claim_report_types = [
        'Claims List', 'Claims Aging Report by Payer',
        'Claims by Patient', 'Claims by Provider',
        'Claim Procedures List'
    ]
    
    for rt in claim_report_types:
        reports.append({
            'name': rt,
            'source': 'Claims Reports (CSV)',
            'category': 'Claims',
            'format': 'CSV',
            'description': f'Exportable claims report: {rt}',
            'fields': [],
            'field_count': 0,
            'has_field_documentation': False
        })
    
    return reports


def parse_analytics_reports():
    """Parse analytics page for insurance report."""
    reports = [{
        'name': 'Patient Insurance Report',
        'source': 'Analytics Reports (CSV)',
        'category': 'Insurance',
        'format': 'CSV',
        'description': 'Patient insurance information report, exportable as CSV',
        'fields': [],
        'field_count': 0,
        'has_field_documentation': False
    }]
    return reports


def build_full_inventory():
    """Build complete entity inventory from all sources."""
    
    # Parse FHIR API
    fhir_entities, bulk_export, ccda = parse_fhir_api()
    
    # Parse billing reports
    billing_reports, csv_mention_count = parse_billing_reports()
    
    # Parse claims reports
    claims_reports = parse_claims_reports()
    
    # Parse analytics
    analytics_reports = parse_analytics_reports()
    
    # Combine all
    all_entities = fhir_entities + billing_reports + claims_reports + analytics_reports
    
    # Build full inventory
    inventory = {
        'product': 'CharmHealth EHR',
        'vendor': 'MedicalMine Inc.',
        'extraction_date': '2026-02-16',
        'sources': {
            'fhir_api': {
                'description': 'FHIR R4 API documentation with 24 resources',
                'format': 'FHIR R4 JSON / NDJSON',
                'entity_count': len(fhir_entities),
                'total_search_params': sum(e['search_parameter_count'] for e in fhir_entities),
                'us_core_profiles': sum(1 for e in fhir_entities if e['profile'] == 'US Core'),
                'base_profiles': sum(1 for e in fhir_entities if e['profile'] != 'US Core'),
            },
            'bulk_export': {
                'description': bulk_export.get('description', ''),
                'operations': [op.get('name', '') for op in bulk_export.get('operations', [])],
            },
            'ccda': {
                'description': ccda.get('description', ''),
                'api_url': ccda.get('apiUrl', ''),
            },
            'billing_csv': {
                'description': 'Billing reports exportable as CSV',
                'report_count': len(billing_reports),
                'csv_mentions_in_doc': csv_mention_count,
            },
            'claims_csv': {
                'description': 'Claims reports exportable as CSV',
                'report_count': len(claims_reports),
            },
            'analytics_csv': {
                'description': 'Analytics/insurance reports exportable as CSV',
                'report_count': len(analytics_reports),
            }
        },
        'entities': all_entities
    }
    
    return inventory


def build_summary(inventory):
    """Build summary statistics from the full inventory."""
    entities = inventory['entities']
    
    fhir_entities = [e for e in entities if e['source'] == 'FHIR R4 API']
    billing_entities = [e for e in entities if 'CSV' in e.get('source', '')]
    
    # Count fields
    total_fhir_fields = sum(e['field_count'] for e in fhir_entities)
    total_fhir_search_params = sum(e['search_parameter_count'] for e in fhir_entities)
    fields_with_descriptions = sum(
        sum(1 for f in e['fields'] if f.get('has_description')) 
        for e in entities
    )
    total_fields = sum(e['field_count'] for e in entities)
    
    # Category breakdown
    categories = {}
    for e in entities:
        cat = e.get('category', 'Other')
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'field_count': 0}
        categories[cat]['entity_count'] += 1
        categories[cat]['field_count'] += e['field_count']
    
    # USCDI coverage check
    uscdi_resources = {
        'AllergyIntolerance', 'CarePlan', 'CareTeam', 'Condition',
        'Device', 'DiagnosticReport', 'DocumentReference', 'Encounter',
        'FamilyMemberHistory', 'Goal', 'Immunization', 'Location',
        'MedicationRequest', 'Medication', 'Observation', 'Organization',
        'Patient', 'Practitioner', 'Procedure', 'Provenance', 'RelatedPerson'
    }
    
    fhir_names = {e['name'] for e in fhir_entities}
    uscdi_covered = uscdi_resources & fhir_names
    uscdi_missing = uscdi_resources - fhir_names
    beyond_uscdi = fhir_names - uscdi_resources
    
    summary = {
        'total_entities': len(entities),
        'fhir_entities': len(fhir_entities),
        'billing_report_entities': len(billing_entities),
        'total_fields_from_examples': total_fhir_fields,
        'total_search_parameters': total_fhir_search_params,
        'fields_with_descriptions': fields_with_descriptions,
        'description_percentage': round(fields_with_descriptions / total_fields * 100, 1) if total_fields > 0 else 0,
        'us_core_profiles': sum(1 for e in fhir_entities if e['profile'] == 'US Core'),
        'base_fhir_profiles': sum(1 for e in fhir_entities if e['profile'] != 'US Core'),
        'categories': categories,
        'uscdi_coverage': {
            'covered': sorted(list(uscdi_covered)),
            'missing': sorted(list(uscdi_missing)),
            'beyond_uscdi': sorted(list(beyond_uscdi)),
            'coverage_pct': round(len(uscdi_covered) / len(uscdi_resources) * 100, 1)
        },
        'export_formats': ['FHIR R4 JSON', 'NDJSON (Bulk)', 'HL7 C-CDA', 'CSV (Billing/Claims)'],
        'export_mechanisms': [
            'FHIR API (single patient)',
            'Bulk Export API (multi-patient NDJSON)',
            'C-CDA API (single patient)',
            'C-CDA UI export (per encounter)',
            'CSV download from billing/claims reports UI'
        ]
    }
    
    return summary


def main():
    inventory = build_full_inventory()
    summary = build_summary(inventory)
    
    # Save full inventory
    with open(os.path.join(OUTPUT_DIR, 'entity-inventory-full.json'), 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Save summary
    with open(os.path.join(OUTPUT_DIR, 'entity-inventory-summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total entities: {summary['total_entities']}")
    print(f"  FHIR resources: {summary['fhir_entities']}")
    print(f"  Billing/Claims CSV reports: {summary['billing_report_entities']}")
    print(f"  US Core profiles: {summary['us_core_profiles']}")
    print(f"  Base FHIR profiles: {summary['base_fhir_profiles']}")
    print(f"Fields from examples: {summary['total_fields_from_examples']}")
    print(f"Search parameters: {summary['total_search_parameters']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_percentage']}%)")
    print(f"\nUSCDI coverage: {summary['uscdi_coverage']['coverage_pct']}%")
    print(f"  Beyond USCDI: {summary['uscdi_coverage']['beyond_uscdi']}")
    print(f"\nCategories:")
    for cat, info in sorted(summary['categories'].items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print(f"\nExport formats: {summary['export_formats']}")


if __name__ == '__main__':
    main()
