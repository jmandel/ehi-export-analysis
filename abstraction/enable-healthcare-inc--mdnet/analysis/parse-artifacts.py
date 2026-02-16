#!/usr/bin/env python3
"""
Parse all EHI export artifacts for Enable Healthcare MDnet and produce
entity-inventory-full.json and entity-inventory-summary.json.

Sources:
- EHI_DATA_EXPort_GUIDE.pdf (9-page PDF describing export methods)
- fhir-capability-statement.json (FHIR R4 CapabilityStatement)

Since the CSV data dictionary URL (https://emr.ehiconnect.com/docs/) returns 404,
we can only document what's described in the PDF and FHIR CapabilityStatement.
"""

import json
import os

ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(os.path.dirname(ANALYSIS_DIR), "downloads")

# Parse FHIR CapabilityStatement
with open(os.path.join(DOWNLOADS_DIR, "fhir-capability-statement.json")) as f:
    cs = json.load(f)

fhir_resources = []
for rest in cs.get("rest", []):
    for resource in rest.get("resource", []):
        rtype = resource["type"]
        interactions = [i["code"] for i in resource.get("interaction", [])]
        search_params = [p["name"] for p in resource.get("searchParam", [])]
        fhir_resources.append({
            "type": rtype,
            "interactions": interactions,
            "search_params": search_params,
            "search_param_count": len(search_params),
        })

# C-CDA sections from the PDF (page 6)
ccda_sections = [
    "Allergy", "Assessment", "Encounters", "Family History",
    "Functional Status", "Cognitive Status", "Immunizations",
    "Medical Equipment", "Medications", "Lab Results", "Problems",
    "Procedures", "Reason for Visit", "Referrals", "Social History",
    "Vitals", "Care Plan", "Goal", "Health Concern", "Clinical Instructions"
]

# Export methods from the PDF
export_methods = [
    {
        "id": "fhir-api",
        "name": "FHIR APIs",
        "format": "FHIR R4 JSON",
        "type": "api",
        "scope": "USCDI / US Core clinical data",
        "resource_count": len(fhir_resources),
        "documented_detail": "Standard (g)(10) FHIR API with CapabilityStatement",
        "has_data_dictionary": False,
    },
    {
        "id": "ccda-export",
        "name": "C-CDA R2.1 Bulk or Single Export",
        "format": "C-CDA R2.1 XML",
        "type": "file_export",
        "scope": "Clinical data - 20 C-CDA sections",
        "section_count": len(ccda_sections),
        "sections": ccda_sections,
        "documented_detail": "Sections listed by name; relies on C-CDA R2.1 standard for field-level detail",
        "has_data_dictionary": False,
    },
    {
        "id": "csv-export",
        "name": "CSV Full Data Set Export",
        "format": "CSV",
        "type": "file_export",
        "scope": "Health, activity, and financial data (claimed)",
        "documented_detail": "Data dictionary URL (https://emr.ehiconnect.com/docs/) returns HTTP 404",
        "has_data_dictionary": False,
        "data_dictionary_url": "https://emr.ehiconnect.com/docs/",
        "data_dictionary_status": "HTTP 404 - Not Found",
    },
    {
        "id": "hl7-adt",
        "name": "HL7 2.x/3.x ADT",
        "format": "HL7 v2/v3",
        "type": "real_time_feed",
        "scope": "Patient demographics and payer information",
        "documented_detail": "One paragraph description; relies on HL7 standard for detail",
        "has_data_dictionary": False,
    },
    {
        "id": "hl7-siu",
        "name": "HL7 2.x SIU",
        "format": "HL7 v2",
        "type": "real_time_feed",
        "scope": "Appointment scheduling updates",
        "documented_detail": "One paragraph description",
        "has_data_dictionary": False,
    },
    {
        "id": "hl7-dft",
        "name": "HL7 2.x DFT",
        "format": "HL7 v2",
        "type": "real_time_feed",
        "scope": "Financial transactions (description appears copied from SIU - likely copy-paste error)",
        "documented_detail": "One paragraph - appears to be copy-paste of SIU description",
        "has_data_dictionary": False,
    },
    {
        "id": "json-scanned-docs",
        "name": "JSON Scanned Documents Exchange",
        "format": "JSON with BASE-64 encoded content",
        "type": "real_time_feed",
        "scope": "Scanned documents, faxes, custom reports",
        "documented_detail": "Brief description of JSON payload structure",
        "has_data_dictionary": False,
    },
    {
        "id": "edi-claims",
        "name": "EDI 837P and 835 Claims Files",
        "format": "EDI 837P / 835",
        "type": "file_feed",
        "scope": "Claims and remittance data",
        "documented_detail": "One sentence description; relies on EDI standards for detail",
        "has_data_dictionary": False,
    },
]

