#!/usr/bin/env python3
"""
Extract and catalog all artifacts from the MedNet Medical Solutions emr4MD
EHI export documentation. Produces:
  - artifact-inventory.json: catalog of all downloaded files with metadata
  - full-entity-inventory.json: parsed FHIR resource types from API docs (the
    only structured data available, as no b(10) data dictionary exists)
  - summary-stats.json: aggregate statistics
"""

import json
import os
import subprocess
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent.parent.parent / "results" / "mednet-medical-solutions--emr4md" / "downloads"
OUTPUT = Path(__file__).resolve().parent

def get_pdf_info(pdf_path):
    """Extract PDF metadata via pdfinfo."""
    try:
        result = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
        info = {}
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                info[k.strip()] = v.strip()
        return info
    except Exception as e:
        return {"error": str(e)}

def extract_pdf_text(pdf_path):
    """Extract text from PDF."""
    try:
        result = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def count_html_elements(html_path):
    """Count key HTML elements."""
    try:
        text = html_path.read_text(errors='replace')
        return {
            "size_bytes": html_path.stat().st_size,
            "lines": text.count("\n"),
            "tables": text.lower().count("<table"),
            "links": text.lower().count("<a "),
            "headings": sum(text.lower().count(f"<h{i}") for i in range(1,7)),
        }
    except Exception as e:
        return {"error": str(e)}

def parse_enrichment_data():
    """Parse the enrichment JSON for FHIR resource details."""
    enrichment_path = DOWNLOADS / "enrichment" / "api-documentation-extracted.json"
    if not enrichment_path.exists():
        return None
    with open(enrichment_path) as f:
        return json.load(f)

def build_artifact_inventory():
    """Build complete inventory of all downloaded artifacts."""
    files_json = DOWNLOADS.parent / "files.json"
    with open(files_json) as f:
        manifest = json.load(f)

    artifacts = []
    for file_entry in manifest.get("files", []):
        fpath = DOWNLOADS.parent / file_entry["path"]
        artifact = {
            "path": file_entry["path"],
            "source_url": file_entry.get("source_url"),
            "description": file_entry.get("description"),
            "size_bytes": file_entry.get("size_bytes"),
            "exists": fpath.exists(),
        }
        if fpath.exists():
            if fpath.suffix == ".pdf":
                artifact["pdf_info"] = get_pdf_info(fpath)
                artifact["type"] = "pdf"
            elif fpath.suffix == ".html":
                artifact["html_stats"] = count_html_elements(fpath)
                artifact["type"] = "html"
            elif fpath.suffix == ".json":
                artifact["type"] = "json"
            elif fpath.suffix in (".ts", ".md"):
                artifact["type"] = fpath.suffix[1:]
        artifacts.append(artifact)
    return artifacts

def build_entity_inventory(enrichment_data):
    """
    Build the full entity inventory from available structured data.
    Since there is no b(10) data dictionary, we document what IS available:
    the FHIR API resource types from interopengine docs and the single
    EHI export entry from the price transparency PDF.
    """
    inventory = {
        "note": "No b(10) EHI export data dictionary or schema exists. This inventory documents the only structured data available: FHIR API resources from g(7)/g(9)/g(10) docs and the single EHI export description from the Price Transparency PDF.",
        "ehi_export_documentation": {
            "source": "Price_Transparency_emr4MD_v9.10.pdf",
            "criteria": "170.315(b)(10)",
            "description": "This functionality allows a practice to create individual and group exports of PHI without programming intervention.",
            "cost": "Included in base service agreement, subscription fee plus Subscription fee from 3rd party - EMR Direct, one time implementation fee and annual subscription charged.",
            "format": "unknown",
            "data_dictionary": None,
            "schema": None,
            "sample_data": None,
            "field_definitions": None,
            "entities": None,
            "total_fields": None,
        },
        "fhir_api_resources": {},
    }

    if enrichment_data:
        for api_version in enrichment_data.get("apiVersions", []):
            version_name = api_version.get("version", "unknown")
            fhir_version = api_version.get("fhirVersion", "unknown")
            resources = api_version.get("resources", [])

            # Deduplicate resource types
            resource_types = {}
            for r in resources:
                rt = r.get("resourceType", "unknown")
                if rt not in resource_types:
                    resource_types[rt] = {
                        "resourceType": rt,
                        "ccdsElements": [],
                        "dataElements": [],
                    }
                ccds = r.get("ccdsElement")
                if ccds and ccds not in resource_types[rt]["ccdsElements"]:
                    resource_types[rt]["ccdsElements"].append(ccds)
                de = r.get("dataElement")
                if de and de not in resource_types[rt]["dataElements"]:
                    resource_types[rt]["dataElements"].append(de)

            inventory["fhir_api_resources"][version_name] = {
                "fhirVersion": fhir_version,
                "totalResourceTypes": len(resource_types),
                "resources": list(resource_types.values()),
                "relevance_to_b10": "NOT relevant - this is g(7)/g(9)/g(10) API documentation, not b(10) EHI export",
            }

    return inventory

def build_summary_stats(artifacts, entity_inventory):
    """Compute summary statistics."""
    stats = {
        "total_artifacts": len(artifacts),
        "artifact_types": {},
        "total_size_bytes": 0,
        "ehi_export_specific_artifacts": 0,
        "ehi_export_data_dictionary": False,
        "ehi_export_schema": False,
        "ehi_export_sample_data": False,
        "ehi_export_format_documented": False,
        "ehi_export_field_count": 0,
        "ehi_export_entity_count": 0,
        "fhir_api_2017_resource_types": 0,
        "fhir_api_2026_resource_types": 0,
    }

    for a in artifacts:
        t = a.get("type", "unknown")
        stats["artifact_types"][t] = stats["artifact_types"].get(t, 0) + 1
        stats["total_size_bytes"] += a.get("size_bytes", 0) or 0

    for version_name, version_data in entity_inventory.get("fhir_api_resources", {}).items():
        if "2017" in version_name:
            stats["fhir_api_2017_resource_types"] = version_data["totalResourceTypes"]
        elif "2026" in version_name:
            stats["fhir_api_2026_resource_types"] = version_data["totalResourceTypes"]

    # The only b(10)-specific artifact is the one sentence in the Price Transparency PDF
    stats["ehi_export_specific_artifacts"] = 1  # Just the PDF sentence

    return stats


if __name__ == "__main__":
    print("Building artifact inventory...")
    artifacts = build_artifact_inventory()
    with open(OUTPUT / "artifact-inventory.json", "w") as f:
        json.dump(artifacts, f, indent=2)
    print(f"  {len(artifacts)} artifacts cataloged")

    print("Parsing enrichment data...")
    enrichment = parse_enrichment_data()

    print("Building entity inventory...")
    entity_inventory = build_entity_inventory(enrichment)
    with open(OUTPUT / "full-entity-inventory.json", "w") as f:
        json.dump(entity_inventory, f, indent=2)

    print("Computing summary stats...")
    stats = build_summary_stats(artifacts, entity_inventory)
    with open(OUTPUT / "summary-stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Stats: {json.dumps(stats, indent=2)}")

    print("Done.")
