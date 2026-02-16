#!/usr/bin/env python3
"""
Parse the TronsHealth EHI Export PDF data dictionary.
Extracts all entities and fields from the PDF using pdftotext -layout.
Outputs entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "170.315b10-Electronic-Health-Information-Export-EHI.pdf"
OUT_DIR = Path(__file__).parent

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", str(PDF_PATH), "-"],
    capture_output=True, text=True
)
raw_text = result.stdout
lines = raw_text.split("\n")

# Parse TOC
toc_sections = []
for line in lines:
    m = re.match(r'^\s*(3\.\d+)\.\s+Patient\s+[–\-]\s+(.+?)\s*\.{2,}', line)
    if m:
        toc_sections.append({"number": m.group(1), "name": f"Patient – {m.group(2).strip()}"})

# Find section headers in the body (not TOC)
DATA_TYPES = {"long", "varchar", "nvarchar", "int", "boolean", "bool", "datetime", "decimal", "string", "list"}

sections = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if "..." in line:
        continue
    m = re.match(r'^(3\.\d+)\.\s+Patient\s+[–\-]\s+(.+?)\s*$', stripped)
    if m:
        sections.append({"num": m.group(1), "name": m.group(2).strip(), "start": i})

entities = []

for si, section in enumerate(sections):
    end_line = sections[si + 1]["start"] if si + 1 < len(sections) else len(lines)
    section_lines = lines[section["start"]:end_line]
    
    entity_name = f"Patient – {section['name']}"
    
    # Special case: Documents & Images
    if section["name"] == "Documents & Images":
        entities.append({
            "sectionNumber": section["num"],
            "name": entity_name,
            "fields": [{
                "name": "Document",
                "dataType": "file",
                "description": "All documents downloaded in their actual/native format (png, jpeg, jpg) under documents folder."
            }]
        })
        continue
    
    # Find table header
    table_start = -1
    for i, line in enumerate(section_lines):
        if re.search(r'Field\s+Data\s*Type\s+Detail', line, re.I):
            table_start = i + 1
            break
    
    if table_start == -1:
        entities.append({"sectionNumber": section["num"], "name": entity_name, "fields": []})
        continue
    
    fields = []
    current = None
    
    for i in range(table_start, len(section_lines)):
        line = section_lines[i]
        trimmed = line.strip()
        
        # Skip noise
        if not trimmed:
            continue
        if re.match(r'^\d+$', trimmed):
            continue
        if "©2024" in trimmed or "All Rights Reserved" in trimmed:
            continue
        if trimmed == "TronsHealth":
            continue
        
        # Try full row: FieldName   datatype   Description
        row_match = re.match(
            r'^\s{0,2}(\S+(?:\s\S+)?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s{2,}(.+)',
            line, re.I
        )
        if row_match:
            if current:
                fields.append({"name": current["name"], "dataType": current["type"], "description": " ".join(current["desc"]).strip()})
            current = {
                "name": re.sub(r'\s+', '', row_match.group(1)),
                "type": row_match.group(2).lower(),
                "desc": [row_match.group(3).strip()]
            }
            continue
        
        # Field + type only (no description on this line)
        ft_match = re.match(
            r'^\s{0,2}(\S+(?:\s\S+)?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s*$',
            line, re.I
        )
        if ft_match:
            if current:
                fields.append({"name": current["name"], "dataType": current["type"], "description": " ".join(current["desc"]).strip()})
            current = {
                "name": re.sub(r'\s+', '', ft_match.group(1)),
                "type": ft_match.group(2).lower(),
                "desc": []
            }
            continue
        
        # Multi-word field name with type and description
        mw_match = re.match(
            r'^\s{0,2}(.+?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s{2,}(.+)',
            line, re.I
        )
        if mw_match:
            if current:
                fields.append({"name": current["name"], "dataType": current["type"], "description": " ".join(current["desc"]).strip()})
            current = {
                "name": mw_match.group(1).strip(),
                "type": mw_match.group(2).lower(),
                "desc": [mw_match.group(3).strip()]
            }
            continue
        
        # Multi-word field + type only
        mwt_match = re.match(
            r'^\s{0,2}(.+?)\s{2,}(long|varchar|nvarchar|int|boolean|bool|datetime|decimal|string|list)\s*$',
            line, re.I
        )
        if mwt_match:
            if current:
                fields.append({"name": current["name"], "dataType": current["type"], "description": " ".join(current["desc"]).strip()})
            current = {
                "name": mwt_match.group(1).strip(),
                "type": mwt_match.group(2).lower(),
                "desc": []
            }
            continue
        
        # Description continuation
        if current and trimmed:
            leading = len(line) - len(line.lstrip())
            if leading >= 10 or re.match(r'^[a-z(]', trimmed):
                current["desc"].append(trimmed)
    
    if current:
        fields.append({"name": current["name"], "dataType": current["type"], "description": " ".join(current["desc"]).strip()})
    
    entities.append({"sectionNumber": section["num"], "name": entity_name, "fields": fields})

# Clean up 'f' ligature artifacts from PDF
def clean_ligatures(s):
    return s.replace("f ", "f").replace("  ", " ") if "f " in s else s

for entity in entities:
    for field in entity["fields"]:
        field["name"] = clean_ligatures(field["name"])
        field["description"] = clean_ligatures(field["description"])

# Identify missing sections
found_nums = {e["sectionNumber"] for e in entities}
missing = [s for s in toc_sections if s["number"] not in found_nums]

# Build full inventory
full_inventory = {
    "vendor": "TronsHealth LLC",
    "product": "TronsHealth",
    "version": "1.0",
    "documentDate": "2024-09-11",
    "exportFormat": "CSV files in ZIP archive",
    "sourceFile": "170.315b10-Electronic-Health-Information-Export-EHI.pdf",
    "sourcePages": 27,
    "tocSections": toc_sections,
    "missingSections": missing,
    "entities": entities
}

# Write full inventory
with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Build summary
total_fields = sum(len(e["fields"]) for e in entities)
fields_with_desc = sum(1 for e in entities for fld in e["fields"] if fld["description"])
fields_with_types = sum(1 for e in entities for fld in e["fields"] if fld["dataType"])

type_counts = {}
for e in entities:
    for fld in e["fields"]:
        t = fld["dataType"]
        type_counts[t] = type_counts.get(t, 0) + 1

summary = {
    "totalEntities": len(entities),
    "totalTocSections": len(toc_sections),
    "missingSectionCount": len(missing),
    "missingSections": [s["name"] for s in missing],
    "totalFields": total_fields,
    "fieldsWithDescriptions": fields_with_desc,
    "fieldsWithTypes": fields_with_types,
    "descriptionCoverage": f"{fields_with_desc/total_fields*100:.1f}%" if total_fields else "N/A",
    "dataTypeCounts": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
    "entitySummary": [
        {
            "sectionNumber": e["sectionNumber"],
            "name": e["name"],
            "fieldCount": len(e["fields"]),
            "fieldsWithDescription": sum(1 for f in e["fields"] if f["description"]),
        }
        for e in entities
    ]
}

with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Entities found: {len(entities)} (TOC lists {len(toc_sections)})")
print(f"Missing sections: {len(missing)} - {[s['name'] for s in missing]}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({fields_with_desc/total_fields*100:.1f}%)")
print(f"Fields with types: {fields_with_types}")
print()
for e in entities:
    desc_count = sum(1 for f in e["fields"] if f["description"])
    print(f"  {e['sectionNumber']} {e['name']}: {len(e['fields'])} fields ({desc_count} described)")
