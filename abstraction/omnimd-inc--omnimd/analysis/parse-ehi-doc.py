"""
Parse the OmniMD EHI Export Word document and OpenAPI PDF to extract
all structured information about the export: C-CDA sections, API parameters,
and endpoints. Produces entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import xml.etree.ElementTree as ET
import subprocess
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")
ANALYSIS = os.path.dirname(os.path.abspath(__file__))

# 1. Parse the Word document for C-CDA sections
def parse_docx():
    import zipfile
    docx_path = os.path.join(DOWNLOADS, "ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc")
    with zipfile.ZipFile(docx_path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    texts = []
    for p in tree.findall('.//w:p', ns):
        line = ''
        for r in p.findall('.//w:r', ns):
            for t in r.findall('w:t', ns):
                if t.text:
                    line += t.text
        if line.strip():
            texts.append(line.strip())
    return texts

# 2. Parse the PDF for API parameters
def parse_pdf():
    result = subprocess.run(
        ["pdftotext", "-layout", os.path.join(DOWNLOADS, "OpenApi.pdf"), "-"],
        capture_output=True, text=True
    )
    return result.stdout

# 3. Extract C-CDA sections from docx
def extract_ccda_sections(doc_lines):
    sections = []
    # The sections are listed as uppercase items after "Sections of EHI exported in CDA"
    in_sections = False
    for line in doc_lines:
        if "Sections of EHI exported" in line:
            in_sections = True
            continue
        if in_sections:
            if line.isupper() and len(line) > 3:
                sections.append(line.strip())
            elif "specifications" in line.lower() or "FHIR" in line:
                break
    return sections

# 4. Extract GetPatientData parameters from PDF
def extract_api_params(pdf_text):
    params = []
    lines = pdf_text.split('\n')
    in_params = False
    for line in lines:
        if "Data Action" in line and "Get Patient Data" in line:
            in_params = True
            continue
        if in_params and "Returns:" in line:
            break
        if in_params:
            # Match parameter lines like "ExternalPatientID–" or "Allergy–"
            m = re.match(r'\s*[\u0e00-\u0eff]*\s*(\w[\w\s]*?)[\s–\-]+(.+)', line)
            if m:
                name = m.group(1).strip()
                desc = m.group(2).strip()
                if name and len(name) > 1:
                    params.append({"name": name, "description": desc})
    return params

# 5. Extract all API endpoints from help HTML
def extract_endpoints():
    help_path = os.path.join(DOWNLOADS, "openapi-help.html")
    with open(help_path) as f:
        content = f.read()
    endpoints = re.findall(r'(GET|POST|PUT|DELETE)\s+(api/\w+/\w+[^<"]*)', content)
    result = []
    for method, path in endpoints:
        result.append({"method": method, "path": path.strip()})
    return result

# Build the inventory
doc_lines = parse_docx()
pdf_text = parse_pdf()

ccda_sections = extract_ccda_sections(doc_lines)
api_params = extract_api_params(pdf_text)
api_endpoints = extract_endpoints()

# Map C-CDA sections to standard categories and typical fields
# Since OmniMD provides NO field-level documentation, we can only document the sections themselves
ccda_section_mapping = {
    "ADVANCE DIRECTIVES": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Type", "Description", "Date", "Status"]},
    "ALLERGIES, ADVERSE REACTIONS, ALERTS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Substance", "Reaction", "Severity", "Status", "Date"]},
    "ASSESSMENTS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Assessment text"]},
    "ENCOUNTERS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Date", "Type", "Provider", "Location", "Diagnosis"]},
    "FAMILY HISTORY": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Relation", "Condition", "Age at onset"]},
    "FUNCTIONAL STATUS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Status", "Date", "Type"]},
    "IMMUNIZATIONS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Vaccine", "Date", "Status", "Lot number"]},
    "INSTRUCTIONS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Instruction text"]},
    "MEDICAL EQUIPMENT": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Device", "Date", "Status"]},
    "HISTORY OF MEDICATION": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Drug", "Dose", "Route", "Frequency", "Start/End date", "Status"]},
    "MEDICATION ADMINISTERED": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Drug", "Dose", "Route", "Date administered"]},
    "INSURANCE PROVIDERS": {"category": "Insurance", "uscdi_mapped": True, "typical_ccda_fields": ["Payer name", "Policy ID", "Group ID", "Coverage type"]},
    "TREATMENT PLAN": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Plan text", "Goals", "Instructions"]},
    "PROBLEM LIST": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Condition", "Code", "Status", "Onset date"]},
    "PROCEDURES": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Procedure", "Code", "Date", "Status"]},
    "PROGRESS NOTE": {"category": "Clinical", "uscdi_mapped": False, "typical_ccda_fields": ["Note text", "Date", "Author"]},
    "CHIEF COMPLAINT AND REASON FOR VISIT": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Complaint text"]},
    "LAB RESULTS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Test name", "Value", "Units", "Reference range", "Date"]},
    "SOCIAL HISTORY": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Observation", "Value", "Date"]},
    "VITAL SIGNS": {"category": "Clinical", "uscdi_mapped": True, "typical_ccda_fields": ["Type", "Value", "Units", "Date"]},
}

# Build entity inventory
entities = []
for section in ccda_sections:
    mapping = ccda_section_mapping.get(section, {"category": "Unknown", "uscdi_mapped": False, "typical_ccda_fields": []})
    entities.append({
        "entity_name": section,
        "source": "C-CDA Section (from EHI Export Word document)",
        "category": mapping["category"],
        "uscdi_mapped": mapping["uscdi_mapped"],
        "fields": [],  # No field-level documentation provided
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation provided. Section name only."
    })

# Also document the API parameters as they show what data can be toggled
api_param_entity = {
    "entity_name": "GetPatientData API Parameters",
    "source": "OpenApi.pdf (pages 5-6)",
    "category": "API",
    "uscdi_mapped": False,
    "fields": api_params,
    "field_count": len(api_params),
    "fields_with_descriptions": len([p for p in api_params if p.get("description")]),
    "fields_with_types": len([p for p in api_params if "true/false" in p.get("description", "")]),
    "notes": "Boolean toggle parameters for selecting which C-CDA sections to include in export"
}

full_inventory = {
    "vendor": "OmniMD Inc.",
    "product": "OmniMD",
    "export_format": "C-CDA XML (CDA 2.1) / FHIR R4 (by reference to g(10))",
    "documentation_version": "1.0",
    "total_ccda_sections": len(ccda_sections),
    "ccda_sections": ccda_sections,
    "total_api_params": len(api_params),
    "total_api_endpoints": len(api_endpoints),
    "entities": entities,
    "api_parameters": api_param_entity,
    "api_endpoints": api_endpoints,
    "data_dictionary_provided": False,
    "field_level_documentation": False,
    "sample_data_provided": False,
    "notes": [
        "OmniMD provides NO field-level documentation for the EHI export.",
        "The export is described only as a list of 20 C-CDA section names.",
        "No data dictionary, no schema, no field definitions, no sample data.",
        "FHIR export is mentioned but only by reference to g(10) specification.",
        "The GetPatientData API shows 33 boolean toggles for section selection.",
        "API returns CDA 2.1 XML format."
    ]
}

# Write full inventory
with open(os.path.join(ANALYSIS, "entity-inventory-full.json"), "w") as f:
    json.dump(full_inventory, f, indent=2)

# Build summary
summary = {
    "vendor": "OmniMD Inc.",
    "product": "OmniMD",
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "data_dictionary": False,
    "sample_data": False,
    "export_formats": ["C-CDA XML (CDA 2.1)", "FHIR R4 (by reference to g(10))"],
    "categories": {
        "Clinical": len([e for e in entities if e["category"] == "Clinical"]),
        "Insurance": len([e for e in entities if e["category"] == "Insurance"]),
    },
    "ccda_sections_listed": len(ccda_sections),
    "api_toggleable_sections": len([p for p in api_params if "true/false" in p.get("description", "")]),
    "api_total_endpoints": len(api_endpoints),
    "coverage_assessment": {
        "clinical_data": "Partial - 20 C-CDA sections cover USCDI clinical data",
        "billing_data": "Not covered - No billing/claims/charges entities",
        "specialty_data": "Not covered - No specialty-specific data entities",
        "patient_communications": "Not covered - No portal messages or communications",
        "documents_attachments": "Not covered - No scanned documents or media",
        "prescribing_detail": "Partial - Medication sections present but not detailed Rx records",
        "insurance": "Minimal - Only payer identity via C-CDA Payers section",
    }
}

with open(os.path.join(ANALYSIS, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print(f"C-CDA Sections found: {len(ccda_sections)}")
for s in ccda_sections:
    print(f"  - {s}")
print(f"\nAPI Parameters (GetPatientData): {len(api_params)}")
for p in api_params:
    print(f"  - {p['name']}: {p['description'][:80]}")
print(f"\nTotal API endpoints: {len(api_endpoints)}")
print(f"\nFiles written:")
print(f"  - entity-inventory-full.json")
print(f"  - entity-inventory-summary.json")
