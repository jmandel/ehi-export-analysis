"""Extract the EHI Export section from the Patient First mandatory disclosure HTML page."""
import re
from html.parser import HTMLParser

with open("/home/jmandel/hobby/ehi-export-analysis/results/patient-first--pas/downloads/mandatory-disclosure-page.html", "r") as f:
    html = f.read()

# Find the EHI Export section
ehi_start = html.find("Electronic Health Information (EHI) Export")
if ehi_start == -1:
    # Try alternate search
    ehi_start = html.lower().find("ehi export")
    
print(f"EHI section found at character position: {ehi_start}")

# Extract a window around it
if ehi_start > -1:
    # Find the section boundaries
    section = html[max(0, ehi_start-200):ehi_start+5000]
    
    # Strip HTML tags for readable text
    class MLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = []
            self.in_td = False
        def handle_data(self, d):
            self.result.append(d)
        def get_data(self):
            return ''.join(self.result)
    
    s = MLStripper()
    s.feed(section)
    text = s.get_data()
    # Clean up whitespace
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    print("\n".join(lines))

print("\n\n--- RAW HTML TABLE ---")
# Extract just the table
table_start = html.find("<table", ehi_start)
table_end = html.find("</table>", table_start) + len("</table>")
if table_start > -1 and table_end > -1:
    table_html = html[table_start:table_end]
    print(table_html[:3000])
