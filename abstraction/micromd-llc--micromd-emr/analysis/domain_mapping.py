"""Map MicroMD XML files to EHI data domains and produce coverage summary."""
import json

# Load inventory
with open('full-entity-inventory.json', 'r') as f:
    inv = json.load(f)

# Domain mapping: XML file -> EHI domains covered
domain_mapping = {
    'Billing.xml': {
        'domains': ['Claims / billing'],
        'elements': 7,
        'attributes': 68,
        'notes': 'Superbills with CPT codes, diagnoses, procedures, modifiers, referring physicians, insurance per transaction'
    },
    'Encounters.xml': {
        'domains': ['Encounters / visits', 'Problems / conditions / diagnoses', 'Medications / prescriptions', 'Orders / referrals', 'Clinical notes / documents', 'Procedures'],
        'elements': 21,
        'attributes': 285,
        'notes': 'SOAP documentation, assessments (ICD/SNOMED), medications (NDC/RxNorm), plans, orders, notes (text + audio), face time'
    },
    'HealthScreening.xml': {
        'domains': ['Immunizations', 'Care plans / goals'],
        'elements': 22,
        'attributes': 374,
        'notes': 'Goal monitoring, health concerns, screenings (LOINC-coded), immunizations (CVX/NDC), risk factors, prevention programs'
    },
    'Histories.xml': {
        'domains': ['Problems / conditions / diagnoses', 'Consents / directives'],
        'elements': 13,
        'attributes': 336,
        'notes': 'Family/medical/social/surgical history, birth history, sexual history, asthma, habits, hospitalizations, consent history'
    },
    'MedicalInfo.xml': {
        'domains': ['Allergies', 'Problems / conditions / diagnoses', 'Vitals', 'Lab results', 'Medications / prescriptions', 'Procedures', 'Care plans / goals'],
        'elements': 29,
        'attributes': 521,
        'notes': 'Allergies, problems (ICD-10/SNOMED + cancer staging), vitals, medications (comprehensive), test results (LOINC), behavioral health, CDS alerts, ultrasound, operations, treatment plans'
    },
    'Miscellaneous.xml': {
        'domains': ['Clinical notes / documents', 'Consents / directives', 'Orders / referrals'],
        'elements': 7,
        'attributes': 141,
        'notes': 'Attachments, letters, advance directives, patient education, referrals in, transitions of care'
    },
    'Orders.xml': {
        'domains': ['Orders / referrals'],
        'elements': 1,
        'attributes': 23,
        'notes': 'Orders with category, priority, sender/receiver, status, work-to-do items'
    },
    'Patient.xml': {
        'domains': ['Demographics', 'Insurance / coverage'],
        'elements': 10,
        'attributes': 312,
        'notes': 'Demographics (incl. SOGI, race/ethnicity), addresses, family members, contacts, insurance policies (detailed), providers, consent records'
    },
    'Schedule.xml': {
        'domains': ['Encounters / visits'],
        'elements': 1,
        'attributes': 15,
        'notes': 'Appointment records with status, provider, times, department, specialty'
    },
    'Specialty.xml': {
        'domains': ['Specialty-specific'],
        'elements': 18,
        'attributes': 287,
        'notes': 'Vision (ophthalmic tests), hearing (audiometric), diabetes (insulin/pump), pediatric developmental, genetic screenings, geriatric assessments, allergy testing'
    },
    'WomenHealth.xml': {
        'domains': ['Specialty-specific'],
        'elements': 21,
        'attributes': 634,
        'notes': 'OB care episodes, initial exams, OB medical history (163 fields!), genetics, deliveries, prenatal visits, EDD calculations, labor progress, pregnancy history, gynecology, menstrual history, family planning'
    }
}

# Print domain summary
print("=" * 80)
print("Domain Coverage Summary")
print("=" * 80)

# Collect all domains
all_domains = set()
for info in domain_mapping.values():
    all_domains.update(info['domains'])

print(f"\nDomains covered: {len(all_domains)}")
for d in sorted(all_domains):
    sources = [f for f, info in domain_mapping.items() if d in info['domains']]
    print(f"  {d}: {', '.join(sources)}")

print("\n" + "=" * 80)
print("File-by-Domain Matrix")
print("=" * 80)
for fname, info in domain_mapping.items():
    print(f"\n{fname} ({info['elements']} elements, {info['attributes']} attributes)")
    print(f"  Domains: {', '.join(info['domains'])}")
    print(f"  Notes: {info['notes']}")

# Save
with open('domain-mapping.json', 'w') as f:
    json.dump(domain_mapping, f, indent=2)

print(f"\nSaved to domain-mapping.json")
