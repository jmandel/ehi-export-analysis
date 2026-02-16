#!/usr/bin/env python3
"""Extract and structure the visible content from the DOX EMR b10doc HTML page."""
import re
import json
import sys

html_path = "../downloads/b10doc-page.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Extract the rendered text content from the Wix SSR HTML
# The meaningful content is in wixui-rich-text__text spans
text_blocks = re.findall(r'class="[^"]*wixui-rich-text__text[^"]*">([^<]+)</span>', html)
text_blocks = [t.strip() for t in text_blocks if t.strip() and len(t.strip()) > 5]

# Extract the title
title_match = re.search(r'<title>([^<]+)</title>', html)
title = title_match.group(1) if title_match else "Unknown"

# Extract links
links = re.findall(r'href="(https?://www\.hl7\.org[^"]*)"', html)

# Extract the specific b10 content sentences
b10_sentences = []
for block in text_blocks:
    cleaned = block.replace("&nbsp;", " ").replace("&sect;", "§").strip()
    if cleaned:
        b10_sentences.append(cleaned)

result = {
    "page_title": title,
    "page_url": "https://www.doxemr.com/b10doc",
    "content_blocks": b10_sentences,
    "external_links": list(set(links)),
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_downloadable_files": False,
    "export_format": "C-CDA XML",
    "uscdi_version": "v1",
    "export_scope": "single patient and patient population",
    "total_content_sentences": len(b10_sentences),
    "documentation_artifacts_count": 0,
    "notes": "Entire (b)(10) documentation is a single web page with ~3 sentences and one external link to the HL7 C-CDA standard."
}

print(json.dumps(result, indent=2))

with open("page-content-extracted.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"\nExtracted {len(b10_sentences)} content blocks from page.", file=sys.stderr)
