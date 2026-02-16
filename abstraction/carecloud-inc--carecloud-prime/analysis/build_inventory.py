#!/usr/bin/env python3
"""
Build entity inventory for CareCloud Prime EHI Export.
Based on manual review of the PDF data dictionary (certification_b10_ehi_export_documentation.pdf).
The PDF has poor tabular structure that doesn't parse well automatically,
so we define the entities manually from careful reading of pages 6-10.
"""

import json

# C-CDA sections from the data dictionary (pages 6-10)
# Each section maps to a C-CDA template with specific data elements
ccd_entities = [
    {
        "entity_name": "Patient Demographics/Information",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": None,
        "field_count": 6,
        "fields": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system": None, "code_system_name": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None, "code_system_name": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Provider's name and office contact information",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": None,
        "field_count": 3,
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None, "code_system_name": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None, "code_system_name": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Date and Location of visit",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.22.1",
        "field_count": 2,
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None, "code_system_name": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Chief Complaint and Reason for visit",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.13",
        "field_count": 1,
        "fields": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Encounters",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.22.1",
        "field_count": 5,
        "fields": [
            {"name": "Encounter Code and Description", "xpath": "2.16.840.1.113883.10.20.22.4.49", "code_system": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "Performer", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Diagnosis", "xpath": None, "code_system": "2.16.840.1.113883.6.96 / 2.16.840.1.113883.6.3", "code_system_name": "SNOMED / ICD10"},
            {"name": "Location", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Immunizations",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.2.1",
        "field_count": 9,
        "fields": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52", "code_system": "2.16.840.1.113883.12.292 / 2.16.840.1.113883.6.12", "code_system_name": "CVX / CPT-4"},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Route", "xpath": None, "code_system": "2.16.840.1.113883.3.26.1.1", "code_system_name": "NCI Thesaurus"},
            {"name": "Site", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Manufacturer", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Dose", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Lot Number", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Notes", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Instructions",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.45",
        "field_count": 1,
        "fields": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ],
    },
    {
        "entity_name": "Treatment Plan",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.10",
        "field_count": 2,
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40 / .39 / .121", "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Social History",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.17",
        "field_count": 3,
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Description", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Dates Observed", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Problems",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.5.1",
        "field_count": 3,
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3", "code_system": "2.16.840.1.113883.6.96 / 2.16.840.1.113883.6.3", "code_system_name": "SNOMED / ICD10"},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Active date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Medications",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.1.1",
        "field_count": 5,
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16", "code_system": "2.16.840.1.113883.6.88 / 2.16.840.1.113883.6.69", "code_system_name": "RxNorm / NDC"},
            {"name": "Directions", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Start Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "End Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Medication Allergies",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.6.1",
        "field_count": 4,
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30", "code_system": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
            {"name": "Reaction", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Severity", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ],
    },
    {
        "entity_name": "Laboratory Tests",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": None,
        "field_count": 3,
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Name", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Laboratory Information",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": None,
        "field_count": 5,
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Lab Address", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Test Report Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Test Performed", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Specimen Source", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Laboratory Results",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.3.1",
        "field_count": 5,
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Result Value", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Interpretation", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Vitals",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.4.1",
        "field_count": 2,
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Observation Date/Time", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Goal",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.60",
        "field_count": 3,
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None, "code_system_name": None},
            {"name": "Value", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Procedures",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.7.1",
        "field_count": 2,
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system": "2.16.840.1.113883.6.12 / .96 / .13", "code_system_name": "CPT-4 / SNOMED / HCPCS"},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Care team member(s)",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.500",
        "field_count": 3,
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500", "code_system": None, "code_system_name": None},
            {"name": "Specialty", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Reason for Referral",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
        "field_count": 1,
        "fields": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ],
    },
    {
        "entity_name": "Medical Equipment",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.23",
        "field_count": 2,
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "GMDN PT Description", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Mental Status",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.56",
        "field_count": 4,
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74", "code_system": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Functional Status",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.14",
        "field_count": 4,
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67", "code_system": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
    {
        "entity_name": "Health Concern",
        "category": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "cda_template_id": "2.16.840.1.113883.10.20.22.2.58",
        "field_count": 3,
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ],
    },
]

# PDF export entities (page 11) - no field-level detail provided
pdf_entities = [
    {
        "entity_name": "Patient Demographic/Insurance",
        "category": "Administrative (PDF)",
        "format": "PDF",
        "description": "Comprehensive view of demographics and insurance details",
        "field_count": 0,
        "fields": [],
    },
    {
        "entity_name": "Advance Directive",
        "category": "Clinical (PDF)",
        "format": "PDF",
        "description": "Comprehensive view of Advance Directive",
        "field_count": 0,
        "fields": [],
    },
    {
        "entity_name": "Appointments",
        "category": "Administrative (PDF)",
        "format": "PDF",
        "description": "Comprehensive view of appointments",
        "field_count": 0,
        "fields": [],
    },
    {
        "entity_name": "Provider-to-Patient Messages",
        "category": "Patient Communications (PDF)",
        "format": "PDF",
        "description": "Comprehensive view of messages",
        "field_count": 0,
        "fields": [],
    },
    {
        "entity_name": "Billing Data (Claim)",
        "category": "Billing (PDF)",
        "format": "PDF",
        "description": "Comprehensive view of billing data (CPT, ICD, Modifier)",
        "field_count": 0,
        "fields": [],
    },
    {
        "entity_name": "Documents",
        "category": "Clinical (PDF)",
        "format": "PDF",
        "description": "Signed progress notes, lab results, radiology reports, scanned/uploaded documents",
        "field_count": 0,
        "fields": [],
    },
]

# FHIR export (page 12)
fhir_entity = {
    "entity_name": "FHIR Bulk Data Export",
    "category": "FHIR",
    "format": "FHIR R4",
    "description": "Single-patient FHIR DocumentReference and FHIR Bulk Data EHI Export for patient population",
    "field_count": 0,
    "fields": [],
}

all_entities = ccd_entities + pdf_entities + [fhir_entity]
total_fields = sum(e["field_count"] for e in all_entities)

# Build full inventory
full_inventory = {
    "product": "CareCloud Prime",
    "version": "2.0",
    "source_document": "certification_b10_ehi_export_documentation.pdf",
    "source_pages": 12,
    "export_formats": ["C-CDA XML", "PDF", "FHIR R4"],
    "total_entities": len(all_entities),
    "total_fields_documented": total_fields,
    "entities": all_entities,
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Build summary
summary = {
    "product": "CareCloud Prime",
    "source_document": "certification_b10_ehi_export_documentation.pdf",
    "total_entities": len(all_entities),
    "total_fields_documented": total_fields,
    "ccd_sections_count": len(ccd_entities),
    "ccd_fields_count": sum(e["field_count"] for e in ccd_entities),
    "pdf_sections_count": len(pdf_entities),
    "pdf_fields_documented": 0,
    "fhir_sections_count": 1,
    "fields_with_code_systems": sum(
        1 for e in all_entities for f in e.get("fields", []) if f.get("code_system")
    ),
    "fields_with_descriptions": 0,  # No field descriptions in the PDF
    "categories": {},
}

for e in all_entities:
    cat = e["category"]
    if cat not in summary["categories"]:
        summary["categories"][cat] = {"entity_count": 0, "field_count": 0, "entities": []}
    summary["categories"][cat]["entity_count"] += 1
    summary["categories"][cat]["field_count"] += e["field_count"]
    summary["categories"][cat]["entities"].append({
        "name": e["entity_name"],
        "field_count": e["field_count"],
        "format": e["format"],
    })

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total entities: {len(all_entities)}")
print(f"  C-CDA sections: {len(ccd_entities)}")
print(f"  PDF sections: {len(pdf_entities)}")
print(f"  FHIR: 1")
print(f"Total fields documented: {total_fields}")
print(f"Fields with code systems: {summary['fields_with_code_systems']}")
print(f"Fields with descriptions: 0")
print()
print("C-CDA Sections:")
for e in ccd_entities:
    print(f"  {e['entity_name']}: {e['field_count']} fields")
print()
print("PDF Sections (no field-level detail):")
for e in pdf_entities:
    print(f"  {e['entity_name']}")
print()
print(f"FHIR: {fhir_entity['entity_name']}")
