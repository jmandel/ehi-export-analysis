#!/usr/bin/env python3
"""Parse the CareCloud Prime EHI export PDF text to extract C-CDA section structure,
count data elements per section, and identify code systems used."""

import re
import json

# Read the extracted PDF text
with open("/tmp/carecloud_ehi.txt", "r") as f:
    text = f.read()

# Extract C-CDA sections and their data elements (pages 6-10)
# Sections are identified by their template IDs in brackets or by header names
sections = []
current_section = None
current_elements = []

lines = text.split("\n")
for line in lines:
    line = line.strip()
    if not line or "Page " in line and " of 12" in line:
        continue

    # Detect section headers - they have template IDs in brackets or are known headers
    section_match = re.match(r'^(.+?)\s*\[([0-9.:]+)\s*(?::\s*[\d-]+)?\]', line)
    header_match = re.match(r'^(Patient Demographics/Information|Provider\'s name and office contact information|'
                           r'Chief Complaint and Reason for visit|Laboratory Tests|Laboratory Information|'
                           r'Date and Location of visit)', line)
    
    if section_match:
        if current_section:
            sections.append({"section": current_section, "template_id": current_template, 
                           "elements": current_elements})
        current_section = section_match.group(1).strip()
        current_template = section_match.group(2).strip()
        current_elements = []
    elif header_match:
        if current_section:
            sections.append({"section": current_section, "template_id": current_template,
                           "elements": current_elements})
        current_section = header_match.group(1).strip()
        current_template = None
        current_elements = []
    elif current_section:
        # Check if line looks like a data element (not a code system OID or page marker)
        if (line and 
            not line.startswith("Data Elements") and 
            not line.startswith("XPATH") and 
            not line.startswith("Code System") and
            not line.startswith("§170.315") and
            not line.startswith("Export") and
            not line.startswith("Standard Referenced") and
            not line.startswith("Sections in the CCD") and
            not line.startswith("CCD Output Format") and
            not line.startswith("(Diagnostic tests") and
            not re.match(r'^2\.16\.840', line) and
            not re.match(r'^and\s+2\.16', line) and
            not re.match(r'^\(translation', line) and
            not re.match(r'^or\s+2\.16', line)):
            # This might be a data element name or a code system name
            # Filter out code system names that appear in the rightmost column
            known_code_systems = ["SNOMED", "ICD10", "CPT", "CPT-4", "LOINC", "RxNorm", "NDC",
                                "CVX", "HCPCS", "AdministrativeGender", "SNOMED and ICD10",
                                "RxNorm and NDC", "CVX and CPT-4", "CPT-4 or SNOMED orHCPCS",
                                "Race & Ethnicity -", "CDC", "National Cancer", "Institute (NCI)",
                                "Thesaurus"]
            if line not in known_code_systems and not line.startswith("-"):
                current_elements.append(line)

# Don't forget the last section
if current_section:
    sections.append({"section": current_section, "template_id": current_template,
                   "elements": current_elements})

