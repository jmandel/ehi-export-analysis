#!/usr/bin/env python3
"""
Parse all EHI export artifacts for Agastha and produce:
1. full-entity-inventory.json - complete inventory of all FHIR resources documented
2. analysis-summary.json - summary statistics
"""

import json
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser

DOWNLOADS = Path(__file__).parent.parent.parent.parent / "results" / "agastha-inc--agastha-enterprise-healthcare-software" / "downloads"
OUTPUT_DIR = Path(__file__).parent

# ============================================================
# 1. Parse PDF text (already extracted)
# ============================================================

def extract_pdf_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(DOWNLOADS / "Agastha-B10-Documentation.pdf"), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_b10_resources(pdf_text):
    """Extract the 21 FHIR resources listed in the B10 PDF."""
    resources = []
    # The resource description table has Name/Description pairs
    lines = pdf_text.split('\n')
    
    resource_names_in_list = [
        "Allergy Intolerance", "Care Plan", "Care Team", "Condition", "Device",
        "Diagnostic Report", "Document Reference", "Encounter", "Goal",
        "Immunization", "Location", "Medication", "Medication Request",
        "Observation", "Organization", "Patient", "Practitioner", "Procedure",
        "Provenance", "Related Person", "Service Request"
    ]
    
    fhir_names = [
        "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
        "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
        "Immunization", "Location", "Medication", "MedicationRequest",
        "Observation", "Organization", "Patient", "Practitioner", "Procedure",
        "Provenance", "RelatedPerson", "ServiceRequest"
    ]
    
    # Parse the description table from the PDF
    descriptions = {}
    current_name = None
    current_desc = []
    
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped == "Resource Description":
            in_table = True
            continue
        if stripped == "Support":
            break
        if not in_table:
            continue
        if stripped == "Name" and "Description" in line:
            continue
            
        # Check if line starts with a resource name
        found_resource = None
        for i, rn in enumerate(resource_names_in_list):
            if stripped.startswith(rn):
                found_resource = (fhir_names[i], stripped[len(rn):].strip())
                break
        
        if found_resource:
            if current_name:
                descriptions[current_name] = ' '.join(current_desc).strip()
            current_name = found_resource[0]
            current_desc = [found_resource[1]] if found_resource[1] else []
        elif current_name and stripped:
            current_desc.append(stripped)
    
    if current_name:
        descriptions[current_name] = ' '.join(current_desc).strip()
    
    return fhir_names, descriptions

# ============================================================
# 2. Parse apiR4.html for additional resource details
# ============================================================

class APIResourceParser(HTMLParser):
    """Parse apiR4.html to extract resource details including example requests/responses."""
    def __init__(self):
        super().__init__()
        self.resources = {}
        self.current_section = None
        self.in_tab_content = False
        self.current_div_id = None
        self.div_depth = 0
        self.capture_depth = 0
        self.captured_text = []
        self.in_pre = False
        self.pre_text = []
        self.in_td = False
        self.td_text = ''
        self.td_texts = []
        self.in_tr = False
        self.tr_tds = []
        self.tables = []
        self.current_table = []
        self.in_table = False
        self.in_b = False
        self.b_text = ''
        self.section_labels = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div':
            self.div_depth += 1
            div_id = attrs_dict.get('id', '')
            if div_id.startswith('list-r'):
                self.current_div_id = div_id
                self.capture_depth = self.div_depth
                self.captured_text = []
        if tag == 'pre':
            self.in_pre = True
            self.pre_text = []
        if tag == 'table':
            self.in_table = True
            self.current_table = []
        if tag == 'tr':
            self.in_tr = True
            self.tr_tds = []
        if tag == 'td':
            self.in_td = True
            self.td_text = ''
        if tag == 'b':
            self.in_b = True
            self.b_text = ''
            
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.div_depth == self.capture_depth and self.current_div_id:
                self.resources[self.current_div_id] = {
                    'text': ' '.join(self.captured_text),
                }
                self.current_div_id = None
            self.div_depth -= 1
        if tag == 'pre':
            self.in_pre = False
        if tag == 'td':
            self.in_td = False
            if self.in_tr:
                self.tr_tds.append(self.td_text.strip())
        if tag == 'tr':
            self.in_tr = False
            if self.in_table and self.tr_tds:
                self.current_table.append(self.tr_tds)
        if tag == 'table':
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = []
        if tag == 'b':
            self.in_b = False
            if self.b_text.strip():
                self.section_labels.append(self.b_text.strip())
                
    def handle_data(self, data):
        if self.current_div_id:
            self.captured_text.append(data.strip())
        if self.in_pre:
            self.pre_text.append(data)
        if self.in_td:
            self.td_text += data
        if self.in_b:
            self.b_text += data

