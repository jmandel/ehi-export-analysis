"""Parse the OrthoplexEMR EHI export HTML page and extract structured data dictionary."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

HTML_PATH = Path("/home/jmandel/hobby/ehi-export-analysis/results/"
    "mendelson-kornblum-orthopedic-spine-specialists--orthoplexemr/"
    "downloads/Healthinformationexport.html")

class SectionParser(HTMLParser):
    """Extract C-CDA sections and their field elements from the HTML."""
    
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.in_bold = False
        self.capture_text = ""
        self.all_text = []
        self.tag_stack = []
    
    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == 'b':
            self.in_bold = True
            self.capture_text = ""
    
    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == 'b':
            self.in_bold = False
            section_name = self.capture_text.strip()
            if section_name:
                self.current_section = {"name": section_name, "raw_elements": ""}
                self.sections.append(self.current_section)
    
    def handle_data(self, data):
        self.all_text.append(data)
        if self.in_bold:
            self.capture_text += data
        elif self.current_section is not None:
            stripped = data.strip()
            if stripped and stripped != "Elements":
                self.current_section["raw_elements"] += " " + stripped

def parse_html(html_path):
    content = html_path.read_text()
    
    # Extract only the "CCDA Data" section
    ccda_start = content.find("<h3>CCDA Data</h3>")
    patient_download = content.find("<h3>Patient Download</h3>")
    if ccda_start == -1 or patient_download == -1:
        raise ValueError("Could not find CCDA Data section boundaries")
    
    ccda_section = content[ccda_start:patient_download]
    
    parser = SectionParser()
    parser.feed(ccda_section)
    
    # Process sections into structured inventory
    entities = []
    total_fields = 0
    
    for section in parser.sections:
        raw = section["raw_elements"].strip()
        
        # Parse field names from comma-separated text
        if raw.startswith("(") and raw.endswith(")"):
            # Free form fields like "(free form)"
            fields = [{"name": raw, "type": None, "description": None}]
        elif raw == "Empty (Immunizations not provided at clinics)":
            fields = []
        else:
            # Split by comma, clean up
            field_names = [f.strip() for f in raw.split(",") if f.strip()]
            fields = [{"name": name, "type": None, "description": None} for name in field_names]
        
        entity = {
            "name": section["name"],
            "field_count": len(fields),
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "fields": fields,
            "notes": None
        }
        
        if "Immunizations" in section["name"]:
            entity["notes"] = "Empty - Immunizations not provided at clinics"
        if "(free form)" in raw:
            entity["notes"] = "Free-form text, no structured fields"
        
        entities.append(entity)
        total_fields += len(fields)
    
    return {
        "source_file": "downloads/Healthinformationexport.html",
        "format": "C-CDA (Continuity of Care Document)",
        "hl7_template": "2.16.840.1.113883.10.20.22.1.2",
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "entities": entities
    }

if __name__ == "__main__":
    result = parse_html(HTML_PATH)
    
    output_path = Path(__file__).parent / "full-entity-inventory.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    # Print summary
    print(f"Parsed {result['total_entities']} C-CDA sections")
    print(f"Total fields: {result['total_fields']}")
    print(f"Fields with descriptions: {result['fields_with_descriptions']}")
    print(f"Fields with types: {result['fields_with_types']}")
    print()
    for entity in result['entities']:
        note = f" [{entity['notes']}]" if entity['notes'] else ""
        print(f"  {entity['name']}: {entity['field_count']} fields{note}")
