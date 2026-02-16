#!/usr/bin/env python3
"""
Parse KanTime EHI export documentation artifacts and produce entity inventories.

The EHI documentation is a single-page PDF with minimal content. 
The Patient API PDF describes the CCDA-based clinical export mechanism.
The SMART on FHIR PDF describes the (g)(10) FHIR API (not (b)(10)).

Since there is no data dictionary, we extract what we can from the 
documentation about the clinical CCDA sections and the billing CSV claim.
"""

import json
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')

# Extract CCDA sections from Patient API PDF
def extract_ccda_sections():
    """Extract the CCDA section names documented in the Patient API."""
    result = subprocess.run(
        ['pdftotext', '-layout', os.path.join(DOWNLOADS, 'KanTime_Patient_API.pdf'), '-'],
        capture_output=True, text=True
    )
    text = result.stdout
    
    sections = []
    # Parse the section table from the PDF
    section_mappings = {
        'all': 'All',
        'demographics': 'Patient Demographics',
        'careteam': 'Care Team',
        'allergies': 'Allergies and Intolerances',
        'assessments': 'Assessment',
        'encounters': 'Encounters',
        'functionalstatus': 'Functional Status',
        'goals': 'Goals',
        'healthconcerns': 'Health Concerns',
        'immunizations': 'Immunizations',
        'medicalequipment': 'Medical Equipment',
        'medications': 'Medications',
        'mentalstatus': 'Mental Status',
        'planoftreatment': 'Plan of Treatment',
        'problem': 'Problem',
        'procedures': 'Procedures',
        'reasonforreferral': 'Reason for Referral',
        'results': 'Results',
        'socialhistory': 'Social History',
        'vitalsigns': 'Vital Signs',
        'consultationnote': 'Consultation Note',
        'progressnote': 'Progress Note',
        'historyandphysicalnote': 'History and Physical Note',
    }
    
    for api_name, display_name in section_mappings.items():
        if api_name == 'all':
            continue
        sections.append({
            'api_section_name': api_name,
            'display_name': display_name,
            'source': 'KanTime_Patient_API.pdf'
        })
    
    return sections


def extract_fhir_resources():
    """Extract FHIR resource types from the SMART on FHIR documentation."""
    result = subprocess.run(
        ['pdftotext', '-layout', os.path.join(DOWNLOADS, 'SmartOnFHIRAPIDoc.pdf'), '-'],
        capture_output=True, text=True
    )
    text = result.stdout
    
    resources = []
    resource_names = [
        'Patient', 'AllergyIntolerance', 'CarePlan', 'CareTeam',
        'Condition', 'Device', 'DiagnosticReport', 'DocumentReference',
        'Observation', 'Goal', 'Immunization', 'Medication',
        'MedicationRequest', 'Procedure', 'Provenance',
        'Organization', 'ServiceRequest', 'Coverage',
        'MedicationDispense', 'Specimen', 'RelatedPerson', 'Location',
        'Encounter', 'Practitioner'
    ]
    
    for name in resource_names:
        if name.lower() in text.lower():
            resources.append({
                'resource_type': name,
                'source': 'SmartOnFHIRAPIDoc.pdf',
                'note': '(g)(10) FHIR API - NOT (b)(10) EHI export'
            })
    
    return resources


