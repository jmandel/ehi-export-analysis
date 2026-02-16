#!/usr/bin/env python3
"""Parse Azalea Health EHI export documentation from HTML artifacts.

Reads:
  - downloads/ambulatory-export.html (57 EHR concept → FHIR resource mappings)
  - downloads/hospital-export.html (45 EHR concept → FHIR resource mappings)
  - downloads/ambulatory-profiles.html (profile definitions)
  - downloads/ambulatory-extensions.html (custom extension definitions)
  - downloads/ambulatory-capability-statement.json
  - downloads/hospital-capability-statement.json
  - downloads/ambulatory-resources.html (resource descriptions w/ search params)

Produces:
  - analysis/entity-inventory-full.json
  - analysis/entity-inventory-summary.json
"""

import json
import re
import os
from html.parser import HTMLParser

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')


class RowExtractor(HTMLParser):
    """Extract 3-column rows from Azalea's div-based tables in main content."""
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.in_col = False
        self.current_row = []
        self.rows = []
        self.current_text = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'main':
            self.in_main = True
        if self.in_main and tag == 'div' and 'col-md' in attrs_dict.get('class', ''):
            self.in_col = True
            self.current_text = ''

    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False
        if self.in_main and self.in_col and tag == 'div':
            self.in_col = False
            self.current_row.append(self.current_text.strip())
            if len(self.current_row) == 3:
                self.rows.append(tuple(self.current_row))
                self.current_row = []

    def handle_data(self, data):
        if self.in_col:
            self.current_text += data


def parse_export_mappings(filepath):
    """Parse EHR concept → FHIR resource mapping table."""
    p = RowExtractor()
    with open(filepath) as f:
        p.feed(f.read())
    # Skip header row
    return [
        {"ehr_concept": r[0], "fhir_resource": r[1], "notes": r[2]}
        for r in p.rows if r[0] != 'EHR Concept'
    ]


def parse_profiles(filepath):
    """Parse profile definitions (name, resource type, description)."""
    p = RowExtractor()
    with open(filepath) as f:
        p.feed(f.read())
    return [
        {"profile_name": r[0], "resource_type": r[1], "description": r[2]}
        for r in p.rows if r[0] != 'Profile Name'
    ]


def parse_extensions(filepath):
    """Parse extension definitions (name, publisher, description)."""
    p = RowExtractor()
    with open(filepath) as f:
        p.feed(f.read())
    return [
        {"extension_name": r[0], "publisher": r[1], "description": r[2]}
        for r in p.rows if r[0] != 'Extension Name'
    ]


def parse_capability_statement(filepath):
    """Extract resource types and their interactions from CapabilityStatement."""
    with open(filepath) as f:
        cs = json.load(f)
    resources = cs.get('rest', [{}])[0].get('resource', [])
    result = []
    for r in resources:
        search_params = [sp['name'] for sp in r.get('searchParam', [])]
        result.append({
            "resource_type": r['type'],
            "interactions": [i['code'] for i in r.get('interaction', [])],
            "search_params": search_params,
            "search_param_count": len(search_params),
        })
    return result


def parse_resources_page(filepath):
    """Parse ambulatory/hospital resources page for detailed resource descriptions."""
    # This page has more complex structure - extract text content per resource
    with open(filepath) as f:
        content = f.read()
    # Find resource sections by looking for heading patterns
    # Each resource section starts with a heading containing the resource type
    sections = re.findall(
        r'<ahi-text[^>]*heading[^>]*>([^<]+)</ahi-text>',
        content
    )
    return sections


