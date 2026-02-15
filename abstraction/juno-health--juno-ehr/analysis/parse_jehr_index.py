"""Parse the Juno EHR data dictionary index HTML to extract all table names and links."""
import re
from html.parser import HTMLParser

class TableLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_section = None
        self.in_h3 = False
        self.in_link = False
        self.current_link = None
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'h3':
            self.in_h3 = True
        if tag == 'a':
            href = attrs_dict.get('href', '')
            if href.startswith('./') and href.endswith('.html'):
                self.in_link = True
                self.current_link = href
                
    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_h3 = False
        if tag == 'a':
            self.in_link = False
            
    def handle_data(self, data):
        if self.in_h3:
            stripped = data.strip()
            if stripped:
                self.current_section = stripped
        if self.in_link and self.current_link:
            table_name = data.strip()
            if table_name:
                self.tables.append({
                    'name': table_name,
                    'link': self.current_link,
                    'section': self.current_section
                })
            self.current_link = None

with open('/home/jmandel/hobby/ehi-export-analysis/results/juno-health--juno-ehr/downloads/jehr-data-dictionary.html') as f:
    html = f.read()

parser = TableLinkParser()
parser.feed(html)

print(f"Total tables found: {len(parser.tables)}")
print(f"\nTables by section:")
sections = {}
for t in parser.tables:
    s = t['section'] or 'Unknown'
    sections.setdefault(s, []).append(t['name'])

for s in sorted(sections.keys()):
    print(f"  {s}: {len(sections[s])} tables")

# Save full list
import json
with open('jehr_table_list.json', 'w') as f:
    json.dump(parser.tables, f, indent=2)

print(f"\nSaved to jehr_table_list.json")

# Show first 20 and last 20
print(f"\nFirst 20 tables:")
for t in parser.tables[:20]:
    print(f"  {t['name']} ({t['section']})")
print(f"\nLast 20 tables:")
for t in parser.tables[-20:]:
    print(f"  {t['name']} ({t['section']})")
