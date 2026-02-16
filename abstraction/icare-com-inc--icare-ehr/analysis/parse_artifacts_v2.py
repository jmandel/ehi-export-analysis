#!/usr/bin/env python3
"""
Thorough parse of the iCare API Guide PDF text and EHI export HTML page.
Extracts all documented data categories, their FHIR resource mappings,
and fields visible in example JSON responses.
"""

import json
import re
from pathlib import Path

ANALYSIS_DIR = Path(".")
DOWNLOADS = Path("../downloads")

def extract_sections_from_api_guide():
    """Extract each data category section with its description and example JSON."""
    text = (ANALYSIS_DIR / "api-guide-full-text.txt").read_text()
    
    # Define the categories in order as they appear in the API guide
    categories = [
        ("patient", "Patient demographics"),
        ("smokingStatus", "Smoking status / social history"),
        ("problem", "Problems / conditions / diagnoses"),
        ("medication", "Medications / prescriptions"),
        ("medAllergy", "Medication allergies"),
        ("labTest", "Lab tests / diagnostic reports"),
        ("labResult", "Lab results / observations"),
        ("vital", "Vital signs"),
        ("procedure", "Procedures"),
        ("careTeam", "Care team members"),
        ("immunization", "Immunizations"),
        ("device", "Implanted devices"),
        ("planOfTreatment", "Plan of treatment / care plans"),
        ("assessment", "Assessments / clinical notes"),
        ("goal", "Goals"),
        ("healthConcern", "Health concerns"),
    ]
    
    results = []
    for i, (cat, desc) in enumerate(categories):
        # Find the output description for this category
        # Look for the pattern: "Output\nA FHIR Bundle..." after the category heading
        # Use a broad search for the text between this category's output and the next category
        if i < len(categories) - 1:
            next_cat = categories[i + 1][0]
            pattern = rf'{re.escape(cat)}\s*\n\s*Input Examples(.*?)\n{re.escape(next_cat)}\s*\n'
        else:
            pattern = rf'{re.escape(cat)}\s*\n\s*Input Examples(.*?)All Criteria Data Request'
        
        match = re.search(pattern, text, re.DOTALL)
        section_text = match.group(1) if match else ""
        
        # Extract the Output description paragraph
        output_match = re.search(r'Output\s*\n(.*?)(?=\n\s*\{)', section_text, re.DOTALL)
        output_desc = output_match.group(1).strip() if output_match else ""
        # Clean up
        output_desc = re.sub(r'\s+', ' ', output_desc)
        output_desc = re.sub(r'© Copyright.*?reserved\.', '', output_desc).strip()
        output_desc = re.sub(r'iCare\.com Application Programming Interface Guide', '', output_desc).strip()
        
        # Extract all JSON keys from example responses
        fields = set()
        # Find JSON-like content  
        json_matches = re.findall(r'"(\w+)"\s*:', section_text)
        for f in json_matches:
            if f not in ('resourceType', 'type', 'entry', 'resource', 'searchset'):
                fields.add(f)
        
        # Map to FHIR resource types
        fhir_types = set()
        rt_matches = re.findall(r'"resourceType"\s*:\s*"(\w+)"', section_text)
        for rt in rt_matches:
            if rt != "Bundle":
                fhir_types.add(rt)
        
        results.append({
            "category": cat,
            "category_description": desc,
            "fhir_resource_types": sorted(list(fhir_types)),
            "output_description": output_desc,
            "example_fields": sorted(list(fields)),
            "field_count": len(fields),
        })
    
    return results

def parse_ehi_page_resources():
    """Parse the FHIR resources listed on the EHI export HTML page."""
    html = (DOWNLOADS / "ehi-export-page.html").read_text()
    
    resources = []
    sections = re.split(r'<h4>', html)
    for section in sections[1:]:
        name_match = re.match(r'(\w+)</h4>', section)
        if not name_match:
            continue
        name = name_match.group(1)
        
        # Extract query pattern
        uri_match = re.search(r'URI:\s*(\S+\?\S+)', section)
        query_pattern = uri_match.group(1) if uri_match else ""
        # Clean HTML entities
        query_pattern = query_pattern.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        
        resources.append({
            "resource_type": name,
            "query_pattern": query_pattern
        })
    
    return resources

