#!/usr/bin/env python3
"""
Parse both Picasso EHI Export PDFs to produce entity-inventory-full.json
and entity-inventory-summary.json.

Uses pdftotext output to extract data classes and their columns.
The Picasso-specific PDF (V1_0-1.pdf) is the actual Picasso EHI export doc.
The V1_0-1-1.pdf is the Amazing Charts sibling product doc (included for reference).
"""

import json
import re
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')

def extract_pdf_text(filename):
    path = os.path.join(DOWNLOADS, filename)
    result = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True)
    return result.stdout

def parse_picasso_pdf():
    """Parse the Picasso-specific EHI export PDF (V1_0-1.pdf)."""
    text = extract_pdf_text('Picasso-EHI-Export-Documentation-V1_0-1.pdf')
    
    # Split into lines and find the data class table
    lines = text.split('\n')
    
    data_classes = []
    current_class = None
    current_columns = []
    
    # Find lines after "Below is a listing of the Data Classes"
    in_table = False
    for line in lines:
        stripped = line.strip()
        
        if 'Below is a listing' in stripped:
            in_table = True
            continue
        
        if not in_table:
            continue
        
        # Skip header lines
        if stripped.startswith('Data Class') or stripped.startswith('Name') or stripped == '':
            continue
        
        # Skip page headers/footers
        if 'Picasso EHI Export' in stripped:
            continue
        if re.match(r'^\d+$', stripped):
            continue
        
        # A new data class starts with a name in the left column followed by columns
        # Check if line has content starting at a left-ish position
        # Data class names appear at the start of the line (indented slightly)
        # Column names are further right
        
        # Try to detect if this line starts a new data class
        # Data class names are left-aligned, columns are right-aligned
        match = re.match(r'^\s{0,5}(\S[\w\s/]+?)\s{3,}([A-Z_,\s]+)$', line)
        if match:
            # Save previous class
            if current_class:
                data_classes.append({
                    'name': current_class,
                    'columns': current_columns
                })
            current_class = match.group(1).strip()
            col_text = match.group(2).strip()
            current_columns = [c.strip() for c in col_text.split(',') if c.strip()]
        else:
            # Continuation line - just columns
            col_match = re.match(r'^\s{10,}([A-Z_,\s]+)$', line)
            if col_match and current_class:
                col_text = col_match.group(1).strip()
                cols = [c.strip() for c in col_text.split(',') if c.strip()]
                current_columns.extend(cols)
    
    # Save last class
    if current_class:
        data_classes.append({
            'name': current_class,
            'columns': current_columns
        })
    
    return data_classes

def parse_amazing_charts_pdf():
    """Parse the Amazing Charts EHI export PDF (V1_0-1-1.pdf)."""
    text = extract_pdf_text('Picasso-EHI-Export-Documentation-V1_0-1-1.pdf')
    
    lines = text.split('\n')
    
    data_classes = []
    current_class = None
    current_columns = []
    
    in_table = False
    for line in lines:
        stripped = line.strip()
        
        if 'Below is a listing' in stripped:
            in_table = True
            continue
        
        if not in_table:
            continue
        
        # Skip header lines and page footers
        if stripped.startswith('Data Class Name') or stripped == '':
            continue
        if 'Amazing Charts EHI Export' in stripped:
            continue
        if re.match(r'^\d+$', stripped):
            continue
        if stripped.startswith('Column Headings'):
            continue
        
        # New data class: name on left, columns on right
        match = re.match(r'^\s{0,5}(\S[\w\s/()&\-]+?)\s{3,}([A-Za-z_,\s\d()]+)$', line)
        if match:
            name = match.group(1).strip()
            col_text = match.group(2).strip()
            
            # Check if this is really a new class or continuation
            # New classes have recognizable names
            if name and not name.startswith(',') and len(name) > 2:
                if current_class:
                    data_classes.append({
                        'name': current_class,
                        'columns': current_columns
                    })
                current_class = name
                current_columns = [c.strip() for c in col_text.split(',') if c.strip()]
            else:
                # Continuation
                cols = [c.strip() for c in stripped.split(',') if c.strip()]
                current_columns.extend(cols)
        else:
            # Continuation line
            if current_class and stripped:
                cols = [c.strip() for c in stripped.split(',') if c.strip()]
                current_columns.extend(cols)
    
    if current_class:
        data_classes.append({
            'name': current_class,
            'columns': current_columns
        })
    
    return data_classes

