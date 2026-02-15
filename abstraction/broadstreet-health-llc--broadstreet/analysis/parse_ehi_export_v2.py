"""
Parse BroadStreet EHI Export rendered HTML using regex-based extraction.
Produces hard counts of resources, fields, and documentation quality metrics.
"""

import json
import re

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/broadstreet-health-llc--broadstreet/downloads"

with open(f"{DOWNLOADS}/ehi-export-page-rendered.html") as f:
    html = f.read()

# Split by h2/h3 headings
def extract_headings_and_lists(html_text):
    """Extract heading hierarchy and list items from HTML."""
    # Find all headings
    headings = re.findall(r'<h([123])[^>]*>.*?</h\1>', html_text, re.DOTALL)
    
    # Split content by headings
    parts = re.split(r'(<h[123][^>]*>.*?</h[123]>)', html_text, flags=re.DOTALL)
    
    sections = []
    current_heading = None
    current_level = 0
    
    for part in parts:
        heading_match = re.match(r'<h([123])[^>]*>(.*?)</h\1>', part, re.DOTALL)
        if heading_match:
            current_level = int(heading_match.group(1))
            # Strip HTML tags from heading text
            current_heading = re.sub(r'<[^>]+>', '', heading_match.group(2)).strip()
            sections.append({
                'level': current_level,
                'heading': current_heading,
                'items': []
            })
        elif current_heading and sections:
            # Extract list items
            items = re.findall(r'<li>(.*?)</li>', part, re.DOTALL)
            for item in items:
                clean = re.sub(r'<[^>]+>', '', item).strip()
                # Normalize whitespace
                clean = re.sub(r'\s+', ' ', clean)
                sections[-1]['items'].append(clean)
    
    return sections

sections = extract_headings_and_lists(html)

# Print section structure
print("=" * 70)
print("SECTION STRUCTURE")
print("=" * 70)
for s in sections:
    indent = "  " * (s['level'] - 1)
    print(f"{indent}[H{s['level']}] {s['heading']} ({len(s['items'])} items)")
    for item in s['items']:
        print(f"{indent}  - {item[:100]}")

# Identify FHIR resources on EHI page
fhir_resources_ehi = []
for s in sections:
    if "FHIR" in s.get('heading', '') and s['level'] == 2:
        for item in s['items']:
            if ':' in item:
                resource = item.split(':')[0].strip()
                fhir_resources_ehi.append(resource)

# Identify Notes HTML fields
notes_fields = []
in_notes = False
for s in sections:
    if 'Broadstreet Notes' in s.get('heading', '') or 'BroadStreet Notes' in s.get('heading', ''):
        in_notes = True
        continue
    if in_notes and s['level'] == 3:
        section_name = s['heading']
        for item in s['items']:
            if ':' in item:
                field = item.split(':')[0].strip()
                desc = ':'.join(item.split(':')[1:]).strip()
                notes_fields.append({
                    'section': section_name,
                    'field': field,
                    'description': desc
                })
            else:
                notes_fields.append({
                    'section': section_name,
                    'field': None,
                    'description': item
                })
    elif in_notes and s['level'] <= 2:
        in_notes = False

# (g)(10) resources from FHIR resources page screenshot
g10_clinical = [
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
    "DiagnosticReport", "Encounter", "Goal", "Immunization",
    "Medication", "MedicationRequest", "Observation", "Procedure"
]
g10_references = [
    "DocumentReference", "Device", "Location", "Organization",
    "Patient", "Practitioner", "PractitionerRole", "Provenance",
    "QuestionnaireResponse", "RelatedPerson", "ServiceRequest"
]
g10_all = set(g10_clinical + g10_references)
ehi_fhir = set(fhir_resources_ehi)

# CDA sections described
cda_items = []
for s in sections:
    if 'CDA' in s.get('heading', '') and s['level'] == 2:
        cda_items = s['items']

print("\n" + "=" * 70)
print("FHIR RESOURCES ON EHI EXPORT PAGE")
print("=" * 70)
print(f"Count: {len(fhir_resources_ehi)}")
for r in fhir_resources_ehi:
    print(f"  - {r}")

print("\n" + "=" * 70)
print("FHIR RESOURCE COMPARISON (EHI page vs g(10) API)")
print("=" * 70)
print(f"(g)(10) API resources: {len(g10_all)}")
print(f"EHI page FHIR resources: {len(ehi_fhir)}")
on_ehi_not_g10 = sorted(ehi_fhir - g10_all)
on_g10_not_ehi = sorted(g10_all - ehi_fhir)
print(f"On EHI page only: {on_ehi_not_g10}")
print(f"In (g)(10) API only: {on_g10_not_ehi}")
print(f"Overlap: {sorted(ehi_fhir & g10_all)}")

print("\n" + "=" * 70)
print("BROADSTREET NOTES (HTML) FIELDS")
print("=" * 70)
named_fields = [f for f in notes_fields if f['field']]
print(f"Total named fields: {len(named_fields)}")
print(f"Sections:")
note_sections = list(dict.fromkeys(f['section'] for f in notes_fields))
for ns in note_sections:
    section_fields = [f for f in notes_fields if f['section'] == ns and f['field']]
    print(f"  {ns}: {len(section_fields)} fields")
    for f in section_fields:
        print(f"    - {f['field']}: {f['description']}")

print("\n" + "=" * 70)
print("CDA 2.1 SECTION")
print("=" * 70)
print(f"Items described: {len(cda_items)}")
for item in cda_items:
    print(f"  - {item[:120]}")

# Compile final results
results = {
    "export_formats": ["CDA 2.1", "FHIR R4", "BroadStreet Notes (HTML)"],
    "fhir_resources_on_ehi_page": fhir_resources_ehi,
    "fhir_resources_on_ehi_page_count": len(fhir_resources_ehi),
    "g10_api_resources": sorted(g10_all),
    "g10_api_resources_count": len(g10_all),
    "on_ehi_not_g10": on_ehi_not_g10,
    "on_g10_not_ehi": on_g10_not_ehi,
    "notes_html_fields": notes_fields,
    "notes_html_named_fields_count": len(named_fields),
    "notes_html_sections": note_sections,
    "notes_html_sections_count": len(note_sections),
    "cda_items": cda_items,
    "cda_items_count": len(cda_items),
    "documentation_quality": {
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_field_types": False,
        "has_relationships": False,
        "has_value_sets": False,
        "has_export_instructions": False,
        "has_machine_readable_artifacts": False
    },
    "section_structure": [
        {"level": s["level"], "heading": s["heading"], "items_count": len(s["items"])}
        for s in sections
    ]
}

with open("ehi_export_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n✅ Results saved to ehi_export_analysis.json")
