#!/usr/bin/env python3
"""Parse WEBeDoctor EHI export artifacts and produce inventory JSONs.

Since WEBeDoctor's (b)(10) export is simply C-CDA 2.1 with no product-specific
data dictionary, there are no entities/fields to parse from a vendor-provided
schema. Instead, we document what C-CDA 2.1 sections are referenced and
produce a minimal inventory reflecting the standard C-CDA sections.
"""

import json
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), "..", "downloads")
ANALYSIS = os.path.dirname(__file__)


def extract_pdf_text(path):
    result = subprocess.run(
        ["pdftotext", "-layout", path, "-"],
        capture_output=True, text=True
    )
    return result.stdout


def analyze_ehi_pdf():
    pdf_path = os.path.join(DOWNLOADS, "WEBeDoctor_EHI_Export.pdf")
    text = extract_pdf_text(pdf_path)

    info = subprocess.run(
        ["pdfinfo", pdf_path], capture_output=True, text=True
    )

    return {
        "file": "WEBeDoctor_EHI_Export.pdf",
        "pages": 3,
        "creation_date": "2023-10-27",
        "author": "Syed Imran Ali",
        "format_described": "C-CDA 2.1",
        "export_mechanism": "Hub > EHI Export",
        "single_patient": True,
        "bulk_export": True,
        "bulk_method": "All Patients checkbox generates ZIP of C-CDA files",
        "data_dictionary_provided": False,
        "field_mapping_provided": False,
        "sample_data_provided": False,
        "schema_provided": False,
        "external_reference": "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
        "key_quotes": [
            "WEBeDoctor is compliant with §170.315(b)(10) Electronic Health Information Export by generating C-CDA 2.1 electronic documents.",
            "The full documentation of the C-CDA format is available from the following location: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
        ],
        "content_summary": "3-page PDF with navigation instructions and screenshots. No data dictionary, no field mapping, no schema. Refers entirely to standard C-CDA 2.1 spec."
    }


def analyze_disclosures_pdf():
    pdf_path = os.path.join(DOWNLOADS, "WEBeDoctor_Mandatory_Disclosures_SLI_01192026_Signed.pdf")
    text = extract_pdf_text(pdf_path)

    # Count certified criteria
    criteria = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("170.315"):
            criteria.append(line.split("–")[0].split("-")[0].strip())

    return {
        "file": "WEBeDoctor_Mandatory_Disclosures_SLI_01192026_Signed.pdf",
        "product": "WEBeDoctor Physician Office V 6.0",
        "certification_date": "2026-01-13",
        "certifying_body": "SLI Compliance",
        "b10_certified": True,
        "criteria_count": len(criteria),
    }


def build_ccda_section_inventory():
    """Standard C-CDA 2.1 CCD sections - this is what the vendor references
    as their entire export. No vendor-specific extensions documented."""
    sections = [
        {"name": "Allergies and Intolerances", "loinc": "48765-2", "domain": "Allergies"},
        {"name": "Medications", "loinc": "10160-0", "domain": "Medications"},
        {"name": "Problem List", "loinc": "11450-4", "domain": "Problems"},
        {"name": "Procedures", "loinc": "47519-4", "domain": "Procedures"},
        {"name": "Results", "loinc": "30954-2", "domain": "Lab results"},
        {"name": "Vital Signs", "loinc": "8716-3", "domain": "Vitals"},
        {"name": "Immunizations", "loinc": "11369-6", "domain": "Immunizations"},
        {"name": "Encounters", "loinc": "46240-8", "domain": "Encounters"},
        {"name": "Plan of Treatment", "loinc": "18776-5", "domain": "Care plans"},
        {"name": "Goals", "loinc": "61146-7", "domain": "Goals"},
        {"name": "Health Concerns", "loinc": "75310-3", "domain": "Problems"},
        {"name": "Social History", "loinc": "29762-2", "domain": "Demographics"},
        {"name": "Reason for Visit", "loinc": "29299-5", "domain": "Encounters"},
        {"name": "Assessment", "loinc": "51848-0", "domain": "Clinical notes"},
        {"name": "Functional Status", "loinc": "47420-5", "domain": "Clinical notes"},
        {"name": "Mental Status", "loinc": "10190-7", "domain": "Clinical notes"},
        {"name": "Medical Equipment", "loinc": "46264-8", "domain": "Devices"},
        {"name": "Payers", "loinc": "48768-6", "domain": "Insurance"},
    ]

    entities = []
    for s in sections:
        entities.append({
            "entity_name": f"C-CDA Section: {s['name']}",
            "loinc_code": s["loinc"],
            "domain": s["domain"],
            "source": "HL7 C-CDA 2.1 standard (not vendor-specific)",
            "fields": [],
            "field_count": 0,
            "vendor_documentation": "None - vendor refers to standard C-CDA spec",
            "note": "Section contents defined by C-CDA 2.1 standard, not by vendor"
        })

    return entities


def main():
    ehi_analysis = analyze_ehi_pdf()
    disclosures_analysis = analyze_disclosures_pdf()
    ccda_sections = build_ccda_section_inventory()

    # Entity inventory - reflecting that there's no vendor data dictionary
    full_inventory = {
        "vendor": "WEBeDoctor, Inc.",
        "product": "WEBeDoctor Physician Office",
        "version": "6.0",
        "export_format": "C-CDA 2.1",
        "data_dictionary_provided": False,
        "vendor_specific_schema": False,
        "note": "Vendor provides no product-specific data dictionary or field mapping. "
                "Export is standard C-CDA 2.1 with no documented extensions. "
                "The sections below are standard C-CDA sections, not vendor-defined entities.",
        "entities": ccda_sections,
        "total_entities": len(ccda_sections),
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
    }

    summary = {
        "vendor": "WEBeDoctor, Inc.",
        "product": "WEBeDoctor Physician Office",
        "version": "6.0",
        "export_format": "C-CDA 2.1",
        "data_dictionary_provided": False,
        "total_entities": len(ccda_sections),
        "total_vendor_defined_fields": 0,
        "fields_with_descriptions": 0,
        "artifacts_analyzed": [ehi_analysis, disclosures_analysis],
        "domain_coverage": {
            "clinical_domains_in_ccda": [s["domain"] for s in ccda_sections],
            "domains_missing": [
                "Claims / billing",
                "Payments",
                "Orders / referrals (detail)",
                "Patient communications / portal messages",
                "Custom forms / specialty data",
                "Scanned documents",
                "Remote patient monitoring data",
                "Telehealth records",
                "E-prescribing detail beyond med list",
                "Fax records",
            ]
        },
        "classification": {
            "coverage_breadth": "Minimal/stub/unclear",
            "export_approach": "Repackaged existing export",
        }
    }

    with open(os.path.join(ANALYSIS, "entity-inventory-full.json"), "w") as f:
        json.dump(full_inventory, f, indent=2)

    with open(os.path.join(ANALYSIS, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("Generated entity-inventory-full.json and entity-inventory-summary.json")
    print(f"  C-CDA sections referenced: {len(ccda_sections)}")
    print(f"  Vendor-defined fields: 0")
    print(f"  Data dictionary provided: No")


if __name__ == "__main__":
    main()
