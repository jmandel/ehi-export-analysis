#!/usr/bin/env python3
"""Parse the extracted text from Data_Export.pdf to enumerate all CSV entities and fields."""

import json
import re
import sys

def parse_data_dictionary(text_file):
    with open(text_file, 'r') as f:
        lines = f.readlines()

    entities = {}
    current_entity = None
    in_header = False
    
    for line in lines:
        stripped = line.strip()
        
        # Detect CSV file headers (e.g., "AllergyIntolerance.csv")
        csv_match = re.match(r'^(\w+(?:\s+\w+)?)\.csv$', stripped)
        if csv_match:
            current_entity = csv_match.group(1)
            entities[current_entity] = []
            in_header = True
            continue
        
        # Skip the "Data  Notes" header line
        if in_header and re.match(r'^\s*Data\s+Notes\s*$', stripped):
            in_header = False
            continue
        
        # Skip empty lines
        if not stripped:
            continue
        
        # If we're in an entity, parse field lines
        if current_entity:
            # Field lines have at least one field name, possibly followed by description
            # They're typically formatted as "FieldName    Description text"
            field_match = re.match(r'^\s*(\w+)\s{2,}(.+)$', line.rstrip())
            if field_match:
                field_name = field_match.group(1)
                description = field_match.group(2).strip()
                entities[current_entity].append({
                    'name': field_name,
                    'description': description
                })
            elif re.match(r'^\s*(\w+)\s*$', stripped) and stripped not in ['Data', 'Notes']:
                # Field name with no description (unlikely but handle it)
                # But check it's not a new entity header
                if not stripped.endswith('.csv'):
                    # Could be a continuation or a standalone field
                    # Check if next would be a CSV - skip for now
                    pass
    
    return entities

def categorize_entity(name):
    """Categorize entities into domains based on their names."""
    clinical = ['AllergyIntolerance', 'CarePlan', 'ClinicalImpression', 'Condition',
                'ConditionChiefComplaint', 'ConditionConcern', 'ConditionFunctionalCognitive',
                'CommunicationEducation', 'Goal', 'Images', 'Immunizations',
                'MedicationRequest', 'Procedure', 'ProcedureDilation',
                'ProcedureDilationRemarks', 'ProcedureIOPs', 'ProcedureIOPsTargets',
                'ProcedureOther', 'ProcedureScreening', 'ServiceRequest', 'Task',
                'Device', 'DocumentReference']
    
    observations = ['ObservationBinocularVision', 'ObservationKeratometry',
                    'ObservationLabResults', 'ObservationLifeStyle', 'ObservationPFSH',
                    'ObservationPhysicalExam', 'ObservationReviewOfSystem', 'ObservationVitals']
    
    optometry = ['Prescription', 'PrescriptionAddOn',
                 'RefractionAutorefraction', 'RefractionContactLensRx',
                 'RefractionCyclopegic', 'RefractionManifest', 'RefractionRetinoscopy',
                 'RefractionSpectacleRx', 'RefractionSpectacleRxAddOns', 'RefractionWavefront',
                 'RxOrder']
    
    demographics = ['Patient', 'PatientAccount', 'PatientAddress', 'PatientAlert',
                    'PatientDocumentReference', 'PatientEmail', 'PatientLinkedAccount',
                    'PatientLocation', 'PatientNote', 'PatientPaymentCard',
                    'PatientPhoneNumber', 'PatientPreference', 'Contact',
                    'ContactLinkedAccount', 'Questionnaire']
    
    billing = ['Claim', 'ClaimDiagnosis', 'ClaimLine', 'ClaimLineCodes', 'ClaimNote',
               'ClaimStatus', 'Invoice', 'InvoiceLine', 'InvoiceLineAdjustment',
               'InvoiceLineDiagnosis', 'Payment', 'PaymentItem']
    
    insurance = ['Benefit', 'BenefitCoverageElectronic', 'BenefitCoverageManual',
                 'Policy', 'PolicyNote']
    
    scheduling = ['Appointment', 'Encounter', 'EncounterProceduresDiagnosis', 'Recall']
    
    reference = ['Locations', 'Provider', 'Product']
    
    if name in clinical:
        return 'Clinical'
    elif name in observations:
        return 'Observations'
    elif name in optometry:
        return 'Optometry-Specific'
    elif name in demographics:
        return 'Patient Demographics & Administration'
    elif name in billing:
        return 'Billing & Financial'
    elif name in insurance:
        return 'Insurance & Benefits'
    elif name in scheduling:
        return 'Scheduling & Encounters'
    elif name in reference:
        return 'Reference / Administrative'
    else:
        return 'Uncategorized'

def main():
    text_file = '/home/jmandel/hobby/ehi-export-analysis/abstraction/visionweb--uprise/analysis/data_export.txt'
    entities = parse_data_dictionary(text_file)
    
    # Build full inventory
    inventory = []
    for entity_name, fields in entities.items():
        category = categorize_entity(entity_name)
        described = sum(1 for f in fields if f['description'] and f['description'].lower() not in ['', 'notes'])
        inventory.append({
            'entity': entity_name,
            'csv_file': f'{entity_name}.csv',
            'category': category,
            'field_count': len(fields),
            'fields_with_descriptions': described,
            'fields': fields
        })
    
    # Save full inventory
    output_path = '/home/jmandel/hobby/ehi-export-analysis/abstraction/visionweb--uprise/analysis/full-entity-inventory.json'
    with open(output_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    total_entities = len(inventory)
    total_fields = sum(e['field_count'] for e in inventory)
    total_described = sum(e['fields_with_descriptions'] for e in inventory)
    
    print(f"=== DATA DICTIONARY SUMMARY ===")
    print(f"Total entities (CSV files): {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({100*total_described/total_fields:.1f}%)")
    print()
    
    # Category breakdown
    categories = {}
    for e in inventory:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entities': 0, 'fields': 0, 'described': 0}
        categories[cat]['entities'] += 1
        categories[cat]['fields'] += e['field_count']
        categories[cat]['described'] += e['fields_with_descriptions']
    
    print(f"=== CATEGORY BREAKDOWN ===")
    print(f"{'Category':<40} {'Entities':>10} {'Fields':>10} {'Described':>10}")
    print("-" * 70)
    for cat, stats in sorted(categories.items()):
        print(f"{cat:<40} {stats['entities']:>10} {stats['fields']:>10} {stats['described']:>10}")
    print()
    
    # Entity detail table
    print(f"=== ENTITY DETAILS ===")
    print(f"{'Entity':<40} {'Fields':>8} {'Described':>10} {'Category'}")
    print("-" * 90)
    for e in sorted(inventory, key=lambda x: (x['category'], x['entity'])):
        print(f"{e['entity']:<40} {e['field_count']:>8} {e['fields_with_descriptions']:>10}   {e['category']}")
    
    # Identify largest entities
    print()
    print(f"=== TOP 15 LARGEST ENTITIES ===")
    for e in sorted(inventory, key=lambda x: -x['field_count'])[:15]:
        print(f"  {e['entity']:<40} {e['field_count']:>4} fields  ({e['category']})")
    
    # Check for any entities with 0 descriptions
    print()
    print(f"=== ENTITIES WITH NO FIELD DESCRIPTIONS ===")
    zero_desc = [e for e in inventory if e['fields_with_descriptions'] == 0]
    if zero_desc:
        for e in zero_desc:
            print(f"  {e['entity']}: {e['field_count']} fields, 0 descriptions")
    else:
        print("  None — all entities have field descriptions")

if __name__ == '__main__':
    main()
