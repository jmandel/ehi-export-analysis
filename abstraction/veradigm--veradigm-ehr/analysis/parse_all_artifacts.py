#!/usr/bin/env python3
"""
Parse all Veradigm EHI export documentation artifacts and produce:
  - entity-inventory-full.json: complete structured extraction of every entity/field
  - entity-inventory-summary.json: aggregate statistics and category breakdowns

Inputs:
  - ../downloads/VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf (via pdftotext)
  - ../downloads/VeradigmePrescribe_EHI_Export_Documentation_v1.pdf (via pdftotext)
  - ../downloads/EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf (via pdftotext)
  - ../downloads/VeradigmFMH_EHI_Export_Data_Guide_v2.pdf (via pdftotext)
  - ../downloads/veradigm-view-v6/*.html
  - ../downloads/fmh-fhir-extensions/*.json
"""

import json
import re
import os
import subprocess
from pathlib import Path
from html.parser import HTMLParser

BASE = Path(__file__).parent.parent
DOWNLOADS = BASE / "downloads"
ANALYSIS = BASE / "analysis"


# ============================================================
# 1. Parse Veradigm EHR PDF
# ============================================================

def parse_ehr_pdf():
    """Parse the 89-page EHR EHI Export PDF data dictionary."""
    txt_path = ANALYSIS / "ehr-export-text.txt"
    if not txt_path.exists():
        subprocess.run([
            "pdftotext", "-layout",
            str(DOWNLOADS / "VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf"),
            str(txt_path)
        ], check=True)

    text = txt_path.read_text(encoding="utf-8")
    # Remove form feed characters that break line-start matching
    text = text.replace('\x0c', '\n')

    entities = []
    # The PDF has sections like:
    # Filename: Demographics.json
    # Description: ...
    # EHR internal database table name: DEMOGRAPHICS
    # Primary key: PatientID
    # Field Definitions
    #  Field name    Description    Type of value

    # Split by "Filename:" markers
    # Require Description on next line to skip ToC entries
    filename_pattern = re.compile(
        r'Filename:\s+(\S+\.json)\s*\n'
        r'Description:\s*(.*?)(?=\nEHR internal database table name:)'
        r'\nEHR internal database table name:\s*(\S+)\s*\n'
        r'Primary key:\s*(\S+)',
        re.DOTALL
    )

    # Find all filename sections
    matches = list(filename_pattern.finditer(text))

    # Map domain sections to categories
    domain_markers = [
        ("Demographics", "Demographics"),
        ("History", "History"),
        ("Vitals", "Vitals"),
        ("Diagnosis", "Diagnosis"),
        ("Medications", "Medications"),
        ("Procedures", "Procedures"),
        ("Lab Orders", "Lab Orders"),
        ("Referrals", "Referrals"),
        ("Flowsheet", "Flowsheet"),
        ("Risk Management", "Risk Management"),
        ("Contact", "Contact"),
        ("Encounter", "Encounter"),
        ("ReasonForVisit", "Encounter"),
        ("Immunization", "Immunization"),
        ("Message", "Message"),
        ("Questionnaire", "Questionnaire"),
        ("Care Plans", "Care Plans"),
        ("Discrete data: Additional .json files", "Additional Files"),
        ("additional .json files", "Additional Files"),
    ]

    # Find domain boundaries
    domain_positions = []
    for marker, category in domain_markers:
        # Look for domain headers
        pos = text.find(marker + "\n")
        if pos == -1:
            pos = text.find(marker + " ")
        if pos >= 0:
            domain_positions.append((pos, category))
    domain_positions.sort(key=lambda x: x[0])

    def get_category(pos):
        cat = "Unknown"
        for dp, dc in domain_positions:
            if dp <= pos:
                cat = dc
            else:
                break
        return cat

    for match in matches:
        filename = match.group(1).strip()
        description = match.group(2).strip().replace("\n", " ")
        # Clean multi-line descriptions
        description = re.sub(r'\s+', ' ', description).strip()
        table_name = match.group(3).strip()
        primary_key = match.group(4).strip()
        category = get_category(match.start())

        # Extract fields from the table after this match
        fields = extract_ehr_fields(text, match.end())

        entities.append({
            "product": "Veradigm EHR",
            "filename": filename,
            "description": description,
            "database_table": table_name,
            "primary_key": primary_key,
            "category": category,
            "export_format": "JSON",
            "fields": fields,
        })

    return entities


