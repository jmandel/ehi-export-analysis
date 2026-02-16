#!/usr/bin/env python3
"""Build complete entity inventory from FHIR API PDF with proper JSON extraction."""

import json
import re
import subprocess
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/endosoft-llc--endovault/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/endosoft-llc--endovault/analysis"

def extract_field_paths(obj, prefix=""):
    """Recursively extract field paths from a JSON object."""
    fields = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            field_entry = {"path": path, "type": infer_type(value)}
            fields.append(field_entry)
            if isinstance(value, dict):
                fields.extend(extract_field_paths(value, path))
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    fields.extend(extract_field_paths(value[0], path + "[]"))
    return fields

def infer_type(value):
    if isinstance(value, str): return "string"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, int): return "integer"
    if isinstance(value, float): return "number"
    if isinstance(value, list): return "array"
    if isinstance(value, dict): return "object"
    if value is None: return "null"
    return "unknown"

def try_extract_json(text, start_pos):
    """Try to extract a complete JSON object starting near start_pos."""
    # Find the opening brace by going backwards
    brace_pos = None
    for i in range(start_pos, max(0, start_pos - 50), -1):
        if text[i] == '{':
            brace_pos = i
            break
    if brace_pos is None:
        brace_pos = text.find('{', start_pos)
    if brace_pos is None or brace_pos == -1:
        return None
    
    depth = 0
    in_string = False
    escape_next = False
    
    for pos in range(brace_pos, min(len(text), brace_pos + 30000)):
        ch = text[pos]
        if escape_next:
            escape_next = False
            continue
        if ch == '\\' and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
        if not in_string:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    json_str = text[brace_pos:pos+1]
                    # Clean whitespace artifacts from PDF extraction
                    json_str = re.sub(r'\n\s*', ' ', json_str)
                    # Remove stray page numbers
                    json_str = re.sub(r'\s+\d{1,3}\s+', ' ', json_str)
                    try:
                        obj = json.loads(json_str)
                        return obj
                    except json.JSONDecodeError:
                        return None
    return None

