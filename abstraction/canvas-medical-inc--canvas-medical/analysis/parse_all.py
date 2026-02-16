#!/usr/bin/env python3
"""
Parse Canvas Medical EHI export artifacts into a complete entity inventory.

Sources:
1. EHI export page (downloads/ehi-export.html) - lists 29 FHIR resources in export
2. FHIR API pages (downloads/api-pages/*.html) - field-level documentation for each resource
3. SDK data model pages (downloads/sdk-data-pages/data-*.html) - internal data model

We parse from the enrichment JSONs (which were extracted from raw HTML sources)
but verify structure independently.
"""

import json
import os
from pathlib import Path
from html.parser import HTMLParser

BASE = Path(__file__).parent.parent

# ---- Parse EHI export page to get the list of resources in the export ----
class EHIPageParser(HTMLParser):
    """Extract the list of FHIR resources from the EHI export page."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_td = False
        self.resources = []
        self.current_text = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        if tag == 'td' and self.in_table:
            self.in_td = True
            self.current_text = ""
    
    def handle_endtag(self, tag):
        if tag == 'td' and self.in_td:
            self.in_td = False
            text = self.current_text.strip()
            if text and text != "Resource":
                self.resources.append(text)
        if tag == 'table':
            self.in_table = False
    
    def handle_data(self, data):
        if self.in_td:
            self.current_text += data

with open(BASE / "downloads/ehi-export.html") as f:
    parser = EHIPageParser()
    parser.feed(f.read())
    ehi_resources = parser.resources

print(f"EHI Export lists {len(ehi_resources)} resources: {ehi_resources}")

# ---- Load enrichment data ----
with open(BASE / "downloads/enrichment/fhir-api-resources.json") as f:
    fhir_data = json.load(f)

with open(BASE / "downloads/enrichment/sdk-data-models.json") as f:
    sdk_data = json.load(f)

# ---- Build entity inventory from FHIR API (what's in the export) ----
fhir_resources = {}
for res in fhir_data["resources"]:
    name = res["name"]
    # Collect all unique fields across all operations (read/search give us what's returned)
    all_fields = {}
    read_fields = {}
    for op in res.get("operations", []):
        method = op.get("method", "")
        path = op.get("path", "")
        # Focus on GET (read/search) operations as these define what's exported
        is_read = method == "GET"
        for attr in op.get("attributes", []):
            fname = attr["name"]
            field_info = {
                "name": fname,
                "type": attr.get("type", ""),
                "description": attr.get("description", ""),
                "required": attr.get("required", False),
            }
            if attr.get("valueOptions"):
                field_info["valueOptions"] = [v for v in attr["valueOptions"] if v.strip()]
            all_fields[fname] = field_info
            if is_read:
                read_fields[fname] = field_info
    
    # Use read fields if available, otherwise all fields
    fields = read_fields if read_fields else all_fields
    fhir_resources[name] = {
        "name": name,
        "source": "FHIR API",
        "sourceUrl": res.get("sourceUrl", ""),
        "lastUpdated": res.get("lastUpdated", ""),
        "description": res.get("description", ""),
        "in_ehi_export": name in ehi_resources,
        "field_count": len(fields),
        "fields": list(fields.values()),
        "endpoints": res.get("endpoints", []),
    }

# ---- Build entity inventory from SDK data models ----
sdk_models = {}
sdk_enums = {}
for page in sdk_data.get("dataPages", []):
    page_name = page["pageName"]
    for model in page.get("models", []):
        model_name = model["name"]
        fields = []
        for f in model.get("fields", []):
            fields.append({
                "name": f["name"],
                "type": f.get("type", ""),
                "description": "",  # SDK pages don't have descriptions in the enrichment
            })
        sdk_models[model_name] = {
            "name": model_name,
            "page": page_name,
            "source": "SDK Data Model",
            "sourceUrl": page.get("sourceUrl", ""),
            "lastUpdated": page.get("lastUpdated", ""),
            "introduction": page.get("introduction", ""),
            "field_count": len(fields),
            "fields": fields,
        }
    for enum in page.get("enums", []):
        enum_name = enum["name"]
        sdk_enums[enum_name] = {
            "name": enum_name,
            "page": page_name,
            "values": enum.get("values", []),
        }

# ---- Combine into full inventory ----
# The EHI export uses FHIR resources, so the primary inventory is FHIR.
# SDK models show what Canvas stores internally (for coverage comparison).

entities = []
for name in ehi_resources:
    if name in fhir_resources:
        entry = fhir_resources[name].copy()
        entry["in_ehi_export"] = True
        entities.append(entry)
    else:
        entities.append({
            "name": name,
            "source": "EHI Export Page",
            "in_ehi_export": True,
            "field_count": 0,
            "fields": [],
            "description": f"Listed in EHI export but no FHIR API page found",
        })

# Also include FHIR resources NOT in the EHI export for comparison
for name, res in fhir_resources.items():
    if name not in ehi_resources:
        entry = res.copy()
        entry["in_ehi_export"] = False
        entities.append(entry)

# ---- Compute statistics ----
total_entities = len([e for e in entities if e["in_ehi_export"]])
total_fields = sum(e["field_count"] for e in entities if e["in_ehi_export"])
fields_with_desc = sum(
    1 for e in entities if e["in_ehi_export"]
    for f in e["fields"]
    if f.get("description", "").strip()
)

# ---- Category mapping ----
category_map = {
    "AllergyIntolerance": "Clinical - Allergies",
    "Appointment": "Administrative - Scheduling",
    "CarePlan": "Clinical - Care Plans",
    "CareTeam": "Clinical - Care Teams",
    "Claim": "Financial - Billing",
    "Communication": "Communication",
    "Condition": "Clinical - Problems",
    "Consent": "Administrative - Consents",
    "Coverage": "Financial - Insurance",
    "CoverageEligibilityResponse": "Financial - Insurance",
    "Device": "Clinical - Devices",
    "DiagnosticReport": "Clinical - Diagnostics",
    "DocumentReference": "Clinical - Documents",
    "Encounter": "Clinical - Encounters",
    "Goal": "Clinical - Goals",
    "Immunization": "Clinical - Immunizations",
    "Media": "Clinical - Documents",
    "MedicationDispense": "Clinical - Medications",
    "MedicationRequest": "Clinical - Medications",
    "MedicationStatement": "Clinical - Medications",
    "Observation": "Clinical - Observations/Vitals/Labs",
    "Patient": "Demographics",
    "Procedure": "Clinical - Procedures",
    "Provenance": "Administrative - Provenance",
    "QuestionnaireResponse": "Clinical - Questionnaires",
    "RelatedPerson": "Demographics",
    "ServiceRequest": "Clinical - Orders/Referrals",
    "Specimen": "Clinical - Labs",
    "Task": "Administrative - Tasks",
}

for e in entities:
    e["category"] = category_map.get(e["name"], "Other")

# ---- Save full inventory ----
inventory = {
    "product": "Canvas Medical",
    "export_format": "FHIR R4 NDJSON (Bulk Data Access)",
    "ehi_resources_count": total_entities,
    "total_fhir_api_resources": len(fhir_resources),
    "total_sdk_models": len(sdk_models),
    "total_sdk_enums": len(sdk_enums),
    "total_fields_in_export": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "entities": entities,
    "sdk_models_summary": {
        name: {
            "name": m["name"],
            "page": m["page"],
            "field_count": m["field_count"],
            "introduction": m["introduction"],
        }
        for name, m in sdk_models.items()
    },
    "sdk_enums_summary": {
        name: {"name": e["name"], "value_count": len(e["values"])}
        for name, e in sdk_enums.items()
    },
}

out_path = Path(__file__).parent / "entity-inventory-full.json"
with open(out_path, "w") as f:
    json.dump(inventory, f, indent=2)
print(f"\nWrote {out_path}")

# ---- Summary ----
summary = {
    "ehi_export_resources": total_entities,
    "total_fields_in_export": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "description_percentage": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "fhir_api_resources_total": len(fhir_resources),
    "fhir_resources_not_in_export": [
        name for name, r in fhir_resources.items() if not r.get("in_ehi_export", name in ehi_resources)
    ],
    "sdk_models_total": len(sdk_models),
    "sdk_enums_total": len(sdk_enums),
    "sdk_total_fields": sum(m["field_count"] for m in sdk_models.values()),
    "categories": {},
}

# Category breakdown
from collections import defaultdict
cat_stats = defaultdict(lambda: {"entities": 0, "fields": 0})
for e in entities:
    if e["in_ehi_export"]:
        cat = e["category"]
        cat_stats[cat]["entities"] += 1
        cat_stats[cat]["fields"] += e["field_count"]
summary["categories"] = dict(cat_stats)

# Per-entity summary
summary["entities"] = [
    {
        "name": e["name"],
        "category": e["category"],
        "field_count": e["field_count"],
        "fields_with_desc": sum(1 for f in e["fields"] if f.get("description", "").strip()),
        "in_ehi_export": e["in_ehi_export"],
    }
    for e in entities
]

sum_path = Path(__file__).parent / "entity-inventory-summary.json"
with open(sum_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {sum_path}")

# ---- Print summary ----
print(f"\n=== EHI Export Summary ===")
print(f"Resources in EHI export: {total_entities}")
print(f"Total fields (FHIR API docs): {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['description_percentage']}%)")
print(f"FHIR API resources total: {len(fhir_resources)}")
print(f"SDK internal models: {len(sdk_models)}")
print(f"SDK total fields: {summary['sdk_total_fields']}")
print(f"SDK enums: {len(sdk_enums)}")

print(f"\n=== Category Breakdown (EHI Export) ===")
for cat, stats in sorted(cat_stats.items()):
    print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")

print(f"\n=== FHIR Resources NOT in EHI Export ===")
not_in_export = [name for name in fhir_resources if name not in ehi_resources]
for name in not_in_export:
    print(f"  {name}")

print(f"\n=== SDK Models not mapped to any FHIR resource ===")
fhir_names_lower = {n.lower() for n in fhir_resources}
for name in sorted(sdk_models):
    if name.lower() not in fhir_names_lower:
        print(f"  {name} ({sdk_models[name]['field_count']} fields)")
