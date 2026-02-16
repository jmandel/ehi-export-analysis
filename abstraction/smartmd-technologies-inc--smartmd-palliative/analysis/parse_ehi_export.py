#!/usr/bin/env python3
"""
Parse the SMARTMD Palliative b(10) EHI export PDF and sample JSON to produce
a complete entity/field inventory (full-entity-inventory.json).

Sources:
  - 170.315b10-Electronic-Health-Information-Export.pdf (pdftotext output)
  - The sample JSON embedded in pages 7-9 of the PDF

Approach:
  1. Parse the documented field tables from the PDF text
  2. Parse the sample JSON to find all fields actually present (including undocumented CaseList)
  3. Merge documented descriptions with sample-observed fields
  4. Output full-entity-inventory.json
"""

import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/smartmd-technologies-inc--smartmd-palliative/downloads")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/smartmd-technologies-inc--smartmd-palliative/analysis")

# Documented field tables from the PDF (manually extracted from pdftotext output)
DOCUMENTED_SECTIONS = {
    "Patient": {
        "description": "Demographic details regarding the patient",
        "fields": [
            {"name": "PatientId", "type": "string", "description": "Universally unique identifier for this patient"},
            {"name": "PatientName", "type": "string", "description": "Formatted as lastname, firstname middle initial"},
            {"name": "ChartID", "type": "string", "description": "Human readable unique identifier for the patient chart"},
            {"name": "DOB", "type": "date", "description": 'Patient\'s date of birth "m/d/yyyy"'},
            {"name": "Case", "type": "string", "description": "Service line (ex: hospice, palliative)"},
            {"name": "Address1", "type": "string", "description": "Patient's residence"},
            {"name": "City", "type": "string", "description": "Patient's residence"},
            {"name": "State", "type": "string", "description": "Patient's residence"},
            {"name": "Zip", "type": "string", "description": 'Either 5 or 9 digit zip code (with "-" separator)'},
            {"name": "Country", "type": "string", "description": "Country of patient's residence (typically \"USA\")"},
            {"name": "HomePhone", "type": "string", "description": "Formatted patient's home number (ex: 888-555-1212)"},
            {"name": "WorkPhone", "type": "string", "description": "Formatted patient's work number (ex: 888-555-1212)"},
            {"name": "MobilePhone", "type": "string", "description": "Formatted patient's mobile number (ex: 888-555-1212)"},
            {"name": "Email", "type": "string", "description": "Patient's email address"},
        ]
    },
    "KinList": {
        "description": "A set of caregivers or relatives of the patient, along with their contact details",
        "fields": [
            {"name": "PatientId", "type": "string", "description": "Universally unique identifier for this patient"},
            {"name": "KinId", "type": "string", "description": "Universally unique identifier for this kin"},
            {"name": "FirstName", "type": "string", "description": "Kin's first name"},
            {"name": "LastName", "type": "date", "description": "Kin's last name"},  # Note: PDF says type=date, likely a typo
            {"name": "MobilePhone", "type": "string", "description": "Formatted contact mobile number (ex: 888-555-1212)"},
            {"name": "Email", "type": "string", "description": "Kin's email address"},
            {"name": "DeceasedFlag", "type": "bool", "description": "Flag that indicates alive or dead"},
            {"name": "Decisional", "type": "bool", "description": "Flag that indicates if this kin can make healthcare decisions on behalf of the patient"},
            {"name": "Country", "type": "string", "description": "Not used"},
            {"name": "RelationshipList", "type": "string", "description": 'Comma separated list of relationship descriptors between kin and patient. For example, "caregiver, spouse".'},
        ]
    },
    "Meds": {
        "description": "A list of medications the patient is actively taking",
        "fields": [
            {"name": "Strength", "type": "string", "description": "Drug strength (without units)"},
            {"name": "StrengthUnit", "type": "string", "description": "Relevant drug strength unit"},
            {"name": "Form", "type": "string", "description": "Packaging of the drug (ex: tablet, capsule, etc)"},
            {"name": "DoseQuantity", "type": "string", "description": "Amount of the drug given per dose"},
            {"name": "StrengthForm", "type": "string", "description": "Concatenation of strength, strength units and form. Typically used for human readability."},
            {"name": "StartDate", "type": "date", "description": "Date patient started taking drug"},
            {"name": "EndDate", "type": "date", "description": "(optional) Date patient was ordered to discontinue taking drug"},
            {"name": "DoseUnit", "type": "string", "description": "Units for dosage"},
            {"name": "Drug", "type": "string", "description": 'Name of drug. (ex: "Lipitor")'},
            {"name": "DrugId", "type": "int", "description": "Unique internal serial number for the drug"},
            {"name": "DrugInstructions", "type": "string", "description": 'Patient instructions for taking the drug (ex: "with meal")'},
            {"name": "WrittenAs", "type": "string", "description": "Human readable description of the medication order"},
            {"name": "Status", "type": "string", "description": "Current status (active or inactive)"},
        ]
    },
    "Allergies": {
        "description": "A list of the patient allergies (drug, food and environmental)",
        "fields": [
            {"name": "Allergen", "type": "string", "description": "Drug, food, or environmental factor the patient is allergic to"},
            {"name": "Reaction", "type": "string", "description": "Patient's reaction to allergen"},
            {"name": "WrittenAs", "type": "string", "description": "Human readable description of allergy"},
            {"name": "Status", "type": "string", "description": "Current status (active or inactive)"},
        ]
    },
    "ClinicalSummaryProblemDetailsList": {
        "description": "A list of active diseases diagnosed by the provider (also known as Problems)",
        "fields": [
            {"name": "DictionaryCode", "type": "string", "description": "ICD10 code of the disease"},
            {"name": "Problems", "type": "string", "description": "ICD10 description of the disease"},
            {"name": "ActiveDate", "type": "date", "description": "Date on onset for the disease"},
            {"name": "ResolvedDate", "type": "date", "description": "Date disease was resolved (optional)"},
            {"name": "ProblemId", "type": "string", "description": "Universally unique identifier for this problem related to this patient"},
            {"name": "isResolved", "type": "bool", "description": "Indicator of whether the disease is resolved (true or false)"},
            {"name": "isPrimaryDx", "type": "bool", "description": "Indicator of whether this disease is the primary reason for treatment (true or false)"},
        ]
    },
}

