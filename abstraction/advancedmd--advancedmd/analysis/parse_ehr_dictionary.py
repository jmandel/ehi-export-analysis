#!/usr/bin/env python3
"""Parse the AdvancedMD EHR Export Data Dictionary PDF into structured JSON.

Reads pdftotext output from advancedmd-ehrExport-dataDictionary.pdf and extracts
all tables, columns, and descriptions into full-entity-inventory.json.
"""

import subprocess
import json
import re
import sys

PDF_PATH = "../../../results/advancedmd--advancedmd/downloads/advancedmd-ehrExport-dataDictionary.pdf"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_ehr_tables(text):
    """Parse column/description pairs from the EHR data dictionary text."""
    tables = []
    current_table = None
    current_desc = None
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Match table headers like "EHR_Allergies" or "EHR_PatientNoteDiagnosis, EHR_Problems"
        table_match = re.match(r'^(EHR_\w+(?:\s*,\s*EHR_\w+)*)\s*$', line)
        if table_match:
            table_names = [t.strip() for t in table_match.group(1).split(',')]
            # For combined headers like "EHR_PatientNoteDiagnosis, EHR_Problems",
            # we'll handle them as separate tables below
            i += 1
            continue
        
        # Match table name followed by description text
        table_match2 = re.match(r'^(EHR_\w+)$', line)
        if table_match2:
            if current_table and current_table['columns']:
                tables.append(current_table)
            current_table = {
                'table_name': table_match2.group(1),
                'description': '',
                'columns': []
            }
            # Look for table description on next line(s)
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('Column') and ('Description' in lines[i] or i+1 < len(lines)):
                    break
                if next_line.startswith('This table'):
                    current_table['description'] = next_line
                elif next_line and not next_line.startswith('Column'):
                    if current_table['description']:
                        current_table['description'] += ' ' + next_line
                    else:
                        current_table['description'] = next_line
                i += 1
            continue
        
        # Match "Column    Description" header
        if re.match(r'^\s*Column\s+Description\s*$', lines[i]):
            i += 1
            continue
        
        # Match column entries: "ColumnName    Description text"
        if current_table is not None:
            col_match = re.match(r'^\s{0,2}(\S+)\s{2,}(.+)$', lines[i])
            if col_match:
                col_name = col_match.group(1)
                col_desc = col_match.group(2).strip()
                # Don't add non-column lines
                if col_name not in ('Column', 'LEGAL', 'The', 'For', 'In', 'By', 'From', 'Notes:', 'This', 'Now', 'And', 'Since', 'As', 'Because', 'We', 'You', 'Scenario', 'Pe_Genito'):
                    current_table['columns'].append({
                        'name': col_name,
                        'description': col_desc
                    })
            # Column with no description
            elif re.match(r'^\s{0,2}(\w+)\s*$', lines[i]) and current_table.get('columns') is not None:
                potential_col = lines[i].strip()
                if potential_col and len(potential_col) > 3 and potential_col[0].isupper() and potential_col not in ('Column', 'LEGAL', 'The', 'For', 'Notes', 'This', 'Now', 'And', 'Since', 'Because', 'We', 'You', 'Scenario'):
                    # Check if it looks like a column name (CamelCase or underscore)
                    if re.match(r'^[A-Z][a-zA-Z_]+$', potential_col):
                        current_table['columns'].append({
                            'name': potential_col,
                            'description': ''
                        })
        
        i += 1
    
    # Don't forget the last table
    if current_table and current_table['columns']:
        tables.append(current_table)
    
    return tables

def parse_ccda_sections(ccda_text):
    """Parse the C-CDA data dictionary into sections."""
    sections = []
    lines = ccda_text.split('\n')
    
    # The C-CDA dictionary maps sections like Allergies, Medications, etc.
    current_section = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('LEGAL') or line.startswith('DATA EXPORT'):
            continue
        
        # Section headers are like "Allergies", "Medications", etc.
        # They have vocabulary codes and descriptions
        # We'll parse this more loosely
        if re.match(r'^(Field Name|Required Text)', line):
            continue
        
    return sections

