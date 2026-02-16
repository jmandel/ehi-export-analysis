#!/usr/bin/env python3
"""Parse the Healthie EHI export HTML data dictionary into structured JSON.
Reads from downloads/ehi-export-page.html and produces entity-inventory-full.json
and entity-inventory-summary.json."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

# Read the enrichment JSON (already parsed from HTML) as our base
data_dict = json.loads(Path("../downloads/enrichment/data-dictionary.json").read_text())

# Assign categories based on filename patterns
def categorize(filename):
    clinical = {"Allergies.csv", "Diagnoses.csv", "Medications.csv", "CarePlans.csv",
                "Goals.csv", "Recommendations.csv", "Immunizations.csv", "Procedures.csv",
                "Charting.pdf", "Vitals.csv"}
    demographics = {"Client_Overview.csv", "Addresses.csv", "Family_and_Contacts.csv",
                    "Client_User_Groups.csv", "Other_Care_Team_Members.csv",
                    "Provider.csv", "Referring_Physicians.csv"}
    billing = {"cms1500s.csv", "superbills.csv", "Payments.csv", "Packages.csv",
               "Insurance.csv", "Insurance_authorizations.csv", "Policies.csv"}
    journaling = {"FoodEntry.csv", "MetricEntry.csv", "MirrorEntry.csv", "NoteEntry.csv",
                  "PoopEntry.csv", "SleepEntry.csv", "SymptomEntry.csv", "WaterIntakeEntry.csv",
                  "WorkoutEntry.csv", "Food_Intolerances.csv", "Food_Preferences.csv",
                  "Food_Sensitivities.csv", "client_metrics.csv", "journal_entries.pdf"}
    messaging = {"Messages.csv"}
    documents = {"Documents folder", "format.html"}
    
    if filename in clinical:
        return "Clinical"
    elif filename in demographics:
        return "Demographics & Care Team"
    elif filename in billing:
        return "Billing & Insurance"
    elif filename in journaling:
        return "Journaling & Wellness Tracking"
    elif filename in messaging:
        return "Patient Communications"
    elif filename in documents:
        return "Documents & Export Metadata"
    else:
        return "Other"

# Build full inventory
entities = []
for f in data_dict["files"]:
    fields = []
    for col in f.get("columns", []):
        field = {
            "name": col["name"],
            "type": None,  # not provided in documentation
            "description": col.get("data_notes"),
            "has_description": col.get("data_notes") is not None and col.get("data_notes") != ""
        }
        fields.append(field)
    
    entity = {
        "entity_name": f["filename"],
        "file_type": f["type"],
        "description": f.get("description"),
        "category": categorize(f["filename"]),
        "field_count": len(fields),
        "fields": fields,
        "row_semantics": f.get("row_semantics"),
        "fields_with_descriptions": sum(1 for fld in fields if fld["has_description"])
    }
    entities.append(entity)

full_inventory = {
    "product": "Healthie",
    "source": "downloads/ehi-export-page.html (via enrichment/data-dictionary.json)",
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "total_fields_with_descriptions": sum(e["fields_with_descriptions"] for e in entities),
    "entities": entities
}

# Write full inventory
Path("entity-inventory-full.json").write_text(json.dumps(full_inventory, indent=2))

# Build summary
category_summary = {}
for e in entities:
    cat = e["category"]
    if cat not in category_summary:
        category_summary[cat] = {"entity_count": 0, "field_count": 0, "fields_with_descriptions": 0, "entities": []}
    category_summary[cat]["entity_count"] += 1
    category_summary[cat]["field_count"] += e["field_count"]
    category_summary[cat]["fields_with_descriptions"] += e["fields_with_descriptions"]
    category_summary[cat]["entities"].append(e["entity_name"])

# Identify journal entry files that share identical schema
journal_entry_files = [e for e in entities if e["entity_name"].endswith("Entry.csv")]
identical_schemas = []
if journal_entry_files:
    base_fields = [f["name"] for f in journal_entry_files[0]["fields"]]
    identical = [e["entity_name"] for e in journal_entry_files 
                 if [f["name"] for f in e["fields"]] == base_fields]
    if len(identical) > 1:
        identical_schemas.append({
            "field_names": base_fields,
            "field_count": len(base_fields),
            "files": identical,
            "note": "These journal entry files all share an identical 21-column schema"
        })

summary = {
    "product": "Healthie",
    "total_entities": full_inventory["total_entities"],
    "total_fields": full_inventory["total_fields"],
    "total_fields_with_descriptions": full_inventory["total_fields_with_descriptions"],
    "description_coverage_pct": round(full_inventory["total_fields_with_descriptions"] / full_inventory["total_fields"] * 100, 1) if full_inventory["total_fields"] > 0 else 0,
    "categories": category_summary,
    "identical_schemas": identical_schemas,
    "export_format": "CSV files + PDF + HTML + Documents folder, delivered as ZIP",
    "export_mechanism": {
        "single_patient": "UI button in patient profile > Charting section",
        "population": "Administrator requests via email to Healthie Support"
    }
}

Path("entity-inventory-summary.json").write_text(json.dumps(summary, indent=2))

# Print key stats
print(f"Total entities: {summary['total_entities']}")
print(f"Total fields: {summary['total_fields']}")
print(f"Fields with descriptions: {summary['total_fields_with_descriptions']} ({summary['description_coverage_pct']}%)")
print(f"\nCategories:")
for cat, info in sorted(category_summary.items()):
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields, {info['fields_with_descriptions']} described")
print(f"\nIdentical journal entry schemas: {len(identical_schemas[0]['files']) if identical_schemas else 0} files")
