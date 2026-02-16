#!/usr/bin/env python3
"""
Parse all Oracle Health EHI export artifacts into a unified entity inventory.

Sources:
1. MySQL data model (from enrichment/mysql-model-tables.json) - 6,604 tables, 129,148 columns
2. HDI Longitudinal Record (from health-data-intelligence-ehi-export-data-format-specifications.pdf)
3. Document Imaging schema (from PDF)
4. Non-DICOM column definitions (from PDF)
5. DICOM data structure (from PDF)

Outputs:
- entity-inventory-full.json: complete entity/field inventory
- entity-inventory-summary.json: aggregated stats
"""

import json
import subprocess
import re
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).parent.parent

def load_mysql_model():
    """Load pre-parsed MySQL model from enrichment."""
    with open(BASE / "downloads/enrichment/mysql-model-tables.json") as f:
        tables = json.load(f)
    return tables

def parse_hdi_entities():
    """Parse HDI Longitudinal Record entities from PDF text."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(BASE / "downloads/health-data-intelligence-ehi-export-data-format-specifications.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # The PDF has entity sections starting with bold markers "**" then entity name
    # and "FullName:" line, then description, then field tables
    entities = []
    
    # Split into pages (form feeds)
    lines = text.split('\n')
    
    current_entity = None
    current_fields = []
    in_field_table = False
    field_header_seen = False
    current_field = None
    description_lines = []
    collecting_description = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect entity headers - they appear as " **" followed by entity name
        if line == '**' or line == '*':
            # Next non-empty line should be entity name
            if current_entity:
                if current_field:
                    current_fields.append(current_field)
                current_entity['fields'] = current_fields
                entities.append(current_entity)
            
            j = i + 1
            entity_name = ''
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                entity_name = lines[j].strip()
            
            # Look for FullName
            full_name = ''
            k = j + 1
            while k < len(lines) and k < j + 5:
                if 'FullName:' in lines[k] or 'FullName' in lines[k]:
                    # Collect full name (may span lines)
                    fn_line = lines[k]
                    if ':' in fn_line:
                        full_name = fn_line.split(':', 1)[1].strip()
                    if not full_name and k + 1 < len(lines):
                        full_name = lines[k+1].strip()
                    break
                k += 1
            
            current_entity = {
                'name': entity_name,
                'full_name': full_name,
                'description': '',
                'type': 'hdi_entity'
            }
            current_fields = []
            in_field_table = False
            field_header_seen = False
            current_field = None
            description_lines = []
            collecting_description = True
            i = k + 1 if k < len(lines) else j + 1
            continue
        
        # Detect if this is an enum (Symbols section)
        if line == 'Symbols' and current_entity:
            collecting_description = False
            current_entity['entity_type'] = 'enum'
            symbols = []
            j = i + 1
            while j < len(lines):
                sym_line = lines[j].strip()
                if sym_line == '**' or sym_line == '*' or (sym_line and sym_line.startswith('FullName')):
                    break
                if sym_line and sym_line not in ('', 'Symbols'):
                    symbols.append(sym_line)
                j += 1
            current_entity['symbols'] = symbols
            i = j
            continue
        
        # Detect field table header
        if current_entity and ('Field name' in line and 'Type' in line):
            collecting_description = False
            if description_lines:
                current_entity['description'] = ' '.join(description_lines).strip()
                description_lines = []
            in_field_table = True
            field_header_seen = True
            i += 1
            continue
        
        # Collect description lines before field table
        if collecting_description and current_entity and line and not line.startswith('FullName'):
            # Skip the entity name line if it repeats
            if line != current_entity['name']:
                description_lines.append(line)
        
        # Parse field rows in the table
        if in_field_table and current_entity and line:
            # Field rows have: field_name, type, description
            # Use position-based parsing since columns are space-separated
            raw = lines[i]
            
            # Check if this looks like a new field (starts with lowercase letter at left margin or indented)
            # Fields typically start with a letter and have type info
            parts = raw.split()
            if len(parts) >= 2:
                potential_name = parts[0]
                # Is this a new field name? Field names are camelCase or lowercase
                if (potential_name[0].islower() or potential_name[0] == '_') and not potential_name.startswith('com.') and potential_name not in ('nullable', 'Array', 'of', 'string', 'long', 'double', 'boolean', 'int', 'Map', 'map'):
                    if current_field:
                        current_fields.append(current_field)
                    
                    # Parse the type and description from the rest
                    field_type = ''
                    desc = ''
                    # Try to identify type columns
                    rest = ' '.join(parts[1:])
                    # Common types: nullable, Array of, string, long, double, Code, etc.
                    type_keywords = ['nullable', 'Array of', 'Map of', 'string', 'long', 'double', 'boolean', 'int', 'Code']
                    
                    current_field = {
                        'name': potential_name,
                        'type': rest[:80] if len(rest) > 0 else '',
                        'description': ''
                    }
                elif current_field:
                    # Continuation of description
                    current_field['description'] += ' ' + line
            elif current_field and line:
                current_field['description'] += ' ' + line
        
        i += 1
    
    # Don't forget the last entity
    if current_entity:
        if current_field:
            current_fields.append(current_field)
        current_entity['fields'] = current_fields
        entities.append(current_entity)
    
    return entities

def parse_hdi_entities_v2():
    """Better HDI parser using section-based splitting."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(BASE / "downloads/health-data-intelligence-ehi-export-data-format-specifications.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Split on the bold "**" markers which appear on their own line
    # Each section is: ** \n EntityName \n FullName: ... \n description \n Field table or Symbols
    
    # First, split by form feed to get pages, then rejoin 
    # Use regex to find entity boundaries
    # Pattern: line with just "**" followed by entity name
    
    sections = re.split(r'\n\s*\*\*?\s*\n', text)
    
    entities = []
    
    for section in sections[1:]:  # Skip the header/title section
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        # First non-empty line is entity name
        entity_name = ''
        idx = 0
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            continue
        entity_name = lines[idx].strip()
        idx += 1
        
        # Look for FullName
        full_name = ''
        while idx < len(lines):
            if 'FullName' in lines[idx]:
                # May be on same line or next
                fn_text = lines[idx]
                if ':' in fn_text:
                    full_name = fn_text.split(':', 1)[1].strip()
                idx += 1
                # Full name may continue on next line
                while idx < len(lines) and lines[idx].strip() and 'FullName' not in lines[idx] and lines[idx].strip()[0].islower():
                    if not full_name:
                        full_name = lines[idx].strip()
                    else:
                        full_name += lines[idx].strip()
                    idx += 1
                break
            idx += 1
        
        # Collect description until we hit "Field name" or "Symbols"
        description_parts = []
        while idx < len(lines):
            l = lines[idx].strip()
            if 'Field name' in l and 'Type' in l:
                break
            if l == 'Symbols':
                break
            if l and not l.startswith('FullName') and l != entity_name:
                description_parts.append(l)
            idx += 1
        
        description = ' '.join(description_parts).strip()
        
        entity = {
            'name': entity_name,
            'full_name': full_name,
            'description': description,
            'source': 'hdi_longitudinal_record'
        }
        
        # Check if it's an enum (Symbols section)
        if idx < len(lines) and lines[idx].strip() == 'Symbols':
            entity['entity_type'] = 'enum'
            symbols = []
            idx += 1
            while idx < len(lines):
                sl = lines[idx].strip()
                if sl and sl not in ('Symbols',):
                    symbols.append(sl)
                idx += 1
            entity['symbols'] = symbols
            entity['fields'] = []
        elif idx < len(lines) and 'Field name' in lines[idx]:
            # Parse field table
            idx += 1  # skip header
            fields = []
            current_field = None
            
            while idx < len(lines):
                raw = lines[idx]
                stripped = raw.strip()
                
                if not stripped:
                    idx += 1
                    continue
                
                # Skip page headers/footers
                if 'Poprecord Entity Types' in stripped or 'Oracle Health-IT' in stripped:
                    idx += 1
                    continue
                if re.match(r'^\d+\s*$', stripped):
                    idx += 1
                    continue
                    
                # Detect new field: starts with a word at or near the left margin
                # Fields have name, type, description in columns
                parts = stripped.split()
                if parts:
                    first = parts[0]
                    # New field if starts with lowercase letter and isn't a type keyword
                    is_type_word = first in ('nullable', 'Array', 'of', 'Map', 'string', 'long', 'double', 'boolean', 'int')
                    is_continuation = first[0].isupper() and first not in ('Array', 'Map', 'SELF', 'PROVIDER')
                    
                    # Check column position - field names start early
                    leading_spaces = len(raw) - len(raw.lstrip())
                    
                    if leading_spaces < 3 and (first[0].islower() or first.startswith('_')) and not is_type_word:
                        # New field
                        if current_field:
                            current_field['description'] = current_field['description'].strip()
                            fields.append(current_field)
                        current_field = {
                            'name': first,
                            'type': '',
                            'nullable': False,
                            'description': ''
                        }
                        # Rest of the line has type and description
                        rest = ' '.join(parts[1:])
                        if 'nullable' in rest:
                            current_field['nullable'] = True
                        current_field['type'] = rest
                    elif current_field:
                        # Continuation - could be type or description
                        current_field['description'] += ' ' + stripped
                
                idx += 1
            
            if current_field:
                current_field['description'] = current_field['description'].strip()
                fields.append(current_field)
            entity['fields'] = fields
        else:
            entity['fields'] = []
        
        if entity_name:
            entities.append(entity)
    
    return entities


