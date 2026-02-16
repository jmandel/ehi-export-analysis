#!/usr/bin/env python3
"""Parse Radysans EHR (b)(10) export artifacts and produce entity inventories."""

import json

# The (b)(10) documentation explicitly lists two export mechanisms:
# 1. C-CDA with 22 sections (USCDI v1)
# 2. FHIR R4 via (g)(10) API with 18 resource types
# There is NO product-specific data dictionary, no field-level documentation,
# and no mapping beyond the standard specs.

# C-CDA sections listed in B-10-Documentation.pdf (1 page)
ccda_sections = [
    "Allergies, Adverse Reactions, Alerts",
    "Assessment Plan",
    "Chief Complaint",
    "Cognitive Status",
    "Demographics",
    "Reason for Visit / Encounters",
    "Family History",
    "Functional Status",
    "Goals",
    "Health Concerns",
    "Immunizations",
    "Instructions",
    "Lab Results",
    "Medical Equipment UDI",
    "Medications",
    "Plan of Care",
    "Problem List",
    "Procedures",
    "Reason for Referral",
    "Social History",
    "Plan of Treatment",
    "Vitals",
]

# FHIR resource types from G10ApplicationAccessTermsandCondition.pdf (sections 1.1-1.18)
fhir_resources = [
    "AllergyIntolerance",
    "CarePlan",
    "CareTeam",
    "Condition",
    "Device",
    "DiagnosticReport",
    "DocumentReference",
    "Encounter",
    "Goal",
    "Immunization",
    "MedicationRequest",
    "Observation",
    "Organization",
    "Patient",
    "Practitioner",
    "PractitionerRole",
    "Procedure",
    "Provenance",
]

# These are exactly the US Core STU3.1.1 resource types - no vendor extensions
us_core_stu3_resources = {
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "Medication", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "PractitionerRole", "Procedure", "Provenance",
}

# Build entity inventory
entities = []

# Add C-CDA sections as entities
for section in ccda_sections:
    entities.append({
        "entity_name": section,
        "entity_type": "ccda_section",
        "format": "C-CDA",
        "source": "B-10-Documentation.pdf",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation provided. Vendor references HL7 C-CDA spec only.",
    })

# Add FHIR resources as entities
for resource in fhir_resources:
    in_us_core = resource in us_core_stu3_resources
    entities.append({
        "entity_name": resource,
        "entity_type": "fhir_resource",
        "format": "FHIR R4",
        "source": "G10ApplicationAccessTermsandCondition.pdf",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "is_us_core_resource": in_us_core,
        "has_sample_output": True,
        "has_vendor_extensions": False,
        "notes": "Standard US Core resource. No vendor-specific extensions or additional fields documented.",
    })

inventory_full = {
    "vendor": "Radysans, Inc",
    "product": "Radysans EHR",
    "version": "5.0",
    "export_formats": ["C-CDA", "FHIR R4"],
    "documentation_source": "B-10-Documentation.pdf (1 page), G10ApplicationAccessTermsandCondition.pdf (41 pages)",
    "has_data_dictionary": False,
    "has_field_level_documentation": False,
    "total_entities": len(entities),
    "ccda_section_count": len(ccda_sections),
    "fhir_resource_count": len(fhir_resources),
    "total_fields_documented": 0,
    "notes": (
        "The vendor provides NO product-specific data dictionary. The (b)(10) documentation "
        "lists C-CDA section names and references the HL7 C-CDA spec for details. "
        "The FHIR export references the (g)(10) API documentation which lists 18 US Core "
        "resource types with sample JSON outputs — all standard US Core with no vendor extensions. "
        "No field-level mapping, no value sets, no relationship documentation."
    ),
    "entities": entities,
}

# Write full inventory
with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(inventory_full, f, indent=2)

# Build summary
summary = {
    "vendor": "Radysans, Inc",
    "product": "Radysans EHR",
    "version": "5.0",
    "export_formats": ["C-CDA", "FHIR R4"],
    "has_data_dictionary": False,
    "has_field_level_documentation": False,
    "total_entities": len(entities),
    "breakdown": {
        "ccda_sections": {
            "count": len(ccda_sections),
            "sections": ccda_sections,
        },
        "fhir_resources": {
            "count": len(fhir_resources),
            "resources": fhir_resources,
            "all_are_us_core": all(r in us_core_stu3_resources for r in fhir_resources),
            "vendor_extensions_found": False,
        },
    },
    "field_documentation": {
        "total_fields_documented": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "percentage_with_descriptions": "N/A",
    },
    "coverage_assessment": {
        "uscdi_domains_covered": [
            "Demographics", "Allergies", "Medications", "Problems/Conditions",
            "Procedures", "Lab Results", "Vital Signs", "Immunizations",
            "Encounters", "Care Plans", "Goals", "Care Team",
            "Clinical Notes (via DocumentReference)", "Devices",
            "Social History", "Family History", "Diagnostic Reports",
        ],
        "non_uscdi_domains_covered": [],
        "domains_missing": [
            "Billing/Claims", "Insurance/Coverage details", "Payments",
            "Referral workflows", "Patient communications/portal messages",
            "Custom forms", "Medication administration records",
            "Scanned documents", "Appointment/scheduling data",
        ],
    },
}

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print stats
print(f"Total entities: {len(entities)}")
print(f"  C-CDA sections: {len(ccda_sections)}")
print(f"  FHIR resources: {len(fhir_resources)}")
print(f"Total field-level documentation: 0 (none provided)")
print(f"All FHIR resources are standard US Core: {all(r in us_core_stu3_resources for r in fhir_resources)}")
print(f"Vendor extensions found: False")
print(f"Data dictionary provided: False")
print("Files written: entity-inventory-full.json, entity-inventory-summary.json")
