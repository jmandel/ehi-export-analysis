#!/usr/bin/env python3
"""
Independent verification of the data dictionary by parsing the raw pdftotext output.
Identifies parse errors in the enrichment JSON and produces corrected counts.
"""

import json
import re
from pathlib import Path

PDF_TEXT = "/tmp/ehi-guide.txt"
OUTPUT_DIR = Path(__file__).parent

with open(PDF_TEXT) as f:
    text = f.read()

# Parse each CSV file section from the PDF
# Each section starts with a table header pattern:
# Description     <text>
# File name       <text>
# Data Provided   Column Heading       Data Type        Description

# Strategy: find each CSV file section by looking for "Description" followed by "File name"
# Then parse the field rows

sections = []
lines = text.split('\n')

current_section = None
in_data_rows = False
i = 0

while i < len(lines):
    line = lines[i].rstrip()
    
    # Detect section start: "Description" followed by description text, then "File name"
    if re.match(r'\s*Description\s{3,}', line) and not in_data_rows:
        # Look ahead for "File name" within next 3 lines
        found_filename = False
        for j in range(i+1, min(i+5, len(lines))):
            if re.match(r'\s*File name\s{3,}', lines[j]):
                found_filename = True
                break
        
        if found_filename:
            # Extract section description
            desc_match = re.match(r'\s*Description\s{3,}(.+)', line)
            desc_text = desc_match.group(1).strip() if desc_match else ""
            
            # Sometimes description continues on next line before "File name"
            k = i + 1
            while k < len(lines) and not re.match(r'\s*File name\s', lines[k]):
                extra = lines[k].strip()
                if extra and not extra.isdigit():
                    desc_text += " " + extra
                k += 1
            
            # Get file name
            fn_match = re.match(r'\s*File name\s{3,}(.+)', lines[k])
            file_name = fn_match.group(1).strip() if fn_match else ""
            
            # Find the "Data Provided" header
            k += 1
            while k < len(lines) and not re.match(r'\s*Data Provided\s', lines[k]):
                k += 1
            
            if current_section:
                sections.append(current_section)
            
            current_section = {
                "description": desc_text,
                "file_name": file_name,
                "fields": []
            }
            
            # Extract section name from file name
            # Pattern: EHIExtract_<name> <date>.csv or EHIExport_<name> <date>.csv
            name_match = re.search(r'EHI(?:Extract|Export)_(?:Deconversion_)?(.+?)\s', file_name)
            if name_match:
                raw_name = name_match.group(1)
                # Convert CamelCase to spaced
                current_section["name"] = re.sub(r'([a-z])([A-Z])', r'\1 \2', raw_name)
            else:
                current_section["name"] = file_name
            
            in_data_rows = True
            i = k + 1
            continue
    
    # Parse field rows
    if in_data_rows and current_section is not None:
        stripped = line.strip()
        
        # Skip empty lines, page numbers, headers
        if not stripped or stripped.isdigit() or stripped.startswith('.csv File Details'):
            i += 1
            continue
        
        # End of section: next "Description" block or end of file
        if re.match(r'\s*Description\s{3,}', line):
            # Don't advance, let outer loop catch it
            in_data_rows = False
            continue
        
        # End markers
        if stripped.startswith('EHI Export in CGM APRIMA'):
            in_data_rows = False
            i += 1
            continue
        
        # Try to parse as a field row
        # Typical format: ColumnName       datatype(len)    Description text
        # Some fields have the column name, type, and description on one line
        # Some have just column name and type (no description)
        # Some have wrapping where description continues on next line
        
        field_match = re.match(
            r'\s{8,}(\S.+?)\s{2,}(\w+(?:\([^)]*\))?)\s{2,}(.+)',
            line
        )
        if field_match:
            col_name = field_match.group(1).strip()
            data_type = field_match.group(2).strip()
            desc = field_match.group(3).strip()
            
            # Check if next line is a continuation (indented further, no type pattern)
            j = i + 1
            while j < len(lines):
                next_line = lines[j].rstrip()
                next_stripped = next_line.strip()
                if not next_stripped or next_stripped.isdigit():
                    j += 1
                    continue
                # Continuation if heavily indented and no data type pattern
                if re.match(r'\s{40,}', next_line) and not re.match(r'\s{8,}\S.+?\s{2,}\w+\(', next_line):
                    desc += " " + next_stripped
                    j += 1
                else:
                    break
            
            current_section["fields"].append({
                "name": col_name,
                "type": data_type,
                "description": desc,
                "has_description": True
            })
            i = j
            continue
        
        # Field with no description (like "glDate   date" or "Authorize Assignment   char(5)")
        field_no_desc = re.match(
            r'\s{8,}(\S.+?)\s{2,}(\w+(?:\([^)]*\))?)\s*$',
            line
        )
        if field_no_desc:
            col_name = field_no_desc.group(1).strip()
            data_type = field_no_desc.group(2).strip()
            current_section["fields"].append({
                "name": col_name,
                "type": data_type,
                "description": "",
                "has_description": False
            })
            i += 1
            continue
        
        # Continuation line for previous field description
        if current_section["fields"] and re.match(r'\s{30,}', line):
            current_section["fields"][-1]["description"] += " " + stripped
            i += 1
            continue
    
    i += 1

if current_section:
    sections.append(current_section)

# Print results
total_fields = 0
fields_with_desc = 0
fields_without_desc = []

print(f"Total CSV files parsed: {len(sections)}")
print()

for section in sections:
    n_fields = len(section["fields"])
    total_fields += n_fields
    n_desc = sum(1 for f in section["fields"] if f["has_description"])
    fields_with_desc += n_desc
    
    print(f"{section['name']}: {n_fields} fields ({n_desc} with descriptions)")
    
    for f in section["fields"]:
        if not f["has_description"]:
            fields_without_desc.append(f"{section['name']}.{f['name']}")

print(f"\nTotal fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc}")
print(f"Fields without descriptions: {total_fields - fields_with_desc}")

if fields_without_desc:
    print("\nFields missing descriptions:")
    for fname in fields_without_desc:
        print(f"  - {fname}")

# Compare with enrichment JSON
enrichment_total = 383
print(f"\nEnrichment JSON total: {enrichment_total}")
print(f"Independent parse total: {total_fields}")
if total_fields != enrichment_total:
    print(f"DISCREPANCY: difference of {total_fields - enrichment_total} fields")

# Save corrected inventory
with open(OUTPUT_DIR / "pdf-verification-results.json", "w") as f:
    json.dump({
        "total_csv_files": len(sections),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": total_fields - fields_with_desc,
        "fields_missing_descriptions": fields_without_desc,
        "sections": [{
            "name": s["name"],
            "file_name": s["file_name"],
            "description": s["description"],
            "field_count": len(s["fields"]),
            "fields": s["fields"]
        } for s in sections]
    }, f, indent=2)
