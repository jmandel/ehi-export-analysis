"""
Refined domain categorization for all 1,256 Juno EHR tables.
Groups tables into EHI-relevant clinical/billing domains and reference/lookup categories.
"""
import json

with open('jehr_full_inventory.json') as f:
    inventory = json.load(f)

# More comprehensive categorization 
rules = [
    ('Pharmacy / Prescriptions (AU_)', lambda n: n.startswith('AU_')),
    ('Billing / Revenue Cycle', lambda n: any(n.startswith(p) for p in ['BILLINGITEM', 'BILLTYPE', 'BILLHOLDREASON', 'RCM', 'CHARGEITEM', 'TRANSACTIONCODE', 'FINANCIALGROUP', 'SLIDINGSCALE', 'ACCOMMODATION', 'LOCATIONACCOMMODATION'])),
    ('Medical Coding', lambda n: n.startswith('MEDICALCODING')),
    ('Patient Demographics', lambda n: n.startswith('PATIENT') or n.startswith('RELATEDPERSON') or n == 'MEDICALRECORDNUMBER'),
    ('Encounter / Visit', lambda n: n.startswith('ENCOUNTER') or n.startswith('EPISODEOFCARE') or n.startswith('BEDSTATUS') or n.startswith('BEDALLOWED') or n.startswith('ADMISSIONWAITLIST') or n.startswith('ADMITTINGCRIMINAL')),
    ('Coverage / Insurance', lambda n: n.startswith('COVERAGE') or n.startswith('MSPQ')),
    ('Care Plan / Treatment Plan', lambda n: n.startswith('CAREPLAN') or n.startswith('CARETEAM') or n.startswith('TREATMENTPLAN')),
    ('Goal / Intervention', lambda n: n.startswith('GOAL') or n.startswith('INTERVENTION') or n.startswith('PROBLEMDEFINITION')),
    ('Condition / Problem', lambda n: n.startswith('CONDITION') or n == 'HEALTHCONCERNREVIEW'),
    ('Allergy', lambda n: n.startswith('ALLERGY')),
    ('Observation / Vitals', lambda n: n.startswith('OBSERVATION') or n.startswith('DRAFTOBSERVATION') or n.startswith('REFERENCERANGE')),
    ('Medication', lambda n: n.startswith('MEDICATION') or n.startswith('DRUG') or n.startswith('DOSAGE') or n.startswith('ROUTE')),
    ('Immunization', lambda n: n.startswith('IMMUNIZATION')),
    ('Surgery / Procedure', lambda n: n.startswith('SURGERY') or n.startswith('IMPLANTABLEDEVICE') or n.startswith('ANESTHESIA')),
    ('Procedure', lambda n: n.startswith('PROCEDURE')),
    ('Imaging', lambda n: n.startswith('IMAGING')),
    ('Laboratory / Specimen', lambda n: n.startswith('SPECIMEN') or n.startswith('LABORATORY')),
    ('Document / Notes', lambda n: n.startswith('DOCUMENT') or n.startswith('AMENDMENTREQUEST') or n.startswith('NARRATIVE') or n.startswith('NOTE') or n.startswith('FILESTORAGE') or n.startswith('CLINICALNOTESCONFIG')),
    ('Media', lambda n: n.startswith('MEDIA')),
    ('Questionnaire / Assessment', lambda n: n.startswith('QUESTIONNAIRE')),
    ('Order', lambda n: n.startswith('ORDER') or n.startswith('PENDINGORDER') or n.startswith('DETECTEDISSUE')),
    ('Nutrition Request', lambda n: n.startswith('NUTRITION')),
    ('Diagnostic Report', lambda n: n.startswith('DIAGNOSTICREPORT')),
    ('Schedule / Appointment', lambda n: n.startswith('SCHEDULE') or n.startswith('SLOT')),
    ('Group (Session)', lambda n: n.startswith('GROUP') or n.startswith('RECURRENCEPATTERN')),
    ('Communication', lambda n: 'COMMUNICATION' in n),
    ('Consent', lambda n: n.startswith('CONSENT')),
    ('Service Request / Referral', lambda n: n.startswith('SERVICEREQUEST') or n.startswith('CONSULTSNOTESREVIEW')),
    ('Release of Information', lambda n: n.startswith('RELEASEOFINFORMATION')),
    ('Item (Charge Definition)', lambda n: n.startswith('ITEM')),
    ('Healthcare Service', lambda n: n.startswith('HEALTHCARESERVICE')),
    ('Location / Organization', lambda n: n.startswith('HCS') or n == 'LOCATION' or n.startswith('ORGANIZATION') or n.startswith('LOCATIONIDENTIFIER') or n.startswith('LOCATIONTYPE')),
    ('Account', lambda n: n.startswith('ACCOUNT')),
    ('Task', lambda n: n.startswith('TASK')),
    ('Contact', lambda n: n.startswith('CONTACT') or n.startswith('EMERGENCYCONTACT')),
    ('Device', lambda n: n.startswith('DEVICE')),
    ('Legal Status (Behavioral Health)', lambda n: n.startswith('LEGALSTATUS') or n.startswith('CRIMINALCHARGE')),
    ('Behavioral Health', lambda n: n.startswith('BEHAVIORAL')),
    ('Practitioner', lambda n: n.startswith('PRACTITIONER')),
    ('Provenance / Audit', lambda n: n.startswith('PROVENANCE') or n.startswith('SENSITIVEPATIENT') or n.startswith('CHARTRESTRICTION') or n.startswith('TRACE_XE')),
    ('Clinical Task', lambda n: n.startswith('CLINICALTASK')),
    ('Program Code', lambda n: n.startswith('PROGRAMCODE')),
    ('Identifier', lambda n: n == 'IDENTIFIER' or (n.startswith('IDENTIFIER') and not n.startswith('IDENTIFIERTYPE'))),
    ('Timing', lambda n: n.startswith('TIMING')),
    ('Coding / Value', lambda n: n in ['VALUE', 'VALUECODING', 'CODING'] or n.startswith('CODING')),
    ('Manufacturer', lambda n: n.startswith('MANUFACTURER')),
    ('Quantity', lambda n: n == 'QUANTITY'),
    ('Address', lambda n: n == 'ADDRESS'),
    ('Lookup Tables', lambda n: n.startswith('LK')),
]

