#!/usr/bin/env python3
"""Parse OneTouch EMR FHIR API PDF to extract resource attribute tables."""
import re, json, sys

with open("pdf-text.txt", "r") as f:
    text = f.read()

resources = [
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "MedicationRequest", "Observation",
    "Organization", "Patient", "Practitioner", "Procedure", "Provenance"
]

name_variants = {"DiagnosticReport": r"Diagnostic\s*Report"}

entities = []

for i, res in enumerate(resources):
    pattern_name = name_variants.get(res, res)
    fhir_res_match = re.search(rf'FHIR Resource:\s*{pattern_name}\b', text)
    if not fhir_res_match:
        print(f"WARNING: Could not find section for {res}", file=sys.stderr)
        entities.append({"name": res, "fields": [], "field_count": 0})
        continue
    
    start = fhir_res_match.start()
    attr_match = re.search(r'The following attributes are supported:', text[start:start+2000])
    if not attr_match:
        entities.append({"name": res, "fields": [], "field_count": 0})
        continue
    
    attr_start = start + attr_match.end()
    
    end_offset = 3000
    for pat in [r'\nFHIR Operations\n', r'\n\nRead\n', r'\nRead\n\n', r'\x0cRead\n']:
        m = re.search(pat, text[attr_start:attr_start+3000])
        if m:
            end_offset = min(end_offset, m.start())
    
    attr_section = text[attr_start:attr_start + end_offset]
    attr_section = re.sub(r'^\s*Name\s+Comments\s*$', '', attr_section, flags=re.MULTILINE)
    
    fields = []
    current_field = None
    current_comment = None
    
    for line in attr_section.strip().split('\n'):
        stripped = line.strip()
        if not stripped:
            if current_field:
                fields.append({"name": current_field, "description": current_comment.strip() if current_comment else ""})
                current_field = None
                current_comment = None
            continue
        
        # Match field name with 2+ spaces before description
        field_match = re.match(r'^([\w][\w.\-]*(?:\s+extension)?(?:\[x\])?)\s{2,}(.+)$', stripped)
        # Also match dotted field names with just 1 space (PDF layout artifact)
        if not field_match:
            field_match = re.match(r'^([\w]+\.[\w.]+)\s+(.+)$', stripped)
        
        if field_match:
            if current_field:
                fields.append({"name": current_field, "description": current_comment.strip() if current_comment else ""})
            current_field = field_match.group(1)
            current_comment = field_match.group(2)
        elif current_field and stripped:
            current_comment = (current_comment or "") + " " + stripped
    
    if current_field:
        fields.append({"name": current_field, "description": current_comment.strip() if current_comment else ""})
    
    entities.append({
        "name": res,
        "us_core_profile": True,
        "field_count": len(fields),
        "fields": fields
    })

output = {
    "source": "OneTouch EMR FHIR Restful API Documentation v3 (PDF, 159 pages)",
    "format": "FHIR R4 NDJSON (US Core STU3 Release 3.1.1)",
    "export_mechanism": "UI-based single patient export via Administration > General > Single Patient Export; bulk via support request",
    "export_delivery": "ZIP file delivered via internal Messaging system",
    "entity_count": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities": entities
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(output, f, indent=2)

fields_with_desc = sum(1 for e in entities for f in e["fields"] if f.get("description"))
summary = {
    "source": output["source"],
    "format": output["format"],
    "entity_count": output["entity_count"],
    "total_fields": output["total_fields"],
    "fields_with_descriptions": fields_with_desc,
    "pct_with_descriptions": round(100 * fields_with_desc / output["total_fields"], 1) if output["total_fields"] > 0 else 0,
    "entities_summary": [{"name": e["name"], "field_count": e["field_count"]} for e in entities]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Parsed {len(entities)} entities with {output['total_fields']} total fields")
print(f"Fields with descriptions: {fields_with_desc} ({summary['pct_with_descriptions']}%)")
for e in entities:
    fl = ", ".join(f["name"] for f in e["fields"])
    print(f"  {e['name']}: {e['field_count']} fields — {fl}")
