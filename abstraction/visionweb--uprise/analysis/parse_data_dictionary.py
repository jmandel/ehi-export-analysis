"""Parse the Uprise Data Export PDF (extracted text) into structured JSON inventory."""

import json
import re

def parse_data_dictionary(text_file: str) -> list[dict]:
    with open(text_file, 'r') as f:
        lines = f.readlines()

    entities = []
    current_entity = None
    current_fields = []
    in_header = False  # track if we just saw Data/Notes header

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Match entity headers like "AllergyIntolerance.csv"
        entity_match = re.match(r'^(\w[\w\s]*?\w?)\.csv\s*$', stripped)
        if entity_match:
            # Save previous entity
            if current_entity:
                entities.append({
                    "entity": current_entity,
                    "file": current_entity + ".csv",
                    "fields": current_fields
                })
            current_entity = entity_match.group(1).strip()
            current_fields = []
            in_header = False
            continue

        # Skip the "Data" / "Notes" header line
        if re.match(r'^\s*Data\s+Notes\s*$', stripped):
            in_header = True
            continue

        # Skip non-entity content before first entity
        if current_entity is None:
            continue

        # Parse field lines: field name followed by description, separated by whitespace
        # The layout uses fixed-width columns, so field and description are separated by 2+ spaces
        field_match = re.match(r'^\s*(\S+)\s{2,}(.+)$', stripped)
        if field_match:
            field_name = field_match.group(1).strip()
            description = field_match.group(2).strip()
            current_fields.append({
                "name": field_name,
                "description": description
            })
        elif stripped and current_entity and not in_header:
            # Could be a continuation or a field with no description
            # Check if it looks like a standalone field name
            if re.match(r'^[A-Z]\w+$', stripped) and len(stripped) < 60:
                current_fields.append({
                    "name": stripped,
                    "description": ""
                })

    # Save last entity
    if current_entity:
        entities.append({
            "entity": current_entity,
            "file": current_entity + ".csv",
            "fields": current_fields
        })

    return entities


def main():
    entities = parse_data_dictionary("analysis/data_export_raw.txt")

    # Full inventory
    with open("analysis/entity-inventory-full.json", "w") as f:
        json.dump(entities, f, indent=2)

    # Summary
    total_fields = sum(len(e["fields"]) for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e["fields"] if f["description"]
    )

    # Categorize entities
    categories = {
        "Clinical": [],
        "Optometry-Specific": [],
        "Demographics & Administration": [],
        "Billing & Financial": [],
        "Insurance & Benefits": [],
        "Scheduling & Encounters": [],
        "Orders & Products": [],
        "Reference": []
    }

    clinical = {"AllergyIntolerance", "CarePlan", "ClinicalImpression", "Condition",
                "ConditionChiefComplaint", "ConditionConcern", "ConditionFunctionalCognitive",
                "CommunicationEducation", "Goal", "Images", "Immunizations",
                "MedicationRequest", "ObservationLabResults", "ObservationLifeStyle",
                "ObservationPFSH", "ObservationPhysicalExam", "ObservationReviewOfSystem",
                "ObservationVitals", "ObservationBinocularVision", "ObservationKeratometry"}

    optometry = {"Prescription", "PrescriptionAddOn", "Procedure", "ProcedureDilation",
                 "ProcedureDilationRemarks", "ProcedureIOPs", "ProcedureIOPsTargets",
                 "ProcedureOther", "ProcedureScreening", "RefractionAutorefraction",
                 "RefractionContactLensRx", "RefractionCyclopegic", "RefractionManifest",
                 "RefractionRetinoscopy", "RefractionSpectacleRx", "RefractionSpectacleRxAddOns",
                 "RefractionWavefront"}

    demographics = {"Patient", "PatientAccount", "PatientAddress", "PatientAlert",
                    "PatientDocumentReference", "PatientEmail", "PatientLinkedAccount",
                    "PatientLocation", "PatientNote", "PatientPaymentCard",
                    "PatientPhoneNumber", "PatientPreference", "Contact",
                    "ContactLinkedAccount", "Device", "Questionnaire"}

    billing = {"Claim", "ClaimDiagnosis", "ClaimLine", "ClaimLineCodes", "ClaimNote",
               "ClaimStatus", "Invoice", "InvoiceLine", "InvoiceLineAdjustment",
               "InvoiceLineDiagnosis", "Payment", "PaymentItem"}

    insurance = {"Benefit", "BenefitCoverageElectronic", "BenefitCoverageManual",
                 "Policy", "PolicyNote"}

    scheduling = {"Appointment", "Encounter", "EncounterProceduresDiagnosis", "Recall"}

    orders = {"RxOrder", "Product", "ServiceRequest", "Task"}

    reference = {"Locations", "Provider", "DocumentReference"}

    for e in entities:
        name = e["entity"]
        if name in clinical:
            categories["Clinical"].append(e)
        elif name in optometry:
            categories["Optometry-Specific"].append(e)
        elif name in demographics:
            categories["Demographics & Administration"].append(e)
        elif name in billing:
            categories["Billing & Financial"].append(e)
        elif name in insurance:
            categories["Insurance & Benefits"].append(e)
        elif name in scheduling:
            categories["Scheduling & Encounters"].append(e)
        elif name in orders:
            categories["Orders & Products"].append(e)
        elif name in reference:
            categories["Reference"].append(e)
        else:
            categories["Reference"].append(e)  # fallback

    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": total_fields - fields_with_desc,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "categories": {},
        "entities_by_category": {}
    }

    for cat, ents in categories.items():
        cat_fields = sum(len(e["fields"]) for e in ents)
        summary["categories"][cat] = {
            "entity_count": len(ents),
            "field_count": cat_fields
        }
        summary["entities_by_category"][cat] = [
            {"entity": e["entity"], "field_count": len(e["fields"])}
            for e in ents
        ]

    # Top entities by field count
    sorted_entities = sorted(entities, key=lambda e: len(e["fields"]), reverse=True)
    summary["top_20_entities"] = [
        {"entity": e["entity"], "field_count": len(e["fields"])}
        for e in sorted_entities[:20]
    ]

    # All entities list
    summary["all_entities"] = [
        {"entity": e["entity"], "field_count": len(e["fields"]),
         "has_all_descriptions": all(f["description"] for f in e["fields"])}
        for e in entities
    ]

    with open("analysis/entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_coverage_pct']}%)")
    print()
    print("Category breakdown:")
    for cat, info in summary["categories"].items():
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print()
    print("Top 20 entities by field count:")
    for item in summary["top_20_entities"]:
        print(f"  {item['entity']}: {item['field_count']} fields")

    # Check for entities with 0 descriptions
    print()
    no_desc = [e for e in entities if any(not f["description"] for f in e["fields"])]
    if no_desc:
        print("Entities with fields missing descriptions:")
        for e in no_desc:
            missing = sum(1 for f in e["fields"] if not f["description"])
            print(f"  {e['entity']}: {missing}/{len(e['fields'])} fields missing descriptions")
    else:
        print("All fields have descriptions.")


if __name__ == "__main__":
    main()
