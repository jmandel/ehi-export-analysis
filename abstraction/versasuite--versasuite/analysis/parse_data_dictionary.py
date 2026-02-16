#!/usr/bin/env python3
"""Parse all VersaSuite HTML data dictionary files into a structured JSON inventory."""

import os
import json
import re
from html.parser import HTMLParser

DATA_DICT_DIR = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'data-dictionary')
OUTPUT_FULL = os.path.join(os.path.dirname(__file__), 'entity-inventory-full.json')
OUTPUT_SUMMARY = os.path.join(os.path.dirname(__file__), 'entity-inventory-summary.json')


class TableParser(HTMLParser):
    """Extract table rows from HTML data dictionary pages."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.in_h1 = False
        self.in_h2 = False
        self.current_row = []
        self.current_cell = ''
        self.rows = []
        self.h1_texts = []
        self.h2_texts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.current_cell = ''
        elif tag == 'h1':
            self.in_h1 = True
        elif tag == 'h2':
            self.in_h2 = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        elif tag == 'h1':
            self.in_h1 = False
        elif tag == 'h2':
            self.in_h2 = False

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data
        elif self.in_h1:
            self.h1_texts.append(data.strip())
        elif self.in_h2:
            self.h2_texts.append(data.strip())


def classify_entity(filename, title):
    """Classify entity into a domain category based on prefix and name."""
    fn = filename.upper()
    title_lower = (title or '').lower()

    if fn.startswith('AP_'):
        # AP = Administrative/Patient core
        if any(k in fn for k in ['ALLERGY']):
            return 'Allergies'
        if any(k in fn for k in ['ALERT']):
            return 'Alerts'
        if any(k in fn for k in ['AUDIT', 'ATNA']):
            return 'Audit'
        if any(k in fn for k in ['ADDR', 'CONTACT', 'PHONE', 'LANG']):
            return 'Demographics / Contact'
        if any(k in fn for k in ['IMG']):
            return 'Images / Documents'
        if any(k in fn for k in ['NOTE']):
            return 'Clinical Notes'
        if any(k in fn for k in ['TASK']):
            return 'Tasks / Workflow'
        if any(k in fn for k in ['RECURRINGCHARGE', 'OUTSIDESALE']):
            return 'Billing / Financial'
        if any(k in fn for k in ['ACK']):
            return 'Acknowledgments'
        return 'Administrative / Patient'

    if fn.startswith('AX_'):
        return 'Accounting / Financial (AX)'

    if fn.startswith('HC_'):
        if any(k in fn for k in ['BLNG', 'STMT']):
            return 'Billing / Financial'
        if any(k in fn for k in ['DRUG', 'MED']):
            return 'Medications'
        if any(k in fn for k in ['LAB']):
            return 'Laboratory'
        if any(k in fn for k in ['PROBLEM']):
            return 'Problems / Conditions'
        if any(k in fn for k in ['APPT']):
            return 'Appointments / Scheduling'
        if any(k in fn for k in ['PT_', 'PT.', 'PTBAL', 'PTPRV']):
            return 'Patient Core'
        if any(k in fn for k in ['BHCP']):
            return 'Behavioral Health'
        if any(k in fn for k in ['BB', 'BT', 'BLOOD']):
            return 'Blood Bank / Transfusion'
        if any(k in fn for k in ['CONTOFCARE']):
            return 'Continuity of Care'
        if any(k in fn for k in ['OVERRIDE']):
            return 'Overrides'
        if any(k in fn for k in ['PHI']):
            return 'PHI Requests'
        if any(k in fn for k in ['OSINST']):
            return 'Orders / Instructions'
        if any(k in fn for k in ['ALLERGY']):
            return 'Allergies'
        return 'Healthcare (HC)'

    if fn.startswith('EM_'):
        if any(k in fn for k in ['MED']):
            return 'Medications'
        if any(k in fn for k in ['TREAT']):
            return 'Treatment Administration'
        return 'Encounters / Administration'

    if fn.startswith('VE_'):
        return 'EHR Exam / Clinical Notes (VE)'

    if fn.startswith('FQ_'):
        return 'Financial / Patient Earnings'

    if fn.startswith('DIRECT'):
        return 'Financial / Direct Deposit'

    # Descriptive names
    if 'address' in title_lower:
        return 'Demographics / Contact'
    if 'attachment' in title_lower:
        return 'Images / Documents'
    if 'clinical note' in title_lower or 'clinical_notes' in fn.lower():
        return 'Clinical Notes'
    if 'encounter' in title_lower:
        return 'Encounters / Administration'
    if 'billing' in title_lower:
        return 'Billing / Financial'
    if 'allergy' in title_lower:
        return 'Allergies'
    if 'patient' in title_lower and 'earning' in title_lower:
        return 'Financial / Patient Earnings'
    if 'behavioral health' in title_lower or 'bhcp' in fn.lower():
        return 'Behavioral Health'
    if 'transfer' in title_lower or 'pttransfer' in fn.lower():
        return 'Encounters / Administration'
    if 'pthis' in fn.lower() or 'pttypehis' in fn.lower():
        return 'Patient Core'
    if 'encounter' in fn.lower() or 'patient_encounter' in fn.lower():
        return 'Encounters / Administration'
    if 'patient' in title_lower:
        return 'Patient Core'
    if fn.startswith('AP_ACK') or fn.startswith('DOCUMENTATION FOR AP_ACK'):
        return 'Acknowledgments'

    return 'Other'


def parse_file(filepath):
    """Parse a single HTML data dictionary file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    parser = TableParser()
    parser.feed(html)

    filename = os.path.basename(filepath)

    # Determine entity title from H1/H2
    title = None
    csv_name = None
    for h in parser.h1_texts:
        if h.startswith('Documentation for '):
            csv_name = h.replace('Documentation for ', '').strip()
        elif h and h != 'Data Dictionary':
            title = h
    for h in parser.h2_texts:
        if h and not title:
            title = h

    if not title:
        title = filename.replace('.html', '')

    if not csv_name:
        # Try to extract from title
        csv_name = filename.replace(' Data Dictionary.html', '.csv').replace('_Documentation.html', '.csv').replace('.html', '.csv')

    # Parse fields from table rows
    fields = []
    header = None
    for row in parser.rows:
        if not row:
            continue
        # Detect header row
        if any('column' in c.lower() or 'description' in c.lower() for c in row):
            header = row
            continue
        if len(row) >= 3:
            field = {
                'column_name': row[0],
                'expanded_name': row[1],
                'description': row[2] if len(row) > 2 else ''
            }
            fields.append(field)
        elif len(row) == 2:
            field = {
                'column_name': row[0],
                'expanded_name': row[1],
                'description': ''
            }
            fields.append(field)

    category = classify_entity(filename, title)

    # Determine description quality
    has_meaningful_desc = 0
    generic_patterns = [
        r'^provides information related to',
        r'^contains detailed information or identifiers for',
        r'^specifies the date associated with',
        r'^records the historical data or changes related to',
    ]
    for f in fields:
        desc = f['description'].lower().strip()
        if desc and not any(re.match(p, desc) for p in generic_patterns):
            has_meaningful_desc += 1

    return {
        'filename': filename,
        'csv_name': csv_name,
        'title': title,
        'category': category,
        'field_count': len(fields),
        'fields_with_description': sum(1 for f in fields if f['description'].strip()),
        'fields_with_meaningful_description': has_meaningful_desc,
        'fields': fields,
        'size_bytes': os.path.getsize(filepath)
    }


