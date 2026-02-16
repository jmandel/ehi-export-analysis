#!/usr/bin/env python3
"""
Build full-entity-inventory.json from MEDENT's EHI export documentation.
Sources:
  1. downloads/enrichment/ehi-specs.json — 33 file specs with 648 fields
  2. downloads/enrichment/ascii-field-list.json — 750 financial/billing fields
  3. Raw PDFs verified via pdftotext for spot-checking
"""

import json
import os
import re
import subprocess

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/medent-community-computer-service-inc--medent"
ANALYSIS_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/medent-community-computer-service-inc--medent/analysis"

# Domain categorization for each EHI file spec
DOMAIN_MAP = {
    "Allergy File Specification": "Allergies",
    "Appointment File Specification": "Encounters / Visits",
    "CareTeam and Resources File Specification": "Care Plans / Goals",
    "Diagnosis File Specification": "Problems / Conditions / Diagnoses",
    "Document Listing File Specification": "Clinical Notes / Documents",
    "Electronic Health Information Export": "Export Configuration (metadata)",
    "Encounter File Specification": "Encounters / Visits",
    "Exchanged Patient Level Files": "Patient Communications",
    "Eye and Contact Script File Specification": "Specialty - Ophthalmology/Optometry",
    "Financial File Specification": "Claims / Billing",
    "Goals File Specification": "Care Plans / Goals",
    "HIPAA File Specification": "Consents / Directives",
    "Immunization File Specification": "Immunizations",
    "Info File Details": "Export Configuration (metadata)",
    "InsurancePlan File Specification": "Insurance / Coverage",
    "Location File Specification": "Reference Data",
    "MedicalHistory File Specification": "Problems / Conditions / Diagnoses",
    "Medication File Specification": "Medications / Prescriptions",
    "OBEpisode File Specification": "Specialty - OB/GYN",
    "OBOutcome File Specification": "Specialty - OB/GYN",
    "Order File Specification": "Orders / Referrals",
    "PatientPlan File Specification": "Insurance / Coverage",
    "Patient File Specification": "Demographics",
    "ProblemList File Specification": "Problems / Conditions / Diagnoses",
    "Procedures File Specification": "Procedures",
    "Progress Note Listing File Specification": "Clinical Notes / Documents",
    "Provider File Specification": "Reference Data",
    "Referral File Specification": "Orders / Referrals",
    "Result File Specification": "Lab Results",
    "Screenings and Assessments File Specification": "Vitals / Screenings",
    "SocialHistory File Specification": "Demographics",
    "SurgicalHistory File Specification": "Procedures",
    "Vital File Specification": "Vitals / Screenings",
}

# ASCII Field List area -> domain mapping
ASCII_DOMAIN_MAP = {
    "A": "Claims / Billing",
    "CC": "Immunizations",
    "DI": "Imaging / Diagnostic Reports",
    "H": "Claims / Billing",
    "HA": "Claims / Billing",
    "I": "Immunizations",
    "L": "Lab Results",
    "O": "Orders / Referrals",
    "OA": "Encounters / Visits",
    "P": "Demographics",
    "PI": "Reference Data",
    "PP": "Demographics",
    "R": "Orders / Referrals",
    "RC": "Reference Data",
    "RD": "Reference Data",
    "SB": "Procedures",
}

def load_ehi_specs():
    """Load parsed EHI field specifications."""
    with open(os.path.join(RESULTS_DIR, "downloads/enrichment/ehi-specs.json")) as f:
        return json.load(f)

def load_ascii_fields():
    """Load parsed ASCII field list."""
    with open(os.path.join(RESULTS_DIR, "downloads/enrichment/ascii-field-list.json")) as f:
        return json.load(f)

def verify_pdf_field_count(filename):
    """Use pdftotext to independently count fields in a PDF."""
    pdf_path = os.path.join(RESULTS_DIR, "downloads/ehi_pdfs", filename)
    if not os.path.exists(pdf_path):
        return None
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    # Count lines that start with a field name (snake_case identifier)
    lines = text.strip().split("\n")
    field_lines = []
    for line in lines:
        stripped = line.strip()
        # Match field names: start with lowercase letter, contain underscores or lowercase
        if re.match(r'^[a-z][a-z0-9_]*\s', stripped):
            field_lines.append(stripped.split()[0])
    return field_lines

