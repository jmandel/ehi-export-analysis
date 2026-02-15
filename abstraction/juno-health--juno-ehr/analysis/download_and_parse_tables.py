"""
Download and parse all Juno EHR individual table documentation pages.
Extracts: table name, description, column count, column details (name, type, description),
foreign keys, primary keys.
"""
import json
import os
import sys
import time
import urllib.request
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load table list
with open('jehr_table_list.json') as f:
    tables = json.load(f)

BASE_URL = 'https://ehiexports.junohealth.com/jehr/'
CACHE_DIR = '/tmp/juno_table_pages'
os.makedirs(CACHE_DIR, exist_ok=True)

def download_page(table_info):
    """Download a single table page, using cache."""
    name = table_info['name']
    link = table_info['link'].replace('./', '')
    cache_path = os.path.join(CACHE_DIR, link)
    
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        with open(cache_path) as f:
            return name, f.read()
    
    url = BASE_URL + link
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        with open(cache_path, 'w') as f:
            f.write(html)
        return name, html
    except Exception as e:
        return name, None

class TablePageParser(HTMLParser):
    """Parse a single table documentation page."""
    def __init__(self):
        super().__init__()
        self.description = ''
        self.columns = []
        self.foreign_keys = []
        self.primary_keys = []
        
        self._in_description = False
        self._in_field_name = False
        self._in_field_type = False
        self._in_field_desc = False
        self._in_field_position = False
        self._in_fk_col = False
        self._in_fk_ref = False
        self._in_pk_col = False
        self._current_col = {}
        self._in_detail_header_body = False
        self._text_buffer = ''
        self._collecting_desc = False
        
    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get('class', '')
        
        if tag == 'div' and 'detail-header-body' in classes:
            self._in_detail_header_body = True
            self._text_buffer = ''
        
        if tag == 'td' and 'field-position' in classes:
            self._in_field_position = True
            self._text_buffer = ''
            
        if tag == 'td' and 'field-name' in classes:
            self._in_field_name = True
            self._text_buffer = ''
            
        if tag == 'td' and 'field-type' in classes:
            self._in_field_type = True
            self._text_buffer = ''
            
        if tag == 'div' and 'field-description' in classes:
            self._in_field_desc = True
            self._text_buffer = ''
    
    def handle_endtag(self, tag):
        if tag == 'div' and self._in_detail_header_body:
            self._in_detail_header_body = False
            desc = self._text_buffer.strip()
            if desc.startswith('Description:'):
                desc = desc[len('Description:'):].strip()
            self.description = desc
            
        if tag == 'td' and self._in_field_position:
            self._in_field_position = False
            self._current_col = {'position': self._text_buffer.strip()}
            
        if tag == 'td' and self._in_field_name:
            self._in_field_name = False
            self._current_col['name'] = self._text_buffer.strip()
            
        if tag == 'td' and self._in_field_type:
            self._in_field_type = False
            self._current_col['type'] = self._text_buffer.strip()
            
        if tag == 'div' and self._in_field_desc:
            self._in_field_desc = False
            desc = self._text_buffer.strip()
            if desc.startswith('Description:'):
                desc = desc[len('Description:'):].strip()
            self._current_col['description'] = desc
            self.columns.append(dict(self._current_col))
            self._current_col = {}
    
    def handle_data(self, data):
        if self._in_detail_header_body or self._in_field_name or self._in_field_type or self._in_field_desc or self._in_field_position:
            self._text_buffer += data

# Download all tables in parallel
print(f"Downloading {len(tables)} table pages...")
results = {}
failed = []
already_cached = sum(1 for t in tables if os.path.exists(os.path.join(CACHE_DIR, t['link'].replace('./', ''))))
print(f"  Already cached: {already_cached}")

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(download_page, t): t for t in tables}
    done = 0
    for future in as_completed(futures):
        done += 1
        name, html = future.result()
        if html and 'WebContentNotFound' not in html:
            results[name] = html
        else:
            failed.append(name)
        if done % 100 == 0:
            print(f"  Downloaded {done}/{len(tables)}...")

