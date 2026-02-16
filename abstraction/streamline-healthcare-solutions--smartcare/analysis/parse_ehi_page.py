"""Parse the EHI export HTML page and WordPress API JSON to extract structured data."""

import json
import re
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/streamline-healthcare-solutions--smartcare/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/streamline-healthcare-solutions--smartcare/analysis"

# Parse the WordPress API JSON (cleaner content)
with open(f"{DOWNLOADS}/ehi-export-page-wp-api.json") as f:
    wp_data = json.load(f)

page_metadata = {
    "page_id": wp_data["id"],
    "title": wp_data["title"]["rendered"],
    "published": wp_data["date"],
    "modified": wp_data["modified"],
    "slug": wp_data["slug"],
    "url": wp_data["link"],
}

# Extract C-CDA sections from the rendered HTML content
content_html = wp_data["content"]["rendered"]

# Find all links and their text
section_pattern = re.compile(
    r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', re.IGNORECASE
)
sections = []
for match in section_pattern.finditer(content_html):
    url = match.group(1)
    text = match.group(2).strip()
    if "build.fhir.org" in url:
        # Extract OID from URL
        oid_match = re.search(r'StructureDefinition-([\d.]+)\.html', url)
        oid = oid_match.group(1) if oid_match else None
        
        # Determine entry requirement
        entry_req = "not specified"
        if "(entries required)" in text:
            entry_req = "entries required"
        elif "(entries optional)" in text:
            entry_req = "entries optional"
        
        clean_name = re.sub(r'\s*\(entries (?:required|optional)\)', '', text).strip()
        
        sections.append({
            "name": clean_name,
            "full_text": text,
            "hl7_url": url,
            "oid": oid,
            "entry_requirement": entry_req,
        })

# Extract bullet points from Getting Started section
bullet_pattern = re.compile(r'<li>([^<]+(?:<[^>]+>[^<]*</[^>]+>)?[^<]*)</li>', re.IGNORECASE)
bullets = []
for match in bullet_pattern.finditer(content_html):
    text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
    # Clean up HTML entities
    text = text.replace('&#8217;', "'").replace('&#8211;', "–")
    bullets.append(text)

# Compute word count of substantive content (excluding HTML tags)
plain_text = re.sub(r'<[^>]+>', ' ', content_html)
plain_text = re.sub(r'\s+', ' ', plain_text).strip()
word_count = len(plain_text.split())

# Build full inventory
inventory = {
    "page_metadata": page_metadata,
    "word_count_substantive": word_count,
    "export_format": "C-CDA 2.2 (HL7 Consolidated Clinical Document Architecture)",
    "export_format_detail": "XML-based patient summary documents (CCDAs)",
    "export_capabilities": bullets,
    "ccda_sections": sections,
    "section_count": len(sections),
    "sections_entries_required": len([s for s in sections if s["entry_requirement"] == "entries required"]),
    "sections_entries_optional": len([s for s in sections if s["entry_requirement"] == "entries optional"]),
    "sections_unspecified": len([s for s in sections if s["entry_requirement"] == "not specified"]),
    "documentation_artifacts": {
        "data_dictionary": False,
        "sample_data": False,
        "schema_documentation": False,
        "field_level_documentation": False,
        "downloadable_files": False,
        "screenshots": False,
        "api_documentation": False,
    },
    "access_info": {
        "cost": "No additional cost for Streamline customers",
        "access_control": "Limited to system administrators and permissioned SmartCare users",
        "single_patient": True,
        "population_export": True,
        "setup_instructions": "Available in help desk documentation (not public)",
    },
}

with open(f"{OUTPUT}/full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== EHI Export Page Analysis ===")
print(f"Page published: {page_metadata['published']}")
print(f"Page modified: {page_metadata['modified']}")
print(f"Substantive word count: {word_count}")
print(f"\nTotal C-CDA sections listed: {len(sections)}")
print(f"  Entries required: {inventory['sections_entries_required']}")
print(f"  Entries optional: {inventory['sections_entries_optional']}")
print(f"  Not specified: {inventory['sections_unspecified']}")
print(f"\nC-CDA Sections:")
for i, s in enumerate(sections, 1):
    print(f"  {i:2d}. {s['full_text']}")
    print(f"      OID: {s['oid']}")
print(f"\nExport capabilities bullet points: {len(bullets)}")
for b in bullets:
    print(f"  - {b}")
print(f"\nDocumentation completeness:")
for k, v in inventory["documentation_artifacts"].items():
    print(f"  {k}: {'Yes' if v else 'No'}")

print(f"\nFull inventory saved to: {OUTPUT}/full-entity-inventory.json")
