"""
Comprehensive parser for all IPClinical EHI export artifacts.
Produces full-entity-inventory.json and summary statistics.
"""
import re
import json
import subprocess

DOWNLOADS = '/home/jmandel/hobby/ehi-export-analysis/results/physicians-emr-llc--ipclinical/downloads'
OUTPUT = '/home/jmandel/hobby/ehi-export-analysis/abstraction/physicians-emr-llc--ipclinical/analysis'

def extract_pdf_text(filename):
    result = subprocess.run(
        ['pdftotext', '-layout', f'{DOWNLOADS}/{filename}', '-'],
        capture_output=True, text=True
    )
    return result.stdout

# ============================================================
# 1. Parse the g10 FHIR API Documentation (121 pages)
# ============================================================
g10_text = extract_pdf_text('IPClinical_g10_API_Documentation.pdf')
lines = g10_text.split('\n')

# Extract unique FHIR resource types from CapabilityStatement
fhir_resource_types_in_cap = sorted(set(
    re.findall(r'"type":\s*"([A-Z]\w+)"', g10_text)
))

# Define documented FHIR resource sections from the TOC
resource_sections = [
    ('Patient', 'Patient', 'Demographics'),
    ('Allergy Intolerance', 'AllergyIntolerance', 'Clinical'),
    ('Care Plan', 'CarePlan', 'Clinical'),
    ('Care Team', 'CareTeam', 'Clinical'),
    ('Conditions', 'Condition', 'Clinical'),
    ('Implantable Device', 'Device', 'Clinical'),
    ('Diagnostic Report for Report and Note exchange', 'DiagnosticReport', 'Clinical'),
    ('Diagnostic Report for Laboratory Results Reporting', 'DiagnosticReport', 'Lab Results'),
    ('Document Reference', 'DocumentReference', 'Documents'),
    ('Goal', 'Goal', 'Clinical'),
    ('Immunization', 'Immunization', 'Clinical'),
    ('MedicationRequest', 'MedicationRequest', 'Medications'),
    ('Smoking Status Observation', 'Observation', 'Vitals/Observations'),
    ('Pediatric Weight for Height Observation', 'Observation', 'Vitals/Observations'),
    ('Laboratory Result Observation', 'Observation', 'Lab Results'),
    ('Pediatric BMI for Age Observation', 'Observation', 'Vitals/Observations'),
    ('Pulse Oximetry', 'Observation', 'Vitals/Observations'),
    ('Pediatric Head Occipital-frontal Circumference Percentile', 'Observation', 'Vitals/Observations'),
    ('Observation Body Height', 'Observation', 'Vitals/Observations'),
    ('Observation Body Temperature', 'Observation', 'Vitals/Observations'),
    ('Observation Blood Pressure', 'Observation', 'Vitals/Observations'),
    ('Observation Body Weight', 'Observation', 'Vitals/Observations'),
    ('Observation Heart Rate', 'Observation', 'Vitals/Observations'),
    ('Observation Respiratory Rate', 'Observation', 'Vitals/Observations'),
    ('Procedure', 'Procedure', 'Clinical'),
    ('Encounter', 'Encounter', 'Clinical'),
    ('Organization', 'Organization', 'Administrative'),
    ('Practitioner', 'Practitioner', 'Administrative'),
    ('Provenance', 'Provenance', 'Administrative'),
    ('Clinical Notes Guidance', 'DocumentReference', 'Documents'),
]

# Find section line numbers (after TOC)
section_line_nums = {}
for i, line in enumerate(lines):
    stripped = line.strip()
    for sec_name, _, _ in resource_sections:
        if stripped == sec_name and i > 100 and '...' not in line:
            if sec_name not in section_line_nums:
                section_line_nums[sec_name] = i

# Parse each section
parsed_sections = []
sorted_sections = sorted(section_line_nums.items(), key=lambda x: x[1])

