#!/usr/bin/env python3
"""Parse gGastro EHI Patient Export Specifications PDF text into structured JSON.

Improved parser that handles multi-line field descriptions properly.
Reads from pdftotext -layout output.
"""

import re
import json
from pathlib import Path
from collections import Counter

def parse_csv_dictionary(lines, start_line, end_line):
    """Parse the CSV Files Dictionary section into entities and fields."""
    entities = []
    current_entity = None
    current_fields = []
    
    # Known type keywords that can appear at start of continuation lines
    continuation_words = {
        'Score', 'Type', 'Status', 'Time', 'Selection', 'Document', 'Condition',
        'DATETIME2', 'Source', 'Code', 'Day', 'Side', 'Email', 'Interval',
        'Occupation', 'Dysplastic', 'Priority', 'Supplemental', 'Person',
        'DirectMailbox', 'Guarantor', 'Vendor', 'Relative',
    }
    
    # Field definition pattern - matches "N - FieldName   Type   ..."
    field_pattern = re.compile(
        r'^\s*(\d+)\s+-\s+(\S+)\s+'
        r'(Alphanumeric|Numeric|GUID|Boolean|Date & Time|Date|Time|Decimal|XML|Small Date &)'
        r'(?:\s+(\d+))?\s*'
        r'(.*?)$'
    )
    
    # Header line pattern
    header_pattern = re.compile(r'Column Number - Name\s+Type\s+Length\s+Format')
    
    # Entity name pattern - PascalCase, starts with uppercase, alone on line
    # Must NOT be a continuation of a previous field's description
    entity_name_pattern = re.compile(r'^([A-Z][A-Za-z0-9]+(?:[A-Z][A-Za-z0-9]*)*)\s*$')
    
    i = start_line
    while i < end_line:
        line = lines[i]
        stripped = line.strip()
        
        # Skip blank lines, header lines, page numbers
        if not stripped or header_pattern.match(stripped):
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
            
            # Check for continuation lines
            while i < end_line:
                next_line = lines[i]
                next_stripped = next_line.strip()
                if not next_stripped:
                    i += 1
                    break
                # Is it a new field?
                if field_pattern.match(next_line):
                    break
                # Is it a header line?
                if header_pattern.match(next_stripped):
                    break
                # Is it a real entity name (not a continuation)?
                entity_match = entity_name_pattern.match(next_stripped)
                if entity_match:
                    # Check if this looks like a continuation of the description
                    # Continuations are typically indented far right (comment area)
                    # or are known continuation words
                    leading_spaces = len(next_line) - len(next_line.lstrip())
                    if leading_spaces > 30:
                        # Indented continuation of description
                        if field.get('description'):
                            field['description'] = field['description'] + ' ' + next_stripped
                        else:
                            field['description'] = next_stripped
                        # Also fix type if it was "Small Date &" + "Time"
                        if field['type'] == 'Small Date &' and next_stripped == 'Time':
                            field['type'] = 'Small Date & Time'
                            field['description'] = None
                        i += 1
                        continue
                    else:
                        # Likely a real entity name
                        break
                else:
                    # Non-entity continuation line
                    leading_spaces = len(next_line) - len(next_line.lstrip())
                    if leading_spaces > 30:
                        if field.get('description'):
                            field['description'] = field['description'] + ' ' + next_stripped
                        else:
                            field['description'] = next_stripped
                    i += 1
                    continue
            continue
        
        # Check for entity name (only if at start of line with minimal indent)
        entity_match = entity_name_pattern.match(stripped)
        leading_spaces = len(line) - len(line.lstrip()) if stripped else 0
        if entity_match and leading_spaces < 10:
            name = entity_match.group(1)
            # Save previous entity
            if current_entity:
                entities.append({
                    'name': current_entity,
                    'fields': current_fields
                })
            current_entity = name
            current_fields = []
            i += 1
            continue
        
        # Unrecognized line - could be continuation of something or noise
        i += 1
    
    # Save last entity
    if current_entity:
        entities.append({
            'name': current_entity,
            'fields': current_fields
        })
    
    return entities


