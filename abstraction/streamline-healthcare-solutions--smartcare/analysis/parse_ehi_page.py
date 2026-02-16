"""Parse the SmartCare EHI export documentation page and extract structured data."""
import json
import re
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/streamline-healthcare-solutions--smartcare/downloads"

# Parse the WordPress API JSON (cleaner content)
with open(f"{RESULTS_DIR}/ehi-export-page-wp-api.json") as f:
    data = json.load(f)

content = data["content"]["rendered"]
page_meta = {
    "title": data["title"]["rendered"],
    "date_published": data["date"],
    "date_modified": data["modified"],
}

# Extract all C-CDA section names and their HL7 links
class SectionExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_href = None
        self.in_link = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href" and "build.fhir.org" in val:
                    self.current_href = val
                    self.in_link = True
                    
    def handle_endtag(self, tag):
        if tag == "a":
            self.in_link = False
            self.current_href = None
            
    def handle_data(self, data):
        if self.in_link and self.current_href and "Section" in data:
            self.sections.append({
                "name": data.strip().replace("\xa0", " "),
                "hl7_url": self.current_href,
            })

extractor = SectionExtractor()
extractor.feed(content)

# Extract plain text content
text = re.sub(r"<[^>]+>", " ", content)
text = re.sub(r"\s+", " ", text).strip()
word_count = len(text.split())

# Classify sections
entries_required = []
entries_optional = []
other_sections = []

for s in extractor.sections:
    name = s["name"]
    if "entries required" in name:
        entries_required.append(name)
    elif "entries optional" in name:
        entries_optional.append(name)
    else:
        other_sections.append(name)

output = {
    "page_metadata": page_meta,
    "content_stats": {
        "total_word_count": word_count,
        "total_char_count": len(text),
    },
    "ccda_sections": {
        "total": len(extractor.sections),
        "entries_required": len(entries_required),
        "entries_optional": len(entries_optional),
        "other": len(other_sections),
        "sections": extractor.sections,
    },
    "key_claims": {
        "format": "C-CDA 2.2 (XML)",
        "single_patient": True,
        "population_export": True,
        "access_restriction": "System administrators and permissioned users",
        "additional_cost": "No",
        "setup_instructions": "Available in help desk documentation (not public)",
    },
}

# Print summary
print("=" * 60)
print("SmartCare EHI Export Page Analysis")
print("=" * 60)
print(f"Published: {page_meta['date_published']}")
print(f"Modified:  {page_meta['date_modified']}")
print(f"Content:   {word_count} words, {len(text)} characters")
print(f"C-CDA sections listed: {len(extractor.sections)}")
print()
print("Entries Required:")
for s in entries_required:
    print(f"  - {s}")
print("Entries Optional:")
for s in entries_optional:
    print(f"  - {s}")
print("Other Sections:")
for s in other_sections:
    print(f"  - {s}")
print()
print("Key observations:")
print(f"  - No data dictionary or field-level documentation")
print(f"  - No sample export files")
print(f"  - No schema/profile documentation beyond HL7 standard links")
print(f"  - No screenshots of export interface")
print(f"  - Setup instructions behind customer login wall")
print(f"  - All 17 links point to generic HL7 C-CDA 2.2 StructureDefinitions")

# Save structured output
output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/streamline-healthcare-solutions--smartcare/analysis/ehi-page-analysis.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nStructured output saved to: {output_path}")
