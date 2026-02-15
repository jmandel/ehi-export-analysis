"""
Categorize Juno EHR tables by domain based on naming patterns.
"""
import json

with open('jehr_full_inventory.json') as f:
    inventory = json.load(f)

# Define categorization rules based on table name prefixes/patterns
categories = {
    'Pharmacy / Prescriptions': lambda n: n.startswith('AU_') and not n.startswith('AU_NON'),
    'Non-Verified Orders': lambda n: n.startswith('AU_NON'),
    'Billing / Revenue Cycle': lambda n: any(n.startswith(p) for p in ['BILLINGITEM', 'BILLTYPE', 'RCM', 'CLAIM', 'CHARGEITEM', 'TRANSACTIONCODE']),
    'Patient Demographics': lambda n: n.startswith('PATIENT') and 'BILLING' not in n,
    'Encounter / Visit': lambda n: n.startswith('ENCOUNTER'),
    'Coverage / Insurance': lambda n: n.startswith('COVERAGE'),
    'Care Plan / Treatment Plan': lambda n: n.startswith('CAREPLAN') or n.startswith('CARETEAM') or n.startswith('TREATMENTPLAN'),
    'Condition / Problem': lambda n: n.startswith('CONDITION'),
    'Allergy': lambda n: n.startswith('ALLERGY'),
    'Observation / Vitals': lambda n: n.startswith('OBSERVATION'),
    'Medication': lambda n: n.startswith('MEDICATION') and not n.startswith('MEDICATIONBARCODE'),
    'Medication Barcode': lambda n: n.startswith('MEDICATIONBARCODE'),
    'Immunization': lambda n: n.startswith('IMMUNIZATION'),
    'Surgery / Procedure': lambda n: n.startswith('SURGERY') or n.startswith('IMPLANTABLEDEVICE'),
    'Procedure': lambda n: n.startswith('PROCEDURE') and 'SURGERY' not in n,
    'Document / Notes': lambda n: n.startswith('DOCUMENT') or n.startswith('AMENDMENTREQUEST') or n.startswith('NARRATIVE'),
    'Questionnaire / Assessment': lambda n: n.startswith('QUESTIONNAIRE'),
    'Order': lambda n: n.startswith('ORDER'),
    'Diagnostic Report': lambda n: n.startswith('DIAGNOSTICREPORT'),
    'Schedule / Appointment': lambda n: n.startswith('SCHEDULE') or n.startswith('SLOT'),
    'Group (Session)': lambda n: n == 'GROUP' or n.startswith('GROUP'),
    'Goal': lambda n: n.startswith('GOAL'),
    'Communication': lambda n: 'COMMUNICATION' in n and 'CLINICALCOMMUNICATION' not in n,
    'Clinical Communication': lambda n: 'CLINICALCOMMUNICATION' in n,
    'Consent': lambda n: n.startswith('CONSENT'),
    'Service Request / Referral': lambda n: n.startswith('SERVICEREQUEST'),
    'Specimen': lambda n: n.startswith('SPECIMEN'),
    'Item / Charge': lambda n: n == 'ITEM' or n.startswith('ITEM'),
    'Identifier': lambda n: n.startswith('IDENTIFIER'),
    'Location (HCS)': lambda n: n.startswith('HCS') or n == 'LOCATION',
    'Episode of Care': lambda n: n.startswith('EPISODEOFCARE'),
    'Account': lambda n: n.startswith('ACCOUNT'),
    'Task': lambda n: n.startswith('TASK'),
    'Contact': lambda n: n.startswith('CONTACT') or n.startswith('EMERGENCYCONTACT'),
    'Nurse Brain': lambda n: n.startswith('NURSEBRAIN'),
    'Organization': lambda n: n.startswith('ORGANIZATION'),
    'Timing': lambda n: n.startswith('TIMING'),
    'Lookup Tables': lambda n: n.startswith('LK'),
    'Coding / Value': lambda n: n in ['VALUE', 'VALUECODING', 'CODING'] or n.startswith('CODING'),
}