for idx, (sec_name, start) in enumerate(sorted_sections):
    end = sorted_sections[idx + 1][1] if idx + 1 < len(sorted_sections) else len(lines)
    section_text = '\n'.join(lines[start:end])
    
    # Extract search parameters
    search_params = []
    for line in lines[start:end]:
        sp = re.match(r'^\s+(\w[\w.-]*)\s+\((\w+)\)\s+(Required|Optional)', line.strip())
        if sp:
            search_params.append({
                'name': sp.group(1), 'type': sp.group(2), 'required': sp.group(3)
            })
    
    # Check for sample data
    has_sample = '"resourceType"' in section_text
    has_request = 'Sample Request' in section_text
    
    # Extract LOINC/SNOMED codes from sample responses
    loinc_codes = re.findall(r'"code":\s*"([\d-]+)"', section_text)
    
    # Find the FHIR resource type and category
    fhir_type = None
    category = None
    for sn, ft, cat in resource_sections:
        if sn == sec_name:
            fhir_type = ft
            category = cat
            break
    
    parsed_sections.append({
        'section_name': sec_name,
        'fhir_resource_type': fhir_type,
        'category': category,
        'line_count': end - start,
        'search_parameters': search_params,
        'has_sample_request': has_request,
        'has_sample_response': has_sample,
        'sample_codes': loinc_codes[:5] if loinc_codes else []
    })

# ============================================================
# 2. Parse the b10 Export PDF (2 pages)
# ============================================================
b10_text = extract_pdf_text('b_10_Electronic_Health_Information_export.pdf')
b10_word_count = len(b10_text.split())

b10_export = {
    'document': 'b_10_Electronic_Health_Information_export.pdf',
    'pages': 2,
    'content_pages': 1,  # page 1 is cover
    'word_count': b10_word_count,
    'formats': [
        {
            'name': 'C-CDA',
            'scope': 'Single patient and patient population',
            'data_standard': 'USCDI Version 1',
            'specifications': [
                'HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1 (2012)',
                'HL7 C-CDA R2.1 (2015, 2019 with Errata)',
                'C-CDA R2.1 Companion Guide R2 (2019)'
            ],
            'field_documentation': 'none',
            'sample_data': 'none'
        },
        {
            'name': 'FHIR',
            'scope': 'Single patient and patient population',
            'data_standard': 'FHIR US Core STU V3.1.1, Bulk Data V1.0.1',
            'external_reference': 'IPClinical (g)(10) FHIR API Documentation (121 pages)',
            'field_documentation': 'via g10 doc',
            'sample_data': 'via g10 doc'
        },
        {
            'name': 'Excel/PDF',
            'scope': 'Described generically',
            'categories': {
                'Patient Documents': {
                    'includes': 'lab results, radiology reports, scanned/imported/faxed documents',
                    'format': 'PDF'
                },
                'Scheduling & Appointments': {
                    'format': 'Excel and PDF'
                },
                'Billing & Financial information': {
                    'format': 'Excel (most), PDF (some)',
                    'note': 'Qualified with "most" — unclear what is excluded'
                },
                'Imaging Result Reports': {
                    'format': 'FHIR',
                    'note': 'Redirected to FHIR format'
                }
            },
            'field_documentation': 'none',
            'sample_data': 'none',
            'schema': 'none',
            'column_definitions': 'none'
        }
    ]
}

# ============================================================
# 3. Parse the older API doc (8 pages)
# ============================================================
api_text = extract_pdf_text('IPClinical-api-documentation.pdf')

# Extract USCDI data classes
uscdi_classes = []
in_table = False
for line in api_text.split('\n'):
    if 'DATA CLASS' in line and 'DATA ELEMENTS' in line:
        in_table = True
        continue
    if in_table:
        if 'Version 2.1' in line or '©' in line:
            continue
        if 'IPClinical API' in line:
            continue
        m = re.match(r'^\s{2,}(\S.+?)\s{3,}(.+)$', line)
        if m:
            uscdi_classes.append({
                'data_class': m.group(1).strip(),
                'data_elements': m.group(2).strip()
            })
        elif line.strip() and uscdi_classes:
            # Continuation of previous entry
            uscdi_classes[-1]['data_elements'] += ' ' + line.strip()

