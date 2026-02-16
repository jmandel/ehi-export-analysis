#!/usr/bin/env python3
"""
Parse all EHI export artifacts for myhELO and produce a full entity inventory.

Inputs:
  - downloads/fhir-well-known.json: FHIR API spec with example responses
  - downloads/fhir-metadata.json: FHIR CapabilityStatement
  - downloads/enrichment/ehi-export-data-dictionary.json: Extracted data dictionary
  - downloads/main-page.html: Rendered EHI export main page
  - downloads/api-docs.html: API documentation page (SPA, partially rendered)

Outputs:
  - full-entity-inventory.json: Complete machine-readable extraction
  - summary-stats.json: Aggregated statistics
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/myhelo-inc--myhelo/downloads")
OUTPUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/myhelo-inc--myhelo/analysis")

def parse_well_known():
    """Parse the FHIR well-known JSON for example response fields."""
    with open(DOWNLOADS / "fhir-well-known.json") as f:
        data = json.load(f)
    
    resources = {}
    for name, spec in data.items():
        resource = {
            "displayName": name,
            "endpoints": {},
            "exampleFields": [],
            "searchParams": [],
            "hasExample": False
        }
        
        if "read" in spec:
            resource["endpoints"]["read"] = {
                "method": spec["read"].get("method", "GET"),
                "url": spec["read"].get("url", ""),
                "baseUrl": spec["read"].get("base_url", "")
            }
            response = spec["read"].get("response", {})
            if response:
                resource["hasExample"] = True
                resource["exampleFields"] = extract_fields_from_example(response, name)
        
        if "search" in spec:
            resource["endpoints"]["search"] = {
                "method": spec["search"].get("method", "GET"),
                "url": spec["search"].get("url", ""),
                "baseUrl": spec["search"].get("base_url", "")
            }
            params = spec["search"].get("parameters", {})
            for pname, pinfo in params.items():
                resource["searchParams"].append({
                    "name": pname,
                    "type": pinfo.get("type", ""),
                    "required": pinfo.get("required", False)
                })
        
        if "export" in spec:
            resource["endpoints"]["export"] = {
                "method": spec["export"].get("method", "GET"),
                "url": spec["export"].get("url", "")
            }
        
        resources[name] = resource
    
    return resources

def extract_fields_from_example(obj, prefix="", depth=0):
    """Recursively extract field paths from a FHIR example response."""
    fields = []
    if not isinstance(obj, dict) or depth > 5:
        return fields
    
    for key, value in obj.items():
        if key == "resourceType":
            continue
        
        field = {
            "name": key,
            "path": f"{prefix}.{key}" if prefix else key,
            "exampleValue": None,
            "type_inferred": infer_type(value),
            "hasChildren": False
        }
        
        if isinstance(value, str):
            field["exampleValue"] = value
        elif isinstance(value, (int, float, bool)):
            field["exampleValue"] = value
        elif isinstance(value, dict):
            field["hasChildren"] = True
            if "coding" in value:
                # CodeableConcept
                field["type_inferred"] = "CodeableConcept"
                codings = value.get("coding", [])
                if codings:
                    field["exampleValue"] = f"{codings[0].get('display', codings[0].get('code', ''))}"
                    field["codeSystem"] = codings[0].get("system", "")
            elif "reference" in value:
                # Reference
                field["type_inferred"] = "Reference"
                field["exampleValue"] = value.get("reference", "")
        elif isinstance(value, list):
            field["hasChildren"] = True
            field["type_inferred"] = f"Array[{len(value)} items]"
        
        fields.append(field)
    
    return fields

def infer_type(value):
    if isinstance(value, str):
        return "string"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "decimal"
    elif isinstance(value, dict):
        return "object"
    elif isinstance(value, list):
        return "array"
    return "unknown"

def parse_capability_statement():
    """Parse the FHIR CapabilityStatement for supported resources."""
    with open(DOWNLOADS / "fhir-metadata.json") as f:
        data = json.load(f)
    
    meta = {
        "fhirVersion": data.get("fhirVersion"),
        "software": data.get("software", {}),
        "format": data.get("format", []),
        "date": data.get("date"),
        "status": data.get("status")
    }
    
    resources = []
    rest = data.get("rest", [])
    if rest:
        for res in rest[0].get("resource", []):
            resource = {
                "type": res["type"],
                "interactions": [i["code"] for i in res.get("interaction", [])],
                "searchParams": [
                    {"name": p["name"], "type": p["type"]}
                    for p in res.get("searchParam", [])
                ],
                "operations": [
                    {"name": op["name"], "definition": op.get("definition", "")}
                    for op in res.get("operation", [])
                ]
            }
            resources.append(resource)
    
    security = {}
    if rest:
        sec = rest[0].get("security", {})
        if sec:
            extensions = sec.get("extension", [])
            for ext in extensions:
                if "oauth-uris" in ext.get("url", ""):
                    for sub_ext in ext.get("extension", []):
                        security[sub_ext["url"]] = sub_ext.get("valueUri", "")
    
    return {"metadata": meta, "resources": resources, "security": security}

def parse_data_dictionary():
    """Parse the enrichment data dictionary JSON."""
    dd_path = DOWNLOADS / "enrichment" / "ehi-export-data-dictionary.json"
    with open(dd_path) as f:
        data = json.load(f)
    return data

def parse_main_page():
    """Parse the rendered main page HTML for dataset listing."""
    with open(DOWNLOADS / "main-page.html") as f:
        html = f.read()
    
    # Extract dataset names from table
    datasets = re.findall(r'<td>([^<]+)</td><td><a href="[^"]*">([^<]+)</a></td>', html)
    
    # Extract intro text
    intro_match = re.search(r'<h1>Introduction</h1><p>(.*?)</p>', html)
    intro = intro_match.group(1) if intro_match else ""
    
    return {
        "datasets": [{"displayName": d[0], "resourceType": d[1]} for d in datasets],
        "introText": intro,
        "datasetCount": len(datasets)
    }

def build_full_inventory():
    """Build the complete entity inventory from all sources."""
    well_known = parse_well_known()
    cap_stmt = parse_capability_statement()
    data_dict = parse_data_dictionary()
    main_page = parse_main_page()
    
    # Map resource type names
    resource_type_map = {}
    for r in data_dict.get("resources", []):
        resource_type_map[r["resourceType"]] = r
    
    # Map well-known names to resource types
    wk_name_to_type = {
        "Allergy Intolerance": "AllergyIntolerance",
        "Care Plan": "CarePlan",
        "Care Team": "CareTeam",
        "Condition": "Condition",
        "Device": "Device",
        "Diagnostic Report": "DiagnosticReport",
        "Document Reference": "DocumentReference",
        "Encounter": "Encounter",
        "Goal": "Goal",
        "Group": "Group",
        "Immunization": "Immunization",
        "Location": "Location",
        "Medication Request": "MedicationRequest",
        "Observation": "Observation",
        "Organization": "Organization",
        "Patient": "Patient",
        "Practitioner": "Practitioner",
        "Procedure": "Procedure",
        "Provenance": "Provenance"
    }
    
    # Build unified inventory
    entities = []
    all_resource_types = set()
    
    # Collect from all sources
    for r in cap_stmt["resources"]:
        all_resource_types.add(r["type"])
    for r in data_dict.get("resources", []):
        all_resource_types.add(r["resourceType"])
    for name in well_known:
        rtype = wk_name_to_type.get(name, name)
        all_resource_types.add(rtype)
    
    # Determine which are in the EHI export (listed on main page)
    ehi_export_types = set(d["resourceType"] for d in main_page["datasets"])
    
    for rtype in sorted(all_resource_types):
        entity = {
            "resourceType": rtype,
            "inEhiExport": rtype in ehi_export_types,
            "inCapabilityStatement": False,
            "inWellKnown": False,
            "fields": [],
            "fieldCount": 0,
            "fieldsWithDescriptions": 0,
            "fieldsWithTypes": 0,
            "fieldsWithExamples": 0,
            "searchParams": [],
            "interactions": [],
            "operations": [],
            "category": categorize_resource(rtype)
        }
        
        # From CapabilityStatement
        for r in cap_stmt["resources"]:
            if r["type"] == rtype:
                entity["inCapabilityStatement"] = True
                entity["interactions"] = r["interactions"]
                entity["operations"] = r["operations"]
                entity["searchParams"] = r["searchParams"]
                break
        
        # From well-known (examples)
        wk_name = None
        for name, mapped_type in wk_name_to_type.items():
            if mapped_type == rtype:
                wk_name = name
                break
        
        if wk_name and wk_name in well_known:
            wk = well_known[wk_name]
            entity["inWellKnown"] = True
            entity["hasExample"] = wk["hasExample"]
            
            # Build fields from example + data dictionary
            dd_fields = {}
            if rtype in resource_type_map:
                for f in resource_type_map[rtype]["fields"]:
                    short_name = f["name"].split(".")[-1] if "." in f["name"] else f["name"]
                    dd_fields[short_name] = f
            
            # Merge example fields with DD fields
            seen_fields = set()
            for ef in wk["exampleFields"]:
                field = {
                    "name": ef["name"],
                    "type": ef["type_inferred"],
                    "description": "",
                    "cardinality": "",
                    "isModifier": False,
                    "isSummary": False,
                    "isUSCDI": False,
                    "exampleValue": ef.get("exampleValue"),
                    "codeSystem": ef.get("codeSystem", ""),
                    "source": "example"
                }
                
                # Enrich from DD
                if ef["name"] in dd_fields:
                    dd = dd_fields[ef["name"]]
                    field["type"] = dd.get("type", field["type"])
                    field["description"] = dd.get("description", "")
                    field["cardinality"] = dd.get("cardinality", "")
                    field["isModifier"] = dd.get("isModifier", False)
                    field["isSummary"] = dd.get("isSummary", False)
                    field["isUSCDI"] = dd.get("isUSCDI", False)
                    field["source"] = "example+dataDictionary"
                
                entity["fields"].append(field)
                seen_fields.add(ef["name"])
            
            # Add DD fields not in example
            for fname, dd in dd_fields.items():
                if fname not in seen_fields:
                    entity["fields"].append({
                        "name": fname,
                        "type": dd.get("type", ""),
                        "description": dd.get("description", ""),
                        "cardinality": dd.get("cardinality", ""),
                        "isModifier": dd.get("isModifier", False),
                        "isSummary": dd.get("isSummary", False),
                        "isUSCDI": dd.get("isUSCDI", False),
                        "exampleValue": None,
                        "codeSystem": "",
                        "source": "dataDictionary"
                    })
            
            if not entity.get("searchParams"):
                entity["searchParams"] = [
                    {"name": p["name"], "type": p["type"]}
                    for p in wk.get("searchParams", [])
                ]
        
        entity["fieldCount"] = len(entity["fields"])
        entity["fieldsWithDescriptions"] = sum(1 for f in entity["fields"] if f.get("description", "").strip())
        entity["fieldsWithTypes"] = sum(1 for f in entity["fields"] if f.get("type", "").strip())
        entity["fieldsWithExamples"] = sum(1 for f in entity["fields"] if f.get("exampleValue") is not None)
        
        entities.append(entity)
    
    # Summary stats
    total_fields = sum(e["fieldCount"] for e in entities)
    total_with_desc = sum(e["fieldsWithDescriptions"] for e in entities)
    total_with_types = sum(e["fieldsWithTypes"] for e in entities)
    total_with_examples = sum(e["fieldsWithExamples"] for e in entities)
    total_uscdi = sum(
        sum(1 for f in e["fields"] if f.get("isUSCDI"))
        for e in entities
    )
    
    ehi_entities = [e for e in entities if e["inEhiExport"]]
    non_ehi_entities = [e for e in entities if not e["inEhiExport"]]
    
    # Category breakdown
    categories = {}
    for e in entities:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = {"entityCount": 0, "fieldCount": 0}
        categories[cat]["entityCount"] += 1
        categories[cat]["fieldCount"] += e["fieldCount"]
    
    inventory = {
        "vendor": "myhELO, Inc.",
        "product": "myhELO",
        "exportFormat": "FHIR R4 JSON",
        "fhirVersion": "4.0.1",
        "softwareVersion": cap_stmt["metadata"]["software"].get("version", ""),
        "collectionDate": "2026-02-15",
        "sources": {
            "capabilityStatement": str(DOWNLOADS / "fhir-metadata.json"),
            "wellKnown": str(DOWNLOADS / "fhir-well-known.json"),
            "dataDictionary": str(DOWNLOADS / "enrichment" / "ehi-export-data-dictionary.json"),
            "mainPage": str(DOWNLOADS / "main-page.html")
        },
        "summary": {
            "totalEntities": len(entities),
            "ehiExportEntities": len(ehi_entities),
            "additionalEntities": len(non_ehi_entities),
            "totalFields": total_fields,
            "fieldsWithDescriptions": total_with_desc,
            "fieldsWithTypes": total_with_types,
            "fieldsWithExamples": total_with_examples,
            "fieldsMarkedUSCDI": total_uscdi,
            "descriptionRate": f"{total_with_desc}/{total_fields} ({(total_with_desc/total_fields*100 if total_fields else 0):.1f}%)",
            "categoryBreakdown": categories
        },
        "security": cap_stmt["security"],
        "mainPageIntro": main_page["introText"],
        "entities": entities
    }
    
    return inventory

def categorize_resource(rtype):
    """Categorize FHIR resource types into clinical domains."""
    categories = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Clinical - Allergies",
        "Condition": "Clinical - Problems",
        "MedicationRequest": "Clinical - Medications",
        "Immunization": "Clinical - Immunizations",
        "Observation": "Clinical - Observations",
        "DiagnosticReport": "Clinical - Diagnostics",
        "DocumentReference": "Clinical - Documents",
        "Procedure": "Clinical - Procedures",
        "Encounter": "Clinical - Encounters",
        "CarePlan": "Clinical - Care Plans",
        "CareTeam": "Clinical - Care Teams",
        "Goal": "Clinical - Goals",
        "Device": "Clinical - Devices",
        "Provenance": "Infrastructure",
        "Practitioner": "Infrastructure",
        "Organization": "Infrastructure",
        "Location": "Infrastructure",
        "Group": "Infrastructure"
    }
    return categories.get(rtype, "Other")

def main():
    inventory = build_full_inventory()
    
    # Write full inventory
    with open(OUTPUT / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2, default=str)
    print(f"Written: full-entity-inventory.json")
    
    # Write summary stats
    summary = inventory["summary"]
    with open(OUTPUT / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Written: summary-stats.json")
    
    # Print summary to stdout
    print(f"\n=== myhELO EHI Export Inventory ===")
    print(f"Total entities: {summary['totalEntities']}")
    print(f"EHI export entities: {summary['ehiExportEntities']}")
    print(f"Additional entities: {summary['additionalEntities']}")
    print(f"Total fields: {summary['totalFields']}")
    print(f"Fields with descriptions: {summary['descriptionRate']}")
    print(f"Fields with types: {summary['fieldsWithTypes']}")
    print(f"Fields with examples: {summary['fieldsWithExamples']}")
    print(f"Fields marked USCDI: {summary['fieldsMarkedUSCDI']}")
    print(f"\nCategory breakdown:")
    for cat, info in sorted(summary['categoryBreakdown'].items()):
        print(f"  {cat}: {info['entityCount']} entities, {info['fieldCount']} fields")
    
    print(f"\nEntity details:")
    for e in inventory["entities"]:
        ehi = "✅" if e["inEhiExport"] else "❌"
        ex = "📋" if e.get("hasExample") else "  "
        print(f"  {ehi} {ex} {e['resourceType']}: {e['fieldCount']} fields, "
              f"{e['fieldsWithDescriptions']} described, "
              f"{e['fieldsWithExamples']} with examples [{e['category']}]")

if __name__ == "__main__":
    main()
