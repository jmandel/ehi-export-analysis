#!/usr/bin/env python3
"""Parse Crystal PM PDF data dictionary (extracted text) into structured JSON."""

import re
import json
import sys

def parse_text(text):
    lines = text.split('\n')
    
    # Find all CSV Export sections
    tables = []
    xml_sections = []
    
    # First pass: identify section boundaries
    csv_export_pattern = re.compile(r'^(.+?)\s*-\s*"(\w+)"\s+CSV Export\s*$')
    xml_extraction_pattern = re.compile(r'^(\w+)\s+table\s*-\s*(\w+)\s+column\s+Custom XML Extraction')
    # Also detect "User Defined Fields - <table> table - <col> column"
    udf_pattern = re.compile(r'^User Defined Fields\s*-\s*(\w+)\s+table\s*-\s*(\w+)\s+column')
    
    sections = []
    for i, line in enumerate(lines):
        m = csv_export_pattern.match(line.strip())
        if m:
            sections.append({
                'type': 'csv_export',
                'label': m.group(1).strip(),
                'table_name': m.group(2).strip(),
                'line': i
            })
        m = xml_extraction_pattern.match(line.strip())
        if m:
            sections.append({
                'type': 'xml_extraction',
                'table_name': m.group(1).strip(),
                'column_name': m.group(2).strip(),
                'line': i
            })
        m = udf_pattern.match(line.strip())
        if m:
            sections.append({
                'type': 'udf_extraction',
                'table_name': m.group(1).strip(),
                'column_name': m.group(2).strip(),
                'line': i
            })
    
    # Sort by line number
    sections.sort(key=lambda s: s['line'])
    
    # For each section, extract content until next section
    for idx, sec in enumerate(sections):
        start = sec['line'] + 1
        end = sections[idx + 1]['line'] if idx + 1 < len(sections) else len(lines)
        sec['content_lines'] = lines[start:end]
    
    # Parse CSV Export sections
    all_entities = []
    
    for sec in sections:
        if sec['type'] == 'csv_export':
            entity = parse_csv_export_section(sec)
            all_entities.append(entity)
        elif sec['type'] in ('xml_extraction', 'udf_extraction'):
            xml_fields = parse_xml_section(sec)
            # Attach to the most recent entity with matching table name
            for ent in reversed(all_entities):
                if ent['table_name'] == sec['table_name']:
                    if 'xml_fields' not in ent:
                        ent['xml_fields'] = []
                    ent['xml_fields'].append({
                        'column': sec.get('column_name', 'xml'),
                        'type': sec['type'],
                        'fields': xml_fields
                    })
                    break
    
    return all_entities


def parse_csv_export_section(sec):
    """Parse a CSV Export section to extract table description and columns."""
    content = sec['content_lines']
    
    # Find the description (text before the column header row)
    # Column header pattern: "Column Name" ... "Data" ... "Description" ... "Extraction"
    header_line_idx = None
    for i, line in enumerate(content):
        # Header may be "Column Name  Data Type  Description  Extraction Method"
        # or split: "Column  Data  Description  Extraction" + "Name  Type  Method"
        stripped = line.strip()
        if 'Description' in stripped and ('Column Name' in stripped or 
            (stripped.startswith('Column') and 'Extraction' in stripped)):
            header_line_idx = i
            break
    
    description = ''
    if header_line_idx is not None:
        desc_lines = [l.strip() for l in content[:header_line_idx] if l.strip() and 'Type' not in l[:20]]
        description = ' '.join(desc_lines)
    
    # Parse columns after header
    columns = []
    if header_line_idx is not None:
        # Skip header and "Type" / "Method" continuation lines
        col_lines = content[header_line_idx + 1:]
        columns = parse_column_table(col_lines)
    
    return {
        'label': sec['label'],
        'table_name': sec['table_name'],
        'description': description.strip(),
        'fields': columns,
        'field_count': len(columns)
    }


