"""Parse the OrthoplexEMR EHI export HTML page and extract section/field counts."""

from html.parser import HTMLParser
import json
import re

class EHIParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.in_bold = False
        self.in_elements = False
        self.capture_text = ""
        self.all_text_parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "b":
            self.in_bold = True
            self.capture_text = ""

    def handle_endtag(self, tag):
        if tag == "b":
            self.in_bold = False
            section_name = self.capture_text.strip()
            if section_name:
                self.current_section = {"name": section_name, "fields": [], "raw_elements": ""}
                self.sections.append(self.current_section)
                self.in_elements = True

    def handle_data(self, data):
        if self.in_bold:
            self.capture_text += data
        elif self.current_section and self.in_elements:
            text = data.strip()
            if text and text != "Elements":
                self.current_section["raw_elements"] += " " + text

def parse_html(filepath):
    with open(filepath) as f:
        content = f.read()

    # Extract only the CCDA Data section
    ccda_start = content.find("<h3>CCDA Data</h3>")
    ccda_end = content.find("<h3>Patient Download</h3>")
    if ccda_start == -1:
        print("ERROR: Could not find CCDA Data section")
        return
    
    ccda_section = content[ccda_start:ccda_end] if ccda_end != -1 else content[ccda_start:]
    
    parser = EHIParser()
    parser.feed(ccda_section)

    total_fields = 0
    results = []
    
    for section in parser.sections:
        raw = section["raw_elements"].strip()
        if raw.startswith("(") and raw.endswith(")"):
            # Free-form sections like "(free form)" or "(Immunizations not provided...)"
            fields = [raw]
            field_count = 0  # Don't count free-form as structured fields
        elif "Empty" in raw:
            fields = [raw]
            field_count = 0
        else:
            # Split on commas, clean up
            fields = [f.strip() for f in raw.split(",") if f.strip()]
            field_count = len(fields)
        
        total_fields += field_count
        results.append({
            "section": section["name"],
            "field_count": field_count,
            "fields": fields
        })

    print(f"Total C-CDA sections: {len(results)}")
    print(f"Total structured fields: {total_fields}")
    print(f"Sections with structured fields: {sum(1 for r in results if r['field_count'] > 0)}")
    print(f"Sections with free-form/empty: {sum(1 for r in results if r['field_count'] == 0)}")
    print()
    
    for r in results:
        status = f"{r['field_count']} fields" if r['field_count'] > 0 else r['fields'][0]
        print(f"  {r['section']}: {status}")
        if r['field_count'] > 0:
            for f in r['fields']:
                print(f"    - {f}")
    
    # Save structured output
    output = {
        "total_sections": len(results),
        "total_structured_fields": total_fields,
        "sections_with_fields": sum(1 for r in results if r['field_count'] > 0),
        "sections_free_form_or_empty": sum(1 for r in results if r['field_count'] == 0),
        "sections": results
    }
    
    with open("parsed_sections.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved structured output to parsed_sections.json")

if __name__ == "__main__":
    parse_html("/home/jmandel/hobby/ehi-export-analysis/results/mendelson-kornblum-orthopedic-spine-specialists--orthoplexemr/downloads/Healthinformationexport.html")
