"""
Parse all Med A-Z EHI export artifacts and produce a full inventory JSON.
Analyzes: Swagger/OpenAPI specs, FHIR CapabilityStatements, endpoint XMLs,
and the certification HTML page.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/medaz-net-llc--med-a-z/downloads")
OUTPUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/medaz-net-llc--med-a-z/analysis")

def parse_capability_statement(filepath):
    """Parse FHIR CapabilityStatement and extract resource types with profiles."""
    with open(filepath) as f:
        cs = json.load(f)
    
    result = {
        "fhir_version": cs.get("fhirVersion"),
        "implementation_url": cs.get("implementation", {}).get("url"),
        "implementation_description": cs.get("implementation", {}).get("description"),
        "format": cs.get("format", []),
        "resource_types": []
    }
    
    rest = cs.get("rest", [{}])[0]
    for r in rest.get("resource", []):
        resource_info = {
            "type": r["type"],
            "supported_profiles": r.get("supportedProfile", []),
            "profile": r.get("profile"),
            "interactions": [i["code"] for i in r.get("interaction", [])],
            "search_params": [
                {"name": sp["name"], "type": sp.get("type"), "definition": sp.get("definition")}
                for sp in r.get("searchParam", [])
            ]
        }
        result["resource_types"].append(resource_info)
    
    return result

def parse_swagger(filepath):
    """Parse OpenAPI spec and extract paths, schemas, and field counts."""
    with open(filepath) as f:
        spec = json.load(f)
    
    result = {
        "title": spec["info"]["title"],
        "version": spec["info"]["version"],
        "description": spec["info"].get("description", ""),
        "servers": [s.get("url") for s in spec.get("servers", [])],
        "path_count": len(spec.get("paths", {})),
        "paths": [],
        "schema_count": len(spec.get("components", {}).get("schemas", {})),
        "schemas": []
    }
    
    # Extract resource-oriented paths (not generic templates)
    for path, methods in sorted(spec.get("paths", {}).items()):
        path_info = {
            "path": path,
            "methods": list(methods.keys()),
            "operations": {}
        }
        for method, details in methods.items():
            if isinstance(details, dict):
                path_info["operations"][method] = {
                    "summary": details.get("summary", ""),
                    "tags": details.get("tags", []),
                    "parameters_count": len(details.get("parameters", []))
                }
        result["paths"].append(path_info)
    
    # Extract schemas with field details
    for name, schema in sorted(spec.get("components", {}).get("schemas", {}).items()):
        schema_info = {
            "name": name,
            "type": schema.get("type", "object"),
            "properties_count": len(schema.get("properties", {})),
            "properties": [],
            "required": schema.get("required", [])
        }
        for prop_name, prop_details in schema.get("properties", {}).items():
            prop_info = {
                "name": prop_name,
                "type": prop_details.get("type"),
                "format": prop_details.get("format"),
                "description": prop_details.get("description", ""),
                "nullable": prop_details.get("nullable"),
                "ref": prop_details.get("$ref"),
                "enum": prop_details.get("enum"),
                "items": str(prop_details.get("items", "")) if prop_details.get("items") else None
            }
            schema_info["properties"].append(prop_info)
        result["schemas"].append(schema_info)
    
    return result

def parse_endpoints_xml(filepath):
    """Parse FHIR Endpoint Bundle XML."""
    ns = {'fhir': 'http://hl7.org/fhir'}
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # Get bundle metadata
    last_modified = root.find('.//fhir:meta/fhir:lastUpdated', ns)
    
    endpoints = []
    for entry in root.findall('.//fhir:entry', ns):
        endpoint = entry.find('.//fhir:Endpoint', ns)
        if endpoint is not None:
            name_elem = endpoint.find('fhir:name', ns)
            addr_elem = endpoint.find('fhir:address', ns)
            status_elem = endpoint.find('fhir:status', ns)
            endpoints.append({
                "name": name_elem.get("value") if name_elem is not None else None,
                "address": addr_elem.get("value") if addr_elem is not None else None,
                "status": status_elem.get("value") if status_elem is not None else None
            })
    
    return {
        "last_updated": last_modified.get("value") if last_modified is not None else None,
        "endpoint_count": len(endpoints),
        "endpoints": endpoints
    }

def parse_certification_html(filepath):
    """Parse certification HTML page to extract structured data."""
    with open(filepath) as f:
        content = f.read()
    
    from html.parser import HTMLParser
    
    # Simple extraction of key sections
    sections = {
        "has_b10_criterion": "(b)(10)" in content,
        "has_data_exchange_section": "DATA EXCHANGE/EXTRACTION" in content,
        "has_data_dictionary": "data dictionary" in content.lower(),
        "has_ehi_export_description": "ehi export" in content.lower() or "electronic health information export" in content.lower(),
        "documentation_links": [],
        "fhir_endpoint_links": [],
        "preferred_formats": [],
        "cost_info": []
    }
    
    # Extract links from data exchange section
    if "fhirapi.mhealthaz.com" in content:
        sections["documentation_links"].append({
            "label": "Single Patient",
            "url": "https://fhirapi.mhealthaz.com/swagger/index.html"
        })
    if "fhirbulk.mhealthaz.com" in content:
        sections["documentation_links"].append({
            "label": "Bulk exports", 
            "url": "https://fhirbulk.mhealthaz.com/swagger/index.html"
        })
    
    sections["fhir_endpoint_links"] = [
        {"label": "Single Patient", "url": "https://fhir.mhealthaz.com/fhirsingle.xml"},
        {"label": "Bulk exports", "url": "https://fhir.mhealthaz.com/fhirsystosys.xml"}
    ]
    
    sections["preferred_formats"] = ["QRDA-1", "CCD-A"]
    
    # Cost info
    if "Data extraction in custom formats" in content:
        sections["cost_info"].append("Data extraction in custom formats has fees")
        sections["cost_info"].append("No fees for extraction in ONC certified formats like QRDA1, CCD, etc.")
    
    return sections

def count_fhir_resource_fields(swagger_data):
    """Count fields per FHIR resource type from swagger schemas."""
    resource_fields = {}
    
    # Map schema names to FHIR resource types
    fhir_resource_types = [
        "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
        "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
        "Immunization", "Location", "Medication", "MedicationRequest",
        "Observation", "Organization", "Patient", "Practitioner",
        "PractitionerRole", "Procedure", "Provenance"
    ]
    
    for schema in swagger_data["schemas"]:
        name = schema["name"]
        # Check if this schema corresponds to a FHIR resource
        for rt in fhir_resource_types:
            if name.lower() == rt.lower() or name.lower().startswith(rt.lower()):
                if rt not in resource_fields:
                    resource_fields[rt] = {
                        "schema_name": name,
                        "field_count": schema["properties_count"],
                        "fields_with_descriptions": sum(1 for p in schema["properties"] if p.get("description")),
                        "fields_with_types": sum(1 for p in schema["properties"] if p.get("type") or p.get("ref")),
                        "fields": schema["properties"]
                    }
                break
    
    return resource_fields

def main():
    inventory = {
        "analysis_date": "2026-02-16",
        "product": "Med A-Z",
        "developer": "MedAZ.Net, LLC",
        "export_type": "FHIR R4 US Core API (standard-based projection)",
        "artifacts": {},
        "resource_types": [],
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "summary": {}
    }
    
    # Parse all artifacts
    print("Parsing capability statements...")
    cs_single = parse_capability_statement(DOWNLOADS / "fhir-capability-statement-single.json")
    cs_bulk = parse_capability_statement(DOWNLOADS / "fhir-capability-statement-bulk.json")
    inventory["artifacts"]["capability_statement_single"] = cs_single
    inventory["artifacts"]["capability_statement_bulk"] = cs_bulk
    
    print("Parsing Swagger specs...")
    swagger_single = parse_swagger(DOWNLOADS / "swagger-single-patient.json")
    swagger_bulk = parse_swagger(DOWNLOADS / "swagger-bulk.json")
    inventory["artifacts"]["swagger_single"] = {
        "title": swagger_single["title"],
        "version": swagger_single["version"],
        "path_count": swagger_single["path_count"],
        "schema_count": swagger_single["schema_count"]
    }
    inventory["artifacts"]["swagger_bulk"] = {
        "title": swagger_bulk["title"],
        "version": swagger_bulk["version"],
        "path_count": swagger_bulk["path_count"],
        "schema_count": swagger_bulk["schema_count"]
    }
    
    print("Parsing FHIR endpoint XMLs...")
    endpoints_single = parse_endpoints_xml(DOWNLOADS / "fhirsingle.xml")
    endpoints_bulk = parse_endpoints_xml(DOWNLOADS / "fhirsystosys.xml")
    inventory["artifacts"]["endpoints_single"] = endpoints_single
    inventory["artifacts"]["endpoints_bulk"] = endpoints_bulk
    
    print("Parsing certification HTML...")
    cert_html = parse_certification_html(DOWNLOADS / "certificationinfo.html")
    inventory["artifacts"]["certification_page"] = cert_html
    
    # Count fields per resource type
    print("Counting fields per resource type...")
    resource_fields = count_fhir_resource_fields(swagger_single)
    
    total_fields = 0
    total_described = 0
    resource_list = []
    
    for rt_info in cs_single["resource_types"]:
        rt_name = rt_info["type"]
        field_info = resource_fields.get(rt_name, {})
        
        resource_entry = {
            "resource_type": rt_name,
            "profiles": rt_info["supported_profiles"],
            "interactions": rt_info["interactions"],
            "search_params": rt_info["search_params"],
            "search_param_count": len(rt_info["search_params"]),
            "schema_fields": field_info.get("field_count", 0),
            "fields_with_descriptions": field_info.get("fields_with_descriptions", 0),
            "fields_with_types": field_info.get("fields_with_types", 0),
            "fields": field_info.get("fields", [])
        }
        
        total_fields += resource_entry["schema_fields"]
        total_described += resource_entry["fields_with_descriptions"]
        resource_list.append(resource_entry)
    
    inventory["resource_types"] = resource_list
    inventory["total_fields"] = total_fields
    inventory["fields_with_descriptions"] = total_described
    
    # Summary statistics
    inventory["summary"] = {
        "resource_type_count": len(cs_single["resource_types"]),
        "fhir_version": cs_single["fhir_version"],
        "total_api_paths_single": swagger_single["path_count"],
        "total_api_paths_bulk": swagger_bulk["path_count"],
        "total_schemas_single": swagger_single["schema_count"],
        "total_schemas_bulk": swagger_bulk["schema_count"],
        "total_fields_in_resource_schemas": total_fields,
        "fields_with_descriptions": total_described,
        "description_percentage": round(total_described / total_fields * 100, 1) if total_fields > 0 else 0,
        "endpoint_count_single": endpoints_single["endpoint_count"],
        "endpoint_count_bulk": endpoints_bulk["endpoint_count"],
        "has_data_dictionary": cert_html["has_data_dictionary"],
        "has_native_model": False,
        "export_is_standard_projection": True,
        "preferred_formats": cert_html["preferred_formats"],
        "custom_fees_for_non_standard": True,
        "no_fees_for_standard_formats": True
    }
    
    # Save full inventory
    output_path = OUTPUT / "full-entity-inventory.json"
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nSaved full inventory to {output_path}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Resource types: {inventory['summary']['resource_type_count']}")
    print(f"FHIR version: {inventory['summary']['fhir_version']}")
    print(f"Total API paths (single): {inventory['summary']['total_api_paths_single']}")
    print(f"Total API paths (bulk): {inventory['summary']['total_api_paths_bulk']}")
    print(f"Total schemas (single): {inventory['summary']['total_schemas_single']}")
    print(f"Total schemas (bulk): {inventory['summary']['total_schemas_bulk']}")
    print(f"Total fields in resource schemas: {inventory['summary']['total_fields_in_resource_schemas']}")
    print(f"Fields with descriptions: {inventory['summary']['fields_with_descriptions']} ({inventory['summary']['description_percentage']}%)")
    print(f"Has data dictionary: {inventory['summary']['has_data_dictionary']}")
    print(f"Export is standard projection: {inventory['summary']['export_is_standard_projection']}")
    
    # Print per-resource breakdown
    print("\n=== RESOURCE TYPE BREAKDOWN ===")
    print(f"{'Resource':<25} {'Fields':<8} {'Described':<10} {'Search Params':<14} {'Interactions'}")
    print("-" * 80)
    for r in sorted(resource_list, key=lambda x: x["schema_fields"], reverse=True):
        print(f"{r['resource_type']:<25} {r['schema_fields']:<8} {r['fields_with_descriptions']:<10} {r['search_param_count']:<14} {', '.join(r['interactions'])}")

if __name__ == "__main__":
    main()
