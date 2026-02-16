#!/usr/bin/env python3
"""
Build a verified, complete entity inventory for the talkEHR EHI export documentation.

The PDF contains:
- Pages 6-10: CCD output format tables listing data elements with XPATHs and code systems
- Page 11: PDF export categories (6 categories, no field-level detail)
- Page 12: One-sentence FHIR mention

This script constructs the inventory from a manually verified parse of the
pdftotext output, ensuring accuracy over automated extraction. Every section
and field has been verified against the raw PDF text.
"""
import json

def build_inventory():
    """Build the complete entity inventory from verified PDF content."""
    
    sections = [
        {
            "section_name": "Patient Demographics/Information",
            "template_id": None,
            "format": "C-CDA XML",
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
            "template_id": None,
            "format": "C-CDA XML",
            "fields": [
                {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system_oid": None, "code_system_name": None},
                {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system_oid": None, "code_system_name": None},
                {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Date and Location of visit",
            "template_id": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Encounter Date/Time", "xpath": "entry/encounter/effectiveTime/@value", "code_system_oid": None, "code_system_name": None},
                {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Chief Complaint and Reason for Visit",
            "template_id": "2.16.840.1.113883.10.20.22.2.13 : 2014-06-09",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Patient visit details/complaints", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Encounters",
            "template_id": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Encounter Code and Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
                {"name": "Performer", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Diagnosis", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
                {"name": "Location", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Immunizations",
            "template_id": "2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01",
            "format": "C-CDA XML",
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
            "template_id": "2.16.840.1.113883.10.20.22.2.45 : 2014-06-09",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"}
            ]
        },
        {
            "section_name": "Treatment Plan",
            "template_id": "2.16.840.1.113883.10.20.22.2.10 : 2014-06-09",
            "format": "C-CDA XML",
            "description": "Diagnostic tests pending, Future appointments, Referrals to other providers, Future scheduled tests, Recommended patient decision aids",
            "fields": [
                {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.39: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Social History",
            "template_id": "2.16.840.1.113883.10.20.22.2.17 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Description", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Dates Observed", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Problems",
            "template_id": "2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
                {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Active date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Medications",
            "template_id": "2.16.840.1.113883.10.20.22.2.1.1 : 2014-06-09",
            "format": "C-CDA XML",
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
            "template_id": "2.16.840.1.113883.10.20.22.2.6.1 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
                {"name": "Reaction", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Severity", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Status", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"}
            ]
        },
        {
            "section_name": "Laboratory Tests",
            "template_id": None,
            "format": "C-CDA XML",
            "fields": [
                {"name": "Test Code", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Code System", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Laboratory Information",
            "template_id": None,
            "format": "C-CDA XML",
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
            "template_id": "2.16.840.1.113883.10.20.22.2.3.1 : 2015-08-01",
            "format": "C-CDA XML",
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
            "template_id": "2.16.840.1.113883.10.20.22.2.4.1 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
                {"name": "Observation Date/Time", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Goal",
            "template_id": "2.16.840.1.113883.10.20.22.2.60",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
                {"name": "Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Procedures",
            "template_id": "2.16.840.1.113883.10.20.22.2.7.1 : 2014-06-09",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Care team member(s)",
            "template_id": "2.16.840.1.113883.10.20.22.2.500 : 2019-07-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system_oid": None, "code_system_name": None},
                {"name": "Specialty", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Reason for Referral",
            "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1 : 2014-06-09",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"}
            ]
        },
        {
            "section_name": "Medical Equipment",
            "template_id": "2.16.840.1.113883.10.20.22.2.23 : 2014-06-09",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "GMDN PT Description", "xpath": None, "code_system_oid": None, "code_system_name": "GMDN"}
            ]
        },
        {
            "section_name": "Mental Status",
            "template_id": "2.16.840.1.113883.10.20.22.2.56 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system_oid": None, "code_system_name": None},
                {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Functional Status",
            "template_id": "2.16.840.1.113883.10.20.22.2.14 : 2014-06-09",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system_oid": None, "code_system_name": None},
                {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        {
            "section_name": "Health Concern",
            "template_id": "2.16.840.1.113883.10.20.22.2.58 : 2015-08-01",
            "format": "C-CDA XML",
            "fields": [
                {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
                {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
                {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None}
            ]
        },
        # PDF export sections (page 11)
        {
            "section_name": "Patient Demographic/Insurance",
            "template_id": None,
            "format": "PDF",
            "description": "A comprehensive view of demographics and insurance details, structured for clarity and ease of access",
            "fields_documented": False,
            "fields": []
        },
        {
            "section_name": "Advance Directive",
            "template_id": None,
            "format": "PDF",
            "description": "A comprehensive view of Advance Directive, structured for clarity and ease of access",
            "fields_documented": False,
            "fields": []
        },
        {
            "section_name": "Appointments",
            "template_id": None,
            "format": "PDF",
            "description": "A comprehensive view of appointments, structured for clarity and ease of access",
            "fields_documented": False,
            "fields": []
        },
        {
            "section_name": "Provider-to-Patient Messages",
            "template_id": None,
            "format": "PDF",
            "description": "A comprehensive view of messages, structured for clarity and ease of access",
            "fields_documented": False,
            "fields": []
        },
        {
            "section_name": "Billing Data (Claim)",
            "template_id": None,
            "format": "PDF",
            "description": "A comprehensive view of billing data (CPT, ICD, Modifier), structured for clarity and ease of access",
            "fields_documented": False,
            "fields": []
        },
        {
            "section_name": "Documents",
            "template_id": None,
            "format": "PDF",
            "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document in the patient's record",
            "fields_documented": False,
            "fields": []
        },
        # FHIR export (page 12) 
        {
            "section_name": "FHIR Data Export",
            "template_id": None,
            "format": "FHIR",
            "description": "talkEHR FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii). No further technical details provided.",
            "fields_documented": False,
            "fields": []
        }
    ]
    
    # Compute statistics
    ccda_sections = [s for s in sections if s["format"] == "C-CDA XML"]
    pdf_sections = [s for s in sections if s["format"] == "PDF"]
    fhir_sections = [s for s in sections if s["format"] == "FHIR"]
    
    total_ccda_fields = sum(len(s["fields"]) for s in ccda_sections)
    
    fields_with_code_system = 0
    fields_with_xpath = 0
    for s in ccda_sections:
        for f in s["fields"]:
            if f.get("code_system_oid") or f.get("code_system_name"):
                fields_with_code_system += 1
            if f.get("xpath"):
                fields_with_xpath += 1
    
    stats = {
        "total_sections": len(sections),
        "ccda_sections": len(ccda_sections),
        "ccda_fields_total": total_ccda_fields,
        "ccda_fields_with_code_systems": fields_with_code_system,
        "ccda_fields_with_xpaths": fields_with_xpath,
        "ccda_fields_without_any_code_or_xpath": total_ccda_fields - max(fields_with_code_system, fields_with_xpath),
        "pdf_export_sections": len(pdf_sections),
        "pdf_export_field_level_documentation": False,
        "fhir_sections": len(fhir_sections),
        "fhir_field_level_documentation": False,
        "sample_data_provided": False,
        "machine_readable_schema_provided": False,
        "code_systems_referenced": [
            "AdministrativeGender (2.16.840.1.113883.5.1)",
            "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)",
            "CPT (2.16.840.1.113883.6.12)",
            "SNOMED (2.16.840.1.113883.6.96)",
            "ICD-10 (2.16.840.1.113883.6.3)",
            "CVX (2.16.840.1.113883.12.292)",
            "CPT-4 (2.16.840.1.113883.6.12)",
            "NCI Thesaurus (2.16.840.1.113883.3.26.1.1)",
            "LOINC (2.16.840.1.113883.6.1)",
            "RxNorm (2.16.840.1.113883.6.88)",
            "NDC (2.16.840.1.113883.6.69)",
            "HCPCS (2.16.840.1.113883.6.13)",
            "GMDN"
        ]
    }
    
    inventory = {
        "product": "talkEHR",
        "vendor": "CareCloud, Inc.",
        "source_document": "talkEHR-b10-EHI-Export-Documentation.pdf",
        "document_version": "V1.0",
        "document_date": "2023-11-14",
        "document_pages": 12,
        "export_formats": [
            "C-CDA R2.1 XML (clinical data)",
            "PDF (demographics, insurance, appointments, billing, messages, documents)",
            "FHIR (mentioned on page 12, no details)"
        ],
        "export_mechanisms": {
            "single_patient_ccda": "CCDA Report > CCDA Export tab > select patient > Generate > Download XML",
            "bulk_patient_ccda": "CCDA Report > Data Portability tab > select date range > Export (downloads ZIP of XML files)",
            "pdf_exports": "Application's 'Reports' section",
            "fhir": "Mentioned but no endpoint/mechanism documented"
        },
        "statistics": stats,
        "sections": sections
    }
    
    return inventory


def main():
    inventory = build_inventory()
    
    out_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/carecloud-inc--talkehr/analysis/full-entity-inventory.json"
    with open(out_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    stats = inventory["statistics"]
    
    print("=== talkEHR EHI Export Inventory (Verified) ===")
    print(f"Total sections: {stats['total_sections']}")
    print(f"  C-CDA sections: {stats['ccda_sections']} ({stats['ccda_fields_total']} fields)")
    print(f"    Fields with code systems: {stats['ccda_fields_with_code_systems']}")
    print(f"    Fields with XPATHs: {stats['ccda_fields_with_xpaths']}")
    print(f"    Fields without code or xpath: {stats['ccda_fields_without_any_code_or_xpath']}")
    print(f"  PDF export sections: {stats['pdf_export_sections']} (0 fields documented)")
    print(f"  FHIR sections: {stats['fhir_sections']} (0 fields documented)")
    print(f"\nCode systems referenced: {len(stats['code_systems_referenced'])}")
    print(f"Sample data: {stats['sample_data_provided']}")
    print(f"Machine-readable schema: {stats['machine_readable_schema_provided']}")
    
    print("\n=== Section Summary ===")
    for s in inventory["sections"]:
        fmt = s["format"]
        name = s["section_name"]
        n_fields = len(s["fields"])
        if fmt == "C-CDA XML":
            print(f"  [{fmt}] {name}: {n_fields} fields")
        else:
            desc = s.get("description", "")[:60]
            print(f"  [{fmt}] {name}: {desc}...")
    
    print(f"\nInventory written to: {out_path}")


if __name__ == "__main__":
    main()
