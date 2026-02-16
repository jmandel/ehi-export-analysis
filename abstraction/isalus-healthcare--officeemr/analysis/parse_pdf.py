"""
Parse the PDF data dictionary to extract field descriptions for entities 
not covered in the XLSX. The PDF uses a two-column layout with 
entity.json names, field names, and multi-line descriptions.
"""
import re
import json

def parse_pdf_dictionary(pdf_text_path):
    with open(pdf_text_path, 'r') as f:
        lines = f.readlines()
    
    # Find clinical and PM sections
    clinical_start = None
    pm_start = None
    for i, line in enumerate(lines):
        if 'Clinical Data Exports' in line and clinical_start is None:
            clinical_start = i
        if 'Practice Management Data Exports' in line:
            pm_start = i
    
    if clinical_start is None:
        print("Could not find Clinical Data Exports section")
        return {}
    
    result = {}  # {entity: {field: description}}
    
    # Parse from clinical_start to end of file
    current_entity = None
    current_field = None
    current_desc_lines = []
    
    # Pattern: entity.json   fieldName   description text
    # Or continuation:                   more description text
    entity_field_pat = re.compile(r'^(\w+\.json)\s{2,}(\w+)\s{2,}(.*)$')
    cont_field_pat = re.compile(r'^\s{20,}(\w+)\s{2,}(.*)$')
    cont_desc_pat = re.compile(r'^\s{30,}(.+)$')
    
    def save_current():
        nonlocal current_entity, current_field, current_desc_lines
        if current_entity and current_field and current_desc_lines:
            ename = current_entity.replace('.json', '')
            if ename not in result:
                result[ename] = {}
            desc = ' '.join(current_desc_lines).strip()
            result[ename][current_field] = desc
    
    for i in range(clinical_start + 2, len(lines)):
        line = lines[i].rstrip('\n')
        
        # Skip page headers/footers
        if line.strip() == '' or 'Page' in line and 'of' in line:
            continue
        if line.strip() in ('Clinical Data Exports', 'Practice Management Data Exports',
                           'Export Name', 'FIELD', 'Description'):
            continue
        if re.match(r'^\s*Export Name\s+FIELD\s+Description\s*$', line):
            continue
            
        # Try entity + field + description pattern
        m = entity_field_pat.match(line)
        if m:
            save_current()
            current_entity = m.group(1)
            current_field = m.group(2)
            current_desc_lines = [m.group(3).strip()] if m.group(3).strip() else []
            continue
        
        # Try same-entity continuation with new field  
        # Pattern: lots of spaces then fieldName then description
        m2 = re.match(r'^' + re.escape(current_entity or '') + r'\s{2,}(\w+)\s{2,}(.*)$', line) if current_entity else None
        if m2:
            save_current()
            current_field = m2.group(1)
            current_desc_lines = [m2.group(2).strip()] if m2.group(2).strip() else []
            continue
        
        # Try continuation of description (deeply indented text)
        stripped = line.strip()
        if stripped and current_field:
            # Check if this looks like a new field (starts with entity name or is a field-like word at right indent)
            # Heuristic: if the line has entity.json pattern, it's a new entry
            if re.match(r'^\w+\.json\s', line):
                m3 = entity_field_pat.match(line)
                if m3:
                    save_current()
                    current_entity = m3.group(1)
                    current_field = m3.group(2)
                    current_desc_lines = [m3.group(3).strip()] if m3.group(3).strip() else []
                    continue
            
            # Check if it's a continuation field (same entity, new field)
            # These typically have leading spaces matching the field column
            m4 = re.match(r'^\s{15,}(\w+)\s{2,}(.*)$', line)
            if m4 and not re.match(r'^[a-z]', m4.group(1)):
                # Likely description continuation
                current_desc_lines.append(stripped)
            elif m4:
                # Check if it looks like a field name (camelCase or snake_case)
                potential_field = m4.group(1)
                if re.match(r'^[a-z][a-zA-Z0-9_]*$', potential_field):
                    save_current()
                    current_field = potential_field
                    current_desc_lines = [m4.group(2).strip()] if m4.group(2).strip() else []
                else:
                    current_desc_lines.append(stripped)
            else:
                # Just continuation text
                current_desc_lines.append(stripped)
    
    save_current()
    return result

if __name__ == '__main__':
    result = parse_pdf_dictionary('/tmp/ehi-pdf.txt')
    print(f"Parsed {len(result)} entities from PDF")
    total_fields = sum(len(v) for v in result.values())
    print(f"Total fields: {total_fields}")
    
    # Check specific entities we're missing from XLSX
    missing = ['eligibility', 'goal_objective', 'goal_problem', 'implantable_device',
               'lab_result', 'preschool_billing', 'problem_list', 'problem_list_note', 'sliding_fee']
    for ename in missing:
        if ename in result:
            print(f"\n{ename}: {len(result[ename])} fields from PDF")
            for fn, desc in list(result[ename].items())[:3]:
                print(f"  {fn}: {desc[:80]}")
        else:
            print(f"\n{ename}: NOT FOUND in PDF")
    
    with open('/tmp/pdf_dictionary.json', 'w') as f:
        json.dump(result, f, indent=2)
