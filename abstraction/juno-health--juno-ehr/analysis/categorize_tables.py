"""Categorize JEHR tables by naming prefix/pattern to understand domain coverage."""

import json

with open('table_index.json') as f:
    data = json.load(f)

jehr_tables = [t['name'] for t in data['jehr']['tables']]
rtvx_tables = [t['name'] for t in data['rtvx']['tables']]

# Define prefix-based categories
categories = {
    'Prescription/Pharmacy (AU_)': [],
    'Allergy': [],
    'Billing/Account': [],
    'Care Plan/Treatment Plan': [],
    'Condition/Problem': [],
    'Document/Note': [],
    'Encounter/Visit': [],
    'Group Session': [],
    'Immunization': [],
    'Medication': [],
    'Observation/Vital/Lab': [],
    'Order': [],
    'Patient/Demographics': [],
    'Procedure/Surgery': [],
    'Questionnaire/Assessment': [],
    'Referral': [],
    'Schedule/Appointment': [],
    'Lookup Tables (LK)': [],
    'Other': [],
}

def categorize(name):
    n = name.upper()
    if n.startswith('AU_PRESCRIPTION') or n.startswith('AU_'):
        return 'Prescription/Pharmacy (AU_)'
    if 'ALLERGY' in n or 'ALLERGEN' in n:
        return 'Allergy'
    if any(x in n for x in ['BILLING', 'ACCOUNT', 'CHARGE', 'CLAIM', 'COVERAGE', 'PAYER', 'PAYMENT', 'INVOICE', 'INSURANCE', 'COPAY', 'GUARANTOR', 'FINANCIAL']):
        return 'Billing/Account'
    if any(x in n for x in ['CAREPLAN', 'CARE_PLAN', 'TREATMENT_PLAN', 'TREATMENTPLAN', 'GOAL']):
        return 'Care Plan/Treatment Plan'
    if any(x in n for x in ['CONDITION', 'PROBLEM', 'DIAGNOSIS', 'DIAGNOS']):
        return 'Condition/Problem'
    if any(x in n for x in ['DOCUMENT', 'NOTE', 'NARRATIVE', 'AMENDMENT']):
        return 'Document/Note'
    if any(x in n for x in ['ENCOUNTER', 'ADMISSION', 'DISCHARGE', 'TRANSFER', 'VISIT', 'BED', 'CENSUS']):
        return 'Encounter/Visit'
    if any(x in n for x in ['GROUP_SESSION', 'GROUPSESSION', 'BEHAVIORAL']):
        return 'Group Session'
    if any(x in n for x in ['IMMUNIZATION', 'VACCINE', 'FORECAST']):
        return 'Immunization'
    if any(x in n for x in ['MEDICATION', 'DRUG', 'FORMULARY', 'PHARMACY', 'PRESCRIPTION', 'MED_']):
        return 'Medication'
    if any(x in n for x in ['OBSERVATION', 'VITAL', 'LAB', 'RESULT', 'SPECIMEN']):
        return 'Observation/Vital/Lab'
    if any(x in n for x in ['ORDER', 'ORDERABLE']):
        return 'Order'
    if any(x in n for x in ['PATIENT', 'PERSON', 'CONTACT', 'GUARDIAN', 'DEMOGRAPHIC', 'RACE', 'ETHNICITY', 'LANGUAGE', 'IDENTIFIER']):
        return 'Patient/Demographics'
    if any(x in n for x in ['PROCEDURE', 'SURGERY', 'SURGICAL', 'PERIOP', 'ANESTHES', 'IMPLANT']):
        return 'Procedure/Surgery'
    if any(x in n for x in ['QUESTIONNAIRE', 'QUESTION', 'ASSESSMENT', 'RESPONSE', 'SURVEY', 'FORM']):
        return 'Questionnaire/Assessment'
    if any(x in n for x in ['REFERRAL', 'CONSULT']):
        return 'Referral'
    if any(x in n for x in ['SCHEDULE', 'APPOINTMENT', 'SLOT', 'BOOKING', 'CALENDAR', 'AVAILABILITY']):
        return 'Schedule/Appointment'
    if n.startswith('LK'):
        return 'Lookup Tables (LK)'
    return 'Other'

# Categorize JEHR
jehr_cats = {}
for t in jehr_tables:
    cat = categorize(t)
    if cat not in jehr_cats:
        jehr_cats[cat] = []
    jehr_cats[cat].append(t)

print("=== JEHR Table Categories ===")
for cat in sorted(jehr_cats.keys()):
    tables = jehr_cats[cat]
    print(f"\n{cat}: {len(tables)} tables")
    # Show first 5
    for t in tables[:5]:
        print(f"  - {t}")
    if len(tables) > 5:
        print(f"  ... and {len(tables)-5} more")

# Categorize RxTracker
rtvx_cats = {}
for t in rtvx_tables:
    cat = categorize(t)
    if cat not in rtvx_cats:
        rtvx_cats[cat] = []
    rtvx_cats[cat].append(t)

print("\n=== RxTracker Table Categories ===")
for cat in sorted(rtvx_cats.keys()):
    tables = rtvx_cats[cat]
    print(f"\n{cat}: {len(tables)} tables")
    for t in tables:
        print(f"  - {t}")

# Save categorized data
cat_output = {
    'jehr_categories': {k: v for k, v in sorted(jehr_cats.items())},
    'rtvx_categories': {k: v for k, v in sorted(rtvx_cats.items())},
    'jehr_summary': {k: len(v) for k, v in sorted(jehr_cats.items())},
    'rtvx_summary': {k: len(v) for k, v in sorted(rtvx_cats.items())}
}

with open('table_categories.json', 'w') as f:
    json.dump(cat_output, f, indent=2)

print("\nSaved to table_categories.json")