def extract_ehr_fields(text, start_pos):
    """Extract field definitions from EHR PDF text starting at start_pos."""
    fields = []

    # Find "Field Definitions" header near start_pos
    fd_pos = text.find("Field Definitions", start_pos)
    if fd_pos == -1 or fd_pos > start_pos + 500:
        return fields

    # Find the next "Filename:" or end of section
    next_filename = text.find("Filename:", fd_pos + 1)
    next_domain = float('inf')
    for marker in ["Demographics\n", "History\n", "Vitals\n", "Diagnosis\n",
                    "Medications\n", "Procedures\n", "Lab Orders\n", "Referrals\n",
                    "Flowsheet\n", "Risk Management", "Contact\n", "Encounter\n",
                    "ReasonForVisit\n", "Immunization\n", "Message\n",
                    "Questionnaire\n", "Care Plans\n", "Discrete data: Additional"]:
        pos = text.find(marker, fd_pos + 100)
        if pos >= 0 and pos < next_domain:
            next_domain = pos

    end_pos = min(
        next_filename if next_filename > 0 else len(text),
        next_domain
    )

    section = text[fd_pos:end_pos]

    # Parse field lines - they look like:
    #  FieldName                Description text                          VARCHAR(255)
    # The challenge is multi-line descriptions and page breaks

    # Remove page headers/footers
    section = re.sub(
        r'November 9, 2023.*?not to be duplicated or disclosed to unauthorized persons\.',
        '', section, flags=re.DOTALL
    )
    # Remove "Field name   Description   Type of value" header rows
    section = re.sub(r'^\s*Field name\s+Description\s+Type of value\s*$', '', section, flags=re.MULTILINE)
    section = re.sub(r'^\s*Field Definitions\s*$', '', section, flags=re.MULTILINE)

    # Parse field lines using column-position approach
    # Fields start at left margin, type is at the right
    lines = section.split('\n')

    current_field = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this line starts a new field (starts with a word at the left margin)
        # Field lines have: FieldName (at col ~1-2), Description (at ~col 40-50), Type (at ~col 90+)
        # Use the pattern: line starts with a capitalized word followed by spaces and more text

        # Try to match a field definition line
        # The field name is typically CamelCase or UPPER_CASE starting near column 1
        field_match = re.match(
            r'^\s{0,2}(\w[\w_]*(?:\s*\w+)?)\s{3,}(.*?)\s{3,}((?:VARCHAR|Integer|DateTime|Date|Numeric|'
            r'SmallInteger|TinyInteger|Char|Datetimeoffset|Varchar|INT|CHAR|BIT|DECIMAL|'
            r'TEXT|varchar|datetime|char|bit|int|tinyint|String|TINYINT|DATETIME|'
            r'decimal|string|NVARCHAR)[\w\s(),.]*?)$',
            line
        )

        if field_match:
            if current_field:
                fields.append(current_field)
            fname = field_match.group(1).strip()
            fdesc = field_match.group(2).strip()
            ftype = field_match.group(3).strip()
            current_field = {
                "name": fname,
                "description": fdesc,
                "data_type": ftype,
            }
        else:
            # Check if this is a continuation of description from previous field
            # Continuation lines are indented and don't have a type at the end
            if current_field and stripped and not re.match(r'^(Filename|Description|EHR|Primary)', stripped):
                # Could be continuation of description
                continuation_match = re.match(r'^\s{10,}(.+?)(?:\s{3,}(\w.*?))?$', line)
                if continuation_match:
                    extra = continuation_match.group(1).strip()
                    if extra and not extra.startswith('Note:'):
                        current_field["description"] += " " + extra

    if current_field:
        fields.append(current_field)

    return fields


# ============================================================
# 2. Parse ePrescribe PDF
# ============================================================

def parse_eprescribe_pdf():
    """Parse the ePrescribe EHI Export PDF."""
    txt_path = ANALYSIS / "eprescribe-export-text.txt"
    if not txt_path.exists():
        subprocess.run([
            "pdftotext", "-layout",
            str(DOWNLOADS / "VeradigmePrescribe_EHI_Export_Documentation_v1.pdf"),
            str(txt_path)
        ], check=True)

    text = txt_path.read_text(encoding="utf-8")
    entities = []

    # Pattern for ePrescribe: "Filename: Allergies.tsv" etc.
    # Require Description on the next line to distinguish from ToC entries
    filename_pattern = re.compile(
        r'Filename:\s+([^\n.]+?\.tsv)\s*\n'
        r'Description:\s*(.*?)(?=\nEHR internal database table name:)'
        r'\nEHR internal database table name:\s*(.+?)\s*\n'
        r'Primary key:\s*(\S+)',
        re.DOTALL
    )

    matches = list(filename_pattern.finditer(text))

    for match in matches:
        filename = match.group(1).strip()
        description = re.sub(r'\s+', ' ', match.group(2).strip())
        table_name = match.group(3).strip()
        primary_key = match.group(4).strip()

        fields = extract_eprescribe_fields(text, match.end(), matches)

        entities.append({
            "product": "Veradigm ePrescribe",
            "filename": filename,
            "description": description,
            "database_table": table_name,
            "primary_key": primary_key,
            "category": categorize_eprescribe(filename),
            "export_format": "TSV",
            "fields": fields,
        })

    return entities


