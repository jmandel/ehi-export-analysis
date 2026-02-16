#!/usr/bin/env python3
"""Parse all iCare EHI export artifacts and produce entity inventory."""

import json
import re
from pathlib import Path
from html.parser import HTMLParser

DOWNLOADS = Path("../downloads")
OUTPUT_DIR = Path(".")

# === Parse the EHI Export HTML page ===
def parse_ehi_html():
    """Extract FHIR resource types and export methods from the EHI export page."""
    html = (DOWNLOADS / "ehi-export-page.html").read_text()
    
    # Extract h4 headers (these are the FHIR resource types)
    resource_types = re.findall(r'<h4>(\w+)</h4>', html)
    
    # Extract export methods
    methods = []
    # Method 1: CCD/HIM
    if "CCDA and HIM" in html or "CCD" in html:
        methods.append({
            "method": "CCD/HIM Export",
            "type": "single_patient",
            "format": "C-CDA",
            "description": "Generate CCD from patient chart or export via HIM Request"
        })
    # Method 2: CSC Request
    if "CSC request" in html:
        methods.append({
            "method": "CSC Request",
            "type": "population",
            "format": "unknown (data files with data dictionary)",
            "description": "Full data export via SFTP with data dictionary"
        })
    # Method 3: FHIR API
    methods.append({
        "method": "FHIR REST API",
        "type": "single_patient, population, group",
        "format": "FHIR R4 JSON (Bulk Data)",
        "description": "FHIR Bulk Data Export via EMR Direct Interoperability Engine"
    })
    
    return {
        "fhir_resource_types": resource_types,
        "export_methods": methods,
        "psychotherapy_exclusion": "items related to psychotherapy will not be included" in html.lower()
    }

# === Parse the API Guide PDF text ===
def parse_api_guide():
    """Parse the API guide text to extract data categories and their fields."""
    text = (OUTPUT_DIR / "api-guide-full-text.txt").read_text()
    
    # The API guide documents these data categories
    categories = [
        "patient", "smokingStatus", "problem", "medication", "medAllergy",
        "labTest", "labResult", "vital", "procedure", "careTeam",
        "immunization", "device", "planOfTreatment", "assessment", "goal", "healthConcern"
    ]
    
    entities = []
    
    for cat in categories:
        entity = {
            "name": cat,
            "source": "iCare-API-Guide.pdf",
            "api_endpoint": f"/rest/extApp/Clinical?id=<id>&category={cat}",
            "fields": [],
            "description": "",
            "response_format": "FHIR R4 JSON"
        }
        
        # Try to extract fields from JSON examples in the text
        # Find the section for this category
        cat_pattern = re.escape(cat)
        
        # Extract description text after category heading
        desc_match = re.search(
            rf'(?:^|\n){cat_pattern}\s*\n\s*Input Examples.*?\n\s*Output\s*\n(.*?)(?=\n\s*\{{|\n[a-zA-Z])',
            text, re.DOTALL | re.IGNORECASE
        )
        if desc_match:
            entity["description"] = desc_match.group(1).strip()[:500]
        
        entities.append(entity)
    
    # Also add the "All Criteria Data Request" which returns C-CDA
    entities.append({
        "name": "allCriteria",
        "source": "iCare-API-Guide.pdf",
        "api_endpoint": "/rest/extApp/Clinical?id=<id>&category=patient,smokingStatus,problem,...",
        "fields": [],
        "description": "Returns all clinical data as a C-CDA XML document",
        "response_format": "C-CDA XML"
    })
    
    return entities

# === Parse FHIR CapabilityStatement ===
def parse_capability_statement():
    """Parse the FHIR CapabilityStatement."""
    with open(DOWNLOADS / "fhir-capability-statement.json") as f:
        cs = json.load(f)
    
    return {
        "fhir_version": cs.get("fhirVersion"),
        "software": cs.get("software", {}).get("name"),
        "software_version": cs.get("software", {}).get("version"),
        "instantiates": cs.get("instantiates", []),
        "resources": [
            {
                "type": r["type"],
                "operations": [op["name"] for op in r.get("operation", [])],
                "interactions": [i["code"] for i in r.get("interaction", [])]
            }
            for r in cs.get("rest", [{}])[0].get("resource", [])
        ]
    }

