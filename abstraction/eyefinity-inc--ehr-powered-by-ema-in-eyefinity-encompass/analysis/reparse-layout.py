#!/usr/bin/env python3
"""
Re-parse the PDF layout text directly to build an accurate entity inventory.
Corrects parser bugs from the original enrichment script.

Input: results/downloads/Data-Dictionary-layout.txt
Output: full-entity-inventory.json (corrected), summary-stats.json (corrected)
"""

import json
import os
import re

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 
    "../../../results/eyefinity-inc--ehr-powered-by-ema-in-eyefinity-encompass")
ANALYSIS_DIR = os.path.dirname(__file__)

layout_path = os.path.join(RESULTS_DIR, "downloads/Data-Dictionary-layout.txt")
with open(layout_path, "r") as f:
    lines = f.readlines()

VALID_GROUPINGS = {
    "Practice", "Patient", "PM Financials", "Ophth Pretesting", "eLab",
    "Visit", "Appointment", "Diagnosis", "Pathology", "Office Flow",
    "Document Management", "Prescription", "CC/HPI", "Inventory", "Exam",
    "Procedure", "Document", "Ophth"
}

# Page artifacts to skip
def is_page_artifact(line):
    stripped = line.strip()
    if not stripped:
        return True
    if re.match(r'^\d+$', stripped):  # page number
        return True
    if re.match(r'^\d+/\d+$', stripped):  # date like 11/2023
        return True
    if stripped.startswith("Grouping") and "Table" in stripped and "Description" in stripped:
        return True
    if stripped == "Tracking":
        return True
    if stripped == "Longitudinal":
        return True
    return False

# State machine parser
tables = []
current_table = None
in_data_section = False

# Find where "Database Tables & Columns:" starts
start_idx = 0
for i, line in enumerate(lines):
    if "Database Tables & Columns:" in line:
        start_idx = i + 1
        break

# Parse the layout text line by line
i = start_idx
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    if is_page_artifact(line):
        i += 1
        continue
    
    # Try to detect a new table entry: starts with grouping name at left margin
    # Format: "Grouping   table_name   Description text   first_column_name   tracking_flag"
    # Or continuation rows: spaces then column_name
    
    # Check if this line starts a new table entry
    # A new table entry has a grouping name or table name at the start
    # Grouping names are left-aligned or start within first ~15 chars
    
    # Detect grouping + table start
    match = re.match(r'^(\w[\w/ ]*?)\s{2,}(\w[\w_]*)\s{2,}(.+)', line)
    if match:
        potential_grouping = match.group(1).strip()
        potential_table = match.group(2).strip()
        rest = match.group(3).strip()
        
        # Check if the "grouping" is actually a multi-word grouping
        full_grouping = None
        for g in ["Document Management", "PM Financials", "Ophth Pretesting", "Office Flow", 
                   "CC/HPI", "Practice", "Patient", "Visit", "Appointment", "Diagnosis",
                   "Pathology", "Prescription", "Inventory", "Exam", "Procedure", "eLab"]:
            if line.strip().startswith(g):
                full_grouping = g
                after_g = line.strip()[len(g):].strip()
                parts = re.split(r'\s{2,}', after_g, maxsplit=1)
                if parts:
                    potential_table = parts[0].strip()
                    rest = parts[1].strip() if len(parts) > 1 else ""
                break
        
        if full_grouping is None:
            # Single word grouping
            if potential_grouping in VALID_GROUPINGS:
                full_grouping = potential_grouping
        
        if full_grouping and re.match(r'^[a-z_]+$', potential_table):
            # This looks like a new table entry
            # Save current table
            if current_table:
                tables.append(current_table)
            
            # Parse columns from the rest of the line
            # The rest might contain: "Description text   column_name   tracking_flag"
            # Split by multiple spaces
            rest_parts = re.split(r'\s{2,}', rest)
            
            # The last part might be tracking flag (Y, N, L, S)
            tracking = ""
            if rest_parts and rest_parts[-1].strip() in ["Y", "N", "L", "S"]:
                tracking = rest_parts[-1].strip()
                rest_parts = rest_parts[:-1]
            
            # The first column name is typically the second-to-last element
            # Everything before it is description
            description = ""
            first_column = ""
            if rest_parts:
                # Last element is likely a column name (snake_case)
                last = rest_parts[-1].strip()
                if re.match(r'^[a-z_]+[a-z0-9_]*$', last) or re.match(r'^[a-z_]+[a-z0-9_]*_id$', last):
                    first_column = last
                    description = " ".join(p.strip() for p in rest_parts[:-1])
                else:
                    description = " ".join(p.strip() for p in rest_parts)
            
            columns = []
            if first_column:
                columns.append(first_column)
            
            current_table = {
                "grouping": full_grouping,
                "table_name": potential_table,
                "description": description,
                "columns": columns,
                "longitudinal_tracking": tracking
            }
            i += 1
            continue
    
    # Check for continuation line with just a column name
    if current_table and stripped:
        # Column names are right-aligned in the Columns column area
        # They are snake_case identifiers
        # Also check for tracking flag at end
        parts = stripped.split()
        
        # Could be just a column name
        if len(parts) == 1 and re.match(r'^[a-z_][a-z0-9_]*$', parts[0]):
            current_table["columns"].append(parts[0])
            i += 1
            continue
        
        # Could be column_name + tracking flag
        if len(parts) == 2 and re.match(r'^[a-z_][a-z0-9_]*$', parts[0]) and parts[1] in ["Y", "N", "L", "S"]:
            current_table["columns"].append(parts[0])
            if not current_table["longitudinal_tracking"]:
                current_table["longitudinal_tracking"] = parts[1]
            i += 1
            continue
        
        # Could be description continuation + column name
        # Check if the last word looks like a column name
        if parts and re.match(r'^[a-z_][a-z0-9_]*$', parts[-1]):
            potential_col = parts[-1]
            # Check if preceding text is description continuation
            desc_text = " ".join(parts[:-1])
            if any(c.isupper() or c == '(' or c == ')' or c == '.' or c == ',' for c in desc_text):
                current_table["description"] += " " + desc_text
                current_table["columns"].append(potential_col)
                i += 1
                continue
        
        # Plain description continuation (no column name)
        if not re.match(r'^[a-z_][a-z0-9_]*$', stripped):
            # Might have a column name embedded
            # Try splitting by position (columns are typically at position ~68+)
            if len(line) > 60:
                left = line[:60].strip()
                right = line[60:].strip()
                if right and re.match(r'^[a-z_][a-z0-9_]*$', right.split()[0] if right.split() else ""):
                    col = right.split()[0]
                    current_table["columns"].append(col)
                    if left:
                        current_table["description"] += " " + left
                    i += 1
                    continue
    
    i += 1