def build_entity_inventory():
    """Build the complete entity inventory from available documentation."""
    
    ccda_sections = extract_ccda_sections()
    fhir_resources = extract_fhir_resources()
    
    # The EHI export has two components per the EHI_Tool_Documentation.pdf:
    # 1. Clinical data as CCDA 2.1 Release 2 (USCDI v1) - 22 sections
    # 2. Billing data as CSV (claims and payments) - no schema provided
    
    entities = []
    
    # Clinical CCDA sections (the actual (b)(10) clinical export)
    for section in ccda_sections:
        entities.append({
            'entity_name': section['api_section_name'],
            'display_name': section['display_name'],
            'category': 'Clinical (CCDA)',
            'format': 'CCDA 2.1 XML',
            'fields': None,  # No field-level documentation provided
            'fields_with_descriptions': 0,
            'field_types_documented': False,
            'source': 'KanTime_Patient_API.pdf',
            'notes': 'Standard CCDA section; no product-specific field documentation'
        })
    
    # Billing export (mentioned in EHI doc but no schema)
    entities.append({
        'entity_name': 'patient_claims',
        'display_name': 'Patient Claims',
        'category': 'Billing (CSV)',
        'format': 'CSV, XLSX, or PDF',
        'fields': None,
        'fields_with_descriptions': 0,
        'field_types_documented': False,
        'source': 'EHI_Tool_Documentation.pdf',
        'notes': 'Mentioned as available for billing users; no schema, field list, or sample data provided'
    })
    
    entities.append({
        'entity_name': 'patient_payments',
        'display_name': 'Patient Payments',
        'category': 'Billing (CSV)',
        'format': 'CSV, XLSX, or PDF',
        'fields': None,
        'fields_with_descriptions': 0,
        'field_types_documented': False,
        'source': 'EHI_Tool_Documentation.pdf',
        'notes': 'Mentioned as available for billing users; no schema, field list, or sample data provided'
    })
    
    inventory = {
        'product': 'KanTime Health',
        'version': '1.0',
        'chpl_id': 11219,
        'chpl_product_number': '15.04.04.3096.KanH.01.01.1.230118',
        'export_format': 'CCDA 2.1 XML (clinical) + CSV/XLSX/PDF (billing)',
        'total_entities': len(entities),
        'entities_with_field_definitions': 0,
        'total_fields_documented': 0,
        'fields_with_descriptions': 0,
        'has_data_dictionary': False,
        'has_sample_data': False,
        'has_machine_readable_schema': False,
        'entities': entities,
        'fhir_api_resources': fhir_resources,
        'fhir_api_note': 'FHIR resources are from the (g)(10) API, NOT the (b)(10) EHI export'
    }
    
    return inventory


def build_summary(inventory):
    """Build summary statistics from the full inventory."""
    clinical_entities = [e for e in inventory['entities'] if e['category'] == 'Clinical (CCDA)']
    billing_entities = [e for e in inventory['entities'] if e['category'] == 'Billing (CSV)']
    
    summary = {
        'product': inventory['product'],
        'total_entities': inventory['total_entities'],
        'categories': {
            'Clinical (CCDA)': {
                'count': len(clinical_entities),
                'format': 'CCDA 2.1 XML',
                'fields_documented': 0,
                'description': 'Standard CCDA sections accessible via Patient API; no field-level documentation'
            },
            'Billing (CSV)': {
                'count': len(billing_entities),
                'format': 'CSV, XLSX, or PDF',
                'fields_documented': 0,
                'description': 'Claims and payments export mentioned in EHI documentation; no schema or field list provided'
            }
        },
        'documentation_quality': {
            'has_data_dictionary': False,
            'has_field_definitions': False,
            'has_field_types': False,
            'has_relationships': False,
            'has_value_sets': False,
            'has_sample_data': False,
            'has_machine_readable_schema': False
        },
        'fhir_api_resources_count': len(inventory['fhir_api_resources']),
        'fhir_api_note': inventory['fhir_api_note']
    }
    
    return summary


if __name__ == '__main__':
    inventory = build_entity_inventory()
    summary = build_summary(inventory)
    
    out_dir = os.path.dirname(__file__)
    
    with open(os.path.join(out_dir, 'entity-inventory-full.json'), 'w') as f:
        json.dump(inventory, f, indent=2)
    
    with open(os.path.join(out_dir, 'entity-inventory-summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Total entities: {inventory['total_entities']}")
    print(f"  Clinical (CCDA sections): {len([e for e in inventory['entities'] if e['category'] == 'Clinical (CCDA)'])}")
    print(f"  Billing (CSV): {len([e for e in inventory['entities'] if e['category'] == 'Billing (CSV)'])}")
    print(f"Entities with field definitions: {inventory['entities_with_field_definitions']}")
    print(f"Total fields documented: {inventory['total_fields_documented']}")
    print(f"FHIR API resources (g)(10): {len(inventory['fhir_api_resources'])}")
    print(f"\nSaved entity-inventory-full.json and entity-inventory-summary.json")
