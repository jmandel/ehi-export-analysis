#!/usr/bin/env python3
"""Parse the EHI Data Dictionary HTML page and extract the NextGen Office section content."""

import re
import json

with open("../downloads/ehi-data-dictionary-page.html", "r") as f:
    content = f.read()

# Strip scripts/styles
content_clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
content_clean = re.sub(r'<style[^>]*>.*?</style>', '', content_clean, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', content_clean)
text = re.sub(r'\s+', ' ', text).strip()

# Extract the NextGen Office section
office_start = text.find("NextGen® Office NextGen Office provides")
if office_start < 0:
    office_start = text.find("NextGen Office provides EHI exports")

# Find end - next section is Direct Messaging
office_end = text.find("NextGen® Direct Messaging", office_start + 10) if office_start >= 0 else -1

office_section = text[office_start:office_end].strip() if office_start >= 0 and office_end >= 0 else "NOT FOUND"

result = {
    "page_title": "ELECTRONIC HEALTH INFORMATION DATA DICTIONARY HYPERLINKS",
    "total_html_size_bytes": len(content),
    "nextgen_office_section": {
        "full_text": office_section,
        "has_data_dictionary_link": "dictionary" in office_section.lower() and "href" in content[content.find("NextGen Office provides"):content.find("Direct Messaging", content.find("NextGen Office provides"))].lower() if "NextGen Office provides" in content else False,
        "export_format_types": [
            "CCDA Format (XML following C-CDA specification)",
            "CSV (Comma-Separated Variable)",
            "Binary files (images and PDFs)",
            "HTML files"
        ],
        "data_dictionary_provided": False,
        "sample_data_provided": False,
        "field_definitions_provided": False,
        "export_instructions_provided": False
    },
    "products_on_page": [
        {"name": "NextGen Enterprise EHR", "has_dictionary_link": True, "dictionary_file": "DD_Complete_EHI_20250627.pdf"},
        {"name": "NextGen Office", "has_dictionary_link": False, "dictionary_file": None},
        {"name": "NextGen Direct Messaging", "has_dictionary_link": False, "dictionary_file": None},
        {"name": "Mirth Connect", "has_dictionary_link": False, "dictionary_file": None}
    ]
}

with open("html-page-analysis.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
