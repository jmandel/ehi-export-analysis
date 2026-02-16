#!/usr/bin/env python3
"""
Comprehensive parser for MEDENT EHI PDF specs + ASCII financial field list.
Produces entity-inventory-full.json and entity-inventory-summary.json.

Uses a two-pass approach:
1. First extract raw text and find field names using the enrichment data as ground truth
2. Then re-parse descriptions from raw PDF text using proper column detection
"""

import json
import re
import subprocess
from pathlib import Path

PDF_DIR = Path("../downloads/ehi_pdfs")
ASCII_JSON = Path("../downloads/enrichment/ascii-field-list.json")
ENRICHMENT = Path("../downloads/enrichment/ehi-specs.json")
RAW_ENRICHMENT = Path("../downloads/enrichment/ehi-specs-raw.json")
OUTPUT_FULL = Path("entity-inventory-full.json")
OUTPUT_SUMMARY = Path("entity-inventory-summary.json")

NON_FIELD_PDFS = {"EHI_Setup_and_File_Format_Specification.pdf", "Info_File_Specification.pdf"}

def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def get_known_field_names(enrichment_data, filename):
    """Get validated field names from the enrichment extraction."""
    for spec in enrichment_data:
        if spec["filename"] == filename:
            return [f["name"] for f in spec.get("fields", [])]
    return []

def parse_pdf_with_known_fields(text, known_fields):
    """Parse PDF text using known field names as anchors.
    
    For each known field name, find the line where it appears and extract
    the description and example from that line, plus any continuation lines.
    """
    lines = text.split('\n')
    fields = []
    
    # Find header to determine column positions
    header_idx = None
    desc_col = None
    example_col = None
    
    for i, line in enumerate(lines):
        if 'Field Name' in line and ('Field Description' in line or 'Field Definition' in line):
            header_idx = i
            if 'Field Description' in line:
                desc_col = line.index('Field Description')
            else:
                desc_col = line.index('Field Definition')
            if 'Example Output' in line:
                example_col = line.index('Example Output')
            elif 'Example' in line:
                # Check it's the column header, not part of description
                idx = line.index('Example')
                if idx > desc_col:
                    example_col = idx
            break
    
    if header_idx is None or desc_col is None:
        # Fallback: just use enrichment descriptions
        return None
    
    # Build a map of line index -> field name for lines containing field names
    field_line_map = {}
    remaining_fields = list(known_fields)
    
    for i, line in enumerate(lines):
        if i <= header_idx:
            continue
        # Check if any known field name appears at start of line
        stripped = line.lstrip()
        for fname in remaining_fields:
            # Field name should appear as a word at the start of the text
            if stripped.startswith(fname) and (len(stripped) == len(fname) or stripped[len(fname)] == ' '):
                field_line_map[i] = fname
                remaining_fields.remove(fname)
                break
    
    # For each field, collect its description from desc_col to example_col,
    # and example from example_col to end of line, including continuation lines
    sorted_field_lines = sorted(field_line_map.keys())
    
    for idx, line_idx in enumerate(sorted_field_lines):
        fname = field_line_map[line_idx]
        
        # Determine range of lines for this field
        next_field_line = sorted_field_lines[idx + 1] if idx + 1 < len(sorted_field_lines) else len(lines)
        
        desc_parts = []
        example_parts = []
        
        for li in range(line_idx, next_field_line):
            line = lines[li]
            # Skip empty lines and page markers
            if not line.strip():
                continue
            if line.strip().startswith('Page ') and '/' in line.strip():
                continue
            # Skip re-appearing headers
            if 'Field Name' in line and ('Field Description' in line or 'Field Definition' in line):
                # Update column positions for new page
                if 'Field Description' in line:
                    desc_col = line.index('Field Description')
                else:
                    desc_col = line.index('Field Definition')
                if 'Example Output' in line:
                    example_col = line.index('Example Output')
                elif 'Example' in line:
                    eidx = line.index('Example')
                    if eidx > desc_col:
                        example_col = eidx
                continue
            
            # Extract description part
            if len(line) > desc_col:
                if example_col and len(line) > example_col:
                    d = line[desc_col:example_col].strip()
                    e = line[example_col:].strip()
                else:
                    d = line[desc_col:].strip()
                    e = ""
                
                if d:
                    desc_parts.append(d)
                if e:
                    example_parts.append(e)
            elif li == line_idx:
                # Field name line but too short for description column
                pass
        
        description = ' '.join(desc_parts)
        example = ' '.join(example_parts)
        
        # Clean up
        description = re.sub(r'\s+', ' ', description).strip()
        example = re.sub(r'\s+', ' ', example).strip()
        
        fields.append({
            "name": fname,
            "description": description,
            "example": example
        })
    
    return fields

