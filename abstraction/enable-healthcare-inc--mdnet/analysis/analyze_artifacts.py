#!/usr/bin/env python3
"""Analyze all downloaded artifacts for the Enable Healthcare MDnet EHI export."""

import json
import os
import subprocess

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/enable-healthcare-inc--mdnet/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/enable-healthcare-inc--mdnet/analysis"

def analyze_pdf():
    """Extract and analyze the EHI Export Guide PDF."""
    pdf_path = os.path.join(DOWNLOADS, "EHI_DATA_EXPort_GUIDE.pdf")
    info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
    text = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True).stdout

    # Count pages, words
    lines = text.strip().split('\n')
    words = len(text.split())

    # Extract C-CDA sections listed in the document
    ccda_sections = []
    in_sections = False
    for line in lines:
        stripped = line.strip()
        if "Allergy" in stripped and "Encounters" not in stripped and in_sections == False:
            in_sections = True
        if in_sections:
            # Roman numeral prefixed lines
            for prefix in ["i.", "ii.", "iii.", "iv.", "v.", "vi.", "vii.", "viii.", "ix.", "x.",
                           "xi.", "xii.", "xiii.", "xiv.", "xv.", "xvi.", "xvii.", "xviii.", "xix.", "xx."]:
                if stripped.lower().startswith(prefix):
                    section_name = stripped[len(prefix):].strip()
                    if section_name and len(section_name) < 50:
                        ccda_sections.append(section_name)
            if "Clinical Instructions" in stripped:
                in_sections = False

    # Deduplicate (sections appear twice in doc)
    seen = set()
    unique_sections = []
    for s in ccda_sections:
        if s not in seen:
            seen.add(s)
            unique_sections.append(s)

    # Extract export methods
    export_methods = [
        "1. FHIR APIs (R4, 27 resource types via US Core)",
        "2. C-CDA R2.1 bulk or single export (20 clinical sections)",
        "3. CSV full data set export (health, activity, financial data)",
        "4. HL7 2.x/3.x ADT (demographics, payer updates)",
        "5. HL7 2.x SIU (appointment scheduling)",
        "6. HL7 2.x DFT (financial transactions — note: description is copy-paste of SIU)",
        "7. JSON-based exchange (scanned documents, faxes, BASE-64 encoded)",
        "8. EDI 837P and 835 (claims and remittance files)"
    ]

    return {
        "file": "EHI_DATA_EXPort_GUIDE.pdf",
        "pages": 9,
        "words": words,
        "lines": len(lines),
        "created": "2023-12-28",
        "author": "Rahul Dewan",
        "title": "DATA INTEROPERABILITY & EHI DATA EXPORT GUIDE",
        "export_methods": export_methods,
        "ccda_sections": unique_sections,
        "ccda_section_count": len(unique_sections),
        "data_dictionary_url": "https://emr.ehiconnect.com/docs/",
        "data_dictionary_accessible": False,
        "data_dictionary_http_status": 404
    }


def analyze_fhir_capability():
    """Analyze the FHIR CapabilityStatement."""
    cs_path = os.path.join(DOWNLOADS, "fhir-capability-statement.json")
    with open(cs_path) as f:
        cs = json.load(f)

    resources = []
    for r in cs.get("rest", [{}])[0].get("resource", []):
        rtype = r["type"]
        interactions = [i["code"] for i in r.get("interaction", [])]
        search_params = [p["name"] for p in r.get("searchParam", [])]
        resources.append({
            "type": rtype,
            "interactions": interactions,
            "search_params": search_params
        })

    return {
        "file": "fhir-capability-statement.json",
        "fhir_version": cs.get("fhirVersion", "unknown"),
        "software_name": cs.get("software", {}).get("name", "unknown"),
        "resource_count": len(resources),
        "resource_types": sorted([r["type"] for r in resources]),
        "resources_detail": resources
    }


def analyze_screenshots():
    """List and describe screenshot artifacts."""
    screenshots = []
    for f in os.listdir(DOWNLOADS):
        if f.endswith(".png"):
            size = os.path.getsize(os.path.join(DOWNLOADS, f))
            screenshots.append({"file": f, "size_bytes": size})
    return screenshots


if __name__ == "__main__":
    results = {
        "pdf_analysis": analyze_pdf(),
        "fhir_analysis": analyze_fhir_capability(),
        "screenshots": analyze_screenshots(),
        "total_artifacts": len(os.listdir(DOWNLOADS)),
        "artifact_list": sorted(os.listdir(DOWNLOADS))
    }

    output_path = os.path.join(OUTPUT, "artifact_analysis.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("=== Artifact Analysis Summary ===")
    print(f"Total artifacts: {results['total_artifacts']}")
    print(f"\nPDF: {results['pdf_analysis']['pages']} pages, {results['pdf_analysis']['words']} words")
    print(f"Created: {results['pdf_analysis']['created']}")
    print(f"Export methods described: {len(results['pdf_analysis']['export_methods'])}")
    print(f"C-CDA sections listed: {results['pdf_analysis']['ccda_section_count']}")
    print(f"Data dictionary URL accessible: {results['pdf_analysis']['data_dictionary_accessible']}")
    print(f"\nFHIR CapabilityStatement:")
    print(f"  Version: {results['fhir_analysis']['fhir_version']}")
    print(f"  Resource types: {results['fhir_analysis']['resource_count']}")
    print(f"  Resources: {', '.join(results['fhir_analysis']['resource_types'])}")
    print(f"\nC-CDA Sections:")
    for i, s in enumerate(results['pdf_analysis']['ccda_sections'], 1):
        print(f"  {i}. {s}")
    print(f"\nExport Methods:")
    for m in results['pdf_analysis']['export_methods']:
        print(f"  {m}")
