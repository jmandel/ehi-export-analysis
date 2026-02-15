"""Parse the MicroMD EHI export PDF text to extract XML elements and attributes."""
import re
import json
from collections import defaultdict

with open("ehi-export-text.txt", "r") as f:
    text = f.read()

# Remove page headers/footers
text = re.sub(r'P: 330-758-8832.*?\d+\s*\n', '', text)
text = re.sub(r'\s*micromd\.com\s*', '', text)

# Parse XML-like schema elements with their attributes
# Pattern: <ElementName attr1="" attr2="" .../>  or <ElementName attr1="" ...>
element_pattern = re.compile(r'<(\w+)(?:\s+([^/>]+?))?(?:/>|>)')

# Track which file each element belongs to
current_file = None
file_elements = defaultdict(list)
all_elements = []

# Split by XML file sections  
lines = text.split('\n')
for line in lines:
    # Detect file markers like "• Billing.xml"
    file_match = re.search(r'•\s+(\w+\.xml)', line)
    if file_match:
        current_file = file_match.group(1)
        continue
    
    # Also detect "Additional files from DMS"
    if 'Additional files from DMS' in line:
        current_file = 'DMS (attachments)'
        continue

# Better approach: process the full text looking for elements
# First, identify file boundaries
file_sections = []
file_markers = list(re.finditer(r'•\s+(\w+\.xml)', text))

for i, marker in enumerate(file_markers):
    file_name = marker.group(1)
    start = marker.end()
    if i + 1 < len(file_markers):
        end = file_markers[i + 1].start()
    else:
        end = len(text)
    section_text = text[start:end]
    file_sections.append((file_name, section_text))

# Parse each section
inventory = {}
total_elements = 0
total_attributes = 0

for file_name, section in file_sections:
    elements = []
    # Find all XML element declarations
    for match in re.finditer(r'<(\w+)\s+((?:[a-zA-Z_]\w*=""\s*)+)', section):
        elem_name = match.group(1)
        attrs_text = match.group(2)
        attrs = re.findall(r'([a-zA-Z_]\w*)=""', attrs_text)
        
        # Skip closing tags and container-only tags
        if elem_name in ('Billing', 'Encounters', 'HealthScreening', 'Histories', 
                         'MedicalInfo', 'Miscellaneous', 'Orders', 'Patient', 
                         'Schedule', 'Specialty', 'WomenHealth',
                         'Assessments', 'Subjectives', 'Objectives', 'ReviewProblems',
                         'Medications', 'Plans', 'Notes', 'GoalMonitoring', 'HealthConcern',
                         'Immunizations', 'Prevention', 'Hospital', 'Problems', 'Behavior',
                         'ClinicalDecisionSupport', 'Operation', 'Treatment',
                         'Attachments', 'Addresses', 'Providers', 'Vision', 'Hearing',
                         'Diabetes', 'Genetic', 'Geriatric', 'Allergy',
                         'Obstetrics', 'Genetics', 'Deliveries', 'Prenatal',
                         'Pregnancies', 'Menstrual'):
            # Only skip if it has no attributes
            if not attrs:
                continue
        
        elements.append({
            'name': elem_name,
            'attributes': attrs,
            'attribute_count': len(attrs)
        })
        total_elements += 1
        total_attributes += len(attrs)
    
    inventory[file_name] = {
        'elements': elements,
        'element_count': len(elements),
        'total_attributes': sum(e['attribute_count'] for e in elements)
    }

# Print summary
print("=" * 80)
print("MicroMD EMR EHI Export Schema Inventory")
print("=" * 80)
print(f"\nTotal XML files: {len(inventory)}")
print(f"Total elements (entity types): {total_elements}")
print(f"Total attributes (fields): {total_attributes}")
print()

print(f"{'XML File':<25} {'Elements':>10} {'Attributes':>12}")
print("-" * 50)
for file_name, data in inventory.items():
    print(f"{file_name:<25} {data['element_count']:>10} {data['total_attributes']:>12}")

print()
print("=" * 80)
print("Detailed Element Inventory")
print("=" * 80)

for file_name, data in inventory.items():
    print(f"\n### {file_name}")
    for elem in data['elements']:
        print(f"  {elem['name']}: {elem['attribute_count']} attributes")
        # Print first few attributes as examples
        if elem['attributes']:
            attr_list = ', '.join(elem['attributes'][:5])
            if len(elem['attributes']) > 5:
                attr_list += f", ... (+{len(elem['attributes'])-5} more)"
            print(f"    e.g.: {attr_list}")

# Save full inventory as JSON
output = {
    'summary': {
        'total_xml_files': len(inventory),
        'total_elements': total_elements,
        'total_attributes': total_attributes
    },
    'files': {}
}

for file_name, data in inventory.items():
    output['files'][file_name] = {
        'element_count': data['element_count'],
        'total_attributes': data['total_attributes'],
        'elements': [{
            'name': e['name'],
            'attribute_count': e['attribute_count'],
            'attributes': e['attributes']
        } for e in data['elements']]
    }

with open('full-entity-inventory.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n\nFull inventory saved to full-entity-inventory.json")
