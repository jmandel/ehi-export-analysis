#!/usr/bin/env python3
"""
Parse both EHI export PDFs (Picasso-specific and Amazing Charts) and the API doc,
producing full-entity-inventory.json and summary statistics.
"""

import json
import os
import sys

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/doc-tor-com--picasso"
ENRICHMENT_DIR = os.path.join(RESULTS_DIR, "downloads/enrichment")
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/doc-tor-com--picasso/analysis"

def load_enrichment(filename):
    with open(os.path.join(ENRICHMENT_DIR, filename)) as f:
        return json.load(f)

def categorize_picasso_class(name):
    """Categorize Picasso data classes into clinical domains."""
    clinical = ["Allergies", "Assessment", "Clinical Notes", "Family History",
                "Health Concerns", "Immunizations", "Implantable Devices", "Labs",
                "Medications", "Orders", "Plan Of Treatment", "Problems",
                "Procedures", "Social History", "Tobacco", "Vitals"]
    admin = ["Demographics", "Care Team", "Encounters", "Tasks"]
    insurance = ["Health Insurance"]

    if name in clinical:
        return "Clinical"
    elif name in admin:
        return "Administrative"
    elif name in insurance:
        return "Insurance / Coverage"
    else:
        return "Other"

def categorize_ac_class(name):
    """Categorize Amazing Charts data classes into domains."""
    billing = ["Billing History"]
    clinical = ["Addendum", "Advance Directives", "Alerts", "Allergies and Intolerances Pending",
                "Allergies and Intolerances", "Assesments", "Clinical Notes",
                "FamilyHistory", "FunctionalStatus", "Goals", "Health Concerns",
                "Immunizations", "Implantable device", "Injections", "Lab Tests",
                "List Problem Pending", "List Problem", "Medications Pending",
                "Medications", "Orders", "Plan of Treatment", "Procedures",
                "Risk Factors", "Smoking Statuses", "Tracked Data", "Travel History",
                "Vital Signs"]
    admin = ["Care Team Members", "Patient Demographics", "Next Of Kin",
             "Scheduling", "Email", "Patient Record Release", "User Defined Fields"]
    insurance = ["Health Insurance"]
    patient = ["Patient Generated Data", "Patient Health Information Capture"]
    immunization = ["Demographic Immunization", "HM Rules Ignored", "HM Rules / Immunizations"]
    docs = ["Imported Items"]
    occupation = ["Occupation and Industry History"]
    referrals = ["Referrals"]

    if name in billing:
        return "Billing"
    elif name in clinical:
        return "Clinical"
    elif name in admin:
        return "Administrative"
    elif name in insurance:
        return "Insurance / Coverage"
    elif name in patient:
        return "Patient-Generated"
    elif name in immunization:
        return "Immunization Registry"
    elif name in docs:
        return "Documents"
    elif name in occupation:
        return "Social / Occupational"
    elif name in referrals:
        return "Referrals"
    else:
        return "Other"

def build_inventory():
    picasso = load_enrichment("picasso-data-classes.json")
    ac = load_enrichment("amazing-charts-data-classes.json")

    inventory = {
        "documents": {
            "picasso_ehi_export": {
                "source_file": "Picasso-EHI-Export-Documentation-V1_0-1.pdf",
                "source_url": "https://doc-tor.com/wp-content/uploads/2024/01/Picasso-EHI-Export-Documentation-V1_0-1.pdf",
                "title": picasso["title"],
                "export_format": picasso["export_format"],
                "pages": 3,
                "author": "Kathiresan Palanisamy",
                "created": "2024-01-04",
                "is_registered_url": False,
                "note": "Picasso-specific data dictionary found on mandatory disclosures page"
            },
            "amazing_charts_ehi_export": {
                "source_file": "Picasso-EHI-Export-Documentation-V1_0-1-1.pdf",
                "source_url": "https://doc-tor.com/wp-content/uploads/2023/11/Picasso-EHI-Export-Documentation-V1_0-1-1.pdf",
                "title": ac["title"],
                "export_format": "CSV, JSON, XML",
                "pages": 8,
                "author": "Kathiresan Palanisamy",
                "created": "2023-10-16",
                "is_registered_url": True,
                "note": "Registered URL document; titled 'Amazing Charts EHI Export' despite Picasso filename"
            },
            "api_documentation": {
                "source_file": "PAA_API_documentation.pdf",
                "source_url": "http://live.picassoemr.com/_PicassoAPI/PAA_API_documentation.pdf",
                "title": "Picasso Application Access API",
                "pages": 4,
                "author": "Nathan Marmelo",
                "created": "2023-01-06",
                "note": "SOAP/REST API returning USCDI-compliant CCD XML; (g)(10) API, not (b)(10) export"
            }
        },
        "picasso_export": {
            "total_data_classes": picasso["total_data_classes"],
            "total_columns": picasso["total_columns"],
            "format": "CSV",
            "data_classes": []
        },
        "amazing_charts_export": {
            "total_data_classes": ac["total_data_classes"],
            "total_columns": ac["total_columns"],
            "format": "CSV, JSON, XML",
            "data_classes": []
        }
    }

    # Process Picasso data classes
    for dc in picasso["data_classes"]:
        entry = {
            "name": dc["name"],
            "column_count": dc["column_count"],
            "columns": dc["columns"],
            "category": categorize_picasso_class(dc["name"]),
            "has_descriptions": False,
            "has_types": False,
            "has_value_sets": False,
            "has_relationships": False,
            "description": None
        }
        inventory["picasso_export"]["data_classes"].append(entry)

    # Process Amazing Charts data classes
    for dc in ac["data_classes"]:
        entry = {
            "name": dc["name"],
            "column_count": dc["column_count"],
            "columns": dc["columns"],
            "category": categorize_ac_class(dc["name"]),
            "has_descriptions": False,
            "has_types": False,
            "has_value_sets": False,
            "has_relationships": False,
            "description": None
        }
        inventory["amazing_charts_export"]["data_classes"].append(entry)

    return inventory

