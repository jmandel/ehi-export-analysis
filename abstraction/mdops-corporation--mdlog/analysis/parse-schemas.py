#!/usr/bin/env python3
"""
Parses MDOps CCD XSD schema files and produces entity-inventory-full.json
and entity-inventory-summary.json.

The schemas are standard HL7 CDA R2 (POCD_MT000040) — no MDLog-specific
customizations were found. We treat CDA complex types as "entities" and
their elements/attributes as "fields" for inventory purposes.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
OUTPUT = Path(__file__).parent

NS = {"xs": "http://www.w3.org/2001/XMLSchema"}

# Map CDA types to rough clinical domain categories
CDA_DOMAIN_MAP = {
    "ClinicalDocument": "Document Structure",
    "Patient": "Demographics",
    "PatientRole": "Demographics",
    "Guardian": "Demographics",
    "Birthplace": "Demographics",
    "LanguageCommunication": "Demographics",
    "Observation": "Clinical Data",
    "ObservationMedia": "Clinical Data",
    "ObservationRange": "Clinical Data",
    "Procedure": "Clinical Data",
    "Encounter": "Clinical Data",
    "SubstanceAdministration": "Medications",
    "Supply": "Medications",
    "Consumable": "Medications",
    "ManufacturedProduct": "Medications",
    "LabeledDrug": "Medications",
    "Material": "Medications",
    "Act": "Clinical Data",
    "Organizer": "Clinical Data",
    "Section": "Document Structure",
    "StructuredBody": "Document Structure",
    "NonXMLBody": "Document Structure",
    "Author": "Provenance",
    "Authenticator": "Provenance",
    "LegalAuthenticator": "Provenance",
    "DataEnterer": "Provenance",
    "Custodian": "Provenance",
    "CustodianOrganization": "Provenance",
    "AssignedCustodian": "Provenance",
    "Organization": "Organization",
    "OrganizationPartOf": "Organization",
    "HealthCareFacility": "Organization",
    "Location": "Organization",
    "Place": "Organization",
    "AssignedAuthor": "Participants",
    "AssignedEntity": "Participants",
    "AssociatedEntity": "Participants",
    "Performer1": "Participants",
    "Performer2": "Participants",
    "Participant1": "Participants",
    "Participant2": "Participants",
    "ParticipantRole": "Participants",
    "Person": "Participants",
    "PlayingEntity": "Participants",
    "RelatedEntity": "Participants",
    "RelatedSubject": "Participants",
    "SubjectPerson": "Participants",
    "InformationRecipient": "Participants",
    "IntendedRecipient": "Participants",
    "Informant12": "Participants",
    "RecordTarget": "Document Structure",
    "Entry": "Document Structure",
    "EntryRelationship": "Document Structure",
    "Component1": "Document Structure",
    "Component2": "Document Structure",
    "Component3": "Document Structure",
    "Component4": "Document Structure",
    "Component5": "Document Structure",
    "Reference": "Document Structure",
    "ReferenceRange": "Document Structure",
    "Precondition": "Document Structure",
    "Criterion": "Document Structure",
    "Subject": "Document Structure",
    "ResponsibleParty": "Participants",
    "EncounterParticipant": "Participants",
    "EncompassingEncounter": "Clinical Data",
    "ServiceEvent": "Clinical Data",
    "DocumentationOf": "Document Structure",
    "InFulfillmentOf": "Document Structure",
    "Order": "Orders",
    "Authorization": "Consent",
    "Consent": "Consent",
    "RelatedDocument": "Document Structure",
    "ParentDocument": "Document Structure",
    "ExternalAct": "References",
    "ExternalDocument": "References",
    "ExternalObservation": "References",
    "ExternalProcedure": "References",
    "Device": "Devices",
    "AuthoringDevice": "Devices",
    "MaintainedEntity": "Participants",
    "Specimen": "Laboratory",
    "SpecimenRole": "Laboratory",
    "Product": "Medications",
    "RegionOfInterest": "Clinical Data",
    "InfrastructureRoot.typeId": "Infrastructure",
    "RegionOfInterest.value": "Clinical Data",
}


def parse_schema(filepath):
    """Parse an XSD file and extract complex types, simple types."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    fname = filepath.name

    complex_types = []
    for ct in root.findall(".//xs:complexType[@name]", NS):
        name = ct.get("name")
        mixed = ct.get("mixed", "false") == "true"

        elements = []
        for el in ct.findall(".//xs:element", NS):
            elements.append({
                "name": el.get("name", ""),
                "type": el.get("type"),
                "minOccurs": el.get("minOccurs"),
                "maxOccurs": el.get("maxOccurs"),
                "fixed": el.get("fixed"),
            })

        attributes = []
        for attr in ct.findall(".//xs:attribute", NS):
            attributes.append({
                "name": attr.get("name", ""),
                "type": attr.get("type"),
                "use": attr.get("use"),
                "fixed": attr.get("fixed"),
            })

        doc_el = ct.find(".//xs:documentation", NS)
        doc = doc_el.text.strip() if doc_el is not None and doc_el.text else None

        complex_types.append({
            "name": name,
            "source_file": fname,
            "elements": elements,
            "attributes": attributes,
            "mixed": mixed,
            "documentation": doc,
        })

    simple_types = []
    for st in root.findall(".//xs:simpleType[@name]", NS):
        name = st.get("name")
        restriction = st.find(".//xs:restriction", NS)
        base = restriction.get("base") if restriction is not None else None
        enums = [e.get("value") for e in st.findall(".//xs:enumeration", NS)]
        simple_types.append({
            "name": name,
            "source_file": fname,
            "restriction_base": base,
            "enumeration_values": enums,
        })

    return complex_types, simple_types