def parse_column_table(lines):
    """Parse the tabular column definitions from extracted PDF text.
    
    The layout is roughly:
    column_name    data_type    description_text    extraction_method
    
    But descriptions can span multiple lines due to wrapping.
    """
    columns = []
    current = None
    
    # Pattern for a new column entry: starts with a word that looks like a column name
    # followed by a data type keyword
    col_start_pattern = re.compile(
        r'^(\w[\w.]*)\s+'
        r'(int|varchar|char|date|datetime|bigint|longblob|tinyint|text|time|mediumblob|blob|smallint|float|double|decimal|enum|bit|longtext|mediumtext)\b'
    )
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Skip header continuation line
        if re.match(r'^Name\s+Type\s', stripped):
            continue
        
        # Stop if we hit a serialized type documentation section
        if re.match(r'^\w+\s+Type$', stripped) or 'Member Name' in stripped:
            break
        
        # Check if this is a new column definition
        m = col_start_pattern.match(stripped)
        if m:
            col_name = m.group(1)
            # Reject false matches: real column names use snake_case or camelCase,
            # not common English words that happen to precede a type keyword
            common_words = {'a', 'an', 'the', 'and', 'or', 'of', 'in', 'to', 'for',
                           'is', 'it', 'on', 'at', 'by', 'as', 'be', 'this', 'that',
                           'with', 'from', 'are', 'was', 'were', 'been', 'has', 'had',
                           'have', 'do', 'does', 'did', 'will', 'would', 'could',
                           'should', 'may', 'might', 'can', 'shall', 'not', 'no',
                           'but', 'if', 'so', 'than', 'then', 'also', 'just',
                           'more', 'most', 'such', 'only', 'other', 'new', 'old',
                           'each', 'every', 'any', 'all', 'both', 'few', 'many',
                           'much', 'some', 'same', 'different', 'various', 'specific',
                           'estimated', 'approximate', 'exact', 'calculated'}
            if col_name.lower() in common_words or col_name == 'default':
                if current:
                    current['description_parts'].append(stripped)
                continue
        if m:
            if current:
                columns.append(finalize_column(current))
            
            col_name = m.group(1)
            data_type = m.group(2)
            rest = stripped[m.end():].strip()
            
            # Strip NOT NULL, default values from the beginning of rest (they're part of data type)
            rest = re.sub(r'^(NOT\s+NULL\s*)?(\s*default\s+\S+\s*)*', '', rest).strip()
            
            # Extract extraction method from end
            extraction = ''
            for method in ['CSV + Binary Deserialization', 'CSV + XML Deserialization', 
                          'CSV + Binary', 'CSV + XML', 'CSV']:
                if rest.endswith(method):
                    extraction = method
                    rest = rest[:-len(method)].strip()
                    break
            
            # Check for "Deserialization" on same line
            if not extraction and 'Deserialization' in rest:
                if 'Binary' in rest or 'XML' in rest:
                    # Try to extract it
                    dm = re.search(r'(CSV\s*\+\s*(Binary|XML)\s*Deserialization)', rest)
                    if dm:
                        extraction = dm.group(1).strip()
                        rest = rest[:dm.start()].strip() + ' ' + rest[dm.end():].strip()
                        rest = rest.strip()
            
            if not extraction:
                # Check if CSV is at end
                if rest.endswith('CSV'):
                    extraction = 'CSV'
                    rest = rest[:-3].strip()
            
            current = {
                'name': col_name,
                'data_type': data_type,
                'description_parts': [rest] if rest else [],
                'extraction_method': extraction
            }
        else:
            # Continuation line
            if current:
                # Check for extraction method markers
                for method in ['CSV + Binary Deserialization', 'CSV + XML Deserialization',
                              'CSV + Binary', 'CSV + XML', 'CSV']:
                    if stripped.endswith(method):
                        current['extraction_method'] = method
                        rest = stripped[:-len(method)].strip()
                        if rest:
                            current['description_parts'].append(rest)
                        stripped = ''
                        break
                
                if stripped == 'Deserialization' and current['extraction_method']:
                    # continuation of extraction method
                    pass
                elif stripped and stripped not in ('Method', 'Type'):
                    # Clean out data type continuations like "default", "NULL", dates
                    clean = re.sub(r"^(default\s*)?'?\d{4}-\d{2}-\d{2}.*$", '', stripped)
                    clean = re.sub(r'^default$', '', clean.strip())
                    clean = re.sub(r'^NULL$', '', clean.strip())
                    if clean.strip():
                        current['description_parts'].append(clean.strip())
    
    if current:
        columns.append(finalize_column(current))
    
    return columns


