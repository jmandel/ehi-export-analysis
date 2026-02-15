#!/usr/bin/env python3
"""
Analyze the coverage of the ClaimPower C-CDA export against the product's
known data domains. Produces a coverage assessment table.
"""

import json

OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/claimpower-inc/analysis"

# Data domains the product stores (from product-research.md)
product_domains = {
    "Demographics": {
        "product_stores": True,
        "source": "Certified (a)(5); visible in C-CDA header and portal screenshot",
        "in_ccda": True,
        "ccda_section": "Patient Demographics",
        "coverage": "Covered",
        "notes": "Standard C-CDA demographics header fields visible in screenshots"
    },
    "Problems / Conditions / Diagnoses": {
        "product_stores": True,
        "source": "Certified (a)(2); problem list in EMR screenshot",
        "in_ccda": True,
        "ccda_section": "Problems",
        "coverage": "Covered",
        "notes": "C-CDA Problems section visible with ICD codes in screenshot (page 3)"
    },
    "Medications / Prescriptions": {
        "product_stores": True,
        "source": "Certified (a)(3); ePrescribing feature ($25/mo)",
        "in_ccda": True,
        "ccda_section": "Medications",
        "coverage": "Partially covered",
        "notes": "C-CDA Medications section present. However, detailed Rx history (refills, pharmacy info, prior auth) likely not in C-CDA"
    },
    "Allergies": {
        "product_stores": True,
        "source": "Certified (a)(4)",
        "in_ccda": True,
        "ccda_section": "Allergies",
        "coverage": "Covered",
        "notes": "Standard C-CDA section"
    },
    "Immunizations": {
        "product_stores": True,
        "source": "Certified (f)(1); dashboard icon visible",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Uncertain",
        "notes": "Not visible in portal section list (page 8), but may be in C-CDA body. Immunization registry export exists as separate report."
    },
    "Vital Signs": {
        "product_stores": True,
        "source": "Clinical documentation feature",
        "in_ccda": True,
        "ccda_section": "Vital Signs",
        "coverage": "Covered",
        "notes": "Standard C-CDA section"
    },
    "Lab Results": {
        "product_stores": True,
        "source": "Lab integration feature; Results icon on dashboard",
        "in_ccda": True,
        "ccda_section": "Results (Discrete)",
        "coverage": "Partially covered",
        "notes": "C-CDA Results section present. Labs Filed Report exists separately, suggesting structured lab data beyond C-CDA"
    },
    "Procedures": {
        "product_stores": True,
        "source": "Clinical documentation",
        "in_ccda": True,
        "ccda_section": "Procedures",
        "coverage": "Covered",
        "notes": "Standard C-CDA section"
    },
    "Clinical Notes / Documents": {
        "product_stores": True,
        "source": "Dragon dictation integration; templates; encounter notes",
        "in_ccda": True,
        "ccda_section": "Patient Medical Documents",
        "coverage": "Partially covered",
        "notes": "C-CDA may include some note content, but rich dictated notes, custom templates, and attached documents are unlikely to be fully represented in C-CDA XML"
    },
    "Encounters / Visits": {
        "product_stores": True,
        "source": "Core EMR function; Patient Census feature",
        "in_ccda": True,
        "ccda_section": "Encounters",
        "coverage": "Partially covered",
        "notes": "C-CDA Encounters section present but likely contains summary data, not full encounter details"
    },
    "Family Health History": {
        "product_stores": True,
        "source": "Certified (a)(12)",
        "in_ccda": True,
        "ccda_section": "Family History",
        "coverage": "Covered",
        "notes": "Standard C-CDA section"
    },
    "Social History": {
        "product_stores": True,
        "source": "Clinical documentation",
        "in_ccda": True,
        "ccda_section": "Social History",
        "coverage": "Covered",
        "notes": "Standard C-CDA section"
    },
    "Care Plans / Goals": {
        "product_stores": True,
        "source": "CCM and TCM features (dashboard icons visible)",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "CCM List and TCM List are separate dashboard modules. No care plan section visible in C-CDA export"
    },
    "Insurance / Coverage": {
        "product_stores": True,
        "source": "Real-time eligibility checking; Insurance Eligibility Status report",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "Insurance data visible in patient search (e.g., 'Aetna HMO', 'Aetna PPO') but not part of C-CDA export"
    },
    "Claims / Billing": {
        "product_stores": True,
        "source": "Core business - managed billing service; Billing icon on dashboard; multiple billing reports",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "Billing/claims is the PRIMARY business of ClaimPower. Multiple billing reports visible (Billing Sent, Billing Stats, Daily Office Collection). None of this data is in C-CDA."
    },
    "Payments": {
        "product_stores": True,
        "source": "Patient Payments feature on website; credit card processing; ERA/EOB posting",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "Payment data is a core part of the billing workflow. Not representable in C-CDA."
    },
    "Patient Communications / Portal Messages": {
        "product_stores": True,
        "source": "Secure messaging in portal (visible in screenshot); text messaging feature",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "Portal has 'Secure Messaging' section (page 8 screenshot). Not part of C-CDA export."
    },
    "Scanned / Attached Documents": {
        "product_stores": True,
        "source": "Attach Documents icon on dashboard; document indexing at $0.10/page",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "Document scanning/indexing is a paid feature. Scanned images/PDFs cannot be represented in C-CDA."
    },
    "Orders / Referrals": {
        "product_stores": True,
        "source": "Certified (a)(1) CPOE",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Not covered",
        "notes": "CPOE orders (lab, imaging, referral) are not standard C-CDA Summary of Care sections"
    },
    "Implantable Devices": {
        "product_stores": True,
        "source": "Certified (a)(14)",
        "in_ccda": False,
        "ccda_section": None,
        "coverage": "Uncertain",
        "notes": "Certified for (a)(14) implantable device list, but no evidence it's in the C-CDA export sections"
    },
}

# Print coverage summary
print("=" * 100)
print("EHI EXPORT COVERAGE ASSESSMENT: ClaimPower Mobile EMR")
print("=" * 100)

covered = 0
partial = 0
not_covered = 0
uncertain = 0

print(f"\n{'Domain':<45} {'Coverage':<20} {'C-CDA Section':<25}")
print("-" * 90)
for domain, info in product_domains.items():
    section = info.get("ccda_section") or "—"
    cov = info["coverage"]
    print(f"{domain:<45} {cov:<20} {section:<25}")
    if cov == "Covered":
        covered += 1
    elif cov == "Partially covered":
        partial += 1
    elif cov == "Not covered":
        not_covered += 1
    else:
        uncertain += 1

print(f"\n{'=' * 90}")
print(f"SUMMARY:")
print(f"  Total domains assessed:  {len(product_domains)}")
print(f"  Covered:                 {covered}")
print(f"  Partially covered:       {partial}")
print(f"  Not covered:             {not_covered}")
print(f"  Uncertain:               {uncertain}")
print(f"\n  Coverage rate (covered+partial): {(covered+partial)/len(product_domains)*100:.0f}%")
print(f"  Full coverage rate:              {covered/len(product_domains)*100:.0f}%")

# Save
with open(f"{OUTPUT}/coverage_assessment.json", "w") as f:
    json.dump(product_domains, f, indent=2)

print(f"\nJSON saved to {OUTPUT}/coverage_assessment.json")
