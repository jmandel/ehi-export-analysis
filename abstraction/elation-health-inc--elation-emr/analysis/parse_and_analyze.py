#!/usr/bin/env python3
"""
Parse and analyze Elation EMR's EHI Export data dictionary.
Reads the enrichment JSON (parsed from PDF) and produces:
  - full-entity-inventory.json: Complete structured parse
  - analysis-stats.json: Summary statistics
"""
import json
import sys
from collections import defaultdict

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/elation-health-inc--elation-emr"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/elation-health-inc--elation-emr/analysis"

def load_data_dictionary():
    with open(f"{RESULTS_DIR}/downloads/enrichment/data-dictionary.json") as f:
        data = json.load(f)
    
    # Fix 1: Remove "Field" -> "Description" artifact (sub-header from page 6, not a data element)
    data = [i for i in data if not (i["data_element"] == "Field" and i.get("data_description") == "Description")]
    
    # Fix 2: Add the missing clinical orders entry (multi-line in PDF, lost during extraction)
    # Raw PDF text: "Lab Order, Imaging Order, Pulmonary Order, Cardiac Order, Sleep Order"
    # Description: "Orders sent by provider for patient"
    # Formats: Computable PDF + JSON (verified from PDF page 3)
    has_orders = any("order" in i["data_element"].lower() and "billing" not in i["section"].lower() 
                     for i in data)
    if not has_orders:
        data.append({
            "data_element": "Lab Order, Imaging Order, Pulmonary Order, Cardiac Order, Sleep Order",
            "data_description": "Orders sent by provider for patient",
            "section": "Clinical Orders",
            "export_formats": {
                "computable_pdf": True,
                "xml": False,
                "json": True,
                "csv": False
            }
        })
    
    # Fix 3: Add the missing "Personal Relationship" entry (multi-line in PDF, lost during extraction)
    # Raw PDF: "Personal Relationship" -> "Non clinical care team members (ie family, or support caregivers)"
    # Format: Computable PDF (verified from PDF page 3)
    has_personal = any("personal relationship" in i["data_element"].lower() for i in data)
    if not has_personal:
        data.append({
            "data_element": "Personal Relationship",
            "data_description": "Non clinical care team members (ie family, or support caregivers)",
            "section": "Clinical Records",
            "export_formats": {
                "computable_pdf": True,
                "xml": False,
                "json": False,
                "csv": False
            }
        })
    
    return data

def normalize_section(section):
    """Merge 'Billing - Patient Liability (continued)' with 'Billing - Patient Liability'."""
    if section == "Billing - Patient Liability (continued)":
        return "Billing - Patient Liability"
    return section

def is_trivial_description(name, desc):
    """Check if description is just restating the field name."""
    if not desc:
        return True
    desc_l = desc.strip().lower()
    name_l = name.strip().lower()
    # Direct restatement
    if desc_l == name_l:
        return True
    # "Patient X" for field "X"
    if desc_l == f"patient {name_l}":
        return True
    if desc_l.replace("patient ", "") == name_l:
        return True
    # "Guarantor for Patient Payment" repeated for all guarantor fields
    if desc_l == "guarantor for patient payment":
        return True
    return False

def classify_domain(section, element_name, description):
    """Map an element to a standardized EHI domain."""
    s = section.lower()
    n = element_name.lower()
    d = (description or "").lower()
    
    if "billing" in s or "eligibility" in s:
        if "eligibility" in s or "insurance" in s:
            return "Insurance / Coverage"
        if "patient liability" in s or "payment" in s:
            return "Payments"
        return "Claims / Billing"
    if s == "appointments":
        return "Encounters / Visits"
    if s == "imaging":
        return "Imaging / Diagnostic Reports"
    if s == "medications":
        return "Medications / Prescriptions"
    if s == "social history":
        return "Demographics"  # social history is often grouped clinically
    if s == "guarantor information":
        return "Claims / Billing"
    if s == "patient status":
        return "Demographics"
    if s == "additional demographics":
        return "Demographics"
    if s == "patient demographics":
        if "insurance" in n or "carrier" in n or "subscriber" in n or "group no" in n or "plan name" in n:
            return "Insurance / Coverage"
        if "pharmacy" in n:
            return "Medications / Prescriptions"
        if "emergency contact" in n:
            return "Demographics"
        return "Demographics"
    if s == "care team & documents":
        if "files" in n or "messages" in n:
            return "Clinical Notes / Documents"
        return "Care Plans / Goals"
    if s == "clinical records":
        if "problem" in n:
            return "Problems / Conditions / Diagnoses"
        if "vital" in n:
            return "Vitals"
        if "allerg" in n:
            return "Allergies"
        if "visit note" in n:
            return "Clinical Notes / Documents"
        if "lab" in n:
            return "Lab Results"
        if "referral" in n:
            return "Orders / Referrals"
        if "letter" in n:
            return "Clinical Notes / Documents"
        if "procedure" in n:
            return "Procedures"
        if "medical history" in n:
            return "Clinical Notes / Documents"
        if "personal relationship" in n:
            return "Demographics"
        if "immunization" in n:
            return "Immunizations"
        return "Clinical Notes / Documents"
    if "clinical orders" in s or "order" in n:
        return "Orders / Referrals"
    return "Other"

