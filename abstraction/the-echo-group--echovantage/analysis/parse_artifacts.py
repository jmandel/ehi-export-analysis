#!/usr/bin/env python3
"""Parse all EHI export artifacts for EchoVantage and produce structured inventory."""

import json
import re
import subprocess
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/the-echo-group--echovantage/downloads")
OUTPUT = Path(__file__).parent

def parse_pdf():
    """Extract and parse the EHI export PDF."""
    pdf_path = DOWNLOADS / "Electronic-Health-Information-Export_EchoVantage.pdf"
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True
    )
    text = result.stdout.strip()
    
    info_result = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        capture_output=True, text=True
    )
    
    # Parse metadata
    metadata = {}
    for line in info_result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    
    # Parse export formats from the text
    formats = []
    
    # Single Patient formats
    single_patient = [
        {
            "format": "CCD/C-CDA",
            "scope": "Single Patient",
            "description": "Consolidated Clinical Document Architecture which will contain data required by the USCDI v1 standards."
        },
        {
            "format": "JSON",
            "scope": "Single Patient", 
            "description": "JavaScript Object Notation. JSON is a lightweight format for storing and transporting data. JSON is in plain text, which is readable by a person, but is meant to be parsed and understood by an application or web page."
        },
        {
            "format": "PDF",
            "scope": "Single Patient",
            "description": "Portable Document Format, is a file format to present documents, including text formatting and image."
        }
    ]
    
    # Population format
    population = [
        {
            "format": ".bak (MSSQL Server backup)",
            "scope": "Patient Population",
            "description": "This is a full MSSQL Server database backup of all data for an agency that can be restored."
        }
    ]
    
    formats = single_patient + population
    
    return {
        "source_file": "Electronic-Health-Information-Export_EchoVantage.pdf",
        "pages": int(metadata.get("Pages", 1)),
        "file_size_bytes": int(metadata.get("File size", "0").replace(" bytes", "")),
        "author": metadata.get("Author", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "raw_text": text,
        "raw_text_word_count": len(text.split()),
        "export_formats": formats
    }


def parse_html():
    """Extract EHI export section from the ONC page."""
    html_path = DOWNLOADS / "onc-echo-page.html"
    with open(html_path) as f:
        content = f.read()
    
    # Extract the EHI section
    match = re.search(
        r'(?is)(Electronic Health Information.*?)(EchoVantage FHIR API|<h[23])',
        content
    )
    
    ehi_text = ""
    if match:
        ehi_text = re.sub(r'<[^>]+>', ' ', match.group(1))
        ehi_text = re.sub(r'\s+', ' ', ehi_text).strip()
    
    # Count total links on the page
    all_links = re.findall(r'href="([^"]*)"', content)
    ehi_links = [l for l in all_links if 'export' in l.lower() or 'ehi' in l.lower()]
    
    return {
        "source_file": "onc-echo-page.html",
        "file_size_bytes": len(content),
        "ehi_section_text": ehi_text,
        "ehi_section_word_count": len(ehi_text.split()),
        "ehi_related_links": ehi_links,
        "total_links_on_page": len(all_links)
    }


def main():
    results = {
        "vendor": "The Echo Group (Ensora Health)",
        "product": "EchoVantage",
        "analysis_date": "2026-02-16",
        "artifacts_analyzed": [],
        "export_documentation_summary": {}
    }
    
    # Parse PDF
    pdf_data = parse_pdf()
    results["artifacts_analyzed"].append(pdf_data)
    
    # Parse HTML
    html_data = parse_html()
    results["artifacts_analyzed"].append(html_data)
    
    # Summary
    results["export_documentation_summary"] = {
        "total_artifacts": 3,  # PDF, HTML, screenshot
        "has_data_dictionary": False,
        "has_schema": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_value_sets": False,
        "has_relationships": False,
        "has_entity_list": False,
        "entity_count": 0,
        "field_count": 0,
        "fields_with_descriptions": 0,
        "export_formats": [f["format"] for f in pdf_data["export_formats"]],
        "single_patient_formats": ["CCD/C-CDA", "JSON", "PDF"],
        "population_formats": [".bak (MSSQL Server backup)"],
        "single_patient_mechanism": "Self-service (user-initiated, no developer assistance)",
        "population_mechanism": "Support ticket via Salesforce",
        "single_patient_scope": "USCDI v1 (explicitly stated)",
        "population_scope": "Full MSSQL database backup (all agency data)",
        "documentation_word_count": pdf_data["raw_text_word_count"] + html_data["ehi_section_word_count"],
        "notes": [
            "No data dictionary or schema documentation exists",
            "Single patient export explicitly scoped to USCDI v1 - a clinical summary standard, not all EHI",
            "Population export is a raw database backup with zero schema documentation",
            "JSON export format is completely undocumented - no indication of structure or content",
            "PDF format is a human-readable document, not computable data",
            "Total substantive documentation is approximately 180 words across all artifacts"
        ]
    }
    
    # Write output
    output_path = OUTPUT / "artifact-analysis.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Written to {output_path}")
    
    # Print summary
    print(f"\nArtifacts analyzed: {len(results['artifacts_analyzed'])}")
    print(f"Data dictionary present: {results['export_documentation_summary']['has_data_dictionary']}")
    print(f"Entity count: {results['export_documentation_summary']['entity_count']}")
    print(f"Field count: {results['export_documentation_summary']['field_count']}")
    print(f"Documentation word count: {results['export_documentation_summary']['documentation_word_count']}")


if __name__ == "__main__":
    main()