def main():
    text = extract_text()
    
    # Parse the tables using a more robust approach
    tables = []
    current_table = None
    
    lines = text.split('\n')
    i = 0
    
    # Table definitions we know exist from reading the PDF
    known_tables = [
        'EHR_Allergies', 'EHR_Immunizations', 'EHR_Messages',
        'EHR_PatientNoteDiagnosis', 'EHR_Problems', 'EHR_Prescriptions',
        'EHR_LabResults', 'EHR_ResultItems', 'EHR_ResultSets', 
        'EHR_ResultValues', 'EHR_PatientNotes', 'EHR_WordMerge'
    ]
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if this line starts a new table
        found_table = None
        for tn in known_tables:
            if stripped == tn or stripped.startswith(tn + ',') or stripped.startswith(tn + ' '):
                found_table = tn
                break
            # Also match combined headers
            if tn in stripped and re.match(r'^EHR_\w+', stripped):
                found_table = tn
                break
        
        if found_table and (current_table is None or current_table['table_name'] != found_table):
            if current_table and current_table['columns']:
                tables.append(current_table)
            current_table = {
                'table_name': found_table,
                'description': '',
                'columns': []
            }
            i += 1
            continue
        
        # Check for "Column    Description" header - skip it
        if re.match(r'^\s*Column\s+Description\s*$', stripped):
            i += 1
            continue
        
        # Parse column entries
        if current_table is not None:
            # Match lines with column name and description separated by spaces
            col_match = re.match(r'^\s{0,3}(\w[\w_]*(?:\s\w+)?)\s{3,}(.+)$', line)
            if col_match:
                col_name = col_match.group(1).strip()
                col_desc = col_match.group(2).strip()
                # Filter out non-column content
                skip_words = {'Column', 'LEGAL', 'The', 'For', 'In', 'By', 'From', 'Notes',
                             'This', 'Now', 'And', 'Since', 'As', 'Because', 'We', 'You',
                             'Scenario', 'Pe_Genito', 'JOIN', 'ON', 'Once', 'Any', 'Note',
                             'Both', 'That', 'What'}
                if col_name not in skip_words and not col_name.startswith('dbo.'):
                    current_table['columns'].append({
                        'name': col_name,
                        'description': col_desc
                    })
            else:
                # Check for column with no description (just name on a line)
                solo_match = re.match(r'^\s{0,3}([A-Z]\w+)\s*$', stripped)
                if solo_match and current_table:
                    col_name = solo_match.group(1)
                    skip_words2 = {'Column', 'LEGAL', 'The', 'For', 'Notes', 'This', 'Now',
                                  'And', 'Since', 'Because', 'We', 'You', 'Scenario',
                                  'EHR', 'AdvancedMD', 'Document'}
                    if col_name not in skip_words2 and len(col_name) > 3:
                        # Verify it looks like a DB column
                        if re.match(r'^[A-Z][a-zA-Z_]+[A-Z_a-z]$', col_name):
                            current_table['columns'].append({
                                'name': col_name,
                                'description': ''
                            })
        
        # Capture table descriptions
        if current_table and current_table['description'] == '' and stripped.startswith('This table'):
            current_table['description'] = stripped
        
        i += 1
    
    # Save last table
    if current_table and current_table['columns']:
        tables.append(current_table)
    
    # Deduplicate tables (the combined header may cause duplicates)
    seen_tables = {}
    for t in tables:
        name = t['table_name']
        if name not in seen_tables:
            seen_tables[name] = t
        else:
            # Merge columns if we have a duplicate
            existing_cols = {c['name'] for c in seen_tables[name]['columns']}
            for c in t['columns']:
                if c['name'] not in existing_cols:
                    seen_tables[name]['columns'].append(c)
                    existing_cols.add(c['name'])
    
    tables = list(seen_tables.values())
    
    # Build the full inventory
    inventory = {
        'source': 'advancedmd-ehrExport-dataDictionary.pdf',
        'export_type': 'EHR Bulk Data Export (SQL Server .bak)',
        'total_tables': len(tables),
        'total_fields': sum(len(t['columns']) for t in tables),
        'fields_with_descriptions': sum(
            1 for t in tables for c in t['columns'] if c['description']
        ),
        'tables': tables
    }
    
    # Print summary
    print(f"Parsed {inventory['total_tables']} tables, {inventory['total_fields']} fields")
    print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
    print()
    for t in tables:
        desc_count = sum(1 for c in t['columns'] if c['description'])
        print(f"  {t['table_name']}: {len(t['columns'])} columns ({desc_count} described)")
    
    # Save to JSON
    with open('ehr-bulk-inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"\nSaved to ehr-bulk-inventory.json")
    return inventory

if __name__ == '__main__':
    main()
