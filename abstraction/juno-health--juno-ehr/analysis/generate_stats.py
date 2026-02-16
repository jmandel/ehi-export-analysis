"""Generate summary statistics and representative tables for analysis.md"""

import json

with open('full-entity-inventory.json') as f:
    inv = json.load(f)

with open('domain_analysis.json') as f:
    domains = json.load(f)

# Table size distribution
all_tables = []
for schema_key in ['jehr', 'rtvx']:
    for entity in inv['schemas'][schema_key]['entities']:
        all_tables.append({
            'name': entity.get('table_name', ''),
            'schema': schema_key,
            'columns': len(entity.get('columns', [])),
            'has_desc': bool(entity.get('description', '').strip()),
            'fk_count': len(entity.get('foreign_keys', [])),
            'pk_count': len(entity.get('primary_keys', []))
        })

# Column count distribution
col_counts = [t['columns'] for t in all_tables]
print(f"Column count distribution:")
print(f"  Min: {min(col_counts)}")
print(f"  Max: {max(col_counts)}")
print(f"  Mean: {sum(col_counts)/len(col_counts):.1f}")
print(f"  Median: {sorted(col_counts)[len(col_counts)//2]}")
print(f"  1 col: {sum(1 for c in col_counts if c <= 1)}")
print(f"  2-5 cols: {sum(1 for c in col_counts if 2 <= c <= 5)}")
print(f"  6-10 cols: {sum(1 for c in col_counts if 6 <= c <= 10)}")
print(f"  11-20 cols: {sum(1 for c in col_counts if 11 <= c <= 20)}")
print(f"  21-50 cols: {sum(1 for c in col_counts if 21 <= c <= 50)}")
print(f"  51-100 cols: {sum(1 for c in col_counts if 51 <= c <= 100)}")
print(f"  100+ cols: {sum(1 for c in col_counts if c > 100)}")

# Tables with FKs
fk_tables = sum(1 for t in all_tables if t['fk_count'] > 0)
print(f"\nTables with foreign keys: {fk_tables} / {len(all_tables)}")

# Print domain summary as markdown table
print("\n\n=== Domain Summary Table ===")
print(f"| Domain | Tables | Columns | % of Total |")
print(f"|---|---|---|---|")
total_cols = sum(d['columns'] for d in domains.values())
for domain in sorted(domains.keys(), key=lambda d: domains[d]['columns'], reverse=True):
    d = domains[domain]
    pct = d['columns'] / total_cols * 100
    if d['columns'] >= 20:  # Skip tiny domains
        print(f"| {domain} | {d['tables']} | {d['columns']} | {pct:.1f}% |")

# Count lookup tables vs data tables
lk_count = sum(1 for t in all_tables if t['name'].startswith('LK'))
lk_cols = sum(t['columns'] for t in all_tables if t['name'].startswith('LK'))
print(f"\nLookup tables (LK prefix): {lk_count} tables, {lk_cols} columns")
print(f"Data tables: {len(all_tables) - lk_count} tables, {sum(c for c in col_counts) - lk_cols} columns")

# Save summary stats
stats = {
    'total_tables': len(all_tables),
    'total_tables_jehr': inv['schemas']['jehr']['stats']['total_tables'],
    'total_tables_rtvx': inv['schemas']['rtvx']['stats']['total_tables'],
    'total_columns': sum(col_counts),
    'total_foreign_keys': sum(t['fk_count'] for t in all_tables),
    'tables_with_fks': fk_tables,
    'tables_with_descriptions': sum(1 for t in all_tables if t['has_desc']),
    'columns_with_descriptions': inv['combined_stats']['columns_with_descriptions'],
    'description_rate': inv['combined_stats']['description_rate'],
    'lookup_tables': lk_count,
    'lookup_table_columns': lk_cols,
    'data_tables': len(all_tables) - lk_count,
    'data_table_columns': sum(c for c in col_counts) - lk_cols,
    'col_distribution': {
        '1': sum(1 for c in col_counts if c <= 1),
        '2-5': sum(1 for c in col_counts if 2 <= c <= 5),
        '6-10': sum(1 for c in col_counts if 6 <= c <= 10),
        '11-20': sum(1 for c in col_counts if 11 <= c <= 20),
        '21-50': sum(1 for c in col_counts if 21 <= c <= 50),
        '51-100': sum(1 for c in col_counts if 51 <= c <= 100),
        '100+': sum(1 for c in col_counts if c > 100)
    },
    'largest_table': max(all_tables, key=lambda t: t['columns'])['name'],
    'largest_table_cols': max(col_counts)
}

with open('summary_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("\nSaved summary_stats.json")
