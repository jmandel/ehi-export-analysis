#!/usr/bin/env python3
"""
Parse all Veradigm EHI export artifacts into a unified full-entity-inventory.json.

Sources parsed:
1. Veradigm EHR PDF (ehr-export-v1.txt) - 43 JSON tables
2. Veradigm ePrescribe PDF (eprescribe-v1.txt) - 6 TSV files
3. Veradigm PM PDF (pm-v2.txt) - JSON billing structure
4. FollowMyHealth PDF (fmh-v2.txt) - 18 FHIR resources
5. Veradigm View enrichment catalog (view-entities-catalog.json) - 87 TSV entities
"""

import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/veradigm--veradigm-ehr")
ANALYSIS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/veradigm--veradigm-ehr/analysis")


def parse_ehr_pdf():
    """Parse the EHR export PDF (extracted text) for table/field definitions."""
    text = (ANALYSIS_DIR / "ehr-export-v1.txt").read_text()
    lines = text.split("\n")

    entities = []
    current_entity = None
    current_domain = None
    in_field_defs = False

    # Domain headings appear as standalone lines before Filename entries
    domain_map = {}

    # First pass: identify domains by their page ranges
    domains = [
        "Demographics", "History", "Vitals", "Diagnosis", "Medications",
        "Procedures", "Lab Orders", "Referrals", "Flowsheet",
        "Risk Management Program", "Contact", "Encounter", "ReasonForVisit",
        "Immunization", "Message", "Questionnaire", "Care Plans",
        "Discrete data: Additional .json files"
    ]

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect domain headings
        for d in domains:
            if stripped == d or stripped.startswith(d + "\n"):
                current_domain = d
                break

        # Detect new entity
        filename_match = re.match(r'^Filename:\s+(.+\.json)\s*$', stripped)
        if filename_match:
            if current_entity:
                entities.append(current_entity)

            filename = filename_match.group(1)
            current_entity = {
                "product": "Veradigm EHR",
                "filename": filename,
                "description": "",
                "database_table": "",
                "primary_key": "",
                "domain": current_domain or "Unknown",
                "format": "JSON",
                "fields": []
            }
            in_field_defs = False
            continue

        if current_entity:
            # Look for Description, table name, primary key
            desc_match = re.match(r'^Description:\s*(.+)', stripped)
            if desc_match:
                current_entity["description"] = desc_match.group(1).strip()
                continue

            table_match = re.match(r'^EHR internal database table name:\s*(.+)', stripped)
            if table_match:
                current_entity["database_table"] = table_match.group(1).strip()
                continue

            pk_match = re.match(r'^Primary key:\s*(.+)', stripped)
            if pk_match:
                current_entity["primary_key"] = pk_match.group(1).strip()
                continue

            if stripped == "Field Definitions":
                in_field_defs = True
                continue

            # Header line for field definitions table
            if in_field_defs and stripped.startswith("Field name") and "Description" in stripped:
                continue

            # Skip page footer/header lines
            if re.match(r'^(November|Copyright|Version|This page)', stripped):
                continue
            if stripped == "":
                continue

            # Parse field definition lines - they have three columns
            if in_field_defs and current_entity:
                # Field lines have: FieldName  Description  Type
                # Use regex to capture multi-space separated columns
                field_match = re.match(r'^\s*(\S+)\s{2,}(.+?)\s{2,}(\S+.*?)\s*$', line)
                if field_match:
                    field_name = field_match.group(1).strip()
                    description = field_match.group(2).strip()
                    data_type = field_match.group(3).strip()
                    # Skip if it looks like a header or footer
                    if field_name in ("Field", "name", "Field name"):
                        continue
                    current_entity["fields"].append({
                        "name": field_name,
                        "description": description,
                        "data_type": data_type
                    })

    if current_entity:
        entities.append(current_entity)

    return entities