def categorize_entity(name):
    """Categorize an entity by its name patterns."""
    lower = name.lower()
    
    if any(k in lower for k in ['billing', 'claim', 'charge', 'payment', 'collection', 'fee', 'prepay', 'edi', 'superbill', 'ledger', 'invoice', 'credit']):
        return 'Billing/Financial'
    if any(k in lower for k in ['insurance', 'eligib', 'authorization']):
        return 'Insurance/Coverage'
    if any(k in lower for k in ['appointment', 'schedule', 'hold', 'wait', 'remind', 'kiosk', 'recall', 'pendingcancel']):
        return 'Scheduling'
    if any(k in lower for k in ['interfacelab', 'interfacetest', 'interfaceresult', 'interfacespecimen', 'specimen', 'interfacerequisition']):
        return 'Lab/Results'
    if any(k in lower for k in ['interfaceoutbound']):
        return 'Lab/Results'
    if any(k in lower for k in ['document', 'letter', 'fax', 'ccda', 'ecr']):
        return 'Documents'
    if any(k in lower for k in ['imaging']):
        return 'Imaging'
    if any(k in lower for k in ['aga', 'giquic', 'finding', 'impression']):
        return 'GI-Specific'
    if any(k in lower for k in ['ophthalmolog', 'lens']):
        return 'Ophthalmology'
    if any(k in lower for k in ['cardiol', 'carotid', 'echocardiog', 'nuclear', 'stress', 'heartcentrix', 'tte']):
        return 'Cardiology'
    if any(k in lower for k in ['portal', 'telehealth']):
        return 'Portal/Telehealth'
    if any(k in lower for k in ['directm', 'message']):
        return 'Communications'
    if any(k in lower for k in ['medication', 'prescription', 'pharmacy', 'drug', 'ndcid', 'ldm', 'renewal', 'formulary']):
        return 'Medications/Prescriptions'
    if any(k in lower for k in ['allerg']):
        return 'Allergies'
    if any(k in lower for k in ['immuniz', 'vaccine', 'cvxcode', 'hl7set']):
        return 'Immunizations'
    if any(k in lower for k in ['vital', 'bloodpressure', 'oxygen', 'physicalmeasurement']):
        return 'Vital Signs'
    if any(k in lower for k in ['diagnosis', 'problem', 'condition', 'disease', 'illness']):
        return 'Diagnoses/Problems'
    if any(k in lower for k in ['order']):
        return 'Orders'
    if any(k in lower for k in ['procedure', 'intervention', 'anesthesia', 'aldrete', 'service', 'addendum']):
        return 'Procedures/Services'
    if any(k in lower for k in ['patient', 'person', 'demographic', 'emergencycontact', 'employment', 'guarantor', 'occupation', 'usaaddress', 'phone', 'email', 'supportperson', 'provider', 'referring']):
        return 'Patient Demographics/History'
    if any(k in lower for k in ['questionnaire', 'chart', 'note', 'ros', 'physicalexam', 'coding', 'mips', 'quality', 'asc']):
        return 'Clinical Documentation'
    if any(k in lower for k in ['task']):
        return 'Tasks/Workflow'
    if any(k in lower for k in ['infusion', 'iv', 'npo', 'instrument', 'preparation', 'nursing', 'pain', 'discharge', 'limitationcomplication', 'generalwellbeing', 'functionalcognitive']):
        return 'Nursing/ASC Operations'
    if any(k in lower for k in ['syndromic', 'surveillance', 'bulkaction', 'export']):
        return 'Reporting/Export'
    if any(k in lower for k in ['guideline', 'interval', 'priorit']):
        return 'Clinical Guidelines'
    return 'Other'


