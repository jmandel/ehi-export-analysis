"""Parse the rendered EHI Export HTML page using BeautifulSoup to extract 
all structured data about export formats and fields documented by BroadStreet."""

import json
from bs4 import BeautifulSoup

INPUT_FILE = "../../../results/broadstreet-health-llc--broadstreet/downloads/ehi-export-page-rendered.html"
OUTPUT_FILE = "ehi-export-page-parsed.json"

with open(INPUT_FILE) as f:
    soup = BeautifulSoup(f.read(), "lxml")

article = soup.find("article")

# Walk through the DOM tree extracting sections
sections = []
current_h2 = None
current_h3 = None
current_items = []

for elem in article.children:
    tag = getattr(elem, "name", None)
    
    if tag == "h2":
        # Save previous h3 section
        if current_h3 and current_items:
            sections.append({"h2": current_h2, "h3": current_h3, "items": list(current_items)})
            current_items = []
        elif current_h2 and current_items and not current_h3:
            sections.append({"h2": current_h2, "h3": None, "items": list(current_items)})
            current_items = []
        current_h2 = elem.get_text(strip=True)
        current_h3 = None
        
    elif tag == "h3":
        if current_h3 and current_items:
            sections.append({"h2": current_h2, "h3": current_h3, "items": list(current_items)})
            current_items = []
        current_h3 = elem.get_text(strip=True)
        
    elif tag == "ul":
        for li in elem.find_all("li", recursive=False):
            strong = li.find("strong")
            field_name = strong.get_text(strip=True).rstrip(":") if strong else None
            full_text = li.get_text(strip=True)
            if field_name:
                desc = full_text[full_text.index(field_name) + len(field_name):].lstrip(":").strip() if field_name in full_text else full_text
            else:
                desc = full_text
            current_items.append({"field_name": field_name, "description": desc})
    
    elif tag == "p":
        text = elem.get_text(strip=True)
        if text:
            current_items.append({"type": "paragraph", "text": text})

# Flush last section
if current_h3 and current_items:
    sections.append({"h2": current_h2, "h3": current_h3, "items": list(current_items)})
elif current_h2 and current_items:
    sections.append({"h2": current_h2, "h3": None, "items": list(current_items)})

# Now categorize: CDA section, FHIR section, Notes section
cda_section = []
fhir_section = []
notes_sections = []

for s in sections:
    h2 = s["h2"] or ""
    if "CDA" in h2:
        cda_section.append(s)
    elif "FHIR" in h2:
        fhir_section.append(s)
    elif "Notes" in h2 or "Broadstreet" in h2:
        notes_sections.append(s)

# Extract FHIR resources from the FHIR section
fhir_resources = []
for s in fhir_section:
    for item in s["items"]:
        if item.get("field_name"):
            fhir_resources.append({
                "resource": item["field_name"],
                "description": item["description"]
            })

# Extract Notes fields
notes_field_inventory = []
for s in notes_sections:
    subsection = s.get("h3") or "General"
    fields = []
    for item in s["items"]:
        if item.get("field_name") is not None:
            fields.append({
                "field_name": item["field_name"],
                "description": item["description"]
            })
        elif "type" not in item:  # skip paragraphs
            fields.append({
                "field_name": None,
                "description": item["description"]
            })
    if fields:
        notes_field_inventory.append({
            "subsection": subsection,
            "fields": fields
        })

# Count
total_notes_fields = sum(len(s["fields"]) for s in notes_field_inventory)
named_notes_fields = sum(1 for s in notes_field_inventory for f in s["fields"] if f["field_name"])

result = {
    "page_title": "EHI Export",
    "export_formats": [
        {
            "name": "CDA 2.1",
            "type": "standard_projection",
            "broadstreet_specific_documentation": "none",
            "notes": "Generic CDA 2.1 description; no BroadStreet-specific templates, section lists, or profiles"
        },
        {
            "name": "FHIR R4",
            "type": "standard_projection",
            "broadstreet_specific_documentation": "none",
            "resources": fhir_resources,
            "resource_count": len(fhir_resources),
            "notes": "Generic FHIR R4 description; resource list matches standard US Core set. No vendor-specific profiles or extensions documented."
        },
        {
            "name": "BroadStreet Notes (HTML)",
            "type": "proprietary",
            "broadstreet_specific_documentation": "field-level",
            "sections": notes_field_inventory,
            "total_fields": total_notes_fields,
            "named_fields": named_notes_fields,
            "notes": "Only BroadStreet-specific export structure documented on this page"
        }
    ],
    "summary": {
        "total_export_formats": 3,
        "fhir_resources_listed_on_ehi_page": len(fhir_resources),
        "notes_html_sections": len(notes_field_inventory),
        "notes_html_total_fields": total_notes_fields,
        "notes_html_named_fields": named_notes_fields,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_machine_readable_schema": False,
        "has_field_types": False,
        "has_value_sets": False,
        "has_relationships": False,
        "has_export_instructions": False
    },
    "raw_sections": sections
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result["summary"], indent=2))
print(f"\nFHIR resources listed on EHI page ({len(fhir_resources)}):")
for r in fhir_resources:
    print(f"  - {r['resource']}: {r['description']}")
print(f"\nNotes HTML sections ({len(notes_field_inventory)}):")
for s in notes_field_inventory:
    print(f"  {s['subsection']} ({len(s['fields'])} fields):")
    for f in s["fields"]:
        print(f"    - {f['field_name']}: {f['description']}")
