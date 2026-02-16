"""Parse FHIR Documentation HTML to extract all resource types, endpoints, and details."""
import re
import json

with open('/home/jmandel/hobby/ehi-export-analysis/results/cursahealth-llc--cursahealth-ehr/downloads/FHIR-Documentation.html', 'r') as f:
    html = f.read()

# Extract resource section IDs (top-level resources, not sub-endpoints)
all_ids = re.findall(r'id="([^"]+)"', html)
# Filter to resource-level IDs (not sub-operations, not utility sections)
skip = {'root', 'navbarSupportedContent', 'Client_Registration', 'Authorization', 
        'Scopes', 'Resources', 'Errors_and_Exceptions', 'Terms_&_Conditions', 'json-pretty'}

resource_ids = []
for i in all_ids:
    if i in skip:
        continue
    # Top-level resources don't contain GET/POST/Search prefixes
    if not any(i.startswith(p) for p in ['Search_', '_search_', 'Allergy_Intolerance_By_Id',
                                          'Observation_By_Id', 'Condition_By_Id', 'CarePlan_By_Id',
                                          'CareTeam_By_Id', 'Device_By_Id', 'DiagnosticReport_By_Id',
                                          'DocumentReference_By_Id', 'Goal_By_Id', 'Immunization_By_Id',
                                          'MedicationRequest_By_', 'Procedure_By_Id']):
        if '_GET_' not in i and '_POST_' not in i:
            resource_ids.append(i)

# Deduplicate while preserving order
seen = set()
unique_resources = []
for r in resource_ids:
    if r not in seen:
        seen.add(r)
        unique_resources.append(r)

# Map to cleaner names
resource_names = []
for r in unique_resources:
    name = r.replace('_', ' ').replace('-', '-')
    resource_names.append({'id': r, 'name': name})

# Count API endpoints per resource
# Look for patterns like GET /api/... and POST /api/...
endpoints = re.findall(r'<h5[^>]*>([^<]*(?:GET|POST|PUT|DELETE)[^<]*)</h5>', html)
print(f"H5 endpoint headers: {len(endpoints)}")
for e in endpoints[:10]:
    print(f"  {e}")

# Try different pattern
endpoint_divs = re.findall(r'id="((?:Search|_search|.*_By_Id|.*_GET_|.*_POST_)[^"]*)"', html)
print(f"\nEndpoint section IDs: {len(endpoint_divs)}")

print(f"\n=== FHIR Resources ({len(resource_names)}) ===")
for r in resource_names:
    # Count sub-operations for this resource
    ops = [i for i in all_ids if r['id'] in i and i != r['id']]
    r['operations'] = len(ops)
    r['operation_ids'] = ops
    print(f"  {r['name']} ({len(ops)} operations)")

# Save full inventory
output = {
    'total_resources': len(resource_names),
    'resources': resource_names
}
with open('fhir_resources.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to fhir_resources.json")
