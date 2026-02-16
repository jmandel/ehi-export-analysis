#!/usr/bin/env python3
"""
Build the final entity-inventory-full.json and entity-inventory-summary.json
by combining the detailed data dictionary (field-level) with the overview
(table-level descriptions, relationships, metadata).
"""
import json

def main():
    # Load parsed data
    with open('analysis/detailed-dd-parsed.json') as f:
        detailed = json.load(f)
    
    with open('analysis/overview-dd-parsed.json') as f:
        overview = json.load(f)
    
    # Build overview lookup by table name
    ov_lookup = {}
    for t in overview['tables']:
        name = t['table']
        if name and name not in ov_lookup:
            ov_lookup[name] = t
    
    # Normalize groupings for the detailed data
    # Map sub-groupings back to main grouping
    GROUPING_MAP = {
        'Ophth Pretesting': 'Ophth Pretesting',
        'PM Financials': 'PM Financials',
        'Document Management': 'Document',
        'Office Flow': 'Office Flow',
        'CC/HPI': 'CC/HPI',
    }
    
    def normalize_grouping(g):
        for prefix, normalized in GROUPING_MAP.items():
            if g.startswith(prefix):
                return normalized
        return g
    
    # Build entities from detailed DD
    entities = {}
    for field in detailed['fields']:
        table = field['table']
        if not table:
            continue
        
        if table not in entities:
            # Get overview info if available
            ov = ov_lookup.get(table, {})
            grouping = normalize_grouping(field['grouping'])
            
            entities[table] = {
                'name': table,
                'grouping': grouping,
                'description': ov.get('description', ''),
                'relationships': ov.get('relationships', []),
                'longitudinalTracking': ov.get('longitudinalTracking', ''),
                'productVertical': ov.get('productVertical', ''),
                'financialPriority': ov.get('financialPriority', ''),
                'refreshFrequency': ov.get('refreshFrequency', ''),
                'fields': []
            }
        
        entities[table]['fields'].append({
            'name': field['column'],
            'description': field['description'],
            'dataType': field['dataType'],
            'nullable': field['nullable'],
            'fieldLength': field['fieldLength'],
            'valuesCodingSchema': field['valuesCodingSchema'],
        })
    
    # Also add tables from overview that aren't in detailed
    for name, ov in ov_lookup.items():
        if name not in entities and name:
            grouping = ov.get('grouping', '')
            entities[name] = {
                'name': name,
                'grouping': grouping,
                'description': ov.get('description', ''),
                'relationships': ov.get('relationships', []),
                'longitudinalTracking': ov.get('longitudinalTracking', ''),
                'productVertical': ov.get('productVertical', ''),
                'financialPriority': ov.get('financialPriority', ''),
                'refreshFrequency': ov.get('refreshFrequency', ''),
                'fields': [],  # No field-level data available
                'overviewOnly': True
            }
    
    # Sort entities by grouping then name
    entity_list = sorted(entities.values(), key=lambda e: (e['grouping'], e['name']))
    
    # Compute summary statistics
    total_entities = len(entity_list)
    entities_with_fields = sum(1 for e in entity_list if e['fields'])
    total_fields = sum(len(e['fields']) for e in entity_list)
    fields_with_desc = sum(
        1 for e in entity_list for f in e['fields'] if f['description']
    )
    fields_with_type = sum(
        1 for e in entity_list for f in e['fields'] if f['dataType']
    )
    fields_with_nullable = sum(
        1 for e in entity_list for f in e['fields'] if f['nullable'] is not None
    )
    fields_with_values = sum(
        1 for e in entity_list for f in e['fields'] if f['valuesCodingSchema']
    )
    
    # Grouping summary
    grouping_stats = {}
    for e in entity_list:
        g = e['grouping'] or '(ungrouped)'
        if g not in grouping_stats:
            grouping_stats[g] = {'entities': 0, 'fields': 0}
        grouping_stats[g]['entities'] += 1
        grouping_stats[g]['fields'] += len(e['fields'])
    
    # Write full inventory
    full_output = {
        'source': 'ModMed EMA EHI Export Data Dictionary',
        'artifacts': [
            'ModMed-EMA-EHI-Export-Data-Dictionary.pdf (96 pages, overview)',
            'ModMed-EMA-Detailed-Data-Dictionary.pdf (210 pages, field-level)'
        ],
        'extractedAt': '2026-02-16',
        'entities': entity_list
    }
    
    with open('analysis/entity-inventory-full.json', 'w') as f:
        json.dump(full_output, f, indent=2)
    
    # Write summary
    summary = {
        'source': 'ModMed EMA EHI Export Data Dictionary',
        'extractedAt': '2026-02-16',
        'stats': {
            'totalEntities': total_entities,
            'entitiesWithFieldDetail': entities_with_fields,
            'totalFields': total_fields,
            'fieldsWithDescription': fields_with_desc,
            'fieldsWithDescriptionPct': round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
            'fieldsWithDataType': fields_with_type,
            'fieldsWithNullable': fields_with_nullable,
            'fieldsWithValues': fields_with_values,
        },
        'groupings': dict(sorted(grouping_stats.items(), key=lambda x: -x[1]['fields'])),
        'largestEntities': [
            {
                'name': e['name'],
                'grouping': e['grouping'],
                'fieldCount': len(e['fields']),
                'description': e['description'][:120]
            }
            for e in sorted(entity_list, key=lambda e: -len(e['fields']))[:30]
        ],
        'entitiesByGrouping': {
            g: sorted([e['name'] for e in entity_list if e['grouping'] == g])
            for g in sorted(grouping_stats.keys())
        }
    }
    
    with open('analysis/entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total entities: {total_entities}")
    print(f"Entities with field-level detail: {entities_with_fields}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({100*fields_with_desc/total_fields:.1f}%)")
    print(f"Fields with data types: {fields_with_type} ({100*fields_with_type/total_fields:.1f}%)")
    print(f"Fields with nullable: {fields_with_nullable}")
    print(f"Fields with values/coding: {fields_with_values}")
    print(f"\nGroupings:")
    for g, s in sorted(grouping_stats.items(), key=lambda x: -x[1]['fields']):
        print(f"  {g}: {s['entities']} entities, {s['fields']} fields")

if __name__ == '__main__':
    main()
