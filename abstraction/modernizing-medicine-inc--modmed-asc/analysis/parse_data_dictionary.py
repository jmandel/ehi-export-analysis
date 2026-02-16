#!/usr/bin/env python3
"""Parse gGastro EHI Patient Export Specifications PDF text into structured JSON.

Reads the pdftotext -layout output and extracts:
- All CSV entity/table definitions with their fields
- Field metadata: position, name, type, length, format/translation/comments
- Data schema (parent-child relationships)
- Translation tables
"""

import re
import json
import sys
from pathlib import Path

def parse_csv_dictionary(lines, start_line, end_line):
    """Parse the CSV Files Dictionary section into entities and fields."""
    entities = []
    current_entity = None
    current_fields = []
    
    # Pattern for entity header line (entity name alone on a line, no leading digits)
    # Entity names are PascalCase or camelCase words, alone on the line
    entity_pattern = re.compile(r'^([A-Z][A-Za-z0-9]+(?:[A-Z][A-Za-z0-9]*)*)\s*$')
    
    # Pattern for field definition: starts with column number, then field name
    # e.g., "0 - AppointmentHoldId                     GUID"
    field_pattern = re.compile(
        r'^\s*(\d+)\s+-\s+(\S+)\s+'  # col number and field name
        r'(Alphanumeric|Numeric|GUID|Boolean|Date & Time|Date|Time|Decimal|XML)'  # type
        r'(?:\s+(\d+))?\s*'  # optional length
        r'(.*?)$'  # rest is format/translation/comments
    )
    
    # Sometimes field lines wrap - continuation has format/translation info
    # Header line pattern
    header_pattern = re.compile(r'^Column Number - Name\s+Type\s+Length\s+Format')
    
    i = start_line
    while i < end_line:
        line = lines[i]
        stripped = line.strip()
        
        # Skip blank lines and header lines
        if not stripped or header_pattern.match(stripped):
            i += 1
            continue
        
        # Check for entity name
        entity_match = entity_pattern.match(stripped)
        if entity_match and not field_pattern.match(line):
            # Save previous entity
            if current_entity:
                entities.append({
                    'name': current_entity,
                    'fields': current_fields
                })
            current_entity = entity_match.group(1)
            current_fields = []
            i += 1
            continue
        
        # Check for field definition
        field_match = field_pattern.match(line)
        if field_match:
            col_num = int(field_match.group(1))
            field_name = field_match.group(2)
            field_type = field_match.group(3)
            field_length = int(field_match.group(4)) if field_match.group(4) else None
            comment = field_match.group(5).strip()
            
            field = {
                'position': col_num,
                'name': field_name,
                'type': field_type,
                'description': comment if comment else None
            }
            if field_length is not None:
                field['max_length'] = field_length
            
            current_fields.append(field)
            i += 1
            
            # Check for continuation lines (indented, no field number prefix)
            while i < end_line:
                next_line = lines[i]
                next_stripped = next_line.strip()
                if not next_stripped:
                    i += 1
                    break
                # Is it a new field, entity, or header?
                if field_pattern.match(next_line) or entity_pattern.match(next_stripped) or header_pattern.match(next_stripped):
                    break
                # Continuation of comment/format
                if comment:
                    field['description'] = field['description'] + ' ' + next_stripped if field['description'] else next_stripped
                else:
                    field['description'] = next_stripped
                i += 1
            continue
        
        i += 1
    
    # Save last entity
    if current_entity:
        entities.append({
            'name': current_entity,
            'fields': current_fields
        })
    
    return entities


def parse_translations(lines, start_line, end_line):
    """Parse the Translations section into translation tables."""
    translations = {}
    current_category = None
    current_table = None
    
    # Translation table headers look like: "Category TableName"
    # Values look like: "code = value"
    
    i = start_line
    while i < end_line:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Look for category/table patterns
        # These are typically multi-word names followed by value mappings
        # e.g., "Billing Claim Status" then "0 = Open", "1 = Closed"
        
        i += 1
    
    return translations


