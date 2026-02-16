"""Parse the OrthoplexEMR EHI export HTML page and extract the data dictionary."""
import json
import re
from html.parser import HTMLParser

with open("downloads/Healthinformationexport.html", "r") as f:
    html = f.read()

# Extract sections and their fields from the HTML
# The pattern is: <b>SectionName</b><br/>Elements<br/>field1, field2, ...
sections = []
# Find all bold section headers followed by Elements and field lists
pattern = r'<b>([^<]+)</b>\s*<br\s*/?\s*>\s*Elements\s*<br\s*/?\s*>\s*(.*?)(?=<br\s*/?\s*>\s*<br|<br\s*/?\s*>\s*</p|$)'
matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

for section_name, fields_text in matches:
    section_name = section_name.strip()
    fields_text = fields_text.strip()
    # Clean HTML tags from fields_text
    fields_text = re.sub(r'<[^>]+>', '', fields_text).strip()
    
    if fields_text.lower().startswith('empty') or fields_text.lower().startswith('(immunizations'):
        fields = []
        note = fields_text
    elif fields_text.startswith('(') or fields_text == '':
        # Free-form or empty sections
        fields = []
        # Trim to first line only for notes
        note_lines = fields_text.split('\n')
        note = note_lines[0].strip() if fields_text else "empty"
    else:
        # Parse comma-separated fields
        raw_fields = [f.strip() for f in fields_text.split(',') if f.strip()]
        fields = raw_fields
        note = None
    
    section = {
        "entity": section_name,
        "fields": [{"name": f, "type": None, "description": None} for f in fields],
        "field_count": len(fields),
        "note": note
    }
    sections.append(section)

# Build entity inventory
entity_inventory = {
    "source": "downloads/Healthinformationexport.html",
    "export_format": "C-CDA (Continuity of Care Document)",
    "export_standard_reference": "http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.1.2.html",
    "total_sections": len(sections),
    "total_fields": sum(s["field_count"] for s in sections),
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "entities": sections
}

with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(entity_inventory, f, indent=2)

# Summary
summary = {
    "source": entity_inventory["source"],
    "export_format": entity_inventory["export_format"],
    "total_sections": entity_inventory["total_sections"],
    "total_fields": entity_inventory["total_fields"],
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "sections_with_fields": sum(1 for s in sections if s["field_count"] > 0),
    "sections_freeform_or_empty": sum(1 for s in sections if s["field_count"] == 0),
    "section_summary": [
        {
            "entity": s["entity"],
            "field_count": s["field_count"],
            "note": s["note"]
        }
        for s in sections
    ]
}

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total sections: {summary['total_sections']}")
print(f"Total fields: {summary['total_fields']}")
print(f"Sections with enumerated fields: {summary['sections_with_fields']}")
print(f"Sections free-form/empty: {summary['sections_freeform_or_empty']}")
print(f"Fields with descriptions: {summary['fields_with_descriptions']}")
print(f"Fields with types: {summary['fields_with_types']}")
print()
for s in sections:
    note = f" [{s['note']}]" if s['note'] else ""
    print(f"  {s['entity']}: {s['field_count']} fields{note}")