def categorize_eprescribe(filename):
    mapping = {
        "Allergies.tsv": "Allergies",
        "Demographics.tsv": "Demographics",
        "Diagnosis.tsv": "Diagnosis",
        "Historical Medications.tsv": "Medications",
        "Insurance.tsv": "Insurance",
        "Prescriptions.tsv": "Prescriptions",
    }
    return mapping.get(filename, "Other")


def extract_eprescribe_fields(text, start_pos, all_matches):
    """Extract fields from ePrescribe PDF tables."""
    fields = []

    # Find "Field Definitions" near start_pos
    fd_pos = text.find("Field Definitions", start_pos)
    if fd_pos == -1 or fd_pos > start_pos + 500:
        return fields

    # Find end of section
    next_positions = [m.start() for m in all_matches if m.start() > fd_pos]
    end_pos = min(next_positions) if next_positions else len(text)

    section = text[fd_pos:end_pos]

    # Remove page headers/footers
    section = re.sub(
        r'November 27, 2023.*?not to be duplicated or disclosed to unauthorized persons\.',
        '', section, flags=re.DOTALL
    )
    section = re.sub(r'^\s*Name\s+Description\s+Data type\s*$', '', section, flags=re.MULTILINE)
    section = re.sub(r'^\s*Field Definitions\s*$', '', section, flags=re.MULTILINE)

    lines = section.split('\n')
    current_field = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Try matching field line: Name   Description   DataType
        field_match = re.match(
            r'^\s{0,2}(\w[\w_]*(?:\s*\w+)?)\s{3,}(.*?)\s{3,}((?:VARCHAR|INT|CHAR|BIT|DECIMAL|'
            r'DATETIME|STRING|TINYINT|varchar|int|char|bit|decimal|datetime|string|tinyint|'
            r'Char|String|Varchar|Bit|Int|Text)[\w\s(),./:]*?)$',
            line
        )

        if field_match:
            if current_field:
                fields.append(current_field)
            current_field = {
                "name": field_match.group(1).strip(),
                "description": field_match.group(2).strip(),
                "data_type": field_match.group(3).strip(),
            }
        elif current_field and stripped:
            # Continuation line
            continuation = re.match(r'^\s{10,}(.+?)(?:\s{3,}(\S.*?))?$', line)
            if continuation:
                extra = continuation.group(1).strip()
                type_extra = continuation.group(2)
                if extra and not extra.startswith(('Note:', 'Figure')):
                    if type_extra:
                        current_field["data_type"] += type_extra.strip()
                    else:
                        current_field["description"] += " " + extra

    if current_field:
        fields.append(current_field)

    return fields


# ============================================================
# 3. Parse Practice Management PDF
# ============================================================

def parse_pm_pdf():
    """Parse the PM EHI Data Export PDF v2."""
    txt_path = ANALYSIS / "pm-export-v2-text.txt"
    if not txt_path.exists():
        subprocess.run([
            "pdftotext", "-layout",
            str(DOWNLOADS / "EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf"),
            str(txt_path)
        ], check=True)

    text = txt_path.read_text(encoding="utf-8")

    # PM has a different structure - it's a single hierarchical JSON document
    # The main fields are listed as FIELD NAME / DESCRIPTION pairs
    # Plus appendix sections for claim info, ailment info, ambulance, drug, anesthesia, dental

    entities = []

    # Parse main voucher structure (Chapter 2)
    main_fields = parse_pm_main_fields(text)
    entities.append({
        "product": "Veradigm Practice Management",
        "filename": "EHI_export.json",
        "description": "Patient financial/billing data export in hierarchical JSON format",
        "database_table": "N/A (hierarchical JSON)",
        "primary_key": "patientNumber",
        "category": "Billing/Claims",
        "export_format": "JSON",
        "fields": main_fields,
    })

    # Parse appendix sections
    appendix_sections = [
        ("Claim information fields", "Claim Information"),
        ("Ailment information fields", "Ailment Information"),
        ("Ambulance information fields", "Ambulance Information"),
        ("Drug information fields", "Drug Information"),
        ("Anesthesia information fields", "Anesthesia Information"),
        ("Dental information fields", "Dental Information"),
    ]

    for section_name, category in appendix_sections:
        fields = parse_pm_appendix(text, section_name)
        entities.append({
            "product": "Veradigm Practice Management",
            "filename": "EHI_export.json (appendix)",
            "description": f"{category} - possible fields for {section_name.split(' fields')[0].lower()}",
            "database_table": "N/A (appendix field list)",
            "primary_key": "N/A",
            "category": category,
            "export_format": "JSON",
            "fields": fields,
        })

    return entities


