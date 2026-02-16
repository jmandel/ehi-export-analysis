#!/usr/bin/env python3
"""
Parse CareCloud Prime EHI Export Documentation PDF.
Extracts C-CDA data dictionary sections and non-clinical PDF export categories
into a structured full-entity-inventory.json.
"""

import json
import re
import sys

PDF_TEXT_FILE = "/tmp/carecloud-ehi.txt"

def parse_pdf_text():
    with open(PDF_TEXT_FILE, "r") as f:
        text = f.read()

    # Parse C-CDA sections from pages 6-10
    ccda_sections = []
    
    # Define all CDA sections with their template IDs (from the PDF)
    section_defs = [
        {
            "section_name": "Patient Demographics/Information",
            "template_id": None,
            "fields": [
                {"name": "Patient Name", "xpath": "patient/name", "code_system": None, "code_system_name": None},
                {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
                {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None, "code_system_name": None},
                {"name": "Race", "xpath": "patient/raceCode", "code_system": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
                {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
                {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Provider Information",
            "template_id": None,
            "fields": [
                {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None, "code_system_name": None},
                {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None, "code_system_name": None},
                {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Date and Location of Visit",
            "template_id": "2.16.840.1.113883.10.20.22.2.22.1",
            "fields": [
                {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None, "code_system_name": None},
                {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Chief Complaint and Reason for Visit",
            "template_id": "2.16.840.1.113883.10.20.22.2.13",
            "fields": [
                {"name": "Patient visit details/complaints", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Encounters",
            "template_id": "2.16.840.1.113883.10.20.22.2.22.1",
            "fields": [
                {"name": "Encounter Code and Description", "xpath": "2.16.840.1.113883.10.20.22.4.49", "code_system": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
                {"name": "Performer", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Diagnosis", "xpath": None, "code_system": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
                {"name": "Location", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Immunizations",
            "template_id": "2.16.840.1.113883.10.20.22.2.2.1",
            "fields": [
                {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52", "code_system": "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12", "code_system_name": "CVX and CPT-4"},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Route", "xpath": None, "code_system": "2.16.840.1.113883.3.26.1.1", "code_system_name": "NCI Thesaurus"},
                {"name": "Site", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Manufacturer", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Dose", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Lot Number", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Notes", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Instructions",
            "template_id": "2.16.840.1.113883.10.20.22.2.45",
            "fields": [
                {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            ]
        },
        {
            "section_name": "Treatment Plan",
            "template_id": "2.16.840.1.113883.10.20.22.2.10",
            "fields": [
                {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40 / 2.16.840.1.113883.10.20.22.4.39 / 2.16.840.1.113883.10.20.22.4.121", "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Social History",
            "template_id": "2.16.840.1.113883.10.20.22.2.17",
            "fields": [
                {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Description", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Dates Observed", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Problems",
            "template_id": "2.16.840.1.113883.10.20.22.2.5.1",
            "fields": [
                {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3", "code_system": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
                {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Active Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Medications",
            "template_id": "2.16.840.1.113883.10.20.22.2.1.1",
            "fields": [
                {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16", "code_system": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
                {"name": "Directions", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Start Date", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "End Date", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Medication Allergies",
            "template_id": "2.16.840.1.113883.10.20.22.2.6.1",
            "fields": [
                {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30", "code_system": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
                {"name": "Reaction", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Severity", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Status", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            ]
        },
        {
            "section_name": "Laboratory Tests",
            "template_id": None,
            "fields": [
                {"name": "Test Code", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Code System", "xpath": None, "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Name", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Laboratory Information",
            "template_id": None,
            "fields": [
                {"name": "Lab Name", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Lab Address", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Test Report Date", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Test Performed", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Specimen Source", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Laboratory Results",
            "template_id": "2.16.840.1.113883.10.20.22.2.3.1",
            "fields": [
                {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Result Value", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Relevant Reference Range", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Interpretation", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Vitals",
            "template_id": "2.16.840.1.113883.10.20.22.2.4.1",
            "fields": [
                {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Observation Date/Time", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Goals",
            "template_id": "2.16.840.1.113883.10.20.22.2.60",
            "fields": [
                {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None, "code_system_name": None},
                {"name": "Value", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Procedures",
            "template_id": "2.16.840.1.113883.10.20.22.2.7.1",
            "fields": [
                {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Care Team Members",
            "template_id": "2.16.840.1.113883.10.20.22.2.500",
            "fields": [
                {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500", "code_system": None, "code_system_name": None},
                {"name": "Specialty", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Reason for Referral",
            "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
            "fields": [
                {"name": "Reason for Visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            ]
        },
        {
            "section_name": "Medical Equipment / Implanted Devices",
            "template_id": "2.16.840.1.113883.10.20.22.2.23",
            "fields": [
                {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "GMDN PT Description", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Mental Status",
            "template_id": "2.16.840.1.113883.10.20.22.2.56",
            "fields": [
                {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74", "code_system": None, "code_system_name": None},
                {"name": "Assessment Date", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Results", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Comments", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Functional Status",
            "template_id": "2.16.840.1.113883.10.20.22.2.14",
            "fields": [
                {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67", "code_system": None, "code_system_name": None},
                {"name": "Assessment Date", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Results", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Comments", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
        {
            "section_name": "Health Concerns",
            "template_id": "2.16.840.1.113883.10.20.22.2.58",
            "fields": [
                {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            ]
        },
    ]

    # Non-clinical PDF exports (page 11)
    pdf_exports = [
        {
            "section_name": "Patient Demographic/Insurance (PDF)",
            "template_id": None,
            "export_format": "PDF",
            "description": "Comprehensive view of demographics and insurance details",
            "fields": [],
            "fields_documented": False,
        },
        {
            "section_name": "Advance Directive (PDF)",
            "template_id": None,
            "export_format": "PDF",
            "description": "Comprehensive view of Advance Directive",
            "fields": [],
            "fields_documented": False,
        },
        {
            "section_name": "Appointments (PDF)",
            "template_id": None,
            "export_format": "PDF",
            "description": "Comprehensive view of appointments",
            "fields": [],
            "fields_documented": False,
        },
        {
            "section_name": "Provider-to-Patient Messages (PDF)",
            "template_id": None,
            "export_format": "PDF",
            "description": "Comprehensive view of messages",
            "fields": [],
            "fields_documented": False,
        },
        {
            "section_name": "Billing Data / Claims (PDF)",
            "template_id": None,
            "export_format": "PDF",
            "description": "Comprehensive view of billing data (CPT, ICD, Modifier)",
            "fields": [
                {"name": "CPT", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "ICD", "xpath": None, "code_system": None, "code_system_name": None},
                {"name": "Modifier", "xpath": None, "code_system": None, "code_system_name": None},
            ],
            "fields_documented": False,  # only names, no types/descriptions
        },
        {
            "section_name": "Documents (PDF)",
            "template_id": None,
            "export_format": "PDF",
            "description": "Signed progress notes, available lab results, radiology reports, and scanned/uploaded documents",
            "fields": [],
            "fields_documented": False,
        },
    ]

    # FHIR export (page 12) - essentially undocumented
    fhir_export = {
        "section_name": "FHIR Data Export",
        "template_id": None,
        "export_format": "FHIR",
        "description": "Single-patient FHIR resource Document Reference and FHIR Bulk Data EHI Export for patient population",
        "fields": [],
        "fields_documented": False,
        "note": "Single sentence in documentation; no resource list, endpoint, or profile info provided"
    }

    # Build full inventory
    inventory = {
        "source_file": "certification_b10_ehi_export_documentation.pdf",
        "source_pages": 12,
        "source_created": "2024-09-12",
        "source_author": "JAHANZAIB NISAR",
        "source_tool": "Microsoft Word 2016",
        "export_standard": "HL7 CDA R2 C-CDA 2.1 (August 2015) for clinical; PDF for non-clinical; FHIR mentioned but undocumented",
        "sections": {
            "ccda_clinical": [],
            "pdf_nonclinical": [],
            "fhir": None,
        },
        "summary": {}
    }

    # Process C-CDA sections
    total_ccda_fields = 0
    fields_with_code_system = 0
    fields_with_xpath = 0
    for sec in section_defs:
        section_entry = {
            "name": sec["section_name"],
            "template_id": sec["template_id"],
            "export_format": "C-CDA XML",
            "field_count": len(sec["fields"]),
            "fields": sec["fields"],
        }
        total_ccda_fields += len(sec["fields"])
        for f in sec["fields"]:
            if f.get("code_system"):
                fields_with_code_system += 1
            if f.get("xpath"):
                fields_with_xpath += 1
        inventory["sections"]["ccda_clinical"].append(section_entry)

    # Process PDF exports
    total_pdf_fields = 0
    for exp in pdf_exports:
        section_entry = {
            "name": exp["section_name"],
            "template_id": None,
            "export_format": "PDF",
            "description": exp["description"],
            "field_count": len(exp["fields"]),
            "fields": exp["fields"],
            "fields_documented": exp["fields_documented"],
        }
        total_pdf_fields += len(exp["fields"])
        inventory["sections"]["pdf_nonclinical"].append(section_entry)

    # FHIR
    inventory["sections"]["fhir"] = fhir_export

    # Summary stats
    total_sections = len(section_defs) + len(pdf_exports) + 1  # +1 for FHIR
    total_fields = total_ccda_fields + total_pdf_fields  # FHIR has 0 documented fields
    inventory["summary"] = {
        "total_sections": total_sections,
        "ccda_section_count": len(section_defs),
        "pdf_export_count": len(pdf_exports),
        "fhir_mentioned": True,
        "fhir_documented": False,
        "total_ccda_fields": total_ccda_fields,
        "total_pdf_fields": total_pdf_fields,
        "total_fields_documented": total_fields,
        "ccda_fields_with_code_system": fields_with_code_system,
        "ccda_fields_with_xpath": fields_with_xpath,
        "ccda_fields_with_description": 0,  # No descriptive text for any field
        "has_sample_data": False,
        "has_machine_readable_schema": False,
        "has_relationships_documented": False,
        "has_value_sets_enumerated": False,
        "pdf_sections_with_field_detail": 0,
        "pdf_sections_without_field_detail": len(pdf_exports),
    }

    return inventory


def print_summary(inventory):
    s = inventory["summary"]
    print("=" * 60)
    print("CareCloud Prime EHI Export Documentation Summary")
    print("=" * 60)
    print(f"Source: {inventory['source_file']} ({inventory['source_pages']} pages)")
    print(f"Created: {inventory['source_created']} by {inventory['source_author']}")
    print()
    print(f"Total sections/entities: {s['total_sections']}")
    print(f"  C-CDA clinical sections: {s['ccda_section_count']}")
    print(f"  PDF non-clinical exports: {s['pdf_export_count']}")
    print(f"  FHIR export: mentioned={s['fhir_mentioned']}, documented={s['fhir_documented']}")
    print()
    print(f"Total fields documented: {s['total_fields_documented']}")
    print(f"  C-CDA fields: {s['total_ccda_fields']}")
    print(f"    With XPATH/entry reference: {s['ccda_fields_with_xpath']}")
    print(f"    With code system: {s['ccda_fields_with_code_system']}")
    print(f"    With descriptive text: {s['ccda_fields_with_description']}")
    print(f"  PDF export fields (names only): {s['total_pdf_fields']}")
    print()
    print(f"PDF exports with field-level detail: {s['pdf_sections_with_field_detail']}/{s['pdf_export_count']}")
    print(f"Sample data provided: {s['has_sample_data']}")
    print(f"Machine-readable schema: {s['has_machine_readable_schema']}")
    print(f"Relationships documented: {s['has_relationships_documented']}")
    print(f"Value sets enumerated: {s['has_value_sets_enumerated']}")
    print()
    print("C-CDA Sections:")
    print("-" * 60)
    for sec in inventory["sections"]["ccda_clinical"]:
        print(f"  {sec['name']}: {sec['field_count']} fields" +
              (f" (template: {sec['template_id']})" if sec['template_id'] else ""))
    print()
    print("PDF Non-Clinical Exports:")
    print("-" * 60)
    for sec in inventory["sections"]["pdf_nonclinical"]:
        detail = f", {sec['field_count']} field names" if sec['field_count'] > 0 else ", no fields documented"
        print(f"  {sec['name']}: {sec['description']}{detail}")
    print()
    print("FHIR Export:")
    print("-" * 60)
    fhir = inventory["sections"]["fhir"]
    print(f"  {fhir['description']}")
    print(f"  NOTE: {fhir['note']}")


if __name__ == "__main__":
    inventory = parse_pdf_text()
    
    # Save full inventory
    out_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/carecloud-inc--carecloud-prime/analysis/full-entity-inventory.json"
    with open(out_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved full inventory to {out_path}")
    print()
    
    # Print summary
    print_summary(inventory)
    
    # Save summary text
    import io
    buf = io.StringIO()
    import contextlib
    with contextlib.redirect_stdout(buf):
        print_summary(inventory)
    summary_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/carecloud-inc--carecloud-prime/analysis/summary-stats.txt"
    with open(summary_path, "w") as f:
        f.write(buf.getvalue())
    print(f"\nSaved summary to {summary_path}")
