#!/usr/bin/env python3
"""Parse all Criterions EHI export artifacts and produce structured inventory."""

import json
import subprocess
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/criterions-software-inc--criterions-ehr/downloads"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_pdf_text(path):
    result = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    return result.stdout

def get_pdf_info(path):
    result = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def parse_ehi_overview(text):
    """Extract the 22 C-CDA sections listed in the EHI overview PDF."""
    sections = []
    in_list = False
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("•"):
            in_list = True
            section_name = line.lstrip("•").strip()
            sections.append(section_name)
        elif in_list and not line:
            continue
    return sections

def parse_mandatory_disclosure_capabilities(text):
    """Extract capability entries from mandatory disclosure PDF."""
    entries = []
    current_cap = None
    current_desc_lines = []
    
    for line in text.split("\n"):
        stripped = line.strip()
        # Detect capability lines starting with 170.315 or §170.315
        if stripped.startswith("170.315") or stripped.startswith("§170.315"):
            if current_cap:
                entries.append({
                    "capability": current_cap,
                    "description": " ".join(current_desc_lines).strip()
                })
            # Extract the capability identifier
            parts = stripped.split(None, 1)
            if len(parts) > 0:
                # Find the capability code and name
                cap_code = parts[0].lstrip("§")
                current_cap = stripped
                current_desc_lines = []
        elif current_cap and stripped and not stripped.startswith("Capability"):
            # Accumulate description lines (stop at cost section)
            if "This capability requires" not in stripped and "Training and implementation" not in stripped:
                current_desc_lines.append(stripped)
    
    if current_cap:
        entries.append({
            "capability": current_cap,
            "description": " ".join(current_desc_lines).strip()
        })
    
    return entries

# Process all artifacts
artifacts = []

# 1. Patient EHI Data Export Overview
ehi_path = os.path.join(DOWNLOADS, "Patient-EHI-Data-Export-Overview.pdf")
ehi_info = get_pdf_info(ehi_path)
ehi_text = extract_pdf_text(ehi_path)
ccda_sections = parse_ehi_overview(ehi_text)

artifacts.append({
    "file": "Patient-EHI-Data-Export-Overview.pdf",
    "type": "PDF",
    "pages": int(ehi_info.get("Pages", 0)),
    "size_bytes": os.path.getsize(ehi_path),
    "created": ehi_info.get("CreationDate", ""),
    "author": ehi_info.get("Author", ""),
    "content_type": "Patient-facing EHI export overview",
    "ccda_sections_listed": ccda_sections,
    "ccda_section_count": len(ccda_sections),
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False
})

# 2. 2022 CURES Disclosures
cures_path = os.path.join(DOWNLOADS, "2022-CURES-DISCLOSURES.pdf")
cures_info = get_pdf_info(cures_path)
cures_text = extract_pdf_text(cures_path)

artifacts.append({
    "file": "2022-CURES-DISCLOSURES.pdf",
    "type": "PDF",
    "pages": int(cures_info.get("Pages", 0)),
    "size_bytes": os.path.getsize(cures_path),
    "created": cures_info.get("CreationDate", ""),
    "author": cures_info.get("Author", ""),
    "content_type": "Cures Act disclosures (MFA + EHI)",
    "ehi_section_text": "The Criterions EHR allows customers to export industry-standard patient information in XML format using CCDA architecture and our Email/Print Chart functionality. Exports can be performed without intervention from programming or Criterions Software, Inc and without charge for individual patients, groups of patients, or automated scheduled export.",
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False
})

# 3. Mandatory Disclosure 2022
mand_path = os.path.join(DOWNLOADS, "MandatoryDisclosure2022.pdf")
mand_info = get_pdf_info(mand_path)
mand_text = extract_pdf_text(mand_path)
capabilities = parse_mandatory_disclosure_capabilities(mand_text)

# Find b(6) and b(10) entries
b6_entry = next((c for c in capabilities if "b)(6)" in c["capability"]), None)
b10_entry = next((c for c in capabilities if "b)(10)" in c["capability"]), None)

artifacts.append({
    "file": "MandatoryDisclosure2022.pdf",
    "type": "PDF",
    "pages": int(mand_info.get("Pages", 0)),
    "size_bytes": os.path.getsize(mand_path),
    "created": mand_info.get("CreationDate", ""),
    "author": mand_info.get("Author", ""),
    "content_type": "Mandatory disclosure table - all certified capabilities",
    "total_capabilities_listed": len(capabilities),
    "b6_description": b6_entry["description"] if b6_entry else None,
    "b10_description": b10_entry["description"] if b10_entry else None,
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False
})

# 4. Screenshot
screenshot_path = os.path.join(DOWNLOADS, "cures-disclosures-page-screenshot.png")
artifacts.append({
    "file": "cures-disclosures-page-screenshot.png",
    "type": "PNG",
    "pages": None,
    "size_bytes": os.path.getsize(screenshot_path),
    "content_type": "Screenshot of CHPL documentation landing page"
})

# Build the full entity inventory
# Since this is a C-CDA export with no data dictionary, we document what sections are listed
inventory = {
    "export_format": "C-CDA (XML)",
    "export_mechanism": "Email/Print Chart + CCDA download",
    "data_dictionary_provided": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "field_level_documentation": False,
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "ccda_sections": [
        {"name": s, "field_count": "N/A - no field-level documentation"} 
        for s in ccda_sections
    ],
    "ccda_section_count": len(ccda_sections),
    "note": "No data dictionary or field-level documentation was provided. The export documentation only lists 22 C-CDA section names without any field definitions, types, relationships, or value sets."
}

# Save outputs
with open(os.path.join(OUTPUT_DIR, "artifacts-summary.json"), "w") as f:
    json.dump(artifacts, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== Artifact Analysis Summary ===")
print(f"Total artifacts: {len(artifacts)}")
for a in artifacts:
    pages = f", {a.get('pages')} pages" if a.get('pages') else ""
    print(f"  - {a['file']} ({a['type']}{pages}, {a['size_bytes']:,} bytes)")

print(f"\n=== EHI Export Overview ===")
print(f"C-CDA sections listed: {len(ccda_sections)}")
for s in ccda_sections:
    print(f"  - {s}")

print(f"\n=== Mandatory Disclosure ===")
print(f"Total capabilities listed: {len(capabilities)}")
print(f"(b)(6) Data export: {b6_entry['description'][:100] if b6_entry else 'Not found'}...")
print(f"(b)(10) EHI export: {b10_entry['description'][:100] if b10_entry else 'Not found'}...")

print(f"\n=== Data Dictionary / Schema ===")
print("Data dictionary: NONE")
print("Field-level documentation: NONE")
print("Sample data: NONE")
print("Machine-readable schema: NONE")

print("\nOutputs saved to:")
print(f"  - {os.path.join(OUTPUT_DIR, 'artifacts-summary.json')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'full-entity-inventory.json')}")
