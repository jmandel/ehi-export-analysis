"""
Parse the full EyeMD EMR FHIR API Postman collection including:
- Collection-level description with USCDI mappings
- All resource folders with search parameters
- Export endpoints
Produces entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import re
from html.parser import HTMLParser


class TableParser(HTMLParser):
    """Parse HTML tables into list of row-lists."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = ""
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.current_table = []
        elif tag == 'tr':
            self.current_row = []
        elif tag in ('td', 'th'):
            self.in_cell = True
            self.current_cell = ""
        elif tag == 'br' and self.in_cell:
            self.current_cell += " | "

    def handle_endtag(self, tag):
        if tag == 'table':
            self.tables.append(self.current_table)
        elif tag == 'tr':
            self.current_table.append(self.current_row)
        elif tag in ('td', 'th'):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data.strip()


def strip_html(html_str):
    if not html_str:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', html_str)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def parse_tables_from_html(html):
    parser = TableParser()
    parser.feed(html)
    return parser.tables


def parse_uscdi_mappings(html):
    """Extract USCDI v3 mapping tables from the collection description."""
    # Find the USCDI section
    uscdi_idx = html.lower().find('uscdi mappings')
    if uscdi_idx < 0:
        return []
    
    uscdi_html = html[uscdi_idx:]
    
    # Parse section headers and their tables
    sections = re.split(r'<h2[^>]*>(.*?)</h2>', uscdi_html)
    
    mappings = []
    i = 1
    while i < len(sections):
        section_name = strip_html(sections[i])
        section_content = sections[i + 1] if i + 1 < len(sections) else ""
        
        tables = parse_tables_from_html(section_content)
        for table in tables:
            if not table:
                continue
            headers = table[0]
            for row in table[1:]:
                mapping = {
                    'uscdi_class': section_name,
                }
                for j, h in enumerate(headers):
                    if j < len(row):
                        key = h.lower().replace(' ', '_').replace('/', '_')
                        mapping[key] = row[j]
                mappings.append(mapping)
        i += 2
    
    return mappings


def parse_resource_folders(items):
    """Parse each resource folder for search parameters and endpoints."""
    skip = {'System Level Operations', 'Export', 'App Registration'}
    resources = []
    
    for item in items:
        name = item.get('name', '')
        desc = item.get('description', '')
        sub_items = item.get('item', [])
        
        # Parse search parameter tables from folder description
        search_params = []
        if desc:
            tables = parse_tables_from_html(desc)
            for table in tables:
                if not table:
                    continue
                headers = [h.lower().strip() for h in table[0]]
                for row in table[1:]:
                    param = {}
                    for j, h in enumerate(headers):
                        if j < len(row):
                            param[h] = row[j]
                    if param:
                        search_params.append(param)
        
        # Parse endpoints
        endpoints = []
        resource_type = None
        for si in sub_items:
            req = si.get('request', {})
            method = req.get('method', '')
            url = req.get('url', '')
            if isinstance(url, dict):
                raw = url.get('raw', '')
            else:
                raw = str(url)
            
            endpoints.append({
                'name': si.get('name', ''),
                'method': method,
                'url': raw,
                'description': strip_html(si.get('description', ''))
            })
            
            if '{{base}}/' in raw:
                path = raw.split('{{base}}/')[1].split('?')[0].split('/')[0]
                if path and path[0].isupper() and not path.startswith('$'):
                    resource_type = path
        
        resources.append({
            'folder_name': name,
            'resource_type': resource_type or name.replace(' ', ''),
            'description': strip_html(desc)[:300] if desc else '',
            'search_parameters': search_params,
            'endpoints': endpoints,
            'is_resource': name not in skip,
            'category': 'FHIR Resource' if name not in skip else 'System'
        })
    
    return resources


