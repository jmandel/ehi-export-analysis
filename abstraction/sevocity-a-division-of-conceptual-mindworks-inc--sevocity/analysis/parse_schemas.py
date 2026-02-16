#!/usr/bin/env python3
"""Parse all Sevocity FHIR API YAML schema files and build entity inventory."""
import json, yaml
from pathlib import Path

BASE = Path("../downloads/fhir-api-docs")
SCHEMA_DIR = BASE / "components" / "schemas"
EXAMPLES_DIR = BASE / "examples"

with open("../downloads/openAPIDocs.yml") as f:
    main_spec = yaml.safe_load(f)

certified_resources = set()
non_certified_resources = set()
for tag in main_spec.get("tags", []):
    name = tag["name"]
    desc = tag.get("description", "")
    if name in ("System Level Operations", "Group"):
        continue
    if "*" in desc:
        certified_resources.add(name)
    else:
        non_certified_resources.add(name)

def flatten_properties(schema, prefix=""):
    fields = []
    props = schema.get("properties", {})
    for pname, pdef in props.items():
        full_name = f"{prefix}{pname}" if not prefix else f"{prefix}.{pname}"
        field = {"name": full_name, "type": pdef.get("type", "object")}
        if pdef.get("description"):
            field["description"] = pdef["description"]
        if "enum" in pdef:
            field["enum_values"] = pdef["enum"]
        if "example" in pdef:
            field["example"] = str(pdef["example"])
        fields.append(field)
        if pdef.get("type") == "object" and "properties" in pdef:
            fields.extend(flatten_properties(pdef, full_name))
        elif pdef.get("type") == "array" and "items" in pdef:
            items = pdef["items"]
            if isinstance(items, dict) and "properties" in items:
                fields.extend(flatten_properties(items, f"{full_name}[]"))
    return fields

# Search schema name -> canonical resource type
search_name_map = {
    "SEARCHALLERGYINTOLERANCE": "AllergyIntolerance",
    "SEARCHAPPOINTMENT": "Appointment",
    "SEARCHCAREPLAN": "CarePlan",
    "SEARCHCARETEAM": "CareTeam",
    "SEARCHCONDITION": "Condition",
    "SEARCHCOVERAGE": "Coverage",
    "SEARCHDEVICES": "Device",
    "SEARCHDIAGNOSTICREPORT": "DiagnosticReport",
    "SEARCHDOCUMENTREFERENCE": "DocumentReference",
    "SEARCHENCOUNTER": "Encounter",
    "SEARCHALLENDPOINTS": "Endpoint",
    "SEARCHGOALS": "Goal",
    "SEARCHIMMUNIZATION": "Immunization",
    "SEARCHMEDICATIONREQUEST": "MedicationRequest",
    "SEARCHMEDICATIONSTATEMENT": "MedicationStatement",
    "SEARCHMEDICATIONDISPENSE": "MedicationDispense",
    "SEARCHOBSERVATION": "Observation",
    "SEARCHORGANIZATION": "Organization",
    "SEARCHPATIENT": "Patient",
    "SEARCHPRACTITIONER": "Practitioner",
    "SEARCHPROCEDURE": "Procedure",
    "SEARCHRELATEDPERSON": "RelatedPerson",
    "SEARCHSERVICEREQUEST": "ServiceRequest",
    "SEARCHQUESTIONNAIRERESPONSE": "QuestionnaireResponse",
    "SEARCHQUESTIONNAIRE": "Questionnaire",
}

read_name_map = {
    "READALLERGYINTOLERANCE": "AllergyIntolerance",
    "READCAREPLAN": "CarePlan",
    "READCARETEAM": "CareTeam",
    "READCONDITION": "Condition",
    "READDEVICE": "Device",
    "READDIAGNOSTICREPORT": "DiagnosticReport",
    "READDOCUMENTREFERENCE": "DocumentReference",
    "READENCOUNTER": "Encounter",
    "READGOAL": "Goal",
    "READIMMUNIZATION": "Immunization",
    "READLOCATION": "Location",
    "READMEDICATION": "Medication",
    "READMEDICATIONREQUEST": "MedicationRequest",
    "READMEDICATIONSTATEMENT": "MedicationStatement",
    "READMEDICATIONDISPENSE": "MedicationDispense",
    "READOBSERVATION": "Observation",
    "READORGANIZATION": "Organization",
    "READPATIENT": "Patient",
    "ReadPractitioner": "Practitioner",
    "READPROCEDURE": "Procedure",
    "READRELATEDPERSON": "RelatedPerson",
    "READSERVICEREQUEST": "ServiceRequest",
    "READQUESTIONNAIRERESPONSE": "QuestionnaireResponse",
}

standalone_map = {
    "APPOINTMENT": "Appointment",
    "PROVENANCE": "Provenance",
}

# First pass: collect READ schemas (priority)
read_schemas = {}
search_schemas = {}