def parse_document_imaging_schema():
    """Parse Document Imaging Content Management Database Schema PDF."""
    pdf_path = BASE / "downloads/patient-population-format-specs/patient-population-ehi-export-data-format-specifications/Oracle Health Document Imaging Content Management Database Schema.pdf"
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    return text


def parse_non_dicom_columns():
    """Parse Non-DICOM column definitions PDF."""
    pdf_path = BASE / "downloads/patient-population-format-specs/patient-population-ehi-export-data-format-specifications/Oracle Health Multimedia Storage Non-DICOM Data Column Definitions.pdf"
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Extract columns
    columns = []
    lines = text.split('\n')
    for line in lines:
        stripped = line.strip()
        # Look for column definitions
        if stripped and any(col in stripped for col in ['ObjectIdentifier', 'CompressionCode', 'GroupIdentifier', 'MimeTypeCode', 'OrigStoredTimeStamp', 'S3Path', 'SourceName', 'TransformationCode']):
            columns.append(stripped)
    
    return {
        'name': 'NonDICOM_Multimedia_Storage',
        'description': 'Non-DICOM multimedia storage CSV export columns',
        'source': 'non_dicom_column_definitions',
        'fields': [
            {'name': 'ObjectIdentifier', 'type': 'string', 'description': 'Unique identifier for the multimedia object'},
            {'name': 'CompressionCode', 'type': 'string', 'description': 'Compression algorithm used (XZ, GZIP, BZIP2)'},
            {'name': 'GroupIdentifier', 'type': 'string', 'description': 'Group identifier for the object'},
            {'name': 'MimeTypeCode', 'type': 'string', 'description': 'MIME type of the stored content'},
            {'name': 'OrigStoredTimeStamp', 'type': 'timestamp', 'description': 'Original storage timestamp'},
            {'name': 'S3Path', 'type': 'string', 'description': 'S3 storage path for the object'},
            {'name': 'SourceName', 'type': 'string', 'description': 'Source system name'},
            {'name': 'TransformationCode', 'type': 'string', 'description': 'Transformation/compression applied to pixel data'}
        ]
    }

