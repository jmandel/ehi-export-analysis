#!/usr/bin/env python3
"""Parse the C-CDA data dictionary from the EHIexport.pdf text extraction.

This script extracts the structured data elements from the PDF's data dictionary
(pages 12-19) and produces a complete JSON inventory of all C-CDA sections and
their fields.
"""

import json
import re
import sys

# The full text extracted from EHIexport.pdf via pdftotext -layout
# We'll parse the data dictionary section (pages 12-19)

PDF_TEXT = """
Patient Demographics/Information
Patient Name                   patient/name                                         -
Sex                            patient/administrativeGenderCode     2.16.840.1.113883.5.1    AdministrativeGender
Date of Birth                  patient/birthTime
Race                           patient/raceCode            2.16.840.1.113883.6.238   Race & Ethnicity - CDC
Ethnicity                      patient/ethnicGroupCode                          2.16.840.1.113883.6.238                        Race & Ethnicity - CDC
Preferred Language             patient/languageCommunication/languageCode

Provider's name and office contact information
Performer                       documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name
Performer                       documentationOf/serviceEvent/performer/assignedEntity/telecom
Performer                       documentationOf/serviceEvent/performer/assignedEntity/addr

Date and Location of visit [2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01]
Encounter                       entry/encounter/effectiveTime/@value
Encounter                       entry/encounter/participant/participantRole/addr

Chief Complaint and Reason for visit [2.16.840.1.113883.10.20.22.2.13 : 2014-06-09]
Patient visit details/complaints

Encounters [2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01]
Encounter Code and Code Description              2.16.840.1.113883.10.20.22.4.49: 2015-08-01    2.16.840.1.113883.6.12            CPT
Performer
Diagnosis                                             2.16.840.1.113883.6.96    SNOMED and ICD10
Location
Date

Immunizations [2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01]
Vaccine                       2.16.840.1.113883.10.20.22.4.52: 2015-08-01    2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12    CVX and CPT-4
Date
Status
Route                                                 2.16.840.1.113883.3.26.1.1    National Cancer Institute (NCI) Thesaurus
Site                                                  2.16.840.1.113883.6.96    SNOMED
Manufacturer
Dose
Lot Number
Notes

Instructions [2.16.840.1.113883.10.20.22.2.45 : 2014-06-09]
Patient Instructions/Followup Reasons                       2.16.840.1.113883.10.20.22.4.20: 2014-06-09    2.16.840.1.113883.6.96       SNOMED

Treatment Plan [2.16.840.1.113883.10.20.22.2.10 : 2014-06-09]
Planned Observation             2.16.840.1.113883.10.20.22.4.44: 2014-06-09    2.16.840.1.113883.6.1       LOINC
Planned Date                    2.16.840.1.113883.10.20.22.4.40: 2014-06-09

Social History [2.16.840.1.113883.10.20.22.2.17 : 2015-08-01]
Social History Observation      2.16.840.1.113883.10.20.22.4.78: 2014-06-09    2.16.840.1.113883.6.1                    LOINC
Description                                       2.16.840.1.113883.6.96                  SNOMED
Dates Observed

Problems [2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01]
Problem                        2.16.840.1.113883.10.20.22.4.3: 2015-08-01    2.16.840.1.113883.6.96      SNOMED and ICD10
Status
Active date

Medications [2.16.840.1.113883.10.20.22.2.1.1 : 2014-06-09]
Medication                   2.16.840.1.113883.10.20.22.4.16: 2014-06-09    2.16.840.1.113883.6.88   RxNorm and NDC
Directions
Start Date
End Date
Status

Medication Allergies [2.16.840.1.113883.10.20.22.2.6.1 : 2015-08-01]
Substance                    2.16.840.1.113883.10.20.22.4.30: 2015-08-01    2.16.840.1.113883.6.88   RxNorm
Reaction                                           2.16.840.1.113883.6.96   SNOMED
Severity                                           2.16.840.1.113883.6.96   SNOMED
Status                                             2.16.840.1.113883.6.96   SNOMED

Laboratory Tests
Test Code
Code System                                        2.16.840.1.113883.6.1    LOINC
Name
Date

Laboratory Information
Lab Name
Lab Address
Test Report Date
Test Performed
Specimen Source

Laboratory value(s)/result(s) [2.16.840.1.113883.10.20.22.2.3.1 : 2015-08-01]
Result Type                  2.16.840.1.113883.10.20.22.4.1: 2015-08-01    2.16.840.1.113883.6.1    LOINC
Result Value
Relevant Reference Range
Interpretation
Date

Vitals [2.16.840.1.113883.10.20.22.2.4.1 : 2015-08-01]
Observation                 2.16.840.1.113883.10.20.22.4.26: 2015-08-01    2.16.840.1.113883.6.1    LOINC
Observation Date/Time

Goal [2.16.840.1.113883.10.20.22.2.60]
Goal                        2.16.840.1.113883.10.20.22.4.121
Value
Date

Procedures [2.16.840.1.113883.10.20.22.2.7.1 : 2014-06-09]
Procedure                   2.16.840.1.113883.10.20.22.4.14: 2014-06-09    2.16.840.1.113883.6.12   CPT-4 or SNOMED or HCPCS
Date

Care team member(s) [2.16.840.1.113883.10.20.22.2.500 : 2019-07-01]
Care Giver Name             2.16.840.1.113883.10.20.22.4.500:2019-07-01
Specialty
Date

Reason for Referral [1.3.6.1.4.1.19376.1.5.3.1.3.1 : 2014-06-09]
Reason for visit             2.16.840.1.113883.10.20.22.4.140    2.16.840.1.113883.6.96    SNOMED

Medical Equipment [2.16.840.1.113883.10.20.22.2.23 : 2014-06-09]
Implanted Device             2.16.840.1.113883.10.20.22.4.14: 2014-06-09    2.16.840.1.113883.6.96    SNOMED
GMDN PT Description

Mental Status [2.16.840.1.113883.10.20.22.2.56 : 2015-08-01]
Assessment                   2.16.840.1.113883.10.20.22.4.74: 2015-08-01
Assessment Date
Results                                              2.16.840.1.113883.6.96   SNOMED
Comments

Functional Status [2.16.840.1.113883.10.20.22.2.14 : 2014-06-09]
Assessment                   2.16.840.1.113883.10.20.22.4.67: 2014-06-09
Assessment Date
Results                                              2.16.840.1.113883.6.96   SNOMED
Comments

Health Concern [2.16.840.1.113883.10.20.22.2.58 : 2015-08-01]
Concern / Observation        2.16.840.1.113883.10.20.22.4.132:2015-08-01    2.16.840.1.113883.6.96       SNOMED
Status
Date
"""