def parse_pm_main_fields(text):
    """Parse the main field list from PM PDF Chapter 2."""
    fields = []

    # Find the main field table (between "FIELD NAME" header and "Appendix"/"Chapter 3")
    start = text.find("FIELD NAME")
    if start == -1:
        return fields
    # End at the Appendix/Chapter 3 section that comes AFTER the field table
    end = text.find("Chapter 3", start)
    if end == -1:
        end = text.find("Appendix", start)
    if end == -1:
        end = text.find("Claim information fields", start)
    if end == -1:
        end = len(text)

    section = text[start:end]

    # Remove page headers/footers
    section = re.sub(
        r'May 07, 2024.*?not to be duplicated or disclosed to unauthorized persons\.',
        '', section, flags=re.DOTALL
    )
    section = re.sub(r'^\s*FIELD NAME\s+DESCRIPTION\s*$', '', section, flags=re.MULTILINE)

    lines = section.split('\n')
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # PM fields have indentation indicating hierarchy
        # Match: fieldName    Description text (field names are camelCase or lowercase)
        field_match = re.match(r'^(\s*)([a-zA-Z]\w*)\s{3,}(.+)$', line)
        if field_match:
            indent_level = len(field_match.group(1)) // 4
            fields.append({
                "name": field_match.group(2).strip(),
                "description": field_match.group(3).strip(),
                "data_type": "JSON value",
                "nesting_level": indent_level,
            })

    return fields


def parse_pm_appendix(text, section_header):
    """Parse an appendix section from PM PDF - these are simple lists of field names."""
    fields = []

    # Find the section header - skip ToC references by looking for header followed by
    # "The following are possible" on the next line
    pattern = re.compile(
        re.escape(section_header) + r'\s*\n'
        r'The following are possible',
        re.IGNORECASE
    )
    match = pattern.search(text)
    if not match:
        # Fallback: find last occurrence (likely the real one, not ToC)
        start = text.rfind(section_header)
        if start == -1:
            return fields
    else:
        start = match.start()

    # Find next section or end - search for ALL possible next headers after this one
    all_headers = [
        "Claim information fields",
        "Ailment information fields",
        "Ambulance information fields",
        "Drug information fields",
        "Anesthesia information fields",
        "Dental information fields",
    ]

    end = len(text)
    for header in all_headers:
        if header == section_header:
            continue
        # Find header after current position, skipping ToC
        pos = start + len(section_header) + 10
        while pos < end:
            pos = text.find(header, pos)
            if pos == -1:
                break
            # Check it's the real section (not ToC) by checking for dots after it
            after = text[pos + len(header):pos + len(header) + 10]
            if '...' not in after:
                if pos < end:
                    end = pos
                break
            pos += len(header)

    section = text[start:end]

    # Remove page headers
    section = re.sub(
        r'May 07, 2024.*?not to be duplicated or disclosed to unauthorized persons\.',
        '', section, flags=re.DOTALL
    )

    lines = section.split('\n')
    # Skip the header line and the "following are possible..." line
    past_intro = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if "following are possible" in stripped.lower():
            past_intro = True
            continue
        if not past_intro:
            continue
        # Each remaining non-empty line is a field name
        if stripped and not stripped.startswith(('May', 'EHI Data', 'Copyright', 'This page')):
            fields.append({
                "name": stripped,
                "description": stripped,
                "data_type": "Appendix field",
            })

    return fields


# ============================================================
# 4. Parse FollowMyHealth PDF + FHIR extensions
# ============================================================

def parse_fmh():
    """Parse FMH EHI Export Data Guide and FHIR extensions."""
    txt_path = ANALYSIS / "fmh-export-v2-text.txt"
    text = txt_path.read_text(encoding="utf-8")

    # FMH uses FHIR R4 resources - extract the resource list
    resources = [
        ("Account", "Billing", "My Account > Billing; Home > Billing widget"),
        ("AllergyIntolerance", "Clinical", "My Health > Allergies"),
        ("Appointment", "Administrative", "Home > Appointments widget"),
        ("Bundle", "Infrastructure", "Container for all FHIR resources"),
        ("Communication", "Messaging", "Messages (secure messaging)"),
        ("Condition", "Clinical", "My Health > Conditions > Health Conditions; Personal Health Conditions"),
        ("DiagnosticReport", "Clinical", "My Health > Results"),
        ("DocumentReference", "Documents", "My Health > Documents (scanned images, CCDAs, Form Builder forms)"),
        ("Encounter", "Clinical", "Not visible in PHR"),
        ("FamilyMemberHistory", "Clinical", "My Health > Conditions > Family Health Conditions"),
        ("Immunization", "Clinical", "My Health > Immunizations"),
        ("Invoice", "Billing", "My Account > Billing; Home > Billing widget"),
        ("Medication", "Clinical", "My Health > Medications (includes prescriptions)"),
        ("MedicationRequest", "Clinical", "My Health > Medications"),
        ("Observation", "Clinical", "My Health > Results; My Health > Vitals; Wellness > Measurements"),
        ("Patient", "Demographics", "Patient demographics with US Core race/ethnicity extensions"),
        ("Practitioner", "Administrative", "My Account > Connections"),
        ("Procedure", "Clinical", "My Health > Conditions > Surgical History"),
    ]

    entities = []
    for resource_type, category, description in resources:
        # Get FHIR resource standard fields (base level)
        fields = get_fhir_base_fields(resource_type)

        entities.append({
            "product": "FollowMyHealth",
            "filename": f"fhir-bundle.json ({resource_type})",
            "description": description,
            "database_table": f"FHIR R4 {resource_type}",
            "primary_key": "id (GUID)",
            "category": category,
            "export_format": "FHIR R4 JSON",
            "fields": fields,
        })

    # Parse FHIR extensions
    extensions = parse_fmh_extensions()

    return entities, extensions