def parse_eprescribe_pdf():
    """Parse the ePrescribe export PDF for TSV file definitions."""
    text = (ANALYSIS_DIR / "eprescribe-v1.txt").read_text()
    lines = text.split("\n")

    entities = []
    current_entity = None
    in_field_defs = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        filename_match = re.match(r'^Filename:\s+(.+\.tsv)\s*$', stripped)
        if filename_match:
            if current_entity:
                entities.append(current_entity)
            filename = filename_match.group(1)
            current_entity = {
                "product": "Veradigm ePrescribe",
                "filename": filename,
                "description": "",
                "database_table": "",
                "primary_key": "",
                "domain": "ePrescribe",
                "format": "TSV",
                "fields": []
            }
            in_field_defs = False
            continue

        if current_entity:
            desc_match = re.match(r'^Description:\s*(.+)', stripped)
            if desc_match:
                current_entity["description"] = desc_match.group(1).strip()
                continue

            table_match = re.match(r'^(ePrescribe internal database table name|Database table):\s*(.+)', stripped)
            if table_match:
                current_entity["database_table"] = table_match.group(2).strip()
                continue

            pk_match = re.match(r'^Primary key:\s*(.+)', stripped)
            if pk_match:
                current_entity["primary_key"] = pk_match.group(1).strip()
                continue

            if "Field Definitions" in stripped or "Field definitions" in stripped:
                in_field_defs = True
                continue

            if in_field_defs and stripped.startswith("Field name") and "Description" in stripped:
                continue

            if re.match(r'^(November|Copyright|Version|This page)', stripped):
                continue
            if stripped == "":
                continue

            if in_field_defs:
                field_match = re.match(r'^\s*(\S+)\s{2,}(.+?)\s{2,}(\S+.*?)\s*$', line)
                if field_match:
                    field_name = field_match.group(1).strip()
                    description = field_match.group(2).strip()
                    data_type = field_match.group(3).strip()
                    if field_name in ("Field", "name"):
                        continue
                    current_entity["fields"].append({
                        "name": field_name,
                        "description": description,
                        "data_type": data_type
                    })

    if current_entity:
        entities.append(current_entity)

    return entities


def parse_pm_pdf():
    """Parse the Practice Management export PDF for billing data structure."""
    text = (ANALYSIS_DIR / "pm-v2.txt").read_text()
    lines = text.split("\n")

    # PM uses a hierarchical JSON structure, not flat tables.
    # Parse the chapter 2 reference for top-level fields
    # and appendix for claim info fields

    main_fields = []
    appendix_sections = {}
    current_appendix = None
    in_chapter2 = False
    in_appendix = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if "Chapter 2:" in stripped or "EHI data export file reference" in stripped:
            in_chapter2 = True
            in_appendix = False
            continue
        if "Chapter 3:" in stripped or "Appendix" in stripped:
            in_chapter2 = False
            in_appendix = True
            continue

        # Parse appendix section headers
        app_header = re.match(r'^(Claim information|Ailment information|Ambulance information|Drug information|Anesthesia information|Dental information)\s+fields', stripped)
        if app_header:
            current_appendix = app_header.group(1).strip()
            appendix_sections[current_appendix] = []
            continue

        if in_chapter2 and stripped:
            # Chapter 2 has hierarchical field docs with indentation
            field_match = re.match(r'^\s{4,}(\w[\w\s]*\w)\s{2,}(.+)$', line)
            if field_match:
                main_fields.append({
                    "name": field_match.group(1).strip(),
                    "description": field_match.group(2).strip()
                })

        if in_appendix and current_appendix and stripped:
            if re.match(r'^(May|Copyright|EHI|This page)', stripped):
                continue
            if re.match(r'^The following', stripped):
                continue
            if stripped and not stripped.startswith("Chapter") and len(stripped) > 2:
                # It's a field name (one per line in the appendix)
                if stripped not in ("fields", "Appendix"):
                    appendix_sections.setdefault(current_appendix, []).append(stripped)

    # Build as a single entity with sub-sections
    entity = {
        "product": "Veradigm Practice Management",
        "filename": "EHI_Export.json",
        "description": "Patient financial/billing data including vouchers, claims, services, and payments",
        "database_table": "N/A (hierarchical JSON)",
        "primary_key": "N/A",
        "domain": "Billing/Claims",
        "format": "JSON",
        "fields": main_fields,
        "appendix_sections": {}
    }

    for section_name, field_names in appendix_sections.items():
        entity["appendix_sections"][section_name] = [
            {"name": fn, "description": f"{section_name} field"} for fn in field_names
        ]

    return [entity]


