#!/usr/bin/env python3
"""
Parse PCE API Data Elements from PDF text.
Simple approach: read all lines, detect entity headers by matching known names,
parse field tables between headers.
"""

import json
import re

INPUT_FILE = '/tmp/pce-data-elements.txt'
OUTPUT_DIR = '/home/jmandel/hobby/ehi-export-analysis/abstraction/pce-systems--pce-care-management/analysis'

KNOWN_ENTITIES = [
    'Address', 'AllergyIntolerance', 'CarePlan', 'CareTeam', 'Claim',
    'Coded Element', 'Condition', 'Coverage', 'Device', 'Diagnostic Report',
    'Document Reference', 'Encounter', 'Goal', 'Healthcare Service',
    'Immunization', 'Location', 'Medication Request', 'Message',
    'Observation', 'Organization', 'Patient', 'Practitioner',
    'Practitioner Role', 'Procedure', 'Provenance', 'Failed Response Header'
]

def is_noise(line):
    s = line.strip()
    if not s:
        return False  # keep blanks for structure
    if 'PCE Care Management v9.4' in line and 'Web Service' in line:
        return True
    if s == 'PCE Systems':
        return True
    if re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d', s):
        return True
    if re.match(r'^Page \d+ of \d+$', s):
        return True
    if s.startswith('© 20'):
        return True
    if s == 'Data Elements':
        return True
    return False

def parse_field_line(line):
    """Try to parse a line as: field_name  type  description"""
    # Field lines have leading whitespace (6 spaces typically)
    if not re.match(r'^\s{4,}', line):
        return None
    stripped = line.strip()
    if not stripped or stripped.startswith('Attribute'):
        return None
    
    # Split by 2+ whitespace characters to find columns
    # But we need to be careful about multi-word types like "Contact Point", "Coded Element"
    parts = re.split(r'\s{2,}', stripped)
    if len(parts) >= 3:
        return {
            'name': parts[0],
            'type': parts[1],
            'description': ' '.join(parts[2:])
        }
    elif len(parts) == 2:
        # Could be field_name + type (description on next line)
        if re.match(r'^[a-z]', parts[0]) or ':' in parts[0]:
            return {
                'name': parts[0],
                'type': parts[1],
                'description': ''
            }
        return {'continuation': parts}
    return None