# Sample JSON from the PDF (pages 7-9) — manually transcribed
SAMPLE_JSON = {
    "PracticeName": "Your Agency",
    "PatientList": [{
        "Patient": {
            "AccountId": 99,
            "PatientId": "8bd3b88a-f110-4cc8-af3b-dcc2dc417a03",
            "PatientName": "Smith, Joel",
            "ChartId": "MRN050140JS",
            "DOB": "5/1/1940",
            "Case": "Hospice",
            "Address1": "5205 N Ironwood Rd",
            "City": "Glendale",
            "State": "WI",
            "Zip": "53217",
            "Country": "USA",
            "HomePhone": "",
            "WorkPhone": "",
            "MobilePhone": "914-282-8409",
            "EMail": "smartmd-bsmith@outook.com"
        },
        "KinList": [{
            "AccountId": 99,
            "PatientId": "8bd3b88a-f110-4cc8-af3b-dcc2dc417a03",
            "KinId": "51ce4e7d-7804-4052-9793-314a0c769b2f",
            "FirstName": "Sam",
            "LastName": "Smith",
            "MobilePhone": "888-555-1212",
            "Email": "ssmith@gmail.com",
            "DeceasedFlag": False,
            "Decisional": True,
            "Country": "",
            "RelationshipList": ["Caregiver"]
        }],
        "CaseList": [{
            "Notes": "",
            "ProviderId": "d329f144-d5c5-4018-aaba-f2bd3c8fe0da",
            "AddressId": "ffa76152-b6b5-4297-a7d3-caf25d021f23",
            "Address1": "5205 N Ironwood Rd",
            "City": "Glendale",
            "State": "WI",
            "Zip": "53217",
            "Country": "USA",
            "HomePhone": "",
            "MobilePhone": "914-282-8409",
            "EMail": "smartmd-bsmith@outook.com",
            "CaseProvider": {
                "ResourceId": "4013624e-37b2-47a3-9580-75ad8e9022c9",
                "ProviderId": "b347f5cb-e90e-49c4-8881-6fd4cf846489",
                "ProviderName": "Strangelove, Mark",
                "ProviderNameFML": "Mark Strangelove MD",
                "FirstName": "Mark",
                "LastName": "Strangelove"
            },
            "PatientId": "8bd3b88a-f110-4cc8-af3b-dcc2dc417a03",
            "PatientLocationId": "b26f18d3-4eee-4d84-96b4-cc3188ef7951",
            "FullName": "Smith, Joel",
            "LastName": "Smith",
            "FirstName": "Joel",
            "Middle": "",
            "ChartId": "MRN050140JS",
            "DOB": "1940-05-01T00:00:00.0000000+00:00",
            "CreatedOn": "2024-05-01T17:18:40.1400000+00:00",
            "DOBStr": "1940-05-01 00:00:00",
            "CaseClosedFlag": False,
            "CaseDescription": "Hospice",
            "Diagnosis1": "",
            "CaseId": "48c002c5-2f62-4438-81c2-f5be5e4d4224",
            "Score": 0,
            "InsuranceList": [],
            "ExternalContactList": [],
            "InternalContactList": []
        }],
        "Meds": [{
            "Strength": "20",
            "StrengthUnit": "MG",
            "Form": "TABS",
            "DoseQuanity": "",
            "StrengthForm": "20 MG TABS",
            "StartDate": "2024-05-05T12:00:00.0000000+00:00",
            "DoseUnit": "MG",
            "RxNtCode": "209964",
            "IsDiscontinued": False,
            "Drug": "Lipitor",
            "DrugId": "47943",
            "DrugInstructions": "QID",
            "WrittenAs": "Lipitor 20MG TABS QID",
            "Status": "Active"
        }],
        "Allergies": [{
            "Allergen": "Penecillin",
            "Reaction": "Hives",
            "WrittenAs": "Penecillin Hives",
            "Status": "Active"
        }],
        "ClinicalSummaryProblemDetailsList": [{
            "DictionaryCode": "I50.20",
            "Problems": "Unspecified systolic (congestive) heart failure",
            "ActiveDate": "2001-01-01T13:00:00.0000000",
            "ProblemId": "7430744b-d39e-4847-9c64-8f4b0bbee355",
            "IsResolved": False,
            "IsPrimaryDx": False
        }]
    }]
}


