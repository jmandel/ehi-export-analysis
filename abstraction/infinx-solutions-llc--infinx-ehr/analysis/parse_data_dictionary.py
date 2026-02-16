#!/usr/bin/env python3
"""Parse the IMED EHI Export Documentation PDF into structured JSON.

Reads pdftotext -layout output and extracts all 15 tables with their fields,
descriptions, types, and value sets.
"""

import subprocess
import re
import json
import sys
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "downloads", "IMED-EHI-Export-Documentation.pdf")

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_value_set(desc):
    """Extract value sets from description text like '[0=active, 1=inactive]' or '(1=Male, 2=Female)'."""
    patterns = [
        r'\[([^\]]+=[^\]]+)\]',
        r'\(([^)]+=[^)]+)\)',
    ]
    for pat in patterns:
        m = re.search(pat, desc)
        if m:
            raw = m.group(1)
            values = {}
            for pair in re.split(r',\s*', raw):
                parts = pair.split('=', 1)
                if len(parts) == 2:
                    values[parts[0].strip()] = parts[1].strip()
            if values:
                return values
    return None

# Table definitions with their expected structures
TABLE_DEFS = {
    "patientinfo": {"has_schema": False, "description": "Basic identifying information about the patient (dob, chart number, ssn), demographic information for the patient, and some medical or social history questions as customized by the clinic."},
    "charges": {"has_schema": True, "description": "All CPT charges associated with the patient's account"},
    "healthmaintenance": {"has_schema": True, "description": "Scheduled recurrent diagnostic labs or tests the provider associated with the patient."},
    "ob": {"has_schema": False, "description": "OB report of pregnancy-related visits"},
    "patient_advforms": {"has_schema": True, "description": "Online patient forms"},
    "patient_codes": {"has_schema": True, "description": "Codes of various code systems associated with the patient"},
    "patient_forms_data": {"has_schema": True, "description": "Forms filled out for the patient"},
    "patient_guarantor": {"has_schema": True, "description": "Guarantor information and demographics associated with the patient"},
    "patient_letters": {"has_schema": False, "description": "Letters written by the clinic that are associated with the patient"},
    "patient_pmp": {"has_schema": True, "description": "Prescription monitoring program database results for the patient."},
    "patient_referrals": {"has_schema": False, "description": "Referrals sent out to other providers on behalf of the patient"},
    "ptinr": {"has_schema": True, "description": "For patient requires periodic prothrombin time(PT) and international normalized ratio(INR) tests, this documents the reason for the test and the frequency decided by the provider"},
    "ptinr_log": {"has_schema": True, "description": "Logs all pt/inr test results for the patient; Connected to ptinr table."},
    "schedules": {"has_schema": True, "description": "Scheduled appointments associated with the patient."},
    "surgerymemo": {"has_schema": True, "description": "Surgical documentation for patient"},
}

def parse_tables(text):
    lines = text.split('\n')
    tables = []
    current_table = None
    current_fields = []
    in_field_section = False
    pending_field = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Detect table headers - they appear as standalone table names
        for tname in TABLE_DEFS:
            # Table name appears alone on a line (possibly with some whitespace)
            if stripped == tname:
                # Save previous table
                if current_table and pending_field:
                    current_fields.append(pending_field)
                    pending_field = None
                if current_table:
                    tables.append({"name": current_table, "fields": current_fields,
                                   "description": TABLE_DEFS[current_table]["description"]})
                current_table = tname
                current_fields = []
                in_field_section = False
                pending_field = None
                break
        
        # Detect the header row
        if current_table and ('Field Name' in stripped and 'Description' in stripped):
            in_field_section = True
            i += 1
            continue
        
        # Parse field lines
        if current_table and in_field_section and stripped:
            # Skip page headers/footers
            if 'Electronic Health Information' in stripped:
                i += 1
                continue
            if re.match(r'^\d+$', stripped):  # page numbers
                i += 1
                continue
                
            has_schema = TABLE_DEFS[current_table]["has_schema"]
            
            # Try to parse a field line - fields start with significant whitespace
            # and have a field name followed by description (and optionally schema)
            parts = re.split(r'\s{3,}', stripped)
            parts = [p.strip() for p in parts if p.strip()]
            
            if not parts:
                i += 1
                continue
            
            # Check if this looks like a field name (no spaces, or very few)
            first = parts[0]
            is_field_name = (len(first.split()) <= 2 and 
                           not first.startswith('Custom function') and
                           not first.startswith('if ') and
                           first != 'Patient Data Tables' and
                           len(first) < 40 and
                           not first.startswith('When data') and
                           not first.startswith('.'))
            
            if is_field_name and len(parts) >= 1:
                # Save pending field
                if pending_field:
                    current_fields.append(pending_field)
                
                field_name = parts[0]
                desc = parts[1] if len(parts) >= 2 else ""
                schema = parts[2] if len(parts) >= 3 else ""
                
                # For continuation lines where description wraps
                if len(parts) == 1 and not re.match(r'^[a-z_]+$', first):
                    # This is likely a continuation of the previous description
                    if pending_field:
                        current_fields.pop() if current_fields and current_fields[-1] == pending_field else None
                        pending_field["description"] += " " + first
                        pending_field = pending_field  # keep pending
                    i += 1
                    continue
                
                pending_field = {
                    "name": field_name,
                    "description": desc,
                }
                if has_schema and schema:
                    pending_field["type"] = schema
                
                # Extract value sets from description
                vs = parse_value_set(desc)
                if vs:
                    pending_field["value_set"] = vs
                if not vs and schema:
                    vs = parse_value_set(schema)
                    if vs:
                        pending_field["value_set"] = vs
                    
            elif pending_field and parts:
                # Continuation line - append to description or schema
                continuation = ' '.join(parts)
                if has_schema and len(parts) >= 2:
                    # Might be description continuation + schema
                    pending_field["description"] += " " + parts[0]
                    if not pending_field.get("type"):
                        pending_field["type"] = parts[-1]
                elif has_schema and pending_field.get("type") and len(parts) == 1:
                    # Could be type continuation
                    pending_field["type"] += " " + parts[0]
                else:
                    pending_field["description"] += " " + continuation
                
                # Re-check value sets
                vs = parse_value_set(pending_field["description"])
                if vs:
                    pending_field["value_set"] = vs
                if pending_field.get("type"):
                    vs = parse_value_set(pending_field["type"])
                    if vs:
                        pending_field["value_set"] = vs
        
        i += 1
    
    # Save last table
    if pending_field:
        current_fields.append(pending_field)
    if current_table:
        tables.append({"name": current_table, "fields": current_fields,
                       "description": TABLE_DEFS[current_table]["description"]})
    
    return tables