def main():
    base_dir = Path(__file__).parent
    text_file = base_dir / 'data-dictionary-text.txt'
    
    with open(text_file, 'r') as f:
        lines = f.readlines()
    
    # Find section boundaries
    csv_dict_start = None
    data_schema_start = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == 'CSV Files Dictionary' and i > 20:
            csv_dict_start = i + 1
        elif stripped == 'Data Schema' and csv_dict_start and not data_schema_start:
            data_schema_start = i
    
    print(f"CSV Dict section: lines {csv_dict_start} to {data_schema_start}")
    
    # Parse entities
    entities = parse_csv_dictionary(lines, csv_dict_start, data_schema_start)
    
    # Deduplicate entity names by checking for issues
    name_counts = Counter(e['name'] for e in entities)
    dupes = {n: c for n, c in name_counts.items() if c > 1}
    if dupes:
        print(f"\nWARNING: Duplicate entity names found: {dupes}")
        print("These may indicate parse errors (continuation lines misidentified as entities)")
    
    # Remove zero-field entities (parse artifacts)
    real_entities = [e for e in entities if len(e['fields']) > 0]
    removed = len(entities) - len(real_entities)
    if removed:
        print(f"Removed {removed} zero-field entities (parse artifacts)")
    entities = real_entities
    
    # Categorize
    for e in entities:
        e['category'] = categorize_entity(e['name'])
    
    # Stats
    total_fields = sum(len(e['fields']) for e in entities)
    fields_with_desc = sum(1 for e in entities for f in e['fields'] if f.get('description'))
    
    print(f"\nParsed Results:")
    print(f"  Total entities: {len(entities)}")
    print(f"  Total fields: {total_fields}")
    print(f"  Fields with descriptions/format info: {fields_with_desc}")
    print(f"  Fields without descriptions: {total_fields - fields_with_desc}")
    print(f"  Description %: {round(fields_with_desc / total_fields * 100, 1) if total_fields else 0}%")
    
    # Category breakdown
    cat_stats = {}
    for e in entities:
        cat = e['category']
        if cat not in cat_stats:
            cat_stats[cat] = {'count': 0, 'fields': 0, 'entities': []}
        cat_stats[cat]['count'] += 1
        cat_stats[cat]['fields'] += len(e['fields'])
        cat_stats[cat]['entities'].append(e['name'])
    
    print(f"\nCategory breakdown:")
    for cat in sorted(cat_stats.keys()):
        s = cat_stats[cat]
        print(f"  {cat}: {s['count']} entities, {s['fields']} fields")
    
    # Top 20 entities
    entity_sizes = sorted(entities, key=lambda e: -len(e['fields']))
    print(f"\nTop 20 largest entities:")
    for e in entity_sizes[:20]:
        print(f"  {e['name']}: {len(e['fields'])} fields [{e['category']}]")
    
    # Field type distribution
    type_counts = Counter(f['type'] for e in entities for f in e['fields'])
    print(f"\nField types:")
    for t, c in type_counts.most_common():
        print(f"  {t}: {c}")
    
    # Build inventory
    inventory = {
        'version': '6.5.3.20251230',
        'source': 'gGastro-EHI-Patient-Export-Specifications-Dec2025.pdf',
        'total_entities': len(entities),
        'total_fields': total_fields,
        'fields_with_descriptions': fields_with_desc,
        'fields_without_descriptions': total_fields - fields_with_desc,
        'description_percentage': round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
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
        'description_percentage': round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        'categories': {
            cat: {
                'entity_count': s['count'],
                'field_count': s['fields'],
                'entities': sorted(s['entities'])
            }
            for cat, s in sorted(cat_stats.items())
        },
        'top_20_entities': [
            {'name': e['name'], 'field_count': len(e['fields']), 'category': e['category']}
            for e in entity_sizes[:20]
        ],
        'entity_field_distribution': {
            '1-5 fields': len([e for e in entities if 1 <= len(e['fields']) <= 5]),
            '6-10 fields': len([e for e in entities if 6 <= len(e['fields']) <= 10]),
            '11-20 fields': len([e for e in entities if 11 <= len(e['fields']) <= 20]),
            '21-50 fields': len([e for e in entities if 21 <= len(e['fields']) <= 50]),
            '50+ fields': len([e for e in entities if len(e['fields']) > 50]),
        }
    }
    
    with open(base_dir / 'entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nOutput written to entity-inventory-full.json and entity-inventory-summary.json")


if __name__ == '__main__':
    main()
