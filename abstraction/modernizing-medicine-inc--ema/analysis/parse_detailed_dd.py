#!/usr/bin/env python3
"""
Parse the detailed data dictionary PDF text (extracted via pdftotext -layout)
into structured JSON. The PDF is a spreadsheet-style layout with columns:
IDX, Grouping, Table, Column, Description, Data Type, Nullable, Field Length, Values/Coding Schema
"""
import re
import json
import sys

def parse_detailed_dd(text_file):
    with open(text_file, 'r') as f:
        lines = f.readlines()
    
    fields = []
    current = None
    header_pattern = re.compile(r'^\s*IDX\s+Grouping\s+Table\s+Column')
    # Match lines starting with an IDX number
    idx_pattern = re.compile(r'^\s*(\d+)\s+')
    # Page number pattern (standalone number at end of page)
    page_pattern = re.compile(r'^\s*\d+\s*$')
    # Title pattern
    title_pattern = re.compile(r'^ModMed EMA:')
    
    skip_next_lines = False
    
    for line_no, line in enumerate(lines):
        stripped = line.rstrip()
        
        # Skip empty lines
        if not stripped.strip():
            continue
        
        # Skip title lines
        if title_pattern.match(stripped.strip()):
            continue
            
        # Skip header rows
        if header_pattern.match(stripped):
            skip_next_lines = True
            continue
        
        # Skip the "Length" continuation of header
        if skip_next_lines:
            if 'Length' in stripped and len(stripped.strip()) < 20:
                skip_next_lines = False
                continue
            skip_next_lines = False
        
        # Skip page numbers
        if page_pattern.match(stripped.strip()):
            continue
        
        # Clean invisible chars
        clean = stripped.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
        
        # Try to match a new field entry (starts with IDX number)
        m = idx_pattern.match(clean)
        if m:
            idx_val = int(m.group(1))
            rest = clean[m.end():]
            
            # Parse the rest of the line using position-based extraction
            # The layout is roughly: Grouping(col ~10-25), Table(col ~25-50), Column(col ~50-85), 
            # Description(col ~85-140), DataType(col ~140-155), Nullable(col ~155-170), 
            # FieldLength(col ~170-185), Values(col ~185+)
            
            # Use the original line with its spacing to detect columns
            parsed = parse_row(line, idx_val)
            if parsed:
                if current:
                    fields.append(current)
                current = parsed
            else:
                # Continuation line that starts with a number but isn't a real IDX
                if current:
                    current['_raw_continuation'].append(clean.strip())
        else:
            # Continuation line - append to current field
            if current:
                # Determine which column this continuation belongs to based on position
                append_continuation(current, line)
    
    if current:
        fields.append(current)
    
    # Clean up fields
    cleaned_fields = []
    for f in fields:
        # Clean whitespace in all string fields
        for key in ['grouping', 'table', 'column', 'description', 'dataType', 'nullable', 'valuesCodingSchema']:
            if isinstance(f.get(key), str):
                f[key] = ' '.join(f[key].split())
        if 'fieldLength' in f and isinstance(f['fieldLength'], str):
            f['fieldLength'] = f['fieldLength'].strip()
            try:
                f['fieldLength'] = int(f['fieldLength'])
            except ValueError:
                pass
        
        # Remove raw continuation tracking
        f.pop('_raw_continuation', None)
        f.pop('_col_positions', None)
        
        cleaned_fields.append(f)
    
    return cleaned_fields


def parse_row(line, idx_val):
    """Parse a row from the fixed-width layout."""
    clean = line.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    # Find column positions by looking at character positions
    # Typical positions in the PDF:
    # IDX: 0-5, Grouping: 6-24, Table: 24-48, Column: 48-82, Description: 82-138, 
    # DataType: 138-152, Nullable: 152-164, FieldLength: 164-180, Values: 180+
    
    # But positions shift. Let's use a smarter approach:
    # After the IDX number, find segments separated by multiple spaces
    
    # Remove the IDX part
    idx_str = str(idx_val)
    idx_pos = clean.find(idx_str)
    if idx_pos < 0:
        return None
    
    after_idx = clean[idx_pos + len(idx_str):]
    
    # Split by 2+ spaces to get fields
    parts = re.split(r'  +', after_idx.strip())
    
    if len(parts) < 3:
        return None
    
    result = {
        'idx': idx_val,
        'grouping': parts[0].strip() if len(parts) > 0 else '',
        'table': parts[1].strip() if len(parts) > 1 else '',
        'column': parts[2].strip() if len(parts) > 2 else '',
        'description': parts[3].strip() if len(parts) > 3 else '',
        'dataType': parts[4].strip() if len(parts) > 4 else '',
        'nullable': parts[5].strip() if len(parts) > 5 else '',
        'fieldLength': parts[6].strip() if len(parts) > 6 else '',
        'valuesCodingSchema': ' '.join(parts[7:]).strip() if len(parts) > 7 else '',
        '_raw_continuation': [],
        '_col_positions': {}
    }
    
    return result


def append_continuation(current, line):
    """Append continuation text to the appropriate field of current record."""
    clean = line.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    stripped = clean.strip()
    
    if not stripped:
        return
    
    # Determine which field based on the starting position of text
    # Find the first non-space character position
    first_char = len(clean) - len(clean.lstrip())
    
    # Rough column boundaries (from the PDF layout)
    if first_char < 24:
        # Could be table name continuation
        current['table'] += ' ' + stripped
    elif first_char < 48:
        # Table name continuation
        current['table'] += ' ' + stripped
    elif first_char < 82:
        # Column name continuation  
        current['column'] += ' ' + stripped
    elif first_char < 138:
        # Description continuation
        current['description'] += ' ' + stripped
    else:
        # Values/coding schema continuation
        current['valuesCodingSchema'] += ' ' + stripped


def main():
    text_file = 'analysis/detailed-dd.txt'
    fields = parse_detailed_dd(text_file)
    
    # Build table inventory
    tables = {}
    for f in fields:
        tbl = f['table']
        if tbl not in tables:
            tables[tbl] = []
        tables[tbl].append(f)
    
    # Compute stats
    groupings = {}
    for f in fields:
        g = f['grouping']
        groupings[g] = groupings.get(g, 0) + 1
    
    has_desc = sum(1 for f in fields if f.get('description', '').strip())
    has_type = sum(1 for f in fields if f.get('dataType', '').strip())
    has_values = sum(1 for f in fields if f.get('valuesCodingSchema', '').strip())
    
    output = {
        'source': 'ModMed-EMA-Detailed-Data-Dictionary.pdf',
        'extractedAt': '2026-02-16',
        'stats': {
            'totalFields': len(fields),
            'totalTables': len(tables),
            'fieldsWithDescription': has_desc,
            'fieldsWithDataType': has_type,
            'fieldsWithValues': has_values,
            'groupings': groupings,
            'tableFieldCounts': {t: len(fs) for t, fs in sorted(tables.items())}
        },
        'fields': fields
    }
    
    with open('analysis/detailed-dd-parsed.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Total fields parsed: {len(fields)}")
    print(f"Total tables: {len(tables)}")
    print(f"Fields with descriptions: {has_desc}")
    print(f"Fields with data types: {has_type}")
    print(f"Fields with values/coding: {has_values}")
    print(f"\nGroupings:")
    for g, c in sorted(groupings.items(), key=lambda x: -x[1]):
        print(f"  {g}: {c}")
    print(f"\nTop 20 tables by field count:")
    for t, fs in sorted(tables.items(), key=lambda x: -len(x[1]))[:20]:
        print(f"  {t}: {len(fs)} fields")


if __name__ == '__main__':
    main()
