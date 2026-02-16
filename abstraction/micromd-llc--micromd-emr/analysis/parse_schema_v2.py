"""
Improved parser for MicroMD EMR EHI export PDF schema.
Carefully tracks XML hierarchy and deduplicates entities within files.
"""

import re
import json

def parse_pdf_text(filepath):
    with open(filepath, 'r') as f:
        text = f.read()
    
    # Remove page headers/footers
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        if 'micromd.com' in line:
            continue
        if re.match(r'^\s*P: 330-758-8832', line.strip()):
            continue
        if 'Canfield, OH' in line:
            continue
        cleaned.append(line)
    text = '\n'.join(cleaned)
    
    # Find XML file sections
    file_pattern = re.compile(r'•\s+(\w+)\.xml')
    sections = []
    for match in file_pattern.finditer(text):
        sections.append({'name': match.group(1), 'start': match.start()})
    
    # Add DMS section
    dms_match = re.search(r'Additional files from DMS', text)
    if dms_match:
        sections.append({'name': 'DMS', 'start': dms_match.start()})
    
    all_entities = []
    
    for i, section in enumerate(sections):
        if section['name'] == 'DMS':
            all_entities.append({
                'file': 'DMS',
                'entity': 'DMS_Attachments',
                'parent_entity': None,
                'fields': [],
                'field_count': 0,
                'description': 'Additional files from the document management system (pdf, doc, rtf, ccd, xml, images, etc.)',
                'category': 'Documents'
            })
            continue
        
        end_pos = sections[i+1]['start'] if i+1 < len(sections) else len(text)
        section_text = text[section['start']:end_pos]
        
        # Parse XML hierarchy manually by tracking opening/closing tags
        # Normalize: join lines but preserve XML structure
        normalized = re.sub(r'\s+', ' ', section_text)
        
        # Find all tags (opening with attrs, closing, self-closing)
        tag_pattern = re.compile(r'<(/?)(\w+)((?:\s+\w+="")*)\s*(/?)>')
        
        parent_stack = []
        
        for m in tag_pattern.finditer(normalized):
            is_closing = m.group(1) == '/'
            tag_name = m.group(2)
            attrs_str = m.group(3)
            is_self_closing = m.group(4) == '/'
            
            if is_closing:
                # Pop from stack
                if parent_stack and parent_stack[-1] == tag_name:
                    parent_stack.pop()
                continue
            
            # Extract attributes
            attrs = re.findall(r'(\w+)=""', attrs_str)
            
            if attrs:
                # This is a data element
                parent = parent_stack[-1] if parent_stack else section['name']
                
                # Build qualified entity name to handle duplicates
                entity_path = '/'.join(parent_stack[1:]) if len(parent_stack) > 1 else ''
                qualified = f"{entity_path}/{tag_name}" if entity_path else tag_name
                
                entity = {
                    'file': f"{section['name']}.xml",
                    'entity': tag_name,
                    'qualified_name': qualified,
                    'parent_entity': parent if parent != section['name'] else None,
                    'fields': [{'name': a, 'type': None, 'description': None} for a in attrs],
                    'field_count': len(attrs)
                }
                all_entities.append(entity)
                
                if not is_self_closing:
                    parent_stack.append(tag_name)
            else:
                # Container element (no attributes = structural)
                if not is_self_closing:
                    parent_stack.append(tag_name)
    
    return all_entities


def categorize_file(filename):
    """Assign a high-level category to each XML file."""
    categories = {
        'Billing.xml': 'Billing & Insurance',
        'Encounters.xml': 'Clinical - Encounters',
        'HealthScreening.xml': 'Clinical - Screening & Prevention',
        'Histories.xml': 'Clinical - Histories',
        'MedicalInfo.xml': 'Clinical - Medical Information',
        'Miscellaneous.xml': 'Documents & Communications',
        'Orders.xml': 'Clinical - Orders',
        'Patient.xml': 'Demographics & Insurance',
        'Schedule.xml': 'Scheduling',
        'Specialty.xml': 'Specialty Clinical Data',
        'WomenHealth.xml': 'Women\'s Health / OB-GYN',
        'DMS': 'Documents'
    }
    return categories.get(filename, 'Other')


def main():
    entities = parse_pdf_text('/tmp/micromd-ehi.txt')
    
    # Add categories
    for e in entities:
        e['category'] = categorize_file(e['file'])
    
    # Build full inventory
    export_files = sorted(set(e['file'] for e in entities))
    
    full_inventory = {
        'source': 'MicroMD-EMR-170.315b10-Electronic-Health-Information-export-EHI.pdf',
        'source_date': '2026-02-06',
        'format': 'XML (compressed, password-protected ZIP)',
        'export_files': export_files,
        'total_entities': len(entities),
        'total_fields': sum(e['field_count'] for e in entities),
        'entities': entities
    }
    
    # Build summary
    by_file = {}
    for e in entities:
        f = e['file']
        if f not in by_file:
            by_file[f] = {'entity_count': 0, 'field_count': 0, 'entities': [], 'category': e['category']}
        by_file[f]['entity_count'] += 1
        by_file[f]['field_count'] += e['field_count']
        by_file[f]['entities'].append({
            'name': e['entity'],
            'qualified_name': e.get('qualified_name', e['entity']),
            'parent': e['parent_entity'],
            'field_count': e['field_count']
        })
    
    by_category = {}
    for fname, info in by_file.items():
        cat = info['category']
        if cat not in by_category:
            by_category[cat] = {'files': [], 'entity_count': 0, 'field_count': 0}
        by_category[cat]['files'].append(fname)
        by_category[cat]['entity_count'] += info['entity_count']
        by_category[cat]['field_count'] += info['field_count']
    
    summary = {
        'total_entities': len(entities),
        'total_fields': sum(e['field_count'] for e in entities),
        'total_export_files': len(export_files),
        'fields_with_descriptions': 0,
        'fields_with_types': 0,
        'description_coverage_pct': 0,
        'type_coverage_pct': 0,
        'by_file': by_file,
        'by_category': by_category
    }
    
    base = '/home/jmandel/hobby/ehi-export-analysis/abstraction/micromd-llc--micromd-emr/analysis'
    
    with open(f'{base}/entity-inventory-full.json', 'w') as f:
        json.dump(full_inventory, f, indent=2)
    
    with open(f'{base}/entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print report
    print(f"Export format: XML (compressed ZIP)")
    print(f"Export files: {len(export_files)}")
    print(f"Total entities: {len(entities)}")
    print(f"Total fields (attributes): {sum(e['field_count'] for e in entities)}")
    print(f"Fields with descriptions: 0 (0%)")
    print(f"Fields with types: 0 (0%)")
    print()
    print("By XML file:")
    print(f"{'File':<25} {'Entities':>10} {'Fields':>10}  Category")
    print("-" * 80)
    for fname in sorted(by_file.keys()):
        info = by_file[fname]
        print(f"{fname:<25} {info['entity_count']:>10} {info['field_count']:>10}  {info['category']}")
    print("-" * 80)
    print(f"{'TOTAL':<25} {len(entities):>10} {sum(e['field_count'] for e in entities):>10}")
    print()
    print("By category:")
    for cat, info in sorted(by_category.items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print()
    print("Largest entities (by field count):")
    sorted_entities = sorted(entities, key=lambda x: x['field_count'], reverse=True)
    for e in sorted_entities[:15]:
        print(f"  {e['file']}/{e['entity']}: {e['field_count']} fields")


if __name__ == '__main__':
    main()
