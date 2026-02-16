#!/usr/bin/env python3
"""Parse Elation EHI Export PDF data dictionary into structured JSON.

Reads the PDF via pdftotext -layout, parses each data element with its
description, section, and export format flags. Produces:
  - entity-inventory-full.json: complete parse of all fields
  - entity-inventory-summary.json: aggregate statistics
"""

import json
import subprocess
import re
import sys
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "elation-designated-record-set-ehi-export.pdf"
OUT_DIR = Path(__file__).parent

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF_PATH), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_dictionary(text):
    lines = text.split("\n")
    
    # We'll organize by sections (categories in the PDF)
    # The PDF has headers repeated on each page; sections are implicit from the structure
    
    sections = []
    current_section = None
    current_elements = []
    
    # Parse the enrichment JSON as our baseline since it's already been validated
    enrichment_path = Path(__file__).parent.parent / "downloads" / "enrichment" / "data-dictionary.json"
    with open(enrichment_path) as f:
        enrichment_data = json.load(f)
    
    # Group by section
    section_groups = {}
    for elem in enrichment_data:
        sec = elem["section"]
        if sec not in section_groups:
            section_groups[sec] = []
        section_groups[sec].append(elem)
    
    # Normalize section names for entity grouping
    # Map the enrichment sections to logical entity/table names
    section_to_entity = {
        "Imaging": "imaging_reports",
        "Appointments": "appointments",
        "Patient Demographics": "patient_demographics",
        "Medications": "medications",
        "Care Team & Documents": "care_team_documents",
        "Clinical Records": "clinical_records",
        "Additional Demographics": "additional_demographics",
        "Guarantor Information": "guarantor_information",
        "Patient Status": "patient_status",
        "Social History": "social_history",
        "Eligibility/Insurance Verification": "eligibility_insurance_verification",
        "Billing - Bills": "billing_bills",
        "Billing - Patient Liability": "billing_patient_liability",
        "Billing - Patient Liability (continued)": "billing_patient_liability",
        "Billing - Payment Requests": "billing_payment_requests",
    }
    
    # Merge "continued" sections
    merged_groups = {}
    for sec, elements in section_groups.items():
        entity = section_to_entity.get(sec, sec)
        if entity not in merged_groups:
            merged_groups[entity] = {"section_name": sec.replace(" (continued)", ""), "fields": []}
        merged_groups[entity]["fields"].extend(elements)
    
    # Build full inventory
    entities = []
    for entity_id, data in merged_groups.items():
        fields = []
        for elem in data["fields"]:
            field = {
                "name": elem["data_element"],
                "description": elem["data_description"],
                "type": None,  # PDF doesn't specify types
                "export_formats": elem["export_formats"],
            }
            fields.append(field)
        
        # Determine primary export format
        format_counts = {"computable_pdf": 0, "xml": 0, "json": 0, "csv": 0}
        for f in fields:
            for fmt, val in f["export_formats"].items():
                if val:
                    format_counts[fmt] += 1
        primary_format = max(format_counts, key=format_counts.get) if any(format_counts.values()) else "unknown"
        
        entities.append({
            "entity": entity_id,
            "display_name": data["section_name"],
            "field_count": len(fields),
            "primary_export_format": primary_format,
            "fields": fields,
        })
    
    return entities

def compute_summary(entities):
    total_fields = sum(e["field_count"] for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e["fields"]
        if f["description"] and f["description"].strip()
    )
    fields_with_types = sum(
        1 for e in entities for f in e["fields"]
        if f["type"] is not None
    )
    
    # Format distribution
    format_dist = {"computable_pdf": 0, "xml": 0, "json": 0, "csv": 0}
    for e in entities:
        for f in e["fields"]:
            for fmt, val in f["export_formats"].items():
                if val:
                    format_dist[fmt] += 1
    
    # Category breakdown
    category_breakdown = []
    for e in entities:
        category_breakdown.append({
            "entity": e["entity"],
            "display_name": e["display_name"],
            "field_count": e["field_count"],
            "primary_format": e["primary_export_format"],
        })
    
    # Domain mapping
    domain_mapping = {
        "Demographics": ["patient_demographics", "additional_demographics", "guarantor_information", "patient_status"],
        "Encounters / Visits": ["appointments"],
        "Problems / Conditions": ["clinical_records"],
        "Medications / Prescriptions": ["medications"],
        "Allergies": ["clinical_records"],
        "Immunizations": ["medications"],
        "Vitals": ["clinical_records"],
        "Lab Results": ["clinical_records"],
        "Imaging / Diagnostic Reports": ["imaging_reports"],
        "Procedures": ["clinical_records"],
        "Clinical Notes / Documents": ["clinical_records", "care_team_documents"],
        "Care Plans / Goals": [],
        "Orders / Referrals": ["clinical_records"],
        "Insurance / Coverage": ["eligibility_insurance_verification"],
        "Claims / Billing": ["billing_bills"],
        "Payments": ["billing_patient_liability", "billing_payment_requests"],
        "Patient Communications": ["care_team_documents"],
        "Social History": ["social_history"],
    }
    
    return {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_types,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "format_distribution": format_dist,
        "category_breakdown": category_breakdown,
        "domain_mapping": domain_mapping,
    }

def main():
    text = extract_text()
    entities = parse_dictionary(text)
    summary = compute_summary(entities)
    
    with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(entities, f, indent=2)
    
    with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Entities: {summary['total_entities']}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_coverage_pct']}%)")
    print(f"Fields with types: {summary['fields_with_types']}")
    print(f"\nFormat distribution: {json.dumps(summary['format_distribution'], indent=2)}")
    print(f"\nCategory breakdown:")
    for cat in summary['category_breakdown']:
        print(f"  {cat['display_name']}: {cat['field_count']} fields ({cat['primary_format']})")

if __name__ == "__main__":
    main()
