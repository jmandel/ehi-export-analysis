#!/usr/bin/env python3
"""
Parse all structured artifacts from the BESTCare EHI export documentation.

The (b)(10) PDF has no data dictionary — just mentions CSV and Oracle DMP formats.
The FHIR capability statement and single-patient API docs describe the (g)(10) API,
which the vendor links from the (b)(10) doc as "API documentation."

This script extracts:
1. FHIR resource types from the capability statement
2. US Core profile fields from the single-patient API HTML
3. Summary statistics
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")


# 1. Parse FHIR CapabilityStatement
with open(DOWNLOADS / "fhir-capability-statement.json") as f:
    cs = json.load(f)

fhir_resources = []
for rest in cs.get("rest", []):
    for r in rest.get("resource", []):
        rtype = r["type"]
        interactions = [i["code"] for i in r.get("interaction", [])]
        search_params = [sp["name"] for sp in r.get("searchParam", [])]
        fhir_resources.append({
            "type": rtype,
            "interactions": interactions,
            "search_params": search_params,
        })

print(f"FHIR CapabilityStatement: {len(fhir_resources)} resource types")
for r in sorted(fhir_resources, key=lambda x: x["type"]):
    print(f"  {r['type']}: interactions={r['interactions']}, searchParams={len(r['search_params'])}")


# 2. Parse Single Patient API HTML for US Core profile details
class ProfileParser(HTMLParser):
    """Extract US Core profile sections and their must-have/must-support fields."""
    def __init__(self):
        super().__init__()
        self.profiles = []
        self.current_text = []
        self.in_body = False
        self.skip_tag = False
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        if tag in ('script', 'style'):
            self.skip_tag = True
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip_tag = False
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

    def handle_data(self, data):
        if self.in_body and not self.skip_tag:
            self.current_text.append(data)

with open(DOWNLOADS / "single-patient-api.html") as f:
    content = f.read()

parser = ProfileParser()
parser.feed(content)
full_text = "".join(parser.current_text)

# Extract profile sections
profile_pattern = re.compile(
    r'(\d+)\.\s+US Core\s+(.+?)\s+Profile'
    r'.*?Each\s+\w+\s+must have:\s*(.*?)'
    r'Each\s+\w+\s+must support:\s*(.*?)'
    r'(?=\d+\.\s+US Core|\d+\.\s+Provenance|$)',
    re.DOTALL
)

profiles = []
# Simpler approach: split by numbered sections
sections = re.split(r'\n(\d+)\.\s+US Core\s+', full_text)

# Parse the table of contents to get profile names
toc_matches = re.findall(r'(\d+)\.\s+US Core\s+(.+?)(?:\s+Profile)', full_text)
profile_names = {num: name.strip() for num, name in toc_matches}

# Also check for Provenance
if 'Provenance' in full_text:
    prov_match = re.search(r'(\d+)\.\s+US Core\s+Provenance', full_text)
    if not prov_match:
        prov_match = re.search(r'(\d+)\.\s+Provenance', full_text)

# Count unique profile names (deduplicate TOC vs body)
unique_profiles = set(profile_names.values())
print(f"\nSingle Patient API: {len(unique_profiles)} US Core profiles documented")
for num in sorted(profile_names.keys(), key=int):
    print(f"  {num}. US Core {profile_names[num]} Profile")

# Extract must-have and must-support fields per profile
# Look for patterns like "Each X must have:" followed by field names
must_have_pattern = re.compile(
    r'Each\s+(\w+)\s+must have:\s*(.*?)(?:Each\s+\w+\s+must support:|API:)',
    re.DOTALL
)
must_support_pattern = re.compile(
    r'Each\s+(\w+)\s+must support:\s*(.*?)(?:API:|$)',
    re.DOTALL
)

# Extract field lists
def extract_fields(text_block):
    """Extract field names from a must-have or must-support block."""
    fields = []
    for line in text_block.split('\n'):
        line = line.strip()
        if line and not line.startswith('API') and not line.startswith('Each'):
            # Remove numbering and clean
            cleaned = re.sub(r'^\d+\.\d+\.?\s*', '', line).strip()
            if cleaned and len(cleaned) < 100:
                fields.append(cleaned)
    return fields

must_haves = must_have_pattern.findall(full_text)
must_supports = must_support_pattern.findall(full_text)

profile_details = {}
for resource, fields_text in must_haves:
    fields = extract_fields(fields_text)
    if resource not in profile_details:
        profile_details[resource] = {"must_have": [], "must_support": []}
    profile_details[resource]["must_have"] = fields

for resource, fields_text in must_supports:
    fields = extract_fields(fields_text)
    if resource not in profile_details:
        profile_details[resource] = {"must_have": [], "must_support": []}
    profile_details[resource]["must_support"] = fields

print(f"\nProfile field details extracted for {len(profile_details)} resources:")
total_fields = 0
for resource in sorted(profile_details.keys()):
    detail = profile_details[resource]
    n = len(detail["must_have"]) + len(detail["must_support"])
    total_fields += n
    print(f"  {resource}: {len(detail['must_have'])} must-have, {len(detail['must_support'])} must-support")
print(f"\nTotal fields across all profiles: {total_fields}")


# 3. Build entity inventory
# Since there's no product-specific data dictionary, the "entities" are just
# the standard US Core FHIR resources from the (g)(10) API.
entities = []
for r in sorted(fhir_resources, key=lambda x: x["type"]):
    rtype = r["type"]
    fields = []
    if rtype in profile_details:
        for f in profile_details[rtype].get("must_have", []):
            fields.append({"name": f, "requirement": "must_have", "type": None, "description": None})
        for f in profile_details[rtype].get("must_support", []):
            fields.append({"name": f, "requirement": "must_support", "type": None, "description": None})
    
    entities.append({
        "entity_name": rtype,
        "source": "FHIR CapabilityStatement + Single Patient API",
        "category": "US Core / USCDI",
        "field_count": len(fields),
        "fields": fields,
        "notes": "Standard US Core profile — no vendor-specific extensions or data dictionary"
    })

# Save full inventory
with open(OUTPUT / "entity-inventory-full.json", "w") as f:
    json.dump({"entities": entities, "metadata": {
        "product": "BESTCare 2.0B",
        "vendor": "ezCaretech Co., Ltd.",
        "source_artifacts": [
            "b.10_EHI_Export.pdf",
            "fhir-capability-statement.json",
            "single-patient-api.html",
            "multi-patient-api.html"
        ],
        "notes": "No product-specific data dictionary exists. The (b)(10) PDF describes "
                 "CSV and Oracle DMP export formats but provides zero field-level documentation. "
                 "The only structured artifact is the FHIR (g)(10) API capability statement, "
                 "which covers standard US Core resources only."
    }}, f, indent=2)

# Save summary
summary = {
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities_with_fields": sum(1 for e in entities if e["field_count"] > 0),
    "entities_without_fields": sum(1 for e in entities if e["field_count"] == 0),
    "field_description_pct": 0,  # No descriptions provided
    "categories": {"US Core / USCDI": {
        "entity_count": len(entities),
        "field_count": sum(e["field_count"] for e in entities),
    }},
    "export_formats": {
        "csv": "Mentioned in (b)(10) PDF — no schema or field documentation",
        "oracle_dmp": "Mentioned in (b)(10) PDF — binary Oracle dump, no documentation",
        "fhir_api": "Linked from (b)(10) PDF as 'API documentation' — standard US Core (g)(10)"
    },
    "data_dictionary_exists": False,
    "sample_data_exists": False,
    "vendor_specific_extensions": False
}

with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nSummary:")
print(f"  Total entities: {summary['total_entities']}")
print(f"  Total fields documented: {summary['total_fields']}")
print(f"  Entities with field details: {summary['entities_with_fields']}")
print(f"  Data dictionary exists: {summary['data_dictionary_exists']}")
print(f"  Sample data exists: {summary['sample_data_exists']}")
print(f"\nFiles written:")
print(f"  entity-inventory-full.json")
print(f"  entity-inventory-summary.json")