def categorize_concept(concept, notes):
    """Assign a domain category to an EHR concept."""
    c = concept.lower()
    n = notes.lower()
    
    if any(w in c for w in ['billing', 'financial', 'claim', 'payment', 'statement', 'pre-cert', 'account']):
        return 'Billing & Financial'
    if any(w in c for w in ['insurance', 'coverage']):
        return 'Insurance'
    if any(w in c for w in ['demographic', 'emergency contact', 'employer', 'employment', 'guarantor', 'next of kin', 'power of attorney']):
        return 'Demographics & Contacts'
    if any(w in c for w in ['allerg']):
        return 'Allergies'
    if any(w in c for w in ['immuniz']):
        return 'Immunizations'
    if any(w in c for w in ['vital']):
        return 'Vital Signs'
    if any(w in c for w in ['lab']):
        return 'Laboratory'
    if any(w in c for w in ['radiology', 'imaging']):
        return 'Radiology / Imaging'
    if any(w in c for w in ['medication', 'prescription', 'emar']):
        return 'Medications'
    if any(w in c for w in ['problem', 'diagnos', 'health concern', 'condition', 'care level']):
        return 'Problems & Diagnoses'
    if any(w in c for w in ['procedure']):
        return 'Procedures'
    if any(w in c for w in ['encounter', 'admission', 'appointment']):
        return 'Encounters & Scheduling'
    if any(w in c for w in ['note', 'document', 'chart', 'handout', 'file', 'amendment']):
        return 'Clinical Notes & Documents'
    if any(w in c for w in ['care plan', 'care team', 'goal', 'recall']):
        return 'Care Plans & Goals'
    if any(w in c for w in ['family']):
        return 'Family History'
    if any(w in c for w in ['social', 'smoking', 'sexual', 'travel']):
        return 'Social History & Observations'
    if any(w in c for w in ['portal', 'message', 'communication', 'comment', 'popup', 'memo']):
        return 'Patient Communications'
    if any(w in c for w in ['device', 'implant']):
        return 'Devices'
    if any(w in c for w in ['evaluation', 'questionnaire', 'question']):
        return 'Assessments & Questionnaires'
    if any(w in c for w in ['dietary', 'nutrition']):
        return 'Dietary / Nutrition'
    if any(w in c for w in ['nursing']):
        return 'Nursing'
    if any(w in c for w in ['cardiology']):
        return 'Cardiology'
    if any(w in c for w in ['therapy']):
        return 'Therapy'
    if any(w in c for w in ['supply']):
        return 'Supplies'
    if any(w in c for w in ['flowsheet']):
        return 'Flowsheets'
    if any(w in c for w in ['death']):
        return 'Patient Status'
    if any(w in c for w in ['pregnancy', 'lactating']):
        return 'Patient Status'
    if any(w in c for w in ['pharmacy']):
        return 'Pharmacy'
    if any(w in c for w in ['provider', 'practitioner', 'location']):
        return 'Administrative'
    if any(w in c for w in ['class', 'group', 'url']):
        return 'Administrative'
    return 'Other'


