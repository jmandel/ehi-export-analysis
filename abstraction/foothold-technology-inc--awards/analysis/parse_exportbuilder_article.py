"""Parse the ExportBuilder article HTML to extract key information about the export mechanism."""
import json
import re
from html.parser import HTMLParser

class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.text_parts = []
    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.in_article = True
        if self.in_article:
            if tag in ('h1','h2','h3','h4','h5','h6'):
                self.text_parts.append(f'\n\n[{tag.upper()}] ')
            elif tag == 'p':
                self.text_parts.append('\n')
            elif tag == 'li':
                self.text_parts.append('\n- ')
            elif tag == 'br':
                self.text_parts.append('\n')
    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article = False
    def handle_data(self, data):
        if self.in_article:
            self.text_parts.append(data.strip())

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/foothold-technology-inc--awards/downloads"

with open(f"{DOWNLOADS}/exportbuilders-main.html") as f:
    html = f.read()

parser = ArticleParser()
parser.feed(html)
text = ''.join(parser.text_parts)

# Extract key information
info = {
    "article_title": "ExportBuilders",
    "last_updated": "June 03, 2025",
    "article_text_length_chars": len(text),
    "export_formats": ["CSV", "TXT", "XLS", "XML"],
    "sub_export_modules": [
        "Hospital > Episodes",
        "Medical > Allergies",
        "Medical > Medications",
        "Employment > Jobs > Job Placements",
        "Employment > Jobs > Job Interviews"
    ],
    "mentioned_exportbuilders": [],
    "formbuilder_integration": True,
    "date_range_limit": "2 years (except HMIS History ExportBuilder)",
    "client_selection_options": [
        "Clients with Records (default)",
        "All Clients",
        "Select Client (single patient)"
    ],
    "field_types": ["Text", "Numeric", "Date", "Time", "Date/Time", "Yes/No", "List", "Phone"],
    "export_delivery": ["Save to computer", "Send in AWARDS Message (inbox)"],
    "key_features": [
        "User-configurable field selection",
        "Field ordering and renaming",
        "Value mapping (translate values during export)",
        "Saved export formats (reusable configurations)",
        "Shared formats across staff",
        "Sub-exports (embed other module data in Demographics XML)",
        "FormBuilder custom field inclusion",
        "Filter/criteria support",
        "Hidden fields (filter-only, not exported)",
        "Scheduled exports"
    ],
    "no_data_dictionary": True,
    "refers_to_reportbuilder_docs": True,
    "data_fields_listed": False,
    "sample_exports_provided": False,
    "schema_provided": False
}

# Search for specific ExportBuilder names mentioned
eb_patterns = [
    ("Demographics ExportBuilder", "Demographics"),
    ("HMIS History ExportBuilder", "HMIS History"),
    ("HMIS ExportBuilder", "HMIS"),
    ("Progress Notes ExportBuilder", "Progress Notes"),
]
for pattern, name in eb_patterns:
    if pattern.lower() in text.lower():
        info["mentioned_exportbuilders"].append(name)

# Check mentions
billing_mention = "billing" in text.lower()
treatment_mention = "treatment" in text.lower()
info["billing_mentioned"] = billing_mention
info["treatment_plan_mentioned"] = treatment_mention

print(json.dumps(info, indent=2))
with open("exportbuilder-analysis.json", "w") as f:
    json.dump(info, f, indent=2)
