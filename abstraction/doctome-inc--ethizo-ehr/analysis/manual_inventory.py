#!/usr/bin/env python3
"""Manual inventory of the CDA data dictionary from ethizo EHI Export PDF.

Since the PDF layout makes automated parsing fragile, this script encodes
the manually-verified data elements from the pdftotext output and produces
structured counts.
"""

import json

# Manually verified from pdftotext -layout output of EHI-Export-b.10-Documentation-v2.pdf
# Each section with its OID (if any), data elements, and code systems

CDA_SECTIONS = [
    {
        "name": "Patient Demographics/Information",
        "oid": None,
        "elements": [
            "Patient Name",
            "Sex",
            "Date of Birth",
            "Race",
            "Ethnicity",
            "Preferred Language"
        ],
        "code_systems": ["AdministrativeGender", "CDC Race & Ethnicity"]
    },
    {
        "name": "Provider's name and office contact information",
        "oid": None,
        "elements": [
            "Performer (name)",
            "Performer (telecom)",
            "Performer (address)"
        ],
        "code_systems": []
    },
    {
        "name": "Date and Location of visit",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "elements": [
            "Encounter (effectiveTime)",
            "Encounter (address)"
        ],
        "code_systems": []
    },
    {
        "name": "Chief Complaint and Reason for visit",
        "oid": "2.16.840.1.113883.10.20.22.2.13",
        "elements": [
            "Patient visit details/complaints"
        ],
        "code_systems": []
    },
    {
        "name": "Encounters",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "elements": [
            "Encounter Code and Code Description",
            "Performer",
            "Diagnosis",
            "Location",
            "Date"
        ],
        "code_systems": ["CPT", "SNOMED", "ICD-10"]
    },
    {
        "name": "Immunizations",
        "oid": "2.16.840.1.113883.10.20.22.2.2.1",
        "elements": [
            "Vaccine",
            "Date",
            "Status",
            "Route",
            "Site",
            "Manufacturer",
            "Dose",
            "Lot Number",
            "Notes"
        ],
        "code_systems": ["CVX", "CPT-4", "NCI Thesaurus", "SNOMED"]
    },
    {
        "name": "Instructions",
        "oid": "2.16.840.1.113883.10.20.22.2.45",
        "elements": [
            "Patient Instructions/Followup Reasons"
        ],
        "code_systems": ["SNOMED"]
    },
    {
        "name": "Treatment Plan",
        "oid": "2.16.840.1.113883.10.20.22.2.10",
        "elements": [
            "Planned Observation",
            "Planned Date"
        ],
        "code_systems": ["LOINC"]
    },
    {
        "name": "Social History",
        "oid": "2.16.840.1.113883.10.20.22.2.17",
        "elements": [
            "Social History Observation",
            "Description",
            "Dates Observed"
        ],
        "code_systems": ["LOINC", "SNOMED"]
    },
    {
        "name": "Problems",
        "oid": "2.16.840.1.113883.10.20.22.2.5.1",
        "elements": [
            "Problem",
            "Status",
            "Active date"
        ],
        "code_systems": ["SNOMED", "ICD-10"]
    },
    {
        "name": "Medications",
        "oid": "2.16.840.1.113883.10.20.22.2.1.1",
        "elements": [
            "Medication",
            "Directions",
            "Start Date",
            "End Date",
            "Status"
        ],
        "code_systems": ["RxNorm", "NDC"]
    },
    {
        "name": "Medication Allergies",
        "oid": "2.16.840.1.113883.10.20.22.2.6.1",
        "elements": [
            "Substance",
            "Reaction",
            "Severity",
            "Status"
        ],
        "code_systems": ["RxNorm", "SNOMED"]
    },
    {
        "name": "Laboratory Tests",
        "oid": None,
        "elements": [
            "Test Code",
            "Code System",
            "Name",
            "Date"
        ],
        "code_systems": ["LOINC"]
    },
    {
        "name": "Laboratory Information",
        "oid": None,
        "elements": [
            "Lab Name",
            "Lab Address",
            "Test Report Date",
            "Test Performed",
            "Specimen Source"
        ],
        "code_systems": []
    },
    {
        "name": "Laboratory value(s)/result(s)",
        "oid": "2.16.840.1.113883.10.20.22.2.3.1",
        "elements": [
            "Result Type",
            "Result Value",
            "Relevant Reference Range",
            "Interpretation",
            "Date"
        ],
        "code_systems": ["LOINC"]
    },
    {
        "name": "Vitals",
        "oid": "2.16.840.1.113883.10.20.22.2.4.1",
        "elements": [
            "Observation",
            "Observation Date/Time"
        ],
        "code_systems": ["LOINC"]
    },
    {
        "name": "Goal",
        "oid": "2.16.840.1.113883.10.20.22.2.60",
        "elements": [
            "Goal",
            "Value",
            "Date"
        ],
        "code_systems": []
    },
    {
        "name": "Procedures",
        "oid": "2.16.840.1.113883.10.20.22.2.7.1",
        "elements": [
            "Procedure",
            "Date"
        ],
        "code_systems": ["CPT-4", "SNOMED", "HCPCS"]
    },
    {
        "name": "Care team member(s)",
        "oid": "2.16.840.1.113883.10.20.22.2.500",
        "elements": [
            "Care Giver Name",
            "Specialty",
            "Date"
        ],
        "code_systems": []
    },
    {
        "name": "Reason for Referral",
        "oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
        "elements": [
            "Reason for visit"
        ],
        "code_systems": ["SNOMED"]
    },
    {
        "name": "Medical Equipment",
        "oid": "2.16.840.1.113883.10.20.22.2.23",
        "elements": [
            "Implanted Device",
            "GMDN PT Description"
        ],
        "code_systems": ["SNOMED", "GMDN"]
    },
    {
        "name": "Mental Status",
        "oid": "2.16.840.1.113883.10.20.22.2.56",
        "elements": [
            "Assessment",
            "Assessment Date",
            "Results",
            "Comments"
        ],
        "code_systems": ["SNOMED"]
    },
    {
        "name": "Functional Status",
        "oid": "2.16.840.1.113883.10.20.22.2.14",
        "elements": [
            "Assessment",
            "Assessment Date",
            "Results",
            "Comments"
        ],
        "code_systems": ["SNOMED"]
    },
    {
        "name": "Health Concern",
        "oid": "2.16.840.1.113883.10.20.22.2.58",
        "elements": [
            "Concern / Observation",
            "Status",
            "Date"
        ],
        "code_systems": ["SNOMED"]
    }
]

