#!/usr/bin/env python3
"""Parse the MDVita EHI Export Data Format PDF into structured JSON.

Reads pdftotext output and extracts all entity (data file) definitions
with their columns, types, descriptions, and coded values.
"""

import json
import re
import subprocess
import sys

PDF_PATH = "../downloads/MDVita_EHR_EHI_DataFormat.pdf"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def clean_lines(text):
    """Remove headers, footers, and page markers."""
    lines = text.split('\n')
    cleaned = []
    skip_patterns = [
        r'^\s*Health Care 2000, Inc\s*$',
        r'^\s*15715 S Dixie Hwy',
        r'^\s*Miami, FL',
        r'^\s*Tel\.',
        r'^\s*Email: support@',
        r'^\s*Page \d+ of \d+',
        r'^\s*Information provided in this document is property',
        r'^\s*the purpose of developing technology',
    ]
    for line in lines:
        if any(re.match(p, line) for p in skip_patterns):
            continue
        cleaned.append(line)
    return cleaned

def parse_entities(lines):
    """Parse entity sections from the cleaned text."""
    entities = []
    current_entity = None
    current_fields = []
    current_field = None
    in_table = False
    
    # Find section headers like "3. Data file. Patients"
    section_re = re.compile(r'^\s*(\d+)\.\s+Data file\.\s+(.+)')
    # Column header row
    col_header_re = re.compile(r'^\s*Column Name\s+Data\s+Description')
    # Type-only continuation line (just "Type" under "Data")
    type_header_re = re.compile(r'^\s+Type\s*$')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for new entity section
        m = section_re.match(line)
        if m:
            # Save previous entity
            if current_entity and current_field:
                current_fields.append(current_field)
                current_field = None
            if current_entity:
                current_entity['fields'] = current_fields
                entities.append(current_entity)
            
            current_entity = {
                'section_number': int(m.group(1)),
                'name': m.group(2).strip(),
                'fields': []
            }
            current_fields = []
            current_field = None
            in_table = False
            i += 1
            continue
        
        # Check for column header
        if col_header_re.match(line):
            in_table = True
            # Skip the "Type" continuation line
            if i + 1 < len(lines) and type_header_re.match(lines[i+1]):
                i += 2
            else:
                i += 1
            continue
        
        if not in_table or not current_entity:
            i += 1
            continue
        
        # Skip blank lines
        if not line.strip():
            i += 1
            continue
        
        # Try to parse a field line: starts with column name in first ~35 chars
        # Format: " ColumnName              DataType      Description text"
        # Also handle edge case where name and type have only 1 space
        field_re = re.compile(r'^\s{1,2}(\S+)\s{2,}(\S+)\s{2,}(.+)')
        fm = field_re.match(line)
        if not fm:
            # Try alternate pattern: "Name Type    Description" with single space between name and type
            field_re2 = re.compile(r'^\s{1,2}(\S+)\s+(Numeric|String|Boolean|DateTime|Date|string)\s{2,}(.+)')
            fm = field_re2.match(line)
        
        if fm:
            # Save previous field
            if current_field:
                current_fields.append(current_field)
            
            col_name = fm.group(1).strip()
            data_type = fm.group(2).strip()
            desc = fm.group(3).strip()
            
            current_field = {
                'name': col_name,
                'type': data_type,
                'description': desc,
                'coded_values': {}
            }
            i += 1
            continue
        
        # Continuation line (indented description or coded values)
        if current_field:
            stripped = line.strip()
            if not stripped:
                i += 1
                continue
            
            # Check for coded value pattern like "F=Female" or "1 = Encounter"
            cv_match = re.match(r'^([A-Za-z0-9_]+)\s*=\s*(.+)', stripped)
            if cv_match:
                code = cv_match.group(1).strip()
                value = cv_match.group(2).strip()
                current_field['coded_values'][code] = value
            elif stripped.startswith('[') and '=' in stripped:
                # [empty] = No value pattern
                cv_match2 = re.match(r'\[(\w+)\]\s*=\s*(.+)', stripped)
                if cv_match2:
                    current_field['coded_values'][f'[{cv_match2.group(1)}]'] = cv_match2.group(2).strip()
                else:
                    current_field['description'] += ' ' + stripped
            else:
                # Check if it's a continuation of description
                current_field['description'] += ' ' + stripped
        
        i += 1
    
    # Save last entity
    if current_entity and current_field:
        current_fields.append(current_field)
    if current_entity:
        current_entity['fields'] = current_fields
        entities.append(current_entity)
    
    return entities

