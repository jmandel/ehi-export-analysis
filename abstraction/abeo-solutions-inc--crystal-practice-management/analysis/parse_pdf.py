#!/usr/bin/env python3
"""Parse the Crystal PM EHI export data dictionary PDF (extracted text) to produce
a structured inventory of all tables, fields, descriptions, and categories."""

import re
import json
from collections import defaultdict

TEXT_FILE = "full-text.txt"

with open(TEXT_FILE) as f:
    lines = f.readlines()

# Find all section headers matching: SomeName - "table_name" CSV Export
header_re = re.compile(r'^(.+?)\s*-\s*"(\w+)"\s+CSV Export\s*$')

sections = []
for i, line in enumerate(lines):
    m = header_re.match(line.strip())
    if m:
        sections.append({
            "line": i,
            "display_name": m.group(1).strip(),
            "table_name": m.group(2).strip(),
        })

# Parse fields for each section
# Fields appear in table format: Column Name | Data Type | Description | Extraction Method
# We look for lines that have a column name followed by a data type keyword

field_start_re = re.compile(
    r'^(\w[\w\.]*)\s+'
    r'(int|varchar|char|date|datetime|bigint|longblob|tinyint|text|time|mediumblob|blob|smallint|float|double|decimal|bit|enum|longtext|mediumtext|varbinary)\b',
    re.IGNORECASE
)

# Also detect the "Column Name" header row to know we're in a field table
header_row_re = re.compile(r'Column Name\s+Data\s+Description\s+Extraction')

for idx, sec in enumerate(sections):
    start = sec["line"]
    end = sections[idx + 1]["line"] if idx + 1 < len(sections) else len(lines)
    
    fields = []
    current_field = None
    in_table = False
    
    for j in range(start, end):
        line = lines[j]
        stripped = line.strip()
        
        # Detect header row
        if header_row_re.search(stripped):
            in_table = True
            continue
        
        if not in_table and j > start + 5:
            # Maybe the table starts without explicit header row — look for field pattern
            pass
        
        m = field_start_re.match(stripped)
        if m:
            if current_field:
                fields.append(current_field)
            col_name = m.group(1)
            data_type = m.group(2)
            # Try to extract description from remainder of line
            remainder = stripped[m.end():].strip()
            # Extract extraction method from end if present
            extraction = ""
            for method in ["CSV + Binary Deserialization", "CSV + XML Deserialization", 
                          "CSV + Binary", "CSV + XML", "CSV"]:
                if remainder.endswith(method):
                    extraction = method
                    remainder = remainder[:-len(method)].strip()
                    break
            current_field = {
                "name": col_name,
                "type": data_type,
                "description": remainder,
                "extraction": extraction,
            }
            in_table = True
        elif current_field and stripped and not header_row_re.search(stripped):
            # Continuation of description
            # Check if this line ends with an extraction method
            for method in ["CSV + Binary Deserialization", "CSV + XML Deserialization",
                          "CSV + Binary", "CSV + XML", "CSV"]:
                if stripped.endswith(method):
                    stripped = stripped[:-len(method)].strip()
                    if not current_field["extraction"]:
                        current_field["extraction"] = method
                    break
            if stripped and not stripped.startswith("Column Name"):
                current_field["description"] += " " + stripped
    
    if current_field:
        fields.append(current_field)
    
    sec["fields"] = fields
    sec["field_count"] = len(fields)

