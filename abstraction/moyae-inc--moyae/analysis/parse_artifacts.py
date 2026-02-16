#!/usr/bin/env python3
"""
Parse all Moyae EHI export artifacts and produce full-entity-inventory.json
and summary statistics.

Inputs:
  - downloads/fhir-capability-statement.json (FHIR R4 CapabilityStatement)
  - downloads/moyae-fhir-api-postman-collection.json (Postman collection)
  - downloads/disclosures-and-costs.html (Disclosures page)

Outputs:
  - analysis/full-entity-inventory.json
  - analysis/summary-stats.json
  - stdout: summary statistics
"""
import json
import sys
import os
from collections import defaultdict
from html.parser import HTMLParser

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'results', 'moyae-inc--moyae', 'downloads')
OUTPUT_DIR = os.path.dirname(__file__)

# --- Parse CapabilityStatement ---
with open(os.path.join(RESULTS_DIR, 'fhir-capability-statement.json')) as f:
    cs = json.load(f)

rest = cs['rest'][0]
resources = rest['resource']

# Categorize resources
CLINICAL_TYPES = {
    'AllergyIntolerance', 'CarePlan', 'CareTeam', 'ClinicalImpression',
    'Communication', 'Composition', 'Condition', 'Consent', 'Device',
    'DeviceUseStatement', 'DiagnosticReport', 'DocumentReference',
    'Encounter', 'EpisodeOfCare', 'FamilyMemberHistory', 'Goal',
    'ImagingStudy', 'Immunization', 'Media', 'MedicationAdministration',
    'MedicationDispense', 'MedicationRequest', 'MedicationStatement',
    'NutritionOrder', 'Observation', 'Patient', 'Procedure',
    'Questionnaire', 'QuestionnaireResponse', 'RelatedPerson',
    'RiskAssessment', 'Specimen', 'VisionPrescription'
}
FINANCIAL_TYPES = {
    'Account', 'ChargeItem', 'ChargeItemDefinition', 'Claim', 'ClaimResponse',
    'Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse',
    'EnrollmentRequest', 'EnrollmentResponse', 'ExplanationOfBenefit',
    'InsurancePlan', 'Invoice', 'PaymentNotice', 'PaymentReconciliation'
}
ADMIN_TYPES = {
    'Appointment', 'AppointmentResponse', 'Endpoint', 'HealthcareService',
    'Location', 'Organization', 'Person', 'Practitioner', 'PractitionerRole',
    'Schedule', 'Slot'
}

def categorize(rtype):
    if rtype in CLINICAL_TYPES:
        return 'clinical'
    elif rtype in FINANCIAL_TYPES:
        return 'financial'
    elif rtype in ADMIN_TYPES:
        return 'administrative'
    else:
        return 'infrastructure/conformance'

# Build full inventory
inventory = []
for r in resources:
    rtype = r['type']
    interactions = sorted([i['code'] for i in r.get('interaction', [])])
    search_params = []
    for sp in r.get('searchParam', []):
        search_params.append({
            'name': sp.get('name'),
            'type': sp.get('type'),
            'documentation': sp.get('documentation', '')
        })
    
    supported_profiles = r.get('supportedProfile', [])
    has_us_core = any('us-core' in p for p in supported_profiles)
    
    entry = {
        'resourceType': rtype,
        'category': categorize(rtype),
        'interactions': interactions,
        'searchParams': search_params,
        'searchParamCount': len(search_params),
        'supportedProfiles': supported_profiles,
        'hasUSCoreProfile': has_us_core,
        'versioning': r.get('versioning'),
        'conditionalCreate': r.get('conditionalCreate', False),
        'conditionalUpdate': r.get('conditionalUpdate', False),
        'conditionalDelete': r.get('conditionalDelete', 'not-supported'),
    }
    inventory.append(entry)

# --- Parse Postman collection for endpoint details ---
with open(os.path.join(RESULTS_DIR, 'moyae-fhir-api-postman-collection.json')) as f:
    pm = json.load(f)

postman_folders = {}
for item in pm.get('item', []):
    name = item.get('name', '')
    sub_items = item.get('item', [])
    endpoints = []
    for sub in sub_items:
        if 'request' in sub:
            req = sub['request']
            url = req.get('url', {})
            raw = url.get('raw', '') if isinstance(url, dict) else url
            params = url.get('query', []) if isinstance(url, dict) else []
            endpoints.append({
                'name': sub.get('name', ''),
                'method': req.get('method', ''),
                'url': raw,
                'hasDescription': bool(req.get('description', '').strip()),
                'hasResponseExample': bool(sub.get('response', [])),
                'queryParamCount': len(params)
            })
    postman_folders[name] = {
        'endpointCount': len(endpoints),
        'endpoints': endpoints
    }