def generate_summary(inventory):
    """Generate summary statistics."""
    p = inventory["picasso_export"]
    ac = inventory["amazing_charts_export"]

    # Picasso category breakdown
    p_categories = {}
    for dc in p["data_classes"]:
        cat = dc["category"]
        if cat not in p_categories:
            p_categories[cat] = {"count": 0, "columns": 0}
        p_categories[cat]["count"] += 1
        p_categories[cat]["columns"] += dc["column_count"]

    # AC category breakdown
    ac_categories = {}
    for dc in ac["data_classes"]:
        cat = dc["category"]
        if cat not in ac_categories:
            ac_categories[cat] = {"count": 0, "columns": 0}
        ac_categories[cat]["count"] += 1
        ac_categories[cat]["columns"] += dc["column_count"]

    # Find classes in AC but not in Picasso (approximate matching)
    picasso_names = {dc["name"].lower().replace(" ", "") for dc in p["data_classes"]}
    ac_only = []
    for dc in ac["data_classes"]:
        ac_norm = dc["name"].lower().replace(" ", "")
        # Check for approximate match
        matched = False
        for pn in picasso_names:
            if pn in ac_norm or ac_norm in pn:
                matched = True
                break
            # Handle specific mappings
            mappings = {
                "allergiesandintolerances": "allergies",
                "allergiesandintolerancespending": "allergies",
                "listproblem": "problems",
                "listproblempending": "problems",
                "careteammembers": "careteam",
                "patientdemographics": "demographics",
                "vitalsigns": "vitals",
                "smokingstatuses": "tobacco",
                "planoftreatment": "planoftreatment",
                "implantabledevice": "implantabledevices",
                "assesments": "assessment",
            }
            if ac_norm in mappings and mappings[ac_norm] in picasso_names:
                matched = True
                break
        if not matched:
            ac_only.append({"name": dc["name"], "column_count": dc["column_count"], "category": dc["category"]})

    summary = {
        "picasso": {
            "total_data_classes": p["total_data_classes"],
            "total_columns": p["total_columns"],
            "format": p["format"],
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "pct_described": "0%",
            "categories": p_categories
        },
        "amazing_charts": {
            "total_data_classes": ac["total_data_classes"],
            "total_columns": ac["total_columns"],
            "format": ac["format"],
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "pct_described": "0%",
            "categories": ac_categories
        },
        "classes_in_ac_not_in_picasso": ac_only,
        "classes_in_ac_not_in_picasso_count": len(ac_only)
    }
    return summary

def main():
    inventory = build_inventory()
    summary = generate_summary(inventory)

    # Save full inventory
    inv_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(inv_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote: {inv_path}")

    # Save summary
    sum_path = os.path.join(OUTPUT_DIR, "summary-statistics.json")
    with open(sum_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote: {sum_path}")

    # Print summary to stdout
    print("\n=== PICASSO EHI EXPORT ===")
    print(f"Data classes: {summary['picasso']['total_data_classes']}")
    print(f"Total columns: {summary['picasso']['total_columns']}")
    print(f"Format: {summary['picasso']['format']}")
    print(f"Field descriptions: 0 (column names only, no descriptions)")
    print(f"Field types: 0 (no types documented)")
    print("\nCategory breakdown:")
    for cat, info in summary['picasso']['categories'].items():
        print(f"  {cat}: {info['count']} classes, {info['columns']} columns")

    print("\n=== AMAZING CHARTS EHI EXPORT (registered URL) ===")
    print(f"Data classes: {summary['amazing_charts']['total_data_classes']}")
    print(f"Total columns: {summary['amazing_charts']['total_columns']}")
    print(f"Format: {summary['amazing_charts']['format']}")
    print(f"Field descriptions: 0 (column names only, no descriptions)")
    print(f"Field types: 0 (no types documented)")
    print("\nCategory breakdown:")
    for cat, info in summary['amazing_charts']['categories'].items():
        print(f"  {cat}: {info['count']} classes, {info['columns']} columns")

    print(f"\n=== CLASSES IN AMAZING CHARTS BUT NOT IN PICASSO ({summary['classes_in_ac_not_in_picasso_count']}) ===")
    for cls in summary['classes_in_ac_not_in_picasso']:
        print(f"  {cls['name']}: {cls['column_count']} cols ({cls['category']})")

if __name__ == "__main__":
    main()