# Save last table
if current_table:
    tables.append(current_table)

# Filter out invalid entries
valid_tables = [t for t in tables if t["table_name"] != "excluded" 
                and not t["table_name"].startswith("Database")
                and t["table_name"] not in ["table"]]

# Clean descriptions
for t in valid_tables:
    t["description"] = re.sub(r'\s+', ' ', t["description"]).strip()
    # Deduplicate columns
    seen = set()
    unique_cols = []
    for c in t["columns"]:
        if c not in seen and c != t["table_name"]:  # remove self-referencing parse errors
            seen.add(c)
            unique_cols.append(c)
        elif c == t["table_name"] and c not in seen:
            seen.add(c)
            # Only keep if it's clearly a column name (like table_name_id pattern)
    t["columns"] = unique_cols

print(f"Parsed {len(valid_tables)} tables from layout text")
total_cols = sum(len(t["columns"]) for t in valid_tables)
print(f"Total columns: {total_cols}")

# Compare with enrichment parse
with open(os.path.join(RESULTS_DIR, "downloads/enrichment/data-dictionary.json")) as f:
    enrichment = json.load(f)

enrichment_map = {t["table_name"]: len(t.get("columns", [])) for t in enrichment if t["table_name"] != "excluded"}

print("\nDifferences from enrichment parse:")
for t in valid_tables:
    enr_count = enrichment_map.get(t["table_name"], -1)
    my_count = len(t["columns"])
    if enr_count != my_count and enr_count >= 0:
        print(f"  {t['table_name']}: enrichment={enr_count}, reparse={my_count}")
    elif enr_count < 0:
        print(f"  {t['table_name']}: NOT in enrichment, reparse={my_count}")

# Check for tables in enrichment but not in reparse
my_names = {t["table_name"] for t in valid_tables}
for name, count in enrichment_map.items():
    if name not in my_names:
        print(f"  {name}: in enrichment ({count} cols) but NOT in reparse")
