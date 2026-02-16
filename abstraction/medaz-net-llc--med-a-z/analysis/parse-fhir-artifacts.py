#!/usr/bin/env python3
"""
Parse all FHIR artifacts from Med A-Z downloads and produce:
- entity-inventory-full.json: complete resource/field inventory
- entity-inventory-summary.json: summary statistics
"""

import json
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')
ANALYSIS = os.path.dirname(__file__)


def parse_capability_statement(path):
    """Extract resource types, profiles, and supported interactions."""
    with open(path) as f:
        cs = json.load(f)
    
    resources = []
    for rest in cs.get('rest', []):
        for r in rest.get('resource', []):
            rtype = r.get('type')
            interactions = [i['code'] for i in r.get('interaction', [])]
            search_params = [sp['name'] for sp in r.get('searchParam', [])]
            supported_profiles = r.get('supportedProfile', [])
            profile = r.get('profile', '')
            resources.append({
                'type': rtype,
                'profile': profile,
                'supportedProfiles': supported_profiles,
                'interactions': interactions,
                'searchParams': search_params,
            })
    
    return {
        'fhirVersion': cs.get('fhirVersion'),
        'implementationGuide': cs.get('implementationGuide', []),
        'implementation_url': cs.get('implementation', {}).get('url'),
        'resources': resources,
    }


def parse_swagger(path, label):
    """Extract paths, schemas, and field-level detail from OpenAPI spec."""
    with open(path) as f:
        sw = json.load(f)
    
    paths = sorted(sw.get('paths', {}).keys())
    
    # Extract schemas (these define the FHIR resource shapes the API returns)
    schemas = {}
    for name, schema_def in sw.get('components', {}).get('schemas', {}).items():
        props = schema_def.get('properties', {})
        fields = []
        for fname, fdef in props.items():
            field = {
                'name': fname,
                'type': fdef.get('type', fdef.get('$ref', 'unknown')),
                'nullable': fdef.get('nullable', False),
                'description': fdef.get('description', ''),
            }
            if 'format' in fdef:
                field['format'] = fdef['format']
            if 'enum' in fdef:
                field['enum'] = fdef['enum']
            fields.append(field)
        if fields:
            schemas[name] = {
                'field_count': len(fields),
                'fields': fields,
                'description': schema_def.get('description', ''),
            }
    
    return {
        'label': label,
        'title': sw.get('info', {}).get('title', ''),
        'version': sw.get('info', {}).get('version', ''),
        'path_count': len(paths),
        'paths': paths,
        'schema_count': len(schemas),
        'schemas': schemas,
    }


def build_entity_inventory(cs_single, cs_bulk, swagger_single, swagger_bulk):
    """
    Build a unified entity inventory from all artifacts.
    Each FHIR resource type becomes an 'entity'.
    """
    entities = []
    
    # Use single-patient capability statement as primary source
    for res in cs_single['resources']:
        rtype = res['type']
        
        # Find matching schema in swagger for field details
        schema_fields = []
        schema_name = None
        for sname, sdef in swagger_single['schemas'].items():
            # Match schema names that correspond to FHIR resource types
            if sname == rtype or sname == f'Fhir{rtype}' or sname.lower() == rtype.lower():
                schema_fields = sdef['fields']
                schema_name = sname
                break
        
        # Determine USCDI category mapping
        uscdi_category = map_to_uscdi(rtype)
        
        entity = {
            'entity_name': rtype,
            'swagger_schema': schema_name,
            'category': uscdi_category,
            'profiles': res['supportedProfiles'],
            'interactions': res['interactions'],
            'search_params': res['searchParams'],
            'field_count': len(schema_fields),
            'fields': schema_fields,
            'in_single_api': True,
            'in_bulk_api': any(r['type'] == rtype for r in cs_bulk['resources']),
            'is_us_core': any('us-core' in p or 'hl7.org/fhir/StructureDefinition' in p 
                             for p in res['supportedProfiles']),
        }
        entities.append(entity)
    
    return entities


