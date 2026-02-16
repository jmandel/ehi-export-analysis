#!/usr/bin/env python3
"""
Analyze all downloaded artifacts for Ulrich Medical Concepts / Team Chart Concept
EHI export documentation assessment.

Parses:
- cost-disclosure-and-transparency.html (the disclosure page)
- fhirR4endpoints-umc.json (FHIR endpoint directory)
- interopengine-open-api-documentation.html (API docs)
- 2025 RWT Plan and Results PDFs (fetched separately)

Outputs: artifact_analysis.json with structured findings
"""
import json
import re
import os
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/ulrich-medical-concepts--team-chart-concept/downloads"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

results = {
    "product": "Team Chart Concept (TCC)",
    "vendor": "Ulrich Medical Concepts",
    "chpl_id": "15.05.05.3049.UL15.01.00.1.191226",
    "chpl_number": 10227,
    "artifacts": [],
    "ehi_export_documentation": {},
    "data_dictionary": None,
    "sample_data": None,
    "schema": None,
}

# 1. Analyze disclosure page HTML
html_path = os.path.join(DOWNLOADS, "cost-disclosure-and-transparency.html")
with open(html_path, "r") as f:
    html_content = f.read()

# Extract the EHI footnote
ehi_match = re.search(r'\*EHI can be exported.*?(?=<div|<\/)', html_content, re.DOTALL)
ehi_text = ""
if ehi_match:
    ehi_text = re.sub(r'<[^>]+>', '', ehi_match.group(0)).strip()

# Count certification criteria listed
criteria_matches = re.findall(r'§170\.315\s*\([a-z]\)\(\d+\)', html_content)
criteria_list = list(set(criteria_matches))

results["artifacts"].append({
    "file": "cost-disclosure-and-transparency.html",
    "type": "HTML",
    "size_bytes": os.path.getsize(html_path),
    "description": "Mandatory ONC disclosure and transparency page",
    "ehi_relevant": True,
    "contains_data_dictionary": False,
    "contains_sample_data": False,
    "certification_criteria_count": len(criteria_list),
    "ehi_footnote_text": ehi_text,
    "ehi_footnote_word_count": len(ehi_text.split()) if ehi_text else 0,
})

results["ehi_export_documentation"] = {
    "source": "Single footnote on disclosure page",
    "full_text": ehi_text,
    "word_count": len(ehi_text.split()) if ehi_text else 0,
    "format_described": "PDF or C-CDA",
    "mechanism_described": "Chart export routine, files saved to user-specified folder",
    "data_dictionary_provided": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "field_listing_provided": False,
    "user_guide_provided": False,
    "what_is_included": "Not specified - 'Records for a patient' with no further detail",
    "what_is_excluded": "Not specified",
}

# 2. Analyze FHIR endpoints JSON
fhir_path = os.path.join(DOWNLOADS, "fhirR4endpoints-umc.json")
with open(fhir_path, "r") as f:
    fhir_data = json.load(f)

has_entries = "entry" in fhir_data and len(fhir_data.get("entry", [])) > 0

results["artifacts"].append({
    "file": "fhirR4endpoints-umc.json",
    "type": "JSON",
    "size_bytes": os.path.getsize(fhir_path),
    "description": "FHIR R4 endpoint directory for UMC customers",
    "ehi_relevant": False,
    "resource_type": fhir_data.get("resourceType"),
    "has_entries": has_entries,
    "entry_count": len(fhir_data.get("entry", [])),
    "note": "Empty bundle - no active FHIR integrations"
})

# 3. Analyze InteropEngine API docs
interop_path = os.path.join(DOWNLOADS, "interopengine-open-api-documentation.html")
with open(interop_path, "r") as f:
    interop_content = f.read()

# Check for any EHI/b10 references
has_ehi_ref = bool(re.search(r'EHI|b\)\(10\)|Electronic Health Information', interop_content, re.IGNORECASE))
has_bulk_data = bool(re.search(r'bulk\s*data', interop_content, re.IGNORECASE))

# Count headings to estimate doc structure
headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', interop_content, re.DOTALL)
heading_texts = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]

results["artifacts"].append({
    "file": "interopengine-open-api-documentation.html",
    "type": "HTML",
    "size_bytes": os.path.getsize(interop_path),
    "description": "EMR Direct Interoperability Engine Open API Documentation (g)(10)",
    "ehi_relevant": False,
    "references_ehi_export": has_ehi_ref,
    "references_bulk_data": has_bulk_data,
    "section_count": len(heading_texts),
    "note": "Generic (g)(10) FHIR API docs from EMR Direct, not specific to UMC or (b)(10)"
})

# 4. Screenshot
png_path = os.path.join(DOWNLOADS, "cost-disclosure-and-transparency-page.png")
results["artifacts"].append({
    "file": "cost-disclosure-and-transparency-page.png",
    "type": "PNG",
    "size_bytes": os.path.getsize(png_path),
    "description": "Full-page screenshot of disclosure page",
    "ehi_relevant": True,
    "note": "Visual confirmation of page layout and content"
})

# Summary
results["summary"] = {
    "total_artifacts": len(results["artifacts"]),
    "ehi_relevant_artifacts": sum(1 for a in results["artifacts"] if a.get("ehi_relevant")),
    "artifacts_with_data_dictionary": 0,
    "artifacts_with_sample_data": 0,
    "artifacts_with_schema": 0,
    "total_entities_documented": 0,
    "total_fields_documented": 0,
    "ehi_documentation_word_count": results["ehi_export_documentation"]["word_count"],
    "export_formats": ["PDF", "C-CDA"],
    "has_native_data_model_export": False,
    "is_standard_projection": True,
    "classification": "Minimal/stub",
}

output_path = os.path.join(OUTPUT_DIR, "artifact_analysis.json")
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Analysis complete. Output: {output_path}")
print(f"Total artifacts: {results['summary']['total_artifacts']}")
print(f"EHI-relevant artifacts: {results['summary']['ehi_relevant_artifacts']}")
print(f"EHI documentation: {results['summary']['ehi_documentation_word_count']} words (entire footnote)")
print(f"Data dictionary: None")
print(f"Sample data: None")
print(f"Schema: None")
print(f"Export formats: {', '.join(results['summary']['export_formats'])}")
print(f"Classification: {results['summary']['classification']}")