def infer_type_from_value(value):
    """Infer a JSON/field type from a sample value."""
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, str):
        # Check for date patterns
        if re.match(r'^\d{4}-\d{2}-\d{2}T', value):
            return "datetime"
        if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', value):
            return "date"
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-', value):
            return "uuid/string"
        return "string"
    return "unknown"


def extract_fields_from_sample(obj, prefix=""):
    """Recursively extract field names and inferred types from a sample JSON object."""
    fields = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                fields.append({"name": key, "type": "object", "sample_value": "{...}"})
                fields.extend(extract_fields_from_sample(value, full_key))
            elif isinstance(value, list):
                fields.append({"name": key, "type": "array", "sample_value": f"[{len(value)} items]"})
                if value and isinstance(value[0], dict):
                    fields.extend(extract_fields_from_sample(value[0], full_key))
                elif value:
                    fields.append({"name": f"{key}[]", "type": infer_type_from_value(value[0]), "sample_value": str(value[0])})
            else:
                fields.append({"name": key, "type": infer_type_from_value(value), "sample_value": str(value) if value != "" else "(empty)"})
    return fields


def build_inventory():
    """Build the complete entity/field inventory."""
    inventory = {
        "source": "170.315b10-Electronic-Health-Information-Export.pdf",
        "product": "SMARTMD Palliative Version 6",
        "export_format": "JSON (per-patient)",
        "documentation_version": "2024v1",
        "entities": []
    }

    # Track all documented field names for comparison
    documented_field_names = {}

    # Process documented sections
    for section_name, section_data in DOCUMENTED_SECTIONS.items():
        entity = {
            "name": section_name,
            "description": section_data["description"],
            "documented": True,
            "is_array": section_name != "Patient",  # Patient is a single object, others are arrays
            "fields": [],
            "field_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
        }

        doc_field_names = set()
        for field in section_data["fields"]:
            field_entry = {
                "name": field["name"],
                "type": field["type"],
                "description": field["description"],
                "documented": True,
                "in_sample": False,
                "sample_value": None,
            }
            doc_field_names.add(field["name"].lower())
            entity["fields"].append(field_entry)

        documented_field_names[section_name] = doc_field_names
        inventory["entities"].append(entity)

    # Now check sample JSON for undocumented fields and add CaseList
    patient_record = SAMPLE_JSON["PatientList"][0]

    # Add top-level PracticeName
    top_level_entity = {
        "name": "ExportRoot",
        "description": "Top-level export wrapper (inferred from sample JSON)",
        "documented": False,
        "is_array": False,
        "fields": [
            {"name": "PracticeName", "type": "string", "description": "", "documented": False, "in_sample": True, "sample_value": "Your Agency"},
            {"name": "PatientList", "type": "array", "description": "", "documented": False, "in_sample": True, "sample_value": "[array of patient records]"},
        ],
        "field_count": 2,
        "fields_with_descriptions": 0,
        "fields_with_types": 2,
    }
    inventory["entities"].insert(0, top_level_entity)

    # Check each documented section against sample
    section_to_sample_key = {
        "Patient": "Patient",
        "KinList": "KinList",
        "Meds": "Meds",
        "Allergies": "Allergies",
        "ClinicalSummaryProblemDetailsList": "ClinicalSummaryProblemDetailsList",
    }

    for entity in inventory["entities"]:
        if entity["name"] == "ExportRoot":
            continue
        sample_key = section_to_sample_key.get(entity["name"])
        if not sample_key or sample_key not in patient_record:
            continue

        sample_data = patient_record[sample_key]
        if isinstance(sample_data, list) and sample_data:
            sample_obj = sample_data[0]
        elif isinstance(sample_data, dict):
            sample_obj = sample_data
        else:
            continue

        # Mark documented fields that appear in sample
        doc_names_lower = {f["name"].lower(): f for f in entity["fields"]}
        for key, value in sample_obj.items():
            key_lower = key.lower()
            if key_lower in doc_names_lower:
                doc_names_lower[key_lower]["in_sample"] = True
                doc_names_lower[key_lower]["sample_value"] = str(value) if not isinstance(value, (dict, list)) else json.dumps(value)
            else:
                # Undocumented field found in sample
                entity["fields"].append({
                    "name": key,
                    "type": infer_type_from_value(value),
                    "description": "",
                    "documented": False,
                    "in_sample": True,
                    "sample_value": str(value) if not isinstance(value, (dict, list)) else json.dumps(value),
                })

    # Add CaseList entity (undocumented, found only in sample)
    case_list_sample = patient_record["CaseList"][0]
    case_list_entity = {
        "name": "CaseList",
        "description": "Case/service line information (NOT documented in field tables, found only in sample JSON)",
        "documented": False,
        "is_array": True,
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
    }

    for key, value in case_list_sample.items():
        if isinstance(value, dict):
            # Nested object (CaseProvider)
            case_list_entity["fields"].append({
                "name": key,
                "type": "object",
                "description": "",
                "documented": False,
                "in_sample": True,
                "sample_value": json.dumps(value),
            })
        elif isinstance(value, list):
            case_list_entity["fields"].append({
                "name": key,
                "type": "array",
                "description": "",
                "documented": False,
                "in_sample": True,
                "sample_value": json.dumps(value),
            })
        else:
            case_list_entity["fields"].append({
                "name": key,
                "type": infer_type_from_value(value),
                "description": "",
                "documented": False,
                "in_sample": True,
                "sample_value": str(value) if value != "" else "(empty)",
            })

    # Add CaseProvider as a sub-entity
    case_provider_entity = {
        "name": "CaseList.CaseProvider",
        "description": "Provider assigned to a case (NOT documented, found only in sample JSON as nested object within CaseList)",
        "documented": False,
        "is_array": False,
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
    }
    case_provider_sample = case_list_sample["CaseProvider"]
    for key, value in case_provider_sample.items():
        case_provider_entity["fields"].append({
            "name": key,
            "type": infer_type_from_value(value),
            "description": "",
            "documented": False,
            "in_sample": True,
            "sample_value": str(value),
        })

    inventory["entities"].append(case_list_entity)
    inventory["entities"].append(case_provider_entity)

    # Compute stats for each entity
    for entity in inventory["entities"]:
        entity["field_count"] = len(entity["fields"])
        entity["fields_with_descriptions"] = sum(1 for f in entity["fields"] if f.get("description"))
        entity["fields_with_types"] = sum(1 for f in entity["fields"] if f.get("type"))

    # Compute overall stats
    total_entities = len(inventory["entities"])
    total_fields = sum(e["field_count"] for e in inventory["entities"])
    documented_entities = sum(1 for e in inventory["entities"] if e["documented"])
    undocumented_entities = total_entities - documented_entities
    total_documented_fields = sum(e["fields_with_descriptions"] for e in inventory["entities"])
    total_fields_in_sample = sum(
        sum(1 for f in e["fields"] if f.get("in_sample")) for e in inventory["entities"]
    )

    inventory["summary"] = {
        "total_entities": total_entities,
        "documented_entities": documented_entities,
        "undocumented_entities": undocumented_entities,
        "total_fields": total_fields,
        "fields_with_descriptions": total_documented_fields,
        "fields_with_types": sum(e["fields_with_types"] for e in inventory["entities"]),
        "fields_found_in_sample": total_fields_in_sample,
        "description_coverage_pct": round(total_documented_fields / total_fields * 100, 1) if total_fields > 0 else 0,
        "sample_data_available": True,
        "value_sets_documented": 0,
        "foreign_keys_documented": 0,
        "relationships_documented": "implicit via PatientId only",
    }

    return inventory


