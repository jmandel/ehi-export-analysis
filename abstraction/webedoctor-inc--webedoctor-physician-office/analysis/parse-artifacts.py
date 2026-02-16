#!/usr/bin/env python3
"""
Parse all EHI export artifacts for WEBeDoctor Physician Office.
Produces full-entity-inventory.json and artifact-summary.json.

Since WEBeDoctor's EHI export is C-CDA 2.1 with no data dictionary,
we document what we know: the export format, the standard C-CDA sections,
and the absence of vendor-specific documentation.
"""

import json
import os
import subprocess

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/webedoctor-inc--webedoctor-physician-office"
ANALYSIS_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/webedoctor-inc--webedoctor-physician-office/analysis"

def get_pdf_info(path):
    """Extract PDF metadata."""
    result = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def get_pdf_text(path):
    """Extract PDF text."""
    result = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    return result.stdout

def analyze_artifacts():
    """Analyze all downloaded artifacts."""
    downloads_dir = os.path.join(RESULTS_DIR, "downloads")
    artifacts = []

    for fname in sorted(os.listdir(downloads_dir)):
        fpath = os.path.join(downloads_dir, fname)
        size = os.path.getsize(fpath)
        artifact = {
            "filename": fname,
            "size_bytes": size,
            "type": os.path.splitext(fname)[1].lower(),
        }

        if fname.endswith(".pdf"):
            info = get_pdf_info(fpath)
            text = get_pdf_text(fpath)
            artifact["pdf_metadata"] = info
            artifact["pages"] = int(info.get("Pages", 0))
            artifact["text_length"] = len(text)
            artifact["text_preview"] = text[:500]

            # Check for EHI-specific content
            text_lower = text.lower()
            artifact["mentions_ccda"] = "c-cda" in text_lower or "ccda" in text_lower
            artifact["mentions_ehi"] = "ehi" in text_lower or "electronic health information" in text_lower
            artifact["mentions_data_dictionary"] = "data dictionary" in text_lower
            artifact["mentions_schema"] = "schema" in text_lower
            artifact["mentions_fhir"] = "fhir" in text_lower
            artifact["mentions_billing"] = "billing" in text_lower or "claim" in text_lower

        elif fname.endswith(".png"):
            artifact["description"] = "Screenshot image"

        artifacts.append(artifact)

    return artifacts

def build_ccda_sections_inventory():
    """
    Since WEBeDoctor exports C-CDA 2.1, document the standard C-CDA sections.
    These are the POTENTIAL sections -- we cannot confirm which ones WEBeDoctor
    actually populates without a sample export file.
    """
    # Standard C-CDA 2.1 document types and their typical sections
    ccda_sections = [
        {"section": "Patient Demographics", "oid": "N/A - header", "status": "likely_included",
         "note": "C-CDA header always contains patient demographics"},
        {"section": "Allergies and Intolerances", "oid": "2.16.840.1.113883.10.20.22.2.6.1",
         "status": "likely_included", "note": "Required in CCD"},
        {"section": "Medications", "oid": "2.16.840.1.113883.10.20.22.2.1.1",
         "status": "likely_included", "note": "Required in CCD"},
        {"section": "Problem List", "oid": "2.16.840.1.113883.10.20.22.2.5.1",
         "status": "likely_included", "note": "Required in CCD"},
        {"section": "Procedures", "oid": "2.16.840.1.113883.10.20.22.2.7.1",
         "status": "likely_included", "note": "Standard CCD section"},
        {"section": "Results (Labs)", "oid": "2.16.840.1.113883.10.20.22.2.3.1",
         "status": "likely_included", "note": "Standard CCD section"},
        {"section": "Vital Signs", "oid": "2.16.840.1.113883.10.20.22.2.4.1",
         "status": "likely_included", "note": "Standard CCD section"},
        {"section": "Immunizations", "oid": "2.16.840.1.113883.10.20.22.2.2.1",
         "status": "likely_included", "note": "Standard CCD section"},
        {"section": "Encounters", "oid": "2.16.840.1.113883.10.20.22.2.22.1",
         "status": "likely_included", "note": "Standard CCD section"},
        {"section": "Plan of Treatment", "oid": "2.16.840.1.113883.10.20.22.2.10",
         "status": "unknown", "note": "Optional CCD section"},
        {"section": "Social History", "oid": "2.16.840.1.113883.10.20.22.2.17",
         "status": "unknown", "note": "Optional but common"},
        {"section": "Family History", "oid": "2.16.840.1.113883.10.20.22.2.15",
         "status": "unknown", "note": "Optional; product is (a)(12) certified"},
        {"section": "Functional Status", "oid": "2.16.840.1.113883.10.20.22.2.14",
         "status": "unknown", "note": "Optional CCD section"},
        {"section": "Medical Equipment", "oid": "2.16.840.1.113883.10.20.22.2.23",
         "status": "unknown", "note": "Optional; product is (a)(14) certified for implantable devices"},
        {"section": "Clinical Notes", "oid": "various", "status": "unknown",
         "note": "C-CDA supports notes but vendor implementation varies"},
        {"section": "Goals", "oid": "2.16.840.1.113883.10.20.22.2.60",
         "status": "unknown", "note": "Optional CCD section"},
        {"section": "Health Concerns", "oid": "2.16.840.1.113883.10.20.22.2.58",
         "status": "unknown", "note": "Optional CCD section"},
        {"section": "Reason for Referral", "oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
         "status": "unknown", "note": "Optional"},
    ]

    return ccda_sections