def get_fhir_base_fields(resource_type):
    """Return key fields for each FHIR resource type used by FMH."""
    # These are the FHIR R4 base elements commonly present in each resource
    base = {
        "Account": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "identifier", "description": "Source EHR IDs", "data_type": "Identifier[]"},
            {"name": "status", "description": "Account status", "data_type": "code"},
            {"name": "name", "description": "Account name", "data_type": "string"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
        ],
        "AllergyIntolerance": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "identifier", "description": "Source EHR IDs", "data_type": "Identifier[]"},
            {"name": "clinicalStatus", "description": "Clinical status", "data_type": "CodeableConcept"},
            {"name": "code", "description": "Allergy substance", "data_type": "CodeableConcept"},
            {"name": "patient", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "reaction", "description": "Reaction details", "data_type": "BackboneElement[]"},
            {"name": "extension:AllergyStatus", "description": "FMH allergy status (Denied, Unknown)", "data_type": "Extension"},
        ],
        "Appointment": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Appointment status (mapped from FMH)", "data_type": "code"},
            {"name": "start", "description": "Appointment start", "data_type": "instant"},
            {"name": "end", "description": "Appointment end", "data_type": "instant"},
            {"name": "participant", "description": "Participants", "data_type": "BackboneElement[]"},
        ],
        "Bundle": [
            {"name": "id", "description": "Bundle ID", "data_type": "string"},
            {"name": "type", "description": "Bundle type", "data_type": "code"},
            {"name": "entry", "description": "Bundle entries", "data_type": "BackboneElement[]"},
            {"name": "link", "description": "Links including service-doc", "data_type": "BackboneElement[]"},
        ],
        "Communication": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Message status", "data_type": "code"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "payload", "description": "Message body + attachments", "data_type": "BackboneElement[]"},
            {"name": "sent", "description": "Date sent", "data_type": "dateTime"},
        ],
        "Condition": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "clinicalStatus", "description": "Clinical status", "data_type": "CodeableConcept"},
            {"name": "code", "description": "Condition code (ICD-10)", "data_type": "CodeableConcept"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "note", "description": "Notes (includes Denied status explanation)", "data_type": "Annotation[]"},
        ],
        "DiagnosticReport": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Report status", "data_type": "code"},
            {"name": "code", "description": "Report type", "data_type": "CodeableConcept"},
            {"name": "result", "description": "Observation references", "data_type": "Reference(Observation)[]"},
            {"name": "extension:CollectedOnDate", "description": "Collection date (FMH extension)", "data_type": "Extension"},
            {"name": "extension:OrderedOnDate", "description": "Order date (FMH extension)", "data_type": "Extension"},
        ],
        "DocumentReference": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Document status", "data_type": "code"},
            {"name": "type", "description": "Document type", "data_type": "CodeableConcept"},
            {"name": "content", "description": "Document content (URL reference to ZIP)", "data_type": "BackboneElement[]"},
        ],
        "Encounter": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Always Unknown (FMH has no status concept)", "data_type": "code"},
            {"name": "class", "description": "Encounter class", "data_type": "Coding"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
        ],
        "FamilyMemberHistory": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Always Completed (real status in extension)", "data_type": "code"},
            {"name": "patient", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "relationship", "description": "Family relationship", "data_type": "CodeableConcept"},
            {"name": "condition", "description": "Health conditions", "data_type": "BackboneElement[]"},
            {"name": "extension:FMHStatus", "description": "FMH health condition status", "data_type": "Extension"},
        ],
        "Immunization": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Immunization status (mapped from FMH)", "data_type": "code"},
            {"name": "vaccineCode", "description": "Vaccine code", "data_type": "CodeableConcept"},
            {"name": "patient", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "occurrence[x]", "description": "Date or 'Date Unavailable'", "data_type": "dateTime|string"},
        ],
        "Invoice": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Invoice status", "data_type": "code"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "totalGross", "description": "Total amount", "data_type": "Money"},
        ],
        "Medication": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "code", "description": "Medication code", "data_type": "CodeableConcept"},
            {"name": "note", "description": "Provider field if present", "data_type": "Annotation[]"},
        ],
        "MedicationRequest": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Request status", "data_type": "code"},
            {"name": "medication[x]", "description": "Medication reference", "data_type": "Reference(Medication)"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "note", "description": "Directions and Provider fields", "data_type": "Annotation[]"},
        ],
        "Observation": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Observation status", "data_type": "code"},
            {"name": "code", "description": "Observation type", "data_type": "CodeableConcept"},
            {"name": "value[x]", "description": "Result value", "data_type": "various"},
            {"name": "interpretation", "description": "Result interpretation", "data_type": "CodeableConcept[]"},
            {"name": "extension:PatientAddedProviderName", "description": "Patient-entered provider name", "data_type": "Extension"},
        ],
        "Patient": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "identifier", "description": "Source EHR IDs", "data_type": "Identifier[]"},
            {"name": "name", "description": "Patient name", "data_type": "HumanName[]"},
            {"name": "telecom", "description": "Contact information", "data_type": "ContactPoint[]"},
            {"name": "gender", "description": "Administrative gender", "data_type": "code"},
            {"name": "birthDate", "description": "Date of birth", "data_type": "date"},
            {"name": "address", "description": "Patient address", "data_type": "Address[]"},
            {"name": "extension:us-core-race", "description": "US Core race extension", "data_type": "Extension"},
            {"name": "extension:us-core-ethnicity", "description": "US Core ethnicity extension", "data_type": "Extension"},
            {"name": "extension:patient-genderidentity", "description": "FHIR gender identity extension", "data_type": "Extension"},
        ],
        "Practitioner": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "name", "description": "Practitioner name", "data_type": "HumanName[]"},
            {"name": "identifier", "description": "Provider identifiers", "data_type": "Identifier[]"},
        ],
        "Procedure": [
            {"name": "id", "description": "FMH GUID", "data_type": "string"},
            {"name": "status", "description": "Unknown or EnteredInError (real status in extension)", "data_type": "code"},
            {"name": "code", "description": "Procedure code", "data_type": "CodeableConcept"},
            {"name": "subject", "description": "Patient reference", "data_type": "Reference(Patient)"},
            {"name": "extension:ProcedureStatus", "description": "FMH procedure status", "data_type": "Extension"},
        ],
    }
    return base.get(resource_type, [])


