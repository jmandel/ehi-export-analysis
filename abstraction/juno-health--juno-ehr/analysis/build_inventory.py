"""Parse ALL cached table HTML pages into full-entity-inventory.json.
This is the master extraction - every entity, every field."""

import json
import os
import re
from html.parser import HTMLParser

class TableDetailParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.table_name = ''
        self.description = ''
        self.primary_keys = []
        self.foreign_keys = []
        self.columns = []
        
        self._in_header = False
        self._in_desc = False
        self._desc_parts = []
        self._in_field_desc = False
        self._field_desc_parts = []
        self._in_td = False
        self._td_text = ''
        self._current_row = []
        self._section = 'none'  # none, pk, fk, col
        self._in_pk_table = False
        self._in_fk_table = False
        self._in_col_table = False
        self._current_field = {}
        self._in_a = False
        self._a_text = ''
        self._fk_row_refs = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        
        if tag == 'div' and cls == 'detail-header':
            self._in_header = True
        elif tag == 'div' and 'detail-header-body' in cls:
            self._in_desc = True
            self._desc_parts = []
        elif tag == 'div' and 'detail-header3' in cls:
            self._section = 'pending'
        elif tag == 'table' and 'detail-items' in cls and 'detail-field-item' not in cls:
            if self._section == 'pk':
                self._in_pk_table = True
            elif self._section == 'fk':
                self._in_fk_table = True
        elif tag == 'table' and 'detail-field-item' in cls:
            self._in_col_table = True
            self._current_row = []
        elif tag == 'div' and 'field-description' in cls:
            self._in_field_desc = True
            self._field_desc_parts = []
        elif tag == 'td':
            self._in_td = True
            self._td_text = ''
        elif tag == 'a':
            if self._in_fk_table and self._in_td:
                self._in_a = True
                self._a_text = ''
        elif tag == 'tr':
            self._current_row = []
            self._fk_row_refs = []
            
    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
            
        if self._in_header:
            self.table_name = text
        elif self._in_desc:
            # Strip "Description:" prefix if present
            clean = text
            if clean.startswith('Description:'):
                clean = clean[12:].strip()
            if clean:
                self._desc_parts.append(clean)
        elif self._in_field_desc:
            clean = text
            if clean.startswith('Description:'):
                clean = clean[12:].strip()
            if clean:
                self._field_desc_parts.append(clean)
        elif self._section == 'pending':
            t = text.lower()
            if 'primary' in t:
                self._section = 'pk'
            elif 'foreign' in t:
                self._section = 'fk'
            elif 'column' in t:
                self._section = 'col'
        elif self._in_td:
            self._td_text += text
        if self._in_a:
            self._a_text += text
    
    def handle_endtag(self, tag):
        if tag == 'div':
            if self._in_header:
                self._in_header = False
            elif self._in_desc:
                self._in_desc = False
                self.description = ' '.join(self._desc_parts).strip()
            elif self._in_field_desc:
                self._in_field_desc = False
                desc = ' '.join(self._field_desc_parts).strip()
                if self._current_field:
                    self._current_field['description'] = desc
        elif tag == 'td':
            self._in_td = False
            self._current_row.append(self._td_text.strip())
        elif tag == 'a':
            if self._in_a:
                self._fk_row_refs.append(self._a_text.strip())
            self._in_a = False
        elif tag == 'tr':
            if self._in_pk_table:
                vals = [v for v in self._current_row if v and v not in ('Column Name', 'Ordinal Position')]
                if vals:
                    self.primary_keys.append(vals[0])
            elif self._in_fk_table:
                vals = [v for v in self._current_row if v and v not in ('Column Name', 'Ordinal Position', 'Referenced Table')]
                refs = [r for r in self._fk_row_refs if r]
                if vals:
                    col_name = vals[0]
                    ref_table = refs[0] if refs else (vals[2] if len(vals) > 2 else '')
                    self.foreign_keys.append({
                        'column': col_name.strip(),
                        'referenced_table': ref_table.strip()
                    })
            elif self._in_col_table:
                vals = [v for v in self._current_row if v]
                if vals and vals[0] not in ('', 'Name'):
                    try:
                        pos = int(vals[0])
                        self._current_field = {
                            'ordinal': pos,
                            'name': vals[1] if len(vals) > 1 else '',
                            'type': vals[2] if len(vals) > 2 else '',
                            'description': ''
                        }
                        self.columns.append(self._current_field)
                    except ValueError:
                        pass
        elif tag == 'table':
            if self._in_pk_table:
                self._in_pk_table = False
            elif self._in_fk_table:
                self._in_fk_table = False


