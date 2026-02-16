#!/usr/bin/env python3
"""
Parse the gGastro EHI Patient Export Specifications PDF text extraction
to produce a complete entity inventory in JSON format.

Usage:
  pdftotext -layout <path-to-pdf> main-dict.txt
  python3 parse_data_dictionary_v2.py

Input: main-dict.txt (pdftotext -layout output of Dec 2025 PDF:
       gGastro-EHI-Patient-Export-Specifications-Dec2025.pdf)
Output: full-entity-inventory.json, summary-stats.json
"""

import json
import re
import sys

def parse_dictionary(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Find section boundaries
    dict_start = None
    dict_end = None
    for i, line in enumerate(lines):
        raw = line.rstrip('\n')
        stripped = raw.strip()
        # First "Column Number - Name" header marks start of dictionary
        if "Column Number - Name" in stripped and dict_start is None:
            # Entity name is on the line above
            for j in range(i-1, max(0, i-5), -1):
                if lines[j].strip():
                    dict_start = j
                    break
            if dict_start is None:
                dict_start = i - 1
        if stripped == "Data Schema" and i > 100:
            dict_end = i
            break

    if dict_start is None or dict_end is None:
        print(f"Could not find section boundaries: start={dict_start}, end={dict_end}")
        sys.exit(1)

    print(f"CSV Files Dictionary section: lines {dict_start+1} to {dict_end+1}")

    entities = []
    current_entity = None
    current_fields = []

    # Entity names start at column 0 (no leading whitespace)
    # They are PascalCase words, possibly with numbers
    entity_pattern = re.compile(r'^([A-Z][A-Za-z0-9]+)$')

    # Field lines start with leading whitespace followed by "N - FieldName"
    # OR start at col 0 with "N - FieldName" (rare, after page breaks)
    field_pattern = re.compile(
        r'^\s*(\d+)\s+-\s+(\S+)\s+'   # column number and name
    )

    for i in range(dict_start, dict_end):
        raw = lines[i].rstrip('\n')
        stripped = raw.strip()

        if not stripped:
            continue

        # Skip header lines and form feeds
        if stripped.startswith("Column Number - Name"):
            continue
        if stripped.startswith('\x0c'):
            stripped = stripped.lstrip('\x0c').strip()
            raw = raw.lstrip('\x0c')

        # Check for page break form-feed at start of line
        if raw.startswith('\x0c'):
            raw = raw[1:]
            stripped = raw.strip()

        # Entity name: starts at column 0, is a single PascalCase word
        leading_spaces = len(raw) - len(raw.lstrip(' '))
        entity_match = entity_pattern.match(stripped)

        if entity_match and leading_spaces == 0:
            # Save previous entity
            if current_entity:
                entities.append({
                    'name': current_entity,
                    'fields': current_fields
                })
            current_entity = stripped
            current_fields = []
            continue

        # Field definition line
        field_match = field_pattern.match(stripped)
        if field_match and current_entity:
            col_num = int(field_match.group(1))
            field_name = field_match.group(2)

            # Parse the rest of the line after field name
            rest_of_line = stripped[field_match.end():]

            # Try to parse type from the rest
            # Types are: GUID, Alphanumeric, Numeric, Boolean, Date & Time, Date, Decimal, Time, XML, Binary, Small Date & Time
            type_pattern = re.compile(
                r'^(GUID|Alphanumeric|Numeric|Boolean|Date & Time|Date|Decimal|Time|XML|Binary|Small Date & Time|DATETIME2)\s*(.*)',
                re.IGNORECASE
            )
            type_match = type_pattern.match(rest_of_line)

            field_type = "Unknown"
            length = None
            format_translation = None

            if type_match:
                field_type = type_match.group(1)
                remainder = type_match.group(2).strip()

                # Try to extract length (numeric value at start)
                length_match = re.match(r'^(\d+)\s*(.*)', remainder)
                if length_match:
                    length = int(length_match.group(1))
                    remainder = length_match.group(2).strip()

                if remainder:
                    # Filter out GUID format patterns and date format patterns
                    if remainder == 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx':
                        pass  # GUID format, skip
                    elif remainder.startswith('MM/dd/') or remainder.startswith('hh:mm'):
                        format_translation = remainder  # Date/time format
                    elif remainder.startswith('0 = False'):
                        pass  # Boolean description, skip
                    else:
                        format_translation = remainder
            else:
                # Sometimes type is split across columns differently
                # Try a more flexible approach
                parts = rest_of_line.split()
                if parts:
                    # Map common types
                    if parts[0] in ['GUID', 'Alphanumeric', 'Numeric', 'Boolean', 'Decimal', 'Time', 'XML', 'Binary']:
                        field_type = parts[0]

            field_info = {
                'column': col_num,
                'name': field_name,
                'type': field_type,
            }
            if length is not None:
                field_info['max_length'] = length
            if format_translation:
                field_info['format_or_translation'] = format_translation

            current_fields.append(field_info)
            continue

        # Continuation line (indented, not a field or entity)
        if current_fields and leading_spaces > 10 and not field_match:
            # This is a continuation of the previous field's format/translation
            if stripped and not stripped.startswith('xxxxxxxx') and stripped != '0 = False / 1 = True':
                if 'format_or_translation' in current_fields[-1]:
                    current_fields[-1]['format_or_translation'] += ' ' + stripped
                else:
                    # Only add if it looks like a translation reference
                    if not stripped.startswith('MM/dd') and not stripped.startswith('hh:mm'):
                        current_fields[-1]['format_or_translation'] = stripped

    # Save last entity
    if current_entity:
        entities.append({
            'name': current_entity,
            'fields': current_fields
        })

    return entities


def categorize_entity(name):
    """Assign a domain category based on entity name patterns."""
    name_lower = name.lower()

    # Billing & Claims
    if any(x in name_lower for x in ['billing', 'claim', 'charge', 'collection',
                                       'superbill', 'autopost', 'edi', 'era', 'feeschedule',
                                       'prepay', 'statement']):
        return "Billing & Claims"
    if name_lower in ['eligibility']:
        return "Billing & Claims"

    # Insurance
    if 'insurance' in name_lower:
        return "Insurance"

    # Payment
    if 'payment' in name_lower or 'refund' in name_lower or 'adjustment' in name_lower:
        if 'billing' in name_lower:
            return "Billing & Claims"
        return "Billing & Claims"

    # Scheduling
    if any(x in name_lower for x in ['appointment', 'scheduler', 'waitlist', 'kiosk']):
        return "Scheduling"

    # GI-Specific
    if any(x in name_lower for x in ['aga', 'giquic', 'colonoscopy', 'endoscop',
                                       'extraintestinal', 'erw']):
        return "GI-Specific"

    # Cardiology
    if any(x in name_lower for x in ['cardio', 'echocard', 'carotid', 'heartcentrix',
                                       'stress', 'nuclear', 'perfusion', 'tte']):
        return "Cardiology"

    # Ophthalmology
    if any(x in name_lower for x in ['ophthalmol', 'lens']):
        return "Ophthalmology"

    # Quality Measures
    if any(x in name_lower for x in ['ascquality', 'mips']):
        return "Quality Measures"

    # Medications
    if any(x in name_lower for x in ['prescription', 'medication', 'drug', 'pharmacy',
                                       'ndc', 'renewal', 'administered']):
        return "Medications"

    # Lab & Results
    if any(x in name_lower for x in ['lab', 'specimen', 'interfaceresult',
                                       'interfacerequisition', 'interfacespecimen']):
        return "Lab & Results"

    # Imaging & Documents
    if any(x in name_lower for x in ['imaging']):
        return "Imaging"

    # Documents & Notes
    if any(x in name_lower for x in ['document', 'letter', 'fax', 'addendum',
                                       'attachment', 'docretrieve']):
        return "Documents & Notes"

    # Procedures & Services
    if any(x in name_lower for x in ['service', 'procedure', 'finding', 'impression',
                                       'operative', 'surgical', 'anesthesia', 'aldrete',
                                       'phase', 'asa', 'instrument', 'infusion', 'iv',
                                       'oxygen', 'npo', 'preparation', 'limitation',
                                       'intervention', 'nursing', 'pain', 'coding',
                                       'procedureoverview', 'roundinglist', 'physicalexam']):
        return "Procedures & Services"

    # Vitals
    if any(x in name_lower for x in ['vital', 'bloodpressure', 'physicalmeasurement']):
        return "Vitals"

    # Problems & Diagnoses
    if any(x in name_lower for x in ['diagnosis', 'problem', 'icd']):
        return "Problems & Diagnoses"

    # Patient Portal
    if any(x in name_lower for x in ['portal', 'consent', 'personalhealthrecord']):
        return "Patient Portal"

    # Orders & Referrals
    if any(x in name_lower for x in ['order', 'referral', 'referr']):
        return "Orders & Referrals"

    # Immunizations
    if any(x in name_lower for x in ['immunization', 'vaccine', 'hl7set']):
        return "Immunizations"

    # Questionnaires & Forms
    if any(x in name_lower for x in ['questionnaire', 'form', 'screening',
                                       'functioncognitive', 'pifreview', 'guideline']):
        return "Questionnaires & Forms"

    # Demographics / Person
    if any(x in name_lower for x in ['person', 'gender', 'race', 'ethnicity',
                                       'tribal', 'disability', 'emergency', 'guarantor',
                                       'employment', 'occupation', 'phone', 'email',
                                       'address', 'supportperson', 'relative']):
        return "Demographics"

    # Patient - general patient-related entities
    if 'patient' in name_lower:
        return "Patient"

    # Communication
    if any(x in name_lower for x in ['directmail', 'message', 'syndromic']):
        return "Communications"

    # Telehealth
    if 'telehealth' in name_lower:
        return "Telehealth"

    # Recall
    if 'recall' in name_lower:
        return "Care Management"

    # Chart
    if 'chart' in name_lower:
        return "Chart"

    # Balance reminders
    if 'balance' in name_lower or 'reminder' in name_lower:
        return "Billing & Claims"

    # LDM
    if 'ldm' in name_lower:
        return "Administrative"

    # Interval
    if 'interval' in name_lower:
        return "GI-Specific"

    return "Other"


def main():
    entities = parse_dictionary('main-dict.txt')

    # Add categories and stats per entity
    for entity in entities:
        entity['category'] = categorize_entity(entity['name'])
        entity['field_count'] = len(entity['fields'])

        # Count fields with translation references (meaningful descriptions beyond format)
        fields_with_translation = sum(
            1 for f in entity['fields']
            if f.get('format_or_translation') and
            not f['format_or_translation'].startswith('MM/dd') and
            not f['format_or_translation'].startswith('hh:mm')
        )
        entity['fields_with_translation_ref'] = fields_with_translation

    # Write full inventory
    with open('full-entity-inventory.json', 'w') as f:
        json.dump(entities, f, indent=2)

    # Summary statistics
    total_entities = len(entities)
    total_fields = sum(e['field_count'] for e in entities)

    # All fields with types
    all_types = {}
    for e in entities:
        for field in e['fields']:
            t = field.get('type', 'Unknown')
            all_types[t] = all_types.get(t, 0) + 1

    # Category breakdown
    categories = {}
    for e in entities:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'field_count': 0, 'entities': []}
        categories[cat]['entity_count'] += 1
        categories[cat]['field_count'] += e['field_count']
        categories[cat]['entities'].append(e['name'])

    # Fields with GUID type (foreign keys)
    guid_fields = sum(
        1 for e in entities for f in e['fields']
        if f.get('type') == 'GUID'
    )

    # Fields with translation references
    translation_refs = sum(
        e['fields_with_translation_ref'] for e in entities
    )

    # Fields with max_length defined
    fields_with_length = sum(
        1 for e in entities for f in e['fields']
        if f.get('max_length') is not None
    )

    # Top 20 largest entities
    top_entities = sorted(entities, key=lambda e: e['field_count'], reverse=True)[:20]

    summary = {
        'total_entities': total_entities,
        'total_fields': total_fields,
        'guid_fields': guid_fields,
        'fields_with_translation_refs': translation_refs,
        'fields_with_max_length': fields_with_length,
        'field_types': all_types,
        'categories': {k: {'entity_count': v['entity_count'],
                           'field_count': v['field_count'],
                           'entities': v['entities']}
                       for k, v in sorted(categories.items())},
        'top_20_largest_entities': [
            {'name': e['name'], 'field_count': e['field_count'], 'category': e['category']}
            for e in top_entities
        ]
    }

    with open('summary-stats.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Total entities: {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"GUID (foreign key) fields: {guid_fields}")
    print(f"Fields with translation refs: {translation_refs}")
    print(f"Fields with max_length: {fields_with_length}")
    print(f"\nField types:")
    for t, count in sorted(all_types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")
    print(f"\nCategories:")
    for cat, info in sorted(categories.items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print(f"\nTop 20 largest entities:")
    for e in top_entities:
        print(f"  {e['name']}: {e['field_count']} fields ({e['category']})")


if __name__ == '__main__':
    main()
