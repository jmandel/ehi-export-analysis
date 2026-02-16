"""Generate the full entity inventory JSON from parsed EHI export page data.
Separates actual FHIR resources from generic feature descriptions, and 
builds a complete field-level inventory of everything documented."""

import json

with open("ehi-export-page-parsed.json") as f:
    data = json.load(f)

# Filter FHIR resources: remove "Key Features" items that aren't actual FHIR resources
actual_fhir_resources = [
    r for r in data["export_formats"][1]["resources"]
    if r["resource"] not in ("Granular Data", "Web Standards", "Extensibility")
]

# Also compare with the FHIR Resources page (from screenshot):
# Clinical: AllergyIntolerance, CarePlan, CareTeam, Condition, DiagnosticReport,
#           Encounter, Goal, Immunization, Medication, MedicationRequest, Observation, Procedure
# References: DocumentReference, Device, Location, Organization, Patient, 
#            Practitioner, PractitionerRole, Provenance, QuestionnaireResponse,
#            RelatedPerson, ServiceRequest

fhir_api_resources = {
    "Clinical Information": [
        "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
        "DiagnosticReport", "Encounter", "Goal", "Immunization",
        "Medication", "MedicationRequest", "Observation", "Procedure"
    ],
    "Resources and References": [
        "DocumentReference", "Device", "Location", "Organization",
        "Patient", "Practitioner", "PractitionerRole", "Provenance",
        "QuestionnaireResponse", "RelatedPerson", "ServiceRequest"
    ]
}

ehi_page_resource_names = [r["resource"] for r in actual_fhir_resources]
all_api_resources = fhir_api_resources["Clinical Information"] + fhir_api_resources["Resources and References"]

# Resources on EHI page but NOT in FHIR API docs
ehi_only = [r for r in ehi_page_resource_names if r not in all_api_resources]
# Resources in FHIR API but NOT on EHI page
api_only = [r for r in all_api_resources if r not in ehi_page_resource_names]

# Build full entity inventory
entities = []

# 1. FHIR resources (union of both lists)
all_fhir = set(ehi_page_resource_names + all_api_resources)
for resource in sorted(all_fhir):
    desc_from_ehi = next((r["description"] for r in actual_fhir_resources if r["resource"] == resource), None)
    on_ehi_page = resource in ehi_page_resource_names
    on_api_page = resource in all_api_resources
    
    entities.append({
        "entity_name": resource,
        "format": "FHIR R4",
        "category": "Clinical Information" if resource in fhir_api_resources["Clinical Information"] else 
                    "Resources and References" if resource in fhir_api_resources["Resources and References"] else
                    "EHI Export Page Only",
        "description": desc_from_ehi,
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "on_ehi_export_page": on_ehi_page,
        "on_fhir_api_page": on_api_page,
        "documentation_level": "resource-name-only",
        "notes": "No field-level documentation; only resource name and one-line generic description"
    })

# 2. BroadStreet Notes (HTML) - the only proprietary format with field-level docs
notes_entity = {
    "entity_name": "BroadStreet Notes (HTML)",
    "format": "HTML",
    "category": "Clinical Notes",
    "description": "Clinical notes exported as HTML with structured sections",
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "on_ehi_export_page": True,
    "on_fhir_api_page": False,
    "documentation_level": "field-level",
    "notes": "Only BroadStreet-specific export structure with field-level detail"
}

notes_data = data["export_formats"][2]
for section in notes_data["sections"]:
    for field in section["fields"]:
        fname = field["field_name"]
        fdesc = field["description"]
        notes_entity["fields"].append({
            "field_name": fname,
            "description": fdesc,
            "section": section["subsection"],
            "type": None,
            "nullable": None,
            "max_length": None,
            "foreign_key": None,
            "value_set": None,
            "has_description": bool(fdesc and fdesc.strip())
        })

notes_entity["field_count"] = len(notes_entity["fields"])
notes_entity["fields_with_descriptions"] = sum(1 for f in notes_entity["fields"] if f["has_description"])
entities.append(notes_entity)

# 3. CDA 2.1 entity (no field-level detail)
entities.append({
    "entity_name": "CDA 2.1 Document",
    "format": "CDA 2.1 (XML)",
    "category": "Clinical Documents",
    "description": "Patient data exported as CDA documents adhering to CDA 2.1 standard",
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "on_ehi_export_page": True,
    "on_fhir_api_page": False,
    "documentation_level": "format-name-only",
    "notes": "Generic CDA description only; no BroadStreet-specific templates, sections, or fields documented"
})

# Build inventory output
inventory = {
    "vendor": "BroadStreet Health LLC",
    "product": "BroadStreet",
    "extraction_source": "ehi-export-page-rendered.html + fhir-resources-page.png",
    "total_entities": len(entities),
    "total_fields_documented": sum(e["field_count"] for e in entities),
    "total_fields_with_descriptions": sum(e["fields_with_descriptions"] for e in entities),
    "fhir_resources_on_ehi_page": len(ehi_page_resource_names),
    "fhir_resources_on_api_page": len(all_api_resources),
    "fhir_resources_total_unique": len(all_fhir),
    "ehi_page_only_resources": ehi_only,
    "api_page_only_resources": api_only,
    "notes_html_fields": notes_entity["field_count"],
    "notes_html_sections": len(notes_data["sections"]),
    "by_format": {
        "FHIR R4": {
            "entity_count": sum(1 for e in entities if e["format"] == "FHIR R4"),
            "field_count": 0,
            "note": "No field-level documentation for any FHIR resource"
        },
        "HTML (BroadStreet Notes)": {
            "entity_count": 1,
            "field_count": notes_entity["field_count"],
            "note": "Field names and descriptions only; no types, constraints, or examples"
        },
        "CDA 2.1": {
            "entity_count": 1,
            "field_count": 0,
            "note": "No BroadStreet-specific documentation"
        }
    },
    "entities": entities
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== Full Entity Inventory Summary ===")
print(f"Total entities: {inventory['total_entities']}")
print(f"Total fields documented: {inventory['total_fields_documented']}")
print(f"Fields with descriptions: {inventory['total_fields_with_descriptions']}")
print(f"\nFHIR resources on EHI page: {len(ehi_page_resource_names)}")
print(f"FHIR resources on API page: {len(all_api_resources)}")
print(f"Total unique FHIR resources: {len(all_fhir)}")
print(f"\nResources on EHI page but NOT in FHIR API: {ehi_only}")
print(f"Resources in FHIR API but NOT on EHI page: {api_only}")
print(f"\nNotes HTML: {notes_entity['field_count']} fields across {len(notes_data['sections'])} sections")
print(f"Notes fields with descriptions: {notes_entity['fields_with_descriptions']}")