def parse_table_html(html):
    parser = TableDetailParser()
    try:
        parser.feed(html)
    except Exception as e:
        return {'parse_error': True, 'error': str(e)}
    
    return {
        'table_name': parser.table_name,
        'description': parser.description,
        'primary_keys': parser.primary_keys,
        'foreign_keys': [fk for fk in parser.foreign_keys if fk.get('column')],
        'columns': parser.columns,
    }


# Load table index
with open('table_index.json') as f:
    idx = json.load(f)

inventory = {
    'schema_name': 'JunoEHR + RxTracker',
    'extraction_date': '2026-02-16',
    'source': 'ehiexports.junohealth.com',
    'schemas': {
        'jehr': {
            'name': 'JunoEHR Export Schema',
            'base_url': 'https://ehiexports.junohealth.com/jehr/',
            'entities': [],
            'stats': {}
        },
        'rtvx': {
            'name': 'RxTracker Export Schema',
            'base_url': 'https://ehiexports.junohealth.com/rtvx/',
            'entities': [],
            'stats': {}
        }
    }
}

for schema_key in ['jehr', 'rtvx']:
    tables = idx[schema_key]['tables']
    entities = []
    total_cols = 0
    total_described = 0
    total_fks = 0
    parse_errors = 0
    
    for t in tables:
        name = t['name']
        cache_file = f"cache/{schema_key}/{name}.html"
        
        if not os.path.exists(cache_file):
            entities.append({
                'table_name': name,
                'parse_error': True,
                'error': 'file not found'
            })
            parse_errors += 1
            continue
            
        with open(cache_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        result = parse_table_html(html)
        if result.get('parse_error'):
            result['table_name'] = name
            entities.append(result)
            parse_errors += 1
            continue
        
        n_cols = len(result['columns'])
        n_desc = sum(1 for c in result['columns'] if c.get('description', '').strip())
        total_cols += n_cols
        total_described += n_desc
        total_fks += len(result['foreign_keys'])
        
        entities.append(result)
    
    inventory['schemas'][schema_key]['entities'] = entities
    inventory['schemas'][schema_key]['stats'] = {
        'total_tables': len(entities),
        'total_columns': total_cols,
        'columns_with_descriptions': total_described,
        'description_rate': round(total_described / total_cols * 100, 1) if total_cols > 0 else 0,
        'total_foreign_keys': total_fks,
        'parse_errors': parse_errors,
        'tables_with_descriptions': sum(1 for e in entities if e.get('description', '').strip()),
    }
    
    stats = inventory['schemas'][schema_key]['stats']
    print(f"\n=== {schema_key.upper()} Stats ===")
    print(f"Tables: {stats['total_tables']}")
    print(f"Total columns: {stats['total_columns']}")
    print(f"Columns with descriptions: {stats['columns_with_descriptions']} ({stats['description_rate']}%)")
    print(f"Foreign keys: {stats['total_foreign_keys']}")
    print(f"Tables with descriptions: {stats['tables_with_descriptions']}")
    print(f"Parse errors: {stats['parse_errors']}")

# Combined stats
j = inventory['schemas']['jehr']['stats']
r = inventory['schemas']['rtvx']['stats']
inventory['combined_stats'] = {
    'total_tables': j['total_tables'] + r['total_tables'],
    'total_columns': j['total_columns'] + r['total_columns'],
    'columns_with_descriptions': j['columns_with_descriptions'] + r['columns_with_descriptions'],
    'total_foreign_keys': j['total_foreign_keys'] + r['total_foreign_keys'],
}
cs = inventory['combined_stats']
cs['description_rate'] = round(cs['columns_with_descriptions'] / cs['total_columns'] * 100, 1) if cs['total_columns'] > 0 else 0

print(f"\n=== COMBINED ===")
print(f"Tables: {cs['total_tables']}")
print(f"Total columns: {cs['total_columns']}")
print(f"Described: {cs['columns_with_descriptions']} ({cs['description_rate']}%)")
print(f"Foreign keys: {cs['total_foreign_keys']}")

# Save
with open('full-entity-inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)

print(f"\nSaved full-entity-inventory.json ({os.path.getsize('full-entity-inventory.json') / 1024 / 1024:.1f} MB)")