def main():
    data = load_data_dictionary()
    
    # Build full inventory
    inventory = []
    sections = defaultdict(list)
    domain_elements = defaultdict(list)
    
    for item in data:
        section = normalize_section(item["section"])
        name = item["data_element"]
        desc = item.get("data_description", "")
        formats = item["export_formats"]
        
        domain = classify_domain(section, name, desc)
        trivial = is_trivial_description(name, desc)
        
        entry = {
            "data_element": name,
            "data_description": desc if desc else None,
            "section": section,
            "domain": domain,
            "export_formats": formats,
            "has_description": bool(desc and desc.strip()),
            "trivial_description": trivial,
            "has_type": False,  # No types in this data dictionary
            "has_value_set": False,  # No value sets documented
            "has_relationship": False,  # No foreign keys documented (though implied by hierarchy)
        }
        
        inventory.append(entry)
        sections[section].append(entry)
        domain_elements[domain].append(entry)
    
    # Section-level stats
    section_stats = {}
    for section, items in sections.items():
        described = sum(1 for i in items if i["has_description"])
        trivial = sum(1 for i in items if i["trivial_description"])
        formats_used = set()
        for i in items:
            for fmt, val in i["export_formats"].items():
                if val:
                    formats_used.add(fmt)
        section_stats[section] = {
            "field_count": len(items),
            "with_description": described,
            "trivial_descriptions": trivial,
            "meaningful_descriptions": described - trivial,
            "primary_formats": sorted(formats_used),
        }
    
    # Domain-level stats
    domain_stats = {}
    for domain, items in domain_elements.items():
        domain_stats[domain] = {
            "field_count": len(items),
            "sections": sorted(set(i["section"] for i in items)),
            "elements": [i["data_element"] for i in items],
        }
    
    # Overall stats
    total = len(inventory)
    with_desc = sum(1 for i in inventory if i["has_description"])
    trivial = sum(1 for i in inventory if i["trivial_description"])
    format_counts = defaultdict(int)
    for i in inventory:
        for fmt, val in i["export_formats"].items():
            if val:
                format_counts[fmt] += 1
    
    stats = {
        "total_elements": total,
        "with_description": with_desc,
        "description_pct": round(with_desc / total * 100, 1),
        "trivial_descriptions": trivial,
        "meaningful_descriptions": with_desc - trivial,
        "meaningful_description_pct": round((with_desc - trivial) / total * 100, 1),
        "with_data_type": 0,
        "with_value_set": 0,
        "with_relationships": 0,
        "format_counts": dict(format_counts),
        "section_count": len(section_stats),
        "section_stats": section_stats,
        "domain_stats": domain_stats,
    }
    
    # Write outputs
    with open(f"{OUTPUT_DIR}/full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(f"{OUTPUT_DIR}/analysis-stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    print(f"Total elements: {total}")
    print(f"With description: {with_desc} ({stats['description_pct']}%)")
    print(f"Trivial descriptions: {trivial}")
    print(f"Meaningful descriptions: {stats['meaningful_descriptions']} ({stats['meaningful_description_pct']}%)")
    print(f"Data types documented: 0")
    print(f"Value sets documented: 0")
    print(f"Sections: {len(section_stats)}")
    print()
    
    print("=== Section Breakdown ===")
    for section, s in sorted(section_stats.items(), key=lambda x: -x[1]["field_count"]):
        print(f"  {section}: {s['field_count']} fields, {s['meaningful_descriptions']} meaningful descs, formats: {', '.join(s['primary_formats'])}")
    
    print()
    print("=== Domain Mapping ===")
    for domain, d in sorted(domain_stats.items(), key=lambda x: -x[1]["field_count"]):
        print(f"  {domain}: {d['field_count']} fields from {d['sections']}")

if __name__ == "__main__":
    main()