all_schema_files = sorted(SCHEMA_DIR.glob("*.yml")) + sorted(SCHEMA_DIR.glob("*.YML"))
for schema_file in all_schema_files:
    name = schema_file.stem
    with open(schema_file) as f:
        try:
            schema = yaml.safe_load(f)
        except:
            continue
    if not schema or not isinstance(schema, dict):
        continue

    if name in read_name_map:
        rt = read_name_map[name]
        read_schemas[rt] = schema
    elif name in search_name_map:
        rt = search_name_map[name]
        # Extract resource from Bundle entry
        entry_items = schema.get("properties", {}).get("entry", {}).get("items", {})
        resource_schema = entry_items.get("properties", {}).get("resource", {})
        if resource_schema and "properties" in resource_schema:
            search_schemas[rt] = resource_schema
    elif name in standalone_map:
        rt = standalone_map[name]
        read_schemas[rt] = schema
    # Skip METADATA, FHIR-JSON-RESOURCE

# Merge: prefer read, fallback to search
all_resource_types = sorted(set(list(read_schemas.keys()) + list(search_schemas.keys())))

entities = []
for rt in all_resource_types:
    if rt in read_schemas:
        schema = read_schemas[rt]
        source = "read"
    else:
        schema = search_schemas[rt]
        source = "search_bundle_entry"
    
    fields = flatten_properties(schema)
    is_certified = rt in certified_resources
    
    has_example = False
    candidate = rt[0].lower() + rt[1:]
    for ext in ['.yml', '.yaml']:
        if (EXAMPLES_DIR / f"{candidate}{ext}").exists():
            has_example = True
            break
    
    entities.append({
        "resource_type": rt,
        "schema_source": source,
        "certified_g10": is_certified,
        "field_count": len([f for f in fields if "." not in f["name"]]),
        "total_fields_including_nested": len(fields),
        "has_example": has_example,
        "fields": fields,
    })

# Non-FHIR
entities.append({
    "resource_type": "PatientsDemographics.csv",
    "schema_source": "non-fhir",
    "certified_g10": False,
    "field_count": 0,
    "total_fields_including_nested": 0,
    "has_example": False,
    "fields": [],
    "note": "CSV demographics file; schema not documented"
})
entities.append({
    "resource_type": "DocumentData (files)",
    "schema_source": "non-fhir",
    "certified_g10": False,
    "field_count": 0,
    "total_fields_including_nested": 0,
    "has_example": False,
    "fields": [],
    "note": "Physical document files (PDFs, JPEGs, PNGs) organized by patient ID"
})

entities.sort(key=lambda e: e["resource_type"])

fhir_entities = [e for e in entities if e["schema_source"] != "non-fhir"]

output = {
    "vendor": "Sevocity (Conceptual MindWorks, Inc.)",
    "product": "Sevocity v13.0",
    "export_format": "FHIR R4 NDJSON + Document files (PDF/JPEG/PNG) + CSV",
    "total_fhir_resource_types": len(fhir_entities),
    "total_fields_top_level": sum(e["field_count"] for e in fhir_entities),
    "total_fields_including_nested": sum(e["total_fields_including_nested"] for e in fhir_entities),
    "certified_g10_count": len([e for e in fhir_entities if e["certified_g10"]]),
    "non_certified_additions": len([e for e in fhir_entities if not e["certified_g10"]]),
    "example_files_count": len(list(EXAMPLES_DIR.glob("*.yml"))),
    "entities": entities,
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

# Summary
summary = {
    "vendor": output["vendor"],
    "product": output["product"],
    "export_format": output["export_format"],
    "total_fhir_resource_types": output["total_fhir_resource_types"],
    "total_fields_top_level": output["total_fields_top_level"],
    "total_fields_including_nested": output["total_fields_including_nested"],
    "certified_g10_count": output["certified_g10_count"],
    "non_certified_additions": output["non_certified_additions"],
    "example_files_count": output["example_files_count"],
    "non_fhir_components": ["PatientsDemographics.csv", "DocumentData (files)"],
    "entities_summary": [
        {
            "resource_type": e["resource_type"],
            "schema_source": e["schema_source"],
            "certified_g10": e.get("certified_g10", False),
            "field_count": e["field_count"],
            "total_fields_nested": e["total_fields_including_nested"],
            "has_example": e["has_example"],
            "note": e.get("note", ""),
        }
        for e in entities
    ],
    "fields_with_descriptions": sum(
        1 for e in entities for f in e["fields"] if f.get("description")
    ),
    "fields_with_types": sum(
        1 for e in entities for f in e["fields"] if f.get("type")
    ),
    "fields_with_enums": sum(
        1 for e in entities for f in e["fields"] if f.get("enum_values")
    ),
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total FHIR resource types: {output['total_fhir_resource_types']}")
print(f"  Certified (g)(10): {output['certified_g10_count']}")
print(f"  Non-certified additions: {output['non_certified_additions']}")
print(f"Total top-level fields: {output['total_fields_top_level']}")
print(f"Total fields (incl nested): {output['total_fields_including_nested']}")
print(f"Fields with descriptions: {summary['fields_with_descriptions']}")
print(f"Fields with types: {summary['fields_with_types']}")
print(f"Fields with enum values: {summary['fields_with_enums']}")
print(f"Example files: {output['example_files_count']}")
print()
for e in entities:
    if e["schema_source"] != "non-fhir":
        cert = "✓" if e["certified_g10"] else " "
        src = "R" if e["schema_source"] == "read" else "S"
        print(f"  [{cert}] {e['resource_type']:30s} {e['field_count']:3d} top / {e['total_fields_including_nested']:3d} nested  [{src}] ex={'Y' if e['has_example'] else 'N'}")
    else:
        print(f"  [ ] {e['resource_type']:30s} (non-FHIR)")
