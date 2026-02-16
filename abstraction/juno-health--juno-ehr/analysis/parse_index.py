"""Parse Juno EHR and RxTracker data dictionary index pages.
Extracts all table names and organizes them by letter section."""

from html.parser import HTMLParser
import json
import sys

class TableIndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_section = None
        self.in_link = False
        self.current_href = None
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'h3' and 'index-section-header' in attrs_dict.get('class', ''):
            self.current_section = attrs_dict.get('id', '')
        if tag == 'a' and attrs_dict.get('href', '').endswith('.html'):
            self.in_link = True
            self.current_href = attrs_dict.get('href', '')
            
    def handle_data(self, data):
        if self.in_link:
            table_name = data.strip()
            if table_name:
                self.tables.append({
                    'name': table_name,
                    'section': self.current_section,
                    'href': self.current_href
                })
            self.in_link = False
            
    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_link = False

def parse_index(filepath, schema_name):
    with open(filepath, 'r') as f:
        html = f.read()
    parser = TableIndexParser()
    parser.feed(html)
    return {
        'schema': schema_name,
        'total_tables': len(parser.tables),
        'sections': {},
        'tables': parser.tables
    }

downloads = '/home/jmandel/hobby/ehi-export-analysis/results/juno-health--juno-ehr/downloads'

# Parse both indexes
jehr = parse_index(f'{downloads}/jehr-data-dictionary.html', 'JunoEHR')
rtvx = parse_index(f'{downloads}/rtvx-data-dictionary.html', 'RxTracker')

# Count by section
for result in [jehr, rtvx]:
    for t in result['tables']:
        sec = t['section']
        result['sections'][sec] = result['sections'].get(sec, 0) + 1

# Print summary
print(f"=== {jehr['schema']} ===")
print(f"Total tables: {jehr['total_tables']}")
for sec in sorted(jehr['sections'].keys()):
    print(f"  Section {sec}: {jehr['sections'][sec]} tables")

print(f"\n=== {rtvx['schema']} ===")
print(f"Total tables: {rtvx['total_tables']}")
for sec in sorted(rtvx['sections'].keys()):
    print(f"  Section {sec}: {rtvx['sections'][sec]} tables")

# Save full data
combined = {
    'jehr': jehr,
    'rtvx': rtvx,
    'total_tables_combined': jehr['total_tables'] + rtvx['total_tables']
}

with open('table_index.json', 'w') as f:
    json.dump(combined, f, indent=2)

print(f"\nCombined total: {combined['total_tables_combined']} tables")
print("Saved to table_index.json")