def assign_categories(entities):
    """Assign domain categories to entities."""
    category_map = {
        'Patients': 'Demographics',
        'ProviderNetwork': 'Providers',
        'ProviderPCPs': 'Providers',
        'Locations': 'Facility',
        'PatientPlans': 'Insurance / Coverage',
        'Appointments': 'Scheduling / Encounters',
        'SOAPNotesIndex': 'Clinical Notes',
        'Orders': 'Orders',
        'ProblemList': 'Clinical - Problems',
        'Allergies': 'Clinical - Allergies',
        'MedicationList': 'Clinical - Medications',
        'ProcedureList': 'Clinical - Procedures',
        'DocumentsIndex': 'Documents',
        'LabResults': 'Clinical - Labs',
        'Claims': 'Billing / Claims',
        'Referrals': 'Orders / Referrals',
        'Emails': 'Communications',
        'Immunizations': 'Clinical - Immunizations',
        'Vitals': 'Clinical - Vitals',
        'DocumentSignatures': 'Documents',
        'ClaimsInsurancePayments': 'Billing / Payments',
        'MemberCharges': 'Billing / Charges',
        'MemberPayments': 'Billing / Payments',
        'DocumentAnnotations': 'Documents',
    }
    for entity in entities:
        entity['category'] = category_map.get(entity['name'], 'Other')
    return entities

def generate_summary(entities):
    """Generate summary statistics."""
    total_fields = sum(len(e['fields']) for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e['fields'] 
        if f['description'] and f['description'].strip()
    )
    fields_with_types = sum(
        1 for e in entities for f in e['fields']
        if f['type'] and f['type'].strip()
    )
    fields_with_coded_values = sum(
        1 for e in entities for f in e['fields']
        if f.get('coded_values')
    )
    
    # Category breakdown
    categories = {}
    for e in entities:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'field_count': 0, 'entities': []}
        categories[cat]['entity_count'] += 1
        categories[cat]['field_count'] += len(e['fields'])
        categories[cat]['entities'].append(e['name'])
    
    return {
        'total_entities': len(entities),
        'total_fields': total_fields,
        'fields_with_descriptions': fields_with_desc,
        'fields_with_types': fields_with_types,
        'fields_with_coded_values': fields_with_coded_values,
        'description_coverage_pct': round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        'type_coverage_pct': round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
        'category_breakdown': categories,
        'entities_overview': [
            {
                'name': e['name'],
                'category': e['category'],
                'field_count': len(e['fields']),
                'fields_with_descriptions': sum(1 for f in e['fields'] if f['description']),
                'fields_with_coded_values': sum(1 for f in e['fields'] if f.get('coded_values')),
            }
            for e in entities
        ]
    }

def main():
    text = extract_text()
    lines = clean_lines(text)
    entities = parse_entities(lines)
    entities = assign_categories(entities)
    
    # Clean up coded_values: remove empty dicts
    for e in entities:
        for f in e['fields']:
            if not f['coded_values']:
                del f['coded_values']
    
    # Write full inventory
    with open('entity-inventory-full.json', 'w') as fp:
        json.dump(entities, fp, indent=2)
    
    # Write summary
    summary = generate_summary(entities)
    with open('entity-inventory-summary.json', 'w') as fp:
        json.dump(summary, fp, indent=2)
    
    # Print summary
    print(f"Entities parsed: {summary['total_entities']}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_coverage_pct']}%)")
    print(f"Fields with types: {summary['fields_with_types']} ({summary['type_coverage_pct']}%)")
    print(f"Fields with coded values: {summary['fields_with_coded_values']}")
    print()
    print("Category breakdown:")
    for cat, info in sorted(summary['category_breakdown'].items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print()
    print("Entity details:")
    for e in summary['entities_overview']:
        print(f"  {e['name']}: {e['field_count']} fields, {e['fields_with_descriptions']} described, {e['fields_with_coded_values']} with coded values")

if __name__ == '__main__':
    main()