def parse_api_html():
    with open(DOWNLOADS / "apiR4.html") as f:
        content = f.read()
    
    parser = APIResourceParser()
    parser.feed(content)
    
    # Map tab names to FHIR resource names
    tab_to_resource = {
        'list-r1': 'AllergyIntolerance',
        'list-r1a': 'Appointment',
        'list-r2': 'CarePlan',
        'list-r3': 'CareTeam',
        'list-r3a': 'ChargeItem',
        'list-r4': 'Condition',
        'list-r4a': 'Coverage',
        'list-r5': 'Device',
        'list-r6': 'DiagnosticReport',
        'list-r7': 'DocumentReference',
        'list-r8': 'Encounter',
        'list-r8a': 'FamilyMemberHistory',
        'list-r9': 'Goal',
        'list-r10': 'Immunization',
        'list-r11': 'MedicationRequest',
        'list-r12': 'Observation',
        'list-r13': 'Organization',
        'list-r14': 'Patient',
        'list-r15': 'Procedure',
        'list-r16': 'Provenance',
        'list-r17': 'Practitioner',
        'list-r18': 'RelatedPerson',
        'list-r19': 'ServiceRequest',
    }
    
    api_resources = {}
    for tab_id, resource_name in tab_to_resource.items():
        if tab_id in parser.resources:
            text = parser.resources[tab_id]['text']
            # Extract search parameters from the text
            has_example = 'Example' in text or 'Request' in text
            has_search_params = 'patient' in text.lower() or '_id' in text
            api_resources[resource_name] = {
                'documented_in_api': True,
                'has_example': has_example,
                'text_length': len(text),
            }
    
    return api_resources


# ============================================================
# 3. Extract sample JSON from apiR4.html  
# ============================================================

def extract_sample_json_from_api():
    """Extract example JSON responses from apiR4.html to understand field coverage."""
    with open(DOWNLOADS / "apiR4.html") as f:
        content = f.read()
    
    # Find all <pre> blocks which contain example JSON
    pre_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL)
    
    samples = []
    for block in pre_blocks:
        # Clean HTML entities
        text = block.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        text = re.sub(r'<[^>]+>', '', text).strip()
        
        # Try to determine if it's a request or response
        if text.startswith('{') or text.startswith('['):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    rt = parsed.get('resourceType', 'unknown')
                    samples.append({
                        'resourceType': rt,
                        'fields': list(parsed.keys()) if isinstance(parsed, dict) else [],
                        'field_count': len(parsed.keys()) if isinstance(parsed, dict) else 0,
                    })
                elif isinstance(parsed, list) and len(parsed) > 0:
                    if isinstance(parsed[0], dict):
                        rt = parsed[0].get('resourceType', 'unknown')
                        samples.append({
                            'resourceType': rt,
                            'fields': list(parsed[0].keys()),
                            'field_count': len(parsed[0].keys()),
                            'record_count': len(parsed),
                        })
            except json.JSONDecodeError:
                pass
        elif 'GET' in text or 'POST' in text:
            # It's a request example
            pass
    
    return samples


# ============================================================
# 4. Build full entity inventory
# ============================================================

