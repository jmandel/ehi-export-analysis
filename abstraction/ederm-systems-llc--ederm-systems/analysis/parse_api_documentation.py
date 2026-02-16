#!/usr/bin/env python3
"""
Parse the eDerm API Documentation PDF to extract:
1. All API endpoints documented
2. All C-CDA data sections/parameters available via GetPatientData
3. C-CDA sections present in the sample response
4. Output a full-entity-inventory.json with all available data fields
"""

import subprocess
import json
import re
import sys
import os

DOWNLOADS = '/home/jmandel/hobby/ehi-export-analysis/results/ederm-systems-llc--ederm-systems/downloads'
PDF_PATH = os.path.join(DOWNLOADS, 'eDerm-API-Documentation-G8-G9.pdf')

# Extract full text from PDF
result = subprocess.run(['pdftotext', '-layout', PDF_PATH, '-'], 
                       capture_output=True, text=True)
text = result.stdout

# Parse GetPatientData boolean parameters using straight quotes
param_pattern = re.compile(r'"(\w+)":\s*"true"')
params = set()
for m in param_pattern.finditer(text):
    name = m.group(1)
    if name not in ('patientid', 'returnformat'):
        params.add(name)

# Parse the mapping table at the end of the PDF (CCDA Element -> parameter)
# The table has format: "  Element Name            "parameter": "true"" with Possible Value column
# Only match lines where the element name starts with an uppercase letter (not JSON body lines)
ccda_element_pattern = re.compile(
    r'^\s+([A-Z][A-Za-z\s()]+?)\s{2,}"(\w+)":\s*"true"', re.MULTILINE
)
ccda_elements = []
seen_params = set()
for m in ccda_element_pattern.finditer(text):
    element_name = m.group(1).strip()
    param_name = m.group(2).strip()
    if param_name not in ('patientid', 'returnformat') and param_name not in seen_params:
        seen_params.add(param_name)
        ccda_elements.append({
            'ccda_element': element_name,
            'parameter': param_name,
            'possible_values': 'true / false'
        })

# Parse C-CDA sections from the sample response
section_pattern = re.compile(r'<title>([^<]+?)</title>')
ccda_sections = list(set(section_pattern.findall(text)))
ccda_sections.sort()

# Parse API endpoints
endpoints = []
url_pattern = re.compile(r'URL:\s*POST\s+(https?://\S+)')
for m in url_pattern.finditer(text):
    url = m.group(1)
    if url not in [e['url'] for e in endpoints]:
        endpoints.append({'method': 'POST', 'url': url})

# Build inventory
inventory = {
    'source': 'eDerm-API-Documentation-G8-G9.pdf',
    'source_type': 'API documentation PDF (26 pages)',
    'documentation_date': '2022-08-08',
    'product_version': '2.8.0',
    'api_type': 'Proprietary REST API (not FHIR)',
    'export_format': 'C-CDA 2.1 (XML), JSON, or HTML',
    'endpoints': endpoints,
    'data_parameters': sorted(list(params)),
    'ccda_element_mapping': ccda_elements,
    'ccda_sections_in_sample': ccda_sections,
    'parameter_count': len(params),
    'ccda_section_count': len(ccda_sections),
    'notes': [
        'API returns C-CDA documents, not native database export',
        'No data dictionary or field-level documentation provided',
        'Sample URLs reference internal hostname "remotedev-5"',
        '"Terms of Use: TBD: Link will be added here" — documentation appears unfinished',
        'No bulk export capability documented',
        'Patient-by-patient API only',
    ]
}

# Build full entity inventory (what we can extract from this minimal documentation)
entities = []

# The only "entity" is the C-CDA document with its sections
for elem in ccda_elements:
    entities.append({
        'entity_name': elem['parameter'],
        'entity_label': elem['ccda_element'],
        'source': 'GetPatientData API parameter',
        'format': 'C-CDA section',
        'fields': [],  # No field-level documentation available
        'field_count': 0,
        'fields_with_descriptions': 0,
        'fields_with_types': 0,
        'description': f"Boolean toggle to include {elem['ccda_element']} section in C-CDA output",
        'category': 'USCDI Clinical Summary'
    })

full_inventory = {
    'extraction_source': 'eDerm-API-Documentation-G8-G9.pdf',
    'extraction_method': 'PDF text extraction + regex parsing',
    'total_entities': len(entities),
    'total_fields': 0,
    'fields_with_descriptions': 0,
    'fields_with_types': 0,
    'entities': entities,
    'notes': [
        'No field-level documentation exists in the source artifacts',
        'Entities represent C-CDA section toggles, not database tables',
        'This is NOT a native data model export — it is a C-CDA API',
        'No data dictionary was provided by the vendor'
    ]
}

# Save outputs
output_dir = '/home/jmandel/hobby/ehi-export-analysis/abstraction/ederm-systems-llc--ederm-systems/analysis'

with open(os.path.join(output_dir, 'api-inventory.json'), 'w') as f:
    json.dump(inventory, f, indent=2)

with open(os.path.join(output_dir, 'full-entity-inventory.json'), 'w') as f:
    json.dump(full_inventory, f, indent=2)

# Print summary
print("=== eDerm API Documentation Analysis ===")
print(f"\nEndpoints found: {len(endpoints)}")
for ep in endpoints:
    print(f"  {ep['method']} {ep['url']}")

print(f"\nGetPatientData parameters: {len(params)}")
for p in sorted(params):
    print(f"  - {p}")

print(f"\nC-CDA element mapping (from table):")
for elem in ccda_elements:
    print(f"  {elem['ccda_element']:45s} -> {elem['parameter']}")

print(f"\nC-CDA sections in sample response: {len(ccda_sections)}")
for s in ccda_sections:
    print(f"  - {s}")

print(f"\nTotal entities in inventory: {len(entities)}")
print(f"Total fields documented: 0 (no field-level documentation)")
print(f"\nSaved: api-inventory.json, full-entity-inventory.json")