categorized = {}
uncategorized = []
for name in sorted(inventory.keys()):
    found = False
    for cat, test in rules:
        if test(name):
            categorized.setdefault(cat, []).append(name)
            found = True
            break
    if not found:
        uncategorized.append(name)

# Print summary
print('=== REFINED DOMAIN CATEGORIZATION ===\n')
print(f'{"Category":<45} {"Tables":>6} {"Columns":>7} {"Described":>9}')
print('-' * 75)

all_data = []
for cat in sorted(categorized.keys(), key=lambda c: -sum(inventory[t]['column_count'] for t in categorized[c])):
    tables = categorized[cat]
    total_cols = sum(inventory[t]['column_count'] for t in tables)
    desc_cols = sum(inventory[t]['columns_with_descriptions'] for t in tables)
    all_data.append((cat, len(tables), total_cols, desc_cols))
    print(f'{cat:<45} {len(tables):>6} {total_cols:>7} {desc_cols:>9}')

if uncategorized:
    total_cols = sum(inventory[t]['column_count'] for t in uncategorized)
    print(f'{"[Uncategorized]":<45} {len(uncategorized):>6} {total_cols:>7}')
    print('\nUncategorized:')
    for t in uncategorized:
        print(f'  {t}: {inventory[t]["column_count"]} cols - {inventory[t]["description"][:80]}')

# Grand totals
total_t = sum(len(categorized[c]) for c in categorized) + len(uncategorized)
total_c = sum(inventory[t]['column_count'] for t in inventory)
total_d = sum(inventory[t]['columns_with_descriptions'] for t in inventory)
print(f'\n{"TOTAL":<45} {total_t:>6} {total_c:>7} {total_d:>9}')

# EHI domain mapping (excluding lookup tables)
non_lk = sum(1 for t in inventory if not t.startswith('LK'))
non_lk_cols = sum(inventory[t]['column_count'] for t in inventory if not t.startswith('LK'))
lk_count = sum(1 for t in inventory if t.startswith('LK'))
lk_cols = sum(inventory[t]['column_count'] for t in inventory if t.startswith('LK'))
print(f'\nEntity tables (non-lookup): {non_lk} tables, {non_lk_cols} columns')
print(f'Lookup/reference tables: {lk_count} tables, {lk_cols} columns')

# Save refined summary
refined = {}
for cat, tables in categorized.items():
    total_cols = sum(inventory[t]['column_count'] for t in tables)
    desc_cols = sum(inventory[t]['columns_with_descriptions'] for t in tables)
    refined[cat] = {
        'table_count': len(tables),
        'total_columns': total_cols,
        'described_columns': desc_cols,
        'tables': tables
    }
with open('jehr_refined_domain_summary.json', 'w') as f:
    json.dump(refined, f, indent=2)