def parse_dictionary():
    sections = []
    current_section = None
    
    for line in PDF_TEXT.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Check if this is a section header
        # Section headers either have an OID in brackets or are known header patterns
        section_with_oid = re.match(r'^(.+?)\s*\[([0-9.:]+(?:\s*:\s*\d{4}-\d{2}-\d{2})?)\]', line)
        known_headers = [
            'Patient Demographics/Information',
            "Provider's name and office contact information",
            'Laboratory Tests',
            'Laboratory Information',
        ]
        
        if section_with_oid:
            section_name = section_with_oid.group(1).strip()
            template_id = section_with_oid.group(2).strip()
            current_section = {
                'section': section_name,
                'template_id': template_id,
                'fields': []
            }
            sections.append(current_section)
        elif line in known_headers:
            current_section = {
                'section': line,
                'template_id': None,
                'fields': []
            }
            sections.append(current_section)
        elif current_section is not None:
            # Parse as a field line
            # Try to extract: field_name, xpath, code_system_oid, code_system_name
            field = {'name': line, 'xpath': None, 'code_system_oid': None, 'code_system_name': None}
            
            # Try to split on whitespace patterns with OIDs
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 1:
                field['name'] = parts[0].strip()
            
            # Look for OIDs in the line
            oid_matches = re.findall(r'(2\.16\.840\.1\.\d+[\d.]+(?::\s*\d{4}-\d{2}-\d{2})?)', line)
            
            # Look for xpath-like patterns
            xpath_match = re.search(r'((?:entry|patient|documentationOf|performer)[/\w@.]+)', line)
            if xpath_match:
                field['xpath'] = xpath_match.group(1)
            elif oid_matches and len(oid_matches) >= 1:
                # First OID might be xpath-style template ref
                first_oid = oid_matches[0]
                if '10.20.22.4' in first_oid:
                    field['xpath'] = first_oid
                    oid_matches = oid_matches[1:]
            
            # Remaining OIDs are code systems
            code_system_names = []
            for oid in oid_matches:
                if '10.20.22' not in oid:
                    field['code_system_oid'] = oid.split(':')[0].strip()
            
            # Extract code system name from the end
            name_patterns = ['SNOMED', 'ICD10', 'LOINC', 'RxNorm', 'NDC', 'CVX', 'CPT', 'CPT-4', 'HCPCS',
                           'AdministrativeGender', 'Race & Ethnicity - CDC',
                           'National Cancer Institute']
            for pat in name_patterns:
                if pat in line and pat not in field['name']:
                    code_system_names.append(pat)
            if code_system_names:
                field['code_system_name'] = ', '.join(code_system_names)
            
            current_section['fields'].append(field)
    
    return sections


def main():
    sections = parse_dictionary()
    
    # Build full inventory
    inventory = {
        'source': 'EHIexport.pdf (pages 12-19)',
        'format': 'C-CDA (Consolidated CDA)',
        'standard': '§170.205(a)(4) HL7 CDA R2 Consolidated CDA Templates DSTU R2.1 Aug 2015',
        'uscdi_version': 'USCDI Version 1',
        'total_sections': len(sections),
        'total_fields': sum(len(s['fields']) for s in sections),
        'fields_with_code_system': sum(
            1 for s in sections for f in s['fields'] if f.get('code_system_oid') or f.get('code_system_name')
        ),
        'fields_with_xpath': sum(
            1 for s in sections for f in s['fields'] if f.get('xpath')
        ),
        'sections': sections
    }
    
    # Print summary
    print(f"=== C-CDA Data Dictionary Summary ===")
    print(f"Total sections: {inventory['total_sections']}")
    print(f"Total fields: {inventory['total_fields']}")
    print(f"Fields with code system: {inventory['fields_with_code_system']}")
    print(f"Fields with XPATH/template: {inventory['fields_with_xpath']}")
    print()
    
    for s in sections:
        coded = sum(1 for f in s['fields'] if f.get('code_system_oid') or f.get('code_system_name'))
        print(f"  {s['section']}: {len(s['fields'])} fields ({coded} with code systems)")
    
    # Write full inventory
    with open('full-entity-inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f"\nFull inventory written to full-entity-inventory.json")


if __name__ == '__main__':
    main()
