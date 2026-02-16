#!/usr/bin/env python3
"""
Parse all Javadoc-style HTML entity pages from downloads/ to produce:
  - entity-inventory-full.json: complete field-level inventory
  - entity-inventory-summary.json: aggregate statistics
"""

import json
import os
import re
from html.parser import HTMLParser

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')

# List of entity HTML files (from files.json)
ENTITY_FILES = [
    'AppointmentsEntity.html', 'CasesEntity.html', 'EmrAllergyEntity.html',
    'EmrEncounterEntity.html', 'EmrImplantableDeviceEntity.html',
    'EmrInjectionEntity.html', 'EmrMedicationEntity.html',
    'EmrPatientOrderItemEntity.html', 'EmrPatientOrderPanelEntity.html',
    'EmrProblemEntity.html', 'EmrRefToProvidersEntity.html',
    'EmrVitalsCategoryEntity.html', 'EmrVitalsEntity.html',
    'EncountersDiagEntity.html', 'EncountersEntity.html',
    'GuarantorEntity.html', 'InsuranceDataAuthorizationsEntity.html',
    'InsuranceDataEntity.html', 'InternalNotesEntity.html',
    'MessagesEntity.html', 'NotesEntity.html', 'PatientCareTeamEntity.html',
    'PatientCustomFieldsEntity.html', 'PatientEntity.html',
    'PatientMedicalFormEntity.html', 'PatientPharmacyEntity.html',
    'PaymentEntity.html', 'ScreeningEntity.html', 'TaskCommentsEntity.html',
    'TasksEntity.html', 'TransactionsEntity.html'
]


class JavadocFieldParser(HTMLParser):
    """Parse Javadoc HTML to extract field names, types, and descriptions."""
    
    def __init__(self):
        super().__init__()
        self.fields = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.in_link = False
        self.current_row = []
        self.current_cell = ''
        self.tables = []  # collect all tables
        self.current_table = []
        self.in_header = False
        self.header_row = []
        self.skip_tag = None
        
        # Track sections
        self.current_section = ''
        self.in_heading = False
        self.heading_text = ''
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'table':
            self.in_table = True
            self.current_table = []
            self.header_row = []
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.in_header = (tag == 'th')
            self.current_cell = ''
        elif tag == 'a' and self.in_cell:
            self.in_link = True
        elif tag in ('h2', 'h3', 'h4'):
            self.in_heading = True
            self.heading_text = ''
            
    def handle_endtag(self, tag):
        if tag == 'table':
            if self.current_table:
                self.tables.append({
                    'headers': self.header_row,
                    'rows': self.current_table
                })
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            if self.in_header:
                pass  # headers handled in td/th
            elif self.current_row:
                self.current_table.append(self.current_row)
        elif tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            cell_text = self.current_cell.strip()
            if self.in_header:
                self.header_row.append(cell_text)
                self.in_header = False
            else:
                self.current_row.append(cell_text)
        elif tag == 'a':
            self.in_link = False
        elif tag in ('h2', 'h3', 'h4'):
            self.in_heading = False
            self.current_section = self.heading_text.strip()
            
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data
        if self.in_heading:
            self.heading_text += data


