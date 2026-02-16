#!/usr/bin/env python3
"""
Analyze ezEMRx EHI export artifacts.

Since no data dictionary or structured documentation exists for this vendor,
this script simply inventories the available artifacts and confirms the absence
of any parseable export documentation.
"""

import json
import os
from pathlib import Path

DOWNLOADS_DIR = Path(__file__).parent.parent / "downloads"
ANALYSIS_DIR = Path(__file__).parent

def analyze_artifacts():
    """Inventory all downloaded artifacts and assess content."""
    artifacts = []
    for f in sorted(DOWNLOADS_DIR.iterdir()):
        if f.is_file():
            info = {
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "extension": f.suffix,
            }
            if f.suffix == ".txt":
                text = f.read_text(encoding="utf-8", errors="replace")
                info["line_count"] = len(text.splitlines())
                info["char_count"] = len(text)
                # Check for any structured data indicators
                info["has_table_markers"] = any(
                    marker in text.lower()
                    for marker in ["field", "column", "table", "entity", "schema", "type"]
                )
                info["has_format_markers"] = any(
                    marker in text.lower()
                    for marker in ["csv", "tsv", "json", "fhir", "c-cda", "xml", "sql"]
                )
            elif f.suffix == ".png":
                info["type"] = "screenshot"
            artifacts.append(info)

    return artifacts


def generate_summary():
    """Generate the summary inventory files."""
    artifacts = analyze_artifacts()

    # Check the text file for any structured content
    text_file = DOWNLOADS_DIR / "ehi-export-page-text.txt"
    text_content = text_file.read_text(encoding="utf-8") if text_file.exists() else ""

    # Count keywords that might indicate documentation
    doc_keywords = [
        "field", "column", "table", "entity", "schema", "type",
        "integer", "varchar", "string", "boolean", "date",
        "primary key", "foreign key", "csv", "tsv", "json",
        "fhir", "c-cda", "xml", "sql"
    ]
    keyword_hits = {kw: text_content.lower().count(kw) for kw in doc_keywords if kw in text_content.lower()}

    full_inventory = {
        "product": "ezEMRx",
        "vendor": "ezEMRx Inc",
        "analysis_date": "2026-02-16",
        "source": "https://www.ezemrx.com/ehi-export",
        "extraction_notes": (
            "No data dictionary, schema, sample data, or any structured export "
            "documentation exists. The page contains only regulatory text and an "
            "empty PDF viewer widget placeholder."
        ),
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "parse_errors": [],
        "artifacts_examined": artifacts,
        "documentation_keyword_scan": keyword_hits if keyword_hits else "No technical keywords found in page text",
    }

    summary = {
        "product": "ezEMRx",
        "vendor": "ezEMRx Inc",
        "analysis_date": "2026-02-16",
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "pct_fields_with_descriptions": None,
        "categories": [],
        "artifacts_count": len(artifacts),
        "artifacts_with_structured_data": 0,
        "notes": (
            "No data dictionary or export documentation exists. The vendor's EHI "
            "export page contains only regulatory boilerplate and an empty PDF "
            "viewer widget."
        ),
    }

    # Write outputs
    with open(ANALYSIS_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)

    with open(ANALYSIS_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("=== ezEMRx EHI Export Artifact Analysis ===")
    print(f"Artifacts found: {len(artifacts)}")
    for a in artifacts:
        print(f"  - {a['filename']} ({a['size_bytes']} bytes, {a['extension']})")
    print(f"\nEntities/tables documented: 0")
    print(f"Fields documented: 0")
    print(f"Technical keywords in page text: {len(keyword_hits)}")
    if keyword_hits:
        for kw, count in keyword_hits.items():
            print(f"  - '{kw}': {count} occurrences")
    else:
        print("  (none found)")
    print(f"\nConclusion: No export documentation exists to parse.")


if __name__ == "__main__":
    generate_summary()
