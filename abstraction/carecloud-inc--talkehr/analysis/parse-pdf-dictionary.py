#!/usr/bin/env python3
"""Parse the talkEHR b(10) PDF to extract all documented data elements.

Reads the PDF text (extracted via pdftotext -layout) and parses:
1. C-CDA sections with their data elements, XPATHs, and code systems (pages 6-10)
2. PDF-format export categories (page 11)
3. FHIR mention (page 12)

Outputs entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import re
import subprocess
import sys

PDF_PATH = "../downloads/talkEHR-b10-EHI-Export-Documentation.pdf"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_ccda_sections(text):
    """Parse the C-CDA field mapping tables from pages 6-10."""
    sections = []
    current_section = None
    current_fields = []
    
    # Split into lines
    lines = text.split('\n')
    
    # Section header pattern: text followed by [OID : date] or standalone header
    section_pattern = re.compile(
        r'^([A-Z][A-Za-z\s/\(\)\-&]+?)\s*'
        r'(?:\[(\d[\d\.]+\d)\s*(?::\s*[\d\-]+)?\])?'
        r'\s*$'
    )
    
    # Known C-CDA section names from the PDF
    known_sections = [
        "Patient Demographics/Information",
        "Provider's name and office contact information",
        "Date and Location of visit",
        "Chief Complaint and Reason for visit",
        "Encounters",
        "Immunizations",
        "Instructions",
        "Treatment Plan",
        "Social History",
        "Problems",
        "Medications",
        "Medication Allergies",
        "Laboratory Tests",
        "Laboratory Information",
        "Laboratory value(s)/result(s)",
        "Vitals",
        "Goal",
        "Procedures",
        "Care team member(s)",
        "Reason for Referral",
        "Medical Equipment",
        "Mental Status",
        "Functional Status",
        "Health Concern",
    ]
    
    in_ccd_section = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines and page headers/footers
        if not stripped or 'Page ' in stripped and ' of 12' in stripped:
            continue
        if '§170.315(b)(10)' in stripped:
            continue
        if 'Export – Documentation' in stripped or 'Export- Documentation' in stripped:
            continue
        if stripped == 'Data Elements' or stripped.startswith('XPATH'):
            continue
        if stripped.startswith('Code System') and 'Name' in stripped:
            continue
            
        # Detect start of CCD output section
        if 'CCD Output Format' in stripped:
            in_ccd_section = True
            continue
        if 'Standard Referenced:' in stripped:
            continue
        if '§ 170.205(a)(4)' in stripped or 'HL7® Implementation' in stripped:
            continue
        if 'Sections in the CCD output' in stripped:
            continue
            
        # Detect end of CCD section (page 11 content)
        if stripped == 'Patient Demographic/Insurance':
            in_ccd_section = False
            # Save current section
            if current_section and current_fields:
                sections.append({
                    "section_name": current_section["name"],
                    "template_oid": current_section.get("oid"),
                    "fields": current_fields
                })
            break
            
        if not in_ccd_section:
            continue
            
        # Check if this line is a section header
        is_section_header = False
        for known in known_sections:
            if stripped.startswith(known) or known.startswith(stripped.split('[')[0].strip()):
                is_section_header = True
                # Save previous section
                if current_section and current_fields:
                    sections.append({
                        "section_name": current_section["name"],
                        "template_oid": current_section.get("oid"),
                        "fields": current_fields
                    })
                
                # Extract OID if present
                oid_match = re.search(r'\[([\d\.]+)', stripped)
                current_section = {
                    "name": known,
                    "oid": oid_match.group(1) if oid_match else None
                }
                current_fields = []
                break
        
        if is_section_header:
            continue
            
        # Parse field lines - they have the field name, sometimes xpath, code system
        if current_section and not is_section_header:
            # Skip lines that are purely OID references or continuations
            if re.match(r'^[\d\.]+$', stripped):
                continue
            if stripped.startswith('(') and stripped.endswith(')'):
                continue
                
            # Extract field name (first meaningful text)
            # Fields are left-aligned, XPATHs are in the middle, code systems right
            parts = re.split(r'\s{3,}', line.rstrip())
            parts = [p.strip() for p in parts if p.strip()]
            
            if parts and not parts[0].startswith('2.16.') and not parts[0].startswith('and '):
                field_name = parts[0]
                # Skip noise
                if field_name in ('Data Elements', 'Code System', 'Code System Name'):
                    continue
                if '(' in field_name and 'Diagnostic' in field_name:
                    continue  # subtitle line
                    
                xpath = None
                code_system_oid = None
                code_system_name = None
                
                for p in parts[1:]:
                    if '2.16.840' in p or '1.3.6.1' in p:
                        if 'entry/' in p or 'patient/' in p or 'documentationOf/' in p:
                            xpath = p
                        else:
                            if code_system_oid:
                                code_system_oid += " " + p
                            else:
                                code_system_oid = p
                    elif any(name in p for name in ['SNOMED', 'LOINC', 'RxNorm', 'NDC', 'CVX', 
                                                       'CPT', 'HCPCS', 'CDC', 'NCI', 'ICD',
                                                       'Administrative', 'Race', 'Thesaurus']):
                        code_system_name = p
                    elif not xpath and ('/' in p or p.startswith('entry')):
                        xpath = p
                
                current_fields.append({
                    "name": field_name,
                    "xpath": xpath,
                    "code_system_oid": code_system_oid,
                    "code_system_name": code_system_name
                })
    
    # Save last section if needed
    if current_section and current_fields:
        sections.append({
            "section_name": current_section["name"],
            "template_oid": current_section.get("oid"),
            "fields": current_fields
        })
    
    return sections

def build_pdf_export_entities():
    """Build entities for the PDF-format exports described on page 11."""
    return [
        {
            "section_name": "Patient Demographic/Insurance (PDF)",
            "template_oid": None,
            "export_format": "PDF",
            "description": "Comprehensive view of demographics and insurance details",
            "fields": [
                {"name": "Demographics (unspecified fields)", "xpath": None, 
                 "code_system_oid": None, "code_system_name": None,
                 "note": "No field-level detail provided in documentation"}
            ]
        },
        {
            "section_name": "Advance Directive (PDF)",
            "template_oid": None,
            "export_format": "PDF",
            "description": "Comprehensive view of Advance Directive",
            "fields": [
                {"name": "Advance Directive (unspecified fields)", "xpath": None,
                 "code_system_oid": None, "code_system_name": None,
                 "note": "No field-level detail provided in documentation"}
            ]
        },
        {
            "section_name": "Appointments (PDF)",
            "template_oid": None,
            "export_format": "PDF",
            "description": "Comprehensive view of appointments",
            "fields": [
                {"name": "Appointments (unspecified fields)", "xpath": None,
                 "code_system_oid": None, "code_system_name": None,
                 "note": "No field-level detail provided in documentation"}
            ]
        },
        {
            "section_name": "Provider-to-Patient Messages (PDF)",
            "template_oid": None,
            "export_format": "PDF",
            "description": "Comprehensive view of messages",
            "fields": [
                {"name": "Messages (unspecified fields)", "xpath": None,
                 "code_system_oid": None, "code_system_name": None,
                 "note": "No field-level detail provided in documentation"}
            ]
        },
        {
            "section_name": "Billing Data / Claims (PDF)",
            "template_oid": None,
            "export_format": "PDF",
            "description": "Comprehensive view of billing data (CPT, ICD, Modifier)",
            "fields": [
                {"name": "CPT codes", "xpath": None,
                 "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
                {"name": "ICD codes", "xpath": None,
                 "code_system_oid": "2.16.840.1.113883.6.3", "code_system_name": "ICD-10"},
                {"name": "Modifiers", "xpath": None,
                 "code_system_oid": None, "code_system_name": None},
                {"name": "Other billing fields (unspecified)", "xpath": None,
                 "code_system_oid": None, "code_system_name": None,
                 "note": "No further field-level detail provided"}
            ]
        },
        {
            "section_name": "Documents (PDF)",
            "template_oid": None,
            "export_format": "PDF",
            "description": "Signed progress notes, lab results, radiology reports, scanned/uploaded documents",
            "fields": [
                {"name": "Progress notes", "xpath": None,
                 "code_system_oid": None, "code_system_name": None},
                {"name": "Lab results", "xpath": None,
                 "code_system_oid": None, "code_system_name": None},
                {"name": "Radiology reports", "xpath": None,
                 "code_system_oid": None, "code_system_name": None},
                {"name": "Scanned/uploaded documents", "xpath": None,
                 "code_system_oid": None, "code_system_name": None}
            ]
        },
    ]

def build_fhir_entity():
    """Build entity for the FHIR export mention on page 12."""
    return {
        "section_name": "FHIR Data Export",
        "template_oid": None,
        "export_format": "FHIR",
        "description": "Single-patient DocumentReference and FHIR Bulk Data EHI Export",
        "fields": [
            {"name": "DocumentReference", "xpath": None,
             "code_system_oid": None, "code_system_name": None,
             "note": "No technical detail provided beyond one-sentence mention"}
        ]
    }

def main():
    text = extract_text()
    
    # Parse C-CDA sections
    ccda_sections = parse_ccda_sections(text)
    
    # Add export format to C-CDA sections
    for s in ccda_sections:
        s["export_format"] = "C-CDA R2.1 XML"
    
    # Build PDF export entities
    pdf_entities = build_pdf_export_entities()
    
    # Build FHIR entity
    fhir_entity = build_fhir_entity()
    
    # Combine all
    all_entities = ccda_sections + pdf_entities + [fhir_entity]
    
    # Compute stats
    total_entities = len(all_entities)
    total_fields = sum(len(e["fields"]) for e in all_entities)
    fields_with_xpath = sum(
        1 for e in all_entities for f in e["fields"] if f.get("xpath")
    )
    fields_with_code_system = sum(
        1 for e in all_entities for f in e["fields"] if f.get("code_system_name")
    )
    fields_with_notes = sum(
        1 for e in all_entities for f in e["fields"] if f.get("note")
    )
    
    # Full inventory
    inventory = {
        "source": "talkEHR-b10-EHI-Export-Documentation.pdf",
        "source_pages": "6-12",
        "extraction_method": "pdftotext -layout + Python parsing",
        "total_entities": total_entities,
        "total_fields": total_fields,
        "fields_with_xpath": fields_with_xpath,
        "fields_with_code_system": fields_with_code_system,
        "entities": all_entities
    }
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Summary
    ccda_field_count = sum(len(e["fields"]) for e in ccda_sections)
    pdf_field_count = sum(len(e["fields"]) for e in pdf_entities)
    
    summary = {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "by_format": {
            "C-CDA R2.1 XML": {
                "entity_count": len(ccda_sections),
                "field_count": ccda_field_count,
                "fields_with_xpath": fields_with_xpath,
                "fields_with_code_system": fields_with_code_system,
                "sections": [
                    {
                        "name": s["section_name"],
                        "template_oid": s.get("template_oid"),
                        "field_count": len(s["fields"])
                    }
                    for s in ccda_sections
                ]
            },
            "PDF": {
                "entity_count": len(pdf_entities),
                "field_count": pdf_field_count,
                "categories": [s["section_name"] for s in pdf_entities],
                "documentation_quality": "Minimal - no field-level detail"
            },
            "FHIR": {
                "entity_count": 1,
                "field_count": 1,
                "documentation_quality": "One sentence, no technical detail"
            }
        },
        "documentation_quality": {
            "ccda_sections_with_detailed_mapping": len(ccda_sections),
            "pdf_sections_with_no_field_detail": len(pdf_entities),
            "fhir_with_no_detail": 1,
            "sample_data_provided": False,
            "machine_readable_schema": False
        }
    }
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total entities: {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"  C-CDA sections: {len(ccda_sections)} with {ccda_field_count} fields")
    print(f"    Fields with XPATH: {fields_with_xpath}")
    print(f"    Fields with code system: {fields_with_code_system}")
    print(f"  PDF export categories: {len(pdf_entities)} with {pdf_field_count} fields")
    print(f"  FHIR mention: 1 entity, 1 field")
    print()
    print("C-CDA Sections:")
    for s in ccda_sections:
        print(f"  {s['section_name']}: {len(s['fields'])} fields")

if __name__ == "__main__":
    main()
