#!/usr/bin/env python3
"""
Re-parse the 3 sections that failed JSON extraction (Device, DiagnosticReport, DocumentReference)
directly from pdftotext output, and merge into full-entity-inventory.json.
Also notes that Body Temperature is an empty section and Body Weight cross-references Pediatric Weight.
"""

import json
import subprocess
import re
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/md-synergy-solutions-llc--althea-smart-ehr")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/md-synergy-solutions-llc--althea-smart-ehr/analysis")

def extract_pdf_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(RESULTS_DIR / "downloads/AltheaEHIDocumentation.pdf"), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def extract_section(text, start_marker, end_marker):
    """Extract text between two section markers."""
    lines = text.split("\n")
    capturing = False
    section_lines = []
    for line in lines:
        if start_marker in line and not capturing:
            capturing = True
            continue
        if end_marker in line and capturing:
            break
        if capturing:
            section_lines.append(line)
    return "\n".join(section_lines)

def try_parse_json_from_section(section_text):
    """Try to extract and fix JSON from a section."""
    # Find the JSON block (starts with { and ends with })
    brace_depth = 0
    json_start = None
    json_chars = []
    
    for i, ch in enumerate(section_text):
        if ch == '{' and json_start is None:
            json_start = i
            brace_depth = 1
            json_chars.append(ch)
        elif json_start is not None:
            json_chars.append(ch)
            if ch == '{':
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    break
    
    if not json_chars:
        return None
    
    raw = "".join(json_chars)
    
    # Fix common issues: line breaks in string values
    # Join lines that are inside string values
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try fixing line-break-split strings
        fixed = re.sub(r'"\s*\n\s*"', '""', raw)  # concatenate split strings
        fixed = re.sub(r'(\w)\s*\n\s*(\w)', r'\1\2', fixed)  # join split identifiers
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            return None

def count_fields_recursive(obj, prefix=""):
    """Recursively count all unique field paths."""
    fields = set()
    if isinstance(obj, dict):
        for key, val in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            fields.add(path)
            if isinstance(val, dict):
                fields.update(count_fields_recursive(val, path))
            elif isinstance(val, list) and val:
                if isinstance(val[0], dict):
                    fields.update(count_fields_recursive(val[0], path))
    return fields

def main():
    text = extract_pdf_text()
    
    # Extract and analyze sections with parse failures
    sections_to_fix = {
        "Device": {
            "start": "Implantable Device",
            "end": "Diagnostic Report",
            "category": "Clinical - Devices",
        },
        "DiagnosticReport": {
            "start": "Diagnostic Report", 
            "end": "Document Reference",
            "category": "Clinical - Diagnostic Reports",
        },
        "DocumentReference": {
            "start": "Document Reference",
            "end": "Goal",
            "category": "Clinical - Documents",
        },
    }
    
    recovered = {}
    for rt, info in sections_to_fix.items():
        section = extract_section(text, info["start"], info["end"])
        parsed = try_parse_json_from_section(section)
        if parsed:
            fields = count_fields_recursive(parsed)
            recovered[rt] = {
                "resource_type": rt,
                "category": info["category"],
                "example_count": 1,
                "unique_field_paths": len(fields),
                "fields_with_descriptions": 0,
                "fields_with_types": len(fields),
                "parse_failure": False,
                "recovered": True,
                "fields": [{"path": p, "type": "from_example", "description": None} for p in sorted(fields)]
            }
            print(f"✓ Recovered {rt}: {len(fields)} field paths")
        else:
            print(f"✗ Could not recover {rt} - keeping as parse failure with raw text")
            # Count fields manually from the raw text
            field_count = len(re.findall(r'"(\w+)":', section))
            recovered[rt] = {
                "resource_type": rt,
                "category": info["category"],
                "example_count": 1,
                "unique_field_paths": field_count,
                "fields_with_descriptions": 0,
                "fields_with_types": 0,
                "parse_failure": True,
                "parse_error": "JSON contains line-break-split values (UDI strings, base64 data)",
                "note": f"Section exists with example but JSON couldn't be cleanly parsed. Estimated ~{field_count} fields from raw text.",
                "fields": []
            }
    
    # Body Temperature and Body Weight notes
    body_temp_note = {
        "resource_type": "Observation (Body Temperature)",
        "category": "Clinical - Observations/Vitals/Labs",
        "example_count": 0,
        "unique_field_paths": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "parse_failure": False,
        "note": "Section header exists but contains no example. Section is empty in PDF.",
        "fields": []
    }
    
    body_weight_note = {
        "resource_type": "Observation (Body Weight)",
        "category": "Clinical - Observations/Vitals/Labs",
        "example_count": 0,
        "unique_field_paths": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "parse_failure": False,
        "note": "Section header exists but says 'See example listed in Pediatric Weight'. Cross-references another section.",
        "fields": []
    }
    
    # Load existing inventory
    with open(OUTPUT_DIR / "full-entity-inventory.json") as f:
        inventory = json.load(f)
    
    # Replace parse failure entries with recovered data
    new_resource_types = []
    for rt_entry in inventory["resource_types"]:
        rt = rt_entry["resource_type"]
        if rt in recovered:
            new_resource_types.append(recovered[rt])
        elif rt == "Observation (Body Temperature)":
            new_resource_types.append(body_temp_note)
        elif rt == "Observation (Body Weight)":
            new_resource_types.append(body_weight_note)
        else:
            new_resource_types.append(rt_entry)
    
    inventory["resource_types"] = new_resource_types
    
    # Recalculate totals
    successfully_parsed = [r for r in inventory["resource_types"] if not r.get("parse_failure") and r["unique_field_paths"] > 0]
    inventory["total_resource_types"] = len(successfully_parsed)
    inventory["total_unique_field_paths"] = sum(r["unique_field_paths"] for r in inventory["resource_types"])
    
    # Count unique FHIR resource types (not subtypes)
    unique_fhir_types = set()
    for r in inventory["resource_types"]:
        rt = r["resource_type"]
        # Normalize observation subtypes
        if rt.startswith("Observation"):
            unique_fhir_types.add("Observation")
        else:
            unique_fhir_types.add(rt)
    inventory["unique_fhir_resource_types"] = len(unique_fhir_types)
    inventory["unique_fhir_resource_type_names"] = sorted(unique_fhir_types)
    
    # Update parse failures list
    inventory["parse_failures"] = [r for r in inventory["resource_types"] if r.get("parse_failure")]
    
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2, default=str)
    print(f"\nUpdated inventory saved. {inventory['unique_fhir_resource_types']} unique FHIR types, {inventory['total_unique_field_paths']} total field paths.")

if __name__ == "__main__":
    main()
