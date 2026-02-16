#!/usr/bin/env python3
"""Parse FHIR API PDF text to extract all resources and their data elements."""

import json
import re
import sys

def parse_fhir_elements(text_file):
    with open(text_file, 'r') as f:
        lines = f.readlines()

    resources = []
    current_resource = None
    in_data_elements = False
    header_seen = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect resource headers (standalone lines that match known resource names)
        resource_names = [
            'Patient', 'Allergy Intolerance', 'Care Plan', 'Care Teams',
            'Conditions', 'Coverages', 'Implantable Devices', 'Diagnostic Reports',
            'Document Reference', 'Encounter', 'Goal', 'Immunization',
            'Location', 'Medical Dispense', 'Medication Request', 'Observation',
            'Procedure', 'Service Request', 'Organization', 'Practitioner',
            'Provenance', 'Related Person', 'Specimen'
        ]

        for rname in resource_names:
            if line == rname:
                if current_resource:
                    resources.append(current_resource)
                current_resource = {
                    'resource': rname,
                    'description': '',
                    'profile': '',
                    'path': '',
                    'data_elements': []
                }
                in_data_elements = False
                header_seen = False
                break

        if current_resource:
            if line.startswith('Description'):
                current_resource['description'] = line.replace('Description', '').strip()
            elif line.startswith('Profile'):
                current_resource['profile'] = line.replace('Profile', '').strip()
            elif line.startswith('Path'):
                current_resource['path'] = line.replace('Path', '').strip()

            if 'Data Elements' in line and 'FHIR Data Elements' not in line:
                in_data_elements = True
                header_seen = False
                i += 1
                continue

            if line.startswith('Endpoints'):
                in_data_elements = False
                i += 1
                continue

            if in_data_elements:
                # Skip header rows
                if 'US Core 6.1.0 Field' in line or 'Data Type' in line or 'Short Description' in line:
                    header_seen = True
                    i += 1
                    continue

                # Skip page numbers and blank lines
                if re.match(r'^\d+$', line) or not line:
                    i += 1
                    continue

                # Parse data element rows - they have field name, data type, and description
                # The layout uses fixed columns roughly
                raw = lines[i]
                if len(raw.strip()) > 0 and not raw.strip().startswith('GET') and not raw.strip().startswith('POST'):
                    # Try to parse as a table row with at least a field name
                    parts = raw.rstrip('\n')
                    # Use column positions from the PDF layout
                    # Field names start at left, types in middle, descriptions at right
                    # Split by multiple spaces
                    cols = re.split(r'\s{3,}', parts.strip())
                    if len(cols) >= 2:
                        field_name = cols[0].strip()
                        # Skip non-field lines
                        if field_name in ('', 'Type', 'Query', 'Path', 'Content Type',
                                         'application/x-www-form-urlencoded'):
                            i += 1
                            continue
                        if field_name.startswith('GET') or field_name.startswith('POST'):
                            i += 1
                            continue

                        data_type = cols[1].strip() if len(cols) >= 2 else ''
                        description = cols[2].strip() if len(cols) >= 3 else ''

                        # Check if next lines are continuation of description
                        j = i + 1
                        while j < len(lines):
                            next_line = lines[j].rstrip('\n')
                            next_stripped = next_line.strip()
                            if not next_stripped or re.match(r'^\d+$', next_stripped):
                                j += 1
                                continue
                            # If line is indented far right (continuation of description)
                            leading_spaces = len(next_line) - len(next_line.lstrip())
                            next_cols = re.split(r'\s{3,}', next_stripped)
                            if leading_spaces > 30 and len(next_cols) == 1:
                                description += ' ' + next_stripped
                                j += 1
                            else:
                                break

                        if field_name and data_type:
                            current_resource['data_elements'].append({
                                'field': field_name,
                                'data_type': data_type,
                                'description': description
                            })
                            i = j
                            continue

        i += 1

    if current_resource:
        resources.append(current_resource)

    return resources


def main():
    text_file = '/home/jmandel/hobby/ehi-export-analysis/abstraction/carbon-health-technologies-inc--carbyos-ehr/analysis/fhir-api-full-text.txt'
    resources = parse_fhir_elements(text_file)

    # Output full inventory
    output = {
        'source': 'carbonhealth-fhir-api-doc-v1_2.pdf',
        'document_type': 'FHIR API Documentation (g)(10) - NOT (b)(10) EHI Export',
        'total_resources': len(resources),
        'total_data_elements': sum(len(r['data_elements']) for r in resources),
        'resources': resources
    }

    out_path = '/home/jmandel/hobby/ehi-export-analysis/abstraction/carbon-health-technologies-inc--carbyos-ehr/analysis/fhir-resources-inventory.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)

    # Print summary
    print(f"Total FHIR resources: {len(resources)}")
    print(f"Total data elements: {sum(len(r['data_elements']) for r in resources)}")
    print()
    print(f"{'Resource':<25} {'Elements':>8}  Profile")
    print('-' * 80)
    for r in resources:
        print(f"{r['resource']:<25} {len(r['data_elements']):>8}  {r['profile']}")

    # Elements with descriptions
    total_with_desc = sum(1 for r in resources for e in r['data_elements'] if e.get('description'))
    total = sum(len(r['data_elements']) for r in resources)
    print(f"\nElements with descriptions: {total_with_desc}/{total}")


if __name__ == '__main__':
    main()