# Build entity inventory
# Since there's no data dictionary, we document what's described
entities = []

# FHIR resources as entities
for r in fhir_resources:
    entities.append({
        "entity_name": r["type"],
        "source": "fhir-capability-statement.json",
        "export_method": "FHIR APIs",
        "format": "FHIR R4 JSON",
        "category": "FHIR Resource",
        "fields": None,  # No field-level documentation beyond FHIR spec
        "field_count": None,
        "fields_with_descriptions": None,
        "notes": f"Standard US Core resource. Interactions: {', '.join(r['interactions'])}. Search params: {r['search_param_count']}.",
    })

# C-CDA sections as entities
for section in ccda_sections:
    entities.append({
        "entity_name": section,
        "source": "EHI_DATA_EXPort_GUIDE.pdf (page 6)",
        "export_method": "C-CDA R2.1 Export",
        "format": "C-CDA R2.1 XML",
        "category": "C-CDA Section",
        "fields": None,
        "field_count": None,
        "fields_with_descriptions": None,
        "notes": "Section name listed in PDF. No field-level documentation; relies on C-CDA R2.1 standard.",
    })

# CSV export - no field detail available
entities.append({
    "entity_name": "CSV Full Data Set (undocumented)",
    "source": "EHI_DATA_EXPort_GUIDE.pdf (page 4)",
    "export_method": "CSV Export",
    "format": "CSV",
    "category": "CSV Export",
    "fields": None,
    "field_count": None,
    "fields_with_descriptions": None,
    "notes": "Described as covering 'health, activity and financial data'. Data dictionary URL returns 404. No field-level documentation available.",
})

# Full inventory
full_inventory = {
    "product": "MDnet V10",
    "developer": "Enable Healthcare Inc.",
    "analysis_date": "2026-02-16",
    "data_dictionary_available": False,
    "data_dictionary_note": "The PDF references a CSV data dictionary at https://emr.ehiconnect.com/docs/ which returns HTTP 404. No field-level documentation exists for any export method.",
    "export_methods": export_methods,
    "entities": entities,
    "totals": {
        "fhir_resource_types": len(fhir_resources),
        "ccda_sections": len(ccda_sections),
        "total_documented_entities": len(entities),
        "entities_with_field_counts": 0,
        "entities_with_descriptions": 0,
        "total_fields_documented": 0,
    }
}

# Summary
summary = {
    "product": "MDnet V10",
    "developer": "Enable Healthcare Inc.",
    "analysis_date": "2026-02-16",
    "export_method_count": len(export_methods),
    "export_methods_summary": [
        {"name": m["name"], "format": m["format"], "scope": m["scope"], "has_data_dictionary": m["has_data_dictionary"]}
        for m in export_methods
    ],
    "fhir_resources": sorted([r["type"] for r in fhir_resources]),
    "fhir_resource_count": len(fhir_resources),
    "ccda_sections": ccda_sections,
    "ccda_section_count": len(ccda_sections),
    "csv_data_dictionary_status": "HTTP 404 - Not Found",
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "has_sample_data": False,
    "has_machine_readable_schema": True,  # FHIR CapabilityStatement
    "key_gap": "CSV data dictionary (the only export claimed to cover financial data) is inaccessible (404). No field-level documentation exists for any export method.",
}

# Write outputs
with open(os.path.join(ANALYSIS_DIR, "entity-inventory-full.json"), "w") as f:
    json.dump(full_inventory, f, indent=2)

with open(os.path.join(ANALYSIS_DIR, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== Entity Inventory Summary ===")
print(f"Export methods described: {len(export_methods)}")
print(f"FHIR resource types: {len(fhir_resources)}")
print(f"C-CDA sections: {len(ccda_sections)}")
print(f"Total documented entities: {len(entities)}")
print(f"Entities with field-level detail: 0")
print(f"Total fields documented: 0")
print(f"CSV data dictionary status: HTTP 404")
print(f"\nFHIR Resources: {', '.join(sorted(r['type'] for r in fhir_resources))}")
print(f"\nC-CDA Sections: {', '.join(ccda_sections)}")
