#!/usr/bin/env python3
"""
Parse the detailed data dictionary from pdftohtml XML output.
Uses precise character positions from the XML to correctly assign columns.
"""
import xml.etree.ElementTree as ET
import json
import re

# Column boundaries from header positions (left values)
# IDX: ~37-65, Grouping: ~68-150, Table: ~154-265, Column: ~268-400
# Description: ~405-765, DataType: ~766-825, Nullable: ~825-890
# FieldLength: ~896-990, Values: ~996+
COL_BOUNDARIES = [
    ('idx_grouping', 30, 150),
    ('table', 150, 265),
    ('column', 265, 403),
    ('description', 403, 765),
    ('dataType', 765, 825),
    ('nullable', 825, 892),
    ('fieldLength', 892, 935),
    ('valuesCodingSchema', 935, 1300),
]

def classify_col(left):
    for name, lo, hi in COL_BOUNDARIES:
        if lo <= left < hi:
            return name
    return None

def get_text(el):
    """Get full text from element including bold children."""
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        if child.text:
            parts.append(child.text)
        if child.tail:
            parts.append(child.tail)
    return ''.join(parts).strip()

# Known groupings from the overview document
KNOWN_GROUPINGS = [
    'PM Financials', 'Ophth Pretesting', 'Document Management', 'Office Flow',
    'CC/HPI', 'Practice', 'Patient', 'Lookup', 'eLab', 'Pathology',
    'Prescription', 'Appointment', 'Visit', 'Exam', 'Diagnosis',
    'Procedure', 'Inventory', 'Document', 'MIPS'
]
# Sort by length descending to match longest first
KNOWN_GROUPINGS.sort(key=len, reverse=True)

def parse_idx_grouping(text):
    """Parse combined IDX+Grouping+possible table start text.
    e.g. '1579 Ophth Pretesting central_retinal_thickne' ->
    idx=1579, grouping='Ophth Pretesting', table_start='central_retinal_thickne'
    """
    m = re.match(r'^(\d+)\s*(.*)', text.strip())
    if not m:
        return None, None, None
    idx_val = int(m.group(1))
    rest = m.group(2).strip()
    
    # Try to match a known grouping
    for g in KNOWN_GROUPINGS:
        if rest.startswith(g):
            after = rest[len(g):].strip()
            return idx_val, g, after if after else None
    
    return idx_val, rest, None