# Clean up - manually define the sections more precisely based on the PDF structure
ccda_sections = [
    {"section": "Patient Demographics/Information", "template_id": None, 
     "elements": ["Patient Name", "Sex", "Date of Birth", "Race", "Ethnicity", "Preferred Language"],
     "code_systems": ["AdministrativeGender", "Race & Ethnicity - CDC"]},
    {"section": "Provider's name and office contact information", "template_id": None,
     "elements": ["Performer Name", "Performer Telecom", "Performer Address"],
     "code_systems": []},
    {"section": "Date and Location of visit", "template_id": "2.16.840.1.113883.10.20.22.2.22.1",
     "elements": ["Encounter effectiveTime", "Encounter participant address"],
     "code_systems": []},
    {"section": "Chief Complaint and Reason for visit", "template_id": "2.16.840.1.113883.10.20.22.2.13",
     "elements": ["Patient visit details/complaints"],
     "code_systems": []},
    {"section": "Encounters", "template_id": "2.16.840.1.113883.10.20.22.2.22.1",
     "elements": ["Encounter Code and Description", "Performer", "Diagnosis", "Location", "Date"],
     "code_systems": ["CPT", "SNOMED", "ICD10"]},
    {"section": "Immunizations", "template_id": "2.16.840.1.113883.10.20.22.2.2.1",
     "elements": ["Vaccine", "Date", "Status", "Route", "Site", "Manufacturer", "Dose", "Lot Number", "Notes"],
     "code_systems": ["CVX", "CPT-4", "NCI Thesaurus", "SNOMED"]},
    {"section": "Instructions", "template_id": "2.16.840.1.113883.10.20.22.2.45",
     "elements": ["Patient Instructions/FollowupReasons"],
     "code_systems": ["SNOMED"]},
    {"section": "Treatment Plan", "template_id": "2.16.840.1.113883.10.20.22.2.10",
     "elements": ["Planned Observation", "Planned Date"],
     "code_systems": ["LOINC"]},
    {"section": "Social History", "template_id": "2.16.840.1.113883.10.20.22.2.17",
     "elements": ["Social History Observation", "Description", "Dates Observed"],
     "code_systems": ["LOINC", "SNOMED"]},
    {"section": "Problems", "template_id": "2.16.840.1.113883.10.20.22.2.5.1",
     "elements": ["Problem", "Status", "Active date"],
     "code_systems": ["SNOMED", "ICD10"]},
    {"section": "Medications", "template_id": "2.16.840.1.113883.10.20.22.2.1.1",
     "elements": ["Medication", "Directions", "Start Date", "End Date", "Status"],
     "code_systems": ["RxNorm", "NDC"]},
    {"section": "Medication Allergies", "template_id": "2.16.840.1.113883.10.20.22.2.6.1",
     "elements": ["Substance", "Reaction", "Severity", "Status"],
     "code_systems": ["RxNorm", "SNOMED"]},
    {"section": "Laboratory Tests", "template_id": None,
     "elements": ["Test Code", "Code System", "Name", "Date"],
     "code_systems": ["LOINC"]},
    {"section": "Laboratory Information", "template_id": None,
     "elements": ["Lab Name", "Lab Address", "Test Report Date", "Test Performed", "Specimen Source"],
     "code_systems": []},
    {"section": "Laboratory value(s)/result(s)", "template_id": "2.16.840.1.113883.10.20.22.2.3.1",
     "elements": ["Result Type", "Result Value", "Relevant Reference Range", "Interpretation", "Date"],
     "code_systems": ["LOINC"]},
    {"section": "Vitals", "template_id": "2.16.840.1.113883.10.20.22.2.4.1",
     "elements": ["Observation", "Observation Date/Time"],
     "code_systems": ["LOINC"]},
    {"section": "Goal", "template_id": "2.16.840.1.113883.10.20.22.2.60",
     "elements": ["Goal", "Value", "Date"],
     "code_systems": []},
    {"section": "Procedures", "template_id": "2.16.840.1.113883.10.20.22.2.7.1",
     "elements": ["Procedure", "Date"],
     "code_systems": ["CPT-4", "SNOMED", "HCPCS"]},
    {"section": "Care team member(s)", "template_id": "2.16.840.1.113883.10.20.22.2.500",
     "elements": ["Care Giver Name", "Specialty", "Date"],
     "code_systems": []},
    {"section": "Reason for Referral", "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
     "elements": ["Reason for visit"],
     "code_systems": ["SNOMED"]},
    {"section": "Medical Equipment", "template_id": "2.16.840.1.113883.10.20.22.2.23",
     "elements": ["Implanted Device", "GMDN PT Description"],
     "code_systems": ["SNOMED"]},
    {"section": "Mental Status", "template_id": "2.16.840.1.113883.10.20.22.2.56",
     "elements": ["Assessment", "Assessment Date", "Results", "Comments"],
     "code_systems": ["SNOMED"]},
    {"section": "Functional Status", "template_id": "2.16.840.1.113883.10.20.22.2.14",
     "elements": ["Assessment", "Assessment Date", "Results", "Comments"],
     "code_systems": ["SNOMED"]},
    {"section": "Health Concern", "template_id": "2.16.840.1.113883.10.20.22.2.58",
     "elements": ["Concern / Observation", "Status", "Date"],
     "code_systems": ["SNOMED"]},
]

# PDF export categories (page 11)
pdf_exports = [
    {"section": "Patient Demographic/Insurance", "format": "PDF", "description": "demographics and insurance details", "fields_documented": 0},
    {"section": "Advance Directive", "format": "PDF", "description": "Advance Directive", "fields_documented": 0},
    {"section": "Appointments", "format": "PDF", "description": "appointments", "fields_documented": 0},
    {"section": "Provider-to-Patient Messages", "format": "PDF", "description": "messages", "fields_documented": 0},
    {"section": "Billing Data (Claim)", "format": "PDF", "description": "billing data (CPT, ICD, Modifier)", "fields_documented": 3},
    {"section": "Documents", "format": "PDF", "description": "signed progress notes, lab results, radiology reports, scanned/uploaded documents", "fields_documented": 0},
]

# Summary statistics
total_ccda_sections = len(ccda_sections)
total_ccda_elements = sum(len(s["elements"]) for s in ccda_sections)
total_pdf_categories = len(pdf_exports)
unique_code_systems = set()
for s in ccda_sections:
    for cs in s["code_systems"]:
        unique_code_systems.add(cs)

print("=" * 60)
print("CareCloud Prime EHI Export - Data Dictionary Analysis")
print("=" * 60)
print(f"\nC-CDA Sections: {total_ccda_sections}")
print(f"Total C-CDA Data Elements: {total_ccda_elements}")
print(f"PDF Export Categories: {total_pdf_categories}")
print(f"Unique Code Systems Referenced: {len(unique_code_systems)}")
print(f"Code Systems: {', '.join(sorted(unique_code_systems))}")

print("\n--- C-CDA Sections Detail ---")
for s in ccda_sections:
    tid = s["template_id"] or "N/A"
    cs = ", ".join(s["code_systems"]) if s["code_systems"] else "None"
    print(f"  {s['section']} [{tid}]: {len(s['elements'])} elements, Code systems: {cs}")

print("\n--- PDF Export Categories ---")
for p in pdf_exports:
    print(f"  {p['section']}: {p['description']} (fields documented: {p['fields_documented']})")

print(f"\nTotal documented data elements (C-CDA + PDF named fields): {total_ccda_elements + sum(p['fields_documented'] for p in pdf_exports)}")

# Save structured output
output = {
    "ccda_sections": ccda_sections,
    "pdf_exports": pdf_exports,
    "summary": {
        "ccda_section_count": total_ccda_sections,
        "ccda_element_count": total_ccda_elements,
        "pdf_category_count": total_pdf_categories,
        "unique_code_systems": sorted(unique_code_systems),
        "total_documented_elements": total_ccda_elements + sum(p['fields_documented'] for p in pdf_exports)
    }
}

with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/carecloud-inc--carecloud-prime/analysis/ccda_dictionary_parsed.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nOutput saved to analysis/ccda_dictionary_parsed.json")