def main():
    with open(INPUT_FILE) as f:
        raw_lines = f.readlines()
    
    # Clean lines: remove noise but keep blanks
    lines = []
    for line in raw_lines:
        if is_noise(line):
            continue
        lines.append(line.rstrip())
    
    # Find entity boundaries
    entity_positions = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in KNOWN_ENTITIES:
            entity_positions.append((i, stripped))
    
    print(f"Found {len(entity_positions)} entity headers")
    
    entities = []
    for idx, (pos, name) in enumerate(entity_positions):
        if name == 'Failed Response Header':
            continue
        
        # End is start of next entity
        end_pos = entity_positions[idx + 1][0] if idx + 1 < len(entity_positions) else len(lines)
        block = lines[pos+1:end_pos]
        
        # Get description: lines between entity name and "Attribute" header row
        description_parts = []
        field_lines_start = 0
        found_attr_header = False
        
        for j, bline in enumerate(block):
            bstripped = bline.strip()
            if bstripped == '':
                continue
            if 'Attribute' in bstripped and 'Data Type' in bstripped:
                # Header may have "Description" on same line or next line
                field_lines_start = j + 1
                # Check if next non-empty line is just "Description" (continuation)
                if field_lines_start < len(block) and block[field_lines_start].strip() == 'Description':
                    field_lines_start += 1
                found_attr_header = True
                break
            # It's a description line (before the table)
            if not re.match(r'^\s{6,}', bline):
                description_parts.append(bstripped)
        
        description = ' '.join(description_parts)
        
        # Parse fields from the table
        fields = []
        if found_attr_header:
            j = field_lines_start
            while j < len(block):
                bline = block[j]
                bstripped = bline.strip()
                
                if bstripped == '':
                    j += 1
                    continue
                
                parsed = parse_field_line(bline)
                if parsed and 'name' in parsed:
                    # Check for continuation lines (multi-line type or description)
                    k = j + 1
                    while k < len(block):
                        next_line = block[k]
                        next_stripped = next_line.strip()
                        if next_stripped == '':
                            k += 1
                            continue
                        # Is it a continuation? (indented, no new field pattern)
                        if re.match(r'^\s{15,}', next_line) and not re.match(r'^\s{4,}[a-z]\S*\s{2,}', next_line):
                            # Check if it's just a type word like "Element" or "Element List"
                            next_parts = re.split(r'\s{2,}', next_stripped)
                            if len(next_parts) == 1 and next_stripped in ('Element', 'Element List', 'Point', 'binary', 'List'):
                                parsed['type'] += ' ' + next_stripped
                            elif len(next_parts) == 1:
                                parsed['description'] += ' ' + next_stripped
                            elif len(next_parts) >= 2:
                                # Could be "Element   Description continuation"
                                if next_parts[0] in ('Element', 'Element List', 'Point', 'List'):
                                    parsed['type'] += ' ' + next_parts[0]
                                    parsed['description'] += ' ' + ' '.join(next_parts[1:])
                                else:
                                    parsed['description'] += ' ' + next_stripped
                            k += 1
                        else:
                            break
                    
                    fields.append(parsed)
                    j = k
                    continue
                
                j += 1
        
        entities.append({
            'name': name,
            'description': description,
            'field_count': len(fields),
            'fields': fields
        })
    
    # Build inventory
    helper_types = {'Address', 'Coded Element', 'Message'}
    fhir_resources = [e for e in entities if e['name'] not in helper_types]
    helpers = [e for e in entities if e['name'] in helper_types]
    
    total_fields = sum(e['field_count'] for e in entities)
    fields_with_desc = sum(1 for e in entities for f in e['fields'] if f.get('description','').strip())
    fields_with_types = sum(1 for e in entities for f in e['fields'] if f.get('type','').strip())
    
    inventory = {
        'source': 'PIX_9_4_API_Documentation.pdf (pages 65-78, Data Elements section)',
        'source_type': 'FHIR R4 API Data Elements for (g)(10) certification',
        'note': 'The (b)(10) EHI export uses a native data model with documentation.json embedded in the export ZIP. This inventory represents the FHIR API data elements, which are a USCDI-conformant projection and likely a subset of the native export model.',
        'extraction_date': '2026-02-16',
        'summary': {
            'total_entities': len(entities),
            'fhir_resources': len(fhir_resources),
            'helper_types': len(helpers),
            'total_fields': total_fields,
            'resource_fields': sum(e['field_count'] for e in fhir_resources),
            'fields_with_descriptions': fields_with_desc,
            'fields_with_types': fields_with_types,
            'description_coverage_pct': round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        },
        'entities': entities
    }
    
    with open(f'{OUTPUT_DIR}/full-entity-inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    print(f"\n=== PCE API Data Elements ===")
    print(f"Total entities: {len(entities)}")
    print(f"  FHIR resources: {len(fhir_resources)}")
    print(f"  Helper types: {len(helpers)}")
    print(f"Total fields: {total_fields}")
    print(f"  With descriptions: {fields_with_desc} ({round(fields_with_desc/total_fields*100,1) if total_fields else 0}%)")
    print(f"  With types: {fields_with_types}")
    print()
    print(f"{'Entity':<25} {'Fields':>6}  Description")
    print("-" * 95)
    for e in entities:
        tag = ' [helper]' if e['name'] in helper_types else ''
        print(f"  {e['name']:<23} {e['field_count']:>4}   {e['description'][:55]}{tag}")

if __name__ == '__main__':
    main()
