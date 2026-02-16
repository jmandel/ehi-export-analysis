"""Parse the RevolutionEHR OpenAPI spec and produce entity-inventory-full.json and summary."""
import json
import os

SPEC_PATH = os.path.join(os.path.dirname(__file__), '..', 'downloads', 'openapiServices.json')
OUT_DIR = os.path.dirname(__file__)

with open(SPEC_PATH) as f:
    spec = json.load(f)

schemas = spec.get('components', {}).get('schemas', {})

def resolve_ref(ref_str):
    """Extract schema name from $ref like '#/components/schemas/Address'."""
    return ref_str.split('/')[-1] if ref_str else None

def get_field_type(prop):
    """Determine field type string from OpenAPI property definition."""
    if '$ref' in prop:
        return resolve_ref(prop['$ref'])
    t = prop.get('type', 'unknown')
    fmt = prop.get('format')
    if t == 'array':
        items = prop.get('items', {})
        if '$ref' in items:
            return f"array<{resolve_ref(items['$ref'])}>"
        item_type = items.get('type', 'unknown')
        item_fmt = items.get('format')
        return f"array<{item_fmt or item_type}>"
    return fmt or t

def parse_schema(name, schema):
    """Parse a single schema into structured inventory."""
    props = schema.get('properties', {})
    required = set(schema.get('required', []))
    fields = []
    references = []
    for fname, fprop in props.items():
        field_type = get_field_type(fprop)
        desc = fprop.get('description', '')
        nullable = fprop.get('nullable', False)
        
        # Track references to other schemas
        ref_target = None
        if '$ref' in fprop:
            ref_target = resolve_ref(fprop['$ref'])
        elif fprop.get('type') == 'array' and '$ref' in fprop.get('items', {}):
            ref_target = resolve_ref(fprop['items']['$ref'])
        if ref_target:
            references.append({'field': fname, 'target_schema': ref_target})
        
        # Check if description is meaningful (not just restating field name)
        name_words = set(fname.lower().replace('_', ' ').split())
        desc_words = set(desc.lower().replace('_', ' ').split()) if desc else set()
        is_trivial_desc = desc_words <= name_words or not desc
        
        fields.append({
            'name': fname,
            'type': field_type,
            'description': desc,
            'has_description': bool(desc),
            'has_meaningful_description': not is_trivial_desc,
            'required': fname in required,
            'nullable': nullable,
        })
    
    return {
        'entity': name,
        'field_count': len(fields),
        'fields': fields,
        'references': references,
        'required_fields': sorted(required),
    }

# Categorize schemas by domain
DOMAIN_MAP = {
    'Patient': 'Root',
    'Demographics': 'Demographics',
    'Address': 'Demographics',
    'Employment': 'Demographics',
    'Contact': 'Demographics',
    'FamilyMember': 'Demographics',
    'Encounter': 'Clinical - Encounters',
    'EncounterDiagnosis': 'Clinical - Encounters',
    'ReasonForVisit': 'Clinical - Encounters',
    'Service': 'Clinical - Encounters',
    'VitalSigns': 'Clinical - Vitals',
    'Refraction': 'Clinical - Optometry',
    'Test': 'Clinical - Diagnostics',
    'TestValue': 'Clinical - Diagnostics',
    'ClinicalDecisionSupport': 'Clinical - Decision Support',
    'OrientationMood': 'Clinical - Assessments',
    'SocialHistory': 'Clinical - Social/Family History',
    'FamilyHealthHistory': 'Clinical - Social/Family History',
    'FamilyHistory': 'Clinical - Social/Family History',
    'Diagnosis': 'Clinical - Diagnoses',
    'DiagnosisCarePlanItem': 'Clinical - Diagnoses',
    'CarePlanItem': 'Clinical - Care Plans',
    'HealthGoal': 'Clinical - Goals',
    'HealthConcern': 'Clinical - Concerns',
    'Allergy': 'Clinical - Allergies',
    'Immunization': 'Clinical - Immunizations',
    'ImplantableDevice': 'Clinical - Devices',
    'MedicalOrder': 'Clinical - Orders/Labs',
    'Referral': 'Clinical - Referrals',
    'Insurance': 'Billing & Insurance',
    'Invoice': 'Billing & Insurance',
    'InvoiceItem': 'Billing & Insurance',
    'Claim': 'Billing & Insurance',
    'Payment': 'Billing & Insurance',
    'Statement': 'Billing & Insurance',
}

# Parse all schemas
entities = []
for name in sorted(schemas.keys()):
    entity = parse_schema(name, schemas[name])
    entity['category'] = DOMAIN_MAP.get(name, 'Other')
    entities.append(entity)

# Write full inventory
with open(os.path.join(OUT_DIR, 'entity-inventory-full.json'), 'w') as f:
    json.dump(entities, f, indent=2)

# Compute summary stats
total_fields = sum(e['field_count'] for e in entities)
fields_with_desc = sum(
    sum(1 for field in e['fields'] if field['has_description'])
    for e in entities
)
fields_with_meaningful_desc = sum(
    sum(1 for field in e['fields'] if field['has_meaningful_description'])
    for e in entities
)

# Category breakdown
from collections import defaultdict
cat_stats = defaultdict(lambda: {'entities': 0, 'fields': 0})
for e in entities:
    cat = e['category']
    cat_stats[cat]['entities'] += 1
    cat_stats[cat]['fields'] += e['field_count']

summary = {
    'total_entities': len(entities),
    'total_fields': total_fields,
    'fields_with_any_description': fields_with_desc,
    'fields_with_meaningful_description': fields_with_meaningful_desc,
    'pct_with_description': round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
    'pct_with_meaningful_description': round(100 * fields_with_meaningful_desc / total_fields, 1) if total_fields else 0,
    'category_breakdown': {
        cat: stats for cat, stats in sorted(cat_stats.items())
    },
    'entity_summary': [
        {
            'entity': e['entity'],
            'category': e['category'],
            'field_count': e['field_count'],
            'fields_described': sum(1 for f in e['fields'] if f['has_description']),
            'fields_meaningful_desc': sum(1 for f in e['fields'] if f['has_meaningful_description']),
            'reference_count': len(e['references']),
        }
        for e in entities
    ]
}

with open(os.path.join(OUT_DIR, 'entity-inventory-summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary to stdout
print(f"Total entities: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with any description: {fields_with_desc} ({summary['pct_with_description']}%)")
print(f"Fields with meaningful description: {fields_with_meaningful_desc} ({summary['pct_with_meaningful_description']}%)")
print()
print("Category breakdown:")
for cat, stats in sorted(cat_stats.items()):
    print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")
print()
print("Entity details:")
for e in entities:
    refs = f" (refs: {', '.join(r['target_schema'] for r in e['references'])})" if e['references'] else ""
    print(f"  {e['entity']}: {e['field_count']} fields [{e['category']}]{refs}")