def main():
    with open('downloads/detailed-dd-xml.xml') as f:
        content = f.read()
    # Skip error line before XML declaration
    idx = content.find('<?xml')
    content = content[idx:]
    
    root = ET.fromstring(content)
    pages = root.findall('.//page')
    
    # Collect all text elements across all pages
    all_elements = []
    for page in pages:
        for el in page.findall('text'):
            text = get_text(el)
            if not text:
                continue
            left = int(el.get('left', 0))
            top = int(el.get('top', 0))
            page_num = int(page.get('number', 0))
            all_elements.append({
                'left': left,
                'top': top,
                'page': page_num,
                'text': text
            })
    
    # Sort by page, then top position
    all_elements.sort(key=lambda e: (e['page'], e['top'], e['left']))
    
    # Identify header rows: every page has headers at top=83 and top=97 (continuation)
    # Collect all header tops by finding "IDX" text positions
    header_positions = set()  # (page, top) pairs to skip
    for el in all_elements:
        if el['text'].strip() == 'IDX' and el['left'] < 60:
            header_positions.add((el['page'], el['top']))
    # Also skip top=97 (header continuation "Length") and title lines
    for el in all_elements:
        if el['text'].strip() in ('Length',) and el['top'] < 110:
            header_positions.add((el['page'], el['top']))
    
    # Parse rows
    rows = []
    cur = None
    
    for el in all_elements:
        col = classify_col(el['left'])
        if not col:
            continue
        
        text = el['text']
        
        # Skip header rows and titles
        if (el['page'], el['top']) in header_positions:
            continue
        # Skip elements on header line (within 2px of a header position)
        skip = False
        for hp, ht in header_positions:
            if el['page'] == hp and abs(el['top'] - ht) <= 2:
                skip = True
                break
        if skip:
            continue
        if text.startswith('ModMed EMA:'):
            continue
        # Skip standalone page numbers (right side, small text)
        if el['left'] > 1100 and text.strip().isdigit():
            continue
        
        if col == 'idx_grouping':
            idx_val, grouping, table_start = parse_idx_grouping(text)
            if idx_val is not None:
                if cur:
                    rows.append(cur)
                cur = {
                    'idx': idx_val,
                    'grouping': grouping,
                    'table_parts': [table_start] if table_start else [],
                    'column_parts': [],
                    'description_parts': [],
                    'dataType_parts': [],
                    'nullable_parts': [],
                    'fieldLength_parts': [],
                    'values_parts': [],
                }
                continue
            # Continuation of grouping text
            if cur and not cur['grouping']:
                # Try to split grouping from table name
                for g in KNOWN_GROUPINGS:
                    if text.strip().startswith(g):
                        cur['grouping'] = g
                        after = text.strip()[len(g):].strip()
                        if after:
                            cur['table_parts'].insert(0, after)
                        break
                else:
                    cur['grouping'] = text.strip()
            continue
        
        if not cur:
            continue
        
        if col == 'table':
            cur['table_parts'].append(text)
        elif col == 'column':
            cur['column_parts'].append(text)
        elif col == 'description':
            cur['description_parts'].append(text)
        elif col == 'dataType':
            cur['dataType_parts'].append(text)
        elif col == 'nullable':
            cur['nullable_parts'].append(text)
        elif col == 'fieldLength':
            cur['fieldLength_parts'].append(text)
        elif col == 'valuesCodingSchema':
            cur['values_parts'].append(text)
    
    if cur:
        rows.append(cur)
    
    # Convert to final entries
    entries = []
    for row in rows:
        table = ''.join(row['table_parts']).strip()
        column = ''.join(row['column_parts']).strip()
        
        # Handle merged table+column: if column is empty and table contains a space,
        # the first word is the table name and the rest is the column name
        if not column and ' ' in table:
            parts = table.split(' ', 1)
            table = parts[0]
            column = parts[1]
        description = ' '.join(row['description_parts']).strip()
        description = re.sub(r'\s+', ' ', description)
        data_type = ' '.join(row['dataType_parts']).strip()
        nullable_str = ' '.join(row['nullable_parts']).strip().lower()
        field_length_str = ''.join(row['fieldLength_parts']).strip()
        values = ' '.join(row['values_parts']).strip()
        values = re.sub(r'\s+', ' ', values)
        
        nullable = None
        if nullable_str == 'true':
            nullable = True
        elif nullable_str == 'false':
            nullable = False
        
        field_length = None
        if field_length_str:
            try:
                field_length = int(field_length_str)
            except ValueError:
                field_length = field_length_str
        
        if not table and not column:
            continue
        
        entries.append({
            'idx': row['idx'],
            'grouping': row['grouping'],
            'table': table,
            'column': column,
            'description': description,
            'dataType': data_type,
            'nullable': nullable,
            'fieldLength': field_length,
            'valuesCodingSchema': values,
        })
    
    # Propagate grouping and table names
    last_grouping = ''
    last_table = ''
    for e in entries:
        if e['grouping']:
            last_grouping = e['grouping']
        else:
            e['grouping'] = last_grouping
        if e['table']:
            last_table = e['table']
        else:
            e['table'] = last_table
    
    # Build stats
    table_set = sorted(set(e['table'] for e in entries if e['table']))
    groupings = {}
    for e in entries:
        g = e['grouping'] or '(empty)'
        groupings[g] = groupings.get(g, 0) + 1
    
    table_field_counts = {}
    for e in entries:
        t = e['table']
        table_field_counts[t] = table_field_counts.get(t, 0) + 1
    
    has_desc = sum(1 for e in entries if e['description'])
    has_type = sum(1 for e in entries if e['dataType'])
    has_nullable = sum(1 for e in entries if e['nullable'] is not None)
    has_values = sum(1 for e in entries if e['valuesCodingSchema'])
    
    stats = {
        'totalFields': len(entries),
        'totalTables': len(table_set),
        'fieldsWithDescription': has_desc,
        'fieldsWithDataType': has_type,
        'fieldsWithNullable': has_nullable,
        'fieldsWithValues': has_values,
        'groupings': dict(sorted(groupings.items(), key=lambda x: -x[1])),
        'tableFieldCounts': dict(sorted(table_field_counts.items()))
    }
    
    output = {
        'source': 'ModMed-EMA-Detailed-Data-Dictionary.pdf',
        'extractedAt': '2026-02-16',
        'stats': stats,
        'tables': table_set,
        'fields': entries
    }
    
    with open('analysis/detailed-dd-parsed.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print(f"Total fields: {len(entries)}")
    print(f"Total tables: {len(table_set)}")
    print(f"Fields with description: {has_desc} ({100*has_desc/len(entries):.1f}%)")
    print(f"Fields with data type: {has_type} ({100*has_type/len(entries):.1f}%)")
    print(f"Fields with nullable: {has_nullable}")
    print(f"Fields with values/coding: {has_values}")
    print()
    print("Groupings:")
    for g, c in sorted(groupings.items(), key=lambda x: -x[1]):
        print(f"  {g}: {c}")
    print()
    # Check for bad table names
    bad = [t for t in table_set if ' ' in t or len(t) > 50]
    print(f"Tables with spaces or >50 chars: {len(bad)}")
    for t in bad[:10]:
        print(f"  {t}")
    print()
    print("Top 20 tables by field count:")
    for t, c in sorted(table_field_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {t}: {c}")


if __name__ == '__main__':
    main()
