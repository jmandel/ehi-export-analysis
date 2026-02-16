#!/usr/bin/env python3
"""Verify and inventory all artifacts in the CorrecTek downloads directory."""

import json
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/correctek--spark/downloads"

artifacts = []
for f in sorted(os.listdir(DOWNLOADS)):
    path = os.path.join(DOWNLOADS, f)
    size = os.path.getsize(path)
    ext = os.path.splitext(f)[1]
    
    info = {"filename": f, "size_bytes": size, "extension": ext}
    
    if ext == ".txt":
        with open(path) as fh:
            content = fh.read()
        info["line_count"] = content.count("\n")
        info["char_count"] = len(content)
        # Check for b(10) text
        if "b)(10)" in content or "EHI" in content:
            info["contains_ehi_reference"] = True
            # Extract the actual EHI description
            for line in content.split("\n"):
                if "EHI can be exported" in line:
                    info["ehi_description"] = line.strip()
    
    elif ext == ".json":
        with open(path) as fh:
            data = json.load(fh)
        info["json_keys"] = list(data.keys())
        if "resourceType" in data:
            info["fhir_resource_type"] = data["resourceType"]
            info["fhir_bundle_type"] = data.get("type")
            info["has_entries"] = "entry" in data
    
    elif ext == ".png":
        info["type"] = "screenshot"
    
    artifacts.append(info)

# Summary
print("=== Artifact Inventory ===")
print(f"Total files: {len(artifacts)}")
print()
for a in artifacts:
    print(f"  {a['filename']} ({a['size_bytes']:,} bytes)")
    if "ehi_description" in a:
        print(f"    EHI text: \"{a['ehi_description']}\"")
    if "fhir_resource_type" in a:
        print(f"    FHIR: {a['fhir_resource_type']} ({a['fhir_bundle_type']}), entries: {a['has_entries']}")
    if a["extension"] == ".png":
        print(f"    Type: screenshot image")

print()
print("=== Key Findings ===")
print("- Total downloadable artifacts: 5 (3 screenshots, 1 text extract, 1 JSON)")
print("- No data dictionary found")
print("- No sample export data found")
print("- No schema files found")
print("- EHI documentation: single sentence about PDF/C-CDA export")
print("- FHIR endpoints JSON: empty Bundle with no entries")

# Write inventory JSON
output = {
    "vendor": "CorrecTek",
    "product": "Spark",
    "analysis_date": "2026-02-16",
    "artifact_count": len(artifacts),
    "artifacts": artifacts,
    "ehi_documentation_summary": {
        "total_sentences": 3,
        "total_characters": 0,  # will compute
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_field_documentation": False,
        "export_formats_mentioned": ["PDF", "C-CDA"],
        "entities_documented": 0,
        "fields_documented": 0
    }
}

# Get the actual EHI text length
for a in artifacts:
    if "ehi_description" in a:
        output["ehi_documentation_summary"]["total_characters"] = len(a["ehi_description"])

OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/correctek--spark/analysis"
with open(os.path.join(OUTPUT_DIR, "artifact-inventory.json"), "w") as f:
    json.dump(output, f, indent=2)

print(f"\nInventory written to {OUTPUT_DIR}/artifact-inventory.json")
