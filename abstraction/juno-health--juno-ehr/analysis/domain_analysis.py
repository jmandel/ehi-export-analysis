"""Analyze domain coverage using parsed table names AND descriptions.
Produces categorized summary with field counts."""

import json

with open('full-entity-inventory.json') as f:
    inv = json.load(f)

# Domain classification rules using table names and descriptions
def classify_domain(entity):
    name = entity.get('table_name', '').upper()
    desc = entity.get('description', '').upper()
    
    # Most specific matches first
    if name.startswith('AU_'):
        return 'Pharmacy/Prescriptions (VA legacy)'
    
    if any(x in name for x in ['IMMUNIZATION', 'VACCINE', 'FORECAST']):
        return 'Immunizations'
    
    if any(x in name for x in ['ALLERGY', 'ALLERGEN', 'ADVERSEEVENT']):
        return 'Allergies/Adverse Events'
    
    if any(x in name for x in ['CAREPLAN', 'CARE_PLAN', 'TREATMENTPLAN', 'TREATMENT_PLAN']):
        return 'Care Plans/Treatment Plans'
    
    if any(x in name for x in ['GROUPSESSION', 'GROUP_SESSION']):
        return 'Behavioral Health'
    if 'BEHAVIORALHEALTH' in name:
        return 'Behavioral Health'
    
    if any(x in name for x in ['RCM', 'BILLING', 'CLAIM', 'CHARGEITEM', 'INVOICE', 'COVERAGE', 'ACCOUNT']):
        if 'ACCOUNTING' not in name or 'RCM' in name:
            return 'Billing/Revenue Cycle'
    if name.startswith('ACCOUNT') or name in ('COVERAGE', 'COVERAGECLASS', 'COVERAGECOSTTOBENEFICIARY',
        'COVERAGECOSTTOBENEFICIARYCODING', 'COVERAGEIDENTIFIER', 'COVERAGEEXCEPTION',
        'COVERAGEEXCEPTIONCODING'):
        return 'Billing/Revenue Cycle'
    
    if any(x in name for x in ['CONDITION', 'PROBLEM']):
        if 'CONDITION' in name or 'PROBLEM' in name:
            return 'Conditions/Problems'
    
    if any(x in name for x in ['ENCOUNTER', 'ADMISSION', 'DISCHARGE', 'TRANSFER', 'BED', 'CENSUS', 'EPISODEOFCARE']):
        return 'Encounters/Visits'
    if name.startswith('ADMITTING') or name.startswith('ADMISSION'):
        return 'Encounters/Visits'
    
    if any(x in name for x in ['DOCUMENT', 'NARRATIVE', 'AMENDMENT', 'COMPOSITION']):
        return 'Documents/Notes'
    
    if any(x in name for x in ['PROCEDURE', 'SURGERY', 'SURGICAL', 'ANESTHESIA', 'PERIOP']):
        return 'Procedures/Surgery'
    if name.startswith('ANESTHESIA'):
        return 'Procedures/Surgery'
    
    if any(x in name for x in ['IMPLANT', 'DEVICE']):
        return 'Devices/Implants'
    
    if any(x in name for x in ['OBSERVATION', 'VITAL', 'SPECIMEN', 'DIAGNOSTIC', 'IMAGINGSTUDY']):
        return 'Observations/Vitals/Labs/Imaging'
    if 'OBSERV' in name:
        return 'Observations/Vitals/Labs/Imaging'
    
    if any(x in name for x in ['MEDICATION', 'DRUG', 'FORMULARY', 'MEDICATIONADMINISTRATION', 'MEDICATIONREQUEST', 'MEDICATIONSTATEMENT', 'MEDICATIONKNOWLEDGE', 'MEDICATIONDISPENSE']):
        return 'Medications'
    
    if any(x in name for x in ['ORDER', 'ORDERABLE', 'CPOE']):
        return 'Orders'
    
    if any(x in name for x in ['PATIENT', 'PERSON', 'HUMANNAME', 'RELATEDPERSON']):
        return 'Patient/Demographics'
    if name in ('CONTACTPOINT', 'CONTACTDETAIL', 'ADDRESS', 'IDENTIFIER'):
        return 'Patient/Demographics'
    
    if any(x in name for x in ['QUESTIONNAIRE', 'QUESTION', 'ITEM']):
        if 'QUESTIONNAIRE' in name or 'QUESTION' in name or name.startswith('ITEM'):
            return 'Questionnaires/Assessments'
    
    if any(x in name for x in ['SCHEDULE', 'APPOINTMENT', 'SLOT', 'AVAILAB']):
        return 'Scheduling'
    
    if any(x in name for x in ['CONSENT', 'DIRECTIVE']):
        return 'Consents/Directives'
    
    if any(x in name for x in ['REFERRAL', 'SERVICEREQUEST']):
        return 'Referrals/Service Requests'
    
    if any(x in name for x in ['COMMUNICATION', 'MESSAGE']):
        return 'Communications'
    
    if any(x in name for x in ['GOAL', 'INTERVENTION']):
        return 'Goals/Interventions'
    
    if any(x in name for x in ['FLAG', 'ALERT']):
        return 'Flags/Alerts'
    
    if any(x in name for x in ['NUTRITION', 'DIET']):
        return 'Nutrition'
    
    if any(x in name for x in ['PAYMENT', 'TRANSACTION']):
        return 'Payments/Transactions'
    
    if name.startswith('HEALTHCARESERVICE'):
        return 'Healthcare Services'
    
    if name.startswith('ORGANIZATION'):
        return 'Organization'
    
    if name.startswith('PRACTITIONER') or name.startswith('PROVIDER'):
        return 'Practitioners'
    
    if name.startswith('LOCATION'):
        return 'Locations'
    
    if name.startswith('LK'):
        # Lookup tables - classify by what they look up
        rest = name[2:]
        if any(x in rest for x in ['ALLERGY', 'ALLERGEN']):
            return 'Allergies/Adverse Events'
        if any(x in rest for x in ['IMMUNIZATION', 'VACCINE']):
            return 'Immunizations'
        if any(x in rest for x in ['MEDICATION', 'DRUG', 'PHARMACY', 'FORMULARY']):
            return 'Medications'
        if any(x in rest for x in ['OBSERVATION', 'VITAL', 'LAB', 'SPECIMEN', 'DIAGNOSTIC']):
            return 'Observations/Vitals/Labs/Imaging'
        if any(x in rest for x in ['CONDITION', 'PROBLEM', 'DIAGNOSIS']):
            return 'Conditions/Problems'
        if any(x in rest for x in ['ENCOUNTER', 'ADMISSION', 'DISCHARGE', 'VISIT', 'BED', 'CENSUS']):
            return 'Encounters/Visits'
        if any(x in rest for x in ['PROCEDURE', 'SURGERY', 'ANESTHESIA']):
            return 'Procedures/Surgery'
        if any(x in rest for x in ['ORDER', 'ORDERABLE', 'CPOE']):
            return 'Orders'
        if any(x in rest for x in ['PATIENT', 'PERSON', 'RACE', 'ETHNICITY', 'LANGUAGE', 'GENDER', 'MARITAL', 'RELIGION', 'VETERAN']):
            return 'Patient/Demographics'
        if any(x in rest for x in ['SCHEDULE', 'APPOINTMENT', 'SLOT']):
            return 'Scheduling'
        if any(x in rest for x in ['BILLING', 'CLAIM', 'CHARGE', 'COVERAGE', 'PAYER', 'ACCOUNT', 'INVOICE', 'INSURANCE']):
            return 'Billing/Revenue Cycle'
        if any(x in rest for x in ['DOCUMENT', 'NOTE', 'NARRATIVE', 'COMPOSITION']):
            return 'Documents/Notes'
        if any(x in rest for x in ['CAREPLAN', 'CARE_PLAN', 'TREATMENT']):
            return 'Care Plans/Treatment Plans'
        if any(x in rest for x in ['QUESTIONNAIRE', 'QUESTION', 'ASSESSMENT', 'FORM']):
            return 'Questionnaires/Assessments'
        if any(x in rest for x in ['CONSENT']):
            return 'Consents/Directives'
        if any(x in rest for x in ['REFERRAL', 'SERVICE']):
            return 'Referrals/Service Requests'
        if any(x in rest for x in ['COMMUNICATION', 'MESSAGE']):
            return 'Communications'
        if any(x in rest for x in ['FLAG', 'ALERT']):
            return 'Flags/Alerts'
        if any(x in rest for x in ['GOAL', 'INTERVENTION']):
            return 'Goals/Interventions'
        if any(x in rest for x in ['NUTRITION', 'DIET']):
            return 'Nutrition'
        if any(x in rest for x in ['DEVICE', 'IMPLANT']):
            return 'Devices/Implants'
        if any(x in rest for x in ['PAYMENT', 'TRANSACTION']):
            return 'Payments/Transactions'
        if any(x in rest for x in ['REG']):
            return 'Registration/Admin'
        if any(x in rest for x in ['ORGANIZATION', 'LOCATION', 'PRACTITIONER', 'PROVIDER']):
            return 'Reference/Configuration'
        if any(x in rest for x in ['STATIC', 'ACTIVE', 'STATUS', 'TYPE', 'CATEGORY', 'UNIT', 'ADDITIVE', 'ADDRESS', 'HOUSING', 'IV']):
            return 'Reference/Configuration'
        return 'Lookup Tables (uncategorized)'
    
    return 'Other/Uncategorized'