def parse_fmh_pdf():
    """Parse the FollowMyHealth FHIR export PDF for supported resources."""
    text = (ANALYSIS_DIR / "fmh-v2.txt").read_text()
    lines = text.split("\n")

    resources = []
    current_resource = None
    collecting_description = False

    # FHIR resource names
    resource_names = [
        "Account", "Allergy Intolerance", "Appointment", "Bundle",
        "Communication", "Condition", "Diagnostic Report", "Document Reference",
        "Encounter", "Family Member History", "Immunization", "Invoice",
        "Medication", "Medication Request", "Observation", "Patient",
        "Practitioner", "Procedure"
    ]

    for i, line in enumerate(lines):
        stripped = line.strip()

        for rn in resource_names:
            if stripped == rn:
                if current_resource:
                    resources.append(current_resource)
                fhir_type = rn.replace(" ", "")
                current_resource = {
                    "product": "FollowMyHealth",
                    "filename": f"{fhir_type} (FHIR R4 Bundle entry)",
                    "description": "",
                    "database_table": "N/A (FHIR resource)",
                    "primary_key": "FHIR resource ID",
                    "domain": "Patient Portal/PHR",
                    "format": "FHIR R4 JSON",
                    "fhir_resource_type": fhir_type,
                    "fields": [],
                    "extensions": [],
                    "location_in_phr": ""
                }
                collecting_description = True
                break

        if current_resource and collecting_description:
            if "Where this information is found" in stripped:
                collecting_description = False
            loc_match = re.match(r'^\s*•\s+(.+)', stripped)
            if loc_match and not collecting_description:
                current_resource["location_in_phr"] += loc_match.group(1) + "; "

            if "Extension" in stripped and "http" in stripped:
                current_resource["extensions"].append(stripped)

    if current_resource:
        resources.append(current_resource)

    return resources


def parse_view_catalog():
    """Load the pre-parsed Veradigm View entity catalog."""
    catalog = json.loads(
        (RESULTS_DIR / "downloads/enrichment/view-entities-catalog.json").read_text()
    )

    entities = []
    # Categorize by looking at the entity descriptions and filenames
    for entry in catalog:
        entity = {
            "product": "Veradigm View (Practice Fusion)",
            "filename": entry["tsvFilename"],
            "description": entry.get("entityDescription", ""),
            "database_table": "N/A (TSV export)",
            "primary_key": "",
            "domain": categorize_view_entity(entry["tsvFilename"]),
            "format": "TSV",
            "fields": entry["fields"]
        }
        entities.append(entity)

    return entities


def categorize_view_entity(filename):
    """Categorize View entities based on filename patterns."""
    f = filename.lower()
    if any(x in f for x in ["demographic", "contact", "ethnicity", "race", "gender", "guarantor", "occupation", "tribal", "communication-settings"]):
        return "Demographics"
    if any(x in f for x in ["encounter", "visit"]):
        return "Encounters"
    if any(x in f for x in ["lab", "specimen", "result"]):
        return "Labs"
    if any(x in f for x in ["insurance", "superbill", "eligibil"]):
        return "Billing/Insurance"
    if any(x in f for x in ["message", "attachment"]):
        return "Messaging"
    if any(x in f for x in ["provider", "user", "facilit", "pharmac", "care-team"]):
        return "Administrative"
    if any(x in f for x in ["allergy", "condition", "diagnos", "medication", "prescription",
                             "procedure", "immunization", "vital", "observation",
                             "referral", "goal", "health-concern", "advance-directive",
                             "smoking", "risk", "restriction", "device", "family",
                             "questionnaire", "worksheet", "document", "addendum",
                             "assessment", "education", "drug-alert"]):
        return "Clinical"
    if any(x in f for x in ["appointment"]):
        return "Administrative"
    return "Other"


