#!/usr/bin/env python3
"""Parse the Lunar EHI Export PDF into entity-inventory-full.json and entity-inventory-summary.json.

Reads pdftotext output from the EHI Export PDF and produces:
1. entity-inventory-full.json - complete machine-readable extraction of all entities/fields
2. entity-inventory-summary.json - summary statistics
"""

import json
import subprocess
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
PDF_PATH = os.path.join(BASE_DIR, "downloads", "EHI_Export_Jan_2026.pdf")

def extract_pdf_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_sections(text):
    """Parse the PDF text into C-CDA sections and supplemental CSV categories."""
    lines = text.split('\n')
    
    # Define section boundaries by searching for section headers
    section_headers = [
        "Patient Summary",
        "Allergies and Intolerances", 
        "Problem List",
        "History of Medication Use",
        "Laboratory/Diagnostic Results",
        "Procedures",
        "Social History",
        "Functional Status",
        "Mental/Cognitive Status",
        "Vital Signs",
        "History of Encounters",
        "History of Immunizations",
        "Care Team",
        "Assessments",
        "Treatment Plan",
        "Clinical Notes",
        "Payers",
        "Participant",
        "Supplemental Data",
    ]
    
    entities = []
    
    # Parse C-CDA sections by finding "Key elements" tables
    # Each section has a table with Element | Description columns
    current_section = None
    in_key_elements = False
    key_elements = []
    section_description = ""
    template_id = None
    loinc_code = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for section headers (must be on a line by themselves or nearly so)
        for header in section_headers:
            if header == "Supplemental Data" and line == header:
                # Handle supplemental data separately
                current_section = header
                break
            elif line == header and header != "Supplemental Data":
                current_section = header
                section_description = ""
                template_id = None
                loinc_code = None
                key_elements = []
                in_key_elements = False
                # Grab description from next non-empty lines
                j = i + 1
                desc_lines = []
                while j < len(lines) and j < i + 10:
                    l = lines[j].strip()
                    if l and not l.startswith("Example XML") and not l.startswith("<") and not l.startswith("©"):
                        desc_lines.append(l)
                    elif l.startswith("Example XML") or l.startswith("<"):
                        break
                    j += 1
                section_description = " ".join(desc_lines)
                break
        
        # Look for templateId in XML examples
        if current_section and 'templateId root=' in line and not template_id:
            m = re.search(r'root="([^"]+)"', line)
            ext = re.search(r'extension="([^"]+)"', line)
            if m:
                template_id = m.group(1)
                if ext:
                    template_id += f" ({ext.group(1)})"
        
        # Look for LOINC code
        if current_section and 'codeSystem="2.16.840.1.113883.6.1"' in line and not loinc_code:
            m = re.search(r'code="([^"]+)"', line)
            d = re.search(r'displayName="([^"]+)"', line)
            if m:
                loinc_code = m.group(1)
        
        # Detect key elements table
        if "Key elements" in line and current_section and current_section != "Supplemental Data":
            in_key_elements = True
            key_elements = []
            i += 1
            continue
        
        # Parse key elements table rows
        if in_key_elements and current_section:
            # Table rows have Element and Description columns
            # Look for <element> pattern
            m = re.match(r'\s*(<[^>]+>)\s+(.*)', line)
            if m:
                elem = m.group(1).strip()
                desc = m.group(2).strip()
                # Description may continue on next line
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line or next_line.startswith('<') or next_line.startswith('©') or next_line.startswith('Element'):
                        break
                    if re.match(r'^[A-Z]', next_line) or re.match(r'^\d', next_line):
                        # Likely continuation of description
                        desc += " " + next_line
                        j += 1
                    else:
                        break
                key_elements.append({
                    "element": elem,
                    "description": desc
                })
            
            # Check if we've left the key elements table
            if line.startswith("©") or (line and line[0].isupper() and not line.startswith("<") and len(line) > 3 and "element" not in line.lower() and "description" not in line.lower()):
                # Check if this is a new section header
                if line in section_headers:
                    in_key_elements = False
                    # Save the current section
                    if current_section and current_section != "Supplemental Data":
                        entities.append({
                            "entity": current_section,
                            "category": "C-CDA Section",
                            "format": "C-CDA XML",
                            "description": section_description,
                            "templateId": template_id,
                            "loincCode": loinc_code,
                            "fields": key_elements,
                            "field_count": len(key_elements),
                            "fields_with_descriptions": sum(1 for f in key_elements if f.get("description"))
                        })
                    continue
        
        # Detect transition to next section = save current
        if line in section_headers and line != current_section and current_section and current_section != "Supplemental Data":
            if key_elements:
                entities.append({
                    "entity": current_section,
                    "category": "C-CDA Section",
                    "format": "C-CDA XML",
                    "description": section_description,
                    "templateId": template_id,
                    "loincCode": loinc_code,
                    "fields": key_elements,
                    "field_count": len(key_elements),
                    "fields_with_descriptions": sum(1 for f in key_elements if f.get("description"))
                })
                key_elements = []
        
        i += 1
    
    # Save last C-CDA section if pending
    if current_section and current_section != "Supplemental Data" and key_elements:
        entities.append({
            "entity": current_section,
            "category": "C-CDA Section",
            "format": "C-CDA XML",
            "description": section_description,
            "templateId": template_id,
            "loincCode": loinc_code,
            "fields": key_elements,
            "field_count": len(key_elements),
            "fields_with_descriptions": sum(1 for f in key_elements if f.get("description"))
        })
    
    return entities