# Categorize tables
categorized = {}
uncategorized = []

for name in sorted(inventory.keys()):
    found = False
    for cat, test in categories.items():
        if test(name):
            categorized.setdefault(cat, []).append(name)
            found = True
            break
    if not found:
        uncategorized.append(name)

# Print results
print("=== DOMAIN CATEGORIZATION ===\n")
for cat in sorted(categorized.keys(), key=lambda c: -len(categorized[c])):
    tables = categorized[cat]
    total_cols = sum(inventory[t]['column_count'] for t in tables)
    print(f"{cat}: {len(tables)} tables, {total_cols} columns")
    for t in tables[:5]:
        info = inventory[t]
        print(f"  - {t}: {info['column_count']} cols")
    if len(tables) > 5:
        print(f"  ... and {len(tables)-5} more")

print(f"\nUncategorized: {len(uncategorized)} tables")
for t in uncategorized:
    info = inventory[t]
    print(f"  - {t}: {info['column_count']} cols - {info['description'][:80]}")

# Save summary
summary = {}
for cat, tables in categorized.items():
    total_cols = sum(inventory[t]['column_count'] for t in tables)
    desc_cols = sum(inventory[t]['columns_with_descriptions'] for t in tables)
    summary[cat] = {
        'table_count': len(tables),
        'total_columns': total_cols,
        'described_columns': desc_cols,
        'tables': tables
    }

summary['Uncategorized'] = {
    'table_count': len(uncategorized),
    'total_columns': sum(inventory[t]['column_count'] for t in uncategorized),
    'described_columns': sum(inventory[t]['columns_with_descriptions'] for t in uncategorized),
    'tables': uncategorized
}

with open('jehr_domain_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# EHI domain mapping
print("\n\n=== EHI DOMAIN MAPPING ===\n")
ehi_domains = {
    'Demographics': ['Patient Demographics', 'Contact'],
    'Encounters / Visits': ['Encounter / Visit', 'Episode of Care'],
    'Problems / Conditions': ['Condition / Problem'],
    'Medications / Prescriptions': ['Pharmacy / Prescriptions', 'Medication', 'Medication Barcode', 'Non-Verified Orders'],
    'Allergies': ['Allergy'],
    'Immunizations': ['Immunization'],
    'Vitals / Observations': ['Observation / Vitals'],
    'Lab / Diagnostic Reports': ['Diagnostic Report', 'Specimen'],
    'Procedures': ['Surgery / Procedure', 'Procedure'],
    'Clinical Notes / Documents': ['Document / Notes', 'Clinical Communication', 'Nurse Brain', 'Narrative'],
    'Care Plans / Goals': ['Care Plan / Treatment Plan', 'Goal'],
    'Orders / Referrals': ['Order', 'Service Request / Referral', 'Task'],
    'Insurance / Coverage': ['Coverage / Insurance'],
    'Claims / Billing': ['Billing / Revenue Cycle', 'Account', 'Item / Charge'],
    'Questionnaires / Assessments': ['Questionnaire / Assessment'],
    'Scheduling': ['Schedule / Appointment'],
    'Consent': ['Consent'],
    'Patient Communications': ['Communication'],
    'Group Therapy': ['Group (Session)'],
}

for domain, cats in ehi_domains.items():
    total_tables = 0
    total_cols = 0
    for cat in cats:
        if cat in summary:
            total_tables += summary[cat]['table_count']
            total_cols += summary[cat]['total_columns']
    if total_tables > 0:
        print(f"✅ {domain}: {total_tables} tables, {total_cols} columns")
    else:
        print(f"❌ {domain}: No tables found")

# Lookup tables
lk = summary.get('Lookup Tables', {})
print(f"\nLookup/Reference tables: {lk.get('table_count', 0)} tables, {lk.get('total_columns', 0)} columns")

