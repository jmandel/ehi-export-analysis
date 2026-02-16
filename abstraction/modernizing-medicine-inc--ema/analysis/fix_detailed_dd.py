#!/usr/bin/env python3
"""Fix the pre-extracted detailed data dictionary JSON.

The enrichment extraction has a systematic column shift issue:
- 'description' field contains actual description + actual dataType appended
- 'dataType' field contains the actual nullable value (True/False)
- 'nullable' is always null

This script fixes these by:
1. Extracting the dataType from the end of the description
2. Moving the current dataType value to nullable
3. Producing corrected output with verified statistics
"""

import json
import re

INPUT = "/home/jmandel/hobby/ehi-export-analysis/results/modernizing-medicine-inc--ema/downloads/enrichment/detailed-data-dictionary.json"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/modernizing-medicine-inc--ema/analysis/full-entity-inventory.json"

with open(INPUT) as f:
    data = json.load(f)

fields = data['fields']
print(f"Input: {len(fields)} fields, {len(data['tables'])} tables")

# Known SQL data types in this dictionary
KNOWN_TYPES = ['string', 'int', 'boolean', 'timestamp', 'date', 'double', 'decimal', 'float', 'bigint']
# Pattern 1: type at end of description (e.g., "...some desc string")
type_pattern = re.compile(r'\s+(' + '|'.join(KNOWN_TYPES) + r')\s*$', re.IGNORECASE)
# Pattern 2: type followed by True/False at end (e.g., "...some desc timestamp True")
type_null_pattern = re.compile(r'\s+(' + '|'.join(KNOWN_TYPES) + r')\s+(True|False)\s*$', re.IGNORECASE)
# Pattern 3: type embedded mid-description due to text wrapping (e.g., "...desc string continuation")
# We'll handle this as a fallback

fixed_count = 0
unfixed_count = 0
parse_errors = []

for f in fields:
    # Step 1: Move current dataType (which is actually nullable) to nullable
    raw_dtype = f.get('dataType', '')
    if raw_dtype in ('True', 'False', 'true', 'false'):
        f['nullable'] = raw_dtype.lower() == 'true'
    elif raw_dtype is None or raw_dtype == '':
        f['nullable'] = None
    else:
        # Unexpected value in dataType - flag it
        f['nullable'] = None
        parse_errors.append({
            'idx': f['idx'],
            'issue': f'unexpected dataType value: {raw_dtype}',
            'table': f['table'],
            'column': f['column']
        })
    
    # Step 2: Extract actual dataType from description
    desc = f.get('description', '') or ''
    
    # Try pattern 2 first (type + True/False at end)
    match2 = type_null_pattern.search(desc)
    if match2:
        f['dataType'] = match2.group(1).lower()
        # The True/False here is a second nullable indicator; use it if we don't already have one
        if f['nullable'] is None:
            f['nullable'] = match2.group(2).lower() == 'true'
        f['description'] = desc[:match2.start()].strip()
        fixed_count += 1
        continue
    
    # Try pattern 1 (type at end)
    match1 = type_pattern.search(desc)
    if match1:
        f['dataType'] = match1.group(1).lower()
        f['description'] = desc[:match1.start()].strip()
        fixed_count += 1
        continue
    
    # Fallback: look for type word anywhere preceded by ". " or similar boundary
    # This handles cases where text wrapping put desc continuation after the type
    fallback = re.search(r'(?:^|\.\s+|\)\s+)(' + '|'.join(KNOWN_TYPES) + r')(?:\s+True|\s+False|\s)', desc, re.IGNORECASE)
    if fallback:
        f['dataType'] = fallback.group(1).lower()
        # Don't modify description in fallback - too risky
        f['description'] = desc  # keep original, flag as partial fix
        fixed_count += 1
        continue
    
    # Could not extract type
    f['dataType'] = ''
    unfixed_count += 1

print(f"Fixed: {fixed_count}, Could not extract type: {unfixed_count}")
print(f"Parse errors: {len(parse_errors)}")
if parse_errors:
    for e in parse_errors[:10]:
        print(f"  IDX {e['idx']}: {e['issue']}")

# Build entity inventory grouped by table
entities = {}
for f in fields:
    tbl = f.get('table', 'UNKNOWN') or 'UNKNOWN'
    if tbl not in entities:
        entities[tbl] = {
            'table': tbl,
            'grouping': f.get('grouping', ''),
            'fields': []
        }
    entities[tbl]['fields'].append({
        'idx': f['idx'],
        'column': f.get('column', ''),
        'description': f.get('description', ''),
        'dataType': f.get('dataType', ''),
        'nullable': f.get('nullable'),
        'fieldLength': f.get('fieldLength'),
        'valuesCodingSchema': f.get('valuesCodingSchema', '')
    })
    if f.get('grouping') and not entities[tbl]['grouping']:
        entities[tbl]['grouping'] = f['grouping']

# Normalize grouping names (some have sub-categories like "Ophth Pretesting visual_acuity")
# Consolidate into main groupings
MAIN_GROUPINGS = {
    'Lookup', 'Practice', 'Document Management', 'Office Flow', 'Patient',
    'eLab', 'Pathology', 'Prescription', 'Ophth Pretesting', 'Appointment',
    'Visit', 'CC/HPI', 'Exam', 'Diagnosis', 'Procedure', 'PM Financials', 'Inventory'
}