def main():
    # Parse all artifacts
    amb_mappings = parse_export_mappings(os.path.join(DOWNLOADS, 'ambulatory-export.html'))
    hosp_mappings = parse_export_mappings(os.path.join(DOWNLOADS, 'hospital-export.html'))
    
    profiles = parse_profiles(os.path.join(DOWNLOADS, 'ambulatory-profiles.html'))
    extensions = parse_extensions(os.path.join(DOWNLOADS, 'ambulatory-extensions.html'))
    
    amb_cs = parse_capability_statement(os.path.join(DOWNLOADS, 'ambulatory-capability-statement.json'))
    hosp_cs = parse_capability_statement(os.path.join(DOWNLOADS, 'hospital-capability-statement.json'))

    # Build entity inventory
    # Each "entity" is an EHR concept mapping
    entities = []
    
    for m in amb_mappings:
        m['platform'] = 'ambulatory'
        m['category'] = categorize_concept(m['ehr_concept'], m['notes'])
        entities.append(m)
    
    for m in hosp_mappings:
        m['platform'] = 'hospital'
        m['category'] = categorize_concept(m['ehr_concept'], m['notes'])
        entities.append(m)

    # Build extension lookup by resource type prefix
    ext_by_resource = {}
    for ext in extensions:
        name = ext['extension_name']
        # Try to identify which resource the extension belongs to
        prefix = name.split(' ')[0]
        ext_by_resource.setdefault(prefix, []).append(ext)

    # Build full inventory
    full_inventory = {
        "extraction_date": "2026-02-16",
        "source_files": [
            "downloads/ambulatory-export.html",
            "downloads/hospital-export.html",
            "downloads/ambulatory-profiles.html",
            "downloads/ambulatory-extensions.html",
            "downloads/ambulatory-capability-statement.json",
            "downloads/hospital-capability-statement.json",
        ],
        "ambulatory": {
            "ehr_concept_count": len(amb_mappings),
            "fhir_resource_types_used": sorted(set(m['fhir_resource'] for m in amb_mappings)),
            "fhir_resource_type_count": len(set(m['fhir_resource'] for m in amb_mappings)),
            "capability_statement_resource_count": len(amb_cs),
            "mappings": amb_mappings,
        },
        "hospital": {
            "ehr_concept_count": len(hosp_mappings),
            "fhir_resource_types_used": sorted(set(m['fhir_resource'] for m in hosp_mappings)),
            "fhir_resource_type_count": len(set(m['fhir_resource'] for m in hosp_mappings)),
            "capability_statement_resource_count": len(hosp_cs),
            "mappings": hosp_mappings,
        },
        "profiles": {
            "count": len(profiles),
            "items": profiles,
        },
        "extensions": {
            "count": len(extensions),
            "items": extensions,
        },
        "capability_statements": {
            "ambulatory": {
                "resource_count": len(amb_cs),
                "resources": amb_cs,
            },
            "hospital": {
                "resource_count": len(hosp_cs),
                "resources": hosp_cs,
            },
        },
    }

    # Build summary
    all_amb_concepts = [m['ehr_concept'] for m in amb_mappings]
    all_hosp_concepts = [m['ehr_concept'] for m in hosp_mappings]
    combined_concepts = sorted(set(all_amb_concepts) | set(all_hosp_concepts))
    
    # Category breakdown
    amb_categories = {}
    for m in amb_mappings:
        cat = m['category']
        amb_categories.setdefault(cat, []).append(m['ehr_concept'])
    
    hosp_categories = {}
    for m in hosp_mappings:
        cat = m['category']
        hosp_categories.setdefault(cat, []).append(m['ehr_concept'])
    
    all_categories = sorted(set(list(amb_categories.keys()) + list(hosp_categories.keys())))
    
    category_summary = []
    for cat in all_categories:
        amb_concepts = amb_categories.get(cat, [])
        hosp_concepts = hosp_categories.get(cat, [])
        combined = sorted(set(amb_concepts + hosp_concepts))
        category_summary.append({
            "category": cat,
            "ambulatory_concepts": len(amb_concepts),
            "hospital_concepts": len(hosp_concepts),
            "combined_unique_concepts": len(combined),
            "concepts": combined,
        })

    # Extension categories
    ext_categories = {}
    for ext in extensions:
        # Categorize by first word of extension name
        first_word = ext['extension_name'].split(' ')[0]
        ext_categories.setdefault(first_word, []).append(ext['extension_name'])

    # Concepts beyond USCDI
    uscdi_concepts = {
        'Allergies', 'Care Plans', 'Care Plans (Goals)', 'Care Teams',
        'Encounter (Clinical)', 'Encounter Diagnoses', 'Encounter Procedures',
        'Family History', 'Health Concerns', 'Immunizations', 'Implantable Devices',
        'Insurance', 'Laboratory Orders', 'Laboratory Reports', 'Laboratory Results',
        'Locations', 'Medications', 'Patient Demographics', 'Prescriptions',
        'Problem History', 'Procedure History', 'Providers', 'Sexual Orientation',
        'Smoking Status', 'Social History', 'Vital Signs',
    }
    
    beyond_uscdi_amb = [m['ehr_concept'] for m in amb_mappings if m['ehr_concept'] not in uscdi_concepts]
    beyond_uscdi_hosp = [m['ehr_concept'] for m in hosp_mappings if m['ehr_concept'] not in uscdi_concepts]

    summary = {
        "extraction_date": "2026-02-16",
        "totals": {
            "ambulatory_ehr_concepts": len(amb_mappings),
            "hospital_ehr_concepts": len(hosp_mappings),
            "combined_unique_ehr_concepts": len(combined_concepts),
            "ambulatory_fhir_resource_types": len(set(m['fhir_resource'] for m in amb_mappings)),
            "hospital_fhir_resource_types": len(set(m['fhir_resource'] for m in hosp_mappings)),
            "combined_fhir_resource_types": len(set(m['fhir_resource'] for m in amb_mappings) | set(m['fhir_resource'] for m in hosp_mappings)),
            "ambulatory_capability_resources": len(amb_cs),
            "hospital_capability_resources": len(hosp_cs),
            "custom_profiles": len(profiles),
            "custom_extensions": len(extensions),
        },
        "concepts_beyond_uscdi": {
            "ambulatory": sorted(beyond_uscdi_amb),
            "ambulatory_count": len(beyond_uscdi_amb),
            "hospital": sorted(beyond_uscdi_hosp),
            "hospital_count": len(beyond_uscdi_hosp),
        },
        "categories": category_summary,
        "extension_groups": {k: len(v) for k, v in sorted(ext_categories.items())},
    }

    # Write outputs
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(full_inventory, f, indent=2)
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Ambulatory EHR concepts: {len(amb_mappings)}")
    print(f"Hospital EHR concepts: {len(hosp_mappings)}")
    print(f"Combined unique concepts: {len(combined_concepts)}")
    print(f"Custom profiles: {len(profiles)}")
    print(f"Custom extensions: {len(extensions)}")
    print(f"\nBeyond USCDI (ambulatory): {len(beyond_uscdi_amb)}")
    print(f"Beyond USCDI (hospital): {len(beyond_uscdi_hosp)}")
    print(f"\nCategories:")
    for cs in category_summary:
        print(f"  {cs['category']}: {cs['combined_unique_concepts']} concepts")
    print(f"\nExtension groups:")
    for k, v in sorted(ext_categories.items(), key=lambda x: -len(x[1])):
        print(f"  {k}: {v} extensions")


if __name__ == '__main__':
    main()
