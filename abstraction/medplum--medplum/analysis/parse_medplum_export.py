#!/usr/bin/env python3
"""
Parse Medplum's EHI export artifacts and produce a full entity inventory.

Reads:
  - enrichment/resources.json (extracted from OpenAPI spec + CapabilityStatement)
  - enrichment/coverage.json (extraction stats)
  - patienteverything.ts (source code for $patient-everything)

Produces:
  - full-entity-inventory.json: Complete resource/field catalog
  - summary-stats.json: Aggregate statistics
"""

import json
import os

RESULTS_DIR = '/home/jmandel/hobby/ehi-export-analysis/results/medplum--medplum/downloads'
OUTPUT_DIR = os.path.dirname(__file__)

def load_json(path):
    with open(path) as f:
        return json.load(f)

def categorize_resource(resource_type):
    """Categorize FHIR resource types into EHI-relevant domains."""
    categories = {
        'Demographics': ['Patient', 'Person', 'RelatedPerson'],
        'Encounters / Visits': ['Encounter', 'EpisodeOfCare'],
        'Problems / Conditions': ['Condition', 'ClinicalImpression'],
        'Medications': ['MedicationRequest', 'MedicationAdministration', 'MedicationDispense',
                        'MedicationStatement', 'Medication', 'MedicationKnowledge'],
        'Allergies': ['AllergyIntolerance'],
        'Immunizations': ['Immunization', 'ImmunizationEvaluation', 'ImmunizationRecommendation'],
        'Vitals / Observations': ['Observation'],
        'Lab Results / Diagnostics': ['DiagnosticReport', 'Specimen', 'MolecularSequence'],
        'Imaging': ['ImagingStudy', 'Media'],
        'Procedures': ['Procedure', 'ServiceRequest'],
        'Clinical Notes / Documents': ['Composition', 'DocumentReference', 'DocumentManifest', 'Binary'],
        'Care Plans / Goals': ['CarePlan', 'CareTeam', 'Goal', 'NutritionOrder'],
        'Orders / Referrals': ['DeviceRequest', 'SupplyRequest', 'SupplyDelivery', 'RequestGroup',
                                'GuidanceResponse', 'Task'],
        'Insurance / Coverage': ['Coverage', 'CoverageEligibilityRequest', 'CoverageEligibilityResponse',
                                  'EnrollmentRequest', 'Contract'],
        'Claims / Billing': ['Claim', 'ClaimResponse', 'ExplanationOfBenefit', 'ChargeItem',
                             'Account', 'Invoice', 'PaymentNotice', 'PaymentReconciliation'],
        'Consents / Directives': ['Consent'],
        'Patient Communications': ['Communication', 'CommunicationRequest'],
        'Scheduling': ['Appointment', 'AppointmentResponse', 'Schedule', 'Slot'],
        'Devices': ['Device', 'DeviceDefinition', 'DeviceMetric', 'DeviceUseStatement'],
        'Family History': ['FamilyMemberHistory'],
        'Risk / Safety': ['AdverseEvent', 'DetectedIssue', 'Flag', 'RiskAssessment'],
        'Body Structure': ['BodyStructure'],
        'Research': ['ResearchStudy', 'ResearchSubject'],
        'Questionnaires / Assessments': ['Questionnaire', 'QuestionnaireResponse'],
        'Lists / Groups': ['List', 'Group'],
        'Provenance / Audit': ['Provenance', 'AuditEvent'],
        'Measures / Quality': ['Measure', 'MeasureReport'],
        'Provider Directory': ['Practitioner', 'PractitionerRole', 'Organization',
                                'OrganizationAffiliation', 'Location', 'HealthcareService', 'Endpoint'],
        'Medplum Custom': [],  # Will be populated dynamically
    }

    # Known Medplum custom types
    medplum_custom = ['AccessPolicy', 'Agent', 'AsyncJob', 'Bot', 'BulkDataExport',
                      'ClientApplication', 'DomainConfiguration', 'IdentityProvider',
                      'JsonWebKey', 'Login', 'PasswordChangeRequest', 'Project',
                      'ProjectMembership', 'SmartAppLaunch', 'User', 'UserConfiguration',
                      'UserSecurityRequest']

    # Definition / infrastructure types not typically patient data
    infrastructure = ['Bundle', 'CapabilityStatement', 'CodeSystem', 'CompartmentDefinition',
                      'ConceptMap', 'EventDefinition', 'Evidence', 'EvidenceVariable',
                      'ExampleScenario', 'GraphDefinition', 'ImplementationGuide',
                      'Library', 'Linkage', 'MessageDefinition', 'MessageHeader',
                      'NamingSystem', 'OperationDefinition', 'OperationOutcome',
                      'Parameters', 'PlanDefinition', 'ActivityDefinition',
                      'SearchParameter', 'StructureDefinition', 'StructureMap',
                      'Subscription', 'TerminologyCapabilities', 'TestReport',
                      'TestScript', 'ValueSet', 'VerificationResult',
                      'CatalogEntry', 'ChargeItemDefinition',
                      'EffectEvidenceSynthesis', 'RiskEvidenceSynthesis',
                      'InsurancePlan', 'ObservationDefinition', 'SpecimenDefinition',
                      'BiologicallyDerivedProduct', 'Substance', 'SubstanceNucleicAcid',
                      'SubstancePolymer', 'SubstanceProtein', 'SubstanceReferenceInformation',
                      'SubstanceSourceMaterial', 'SubstanceSpecification',
                      'MedicinalProduct', 'MedicinalProductAuthorization',
                      'MedicinalProductContraindication', 'MedicinalProductIndication',
                      'MedicinalProductIngredient', 'MedicinalProductInteraction',
                      'MedicinalProductManufactured', 'MedicinalProductPackaged',
                      'MedicinalProductPharmaceutical', 'MedicinalProductUndesirableEffect',
                      'ResearchDefinition', 'ResearchElementDefinition']

    for cat, types in categories.items():
        if resource_type in types:
            return cat

    if resource_type in medplum_custom:
        return 'Medplum Custom (Platform)'

    if resource_type in infrastructure:
        return 'Infrastructure / Definitions'

    return 'Other'