def map_to_uscdi(resource_type):
    """Map FHIR resource type to USCDI data class."""
    mapping = {
        'AllergyIntolerance': 'Allergies & Intolerances',
        'CarePlan': 'Assessment & Plan of Treatment',
        'CareTeam': 'Care Team Members',
        'Condition': 'Problems / Encounters',
        'Device': 'Medical Devices',
        'DiagnosticReport': 'Clinical Tests / Lab / Imaging',
        'DocumentReference': 'Clinical Notes',
        'Encounter': 'Encounters',
        'Goal': 'Goals & Preferences',
        'Immunization': 'Immunizations',
        'Location': 'Facility Information',
        'Medication': 'Medications',
        'MedicationRequest': 'Medications',
        'Observation': 'Vitals / Lab / Clinical Tests',
        'Organization': 'Facility Information',
        'Patient': 'Patient Demographics',
        'Practitioner': 'Care Team Members',
        'PractitionerRole': 'Care Team Members',
        'Procedure': 'Procedures',
        'Provenance': 'Provenance',
    }
    return mapping.get(resource_type, 'Other')


def build_summary(entities, cs_single, swagger_single, swagger_bulk):
    """Build summary statistics from the full inventory."""
    total_fields = sum(e['field_count'] for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e['fields'] if f.get('description')
    )
    total_field_objects = sum(len(e['fields']) for e in entities)
    
    # Category breakdown
    categories = {}
    for e in entities:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'field_count': 0}
        categories[cat]['entity_count'] += 1
        categories[cat]['field_count'] += e['field_count']
    
    # Profile analysis
    us_core_count = sum(1 for e in entities if e['is_us_core'])
    custom_profiles = [e for e in entities if not e['is_us_core']]
    
    return {
        'total_entities': len(entities),
        'total_fields': total_fields,
        'fields_with_descriptions': fields_with_desc,
        'description_percentage': round(fields_with_desc / total_field_objects * 100, 1) if total_field_objects > 0 else 0,
        'us_core_entities': us_core_count,
        'custom_profile_entities': len(custom_profiles),
        'categories': categories,
        'fhir_version': cs_single['fhirVersion'],
        'implementation_guides': cs_single['implementationGuide'],
        'single_api_paths': swagger_single['path_count'],
        'bulk_api_paths': swagger_bulk['path_count'],
        'swagger_schemas_single': swagger_single['schema_count'],
        'swagger_schemas_bulk': swagger_bulk['schema_count'],
        'resource_types': [e['entity_name'] for e in entities],
        'domains_covered': sorted(set(e['category'] for e in entities)),
        'domains_not_covered': [
            'Claims / Billing',
            'Insurance / Coverage (beyond basic)',
            'Payments',
            'Patient Communications',
            'Custom Forms / Questionnaires',
            'Referral Workflows',
            'Scheduling',
            'Prior Authorizations',
        ],
    }


def main():
    # Parse all artifacts
    cs_single = parse_capability_statement(os.path.join(DOWNLOADS, 'fhir-capability-statement-single.json'))
    cs_bulk = parse_capability_statement(os.path.join(DOWNLOADS, 'fhir-capability-statement-bulk.json'))
    swagger_single = parse_swagger(os.path.join(DOWNLOADS, 'swagger-single-patient.json'), 'Single Patient API')
    swagger_bulk = parse_swagger(os.path.join(DOWNLOADS, 'swagger-bulk.json'), 'Bulk Export API')
    
    # Build entity inventory
    entities = build_entity_inventory(cs_single, cs_bulk, swagger_single, swagger_bulk)
    
    # Build summary
    summary = build_summary(entities, cs_single, swagger_single, swagger_bulk)
    
    # Write full inventory
    full_output = {
        'product': 'Med A-Z',
        'developer': 'MedAZ.Net, LLC',
        'export_format': 'FHIR R4 (US Core 3.1.1)',
        'source_artifacts': [
            'fhir-capability-statement-single.json',
            'fhir-capability-statement-bulk.json', 
            'swagger-single-patient.json',
            'swagger-bulk.json',
        ],
        'entities': entities,
    }
    
    with open(os.path.join(ANALYSIS, 'entity-inventory-full.json'), 'w') as f:
        json.dump(full_output, f, indent=2)
    
    with open(os.path.join(ANALYSIS, 'entity-inventory-summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Entities: {summary['total_entities']}")
    print(f"Total fields (from swagger schemas): {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_percentage']}%)")
    print(f"US Core entities: {summary['us_core_entities']}")
    print(f"Custom profile entities: {summary['custom_profile_entities']}")
    print(f"\nCategories:")
    for cat, info in sorted(summary['categories'].items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print(f"\nSingle API paths: {summary['single_api_paths']}")
    print(f"Bulk API paths: {summary['bulk_api_paths']}")
    print(f"\nSwagger schemas (single): {summary['swagger_schemas_single']}")
    print(f"Swagger schemas (bulk): {summary['swagger_schemas_bulk']}")


if __name__ == '__main__':
    main()