def main():
    text = extract_text()
    tables = parse_tables(text)
    
    # Build entity inventory
    inventory = {
        "source": "IMED-EHI-Export-Documentation.pdf",
        "export_format": {
            "primary": "ZIP archive containing CSV + C-CDA XML + PDF files",
            "structured_data": "CSV (one file per table, comma-separated with header row)",
            "clinical_data": "C-CDA XML (ccda.xml for main clinical data, ccda_[id].xml for referrals)",
            "documents": "PDF files (SoapDoc_, document_, Labs_, formletter_, OB_ prefixes)"
        },
        "tables": []
    }
    
    total_fields = 0
    fields_with_desc = 0
    fields_with_type = 0
    fields_with_valueset = 0
    
    for table in tables:
        t_entry = {
            "name": table["name"],
            "description": table["description"],
            "field_count": len(table["fields"]),
            "fields": []
        }
        for f in table["fields"]:
            field_entry = {
                "name": f["name"],
                "description": f.get("description", ""),
            }
            if f.get("type"):
                field_entry["type"] = f["type"]
            if f.get("value_set"):
                field_entry["value_set"] = f["value_set"]
            
            t_entry["fields"].append(field_entry)
            total_fields += 1
            if f.get("description", "").strip():
                fields_with_desc += 1
            if f.get("type", "").strip():
                fields_with_type += 1
            if f.get("value_set"):
                fields_with_valueset += 1
        
        inventory["tables"].append(t_entry)
    
    # Summary
    summary = {
        "total_tables": len(tables),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "fields_with_value_sets": fields_with_valueset,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "type_coverage_pct": round(fields_with_type / total_fields * 100, 1) if total_fields else 0,
        "tables_summary": []
    }
    
    for table in tables:
        t_sum = {
            "name": table["name"],
            "description": table["description"],
            "field_count": len(table["fields"]),
            "fields_with_descriptions": sum(1 for f in table["fields"] if f.get("description", "").strip()),
            "fields_with_types": sum(1 for f in table["fields"] if f.get("type", "").strip()),
        }
        summary["tables_summary"].append(t_sum)
    
    # Write outputs
    out_dir = os.path.dirname(__file__)
    
    with open(os.path.join(out_dir, "entity-inventory-full.json"), "w") as fp:
        json.dump(inventory, fp, indent=2)
    
    with open(os.path.join(out_dir, "entity-inventory-summary.json"), "w") as fp:
        json.dump(summary, fp, indent=2)
    
    # Print summary
    print(f"Tables: {len(tables)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_coverage_pct']}%)")
    print(f"Fields with types: {fields_with_type} ({summary['type_coverage_pct']}%)")
    print(f"Fields with value sets: {fields_with_valueset}")
    print()
    for t in summary["tables_summary"]:
        print(f"  {t['name']}: {t['field_count']} fields, {t['fields_with_descriptions']} described, {t['fields_with_types']} typed")

if __name__ == "__main__":
    main()