# --- Extract CCDA sections from sample ---
ccda_sections = []
for item in pm['item']:
    if item.get('name') == 'CCDA':
        for sub in item.get('item', []):
            if sub.get('name') == 'CCDA_GET' and sub.get('response'):
                body = sub['response'][0].get('body', '')
                if body:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(body)
                    ns = '{urn:hl7-org:v3}'
                    for comp in root.findall(f'.//{ns}component/{ns}structuredBody/{ns}component'):
                        section = comp.find(f'{ns}section')
                        if section is not None:
                            title = section.find(f'{ns}title')
                            entries = section.findall(f'{ns}entry')
                            templates = [t.get('root', '') for t in section.findall(f'{ns}templateId')]
                            ccda_sections.append({
                                'title': title.text if title is not None else 'Untitled',
                                'entryCount': len(entries),
                                'templateIds': templates
                            })

# --- Compute summary statistics ---
category_counts = defaultdict(lambda: {'count': 0, 'with_us_core': 0, 'total_search_params': 0})
for entry in inventory:
    cat = entry['category']
    category_counts[cat]['count'] += 1
    if entry['hasUSCoreProfile']:
        category_counts[cat]['with_us_core'] += 1
    category_counts[cat]['total_search_params'] += entry['searchParamCount']

us_core_resources = [e['resourceType'] for e in inventory if e['hasUSCoreProfile']]
total_search_params = sum(e['searchParamCount'] for e in inventory)

# Postman stats
total_postman_endpoints = sum(f['endpointCount'] for f in postman_folders.values())
endpoints_with_desc = sum(
    1 for f in postman_folders.values()
    for e in f['endpoints']
    if e['hasDescription']
)
endpoints_with_responses = sum(
    1 for f in postman_folders.values()
    for e in f['endpoints']
    if e['hasResponseExample']
)

summary = {
    'capabilityStatement': {
        'totalResourceTypes': len(inventory),
        'fhirVersion': cs.get('fhirVersion'),
        'publisher': cs.get('publisher'),
        'softwareVersion': cs.get('software', {}).get('version'),
        'operations': [o['name'] for o in rest.get('operation', [])],
        'categoryCounts': dict(category_counts),
        'usCoreSupportedResources': us_core_resources,
        'usCoreSupportedCount': len(us_core_resources),
        'totalSearchParams': total_search_params,
    },
    'postmanCollection': {
        'totalFolders': len(postman_folders),
        'totalEndpoints': total_postman_endpoints,
        'endpointsWithDescriptions': endpoints_with_desc,
        'endpointsWithResponseExamples': endpoints_with_responses,
        'exportEndpoints': postman_folders.get('Export', {}).get('endpoints', []),
        'ccdaEndpoints': postman_folders.get('CCDA', {}).get('endpoints', []),
    },
    'ccdaSample': {
        'available': len(ccda_sections) > 0,
        'sectionCount': len(ccda_sections),
        'sections': ccda_sections,
        'totalEntries': sum(s['entryCount'] for s in ccda_sections),
    },
    'exportMechanism': {
        'type': 'FHIR Bulk Data $export',
        'format': 'NDJSON (Newline Delimited JSON)',
        'fhirVersion': '4.0.1',
        'endpoint': '{{API_URL}}/$export',
        'parameters': ['_outputFormat', '_since', '_type'],
        'authentication': 'OAuth2/SMART on FHIR (Auth0-based)',
        'jobManagement': True,
    }
}

# Write outputs
with open(os.path.join(OUTPUT_DIR, 'full-entity-inventory.json'), 'w') as f:
    json.dump({
        'generatedAt': '2026-02-16',
        'source': 'FHIR CapabilityStatement + Postman Collection',
        'totalResourceTypes': len(inventory),
        'resources': inventory,
        'postmanFolders': postman_folders,
        'ccdaSample': {
            'sections': ccda_sections
        }
    }, f, indent=2)

with open(os.path.join(OUTPUT_DIR, 'summary-stats.json'), 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== Moyae EHI Export Artifact Analysis ===\n")
print(f"CapabilityStatement: {len(inventory)} resource types")
print(f"  Clinical: {category_counts['clinical']['count']}")
print(f"  Financial: {category_counts['financial']['count']}")
print(f"  Administrative: {category_counts['administrative']['count']}")
print(f"  Infrastructure/conformance: {category_counts['infrastructure/conformance']['count']}")
print(f"  Total search parameters: {total_search_params}")
print(f"  US Core profiled resources: {len(us_core_resources)}")
print(f"    {us_core_resources}")
print(f"\nPostman Collection: {total_postman_endpoints} endpoints in {len(postman_folders)} folders")
print(f"  Endpoints with descriptions: {endpoints_with_desc}")
print(f"  Endpoints with response examples: {endpoints_with_responses}")
print(f"\nC-CDA Sample: {len(ccda_sections)} sections, {sum(s['entryCount'] for s in ccda_sections)} total entries")
for s in ccda_sections:
    print(f"  {s['title']}: {s['entryCount']} entries")
print(f"\nExport: FHIR Bulk Data $export (NDJSON)")
print(f"  Authentication: OAuth2/SMART on FHIR")
print(f"\nFiles written:")
print(f"  analysis/full-entity-inventory.json")
print(f"  analysis/summary-stats.json")
