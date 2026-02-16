"""
Parse the talkEHR b(10) EHI Export Documentation PDF to extract:
- CCD sections and their data elements
- Non-CCD export categories  
- Count of data elements per section
"""
import subprocess
import json
import re

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/carecloud-inc--talkehr/downloads/talkEHR-b10-EHI-Export-Documentation.pdf"

result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Parse CCD sections
ccd_sections = []
current_section = None
current_elements = []

lines = text.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Match CCD section headers like "Problems [2.16.840..."
    section_match = re.match(r'^(.+?)\s*\[([0-9.:]+)\s*(?::\s*[0-9-]+)?\]', line)
    if section_match:
        if current_section:
            ccd_sections.append({
                "section": current_section,
                "oid": current_oid,
                "data_elements": current_elements
            })
        current_section = section_match.group(1).strip()
        current_oid = section_match.group(2).strip()
        current_elements = []
        continue
    
    # Match section headers without OIDs (like "Patient Demographics/Information")
    if line in ["Patient Demographics/Information", "Provider's name and office contact information",
                "Laboratory Tests", "Laboratory Information"]:
        if current_section:
            ccd_sections.append({
                "section": current_section,
                "oid": current_oid if 'current_oid' in dir() else None,
                "data_elements": current_elements
            })
        current_section = line
        current_oid = None
        current_elements = []
        continue
    
    # Skip page numbers, headers
    if re.match(r'^Page \d+ of \d+$', line):
        continue
    if "§170.315(b)(10)" in line:
        continue
    if line in ["Export – Documentation", "Export- Documentation", "Data Elements",
                "XPATH / Entry", "Code System", "Code System Name",
                "Sections in the CCD output", "CCD Output Format",
                "Standard Referenced:"]:
        continue
    if "HL7® Implementation Guide" in line:
        continue
    
    # Data elements are typically the first column items
    if current_section and line and not line.startswith("2.16.840") and not line.startswith("0.22"):
        # Skip entries that are just OIDs, code system names, or continuations
        if re.match(r'^[0-9.:]+$', line):
            continue
        if line in ["CPT", "SNOMED", "LOINC", "RxNorm", "CVX", "NDC", "HCPCS",
                     "SNOMED and ICD10", "RxNorm and NDC", "CVX and CPT-4",
                     "CPT-4 or SNOMED orHCPCS", "AdministrativeGender",
                     "Race & Ethnicity -", "CDC", "(translation code)",
                     "National Cancer", "Institute (NCI)", "Thesaurus"]:
            continue
        current_elements.append(line)

if current_section:
    ccd_sections.append({
        "section": current_section,
        "oid": current_oid,
        "data_elements": current_elements
    })

