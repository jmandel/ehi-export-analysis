"""
Generate summary statistics from full-entity-inventory.json
for the InPracSys EHI export analysis.
"""

import json

with open('full-entity-inventory.json') as f:
    resources = json.load(f)

total_resources = len(resources)
total_fields = sum(len(r['response_fields']) for r in resources)

# Count fields with descriptions and types
fields_with_desc = 0
fields_with_type = 0
fields_with_cardinality = 0

for r in resources:
    for field in r['response_fields']:
        if field.get('Description', '').strip():
            fields_with_desc += 1
        if field.get('Type', '').strip():
            fields_with_type += 1
        if field.get('Cardinality', '').strip():
            fields_with_cardinality += 1

desc_pct = round(100 * fields_with_desc / total_fields, 1) if total_fields > 0 else 0
type_pct = round(100 * fields_with_type / total_fields, 1) if total_fields > 0 else 0

# Count resources with sample JSON, with non-standard patterns
resources_with_sample = sum(1 for r in resources if r.get('sample_json'))
resources_with_nonstandard = 0
for r in resources:
    sj = r.get('sample_json', '') or ''
    if 'ValueElement' in sj or 'SystemElement' in sj or 'CodeElement' in sj or 'TotalElement' in sj:
        resources_with_nonstandard += 1

# Resource-by-resource breakdown
print("=" * 70)
print("InPracSys FHIR API Documentation - Summary Statistics")
print("=" * 70)
print(f"Total resources documented:        {total_resources}")
print(f"Total response fields:             {total_fields}")
print(f"Fields with descriptions:          {fields_with_desc} ({desc_pct}%)")
print(f"Fields with types:                 {fields_with_type} ({type_pct}%)")
print(f"Fields with cardinality:           {fields_with_cardinality}")
print(f"Resources with sample JSON:        {resources_with_sample}")
print(f"Resources with non-standard JSON:  {resources_with_nonstandard}")
print()
print(f"{'Resource':<40} {'Fields':>6}  {'Desc':>5}  {'Types':>5}  {'Sample':>6}")
print("-" * 70)

for r in resources:
    name = r['name']
    fc = len(r['response_fields'])
    desc = sum(1 for f in r['response_fields'] if f.get('Description', '').strip())
    types = sum(1 for f in r['response_fields'] if f.get('Type', '').strip())
    has_sample = 'Yes' if r.get('sample_json') else 'No'
    print(f"{name:<40} {fc:>6}  {desc:>5}  {types:>5}  {has_sample:>6}")

print("-" * 70)
print(f"{'TOTAL':<40} {total_fields:>6}  {fields_with_desc:>5}  {fields_with_type:>5}")

# Also output as JSON for reference
stats = {
    'total_resources': total_resources,
    'total_response_fields': total_fields,
    'fields_with_descriptions': fields_with_desc,
    'fields_with_descriptions_pct': desc_pct,
    'fields_with_types': fields_with_type,
    'fields_with_types_pct': type_pct,
    'resources_with_sample_json': resources_with_sample,
    'resources_with_nonstandard_json': resources_with_nonstandard,
    'per_resource': []
}
for r in resources:
    stats['per_resource'].append({
        'name': r['name'],
        'field_count': len(r['response_fields']),
        'fields_with_descriptions': sum(1 for f in r['response_fields'] if f.get('Description', '').strip()),
        'fields_with_types': sum(1 for f in r['response_fields'] if f.get('Type', '').strip()),
        'has_sample_json': bool(r.get('sample_json')),
    })

with open('summary-stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("\nSaved summary-stats.json")