def categorize_entity(filename):
    fname = filename.lower()
    mapping = [
        ("patient_file", "Demographics"),
        ("allergy", "Clinical - Allergies"),
        ("appointment", "Scheduling"),
        ("careteam", "Clinical - Care Team"),
        ("diagnosis", "Clinical - Diagnoses"),
        ("document_listing", "Clinical - Documents"),
        ("encounter", "Clinical - Encounters"),
        ("exchanged", "Data Exchange"),
        ("eye", "Specialty - Ophthalmology"),
        ("financial", "Billing / Financial"),
        ("goal", "Clinical - Goals"),
        ("hipaa", "Consent / HIPAA"),
        ("immunization", "Clinical - Immunizations"),
        ("insuranceplan", "Insurance"),
        ("location", "Reference - Locations"),
        ("medicalhistory", "Clinical - Medical History"),
        ("medication_file", "Clinical - Medications"),
        ("obepisode", "Specialty - OB/GYN"),
        ("oboutcome", "Specialty - OB/GYN"),
        ("order", "Clinical - Orders"),
        ("patientplan", "Insurance"),
        ("problem", "Clinical - Problems"),
        ("procedure", "Clinical - Procedures"),
        ("progress_note", "Clinical - Notes"),
        ("provider", "Reference - Providers"),
        ("referral", "Clinical - Referrals"),
        ("result", "Clinical - Lab Results"),
        ("screening", "Clinical - Screenings/Assessments"),
        ("socialhistory", "Clinical - Social History"),
        ("surgicalhistory", "Clinical - Surgical History"),
        ("vital", "Clinical - Vitals"),
    ]
    for key, cat in mapping:
        if key in fname:
            return cat
    return "Other"