def parse_data_schema(lines, start_line, end_line):
    """Parse the Data Schema section to extract parent-child relationships."""
    relationships = []
    
    for i in range(start_line, end_line):
        line = lines[i]
        # Schema lines show indentation-based tree structure
        # with entity names and linking fields
        stripped = line.strip()
        if not stripped:
            continue
        
        # Look for patterns like "EntityName (FieldName)"
        match = re.match(r'^(\s*)(\w+)\s*(?:\((\w+)\))?\s*$', line.rstrip())
        if match:
            indent = len(match.group(1))
            entity = match.group(2)
            link_field = match.group(3)
            relationships.append({
                'entity': entity,
                'link_field': link_field,
                'indent_level': indent
            })
    
    return relationships


def main():
    base_dir = Path(__file__).parent
    text_file = base_dir / 'data-dictionary-text.txt'
    
    with open(text_file, 'r') as f:
        lines = f.readlines()
    
    # Find section boundaries
    csv_dict_start = None
    data_schema_start = None
    translations_start = None
    patient_docs_start = None
    glossary_start = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == 'CSV Files Dictionary' and i > 20:  # Skip TOC
            csv_dict_start = i + 1
        elif stripped == 'Data Schema' and csv_dict_start and not data_schema_start:
            data_schema_start = i + 1
        elif stripped == 'Translations' and data_schema_start:
            translations_start = i + 1
        elif stripped == 'Patient Documents' and translations_start and not patient_docs_start:
            patient_docs_start = i + 1
        elif stripped == 'Glossary' and patient_docs_start:
            glossary_start = i + 1
    
    print(f"Section boundaries:")
    print(f"  CSV Dict: line {csv_dict_start}")
    print(f"  Data Schema: line {data_schema_start}")
    print(f"  Translations: line {translations_start}")
    print(f"  Patient Documents: line {patient_docs_start}")
    print(f"  Glossary: line {glossary_start}")
    
    # Parse CSV Files Dictionary
    entities = parse_csv_dictionary(lines, csv_dict_start, data_schema_start - 1 if data_schema_start else len(lines))
    
    total_fields = sum(len(e['fields']) for e in entities)
    fields_with_desc = sum(1 for e in entities for f in e['fields'] if f.get('description'))
    
    print(f"\nCSV Files Dictionary:")
    print(f"  Total entities: {len(entities)}")
    print(f"  Total fields: {total_fields}")
    print(f"  Fields with descriptions/comments: {fields_with_desc}")
    print(f"  Fields without descriptions: {total_fields - fields_with_desc}")
    
    # Show entity sizes
    entity_sizes = [(e['name'], len(e['fields'])) for e in entities]
    entity_sizes.sort(key=lambda x: -x[1])
    
    print(f"\nTop 20 largest entities:")
    for name, count in entity_sizes[:20]:
        print(f"  {name}: {count} fields")
    
    print(f"\nSmallest entities (<=2 fields):")
    for name, count in entity_sizes:
        if count <= 2:
            print(f"  {name}: {count} fields")
    
    # Categorize entities by name patterns
    categories = {
        'Billing/Financial': [],
        'Clinical/Service': [],
        'Patient': [],
        'Scheduling': [],
        'Lab/Results': [],
        'Documents/Imaging': [],
        'GI-Specific': [],
        'Ophthalmology': [],
        'Cardiology': [],
        'Portal/Communication': [],
        'Administrative': [],
        'Other': []
    }
    
    for e in entities:
        name = e['name'].lower()
        if any(k in name for k in ['billing', 'claim', 'charge', 'payment', 'collection', 'insurance', 'fee', 'prepay', 'edi', 'adjustment', 'authorization', 'eligib']):
            categories['Billing/Financial'].append(e['name'])
        elif any(k in name for k in ['appointment', 'schedule', 'hold', 'wait', 'remind', 'kiosk']):
            categories['Scheduling'].append(e['name'])
        elif any(k in name for k in ['lab', 'specimen', 'result', 'interface']):
            categories['Lab/Results'].append(e['name'])
        elif any(k in name for k in ['document', 'image', 'imaging', 'letter', 'statement', 'fax']):
            categories['Documents/Imaging'].append(e['name'])
        elif any(k in name for k in ['aga', 'giquic', 'finding', 'impression', 'colonoscop', 'endoscop', 'polyp']):
            categories['GI-Specific'].append(e['name'])
        elif any(k in name for k in ['ophthalmolog', 'lens', 'cataract', 'eye']):
            categories['Ophthalmology'].append(e['name'])
        elif any(k in name for k in ['cardiol', 'carotid', 'echocardiog', 'nuclear', 'stress', 'heartcentrix']):
            categories['Cardiology'].append(e['name'])
        elif any(k in name for k in ['portal', 'message', 'telehealth']):
            categories['Portal/Communication'].append(e['name'])
        elif any(k in name for k in ['patient']) and not any(k in name for k in ['billing', 'claim']):
            categories['Patient'].append(e['name'])
        elif any(k in name for k in ['service', 'procedure', 'diagnos', 'allerg', 'medication', 'prescription', 'vital', 'problem', 'addend', 'anesthesia', 'aldrete', 'clinical', 'note', 'questionnaire', 'immuniz', 'vaccine', 'order']):
            categories['Clinical/Service'].append(e['name'])
        elif any(k in name for k in ['staff', 'user', 'location', 'task', 'audit', 'config', 'security']):
            categories['Administrative'].append(e['name'])
        else:
            categories['Other'].append(e['name'])
    
    print(f"\nEntities by category:")
    for cat, ents in categories.items():
        if ents:
            field_count = sum(len(e['fields']) for e in entities if e['name'] in ents)
            print(f"  {cat}: {len(ents)} entities, {field_count} fields")
            for ename in sorted(ents):
                eobj = next(e for e in entities if e['name'] == ename)
                print(f"    - {ename} ({len(eobj['fields'])} fields)")
    
    # Build full inventory
    inventory = {
        'version': '6.5.3.20251230',
        'source': 'gGastro-EHI-Patient-Export-Specifications-Dec2025.pdf',
        'total_entities': len(entities),
        'total_fields': total_fields,
        'fields_with_descriptions': fields_with_desc,
        'entities': entities
    }
    
    with open(base_dir / 'entity-inventory-full.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Build summary
    summary = {
        'version': '6.5.3.20251230',
        'source': 'gGastro-EHI-Patient-Export-Specifications-Dec2025.pdf',
        'total_entities': len(entities),
        'total_fields': total_fields,
        'fields_with_descriptions': fields_with_desc,
        'fields_without_descriptions': total_fields - fields_with_desc,
        'description_percentage': round(fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
        'categories': {},
        'top_20_entities': [{'name': n, 'field_count': c} for n, c in entity_sizes[:20]],
        'entity_field_distribution': {
            '1-5 fields': len([e for e in entities if len(e['fields']) <= 5]),
            '6-10 fields': len([e for e in entities if 6 <= len(e['fields']) <= 10]),
            '11-20 fields': len([e for e in entities if 11 <= len(e['fields']) <= 20]),
            '21-50 fields': len([e for e in entities if 21 <= len(e['fields']) <= 50]),
            '50+ fields': len([e for e in entities if len(e['fields']) > 50]),
        }
    }
    
    for cat, ents in categories.items():
        if ents:
            field_count = sum(len(e['fields']) for e in entities if e['name'] in ents)
            summary['categories'][cat] = {
                'entity_count': len(ents),
                'field_count': field_count,
                'entities': sorted(ents)
            }
    
    with open(base_dir / 'entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nField distribution:")
    for bucket, count in summary['entity_field_distribution'].items():
        print(f"  {bucket}: {count} entities")
    
    print(f"\nOutput files written:")
    print(f"  entity-inventory-full.json")
    print(f"  entity-inventory-summary.json")


if __name__ == '__main__':
    main()
