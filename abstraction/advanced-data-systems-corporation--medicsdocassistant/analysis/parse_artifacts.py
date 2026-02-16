#!/usr/bin/env python3
"""
Parse all EHI export artifacts for MedicsDocAssistant.
Extracts FHIR resource types from g(10) API doc, analyzes B10 page content,
and produces a full inventory JSON.
"""

import json
import re
import os
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/advanced-data-systems-corporation--medicsdocassistant/downloads"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


class TextExtractor(HTMLParser):
    """Extract plain text from HTML, preserving some structure."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_style = False
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.in_style = True
        elif tag == 'script':
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        elif tag == 'script':
            self.in_script = False

    def handle_data(self, data):
        if not self.in_style and not self.in_script:
            self.text_parts.append(data)

    def get_text(self):
        return ' '.join(self.text_parts)


def analyze_b10_page():
    """Analyze the B10 EHI Export documentation page."""
    with open(os.path.join(DOWNLOADS, "B10_MedicsDocAssistant.html")) as f:
        content = f.read()
    
    size = len(content)
    
    extractor = TextExtractor()
    extractor.feed(content)
    text = extractor.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Extract links
    links = re.findall(r'href="([^"]+)"', content)
    external_links = [l for l in links if l.startswith('http') and 'bootstrap' not in l]
    
    return {
        "file": "B10_MedicsDocAssistant.html",
        "size_bytes": size,
        "text_content": text,
        "word_count": len(text.split()),
        "external_links": external_links,
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_export_instructions": False,
        "has_schema": False,
        "formats_mentioned": ["HL7 CCDA XML", "HL7 FHIR v4.0.1 US Core v3.1.1"],
        "claims_single_patient": True,
        "claims_population_export": True,
    }


def analyze_fhir_doc():
    """Analyze the FHIR API documentation (g(10) doc, not b(10))."""
    with open(os.path.join(DOWNLOADS, "FHIRMedicsDocAssistant.htm"), errors='ignore') as f:
        content = f.read()
    
    size = len(content)
    line_count = content.count('\n') + 1
    
    # Extract resource sections from bold text
    bold_matches = re.findall(r'<b[^>]*>(.*?)</b>', content, re.DOTALL)
    resource_sections = []
    for bm in bold_matches:
        clean = re.sub(r'<[^>]+>', '', bm).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if clean.startswith('Request:') and len(clean) > 10:
            resource_name = clean.replace('Request:', '').replace('-', '').strip()
            resource_sections.append(resource_name)
    
    # Map to FHIR resource types
    resource_type_map = {
        "Patient": "Patient",
        "AllergyIntolerance": "AllergyIntolerance",
        "CarePlan": "CarePlan",
        "CareTeam": "CareTeam",
        "Condition Tests": "Condition",
        "Implantable Device Tests": "Device",
        "DiagnosticReport for Report and Note exchange": "DiagnosticReport",
        "Laboratory Results": "Observation (Laboratory)",
        "DocumentReference": "DocumentReference",
        "Goal": "Goal",
        "Immunization": "Immunization",
        "Smoking Status": "Observation (Smoking Status)",
        "Vitals": "Observation (Vitals)",
        "Procedure": "Procedure",
        "Encounter": "Encounter",
        "Organization": "Organization",
        "Practitioner": "Practitioner",
        "Provenance": "Provenance",
        "Clinical Notes Guidance": "DocumentReference (Clinical Notes)",
    }
    
    mapped_resources = []
    for section in resource_sections:
        fhir_type = resource_type_map.get(section, section)
        mapped_resources.append({
            "section_name": section,
            "fhir_resource_type": fhir_type,
            "is_us_core_required": True,
        })
    
    # Check for bulk data documentation
    bulk_mentions = len(re.findall(r'bulk\s*data|Bulk\s*Data|\$export', content, re.I))
    has_bulk_doc = bulk_mentions > 2  # More than passing mentions
    
    return {
        "file": "FHIRMedicsDocAssistant.htm",
        "size_bytes": size,
        "line_count": line_count,
        "is_b10_documentation": False,
        "is_g10_documentation": True,
        "resource_sections": mapped_resources,
        "unique_fhir_resource_types": len(set(r["fhir_resource_type"] for r in mapped_resources)),
        "total_resource_sections": len(resource_sections),
        "bulk_data_mentions": bulk_mentions,
        "has_bulk_data_documentation": has_bulk_doc,
        "standards_referenced": [
            "FHIR R4 v4.0.1",
            "US Core STU3.1.1",
            "SMART App Launch 1.0",
            "Bulk Data 1.0.1 (mentioned only)",
        ],
    }


def analyze_service_urls():
    """Analyze the service base URLs JSON."""
    with open(os.path.join(DOWNLOADS, "service-base-urls.json")) as f:
        data = json.load(f)
    
    entries = data.get("entry", [])
    endpoints = [e for e in entries if e.get("resource", {}).get("resourceType") == "Endpoint"]
    orgs = [e for e in entries if e.get("resource", {}).get("resourceType") == "Organization"]
    
    return {
        "file": "service-base-urls.json",
        "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "service-base-urls.json")),
        "total_entries": len(entries),
        "endpoint_count": len(endpoints),
        "organization_count": len(orgs),
        "confirms_fhir_service_active": len(endpoints) > 0,
        "is_b10_documentation": False,
    }


def build_full_inventory():
    """Build the full entity inventory based on what the export documentation describes."""
    # Since the B10 page only references CCDA and FHIR US Core with no vendor-specific 
    # data dictionary, the "entities" are the FHIR resource types / CCDA sections
    
    us_core_resources = [
        {
            "entity_name": "Patient",
            "fhir_resource_type": "Patient",
            "standard": "US Core 3.1.1",
            "category": "Demographics",
            "description": "Patient demographics including name, DOB, sex, race, ethnicity, language, identifiers, contact info",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,  # No field-level documentation in B10 page
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "AllergyIntolerance",
            "fhir_resource_type": "AllergyIntolerance",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Patient allergy and intolerance records",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "CarePlan",
            "fhir_resource_type": "CarePlan",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Patient care plans",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "CareTeam",
            "fhir_resource_type": "CareTeam",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Care team members for a patient",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Condition",
            "fhir_resource_type": "Condition",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Problems, diagnoses, conditions",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Device (Implantable)",
            "fhir_resource_type": "Device",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Implantable device records",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "DiagnosticReport",
            "fhir_resource_type": "DiagnosticReport",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Diagnostic reports for report and note exchange",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Observation (Laboratory)",
            "fhir_resource_type": "Observation",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Laboratory test results",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "DocumentReference",
            "fhir_resource_type": "DocumentReference",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Document references including clinical notes",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Goal",
            "fhir_resource_type": "Goal",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Patient goals",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Immunization",
            "fhir_resource_type": "Immunization",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Immunization records",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Observation (Smoking Status)",
            "fhir_resource_type": "Observation",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Smoking status observations",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Observation (Vitals)",
            "fhir_resource_type": "Observation",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Vital signs observations",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Procedure",
            "fhir_resource_type": "Procedure",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Procedure records",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Encounter",
            "fhir_resource_type": "Encounter",
            "standard": "US Core 3.1.1",
            "category": "Clinical",
            "description": "Patient encounters/visits",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Organization",
            "fhir_resource_type": "Organization",
            "standard": "US Core 3.1.1",
            "category": "Administrative",
            "description": "Healthcare organization records",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Practitioner",
            "fhir_resource_type": "Practitioner",
            "standard": "US Core 3.1.1",
            "category": "Administrative",
            "description": "Practitioner/provider records",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
        {
            "entity_name": "Provenance",
            "fhir_resource_type": "Provenance",
            "standard": "US Core 3.1.1",
            "category": "Administrative",
            "description": "Data provenance/origin tracking",
            "documented_in": "FHIRMedicsDocAssistant.htm",
            "field_count": None,
            "fields_with_descriptions": None,
            "vendor_specific_extensions": None,
        },
    ]
    
    return {
        "vendor": "Advanced Data Systems Corporation",
        "product": "MedicsDocAssistant",
        "version": "8.0",
        "export_documentation_type": "standard_based_projection",
        "data_dictionary_provided": False,
        "vendor_specific_schema_provided": False,
        "entities": us_core_resources,
        "entity_count": len(us_core_resources),
        "total_fields": "N/A - no field-level documentation provided",
        "fields_with_descriptions": "N/A",
        "notes": [
            "No vendor-specific data dictionary exists. The B10 page only references HL7 CCDA and FHIR US Core standards.",
            "Entity list derived from the g(10) FHIR API documentation, which documents 19 resource sections mapping to ~15 unique FHIR resource types.",
            "No field-level documentation is provided by the vendor beyond the external HL7 standards.",
            "No sample export data is provided.",
            "Medication resource is mentioned in the FHIR doc but not listed as a separate request section.",
        ],
    }


def main():
    results = {
        "b10_page": analyze_b10_page(),
        "fhir_api_doc": analyze_fhir_doc(),
        "service_urls": analyze_service_urls(),
    }
    
    # Save analysis results
    with open(os.path.join(OUTPUT_DIR, "artifact-analysis.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("Saved artifact-analysis.json")
    
    # Save full entity inventory
    inventory = build_full_inventory()
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    print("Saved full-entity-inventory.json")
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"B10 page: {results['b10_page']['size_bytes']} bytes, {results['b10_page']['word_count']} words")
    print(f"FHIR API doc: {results['fhir_api_doc']['size_bytes']} bytes, {results['fhir_api_doc']['line_count']} lines")
    print(f"FHIR resource sections: {results['fhir_api_doc']['total_resource_sections']}")
    print(f"Unique FHIR resource types: {results['fhir_api_doc']['unique_fhir_resource_types']}")
    print(f"Bulk data documentation: {'Yes' if results['fhir_api_doc']['has_bulk_data_documentation'] else 'No (mentioned only)'}")
    print(f"Service endpoints: {results['service_urls']['endpoint_count']} client practices")
    print(f"Entity inventory: {inventory['entity_count']} resource types (all US Core standard)")
    print(f"Data dictionary: {'Yes' if inventory['data_dictionary_provided'] else 'No'}")


if __name__ == "__main__":
    main()