def build_inventory():
    ehi_specs = load_ehi_specs()
    ascii_data = load_ascii_fields()

    entities = []
    total_ehi_fields = 0
    fields_with_descriptions = 0
    fields_with_examples = 0

    # Process each EHI file spec
    for spec in ehi_specs:
        filename = spec["filename"]
        title = spec["title"]
        fields = spec.get("fields", [])

        # Skip metadata-only specs (no data fields)
        if title in ("Electronic Health Information Export", "Info File Details"):
            entities.append({
                "entity_name": title,
                "source_file": filename,
                "category": DOMAIN_MAP.get(title, "Unknown"),
                "type": "metadata",
                "field_count": 0,
                "fields": [],
                "note": "Configuration/metadata document, not a data export file"
            })
            continue

        # The Financial spec has 4 header fields but the prior extraction garbled it.
        # We know from the PDF: practice_id, patient_id, MEDENT_id, Financial_id
        if title == "Financial File Specification":
            financial_fields = [
                {"name": "practice_id", "description": "Practice ID", "has_description": True},
                {"name": "patient_id", "description": "Patient MRN", "has_description": True},
                {"name": "MEDENT_id", "description": "Patient MEDENT account#", "has_description": True},
                {"name": "Financial_id", "description": "Activity#", "has_description": True},
            ]
            total_ehi_fields += 4
            fields_with_descriptions += 4

            entities.append({
                "entity_name": title,
                "source_file": filename,
                "category": DOMAIN_MAP.get(title, "Unknown"),
                "type": "data_file",
                "field_count": 4,
                "fields": financial_fields,
                "note": "4 header fields; remaining columns are configurable from ASCII Field List (750 fields)"
            })
            continue

        # Normal spec processing
        entity_fields = []
        for field in fields:
            desc_raw = field.get("description", "").strip()
            has_desc = bool(desc_raw) and desc_raw.lower() not in ("blank", "")

            entity_fields.append({
                "name": field["name"],
                "description": desc_raw,
                "has_description": has_desc,
            })
            total_ehi_fields += 1
            if has_desc:
                fields_with_descriptions += 1

        # Verify against PDF
        pdf_fields = verify_pdf_field_count(filename)
        verified_count = len(pdf_fields) if pdf_fields else None

        entities.append({
            "entity_name": title,
            "source_file": filename,
            "category": DOMAIN_MAP.get(title, "Unknown"),
            "type": "data_file",
            "field_count": len(entity_fields),
            "pdf_verified_field_names": verified_count,
            "fields": entity_fields,
        })

    # Process ASCII Field List as a separate section
    ascii_fields_by_area = {}
    for field in ascii_data["fields"]:
        area = field.get("area", "")
        if area not in ascii_fields_by_area:
            ascii_fields_by_area[area] = {
                "area_code": area,
                "area_description": field.get("area_description", ""),
                "domain": ASCII_DOMAIN_MAP.get(area, "Unknown"),
                "fields": []
            }
        has_notes = bool(field.get("notes", "").strip())
        ascii_fields_by_area[area]["fields"].append({
            "format_number": field["format_number"],
            "name": field["name"],
            "notes": field.get("notes", ""),
            "has_description": has_notes,
        })

    ascii_entities = []
    total_ascii_fields = 0
    ascii_fields_with_desc = 0
    for area_code, area_data in sorted(ascii_fields_by_area.items()):
        count = len(area_data["fields"])
        desc_count = sum(1 for f in area_data["fields"] if f["has_description"])
        total_ascii_fields += count
        ascii_fields_with_desc += desc_count
        ascii_entities.append({
            "entity_name": f"ASCII Field List - {area_data['area_description']}",
            "area_code": area_code,
            "category": area_data["domain"],
            "type": "financial_field_list",
            "field_count": count,
            "fields_with_notes": desc_count,
            "fields": area_data["fields"],
        })

    # Build summary
    data_entities = [e for e in entities if e["type"] == "data_file"]

    inventory = {
        "product": "MEDENT",
        "vendor": "Community Computer Service, Inc.",
        "export_type": "Native data model (delimited text + C-CDA documents)",
        "summary": {
            "ehi_file_specs": {
                "total_specs": len(ehi_specs),
                "data_file_specs": len(data_entities),
                "metadata_specs": 2,
                "total_fields": total_ehi_fields,
                "fields_with_descriptions": fields_with_descriptions,
                "description_percentage": round(fields_with_descriptions / total_ehi_fields * 100, 1) if total_ehi_fields else 0,
            },
            "ascii_field_list": {
                "total_fields": total_ascii_fields,
                "areas": len(ascii_fields_by_area),
                "fields_with_notes": ascii_fields_with_desc,
                "notes_percentage": round(ascii_fields_with_desc / total_ascii_fields * 100, 1) if total_ascii_fields else 0,
            },
            "combined_total_fields": total_ehi_fields + total_ascii_fields,
        },
        "ehi_entities": entities,
        "ascii_field_list_entities": ascii_entities,
    }

    # Category breakdown
    cat_stats = {}
    for e in entities:
        cat = e["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"entity_count": 0, "field_count": 0}
        cat_stats[cat]["entity_count"] += 1
        cat_stats[cat]["field_count"] += e["field_count"]
    for ae in ascii_entities:
        cat = ae["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"entity_count": 0, "field_count": 0}
        cat_stats[cat]["entity_count"] += 1
        cat_stats[cat]["field_count"] += ae["field_count"]

    inventory["category_breakdown"] = dict(sorted(cat_stats.items()))

    return inventory

if __name__ == "__main__":
    inventory = build_inventory()

    output_path = os.path.join(ANALYSIS_DIR, "full-entity-inventory.json")
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)

    # Print summary
    s = inventory["summary"]
    print("=== MEDENT EHI Export Inventory ===")
    print(f"EHI File Specs: {s['ehi_file_specs']['total_specs']} specs, {s['ehi_file_specs']['total_fields']} fields")
    print(f"  Fields with descriptions: {s['ehi_file_specs']['fields_with_descriptions']} ({s['ehi_file_specs']['description_percentage']}%)")
    print(f"ASCII Field List: {s['ascii_field_list']['total_fields']} fields across {s['ascii_field_list']['areas']} areas")
    print(f"  Fields with notes: {s['ascii_field_list']['fields_with_notes']} ({s['ascii_field_list']['notes_percentage']}%)")
    print(f"Combined total: {s['combined_total_fields']} fields")
    print()
    print("=== Category Breakdown ===")
    for cat, stats in sorted(inventory["category_breakdown"].items()):
        print(f"  {cat}: {stats['entity_count']} entities, {stats['field_count']} fields")

    # Per-entity summary table
    print()
    print("=== EHI Entity Summary ===")
    print(f"{'Entity':<55} {'Fields':>6} {'Cat'}")
    print("-" * 90)
    for e in inventory["ehi_entities"]:
        if e["type"] == "metadata":
            continue
        print(f"{e['entity_name']:<55} {e['field_count']:>6}  {e['category']}")

    print()
    print(f"Saved to: {output_path}")
