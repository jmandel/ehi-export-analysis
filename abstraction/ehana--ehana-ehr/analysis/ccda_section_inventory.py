#!/usr/bin/env python3
"""
Catalog the 18 C-CDA sections documented in the eHana EHI Export PDF.

Since the PDF is image-based (no extractable text), this inventory is
compiled from visual inspection of all 15 rendered pages (ehi_page-01.png
through ehi_page-15.png).

Each section entry records:
  - Section name (as labeled in the PDF)
  - Page number(s) where it appears
  - LOINC code (from XML element if visible)
  - C-CDA template OID (from XML element if visible)
  - Key data elements visible in the HTML/XML examples
  - Standard code systems referenced
  - Overview description (from the PDF)
"""

import json
import os

sections = [
    {
        "number": 1,
        "name": "Electronic Chart / Patient Data",
        "pages": [2, 3],
        "loinc_code": None,
        "template_oid": "2.16.840.1.113883.10.20.22.1.1",
        "overview": "Patient demographic data including name, DOB, gender, race, ethnicity, language, telecom, and address.",
        "key_data_elements": [
            "Patient name (given, family)",
            "Date of birth",
            "Gender (administrativeGenderCode)",
            "Race (raceCode, CDC Race/Ethnicity OID 2.16.840.1.113883.6.238)",
            "Ethnicity (ethnicGroupCode)",
            "Preferred language (languageCommunication)",
            "Telecom (phone, email)",
            "Address (street, city, state, zip, country)"
        ],
        "code_systems": ["HL7 AdministrativeGender", "CDC Race and Ethnicity (2.16.840.1.113883.6.238)"],
        "ccda_standard_section": "Demographics (recordTarget)"
    },
    {
        "number": 2,
        "name": "Vital Signs",
        "pages": [3, 4],
        "loinc_code": "8716-3",
        "template_oid": "2.16.840.1.113883.10.20.22.2.4.1",
        "overview": "Patient vital signs captured during encounters.",
        "key_data_elements": [
            "Vital sign type (LOINC coded)",
            "Value with units",
            "Effective time",
            "Author/organization"
        ],
        "code_systems": ["LOINC"],
        "ccda_standard_section": "Vital Signs"
    },
    {
        "number": 3,
        "name": "Immunization",
        "pages": [4],
        "loinc_code": "11369-6",
        "template_oid": "2.16.840.1.113883.10.20.22.2.2.1",
        "overview": "Immunization records for the patient.",
        "key_data_elements": [
            "Vaccine code (CVX)",
            "Manufacturer",
            "Lot number",
            "Administration date",
            "Route"
        ],
        "code_systems": ["CVX"],
        "ccda_standard_section": "Immunizations"
    },
    {
        "number": 4,
        "name": "Allergies, Adverse Reactions, Alerts",
        "pages": [5],
        "loinc_code": "48765-2",
        "template_oid": "2.16.840.1.113883.10.20.22.2.6.1",
        "overview": "Patient allergy and adverse reaction records.",
        "key_data_elements": [
            "Allergen substance (RxNorm/SNOMED coded)",
            "Reaction type",
            "Severity",
            "Status",
            "Onset date"
        ],
        "code_systems": ["SNOMED-CT", "RxNorm"],
        "ccda_standard_section": "Allergies and Adverse Reactions"
    },
    {
        "number": 5,
        "name": "History of Medication Use",
        "pages": [6],
        "loinc_code": "10160-0",
        "template_oid": "2.16.840.1.113883.10.20.22.2.1.1",
        "overview": "Prescribed and reported concurrent medications for the patient.",
        "key_data_elements": [
            "Medication name",
            "RxNorm/NDC code",
            "Start date",
            "End date",
            "Frequency/dose",
            "Instructions",
            "Status"
        ],
        "code_systems": ["RxNorm", "NDC"],
        "ccda_standard_section": "Medications"
    },
    {
        "number": 6,
        "name": "Instructions",
        "pages": [7],
        "loinc_code": "69730-0",
        "template_oid": "2.16.840.1.113883.10.20.22.2.45",
        "overview": "Clinician instructions provided to the patient during encounters.",
        "key_data_elements": [
            "Instruction text",
            "Date",
            "Author"
        ],
        "code_systems": ["LOINC"],
        "ccda_standard_section": "Instructions"
    },
    {
        "number": 7,
        "name": "Functional and Cognitive Status",
        "pages": [7, 8],
        "loinc_code": "47420-5",
        "template_oid": "2.16.840.1.113883.10.20.22.2.14",
        "overview": "Functional and cognitive status assessments for the patient.",
        "key_data_elements": [
            "Assessment type",
            "Status observation",
            "Effective date",
            "Value"
        ],
        "code_systems": ["SNOMED-CT", "LOINC"],
        "ccda_standard_section": "Functional Status"
    },
    {
        "number": 8,
        "name": "Chief Complaint / Reason For Visit",
        "pages": [8],
        "loinc_code": "46239-0",
        "template_oid": "2.16.840.1.113883.10.20.22.2.13",
        "overview": "Chief complaint or reason for the patient's visit.",
        "key_data_elements": [
            "Complaint/reason text",
            "Date"
        ],
        "code_systems": [],
        "ccda_standard_section": "Chief Complaint / Reason for Visit"
    },
    {
        "number": 9,
        "name": "Problem List",
        "pages": [9],
        "loinc_code": "11450-4",
        "template_oid": "2.16.840.1.113883.10.20.22.2.5.1",
        "overview": "Diagnoses captured during encounters.",
        "key_data_elements": [
            "Problem/diagnosis (SNOMED coded)",
            "Status",
            "Onset date",
            "Resolution date"
        ],
        "code_systems": ["SNOMED-CT"],
        "ccda_standard_section": "Problem List"
    },
    {
        "number": 10,
        "name": "Social History",
        "pages": [10],
        "loinc_code": "29762-2",
        "template_oid": "2.16.840.1.113883.10.20.22.2.17",
        "overview": "Social history including smoking status and birth gender.",
        "key_data_elements": [
            "Smoking status (SNOMED coded)",
            "Birth sex"
        ],
        "code_systems": ["SNOMED-CT"],
        "ccda_standard_section": "Social History"
    },
    {
        "number": 11,
        "name": "Encounters",
        "pages": [10],
        "loinc_code": "46240-8",
        "template_oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "overview": "Encounter records with associated problems.",
        "key_data_elements": [
            "Encounter type",
            "Date/time",
            "Provider",
            "Associated diagnoses",
            "Location"
        ],
        "code_systems": ["CPT"],
        "ccda_standard_section": "Encounters"
    },
    {
        "number": 12,
        "name": "Results",
        "pages": [10],
        "loinc_code": "30954-2",
        "template_oid": "2.16.840.1.113883.10.20.22.2.3.1",
        "overview": "Lab and diagnostic results for the patient.",
        "key_data_elements": [
            "Result type (LOINC coded)",
            "Value with units",
            "Reference range",
            "Date",
            "Interpretation"
        ],
        "code_systems": ["LOINC"],
        "ccda_standard_section": "Results"
    },
    {
        "number": 13,
        "name": "Procedures",
        "pages": [11],
        "loinc_code": "47519-4",
        "template_oid": "2.16.840.1.113883.10.20.22.4.14",
        "overview": "Scheduled and performed client procedures.",
        "key_data_elements": [
            "Procedure code (SNOMED coded)",
            "Display name",
            "Date performed",
            "Status",
            "Provider/organization"
        ],
        "code_systems": ["SNOMED-CT"],
        "ccda_standard_section": "Procedures"
    },
    {
        "number": 14,
        "name": "Reason for Referral",
        "pages": [11],
        "loinc_code": "42349-1",
        "template_oid": "2.16.840.1.113883.10.20.22.4.20",
        "overview": "Clinician's reported reason for referral.",
        "key_data_elements": [
            "Referral reason text",
            "Date",
            "Referred to",
            "Status"
        ],
        "code_systems": ["SNOMED-CT"],
        "ccda_standard_section": "Reason for Referral"
    },
    {
        "number": 15,
        "name": "Implantable Devices",
        "pages": [12],
        "loinc_code": None,
        "template_oid": "2.16.840.1.113883.10.20.22.4.14",
        "overview": "Clinician's reported reason for referral.",  # Note: overview text on page says this but section is Implantable Devices
        "key_data_elements": [
            "Device UDI",
            "Device name/description",
            "Assigning authority (FDA)",
            "Implant date"
        ],
        "code_systems": ["SNOMED-CT"],
        "ccda_standard_section": "Medical Equipment (Implantable Devices)"
    },
    {
        "number": 16,
        "name": "Health Concerns",
        "pages": [13],
        "loinc_code": "75310-3",
        "template_oid": "2.16.840.1.113883.10.20.22.2.58",
        "overview": "Clinician's documented concerns related to client's health.",
        "key_data_elements": [
            "Health concern text",
            "Date",
            "Author/organization"
        ],
        "code_systems": ["LOINC"],
        "ccda_standard_section": "Health Concerns"
    },
    {
        "number": 17,
        "name": "Assessment and Plan",
        "pages": [14],
        "loinc_code": "51847-2",
        "template_oid": "2.16.840.1.113883.10.20.22.2.9",
        "overview": "Assessment and plan of care for the client, as documented by the clinician during an encounter.",
        "key_data_elements": [
            "Assessment narrative text",
            "Plan items",
            "Date",
            "Author/organization"
        ],
        "code_systems": ["LOINC"],
        "ccda_standard_section": "Assessment and Plan"
    },
    {
        "number": 18,
        "name": "Goals",
        "pages": [15],
        "loinc_code": "61146-7",
        "template_oid": "2.16.840.1.113883.10.20.22.2.60",
        "overview": "Client's goals documented during an encounter.",
        "key_data_elements": [
            "Goal text",
            "Date",
            "Author/organization"
        ],
        "code_systems": ["LOINC"],
        "ccda_standard_section": "Goals"
    }
]

