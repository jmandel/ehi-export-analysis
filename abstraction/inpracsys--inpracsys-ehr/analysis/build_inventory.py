"""Build clean entity inventory from parsed FHIR docs, mapping headings to 
proper FHIR resource names and computing summary statistics."""

import json

with open("analysis/entity-inventory-full.json") as f:
    raw = json.load(f)

# Map verbose headings to clean resource names and FHIR types
HEADING_MAP = {
    "Overview": None,  # skip - this is the search param table
    "Searching for a patient": None,  # skip - search params
    "Retrieving a patient": "Patient",
    "Smoking status": "Observation (Smoking Status)",
    "Detailed information about conditions, problems, or diagnoses": "Condition",
    "Record of medication being taken by a patient": "MedicationStatement",
    "Allergy or intolerance (generally: risk of adverse reaction to a substance)": "AllergyIntolerance",
    "Lab Orders": "DiagnosticReport (Lab Orders)",
    "Diagnostic Order:": "Observation (Lab Results)",
    "Measurements and simple assertions": "Observation (Vital Signs)",
    "Procedure: an action that is being or was performed on a patient": "Procedure",
    "Care team for patient": "CareTeam",
    "Immunization event information": "Immunization",
    "An instance of a manufactured device that is used in the provision of healthcare": "Device",
    "Healthcare plan for patient or group": "CarePlan",
    "Intended objective(s) for a patient, group or organization": "Goal",
    "Detailed information about health concerns": "Condition (Health Concerns)",
}

# Map to USCDI data classes
USCDI_MAP = {
    "Patient": "Patient Demographics",
    "Observation (Smoking Status)": "Health Status Assessments",
    "Condition": "Problems",
    "MedicationStatement": "Medications",
    "AllergyIntolerance": "Allergies & Intolerances",
    "DiagnosticReport (Lab Orders)": "Laboratory",
    "Observation (Lab Results)": "Laboratory",
    "Observation (Vital Signs)": "Vital Signs",
    "Procedure": "Procedures",
    "CareTeam": "Care Team Members",
    "Immunization": "Immunizations",
    "Device": "Medical Devices",
    "CarePlan": "Assessment & Plan of Treatment",
    "Goal": "Goals & Preferences",
    "Condition (Health Concerns)": "Health Status Assessments",
}

entities = []
total_fields = 0
fields_with_desc = 0
fields_with_type = 0

for heading, res_data in raw.items():
    clean_name = HEADING_MAP.get(heading)
    if clean_name is None:
        continue  # skip non-resource tables
    
    fields = []
    for f in res_data["fields"]:
        field = {
            "name": f.get("name", ""),
            "type": f.get("type", ""),
            "description": f.get("description", ""),
            "cardinality": f.get("cardinality", f.get("required?", f.get("required", ""))),
        }
        # Add any extra columns
        for k, v in f.items():
            if k not in ("name", "type", "description", "cardinality", "required?", "required"):
                field[k] = v
        
        fields.append(field)
        total_fields += 1
        if field["description"].strip():
            fields_with_desc += 1
        if field["type"].strip():
            fields_with_type += 1
    
    entity = {
        "entity_name": clean_name,
        "original_heading": heading,
        "uscdi_data_class": USCDI_MAP.get(clean_name, ""),
        "field_count": len(fields),
        "fields": fields,
    }
    entities.append(entity)

# Save full inventory
inventory = {
    "product": "InPracSys EHR",
    "version": "9.0",
    "source": "downloads/fhir-api-documentation-page.html",
    "format": "FHIR R4 (non-standard serialization)",
    "entity_count": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_type,
    "entities": entities,
}

with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Generate summary
summary = {
    "product": inventory["product"],
    "version": inventory["version"],
    "source": inventory["source"],
    "format": inventory["format"],
    "total_entities": inventory["entity_count"],
    "total_fields": inventory["total_fields"],
    "fields_with_descriptions": inventory["fields_with_descriptions"],
    "fields_with_types": inventory["fields_with_types"],
    "pct_fields_with_descriptions": round(100 * fields_with_desc / total_fields, 1) if total_fields > 0 else 0,
    "pct_fields_with_types": round(100 * fields_with_type / total_fields, 1) if total_fields > 0 else 0,
    "entities_by_uscdi_class": {},
    "entity_summary": [],
}

for e in entities:
    uscdi = e["uscdi_data_class"] or "Uncategorized"
    if uscdi not in summary["entities_by_uscdi_class"]:
        summary["entities_by_uscdi_class"][uscdi] = {"count": 0, "total_fields": 0}
    summary["entities_by_uscdi_class"][uscdi]["count"] += 1
    summary["entities_by_uscdi_class"][uscdi]["total_fields"] += e["field_count"]
    
    desc_count = sum(1 for f in e["fields"] if f.get("description", "").strip())
    summary["entity_summary"].append({
        "name": e["entity_name"],
        "field_count": e["field_count"],
        "fields_with_descriptions": desc_count,
        "uscdi_class": e["uscdi_data_class"],
    })

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Entities: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['pct_fields_with_descriptions']}%)")
print(f"Fields with types: {fields_with_type} ({summary['pct_fields_with_types']}%)")
print()
print("Entity breakdown:")
for e in summary["entity_summary"]:
    print(f"  {e['name']:40s}  {e['field_count']:3d} fields  ({e['fields_with_descriptions']} described)  [{e['uscdi_class']}]")
print()
print("By USCDI class:")
for cls, info in summary["entities_by_uscdi_class"].items():
    print(f"  {cls:35s}  {info['count']} entities, {info['total_fields']} fields")
