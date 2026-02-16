#!/usr/bin/env python3
"""Parse the overview data dictionary from pdftotext -layout output.

Uses regex matching for grouping names since column positions don't reliably
align between header labels and data. The 17+3 known groupings make this feasible.
"""

import json
import re

INPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/modernizing-medicine-inc--ema/analysis/overview-dd-text.txt"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/modernizing-medicine-inc--ema/analysis/overview-tables-parsed.json"

with open(INPUT, encoding='utf-8') as f:
    text = f.read()

# Clean Unicode artifacts
text = re.sub(r'[\u200b\u200c\u200d\ufeff\u00ad]', '', text)
text = text.replace('\f', '\n')
lines = text.split('\n')

# Known groupings from the document
GROUPINGS = [
    'Practice', 'Lookup', 'Document', 'Office Flow', 'Patient',
    'eLab', 'Pathology', 'Prescription', 'Ophth Pretesting', 'Appointment',
    'Visit', 'CC/HPI', 'Exam', 'Diagnosis', 'Procedure', 'PM Financials',
    'Inventory', 'Medical Lookup', 'MIPS'
]
# Full grouping names for normalization
GROUPING_FULL_NAMES = {
    'Document': 'Document Management',
    'Office': 'Office Flow',
    'Ophth': 'Ophth Pretesting',
    'PM': 'PM Financials',
    'Medical': 'Medical Lookup',
}
# Sort by length descending to match longer names first
GROUPINGS.sort(key=len, reverse=True)
grp_pattern = '|'.join(re.escape(g) for g in GROUPINGS)

# Pattern to match a data line: starts with IDX number, then grouping, then table name
# Format: " IDX  Grouping     table_name    Description..."
line_pattern = re.compile(
    r'^\s*(\d+)\s+(' + grp_pattern + r')\s+(\S+)\s+(.*)',
    re.IGNORECASE
)

records = []
current = None
last_grouping = ""
in_tables_section = False
past_data_dictionary = False

for li, raw in enumerate(lines):
    line = raw.rstrip()
    
    # Detect section boundaries
    if 'Database Tables' == line.strip():
        in_tables_section = True
        continue
    # Only stop at "Data Dictionary" if we're already in the tables section
    if in_tables_section and line.strip() == 'Data Dictionary':
        past_data_dictionary = True
        continue
    if in_tables_section and line.strip().startswith('Appendix'):
        past_data_dictionary = True
        continue
    
    if not in_tables_section or past_data_dictionary:
        continue
    
    # Skip headers and empty lines
    s = line.strip()
    if not s:
        continue
    if 'IDX' in line and 'Grouping' in line:
        continue
    if s in ('Tracking', 'Vertical', 'Priority', 'Delivery', 'Frequency', 'Length'):
        continue
    if re.match(r'^\d{1,3}$', s):
        continue
    
    # Try to match a data line
    m = line_pattern.match(line)
    if m:
        if current:
            records.append(current)
        
        idx_val = int(m.group(1))
        grouping = m.group(2)
        table = m.group(3)
        rest = m.group(4)
        
        # The rest contains: description (possibly with relationships, longitudinal, etc.)
        # These are hard to split by position since alignment varies
        # Just capture the whole rest as description for now
        current = {
            'idx': idx_val,
            'grouping': grouping,
            'table': table,
            'description': rest.strip()
        }
        last_grouping = grouping
    elif current is not None:
        # Continuation line - could be table name continuation, description continuation, 
        # or relationships
        s = line.strip()
        
        # Check if this is a single short word that completes a wrapped table name
        # (table names don't contain spaces; wrapped names are like "improvemen" + "t_activity")
        if re.match(r'^[a-z_]+$', s) and len(s) < 30:
            # Could be table name continuation or relationship name
            # If the current table looks truncated (ends mid-word), append
            if current['table'] and not current['table'].endswith('_') and len(current['table']) < 30:
                # Check if joining makes a valid name
                current['table'] += s
            else:
                # It's probably a relationship reference or description continuation
                current['description'] += ' ' + s
        else:
            # Description or relationship continuation
            current['description'] += ' ' + s

if current:
    records.append(current)

# Post-process
for r in records:
    r['description'] = re.sub(r'\s+', ' ', r['description']).strip()
    r['table'] = r['table'].strip()

# Check IDX continuity
idx_vals = [r['idx'] for r in records]
print(f"Parsed {len(records)} table entries")
print(f"IDX range: {min(idx_vals)} to {max(idx_vals)}")

from collections import Counter
idx_counts = Counter(idx_vals)
dups = {k: v for k, v in idx_counts.items() if v > 1}
if dups:
    print(f"Duplicate IDXs: {dups}")
expected = set(range(1, max(idx_vals) + 1))
missing = expected - set(idx_vals)
if missing:
    print(f"Missing IDXs ({len(missing)}): {sorted(missing)}")

# Group by normalized grouping
grp_summary = {}
for r in records:
    g = r['grouping']
    if g not in grp_summary:
        grp_summary[g] = []
    grp_summary[g].append(r['table'])

print(f"\nGrouping summary:")
for g, tables in sorted(grp_summary.items(), key=lambda x: -len(x[1])):
    print(f"  {g}: {len(tables)} tables")

# Save output
output = {
    'source': 'ModMed-EMA-EHI-Export-Data-Dictionary.pdf (overview, 96 pages)',
    'parsedAt': '2026-02-16',
    'totalTables': len(records),
    'groupingSummary': {g: len(t) for g, t in sorted(grp_summary.items(), key=lambda x: -len(x[1]))},
    'tables': records
}

with open(OUTPUT, 'w') as f:
    json.dump(output, f, indent=2)

# Show samples
print(f"\nFirst 10 records:")
for r in records[:10]:
    print(f"  [{r['idx']}] {r['grouping']} / {r['table']}: {r['description'][:70]}")
print(f"\nLast 5 records:")
for r in records[-5:]:
    print(f"  [{r['idx']}] {r['grouping']} / {r['table']}: {r['description'][:70]}")