# Categorize tables
def categorize(display_name, table_name):
    tn = table_name.lower()
    dn = display_name.lower()
    
    if tn == "patients":
        return "Patient Demographics"
    if tn in ("recall", "reminders", "rem_log", "directmail_message", "pat_markets", "comments", "kno2_message"):
        return "Patient Engagement & Communication"
    if tn in ("alerts",):
        return "Administrative"
    if tn in ("hippadisc", "authlogs", "mu_measures"):
        return "Administrative & Compliance"
    if tn.startswith("mcrx") or tn.startswith("mcs"):
        return "Prescriptions & Medication"
    if tn in ("invoice", "inv_trans_items", "trans_pay", "trans_data", "hcfa_print", "hcfa_data", "rslip"):
        return "Billing & Financial"
    if tn.startswith("vsp_") or tn == "frame_for_vsp":
        return "Insurance (VSP)"
    if tn in ("framepage", "fp_log", "cl_log", "contorders", "inv_log", "clrx_notes", "sprx_notes"):
        return "Optical & Inventory"
    if tn in ("appts", "appt_waitlist", "appt_log"):
        return "Scheduling & Appointments"
    if tn.startswith("pat_photo") or tn.startswith("pat_file") or tn.startswith("med_image") or tn.startswith("pat_ins_card") or tn.startswith("ins_card"):
        return "Documents & Images"
    if tn == "ehr_file":
        return "Clinical / EHR"
    if tn == "clinical_note":
        return "Clinical / EHR"
    if tn in ("order_groups", "result_groups"):
        return "Clinical / EHR"
    if tn == "pro_refrl":
        return "Referrals"
    if tn == "hl7_record":
        return "Interoperability"
    return "Other"

for sec in sections:
    sec["category"] = categorize(sec["display_name"], sec["table_name"])

# Build summary
total_sections = len(sections)
distinct_tables = set(s["table_name"] for s in sections)
total_fields = sum(s["field_count"] for s in sections)
fields_with_desc = sum(1 for s in sections for f in s["fields"] if f["description"].strip())

# Category breakdown
cat_stats = defaultdict(lambda: {"sections": 0, "fields": 0, "tables": set()})
for s in sections:
    cat = s["category"]
    cat_stats[cat]["sections"] += 1
    cat_stats[cat]["fields"] += s["field_count"]
    cat_stats[cat]["tables"].add(s["table_name"])

# Print summary
print("=" * 70)
print("CRYSTAL PM EHI EXPORT DATA DICTIONARY ANALYSIS")
print("=" * 70)
print(f"Total export sections:     {total_sections}")
print(f"Distinct database tables:  {len(distinct_tables)}")
print(f"Total fields documented:   {total_fields}")
print(f"Fields with descriptions:  {fields_with_desc} ({100*fields_with_desc/total_fields:.1f}%)")
print()

print("CATEGORY BREAKDOWN:")
print("-" * 70)
print(f"{'Category':<40} {'Sections':>8} {'Tables':>8} {'Fields':>8}")
print("-" * 70)
for cat in sorted(cat_stats.keys()):
    stats = cat_stats[cat]
    print(f"{cat:<40} {stats['sections']:>8} {len(stats['tables']):>8} {stats['fields']:>8}")
print("-" * 70)
print(f"{'TOTAL':<40} {total_sections:>8} {len(distinct_tables):>8} {total_fields:>8}")
print()

print("ALL SECTIONS (sorted by category, then table name):")
print("-" * 90)
print(f"{'Display Name':<35} {'Table':<25} {'Fields':>6} {'Category':<25}")
print("-" * 90)
for s in sorted(sections, key=lambda x: (x["category"], x["table_name"], x["display_name"])):
    print(f"{s['display_name']:<35} {s['table_name']:<25} {s['field_count']:>6} {s['category']:<25}")

print()
print("DISTINCT DATABASE TABLES:")
for t in sorted(distinct_tables):
    print(f"  - {t}")

# Save full inventory as JSON
inventory = []
for s in sections:
    inventory.append({
        "display_name": s["display_name"],
        "table_name": s["table_name"],
        "category": s["category"],
        "field_count": s["field_count"],
        "fields": [{
            "name": f["name"],
            "type": f["type"],
            "description": f["description"].strip(),
            "extraction": f["extraction"],
            "has_description": bool(f["description"].strip())
        } for f in s["fields"]]
    })

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Save category summary
cat_summary = {}
for cat in sorted(cat_stats.keys()):
    stats = cat_stats[cat]
    cat_summary[cat] = {
        "sections": stats["sections"],
        "distinct_tables": len(stats["tables"]),
        "tables": sorted(stats["tables"]),
        "total_fields": stats["fields"],
    }

with open("category-summary.json", "w") as f:
    json.dump(cat_summary, f, indent=2)

print(f"\nSaved full-entity-inventory.json and category-summary.json")