def build_inventory():
    pdf_text = extract_pdf_text()
    b10_resources, b10_descriptions = parse_b10_resources(pdf_text)
    api_resources = parse_api_html()
    sample_jsons = extract_sample_json_from_api()
    
    # All unique resources across B10 and API
    all_resources = set(b10_resources) | set(api_resources.keys())
    
    # FHIR R4 resource category mapping
    resource_categories = {
        'AllergyIntolerance': 'Clinical',
        'Appointment': 'Administrative',
        'CarePlan': 'Clinical',
        'CareTeam': 'Clinical',
        'ChargeItem': 'Financial',
        'Condition': 'Clinical',
        'Coverage': 'Financial',
        'Device': 'Clinical',
        'DiagnosticReport': 'Clinical',
        'DocumentReference': 'Clinical',
        'Encounter': 'Clinical',
        'FamilyMemberHistory': 'Clinical',
        'Goal': 'Clinical',
        'Immunization': 'Clinical',
        'Location': 'Administrative',
        'Medication': 'Clinical',
        'MedicationRequest': 'Clinical',
        'Observation': 'Clinical',
        'Organization': 'Administrative',
        'Patient': 'Administrative',
        'Practitioner': 'Administrative',
        'Procedure': 'Clinical',
        'Provenance': 'Infrastructure',
        'RelatedPerson': 'Administrative',
        'ServiceRequest': 'Clinical',
    }
    
    # Map sample JSON fields to resources
    sample_fields_by_resource = {}
    for s in sample_jsons:
        rt = s['resourceType']
        if rt not in sample_fields_by_resource:
            sample_fields_by_resource[rt] = s
    
    inventory = []
    for resource in sorted(all_resources):
        entry = {
            'resource_name': resource,
            'category': resource_categories.get(resource, 'Unknown'),
            'in_b10_pdf': resource in b10_resources,
            'in_api_docs': resource in api_resources,
            'description': b10_descriptions.get(resource, ''),
            'description_source': 'FHIR R4 specification (verbatim copy)' if resource in b10_descriptions else 'not provided',
            'vendor_specific_documentation': False,  # All descriptions are generic FHIR
            'field_level_documentation': False,
            'fields': [],
        }
        
        if resource in api_resources:
            entry['api_details'] = api_resources[resource]
        
        if resource in sample_fields_by_resource:
            sample = sample_fields_by_resource[resource]
            entry['sample_fields'] = sample['fields']
            entry['sample_field_count'] = sample['field_count']
        
        inventory.append(entry)
    
    return inventory, sample_jsons

# ============================================================
# 5. Build summary statistics
# ============================================================

def build_summary(inventory, sample_jsons):
    total_resources = len(inventory)
    in_b10 = sum(1 for r in inventory if r['in_b10_pdf'])
    in_api = sum(1 for r in inventory if r['in_api_docs'])
    with_description = sum(1 for r in inventory if r['description'])
    with_vendor_specific = sum(1 for r in inventory if r['vendor_specific_documentation'])
    with_field_level = sum(1 for r in inventory if r['field_level_documentation'])
    
    categories = {}
    for r in inventory:
        cat = r['category']
        if cat not in categories:
            categories[cat] = {'count': 0, 'resources': []}
        categories[cat]['count'] += 1
        categories[cat]['resources'].append(r['resource_name'])
    
    b10_only = [r['resource_name'] for r in inventory if r['in_b10_pdf'] and not r['in_api_docs']]
    api_only = [r['resource_name'] for r in inventory if r['in_api_docs'] and not r['in_b10_pdf']]
    
    return {
        'total_unique_resources': total_resources,
        'resources_in_b10_pdf': in_b10,
        'resources_in_api_docs': in_api,
        'resources_with_description': with_description,
        'descriptions_are_vendor_specific': with_vendor_specific,
        'resources_with_field_level_docs': with_field_level,
        'categories': categories,
        'in_b10_only': b10_only,
        'in_api_only': api_only,
        'sample_json_count': len(sample_jsons),
        'sample_resource_types': list(set(s['resourceType'] for s in sample_jsons)),
        'artifacts_analyzed': {
            'Agastha-B10-Documentation.pdf': {
                'pages': 7,
                'size_bytes': 586413,
                'content': '21 FHIR R4 resources with FHIR spec descriptions, export UI screenshots, overview text',
            },
            'dataExport.html': {
                'size_bytes': 5060,
                'content': 'Landing page with version history (v1.0, 2023-04-10) and link to B10 PDF',
            },
            'apiR4.html': {
                'size_bytes': 214752,
                'tables': 50,
                'content': 'FHIR R4 API documentation for (g)(10), covers 23 resources with API endpoints and examples',
            },
        },
    }


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    inventory, sample_jsons = build_inventory()
    summary = build_summary(inventory, sample_jsons)
    
    with open(OUTPUT_DIR / 'full-entity-inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    with open(OUTPUT_DIR / 'analysis-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Inventory: {len(inventory)} resources")
    print(f"Summary saved to analysis-summary.json")
    print(json.dumps(summary, indent=2))