def build_full_inventory():
    """Build complete entity inventory from all sources."""
    
    print("Loading MySQL model from enrichment...")
    mysql_tables = load_mysql_model()
    
    print(f"Loaded {len(mysql_tables)} MySQL tables")
    
    print("Parsing HDI entities...")
    hdi_entities = parse_hdi_entities_v2()
    print(f"Parsed {len(hdi_entities)} HDI entities")
    
    # Build unified inventory
    inventory = {
        'sources': {
            'millennium_database': {
                'description': 'Core Millennium EHR database (MySQL/Oracle data model)',
                'table_count': len(mysql_tables),
                'column_count': sum(len(t.get('columns', [])) for t in mysql_tables),
                'format': 'SQL (DDL + INSERT statements)'
            },
            'hdi_longitudinal_record': {
                'description': 'Health Data Intelligence Longitudinal Record (Avro entities via REST API)',
                'entity_count': len(hdi_entities),
                'field_count': sum(len(e.get('fields', [])) for e in hdi_entities),
                'format': 'Avro via REST API'
            },
            'multimedia_storage': {
                'description': 'DICOM and non-DICOM multimedia files',
                'format': 'Native files (DICOM, images, audio, video, PDF)'
            },
            'document_imaging': {
                'description': 'Document imaging content management database',
                'format': 'Binary files (.bin) with SQL metadata'
            }
        },
        'millennium_tables': [],
        'hdi_entities': [],
        'ancillary_schemas': []
    }
    
    # Process MySQL tables
    for t in mysql_tables:
        entry = {
            'name': t['name'],
            'description': t.get('description', ''),
            'definition': t.get('definition', ''),
            'table_type': t.get('table_type', ''),
            'subject_area': t.get('subject_area', ''),
            'source': 'millennium_database',
            'fields': []
        }
        for c in t.get('columns', []):
            field = {
                'name': c['name'],
                'type': c.get('type', ''),
                'nullable': c.get('nullable', None),
                'description': c.get('definition', '')
            }
            entry['fields'].append(field)
        inventory['millennium_tables'].append(entry)
    
    # Process HDI entities
    for e in hdi_entities:
        entry = {
            'name': e['name'],
            'full_name': e.get('full_name', ''),
            'description': e.get('description', ''),
            'entity_type': e.get('entity_type', 'record'),
            'source': 'hdi_longitudinal_record',
            'fields': e.get('fields', []),
        }
        if 'symbols' in e:
            entry['symbols'] = e['symbols']
        inventory['hdi_entities'].append(entry)
    
    # Add non-DICOM schema
    non_dicom = parse_non_dicom_columns()
    inventory['ancillary_schemas'].append(non_dicom)
    
    return inventory

