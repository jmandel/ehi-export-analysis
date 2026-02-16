#!/usr/bin/env python3
"""
Parses OdataMetadata.xml (EDMX format) into entity-inventory-full.json and
entity-inventory-summary.json. Extracts all entity types, properties, navigation
properties, associations, and entity sets from Cyfluent's OData schema.

Usage: python parse-odata-schema.py
Input:  ../downloads/OdataMetadata.xml
Output: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
INPUT_PATH = SCRIPT_DIR / ".." / "downloads" / "OdataMetadata.xml"
FULL_OUTPUT = SCRIPT_DIR / "entity-inventory-full.json"
SUMMARY_OUTPUT = SCRIPT_DIR / "entity-inventory-summary.json"

# Parse the XML
tree = ET.parse(INPUT_PATH)
root = tree.getroot()

# Namespace handling for EDMX
NS = {
    "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
    "edm": "http://schemas.microsoft.com/ado/2009/11/edm",
}


def categorize_entity(name: str) -> str:
    """Classify entity types into EHI-relevant categories."""
    n = name.lower()
    # Patient-specific data
    if n.startswith("patient"):
        return "patient"
    if n.startswith("encounter"):
        return "encounter"
    if n.startswith("actionitem"):
        return "orders-results"
    if n.startswith("actionableitem"):
        return "orders-results"
    if n.startswith("code") or n.startswith("codeset"):
        return "code-sets"
    if n.startswith("facility"):
        return "facility-config"
    if n.startswith("application"):
        # Some application entities are patient-relevant (ApplicationFile, etc.)
        return "application"
    if n.startswith("report"):
        return "reporting"
    if n.startswith("scan"):
        return "scanning"
    if n.startswith("ddo"):
        return "custom-forms"
    if n.startswith("hpi"):
        return "clinical-templates"
    if n.startswith("geo"):
        return "geography"
    if n.startswith("eligibility"):
        return "eligibility"
    if n.startswith("secure"):
        return "messaging"
    if n.startswith("human"):
        return "human-resources"
    if n.startswith("location"):
        return "location"
    if n.startswith("gender"):
        return "code-sets"
    if n.startswith("smokingstatu"):
        return "code-sets"
    if n.startswith("insurance"):
        return "insurance"
    if n.startswith("prefix") or n.startswith("suffix"):
        return "code-sets"
    return "other"


def ehi_relevance(name: str, category: str) -> str:
    """Assess whether this entity is EHI (patient record data) vs system/config."""
    n = name.lower()
    if category in ("patient", "encounter", "orders-results", "scanning", "eligibility", "messaging", "insurance"):
        return "patient-record"
    if category == "custom-forms":
        return "patient-record"
    if category in ("code-sets",):
        return "reference-data"
    if category in ("facility-config", "geography", "human-resources", "location"):
        return "system-config"
    if category == "reporting":
        return "system-config"
    if category == "clinical-templates":
        return "reference-data"
    if category == "application":
        # Some are patient-relevant
        if any(kw in n for kw in ("file", "interface", "alert", "message", "notification")):
            return "patient-record"
        return "system-config"
    return "unclear"


# Extract entity types
schema = root.find(".//edm:Schema", NS)
entities = []

for et in schema.findall("edm:EntityType", NS):
    name = et.get("Name")
    
    # Key properties
    key_props = []
    key_el = et.find("edm:Key", NS)
    if key_el is not None:
        for pr in key_el.findall("edm:PropertyRef", NS):
            key_props.append(pr.get("Name"))
    
    # Properties
    properties = []
    for prop in et.findall("edm:Property", NS):
        p = {
            "name": prop.get("Name"),
            "type": prop.get("Type"),
            "nullable": prop.get("Nullable", "true") == "true",
            "description": "",  # OData EDMX doesn't include descriptions
        }
        if prop.get("MaxLength"):
            p["maxLength"] = prop.get("MaxLength")
        if prop.get("FixedLength"):
            p["fixedLength"] = prop.get("FixedLength") == "true"
        if prop.get("Unicode"):
            p["unicode"] = prop.get("Unicode") == "true"
        if prop.get("Precision"):
            p["precision"] = int(prop.get("Precision"))
        properties.append(p)
    
    # Navigation properties
    nav_props = []
    for nav in et.findall("edm:NavigationProperty", NS):
        nav_props.append({
            "name": nav.get("Name"),
            "relationship": nav.get("Relationship"),
            "toRole": nav.get("ToRole"),
            "fromRole": nav.get("FromRole"),
        })
    
    cat = categorize_entity(name)
    entities.append({
        "name": name,
        "category": cat,
        "ehiRelevance": ehi_relevance(name, cat),
        "keyProperties": key_props,
        "propertyCount": len(properties),
        "navigationPropertyCount": len(nav_props),
        "properties": properties,
        "navigationProperties": nav_props,
    })

# Extract associations
associations = []
for assoc in schema.findall("edm:Association", NS):
    a = {"name": assoc.get("Name"), "ends": []}
    for end in assoc.findall("edm:End", NS):
        a["ends"].append({
            "type": end.get("Type"),
            "multiplicity": end.get("Multiplicity"),
            "role": end.get("Role"),
        })
    rc = assoc.find("edm:ReferentialConstraint", NS)
    if rc is not None:
        principal = rc.find("edm:Principal", NS)
        dependent = rc.find("edm:Dependent", NS)
        if principal is not None and dependent is not None:
            p_ref = principal.find("edm:PropertyRef", NS)
            d_ref = dependent.find("edm:PropertyRef", NS)
            a["referentialConstraint"] = {
                "principal": {"role": principal.get("Role"), "propertyRef": p_ref.get("Name") if p_ref is not None else None},
                "dependent": {"role": dependent.get("Role"), "propertyRef": d_ref.get("Name") if d_ref is not None else None},
            }
    associations.append(a)

# Extract entity sets (may be in a different Schema element)
entity_sets = []
edm_ns = "http://schemas.microsoft.com/ado/2009/11/edm"
for s in root.iter(f"{{{edm_ns}}}Schema"):
    ec = s.find(f"{{{edm_ns}}}EntityContainer")
    if ec is not None:
        for es in ec.findall(f"{{{edm_ns}}}EntitySet"):
            entity_sets.append({
                "name": es.get("Name"),
                "entityType": es.get("EntityType"),
            })

# Build full inventory
total_properties = sum(e["propertyCount"] for e in entities)
total_nav_props = sum(e["navigationPropertyCount"] for e in entities)
total_with_descriptions = 0  # EDMX has no field descriptions

full_inventory = {
    "source": "OdataMetadata.xml",
    "namespace": "CfChartOpModel",
    "stats": {
        "totalEntityTypes": len(entities),
        "totalProperties": total_properties,
        "totalNavigationProperties": total_nav_props,
        "totalAssociations": len(associations),
        "totalEntitySets": len(entity_sets),
        "fieldsWithDescriptions": total_with_descriptions,
        "descriptionCoverage": "0%",
    },
    "entities": entities,
    "associations": associations,
    "entitySets": entity_sets,
}

with open(FULL_OUTPUT, "w") as f:
    json.dump(full_inventory, f, indent=2)

# Build summary
category_stats = defaultdict(lambda: {"count": 0, "totalFields": 0, "totalNavProps": 0, "entities": []})
ehi_relevance_stats = defaultdict(lambda: {"count": 0, "totalFields": 0})

for e in entities:
    cat = e["category"]
    category_stats[cat]["count"] += 1
    category_stats[cat]["totalFields"] += e["propertyCount"]
    category_stats[cat]["totalNavProps"] += e["navigationPropertyCount"]
    category_stats[cat]["entities"].append(e["name"])
    
    rel = e["ehiRelevance"]
    ehi_relevance_stats[rel]["count"] += 1
    ehi_relevance_stats[rel]["totalFields"] += e["propertyCount"]

# Top 20 largest entities
top_entities = sorted(entities, key=lambda e: e["propertyCount"], reverse=True)[:20]

summary = {
    "source": "OdataMetadata.xml",
    "stats": full_inventory["stats"],
    "categoryBreakdown": {k: {
        "entityCount": v["count"],
        "totalFields": v["totalFields"],
        "totalNavProps": v["totalNavProps"],
        "entities": v["entities"],
    } for k, v in sorted(category_stats.items(), key=lambda x: -x[1]["count"])},
    "ehiRelevanceBreakdown": {k: dict(v) for k, v in sorted(ehi_relevance_stats.items(), key=lambda x: -x[1]["count"])},
    "top20LargestEntities": [{
        "name": e["name"],
        "category": e["category"],
        "ehiRelevance": e["ehiRelevance"],
        "propertyCount": e["propertyCount"],
        "navigationPropertyCount": e["navigationPropertyCount"],
    } for e in top_entities],
    "patientRecordEntities": [{
        "name": e["name"],
        "category": e["category"],
        "propertyCount": e["propertyCount"],
        "navigationPropertyCount": e["navigationPropertyCount"],
    } for e in entities if e["ehiRelevance"] == "patient-record"],
}

with open(SUMMARY_OUTPUT, "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Entity types: {len(entities)}")
print(f"Total properties: {total_properties}")
print(f"Total navigation properties: {total_nav_props}")
print(f"Total associations: {len(associations)}")
print(f"Fields with descriptions: {total_with_descriptions} (0% - EDMX format has no descriptions)")
print()
print("Category breakdown:")
for cat, stats in sorted(category_stats.items(), key=lambda x: -x[1]["count"]):
    print(f"  {cat}: {stats['count']} entities, {stats['totalFields']} fields")
print()
print("EHI relevance:")
for rel, stats in sorted(ehi_relevance_stats.items(), key=lambda x: -x[1]["count"]):
    print(f"  {rel}: {stats['count']} entities, {stats['totalFields']} fields")
print()
print("Top 20 largest entities:")
for e in top_entities:
    print(f"  {e['name']}: {e['propertyCount']} properties, {e['navigationPropertyCount']} nav props ({e['category']})")
print()
print(f"Output: {FULL_OUTPUT}")
print(f"Summary: {SUMMARY_OUTPUT}")
