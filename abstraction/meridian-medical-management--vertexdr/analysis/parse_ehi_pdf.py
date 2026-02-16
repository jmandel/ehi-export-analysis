#!/usr/bin/env python3
"""Parse the VertexDr EHI Export Documentation PDF text to extract
all C-CDA sections and data elements, plus non-CCD export categories."""

import json
import re

INPUT = "ehi-export-text.txt"
OUTPUT = "full-entity-inventory.json"

with open(INPUT) as f:
    text = f.read()

# --- Parse C-CDA sections and their data elements ---
# Sections are identified by headers like:
#   Patient Demographics/Information
#   Encounters [2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01]
#   Immunizations [2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01]

# Extract pages 6-10 content (CCD Output Format section)
ccd_start = text.find("Sections in the CCD output")
ccd_end = text.find("Patient Demographic/Insurance\nPDF format")
if ccd_end == -1:
    ccd_end = text.find("Patient Demographic/Insurance")

ccd_text = text[ccd_start:ccd_end]

# Define sections we expect based on the PDF
section_patterns = [
    r"Patient Demographics/Information",
    r"Provider's name and office contact information",
    r"Date and Location of visit \[.*?\]",
    r"Chief Complaint and Reason for visit \[.*?\]",
    r"Encounters \[.*?\]",
    r"Immunizations \[.*?\]",
    r"Instructions \[.*?\]",
    r"Treatment Plan \[.*?\]",
    r"Social History \[.*?\]",
    r"Problems \[.*?\]",
    r"Medications \[.*?\]",
    r"Medication Allergies \[.*?\]",
    r"Laboratory Tests",
    r"Laboratory Information",
    r"Laboratory value\(s\)/result\(s\) \[.*?\]",
    r"Vitals \[.*?\]",
    r"Goal \[.*?\]",
    r"Procedures \[.*?\]",
    r"Care team member\(s\) \[.*?\]",
    r"Reason for Referral \[.*?\]",
    r"Medical Equipment \[.*?\]",
    r"Mental Status \[.*?\]",
    r"Functional Status \[.*?\]",
    r"Health Concern \[.*?\]",
]

# Manual parsing approach: split by lines and track sections
lines = ccd_text.split('\n')

sections = []
current_section = None
current_fields = []

def is_section_header(line):
    """Check if a line is a section header."""
    stripped = line.strip()
    if not stripped:
        return False
    # Section headers are either plain text or text with [OID : date]
    # They don't start with spaces (relative to the column layout)
    # and they don't contain XPATH-like patterns as their primary content
    if stripped.startswith("Data Elements"):
        return False
    if stripped.startswith("Page "):
        return False
    if stripped.startswith("§170"):
        return False
    if stripped.startswith("Information Export"):
        return False
    if stripped.startswith("Standard Referenced"):
        return False
    if stripped.startswith("Sections in"):
        return False
    if stripped.startswith("•"):
        return False
    if stripped.startswith("Version:"):
        return False
    # Check for known section patterns
    for pat in section_patterns:
        if re.match(pat, stripped):
            return True
    return False

def extract_oid(header):
    """Extract OID from section header like 'Problems [2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01]'"""
    m = re.search(r'\[([\d.]+)\s*:\s*([\d-]+)\]', header)
    if m:
        return m.group(1), m.group(2)
    m = re.search(r'\[([\d.]+)\]', header)
    if m:
        return m.group(1), None
    return None, None

def clean_section_name(header):
    """Remove OID bracket from section name."""
    return re.sub(r'\s*\[.*?\]', '', header).strip()

# Parse the CCD data element table
# Fields are identified as lines that have a data element name
# (often in the first column), an XPATH/entry path, and optionally code system info

# Simpler approach: manually define the sections and their fields
# based on careful reading of the extracted text

ccda_sections = []

# Re-read the text more carefully, line by line
field_lines = []
current_section_name = None
current_section_oid = None
current_section_version = None

for line in lines:
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith("Page ") and "of 11" in stripped:
        continue
    if stripped.startswith("§170.315"):
        continue
    if stripped.startswith("Information Export"):
        continue
    if stripped.startswith("Data Elements") and "XPATH" in stripped:
        continue
    if stripped.startswith("Sections in the CCD output"):
        continue
    if stripped.startswith("Standard Referenced"):
        continue
    if stripped.startswith("•"):
        continue
    if stripped.startswith("(Diagnostic tests"):
        continue

    if is_section_header(stripped):
        if current_section_name and current_fields:
            ccda_sections.append({
                "section_name": current_section_name,
                "template_oid": current_section_oid,
                "template_version": current_section_version,
                "fields": current_fields
            })
        current_section_name = clean_section_name(stripped)
        current_section_oid, current_section_version = extract_oid(stripped)
        current_fields = []
    else:
        # This is a field/data element line
        if current_section_name:
            # Extract field info - some lines have code system info
            # Try to parse: field_name, xpath, code_system_oid, code_system_name
            # The layout has columns but they're not perfectly aligned
            field_name = stripped

            # Check if this line contains code system info
            code_system_oid = None
            code_system_name = None

            # Look for OID patterns (2.16.840.1.xxx)
            oid_match = re.findall(r'(2\.16\.840\.1\.[\d.]+)', stripped)
            if oid_match:
                # Try to separate field name from OID
                parts = re.split(r'\s{2,}', stripped)
                if len(parts) >= 2:
                    field_name = parts[0].strip()
                    # Remaining parts may have xpath, oid, name
                    for p in parts[1:]:
                        p = p.strip()
                        if re.match(r'2\.16\.840\.1\.', p):
                            if 'and' in p:
                                code_system_oid = p
                            elif code_system_oid is None:
                                code_system_oid = p
                        elif p and not p.startswith('0.22.') and not p.startswith('entry/') and not p.startswith('patient/') and not p.startswith('documentationOf/'):
                            if code_system_name is None and not re.match(r'2\.16\.', p):
                                code_system_name = p
                else:
                    field_name = stripped

            # Clean up field name - remove xpath fragments
            field_name = re.sub(r'\s*2\.16\.840\.1\.[\d.]+.*$', '', field_name)
            field_name = re.sub(r'\s*entry/.*$', '', field_name)
            field_name = re.sub(r'\s*/.*$', '', field_name)
            field_name = field_name.strip()

            if field_name and not field_name.startswith('0.22.') and not field_name.startswith('nedEntity') and not field_name.startswith('eEvent'):
                current_fields.append({
                    "name": field_name,
                    "code_system_oid": code_system_oid,
                    "code_system_name": code_system_name
                })

