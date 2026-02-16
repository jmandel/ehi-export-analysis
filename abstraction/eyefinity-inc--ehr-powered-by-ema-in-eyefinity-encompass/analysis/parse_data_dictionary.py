#!/usr/bin/env python3
"""
Parse the ModMed EMA EHI Export Data Dictionary from pdftotext -layout output.
Cross-references with enrichment parse for completeness.

Output: entity-inventory-full.json, entity-inventory-summary.json
"""

import re
import json
from pathlib import Path

INPUT = Path(__file__).parent.parent / "downloads" / "Data-Dictionary-layout.txt"
ENRICHMENT = Path(__file__).parent.parent / "downloads" / "enrichment" / "data-dictionary.json"
OUTPUT_FULL = Path(__file__).parent / "entity-inventory-full.json"
OUTPUT_SUMMARY = Path(__file__).parent / "entity-inventory-summary.json"

lines = INPUT.read_text().split("\n")

KNOWN_GROUPINGS = {
    "Document Management", "Ophth Pretesting", "PM Financials",
    "Medical Lookup", "Office Flow", "Practice", "Patient", "eLab",
    "Pathology", "Prescription", "Appointment", "Visit", "CC/HPI",
    "Exam", "Diagnosis", "Procedure", "Lookup", "MIPS", "Inventory",
}

MULTI_WORD_PREFIXES = {
    "Document": "Document Management",
    "Ophth": "Ophth Pretesting",
    "PM": "PM Financials",
    "Medical": "Medical Lookup",
    "Office": "Office Flow",
}

SNAKE = re.compile(r'^[a-z][a-z0-9_]{2,}$')
PAGE_HEADER = re.compile(r'^Grouping\s+Table\s+Description\s+Columns\s+Longitudinal')
TRACKING_LINE = re.compile(r'^\s+Tracking\s*$')
PAGE_NUM = re.compile(r'^\s+\d{1,3}\s*$')
DATE_FOOTER = re.compile(r'^\s+\d{1,2}/\d{4}\s*$')

# Common short English words that leak from descriptions
FALSE_COL_NAMES = {
    'the', 'for', 'and', 'not', 'are', 'was', 'per', 'one', 'all', 'its',
    'hot', 'yet', 'row', 'son', 'eye', 'fin', 'dot', 'key', 'sig',
    'nce', 'of', 'or', 'in', 'if', 'as', 'to', 'by', 'on', 'up', 'be',
    'using', 'information', 'table', 'associated', 'entry',
    'excluded', 'transaction', 'that', 'with', 'from', 'this',
    'have', 'will', 'been', 'each', 'their', 'more', 'when', 'about',
    'which', 'than', 'into', 'other', 'only', 'also',
    'can', 'has', 'may', 'but', 'who', 'did', 'get', 'set', 'new', 'now',
    'way', 'see', 'use', 'two', 'how', 'our', 'out', 'his', 'her',
}

start_idx = 0
for i, line in enumerate(lines):
    if "Database Tables & Columns:" in line:
        start_idx = i + 1
        break

def is_artifact(line):
    s = line.strip()
    if not s:
        return True
    if PAGE_HEADER.match(s):
        return True
    if TRACKING_LINE.match(line):
        return True
    if PAGE_NUM.match(line):
        return True
    if DATE_FOOTER.match(line):
        return True
    return False

# Strategy: Use the enrichment parse (which got all 197 tables) as the table/grouping
# framework, but rebuild column lists from the layout text which has clear positional
# separation between description and column regions.

# First, build a map of all table entries from the layout text by detecting new-table lines
# A new table line has: grouping in col 0-10, table_name in col 12-35

enrichment = json.load(open(ENRICHMENT))
enrichment_map = {t["table_name"]: t for t in enrichment}

# Parse layout text to extract columns per table
# We'll identify table boundaries and then extract snake_case tokens from the column zone

table_entries = []  # (line_idx, grouping, table_name)
current_grouping = None

for i in range(start_idx, len(lines)):
    line = lines[i]
    if is_artifact(line):
        continue
    
    left = line[:12].strip() if len(line) >= 12 else line.strip()
    
    # Detect grouping
    found_grouping = None
    for g in KNOWN_GROUPINGS:
        if left == g:
            found_grouping = g
            break
    if not found_grouping and left in MULTI_WORD_PREFIXES:
        found_grouping = MULTI_WORD_PREFIXES[left]
    
    if found_grouping:
        current_grouping = found_grouping
        # Check for table name in the table region
        table_region = line[12:38].strip() if len(line) > 12 else ""
        if table_region:
            first_word = table_region.split()[0]
            if SNAKE.match(first_word):
                table_entries.append((i, current_grouping, first_word))

# Now for each table entry, collect all lines until the next table entry
# and extract column names from the right side of those lines

def extract_columns_from_block(block_lines):
    """Extract column names from lines, looking at positions >= 65."""
    columns = []
    for line in block_lines:
        # Look for snake_case tokens starting at position 65 or later
        # These are in the "Columns" zone of the PDF
        for m in re.finditer(r'\b([a-z][a-z0-9_]+)\b', line):
            if m.start() >= 65:
                token = m.group(1)
                if token not in FALSE_COL_NAMES:
                    columns.append(token)
        
        # Also check for lines that are entirely a single snake_case token
        # indented significantly (continuation column names)
        stripped = line.strip()
        if SNAKE.match(stripped) and stripped not in FALSE_COL_NAMES:
            leading = len(line) - len(line.lstrip())
            if leading >= 50 and stripped not in columns:
                columns.append(stripped)
    
    # Deduplicate preserving order
    seen = set()
    result = []
    for c in columns:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return result

