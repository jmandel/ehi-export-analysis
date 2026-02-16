#!/usr/bin/env python3
"""Parse the ethizo EHI Export PDF data dictionary into structured JSON.

Reads pdftotext output and extracts:
- CDA sections with their template IDs
- Data elements with XPATH, code systems, and code system names
- Non-CDA export components (CSV, documents)
"""

import json
import re
import sys

def parse_pdf():
    import subprocess
    result = subprocess.run(
        ["pdftotext", "-layout", "../downloads/EHI-Export-b.10-Documentation-v2.pdf", "-"],
        capture_output=True, text=True
    )
    text = result.stdout

    entities = []

    # Parse CDA sections - each section header has a template ID in brackets
    # Format: "Section Name [templateID : date]"
    sections_raw = text.split("\n")

    current_section = None
    current_fields = []

    # Track all lines for the CDA data dictionary (pages 4-8)
    in_cda_table = False

    # Known sections from the PDF
    section_defs = [
        ("Patient Demographics/Information", None, "Demographics"),
        ("Provider's name and office contact information", None, "Provider"),
        ("Date and Location of visit", "2.16.840.1.113883.10.20.22.2.22.1", "Encounter"),
        ("Chief Complaint and Reason for visit", "2.16.840.1.113883.10.20.22.2.13", "Chief Complaint"),
        ("Encounters", "2.16.840.1.113883.10.20.22.2.22.1", "Encounter"),
        ("Immunizations", "2.16.840.1.113883.10.20.22.2.2.1", "Immunization"),
        ("Instructions", "2.16.840.1.113883.10.20.22.2.45", "Instructions"),
        ("Treatment Plan", "2.16.840.1.113883.10.20.22.2.10", "Treatment Plan"),
        ("Social History", "2.16.840.1.113883.10.20.22.2.17", "Social History"),
        ("Problems", "2.16.840.1.113883.10.20.22.2.5.1", "Problems"),
        ("Medications", "2.16.840.1.113883.10.20.22.2.1.1", "Medications"),
        ("Medication Allergies", "2.16.840.1.113883.10.20.22.2.6.1", "Allergies"),
        ("Laboratory Tests", None, "Laboratory"),
        ("Laboratory Information", None, "Laboratory"),
        ("Laboratory value(s)/result(s)", "2.16.840.1.113883.10.20.22.2.3.1", "Laboratory"),
        ("Vitals", "2.16.840.1.113883.10.20.22.2.4.1", "Vitals"),
        ("Goal", "2.16.840.1.113883.10.20.22.2.60", "Goals"),
        ("Procedures", "2.16.840.1.113883.10.20.22.2.7.1", "Procedures"),
        ("Care team member(s)", "2.16.840.1.113883.10.20.22.2.500", "Care Team"),
        ("Reason for Referral", "1.3.6.1.4.1.19376.1.5.3.1.3.1", "Referrals"),
        ("Medical Equipment", "2.16.840.1.113883.10.20.22.2.23", "Medical Equipment"),
        ("Mental Status", "2.16.840.1.113883.10.20.22.2.56", "Mental Status"),
        ("Functional Status", "2.16.840.1.113883.10.20.22.2.14", "Functional Status"),
        ("Health Concern", "2.16.840.1.113883.10.20.22.2.58", "Health Concerns"),
    ]

    # Build structured entities from manual parse of the PDF content
    # CDA Clinical Data entity
    cda_sections = []

    # Patient Demographics/Information
    cda_sections.append({
        "section": "Patient Demographics/Information",
        "template_id": None,
        "fields": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system_oid": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system_oid": None, "code_system_name": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Provider's name and office contact
    cda_sections.append({
        "section": "Provider's name and office contact information",
        "template_id": None,
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Date and Location of visit
    cda_sections.append({
        "section": "Date and Location of visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1",
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system_oid": None, "code_system_name": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Chief Complaint
    cda_sections.append({
        "section": "Chief Complaint and Reason for visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.13",
        "fields": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Encounters
    cda_sections.append({
        "section": "Encounters",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1",
        "fields": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "Performer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Diagnosis", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Location", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Immunizations
    cda_sections.append({
        "section": "Immunizations",
        "template_id": "2.16.840.1.113883.10.20.22.2.2.1",
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
    })

    # Instructions
    cda_sections.append({
        "section": "Instructions",
        "template_id": "2.16.840.1.113883.10.20.22.2.45",
        "fields": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    })

    # Treatment Plan
    cda_sections.append({
        "section": "Treatment Plan",
        "template_id": "2.16.840.1.113883.10.20.22.2.10",
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.39: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Social History
    cda_sections.append({
        "section": "Social History",
        "template_id": "2.16.840.1.113883.10.20.22.2.17",
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Description", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Dates Observed", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Problems
    cda_sections.append({
        "section": "Problems",
        "template_id": "2.16.840.1.113883.10.20.22.2.5.1",
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Active date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Medications
    cda_sections.append({
        "section": "Medications",
        "template_id": "2.16.840.1.113883.10.20.22.2.1.1",
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
            {"name": "Directions", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Start Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "End Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Medication Allergies
    cda_sections.append({
        "section": "Medication Allergies",
        "template_id": "2.16.840.1.113883.10.20.22.2.6.1",
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
            {"name": "Reaction", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Severity", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    })

    # Laboratory Tests
    cda_sections.append({
        "section": "Laboratory Tests",
        "template_id": None,
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Code System", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Laboratory Information
    cda_sections.append({
        "section": "Laboratory Information",
        "template_id": None,
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lab Address", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Report Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Performed", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Specimen Source", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Laboratory Results
    cda_sections.append({
        "section": "Laboratory value(s)/result(s)",
        "template_id": "2.16.840.1.113883.10.20.22.2.3.1",
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Result Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Interpretation", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Vitals
    cda_sections.append({
        "section": "Vitals",
        "template_id": "2.16.840.1.113883.10.20.22.2.4.1",
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Observation Date/Time", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Goal
    cda_sections.append({
        "section": "Goal",
        "template_id": "2.16.840.1.113883.10.20.22.2.60",
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
            {"name": "Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Procedures
    cda_sections.append({
        "section": "Procedures",
        "template_id": "2.16.840.1.113883.10.20.22.2.7.1",
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Care Team
    cda_sections.append({
        "section": "Care team member(s)",
        "template_id": "2.16.840.1.113883.10.20.22.2.500",
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system_oid": None, "code_system_name": None},
            {"name": "Specialty", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Reason for Referral
    cda_sections.append({
        "section": "Reason for Referral",
        "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
        "fields": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    })

    # Medical Equipment
    cda_sections.append({
        "section": "Medical Equipment",
        "template_id": "2.16.840.1.113883.10.20.22.2.23",
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "GMDN PT Description", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Mental Status
    cda_sections.append({
        "section": "Mental Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.56",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Functional Status
    cda_sections.append({
        "section": "Functional Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.14",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Health Concerns
    cda_sections.append({
        "section": "Health Concern",
        "template_id": "2.16.840.1.113883.10.20.22.2.58",
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    })

    # Build the full entity inventory
    entities = []

    # Entity 1: CDA Clinical Document
    cda_entity = {
        "entity_name": "CDA Clinical Document (CCD)",
        "format": "CDA XML (C-CDA R2.1)",
        "category": "Clinical Data",
        "standard": "HL7 CDA Release 2: C-CDA R2.1 (August 2015), §170.205(a)(4)",
        "sections": cda_sections,
        "total_fields": sum(len(s["fields"]) for s in cda_sections),
        "total_sections": len(cda_sections),
    }
    entities.append(cda_entity)

    # Entity 2: Demographics and Insurance CSV
    entities.append({
        "entity_name": "Patient Demographics and Insurance Details",
        "format": "CSV",
        "category": "Demographics / Insurance",
        "description": "Comprehensive view of demographics and insurance details, structured for clarity and ease of access.",
        "fields": [],
        "fields_documented": False,
        "note": "No field-level documentation provided in the PDF. Only format (CSV, comma-separated) is specified."
    })

    # Entity 3: Appointments CSV
    entities.append({
        "entity_name": "Appointments",
        "format": "CSV",
        "category": "Scheduling",
        "description": "Comprehensive view of all future appointments details, structured for clarity and ease of access.",
        "fields": [],
        "fields_documented": False,
        "note": "No field-level documentation provided. Only future appointments mentioned. No field names, types, or descriptions."
    })

    # Entity 4: Documents
    entities.append({
        "entity_name": "Scanned Documents",
        "format": "PDF, JPG, PNG",
        "category": "Documents",
        "description": "Signed progress notes, lab results, radiology reports, and other scanned or uploaded documents. Organized by patient chart number with category subfolders.",
        "fields": [
            {"name": "Document file", "description": "The actual document file (PDF/JPG/PNG)"},
            {"name": "Patient chart number folder", "description": "Top-level folder organizing by patient"},
            {"name": "Category subfolder", "description": "Category classification (e.g., Lab Reports, Radiology, Scanned Receipts)"},
        ],
        "fields_documented": True,
        "note": "Organizational structure documented but no metadata schema (e.g., document date, author, type codes) is specified."
    })

    # Entity 5: FHIR Bulk Data (mentioned but undocumented)
    entities.append({
        "entity_name": "FHIR Bulk Data Export",
        "format": "FHIR R4",
        "category": "Alternative Export Pathway",
        "description": "Single-patient FHIR DocumentReference and FHIR Bulk Data EHI Export for patient population per §170.315(b)(10)(ii).",
        "fields": [],
        "fields_documented": False,
        "note": "Mentioned in a single sentence at end of PDF. No documentation provided. FHIR API at fhir-api.ethizo.com shows standard US Core resources only — no EHI-specific extensions."
    })

    return entities


def compute_summary(entities):
    """Compute summary statistics from the entity inventory."""
    total_entities = len(entities)

    # Count CDA fields
    cda_entity = entities[0]
    cda_fields = cda_entity["total_fields"]
    cda_sections_count = cda_entity["total_sections"]

    # Count fields with code systems (as a proxy for "described")
    fields_with_codes = 0
    fields_with_xpath = 0
    total_cda_fields = 0
    for section in cda_entity["sections"]:
        for field in section["fields"]:
            total_cda_fields += 1
            if field.get("code_system_oid"):
                fields_with_codes += 1
            if field.get("xpath"):
                fields_with_xpath += 1

    # CSV entities have 0 documented fields
    csv_entities = [e for e in entities if e["format"] == "CSV"]
    doc_entity = entities[3]
    fhir_entity = entities[4]

    summary = {
        "total_export_components": total_entities,
        "cda_clinical_document": {
            "sections": cda_sections_count,
            "total_fields": total_cda_fields,
            "fields_with_xpath": fields_with_xpath,
            "fields_with_code_systems": fields_with_codes,
            "fields_without_code_systems": total_cda_fields - fields_with_codes,
            "code_systems_used": [
                "SNOMED CT (2.16.840.1.113883.6.96)",
                "ICD-10 (2.16.840.1.113883.6.3)",
                "LOINC (2.16.840.1.113883.6.1)",
                "RxNorm (2.16.840.1.113883.6.88)",
                "NDC (2.16.840.1.113883.6.69)",
                "CPT/CPT-4 (2.16.840.1.113883.6.12)",
                "CVX (2.16.840.1.113883.12.292)",
                "HCPCS (2.16.840.1.113883.6.13)",
                "GMDN",
                "AdministrativeGender (2.16.840.1.113883.5.1)",
                "Race & Ethnicity CDC (2.16.840.1.113883.6.238)",
                "NCI Thesaurus (2.16.840.1.113883.3.26.1.1)"
            ]
        },
        "csv_components": {
            "count": len(csv_entities),
            "fields_documented": 0,
            "note": "Neither CSV component has field-level documentation"
        },
        "document_export": {
            "formats": ["PDF", "JPG", "PNG"],
            "organization": "By patient chart number with category subfolders",
            "metadata_documented": False
        },
        "fhir_bulk_data": {
            "documented": False,
            "note": "Single sentence mention only; FHIR API shows standard US Core resources"
        },
        "overall_stats": {
            "total_documented_fields_cda": total_cda_fields,
            "total_documented_fields_csv": 0,
            "total_documented_fields_all": total_cda_fields,
            "fields_with_code_systems": fields_with_codes,
            "pct_fields_with_code_systems": round(fields_with_codes / total_cda_fields * 100, 1) if total_cda_fields > 0 else 0,
            "sample_data_provided": False,
            "machine_readable_schema": False,
        }
    }
    return summary


if __name__ == "__main__":
    entities = parse_pdf()

    # Save full inventory
    with open("entity-inventory-full.json", "w") as f:
        json.dump(entities, f, indent=2)
    print(f"Saved entity-inventory-full.json")

    # Save summary
    summary = compute_summary(entities)
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved entity-inventory-summary.json")

    # Print summary to stdout
    print(f"\n=== Summary ===")
    print(f"Export components: {summary['total_export_components']}")
    print(f"CDA sections: {summary['cda_clinical_document']['sections']}")
    print(f"CDA fields: {summary['cda_clinical_document']['total_fields']}")
    print(f"  with XPATH: {summary['cda_clinical_document']['fields_with_xpath']}")
    print(f"  with code systems: {summary['cda_clinical_document']['fields_with_code_systems']}")
    print(f"CSV documented fields: {summary['csv_components']['fields_documented']}")
    print(f"Code systems: {len(summary['cda_clinical_document']['code_systems_used'])}")
    print(f"Sample data: {summary['overall_stats']['sample_data_provided']}")