def parse_fmh_extensions():
    """Parse FHIR extension JSON files."""
    extensions = []
    ext_dir = DOWNLOADS / "fmh-fhir-extensions"
    if not ext_dir.exists():
        return extensions

    for f in sorted(ext_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            extensions.append({
                "filename": f.name,
                "resourceType": data.get("resourceType", "Unknown"),
                "url": data.get("url", ""),
                "name": data.get("name", f.stem),
                "description": data.get("description", ""),
                "status": data.get("status", ""),
            })
        except Exception as e:
            extensions.append({
                "filename": f.name,
                "parse_error": True,
                "error": str(e),
            })

    return extensions


# ============================================================
# 5. Parse Veradigm View HTML pages
# ============================================================

def parse_view_html():
    """Parse all 87+ Veradigm View HTML entity pages."""
    view_dir = DOWNLOADS / "veradigm-view-v6"
    if not view_dir.exists():
        return []

    entities = []
    html_files = sorted(view_dir.glob("*.html"))

    # Category mapping based on known groupings from the index page
    category_map = {}
    index_path = view_dir / "index.html"
    if index_path.exists():
        category_map = parse_view_index(index_path)

    for html_file in html_files:
        if html_file.name == "index.html":
            continue

        try:
            html = html_file.read_text(encoding="utf-8")
            file_entities = parse_view_entity_page(html, html_file.name, category_map)
            entities.extend(file_entities)
        except Exception as e:
            entities.append({
                "product": "Veradigm View",
                "filename": html_file.name,
                "description": f"Parse error: {str(e)}",
                "database_table": "Unknown",
                "primary_key": "Unknown",
                "category": "Unknown",
                "export_format": "TSV",
                "fields": [],
                "parse_error": True,
            })

    return entities


def parse_view_index(index_path):
    """Parse the View index page to get category assignments."""
    html = index_path.read_text(encoding="utf-8")
    category_map = {}

    # The index page has category sections with links to entity pages
    # Look for category headers and the links that follow
    current_category = "Uncategorized"

    # Find h2 or h3 headers that are category names
    # Then find href links in the subsequent content
    sections = re.split(r'<h[23][^>]*>(.*?)</h[23]>', html)

    for i in range(1, len(sections), 2):
        header = re.sub(r'<[^>]*>', '', sections[i]).strip()
        if header and i + 1 < len(sections):
            content = sections[i + 1]
            # Find all links in this section
            links = re.findall(r'href="[^"]*?/v6/([^/"]+)/"', content)
            for link in links:
                category_map[link + ".html"] = header

    return category_map


def parse_view_entity_page(html, filename, category_map):
    """Parse a single Veradigm View entity HTML page."""
    entities = []

    # Extract page title from <h1>
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    page_title = re.sub(r'<[^>]*>', '', h1_match.group(1)).strip() if h1_match else filename

    # Find all h2 elements (TSV filenames)
    h2_matches = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE | re.DOTALL))
    table_matches = list(re.finditer(r'<table[^>]*>([\s\S]*?)</table>', html, re.IGNORECASE))
    h4_matches = list(re.finditer(r'<h4[^>]*>(.*?)</h4>', html, re.IGNORECASE | re.DOTALL))

    # Filter h2s with .tsv
    tsv_h2s = [m for m in h2_matches if '.tsv' in m.group(1)]

    category = category_map.get(filename, "Uncategorized")

    for i, h2 in enumerate(tsv_h2s):
        tsv_name = re.sub(r'<[^>]*>', '', h2.group(1)).strip()
        h2_pos = h2.start()
        next_h2_pos = tsv_h2s[i + 1].start() if i + 1 < len(tsv_h2s) else len(html)

        # Find h4 description in this region
        region_h4s = [m for m in h4_matches if h2_pos < m.start() < next_h2_pos]
        entity_desc = re.sub(r'<[^>]*>', '', region_h4s[0].group(1)).strip() if region_h4s else ""

        # Find table in this region
        region_tables = [m for m in table_matches if h2_pos < m.start() < next_h2_pos]

        fields = []
        if region_tables:
            fields = extract_view_table_fields(region_tables[0].group(0))

        entities.append({
            "product": "Veradigm View",
            "filename": tsv_name,
            "description": entity_desc,
            "database_table": f"Practice Fusion: {tsv_name.replace('.tsv', '')}",
            "primary_key": "id (implied)",
            "category": category,
            "export_format": "TSV",
            "fields": fields,
        })

    return entities


