"""
Build entity inventory from the FHIR API documentation.
Since the B10 export claims FHIR US Core 3.1.1 as format, the "entities"
are the FHIR resource types documented in the FHIR API doc.
There is NO vendor-specific data dictionary.
"""
import re
import json

with open('../downloads/FHIRMedicsDocAssistant.htm', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Resource types found in JSON examples (the actual resources the API serves)
resourcetype_pattern = re.compile(r'"resourceType"\s*:\s*"(\w+)"')
example_resources = resourcetype_pattern.findall(content)
unique_examples = sorted(set(example_resources))

# These are the US Core resource types with examples in the doc
# (excluding Bundle which is a container, not a clinical resource)
us_core_resources = [r for r in unique_examples if r != 'Bundle']

# Map resources to USCDI categories
uscdi_mapping = {
    'Patient': {'category': 'Demographics', 'uscdi_class': 'Patient Demographics'},
    'AllergyIntolerance': {'category': 'Clinical', 'uscdi_class': 'Allergies & Intolerances'},
    'CarePlan': {'category': 'Clinical', 'uscdi_class': 'Assessment & Plan of Treatment'},
    'CareTeam': {'category': 'Clinical', 'uscdi_class': 'Care Team Members'},
    'Condition': {'category': 'Clinical', 'uscdi_class': 'Problems'},
    'Device': {'category': 'Clinical', 'uscdi_class': 'Medical Devices'},
    'DiagnosticReport': {'category': 'Clinical', 'uscdi_class': 'Clinical Tests / Diagnostic Imaging'},
    'DocumentReference': {'category': 'Clinical', 'uscdi_class': 'Clinical Notes'},
    'Encounter': {'category': 'Clinical', 'uscdi_class': 'Encounters'},
    'Goal': {'category': 'Clinical', 'uscdi_class': 'Goals & Preferences'},
    'Immunization': {'category': 'Clinical', 'uscdi_class': 'Immunizations'},
    'MedicationRequest': {'category': 'Clinical', 'uscdi_class': 'Medications'},
    'Observation': {'category': 'Clinical', 'uscdi_class': 'Vitals / Labs / Clinical Tests'},
    'Organization': {'category': 'Administrative', 'uscdi_class': 'Facility Information'},
    'Practitioner': {'category': 'Administrative', 'uscdi_class': 'Care Team Members'},
    'Procedure': {'category': 'Clinical', 'uscdi_class': 'Procedures'},
    'Provenance': {'category': 'Administrative', 'uscdi_class': 'Provenance'},
}

# Build entity inventory
entities = []
for resource in us_core_resources:
    mapping = uscdi_mapping.get(resource, {'category': 'Other', 'uscdi_class': 'Unknown'})
    entities.append({
        'entity_name': resource,
        'resource_type': resource,
        'category': mapping['category'],
        'uscdi_class': mapping['uscdi_class'],
        'fields': 'N/A - no vendor-specific field documentation',
        'field_count': None,
        'descriptions': 'N/A',
        'source': 'FHIR US Core 3.1.1 standard (no vendor-specific mapping)',
        'example_in_doc': True,
        'notes': 'Only standard US Core elements documented; no vendor extensions or custom fields'
    })

inventory = {
    'product': 'MedicsDocAssistant',
    'version': '8.0',
    'vendor': 'Advanced Data Systems Corporation',
    'export_format': 'HL7 FHIR US Core 3.1.1 / HL7 C-CDA',
    'data_dictionary_available': False,
    'vendor_specific_documentation': False,
    'total_resource_types': len(entities),
    'total_fields': None,
    'fields_with_descriptions': None,
    'notes': [
        'The B10 documentation page contains a single paragraph stating exports are in C-CDA and FHIR US Core 3.1.1 format.',
        'The only links are to external HL7 standards (C-CDA IG and US Core 3.1.1 IG).',
        'No vendor-specific data dictionary, schema, field mapping, or sample export data is provided.',
        'The FHIR API documentation (g(10)) shows 17 US Core resource types with sample JSON responses.',
        'Zero billing/financial FHIR resources (Coverage, Claim, ExplanationOfBenefit, etc.) are documented.',
        'No vendor FHIR extensions are documented beyond standard US Core profiles.',
    ],
    'entities': entities
}

with open('entity-inventory-full.json', 'w') as f:
    json.dump(inventory, f, indent=2)

# Summary
summary = {
    'product': inventory['product'],
    'version': inventory['version'],
    'vendor': inventory['vendor'],
    'export_format': inventory['export_format'],
    'data_dictionary_available': False,
    'total_resource_types': len(entities),
    'total_fields': 'N/A',
    'fields_with_descriptions': 'N/A',
    'categories': {
        'Clinical': len([e for e in entities if e['category'] == 'Clinical']),
        'Demographics': len([e for e in entities if e['category'] == 'Demographics']),
        'Administrative': len([e for e in entities if e['category'] == 'Administrative']),
    },
    'resource_list': [e['entity_name'] for e in entities],
    'billing_resources_present': False,
    'vendor_extensions_present': False,
    'sample_data_provided': False,
}

with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
print(f"\nSaved entity-inventory-full.json and entity-inventory-summary.json")