def build_full_inventory():
    """Build the complete entity inventory."""
    
    api_sections = extract_sections_from_api_guide()
    ehi_resources = parse_ehi_page_resources()
    
    # Read capability statement
    with open(DOWNLOADS / "fhir-capability-statement.json") as f:
        cs = json.load(f)
    
    # Build entities from API guide categories
    entities = []
    for section in api_sections:
        entity = {
            "entity_name": section["category"],
            "description": section["category_description"],
            "fhir_resource_types": section["fhir_resource_types"],
            "output_description": section["output_description"],
            "field_count": section["field_count"],
            "fields": [
                {
                    "name": f,
                    "type": "FHIR (inferred from example)",
                    "description": "",
                    "has_description": False
                }
                for f in section["example_fields"]
            ],
            "fields_with_descriptions": 0,
            "source": "iCare-API-Guide.pdf",
            "category": classify_domain(section["category"])
        }
        entities.append(entity)
    
    # Add "All Criteria" C-CDA entity
    entities.append({
        "entity_name": "allCriteria (C-CDA)",
        "description": "All clinical data as a C-CDA XML document combining all 16 categories above",
        "fhir_resource_types": [],
        "output_description": "CCDA compliant XML document containing all clinical data categories",
        "field_count": 0,
        "fields": [],
        "fields_with_descriptions": 0,
        "source": "iCare-API-Guide.pdf",
        "category": "All Clinical (C-CDA)"
    })
    
    # Build domain summary
    domain_summary = {}
    for e in entities:
        cat = e["category"]
        if cat not in domain_summary:
            domain_summary[cat] = {"entity_count": 0, "total_fields": 0}
        domain_summary[cat]["entity_count"] += 1
        domain_summary[cat]["total_fields"] += e["field_count"]
    
    total_fields = sum(e["field_count"] for e in entities)
    
    inventory = {
        "product": "iCare EHR",
        "version": "Version 2",
        "chpl_id": "15.04.04.2617.iCar.02.00.1.200220",
        "analysis_date": "2026-02-16",
        "sources": {
            "ehi_export_page": {
                "url": "https://icare.com/developers/ehi_export/",
                "last_modified": "2025-10-18",
                "description": "Single HTML page describing 3 export methods and 13 FHIR resource types"
            },
            "api_guide_pdf": {
                "url": "https://icare.com/wp-content/uploads/2023/09/iCare.com-Application-Programming-Interface-Guide.pdf",
                "pages": 67,
                "copyright": 2020,
                "description": "Proprietary REST API guide with 16 data categories, input/output examples"
            },
            "fhir_capability_statement": {
                "url": "https://sandbox-r4.interopengine.com/fhir/r4/icare/metadata",
                "software": cs.get("software", {}).get("name"),
                "fhir_version": cs.get("fhirVersion"),
                "description": "CapabilityStatement from EMR Direct sandbox - only declares Group/$export"
            }
        },
        "export_methods": [
            {
                "name": "CCD/HIM Export",
                "scope": "single_patient",
                "format": "C-CDA / HIM records",
                "mechanism": "In-app UI (Reports > Clinical Summary)",
                "documentation_depth": "minimal - just navigation instructions"
            },
            {
                "name": "CSC Request for Full Data Export",
                "scope": "population",
                "format": "Unknown (data files + data dictionary provided with export)",
                "mechanism": "Contact vendor (CSC request), delivery via SFTP",
                "documentation_depth": "none - no format spec, no data dictionary, no samples publicly available"
            },
            {
                "name": "FHIR REST API",
                "scope": "single_patient, population, group",
                "format": "FHIR R4 JSON (Bulk Data Export)",
                "mechanism": "REST API via EMR Direct Interoperability Engine",
                "documentation_depth": "moderate - 13 resource types listed with example URIs but no field-level docs"
            }
        ],
        "ehi_page_fhir_resources": [r["resource_type"] for r in ehi_resources],
        "psychotherapy_exclusion": True,
        "entities": entities,
        "total_entities": len(entities),
        "total_fields_in_examples": total_fields,
        "fields_with_descriptions": 0,
        "domain_summary": domain_summary,
        "data_dictionary_exists": False,
        "sample_data_exists": False,
        "schema_exists": False
    }
    
    return inventory

def classify_domain(name):
    mapping = {
        "patient": "Demographics",
        "smokingStatus": "Social History",
        "problem": "Problems / Conditions",
        "medication": "Medications",
        "medAllergy": "Allergies",
        "labTest": "Laboratory",
        "labResult": "Laboratory",
        "vital": "Vitals",
        "procedure": "Procedures",
        "careTeam": "Care Team",
        "immunization": "Immunizations",
        "device": "Devices",
        "planOfTreatment": "Care Plans",
        "assessment": "Clinical Notes / Documents",
        "goal": "Goals",
        "healthConcern": "Health Concerns",
    }
    return mapping.get(name, "Other")

def build_summary(inventory):
    return {
        "product": inventory["product"],
        "version": inventory["version"],
        "chpl_id": inventory["chpl_id"],
        "analysis_date": inventory["analysis_date"],
        "total_entities": inventory["total_entities"],
        "total_fields_in_examples": inventory["total_fields_in_examples"],
        "fields_with_descriptions": 0,
        "description_percentage": "0%",
        "data_dictionary_exists": False,
        "sample_data_exists": False,
        "schema_exists": False,
        "export_methods_count": len(inventory["export_methods"]),
        "ehi_page_fhir_resource_count": len(inventory["ehi_page_fhir_resources"]),
        "api_guide_category_count": 16,
        "psychotherapy_exclusion": True,
        "domain_summary": inventory["domain_summary"],
        "export_formats": ["FHIR R4 JSON", "C-CDA XML"],
        "missing_domains": [
            "Billing / Claims / Revenue Cycle",
            "Insurance / Coverage details",
            "Payments / Accounts Receivable",
            "Scheduling / Appointments",
            "Patient Portal Messages",
            "E-Prescribing transaction records",
            "Document vault (non-clinical attachments)",
            "Orders (beyond MedicationRequest)",
            "Referrals",
            "Inpatient nursing / MAR",
            "Behavioral health (explicitly excluded)"
        ]
    }

if __name__ == "__main__":
    inventory = build_full_inventory()
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    summary = build_summary(inventory)
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"=== iCare EHI Export Analysis ===")
    print(f"Total entities/categories: {inventory['total_entities']}")
    print(f"Total fields visible in examples: {inventory['total_fields_in_examples']}")
    print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
    print(f"Data dictionary provided: {inventory['data_dictionary_exists']}")
    print(f"FHIR resources on EHI page: {inventory['ehi_page_fhir_resources']}")
    print(f"\nDomain breakdown:")
    for domain, counts in inventory["domain_summary"].items():
        print(f"  {domain}: {counts['entity_count']} entities, {counts['total_fields']} fields")
    print(f"\nMissing domains:")
    for d in summary["missing_domains"]:
        print(f"  - {d}")
    
    print(f"\n=== Per-entity detail ===")
    for e in inventory["entities"]:
        fhir = ", ".join(e["fhir_resource_types"]) if e["fhir_resource_types"] else "N/A"
        print(f"  {e['entity_name']}: {e['field_count']} fields, FHIR types: {fhir}")
