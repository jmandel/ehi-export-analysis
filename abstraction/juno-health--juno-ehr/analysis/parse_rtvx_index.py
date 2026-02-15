"""Parse the RxTracker data dictionary index HTML to extract all table names."""
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

with open('/home/jmandel/hobby/ehi-export-analysis/results/juno-health--juno-ehr/downloads/rtvx-data-dictionary.html') as f:
    html = f.read()

parser = TableLinkParser()
parser.feed(html)

print(f"Total RxTracker tables: {len(parser.tables)}")
for t in parser.tables:
    print(f"  {t['name']}")

import json
with open('rtvx_table_list.json', 'w') as f:
    json.dump(parser.tables, f, indent=2)