def parse_entity_html(filepath):
    """Parse a single entity HTML file and return field definitions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = JavadocFieldParser()
    parser.feed(content)
    
    fields = []
    
    for table in parser.tables:
        headers = [h.lower().strip() for h in table.get('headers', [])]
        
        # Look for field summary tables - they typically have columns like
        # "Modifier and Type", "Field", "Description" or similar
        if not headers:
            continue
            
        # Find the right columns
        type_col = None
        name_col = None
        desc_col = None
        
        for i, h in enumerate(headers):
            h_lower = h.lower()
            if 'type' in h_lower:
                type_col = i
            if 'field' in h_lower or 'name' in h_lower:
                name_col = i
            if 'description' in h_lower:
                desc_col = i
        
        if name_col is None and type_col is None:
            continue
            
        for row in table['rows']:
            if len(row) <= max(filter(lambda x: x is not None, [type_col, name_col, desc_col]), default=0):
                continue
                
            field = {}
            if type_col is not None and type_col < len(row):
                field['type'] = row[type_col].strip()
            if name_col is not None and name_col < len(row):
                field['name'] = row[name_col].strip()
            if desc_col is not None and desc_col < len(row):
                field['description'] = row[desc_col].strip()
            
            if field.get('name'):
                fields.append(field)
    
    return fields


def categorize_entity(name):
    """Assign a domain category based on entity name."""
    name_lower = name.lower()
    if 'patient' in name_lower and ('entity' == name_lower.replace('patient','').replace('entity','').strip() or name == 'PatientEntity'):
        return 'Demographics'
    if name_lower in ('patientcustomfieldsentity', 'patientcareteamentity', 'patientmedicalformentity', 'patientpharmacyentity'):
        return 'Demographics'
    if 'allergy' in name_lower:
        return 'Clinical - Allergies'
    if 'medication' in name_lower:
        return 'Clinical - Medications'
    if 'injection' in name_lower:
        return 'Clinical - Immunizations'
    if 'problem' in name_lower:
        return 'Clinical - Problems'
    if 'vital' in name_lower:
        return 'Clinical - Vitals'
    if 'encounter' in name_lower and 'diag' not in name_lower:
        return 'Clinical - Encounters'
    if 'encountersdiag' in name_lower:
        return 'Clinical - Diagnoses'
    if 'emrencounter' in name_lower:
        return 'Clinical - Encounters'
    if 'order' in name_lower:
        return 'Clinical - Orders/Labs'
    if 'implantable' in name_lower:
        return 'Clinical - Devices'
    if 'screening' in name_lower:
        return 'Clinical - Screenings'
    if 'refto' in name_lower:
        return 'Clinical - Referrals'
    if 'insurance' in name_lower:
        return 'Insurance'
    if 'guarantor' in name_lower:
        return 'Insurance'
    if 'transaction' in name_lower:
        return 'Billing'
    if 'payment' in name_lower:
        return 'Billing'
    if 'case' in name_lower:
        return 'Cases'
    if 'appointment' in name_lower:
        return 'Scheduling'
    if 'message' in name_lower:
        return 'Communications'
    if 'note' in name_lower:
        return 'Notes'
    if 'task' in name_lower:
        return 'Tasks'
    if 'careplan' in name_lower or 'careteam' in name_lower:
        return 'Care Team'
    return 'Other'


def main():
    entities = []
    total_fields = 0
    total_described = 0
    total_typed = 0
    
    for filename in ENTITY_FILES:
        filepath = os.path.join(DOWNLOADS, filename)
        entity_name = filename.replace('.html', '')
        
        if not os.path.exists(filepath):
            print(f"WARNING: {filepath} not found")
            continue
        
        fields = parse_entity_html(filepath)
        
        # Also cross-reference with the pre-extracted JSON
        json_path = os.path.join(DOWNLOADS, 'entity-data-dictionary.json')
        with open(json_path) as f:
            json_data = json.load(f)
        
        json_fields = json_data.get(entity_name, [])
        
        # Use JSON data if HTML parsing got fewer fields (the JSON was carefully extracted)
        if len(json_fields) > len(fields):
            fields = json_fields
        
        n_fields = len(fields)
        n_described = sum(1 for f in fields if f.get('description', '').strip())
        n_typed = sum(1 for f in fields if f.get('type', '').strip())
        
        category = categorize_entity(entity_name)
        
        entity = {
            'entity_name': entity_name,
            'source_file': filename,
            'category': category,
            'field_count': n_fields,
            'fields_with_descriptions': n_described,
            'fields_with_types': n_typed,
            'fields': fields
        }
        
        entities.append(entity)
        total_fields += n_fields
        total_described += n_described
        total_typed += n_typed
    
    # Write full inventory
    output_path = os.path.join(os.path.dirname(__file__), 'entity-inventory-full.json')
    with open(output_path, 'w') as f:
        json.dump(entities, f, indent=2)
    
    # Build summary
    categories = {}
    for e in entities:
        cat = e['category']
        if cat not in categories:
            categories[cat] = {'entity_count': 0, 'field_count': 0, 'fields_described': 0, 'entities': []}
        categories[cat]['entity_count'] += 1
        categories[cat]['field_count'] += e['field_count']
        categories[cat]['fields_described'] += e['fields_with_descriptions']
        categories[cat]['entities'].append(e['entity_name'])
    
    summary = {
        'total_entities': len(entities),
        'total_fields': total_fields,
        'total_fields_with_descriptions': total_described,
        'total_fields_with_types': total_typed,
        'description_coverage_pct': round(100 * total_described / total_fields, 1) if total_fields else 0,
        'type_coverage_pct': round(100 * total_typed / total_fields, 1) if total_fields else 0,
        'categories': categories,
        'entities': [{
            'entity_name': e['entity_name'],
            'category': e['category'],
            'field_count': e['field_count'],
            'fields_with_descriptions': e['fields_with_descriptions'],
            'fields_with_types': e['fields_with_types']
        } for e in sorted(entities, key=lambda x: -x['field_count'])]
    }
    
    summary_path = os.path.join(os.path.dirname(__file__), 'entity-inventory-summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({summary['description_coverage_pct']}%)")
    print(f"Fields with types: {total_typed} ({summary['type_coverage_pct']}%)")
    print()
    print("By category:")
    for cat, info in sorted(categories.items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields, {info['fields_described']} described")
    print()
    print("Top 10 entities by field count:")
    for e in sorted(entities, key=lambda x: -x['field_count'])[:10]:
        print(f"  {e['entity_name']}: {e['field_count']} fields ({e['fields_with_descriptions']} described)")


if __name__ == '__main__':
    main()