# Summary statistics
total_sections = len(sections)
total_data_elements = sum(len(s["key_data_elements"]) for s in sections)
code_systems_used = set()
for s in sections:
    code_systems_used.update(s["code_systems"])

print(f"=== eHana EHI Export: C-CDA Section Inventory ===")
print(f"Total sections: {total_sections}")
print(f"Total key data elements across all sections: {total_data_elements}")
print(f"Standard code systems referenced: {', '.join(sorted(code_systems_used))}")
print()

print("Section Summary:")
print(f"{'#':<4} {'Section Name':<45} {'Pages':<10} {'LOINC':<10} {'Data Elements'}")
print("-" * 100)
for s in sections:
    pages = ",".join(str(p) for p in s["pages"])
    loinc = s["loinc_code"] or "N/A"
    print(f"{s['number']:<4} {s['name']:<45} {pages:<10} {loinc:<10} {len(s['key_data_elements'])}")

print()
print(f"Total data elements: {total_data_elements}")

# Save full inventory as JSON
output_path = os.path.join(os.path.dirname(__file__), "ccda_section_inventory.json")
with open(output_path, "w") as f:
    json.dump({
        "summary": {
            "total_sections": total_sections,
            "total_data_elements": total_data_elements,
            "code_systems": sorted(code_systems_used),
            "format": "C-CDA R2 (CDA R2)",
            "source_artifact": "EHI_Export.pdf (15 pages, image-based)"
        },
        "sections": sections
    }, f, indent=2)

print(f"\nFull inventory saved to: {output_path}")