# === Parse FHIR resource details from EHI page ===
def parse_fhir_resources_from_html():
    """Extract detailed info about each FHIR resource from the HTML page."""
    html = (DOWNLOADS / "ehi-export-page.html").read_text()
    
    resources = []
    # Find each h4 section
    sections = re.split(r'<h4>', html)
    for section in sections[1:]:  # skip first split before any h4
        name_match = re.match(r'(\w+)</h4>', section)
        if not name_match:
            continue
        name = name_match.group(1)
        
        # Extract the query URI pattern
        uri_match = re.search(r'URI:\s*(\S+\?\S+)', section)
        query_uri = uri_match.group(1) if uri_match else None
        
        # Extract example URL
        example_match = re.search(r'Example:\s*<?a[^>]*href="([^"]*)"', section)
        if not example_match:
            example_match = re.search(r'Example:\s*(https?://\S+)', section)
        example_url = example_match.group(1) if example_match else None
        
        # Check for notes
        note_match = re.search(r'Note:?\s*(.+?)(?:<|$)', section)
        note = note_match.group(1).strip() if note_match else None
        
        resources.append({
            "resource_type": name,
            "query_uri": query_uri,
            "example_url": example_url,
            "note": note
        })
    
    return resources

# === Extract fields from API guide JSON examples ===
def extract_fields_from_json_examples():
    """Parse JSON examples from the API guide to identify all fields used."""
    text = (OUTPUT_DIR / "api-guide-full-text.txt").read_text()
    
    # Find all JSON blocks in the text
    json_blocks = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    
    resource_fields = {}
    
    for block in json_blocks:
        try:
            # Clean up common PDF extraction issues
            block = block.replace('\n', ' ').replace('  ', ' ')
            data = json.loads(block)
            rt = data.get("resourceType")
            if rt:
                if rt not in resource_fields:
                    resource_fields[rt] = set()
                def collect_keys(obj, prefix=""):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            full_key = f"{prefix}.{k}" if prefix else k
                            resource_fields[rt].add(full_key)
                            collect_keys(v, full_key)
                    elif isinstance(obj, list):
                        for item in obj:
                            collect_keys(item, prefix)
                collect_keys(data)
        except (json.JSONDecodeError, TypeError):
            pass
    
    return {rt: sorted(list(fields)) for rt, fields in resource_fields.items()}

# === Build complete entity inventory ===
def build_entity_inventory():
    """Build the complete entity inventory combining all sources."""
    
    ehi_data = parse_ehi_html()
    api_entities = parse_api_guide()
    capability = parse_capability_statement()
    fhir_resources = parse_fhir_resources_from_html()
    example_fields = extract_fields_from_json_examples()
    
    # Map API categories to FHIR resource types
    category_to_fhir = {
        "patient": "Patient",
        "smokingStatus": "Observation (Social History)",
        "problem": "Condition",
        "medication": "MedicationRequest",
        "medAllergy": "AllergyIntolerance",
        "labTest": "DiagnosticReport",
        "labResult": "Observation (Laboratory)",
        "vital": "Observation (Vital Signs)",
        "procedure": "Procedure",
        "careTeam": "CareTeam",
        "immunization": "Immunization",
        "device": "Device",
        "planOfTreatment": "CarePlan",
        "assessment": "DocumentReference / Assessment",
        "goal": "Goal",
        "healthConcern": "Condition (Health Concern)",
        "allCriteria": "C-CDA Document (all above)"
    }
    
    # Build inventory entries
    entities = []
    for api_entity in api_entities:
        cat = api_entity["name"]
        fhir_type = category_to_fhir.get(cat, "Unknown")
        fields = example_fields.get(fhir_type.split(" ")[0] if " " not in fhir_type else fhir_type, [])
        
        # Try to get fields from simple FHIR type name
        simple_type = fhir_type.split(" ")[0]
        if simple_type in example_fields:
            fields = example_fields[simple_type]
        
        entity = {
            "entity_name": cat,
            "fhir_resource_type": fhir_type,
            "source": "iCare-API-Guide.pdf + EHI Export page",
            "category": classify_domain(cat),
            "field_count": len(fields),
            "fields": [
                {
                    "name": f,
                    "type": "varies (FHIR)",
                    "description": "",
                    "has_description": False
                }
                for f in fields
            ],
            "description": api_entity.get("description", ""),
            "response_format": api_entity["response_format"]
        }
        entities.append(entity)
    
    # Add FHIR resource types from EHI page that may not be in API guide
    ehi_resource_types = set(ehi_data["fhir_resource_types"])
    api_fhir_types = set(category_to_fhir.values())
    
    for rt in ehi_resource_types:
        fields = example_fields.get(rt, [])
        # Check if already covered
        already = any(e["fhir_resource_type"].startswith(rt) for e in entities)
        if not already:
            entities.append({
                "entity_name": rt,
                "fhir_resource_type": rt,
                "source": "EHI Export page",
                "category": classify_domain(rt),
                "field_count": len(fields),
                "fields": [
                    {
                        "name": f,
                        "type": "varies (FHIR)",
                        "description": "",
                        "has_description": False
                    }
                    for f in fields
                ],
                "description": f"FHIR {rt} resource accessible via REST API",
                "response_format": "FHIR R4 JSON"
            })
    
    return {
        "product": "iCare EHR",
        "version": "Version 2",
        "export_methods": ehi_data["export_methods"],
        "fhir_capability": capability,
        "psychotherapy_exclusion": ehi_data["psychotherapy_exclusion"],
        "entities": entities,
        "total_entities": len(entities),
        "total_fields": sum(e["field_count"] for e in entities),
        "fields_with_descriptions": 0,  # No field descriptions provided
        "example_fields_by_resource": example_fields
    }

