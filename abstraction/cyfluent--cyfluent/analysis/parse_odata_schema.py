#!/usr/bin/env python3
"""Parse OData EDMX metadata XML into a complete entity inventory JSON.

Reads: results/cyfluent--cyfluent/downloads/OdataMetadata.xml
Writes: full-entity-inventory.json, schema-statistics.json
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter

BASE = Path("/home/jmandel/hobby/ehi-export-analysis")
RESULTS_DIR = BASE / "results" / "cyfluent--cyfluent" / "downloads"
OUTPUT_DIR = BASE / "abstraction" / "cyfluent--cyfluent" / "analysis"

NS = {
    "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
    "edm": "http://schemas.microsoft.com/ado/2009/11/edm",
}

def categorize_entity(name: str) -> str:
    """Assign a domain category based on entity name patterns."""
    n = name.lower()
    if n.startswith("patient") and not n.startswith("patientuser"):
        return "patient"
    if n.startswith("encounter"):
        return "encounter"
    if n.startswith("actionitem") or n.startswith("actionableitem"):
        return "orders/actions"
    if n.startswith("code") or n.startswith("codeset"):
        return "code-sets"
    if n.startswith("facility"):
        return "facility-config"
    if n.startswith("application"):
        return "application"
    if n.startswith("ddo") or n.startswith("hpi"):
        return "clinical-templates"
    if n.startswith("scan"):
        return "scanning"
    if n.startswith("geo"):
        return "geography"
    if n.startswith("location"):
        return "location"
    if n.startswith("humanresource"):
        return "human-resources"
    if n.startswith("eligibility"):
        return "eligibility"
    if n.startswith("securemessage"):
        return "messaging"
    if n.startswith("report"):
        return "reporting"
    return "other"

def ehi_relevance(name: str, category: str) -> str:
    """Classify EHI relevance for coverage assessment."""
    n = name.lower()
    # Direct patient clinical data
    if category == "patient":
        return "patient-record"
    if category == "encounter":
        return "patient-record"
    if category == "orders/actions":
        return "patient-record"
    if category == "scanning":
        return "patient-record"
    if category == "messaging":
        return "patient-record"
    if category == "eligibility":
        return "patient-record"
    if category == "reporting" and "patient" in n:
        return "patient-record"
    # Reference/code data
    if category == "code-sets":
        return "reference-data"
    if category == "clinical-templates":
        return "reference-data"
    # Infrastructure
    if category in ("facility-config", "application", "geography", "location", "human-resources"):
        return "infrastructure"
    if category == "reporting" and "patient" not in n:
        return "infrastructure"
    return "infrastructure"

def parse_schema():
    tree = ET.parse(RESULTS_DIR / "OdataMetadata.xml")
    root = tree.getroot()

    schema = root.find(".//edm:Schema", NS)
    namespace = schema.get("Namespace", "")

    # Parse associations
    associations = {}
    for assoc in schema.findall("edm:Association", NS):
        assoc_name = assoc.get("Name")
        ends = assoc.findall("edm:End", NS)
        ref_constraint = assoc.find("edm:ReferentialConstraint", NS)
        principal = dependent = None
        if ref_constraint is not None:
            p = ref_constraint.find("edm:Principal", NS)
            d = ref_constraint.find("edm:Dependent", NS)
            if p is not None and d is not None:
                principal = {
                    "role": p.get("Role"),
                    "property": [pr.get("Name") for pr in p.findall("edm:PropertyRef", NS)]
                }
                dependent = {
                    "role": d.get("Role"),
                    "property": [pr.get("Name") for pr in d.findall("edm:PropertyRef", NS)]
                }
        associations[assoc_name] = {
            "ends": [{"role": e.get("Role"), "type": e.get("Type").replace(namespace + ".", ""), "multiplicity": e.get("Multiplicity")} for e in ends],
            "principal": principal,
            "dependent": dependent,
        }

    # Parse entity types
    entities = []
    for et in schema.findall("edm:EntityType", NS):
        name = et.get("Name")
        category = categorize_entity(name)
        relevance = ehi_relevance(name, category)

        # Key properties
        key_el = et.find("edm:Key", NS)
        keys = [pr.get("Name") for pr in key_el.findall("edm:PropertyRef", NS)] if key_el is not None else []

        # Properties
        properties = []
        for prop in et.findall("edm:Property", NS):
            p = {
                "name": prop.get("Name"),
                "type": prop.get("Type"),
                "nullable": prop.get("Nullable", "true") == "true",
            }
            if prop.get("MaxLength"):
                p["maxLength"] = prop.get("MaxLength")
            if prop.get("Precision"):
                p["precision"] = prop.get("Precision")
            if prop.get("Scale"):
                p["scale"] = prop.get("Scale")
            if prop.get("FixedLength"):
                p["fixedLength"] = prop.get("FixedLength") == "true"
            if prop.get("Unicode"):
                p["unicode"] = prop.get("Unicode") == "true"
            properties.append(p)

        # Navigation properties
        nav_props = []
        for nav in et.findall("edm:NavigationProperty", NS):
            relationship = nav.get("Relationship", "").replace(namespace + ".", "")
            np = {
                "name": nav.get("Name"),
                "relationship": relationship,
                "fromRole": nav.get("FromRole"),
                "toRole": nav.get("ToRole"),
            }
            # Resolve multiplicity from association
            if relationship in associations:
                assoc = associations[relationship]
                for end in assoc["ends"]:
                    if end["role"] == nav.get("ToRole"):
                        np["targetType"] = end["type"]
                        np["targetMultiplicity"] = end["multiplicity"]
                    if end["role"] == nav.get("FromRole"):
                        np["sourceMultiplicity"] = end["multiplicity"]
            nav_props.append(np)

        entities.append({
            "name": name,
            "category": category,
            "ehi_relevance": relevance,
            "key": keys,
            "properties": properties,
            "navigationProperties": nav_props,
            "propertyCount": len(properties),
            "navigationPropertyCount": len(nav_props),
        })

    # Parse entity sets
    container = schema.find("edm:EntityContainer", NS)
    entity_sets = {}
    if container is not None:
        for es in container.findall("edm:EntitySet", NS):
            et_name = es.get("EntityType", "").replace(namespace + ".", "")
            entity_sets[et_name] = es.get("Name")

    # Compute statistics
    total_props = sum(e["propertyCount"] for e in entities)
    total_nav = sum(e["navigationPropertyCount"] for e in entities)
    cat_counts = Counter(e["category"] for e in entities)
    cat_props = {}
    for cat in cat_counts:
        cat_entities = [e for e in entities if e["category"] == cat]
        cat_props[cat] = {
            "entities": len(cat_entities),
            "properties": sum(e["propertyCount"] for e in cat_entities),
            "navigationProperties": sum(e["navigationPropertyCount"] for e in cat_entities),
        }

    relevance_counts = Counter(e["ehi_relevance"] for e in entities)
    relevance_props = {}
    for rel in relevance_counts:
        rel_entities = [e for e in entities if e["ehi_relevance"] == rel]
        relevance_props[rel] = {
            "entities": len(rel_entities),
            "properties": sum(e["propertyCount"] for e in rel_entities),
        }

    # Type distribution
    type_counts = Counter()
    for e in entities:
        for p in e["properties"]:
            type_counts[p["type"]] += 1

    # Fields with non-null constraints
    non_nullable = sum(1 for e in entities for p in e["properties"] if not p["nullable"])

    stats = {
        "namespace": namespace,
        "totalEntityTypes": len(entities),
        "totalProperties": total_props,
        "totalNavigationProperties": total_nav,
        "totalAssociations": len(associations),
        "totalEntitySets": len(entity_sets),
        "nonNullableProperties": non_nullable,
        "fieldDescriptions": 0,  # OData EDMX has no description annotations
        "categoryBreakdown": cat_props,
        "ehiRelevanceBreakdown": relevance_props,
        "typeDistribution": dict(type_counts.most_common()),
    }

    # Write outputs
    inventory = {
        "source": "OdataMetadata.xml",
        "namespace": namespace,
        "statistics": stats,
        "entities": entities,
        "associations": associations,
    }
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)

    with open(OUTPUT_DIR / "schema-statistics.json", "w") as f:
        json.dump(stats, f, indent=2)

    # Print summary
    print(f"Namespace: {namespace}")
    print(f"Entity types: {len(entities)}")
    print(f"Total properties: {total_props}")
    print(f"Total navigation properties: {total_nav}")
    print(f"Associations: {len(associations)}")
    print(f"Non-nullable properties: {non_nullable}")
    print(f"Field descriptions: 0 (OData EDMX provides no description annotations)")
    print()
    print("Category breakdown:")
    for cat, info in sorted(cat_props.items(), key=lambda x: -x[1]["entities"]):
        print(f"  {cat}: {info['entities']} entities, {info['properties']} properties, {info['navigationProperties']} nav props")
    print()
    print("EHI relevance:")
    for rel, info in sorted(relevance_props.items(), key=lambda x: -x[1]["entities"]):
        print(f"  {rel}: {info['entities']} entities, {info['properties']} properties")
    print()
    print("Top 15 largest entities by property count:")
    for e in sorted(entities, key=lambda x: -x["propertyCount"])[:15]:
        print(f"  {e['name']}: {e['propertyCount']} props, {e['navigationPropertyCount']} nav props ({e['category']})")

if __name__ == "__main__":
    parse_schema()
