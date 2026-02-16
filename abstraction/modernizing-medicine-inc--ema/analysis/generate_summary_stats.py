#!/usr/bin/env python3
"""Generate summary statistics for the analysis.md from parsed data.

Combines overview table inventory (420 tables, 19 groupings) and 
detailed data dictionary (257 tables, 5250 fields, 16 groupings) 
to produce consolidated statistics.
"""

import json

# Load parsed data
with open('/home/jmandel/hobby/ehi-export-analysis/abstraction/modernizing-medicine-inc--ema/analysis/overview-tables-parsed.json') as f:
    overview = json.load(f)

with open('/home/jmandel/hobby/ehi-export-analysis/abstraction/modernizing-medicine-inc--ema/analysis/full-entity-inventory.json') as f:
    detailed = json.load(f)

print("=" * 70)
print("SUMMARY STATISTICS FOR ANALYSIS")
print("=" * 70)

print(f"\n--- OVERVIEW DATA DICTIONARY (96 pages) ---")
print(f"Total table entries: {overview['totalTables']}")
print(f"Groupings: {len(overview['groupingSummary'])}")
print(f"\nGrouping breakdown (overview):")
for g, count in sorted(overview['groupingSummary'].items(), key=lambda x: -x[1]):
    print(f"  {g}: {count} tables")

print(f"\n--- DETAILED DATA DICTIONARY (210 pages) ---")
stats = detailed['stats']
print(f"Total fields: {stats['totalFields']}")
print(f"Total tables (with field-level detail): {stats['totalTables']}")
print(f"Fields with description: {stats['fieldsWithDescription']} ({stats['descriptionPct']}%)")
print(f"Fields with data type: {stats['fieldsWithType']} ({stats['typePct']}%)")
print(f"Fields nullable=True: {stats.get('fieldsNullableTrue', 'N/A')}")
print(f"Fields nullable=False: {stats.get('fieldsNullableFalse', 'N/A')}")

print(f"\nData type distribution:")
for dt, count in stats['dataTypeDistribution'].items():
    print(f"  {dt}: {count}")

print(f"\nGrouping breakdown (detailed - field counts):")
for g, gs in sorted(detailed['groupingStats'].items(), key=lambda x: -x[1]['fields']):
    print(f"  {g}: {gs['tables']} tables, {gs['fields']} fields")

print(f"\nTop 20 tables by field count:")
top_tables = sorted(detailed['entities'], key=lambda x: -x['fieldCount'])[:20]
for t in top_tables:
    print(f"  {t['table']} ({t['normalizedGrouping']}): {t['fieldCount']} fields")

# Merge groupings from both sources for unified view
print(f"\n--- UNIFIED GROUPING VIEW ---")
all_groupings = set(overview['groupingSummary'].keys()) | set(detailed['groupingStats'].keys())
# Normalize overview groupings
NORM = {'Document': 'Document Management'}
unified = {}
for g in all_groupings:
    norm_g = NORM.get(g, g)
    if norm_g not in unified:
        unified[norm_g] = {'overviewTables': 0, 'detailedTables': 0, 'fields': 0}
    unified[norm_g]['overviewTables'] += overview['groupingSummary'].get(g, 0)
    gs = detailed['groupingStats'].get(g, {})
    unified[norm_g]['detailedTables'] += gs.get('tables', 0)
    unified[norm_g]['fields'] += gs.get('fields', 0)

print(f"{'Grouping':<25} {'Ov.Tables':<12} {'Det.Tables':<12} {'Fields':<10}")
print("-" * 59)
for g in sorted(unified.keys(), key=lambda x: -unified[x]['fields']):
    u = unified[g]
    print(f"{g:<25} {u['overviewTables']:<12} {u['detailedTables']:<12} {u['fields']:<10}")

# Save unified stats
output = {
    'overviewStats': {
        'totalTables': overview['totalTables'],
        'groupings': len(overview['groupingSummary'])
    },
    'detailedStats': stats,
    'unifiedGroupings': unified,
    'topTablesByFieldCount': [
        {'table': t['table'], 'grouping': t['normalizedGrouping'], 'fieldCount': t['fieldCount']}
        for t in top_tables
    ]
}

with open('/home/jmandel/hobby/ehi-export-analysis/abstraction/modernizing-medicine-inc--ema/analysis/summary-stats.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\nSaved summary-stats.json")
