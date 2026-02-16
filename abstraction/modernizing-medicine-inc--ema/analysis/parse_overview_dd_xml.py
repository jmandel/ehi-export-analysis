#!/usr/bin/env python3
"""
Parse the overview data dictionary from pdftohtml XML output.
Extracts the table inventory with descriptions, groupings, relationships, etc.
"""
import xml.etree.ElementTree as ET
import json
import re

# Column positions from the overview PDF (landscape orientation, different from detailed)
# IDX: ~33, Grouping: ~53-100, Table: ~140-260, Description: ~285-530
# Relationships: ~540-620, Longitudinal: ~635-670, Product/Vertical: ~675-710
# Financial Priority: ~715-750, Refresh Frequency: ~755-790

def get_text(el):
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        if child.text:
            parts.append(child.text)
        if child.tail:
            parts.append(child.tail)
    return ''.join(parts).strip()

def main():
    with open('downloads/overview-dd-xml.xml') as f:
        content = f.read()
    idx_pos = content.find('<?xml')
    content = content[idx_pos:]
    root = ET.fromstring(content)
    pages = root.findall('.//page')
    print(f'Total pages: {len(pages)}')
    
    # The table inventory starts on page 5 (0-indexed page 4)
    # First, find the "Database Tables" section header positions
    
    # Collect all elements
    all_elements = []
    for page in pages:
        pn = int(page.get('number', 0))
        for el in page.findall('text'):
            text = get_text(el)
            if not text:
                continue
            left = int(el.get('left', 0))
            top = int(el.get('top', 0))
            all_elements.append({
                'left': left,
                'top': top,
                'page': pn,
                'text': text
            })
    
    all_elements.sort(key=lambda e: (e['page'], e['top'], e['left']))
    
    # Find header rows (contain "IDX" at the start)
    header_tops = set()
    for el in all_elements:
        if el['text'].strip() == 'IDX' and el['left'] < 50:
            header_tops.add((el['page'], el['top']))
    
    # Determine column positions from headers
    # Look at first header page to calibrate
    for el in all_elements:
        if el['page'] == 5 and 80 <= el['top'] <= 120:
            pass  # Will examine below
    
    # Parse table rows from the overview
    # The overview has a different column layout
    # Let me first examine the positions on data pages
    
    # Look at first few data rows to calibrate
    print("\nCalibrating column positions from page 5:")
    for el in all_elements:
        if el['page'] == 5 and el['top'] < 200:
            print(f"  left={el['left']:>5} top={el['top']:>5} text=\"{el['text'][:60]}\"")
    
    # Column bounds for overview (landscape format, width ~1188)
    OV_COLS = [
        ('idx_grouping', 55, 205),
        ('table', 205, 330),
        ('description', 330, 685),
        ('relationships', 685, 830),
        ('longitudinal', 830, 920),
        ('product_vertical', 920, 995),
        ('financial_priority', 995, 1060),
        ('refresh_frequency', 1060, 1130),
    ]
    
    def classify(left):
        for name, lo, hi in OV_COLS:
            if lo <= left < hi:
                return name
        return None
    
    # Known groupings
    KNOWN_GROUPINGS = [
        'PM Financials', 'Ophth Pretesting', 'Document Management', 'Office Flow',
        'CC/HPI', 'Practice', 'Patient', 'Lookup', 'eLab', 'Pathology',
        'Prescription', 'Appointment', 'Visit', 'Exam', 'Diagnosis',
        'Procedure', 'Inventory', 'Document', 'MIPS'
    ]
    KNOWN_GROUPINGS.sort(key=len, reverse=True)
    
    def parse_idx_grp(text):
        m = re.match(r'^(\d+)\s*(.*)', text.strip())
        if not m:
            return None, None, None
        idx_val = int(m.group(1))
        rest = m.group(2).strip()
        for g in KNOWN_GROUPINGS:
            if rest.startswith(g):
                after = rest[len(g):].strip()
                return idx_val, g, after if after else None
        return idx_val, rest, None
    
    # Parse rows
    rows = []
    cur = None
    
    for el in all_elements:
        if el['page'] < 5 or el['page'] > 77:
            continue
        
        col = classify(el['left'])
        if not col:
            continue
        
        text = el['text']
        
        # Skip headers
        if any(el['page'] == hp and abs(el['top'] - ht) <= 5 for hp, ht in header_tops):
            continue
        if text in ('IDX', 'Grouping', 'Table', 'Description', 'Relationships', 
                     'Longitudinal', 'Tracking', 'Product/', 'Vertical', 'Financial',
                     'Priority', 'Refresh', 'Frequency', 'Delivery'):
            continue
        if text.startswith('ModMed EMA:') or text == 'Database Tables':
            continue
        
        if col == 'idx_grouping':
            idx_val, grouping, table_start = parse_idx_grp(text)
            if idx_val is not None:
                if cur:
                    rows.append(cur)
                cur = {
                    'idx': idx_val,
                    'grouping': grouping or '',
                    'table_parts': [table_start] if table_start else [],
                    'description_parts': [],
                    'relationships_parts': [],
                    'longitudinal_parts': [],
                    'product_vertical_parts': [],
                    'financial_priority_parts': [],
                    'refresh_parts': [],
                }
                continue
            # Continuation
            if cur and not cur.get('grouping'):
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
        elif col == 'description':
            cur['description_parts'].append(text)
        elif col == 'relationships':
            cur['relationships_parts'].append(text)
        elif col == 'longitudinal':
            cur['longitudinal_parts'].append(text)
        elif col == 'product_vertical':
            cur['product_vertical_parts'].append(text)
        elif col == 'financial_priority':
            cur['financial_priority_parts'].append(text)
        elif col == 'refresh_frequency':
            cur['refresh_parts'].append(text)
    
    if cur:
        rows.append(cur)
    
    # Convert to entries
    entries = []
    for row in rows:
        table = ''.join(row['table_parts']).strip()
        # Clean up table name: remove line-break artifacts
        table = re.sub(r'\s+', '_', table) if table else ''
        # Actually just join without space for wrapped names
        table = ''.join(p.strip() for p in row['table_parts']).strip()
        
        # Handle merged table+description: table names are snake_case, 
        # descriptions start with uppercase. Split if we detect this.
        if '   ' in table:
            # Multiple spaces indicate table name ended and description began
            parts = re.split(r'   +', table, 1)
            table = parts[0].strip()
            if len(parts) > 1:
                description = parts[1].strip() + ' ' + description
                description = description.strip()
        
        grouping = row.get('grouping', '')
        description = ' '.join(row['description_parts']).strip()
        description = re.sub(r'\s+', ' ', description)
        relationships = [r.strip() for r in row['relationships_parts'] if r.strip()]
        longitudinal = ' '.join(row['longitudinal_parts']).strip()
        product_vertical = ' '.join(row['product_vertical_parts']).strip()
        financial_priority = ' '.join(row['financial_priority_parts']).strip()
        refresh = ' '.join(row['refresh_parts']).strip()
        
        entries.append({
            'idx': row['idx'],
            'grouping': grouping,
            'table': table,
            'description': description,
            'relationships': relationships,
            'longitudinalTracking': longitudinal,
            'productVertical': product_vertical,
            'financialPriority': financial_priority,
            'refreshFrequency': refresh,
        })
    
    # Propagate grouping
    last_grouping = ''
    for e in entries:
        if e['grouping']:
            last_grouping = e['grouping']
        else:
            e['grouping'] = last_grouping
    
    # Stats
    table_set = sorted(set(e['table'] for e in entries if e['table']))
    groupings = {}
    for e in entries:
        g = e['grouping'] or '(empty)'
        groupings[g] = groupings.get(g, 0) + 1
    
    output = {
        'source': 'ModMed-EMA-EHI-Export-Data-Dictionary.pdf',
        'extractedAt': '2026-02-16',
        'stats': {
            'totalTables': len(entries),
            'uniqueTableNames': len(table_set),
            'groupings': dict(sorted(groupings.items(), key=lambda x: -x[1]))
        },
        'tables': entries
    }
    
    with open('analysis/overview-dd-parsed.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nTotal table entries: {len(entries)}")
    print(f"Unique table names: {len(table_set)}")
    print(f"\nGroupings:")
    for g, c in sorted(groupings.items(), key=lambda x: -x[1]):
        print(f"  {g}: {c}")
    
    # Check for bad names
    bad = [t for t in table_set if ' ' in t]
    print(f"\nTables with spaces: {len(bad)}")
    for t in bad[:10]:
        print(f"  {t}")
    
    # Show first few entries
    print("\nFirst 5 entries:")
    for e in entries[:5]:
        print(f"  IDX={e['idx']} grp={e['grouping']} tbl={e['table']} desc={e['description'][:60]}")

if __name__ == '__main__':
    main()