def finalize_column(col):
    desc = ' '.join(col['description_parts']).strip()
    # Clean up description
    desc = re.sub(r'\s+', ' ', desc)
    return {
        'name': col['name'],
        'data_type': col['data_type'],
        'description': desc,
        'extraction_method': col.get('extraction_method', '')
    }


def parse_xml_section(sec):
    """Parse XML extraction or UDF section."""
    content = sec['content_lines']
    fields = []
    current = None
    
    # Header line: "Name   Description   Field   Data   Serialization   Serialized"
    # or similar
    header_idx = None
    for i, line in enumerate(content):
        if 'Name' in line and 'Description' in line:
            header_idx = i
            break
    
    if header_idx is None:
        return fields
    
    # Parse entries after header
    data_lines = content[header_idx + 1:]
    
    # XML field pattern: starts with a PascalCase or camelCase name
    field_pattern = re.compile(r'^(\w+)\s+(.+)$')
    
    for line in data_lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check if this looks like a new field (starts with a word, has description after)
        m = field_pattern.match(stripped)
        if m:
            name = m.group(1)
            # Heuristic: if it starts with uppercase or is a known field-like name
            if name[0].isupper() or name in ('acctid', 'type', 'status'):
                if current:
                    fields.append(finalize_xml_field(current))
                current = {
                    'name': name,
                    'description_parts': [m.group(2)],
                }
            elif current:
                current['description_parts'].append(stripped)
        elif current:
            current['description_parts'].append(stripped)
    
    if current:
        fields.append(finalize_xml_field(current))
    
    return fields


def finalize_xml_field(field):
    desc = ' '.join(field['description_parts']).strip()
    desc = re.sub(r'\s+', ' ', desc)
    
    # Try to extract data type from description
    data_type = ''
    for t in ['String', 'Integer 32-Bit', 'Integer 64-Bit', 'Bool', 'DateTime',
              'Decimal', 'Double', 'Byte', 'Guid', 'TimeSpan']:
        if t in desc:
            data_type = t
            break
    
    return {
        'name': field['name'],
        'description': desc,
        'data_type': data_type,
        'source': 'xml_field'
    }


def main():
    with open('raw-text.txt', 'r') as f:
        text = f.read()
    
    entities = parse_text(text)
    
    # Build full inventory
    full_inventory = []
    for ent in entities:
        entry = {
            'label': ent['label'],
            'table_name': ent['table_name'],
            'description': ent['description'],
            'field_count': len(ent['fields']),
            'fields': ent['fields']
        }
        
        # Add XML sub-fields if present
        if 'xml_fields' in ent:
            xml_total = 0
            xml_sections = []
            for xs in ent['xml_fields']:
                xml_total += len(xs['fields'])
                xml_sections.append({
                    'column': xs['column'],
                    'type': xs['type'],
                    'field_count': len(xs['fields']),
                    'fields': xs['fields']
                })
            entry['xml_sections'] = xml_sections
            entry['xml_field_count'] = xml_total
        
        full_inventory.append(entry)
    
    # Save full inventory
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(full_inventory, f, indent=2)
    
    # Build summary
    total_fields = sum(e['field_count'] for e in full_inventory)
    total_xml_fields = sum(e.get('xml_field_count', 0) for e in full_inventory)
    fields_with_desc = sum(
        1 for e in full_inventory 
        for field in e['fields'] 
        if field['description'].strip()
    )
    xml_fields_with_desc = sum(
        1 for e in full_inventory
        for xs in e.get('xml_sections', [])
        for f in xs['fields']
        if f['description'].strip()
    )
    
    # Categorize entities
    categories = categorize_entities(full_inventory)
    
    summary = {
        'total_entities': len(full_inventory),
        'unique_table_names': len(set(e['table_name'] for e in full_inventory)),
        'total_csv_fields': total_fields,
        'total_xml_fields': total_xml_fields,
        'total_all_fields': total_fields + total_xml_fields,
        'csv_fields_with_descriptions': fields_with_desc,
        'xml_fields_with_descriptions': xml_fields_with_desc,
        'description_coverage_csv': f"{fields_with_desc}/{total_fields} ({100*fields_with_desc//total_fields}%)" if total_fields > 0 else "N/A",
        'categories': categories,
        'entities': [
            {
                'label': e['label'],
                'table_name': e['table_name'],
                'csv_fields': e['field_count'],
                'xml_fields': e.get('xml_field_count', 0),
                'total_fields': e['field_count'] + e.get('xml_field_count', 0),
                'category': get_category(e)
            }
            for e in full_inventory
        ]
    }
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary to stdout
    print(f"Total entities (CSV Export sections): {len(full_inventory)}")
    print(f"Unique table names: {summary['unique_table_names']}")
    print(f"Total CSV fields: {total_fields}")
    print(f"Total XML sub-fields: {total_xml_fields}")
    print(f"Total all fields: {total_fields + total_xml_fields}")
    print(f"CSV fields with descriptions: {fields_with_desc}/{total_fields}")
    print(f"XML fields with descriptions: {xml_fields_with_desc}/{total_xml_fields}")
    print()
    print("Entities by category:")
    for cat, items in categories.items():
        cat_csv = sum(i['csv_fields'] for i in items)
        cat_xml = sum(i['xml_fields'] for i in items)
        print(f"  {cat}: {len(items)} entities, {cat_csv} CSV fields, {cat_xml} XML fields")
    print()
    print("All entities:")
    for e in summary['entities']:
        print(f"  {e['label']:45s} ({e['table_name']:25s}) - {e['csv_fields']:3d} CSV + {e['xml_fields']:3d} XML = {e['total_fields']:4d} fields [{e['category']}]")


