"""
Parse the B10 EHI Export PDF and FHIR docs screenshot to build a structured
inventory of what the export covers. Since there's no data dictionary,
this captures the export components as described in the documentation.
"""

import json

# Export components extracted from B10-Electronic-Health-information-Export.pdf
# (4 pages, created 2023-10-03 by Nouman Zafar)
export_components = [
    {
        "id": "ccda_export",
        "name": "CCD/C-CDA Documents",
        "format": "HL7 C-CDA XML (R2.1)",
        "description": "Bulk export of HL7 CCDA xml files which comply to US Core Data for Interoperability (USCDI), Version 1 requirements.",
        "standard": "C-CDA R2.1, USCDI v1",
        "fields_documented": 0,
        "field_level_detail": False,
        "sample_data_provided": False,
        "notes": "References standard HL7 C-CDA specifications. No product-specific mapping or customization documented."
    },
    {
        "id": "fhir_bulk_data",
        "name": "FHIR Bulk Data Access",
        "format": "FHIR R4 / US Core STU V3.1.1",
        "description": "HL7 FHIR R4, FHIR US Core Implementation Guide STU V3.1.1, HL7 FHIR Bulk Data export.",
        "standard": "FHIR R4, US Core 3.1.1",
        "fields_documented": 0,
        "field_level_detail": False,
        "sample_data_provided": False,
        "notes": "Explicitly references 170.315(g)(10) SmartOnFHIR API Documentation. Points to documents.maximus.care which documents standard US Core resources only."
    },
    {
        "id": "demographics_insurance_excel",
        "name": "Patient Demographics & Insurance",
        "format": "Excel",
        "description": "This file offers a comprehensive view of demographics and insurance details structured for clarity and ease of access.",
        "standard": None,
        "fields_documented": 0,
        "field_level_detail": False,
        "sample_data_provided": False,
        "notes": "One-sentence description only. No column headers, field names, data types, or value sets documented."
    },
    {
        "id": "appointments_excel",
        "name": "Appointments",
        "format": "Excel",
        "description": "This file offers a comprehensive view of all future appointment details, structured for clarity and ease of access.",
        "standard": None,
        "fields_documented": 0,
        "field_level_detail": False,
        "sample_data_provided": False,
        "notes": "One-sentence description only. Specifies 'future' appointments only — historical visit data apparently excluded."
    },
    {
        "id": "documents_files",
        "name": "Documents (Scanned Documents)",
        "format": "PDF, JPG, PNG",
        "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document in the patient's record. Sorted and indexed within patient chart number folders with category subfolders.",
        "standard": None,
        "fields_documented": 0,
        "field_level_detail": False,
        "sample_data_provided": False,
        "notes": "Documents organized by patient chart number with category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.). No metadata schema or manifest documented."
    }
]

# FHIR resources documented at documents.maximus.care (from screenshot)
# These are standard US Core STU3.1.1 resources — no custom profiles or extensions
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
    "Location",
    "MedicationRequest",
    "Observation",  # vitals, labs, smoking status, pediatric
    "Organization",
    "Patient",
    "Practitioner",
    "Procedure",
    "Provenance"
]

# Build full inventory
inventory = {
    "product": "Maximus",
    "version": "1.0",
    "vendor": "MaxRemind Inc",
    "source_document": "B10-Electronic-Health-information-Export.pdf",
    "source_document_pages": 4,
    "source_document_date": "2023-10-03",
    "fhir_docs_url": "https://documents.maximus.care/",
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema_files": False,
    "export_components": export_components,
    "fhir_resources_documented": fhir_resources,
    "fhir_resource_count": len(fhir_resources),
    "total_export_components": len(export_components),
    "components_with_field_detail": 0,
    "components_with_sample_data": 0,
    "entities": []
}

# Build entity-level inventory
# Since there's no data dictionary, entities are the export components themselves
# plus individual FHIR resources
entities = []

# Add the non-FHIR export components as entities
for comp in export_components:
    if comp["id"] not in ("ccda_export", "fhir_bulk_data"):
        entities.append({
            "name": comp["name"],
            "source": comp["id"],
            "format": comp["format"],
            "category": "Proprietary Export",
            "fields": [],
            "field_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "description": comp["description"],
            "notes": comp["notes"]
        })

# Add C-CDA as a single entity (no section-level detail provided)
entities.append({
    "name": "C-CDA Clinical Document",
    "source": "ccda_export",
    "format": "HL7 C-CDA XML R2.1",
    "category": "Clinical Exchange Standard",
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "description": "C-CDA documents complying with USCDI v1. No product-specific sections or customizations documented.",
    "notes": "Standard C-CDA — inherits whatever sections the standard defines. No vendor documentation of which sections are populated."
})

# Add each FHIR resource as an entity
for resource in fhir_resources:
    entities.append({
        "name": resource,
        "source": "fhir_bulk_data",
        "format": "FHIR R4 / US Core STU 3.1.1",
        "category": "FHIR US Core Resource",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "description": f"Standard US Core STU3.1.1 {resource} resource. No vendor-specific extensions or custom mappings documented.",
        "notes": "Part of (g)(10) FHIR API. No evidence of (b)(10)-specific additions."
    })

inventory["entities"] = entities

# Summary stats
summary = {
    "product": "Maximus 1.0",
    "vendor": "MaxRemind Inc",
    "total_export_components": len(export_components),
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema_files": False,
    "fhir_resource_count": len(fhir_resources),
    "non_fhir_components": sum(1 for e in entities if e["category"] != "FHIR US Core Resource"),
    "categories": {},
    "source_document_pages": 4,
    "documentation_quality": "Very poor — no field-level documentation for any component"
}

# Category breakdown
cats = {}
for e in entities:
    cat = e["category"]
    if cat not in cats:
        cats[cat] = {"entity_count": 0, "total_fields": 0}
    cats[cat]["entity_count"] += 1
    cats[cat]["total_fields"] += e["field_count"]
summary["categories"] = cats

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== Summary ===")
print(f"Total export components: {len(export_components)}")
print(f"Total entities (components + FHIR resources): {len(entities)}")
print(f"FHIR resources: {len(fhir_resources)}")
print(f"Non-FHIR components: {summary['non_fhir_components']}")
print(f"Total fields documented: 0 (no data dictionary exists)")
print(f"Fields with descriptions: 0")
print(f"Has sample data: No")
print(f"Has schema files: No")
print(f"\nCategory breakdown:")
for cat, info in cats.items():
    print(f"  {cat}: {info['entity_count']} entities, {info['total_fields']} fields")