def classify_domain(name):
    """Classify an entity into a domain category."""
    mapping = {
        "patient": "Demographics",
        "Patient": "Demographics",
        "smokingStatus": "Social History",
        "problem": "Problems / Conditions",
        "Condition": "Problems / Conditions",
        "medication": "Medications",
        "MedicationRequest": "Medications",
        "medAllergy": "Allergies",
        "AllergyIntolerance": "Allergies",
        "labTest": "Laboratory",
        "labResult": "Laboratory",
        "DiagnosticReport": "Laboratory",
        "Observation": "Clinical Observations",
        "vital": "Vitals",
        "procedure": "Procedures",
        "Procedure": "Procedures",
        "careTeam": "Care Team",
        "CareTeam": "Care Team",
        "immunization": "Immunizations",
        "Immunization": "Immunizations",
        "device": "Devices",
        "Device": "Devices",
        "planOfTreatment": "Care Plans",
        "CarePlan": "Care Plans",
        "assessment": "Clinical Notes / Documents",
        "DocumentReference": "Clinical Notes / Documents",
        "goal": "Goals",
        "Goal": "Goals",
        "healthConcern": "Health Concerns",
        "allCriteria": "All Clinical (C-CDA)",
        "Encounter": "Encounters"
    }
    return mapping.get(name, "Other")

def build_summary(inventory):
    """Build summary statistics from the full inventory."""
    entities = inventory["entities"]
    
    # Domain breakdown
    domain_counts = {}
    for e in entities:
        cat = e["category"]
        if cat not in domain_counts:
            domain_counts[cat] = {"entities": 0, "fields": 0}
        domain_counts[cat]["entities"] += 1
        domain_counts[cat]["fields"] += e["field_count"]
    
    return {
        "product": inventory["product"],
        "total_entities": inventory["total_entities"],
        "total_fields": inventory["total_fields"],
        "fields_with_descriptions": inventory["fields_with_descriptions"],
        "description_percentage": 0,
        "export_methods": len(inventory["export_methods"]),
        "psychotherapy_exclusion": inventory["psychotherapy_exclusion"],
        "domain_breakdown": domain_counts,
        "export_formats": ["FHIR R4 JSON", "C-CDA XML"],
        "fhir_resource_types_documented": len([e for e in entities if e["response_format"] == "FHIR R4 JSON"]),
        "data_dictionary_provided": False,
        "sample_data_provided": False,
        "schemas_provided": False
    }

if __name__ == "__main__":
    inventory = build_entity_inventory()
    
    with open(OUTPUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    summary = build_summary(inventory)
    with open(OUTPUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Total entities: {inventory['total_entities']}")
    print(f"Total fields (from examples): {inventory['total_fields']}")
    print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
    print(f"Export methods: {len(inventory['export_methods'])}")
    print(f"\nDomain breakdown:")
    for domain, counts in summary["domain_breakdown"].items():
        print(f"  {domain}: {counts['entities']} entities, {counts['fields']} fields")
    print(f"\nFHIR resource types on EHI page: {inventory.get('fhir_capability', {}).get('resources', [])}")
    print(f"\nExample fields extracted by resource type:")
    for rt, fields in inventory["example_fields_by_resource"].items():
        print(f"  {rt}: {len(fields)} fields")