def main():
    entities = []
    errors = []

    for filename in sorted(os.listdir(DATA_DICT_DIR)):
        if not filename.endswith('.html') or filename == 'index.html':
            continue
        filepath = os.path.join(DATA_DICT_DIR, filename)
        try:
            entity = parse_file(filepath)
            entities.append(entity)
        except Exception as e:
            errors.append({'filename': filename, 'error': str(e)})

    # Write full inventory
    with open(OUTPUT_FULL, 'w') as f:
        json.dump({
            'total_entities': len(entities),
            'total_fields': sum(e['field_count'] for e in entities),
            'total_fields_with_description': sum(e['fields_with_description'] for e in entities),
            'total_fields_with_meaningful_description': sum(e['fields_with_meaningful_description'] for e in entities),
            'parse_errors': errors,
            'entities': entities
        }, f, indent=2)

    # Build summary
    categories = {}
    for e in entities:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'total_fields': 0, 'entities': []}
        categories[cat]['entity_count'] += 1
        categories[cat]['total_fields'] += e['field_count']
        categories[cat]['entities'].append({
            'filename': e['filename'],
            'title': e['title'],
            'field_count': e['field_count'],
            'fields_with_description': e['fields_with_description'],
            'fields_with_meaningful_description': e['fields_with_meaningful_description']
        })

    summary = {
        'total_entities': len(entities),
        'total_fields': sum(e['field_count'] for e in entities),
        'total_fields_with_description': sum(e['fields_with_description'] for e in entities),
        'total_fields_with_meaningful_description': sum(e['fields_with_meaningful_description'] for e in entities),
        'parse_errors': len(errors),
        'categories': categories,
        'top_entities_by_field_count': sorted(
            [{'filename': e['filename'], 'title': e['title'], 'category': e['category'], 'field_count': e['field_count']} for e in entities],
            key=lambda x: x['field_count'],
            reverse=True
        )[:20]
    }

    with open(OUTPUT_SUMMARY, 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Entities parsed: {len(entities)}")
    print(f"Parse errors: {len(errors)}")
    print(f"Total fields: {sum(e['field_count'] for e in entities)}")
    print(f"Fields with any description: {sum(e['fields_with_description'] for e in entities)}")
    print(f"Fields with meaningful description: {sum(e['fields_with_meaningful_description'] for e in entities)}")
    print()
    print("Categories:")
    for cat in sorted(categories.keys()):
        c = categories[cat]
        print(f"  {cat}: {c['entity_count']} entities, {c['total_fields']} fields")
    print()
    print("Top 20 entities by field count:")
    for e in summary['top_entities_by_field_count']:
        print(f"  {e['filename']}: {e['field_count']} fields ({e['category']})")

    if errors:
        print("\nParse errors:")
        for e in errors:
            print(f"  {e['filename']}: {e['error']}")


if __name__ == '__main__':
    main()
