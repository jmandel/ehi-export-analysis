#!/usr/bin/env python3
"""
Parse the PrognoCIS EHI Export PDF text into a structured data dictionary.

Input:  ../downloads/b-10-EHI-Export_PrognoCIS-Support.txt
Output: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_PATH = os.path.join(SCRIPT_DIR, "..", "downloads", "b-10-EHI-Export_PrognoCIS-Support.txt")

with open(TXT_PATH, "r") as f:
    raw = f.read()

# Clean up headers/footers/page numbers
cleaned = raw
cleaned = cleaned.replace("\f", "")
cleaned = re.sub(r"2429 Military Suite 300.*?Phone \(Support\):.*?\d+", "", cleaned, flags=re.DOTALL)
cleaned = re.sub(r"§170\.315\(b\)\(10\) Electronic Health Information export_Self Attestation Document", "", cleaned)
cleaned = re.sub(r"\n\d{1,2}\n", "\n", cleaned)
cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
cleaned = cleaned.replace("\u201c", '"').replace("\u201d", '"')

# 47 known sections
SECTIONS = [
    (1, "Insurance Master", "Reference/Provider Data"),
    (2, "Medics", "Reference/Provider Data"),
    (3, "Referring Doctor", "Reference/Provider Data"),
    (4, "Adjusters", "Reference/Provider Data"),
    (5, "Attorneys", "Reference/Provider Data"),
    (6, "Employers", "Reference/Provider Data"),
    (7, "Guarantor", "Reference/Provider Data"),
    (8, "Patient Demographics", "Patient Clinical Data"),
    (9, "Patient Insurance", "Patient Clinical Data"),
    (10, "Vaccination", "Patient Clinical Data"),
    (11, "Health Maintenance", "Patient Clinical Data"),
    (12, "Family History", "Patient Clinical Data"),
    (13, "Past Medical Hist", "Patient Clinical Data"),
    (14, "Surgery", "Patient Clinical Data"),
    (15, "Allergy", "Patient Clinical Data"),
    (16, "Current Medication", "Patient Clinical Data"),
    (17, "Social History", "Patient Clinical Data"),
    (18, "Legal Documents", "Patient Clinical Data"),
    (19, "Other Documents", "Patient Clinical Data"),
    (20, "Enc Attach Docs", "Patient Clinical Data"),
    (21, "Old Progress Notes", "Patient Clinical Data"),
    (22, "Messages", "Patient Clinical Data"),
    (23, "Future Appointments", "Patient Clinical Data"),
    (24, "Vitals", "Patient Clinical Data"),
    (25, "Diagnosis Code", "Patient Clinical Data"),
    (26, "CPT Codes", "Patient Clinical Data"),
    (27, "HCPC Codes", "Patient Clinical Data"),
    (28, "CCD", "Patient Clinical Data"),
    (29, "Prescriptions", "Patient Clinical Data"),
    (30, "Lab Results", "Patient Clinical Data"),
    (31, "Rad Results", "Patient Clinical Data"),
    (32, "Procedure Orders", "Patient Clinical Data"),
    (33, "Consults", "Patient Clinical Data"),
    (34, "Enc Progress Notes", "Patient Clinical Data"),
    (35, "Procedure Notes", "Patient Clinical Data"),
    (36, "Letters", "Patient Clinical Data"),
    (37, "All Vitals", "Patient Clinical Data"),
    (38, "Lab Test Result Values", "Patient Clinical Data"),
    (39, "Patient Cases", "Patient Administrative/Case Data"),
    (40, "Patient Notes", "Patient Administrative/Case Data"),
    (41, "Patient Alert", "Patient Administrative/Case Data"),
    (42, "Past Appointments", "Patient Administrative/Case Data"),
    (43, "Billing Ledger", "Billing Data"),
    (44, "Billing Claims", "Billing Data"),
    (45, "Billing Charges", "Billing Data"),
    (46, "Patient Advance", "Billing Data"),
    (47, "Statements", "Billing Data"),
]

# Find the detailed description section
detail_start = cleaned.find("Detailed Description of the Data Export Contents")
if detail_start == -1:
    raise ValueError("Could not find detailed description section")

detailed = cleaned[detail_start:]

# Locate each section
section_positions = []
for num, name, cat in SECTIONS:
    escaped = re.escape(name)
    pattern = re.compile(rf"(?:^|\n){num}\.\s+{escaped}", re.MULTILINE)
    m = pattern.search(detailed)
    if m:
        section_positions.append((num, name, cat, m.start()))
    else:
        print(f"WARNING: Section {num}. {name} not found")

section_positions.sort(key=lambda x: x[3])

entities = []

for i, (num, name, cat, pos) in enumerate(section_positions):
    next_pos = section_positions[i + 1][3] if i + 1 < len(section_positions) else len(detailed)
    
    # Get section body (skip header line)
    header_pattern = re.compile(rf"{num}\.\s+{re.escape(name)}")
    hm = header_pattern.search(detailed[pos:])
    header_len = len(hm.group()) if hm else len(name) + 4
    body = detailed[pos + header_len:next_pos].strip()
    
    # Extract fields
    fields = []
    field_list_match = re.search(r'Exported field list is[\s\S]{0,50}?"([\s\S]*?)"', body)
    if field_list_match:
        raw_fields = field_list_match.group(1).replace("\n", " ")
        fields = [f.strip() for f in raw_fields.split(",") if f.strip()]
    else:
        # Try without quotes
        no_quote = re.search(r'Exported field list is[\s\-\u2013:]+([A-Z][^"]*?)(?:\n\n|\n\d+\.|$)', body, re.DOTALL)
        if no_quote:
            raw_fields = no_quote.group(1).replace("\n", " ")
            fields = [f.strip() for f in raw_fields.split(",") if f.strip()]
    
    # Has file column (document attachments)
    has_file_column = 'column labeled "File"' in body or "CHART01/" in body
    
    # Extract description
    desc = body
    exp_idx = body.find("Exported field list")
    if exp_idx > 0:
        desc = body[:exp_idx].strip()
    file_col_idx = desc.find("It contains a specific column")
    if file_col_idx > 0:
        desc = desc[:file_col_idx].strip()
    mul_idx = desc.find("Multiple attachments")
    if mul_idx > 0:
        desc = desc[:mul_idx].strip()
    
    # Clean description
    desc = re.sub(r"\n", " ", desc)
    desc = re.sub(r"\s{2,}", " ", desc).strip()
    
    # Extract notes
    notes = []
    for pat in [
        r"Only .+? are exported\.?",
        r"Please note .+",
        r"We (?:only|do not) .+",
        r"Void (?:claims|Charges) (?:will )?not be exported\.?",
    ]:
        for m in re.finditer(pat, body):
            notes.append(m.group().strip())
    
    # Build field objects
    field_objects = []
    for f in fields:
        field_objects.append({
            "name": f,
            "type": None,
            "description": None,
            "nullable": None,
        })
    
    # For document-only sections, note the file export
    export_type = "structured_data"
    if has_file_column and len(fields) == 0:
        export_type = "document_files_only"
    elif has_file_column:
        export_type = "structured_data_with_documents"
    
    # Special cases
    if name == "CCD":
        export_type = "ccd_export"
        desc = "Contains the CCD (Continuity of Care Document) details. Exports HTML and XML (C-CDA) files."
    elif name == "Billing Ledger":
        export_type = "report_export"
        desc = "Exports the Ledger for Run Date. Ledger will be exported for billed claims only. Does not export claim-wise ledger."
    elif name == "Statements":
        export_type = "document_files_only"
        desc = "Exports the latest patient statement as PDF. Only the most recent statement date is exported."
    
    entities.append({
        "number": num,
        "name": name,
        "category": cat,
        "description": desc,
        "export_type": export_type,
        "field_count": len(field_objects),
        "has_file_attachments": has_file_column,
        "fields": field_objects,
        "notes": notes,
    })

# Build full inventory
full_inventory = {
    "source_file": "b-10-EHI-Export_PrognoCIS-Support.pdf",
    "product": "PrognoCIS",
    "version": "Denali 3.1",
    "document_date": "2023-12-01",
    "pages": 26,
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities_with_fields": sum(1 for e in entities if e["field_count"] > 0),
    "entities_document_only": sum(1 for e in entities if e["export_type"] in ("document_files_only", "ccd_export", "report_export")),
    "fields_with_descriptions": 0,  # No field has descriptions in source
    "fields_with_types": 0,  # No field has types in source
    "entities": entities,
}

# Build summary
category_summary = {}
for e in entities:
    cat = e["category"]
    if cat not in category_summary:
        category_summary[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
    category_summary[cat]["entity_count"] += 1
    category_summary[cat]["field_count"] += e["field_count"]
    category_summary[cat]["entities"].append(e["name"])

# Top entities by field count
top_entities = sorted(entities, key=lambda e: e["field_count"], reverse=True)[:15]

summary = {
    "source_file": "b-10-EHI-Export_PrognoCIS-Support.pdf",
    "product": "PrognoCIS",
    "version": "Denali 3.1",
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities_with_fields": sum(1 for e in entities if e["field_count"] > 0),
    "entities_document_only": sum(1 for e in entities if e["export_type"] in ("document_files_only", "ccd_export", "report_export")),
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "categories": category_summary,
    "top_entities_by_field_count": [
        {"name": e["name"], "category": e["category"], "field_count": e["field_count"]}
        for e in top_entities
    ],
}

# Save outputs
full_path = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
summary_path = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")

with open(full_path, "w") as f:
    json.dump(full_inventory, f, indent=2)

with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total entities: {len(entities)}")
print(f"Total fields: {sum(e['field_count'] for e in entities)}")
print(f"Entities with field lists: {sum(1 for e in entities if e['field_count'] > 0)}")
print(f"Document-only entities: {sum(1 for e in entities if e['export_type'] in ('document_files_only', 'ccd_export', 'report_export'))}")
print()
print("By category:")
for cat, info in category_summary.items():
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
print()
print("Top 15 by field count:")
for e in top_entities:
    print(f"  {e['name']:30s}  {e['field_count']:4d} fields  ({e['category']})")
print()
print(f"Output: {full_path}")
print(f"Output: {summary_path}")