def main():
    # Load enrichment data for field name ground truth
    with open(ENRICHMENT) as f:
        enrichment_data = json.load(f)
    
    entities = []
    parse_issues = []
    
    for pdf_file in sorted(PDF_DIR.glob("*.pdf")):
        if pdf_file.name in NON_FIELD_PDFS:
            continue
        
        known_fields = get_known_field_names(enrichment_data, pdf_file.name)
        if not known_fields:
            # Financial spec has only 1 field in enrichment; handle specially
            if 'Financial' in pdf_file.name:
                pass  # Will be handled below
            continue
        
        text = extract_pdf_text(pdf_file)
        parsed_fields = parse_pdf_with_known_fields(text, known_fields)
        
        if parsed_fields is None:
            # Fallback to enrichment data
            for spec in enrichment_data:
                if spec["filename"] == pdf_file.name:
                    parsed_fields = []
                    for ef in spec.get("fields", []):
                        # Try to split description from example
                        desc = ef.get("description", "")
                        parsed_fields.append({
                            "name": ef["name"],
                            "description": desc,
                            "example": ""
                        })
                    parse_issues.append(f"{pdf_file.name}: used enrichment fallback")
                    break
        
        if parsed_fields is None:
            parsed_fields = []
            parse_issues.append(f"{pdf_file.name}: no fields found")
        
        entity_name = pdf_file.stem.replace("_File_Specification", "").replace("_Specification", "").replace("FileSpecification", "").replace("FileSpec", "")
        category = categorize_entity(pdf_file.name)
        
        # Verify count matches enrichment
        expected = len(known_fields)
        actual = len(parsed_fields)
        if actual != expected:
            parse_issues.append(f"{pdf_file.name}: expected {expected} fields, got {actual}")
        
        entity = {
            "entity_name": entity_name,
            "source_file": pdf_file.name,
            "category": category,
            "field_count": len(parsed_fields),
            "fields": parsed_fields,
        }
        entities.append(entity)
    
    # Handle Financial entity (references ASCII Field List)
    # The PDF itself just has a few header fields; the real content is the ASCII list
    financial_text = extract_pdf_text(PDF_DIR / "Financial_File_Specification.pdf")
    fin_known = get_known_field_names(enrichment_data, "Financial_File_Specification.pdf")
    fin_fields = parse_pdf_with_known_fields(financial_text, fin_known) if fin_known else []
    if not fin_fields:
        fin_fields = [{"name": "financial_data", "description": "References 750-field ASCII Field List for configurable billing fields", "example": ""}]
    
    entities.append({
        "entity_name": "Financial",
        "source_file": "Financial_File_Specification.pdf",
        "category": "Billing / Financial",
        "field_count": len(fin_fields),
        "note": "Header fields only; actual financial content comes from 750-field ASCII Field List",
        "fields": fin_fields
    })
    
    # Load ASCII Field List
    with open(ASCII_JSON) as f:
        ascii_data = json.load(f)
    
    ascii_fields = ascii_data.get("fields", [])
    area_descs = ascii_data.get("area_descriptions", {})
    fields_by_area = ascii_data.get("fields_by_area", {})
    
    area_groups = {}
    for field in ascii_fields:
        area = field.get("area", "Unknown")
        if area not in area_groups:
            area_groups[area] = []
        area_groups[area].append(field)
    
    entities.append({
        "entity_name": "Financial_ASCII_FieldList",
        "source_file": "asciifieldlistinter.html",
        "category": "Billing / Financial",
        "field_count": len(ascii_fields),
        "note": "750 configurable financial/billing export fields organized by area",
        "areas": {
            area: {
                "description": area_descs.get(area, ""),
                "field_count": len(flds),
                "fields": flds
            }
            for area, flds in sorted(area_groups.items())
        },
        "fields": ascii_fields
    })
    
    # Calculate totals
    ehi_field_total = sum(e["field_count"] for e in entities if e["source_file"].endswith(".pdf"))
    ascii_count = len(ascii_fields)
    
    inventory = {
        "product": "MEDENT",
        "version": "v23.7",
        "export_format": "CSV/pipe-delimited text files + C-CDA 2.1 Unstructured Documents",
        "total_entities": len(entities),
        "total_fields_ehi_specs": ehi_field_total,
        "total_fields_ascii_financial": ascii_count,
        "total_fields_all": ehi_field_total + ascii_count,
        "parse_issues": parse_issues,
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
    
    # Count described fields
    described_ehi = 0
    total_ehi = 0
    for e in entities:
        if e["source_file"].endswith(".pdf"):
            for fld in e["fields"]:
                total_ehi += 1
                if fld.get("description") and len(fld["description"]) > 5:
                    described_ehi += 1
    
    described_ascii = sum(1 for f in ascii_fields if f.get("description") and len(f["description"]) > 2)
    
    summary = {
        "product": "MEDENT",
        "total_entities": len(entities),
        "total_fields_ehi_specs": ehi_field_total,
        "total_fields_ascii_financial": ascii_count,
        "total_fields_combined": ehi_field_total + ascii_count,
        "ehi_fields_with_descriptions": described_ehi,
        "ehi_fields_description_pct": round(described_ehi / total_ehi * 100, 1) if total_ehi > 0 else 0,
        "ascii_fields_with_descriptions": described_ascii,
        "ascii_fields_description_pct": round(described_ascii / ascii_count * 100, 1) if ascii_count else 0,
        "categories": {k: v for k, v in sorted(category_stats.items())},
        "parse_issues": parse_issues
    }
    
    with open(OUTPUT_SUMMARY, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print results
    print(f"=== MEDENT EHI Export Inventory ===")
    print(f"Total entities: {len(entities)}")
    print(f"EHI spec fields: {ehi_field_total}")
    print(f"ASCII financial fields: {ascii_count}")
    print(f"Combined total: {ehi_field_total + ascii_count}")
    print(f"EHI fields with descriptions: {described_ehi}/{total_ehi} ({summary['ehi_fields_description_pct']}%)")
    print(f"ASCII fields with descriptions: {described_ascii}/{ascii_count} ({summary['ascii_fields_description_pct']}%)")
    print()
    if parse_issues:
        print("Parse issues:")
        for issue in parse_issues:
            print(f"  - {issue}")
        print()
    
    print("By entity:")
    for e in entities:
        if e["source_file"].endswith(".pdf"):
            print(f"  {e['entity_name']:40s} {e['field_count']:4d} fields  [{e['category']}]")
    print(f"  {'Financial_ASCII_FieldList':40s} {ascii_count:4d} fields  [Billing / Financial]")
    print()
    print("By category:")
    for cat, stats in sorted(category_stats.items()):
        print(f"  {cat}: {stats['entity_count']} entities, {stats['total_fields']} fields")

if __name__ == "__main__":
    main()