print(f"\nDownloaded: {len(results)} tables, Failed/404: {len(failed)} tables")

# Parse all successful pages
print("\nParsing table pages...")
parsed = {}
for name, html in results.items():
    parser = TablePageParser()
    try:
        parser.feed(html)
        parsed[name] = {
            'description': parser.description,
            'column_count': len(parser.columns),
            'columns': parser.columns,
            'has_description': bool(parser.description.strip()),
        }
        
        # Check description quality
        cols_with_desc = sum(1 for c in parser.columns if c.get('description', '').strip())
        parsed[name]['columns_with_descriptions'] = cols_with_desc
        parsed[name]['columns_with_types'] = sum(1 for c in parser.columns if c.get('type', '').strip())
    except Exception as e:
        print(f"  Error parsing {name}: {e}")

# Save full inventory
with open('jehr_full_inventory.json', 'w') as f:
    # Save without full column details for the summary
    inventory = {}
    for name, info in parsed.items():
        inventory[name] = {
            'description': info['description'],
            'column_count': info['column_count'],
            'columns_with_descriptions': info['columns_with_descriptions'],
            'columns_with_types': info['columns_with_types'],
            'has_description': info['has_description'],
            'column_names': [c['name'] for c in info['columns']],
            'column_types': [c.get('type', '') for c in info['columns']],
        }
    json.dump(inventory, f, indent=2)

# Summary stats
total_cols = sum(info['column_count'] for info in parsed.values())
total_desc = sum(info['columns_with_descriptions'] for info in parsed.values())
total_types = sum(info['columns_with_types'] for info in parsed.values())
tables_with_desc = sum(1 for info in parsed.values() if info['has_description'])

print(f"\n=== SUMMARY ===")
print(f"Tables parsed: {len(parsed)}")
print(f"Tables with 404: {len(failed)}")
print(f"Tables with table-level description: {tables_with_desc}/{len(parsed)} ({100*tables_with_desc/len(parsed):.1f}%)")
print(f"Total columns: {total_cols}")
print(f"Columns with descriptions: {total_desc}/{total_cols} ({100*total_desc/total_cols:.1f}%)")
print(f"Columns with types: {total_types}/{total_cols} ({100*total_types/total_cols:.1f}%)")

# Distribution of column counts
col_counts = sorted([info['column_count'] for info in parsed.values()])
print(f"\nColumn count distribution:")
print(f"  Min: {col_counts[0]}")
print(f"  25th: {col_counts[len(col_counts)//4]}")
print(f"  Median: {col_counts[len(col_counts)//2]}")
print(f"  75th: {col_counts[3*len(col_counts)//4]}")
print(f"  Max: {col_counts[-1]}")
print(f"  Mean: {total_cols/len(parsed):.1f}")

# Top 20 largest tables
by_size = sorted(parsed.items(), key=lambda x: x[1]['column_count'], reverse=True)
print(f"\nTop 20 largest tables:")
for name, info in by_size[:20]:
    desc_pct = 100*info['columns_with_descriptions']/info['column_count'] if info['column_count'] > 0 else 0
    print(f"  {name}: {info['column_count']} columns, {info['columns_with_descriptions']} described ({desc_pct:.0f}%)")

# Tables without descriptions
no_desc = [(name, info) for name, info in parsed.items() if not info['has_description']]
print(f"\nTables WITHOUT table-level description: {len(no_desc)}")
if no_desc:
    for name, info in no_desc[:20]:
        print(f"  {name}: {info['column_count']} columns")

# Failed tables
print(f"\nFailed/404 tables ({len(failed)}):")
for name in sorted(failed):
    print(f"  {name}")

# Save failed list
with open('jehr_failed_tables.json', 'w') as f:
    json.dump(sorted(failed), f, indent=2)
    
print(f"\nSaved: jehr_full_inventory.json, jehr_failed_tables.json")