def compute_summary(all_entities):
    """Compute summary statistics across all products."""
    summary = {
        "by_product": {},
        "totals": {
            "entities": 0,
            "fields": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0
        }
    }

    for entity in all_entities:
        product = entity["product"]
        if product not in summary["by_product"]:
            summary["by_product"][product] = {
                "entities": 0,
                "fields": 0,
                "fields_with_descriptions": 0,
                "fields_with_types": 0,
                "format": entity["format"],
                "domains": {}
            }

        ps = summary["by_product"][product]
        ps["entities"] += 1
        summary["totals"]["entities"] += 1

        domain = entity.get("domain", "Unknown")
        if domain not in ps["domains"]:
            ps["domains"][domain] = {"entities": 0, "fields": 0}
        ps["domains"][domain]["entities"] += 1

        for field in entity.get("fields", []):
            ps["fields"] += 1
            summary["totals"]["fields"] += 1
            ps["domains"][domain]["fields"] += 1

            desc = field.get("description", "")
            if desc and desc.strip() and desc.strip() not in ("", "-", "N/A"):
                ps["fields_with_descriptions"] += 1
                summary["totals"]["fields_with_descriptions"] += 1

            dtype = field.get("data_type", field.get("dataType", ""))
            if dtype and dtype.strip():
                ps["fields_with_types"] += 1
                summary["totals"]["fields_with_types"] += 1

        # Count appendix fields for PM
        for section_name, app_fields in entity.get("appendix_sections", {}).items():
            for af in app_fields:
                ps["fields"] += 1
                summary["totals"]["fields"] += 1

    return summary


def main():
    print("Parsing Veradigm EHR PDF...", file=sys.stderr)
    ehr_entities = parse_ehr_pdf()
    print(f"  Found {len(ehr_entities)} entities, {sum(len(e['fields']) for e in ehr_entities)} fields", file=sys.stderr)

    print("Parsing Veradigm ePrescribe PDF...", file=sys.stderr)
    eprescribe_entities = parse_eprescribe_pdf()
    print(f"  Found {len(eprescribe_entities)} entities, {sum(len(e['fields']) for e in eprescribe_entities)} fields", file=sys.stderr)

    print("Parsing Veradigm PM PDF...", file=sys.stderr)
    pm_entities = parse_pm_pdf()
    pm_main_fields = sum(len(e['fields']) for e in pm_entities)
    pm_appendix_fields = sum(sum(len(v) for v in e.get('appendix_sections', {}).values()) for e in pm_entities)
    print(f"  Found {len(pm_entities)} entities, {pm_main_fields} main fields + {pm_appendix_fields} appendix fields", file=sys.stderr)

    print("Parsing FollowMyHealth PDF...", file=sys.stderr)
    fmh_entities = parse_fmh_pdf()
    print(f"  Found {len(fmh_entities)} resources", file=sys.stderr)

    print("Loading Veradigm View catalog...", file=sys.stderr)
    view_entities = parse_view_catalog()
    print(f"  Found {len(view_entities)} entities, {sum(len(e['fields']) for e in view_entities)} fields", file=sys.stderr)

    all_entities = ehr_entities + eprescribe_entities + pm_entities + fmh_entities + view_entities

    summary = compute_summary(all_entities)

    output = {
        "metadata": {
            "analysis_date": "2026-02-16",
            "products_analyzed": [
                "Veradigm EHR",
                "Veradigm ePrescribe",
                "Veradigm Practice Management",
                "FollowMyHealth",
                "Veradigm View (Practice Fusion)"
            ],
            "sources": {
                "ehr": "VeradigmEHR_EHI_Export_output_format_documentation_v1.pdf (89 pages, Nov 2023)",
                "eprescribe": "VeradigmePrescribe_EHI_Export_Documentation_v1.pdf (22 pages, Nov 2023)",
                "pm": "EHIDataExportFile_ReferenceGuide_VeradigmPM_V2.pdf (20 pages, May 2024)",
                "fmh": "VeradigmFMH_EHI_Export_Data_Guide_v2.pdf (20 pages, Feb 2024)",
                "view": "veradigm-view-v6 HTML site (88 pages, Jan 2026)"
            }
        },
        "summary": summary,
        "entities": all_entities
    }

    # Save full inventory
    inventory_path = ANALYSIS_DIR / "full-entity-inventory.json"
    with open(inventory_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved full inventory to {inventory_path}", file=sys.stderr)

    # Save summary separately
    summary_path = ANALYSIS_DIR / "summary-stats.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary to {summary_path}", file=sys.stderr)

    # Print summary to stdout
    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