def main():
    with open('../downloads/eyemd-fhir-api-postman-collection.json') as f:
        data = json.load(f)

    # Parse collection-level description for USCDI mappings and other content
    info = data.get('info', {})
    collection_desc = info.get('description', '')
    
    # Save raw description
    with open('collection-description.html', 'w') as f:
        f.write(collection_desc)
    
    # Parse USCDI mappings
    uscdi_mappings = parse_uscdi_mappings(collection_desc)
    
    # Extract other sections from collection description
    # Look for sections before USCDI
    desc_plain = strip_html(collection_desc)
    
    # Parse resource folders
    items = data.get('item', [])
    resources = parse_resource_folders(items)
    
    resource_items = [r for r in resources if r['is_resource']]
    system_items = [r for r in resources if not r['is_resource']]
    
    # Deduplicate resource types (Coverage folder points to Condition URLs - likely a bug)
    resource_types = set()
    for r in resource_items:
        resource_types.add(r['resource_type'])
    
    # Build full inventory
    full_inventory = {
        'product': 'EyeMD Electronic Medical Records',
        'source': 'EyeMD EMR FHIR API Postman Collection',
        'source_file': 'downloads/eyemd-fhir-api-postman-collection.json',
        'export_format': 'FHIR R4 (NDJSON via Bulk Data $export)',
        'collection_description_length': len(collection_desc),
        'statistics': {
            'total_folders': len(items),
            'resource_folders': len(resource_items),
            'unique_resource_types': len(resource_types),
            'total_search_parameters': sum(len(r['search_parameters']) for r in resource_items),
            'total_endpoints': sum(len(r['endpoints']) for r in resources),
            'uscdi_mapping_entries': len(uscdi_mappings),
        },
        'resource_types_list': sorted(resource_types),
        'entities': [],
        'uscdi_mappings': uscdi_mappings,
        'system_operations': system_items,
        'notes': [
            'Coverage folder description and URLs appear to reference Condition (likely a copy-paste error in the Postman collection)',
            'Export folder has 2 endpoints with zero documentation (no descriptions)',
            'No field-level data dictionary exists - only search parameters are documented',
            'No vendor-specific FHIR extensions are documented (though they exist per the Endpoints bundle)',
            'Documentation is explicitly for (g)(10) standardized API, never mentions (b)(10) or EHI'
        ]
    }
    
    for r in resource_items:
        entity = {
            'name': r['folder_name'],
            'resource_type': r['resource_type'],
            'description': r['description'],
            'fields': r['search_parameters'],  # search params are the closest to "fields"
            'field_count': len(r['search_parameters']),
            'endpoints': r['endpoints'],
            'endpoint_count': len(r['endpoints']),
            'has_description': bool(r['description']),
        }
        full_inventory['entities'].append(entity)
    
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(full_inventory, f, indent=2)
    
    # Summary
    summary = {
        'product': 'EyeMD Electronic Medical Records',
        'source': 'EyeMD EMR FHIR API Postman Collection',
        'export_format': 'FHIR R4 (NDJSON via Bulk Data $export)',
        'statistics': full_inventory['statistics'],
        'resource_types': sorted(resource_types),
        'resources_by_detail': [],
        'uscdi_classes_covered': [],
        'coverage_notes': {
            'what_is_documented': 'Standard FHIR R4 resources with US Core STU6.1 profiles. Only search parameters are documented per resource - no field-level data dictionary exists.',
            'what_is_missing': 'No ophthalmology-specific data, no billing/claims, no optical shop data, no patient engagement data, no imaging data, no surgical details, no practice management data.',
            'export_documentation': 'The $export endpoint (Bulk Data) has zero documentation - no description of what resource types are included, what data elements are populated, or how to interpret output.',
        }
    }
    
    for r in resource_items:
        summary['resources_by_detail'].append({
            'name': r['folder_name'],
            'resource_type': r['resource_type'],
            'search_params': len(r['search_parameters']),
            'endpoints': len(r['endpoints']),
        })
    
    # Summarize USCDI classes
    uscdi_classes = set()
    for m in uscdi_mappings:
        uscdi_classes.add(m.get('uscdi_class', ''))
    summary['uscdi_classes_covered'] = sorted(uscdi_classes)
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print report
    print("=" * 60)
    print("EyeMD EMR FHIR API - Postman Collection Analysis")
    print("=" * 60)
    print(f"\nCollection description: {len(collection_desc):,} characters")
    print(f"Total folders: {len(items)}")
    print(f"FHIR resource folders: {len(resource_items)}")
    print(f"Unique FHIR resource types: {len(resource_types)}")
    print(f"Total search parameters: {sum(len(r['search_parameters']) for r in resource_items)}")
    print(f"Total endpoints: {sum(len(r['endpoints']) for r in resources)}")
    print(f"USCDI mapping entries: {len(uscdi_mappings)}")
    
    print(f"\nUSCDI Data Classes mapped ({len(uscdi_classes)}):")
    for c in sorted(uscdi_classes):
        count = sum(1 for m in uscdi_mappings if m.get('uscdi_class') == c)
        print(f"  {c}: {count} entries")
    
    print(f"\nFHIR Resource Types ({len(resource_types)}):")
    for r in sorted(resource_types):
        matching = [x for x in resource_items if x['resource_type'] == r]
        params = sum(len(x['search_parameters']) for x in matching)
        print(f"  {r:25s} | {params:2d} search params")
    
    print("\nExport endpoints:")
    for r in resources:
        if r['folder_name'] == 'Export':
            for ep in r['endpoints']:
                print(f"  {ep['method']} {ep['url']}")
                print(f"    Description: {ep['description'] or '(none)'}")


if __name__ == '__main__':
    main()
