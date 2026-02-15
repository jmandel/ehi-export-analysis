"""
Analyze all FHIR artifacts from Med A-Z downloads:
- CapabilityStatements (single + bulk)
- OpenAPI/Swagger specs (single + bulk)
- FHIR Endpoint XML files
- Certification HTML page

Produces a summary JSON with hard numbers for the analysis.
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent.parent.parent / "results" / "medaz-net-llc--med-a-z" / "downloads"
OUTPUT = Path(__file__).resolve().parent

def parse_capability_statement(path, label):
    with open(path) as f:
        cs = json.load(f)
    resources = []
    for rest in cs.get("rest", []):
        for res in rest.get("resource", []):
            profiles = res.get("supportedProfile", [])
            if res.get("profile"):
                profiles = [res["profile"]] + profiles
            resources.append({
                "type": res["type"],
                "profiles": profiles,
                "interactions": [i["code"] for i in res.get("interaction", [])],
                "searchParams": [sp["name"] for sp in res.get("searchParam", [])]
            })
    return {
        "label": label,
        "name": cs.get("name"),
        "fhirVersion": cs.get("fhirVersion"),
        "status": cs.get("status"),
        "description": cs.get("description", ""),
        "implementationGuides": cs.get("implementationGuide", []),
        "resourceCount": len(resources),
        "resources": resources
    }

def parse_swagger(path, label):
    with open(path) as f:
        spec = json.load(f)
    paths = spec.get("paths", {})
    schemas = spec.get("components", {}).get("schemas", {})
    
    # Extract FHIR resource-specific paths
    fhir_resources = set()
    for p in paths:
        parts = p.strip("/").split("/")
        if parts and parts[0] and parts[0][0].isupper() and parts[0] not in ("Group",):
            base = parts[0].replace("Pagination", "")
            fhir_resources.add(base)
    
    return {
        "label": label,
        "title": spec.get("info", {}).get("title"),
        "version": spec.get("info", {}).get("version"),
        "pathCount": len(paths),
        "schemaCount": len(schemas),
        "fhirResources": sorted(fhir_resources),
        "fhirResourceCount": len(fhir_resources),
        "allPaths": sorted(paths.keys()),
        "schemaNames": sorted(schemas.keys())
    }

def parse_endpoint_xml(path, label):
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"fhir": "http://hl7.org/fhir"}
    
    endpoints = []
    for entry in root.findall(".//fhir:entry", ns):
        resource = entry.find(".//fhir:Endpoint", ns)
        if resource is not None:
            name_el = resource.find("fhir:name", ns)
            addr_el = resource.find("fhir:address", ns)
            name = name_el.get("value") if name_el is not None else "?"
            addr = addr_el.get("value") if addr_el is not None else "?"
            endpoints.append({"name": name, "address": addr})
    
    return {
        "label": label,
        "endpointCount": len(endpoints),
        "endpoints": endpoints
    }

def parse_certification_html(path):
    """Extract key facts from the certification HTML."""
    text = path.read_text()
    
    # Check for (b)(10) mention
    has_b10 = "(b)(10)" in text
    
    # Check for data dictionary links
    has_data_dict = any(term in text.lower() for term in ["data dictionary", "data model", "schema", "field definitions"])
    
    # Check for EHI-specific content
    has_ehi_section = any(term in text.lower() for term in ["ehi export", "electronic health information export", "all electronic health information"])
    
    # Extract links
    import re
    links = re.findall(r'href="([^"]+)"', text)
    
    return {
        "has_b10_listed": has_b10,
        "has_data_dictionary_link": has_data_dict,
        "has_ehi_specific_section": has_ehi_section,
        "documentation_links": [l for l in links if "fhir" in l.lower() or "swagger" in l.lower() or "export" in l.lower()],
        "total_links": len(links)
    }

# Run all analyses
results = {
    "capabilityStatements": {
        "single": parse_capability_statement(DOWNLOADS / "fhir-capability-statement-single.json", "Single Patient"),
        "bulk": parse_capability_statement(DOWNLOADS / "fhir-capability-statement-bulk.json", "Bulk Export")
    },
    "swaggerSpecs": {
        "single": parse_swagger(DOWNLOADS / "swagger-single-patient.json", "Single Patient"),
        "bulk": parse_swagger(DOWNLOADS / "swagger-bulk.json", "Bulk Export")
    },
    "endpointXMLs": {
        "single": parse_endpoint_xml(DOWNLOADS / "fhirsingle.xml", "Single Patient"),
        "bulk": parse_endpoint_xml(DOWNLOADS / "fhirsystosys.xml", "Bulk/System-to-System")
    },
    "certificationPage": parse_certification_html(DOWNLOADS / "certificationinfo.html"),
    "summary": {}
}

# Build summary
all_resource_types = set()
for cs in results["capabilityStatements"].values():
    for r in cs["resources"]:
        all_resource_types.add(r["type"])

results["summary"] = {
    "totalUniqueResourceTypes": len(all_resource_types),
    "resourceTypeList": sorted(all_resource_types),
    "singlePatientPaths": results["swaggerSpecs"]["single"]["pathCount"],
    "bulkPaths": results["swaggerSpecs"]["bulk"]["pathCount"],
    "singleSchemas": results["swaggerSpecs"]["single"]["schemaCount"],
    "bulkSchemas": results["swaggerSpecs"]["bulk"]["schemaCount"],
    "hasDataDictionary": False,
    "hasSampleData": False,
    "hasNativeDataModel": False,
    "exportType": "FHIR R4 US Core API (standard-based projection)",
    "b10_has_dedicated_documentation": False
}

out_path = OUTPUT / "fhir-artifact-analysis.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=== Med A-Z FHIR Artifact Analysis Summary ===")
print(f"FHIR Resource Types: {results['summary']['totalUniqueResourceTypes']}")
print(f"Resource Types: {', '.join(results['summary']['resourceTypeList'])}")
print(f"\nSingle Patient API: {results['summary']['singlePatientPaths']} paths, {results['summary']['singleSchemas']} schemas")
print(f"Bulk API: {results['summary']['bulkPaths']} paths, {results['summary']['bulkSchemas']} schemas")
print(f"\nHas dedicated (b)(10) documentation: {results['summary']['b10_has_dedicated_documentation']}")
print(f"Has data dictionary: {results['summary']['hasDataDictionary']}")
print(f"Has sample data: {results['summary']['hasSampleData']}")
print(f"Has native data model export: {results['summary']['hasNativeDataModel']}")
print(f"Export type: {results['summary']['exportType']}")
print(f"\nCertification page:")
cp = results["certificationPage"]
print(f"  (b)(10) listed: {cp['has_b10_listed']}")
print(f"  Data dictionary link: {cp['has_data_dictionary_link']}")
print(f"  EHI-specific section: {cp['has_ehi_specific_section']}")
print(f"  FHIR-related links: {cp['documentation_links']}")
print(f"\nOutput saved to: {out_path}")
