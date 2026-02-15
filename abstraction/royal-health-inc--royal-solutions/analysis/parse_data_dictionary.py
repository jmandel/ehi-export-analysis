#!/usr/bin/env python3
"""Parse the B10 data dictionary PDF text to extract CSV file structures and field counts."""

import json
import re

with open("pdf-text.txt", "r") as f:
    text = f.read()

# Split into sections by CSV file headers (e.g., "Patients.csv", "Appointments.csv")
csv_pattern = re.compile(r'^(\w+)\.csv\s*$', re.MULTILINE)
matches = list(csv_pattern.finditer(text))

results = {}
total_fields = 0
total_described = 0

for i, match in enumerate(matches):
    csv_name = match.group(1)
    start = match.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    section = text[start:end]

    # Find field lines: look for lines starting with a field name (word chars)
    # followed by whitespace and a description
    fields = []
    lines = section.split('\n')
    
    current_field = None
    current_desc = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.lower() in ('field', 'description', 'field description'):
            continue
        # Skip table header rows like "Field    Description"
        if re.match(r'^\s*Field\s{2,}Description\s*$', line):
            continue
        
        # Check if this line starts a new field definition
        # Fields start at left margin with a word, followed by spaces and description
        # Skip if the field name is literally "Field" (column header)
        # Use \s+ (not \s{2,}) to catch fields with just one space before description
        field_match = re.match(r'^\s{0,2}(\w[\w_]*)\s{2,}(.+)$', line)
        if not field_match:
            # Try single space for long field names
            field_match = re.match(r'^\s{0,2}([A-Z]\w*_\w+)\s+(.+)$', line)
        if field_match and field_match.group(1) == 'Field':
            continue
        if field_match:
            if current_field:
                fields.append({
                    'name': current_field,
                    'description': current_desc.strip(),
                    'has_description': bool(current_desc.strip())
                })
            current_field = field_match.group(1)
            current_desc = field_match.group(2)
        elif current_field and stripped:
            # Continuation of description
            # Check if this is a field name with no description on same line
            solo_field = re.match(r'^\s{0,2}(\w[\w_]*)\s*$', line)
            if solo_field and not re.match(r'^(the|a|an|for|and|or|if|this|that|in|on|at|to|of|from|by|with|as|is|was|are|were|has|have|had|do|does|did|will|would|could|should|may|might|can|shall|be|been|being)\b', stripped.lower()):
                # Could be a field with no description - save current and start new
                if current_field:
                    fields.append({
                        'name': current_field,
                        'description': current_desc.strip(),
                        'has_description': bool(current_desc.strip())
                    })
                current_field = solo_field.group(1)
                current_desc = ""
            else:
                current_desc += " " + stripped
    
    # Don't forget the last field
    if current_field:
        fields.append({
            'name': current_field,
            'description': current_desc.strip(),
            'has_description': bool(current_desc.strip())
        })
    
    field_count = len(fields)
    described_count = sum(1 for f in fields if f['has_description'])
    total_fields += field_count
    total_described += described_count
    
    results[csv_name] = {
        'file': f'{csv_name}.csv',
        'field_count': field_count,
        'fields_with_description': described_count,
        'fields': fields
    }

# Print summary
print("=" * 70)
print("B10 EHI Export Data Dictionary Summary")
print("=" * 70)
print(f"\nTotal CSV files: {len(results)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {total_described}")
print(f"Description coverage: {total_described/total_fields*100:.1f}%")
print()

print(f"{'CSV File':<25} {'Fields':>8} {'Described':>10} {'Category'}")
print("-" * 70)

# Assign categories based on content
categories = {
    'Patients': 'Demographics',
    'Demographics2': 'Demographics',
    'Appointments': 'Radiology Operations / Insurance',
    'Transactions': 'Billing / Payments',
    'Orders': 'Orders / Referrals',
    'Allergies': 'Clinical',
    'Devices': 'Clinical',
    'Immunizations': 'Clinical',
    'Medications': 'Clinical',
    'Problems': 'Clinical',
    'Procedures': 'Clinical',
    'Vitals': 'Clinical',
}

for name, data in results.items():
    cat = categories.get(name, 'Unknown')
    data['category'] = cat
    print(f"{data['file']:<25} {data['field_count']:>8} {data['fields_with_description']:>10}   {cat}")

print("-" * 70)
print(f"{'TOTAL':<25} {total_fields:>8} {total_described:>10}")

# Category summary
print("\n\nCategory Summary:")
print(f"{'Category':<35} {'Files':>6} {'Fields':>8}")
print("-" * 55)
cat_summary = {}
for name, data in results.items():
    cat = data['category']
    if cat not in cat_summary:
        cat_summary[cat] = {'files': 0, 'fields': 0}
    cat_summary[cat]['files'] += 1
    cat_summary[cat]['fields'] += data['field_count']

for cat, summary in sorted(cat_summary.items()):
    print(f"{cat:<35} {summary['files']:>6} {summary['fields']:>8}")

# Save full results as JSON
with open("full-entity-inventory.json", "w") as f:
    json.dump({
        'summary': {
            'total_csv_files': len(results),
            'total_fields': total_fields,
            'total_fields_with_descriptions': total_described,
            'description_coverage_pct': round(total_described/total_fields*100, 1)
        },
        'category_summary': cat_summary,
        'entities': results
    }, f, indent=2)

print("\n\nFull inventory saved to full-entity-inventory.json")
