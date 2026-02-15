#!/usr/bin/env python3
"""Compare USCDI v1 / C-CDA coverage against DOX EMR's known data domains.

Produces a coverage gap analysis showing which data domains the product stores
versus what C-CDA USCDI v1 can represent.
"""

import json
import os

# Data domains DOX EMR stores (from product-research.md)
product_domains = {
    "Demographics & contacts": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA recordTarget covers basic demographics"
    },
    "Insurance / coverage": {
        "stored": True,
        "ccda_coverage": "not_covered",
        "notes": "C-CDA has no section for payer/insurance details beyond basic header"
    },
    "Encounters / visits": {
        "stored": True,
        "ccda_coverage": "partial",
        "notes": "C-CDA Encounters section exists but limited vs full visit model"
    },
    "Problems / diagnoses": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Problems section; USCDI v1 includes conditions"
    },
    "Medications / prescriptions": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Medications section; USCDI v1 includes meds"
    },
    "Allergies": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Allergies section; USCDI v1 includes allergies"
    },
    "Immunizations": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Immunizations section; USCDI v1 includes immunizations"
    },
    "Vitals": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Vital Signs section; USCDI v1 includes vitals"
    },
    "Lab results": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Results section; USCDI v1 includes lab results"
    },
    "Procedures": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA Procedures section; USCDI v1 includes procedures"
    },
    "Clinical notes": {
        "stored": True,
        "ccda_coverage": "partial",
        "notes": "USCDI v1 includes clinical notes but may not capture full podiatry-specific structured data"
    },
    "Care plans / goals": {
        "stored": True,
        "ccda_coverage": "covered",
        "notes": "C-CDA has Goals and Plan of Treatment sections"
    },
    "Orders / referrals": {
        "stored": True,
        "ccda_coverage": "partial",
        "notes": "C-CDA can represent some orders but not full order lifecycle"
    },
    "Billing (CPT/ICD codes, claims, invoices)": {
        "stored": True,
        "ccda_coverage": "not_covered",
        "notes": "C-CDA has no billing/claims sections; DOX auto-extracts CPT/ICD from charts"
    },
    "Payments": {
        "stored": True,
        "ccda_coverage": "not_covered",
        "notes": "C-CDA has no payment tracking capability"
    },
    "Podiatry-specific structured data": {
        "stored": True,
        "ccda_coverage": "not_covered",
        "notes": "Pre-built podiatry database for conditions below the knee; proprietary structured data unlikely to map to standard C-CDA"
    },
    "Patient portal data (patient-entered histories)": {
        "stored": True,
        "ccda_coverage": "not_covered",
        "notes": "Patient-completed online histories not representable in C-CDA"
    },
    "Clinical quality measures (MIPS)": {
        "stored": True,
        "ccda_coverage": "not_covered",
        "notes": "CQM numerator/denominator data not in C-CDA"
    },
}

# Count coverage
covered = sum(1 for d in product_domains.values() if d["ccda_coverage"] == "covered")
partial = sum(1 for d in product_domains.values() if d["ccda_coverage"] == "partial")
not_covered = sum(1 for d in product_domains.values() if d["ccda_coverage"] == "not_covered")

result = {
    "total_domains": len(product_domains),
    "covered_by_ccda": covered,
    "partially_covered": partial,
    "not_covered": not_covered,
    "coverage_percentage": round(covered / len(product_domains) * 100, 1),
    "coverage_with_partial": round((covered + partial) / len(product_domains) * 100, 1),
    "domains": product_domains
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'coverage-gap-analysis.json')
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)

print(f"Total data domains DOX EMR stores: {len(product_domains)}")
print(f"Covered by C-CDA/USCDI v1:         {covered} ({result['coverage_percentage']}%)")
print(f"Partially covered:                  {partial}")
print(f"Not covered:                        {not_covered}")
print()

print("=== COVERED ===")
for name, d in product_domains.items():
    if d["ccda_coverage"] == "covered":
        print(f"  ✓ {name}")

print("\n=== PARTIALLY COVERED ===")
for name, d in product_domains.items():
    if d["ccda_coverage"] == "partial":
        print(f"  ~ {name}: {d['notes']}")

print("\n=== NOT COVERED (gaps) ===")
for name, d in product_domains.items():
    if d["ccda_coverage"] == "not_covered":
        print(f"  ✗ {name}: {d['notes']}")