api_doc = {
    'document': 'IPClinical-api-documentation.pdf',
    'pages': 8,
    'api_version': '5.0',
    'auth_method': 'OAuth2.0',
    'response_format': 'C-CDA XML',
    'uscdi_data_classes': uscdi_classes,
    'patient_search_params': ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number'],
    'data_retrieval_params': ['PatientKey', 'DateRange', 'IncludedComponents', 'ResponseType']
}

# ============================================================
# 4. Build complete inventory
# ============================================================

unique_fhir_types = sorted(set(s['fhir_resource_type'] for s in parsed_sections))

inventory = {
    'vendor': 'Physicians EMR, LLC',
    'product': 'IPClinical',
    'version': '2.1',
    'analysis_date': '2026-02-16',
    
    'summary': {
        'total_artifacts': 3,
        'total_pages': 131,  # 2 + 121 + 8
        'b10_content_pages': 1,
        'export_formats': ['C-CDA', 'FHIR R4 (US Core 3.1.1)', 'Excel', 'PDF'],
        'has_data_dictionary': False,
        'has_native_schema': False,
        'has_sample_export_files': False,
        'has_field_level_docs_for_excel_pdf': False,
        'fhir_resource_types_in_capability_statement': fhir_resource_types_in_cap,
        'fhir_resource_type_count': len(fhir_resource_types_in_cap),
        'fhir_resource_sections_documented': len(parsed_sections),
        'unique_fhir_types_documented': unique_fhir_types,
        'uscdi_data_class_count': len(uscdi_classes),
        'excel_pdf_categories_mentioned': 4,
        'excel_pdf_field_definitions': 0
    },
    
    'b10_export_documentation': b10_export,
    'g10_fhir_documentation': {
        'document': 'IPClinical_g10_API_Documentation.pdf',
        'pages': 121,
        'fhir_version': '4.0.1',
        'implementation_guide': 'hl7.fhir.us.core|3.1.1',
        'fhir_endpoint': 'https://staging.pemr.com:93/api',
        'auth_endpoint': 'https://staging.pemr.com:93/api/authorize/authorize',
        'supports_bulk_export': True,
        'bulk_operations': ['group-export', 'patient-export', 'export'],
        'resource_types_in_capability_statement': fhir_resource_types_in_cap,
        'documented_resource_sections': parsed_sections
    },
    'proprietary_api_documentation': api_doc
}

# Save full inventory
with open(f'{OUTPUT}/full-entity-inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)

# ============================================================
# Print summary
# ============================================================
print("="*60)
print("IPClinical EHI Export - Full Inventory Summary")
print("="*60)
print(f"\nArtifacts analyzed: 3 PDFs, {131} total pages")
print(f"  b10 doc: 2 pages (1 content page)")
print(f"  g10 doc: 121 pages")
print(f"  API doc: 8 pages")
print(f"\nFHIR Resource Types in CapabilityStatement: {len(fhir_resource_types_in_cap)}")
for rt in fhir_resource_types_in_cap:
    print(f"  - {rt}")
print(f"\nDocumented resource sections: {len(parsed_sections)}")
print(f"Unique FHIR types across sections: {len(unique_fhir_types)}")
print(f"Sections with sample responses: {sum(1 for s in parsed_sections if s['has_sample_response'])}")
print(f"\nUSCDI v1 Data Classes (API doc): {len(uscdi_classes)}")
print(f"\nExcel/PDF export categories: 4 (no field definitions)")
print(f"\nData dictionary: NOT PRESENT")
print(f"Native database schema: NOT PRESENT")
print(f"Sample export files: NOT PRESENT")

print(f"\nSaved: {OUTPUT}/full-entity-inventory.json")
