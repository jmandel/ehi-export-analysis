#!/usr/bin/env python3
"""Parse all OmniMD EHI export artifacts and produce structured JSON inventories."""

import json
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent.parent.parent / "results" / "omnimd-inc--omnimd" / "downloads"
OUTPUT = Path(__file__).resolve().parent

# --- Parse EHI Export Word Document ---
def parse_ehi_doc():
    """Extract content from the EHI export .doc (actually .docx) file."""
    import zipfile
    doc_path = DOWNLOADS / "ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc"
    
    with zipfile.ZipFile(doc_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
    
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    paragraphs = []
    for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        line = ''
        for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            line += (t.text or '')
        if line.strip():
            paragraphs.append(line.strip())
    
    # Extract C-CDA sections
    ccda_sections = []
    in_sections = False
    for para in paragraphs:
        if 'Sections of EHI exported in CDA' in para:
            in_sections = True
            continue
        if in_sections:
            if para.startswith('The specifications') or para.startswith('FHIR:'):
                break
            if para.isupper() or (para[0].isupper() and len(para) > 3):
                ccda_sections.append(para)
    
    return {
        "source_file": "ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc",
        "document_title": "OmniMD 170.315(b)(10) Electronic Health Information Export Version 1.0",
        "file_size_bytes": os.path.getsize(doc_path),
        "format": "Microsoft Word 2007+ (docx)",
        "export_mechanisms": [
            {
                "name": "C-CDA Export",
                "format": "HL7 C-CDA XML (CDA 2.1)",
                "standard": "USCDI Version 1",
                "scope": "Single patient and patient population (bulk)",
                "sections": ccda_sections,
                "section_count": len(ccda_sections)
            },
            {
                "name": "FHIR Bulk Data",
                "format": "FHIR R4",
                "standard": "HL7 FHIR R4 4.0.1, US Core STU V3.1.1",
                "scope": "By reference to 170.315(g)(10)",
                "note": "No additional documentation provided; refers to g(10) specification"
            }
        ],
        "data_dictionary": False,
        "field_level_detail": False,
        "sample_data": False,
        "total_paragraphs": len(paragraphs),
        "full_text": paragraphs
    }


# --- Parse OpenAPI PDF ---
def parse_openapi_pdf():
    """Extract content from the OpenApi.pdf using pdftotext."""
    import subprocess
    pdf_path = DOWNLOADS / "OpenApi.pdf"
    
    result = subprocess.run(
        ['pdftotext', '-layout', str(pdf_path), '-'],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Get PDF metadata
    info_result = subprocess.run(
        ['pdfinfo', str(pdf_path)],
        capture_output=True, text=True
    )
    
    # Extract API endpoints
    endpoints = []
    for line in text.split('\n'):
        line = line.strip()
        match = re.match(r'(GET|POST|PUT|DELETE)\s+(api/\S+)', line)
        if match:
            endpoints.append({
                "method": match.group(1),
                "path": match.group(2)
            })
    
    # Extract GetPatientData parameters (C-CDA section toggles)
    section_params = []
    for line in text.split('\n'):
        line = line.strip()
        # Match parameter names like "AdvanceDirective", "Allergy", etc.
        match = re.match(r'[฀\u0e00]*\s*(\w+)\s*[–-]+\s*whether to return', line)
        if match:
            section_params.append(match.group(1))
    
    return {
        "source_file": "OpenApi.pdf",
        "document_title": "OmniMD EHR OpenAPI Version 1.1",
        "page_count": 9,
        "file_size_bytes": os.path.getsize(pdf_path),
        "purpose": "Documents (g)(7)/(g)(9) API, NOT the (b)(10) EHI export",
        "api_version": "1.1",
        "base_url": "https://prod.omnixchange.com/openAPI",
        "endpoints": endpoints,
        "endpoint_count": len(endpoints),
        "patient_data_section_toggles": section_params,
        "section_toggle_count": len(section_params),
        "output_format": "CDA 2.1 XML",
        "authentication": "Bearer token (OAuth2 password grant)",
        "pdf_info": info_result.stdout
    }


# --- Parse HTML API Help Page ---
def parse_api_help_html():
    """Parse the ASP.NET Web API Help page to extract endpoints."""
    html_path = DOWNLOADS / "openapi-help.html"
    with open(html_path, 'r') as f:
        content = f.read()
    
    # Extract endpoint categories and endpoints
    categories = {}
    current_category = None
    
    # Parse categories from h2 tags
    cat_pattern = re.compile(r'<h2 id="(\w+)">(\w+)</h2>')
    for match in cat_pattern.finditer(content):
        current_category = match.group(2)
        categories[current_category] = []
    
    # Parse endpoints from table rows
    endpoint_pattern = re.compile(r'<a href="[^"]*">((?:GET|POST|PUT|DELETE)\s+api/[^<]+)</a>')
    desc_pattern = re.compile(r'<p>([^<]+)</p>')
    
    # Walk through categories
    for cat_match in cat_pattern.finditer(content):
        cat_name = cat_match.group(2)
        cat_start = cat_match.end()
        # Find next category or end
        next_cat = cat_pattern.search(content, cat_start)
        cat_end = next_cat.start() if next_cat else len(content)
        cat_content = content[cat_start:cat_end]
        
        for ep_match in endpoint_pattern.finditer(cat_content):
            categories[cat_name].append({
                "endpoint": ep_match.group(1),
                "documented": False  # All say "No documentation available"
            })
    
    total_endpoints = sum(len(eps) for eps in categories.values())
    
    return {
        "source_file": "openapi-help.html",
        "page_title": "ASP.NET Web API Help Page",
        "categories": categories,
        "category_count": len(categories),
        "total_endpoints": total_endpoints,
        "documented_endpoints": 0,
        "note": "All endpoints show 'No documentation available' - default scaffold never populated"
    }


# --- Parse Interactive API UI HTML ---
def parse_api_ui_html():
    """Parse the interactive OpenAPI UI page."""
    html_path = DOWNLOADS / "openapiui.html"
    with open(html_path, 'r') as f:
        content = f.read()
    
    # Extract navigation sections
    nav_pattern = re.compile(r'<a href="#line\d+">([^<]+)</a>')
    sections = [m.group(1) for m in nav_pattern.finditer(content)]
    
    # Extract selectable sections from the "Selected Data" list
    sections_list = []
    sel_match = re.search(r'Sections - ([^<]+)', content)
    if sel_match:
        sections_list = [s.strip() for s in sel_match.group(1).split('|')]
    
    return {
        "source_file": "openapiui.html",
        "page_title": "OmniMD OpenAPI Version 1.0",
        "purpose": "Interactive API documentation for (g)(7)/(g)(9)",
        "stated_purpose": "satisfies the requirements of CEHRT Regulations § 170.315(g)(7), and § 170.315(g)(9)",
        "nav_sections": sections,
        "selectable_ccda_sections": sections_list,
        "selectable_section_count": len(sections_list),
        "has_login_form": True,
        "login_url": "https://prod.omnixchange.com/openAPI/Token",
        "copyright": "2017 © Copyright Integrated System Management Inc."
    }


# --- Build complete entity inventory ---
def build_entity_inventory(ehi_doc, openapi_pdf, api_ui):
    """Build a unified inventory of what the export covers.
    
    Since there's no data dictionary, the 'entities' are C-CDA sections.
    We document what's known about each from across all artifacts.
    """
    
    # Canonical list from the EHI export doc
    ccda_sections = ehi_doc["export_mechanisms"][0]["sections"]
    
    # Map section names to API parameter names from the PDF
    section_to_api_param = {}
    pdf_params = openapi_pdf["patient_data_section_toggles"]
    
    # Also get sections from the interactive UI
    ui_sections = api_ui.get("selectable_ccda_sections", [])
    
    entities = []
    for section in ccda_sections:
        entity = {
            "name": section,
            "source": "EHI Export Document",
            "format": "C-CDA XML section",
            "type": "C-CDA Section",
            "fields": "N/A - no field-level documentation",
            "field_count": None,
            "descriptions": False,
            "types_documented": False,
            "value_sets": False,
            "relationships": False,
            "sample_data": False,
            "category": classify_section(section)
        }
        entities.append(entity)
    
    # Check for additional sections in the OpenAPI PDF params that aren't in the EHI doc
    ehi_section_names_lower = [s.lower() for s in ccda_sections]
    additional_pdf_sections = []
    for param in pdf_params:
        param_lower = param.lower()
        # Check if this param maps to any existing section
        found = False
        for s in ehi_section_names_lower:
            if param_lower in s.lower().replace(' ', '') or s.lower().replace(' ', '') in param_lower:
                found = True
                break
        if not found:
            additional_pdf_sections.append(param)
    
    # Add additional sections found in PDF but not in EHI doc
    for section in additional_pdf_sections:
        entity = {
            "name": section,
            "source": "OpenApi.pdf (GetPatientData parameter)",
            "format": "C-CDA XML section",
            "type": "C-CDA Section (additional)",
            "fields": "N/A - no field-level documentation",
            "field_count": None,
            "descriptions": False,
            "types_documented": False,
            "value_sets": False,
            "relationships": False,
            "sample_data": False,
            "category": classify_section(section)
        }
        entities.append(entity)
    
    return {
        "vendor": "OmniMD Inc.",
        "product": "OmniMD",
        "export_type": "C-CDA / FHIR standard-based projection",
        "has_data_dictionary": False,
        "has_native_model": False,
        "total_entities": len(entities),
        "total_fields": 0,  # No field-level documentation
        "fields_with_descriptions": 0,
        "entities": entities,
        "additional_sections_in_pdf_only": additional_pdf_sections,
        "notes": [
            "No data dictionary exists - entities are C-CDA section names only",
            "No field-level detail, types, value sets, or relationships documented",
            "No sample data provided",
            "The EHI doc lists 20 C-CDA sections",
            f"The OpenAPI PDF adds {len(additional_pdf_sections)} additional section toggles not in EHI doc",
            "FHIR Bulk Data mentioned but deferred to g(10) with no additional detail"
        ]
    }


def classify_section(section_name):
    """Classify a C-CDA section into a domain category."""
    name = section_name.lower()
    if any(w in name for w in ['allerg', 'adverse']):
        return "Allergies"
    elif any(w in name for w in ['medication', 'med admin']):
        return "Medications"
    elif any(w in name for w in ['problem', 'diagnos']):
        return "Problems/Conditions"
    elif any(w in name for w in ['immuniz']):
        return "Immunizations"
    elif any(w in name for w in ['vital']):
        return "Vitals"
    elif any(w in name for w in ['lab', 'result']):
        return "Lab Results"
    elif any(w in name for w in ['procedure']):
        return "Procedures"
    elif any(w in name for w in ['encounter']):
        return "Encounters"
    elif any(w in name for w in ['advance directive']):
        return "Consents/Directives"
    elif any(w in name for w in ['family']):
        return "Family History"
    elif any(w in name for w in ['social']):
        return "Social History"
    elif any(w in name for w in ['functional', 'function status']):
        return "Functional Status"
    elif any(w in name for w in ['insurance', 'payer']):
        return "Insurance/Coverage"
    elif any(w in name for w in ['treatment', 'plan of care', 'careplan', 'care plan']):
        return "Care Plans"
    elif any(w in name for w in ['progress note', 'assessment', 'chief complaint', 'reason for visit']):
        return "Clinical Notes"
    elif any(w in name for w in ['instruction']):
        return "Patient Education"
    elif any(w in name for w in ['equipment']):
        return "Medical Equipment"
    elif any(w in name for w in ['referral']):
        return "Referrals"
    elif any(w in name for w in ['pregnancy']):
        return "Pregnancy"
    elif any(w in name for w in ['contact']):
        return "Demographics"
    elif any(w in name for w in ['appointment']):
        return "Scheduling"
    elif any(w in name for w in ['careteam', 'care team']):
        return "Care Team"
    elif any(w in name for w in ['clinic information']):
        return "Practice Information"
    elif any(w in name for w in ['planned']):
        return "Care Plans"
    else:
        return "Other"


def main():
    print("Parsing EHI Export Word Document...")
    ehi_doc = parse_ehi_doc()
    
    print("Parsing OpenAPI PDF...")
    openapi_pdf = parse_openapi_pdf()
    
    print("Parsing API Help HTML...")
    api_help = parse_api_help_html()
    
    print("Parsing API UI HTML...")
    api_ui = parse_api_ui_html()
    
    print("Building entity inventory...")
    inventory = build_entity_inventory(ehi_doc, openapi_pdf, api_ui)
    
    # Save all outputs
    with open(OUTPUT / "ehi-doc-parsed.json", 'w') as f:
        json.dump(ehi_doc, f, indent=2)
    
    with open(OUTPUT / "openapi-pdf-parsed.json", 'w') as f:
        json.dump(openapi_pdf, f, indent=2)
    
    with open(OUTPUT / "api-help-parsed.json", 'w') as f:
        json.dump(api_help, f, indent=2)
    
    with open(OUTPUT / "api-ui-parsed.json", 'w') as f:
        json.dump(api_ui, f, indent=2)
    
    with open(OUTPUT / "full-entity-inventory.json", 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"EHI Doc: {ehi_doc['export_mechanisms'][0]['section_count']} C-CDA sections listed")
    print(f"OpenAPI PDF: {openapi_pdf['endpoint_count']} API endpoints, {openapi_pdf['section_toggle_count']} section toggles")
    print(f"API Help: {api_help['total_endpoints']} endpoints across {api_help['category_count']} categories, {api_help['documented_endpoints']} documented")
    print(f"API UI: {api_ui['selectable_section_count']} selectable C-CDA sections")
    print(f"Entity Inventory: {inventory['total_entities']} entities (C-CDA sections)")
    print(f"  - Total fields: {inventory['total_fields']} (no field-level documentation exists)")
    print(f"  - Has data dictionary: {inventory['has_data_dictionary']}")
    print(f"  - Has native model: {inventory['has_native_model']}")
    print(f"  - Additional sections in PDF only: {inventory['additional_sections_in_pdf_only']}")


if __name__ == "__main__":
    main()
