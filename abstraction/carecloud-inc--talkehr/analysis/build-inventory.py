#!/usr/bin/env python3
"""Build clean entity inventory from the talkEHR b(10) PDF.

Based on manual verification of pdftotext output against the PDF structure.
The C-CDA mapping on pages 6-10 documents specific data elements per section.
Pages 11-12 document PDF and FHIR exports with minimal detail.
"""

import json

# Manually verified C-CDA sections and their fields from pages 6-10
ccda_sections = [
    {
        "section_name": "Patient Demographics/Information",
        "template_oid": None,
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system_oid": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system_oid": None, "code_system_name": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Provider's Name and Office Contact Information",
        "template_oid": None,
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Date and Location of Visit",
        "template_oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system_oid": None, "code_system_name": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Chief Complaint and Reason for Visit",
        "template_oid": "2.16.840.1.113883.10.20.22.2.13",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Patient Visit Details/Complaints", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Encounters",
        "template_oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Encounter Code and Description", "xpath": "2.16.840.1.113883.10.20.22.4.49", "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "Performer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Diagnosis", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Location", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Immunizations",
        "template_oid": "2.16.840.1.113883.10.20.22.2.2.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52", "code_system_oid": "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12", "code_system_name": "CVX and CPT-4"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Route", "xpath": None, "code_system_oid": "2.16.840.1.113883.3.26.1.1", "code_system_name": "NCI Thesaurus"},
            {"name": "Site", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Manufacturer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Dose", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lot Number", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Notes", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Instructions",
        "template_oid": "2.16.840.1.113883.10.20.22.2.45",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "section_name": "Treatment Plan",
        "template_oid": "2.16.840.1.113883.10.20.22.2.10",
        "export_format": "C-CDA R2.1 XML",
        "description": "Diagnostic tests pending, Future appointments, Referrals to other providers, Future scheduled tests, Recommended patient decision aids",
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40 / 2.16.840.1.113883.10.20.22.4.39 / 2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Social History",
        "template_oid": "2.16.840.1.113883.10.20.22.2.17",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Description", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Dates Observed", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Problems",
        "template_oid": "2.16.840.1.113883.10.20.22.2.5.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3", "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Active Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Medications",
        "template_oid": "2.16.840.1.113883.10.20.22.2.1.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16", "code_system_oid": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
            {"name": "Directions", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Start Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "End Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Medication Allergies",
        "template_oid": "2.16.840.1.113883.10.20.22.2.6.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30", "code_system_oid": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
            {"name": "Reaction", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Severity", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "section_name": "Laboratory Tests",
        "template_oid": None,
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Code System", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Laboratory Information",
        "template_oid": None,
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lab Address", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Report Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Performed", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Specimen Source", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Laboratory Values/Results",
        "template_oid": "2.16.840.1.113883.10.20.22.2.3.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Result Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Interpretation", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Vitals",
        "template_oid": "2.16.840.1.113883.10.20.22.2.4.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Observation Date/Time", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Goal",
        "template_oid": "2.16.840.1.113883.10.20.22.2.60",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
            {"name": "Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Procedures",
        "template_oid": "2.16.840.1.113883.10.20.22.2.7.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system_oid": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Care Team Members",
        "template_oid": "2.16.840.1.113883.10.20.22.2.500",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500", "code_system_oid": None, "code_system_name": None},
            {"name": "Specialty", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Reason for Referral",
        "template_oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Reason for Visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "section_name": "Medical Equipment",
        "template_oid": "2.16.840.1.113883.10.20.22.2.23",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "GMDN PT Description", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Mental Status",
        "template_oid": "2.16.840.1.113883.10.20.22.2.56",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Functional Status",
        "template_oid": "2.16.840.1.113883.10.20.22.2.14",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Health Concern",
        "template_oid": "2.16.840.1.113883.10.20.22.2.58",
        "export_format": "C-CDA R2.1 XML",
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
]

# PDF export categories from page 11
pdf_entities = [
    {
        "section_name": "Patient Demographic/Insurance (PDF)",
        "template_oid": None,
        "export_format": "PDF",
        "description": "Comprehensive view of demographics and insurance details",
        "fields": [
            {"name": "Demographics and insurance (unspecified fields)", "xpath": None,
             "code_system_oid": None, "code_system_name": None,
             "note": "No field-level detail provided in documentation"}
        ]
    },
    {
        "section_name": "Advance Directive (PDF)",
        "template_oid": None,
        "export_format": "PDF",
        "description": "Comprehensive view of Advance Directive",
        "fields": [
            {"name": "Advance Directive (unspecified fields)", "xpath": None,
             "code_system_oid": None, "code_system_name": None,
             "note": "No field-level detail provided in documentation"}
        ]
    },
    {
        "section_name": "Appointments (PDF)",
        "template_oid": None,
        "export_format": "PDF",
        "description": "Comprehensive view of appointments",
        "fields": [
            {"name": "Appointments (unspecified fields)", "xpath": None,
             "code_system_oid": None, "code_system_name": None,
             "note": "No field-level detail provided in documentation"}
        ]
    },
    {
        "section_name": "Provider-to-Patient Messages (PDF)",
        "template_oid": None,
        "export_format": "PDF",
        "description": "Comprehensive view of messages",
        "fields": [
            {"name": "Messages (unspecified fields)", "xpath": None,
             "code_system_oid": None, "code_system_name": None,
             "note": "No field-level detail provided in documentation"}
        ]
    },
    {
        "section_name": "Billing Data / Claims (PDF)",
        "template_oid": None,
        "export_format": "PDF",
        "description": "Comprehensive view of billing data (CPT, ICD, Modifier)",
        "fields": [
            {"name": "CPT codes", "xpath": None,
             "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "ICD codes", "xpath": None,
             "code_system_oid": "2.16.840.1.113883.6.3", "code_system_name": "ICD-10"},
            {"name": "Modifiers", "xpath": None,
             "code_system_oid": None, "code_system_name": None},
            {"name": "Other billing fields (unspecified)", "xpath": None,
             "code_system_oid": None, "code_system_name": None,
             "note": "No further field-level detail provided"}
        ]
    },
    {
        "section_name": "Documents (PDF)",
        "template_oid": None,
        "export_format": "PDF",
        "description": "Signed progress notes, lab results, radiology reports, scanned/uploaded documents",
        "fields": [
            {"name": "Progress notes", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lab results", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Radiology reports", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Scanned/uploaded documents", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
]

# FHIR export from page 12
fhir_entity = {
    "section_name": "FHIR Data Export",
    "template_oid": None,
    "export_format": "FHIR",
    "description": "Single-patient DocumentReference and FHIR Bulk Data EHI Export for patient population",
    "fields": [
        {"name": "DocumentReference", "xpath": None,
         "code_system_oid": None, "code_system_name": None,
         "note": "No technical detail provided beyond one-sentence mention"}
    ]
}

all_entities = ccda_sections + pdf_entities + [fhir_entity]

# Compute stats
total_entities = len(all_entities)
total_fields = sum(len(e["fields"]) for e in all_entities)

ccda_count = len(ccda_sections)
ccda_fields = sum(len(e["fields"]) for e in ccda_sections)
fields_with_xpath = sum(1 for e in all_entities for f in e["fields"] if f.get("xpath"))
fields_with_code_system = sum(1 for e in all_entities for f in e["fields"] if f.get("code_system_name"))

pdf_count = len(pdf_entities)
pdf_fields = sum(len(e["fields"]) for e in pdf_entities)

# Full inventory
inventory = {
    "source": "talkEHR-b10-EHI-Export-Documentation.pdf",
    "source_pages": "6-12",
    "extraction_method": "Manual verification from pdftotext output",
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_xpath": fields_with_xpath,
    "fields_with_code_system": fields_with_code_system,
    "entities": all_entities
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Summary
summary = {
    "total_entities": total_entities,
    "total_fields": total_fields,
    "by_format": {
        "C-CDA R2.1 XML": {
            "entity_count": ccda_count,
            "field_count": ccda_fields,
            "fields_with_xpath": fields_with_xpath,
            "fields_with_code_system": fields_with_code_system,
            "sections": [
                {
                    "name": s["section_name"],
                    "template_oid": s.get("template_oid"),
                    "field_count": len(s["fields"])
                }
                for s in ccda_sections
            ]
        },
        "PDF": {
            "entity_count": pdf_count,
            "field_count": pdf_fields,
            "categories": [s["section_name"] for s in pdf_entities],
            "documentation_quality": "Minimal - single sentence per category, no field-level detail"
        },
        "FHIR": {
            "entity_count": 1,
            "field_count": 1,
            "documentation_quality": "One sentence, no technical detail"
        }
    },
    "documentation_quality": {
        "ccda_sections_with_detailed_mapping": ccda_count,
        "pdf_sections_with_no_field_detail": pdf_count,
        "fhir_with_no_detail": 1,
        "sample_data_provided": False,
        "machine_readable_schema": False
    }
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"  C-CDA sections: {ccda_count} with {ccda_fields} fields")
print(f"    Fields with XPATH/template ref: {fields_with_xpath}")
print(f"    Fields with code system: {fields_with_code_system}")
print(f"  PDF export categories: {pdf_count} with {pdf_fields} fields")
print(f"  FHIR mention: 1 entity, 1 field")
print()
print("C-CDA Sections:")
for s in ccda_sections:
    oid = f" [{s['template_oid']}]" if s.get('template_oid') else ""
    print(f"  {s['section_name']}{oid}: {len(s['fields'])} fields")