def compute_summary(inventory):
    """Compute summary statistics from inventory."""
    
    # Millennium stats
    mill_tables = inventory['millennium_tables']
    mill_total_fields = sum(len(t['fields']) for t in mill_tables)
    mill_described_fields = sum(1 for t in mill_tables for f in t['fields'] if f.get('description', '').strip())
    mill_typed_fields = sum(1 for t in mill_tables for f in t['fields'] if f.get('type', '').strip())
    
    # Subject area breakdown
    sa_counts = defaultdict(lambda: {'tables': 0, 'fields': 0, 'described': 0})
    for t in mill_tables:
        sa = t.get('subject_area', 'unknown')
        sa_counts[sa]['tables'] += 1
        sa_counts[sa]['fields'] += len(t['fields'])
        sa_counts[sa]['described'] += sum(1 for f in t['fields'] if f.get('description', '').strip())
    
    # Sort by table count
    sa_sorted = sorted(sa_counts.items(), key=lambda x: -x[1]['tables'])
    
    # HDI stats
    hdi_entities = inventory['hdi_entities']
    hdi_records = [e for e in hdi_entities if e.get('entity_type') != 'enum']
    hdi_enums = [e for e in hdi_entities if e.get('entity_type') == 'enum']
    hdi_total_fields = sum(len(e['fields']) for e in hdi_records)
    hdi_described_fields = sum(1 for e in hdi_records for f in e['fields'] if f.get('description', '').strip())
    
    # Top 20 largest millennium tables by field count
    largest_tables = sorted(mill_tables, key=lambda t: -len(t['fields']))[:20]
    
    summary = {
        'millennium_database': {
            'total_tables': len(mill_tables),
            'total_fields': mill_total_fields,
            'fields_with_descriptions': mill_described_fields,
            'fields_with_types': mill_typed_fields,
            'description_coverage_pct': round(100 * mill_described_fields / mill_total_fields, 1) if mill_total_fields else 0,
            'subject_area_count': len(sa_counts),
            'subject_areas': [
                {
                    'name': name,
                    'tables': stats['tables'],
                    'fields': stats['fields'],
                    'fields_described': stats['described']
                }
                for name, stats in sa_sorted
            ],
            'largest_tables': [
                {
                    'name': t['name'],
                    'subject_area': t.get('subject_area', ''),
                    'field_count': len(t['fields']),
                    'description': t.get('description', '')[:100]
                }
                for t in largest_tables
            ]
        },
        'hdi_longitudinal_record': {
            'total_entities': len(hdi_entities),
            'record_entities': len(hdi_records),
            'enum_entities': len(hdi_enums),
            'total_fields': hdi_total_fields,
            'fields_with_descriptions': hdi_described_fields,
            'description_coverage_pct': round(100 * hdi_described_fields / hdi_total_fields, 1) if hdi_total_fields else 0
        },
        'ancillary_schemas': {
            'non_dicom_columns': 8,
            'document_imaging_tables': 'multiple (AE_APPS, AE_ADEFS, AE_DT#, AE_DL#, AE_RH#, AE_PATHS)',
            'dicom_structure': 'hierarchical XML/JSON per patient/study'
        },
        'overall': {
            'total_entities_all_sources': len(mill_tables) + len(hdi_entities),
            'total_fields_all_sources': mill_total_fields + hdi_total_fields + 8,
            'export_formats': ['SQL (DDL + INSERT)', 'Avro/REST API', 'Native multimedia files', 'Binary document files'],
            'export_mechanisms': ['Single-patient automated extract', 'Population bulk extract', 'HDI REST API'],
        }
    }
    
    return summary

