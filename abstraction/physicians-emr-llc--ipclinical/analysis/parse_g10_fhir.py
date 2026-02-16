#!/usr/bin/env python3
"""Parse IPClinical g10 API documentation to extract FHIR resources and their fields."""

import re
import json

with open("g10_raw_text.txt", "r") as f:
    text = f.read()

# The TOC tells us the FHIR resource sections
# Extract sections starting from "Patient" through "Clinical Notes Guidance"
resource_sections = [
    "Patient",
    "Allergy Intolerance",
    "Care Plan",
    "Care Team",
    "Conditions",
    "Implantable Device",
    "Diagnostic Report for Report and Note exchange",
    "Diagnostic Report for Laboratory Results Reporting",
    "Document Reference",
    "Goal",
    "Immunization",
    "MedicationRequest",
    "Smoking Status Observation",
    "Pediatric Weight for Height Observation",
    "Laboratory Result Observation",
    "Pediatric BMI for Age Observation",
    "Pulse Oximetry",
    "Pediatric Head Occipital-frontal Circumference Percentile",
    "Observation Body Height",
    "Observation Body Temperature",
    "Observation Blood Pressure",
    "Observation Body Weight",
    "Observation Heart Rate",
    "Observation Respiratory Rate",
    "Procedure",
    "Encounter",
    "Organization",
    "Practitioner",
    "Provenance",
    "Clinical Notes Guidance",
]

# Map section names to FHIR resource types
section_to_resource = {
    "Patient": "Patient",
    "Allergy Intolerance": "AllergyIntolerance",
    "Care Plan": "CarePlan",
    "Care Team": "CareTeam",
    "Conditions": "Condition",
    "Implantable Device": "Device",
    "Diagnostic Report for Report and Note exchange": "DiagnosticReport",
    "Diagnostic Report for Laboratory Results Reporting": "DiagnosticReport",
    "Document Reference": "DocumentReference",
    "Goal": "Goal",
    "Immunization": "Immunization",
    "MedicationRequest": "MedicationRequest",
    "Smoking Status Observation": "Observation",
    "Pediatric Weight for Height Observation": "Observation",
    "Laboratory Result Observation": "Observation",
    "Pediatric BMI for Age Observation": "Observation",
    "Pulse Oximetry": "Observation",
    "Pediatric Head Occipital-frontal Circumference Percentile": "Observation",
    "Observation Body Height": "Observation",
    "Observation Body Temperature": "Observation",
    "Observation Blood Pressure": "Observation",
    "Observation Body Weight": "Observation",
    "Observation Heart Rate": "Observation",
    "Observation Respiratory Rate": "Observation",
    "Procedure": "Procedure",
    "Encounter": "Encounter",
    "Organization": "Organization",
    "Practitioner": "Practitioner",
    "Provenance": "Provenance",
    "Clinical Notes Guidance": "DocumentReference",
}

# Count unique FHIR resource types
unique_resources = set(section_to_resource.values())
print(f"Unique FHIR resource types documented: {len(unique_resources)}")
print(f"Resource types: {sorted(unique_resources)}")
print(f"Total sections (profiles/views): {len(resource_sections)}")

# Now try to extract field-level info from each section
# Look for table-like patterns with field names

lines = text.split('\n')

# Find lines that look like field definitions (common pattern: field name followed by type/cardinality)
field_pattern = re.compile(r'^\s{2,}(\w[\w.]+)\s+', re.MULTILINE)

# Extract the Capability Statement section to understand supported interactions
cap_start = text.find("Capability Statement")
cap_end = text.find("Patient\n", cap_start + 100) if cap_start > 0 else -1

if cap_start > 0 and cap_end > 0:
    cap_text = text[cap_start:cap_end]
    # Count resource types in CapabilityStatement
    resource_refs = re.findall(r'"type"\s*:\s*"(\w+)"', cap_text)
    if resource_refs:
        print(f"\nResource types in CapabilityStatement: {len(resource_refs)}")
        for r in resource_refs:
            print(f"  - {r}")

# Build entity inventory
entities = []
for i, section in enumerate(resource_sections):
    fhir_type = section_to_resource[section]
    
    # Find section in text
    section_start = text.find(section + "\n")
    if section_start < 0:
        section_start = text.find(section)
    
    if i + 1 < len(resource_sections):
        next_section = resource_sections[i + 1]
        section_end = text.find(next_section + "\n", section_start + len(section))
        if section_end < 0:
            section_end = text.find(next_section, section_start + len(section))
    else:
        section_end = len(text)
    
    if section_start >= 0 and section_end > section_start:
        section_text = text[section_start:section_end]
        
        # Count "Must Support" elements by looking for field-like rows in tables
        # Look for patterns like "Element Name    Must Support    Cardinality"
        must_support = section_text.lower().count("must support")
        
        # Look for element/field names - lines that have structure like:
        # fieldName    Yes/No    0..1/1..1    type
        field_lines = []
        for line in section_text.split('\n'):
            # Look for lines with field-like patterns
            if re.match(r'\s+\w+[\w.]*\s+(Yes|No)\s+', line):
                field_lines.append(line.strip())
            elif re.match(r'\s+\w+[\w.]*\s+\d+\.\.\d+', line):
                field_lines.append(line.strip())
        
        entities.append({
            "section_name": section,
            "fhir_resource_type": fhir_type,
            "fields_found": len(field_lines),
            "must_support_mentions": must_support,
            "section_length_chars": len(section_text),
        })

# Output summary
total_fields = sum(e["fields_found"] for e in entities)
print(f"\nTotal field-like rows found across all sections: {total_fields}")

# Save inventory
with open("fhir_resource_inventory.json", "w") as f:
    json.dump(entities, f, indent=2)

print("\nPer-section breakdown:")
for e in entities:
    print(f"  {e['section_name']:55s} | {e['fhir_resource_type']:20s} | {e['fields_found']:3d} fields | {e['section_length_chars']:6d} chars")
