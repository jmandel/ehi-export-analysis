#!/usr/bin/env python3
"""Parse the EHNOTE EHI export HTML page and extract all structured content."""

import json
import re
from html.parser import HTMLParser

HTML_PATH = "../../../results/ehnote-inc--ehnote/downloads/ehi-export-page.html"

class TextExtractor(HTMLParser):
    """Extract visible text from HTML, stripping tags."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'head'}
        self.skip_depth = 0
        
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1
    
    def handle_data(self, data):
        if self.skip_depth == 0:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)
    
    def get_text(self):
        return '\n'.join(self.text_parts)

with open(HTML_PATH, 'r', encoding='utf-8-sig') as f:
    html_content = f.read()

# Extract text
extractor = TextExtractor()
extractor.feed(html_content)
visible_text = extractor.get_text()

# Count substantive content sections
sections = {
    "Introduction": None,
    "Understanding the Files": None,
    "Linking the Files": None,
    "Understanding the Fields and Descriptions": None,
    "Usage Terms": None,
    "Contact Information": None,
}

# Find each section in the HTML
for section_name in sections:
    pattern = re.compile(re.escape(section_name), re.IGNORECASE)
    matches = list(pattern.finditer(html_content))
    sections[section_name] = len(matches)

# Count downloadable file links
download_patterns = re.findall(r'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml|xml)', html_content, re.IGNORECASE)
outbound_links = re.findall(r'href="(https?://[^"]+)"', html_content)

# Count words in the substantive content area (between <ol class="list-sub-comb"> and closing </ol>)
content_match = re.search(r'<ol class="list-sub-comb".*?>(.*?)</ol>\s*</div>', html_content, re.DOTALL)
if content_match:
    content_html = content_match.group(1)
    # Strip tags
    content_text = re.sub(r'<[^>]+>', ' ', content_html)
    content_text = re.sub(r'\s+', ' ', content_text).strip()
    content_word_count = len(content_text.split())
else:
    content_text = ""
    content_word_count = 0

# Separate usage terms from technical content
usage_terms_match = re.search(r'<label>\s*Usage Terms\s*</label>(.*)', content_html, re.DOTALL) if content_match else None
if usage_terms_match:
    usage_text = re.sub(r'<[^>]+>', ' ', usage_terms_match.group(1))
    usage_word_count = len(usage_text.split())
    technical_word_count = content_word_count - usage_word_count
else:
    usage_word_count = 0
    technical_word_count = content_word_count

# Extract named data fields/categories mentioned
data_categories = [
    "Investigations",
    "Surgery consents",
    "Referrals",
    "Billings and Authorization files",
    "Case history",
    "Case sheets",
]

# Extract the DATA description
data_desc_match = re.search(r'DATA:\s*(.*?)(?:</p>|$)', html_content, re.DOTALL)
data_description = re.sub(r'<[^>]+>', '', data_desc_match.group(1)).strip() if data_desc_match else "Not found"

# Build results
results = {
    "page_url": "https://ehnote.com/certification/ehi-export",
    "page_size_bytes": len(html_content),
    "page_last_modified": "2025-06-03",
    "sections_found": sections,
    "total_content_words": content_word_count,
    "technical_content_words": technical_word_count,
    "usage_terms_words": usage_word_count,
    "downloadable_files": len(download_patterns),
    "outbound_links": outbound_links,
    "export_format": {
        "primary": "PDF (case sheets per appointment)",
        "secondary": "PNG/JPEG images (investigations, surgery consents, referrals, authorization files)",
        "structured_data": False,
        "machine_readable": False,
    },
    "file_naming_conventions": {
        "pdf": "CaseSheet_{BranchId}P{PatientId}_A{AppointmentDate}.pdf",
        "image": "{PatientName}_P{PatientId}_{Date}.{ext}",
    },
    "data_categories_mentioned": data_categories,
    "data_fields_described": data_description,
    "data_dictionary": {
        "exists": False,
        "entity_count": 0,
        "field_count": 0,
        "descriptions_provided": False,
        "types_provided": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False,
    },
    "export_mechanism": {
        "description": "Single patient export via 'export and download' button click",
        "bulk_export": False,
        "api_available": False,
        "fees": "No extra costs for basic export; fees possible if export exceeds contracted storage",
    },
    "vendor_statement_on_fields": "There is no 'one size fits all' set of fields in the software because of the extensive customization that is possible.",
}

with open("ehi_page_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=== EHNOTE EHI Export Page Analysis ===")
print(f"Page size: {results['page_size_bytes']:,} bytes")
print(f"Total content words: {results['total_content_words']}")
print(f"Technical content words: {results['technical_content_words']}")
print(f"Usage terms words: {results['usage_terms_words']}")
print(f"Downloadable files linked: {results['downloadable_files']}")
print(f"Outbound links: {results['outbound_links']}")
print(f"\nSections found:")
for s, c in results['sections_found'].items():
    print(f"  {s}: {c} occurrence(s)")
print(f"\nExport format: {results['export_format']['primary']}")
print(f"Data dictionary exists: {results['data_dictionary']['exists']}")
print(f"Data categories mentioned: {', '.join(results['data_categories_mentioned'])}")
print(f"Data fields described: {results['data_fields_described']}")
print(f"\nVendor statement: \"{results['vendor_statement_on_fields']}\"")
print(f"\nResults saved to ehi_page_analysis.json")