def main():
    resources = load_json(os.path.join(RESULTS_DIR, 'enrichment', 'resources.json'))
    coverage = load_json(os.path.join(RESULTS_DIR, 'enrichment', 'coverage.json'))

    # Build full entity inventory
    inventory = []
    for r in resources:
        entry = {
            'resourceType': r['resourceType'],
            'description': r.get('description', ''),
            'category': categorize_resource(r['resourceType']),
            'inPatientCompartment': r.get('inPatientCompartment', False),
            'patientCompartmentParams': r.get('patientCompartmentParams', []),
            'fieldCount': len(r.get('fields', [])),
            'fieldsWithDescriptions': sum(1 for f in r.get('fields', []) if f.get('description')),
            'fieldsWithTypes': sum(1 for f in r.get('fields', []) if f.get('type')),
            'searchParamCount': len(r.get('searchParams', [])),
            'interactions': r.get('interactions', []),
            'sourceUrl': r.get('sourceUrl', ''),
            'fields': []
        }
        for f in r.get('fields', []):
            field_entry = {
                'name': f['name'],
                'type': f.get('type', ''),
                'description': f.get('description', ''),
                'isArray': f.get('isArray', False),
                'required': f.get('required', False),
            }
            entry['fields'].append(field_entry)
        inventory.append(entry)

    # Sort: patient compartment resources first, then by category
    inventory.sort(key=lambda x: (not x['inPatientCompartment'], x['category'], x['resourceType']))

    # Save full inventory
    with open(os.path.join(OUTPUT_DIR, 'full-entity-inventory.json'), 'w') as f:
        json.dump(inventory, f, indent=2)

    # Compute summary stats
    total_resources = len(inventory)
    compartment_resources = [r for r in inventory if r['inPatientCompartment']]
    total_fields = sum(r['fieldCount'] for r in inventory)
    compartment_fields = sum(r['fieldCount'] for r in compartment_resources)
    fields_with_desc = sum(r['fieldsWithDescriptions'] for r in inventory)
    fields_with_types = sum(r['fieldsWithTypes'] for r in inventory)

    # Category breakdown
    categories = {}
    for r in inventory:
        cat = r['category']
        if cat not in categories:
            categories[cat] = {'resources': 0, 'fields': 0, 'inCompartment': 0}
        categories[cat]['resources'] += 1
        categories[cat]['fields'] += r['fieldCount']
        if r['inPatientCompartment']:
            categories[cat]['inCompartment'] += 1

    # Resources resolved via references (not in compartment but included)
    resolved_types = ['Organization', 'Practitioner', 'PractitionerRole', 'Location', 'Medication', 'Device']
    resolved = [r for r in inventory if r['resourceType'] in resolved_types]

    # Summary
    summary = {
        'totalResources': total_resources,
        'resourcesInPatientCompartment': len(compartment_resources),
        'resourcesResolvedViaReferences': len(resolved),
        'totalExportableResources': len(compartment_resources) + len(resolved),
        'totalFields': total_fields,
        'fieldsInCompartmentResources': compartment_fields,
        'fieldsWithDescriptions': fields_with_desc,
        'fieldsWithTypes': fields_with_types,
        'descriptionCoverage': f'{100 * fields_with_desc / total_fields:.1f}%',
        'typeCoverage': f'{100 * fields_with_types / total_fields:.1f}%',
        'categoryBreakdown': dict(sorted(categories.items())),
        'compartmentResourceList': [r['resourceType'] for r in compartment_resources],
        'resolvedReferenceTypes': resolved_types,
        'medplumCustomTypes': [r['resourceType'] for r in inventory if r['category'] == 'Medplum Custom (Platform)'],
        'serverVersion': coverage['source_files']['capability_statement']['server_version'],
        'fhirVersion': coverage['source_files']['capability_statement']['fhir_version'],
        'openApiSchemaCount': coverage['source_files']['openapi_spec']['total_schemas'],
        'top20ByFieldCount': sorted(
            [{'resourceType': r['resourceType'], 'fields': r['fieldCount'],
              'inCompartment': r['inPatientCompartment'], 'category': r['category']}
             for r in inventory],
            key=lambda x: -x['fields']
        )[:20],
    }

    with open(os.path.join(OUTPUT_DIR, 'summary-stats.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Total resource types: {total_resources}")
    print(f"In Patient Compartment: {len(compartment_resources)}")
    print(f"Resolved via references: {len(resolved)}")
    print(f"Total exportable: {len(compartment_resources) + len(resolved)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({100*fields_with_desc/total_fields:.1f}%)")
    print(f"Fields with types: {fields_with_types} ({100*fields_with_types/total_fields:.1f}%)")
    print()
    print("Category breakdown:")
    for cat, info in sorted(categories.items()):
        print(f"  {cat}: {info['resources']} resources, {info['fields']} fields, {info['inCompartment']} in compartment")
    print()
    print("Top 20 resources by field count:")
    for item in summary['top20ByFieldCount']:
        comp = '✓' if item['inCompartment'] else ' '
        print(f"  [{comp}] {item['resourceType']}: {item['fields']} fields ({item['category']})")


if __name__ == '__main__':
    main()