if __name__ == '__main__':
    inventory = build_full_inventory()
    
    print("\nComputing summary...")
    summary = compute_summary(inventory)
    
    # Save full inventory
    out_dir = Path(__file__).parent
    
    with open(out_dir / 'entity-inventory-full.json', 'w') as f:
        json.dump(inventory, f, indent=2, default=str)
    print(f"Saved entity-inventory-full.json ({(out_dir / 'entity-inventory-full.json').stat().st_size / 1024 / 1024:.1f} MB)")
    
    with open(out_dir / 'entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved entity-inventory-summary.json")
    
    # Print key stats
    print(f"\n=== KEY STATS ===")
    ms = summary['millennium_database']
    print(f"Millennium DB: {ms['total_tables']} tables, {ms['total_fields']} fields, {ms['fields_with_descriptions']} described ({ms['description_coverage_pct']}%)")
    print(f"Subject areas: {ms['subject_area_count']}")
    
    hs = summary['hdi_longitudinal_record']
    print(f"HDI: {hs['total_entities']} entities ({hs['record_entities']} records, {hs['enum_entities']} enums), {hs['total_fields']} fields")
    
    print(f"\nTop 10 subject areas:")
    for sa in ms['subject_areas'][:10]:
        print(f"  {sa['name']:40s} {sa['tables']:>5d} tables, {sa['fields']:>6d} fields")
    
    print(f"\nTop 10 largest tables:")
    for t in ms['largest_tables'][:10]:
        print(f"  {t['name']:50s} {t['field_count']:>4d} fields ({t['subject_area']})")
