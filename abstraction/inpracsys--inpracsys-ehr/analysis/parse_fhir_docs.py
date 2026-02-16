"""
Parse the InPracSys FHIR API documentation HTML page (Elementor-based).
The page has h2 headings for resource types, h3 for sub-sections, and tables
for request parameters and response field definitions. Tables with a 
"Cardinality" header are response field definitions; those with "Required?"
are request parameter tables. We extract both.
Outputs full-entity-inventory.json and parse-summary.json.
"""

import json
import re
from bs4 import BeautifulSoup

HTML_FILE = '/home/jmandel/hobby/ehi-export-analysis/results/inpracsys--inpracsys-ehr/downloads/fhir-api-documentation-page.html'
OUTPUT_FILE = 'full-entity-inventory.json'
SUMMARY_FILE = 'parse-summary.json'

with open(HTML_FILE, 'r', encoding='utf-8', errors='replace') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

# Map from h2 heading text -> resource name for grouping
h2_to_resource = {}
for h2 in soup.find_all('h2'):
    title = h2.get_text(strip=True)
    if title != 'Overview':
        h2_to_resource[title] = {
            'name': title,
            'h3_description': None,
            'request_params': [],
            'response_fields': [],
            'endpoint': None,
            'sample_json': None,
        }

# For each table, find its closest h2 and h3 ancestors/predecessors
tables = soup.find_all('table')

for table in tables:
    rows = table.find_all('tr')
    if len(rows) < 2:
        continue

    # Get headers
    header_cells = rows[0].find_all(['th', 'td'])
    headers = [c.get_text(strip=True) for c in header_cells]
    headers_lower = [h.lower() for h in headers]

    # Find closest preceding h2
    closest_h2 = None
    for prev_h2 in table.find_all_previous('h2'):
        closest_h2 = prev_h2.get_text(strip=True)
        break

    if not closest_h2 or closest_h2 not in h2_to_resource:
        continue

    resource = h2_to_resource[closest_h2]

    # Find closest preceding h3 for context
    closest_h3 = None
    for prev_h3 in table.find_all_previous('h3'):
        closest_h3 = prev_h3.get_text(strip=True)
        break

    if not resource['h3_description']:
        resource['h3_description'] = closest_h3

    # Determine table type
    is_response = 'cardinality' in headers_lower
    is_request = 'required?' in headers_lower or 'required' in headers_lower

    # Parse rows
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        entry = {}
        for i, cell in enumerate(cells):
            if i < len(headers):
                entry[headers[i]] = cell.get_text(strip=True)
            else:
                entry[f'col_{i}'] = cell.get_text(strip=True)
        
        if is_response:
            resource['response_fields'].append(entry)
        elif is_request:
            resource['request_params'].append(entry)

# Now extract endpoints and sample JSON from the full page text
# Look for endpoint URLs in text near each resource section
all_text_blocks = soup.find_all(['p', 'div', 'span'])
for block in all_text_blocks:
    text = block.get_text(strip=True)
    url_match = re.search(r'(https?://\S+fhir\S*/\w+)', text)
    if url_match:
        url = url_match.group(1)
        # Find closest h2
        for prev_h2 in block.find_all_previous('h2'):
            h2_text = prev_h2.get_text(strip=True)
            if h2_text in h2_to_resource and not h2_to_resource[h2_text]['endpoint']:
                h2_to_resource[h2_text]['endpoint'] = url
            break

# Extract sample JSON from code/pre blocks
for code_block in soup.find_all(['pre', 'code']):
    text = code_block.get_text()
    if '{' not in text or len(text.strip()) < 20:
        continue
    for prev_h2 in code_block.find_all_previous('h2'):
        h2_text = prev_h2.get_text(strip=True)
        if h2_text in h2_to_resource and not h2_to_resource[h2_text]['sample_json']:
            h2_to_resource[h2_text]['sample_json'] = text.strip()[:3000]
        break

# Build output
resources = list(h2_to_resource.values())

with open(OUTPUT_FILE, 'w') as f:
    json.dump(resources, f, indent=2)

# Compute summary
total_response_fields = sum(len(r['response_fields']) for r in resources)
total_request_params = sum(len(r['request_params']) for r in resources)
total_resources = len(resources)

fields_with_desc = 0
fields_with_type = 0
for r in resources:
    for field in r['response_fields']:
        if field.get('Description', '').strip():
            fields_with_desc += 1
        if field.get('Type', '').strip():
            fields_with_type += 1

summary = {
    'total_resources': total_resources,
    'total_response_fields': total_response_fields,
    'total_request_params': total_request_params,
    'fields_with_descriptions': fields_with_desc,
    'fields_with_types': fields_with_type,
    'resources': []
}

for r in resources:
    rsummary = {
        'name': r['name'],
        'h3_description': r['h3_description'],
        'response_field_count': len(r['response_fields']),
        'request_param_count': len(r['request_params']),
        'has_endpoint': bool(r['endpoint']),
        'has_sample_json': bool(r['sample_json']),
        'endpoint': r['endpoint'],
    }
    if r['response_fields']:
        rsummary['sample_field'] = r['response_fields'][0]
    summary['resources'].append(rsummary)

with open(SUMMARY_FILE, 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