def extract_description_from_block(block_lines, table_name):
    """Extract description text from the description zone (col ~36-84)."""
    desc_parts = []
    for line in block_lines:
        desc_zone = line[36:85].strip() if len(line) > 36 else ""
        if desc_zone:
            # Skip if it looks like it's just column names
            words = desc_zone.split()
            non_snake = [w for w in words if not SNAKE.match(w)]
            if non_snake:
                desc_parts.append(desc_zone)
        # Also check table_region for description overflow
        table_region = line[12:36].strip() if len(line) > 12 else ""
        if table_region and table_region != table_name:
            words = table_region.split()
            non_snake = [w for w in words if not SNAKE.match(w)]
            if non_snake:
                desc_parts.append(table_region)
    
    desc = " ".join(desc_parts).strip()
    return re.sub(r'\s+', ' ', desc)

# Build final tables from layout parse
layout_tables = []
for idx, (line_idx, grouping, table_name) in enumerate(table_entries):
    # Determine end of this table's block
    if idx + 1 < len(table_entries):
        next_line_idx = table_entries[idx + 1][0]
    else:
        next_line_idx = len(lines)
    
    block = [lines[j] for j in range(line_idx, next_line_idx) if not is_artifact(lines[j])]
    
    columns = extract_columns_from_block(block)
    description = extract_description_from_block(block, table_name)
    
    # Extract tracking flag
    tracking = ""
    for line in block:
        t_zone = line[130:].strip() if len(line) > 130 else ""
        if t_zone in ("Y", "N", "L", "S"):
            tracking = t_zone
            break
    
    layout_tables.append({
        "grouping": grouping,
        "table_name": table_name,
        "description": description,
        "columns": columns,
        "longitudinal_tracking": tracking,
    })

layout_map = {t["table_name"]: t for t in layout_tables}

# Merge: start with layout parse, add missing from enrichment
final_tables = []
seen_tables = set()

for t in layout_tables:
    seen_tables.add(t["table_name"])
    # If enrichment has more columns, it might have captured some that layout missed
    # But enrichment also has false positives. Trust layout for column names.
    # If layout has significantly fewer columns than enrichment, flag it.
    et = enrichment_map.get(t["table_name"])
    
    desc = t["description"]
    if not desc and et:
        desc = et["description"]
    
    final_tables.append({
        "grouping": t["grouping"],
        "table_name": t["table_name"],
        "description": desc,
        "columns": t["columns"],
        "longitudinal_tracking": t["longitudinal_tracking"] or (et["longitudinal_tracking"] if et else ""),
    })

# Add tables from enrichment that layout missed
for tname, et in enrichment_map.items():
    if tname not in seen_tables:
        clean_cols = [c for c in et["columns"] if c not in FALSE_COL_NAMES]
        final_tables.append({
            "grouping": et["grouping"],
            "table_name": tname,
            "description": et["description"],
            "columns": clean_cols,
            "longitudinal_tracking": et["longitudinal_tracking"],
        })

final_tables.sort(key=lambda t: (t["grouping"], t["table_name"]))

# Build inventory
inventory = []
for t in final_tables:
    fields = [{"name": c, "type": None, "description": None, "nullable": None,
               "max_length": None, "foreign_key": None, "value_set": None}
              for c in t["columns"]]
    inventory.append({
        "entity_name": t["table_name"],
        "grouping": t["grouping"],
        "description": t["description"],
        "longitudinal_tracking": t["longitudinal_tracking"],
        "field_count": len(fields),
        "fields": fields,
    })

json.dump(inventory, open(OUTPUT_FULL, 'w'), indent=2)

# Summary
grouping_stats = {}
total_fields = 0
for t in inventory:
    g = t["grouping"]
    if g not in grouping_stats:
        grouping_stats[g] = {"table_count": 0, "field_count": 0, "tables": []}
    grouping_stats[g]["table_count"] += 1
    grouping_stats[g]["field_count"] += t["field_count"]
    grouping_stats[g]["tables"].append({
        "name": t["entity_name"],
        "field_count": t["field_count"],
        "longitudinal_tracking": t["longitudinal_tracking"],
        "has_description": bool(t["description"]),
    })
    total_fields += t["field_count"]

summary = {
    "source": "Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf",
    "total_entities": len(inventory),
    "total_fields": total_fields,
    "fields_with_descriptions": 0,
    "tables_with_descriptions": sum(1 for t in inventory if t["description"]),
    "field_types_documented": False,
    "value_sets_documented": False,
    "foreign_keys_documented": False,
    "declared_but_empty_groupings": ["Lookup", "MIPS", "Medical Lookup"],
    "groupings": {
        g: {"table_count": s["table_count"], "field_count": s["field_count"], "tables": s["tables"]}
        for g, s in sorted(grouping_stats.items(), key=lambda x: -x[1]["field_count"])
    },
}

json.dump(summary, open(OUTPUT_SUMMARY, 'w'), indent=2)

# Report
print(f"Final: {len(inventory)} entities, {total_fields} fields")
print(f"Tables with descriptions: {summary['tables_with_descriptions']}/{len(inventory)}")
print(f"\nGrouping breakdown:")
for g, s in sorted(grouping_stats.items(), key=lambda x: -x[1]["field_count"]):
    print(f"  {g}: {s['table_count']} tables, {s['field_count']} fields")

# Compare with enrichment
print(f"\n--- Comparison with enrichment ---")
for tname in sorted(set(t["table_name"] for t in final_tables)):
    my = next((t for t in final_tables if t["table_name"] == tname), None)
    et = enrichment_map.get(tname)
    if my and et:
        diff = len(my["columns"]) - len(et["columns"])
        if abs(diff) > 5:
            print(f"  {tname}: mine={len(my['columns'])}, enrichment={len(et['columns'])} (diff={diff})")
