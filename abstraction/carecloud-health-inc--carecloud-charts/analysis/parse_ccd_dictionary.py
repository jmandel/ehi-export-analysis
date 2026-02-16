#!/usr/bin/env python3
"""Parse CareCloud Charts EHI export PDF to extract CCD data dictionary and export components."""

import json
import re
import subprocess

# Extract text from PDF
result = subprocess.run(['pdftotext', '-layout', '../downloads/ehi-export-documentation.pdf', '-'],
                       capture_output=True, text=True)
text = result.stdout

# Parse the CCD sections and their data elements
sections = []
current_section = None
current_elements = []

lines = text.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Detect section headers (contain OID patterns like [2.16.840...])
    section_match = re.match(r'^(.+?)\s*\[([0-9.]+)\s*:\s*([0-9-]+)\]', line)
    if section_match:
        if current_section:
            sections.append({'section': current_section, 'oid': current_oid, 'elements': current_elements})
        current_section = section_match.group(1).strip()
        current_oid = section_match.group(2).strip()
        current_elements = []
        continue
    
    # Detect standalone section headers
    standalone_sections = [
        'Patient Demographics/Information',
        'Provider\'s name and office contact information',
        'Laboratory Tests', 'Laboratory Information',
    ]
    if line in standalone_sections:
        if current_section:
            sections.append({'section': current_section, 'oid': current_oid if 'current_oid' in dir() else None, 'elements': current_elements})
        current_section = line
        current_oid = None
        current_elements = []
        continue

# Don't forget the last section
if current_section:
    sections.append({'section': current_section, 'oid': current_oid, 'elements': current_elements})