def get_category(entity):
    label = entity['label'].lower()
    table = entity['table_name'].lower()
    
    if table == 'patients':
        return 'Patient Demographics'
    elif table in ('ehr_file', 'clinical_note'):
        if any(kw in label.lower() for kw in ['lab order', 'lab result']):
            return 'Clinical - Lab'
        elif any(kw in label.lower() for kw in ['medication', 'drug', 'formulary']):
            return 'Clinical - Medications'
        elif 'immunization' in label.lower():
            return 'Clinical - Immunizations'
        elif 'problem' in label.lower():
            return 'Clinical - Problems'
        elif 'observation' in label.lower():
            return 'Clinical - Observations'
        elif 'procedure' in label.lower():
            return 'Clinical - Procedures'
        elif 'smoking' in label.lower():
            return 'Clinical - Social History'
        elif 'implantable' in label.lower() or 'device' in label.lower():
            return 'Clinical - Devices'
        elif 'intervention' in label.lower():
            return 'Clinical - Interventions'
        elif 'diagnostic' in label.lower():
            return 'Clinical - Diagnostic Studies'
        elif 'eye care' in label.lower():
            return 'Clinical - Eye Care Specialty'
        elif 'clinical note' in label.lower():
            return 'Clinical - Notes'
        else:
            return 'Clinical - Other'
    elif table in ('mcrx', 'mcs', 'mcs_log'):
        return 'Prescriptions/Medications'
    elif table in ('invoice', 'inv_trans_items', 'trans_pay', 'trans_data', 'hcfa_print', 'hcfa_data', 'rslip'):
        return 'Billing & Financial'
    elif table.startswith('vsp_') or table == 'frame_for_vsp':
        return 'Vision Insurance (VSP)'
    elif table in ('framepage', 'fp_log', 'cl_log', 'contorders', 'inv_log', 'clrx_notes', 'sprx_notes'):
        return 'Optical & Inventory'
    elif table in ('appts', 'appt_waitlist', 'appt_log'):
        return 'Scheduling'
    elif table in ('recall', 'reminders', 'rem_log', 'directmail_message', 'pat_markets', 'comments', 'kno2_message'):
        return 'Patient Engagement & Communication'
    elif table in ('med_image_info', 'med_image_data', 'pat_file', 'pat_file_data', 
                   'pat_photo_info', 'pat_photo_data', 'pat_photos', 'pat_ins_card', 
                   'ins_card_info', 'ins_card_data'):
        return 'Documents & Images'
    elif table in ('alerts', 'hippadisc', 'authlogs', 'mu_measures', 'order_groups', 
                   'result_groups', 'pro_refrl', 'hl7_record'):
        return 'Administrative & Compliance'
    else:
        return 'Other'


def categorize_entities(inventory):
    categories = {}
    for e in inventory:
        cat = get_category(e)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            'label': e['label'],
            'table_name': e['table_name'],
            'csv_fields': e['field_count'],
            'xml_fields': e.get('xml_field_count', 0)
        })
    return categories


if __name__ == '__main__':
    main()
