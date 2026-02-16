"""Fetch all individual JEHR and RxTracker table pages and parse field-level detail.
Saves raw HTML to a cache directory and parses to JSON."""

import json
import os
import subprocess
import time
from html.parser import HTMLParser
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('table_index.json') as f:
    data = json.load(f)

# Create cache dirs
os.makedirs('cache/jehr', exist_ok=True)
os.makedirs('cache/rtvx', exist_ok=True)

def fetch_table_page(schema, table_name):
    """Fetch a single table page HTML."""
    base_url = f"https://ehiexports.junohealth.com/{schema}/"
    url = f"{base_url}{table_name}.html"
    cache_dir = f"cache/{schema}"
    cache_file = f"{cache_dir}/{table_name}.html"
    
    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
        with open(cache_file, 'r') as f:
            return f.read()
    
    try:
        result = subprocess.run(
            ['curl', '-sL', url, '-H', 'User-Agent: Mozilla/5.0', '--max-time', '10'],
            capture_output=True, text=True, timeout=15
        )
        html = result.stdout
        if html and len(html) > 100:
            with open(cache_file, 'w') as f:
                f.write(html)
            return html
    except Exception as e:
        pass
    return None

class TableDetailParser(HTMLParser):
    """Parse an individual table detail page."""
    def __init__(self):
        super().__init__()
        self.table_name = ''
        self.description = ''
        self.primary_keys = []
        self.foreign_keys = []
        self.columns = []
        
        self._in_header = False
        self._in_desc = False
        self._in_pk_table = False
        self._in_fk_table = False
        self._in_col_table = False
        self._in_field_desc = False
        self._current_row = []
        self._in_td = False
        self._in_th = False
        self._in_a = False
        self._current_a_text = ''
        self._td_text = ''
        self._current_field = {}
        self._section = 'none'
        self._row_count = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        
        if tag == 'div' and 'detail-header' == cls:
            self._in_header = True
        elif tag == 'div' and 'detail-header-body' in cls:
            self._in_desc = True
        elif tag == 'div' and 'detail-header3' in cls:
            self._section = 'pending'
        elif tag == 'table' and 'detail-items' in cls and 'detail-field-item' not in cls:
            if self._section == 'pk':
                self._in_pk_table = True
            elif self._section == 'fk':
                self._in_fk_table = True
        elif tag == 'table' and 'detail-field-item' in cls:
            self._in_col_table = True
        elif tag == 'div' and 'field-description' in cls:
            self._in_field_desc = True
        elif tag == 'td':
            self._in_td = True
            self._td_text = ''
        elif tag == 'th':
            self._in_th = True
        elif tag == 'a' and self._in_td:
            self._in_a = True
            self._current_a_text = ''
        elif tag == 'tr':
            self._current_row = []
            self._row_count += 1
            
    def handle_data(self, data):
        text = data.strip()
        if self._in_header:
            self.table_name = text
        elif self._in_desc:
            # Clean "Description:" prefix
            if text.startswith('Description:'):
                text = text[len('Description:'):].strip()
            self.description += text + ' '
        elif self._in_field_desc:
            if text.startswith('Description:'):
                text = text[len('Description:'):].strip()
            self._current_field['description'] = text
        elif self._section == 'pending' and text.strip():
            t = text.strip().lower()
            if 'primary' in t:
                self._section = 'pk'
            elif 'foreign' in t:
                self._section = 'fk'
            elif 'column' in t:
                self._section = 'col'
        elif self._in_td:
            self._td_text += text
        elif self._in_a and self._in_td:
            self._current_a_text += text
    
    def handle_endtag(self, tag):
        if tag == 'div':
            if self._in_header:
                self._in_header = False
            elif self._in_desc:
                self._in_desc = False
                self.description = self.description.strip()
            elif self._in_field_desc:
                self._in_field_desc = False
        elif tag == 'td':
            self._in_td = False
            self._current_row.append(self._td_text.strip())
        elif tag == 'th':
            self._in_th = False
        elif tag == 'a':
            if self._in_a:
                self._current_row.append(self._current_a_text.strip())
            self._in_a = False
        elif tag == 'tr':
            if self._in_pk_table and len(self._current_row) >= 1:
                if self._current_row[0] and self._current_row[0] != 'Column Name':
                    self.primary_keys.append(self._current_row[0])
            elif self._in_fk_table and len(self._current_row) >= 3:
                if self._current_row[0] and self._current_row[0] != 'Column Name':
                    self.foreign_keys.append({
                        'column': self._current_row[0],
                        'referenced_table': self._current_row[-1] if len(self._current_row) > 2 else ''
                    })
            elif self._in_col_table and len(self._current_row) >= 2:
                # Column row: position, name, type
                row = [r for r in self._current_row if r]
                if len(row) >= 2 and row[0] not in ('', 'Name'):
                    try:
                        pos = int(row[0])
                        self._current_field = {
                            'ordinal': pos,
                            'name': row[1] if len(row) > 1 else '',
                            'type': row[2] if len(row) > 2 else '',
                            'description': ''
                        }
                        self.columns.append(self._current_field)
                    except (ValueError, IndexError):
                        pass
        elif tag == 'table':
            self._in_pk_table = False
            self._in_fk_table = False
            # Don't reset _in_col_table here; each field is its own table

def parse_table_html(html):
    """Parse a single table detail page HTML."""
    parser = TableDetailParser()
    parser.feed(html)
    return {
        'table_name': parser.table_name,
        'description': parser.description,
        'primary_keys': parser.primary_keys,
        'foreign_keys': [fk for fk in parser.foreign_keys if fk['column']],
        'columns': parser.columns,
        'column_count': len(parser.columns),
        'described_columns': sum(1 for c in parser.columns if c.get('description', '').strip()),
    }

# Test with AU_PRESCRIPTION first
print("Testing parser with AU_PRESCRIPTION...")
html = fetch_table_page('jehr', 'AU_PRESCRIPTION')
if html:
    result = parse_table_html(html)
    print(f"  Table: {result['table_name']}")
    print(f"  Description: {result['description'][:100]}...")
    print(f"  Primary keys: {result['primary_keys']}")
    print(f"  Foreign keys: {len(result['foreign_keys'])}")
    print(f"  Columns: {result['column_count']}")
    print(f"  Described: {result['described_columns']}")
    # Show first 3 columns
    for c in result['columns'][:3]:
        print(f"    {c['ordinal']}. {c['name']} ({c['type']}): {c['description'][:80]}")
else:
    print("  FAILED to fetch")

print("\nParser test complete.")
