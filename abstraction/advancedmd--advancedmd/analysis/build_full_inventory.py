#!/usr/bin/env python3
"""Parse all AdvancedMD EHI export artifacts into a comprehensive inventory.

Combines:
1. EHR Bulk Export Data Dictionary (SQL .bak) - 12 tables
2. C-CDA Data Dictionary - section mappings
3. HTML page content - CSV/MDB export field lists
4. Scanned Documents guidance

Outputs full-entity-inventory.json with all export mechanisms and their content.
"""

import json
import re
import subprocess

DOWNLOADS = "../../../results/advancedmd--advancedmd/downloads"

def parse_ccda_dictionary():
    """Parse the C-CDA data dictionary PDF into sections."""
    result = subprocess.run(
        ["pdftotext", "-layout", f"{DOWNLOADS}/advancedmd-dataExport-dataDictionary.pdf", "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    sections = []
    lines = text.split('\n')
    
    current_section = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('LEGAL') or stripped.startswith('DATA EXPORT'):
            continue
        if stripped.startswith('Field Name') or stripped.startswith('Required Text'):
            continue
        
        # Section names are in the first column, like "Allergies", "Medications"
        # They have vocabulary codes after them
        # Look for known section names
        section_names = [
            'Allergies', 'Medications', 'Problem List', 'Encounters', 'Procedure List',
            'Procedure Note', 'Immunization', 'Functional Status', 'Mental (Cognitive) Status',
            'Assessments', 'Goals', 'Health Concerns', 'Plan of Treatment',
            'Social History/Sex', 'Lab Results', 'Lab Narrative', 'Medical Equipment',
            'Vital Signs', 'Pediatric Vital Signs', 'Care Team Information',
            'Consultation Notes', 'History and Physical Notes', 'Discharge Summary',
            'Progress Note', 'Imaging Narrative', 'Pathology Narrative',
            'Advanced Directives'
        ]
        
        for sn in section_names:
            if stripped.startswith(sn) and (current_section is None or current_section['name'] != sn):
                if current_section:
                    sections.append(current_section)
                current_section = {
                    'name': sn,
                    'vocabulary_codes': [],
                    'description_lines': []
                }
                # Extract vocab codes from same line
                rest = stripped[len(sn):].strip()
                codes = re.findall(r'(RxNorm|SNOMED|ICD10|CPT|LOINC)\s*(\S*)', rest)
                for code_type, code_val in codes:
                    entry = {'system': code_type}
                    if code_val:
                        entry['code'] = code_val
                    current_section['vocabulary_codes'].append(entry)
                break
        else:
            if current_section:
                # Check for additional vocab codes on subsequent lines
                codes = re.findall(r'(RxNorm|SNOMED|ICD10|CPT|LOINC)\s+(\S+)', stripped)
                if codes:
                    for code_type, code_val in codes:
                        entry = {'system': code_type}
                        if code_val and code_val not in ('N/A', 'and'):
                            entry['code'] = code_val
                        current_section['vocabulary_codes'].append(entry)
                elif stripped and not stripped.startswith('('):
                    current_section['description_lines'].append(stripped)
    
    if current_section:
        sections.append(current_section)
    
    return sections

def parse_html_csv_fields():
    """Parse the HTML page to extract CSV export field lists."""
    with open(f"{DOWNLOADS}/data-export-page.html", 'r') as f:
        content = f.read()
    
    # Remove tags to get text
    text_clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text_clean = re.sub(r'<style[^>]*>.*?</style>', '', text_clean, flags=re.DOTALL)
    text_clean = re.sub(r'<[^>]+>', '\n', text_clean)
    
    import html
    text_clean = html.unescape(text_clean)
    text_clean = re.sub(r'\n{3,}', '\n\n', text_clean)
    
    exports = {}
    
    # Patient Transaction Report fields (from the flyer/HTML)
    exports['patient_transaction_report'] = {
        'name': 'Patient Transaction Report',
        'format': 'CSV',
        'scope': 'single_patient',
        'mechanism': 'Reports > Patient Listings > Patient Transaction Report',
        'requires_developer': False,
        'header_fields': [
            'Patient', 'Chart Number', 'Address', 'Birthdate', 'Responsible Party',
            'Phone', 'Email', 'Provider', 'SSN', 'Sex',
            'Insurance (Primary)', 'Insurance (Secondary)', 'Insurance (Tertiary)'
        ],
        'body_fields': [
            'Transaction Type', 'Visit Number', 'Facility Name', 'Provider',
            'Charge Code', 'Transaction Code', 'Transaction Code Description',
            'Modifiers', 'Visit Primary', 'Visit Secondary', 'Transaction Carrier',
            'Primary Diagnosis', 'Payment Method', 'Check Number',
            'Date of Service', 'Date of Entry', 'Date of Deposit', 'Void',
            'Units', 'Charges', 'Patient Payments', 'Insurance Payments',
            'Total Payments', 'Adjustments'
        ]
    }
    
    exports['patient_visit_summary'] = {
        'name': 'Patient Visit Summary Report',
        'format': 'CSV',
        'scope': 'single_patient',
        'mechanism': 'Reports > Patient Listings > Patient Visit Summary',
        'requires_developer': False,
        'header_fields': [
            'Patient', 'Birthdate', 'Chart Number', 'Email'
        ],
        'body_fields': [
            'Visit Number', 'Date of Service', 'Charge Code',
            'Charge Code Description', 'Claim Charge Code',
            'Claim Charge Code Description', 'CPT Code', 'CPT Code Description',
            'Diagnosis Codes', 'Modifiers', 'Place of Service', 'Carrier',
            'Copay', 'Current Balance', 'Billing Provider', 'Group Name',
            'Provider Name', 'Facility Name', 'Facility Code',
            'Appointment Status', 'Appointment Date', 'Appointment Time',
            'Appointment Type'
        ]
    }
    
    exports['ehr_data_portability'] = {
        'name': 'EHR Data Portability Export Tool',
        'format': 'C-CDA XML + HTML',
        'scope': 'single_patient',
        'mechanism': 'EHR > Tools > Data Portability Export Tool',
        'requires_developer': False,
        'sections': [
            'Allergies', 'Adverse Reactions and Alerts', 'Medications',
            'Problems', 'Procedures', 'Results', 'Medical Equipment',
            'Vital Signs', 'Assessments', 'Plan of Treatment', 'Goals',
            'Health Concerns', 'Consultation Note', 'History and Physical Note',
            'Progress Note', 'Discharge Summary', 'Imaging Narrative',
            'Pathology Narrative', 'Immunizations', 'Reason for Referral',
            'Functional Status', 'Mental Status', 'Encounters', 'Social History',
            'Care Team Information', 'Advance Directives'
        ]
    }
    
    exports['ehr_chart_print'] = {
        'name': 'EHR Patient Chart Print Tool',
        'format': 'PDF',
        'scope': 'single_patient',
        'mechanism': 'Chart Print icon in patient chart',
        'requires_developer': False,
        'sections': [
            'Demographics', 'Insurance', 'Patient Allergies', 'Problems List',
            'Immunization History', 'Risk Factors', 'Advanced Directives',
            'Misc Info Note', 'Audit Trail', 'Messages', 'Annotations',
            'Healthwatcher Items', 'Education Lists',
            'Patient Portal and Staff Messages',
            'Current and Historical Medications', 'Orders/Tests',
            'Appointments', 'Documents Saved to Chart', 'Results',
            'Patient Notes'
        ]
    }
    
    exports['pm_data_export'] = {
        'name': 'Practice Management Data Export',
        'format': 'Microsoft Access .mdb',
        'scope': 'bulk',
        'mechanism': 'Utilities > Data Export',
        'requires_developer': False,
        'content': [
            'Demographics (always included)', 'Transactions (optional)',
            'Appointment data (optional)', 'Charges', 'Payments', 'Write-offs',
            'Patient demographics', 'Provider information',
            'Appointments', 'Carrier information'
        ]
    }
    
    exports['scanned_docs_images'] = {
        'name': 'Scanned Documents & Images',
        'format': 'Native file formats (JPG, DOC, etc.) with text index files',
        'scope': 'bulk',
        'mechanism': 'Contact Client Support Services',
        'requires_developer': True,
        'content': [
            'PM Documents (decrypted-pm folder)',
            'EHR Documents (decrypted-ehr folder)',
            'PM index file (PM.Export.XXXXXX)',
            'EHR index file (EHR.docmap.Export.XXXXXX)',
            'EHR blob data CSV',
            'PM templates CSV'
        ],
        'pm_index_columns': [
            'FirstName', 'LastName', 'ChartNumber', 'ProfileCode',
            'CategoryName', 'FileLocation', 'FileName'
        ],
        'ehr_index_columns': [
            'File_Key_Ptr', 'Document_UID'
        ]
    }
    
    return exports

def build_full_inventory():
    """Build the comprehensive entity inventory."""
    
    # Load EHR bulk inventory
    with open('ehr-bulk-inventory.json') as f:
        ehr_bulk = json.load(f)
    
    # Parse C-CDA dictionary
    ccda_sections = parse_ccda_dictionary()
    
    # Parse HTML/flyer CSV fields
    other_exports = parse_html_csv_fields()
    
    # Build complete inventory
    inventory = {
        'vendor': 'AdvancedMD',
        'product': 'AdvancedMD',
        'analysis_date': '2026-02-16',
        'sources': [
            'advancedmd-ehrExport-dataDictionary.pdf (13 pages)',
            'advancedmd-dataExport-dataDictionary.pdf (6 pages)',
            'advancedmd-bulkDataExport-scannedDocsImages.pdf (9 pages)',
            'advancedmd-flyer-dataExport.pdf (2 pages)',
            'data-export-page.html'
        ],
        'export_mechanisms': {
            'single_patient': [
                other_exports['patient_transaction_report'],
                other_exports['patient_visit_summary'],
                other_exports['ehr_data_portability'],
                other_exports['ehr_chart_print']
            ],
            'bulk': [
                other_exports['pm_data_export'],
                other_exports['scanned_docs_images'],
                {
                    'name': 'EHR Bulk Data Export',
                    'format': 'SQL Server .bak file',
                    'scope': 'bulk',
                    'mechanism': 'Contact Client Support Services',
                    'requires_developer': True,
                    'tables': ehr_bulk['tables'],
                    'total_tables': ehr_bulk['total_tables'],
                    'total_fields': ehr_bulk['total_fields'],
                    'fields_with_descriptions': ehr_bulk['fields_with_descriptions']
                }
            ]
        },
        'ccda_sections': ccda_sections,
        'summary_statistics': {
            'total_export_mechanisms': 7,
            'single_patient_mechanisms': 4,
            'bulk_mechanisms': 3,
            'ehr_bulk_tables': ehr_bulk['total_tables'],
            'ehr_bulk_fields': ehr_bulk['total_fields'],
            'ehr_bulk_fields_with_descriptions': ehr_bulk['fields_with_descriptions'],
            'ehr_bulk_description_rate': round(
                ehr_bulk['fields_with_descriptions'] / ehr_bulk['total_fields'] * 100, 1
            ),
            'ccda_sections': len(ccda_sections),
            'pm_csv_fields': {
                'transaction_report': {
                    'header': len(other_exports['patient_transaction_report']['header_fields']),
                    'body': len(other_exports['patient_transaction_report']['body_fields']),
                    'total': len(other_exports['patient_transaction_report']['header_fields']) + 
                             len(other_exports['patient_transaction_report']['body_fields'])
                },
                'visit_summary': {
                    'header': len(other_exports['patient_visit_summary']['header_fields']),
                    'body': len(other_exports['patient_visit_summary']['body_fields']),
                    'total': len(other_exports['patient_visit_summary']['header_fields']) + 
                             len(other_exports['patient_visit_summary']['body_fields'])
                }
            }
        }
    }
    
    with open('full-entity-inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    stats = inventory['summary_statistics']
    print("=== AdvancedMD EHI Export Full Inventory ===")
    print(f"Export mechanisms: {stats['total_export_mechanisms']} total")
    print(f"  Single patient: {stats['single_patient_mechanisms']}")
    print(f"  Bulk: {stats['bulk_mechanisms']}")
    print()
    print(f"EHR Bulk Export (SQL .bak):")
    print(f"  Tables: {stats['ehr_bulk_tables']}")
    print(f"  Fields: {stats['ehr_bulk_fields']}")
    print(f"  Fields with descriptions: {stats['ehr_bulk_fields_with_descriptions']} ({stats['ehr_bulk_description_rate']}%)")
    print()
    print(f"C-CDA Export sections: {stats['ccda_sections']}")
    for s in ccda_sections:
        codes = ', '.join(f"{c['system']}:{c.get('code','')}" for c in s['vocabulary_codes'])
        print(f"  - {s['name']}" + (f" [{codes}]" if codes else ""))
    print()
    print(f"Patient Transaction Report: {stats['pm_csv_fields']['transaction_report']['total']} fields")
    print(f"Patient Visit Summary: {stats['pm_csv_fields']['visit_summary']['total']} fields")
    print()
    print("Saved to full-entity-inventory.json")

if __name__ == '__main__':
    build_full_inventory()