def build_entity_inventory(data_classes, source_file, product_name):
    """Build the entity inventory from parsed data classes."""
    entities = []
    for dc in data_classes:
        fields = []
        for col in dc['columns']:
            fields.append({
                'name': col,
                'type': None,  # Not provided in the documentation
                'description': None,  # Not provided in the documentation
                'nullable': None,
                'max_length': None,
                'foreign_key': None,
                'value_set': None,
                'coded_values': None,
                'default_value': None,
                'example_data': None
            })
        entities.append({
            'entity_name': dc['name'],
            'source_file': source_file,
            'product': product_name,
            'field_count': len(fields),
            'fields': fields
        })
    return entities

def main():
    # Parse Picasso PDF
    picasso_classes = parse_picasso_pdf()
    
    # Cross-check with enrichment data
    enrichment_path = os.path.join(DOWNLOADS, 'enrichment', 'picasso-data-classes.json')
    with open(enrichment_path) as f:
        enrichment = json.load(f)
    
    print("=== Picasso EHI Export ===")
    print(f"Parsed {len(picasso_classes)} data classes from PDF")
    print(f"Enrichment has {len(enrichment['data_classes'])} data classes")
    
    # Use enrichment data since it was carefully parsed - but verify
    # Let's compare
    for i, dc in enumerate(picasso_classes):
        if i < len(enrichment['data_classes']):
            edc = enrichment['data_classes'][i]
            if dc['name'] != edc['name']:
                print(f"  Name mismatch at {i}: '{dc['name']}' vs '{edc['name']}'")
            if len(dc['columns']) != edc['column_count']:
                print(f"  Column count mismatch for {dc['name']}: {len(dc['columns'])} vs {edc['column_count']}")
    
    # Use enrichment data as the authoritative source since it matches the PDF
    picasso_entities = []
    for dc in enrichment['data_classes']:
        fields = []
        for col in dc['columns']:
            fields.append({
                'name': col,
                'type': None,
                'description': None,
                'nullable': None,
                'max_length': None,
                'foreign_key': None,
                'value_set': None,
                'coded_values': None,
                'default_value': None,
                'example_data': None
            })
        picasso_entities.append({
            'entity_name': dc['name'],
            'source_file': 'Picasso-EHI-Export-Documentation-V1_0-1.pdf',
            'product': 'Picasso',
            'field_count': len(fields),
            'fields': fields
        })
    
    # Parse Amazing Charts PDF
    ac_enrichment_path = os.path.join(DOWNLOADS, 'enrichment', 'amazing-charts-data-classes.json')
    with open(ac_enrichment_path) as f:
        ac_enrichment = json.load(f)
    
    print(f"\n=== Amazing Charts EHI Export (sibling product, same URL) ===")
    print(f"Enrichment has {len(ac_enrichment['data_classes'])} data classes")
    
    ac_entities = []
    for dc in ac_enrichment['data_classes']:
        fields = []
        for col in dc['columns']:
            fields.append({
                'name': col,
                'type': None,
                'description': None,
                'nullable': None,
                'max_length': None,
                'foreign_key': None,
                'value_set': None,
                'coded_values': None,
                'default_value': None,
                'example_data': None
            })
        ac_entities.append({
            'entity_name': dc['name'],
            'source_file': 'Picasso-EHI-Export-Documentation-V1_0-1-1.pdf',
            'product': 'Amazing Charts',
            'field_count': len(fields),
            'fields': fields
        })
    
    # Build full inventory (Picasso is the primary product)
    full_inventory = {
        'product': 'Picasso',
        'developer': 'Doc-tor.com (Harris Healthcare)',
        'extraction_date': '2026-02-16',
        'primary_source': 'Picasso-EHI-Export-Documentation-V1_0-1.pdf',
        'additional_source': 'Picasso-EHI-Export-Documentation-V1_0-1-1.pdf (Amazing Charts - sibling product)',
        'export_format': 'CSV',
        'notes': [
            'The CHPL-registered EHI documentation URL points to the Amazing Charts PDF (V1_0-1-1.pdf)',
            'A separate Picasso-specific PDF (V1_0-1.pdf) was found on the mandatory disclosures page',
            'No field descriptions, types, value sets, or relationships are provided in either document',
            'Column names are the only documentation provided'
        ],
        'picasso_entities': picasso_entities,
        'amazing_charts_entities': ac_entities
    }
    
    # Save full inventory
    output_path = os.path.join(os.path.dirname(__file__), 'entity-inventory-full.json')
    with open(output_path, 'w') as f:
        json.dump(full_inventory, f, indent=2)
    print(f"\nSaved full inventory to {output_path}")
    
    # Build summary
    total_picasso_fields = sum(e['field_count'] for e in picasso_entities)
    total_ac_fields = sum(e['field_count'] for e in ac_entities)
    
    # Categorize Picasso entities by domain
    domain_mapping = {
        'Demographics': ['Demographics'],
        'Clinical - Encounters': ['Encounters'],
        'Clinical - Problems/Diagnoses': ['Assessment', 'Problems'],
        'Clinical - Medications': ['Medications'],
        'Clinical - Allergies': ['Allergies'],
        'Clinical - Immunizations': ['Immunizations'],
        'Clinical - Vitals': ['Vitals'],
        'Clinical - Labs': ['Labs'],
        'Clinical - Orders': ['Orders'],
        'Clinical - Notes': ['Clinical Notes'],
        'Clinical - Procedures': ['Procedures'],
        'Clinical - Care Team': ['Care Team'],
        'Clinical - Family History': ['Family History'],
        'Clinical - Health Concerns': ['Health Concerns'],
        'Clinical - Plan of Treatment': ['Plan Of Treatment'],
        'Clinical - Social History': ['Social History'],
        'Clinical - Tobacco': ['Tobacco'],
        'Clinical - Implantable Devices': ['Implantable Devices'],
        'Clinical - Tasks': ['Tasks'],
        'Insurance': ['Health Insurance'],
    }
    
    category_stats = {}
    for category, entity_names in domain_mapping.items():
        matching = [e for e in picasso_entities if e['entity_name'] in entity_names]
        category_stats[category] = {
            'entity_count': len(matching),
            'total_fields': sum(e['field_count'] for e in matching),
            'entities': [e['entity_name'] for e in matching]
        }
    
    # Find provider-related columns (repeated across many entities)
    provider_cols = ['PROV_LAST', 'PROV_FIRST', 'PROV_PHONE', 'PROV_TITLE', 
                     'PROV_DEA', 'PROV_LIC', 'PROV_EMAIL', 'PROV_UPIN', 'PROVIDERSID']
    entities_with_provider = 0
    provider_field_count = 0
    for e in picasso_entities:
        prov_fields = [f for f in e['fields'] if f['name'] in provider_cols]
        if prov_fields:
            entities_with_provider += 1
            provider_field_count += len(prov_fields)
    
    summary = {
        'product': 'Picasso',
        'picasso_export': {
            'total_entities': len(picasso_entities),
            'total_fields': total_picasso_fields,
            'fields_with_descriptions': 0,
            'fields_with_types': 0,
            'description_percentage': 0.0,
            'export_format': 'CSV',
            'entities_by_field_count': sorted(
                [{'name': e['entity_name'], 'fields': e['field_count']} for e in picasso_entities],
                key=lambda x: -x['fields']
            ),
            'category_breakdown': category_stats,
            'provider_column_analysis': {
                'entities_with_provider_columns': entities_with_provider,
                'total_provider_field_occurrences': provider_field_count,
                'note': 'Provider info (name, DEA, license, etc.) is denormalized into most entities'
            }
        },
        'amazing_charts_export_for_reference': {
            'total_entities': len(ac_entities),
            'total_fields': total_ac_fields,
            'note': 'Sibling product doc found at same CHPL URL - NOT the Picasso export'
        }
    }
    
    summary_path = os.path.join(os.path.dirname(__file__), 'entity-inventory-summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary to {summary_path}")
    
    # Print summary stats
    print(f"\n=== PICASSO SUMMARY ===")
    print(f"Data classes: {len(picasso_entities)}")
    print(f"Total fields: {total_picasso_fields}")
    print(f"Fields with descriptions: 0 (none provided)")
    print(f"Fields with types: 0 (none provided)")
    print(f"\nEntities by size:")
    for e in sorted(picasso_entities, key=lambda x: -x['field_count']):
        print(f"  {e['entity_name']:25s} {e['field_count']:3d} fields")
    
    print(f"\nProvider columns appear in {entities_with_provider}/{len(picasso_entities)} entities ({provider_field_count} total occurrences)")
    
    print(f"\n=== AMAZING CHARTS SUMMARY (for reference) ===")
    print(f"Data classes: {len(ac_entities)}")
    print(f"Total fields: {total_ac_fields}")
    for e in sorted(ac_entities, key=lambda x: -x['field_count']):
        print(f"  {e['entity_name']:35s} {e['field_count']:3d} fields")

if __name__ == '__main__':
    main()