# Classify all entities
domain_data = {}
for schema_key in ['jehr', 'rtvx']:
    for entity in inv['schemas'][schema_key]['entities']:
        domain = classify_domain(entity)
        if domain not in domain_data:
            domain_data[domain] = {'tables': 0, 'columns': 0, 'described': 0, 'entities': []}
        
        n_cols = len(entity.get('columns', []))
        n_desc = sum(1 for c in entity.get('columns', []) if c.get('description', '').strip())
        
        domain_data[domain]['tables'] += 1
        domain_data[domain]['columns'] += n_cols
        domain_data[domain]['described'] += n_desc
        domain_data[domain]['entities'].append({
            'name': entity.get('table_name', ''),
            'schema': schema_key,
            'columns': n_cols,
            'described': n_desc,
            'has_table_desc': bool(entity.get('description', '').strip()),
            'fk_count': len(entity.get('foreign_keys', []))
        })

# Print summary sorted by column count
print(f"{'Domain':<45} {'Tables':>7} {'Columns':>8} {'Described':>10}")
print("-" * 75)
total_t = 0
total_c = 0
total_d = 0
for domain in sorted(domain_data.keys(), key=lambda d: domain_data[d]['columns'], reverse=True):
    d = domain_data[domain]
    total_t += d['tables']
    total_c += d['columns']
    total_d += d['described']
    print(f"{domain:<45} {d['tables']:>7} {d['columns']:>8} {d['described']:>10}")