# Clean up - manually define the CCD sections based on careful reading
ccd_sections_clean = [
    {"section": "Patient Demographics/Information", "elements": [
        "Patient Name", "Sex", "Date of Birth", "Race", "Ethnicity", "Preferred Language"
    ]},
    {"section": "Provider's name and office contact information", "elements": [
        "Performer Name", "Performer Telecom", "Performer Address"
    ]},
    {"section": "Date and Location of visit", "elements": [
        "Encounter Date/Time", "Encounter Location"
    ]},
    {"section": "Chief Complaint and Reason for visit", "elements": [
        "Patient visit details/complaints"
    ]},
    {"section": "Encounters", "elements": [
        "Encounter Code and Description", "Performer", "Diagnosis", "Location", "Date"
    ]},
    {"section": "Immunizations", "elements": [
        "Vaccine", "Date", "Status", "Route", "Site", "Manufacturer", "Dose", "Lot Number", "Notes"
    ]},
    {"section": "Instructions", "elements": [
        "Patient Instructions/FollowupReasons"
    ]},
    {"section": "Treatment Plan", "elements": [
        "Planned Observation", "Planned Date"
    ]},
    {"section": "Social History", "elements": [
        "Social History Observation", "Description", "Dates Observed"
    ]},
    {"section": "Problems", "elements": [
        "Problem", "Status", "Active date"
    ]},
    {"section": "Medications", "elements": [
        "Medication", "Directions", "Start Date", "End Date", "Status"
    ]},
    {"section": "Medication Allergies", "elements": [
        "Substance", "Reaction", "Severity", "Status"
    ]},
    {"section": "Laboratory Tests", "elements": [
        "Test Code", "Code System", "Name", "Date"
    ]},
    {"section": "Laboratory Information", "elements": [
        "Lab Name", "Lab Address", "Test Report Date", "Test Performed", "Specimen Source"
    ]},
    {"section": "Laboratory value(s)/result(s)", "elements": [
        "Result Type", "Result Value", "Relevant Reference Range", "Interpretation", "Date"
    ]},
    {"section": "Vitals", "elements": [
        "Observation", "Observation Date/Time"
    ]},
    {"section": "Goal", "elements": [
        "Goal", "Value", "Date"
    ]},
    {"section": "Procedures", "elements": [
        "Procedure", "Date"
    ]},
    {"section": "Care team member(s)", "elements": [
        "Care Giver Name", "Specialty", "Date"
    ]},
    {"section": "Reason for Referral", "elements": [
        "Reason for visit"
    ]},
    {"section": "Medical Equipment", "elements": [
        "Implanted Device", "GMDN PT Description"
    ]},
    {"section": "Mental Status", "elements": [
        "Assessment", "Assessment Date", "Results", "Comments"
    ]},
    {"section": "Functional Status", "elements": [
        "Assessment", "Assessment Date", "Results", "Comments"
    ]},
    {"section": "Health Concern", "elements": [
        "Concern / Observation", "Status", "Date"
    ]},
]

# Non-CCD export categories (from page 11)
non_ccd_exports = [
    {"category": "Patient Demographic/Insurance", "format": "PDF", 
     "description": "Demographics and insurance details"},
    {"category": "Advance Directive", "format": "PDF",
     "description": "Advance Directive data"},
    {"category": "Appointments", "format": "PDF",
     "description": "Appointment data"},
    {"category": "Provider-to-Patient Messages", "format": "PDF",
     "description": "Secure messages between providers and patients"},
    {"category": "Billing Data (Claim)", "format": "PDF",
     "description": "Billing data including CPT, ICD, Modifier"},
    {"category": "Documents", "format": "PDF",
     "description": "Signed progress notes, lab results, radiology reports, scanned/uploaded documents"},
]

# Summary
total_ccd_sections = len(ccd_sections_clean)
total_ccd_elements = sum(len(s["elements"]) for s in ccd_sections_clean)
total_non_ccd = len(non_ccd_exports)

output = {
    "summary": {
        "total_ccd_sections": total_ccd_sections,
        "total_ccd_data_elements": total_ccd_elements,
        "total_non_ccd_categories": total_non_ccd,
        "ccd_format": "C-CDA XML (§170.205(a)(4), CDA R2 C-CDA 2.1 DSTU August 2015)",
        "non_ccd_format": "PDF",
        "additional_export": "FHIR Bulk Data (mentioned but not detailed)",
    },
    "ccd_sections": ccd_sections_clean,
    "non_ccd_exports": non_ccd_exports,
    "export_mechanisms": {
        "single_patient": "CCDA Export Tab → select patient → Generate → Download XML",
        "bulk_patient": "Data Portability Tab → select date range → Export → ZIP of XMLs",
        "fhir": "FHIR server single-patient DocumentReference + FHIR Bulk Data for population",
        "reports_section": "Reports section for appointments, demographics, insurance, messages, claims in PDF",
    }
}

print(json.dumps(output, indent=2))

# Print summary
print(f"\n=== SUMMARY ===")
print(f"CCD Sections: {total_ccd_sections}")
print(f"CCD Data Elements: {total_ccd_elements}")
print(f"Non-CCD Export Categories: {total_non_ccd}")
print(f"Total documented data elements: {total_ccd_elements} (CCD only; non-CCD categories lack field-level detail)")

print(f"\n=== CCD SECTIONS ===")
for s in ccd_sections_clean:
    print(f"  {s['section']}: {len(s['elements'])} elements")

print(f"\n=== NON-CCD EXPORTS (PDF format, no field-level detail) ===")
for e in non_ccd_exports:
    print(f"  {e['category']}: {e['description']}")