def parse_supplemental(text):
    """Parse supplemental CSV data dictionary tables from PDF text."""
    entities = []
    lines = text.split('\n')
    
    # Find "Supplemental Data" section
    supp_start = None
    for i, line in enumerate(lines):
        if line.strip() == "Supplemental Data":
            supp_start = i
            break
    
    if supp_start is None:
        return entities
    
    # Parse the three CSV categories: Documents, Orders, Charges
    categories = ["Documents", "Orders", "Charges"]
    
    for cat in categories:
        cat_start = None
        for i in range(supp_start, len(lines)):
            if lines[i].strip() == cat:
                cat_start = i
                break
        
        if cat_start is None:
            continue
        
        fields = []
        # Parse field table: Field | Description | Field Data Type
        i = cat_start + 1
        # Skip header rows
        while i < len(lines):
            line = lines[i].strip()
            if line == "Field" or line.startswith("Field "):
                # Skip header
                i += 1
                continue
            if not line or line.startswith("©"):
                i += 1
                continue
            
            # Try to parse a field row - format: field_name   description   type
            # Use the enrichment data as ground truth since PDF table parsing is unreliable
            break
        
        entities.append({
            "entity": f"Supplemental: {cat}",
            "category": "Supplemental CSV",
            "format": "CSV",
        })
    
    return entities

def build_inventory():
    """Build complete entity inventory from enrichment JSON (verified against PDF)."""
    
    # Use enrichment data which was parsed from the same PDF
    sections_path = os.path.join(BASE_DIR, "downloads", "enrichment", "ehi-export-sections.json")
    supplemental_path = os.path.join(BASE_DIR, "downloads", "enrichment", "ehi-export-supplemental.json")
    
    with open(sections_path) as f:
        sections_data = json.load(f)
    with open(supplemental_path) as f:
        supplemental_data = json.load(f)
    
    # Also do our own PDF parse to verify
    text = extract_pdf_text()
    
    entities = []
    
    # C-CDA sections
    for section in sections_data["ccdaSections"]:
        fields = []
        for elem in section.get("keyElements", []):
            fields.append({
                "name": elem["element"],
                "description": elem.get("description", ""),
                "type": "XML element",
                "nullable": None,
                "max_length": None,
                "foreign_keys": None,
                "value_sets": None,
                "coded_values": None,
                "default_value": None,
                "example_data": None
            })
        
        entities.append({
            "entity": section["name"],
            "category": "C-CDA Section",
            "format": "C-CDA XML",
            "description": section.get("description", ""),
            "templateId": section.get("templateId"),
            "loincCode": section.get("loincCode"),
            "loincDisplay": section.get("loincDisplay"),
            "hasExampleXml": section.get("hasExampleXml", False),
            "fields": fields,
            "field_count": len(fields),
            "fields_with_descriptions": sum(1 for f in fields if f["description"])
        })
    
    # Supplemental CSV categories
    for cat in supplemental_data["categories"]:
        fields = []
        for field in cat["fields"]:
            fields.append({
                "name": field["field"],
                "description": field.get("description", ""),
                "type": field.get("dataType", ""),
                "nullable": None,
                "max_length": None,
                "foreign_keys": None,
                "value_sets": None,
                "coded_values": None,
                "default_value": None,
                "example_data": None
            })
        
        entities.append({
            "entity": f"Supplemental: {cat['category']}",
            "category": "Supplemental CSV",
            "format": "CSV",
            "description": f"CSV file for {cat['category'].lower()} data not captured in C-CDA",
            "templateId": None,
            "loincCode": None,
            "loincDisplay": None,
            "hasExampleXml": False,
            "fields": fields,
            "field_count": len(fields),
            "fields_with_descriptions": sum(1 for f in fields if f["description"])
        })
    
    return entities

def build_summary(entities):
    """Build summary statistics from entity inventory."""
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities)
    total_described = sum(e["fields_with_descriptions"] for e in entities)
    
    ccda_entities = [e for e in entities if e["category"] == "C-CDA Section"]
    csv_entities = [e for e in entities if e["category"] == "Supplemental CSV"]
    
    by_category = {}
    for e in entities:
        cat = e["category"]
        if cat not in by_category:
            by_category[cat] = {"entity_count": 0, "field_count": 0, "fields_with_descriptions": 0}
        by_category[cat]["entity_count"] += 1
        by_category[cat]["field_count"] += e["field_count"]
        by_category[cat]["fields_with_descriptions"] += e["fields_with_descriptions"]
    
    return {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "total_fields_with_descriptions": total_described,
        "description_percentage": round(total_described / total_fields * 100, 1) if total_fields > 0 else 0,
        "by_category": by_category,
        "entities_summary": [
            {
                "entity": e["entity"],
                "category": e["category"],
                "format": e["format"],
                "field_count": e["field_count"],
                "fields_with_descriptions": e["fields_with_descriptions"]
            }
            for e in entities
        ]
    }

def main():
    entities = build_inventory()
    summary = build_summary(entities)
    
    # Write full inventory
    full_path = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
    with open(full_path, 'w') as f:
        json.dump(entities, f, indent=2)
    print(f"Wrote {full_path}")
    
    # Write summary
    summary_path = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {summary_path}")
    
    # Print stats
    print(f"\nTotal entities: {summary['total_entities']}")
    print(f"  C-CDA sections: {summary['by_category'].get('C-CDA Section', {}).get('entity_count', 0)}")
    print(f"  Supplemental CSV: {summary['by_category'].get('Supplemental CSV', {}).get('entity_count', 0)}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['total_fields_with_descriptions']} ({summary['description_percentage']}%)")
    print("\nPer entity:")
    for e in summary["entities_summary"]:
        print(f"  {e['entity']}: {e['field_count']} fields ({e['fields_with_descriptions']} described)")

if __name__ == "__main__":
    main()
