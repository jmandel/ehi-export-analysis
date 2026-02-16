"""
Parse the CGM APRIMA EHI Export User Guide PDF into a structured JSON data dictionary.
Uses pdftotext output and regex-based parsing to extract all CSV file definitions and fields.
"""

import re
import json
import subprocess
import sys

def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_data_dictionary(text):
    lines = text.split('\n')
    csv_files = []
    current_file = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect start of a new CSV file section: "Description" followed by file description
        # Pattern: line starts with "Description" and next line has "File name"
        if line.startswith('Description') and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith('File name') and 'EHI' in next_line:
                # Extract description (may span multiple lines before File name)
                desc_text = line.replace('Description', '', 1).strip()
                # Check if description continues on next lines before File name
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('File name'):
                    desc_text += ' ' + lines[j].strip()
                    j += 1
                
                file_name_line = lines[j].strip()
                file_name = file_name_line.replace('File name', '', 1).strip()
                
                # Extract the CSV name from file_name pattern
                name_match = re.search(r'EHI(?:Extract|Export)_(?:Deconversion_)?(\w+)', file_name)
                csv_name = name_match.group(1) if name_match else file_name
                
                current_file = {
                    'name': csv_name,
                    'file_name_pattern': file_name,
                    'description': desc_text,
                    'fields': []
                }
                csv_files.append(current_file)
                
                # Skip to "Data Provided" / "Column Heading" header line
                i = j + 1
                while i < len(lines):
                    if 'Column Heading' in lines[i] and 'Data Type' in lines[i]:
                        i += 1  # skip header
                        break
                    i += 1
                continue
        
        # Parse field lines for current CSV file
        if current_file is not None and line:
            # Skip page numbers, headers, footers
            if re.match(r'^\d+$', line):
                i += 1
                continue
            if line.startswith('EHI Export'):
                i += 1
                continue
            if line.startswith('November 2, 2023'):
                i += 1
                continue
            if line.startswith('©'):
                i += 1
                continue
            if line.startswith('Data Provided') or line.startswith('Column Heading'):
                i += 1
                continue
            
            # Try to parse a field line: column_heading  data_type  description
            # The challenge: variable whitespace and multi-line descriptions
            # Data types follow patterns like: char(N), datetime, money, bit, int, 
            #   uniqueidentifier, decimal(N,N), smallint, tinyint, varchar(N), nvarchar(N)
            field_match = re.match(
                r'^(\s*)(\S+(?:\s+\S+)*?)\s{2,}(char\(\d+\)|datetime|money|bit|int|uniqueidentifier|decimal\(\d+,\s*\d+\)|smallint|tinyint|varchar\(\d+\)|nvarchar\(\d+\)|float)\s{2,}(.+)',
                lines[i]
            )
            
            if field_match:
                col_heading = field_match.group(2).strip()
                data_type = field_match.group(3).strip()
                desc = field_match.group(4).strip()
                
                # Check for continuation lines (indented text that's part of description)
                j = i + 1
                while j < len(lines):
                    next_l = lines[j]
                    next_stripped = next_l.strip()
                    # Skip empty lines
                    if not next_stripped:
                        j += 1
                        continue
                    # Page number
                    if re.match(r'^\d+$', next_stripped):
                        j += 1
                        continue
                    # Header/footer
                    if next_stripped.startswith('EHI Export') or next_stripped.startswith('November 2, 2023') or next_stripped.startswith('©'):
                        j += 1
                        continue
                    # Check if this is a new field (has a data type pattern)
                    if re.search(r'\s(char\(\d+\)|datetime|money|bit|int|uniqueidentifier|decimal\(\d+,\s*\d+\)|smallint|tinyint|varchar\(\d+\)|nvarchar\(\d+\)|float)\s', next_l):
                        break
                    # Check if it's a new section
                    if next_stripped.startswith('Description') and j + 1 < len(lines) and 'File name' in lines[j+1]:
                        break
                    if next_stripped.startswith('EHI Export in CGM APRIMA'):
                        break
                    # It's a continuation line
                    # But only if indented enough (description continuation)
                    if len(next_l) > 0 and (next_l[0] == ' ' or next_l[0] == '\t'):
                        desc += ' ' + next_stripped
                        j += 1
                    else:
                        break
                
                current_file['fields'].append({
                    'column_heading': col_heading,
                    'data_type': data_type,
                    'description': desc
                })
                i = j
                continue
        
        i += 1
    
    return csv_files

def apply_manual_name_fixes(csv_files):
    """Fix CSV file names to match the original document headings."""
    name_map = {
        'AuditTrail': 'Audit Trail',
        'Contacts': 'Contacts',
        'ActiveMedication': 'Active Medication',
        'Allergies': 'Allergies',
        'AppointmentInformation': 'Appointment Information',
        'FamilyHistory': 'Family History',
        'Immunization': 'Immunization',
        'MedicalHistory': 'Medical History',
        'PatientDemographics': 'Patient Demographics',
        'PatientInsurance': 'Patient Insurance',
        'ProblemList': 'Problem List',
        'ResponsibleParty': 'Responsible Party',
        'Results': 'Results',
        'SocialHistory': 'Social History',
        'VisitComment': 'Visit Comments',
        'Vitals': 'Vitals',
        'Eligibility': 'Eligibility',
        'Employment': 'Employment',
        'PatientLedger': 'Patient Ledger',
        'PatientReferrals': 'Patient Referrals',
        'Providers': 'Providers',
        'ResponseReport': 'Response Report',
    }
    for f in csv_files:
        if f['name'] in name_map:
            f['name'] = name_map[f['name']]

def main():
    pdf_path = "downloads/cgm-aprima-electronic-health-information-export-user-guide.pdf"
    text = extract_pdf_text(pdf_path)
    csv_files = parse_data_dictionary(text)
    apply_manual_name_fixes(csv_files)
    
    # Build the full inventory
    inventory = {
        "source_pdf": "cgm-aprima-electronic-health-information-export-user-guide.pdf",
        "source_date": "2023-11-02",
        "product": "CGM APRIMA v19",
        "export_format": "ZIP (CSV files + images + USCDI XML + Complete Patient Chart PDF)",
        "csv_files": csv_files
    }
    
    # Print summary
    total_fields = 0
    fields_with_desc = 0
    fields_with_type = 0
    for f in csv_files:
        n = len(f['fields'])
        total_fields += n
        for field in f['fields']:
            if field.get('description', '').strip():
                fields_with_desc += 1
            if field.get('data_type', '').strip():
                fields_with_type += 1
        print(f"  {f['name']}: {n} fields", file=sys.stderr)
    
    print(f"\nTotal CSV files: {len(csv_files)}", file=sys.stderr)
    print(f"Total fields: {total_fields}", file=sys.stderr)
    print(f"Fields with descriptions: {fields_with_desc}", file=sys.stderr)
    print(f"Fields with data types: {fields_with_type}", file=sys.stderr)
    
    # Write full inventory
    with open('analysis/entity-inventory-full.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    print("\nWrote analysis/entity-inventory-full.json", file=sys.stderr)
    
    # Write summary
    summary = {
        "total_csv_files": len(csv_files),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "files_summary": []
    }
    for cf in csv_files:
        summary["files_summary"].append({
            "name": cf['name'],
            "file_name_pattern": cf['file_name_pattern'],
            "field_count": len(cf['fields']),
            "description": cf['description']
        })
    
    with open('analysis/entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("Wrote analysis/entity-inventory-summary.json", file=sys.stderr)

if __name__ == '__main__':
    main()