def build_coverage_assessment():
    """Assess data domain coverage given C-CDA as the export format."""
    domains = [
        {
            "domain": "Demographics",
            "coverage": "likely_partial",
            "evidence": "C-CDA header includes basic demographics; product stores richer data (insurance verification, pre-visit checklists)",
            "gap": "C-CDA carries standard demographics but not full practice management demographics data"
        },
        {
            "domain": "Encounters / visits",
            "coverage": "likely_partial",
            "evidence": "C-CDA Encounters section likely included; but telehealth visit metadata, scheduling details probably not",
            "gap": "Visit types, telehealth specifics, scheduling data likely omitted"
        },
        {
            "domain": "Problems / conditions / diagnoses",
            "coverage": "likely_included",
            "evidence": "Required C-CDA section; product certified for (a)(1)-(a)(5)",
            "gap": "Minimal - standard C-CDA section"
        },
        {
            "domain": "Medications / prescriptions",
            "coverage": "likely_partial",
            "evidence": "C-CDA Medications section likely included; but full e-prescribing workflow (pharmacy routing, EPCS records, refill history) not in C-CDA",
            "gap": "E-prescribing workflow data, controlled substance records likely missing"
        },
        {
            "domain": "Allergies",
            "coverage": "likely_included",
            "evidence": "Required C-CDA section",
            "gap": "Minimal"
        },
        {
            "domain": "Immunizations",
            "coverage": "likely_included",
            "evidence": "Standard C-CDA section; product certified for (f)(1) immunization registry",
            "gap": "Minimal"
        },
        {
            "domain": "Vitals",
            "coverage": "likely_included",
            "evidence": "Standard C-CDA section",
            "gap": "Minimal for in-office vitals"
        },
        {
            "domain": "Lab results",
            "coverage": "likely_included",
            "evidence": "Standard C-CDA Results section; product integrates LabCorp/Quest",
            "gap": "Structured results likely included; raw HL7 lab messages may not be"
        },
        {
            "domain": "Imaging / diagnostic reports",
            "coverage": "unknown",
            "evidence": "Product supports clinical images with annotations; C-CDA cannot carry full image data",
            "gap": "Clinical images, annotations, PACS data almost certainly not in C-CDA XML"
        },
        {
            "domain": "Procedures",
            "coverage": "likely_included",
            "evidence": "Standard C-CDA section",
            "gap": "Minimal for coded procedures"
        },
        {
            "domain": "Clinical notes / documents",
            "coverage": "likely_partial",
            "evidence": "C-CDA supports some note types; product uses specialty templates, dictation, AI-generated notes",
            "gap": "Custom specialty templates, handwriting recognition data, AI-generated notes may not map to C-CDA"
        },
        {
            "domain": "Care plans / goals",
            "coverage": "unknown",
            "evidence": "Optional C-CDA sections; product certified for (b)(11) decision support",
            "gap": "Unknown whether WEBeDoctor populates these optional sections"
        },
        {
            "domain": "Orders / referrals",
            "coverage": "unknown",
            "evidence": "Product supports CPOE and referral management; C-CDA has limited order support",
            "gap": "Referral details, CPOE order history likely incomplete in C-CDA"
        },
        {
            "domain": "Insurance / coverage",
            "coverage": "not_covered",
            "evidence": "C-CDA has no insurance/coverage sections; product stores insurance verification data",
            "gap": "No insurance data in C-CDA format"
        },
        {
            "domain": "Claims / billing",
            "coverage": "not_covered",
            "evidence": "C-CDA has no billing sections; product has full billing/claims/EDI capabilities",
            "gap": "Significant gap - all claims, payments, adjustments, EDI data excluded"
        },
        {
            "domain": "Payments",
            "coverage": "not_covered",
            "evidence": "C-CDA has no payment sections; product tracks payments and adjustments",
            "gap": "All payment records excluded"
        },
        {
            "domain": "Patient communications / portal messages",
            "coverage": "not_covered",
            "evidence": "C-CDA has no messaging sections; product has patient portal with secure messaging",
            "gap": "All portal messages, appointment requests, refill requests excluded"
        },
        {
            "domain": "Remote patient monitoring",
            "coverage": "not_covered",
            "evidence": "C-CDA has no RPM sections; product supports BP, weight, glucose monitoring",
            "gap": "All RPM device readings excluded; some vitals may appear in Vital Signs section but RPM workflow data would not"
        },
        {
            "domain": "Consents / directives",
            "coverage": "unknown",
            "evidence": "C-CDA has optional Advance Directives section; unclear if populated",
            "gap": "Unknown"
        },
    ]
    return domains