def normalize_grouping(g):
    """Map sub-groupings to main groupings."""
    if not g:
        return 'Unknown'
    for main in MAIN_GROUPINGS:
        if g.startswith(main) or g == main:
            return main
    # Handle truncated names from PDF parsing
    if 'Financials' in g or g.startswith('PM'):
        return 'PM Financials'
    if 'Pretesting' in g or 'Ophth' in g:
        return 'Ophth Pretesting'
    if 'Patient' in g or g == 'Patient':
        return 'Patient'
    if 'Appointment' in g:
        return 'Appointment'
    if 'Visit' in g:
        return 'Visit'
    if 'Lab' in g or g == 'eLab':
        return 'eLab'
    if 'Prescription' in g:
        return 'Prescription'
    if 'Pathology' in g:
        return 'Pathology'
    if 'Diagnosis' in g:
        return 'Diagnosis'
    if 'Procedure' in g:
        return 'Procedure'
    if 'CC/HPI' in g or 'HPI' in g:
        return 'CC/HPI'
    if 'Exam' in g:
        return 'Exam'
    if 'Inventory' in g:
        return 'Inventory'
    if 'Document' in g:
        return 'Document Management'
    if 'Office' in g or 'Flow' in g:
        return 'Office Flow'
    if 'Practice' in g:
        return 'Practice'
    if 'Lookup' in g:
        return 'Lookup'
    return g

# Apply normalized grouping
for tn, td in entities.items():
    td['normalizedGrouping'] = normalize_grouping(td['grouping'])

# Compute statistics
total = len(fields)
desc_count = sum(1 for f in fields if f.get('description') and f['description'].strip())
type_count = sum(1 for f in fields if f.get('dataType') and f['dataType'].strip())
vals_count = sum(1 for f in fields if f.get('valuesCodingSchema') and f['valuesCodingSchema'].strip())
null_true = sum(1 for f in fields if f.get('nullable') is True)
null_false = sum(1 for f in fields if f.get('nullable') is False)

# Data type distribution
dtypes = {}
for f in fields:
    dt = f.get('dataType', '') or '(empty)'
    dtypes[dt] = dtypes.get(dt, 0) + 1

# Grouping statistics (using normalized groupings)
grp_stats = {}
for tn, td in entities.items():
    g = td['normalizedGrouping']
    if g not in grp_stats:
        grp_stats[g] = {'tables': 0, 'fields': 0, 'fieldsWithDescription': 0, 'fieldsWithType': 0}
    grp_stats[g]['tables'] += 1
    grp_stats[g]['fields'] += len(td['fields'])
    grp_stats[g]['fieldsWithDescription'] += sum(1 for f in td['fields'] if f.get('description') and f['description'].strip())
    grp_stats[g]['fieldsWithType'] += sum(1 for f in td['fields'] if f.get('dataType') and f['dataType'].strip())

# Sort entities
entity_list = sorted(entities.values(), key=lambda x: x['fields'][0]['idx'] if x['fields'] else 0)
for e in entity_list:
    e['fieldCount'] = len(e['fields'])

output = {
    'source': 'ModMed-EMA-Detailed-Data-Dictionary.pdf (210 pages) — corrected from enrichment extraction',
    'parsedAt': '2026-02-16',
    'correctionNote': 'The enrichment extraction had a systematic column shift: description absorbed dataType, dataType showed nullable. This was corrected by extracting types from description text.',
    'stats': {
        'totalFields': total,
        'totalTables': len(entities),
        'fieldsWithDescription': desc_count,
        'fieldsWithType': type_count,
        'fieldsWithValues': vals_count,
        'fieldsNullableTrue': null_true,
        'fieldsNullableFalse': null_false,
        'descriptionPct': round(desc_count / total * 100, 1) if total else 0,
        'typePct': round(type_count / total * 100, 1) if total else 0,
        'dataTypeDistribution': dict(sorted(dtypes.items(), key=lambda x: -x[1]))
    },
    'groupingStats': dict(sorted(grp_stats.items(), key=lambda x: -x[1]['fields'])),
    'parseErrors': parse_errors,
    'entities': entity_list
}

with open(OUTPUT, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n=== Corrected Parse Results ===")
print(f"Total fields: {total}")
print(f"Total tables: {len(entities)}")
print(f"Fields with description: {desc_count} ({desc_count/total*100:.1f}%)")
print(f"Fields with data type: {type_count} ({type_count/total*100:.1f}%)")
print(f"Fields with values/coding: {vals_count}")
print(f"Fields nullable=True: {null_true}, nullable=False: {null_false}")
print(f"\nData type distribution:")
for dt, c in sorted(dtypes.items(), key=lambda x: -x[1]):
    print(f"  {dt}: {c}")
print(f"\nGrouping breakdown (normalized):")
for g, s in sorted(grp_stats.items(), key=lambda x: -x[1]['fields']):
    dp = s['fieldsWithDescription'] / s['fields'] * 100 if s['fields'] else 0
    print(f"  {g}: {s['tables']} tables, {s['fields']} fields ({dp:.0f}% described)")
print(f"\nTop 20 tables by field count:")
for t in sorted(entity_list, key=lambda x: -x['fieldCount'])[:20]:
    print(f"  {t['table']} ({t['normalizedGrouping']}): {t['fieldCount']} fields")

# Spot check: verify first few records look correct
print(f"\nSpot check - first 5 records:")
for f in fields[:5]:
    print(f"  idx={f['idx']} tbl={f['table']} col={f['column']}")
    print(f"    desc=\"{f['description'][:80]}\"")
    print(f"    type={f['dataType']} nullable={f['nullable']} len={f.get('fieldLength')}")