NON_CDA_EXPORTS = [
    {
        "name": "Patient Demographics and Insurance Details",
        "format": "CSV",
        "field_documentation": False,
        "notes": "No field names, types, or value sets documented. PDF says only 'comprehensive view of demographics and insurance details.'"
    },
    {
        "name": "Appointments",
        "format": "CSV",
        "field_documentation": False,
        "notes": "Future appointments only. No field documentation. PDF says 'comprehensive view of all future appointments details.'"
    },
    {
        "name": "Documents",
        "format": "PDF/JPG/PNG",
        "field_documentation": False,
        "notes": "Scanned/uploaded documents organized by patient chart number folders and category subfolders."
    },
    {
        "name": "FHIR Bulk Data Export",
        "format": "FHIR",
        "field_documentation": False,
        "notes": "Single sentence mention at end of PDF. No endpoints, auth, or resource list documented."
    }
]

def main():
    total_elements = 0
    all_code_systems = set()
    sections_with_oid = 0
    
    for s in CDA_SECTIONS:
        total_elements += len(s["elements"])
        all_code_systems.update(s["code_systems"])
        if s["oid"]:
            sections_with_oid += 1

    print("=" * 70)
    print("CDA DATA DICTIONARY INVENTORY - ethizo EHR")
    print("=" * 70)
    print()
    print(f"Total CDA sections: {len(CDA_SECTIONS)}")
    print(f"  - With OID identifiers: {sections_with_oid}")
    print(f"  - Without OID: {len(CDA_SECTIONS) - sections_with_oid}")
    print(f"Total CDA data elements: {total_elements}")
    print(f"Unique code systems referenced: {len(all_code_systems)}")
    print(f"  Code systems: {', '.join(sorted(all_code_systems))}")
    print()
    
    print("SECTION DETAIL:")
    print("-" * 70)
    print(f"{'Section':<45} {'Elements':>8}  {'Code Systems'}")
    print("-" * 70)
    for s in CDA_SECTIONS:
        cs = ', '.join(s["code_systems"]) if s["code_systems"] else "(none)"
        print(f"{s['name']:<45} {len(s['elements']):>8}  {cs}")
    print("-" * 70)
    print(f"{'TOTAL':<45} {total_elements:>8}")
    print()
    
    print("NON-CDA EXPORT COMPONENTS:")
    print("-" * 70)
    for item in NON_CDA_EXPORTS:
        print(f"  {item['name']} [{item['format']}]")
        print(f"    Field documentation: {'Yes' if item['field_documentation'] else 'No'}")
        print(f"    Notes: {item['notes']}")
        print()
    
    # Export structure
    output = {
        "source_pdf": "EHI-Export-b.10-Documentation-v2.pdf",
        "source_pdf_pages": 9,
        "source_pdf_created": "2025-03-01",
        "cda_sections": CDA_SECTIONS,
        "non_cda_exports": NON_CDA_EXPORTS,
        "summary": {
            "total_cda_sections": len(CDA_SECTIONS),
            "total_cda_elements": total_elements,
            "sections_with_oid": sections_with_oid,
            "unique_code_systems": len(all_code_systems),
            "code_systems_list": sorted(all_code_systems),
            "export_components": 4,
            "export_component_names": [
                "CDA XML (clinical data)",
                "CSV (demographics/insurance)",
                "CSV (appointments)",
                "Documents (PDF/JPG/PNG)"
            ],
            "documented_field_count": total_elements,
            "undocumented_csv_components": 2,
            "fhir_documented": False
        }
    }
    
    outpath = "/home/jmandel/hobby/ehi-export-analysis/abstraction/doctome-inc--ethizo-ehr/analysis/cda_dictionary_analysis.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"JSON saved to {outpath}")

if __name__ == "__main__":
    main()