def extract_view_table_fields(table_html):
    """Extract fields from a View HTML table."""
    fields = []
    # Match table rows with 3 cells: Field Name, Data Type, Description
    row_pattern = re.compile(
        r'<tr>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>',
        re.IGNORECASE | re.DOTALL
    )

    for match in row_pattern.finditer(table_html):
        name = re.sub(r'<[^>]*>', '', match.group(1)).strip()
        data_type = re.sub(r'<[^>]*>', '', match.group(2)).strip()
        description = re.sub(r'<[^>]*>', '', match.group(3)).strip()

        # Clean up HTML entities
        for entity, char in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
                              ('&quot;', '"'), ('&#39;', "'"), ('&nbsp;', ' ')]:
            name = name.replace(entity, char)
            description = description.replace(entity, char)
            data_type = data_type.replace(entity, char)

        if name and name.lower() != "field name":  # Skip header row
            fields.append({
                "name": name,
                "description": description,
                "data_type": data_type,
            })

    return fields


# ============================================================
# Main: Combine all products
# ============================================================

def main():
    print("Parsing Veradigm EHR PDF...")
    ehr_entities = parse_ehr_pdf()
    print(f"  Found {len(ehr_entities)} entities, {sum(len(e['fields']) for e in ehr_entities)} fields")

    print("Parsing Veradigm ePrescribe PDF...")
    eprescribe_entities = parse_eprescribe_pdf()
    print(f"  Found {len(eprescribe_entities)} entities, {sum(len(e['fields']) for e in eprescribe_entities)} fields")

    print("Parsing Veradigm Practice Management PDF...")
    pm_entities = parse_pm_pdf()
    print(f"  Found {len(pm_entities)} entities, {sum(len(e['fields']) for e in pm_entities)} fields")

    print("Parsing FollowMyHealth...")
    fmh_entities, fmh_extensions = parse_fmh()
    print(f"  Found {len(fmh_entities)} FHIR resources, {sum(len(e['fields']) for e in fmh_entities)} fields")
    print(f"  Found {len(fmh_extensions)} FHIR extension definitions")

    print("Parsing Veradigm View HTML...")
    view_entities = parse_view_html()
    print(f"  Found {len(view_entities)} entities, {sum(len(e['fields']) for e in view_entities)} fields")

    # Combine everything
    all_entities = ehr_entities + eprescribe_entities + pm_entities + fmh_entities + view_entities

    full_inventory = {
        "products": [
            {
                "name": "Veradigm EHR",
                "export_format": "JSON (password-protected ZIP)",
                "doc_version": "v1 (Nov 9, 2023)",
                "doc_pages": 89,
                "entities": ehr_entities,
            },
            {
                "name": "Veradigm ePrescribe",
                "export_format": "TSV (ZIP)",
                "doc_version": "v1 (Nov 27, 2023)",
                "doc_pages": 22,
                "entities": eprescribe_entities,
            },
            {
                "name": "Veradigm Practice Management",
                "export_format": "JSON",
                "doc_version": "v2 (May 7, 2024)",
                "doc_pages": 20,
                "entities": pm_entities,
            },
            {
                "name": "FollowMyHealth",
                "export_format": "FHIR R4 JSON Bundle (ZIP)",
                "doc_version": "v2 (Feb 28, 2024)",
                "doc_pages": 20,
                "fhir_extensions": fmh_extensions,
                "entities": fmh_entities,
            },
            {
                "name": "Veradigm View (Practice Fusion)",
                "export_format": "TSV",
                "doc_version": "v6 (Jan 12, 2026)",
                "doc_pages": "87 HTML pages + index",
                "entities": view_entities,
            },
        ],
        "totals": {
            "total_products": 5,
            "total_entities": len(all_entities),
            "total_fields": sum(len(e["fields"]) for e in all_entities),
            "entities_by_product": {
                "Veradigm EHR": len(ehr_entities),
                "Veradigm ePrescribe": len(eprescribe_entities),
                "Veradigm Practice Management": len(pm_entities),
                "FollowMyHealth": len(fmh_entities),
                "Veradigm View": len(view_entities),
            },
            "fields_by_product": {
                "Veradigm EHR": sum(len(e["fields"]) for e in ehr_entities),
                "Veradigm ePrescribe": sum(len(e["fields"]) for e in eprescribe_entities),
                "Veradigm Practice Management": sum(len(e["fields"]) for e in pm_entities),
                "FollowMyHealth": sum(len(e["fields"]) for e in fmh_entities),
                "Veradigm View": sum(len(e["fields"]) for e in view_entities),
            },
        },
    }

    # Write full inventory
    with open(ANALYSIS / "entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"\nWrote entity-inventory-full.json")

    # Build summary
    summary = build_summary(full_inventory, all_entities)
    with open(ANALYSIS / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")

    print(f"\n=== TOTALS ===")
    print(f"Products: {full_inventory['totals']['total_products']}")
    print(f"Total entities: {full_inventory['totals']['total_entities']}")
    print(f"Total fields: {full_inventory['totals']['total_fields']}")
    for product, count in full_inventory['totals']['entities_by_product'].items():
        fc = full_inventory['totals']['fields_by_product'][product]
        print(f"  {product}: {count} entities, {fc} fields")


def build_summary(full_inventory, all_entities):
    """Build summary statistics from the full inventory."""

    # Fields with descriptions
    fields_with_desc = 0
    fields_total = 0
    fields_with_types = 0
    for e in all_entities:
        for f in e["fields"]:
            fields_total += 1
            if f.get("description") and f["description"].strip():
                fields_with_desc += 1
            if f.get("data_type") and f["data_type"].strip():
                fields_with_types += 1

    # Category breakdown by product
    category_breakdown = {}
    for product_data in full_inventory["products"]:
        product_name = product_data["name"]
        categories = {}
        for entity in product_data["entities"]:
            cat = entity.get("category", "Uncategorized")
            if cat not in categories:
                categories[cat] = {"entity_count": 0, "field_count": 0}
            categories[cat]["entity_count"] += 1
            categories[cat]["field_count"] += len(entity["fields"])
        category_breakdown[product_name] = categories

    # Top entities by field count
    entity_sizes = []
    for e in all_entities:
        entity_sizes.append({
            "product": e["product"],
            "filename": e["filename"],
            "category": e.get("category", ""),
            "field_count": len(e["fields"]),
            "has_descriptions": all(
                f.get("description", "").strip() != "" for f in e["fields"]
            ) if e["fields"] else False,
        })
    entity_sizes.sort(key=lambda x: x["field_count"], reverse=True)

    return {
        "totals": full_inventory["totals"],
        "field_quality": {
            "total_fields": fields_total,
            "fields_with_descriptions": fields_with_desc,
            "fields_with_types": fields_with_types,
            "description_coverage_pct": round(100 * fields_with_desc / fields_total, 1) if fields_total else 0,
            "type_coverage_pct": round(100 * fields_with_types / fields_total, 1) if fields_total else 0,
        },
        "category_breakdown_by_product": category_breakdown,
        "top_20_entities_by_field_count": entity_sizes[:20],
        "entities_with_zero_fields": [e for e in entity_sizes if e["field_count"] == 0],
    }


if __name__ == "__main__":
    main()