def print_summary(inventory):
    """Print a human-readable summary of the inventory."""
    s = inventory["summary"]
    print("=" * 60)
    print("SMARTMD Palliative EHI Export - Field Inventory Summary")
    print("=" * 60)
    print(f"Total entities:              {s['total_entities']}")
    print(f"  Documented:                {s['documented_entities']}")
    print(f"  Undocumented (sample only):{s['undocumented_entities']}")
    print(f"Total fields:                {s['total_fields']}")
    print(f"  With descriptions:         {s['fields_with_descriptions']} ({s['description_coverage_pct']}%)")
    print(f"  With types:                {s['fields_with_types']}")
    print(f"  Found in sample JSON:      {s['fields_found_in_sample']}")
    print(f"Value sets documented:       {s['value_sets_documented']}")
    print(f"Foreign keys documented:     {s['foreign_keys_documented']}")
    print(f"Relationships:               {s['relationships_documented']}")
    print()

    for entity in inventory["entities"]:
        doc_status = "✅ Documented" if entity["documented"] else "⚠️ Undocumented"
        print(f"\n--- {entity['name']} ({doc_status}) ---")
        print(f"    {entity['description']}")
        print(f"    Fields: {entity['field_count']} | Described: {entity['fields_with_descriptions']} | Typed: {entity['fields_with_types']}")
        for f in entity["fields"]:
            doc_mark = "📝" if f["documented"] else "❓"
            sample_mark = "✓" if f.get("in_sample") else "✗"
            desc_short = f["description"][:60] if f.get("description") else "(no description)"
            print(f"    {doc_mark} {f['name']:30s} {f['type']:15s} sample:{sample_mark}  {desc_short}")


if __name__ == "__main__":
    inventory = build_inventory()

    # Save full inventory
    output_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(output_path, "w") as fp:
        json.dump(inventory, fp, indent=2)
    print(f"Saved full inventory to {output_path}")

    # Save summary
    summary_path = OUTPUT_DIR / "inventory-summary.txt"
    import io
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    print_summary(inventory)
    sys.stdout = old_stdout
    summary_text = buf.getvalue()
    with open(summary_path, "w") as fp:
        fp.write(summary_text)
    print(summary_text)
    print(f"\nSaved summary to {summary_path}")
