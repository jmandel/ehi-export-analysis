#!/usr/bin/env python3
"""Parse all EndoVault EHI export artifacts and produce entity-inventory-full.json and summary."""

import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT_DIR = Path(".")

# --- Parse the EHI page HTML to extract the 22+ export sections ---
def parse_ehi_sections():
    with open(DOWNLOADS / "ephi-page.html") as f:
        content = f.read()
    
    # Find the section after "available sections" text and extract <li> items
    idx = content.find('available sections')
    if idx < 0:
        idx = content.find('choose')
    snippet = content[idx:idx+3000] if idx >= 0 else content
    items = re.findall(r'<li[^>]*>(.*?)</li>', snippet, re.DOTALL)
    sections = []
    exclude = {"Single/multi patient export", "Bulk EHI export"}
    for item in items:
        clean = re.sub(r'<[^>]+>', '', item).strip()
        if clean and clean not in exclude:
            sections.append(clean)
    return sections

# --- Parse the FHIR API PDF to extract resource types and bulk endpoints ---
def parse_fhir_pdf():
    result = subprocess.run(
        ["pdftotext", "-layout", str(DOWNLOADS / "170.315-g10-Standardized-API-FHIR-2.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Extract bulk data resource endpoints
    bulk_resources = []
    for match in re.finditer(r'(\w[\w-]*)-bulkfile\.ndjson', text):
        name = match.group(1)
        if name not in [r["endpoint_name"] for r in bulk_resources]:
            bulk_resources.append({
                "endpoint_name": name,
                "url_pattern": f"<base bulk url>/{name}-bulkfile.ndjson",
            })
    
    # Extract individual API resources from Table 4-1
    api_resources = []
    in_table = False
    for line in text.split('\n'):
        if 'REST Resource' in line and 'Description' in line:
            in_table = True
            continue
        if in_table:
            if 'Table 4-1' in line:
                break
            m = re.match(r'\s*/(\w+)\s+(.*)', line)
            if m:
                api_resources.append({
                    "resource": m.group(1),
                    "description": m.group(2).strip()
                })
    
    # Count pages
    info = subprocess.run(["pdfinfo", str(DOWNLOADS / "170.315-g10-Standardized-API-FHIR-2.pdf")],
                          capture_output=True, text=True)
    pages = 0
    for line in info.stdout.split('\n'):
        if line.startswith('Pages:'):
            pages = int(line.split(':')[1].strip())
    
    return {
        "total_pages": pages,
        "bulk_resources": bulk_resources,
        "api_resources": api_resources,
        "bulk_resource_count": len(bulk_resources),
        "api_resource_count": len(api_resources),
    }

# --- Build entity inventory ---
def build_entity_inventory(ehi_sections, fhir_data):
    """Map the export data into entity-inventory format.
    Since the export is FHIR-based with no product-specific data dictionary,
    each bulk FHIR resource type is an "entity" with fields from the FHIR spec."""
    
    # Map bulk resource names to FHIR resource types
    resource_map = {
        "allergyintolerance": "AllergyIntolerance",
        "careplan": "CarePlan",
        "careteam": "CareTeam",
        "condition": "Condition",
        "device": "Device",
        "diagnosticreport": "DiagnosticReport",
        "documentreference": "DocumentReference",
        "encounter": "Encounter",
        "goal": "Goal",
        "immunization": "Immunization",
        "medicationrequest": "MedicationRequest",
        "observation": "Observation",
        "organization": "Organization",
        "patient": "Patient",
        "practitioner": "Practitioner",
        "procedure": "Procedure",
        "provenance": "Provenance",
        "relatedperson": "RelatedPerson",
        "servicerequest": "ServiceRequest",
    }
    
    # Map C-CDA sections to USCDI categories
    ccda_section_mapping = {
        "Allergies": "Allergies & Intolerances",
        "Encounter": "Encounters",
        "Immunizations": "Immunizations",
        "Medications": "Medications",
        "Plan of treatment": "Assessment & Plan of Treatment",
        "Referral reason": "Orders / Referrals",
        "Active problems": "Problems",
        "Reason for visit": "Encounters",
        "Implants": "Medical Devices",
        "Health concerns": "Health Status Assessments",
        "Procedures": "Procedures",
        "Functional status": "Health Status Assessments",
        "Results": "Laboratory / Clinical Tests",
        "Social history": "Health Status Assessments",
        "Vitals": "Vital Signs",
        "Goals": "Goals & Preferences",
        "Discharge instructions": "Clinical Notes",
        "Assessments": "Health Status Assessments",
        "Cognitive status": "Health Status Assessments",
        "Media": "Clinical Notes / Documents",
        "Diagnostic Report": "Diagnostic Imaging",
        "Documents": "Clinical Notes / Documents",
        "Service Request": "Orders / Referrals",
    }
    
    entities = []
    for br in fhir_data["bulk_resources"]:
        name = br["endpoint_name"]
        fhir_type = resource_map.get(name, name.title())
        entities.append({
            "entity_name": fhir_type,
            "source": "FHIR Bulk Data API",
            "endpoint": br["url_pattern"],
            "format": "NDJSON",
            "fhir_profile": f"US Core {fhir_type}" if fhir_type not in ["Organization", "Provenance"] else f"FHIR R4 {fhir_type}",
            "fields_documented": "No (standard FHIR spec only, no vendor-specific field documentation)",
            "field_count": "N/A - no product-specific data dictionary",
            "description_quality": "None - relies on generic FHIR R4 / US Core spec",
            "vendor_extensions": "None observed in sample data",
            "category": "USCDI / US Core",
        })
    
    return {
        "export_name": "EndoVault EHI Export",
        "export_format": "FHIR R4 NDJSON (bulk) / C-CDA 2.1 XML (single/multi patient)",
        "data_dictionary_provided": False,
        "product_specific_schema": False,
        "total_entities": len(entities),
        "total_fields": "N/A - no product-specific data dictionary provided",
        "fields_with_descriptions": "N/A",
        "entities": entities,
        "ccda_sections": [
            {"section_name": s, "uscdi_category": ccda_section_mapping.get(s, "Unknown")}
            for s in ehi_sections
        ],
        "ccda_section_count": len(ehi_sections),
    }

def build_summary(inventory):
    """Build summary statistics."""
    return {
        "product": "EndoVault",
        "vendor": "EndoSoft, LLC",
        "export_formats": ["FHIR R4 NDJSON (bulk)", "C-CDA 2.1 XML (single/multi-patient)"],
        "total_fhir_bulk_resources": inventory["total_entities"],
        "total_ccda_sections": inventory["ccda_section_count"],
        "data_dictionary_provided": False,
        "product_specific_field_documentation": False,
        "vendor_extensions_observed": False,
        "fhir_bulk_resources": [e["entity_name"] for e in inventory["entities"]],
        "ccda_sections": [s["section_name"] for s in inventory["ccda_sections"]],
        "uscdi_categories_covered": sorted(set(
            s["uscdi_category"] for s in inventory["ccda_sections"] if s["uscdi_category"] != "Unknown"
        )),
        "domains_missing_vs_product": [
            "Billing / charges / time-and-material tracking",
            "Procedure images and video (endoscopy)",
            "Pathology requisitions and results (beyond DiagnosticReport)",
            "Oncology-specific data (staging, chemo regimens, MAR)",
            "Scheduling / recall management",
            "Inventory / scope tracking",
            "Patient portal messages",
            "Custom specialty templates and forms",
            "Electronic nursing record (ENR) intra-procedure data",
            "Consent forms and electronic signatures",
        ],
        "assessment": {
            "coverage_breadth": "Minimal/stub/unclear",
            "export_approach": "Repackaged existing export",
            "rationale": "The (b)(10) export is the vendor's existing (g)(10) FHIR API and C-CDA export relabeled. 18 FHIR resource types match standard US Core profiles exactly. No product-specific data dictionary, no vendor extensions, no coverage of billing, endoscopy images/video, oncology-specific data, pathology details, ENR data, or any other specialty content that EndoVault stores.",
        }
    }

if __name__ == "__main__":
    print("Parsing EHI page sections...")
    sections = parse_ehi_sections()
    print(f"  Found {len(sections)} C-CDA export sections: {sections}")
    
    print("Parsing FHIR API PDF...")
    fhir_data = parse_fhir_pdf()
    print(f"  PDF: {fhir_data['total_pages']} pages")
    print(f"  Bulk resources: {fhir_data['bulk_resource_count']}")
    print(f"  API resources: {fhir_data['api_resource_count']}")
    
    print("Building entity inventory...")
    inventory = build_entity_inventory(sections, fhir_data)
    
    with open(OUTPUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"  Wrote entity-inventory-full.json")
    
    print("Building summary...")
    summary = build_summary(inventory)
    
    with open(OUTPUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Wrote entity-inventory-summary.json")
    
    # Print key stats
    print("\n=== KEY STATS ===")
    print(f"FHIR Bulk Resource Types: {inventory['total_entities']}")
    print(f"C-CDA Sections: {inventory['ccda_section_count']}")
    print(f"Data Dictionary: {'Yes' if inventory['data_dictionary_provided'] else 'No'}")
    print(f"Product-Specific Schema: {'Yes' if inventory['product_specific_schema'] else 'No'}")
    print(f"Vendor Extensions: None observed")
    for r in fhir_data["bulk_resources"]:
        print(f"  Bulk: {r['endpoint_name']}")
    for s in sections:
        print(f"  C-CDA: {s}")
