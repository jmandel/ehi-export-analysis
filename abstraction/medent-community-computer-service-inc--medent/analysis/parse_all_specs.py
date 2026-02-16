#!/usr/bin/env python3
"""Parse all MEDENT EHI PDF specifications and ASCII field list into a unified inventory."""

import json
import re
import subprocess
import os
from pathlib import Path
from html.parser import HTMLParser

PDF_DIR = Path("../downloads/ehi_pdfs")
ASCII_HTML = Path("../downloads/asciifieldlistinter.html")
OUTPUT_FULL = Path("entity-inventory-full.json")
OUTPUT_SUMMARY = Path("entity-inventory-summary.json")

# PDFs that are metadata/setup docs, not field specifications
NON_FIELD_PDFS = {"EHI_Setup_and_File_Format_Specification.pdf", "Info_File_Specification.pdf"}

def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext -layout."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_field_spec(text, filename):
    """Parse a MEDENT field specification PDF text into structured fields."""
    lines = text.split('\n')
    fields = []
    
    # Find the header line to understand column positions
    # Headers can be "Field Description" or "Field Definition"
    header_idx = None
    for i, line in enumerate(lines):
        if 'Field Name' in line and ('Field Description' in line or 'Field Definition' in line):
            header_idx = i
            break
    
    if header_idx is None:
        return fields, "no_header_found"
    
    def parse_header(hline):
        ns = hline.index('Field Name')
        if 'Field Description' in hline:
            ds = hline.index('Field Description')
        else:
            ds = hline.index('Field Definition')
        es = None
        if 'Example Output' in hline:
            es = hline.index('Example Output')
        elif 'Example' in hline:
            es = hline.index('Example')
        return ns, ds, es
    
    header_line = lines[header_idx]
    name_start, desc_start, example_start = parse_header(header_line)
    
    # Parse field rows after header
    current_field = None
    for i in range(header_idx + 1, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
        if line.strip().startswith('Page ') and '/' in line.strip():
            continue
        # Re-detect header on subsequent pages
        if 'Field Name' in line and ('Field Description' in line or 'Field Definition' in line):
            header_line = line
            name_start, desc_start, example_start = parse_header(header_line)
            continue
        
        # Extract field name part (before desc_start)
        name_part = line[name_start:desc_start].strip() if len(line) > desc_start else line[name_start:].strip()
        
        if example_start and len(line) > example_start:
            desc_part = line[desc_start:example_start].strip()
            example_part = line[example_start:].strip()
        else:
            desc_part = line[desc_start:].strip() if len(line) > desc_start else ""
            example_part = ""
        
        if name_part:
            # New field
            if current_field:
                fields.append(current_field)
            current_field = {
                "name": name_part,
                "description": desc_part,
                "example": example_part
            }
        elif current_field and desc_part:
            # Continuation of previous field's description
            current_field["description"] += " " + desc_part
            if example_part:
                current_field["example"] += " " + example_part if current_field["example"] else example_part
    
    if current_field:
        fields.append(current_field)
    
    return fields, None

def parse_ascii_field_list(html_path):
    """Parse the ASCII Field List HTML page into structured fields."""
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    
    # The data is in a table, extract with regex
    # Look for table rows with field data
    fields = []
    
    # Find all table rows
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    cell_pattern = re.compile(r'<t[dh][^>]*>(.*?)</t[dh]>', re.DOTALL | re.IGNORECASE)
    tag_pattern = re.compile(r'<[^>]+>')
    
    for row_match in row_pattern.finditer(html):
        row_html = row_match.group(1)
        cells = cell_pattern.findall(row_html)
        if len(cells) >= 4:
            # Clean HTML tags from cells
            cleaned = [tag_pattern.sub('', c).strip() for c in cells]
            # Skip header row
            if cleaned[0] == 'Format #' or cleaned[0] == '' and cleaned[1] == '':
                continue
            # Try to parse format number
            format_num = cleaned[0].strip()
            if format_num and format_num.isdigit():
                field = {
                    "format_number": format_num,
                    "area": cleaned[1].strip() if len(cleaned) > 1 else "",
                    "name": cleaned[2].strip() if len(cleaned) > 2 else "",
                    "description": cleaned[3].strip() if len(cleaned) > 3 else "",
                    "notes": cleaned[4].strip() if len(cleaned) > 4 else ""
                }
                fields.append(field)
    
    return fields

def categorize_entity(filename):
    """Assign a category based on filename."""
    fname = filename.lower()
    categories = {
        "patient": "Demographics",
        "allergy": "Clinical - Allergies",
        "appointment": "Scheduling",
        "careteam": "Clinical - Care Team",
        "diagnosis": "Clinical - Diagnoses",
        "document": "Clinical - Documents",
        "encounter": "Clinical - Encounters",
        "exchanged": "Data Exchange",
        "eye": "Specialty - Ophthalmology",
        "financial": "Billing / Financial",
        "goal": "Clinical - Goals",
        "hipaa": "Consent / HIPAA",
        "immunization": "Clinical - Immunizations",
        "insurance": "Insurance",
        "location": "Reference - Locations",
        "medical_history": "Clinical - Medical History",
        "medicalhistory": "Clinical - Medical History",
        "medication": "Clinical - Medications",
        "obepisode": "Specialty - OB/GYN",
        "oboutcome": "Specialty - OB/GYN",
        "order": "Clinical - Orders",
        "patientplan": "Insurance",
        "problem": "Clinical - Problems",
        "procedure": "Clinical - Procedures",
        "progress_note": "Clinical - Notes",
        "provider": "Reference - Providers",
        "referral": "Clinical - Referrals",
        "result": "Clinical - Lab Results",
        "screening": "Clinical - Screenings/Assessments",
        "social": "Clinical - Social History",
        "surgical": "Clinical - Surgical History",
        "vital": "Clinical - Vitals",
    }
    for key, cat in categories.items():
        if key in fname:
            return cat
    return "Other"

def main():
    entities = []
    parse_errors = []
    
    # Process all PDFs
    for pdf_file in sorted(PDF_DIR.glob("*.pdf")):
        if pdf_file.name in NON_FIELD_PDFS:
            continue
        
        text = extract_pdf_text(pdf_file)
        fields, error = parse_field_spec(text, pdf_file.name)
        
        entity_name = pdf_file.stem.replace("_File_Specification", "").replace("_Specification", "").replace("FileSpecification", "").replace("FileSpec", "")
        category = categorize_entity(pdf_file.name)
        
        # Clean up field descriptions
        for f in fields:
            f["description"] = re.sub(r'\s+', ' ', f["description"]).strip()
            f["example"] = re.sub(r'\s+', ' ', f.get("example", "")).strip()
        
        entity = {
            "entity_name": entity_name,
            "source_file": pdf_file.name,
            "category": category,
            "field_count": len(fields),
            "fields": fields,
        }
        if error:
            entity["parse_error"] = error
            parse_errors.append(pdf_file.name)
        
        entities.append(entity)
    
    # Process ASCII Field List as a special "Financial" entity
    ascii_fields = parse_ascii_field_list(ASCII_HTML)
    
    # Group ASCII fields by area
    area_groups = {}
    for f in ascii_fields:
        area = f.get("area", "Unknown")
        if area not in area_groups:
            area_groups[area] = []
        area_groups[area].append(f)
    
    # Get area descriptions from enrichment file if available
    area_descs = {}
    enrichment_path = Path("../downloads/enrichment/ascii-field-list.json")
    if enrichment_path.exists():
        with open(enrichment_path) as ef:
            enrichment = json.load(ef)
            area_descs = enrichment.get("area_descriptions", {})
    
    financial_entity = {
        "entity_name": "Financial_ASCII_FieldList",
        "source_file": "asciifieldlistinter.html",
        "category": "Billing / Financial",
        "field_count": len(ascii_fields),
        "note": "750 configurable financial/billing export fields from MEDENT ASCII Field List, organized by area",
        "areas": {
            area: {
                "description": area_descs.get(area, ""),
                "field_count": len(flds),
                "fields": flds
            }
            for area, flds in sorted(area_groups.items())
        },
        "fields": ascii_fields
    }
    entities.append(financial_entity)
    
    # Build full inventory
    inventory = {
        "product": "MEDENT",
        "version": "v23.7",
        "export_format": "CSV/pipe-delimited text files + C-CDA 2.1 Unstructured Documents",
        "total_entities": len(entities),
        "total_fields_ehi_specs": sum(e["field_count"] for e in entities if e["source_file"].endswith(".pdf")),
        "total_fields_ascii_financial": len(ascii_fields),
        "total_fields_all": sum(e["field_count"] for e in entities),
        "parse_errors": parse_errors,
        "entities": entities
    }
    
    with open(OUTPUT_FULL, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Build summary
    category_stats = {}
    for e in entities:
        cat = e["category"]
        if cat not in category_stats:
            category_stats[cat] = {"entity_count": 0, "total_fields": 0, "entities": []}
        category_stats[cat]["entity_count"] += 1
        category_stats[cat]["total_fields"] += e["field_count"]
        category_stats[cat]["entities"].append({
            "name": e["entity_name"],
            "fields": e["field_count"],
            "source": e["source_file"]
        })
    
    # Fields with descriptions
    described_ehi = 0
    total_ehi = 0
    for e in entities:
        if e["source_file"].endswith(".pdf"):
            for f in e["fields"]:
                total_ehi += 1
                if f.get("description") and len(f["description"]) > 2:
                    described_ehi += 1
    
    described_ascii = 0
    for f in ascii_fields:
        if f.get("description") and len(f["description"]) > 2:
            described_ascii += 1
    
    summary = {
        "product": "MEDENT",
        "total_entities": len(entities),
        "total_fields_ehi_specs": inventory["total_fields_ehi_specs"],
        "total_fields_ascii_financial": len(ascii_fields),
        "total_fields_combined": inventory["total_fields_all"],
        "ehi_fields_with_descriptions": described_ehi,
        "ehi_fields_description_pct": round(described_ehi / total_ehi * 100, 1) if total_ehi > 0 else 0,
        "ascii_fields_with_descriptions": described_ascii,
        "ascii_fields_description_pct": round(described_ascii / len(ascii_fields) * 100, 1) if ascii_fields else 0,
        "categories": {k: v for k, v in sorted(category_stats.items())},
        "parse_errors": parse_errors
    }
    
    with open(OUTPUT_SUMMARY, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"=== MEDENT EHI Export Inventory ===")
    print(f"Total entities: {len(entities)}")
    print(f"EHI spec fields: {inventory['total_fields_ehi_specs']}")
    print(f"ASCII financial fields: {len(ascii_fields)}")
    print(f"Combined total: {inventory['total_fields_all']}")
    print(f"EHI fields with descriptions: {described_ehi}/{total_ehi} ({summary['ehi_fields_description_pct']}%)")
    print(f"ASCII fields with descriptions: {described_ascii}/{len(ascii_fields)} ({summary['ascii_fields_description_pct']}%)")
    print(f"Parse errors: {parse_errors}")
    print()
    print("By category:")
    for cat, stats in sorted(category_stats.items()):
        print(f"  {cat}: {stats['entity_count']} entities, {stats['total_fields']} fields")
        for e in stats['entities']:
            print(f"    - {e['name']} ({e['fields']} fields)")

if __name__ == "__main__":
    main()
