#!/usr/bin/env python3
"""
Parse the ethizo EHR EHI Export PDF's CDA data dictionary into structured JSON.
The PDF contains a table mapping CCD sections to data elements, XPATH paths,
code systems (OIDs), and code system names. We also capture the CSV and
document export sections.

Output: full-entity-inventory.json
"""

import json
import re
import subprocess
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/doctome-inc--ethizo-ehr/downloads/EHI-Export-b.10-Documentation-v2.pdf"
OUT_PATH = "/home/jmandel/hobby/ehi-export-analysis/abstraction/doctome-inc--ethizo-ehr/analysis/full-entity-inventory.json"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Define the CCD sections we expect based on manual review
# Each section has a template ID (OID) and contains data elements
sections = []

# Parse sections from the PDF text
# Sections are identified by a header line like:
#   Patient Demographics/Information
#   Encounters [2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01]
section_pattern = re.compile(
    r'^([A-Z][A-Za-z\s/()&–\-]+?)(?:\s*\[(\d[\d.]+(?:\s*:\s*[\d-]+)?)\])?\s*$'
)

# We'll manually define the sections based on our reading of the PDF
# since the layout makes automated parsing unreliable

cda_sections = [
    {
        "section_name": "Patient Demographics/Information",
        "template_id": None,
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
        "section_name": "Provider's name and office contact information",
        "template_id": None,
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Date and Location of visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system_oid": None, "code_system_name": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Chief Complaint and Reason for visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.13 : 2014-06-09",
        "fields": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Encounters",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "fields": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "Performer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Diagnosis", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Location", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Immunizations",
        "template_id": "2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01",
        "fields": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", "code_system_oid": "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12", "code_system_name": "CVX and CPT-4"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Route", "xpath": None, "code_system_oid": "2.16.840.1.113883.3.26.1.1", "code_system_name": "National Cancer Institute (NCI) Thesaurus"},
            {"name": "Site", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Manufacturer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Dose", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lot Number", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Notes", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Instructions",
        "template_id": "2.16.840.1.113883.10.20.22.2.45 : 2014-06-09",
        "fields": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "section_name": "Treatment Plan",
        "template_id": "2.16.840.1.113883.10.20.22.2.10 : 2014-06-09",
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.39: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Social History",
        "template_id": "2.16.840.1.113883.10.20.22.2.17 : 2015-08-01",
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Description", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Dates Observed", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Problems",
        "template_id": "2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01",
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Active date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Medications",
        "template_id": "2.16.840.1.113883.10.20.22.2.1.1 : 2014-06-09",
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
            {"name": "Directions", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Start Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "End Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Medication Allergies",
        "template_id": "2.16.840.1.113883.10.20.22.2.6.1 : 2015-08-01",
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
            {"name": "Reaction", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Severity", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "section_name": "Laboratory Tests",
        "template_id": None,
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Code System", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Laboratory Information",
        "template_id": None,
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lab Address", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Report Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Performed", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Specimen Source", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Laboratory value(s)/result(s)",
        "template_id": "2.16.840.1.113883.10.20.22.2.3.1 : 2015-08-01",
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Result Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Interpretation", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Vitals",
        "template_id": "2.16.840.1.113883.10.20.22.2.4.1 : 2015-08-01",
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Observation Date/Time", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Goals",
        "template_id": "2.16.840.1.113883.10.20.22.2.60",
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
            {"name": "Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Procedures",
        "template_id": "2.16.840.1.113883.10.20.22.2.7.1 : 2014-06-09",
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Care team member(s)",
        "template_id": "2.16.840.1.113883.10.20.22.2.500 : 2019-07-01",
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system_oid": None, "code_system_name": None},
            {"name": "Specialty", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Reason for Referral",
        "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1 : 2014-06-09",
        "fields": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "section_name": "Medical Equipment (Implanted Devices)",
        "template_id": "2.16.840.1.113883.10.20.22.2.23 : 2014-06-09",
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "GMDN PT Description", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Mental Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.56 : 2015-08-01",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Functional Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.14 : 2014-06-09",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "section_name": "Health Concerns",
        "template_id": "2.16.840.1.113883.10.20.22.2.58 : 2015-08-01",
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
]

# Non-CDA export components
non_cda_components = [
    {
        "component_name": "Patient Demographics and Insurance Details",
        "format": "CSV",
        "description": "Comprehensive view of demographics and insurance details, structured for clarity and ease of access.",
        "fields_documented": False,
        "fields": []
    },
    {
        "component_name": "Appointments",
        "format": "CSV",
        "description": "Comprehensive view of all future appointments details, structured for clarity and ease of access.",
        "fields_documented": False,
        "fields": []
    },
    {
        "component_name": "Documents",
        "format": "PDF/JPG/PNG",
        "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document. Organized into patient chart number folders with category subfolders.",
        "fields_documented": False,
        "fields": []
    },
]

# Compute statistics
total_cda_sections = len(cda_sections)
total_cda_fields = sum(len(s["fields"]) for s in cda_sections)
fields_with_xpath = sum(1 for s in cda_sections for f in s["fields"] if f["xpath"])
fields_with_code_system = sum(1 for s in cda_sections for f in s["fields"] if f["code_system_oid"])
fields_with_template_id = sum(1 for s in cda_sections if s["template_id"])

inventory = {
    "product": "ethizo EHR",
    "developer": "DocToMe, Inc.",
    "source_document": "EHI-Export-b.10-Documentation-v2.pdf",
    "source_url": "https://www.ethizo.com/wp-content/uploads/2025/03/EHI-Export-b.10-Documentation-v2.pdf",
    "document_date": "2025-03-01",
    "document_pages": 9,
    "export_standard": "C-CDA R2.1 (HL7 CDA Release 2, August 2015) + CSV + Documents",
    "standard_reference": "§ 170.205(a)(4)",
    "export_mechanism": {
        "single_patient": "Share Data menu → select sections → Process → secure link via email/text → download ZIP",
        "bulk_population": "Quick Links → Share Data → EHI export for single or bulk → Process → secure link → download ZIP of ZIPs",
        "fhir_bulk_data": "Mentioned as alternative: FHIR DocumentReference (single) and FHIR Bulk Data (population). No detailed documentation provided."
    },
    "statistics": {
        "cda_sections": total_cda_sections,
        "total_cda_fields": total_cda_fields,
        "fields_with_xpath": fields_with_xpath,
        "fields_with_code_system": fields_with_code_system,
        "sections_with_template_id": fields_with_template_id,
        "non_cda_components": len(non_cda_components),
        "csv_fields_documented": 0,
    },
    "cda_data_dictionary": cda_sections,
    "non_cda_components": non_cda_components,
}

with open(OUT_PATH, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"CDA Sections: {total_cda_sections}")
print(f"Total CDA fields: {total_cda_fields}")
print(f"Fields with XPATH: {fields_with_xpath}")
print(f"Fields with code system: {fields_with_code_system}")
print(f"Sections with template ID: {fields_with_template_id}")
print(f"Non-CDA components: {len(non_cda_components)}")
print(f"\nSections breakdown:")
for s in cda_sections:
    n = len(s["fields"])
    coded = sum(1 for f in s["fields"] if f["code_system_oid"])
    print(f"  {s['section_name']}: {n} fields ({coded} with code systems)")
print(f"\nOutput written to: {OUT_PATH}")