print("-" * 75)
print(f"{'TOTAL':<45} {total_t:>7} {total_c:>8} {total_d:>10}")

# Save domain summary
domain_summary = {}
for domain, d in sorted(domain_data.items(), key=lambda x: x[1]['columns'], reverse=True):
    entities_summary = sorted(d['entities'], key=lambda e: e['columns'], reverse=True)
    domain_summary[domain] = {
        'tables': d['tables'],
        'columns': d['columns'],
        'columns_with_descriptions': d['described'],
        'top_entities': entities_summary[:10],
        'all_entity_names': [e['name'] for e in entities_summary]
    }

with open('domain_analysis.json', 'w') as f:
    json.dump(domain_summary, f, indent=2)

print("\nSaved to domain_analysis.json")

# Show top 20 largest tables
print("\n\n=== Top 20 Largest Tables ===")
all_entities = []
for schema_key in ['jehr', 'rtvx']:
    for entity in inv['schemas'][schema_key]['entities']:
        all_entities.append({
            'name': entity.get('table_name', ''),
            'schema': schema_key,
            'columns': len(entity.get('columns', [])),
            'domain': classify_domain(entity),
            'desc_snippet': entity.get('description', '')[:80]
        })

for e in sorted(all_entities, key=lambda x: x['columns'], reverse=True)[:20]:
    print(f"  {e['name']:<50} {e['columns']:>4} cols  [{e['domain']}]")
    print(f"    {e['desc_snippet']}")