# Don't forget the last section
if current_section_name and current_fields:
    ccda_sections.append({
        "section_name": current_section_name,
        "template_oid": current_section_oid,
        "template_version": current_section_version,
        "fields": current_fields
    })

# --- Parse non-CCD export categories ---
non_ccd_start = text.find("Patient Demographic/Insurance\nPDF format")
if non_ccd_start == -1:
    non_ccd_start = text.find("Patient Demographic/Insurance")
non_ccd_text = text[non_ccd_start:]

pdf_exports = []
pdf_categories = [
    {
        "name": "Patient Demographic/Insurance",
        "description": "PDF format - comprehensive view of demographics and insurance details",
        "format": "PDF"
    },
    {
        "name": "Advance Directive",
        "description": "PDF format - comprehensive view of Advance Directive",
        "format": "PDF"
    },
    {
        "name": "Appointments",
        "description": "PDF format - comprehensive view of appointments",
        "format": "PDF"
    },
    {
        "name": "Provider-to-Patient Messages",
        "description": "PDF format - comprehensive view of messages",
        "format": "PDF"
    },
    {
        "name": "Billing Data (Claim)",
        "description": "PDF format - comprehensive view of billing data (CPT, ICD, Modifier)",
        "format": "PDF"
    },
    {
        "name": "Documents",
        "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document. Exported in PDF format.",
        "format": "PDF"
    },
]

# --- FHIR export ---
fhir_export = {
    "name": "FHIR Data Export",
    "description": "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii).",
    "documentation_detail": "single_sentence",
    "fields_documented": 0
}

# --- Build full inventory ---
inventory = {
    "product": "VertexDr",
    "version": "9.1",
    "vendor": "Meridian Medical Management (CareCloud)",
    "source_document": "VertexDr-b10-EHI-Export-Documentation.pdf",
    "source_pages": 11,
    "export_mechanisms": [
        {
            "name": "CCD/C-CDA Export",
            "format": "XML (C-CDA)",
            "standard": "HL7 CDA R2 Consolidated CDA Templates, DSTU R2.1, August 2015",
            "capabilities": ["single_patient", "bulk_patient"],
            "bulk_output": "ZIP file with CCDA XML documents"
        },
        {
            "name": "PDF Exports",
            "format": "PDF",
            "standard": "None (proprietary PDF)",
            "capabilities": ["single_patient"],
            "notes": "Accessible via Reports section"
        },
        {
            "name": "FHIR Bulk Data Export",
            "format": "FHIR",
            "standard": "FHIR",
            "capabilities": ["single_patient", "bulk_patient"],
            "notes": "Mentioned in single sentence, no documentation"
        }
    ],
    "ccda_sections": ccda_sections,
    "pdf_export_categories": pdf_categories,
    "fhir_export": fhir_export,
    "summary_statistics": {}
}

# Calculate statistics
total_ccda_fields = sum(len(s["fields"]) for s in ccda_sections)
total_ccda_sections = len(ccda_sections)
fields_with_code_system = sum(
    1 for s in ccda_sections for f in s["fields"]
    if f.get("code_system_oid") or f.get("code_system_name")
)
total_pdf_categories = len(pdf_categories)

inventory["summary_statistics"] = {
    "ccda_sections": total_ccda_sections,
    "ccda_fields_total": total_ccda_fields,
    "ccda_fields_with_code_system": fields_with_code_system,
    "pdf_export_categories": total_pdf_categories,
    "pdf_fields_documented": 0,  # No field-level docs for PDF exports
    "total_export_components": total_ccda_sections + total_pdf_categories + 1,  # +1 for FHIR
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "has_data_dictionary": False,  # C-CDA element mapping, not a true data dictionary
    "has_field_descriptions": False,  # Fields listed but not described
    "has_relationships": False,
    "has_value_sets": False  # Code systems named but not enumerated
}

with open(OUTPUT, 'w') as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"C-CDA Sections: {total_ccda_sections}")
print(f"C-CDA Fields Total: {total_ccda_fields}")
print(f"C-CDA Fields with Code Systems: {fields_with_code_system}")
print(f"PDF Export Categories: {total_pdf_categories}")
print(f"PDF Fields Documented: 0")
print()

print("=== C-CDA Sections ===")
for s in ccda_sections:
    oid_str = f" [{s['template_oid']}]" if s['template_oid'] else ""
    print(f"  {s['section_name']}{oid_str}: {len(s['fields'])} fields")
    for f_item in s['fields']:
        cs = f" ({f_item['code_system_name']})" if f_item.get('code_system_name') else ""
        print(f"    - {f_item['name']}{cs}")

print()
print("=== PDF Export Categories ===")
for cat in pdf_categories:
    print(f"  {cat['name']}: {cat['description']}")

print()
print("=== FHIR Export ===")
print(f"  {fhir_export['description']}")