# Now re-parse more carefully to get data elements per section
# Use a structured approach based on the known sections from the PDF
ccd_sections = {
    "Patient Demographics/Information": [
        {"name": "Patient Name", "xpath": "patient/name", "code_system": None},
        {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "AdministrativeGender"},
        {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None},
        {"name": "Race", "xpath": "patient/raceCode", "code_system": "Race & Ethnicity - CDC"},
        {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "Race & Ethnicity - CDC"},
        {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None},
    ],
    "Provider Information": [
        {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None},
        {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None},
        {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None},
    ],
    "Date and Location of Visit": [
        {"name": "Encounter Time", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None},
        {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None},
    ],
    "Chief Complaint and Reason for Visit": [
        {"name": "Patient visit details/complaints", "xpath": None, "code_system": None},
    ],
    "Encounters": [
        {"name": "Encounter Code and Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system": "CPT"},
        {"name": "Performer", "xpath": None, "code_system": None},
        {"name": "Diagnosis", "xpath": None, "code_system": "SNOMED and ICD10"},
        {"name": "Location", "xpath": None, "code_system": None},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
    "Immunizations": [
        {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", "code_system": "CVX and CPT-4"},
        {"name": "Date", "xpath": None, "code_system": None},
        {"name": "Status", "xpath": None, "code_system": None},
        {"name": "Route", "xpath": None, "code_system": "NCI Thesaurus"},
        {"name": "Site", "xpath": None, "code_system": "SNOMED"},
        {"name": "Manufacturer", "xpath": None, "code_system": None},
        {"name": "Dose", "xpath": None, "code_system": None},
        {"name": "Lot Number", "xpath": None, "code_system": None},
        {"name": "Notes", "xpath": None, "code_system": None},
    ],
    "Instructions": [
        {"name": "Patient Instructions/Follow-up Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system": "SNOMED"},
    ],
    "Treatment Plan": [
        {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system": "LOINC"},
        {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40/39/121", "code_system": None},
    ],
    "Social History": [
        {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system": "LOINC"},
        {"name": "Description", "xpath": None, "code_system": "SNOMED"},
        {"name": "Dates Observed", "xpath": None, "code_system": None},
    ],
    "Problems": [
        {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system": "SNOMED and ICD10"},
        {"name": "Status", "xpath": None, "code_system": None},
        {"name": "Active date", "xpath": None, "code_system": None},
    ],
    "Medications": [
        {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system": "RxNorm and NDC"},
        {"name": "Directions", "xpath": None, "code_system": None},
        {"name": "Start Date", "xpath": None, "code_system": None},
        {"name": "End Date", "xpath": None, "code_system": None},
        {"name": "Status", "xpath": None, "code_system": None},
    ],
    "Medication Allergies": [
        {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system": "RxNorm"},
        {"name": "Reaction", "xpath": None, "code_system": "SNOMED"},
        {"name": "Severity", "xpath": None, "code_system": "SNOMED"},
        {"name": "Status", "xpath": None, "code_system": "SNOMED"},
    ],
    "Laboratory Tests": [
        {"name": "Test Code", "xpath": None, "code_system": None},
        {"name": "Code System", "xpath": None, "code_system": "LOINC"},
        {"name": "Name", "xpath": None, "code_system": None},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
    "Laboratory Information": [
        {"name": "Lab Name", "xpath": None, "code_system": None},
        {"name": "Lab Address", "xpath": None, "code_system": None},
        {"name": "Test Report Date", "xpath": None, "code_system": None},
        {"name": "Test Performed", "xpath": None, "code_system": None},
        {"name": "Specimen Source", "xpath": None, "code_system": None},
    ],
    "Laboratory Results": [
        {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system": "LOINC"},
        {"name": "Result Value", "xpath": None, "code_system": None},
        {"name": "Relevant Reference Range", "xpath": None, "code_system": None},
        {"name": "Interpretation", "xpath": None, "code_system": None},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
    "Vitals": [
        {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system": "LOINC"},
        {"name": "Observation Date/Time", "xpath": None, "code_system": None},
    ],
    "Goals": [
        {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None},
        {"name": "Value", "xpath": None, "code_system": None},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
    "Procedures": [
        {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system": "CPT-4 or SNOMED or HCPCS"},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
    "Care Team Members": [
        {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system": None},
        {"name": "Specialty", "xpath": None, "code_system": None},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
    "Reason for Referral": [
        {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "SNOMED"},
    ],
    "Medical Equipment": [
        {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system": "SNOMED"},
        {"name": "GMDN PT Description", "xpath": None, "code_system": None},
    ],
    "Mental Status": [
        {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system": None},
        {"name": "Assessment Date", "xpath": None, "code_system": None},
        {"name": "Results", "xpath": None, "code_system": "SNOMED"},
        {"name": "Comments", "xpath": None, "code_system": None},
    ],
    "Functional Status": [
        {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system": None},
        {"name": "Assessment Date", "xpath": None, "code_system": None},
        {"name": "Results", "xpath": None, "code_system": "SNOMED"},
        {"name": "Comments", "xpath": None, "code_system": None},
    ],
    "Health Concern": [
        {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system": "SNOMED"},
        {"name": "Status", "xpath": None, "code_system": None},
        {"name": "Date", "xpath": None, "code_system": None},
    ],
}

# PDF export components (non-CCD)
pdf_exports = [
    {
        "name": "Patient Demographic/Insurance",
        "format": "PDF",
        "description": "Comprehensive view of patient demographics and insurance details"
    },
    {
        "name": "Advance Directive",
        "format": "PDF",
        "description": "Comprehensive view of patient's Advance Directive"
    },
    {
        "name": "Appointments",
        "format": "PDF",
        "description": "Comprehensive view of patient's Appointments"
    },
    {
        "name": "Provider-to-Patient Messages",
        "format": "PDF",
        "description": "Comprehensive view of messages"
    },
    {
        "name": "Billing Data (Claim)",
        "format": "PDF",
        "description": "Comprehensive view of billing data (CPT, ICD, Modifier)"
    },
    {
        "name": "Documents",
        "format": "PDF",
        "description": "Signed progress notes, available lab results, radiology reports and any other scanned or uploaded document"
    },
]

# FHIR export
fhir_export = {
    "name": "FHIR Data Export",
    "description": "FHIR Server creates single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in §170.315(b)(10)(ii)"
}

# Build entity inventory
entities = []

# CCD as one entity with all sections
total_ccd_fields = 0
for section_name, fields in ccd_sections.items():
    entity = {
        "entity_name": f"CCD - {section_name}",
        "category": "Clinical Data (CCD/C-CDA)",
        "format": "XML (C-CDA)",
        "field_count": len(fields),
        "fields": []
    }
    for f in fields:
        entity["fields"].append({
            "name": f["name"],
            "type": "C-CDA element",
            "xpath": f["xpath"],
            "code_system": f["code_system"],
            "description": None,  # No descriptions beyond the name
            "has_description": False
        })
    total_ccd_fields += len(fields)
    entities.append(entity)

# PDF exports as entities
for pe in pdf_exports:
    entities.append({
        "entity_name": pe["name"],
        "category": "PDF Export",
        "format": "PDF",
        "field_count": 0,  # No field-level documentation
        "fields": [],
        "description": pe["description"],
        "note": "No field-level data dictionary provided; exported as human-readable PDF"
    })

# FHIR export
entities.append({
    "entity_name": "FHIR Data Export",
    "category": "FHIR Bulk Data",
    "format": "FHIR R4",
    "field_count": 0,
    "fields": [],
    "description": fhir_export["description"],
    "note": "No FHIR resource type list or field mapping provided; references §170.315(b)(10)(ii)"
})

# Compute stats
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
fields_with_descriptions = sum(
    1 for e in entities for f in e.get("fields", []) if f.get("has_description", False)
)
fields_with_code_systems = sum(
    1 for e in entities for f in e.get("fields", []) if f.get("code_system")
)

ccd_section_count = len(ccd_sections)
pdf_export_count = len(pdf_exports)

summary = {
    "product": "CareCloud Charts v3.0",
    "source_file": "ehi-export-documentation.pdf",
    "source_pages": 11,
    "export_components": {
        "ccd_clinical_data": {
            "format": "C-CDA (XML/HTML)",
            "sections": ccd_section_count,
            "total_data_elements": total_ccd_fields,
            "export_modes": ["Single Patient", "Bulk Patient (via Analytics)"],
            "standard": "HL7 CDA R2 C-CDA 2.1 (DSTU)"
        },
        "pdf_exports": {
            "format": "PDF",
            "count": pdf_export_count,
            "components": [pe["name"] for pe in pdf_exports],
            "field_level_documentation": False
        },
        "fhir_export": {
            "format": "FHIR R4",
            "documentation_detail": "One sentence; no resource types or fields listed",
            "references_b10_ii": True
        }
    },
    "documentation_quality": {
        "total_entities_documented": total_entities,
        "total_fields_documented": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "pct_fields_with_descriptions": 0.0,
        "fields_with_code_systems": fields_with_code_systems,
        "pct_fields_with_code_systems": round(fields_with_code_systems / total_fields * 100, 1) if total_fields > 0 else 0,
        "field_types_documented": False,
        "relationships_documented": False,
        "value_sets_documented": False,
        "sample_data_provided": False
    },
    "ccd_sections_breakdown": {section: len(fields) for section, fields in ccd_sections.items()},
    "pdf_exports_breakdown": {pe["name"]: pe["description"] for pe in pdf_exports}
}

# Write full inventory
with open('entity-inventory-full.json', 'w') as f:
    json.dump(entities, f, indent=2)

# Write summary
with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"=== CareCloud Charts EHI Export Documentation Analysis ===")
print(f"Source: ehi-export-documentation.pdf (11 pages)")
print(f"\nExport Components:")
print(f"  1. CCD (C-CDA) clinical data: {ccd_section_count} sections, {total_ccd_fields} data elements")
print(f"  2. PDF exports: {pdf_export_count} document types (no field-level docs)")
print(f"  3. FHIR Bulk Data: mentioned in 1 sentence (no detail)")
print(f"\nCCD Sections:")
for section, fields in ccd_sections.items():
    print(f"  - {section}: {len(fields)} elements")
print(f"\nPDF Exports:")
for pe in pdf_exports:
    print(f"  - {pe['name']}: {pe['description']}")
print(f"\nDocumentation Quality:")
print(f"  Total fields with any documentation: {total_fields}")
print(f"  Fields with descriptions beyond name: {fields_with_descriptions} (0%)")
print(f"  Fields with code systems specified: {fields_with_code_systems} ({summary['documentation_quality']['pct_fields_with_code_systems']}%)")
print(f"  Field types documented: No")
print(f"  Relationships/FKs documented: No")
print(f"  Value sets documented: No (code system OIDs only)")
print(f"  Sample data provided: No")
