"""Parse FHIR API Documentation PDF text to extract resources and parameters.
Handles the multi-line example values in the response parameter tables."""

import re
import json

with open('/tmp/copilot-tool-output-1771247281956-jo4nou.txt', 'r') as f:
    text = f.read()

lines = text.split('\n')

resource_names = [
    'Patient', 'AllergyIntolerance', 'CarePlan', 'CareTeam', 'Condition',
    'Device', 'DiagnosticReport', 'DocumentReference', 'Goal', 'Immunization',
    'MedicationRequest', 'Observation', 'Procedure', 'Encounter', 'Provenance'
]

resources = []
current_resource = None
in_response = False
in_request = False
response_params = []
request_params = []

# Pattern for parameter line: starts with name, then type, then example/description
# e.g. "   id                  string     \"10006-111-20180823\""
param_pattern = re.compile(r'^\s{2,4}(\w[\w.]*)\s{3,}(\w+)\s{3,}(.+)')

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Skip page footers
    if stripped.startswith('fhir_api_doc') or stripped.startswith('PARADIGM® FHIR'):
        continue
    
    # Resource header
    if stripped in resource_names and i > 300:
        # Save previous resource
        if current_resource:
            resources.append({
                'resource': current_resource,
                'request_parameters': request_params,
                'response_parameters': [p['name'] for p in response_params],
                'response_param_details': response_params,
                'request_param_count': len(request_params),
                'response_param_count': len(response_params)
            })
        current_resource = stripped
        response_params = []
        request_params = []
        in_response = False
        in_request = False
        continue
    
    if stripped.startswith('Error and Exceptions') and i > 300:
        if current_resource:
            resources.append({
                'resource': current_resource,
                'request_parameters': request_params,
                'response_parameters': [p['name'] for p in response_params],
                'response_param_details': response_params,
                'request_param_count': len(request_params),
                'response_param_count': len(response_params)
            })
        break
    
    if 'Response Parameters' in stripped:
        in_response = True
        in_request = False
        continue
    
    if 'Request Parameters' in stripped:
        in_request = True
        in_response = False
        continue
    
    if stripped.startswith('Request:') or stripped.startswith('Example:'):
        in_response = False
        in_request = False
        continue
    
    if not current_resource:
        continue
    
    # Parse response params
    if in_response:
        # Header line
        if stripped.startswith('Name') and ('Type' in stripped):
            continue
        m = param_pattern.match(line)
        if m:
            name = m.group(1)
            ptype = m.group(2)
            # Skip false positives
            if name in ('Name', 'the', 'Page', 'PARADIGM'):
                continue
            response_params.append({'name': name, 'type': ptype})
    
    # Parse request params
    if in_request:
        if stripped.startswith('Name') and ('Type' in stripped):
            continue
        m = param_pattern.match(line)
        if m:
            name = m.group(1)
            ptype = m.group(2)
            if name in ('Name', 'the', 'Page', 'PARADIGM'):
                continue
            request_params.append({'name': name, 'type': ptype})

# Summary output
total_response = sum(r['response_param_count'] for r in resources)
total_request = sum(r['request_param_count'] for r in resources)

print(f"FHIR Resources: {len(resources)}")
print(f"Total Request Parameters: {total_request}")
print(f"Total Response Parameters: {total_response}")
print()

for r in resources:
    params = ', '.join(r['response_parameters'])
    print(f"  {r['resource']}: {r['response_param_count']} response params ({params})")

# Save
output = {
    'total_resources': len(resources),
    'total_response_parameters': total_response,
    'resources': [{
        'resource': r['resource'],
        'request_param_count': r['request_param_count'],
        'response_param_count': r['response_param_count'],
        'response_parameters': r['response_param_details']
    } for r in resources]
}

with open('/home/jmandel/hobby/ehi-export-analysis/abstraction/qrs-inc--paradigm/analysis/fhir_resources.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to analysis/fhir_resources.json")
