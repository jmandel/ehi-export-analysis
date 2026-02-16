#!/usr/bin/env python3
"""Parse FHIR CapabilityStatement and SMART config to inventory available resources."""
import json

# Parse CapabilityStatement
with open("../downloads/fhir-capability-statement.json") as f:
    cap = json.load(f)

resources = cap.get("rest", [{}])[0].get("resource", [])
print(f"=== FHIR CapabilityStatement ===")
print(f"Total resource types: {len(resources)}")
print()

resource_inventory = []
for r in resources:
    rtype = r["type"]
    interactions = [i["code"] for i in r.get("interaction", [])]
    search_params = [p["name"] for p in r.get("searchParam", [])]
    resource_inventory.append({
        "type": rtype,
        "interactions": interactions,
        "search_params": search_params,
        "search_param_count": len(search_params)
    })
    print(f"  {rtype}: interactions={interactions}, search_params={len(search_params)}")

# Parse SMART config
with open("../downloads/fhir-smart-configuration.json") as f:
    smart = json.load(f)

scopes = smart.get("scopes_supported", [])
resource_types_in_scopes = set()
for s in scopes:
    parts = s.split("/")
    if len(parts) == 2 and "." in parts[1]:
        res = parts[1].split(".")[0]
        resource_types_in_scopes.add(res)

print(f"\n=== SMART Configuration ===")
print(f"Total scopes: {len(scopes)}")
print(f"Resource types from scopes: {len(resource_types_in_scopes)}")
print(f"  {sorted(resource_types_in_scopes)}")

# Capabilities listed
caps = smart.get("capabilities", [])
print(f"SMART capabilities: {caps}")

# Save inventory
output = {
    "capability_statement": {
        "fhir_version": cap.get("fhirVersion"),
        "status": cap.get("status"),
        "resource_count": len(resources),
        "resources": resource_inventory
    },
    "smart_configuration": {
        "total_scopes": len(scopes),
        "resource_types_from_scopes": sorted(resource_types_in_scopes),
        "capabilities": caps
    }
}

with open("fhir-inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nSaved to fhir-inventory.json")
