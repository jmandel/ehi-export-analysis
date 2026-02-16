#!/usr/bin/env python3
"""Parse the myUnity EHI Export PDF data dictionary into structured JSON.

Reads pdftotext output and extracts all export files, their descriptions,
and field definitions (name, type, description).
"""

import json
import re
import sys

def parse_pdf_text(text: str) -> dict:
    lines = text.split('\n')
    
    # Find file documentation sections
    files = []
    current_file = None
    current_field = None
    in_sections = False  # For CCD sections list
    state = 'seeking_file'
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip page numbers (standalone small numbers at end of pages)
        if re.match(r'^\d{1,2}$', line):
            i += 1
            continue
        
        # Skip the document title and headers
        if line.startswith('EHI Export: myUnity File Documentation'):
            i += 1
            continue
        if line.startswith('Last Updated:'):
            i += 1
            continue
        if line == 'Contents':
            # Skip table of contents
            while i < len(lines) and not lines[i].strip().startswith('Overview'):
                i += 1
            continue
        
        # Detect file documentation sections
        file_match = re.match(r'^(\w+)\s+File Documentation$', line)
        if file_match:
            if current_file and current_field:
                current_file['fields'].append(current_field)
                current_field = None
            if current_file:
                files.append(current_file)
            
            file_name = file_match.group(1)
            current_file = {
                'file_name': file_name,
                'file_description': '',
                'fields': [],
                'sections': []
            }
            state = 'seeking_description'
            in_sections = False
            i += 1
            continue
        
        if current_file is None:
            i += 1
            continue
        
        # File description
        if state == 'seeking_description':
            desc_match = re.match(r'^File Description:\s*(.*)$', line)
            if desc_match:
                desc = desc_match.group(1)
                # Collect multiline description
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line == '' or next_line.startswith('-') or next_line.startswith('Name:') or next_line.startswith('CCD Sections'):
                        break
                    desc += ' ' + next_line
                    i += 1
                current_file['file_description'] = desc.strip()
                state = 'seeking_fields'
                continue
            i += 1
            continue
        
        if state == 'seeking_fields':
            # Check for CCD sections list
            if line.startswith('CCD Sections'):
                in_sections = True
                i += 1
                continue
            
            if in_sections:
                if line.startswith('•') or line.startswith('-'):
                    section = line.lstrip('•- ').strip()
                    if section:
                        current_file['sections'].append(section)
                    i += 1
                    continue
                elif line == '' or line == '---' or line.startswith('----'):
                    i += 1
                    continue
                elif re.match(r'^(\w+)\s+File Documentation$', line):
                    in_sections = False
                    continue  # Don't increment, let it match file section
                elif line and not line.startswith('Name:'):
                    # Could be continuation of section name or other content
                    i += 1
                    continue
                else:
                    in_sections = False
            
            # Field definitions
            name_match = re.match(r'^Name:\s*(.+)$', line)
            if name_match:
                if current_field:
                    current_file['fields'].append(current_field)
                current_field = {
                    'name': name_match.group(1).strip(),
                    'type': '',
                    'description': ''
                }
                i += 1
                continue
            
            type_match = re.match(r'^Type:\s*(.+)$', line)
            if type_match and current_field:
                current_field['type'] = type_match.group(1).strip()
                i += 1
                continue
            
            desc_match = re.match(r'^Description:\s*(.*)$', line)
            if desc_match and current_field:
                desc = desc_match.group(1)
                # Collect multiline description
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if (next_line == '' or next_line.startswith('Name:') or 
                        next_line.startswith('---') or next_line.startswith('----') or
                        re.match(r'^(\w+)\s+File Documentation$', next_line) or
                        re.match(r'^\d{1,2}$', next_line)):
                        break
                    desc += ' ' + next_line
                    i += 1
                current_field['description'] = desc.strip()
                continue
        
        i += 1
    
    # Don't forget the last file/field
    if current_file and current_field:
        current_file['fields'].append(current_field)
    if current_file:
        files.append(current_file)
    
    return files


def main():
    with open('/tmp/myunity-dd.txt', 'r') as f:
        text = f.read()
    
    files = parse_pdf_text(text)
    
    # Build full inventory
    inventory = {
        'source': 'ehi_export_all_files_myunity_fall_2024.pdf',
        'last_updated': '08/15/2024',
        'total_files': len(files),
        'total_fields': sum(len(f['fields']) for f in files),
        'export_files': []
    }
    
    for f in files:
        entry = {
            'file_name': f['file_name'],
            'file_description': f['file_description'],
            'field_count': len(f['fields']),
            'fields': f['fields']
        }
        if f['sections']:
            entry['sections'] = f['sections']
        
        # Stats
        described = sum(1 for fld in f['fields'] if fld.get('description', '').strip())
        typed = sum(1 for fld in f['fields'] if fld.get('type', '').strip())
        entry['fields_with_descriptions'] = described
        entry['fields_with_types'] = typed
        
        inventory['export_files'].append(entry)
    
    # Summary stats
    all_fields = [fld for f in files for fld in f['fields']]
    inventory['total_fields_with_descriptions'] = sum(1 for fld in all_fields if fld.get('description', '').strip())
    inventory['total_fields_with_types'] = sum(1 for fld in all_fields if fld.get('type', '').strip())
    
    # Write full inventory
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Write summary
    summary = {
        'source': inventory['source'],
        'last_updated': inventory['last_updated'],
        'total_files': inventory['total_files'],
        'total_fields': inventory['total_fields'],
        'total_fields_with_descriptions': inventory['total_fields_with_descriptions'],
        'total_fields_with_types': inventory['total_fields_with_types'],
        'pct_described': round(inventory['total_fields_with_descriptions'] / max(inventory['total_fields'], 1) * 100, 1),
        'pct_typed': round(inventory['total_fields_with_types'] / max(inventory['total_fields'], 1) * 100, 1),
        'files_summary': []
    }
    
    for entry in inventory['export_files']:
        file_sum = {
            'file_name': entry['file_name'],
            'file_description': entry['file_description'],
            'field_count': entry['field_count'],
            'fields_with_descriptions': entry['fields_with_descriptions'],
            'fields_with_types': entry['fields_with_types'],
        }
        if 'sections' in entry:
            file_sum['sections'] = entry['sections']
        summary['files_summary'].append(file_sum)
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary to console
    print(f"Parsed {inventory['total_files']} export files with {inventory['total_fields']} total fields")
    print(f"  Fields with descriptions: {inventory['total_fields_with_descriptions']} ({summary['pct_described']}%)")
    print(f"  Fields with types: {inventory['total_fields_with_types']} ({summary['pct_typed']}%)")
    print()
    for entry in inventory['export_files']:
        print(f"  {entry['file_name']}: {entry['field_count']} fields ({entry['fields_with_descriptions']} described, {entry['fields_with_types']} typed)")
        if 'sections' in entry:
            print(f"    Sections: {', '.join(entry['sections'])}")


if __name__ == '__main__':
    main()
