#!/usr/bin/env python3
"""
Parses the escribeHOST EHI Export Format Documentation HTML into structured JSON.
Reads raw HTML from downloads/ehi-export-doc.html and produces:
  - entity-inventory-full.json  (complete field-level extraction)
  - entity-inventory-summary.json (aggregate stats)
"""

import re
import json
import html
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
HTML_PATH = SCRIPT_DIR.parent / "downloads" / "ehi-export-doc.html"

raw = HTML_PATH.read_text(encoding="utf-8")

def strip_tags(s):
    return re.sub(r'<[^>]*>', '', s).strip()

def normalize_ws(s):
    return re.sub(r'\s+', ' ', s).strip()

# Find all h2 sections with ids (these are the table definitions)
h2_pattern = re.compile(r'<h2\s+id="([^"]+)"[^>]*>(.*?)</h2>', re.DOTALL)
h2_matches = list(h2_pattern.finditer(raw))

tables = []
parse_errors = []

for idx, match in enumerate(h2_matches):
    table_id = match.group(1)
    heading_html = match.group(2)
    heading_text = normalize_ws(strip_tags(heading_html))
    
    # Get section content until next h2
    start = match.end()
    if idx + 1 < len(h2_matches):
        end = h2_matches[idx + 1].start()
    else:
        end = len(raw)
    section = raw[start:end]
    
    # Extract description from heading: "TABLE_NAME - Description text."
    desc_match = re.match(r'^[A-Z_]+\s*-\s*(.*)', heading_text)
    description = desc_match.group(1).strip() if desc_match else heading_text
    
    # Parse column rows from the table
    # Each column starts with <tr class="borderBottom"> containing two <td> cells
    # Followed by description <tr> with colspan="2" and optional constraint rows
    
    row_pattern = re.compile(r'<tr([^>]*)>(.*?)</tr>', re.DOTALL)
    rows = list(row_pattern.finditer(section))
    
    columns = []
    state = {'current_col': None, 'desc_parts': [], 'constraint_parts': []}
    
    def flush():
        if state['current_col']:
            state['current_col']['description'] = normalize_ws(' '.join(state['desc_parts']))
            state['current_col']['constraints'] = [c for c in state['constraint_parts'] if c.strip()]
            columns.append(state['current_col'])
        state['current_col'] = None
        state['desc_parts'] = []
        state['constraint_parts'] = []
    
    for row_match in rows:
        attrs = row_match.group(1)
        inner = row_match.group(2)
        is_border = 'borderBottom' in attrs
        is_constraint = 'checkConstraints' in inner
        
        if is_border:
            flush()
            # Extract td cells
            tds = re.findall(r'<td[^>]*>(.*?)</td>', inner, re.DOTALL)
            if len(tds) >= 2:
                name_text = normalize_ws(strip_tags(tds[0]))
                type_text = normalize_ws(strip_tags(tds[1]))
                
                # Parse "1. COLUMN_NAME (PK) (nullable)"
                name_match = re.match(r'(\d+)\s*\.\s*([A-Z_][A-Z0-9_]*)', name_text)
                ordinal = int(name_match.group(1)) if name_match else 0
                name = name_match.group(2) if name_match else name_text
                is_pk = '(PK)' in name_text
                is_nullable = '(nullable)' in name_text
                
                state['current_col'] = {
                    'ordinal': ordinal,
                    'name': name,
                    'isPrimaryKey': is_pk,
                    'dataType': type_text,
                    'nullable': is_nullable,
                }
        elif 'colspan' in inner:
            text = normalize_ws(strip_tags(inner))
            # Skip header rows
            if text in ('Column Name', 'Data Type', 'Column NameData Type', ''):
                continue
            if is_constraint:
                state['constraint_parts'].append(text)
            else:
                state['desc_parts'].append(text)
    
    flush()
    
    if columns:
        tables.append({
            'name': table_id,
            'description': description,
            'columns': columns,
        })
    elif table_id not in ('Exported Files', 'Tables Index'):
        # Not a data table section
        parse_errors.append({'table': table_id, 'error': 'No columns found'})

# Build entity-inventory-full.json
full_inventory = []
for t in tables:
    entity = {
        'entity': t['name'],
        'description': t['description'],
        'field_count': len(t['columns']),
        'fields': []
    }
    for c in t['columns']:
        field = {
            'name': c['name'],
            'ordinal': c['ordinal'],
            'dataType': c['dataType'],
            'isPrimaryKey': c['isPrimaryKey'],
            'nullable': c['nullable'],
            'description': c.get('description', ''),
            'constraints': c.get('constraints', []),
        }
        entity['fields'].append(field)
    full_inventory.append(entity)

# Build summary
total_fields = sum(e['field_count'] for e in full_inventory)
fields_with_desc = sum(1 for e in full_inventory for f in e['fields'] if f['description'])
fields_with_type = sum(1 for e in full_inventory for f in e['fields'] if f['dataType'])
fields_with_constraints = sum(1 for e in full_inventory for f in e['fields'] if f['constraints'])
pks = sum(1 for e in full_inventory for f in e['fields'] if f['isPrimaryKey'])