def main():
    artifacts = analyze_artifacts()
    ccda_sections = build_ccda_sections_inventory()
    coverage = build_coverage_assessment()

    # Summary
    summary = {
        "vendor": "WEBeDoctor, Inc.",
        "product": "WEBeDoctor Physician Office",
        "version": "6.0",
        "chpl_id": "15.99.05.2526.WEBe.06.02.1.260113",
        "analysis_date": "2026-02-15",
        "export_format": "C-CDA 2.1 (XML)",
        "export_mechanism": "UI-based: Hub > EHI Export > One Time",
        "single_patient": True,
        "bulk_export": True,
        "bulk_format": "ZIP of individual C-CDA files",
        "data_dictionary_provided": False,
        "sample_data_provided": False,
        "schema_provided": False,
        "field_level_documentation": False,
        "total_artifacts": len(artifacts),
        "ehi_specific_artifacts": 1,
        "documentation_pages": 3,
        "classification": "Standard-based projection",
        "artifacts": artifacts,
        "ccda_sections_potential": ccda_sections,
        "domain_coverage": coverage,
    }

    # Count coverage stats
    covered = sum(1 for d in coverage if d["coverage"] in ("likely_included",))
    partial = sum(1 for d in coverage if d["coverage"] in ("likely_partial",))
    not_covered = sum(1 for d in coverage if d["coverage"] == "not_covered")
    unknown = sum(1 for d in coverage if d["coverage"] == "unknown")

    summary["coverage_stats"] = {
        "total_domains_assessed": len(coverage),
        "likely_covered": covered,
        "likely_partial": partial,
        "not_covered": not_covered,
        "unknown": unknown,
    }

    # Save outputs
    with open(os.path.join(ANALYSIS_DIR, "artifact-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Full entity inventory - since there's no data dictionary, we document
    # what we know about the C-CDA structure
    inventory = {
        "source": "C-CDA 2.1 standard (no vendor-specific data dictionary provided)",
        "note": "WEBeDoctor provides no field-level documentation. These sections are inferred from the C-CDA 2.1 standard. Actual content of exports cannot be verified without sample data.",
        "total_sections": len(ccda_sections),
        "sections_likely_included": sum(1 for s in ccda_sections if s["status"] == "likely_included"),
        "sections_unknown": sum(1 for s in ccda_sections if s["status"] == "unknown"),
        "vendor_field_documentation": "none",
        "vendor_type_documentation": "none",
        "vendor_relationship_documentation": "none",
        "vendor_value_set_documentation": "none",
        "entities": ccda_sections,
    }

    with open(os.path.join(ANALYSIS_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    # Print summary
    print(f"Artifacts analyzed: {len(artifacts)}")
    print(f"EHI-specific artifacts: 1 (WEBeDoctor_EHI_Export.pdf, 3 pages)")
    print(f"Export format: C-CDA 2.1")
    print(f"Data dictionary: None")
    print(f"Sample data: None")
    print(f"Schema: None (references HL7 C-CDA spec)")
    print(f"\nDomain coverage:")
    print(f"  Likely covered: {covered}")
    print(f"  Likely partial: {partial}")
    print(f"  Not covered: {not_covered}")
    print(f"  Unknown: {unknown}")
    print(f"\nC-CDA sections (potential): {len(ccda_sections)}")
    print(f"  Likely included: {sum(1 for s in ccda_sections if s['status'] == 'likely_included')}")
    print(f"  Unknown: {sum(1 for s in ccda_sections if s['status'] == 'unknown')}")

if __name__ == "__main__":
    main()