def get_domain(type_name):
    """Map a CDA type to a domain category."""
    short = type_name.replace("POCD_MT000040.", "")
    return CDA_DOMAIN_MAP.get(short, "Other")


def main():
    schema_files = sorted(DOWNLOADS.glob("*-schema.xml"))
    all_complex = []
    all_simple = []

    for f in schema_files:
        ct, st = parse_schema(f)
        all_complex.extend(ct)
        all_simple.extend(st)

    # Build entity inventory
    entities = []
    for ct in all_complex:
        short_name = ct["name"].replace("POCD_MT000040.", "")
        fields = []
        for el in ct["elements"]:
            fields.append({
                "name": el["name"],
                "field_type": "element",
                "data_type": el["type"],
                "required": el.get("minOccurs") not in ("0", None) or el.get("fixed") is not None,
                "repeating": el.get("maxOccurs") == "unbounded",
                "description": None,  # Standard CDA schema has no field descriptions
                "fixed_value": el.get("fixed"),
            })
        for attr in ct["attributes"]:
            fields.append({
                "name": attr["name"],
                "field_type": "attribute",
                "data_type": attr["type"],
                "required": attr.get("use") == "required",
                "repeating": False,
                "description": None,
                "fixed_value": attr.get("fixed"),
            })

        entities.append({
            "entity_name": ct["name"],
            "short_name": short_name,
            "source_file": ct["source_file"],
            "domain": get_domain(ct["name"]),
            "documentation": ct["documentation"],
            "field_count": len(fields),
            "fields_with_descriptions": 0,
            "fields_with_types": sum(1 for f in fields if f["data_type"]),
            "fields": fields,
        })

    # Value sets from simple types
    value_sets = []
    for st in all_simple:
        if st["enumeration_values"]:
            value_sets.append({
                "name": st["name"],
                "source_file": st["source_file"],
                "base_type": st["restriction_base"],
                "values": st["enumeration_values"],
                "value_count": len(st["enumeration_values"]),
            })

    # Full inventory
    full_inventory = {
        "product": "MDLog",
        "vendor": "MDOps Corporation",
        "extraction_date": "2026-02-16",
        "schema_type": "HL7 CDA R2 (POCD_MT000040) — standard, unmodified",
        "note": "This is the standard HL7 CDA R2 XML schema, not a vendor-specific data dictionary. "
                "MDOps provides no MDLog-specific documentation, field mappings, or extensions.",
        "schema_files": [f.name for f in schema_files],
        "entities": entities,
        "value_sets": value_sets,
        "is_vendor_specific": False,
    }

    # Summary
    total_fields = sum(e["field_count"] for e in entities)
    fields_with_desc = sum(e["fields_with_descriptions"] for e in entities)
    fields_with_types = sum(e["fields_with_types"] for e in entities)

    domain_breakdown = {}
    for e in entities:
        d = e["domain"]
        if d not in domain_breakdown:
            domain_breakdown[d] = {"entity_count": 0, "field_count": 0}
        domain_breakdown[d]["entity_count"] += 1
        domain_breakdown[d]["field_count"] += e["field_count"]

    # CDA types by source file
    by_file = {}
    for e in entities:
        sf = e["source_file"]
        if sf not in by_file:
            by_file[sf] = {"entity_count": 0, "field_count": 0}
        by_file[sf]["entity_count"] += 1
        by_file[sf]["field_count"] += e["field_count"]

    summary = {
        "product": "MDLog",
        "vendor": "MDOps Corporation",
        "schema_type": "HL7 CDA R2 (POCD_MT000040) — standard, unmodified",
        "is_vendor_specific": False,
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_descriptions_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "fields_with_types": fields_with_types,
        "fields_with_types_pct": round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
        "total_value_sets": len(value_sets),
        "total_enumeration_values": sum(v["value_count"] for v in value_sets),
        "domain_breakdown": domain_breakdown,
        "by_source_file": by_file,
        "top_entities_by_field_count": sorted(
            [{"name": e["entity_name"], "fields": e["field_count"], "domain": e["domain"]}
             for e in entities],
            key=lambda x: -x["fields"]
        )[:20],
    }

    # Write outputs
    with open(OUTPUT / "entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)
    with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['fields_with_descriptions_pct']}%)")
    print(f"Fields with types: {fields_with_types} ({summary['fields_with_types_pct']}%)")
    print(f"Value sets: {len(value_sets)} with {summary['total_enumeration_values']} values")
    print(f"\nDomain breakdown:")
    for d, info in sorted(domain_breakdown.items(), key=lambda x: -x[1]["field_count"]):
        print(f"  {d}: {info['entity_count']} entities, {info['field_count']} fields")
    print(f"\nBy source file:")
    for sf, info in sorted(by_file.items()):
        print(f"  {sf}: {info['entity_count']} entities, {info['field_count']} fields")


if __name__ == "__main__":
    main()