# Categorize tables by domain
def categorize(name):
    n = name.upper()
    if n.startswith('PATIENT') and ('INSURANCE' in n or 'ELIGIBILITY' in n):
        return 'Insurance & Eligibility'
    if n.startswith('LAB') or n == 'LABORATORY_TESTS':
        return 'Laboratory'
    if n.startswith('MED') or n.startswith('RXHUB') or n == 'DRUG_HISTORY_REQUESTS' or n == 'DRUG_HISTORY_REQUEST_MESSAGES':
        return 'Medications & Allergies'
    if n.startswith('PHR'):
        return 'Patient Portal / Communications'
    if n.startswith('SURVEY'):
        return 'Surveys / Custom Forms'
    if n.startswith('RS_'):
        return 'Research Studies'
    if n.startswith('PATIENT'):
        return 'Patient Demographics & History'
    if n in ('PE_PATIENT_ENCOUNTER',):
        return 'Encounters'
    if n in ('PROBLEMS', 'PROBLEMS_DOCUMENTED'):
        return 'Problems / Diagnoses'
    if n in ('VITALS', 'PATIENT_REPORTED_VITALS'):
        return 'Vitals'
    if n in ('ORDERS', 'ORDERS_ACTIONS'):
        return 'Orders'
    if n in ('INTERVENTIONS', 'INTERVENTIONS_NOT_DONE'):
        return 'Interventions / Procedures'
    if n in ('PROVIDERS', 'USERS', 'LOCATIONS'):
        return 'Providers & System'
    if n in ('OTHER_CONTACTS', 'PC_PATIENT_CONTACTS', 'HEALTH_CARE_TEAM_OTH_CONTACTS', 'HEALTH_CARE_TEAM_PROVIDERS'):
        return 'Care Team & Contacts'
    if n in ('CCDS_IMPORTED_DOCUMENTS', 'DOCUMENT_SNAPSHOTS', 'TOC_REQUESTS', 'TRANSITION_OF_CARE_HISTORY_LOG'):
        return 'Documents & Transitions of Care'
    if n in ('DIAGNOSTIC_IMAGING_REPORTS',):
        return 'Imaging'
    if n in ('SCANNED_CARDS',):
        return 'Scanned Documents'
    if n in ('AMENDMENT_REQUESTS',):
        return 'Amendment Requests'
    if n in ('SOCIAL_HISTORY_ENTRIES',):
        return 'Social History'
    if n in ('RECONCILIATION_HISTORY',):
        return 'Reconciliation'
    if n in ('ETHNICITIES',):
        return 'Reference Data'
    if n in ('MISC_DEVICES',):
        return 'Medical Devices'
    return 'Other'

# Build category breakdown
from collections import Counter, defaultdict
cat_tables = defaultdict(list)
cat_fields = Counter()
for e in full_inventory:
    cat = categorize(e['entity'])
    cat_tables[cat].append(e['entity'])
    cat_fields[cat] += e['field_count']

summary = {
    'total_entities': len(full_inventory),
    'total_fields': total_fields,
    'fields_with_descriptions': fields_with_desc,
    'fields_with_descriptions_pct': round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
    'fields_with_types': fields_with_type,
    'fields_with_constraints': fields_with_constraints,
    'primary_keys': pks,
    'parse_errors': parse_errors,
    'categories': {
        cat: {
            'table_count': len(tbls),
            'field_count': cat_fields[cat],
            'tables': tbls,
        }
        for cat, tbls in sorted(cat_tables.items())
    },
    'tables': [
        {
            'entity': e['entity'],
            'description': e['description'],
            'field_count': e['field_count'],
            'category': categorize(e['entity']),
            'primary_keys': [f['name'] for f in e['fields'] if f['isPrimaryKey']],
            'foreign_key_hints': [f['name'] for f in e['fields'] if f['name'].endswith('_ID') and not f['isPrimaryKey']],
        }
        for e in full_inventory
    ]
}

# Write outputs
out_full = SCRIPT_DIR / "entity-inventory-full.json"
out_summary = SCRIPT_DIR / "entity-inventory-summary.json"

out_full.write_text(json.dumps(full_inventory, indent=2))
out_summary.write_text(json.dumps(summary, indent=2))

print(f"Parsed {len(full_inventory)} tables with {total_fields} total fields")
print(f"Fields with descriptions: {fields_with_desc} ({summary['fields_with_descriptions_pct']}%)")
print(f"Fields with types: {fields_with_type}")
print(f"Fields with constraints: {fields_with_constraints}")
print(f"Primary keys: {pks}")
print(f"Parse errors: {len(parse_errors)}")
print()
print("Category breakdown:")
for cat in sorted(cat_tables.keys()):
    print(f"  {cat}: {len(cat_tables[cat])} tables, {cat_fields[cat]} fields")
