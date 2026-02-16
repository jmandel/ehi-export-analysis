"""
Parse the MaximEyes FHIR API Swagger/OpenAPI spec to extract:
- All FHIR resource types exposed
- Endpoints per resource (search, read, etc.)
- Whether response schemas are documented
- Billing vs clinical resource classification
"""
import json
import re
from collections import defaultdict

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/first-insight-corporation--maximeyes-com/downloads"

with open(f"{DOWNLOADS}/swagger-v1.json") as f:
    spec = json.load(f)

paths = spec.get("paths", {})

# Extract resource types from paths
resource_endpoints = defaultdict(list)
export_endpoints = []
other_endpoints = []

for path, methods in paths.items():
    # Extract resource type from path like /api/{customerName}/R4/Patient
    match = re.match(r"/api/\{customerName\}/R4/([A-Z][a-zA-Z]+)", path)
    if match:
        resource_type = match.group(1)
        # Classify by endpoint type
        if resource_type in ("Export", "Status", "Download"):
            export_endpoints.append(path)
        elif resource_type == "Group":
            export_endpoints.append(path)
        else:
            ops = []
            for method, detail in methods.items():
                if method in ("get", "post", "put", "delete"):
                    # Check if response schema is documented
                    responses = detail.get("responses", {})
                    has_schema = False
                    for code, resp in responses.items():
                        if "content" in resp:
                            for ct, ct_detail in resp["content"].items():
                                if "schema" in ct_detail and ct_detail["schema"]:
                                    has_schema = True
                    ops.append({
                        "method": method.upper(),
                        "path": path,
                        "summary": detail.get("summary", ""),
                        "has_response_schema": has_schema
                    })
            resource_endpoints[resource_type].extend(ops)
    else:
        match2 = re.match(r"/api/\{customerName\}/[rR]4/", path)
        if match2:
            other_endpoints.append(path)

# Classify resources
US_CORE_RESOURCES = {
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "Medication", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "PractitionerRole", "Procedure", "Provenance"
}

BILLING_RESOURCES = {"Account", "ChargeItem", "Coverage"}

results = {
    "openapi_version": spec.get("openapi"),
    "api_title": spec.get("info", {}).get("title"),
    "total_paths": len(paths),
    "total_resource_types": len(resource_endpoints),
    "resource_types": {},
    "export_endpoints": export_endpoints,
    "other_endpoints": other_endpoints,
    "summary": {
        "us_core_resources": [],
        "beyond_us_core_resources": [],
        "total_endpoints_with_schema": 0,
        "total_endpoints_without_schema": 0
    }
}

for resource, ops in sorted(resource_endpoints.items()):
    classification = "US Core" if resource in US_CORE_RESOURCES else "Beyond US Core (billing)"
    endpoint_types = []
    for op in ops:
        if "/_search" in op["path"]:
            endpoint_types.append("search-post")
        elif "/{id}" in op["path"]:
            endpoint_types.append("read")
        else:
            endpoint_types.append("search-get")

    has_any_schema = any(op["has_response_schema"] for op in ops)

    results["resource_types"][resource] = {
        "classification": classification,
        "endpoint_count": len(ops),
        "endpoint_types": list(set(endpoint_types)),
        "has_response_schema": has_any_schema
    }

    if resource in US_CORE_RESOURCES:
        results["summary"]["us_core_resources"].append(resource)
    else:
        results["summary"]["beyond_us_core_resources"].append(resource)

    for op in ops:
        if op["has_response_schema"]:
            results["summary"]["total_endpoints_with_schema"] += 1
        else:
            results["summary"]["total_endpoints_without_schema"] += 1

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/first-insight-corporation--maximeyes-com/analysis/swagger-analysis.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print(f"OpenAPI version: {results['openapi_version']}")
print(f"Total paths: {results['total_paths']}")
print(f"Total FHIR resource types: {results['total_resource_types']}")
print(f"\nUS Core resources ({len(results['summary']['us_core_resources'])}):")
for r in sorted(results["summary"]["us_core_resources"]):
    info = results["resource_types"][r]
    print(f"  {r}: {info['endpoint_count']} endpoints, schema={info['has_response_schema']}")
print(f"\nBeyond US Core ({len(results['summary']['beyond_us_core_resources'])}):")
for r in sorted(results["summary"]["beyond_us_core_resources"]):
    info = results["resource_types"][r]
    print(f"  {r}: {info['endpoint_count']} endpoints, schema={info['has_response_schema']}")
print(f"\nEndpoints with response schema: {results['summary']['total_endpoints_with_schema']}")
print(f"Endpoints without response schema: {results['summary']['total_endpoints_without_schema']}")
print(f"\nExport endpoints: {export_endpoints}")
