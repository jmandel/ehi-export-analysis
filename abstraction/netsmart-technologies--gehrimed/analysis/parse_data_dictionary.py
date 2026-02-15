"""
Parse the GEHRIMED EHI Export data dictionary text file (extracted from PDF).
Extracts table names, column names, types, max lengths, and descriptions.
Produces summary stats and a full inventory JSON.
"""

import json
import re
import sys

INPUT_FILE = "/home/jmandel/hobby/ehi-export-analysis/results/netsmart-technologies--gehrimed/downloads/ehi_export_all_tables_gehrimed_2023.txt"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/netsmart-technologies--gehrimed/analysis"

def parse_data_dictionary(text):
    lines = text.split('\n')
    tables = []
    current_table = None
    current_column = None
    i = 0
    in_toc = True  # Start in TOC mode
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip boilerplate
        if line.startswith('Confidential.') or line == '' or re.match(r'^\d+$', line):
            i += 1
            continue
        
        # Skip TOC entries (have dots followed by page numbers)
        if '......' in line or re.match(r'^(Contents|Overview|Glossary of Terms|Tables)(\s|\.)', line):
            i += 1
            continue
        
        # Skip header/glossary content before actual tables
        if in_toc:
            # The glossary section has specific known lines
            if line in ('Overview', 'Glossary of Terms', 'Tables', 'Field Name', 'Description'):
                i += 1
                continue
            # Glossary term definitions
            glossary_terms = ['Id', 'PatientID', 'LastModifiedBy', 'LastModifiedDate', 
                            'CreatedBy', 'AddedBy', 'DictationID', 'AddedDate']
            if line in glossary_terms:
                i += 1
                continue
            # Glossary descriptions (multi-line text before first table)
            if not line.startswith('Table Name:') and not line.startswith('Column Name:'):
                # Check if this looks like a glossary description
                if any(term in line for term in ['database row id', 'unique patient', 'last updated', 
                                                  'who created', 'who added', 'encounter in GEHRIMED',
                                                  'Date record was added', 'identifier within']):
                    i += 1
                    continue
        
        # Table name (real definition, not TOC)
        table_match = re.match(r'^Table Name:\s*(\S+)\s*$', line)
        if table_match:
            in_toc = False
            table_name = table_match.group(1).strip()
            # Next non-empty, non-boilerplate line might be table description
            table_desc = ""
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if next_line == '' or next_line.startswith('Confidential.') or re.match(r'^\d+$', next_line):
                    j += 1
                    continue
                if next_line.startswith('Column Name:') or next_line.startswith('Table Name:'):
                    break
                # This is the table description
                table_desc = next_line
                j += 1
                break
            
            current_table = {
                'name': table_name,
                'description': table_desc,
                'columns': []
            }
            tables.append(current_table)
            current_column = None
            if table_desc:
                i = j
            else:
                i += 1
            continue
        
        # Column name
        col_match = re.match(r'^Column Name:\s*(.+)$', line)
        if col_match and current_table is not None:
            col_name = col_match.group(1).strip()
            current_column = {
                'name': col_name,
                'type': None,
                'max_length': None,
                'description': ''
            }
            current_table['columns'].append(current_column)
            i += 1
            continue
        
        # Column type
        type_match = re.match(r'^ColumnType:\s*(.+)$', line)
        if type_match and current_column is not None:
            current_column['type'] = type_match.group(1).strip()
            i += 1
            continue
        
        # Max length
        len_match = re.match(r'^Max Length:\s*(.+)$', line)
        if len_match and current_column is not None:
            current_column['max_length'] = len_match.group(1).strip()
            i += 1
            continue
        
        # If we get here and have a current column, and it's not a known label,
        # it's likely a description line
        if current_column is not None and not line.startswith(('Column Name:', 'ColumnType:', 'Max Length:', 'Table Name:')):
            if line:
                if current_column['description']:
                    current_column['description'] += ' ' + line
                else:
                    current_column['description'] = line
        
        i += 1
    
    return tables

def main():
    with open(INPUT_FILE, 'r') as f:
        text = f.read()
    
    tables = parse_data_dictionary(text)
    
    # Summary stats
    total_tables = len(tables)
    total_columns = sum(len(t['columns']) for t in tables)
    cols_with_desc = sum(1 for t in tables for c in t['columns'] if c['description'].strip())
    cols_with_type = sum(1 for t in tables for c in t['columns'] if c['type'])
    
    print(f"=== GEHRIMED EHI Export Data Dictionary Summary ===")
    print(f"Total tables: {total_tables}")
    print(f"Total columns: {total_columns}")
    print(f"Columns with descriptions: {cols_with_desc} ({100*cols_with_desc/total_columns:.1f}%)")
    print(f"Columns with types: {cols_with_type} ({100*cols_with_type/total_columns:.1f}%)")
    print()
    
    # Per-table breakdown
    print(f"{'Table':<35} {'Cols':>5} {'Desc':>5} {'Desc%':>6}")
    print("-" * 55)
    for t in tables:
        n_cols = len(t['columns'])
        n_desc = sum(1 for c in t['columns'] if c['description'].strip())
        pct = 100 * n_desc / n_cols if n_cols else 0
        print(f"{t['name']:<35} {n_cols:>5} {n_desc:>5} {pct:>5.0f}%")
    
    # Save full inventory as JSON
    with open(f"{OUTPUT_DIR}/full-entity-inventory.json", 'w') as f:
        json.dump(tables, f, indent=2)
    
    # Save summary as text
    with open(f"{OUTPUT_DIR}/table-summary.txt", 'w') as f:
        f.write(f"GEHRIMED EHI Export Data Dictionary Summary\n")
        f.write(f"Source: EHI Export All Tables - November2023 (GEHRIMED).pdf\n")
        f.write(f"{'='*55}\n")
        f.write(f"Total tables: {total_tables}\n")
        f.write(f"Total columns: {total_columns}\n")
        f.write(f"Columns with descriptions: {cols_with_desc} ({100*cols_with_desc/total_columns:.1f}%)\n")
        f.write(f"Columns with types: {cols_with_type} ({100*cols_with_type/total_columns:.1f}%)\n\n")
        f.write(f"{'Table':<35} {'Cols':>5} {'Desc':>5} {'Desc%':>6}\n")
        f.write(f"{'-'*55}\n")
        for t in tables:
            n_cols = len(t['columns'])
            n_desc = sum(1 for c in t['columns'] if c['description'].strip())
            pct = 100 * n_desc / n_cols if n_cols else 0
            f.write(f"{t['name']:<35} {n_cols:>5} {n_desc:>5} {pct:>5.0f}%\n")
    
    print(f"\nFull inventory saved to {OUTPUT_DIR}/full-entity-inventory.json")
    print(f"Summary saved to {OUTPUT_DIR}/table-summary.txt")

if __name__ == '__main__':
    main()
