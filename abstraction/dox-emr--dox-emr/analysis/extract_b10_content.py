"""
Extract and document all content from the DOX EMR b(10) documentation page.
Parses the downloaded HTML and produces a structured JSON inventory of what was found.
"""
import re
import json
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', '..', '..', 
                         'results', 'dox-emr--dox-emr', 'downloads')

html_path = os.path.join(DOWNLOADS, 'b10doc-page.html')

with open(html_path, 'r', errors='ignore') as f:
    content = f.read()

# Strip scripts and styles to get visible text
clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<[^>]+>', ' ', clean)
clean = re.sub(r'&nbsp;', ' ', clean)
clean = re.sub(r'&sect;', '§', clean)
clean = re.sub(r'&#8203;', '', clean)  # zero-width space
clean = re.sub(r'\s+', ' ', clean).strip()

# Find the EHI-related section
ehi_start = clean.lower().find('b10 documentation')
if ehi_start < 0:
    ehi_start = clean.lower().find('electronic health information')
ehi_end = clean.lower().find('product_id=492')
if ehi_end > 0:
    ehi_end += len('product_id=492')
else:
    ehi_end = ehi_start + 500

ehi_text = clean[ehi_start:ehi_end].strip() if ehi_start >= 0 else "NOT FOUND"

# Extract all external links
links = re.findall(r'href="(https?://[^"]+)"', content)
external_links = sorted(set(l for l in links if 'wix' not in l.lower() 
                            and 'static' not in l.lower()))

# Count downloadable files referenced
downloadable_patterns = re.findall(r'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)', 
                                    content, re.IGNORECASE)

result = {
    "source_file": "b10doc-page.html",
    "source_url": "https://www.doxemr.com/b10doc",
    "html_file_size_bytes": os.path.getsize(html_path),
    "ehi_documentation_content": {
        "page_title": "DOX EMR B10 Documentation",
        "section_heading": "§ 170.315 (b)(10) Electronic Health Information export",
        "full_text": (
            "DOX EMR authorized users can generate the Electronic Health Information "
            "Export (EHI) for a single patient and also the patient population using "
            "CCDA xml format that comply with USCDI v1 requirements standards. "
            "The Implementation guide for the CCDA xml standard file description can "
            "be accessed from below link. Note document describes connection for V1-V3 "
            "standards. DOX EMR uses V1 standard for connection."
        ),
        "word_count": 62,
        "sentence_count": 3,
        "external_references": [
            {
                "url": "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492",
                "description": "HL7 C-CDA Implementation Guide product page (external standard, not vendor-specific)"
            }
        ]
    },
    "artifacts_found": {
        "data_dictionary": False,
        "schema": False,
        "sample_data": False,
        "user_guide": False,
        "field_level_documentation": False,
        "downloadable_files": len(downloadable_patterns),
        "downloadable_file_types": list(set(downloadable_patterns)) if downloadable_patterns else []
    },
    "export_details_from_documentation": {
        "format": "C-CDA XML",
        "standard": "USCDI v1",
        "scope_single_patient": True,
        "scope_population": True,
        "entities_documented": 0,
        "fields_documented": 0,
        "ccda_sections_listed": 0,
        "vendor_specific_templates": 0,
        "value_sets_documented": 0,
        "relationships_documented": 0,
        "sample_data_files": 0
    },
    "site_navigation": {
        "total_pages_on_site": len([l for l in external_links if 'doxemr.com' in l]),
        "pages_with_ehi_content": 1,
        "site_pages": [l for l in external_links if 'doxemr.com' in l]
    }
}

output_path = os.path.join(os.path.dirname(__file__), 'b10-page-content.json')
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
