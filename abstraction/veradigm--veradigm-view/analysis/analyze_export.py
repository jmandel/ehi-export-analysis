#!/usr/bin/env python3
"""Analyze Veradigm View EHI export documentation.
Reads the full-entity-inventory.json and produces summary statistics."""

import json

with open('full-entity-inventory.json') as f:
    inventory = json.load(f)

print("=" * 70)
print("VERADIGM VIEW EHI EXPORT ANALYSIS SUMMARY")
print("=" * 70)

print(f"\nTotal entities: {inventory['total_entities']}")
print(f"Total fields: {inventory['total_fields']}")

print("\n--- Field Description Quality ---")
fq = inventory['field_quality']
print(f"  With descriptions: {fq['fields_with_descriptions']} ({fq['description_rate']}%)")
print(f"  Meaningful descriptions: {fq['fields_with_meaningful_descriptions']} ({fq['meaningful_description_rate']}%)")
print(f"  Trivial descriptions: {fq['fields_with_trivial_descriptions']}")
print(f"  No descriptions: {fq['fields_without_descriptions']}")

print("\n--- Data Types ---")
for dtype, count in sorted(inventory['data_types'].items(), key=lambda x: -x[1]):
    print(f"  {dtype}: {count}")

print("\n--- Categories ---")
print(f"{'Category':<30} {'Entities':>8} {'Fields':>8}")
print("-" * 50)
for cat, info in sorted(inventory['categories'].items(), key=lambda x: -x[1]['field_count']):
    print(f"{cat:<30} {info['entity_count']:>8} {info['field_count']:>8}")
print("-" * 50)
print(f"{'TOTAL':<30} {inventory['total_entities']:>8} {inventory['total_fields']:>8}")

print("\n--- Top 20 Entities by Field Count ---")
sorted_entities = sorted(inventory['entities'], key=lambda x: -x['field_count'])
print(f"{'Entity':<50} {'Fields':>6} {'Category':<30}")
print("-" * 90)
for e in sorted_entities[:20]:
    print(f"{e['slug']:<50} {e['field_count']:>6} {e['category']:<30}")

print("\n--- Smallest Entities (≤5 fields) ---")
for e in sorted_entities:
    if e['field_count'] <= 5:
        print(f"  {e['slug']}: {e['field_count']} fields ({e['category']})")

print("\n--- Potential Foreign Key Relationships ---")
# Count Guid and Guid? fields that reference other entities
fk_fields = []
for e in inventory['entities']:
    for f in e['fields']:
        if f['data_type'] in ('Guid', 'Guid?') and 'Guid' in f['name']:
            fk_fields.append({
                'entity': e['slug'],
                'field': f['name'],
                'type': f['data_type']
            })

print(f"  Total Guid/Guid? fields: {len(fk_fields)}")
# Common FK patterns
fk_names = {}
for fk in fk_fields:
    name = fk['field']
    fk_names[name] = fk_names.get(name, 0) + 1
print("  Most common FK field names:")
for name, count in sorted(fk_names.items(), key=lambda x: -x[1])[:15]:
    print(f"    {name}: used in {count} entities")

# Save summary stats to a file
summary = {
    'total_entities': inventory['total_entities'],
    'total_fields': inventory['total_fields'],
    'field_quality': inventory['field_quality'],
    'data_types': inventory['data_types'],
    'categories': {k: {'entity_count': v['entity_count'], 'field_count': v['field_count']}
                   for k, v in inventory['categories'].items()},
    'top_20_entities': [{'slug': e['slug'], 'fields': e['field_count'], 'category': e['category']}
                        for e in sorted_entities[:20]],
    'entities_with_5_or_fewer_fields': [{'slug': e['slug'], 'fields': e['field_count'], 'category': e['category']}
                                         for e in sorted_entities if e['field_count'] <= 5]
}
with open('summary-stats.json', 'w') as f:
    json.dump(summary, f, indent=2)
print("\nSummary stats saved to summary-stats.json")
