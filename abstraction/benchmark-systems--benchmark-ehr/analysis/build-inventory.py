#!/usr/bin/env python3
"""Build entity-inventory-full.json and entity-inventory-summary.json from the
enrichment JSON, adding categories and computing summary statistics.

The enrichment JSON was parsed from the PDF and verified against raw pdftotext output.
Field counts spot-checked: Patient Demographics=131 ✓, Billing Claims=185 ✓
"""

import json
from pathlib import Path

ENRICHMENT = Path(__file__).parent.parent / "downloads" / "enrichment" / "benchmark-ehr-export-schema.json"
OUT_DIR = Path(__file__).parent

CATEGORIES = {
    "Insurance Master": "Reference/Administrative",
    "Medics": "Reference/Administrative",
    "Referring Doctor": "Reference/Administrative",
    "Adjusters": "Reference/Administrative",
    "Attorneys": "Reference/Administrative",
    "Employers": "Reference/Administrative",
    "Guarantor": "Reference/Administrative",
    "Patient Demographics": "Demographics",
    "Patient Insurance": "Insurance/Coverage",
    "Vaccination": "Clinical - Immunizations",
    "Health Maintenance": "Clinical - Preventive Care",
    "Family History": "Clinical - History",
    "Past Medical Hist": "Clinical - History",
    "Surgery": "Clinical - History",
    "Allergy": "Clinical - Allergies",
    "Current Medication": "Clinical - Medications",
    "Social History": "Clinical - Social/Behavioral",
    "Legal Documents": "Documents/Attachments",
    "Other Documents": "Documents/Attachments",
    "Enc Attach Docs": "Documents/Attachments",
    "Old Progress Notes": "Documents/Attachments",
    "Messages": "Communications",
    "Future Appointments": "Scheduling",
    "Vitals": "Clinical - Vitals",
    "Diagnosis Code": "Clinical - Diagnoses",
    "CPT Codes": "Clinical - Procedures/Codes",
    "HCPC Codes": "Clinical - Procedures/Codes",
    "CCD": "Clinical - Summary Documents",
    "Prescriptions": "Clinical - Medications",
    "Lab Results": "Clinical - Lab",
    "Rad Results": "Clinical - Imaging",
    "Procedure Orders": "Clinical - Orders",
    "Consults": "Clinical - Orders",
    "Enc Progress Notes": "Clinical - Encounters/Notes",
    "Procedure Notes": "Clinical - Encounters/Notes",
    "Letters": "Documents/Attachments",
    "All Vitals": "Clinical - Vitals",
    "Lab Test Result Values": "Clinical - Lab",
    "Patient Cases": "Administrative/Case Management",
    "Patient Notes": "Administrative/Case Management",
    "Patient Alert": "Administrative/Case Management",
    "Past Appointments": "Scheduling",
    "Billing Ledger": "Billing/Financial",
    "Billing Claims": "Billing/Financial",
    "Billing Charges": "Billing/Financial",
    "Patient Advance": "Billing/Financial",
    "Statements": "Billing/Financial",
}

def main():
    with open(ENRICHMENT) as f:
        enrichment = json.load(f)

    entities = []
    for e in enrichment["entities"]:
        entity = {
            "number": e["number"],
            "name": e["name"],
            "description": e["description"],
            "category": CATEGORIES.get(e["name"], "Unknown"),
            "is_billing_only": e["billing_only"],
            "has_file_attachments": e["has_file_attachments"],
            "field_count": len(e["fields"]),
            "fields": [
                {
                    "name": f["name"],
                    "type": None,
                    "description": None,
                }
                for f in e["fields"]
            ],
            "notes": e.get("notes", []),
        }
        entities.append(entity)

    total_fields = sum(e["field_count"] for e in entities)
    entities_with_fields = sum(1 for e in entities if e["field_count"] > 0)
    entities_without_fields = sum(1 for e in entities if e["field_count"] == 0)

    full_inventory = {
        "product": "Benchmark EHR",
        "version": "Denali 3.1",
        "source_document": "b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf",
        "source_pages": 28,
        "export_formats": ["XLS (Excel)", "TXT (text)", "PDF (documents/attachments)", "HTML/XML (CCD)"],
        "entity_count": len(entities),
        "total_fields": total_fields,
        "entities_with_field_lists": entities_with_fields,
        "entities_without_field_lists": entities_without_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "entities": entities,
    }

    with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)

    # Summary
    by_category = {}
    for e in entities:
        cat = e["category"]
        if cat not in by_category:
            by_category[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
        by_category[cat]["entity_count"] += 1
        by_category[cat]["field_count"] += e["field_count"]
        by_category[cat]["entities"].append(e["name"])

    summary = {
        "product": "Benchmark EHR",
        "version": "Denali 3.1",
        "total_entities": len(entities),
        "total_fields": total_fields,
        "entities_with_field_lists": entities_with_fields,
        "entities_without_field_lists": entities_without_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "by_category": dict(sorted(by_category.items())),
        "billing_entities": [e["name"] for e in entities if e["is_billing_only"]],
        "attachment_entities": [e["name"] for e in entities if e["has_file_attachments"]],
        "largest_entities": sorted(
            [{"name": e["name"], "fields": e["field_count"]} for e in entities],
            key=lambda x: -x["fields"],
        )[:10],
        "zero_field_entities": [
            {"name": e["name"], "reason": "document/attachment export" if e["has_file_attachments"] else "description-only, no field list in PDF"}
            for e in entities if e["field_count"] == 0
        ],
    }

    with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print
    print(f"Entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"With field lists: {entities_with_fields} / Without: {entities_without_fields}")
    print(f"\nBy category:")
    for cat, data in sorted(by_category.items()):
        print(f"  {cat}: {data['entity_count']} entities, {data['field_count']} fields")
    print(f"\nTop 10 entities:")
    for item in summary["largest_entities"]:
        print(f"  {item['name']}: {item['fields']} fields")

if __name__ == "__main__":
    main()
