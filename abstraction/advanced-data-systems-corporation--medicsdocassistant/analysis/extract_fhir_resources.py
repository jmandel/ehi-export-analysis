"""Extract the specific FHIR resource sections from the FHIR API doc."""
import re
import json

with open('../downloads/FHIRMedicsDocAssistant.htm', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find resource endpoint documentation sections
# Look for patterns like "GET [base]/Patient" or resource documentation blocks
endpoint_pattern = re.compile(r'(?:GET|POST|PUT|DELETE)\s+\[base\]/(\w+)', re.IGNORECASE)
endpoints = endpoint_pattern.findall(content)
unique_endpoints = sorted(set(endpoints))
print(f"=== FHIR Endpoints documented ({len(unique_endpoints)}) ===")
for ep in unique_endpoints:
    count = endpoints.count(ep)
    print(f"  {ep} ({count} endpoints)")

# Look for search parameter tables
# Pattern: resource type followed by search parameters
search_param_pattern = re.compile(r'search\s*parameter', re.IGNORECASE)
sp_count = len(search_param_pattern.findall(content))
print(f"\n=== 'search parameter' mentions: {sp_count} ===")

# Look for sample JSON responses - count resource types in examples
resourcetype_pattern = re.compile(r'"resourceType"\s*:\s*"(\w+)"')
example_resources = resourcetype_pattern.findall(content)
unique_examples = sorted(set(example_resources))
print(f"\n=== Resource types in JSON examples ({len(unique_examples)}) ===")
for r in unique_examples:
    print(f"  {r} ({example_resources.count(r)} examples)")

# Check for Coverage, Claim, EOB - billing resources
billing_resources = ['Coverage', 'Claim', 'ExplanationOfBenefit', 'ChargeItem', 'Invoice', 'Account']
print(f"\n=== Billing resource mentions ===")
for br in billing_resources:
    count = len(re.findall(r'\b' + br + r'\b', content))
    print(f"  {br}: {count}")

# Save
results = {
    'endpoints_documented': unique_endpoints,
    'endpoint_counts': {ep: endpoints.count(ep) for ep in unique_endpoints},
    'example_resource_types': unique_examples,
    'example_counts': {r: example_resources.count(r) for r in unique_examples}
}
with open('fhir_endpoints.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved to fhir_endpoints.json")
