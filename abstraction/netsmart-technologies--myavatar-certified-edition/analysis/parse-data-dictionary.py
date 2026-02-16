#!/usr/bin/env python3
"""
Parses the pdftotext output of the myAvatar EHI data dictionary PDF
into entity-inventory-full.json and entity-inventory-summary.json.

Input: ../downloads/ehi-export-all-tables.txt
Output: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import re
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "downloads", "ehi-export-all-tables.txt")
FULL_OUTPUT = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
SUMMARY_OUTPUT = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")

with open(INPUT_PATH, "r") as f:
    raw = f.read()

lines = raw.split("\n")

# Parse into structured data
tables = []  # list of {form_name, table_name, schema, short_name, description, columns: [{name, type, max_length, description}]}
glossary_entries = []

current_form = None
current_table = None
current_table_desc = None
current_table_desc_lines = []
current_columns = []
current_column = None  # {name, type, max_length}
desc_lines = []
in_toc = True
in_glossary = False
past_glossary = False

def flush_column():
    global current_column, desc_lines
    if current_column and current_column.get("name") and current_column.get("type"):
        desc = " ".join(desc_lines).strip() or None
        current_columns.append({
            "name": current_column["name"],
            "type": current_column["type"],
            "max_length": current_column.get("max_length"),
            "description": desc,
        })
    current_column = None
    desc_lines = []

def flush_table():
    global current_table, current_table_desc, current_table_desc_lines, current_columns
    flush_column()
    if current_table:
        parts = current_table.split(".", 1)
        schema = parts[0] if len(parts) > 1 else ""
        short_name = parts[1] if len(parts) > 1 else current_table
        
        # Build table description from accumulated lines
        if current_table_desc_lines:
            table_desc = " ".join(current_table_desc_lines).strip()
        else:
            table_desc = current_table_desc
            
        tables.append({
            "form_name": current_form or "",
            "table_name": current_table,
            "schema": schema,
            "table_short_name": short_name,
            "table_description": table_desc,
            "columns": current_columns,
        })
    current_table = None
    current_table_desc = None
    current_table_desc_lines = []
    current_columns = []

for i, line in enumerate(lines):
    trimmed = line.strip()
    
    # Skip blank lines and page numbers
    if trimmed == "" or re.match(r"^\d+$", trimmed):
        continue
    
    # Skip TOC lines
    if ".........." in trimmed:
        continue
    
    # Detect end of TOC
    if in_toc:
        if trimmed == "Overview":
            in_toc = False
            in_glossary = True
        continue
    
    # Skip header lines that appear on each page
    if trimmed.startswith("EHI Export: myAvatar"):
        continue
    if trimmed.startswith("Last Updated:"):
        continue
    if trimmed == "Table of Contents":
        continue
    
    # Form header marks end of glossary
    if trimmed.startswith("Documentation for form:"):
        if in_glossary:
            in_glossary = False
            past_glossary = True
        flush_table()
        current_form = trimmed.replace("Documentation for form:", "").strip()
        continue
    
    # In glossary section, skip
    if in_glossary and not past_glossary:
        continue
    
    # Table name
    if trimmed.startswith("Table Name:"):
        if current_table:
            flush_table()
        current_table = trimmed.replace("Table Name:", "").strip()
        current_table_desc_lines = []
        continue
    
    # Table description
    if trimmed.startswith("Table Description:"):
        desc_text = trimmed.replace("Table Description:", "").strip()
        current_table_desc = desc_text
        current_table_desc_lines = [desc_text] if desc_text else []
        continue
    
    # Separator line
    if trimmed == "-------------":
        continue
    
    # Column name
    if trimmed.startswith("Column Name:"):
        flush_column()
        current_column = {"name": trimmed.replace("Column Name:", "").strip()}
        continue
    
    # Column type
    if trimmed.startswith("Column Type:") and current_column is not None:
        current_column["type"] = trimmed.replace("Column Type:", "").strip()
        continue
    
    # Max length
    if trimmed.startswith("Max Length:") and current_column is not None:
        val = trimmed.replace("Max Length:", "").strip()
        try:
            current_column["max_length"] = int(val)
        except ValueError:
            current_column["max_length"] = None
        continue
    
    # If we're in a column and have the type, remaining text is description
    if current_column is not None and "type" in current_column:
        desc_lines.append(trimmed)
        continue
    
    # Continuation of table description (between Table Description and first Column Name)
    if current_table and current_column is None and current_table_desc is not None:
        current_table_desc_lines.append(trimmed)
        continue

# Flush final table
flush_table()

# Deduplicate: same table may appear under multiple forms
# We keep all entries (form-table pairs) for completeness
# but also build a unique table view

# Build unique tables with merged columns (take the union of columns across forms)
unique_tables = {}
for entry in tables:
    tname = entry["table_name"]
    if tname not in unique_tables:
        unique_tables[tname] = {
            "table_name": tname,
            "schema": entry["schema"],
            "table_short_name": entry["table_short_name"],
            "table_description": entry["table_description"],
            "forms": [entry["form_name"]],
            "columns": {c["name"]: c for c in entry["columns"]},
        }
    else:
        if entry["form_name"] and entry["form_name"] not in unique_tables[tname]["forms"]:
            unique_tables[tname]["forms"].append(entry["form_name"])
        # Merge columns: keep existing, add new
        for c in entry["columns"]:
            if c["name"] not in unique_tables[tname]["columns"]:
                unique_tables[tname]["columns"][c["name"]] = c
            else:
                # If existing has no description but new one does, prefer new
                existing = unique_tables[tname]["columns"][c["name"]]
                if not existing.get("description") and c.get("description"):
                    unique_tables[tname]["columns"][c["name"]] = c

# Convert to list form for output
full_inventory = []
for tname in sorted(unique_tables.keys()):
    t = unique_tables[tname]
    cols = list(t["columns"].values())
    full_inventory.append({
        "table_name": t["table_name"],
        "schema": t["schema"],
        "table_short_name": t["table_short_name"],
        "table_description": t["table_description"],
        "forms": t["forms"],
        "column_count": len(cols),
        "columns": cols,
    })

# Categorize tables
def categorize(table_name, forms):
    t = table_name.lower()
    f = " ".join(forms).lower()
    combined = t + " " + f
    categories = []
    
    if re.search(r"billing|claim|charge|payment|remit|financial|ledger|cash|fee|835|837|276|277|834|selfpay|payor|invoice|retro_payor", combined):
        categories.append("Billing & Financial")
    if re.search(r"note|progress|document|clinical_rec|cw_patient|scratch|cosign|significant_finding|service_doc", combined):
        categories.append("Clinical Notes & Documents")
    if re.search(r"med_order|drug|pharm|rx|prescri|emar|methadone|ncpdp|medication|med_d", combined):
        categories.append("Medications & Pharmacy")
    if re.search(r"client|patient|demo|enroll|admit|discharg|episode|patid|outreach|merge|purge|pre_admit|current_demo", combined):
        categories.append("Demographics & Patient")
    if re.search(r"appoint|schedul|waiting|check_in|check_out|telehealth|front_desk|appt|calendar", combined):
        categories.append("Scheduling & Appointments")
    if re.search(r"diag|problem|condition", combined):
        categories.append("Diagnoses")
    if re.search(r"order|lab|result|specimen|poc_result", combined):
        categories.append("Labs & Orders")
    if re.search(r"treat|tx_plan|care_path|goal|pathway|recovery|discharge_sum", combined):
        categories.append("Treatment & Care Plans")
    if re.search(r"vital|observation|height_weight", combined):
        categories.append("Vitals & Observations")
    if re.search(r"allerg|hypersens", combined):
        categories.append("Allergies")
    if re.search(r"immun|vaccine", combined):
        categories.append("Immunizations")
    if re.search(r"consent|disclos|privacy|rad.*consent", combined):
        categories.append("Consent & Disclosure")
    if re.search(r"seclus|restrain|incident|leave|acuit|detox", combined):
        categories.append("Behavioral Health Specific")
    if re.search(r"stateform|florida|georgia|ohio|michigan|kansas|indiana|louisiana|wams|cimor|bhhf|ca_dcr|nys_pas|fsr|aso", combined):
        categories.append("State-Specific Reporting")
    if re.search(r"service_auth|fund_auth|member_auth|prov_auth|mso_service|authorization", combined):
        categories.append("Service Authorization")
    if re.search(r"family|women|health_maint|amput|implant|surgical|hospital|preg|delivery", combined):
        categories.append("Health History")
    if re.search(r"bed|room|movement|census", combined):
        categories.append("Bed Management")
    if re.search(r"referral|transfer|carefabric", combined):
        categories.append("Referral & Transfer")
    if re.search(r"staff|provider|team|nursing", combined):
        categories.append("Staff & Provider")
    if re.search(r"ccd|hl7|fhir|interop", combined):
        categories.append("Interoperability")
    
    if not categories:
        categories.append("Other")
    return categories

# Add categories to each table
for item in full_inventory:
    item["categories"] = categorize(item["table_name"], item["forms"])

# Compute statistics
total_tables = len(full_inventory)
total_columns = sum(t["column_count"] for t in full_inventory)
columns_with_desc = sum(
    1 for t in full_inventory for c in t["columns"] if c.get("description")
)
columns_with_max_length = sum(
    1 for t in full_inventory for c in t["columns"] if c.get("max_length") is not None
)

# Schema breakdown
schema_counts = defaultdict(lambda: {"tables": 0, "columns": 0})
for t in full_inventory:
    s = t["schema"] or "(none)"
    schema_counts[s]["tables"] += 1
    schema_counts[s]["columns"] += t["column_count"]

# Category breakdown
category_counts = defaultdict(lambda: {"tables": 0, "columns": 0, "sample_tables": []})
for t in full_inventory:
    for cat in t["categories"]:
        category_counts[cat]["tables"] += 1
        category_counts[cat]["columns"] += t["column_count"]
        if len(category_counts[cat]["sample_tables"]) < 5:
            category_counts[cat]["sample_tables"].append(t["table_name"])

# Top 20 largest tables
largest_tables = sorted(full_inventory, key=lambda t: t["column_count"], reverse=True)[:20]

summary = {
    "source": "EHI Export All Tables - September 2023.pdf",
    "total_form_table_pairs": len(tables),
    "unique_tables": total_tables,
    "unique_forms": len(set(e["form_name"] for e in tables if e["form_name"])),
    "total_columns": total_columns,
    "columns_with_description": columns_with_desc,
    "columns_without_description": total_columns - columns_with_desc,
    "description_coverage_pct": round(columns_with_desc / total_columns * 100, 1) if total_columns else 0,
    "columns_with_max_length": columns_with_max_length,
    "schema_breakdown": {
        k: v for k, v in sorted(schema_counts.items(), key=lambda x: -x[1]["tables"])
    },
    "category_breakdown": {
        k: v for k, v in sorted(category_counts.items(), key=lambda x: -x[1]["tables"])
    },
    "largest_tables": [
        {"table_name": t["table_name"], "column_count": t["column_count"], "description": t["table_description"]}
        for t in largest_tables
    ],
}

with open(FULL_OUTPUT, "w") as f:
    json.dump(full_inventory, f, indent=2)

with open(SUMMARY_OUTPUT, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Parsed {len(tables)} form-table pairs → {total_tables} unique tables")
print(f"Total columns: {total_columns}")
print(f"Columns with descriptions: {columns_with_desc} ({summary['description_coverage_pct']}%)")
print(f"Columns with max_length: {columns_with_max_length}")
print(f"\nSchema breakdown:")
for s, v in sorted(schema_counts.items(), key=lambda x: -x[1]["tables"]):
    print(f"  {s}: {v['tables']} tables, {v['columns']} columns")
print(f"\nCategory breakdown:")
for cat, v in sorted(category_counts.items(), key=lambda x: -x[1]["tables"]):
    print(f"  {cat}: {v['tables']} tables, {v['columns']} columns")
print(f"\nTop 10 largest tables:")
for t in largest_tables[:10]:
    print(f"  {t['table_name']}: {t['column_count']} columns")
print(f"\nOutput: {FULL_OUTPUT}")
print(f"Summary: {SUMMARY_OUTPUT}")