def main():
    result = subprocess.run(
        ["pdftotext", "-layout", os.path.join(DOWNLOADS, "170.315-g10-Standardized-API-FHIR-2.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Clean page footers from text
    text = re.sub(r'Company Confidential\s*\d*', '', text)
    
    # Separate individual and bulk sections
    bulk_start = text.find("Bulk Data Access")
    exception_start = text.find("Exception Handling")
    individual_text = text[:bulk_start]
    bulk_text = text[bulk_start:exception_start]
    
    # Define resources with their categories (matching PDF TOC structure)
    resource_defs = [
        # Individual section
        ("Patient", "Individual", "Demographics and administrative information"),
        ("Practitioner", "Individual", "Healthcare practitioners"),
        ("RelatedPerson", "Individual", "Related persons (next of kin, etc.)"),
        # Entities section
        ("Organization", "Entities", "Healthcare organizations"),
        # Management section  
        ("Encounter", "Management", "Healthcare encounters/visits"),
        # Clinical section
        ("AllergyIntolerance", "Clinical", "Allergy and intolerance records"),
        ("Condition", "Clinical", "Diagnoses, problems, health concerns"),
        ("Procedure", "Clinical", "Clinical procedures performed"),
        ("DiagnosticReport", "Clinical", "Diagnostic reports (lab, imaging)"),
        ("Observation", "Clinical", "Clinical observations (labs, vitals, social history, etc.)"),
        ("MedicationRequest", "Clinical", "Medication orders and prescriptions"),
        ("Immunization", "Clinical", "Immunization records"),
        ("CarePlan", "Clinical", "Care plans and treatment plans"),
        ("CareTeam", "Clinical", "Care team members and roles"),
        ("Goal", "Clinical", "Patient care goals"),
        ("ServiceRequest", "Clinical", "Service requests and orders"),
        ("DocumentReference", "Clinical", "Clinical documents and notes"),
        ("Device", "Clinical", "Implantable devices"),
        ("Provenance", "Security", "Data provenance tracking"),
    ]
    
    # Observation subcategories
    observation_profiles = [
        "Laboratory Results", "SDOH Assessments", "Respiratory Rate",
        "Social History", "Heart Rate", "Body Temperature",
        "Pediatric Weight for Height", "Pulse Oximetry", "Smoking Status",
        "Sexual Orientation", "Head Circumference", "Body Height",
        "BMI", "Blood Pressure", "Imaging Result", "Clinical Test Result",
        "Pediatric BMI for Age", 
        "Pediatric Head Occipital-frontal Circumference Percentile",
        "Body Weight"
    ]
    
    # Extract search parameters from the API resource table
    resource_search_params = {
        "Patient": ["_id", "identifier", "name", "birthdate", "gender"],
        "Practitioner": ["_id", "identifier", "name"],
        "RelatedPerson": ["_id", "patient"],
        "Organization": ["name", "address"],
        "Encounter": ["_id", "identifier", "patient", "date", "class", "type", "status"],
        "AllergyIntolerance": ["patient", "clinical-status"],
        "Condition": ["patient", "category", "clinical-status", "onset-date", "code", "asserted-date", "recorded-date", "identifier"],
        "Procedure": ["patient", "date", "code", "status", "identifier"],
        "DiagnosticReport": ["patient", "category", "date", "code", "identifier", "status"],
        "Observation": ["patient", "category", "date", "code", "identifier", "status"],
        "MedicationRequest": ["patient", "intent", "status", "authoredon", "identifier"],
        "Immunization": ["patient", "date", "status", "identifier"],
        "CarePlan": ["patient", "category", "date", "status", "identifier"],
        "CareTeam": ["patient", "status", "identifier"],
        "Goal": ["patient", "lifecycle-status", "target-date", "identifier"],
        "ServiceRequest": ["patient", "category", "_id", "identifier"],
        "DocumentReference": ["patient", "category", "date", "type", "identifier", "period"],
        "Device": ["patient", "type", "identifier"],
    }
    
    # Extract sample JSON from the PDF for each resource
    entities = []
    
    for rname, category, description in resource_defs:
        # Find all sample JSON for this resource type
        pattern = rf'"resourceType"\s*:\s*"{rname}"'
        
        all_fields = {}
        sample_count = 0
        
        for match in re.finditer(pattern, text):
            obj = try_extract_json(text, match.start())
            if obj and obj.get("resourceType") == rname:
                sample_count += 1
                for field in extract_field_paths(obj):
                    path = field["path"]
                    if path not in all_fields:
                        all_fields[path] = field
            elif obj and obj.get("resourceType") == "Bundle":
                # Extract from Bundle entries
                entries = obj.get("entry", [])
                for entry in entries:
                    resource = entry.get("resource", {})
                    if resource.get("resourceType") == rname:
                        sample_count += 1
                        for field in extract_field_paths(resource):
                            path = field["path"]
                            if path not in all_fields:
                                all_fields[path] = field
        
        has_bulk = rname != "Patient"  # Patient not in bulk endpoints per Table 4-1
        
        entity = {
            "name": rname,
            "category": category,
            "description": description,
            "has_individual_endpoint": True,
            "has_bulk_endpoint": has_bulk,
            "bulk_endpoint": f"/bulk/{rname.lower()}-bulkfile.ndjson" if has_bulk else None,
            "individual_endpoint": f"/{rname}",
            "search_parameters": resource_search_params.get(rname, []),
            "fhir_profile": f"http://hl7.org/fhir/us/core/StructureDefinition/us-core-{rname.lower()}",
            "fields": sorted(all_fields.values(), key=lambda x: x["path"]),
            "field_count": len(all_fields),
            "samples_found_in_pdf": sample_count,
            "field_descriptions": 0,  # FHIR resources don't have custom descriptions in this PDF
        }
        
        if rname == "Observation":
            entity["subcategories"] = observation_profiles
            entity["subcategory_count"] = len(observation_profiles)
        
        entities.append(entity)
    
    # C-CDA sections from the ePHI page
    ccda_sections = [
        "Allergies", "Encounter", "Immunizations", "Medications",
        "Plan of treatment", "Referral reason", "Active problems",
        "Reason for visit", "Implants", "Health concerns", "Procedures",
        "Functional status", "Results", "Social history", "Vitals",
        "Goals", "Discharge instructions", "Assessments",
        "Cognitive status", "Media", "Diagnostic Report", "Documents",
        "Service Request"
    ]
    
    # Summary statistics
    total_fields = sum(e["field_count"] for e in entities)
    clinical_entities = [e for e in entities if e["category"] == "Clinical"]
    
    inventory = {
        "metadata": {
            "product": "EndoVault",
            "vendor": "EndoSoft, LLC",
            "analysis_date": "2026-02-16",
            "source_documents": [
                "170.315-g10-Standardized-API-FHIR-2.pdf (138 pages, dated 2022-11-25)",
                "ephi-page.html (EHI export page at www.endosoft.com/ephi/)",
                "fhir-page.html (FHIR API landing page)",
                "endovault_ehr_disclosure_onc_2015-10_15_25.xlsx (cost disclosure)"
            ]
        },
        "export_methods": {
            "method_1": {
                "name": "Single/Multi-Patient C-CDA Export",
                "format": "C-CDA 2.1 XML",
                "mechanism": "UI export (details not documented)",
                "sections": ccda_sections,
                "section_count": len(ccda_sections)
            },
            "method_2": {
                "name": "Bulk EHI Export via FHIR API",
                "format": "NDJSON (FHIR R4)",
                "mechanism": "RESTful API (GET requests to static NDJSON endpoints)",
                "base_url": "https://fhirapi.endosoft.com/bulk/",
                "authorization": "OAuth 2.0 Bearer token"
            }
        },
        "fhir_resources": entities,
        "summary": {
            "total_fhir_resource_types": len(entities),
            "total_fields_extracted_from_samples": total_fields,
            "resources_with_bulk_endpoint": sum(1 for e in entities if e["has_bulk_endpoint"]),
            "resources_with_individual_endpoint": sum(1 for e in entities if e["has_individual_endpoint"]),
            "ccda_sections": len(ccda_sections),
            "observation_subcategories": len(observation_profiles),
            "field_descriptions_provided": 0,
            "fields_with_types": total_fields,
            "categories": {
                "Clinical": {
                    "resource_count": sum(1 for e in entities if e["category"] == "Clinical"),
                    "total_fields": sum(e["field_count"] for e in entities if e["category"] == "Clinical")
                },
                "Individual": {
                    "resource_count": sum(1 for e in entities if e["category"] == "Individual"),
                    "total_fields": sum(e["field_count"] for e in entities if e["category"] == "Individual")
                },
                "Management": {
                    "resource_count": sum(1 for e in entities if e["category"] == "Management"),
                    "total_fields": sum(e["field_count"] for e in entities if e["category"] == "Management")
                },
                "Entities": {
                    "resource_count": sum(1 for e in entities if e["category"] == "Entities"),
                    "total_fields": sum(e["field_count"] for e in entities if e["category"] == "Entities")
                },
                "Security": {
                    "resource_count": sum(1 for e in entities if e["category"] == "Security"),
                    "total_fields": sum(e["field_count"] for e in entities if e["category"] == "Security")
                },
            }
        },
        "key_observations": [
            "The FHIR API PDF is explicitly the g(10) standardized API document, reused as b(10) documentation",
            "18 FHIR R4 resource types have bulk data endpoints; Patient is individual-only",
            "All resources use standard US Core profiles with no vendor-specific extensions",
            "The Observation resource alone spans 59 pages with 19 subcategories (different US Core profiles)",
            "No native database model is exported - this is purely a standard FHIR projection",
            "No data dictionary exists beyond the FHIR resource structure itself",
            "The C-CDA export lists 23 sections but provides no technical documentation of their content",
            "Endoscopy images/video, oncology data, ENR nursing data, pathology, and billing are all absent from the export"
        ]
    }
    
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    
    print(f"Full entity inventory saved to {OUTPUT_DIR}/full-entity-inventory.json")
    print(f"\n=== SUMMARY ===")
    print(f"FHIR resource types: {len(entities)}")
    print(f"Total fields extracted from sample JSON: {total_fields}")
    print(f"Resources with bulk endpoint: {sum(1 for e in entities if e['has_bulk_endpoint'])}")
    print(f"C-CDA sections: {len(ccda_sections)}")
    print(f"Observation subcategories: {len(observation_profiles)}")
    print()
    print(f"{'Resource':<25} {'Category':<12} {'Fields':>6} {'Bulk':>5} {'Samples':>8}")
    print("-" * 65)
    for e in entities:
        print(f"{e['name']:<25} {e['category']:<12} {e['field_count']:>6} {'Yes' if e['has_bulk_endpoint'] else 'No':>5} {e['samples_found_in_pdf']:>8}")

if __name__ == "__main__":
    main()
