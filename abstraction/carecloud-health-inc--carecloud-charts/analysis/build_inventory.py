#!/usr/bin/env python3
"""
Manually curated CCD data dictionary and complete export inventory
for CareCloud Charts v3.0 §170.315(b)(10) EHI Export.

Source: ehi-export-documentation.pdf (11 pages, 457,681 bytes)
Author: Rico Lopez, Created: 2023-11-14
"""
import json

# CCD sections with their data elements, parsed from pages 6-10 of the PDF
ccd_sections = [
    {
        "section": "Patient Demographics/Information",
        "template_id": None,
        "elements": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "AdministrativeGender (2.16.840.1.113883.5.1)"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system": "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None},
        ]
    },
    {
        "section": "Provider's Name and Office Contact Information",
        "template_id": None,
        "elements": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None},
        ]
    },
    {
        "section": "Date and Location of Visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1:2015-08-01",
        "elements": [
            {"name": "Encounter Time", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None},
            {"name": "Encounter Address", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None},
        ]
    },
    {
        "section": "Chief Complaint and Reason for Visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.13:2014-06-09",
        "elements": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Encounters",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1:2015-08-01",
        "elements": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49:2015-08-01", "code_system": "CPT (2.16.840.1.113883.6.12)"},
            {"name": "Performer", "xpath": None, "code_system": None},
            {"name": "Diagnosis", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96) and ICD10 (2.16.840.1.113883.6.3)"},
            {"name": "Location", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Immunizations",
        "template_id": "2.16.840.1.113883.10.20.22.2.2.1:2015-08-01",
        "elements": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52:2015-08-01", "code_system": "CVX (2.16.840.1.113883.12.292) and CPT-4 (2.16.840.1.113883.6.12)"},
            {"name": "Date", "xpath": None, "code_system": None},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Route", "xpath": None, "code_system": "NCI Thesaurus (2.16.840.1.113883.3.26.1.1)"},
            {"name": "Site", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Manufacturer", "xpath": None, "code_system": None},
            {"name": "Dose", "xpath": None, "code_system": None},
            {"name": "Lot Number", "xpath": None, "code_system": None},
            {"name": "Notes", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Instructions",
        "template_id": "2.16.840.1.113883.10.20.22.2.45:2014-06-09",
        "elements": [
            {"name": "Patient Instructions/Follow-up Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20:2014-06-09", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section": "Treatment Plan",
        "template_id": "2.16.840.1.113883.10.20.22.2.10:2014-06-09",
        "elements": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44:2014-06-09", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40:2014-06-09 / 2.16.840.1.113883.10.20.22.4.39:2014-06-09 / 2.16.840.1.113883.10.20.22.4.121", "code_system": None},
        ]
    },
    {
        "section": "Social History",
        "template_id": "2.16.840.1.113883.10.20.22.2.17:2015-08-01",
        "elements": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78:2014-06-09", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Description", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Dates Observed", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Problems",
        "template_id": "2.16.840.1.113883.10.20.22.2.5.1:2015-08-01",
        "elements": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3:2015-08-01", "code_system": "SNOMED (2.16.840.1.113883.6.96) and ICD10 (2.16.840.1.113883.6.3)"},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Active date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Medications",
        "template_id": "2.16.840.1.113883.10.20.22.2.1.1:2014-06-09",
        "elements": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16:2014-06-09", "code_system": "RxNorm (2.16.840.1.113883.6.88) and NDC (2.16.840.1.113883.6.69)"},
            {"name": "Directions", "xpath": None, "code_system": None},
            {"name": "Start Date", "xpath": None, "code_system": None},
            {"name": "End Date", "xpath": None, "code_system": None},
            {"name": "Status", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Medication Allergies",
        "template_id": "2.16.840.1.113883.10.20.22.2.6.1:2015-08-01",
        "elements": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30:2015-08-01", "code_system": "RxNorm (2.16.840.1.113883.6.88)"},
            {"name": "Reaction", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Severity", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Status", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section": "Laboratory Tests",
        "template_id": None,
        "elements": [
            {"name": "Test Code", "xpath": None, "code_system": None},
            {"name": "Code System", "xpath": None, "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Name", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Laboratory Information",
        "template_id": None,
        "elements": [
            {"name": "Lab Name", "xpath": None, "code_system": None},
            {"name": "Lab Address", "xpath": None, "code_system": None},
            {"name": "Test Report Date", "xpath": None, "code_system": None},
            {"name": "Test Performed", "xpath": None, "code_system": None},
            {"name": "Specimen Source", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Laboratory Values/Results",
        "template_id": "2.16.840.1.113883.10.20.22.2.3.1:2015-08-01",
        "elements": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1:2015-08-01", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Result Value", "xpath": None, "code_system": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system": None},
            {"name": "Interpretation", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Vitals",
        "template_id": "2.16.840.1.113883.10.20.22.2.4.1:2015-08-01",
        "elements": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26:2015-08-01", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Observation Date/Time", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Goal",
        "template_id": "2.16.840.1.113883.10.20.22.2.60",
        "elements": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None},
            {"name": "Value", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Procedures",
        "template_id": "2.16.840.1.113883.10.20.22.2.7.1:2014-06-09",
        "elements": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14:2014-06-09", "code_system": "CPT-4 (2.16.840.1.113883.6.12) or SNOMED (2.16.840.1.113883.6.96) or HCPCS (2.16.840.1.113883.6.13)"},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Care Team Members",
        "template_id": "2.16.840.1.113883.10.20.22.2.500:2019-07-01",
        "elements": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500:2019-07-01", "code_system": None},
            {"name": "Specialty", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Reason for Referral",
        "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1:2014-06-09",
        "elements": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section": "Medical Equipment",
        "template_id": "2.16.840.1.113883.10.20.22.2.23:2014-06-09",
        "elements": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14:2014-06-09", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "GMDN PT Description", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Mental Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.56:2015-08-01",
        "elements": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74:2015-08-01", "code_system": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None},
            {"name": "Results", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Comments", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Functional Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.14:2014-06-09",
        "elements": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67:2014-06-09", "code_system": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None},
            {"name": "Results", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Comments", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Health Concern",
        "template_id": "2.16.840.1.113883.10.20.22.2.58:2015-08-01",
        "elements": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132:2015-08-01", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
]

# PDF exports described on page 11
pdf_exports = [
    {
        "name": "Patient Demographic/Insurance",
        "description": "Demographics and insurance details",
        "format": "PDF",
        "field_level_docs": False,
    },
    {
        "name": "Advance Directive",
        "description": "Advance directive information",
        "format": "PDF",
        "field_level_docs": False,
    },
    {
        "name": "Appointments",
        "description": "Patient appointments",
        "format": "PDF",
        "field_level_docs": False,
    },
    {
        "name": "Provider-to-Patient Messages",
        "description": "Secure messages",
        "format": "PDF",
        "field_level_docs": False,
    },
    {
        "name": "Billing Data (Claim)",
        "description": "Billing data including CPT, ICD, Modifier",
        "format": "PDF",
        "field_level_docs": False,
    },
    {
        "name": "Documents",
        "description": "Signed progress notes, lab results, radiology reports, scanned/uploaded documents",
        "format": "PDF",
        "field_level_docs": False,
    },
]

# FHIR export (mentioned briefly on page 11)
fhir_export = {
    "description": "Single-patient FHIR DocumentReference and FHIR Bulk Data EHI Export",
    "detail_level": "Single paragraph, no resource list or field documentation",
}

# Compute statistics
total_ccd_sections = len(ccd_sections)
total_ccd_elements = sum(len(s["elements"]) for s in ccd_sections)
elements_with_xpath = sum(1 for s in ccd_sections for e in s["elements"] if e["xpath"])
elements_with_code_system = sum(1 for s in ccd_sections for e in s["elements"] if e["code_system"])

# Code systems used
code_systems = set()
for s in ccd_sections:
    for e in s["elements"]:
        if e["code_system"]:
            # Extract individual code systems
            cs = e["code_system"]
            for part in cs.split(" and "):
                part = part.strip()
                if " or " in part:
                    for sub in part.split(" or "):
                        code_systems.add(sub.strip().split(" (")[0])
                else:
                    code_systems.add(part.split(" (")[0])

output = {
    "summary": {
        "total_ccd_sections": total_ccd_sections,
        "total_ccd_elements": total_ccd_elements,
        "elements_with_xpath": elements_with_xpath,
        "elements_with_code_system": elements_with_code_system,
        "pct_with_code_system": round(elements_with_code_system / total_ccd_elements * 100, 1),
        "code_systems_used": sorted(list(code_systems)),
        "pdf_export_categories": len(pdf_exports),
        "fhir_export": "Mentioned but undocumented",
    },
    "ccd_sections": ccd_sections,
    "pdf_exports": pdf_exports,
    "fhir_export": fhir_export,
}

# Print summary
print("=" * 70)
print("CareCloud Charts v3.0 - EHI Export Inventory")
print("=" * 70)
print(f"\nCCD DATA DICTIONARY (pages 6-10)")
print(f"  Sections:                {total_ccd_sections}")
print(f"  Total data elements:     {total_ccd_elements}")
print(f"  Elements with XPATH:     {elements_with_xpath}")
print(f"  Elements with code sys:  {elements_with_code_system} ({output['summary']['pct_with_code_system']}%)")
print(f"  Code systems referenced: {', '.join(sorted(code_systems))}")

print(f"\nCCD SECTIONS DETAIL:")
for s in ccd_sections:
    n = len(s["elements"])
    tid = f" [{s['template_id']}]" if s["template_id"] else ""
    print(f"  {s['section']}{tid}: {n} elements")
    for e in s["elements"]:
        cs = f" ({e['code_system']})" if e["code_system"] else ""
        print(f"    - {e['name']}{cs}")

print(f"\nPDF EXPORTS (page 11): {len(pdf_exports)} categories")
for p in pdf_exports:
    print(f"  - {p['name']}: {p['description']}")

print(f"\nFHIR EXPORT (page 11): {fhir_export['description']}")
print(f"  Detail: {fhir_export['detail_level']}")

# Save
with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/carecloud-health-inc--carecloud-charts/analysis/full-entity-inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved full inventory to full-entity-inventory.json")
