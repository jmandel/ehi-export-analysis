"""
Build corrected entity-inventory-full.json from the enrichment data + PDF verification.
Fixes known enrichment parsing errors identified by cross-referencing pdftotext output.
"""

import json

# Load enrichment base
with open('downloads/enrichment/ehi-data-dictionary.json') as f:
    data = json.load(f)

# Apply corrections based on PDF verification

for cf in data['csv_files']:
    # Fix 1: Audit Trail - missing "Description" field
    if cf['name'] == 'Audit Trail':
        # Insert Description before Type
        new_fields = []
        for field in cf['fields']:
            if field['column_heading'] == 'Type':
                new_fields.append({
                    'column_heading': 'Description',
                    'data_type': 'char(2000)',
                    'description': 'Description of the change made.'
                })
            new_fields.append(field)
        cf['fields'] = new_fields

    # Fix 2: Appointment Information - missing "Appointment Type Code"
    if cf['name'] == 'Appointment Information':
        new_fields = []
        for field in cf['fields']:
            if field['column_heading'] == 'Appointment Type Description':
                new_fields.append({
                    'column_heading': 'Appointment Type Code',
                    'data_type': 'char(25)',
                    'description': 'Appointment type identifier.'
                })
            new_fields.append(field)
        cf['fields'] = new_fields

    # Fix 3: Eligibility - "Authorize Assignment" description was merged with next field
    if cf['name'] == 'Eligibility':
        new_fields = []
        for field in cf['fields']:
            if field['column_heading'] == 'Authorize Assignment':
                # Fix: this field has no description in PDF, and Payer Name was next
                new_fields.append({
                    'column_heading': 'Authorize Assignment',
                    'data_type': 'char(5)',
                    'description': ''
                })
                new_fields.append({
                    'column_heading': 'Payer Name',
                    'data_type': 'char(100)',
                    'description': 'Insurance carrier name.'
                })
                continue
            new_fields.append(field)
        # Also add OutNetwork Deductible (missing between InNetwork Deductible and InNetwork Remaining)
        final_fields = []
        for field in new_fields:
            final_fields.append(field)
            if field['column_heading'] == 'InNetwork Deductible':
                final_fields.append({
                    'column_heading': 'OutNetwork Deductible',
                    'data_type': 'money',
                    'description': 'Out of network deductible amount.'
                })
        cf['fields'] = final_fields

    # Fix 4: Patient Ledger - glDate description was merged with whoPaid
    if cf['name'] == 'Patient Ledger':
        new_fields = []
        for field in cf['fields']:
            if field['column_heading'] == 'glDate' and field.get('description') == 'whoPaid':
                new_fields.append({
                    'column_heading': 'glDate',
                    'data_type': 'date',
                    'description': ''
                })
                new_fields.append({
                    'column_heading': 'whoPaid',
                    'data_type': 'char(100)',
                    'description': 'Superbill payer.'
                })
                continue
            new_fields.append(field)
        # Also add lastInsurancePaymentAmount (missing after lastPatientPaymentAmount)
        final_fields = []
        for field in new_fields:
            final_fields.append(field)
            if field['column_heading'] == 'lastPatientPaymentAmount':
                final_fields.append({
                    'column_heading': 'lastInsurancePaymentAmount',
                    'data_type': 'money',
                    'description': 'Amount of last insurance payment.'
                })
        cf['fields'] = final_fields

# Assign categories to each CSV file
category_map = {
    'Audit Trail': 'Administrative',
    'Contacts': 'Demographics',
    'Active Medication': 'Clinical',
    'Allergies': 'Clinical',
    'Appointment Information': 'Administrative',
    'Family History': 'Clinical',
    'Immunization': 'Clinical',
    'Medical History': 'Clinical',
    'Patient Demographics': 'Demographics',
    'Patient Insurance': 'Insurance',
    'Problem List': 'Clinical',
    'Responsible Party': 'Demographics',
    'Results': 'Clinical',
    'Social History': 'Clinical',
    'Visit Comments': 'Clinical',
    'Vitals': 'Clinical',
    'Eligibility': 'Insurance',
    'Employment': 'Demographics',
    'Patient Ledger': 'Billing / Financial',
    'Patient Referrals': 'Clinical',
    'Providers': 'Care Team',
    'Response Report': 'Clinical Decision Support',
}

for cf in data['csv_files']:
    cf['category'] = category_map.get(cf['name'], 'Other')

# Build full inventory
inventory = {
    'source_pdf': 'cgm-aprima-electronic-health-information-export-user-guide.pdf',
    'source_date': '2023-11-02',
    'product': 'CGM APRIMA v19',
    'export_format': 'ZIP (CSV files + images + USCDI XML + Complete Patient Chart PDF)',
    'export_components': data.get('export_components', []),
    'csv_files': data['csv_files']
}

# Calculate stats
total_fields = 0
fields_with_desc = 0
fields_with_type = 0
for cf in data['csv_files']:
    n = len(cf['fields'])
    total_fields += n
    for field in cf['fields']:
        if field.get('description', '').strip():
            fields_with_desc += 1
        if field.get('data_type', '').strip():
            fields_with_type += 1

# Summary
summary = {
    'total_csv_files': len(data['csv_files']),
    'total_fields': total_fields,
    'fields_with_descriptions': fields_with_desc,
    'fields_with_types': fields_with_type,
    'description_coverage_pct': round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    'categories': {},
    'files_summary': []
}

for cf in data['csv_files']:
    cat = cf['category']
    if cat not in summary['categories']:
        summary['categories'][cat] = {'file_count': 0, 'field_count': 0}
    summary['categories'][cat]['file_count'] += 1
    summary['categories'][cat]['field_count'] += len(cf['fields'])
    
    n_desc = sum(1 for f in cf['fields'] if f.get('description', '').strip())
    summary['files_summary'].append({
        'name': cf['name'],
        'category': cf['category'],
        'file_name_pattern': cf.get('file_name_pattern', ''),
        'field_count': len(cf['fields']),
        'fields_with_descriptions': n_desc,
        'description': cf.get('description', '')
    })

with open('analysis/entity-inventory-full.json', 'w') as f:
    json.dump(inventory, f, indent=2)

with open('analysis/entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# Print verification
print(f"Total CSV files: {len(data['csv_files'])}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['description_coverage_pct']}%)")
print(f"Fields with types: {fields_with_type}")
print()
for cf in data['csv_files']:
    n_desc = sum(1 for fld in cf['fields'] if fld.get('description', '').strip())
    print(f"  {cf['name']:30s} {len(cf['fields']):3d} fields  ({n_desc} described)  [{cf['category']}]")
print()
print("By category:")
for cat, stats in sorted(summary['categories'].items()):
    print(f"  {cat:30s} {stats['file_count']:2d} files, {stats['field_count']:3d} fields")
