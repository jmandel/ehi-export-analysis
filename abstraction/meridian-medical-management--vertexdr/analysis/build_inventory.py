#!/usr/bin/env python3
"""
Manually-verified inventory of VertexDr EHI Export content.
Built by carefully reading the pdftotext output of the 11-page PDF.
Each C-CDA section and its fields are enumerated exactly as documented.
"""

import json

inventory = {
    "product": "VertexDr",
    "version": "9.1",
    "vendor": "Meridian Medical Management (CareCloud)",
    "chpl_id": "15.04.04.2112.Vert.09.01.1.221024",
    "chpl_number": 11002,
    "source_document": "VertexDr-b10-EHI-Export-Documentation.pdf",
    "source_pages": 11,
    "source_date": "2023-11-16",
    "export_mechanisms": [
        {
            "name": "CCD/C-CDA Export",
            "format": "XML (C-CDA R2.1)",
            "standard": "HL7 CDA R2 Consolidated CDA Templates for Clinical Notes (US Realm), DSTU R2.1, August 2015",
            "standard_ref": "§ 170.205(a)(4)",
            "single_patient": True,
            "single_patient_method": "File → Export CCD from patient chart; user selects sections",
            "bulk_patient": True,
            "bulk_patient_method": "File → Export CCD(s) for Patients; generates ZIP file with CCDA XML"
        },
        {
            "name": "PDF Exports (Non-Clinical)",
            "format": "PDF",
            "standard": None,
            "single_patient": True,
            "single_patient_method": "Via application's Reports section",
            "bulk_patient": False,
            "bulk_patient_method": None,
            "note": "Not machine-readable"
        },
        {
            "name": "FHIR Data Export",
            "format": "FHIR",
            "standard": "FHIR",
            "single_patient": True,
            "single_patient_method": "FHIR server creates single-patient FHIR resource Document Reference",
            "bulk_patient": True,
            "bulk_patient_method": "Supports FHIR Bulk Data EHI Export per § 170.315(b)(10)(ii)",
            "documentation_detail": "Single sentence only; no endpoint, auth, resource type, or format details"
        }
    ],
    "ccda_sections": [
        {
            "section_name": "Patient Demographics/Information",
            "template_oid": None,
            "template_version": None,
            "fields": [
                {"name": "Patient Name", "xpath": "patient/name", "code_system_oid": None, "code_system_name": None},
                {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system_oid": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
                {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system_oid": None, "code_system_name": None},
                {"name": "Race", "xpath": "patient/raceCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
                {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
                {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Provider's name and office contact information",
            "template_oid": None,
            "template_version": None,
            "fields": [
                {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system_oid": None, "code_system_name": None},
                {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system_oid": None, "code_system_name": None},
                {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Date and Location of visit",
            "template_oid": "2.16.840.1.113883.10.20.22.2.22.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system_oid": None, "code_system_name": None},
                {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Chief Complaint and Reason for visit",
            "template_oid": "2.16.840.1.113883.10.20.22.2.13",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Patient visit details/complaints", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Encounters",
            "template_oid": "2.16.840.1.113883.10.20.22.2.22.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
                {"name": "Performer", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Diagnosis", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
                {"name": "Location", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Immunizations",
            "template_oid": "2.16.840.1.113883.10.20.22.2.2.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", "code_system_oid": "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12", "code_system_name": "CVX and CPT-4"},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Route", "xpath": None, "code_system_oid": "2.16.840.1.113883.3.26.1.1", "code_system_name": "NCI Thesaurus"},
                {"name": "Site", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Manufacturer", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Dose", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Lot Number", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Notes", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Instructions",
            "template_oid": "2.16.840.1.113883.10.20.22.2.45",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Patient Instructions/FollowupReasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"}
            ]
        },
        {
            "section_name": "Treatment Plan",
            "template_oid": "2.16.840.1.113883.10.20.22.2.10",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40/39/121", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Social History",
            "template_oid": "2.16.840.1.113883.10.20.22.2.17",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Description", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Dates Observed", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Problems",
            "template_oid": "2.16.840.1.113883.10.20.22.2.5.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
                {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Active date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Medications",
            "template_oid": "2.16.840.1.113883.10.20.22.2.1.1",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
                {"name": "Directions", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Start Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "End Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Medication Allergies",
            "template_oid": "2.16.840.1.113883.10.20.22.2.6.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
                {"name": "Reaction", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Severity", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Status", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"}
            ]
        },
        {
            "section_name": "Laboratory Tests",
            "template_oid": None,
            "template_version": None,
            "fields": [
                {"name": "Test Code", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Code System", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Laboratory Information",
            "template_oid": None,
            "template_version": None,
            "fields": [
                {"name": "Lab Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Lab Address", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Test Report Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Test Performed", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Specimen Source", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Laboratory value(s)/result(s)",
            "template_oid": "2.16.840.1.113883.10.20.22.2.3.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Result Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Relevant Reference Range", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Interpretation", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Vitals",
            "template_oid": "2.16.840.1.113883.10.20.22.2.4.1",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Observation Date/Time", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Goal",
            "template_oid": "2.16.840.1.113883.10.20.22.2.60",
            "template_version": None,
            "fields": [
                {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
                {"name": "Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Procedures",
            "template_oid": "2.16.840.1.113883.10.20.22.2.7.1",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Care team member(s)",
            "template_oid": "2.16.840.1.113883.10.20.22.2.500",
            "template_version": "2019-07-01",
            "fields": [
                {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system_oid": None, "code_system_name": None},
                {"name": "Specialty", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Reason for Referral",
            "template_oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"}
            ]
        },
        {
            "section_name": "Medical Equipment",
            "template_oid": "2.16.840.1.113883.10.20.22.2.23",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "GMDN PT Description", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Mental Status",
            "template_oid": "2.16.840.1.113883.10.20.22.2.56",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system_oid": None, "code_system_name": None},
                {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Functional Status",
            "template_oid": "2.16.840.1.113883.10.20.22.2.14",
            "template_version": "2014-06-09",
            "fields": [
                {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system_oid": None, "code_system_name": None},
                {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Health Concern",
            "template_oid": "2.16.840.1.113883.10.20.22.2.58",
            "template_version": "2015-08-01",
            "fields": [
                {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        }
    ],
    "pdf_export_categories": [
        {
            "name": "Patient Demographic/Insurance",
            "format": "PDF",
            "description": "Comprehensive view of demographics and insurance details, structured for clarity and ease of access",
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "Advance Directive",
            "format": "PDF",
            "description": "Comprehensive view of Advance Directive, structured for clarity and ease of access",
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "Appointments",
            "format": "PDF",
            "description": "Comprehensive view of appointments, structured for clarity and ease of access",
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "Provider-to-Patient Messages",
            "format": "PDF",
            "description": "Comprehensive view of messages, structured for clarity and ease of access",
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "Billing Data (Claim)",
            "format": "PDF",
            "description": "Comprehensive view of billing data (CPT, ICD, Modifier), structured for clarity and ease of access. Accessible via Reports section.",
            "fields_documented": False,
            "field_count": None,
            "mentioned_fields": ["CPT", "ICD", "Modifier"]
        },
        {
            "name": "Documents",
            "format": "PDF",
            "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document in the patient's record",
            "fields_documented": False,
            "field_count": None,
            "document_types_mentioned": ["signed progress notes", "lab results", "radiology reports", "scanned/uploaded documents"]
        }
    ],
    "fhir_export": {
        "name": "FHIR Data Export",
        "description": "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii).",
        "documentation_level": "single_sentence",
        "endpoint_documented": False,
        "auth_documented": False,
        "resource_types_documented": False,
        "sample_data_provided": False
    }
}

# Calculate summary statistics
total_ccda_sections = len(inventory["ccda_sections"])
total_ccda_fields = sum(len(s["fields"]) for s in inventory["ccda_sections"])
fields_with_code_system = sum(
    1 for s in inventory["ccda_sections"]
    for f in s["fields"]
    if f.get("code_system_oid") or f.get("code_system_name")
)
fields_with_xpath = sum(
    1 for s in inventory["ccda_sections"]
    for f in s["fields"]
    if f.get("xpath")
)
total_pdf_categories = len(inventory["pdf_export_categories"])

inventory["summary_statistics"] = {
    "ccda_sections": total_ccda_sections,
    "ccda_fields_total": total_ccda_fields,
    "ccda_fields_with_code_system": fields_with_code_system,
    "ccda_fields_with_xpath": fields_with_xpath,
    "pdf_export_categories": total_pdf_categories,
    "pdf_fields_documented": 0,
    "total_documented_components": total_ccda_sections + total_pdf_categories + 1,
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "has_native_data_dictionary": False,
    "has_field_descriptions": False,
    "has_field_types": False,
    "has_relationships": False,
    "has_value_sets_enumerated": False,
    "code_systems_referenced": True
}

# Write output
OUTPUT = "full-entity-inventory.json"
with open(OUTPUT, 'w') as f:
    json.dump(inventory, f, indent=2)

# Print summary report
print("=" * 60)
print("VertexDr EHI Export Documentation - Summary")
print("=" * 60)
print(f"\nSource: {inventory['source_document']} ({inventory['source_pages']} pages)")
print(f"Date: {inventory['source_date']}")
print()
print("EXPORT MECHANISMS:")
for m in inventory["export_mechanisms"]:
    sp = "Yes" if m["single_patient"] else "No"
    bp = "Yes" if m["bulk_patient"] else "No"
    print(f"  {m['name']} ({m['format']}): single={sp}, bulk={bp}")
print()
print("C-CDA SECTIONS:")
print(f"  Total sections: {total_ccda_sections}")
print(f"  Total fields: {total_ccda_fields}")
print(f"  Fields with code system: {fields_with_code_system} ({100*fields_with_code_system//total_ccda_fields}%)")
print(f"  Fields with XPATH: {fields_with_xpath} ({100*fields_with_xpath//total_ccda_fields}%)")
print()
for s in inventory["ccda_sections"]:
    n_cs = sum(1 for f in s["fields"] if f.get("code_system_oid"))
    oid_tag = f" [{s['template_oid']}]" if s["template_oid"] else ""
    print(f"  {s['section_name']}{oid_tag}: {len(s['fields'])} fields ({n_cs} with code systems)")
print()
print("PDF EXPORT CATEGORIES (no field-level documentation):")
for cat in inventory["pdf_export_categories"]:
    print(f"  {cat['name']}")
print()
print("FHIR EXPORT:")
print(f"  Documentation: {inventory['fhir_export']['documentation_level']}")
print()
print("DOCUMENTATION QUALITY:")
print(f"  Field descriptions: No")
print(f"  Field types: No (code systems named but types not specified)")
print(f"  Relationships/FKs: No")
print(f"  Value sets enumerated: No (code systems named, not enumerated)")
print(f"  Sample data: No")
print(f"  Machine-readable schema: No")

with open("summary-stats.txt", 'w') as f:
    f.write(f"C-CDA Sections: {total_ccda_sections}\n")
    f.write(f"C-CDA Fields Total: {total_ccda_fields}\n")
    f.write(f"C-CDA Fields with Code Systems: {fields_with_code_system}\n")
    f.write(f"C-CDA Fields with XPATH: {fields_with_xpath}\n")
    f.write(f"PDF Export Categories: {total_pdf_categories}\n")
    f.write(f"PDF Fields Documented: 0\n")
    f.write(f"Total Components: {total_ccda_sections + total_pdf_categories + 1}\n")
