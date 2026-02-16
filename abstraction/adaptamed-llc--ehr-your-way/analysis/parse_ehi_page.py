"""Parse the EHI export HTML page to extract all content and the data dictionary table."""
import html
import re
import json
from html.parser import HTMLParser

HTML_PATH = "../downloads/ehi-export-page.html"

class TextExtractor(HTMLParser):
    """Extract visible text content from the main article/content area."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_style = False
        self.in_script = False
        self.in_nav = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'style': self.in_style = True
        if tag == 'script': self.in_script = True
        if tag == 'nav': self.in_nav = True
        if tag in ('br', 'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr'):
            self.text_parts.append('\n')
            
    def handle_endtag(self, tag):
        if tag == 'style': self.in_style = False
        if tag == 'script': self.in_script = False
        if tag == 'nav': self.in_nav = False
        
    def handle_data(self, data):
        if not self.in_style and not self.in_script and not self.in_nav:
            self.text_parts.append(data)
    
    def get_text(self):
        return re.sub(r'\n{3,}', '\n\n', ''.join(self.text_parts).strip())

class TableExtractor(HTMLParser):
    """Extract all HTML tables with their content."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = None
        self.current_cell = None
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_tag = None
        self.in_style = False
        self.in_script = False
        self.rowspan_tracking = {}  # col_idx -> (value, remaining_rows)
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'style': self.in_style = True
        if tag == 'script': self.in_script = True
        if tag == 'table':
            self.in_table = True
            self.current_table = []
            self.rowspan_tracking = {}
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.cell_tag = tag
            rowspan = int(attrs_dict.get('rowspan', 1))
            colspan = int(attrs_dict.get('colspan', 1))
            self.current_cell = {'text': '', 'tag': tag, 'rowspan': rowspan, 'colspan': colspan}
            
    def handle_endtag(self, tag):
        if tag == 'style': self.in_style = False
        if tag == 'script': self.in_script = False
        if tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            self.current_cell['text'] = self.current_cell['text'].strip()
            self.current_row.append(self.current_cell)
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag == 'table' and self.in_table:
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
                
    def handle_data(self, data):
        if self.in_cell and not self.in_style and not self.in_script:
            self.current_cell['text'] += data

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract text
text_ext = TextExtractor()
text_ext.feed(html_content)
page_text = text_ext.get_text()

# Extract tables
table_ext = TableExtractor()
table_ext.feed(html_content)

print(f"=== Page text length: {len(page_text)} chars ===")
print(f"=== Number of tables found: {len(table_ext.tables)} ===")

for i, table in enumerate(table_ext.tables):
    print(f"\n--- Table {i+1}: {len(table)} rows ---")
    for j, row in enumerate(table[:3]):  # First 3 rows
        cells = [c['text'][:50] for c in row]
        print(f"  Row {j}: {cells}")
    if len(table) > 3:
        print(f"  ... ({len(table) - 3} more rows)")

# Save extracted text to file for reference
with open('page-text-extract.txt', 'w') as f:
    f.write(page_text)

print(f"\n=== Saved page text to page-text-extract.txt ===")
