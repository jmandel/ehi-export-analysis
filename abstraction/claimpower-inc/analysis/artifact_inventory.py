#!/usr/bin/env python3
"""
Inventory all artifacts in the ClaimPower downloads directory.
Extracts metadata (size, page count, text content) from each PDF.
Catalogs what data sections are visible in the C-CDA Summary of Care screenshots.
"""

import os
import subprocess
import json

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/claimpower-inc/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/claimpower-inc/analysis"

artifacts = []
for fname in sorted(os.listdir(DOWNLOADS)):
    fpath = os.path.join(DOWNLOADS, fname)
    size = os.path.getsize(fpath)
    info = {"filename": fname, "size_bytes": size}

    if fname.lower().endswith(".pdf"):
        # Get page count
        result = subprocess.run(
            ["pdfinfo", fpath], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("Pages:"):
                info["pages"] = int(line.split(":")[1].strip())
            if line.startswith("CreationDate:"):
                info["creation_date"] = line.split(":", 1)[1].strip()
            if line.startswith("Author:"):
                info["author"] = line.split(":", 1)[1].strip()

        # Get text length
        result = subprocess.run(
            ["pdftotext", "-layout", fpath, "-"], capture_output=True, text=True
        )
        info["text_chars"] = len(result.stdout)
        info["text_lines"] = len(result.stdout.splitlines())

    artifacts.append(info)

# Summary
print("=" * 70)
print("ARTIFACT INVENTORY")
print("=" * 70)
total_size = 0
total_pages = 0
for a in artifacts:
    total_size += a["size_bytes"]
    pages = a.get("pages", 0)
    total_pages += pages
    print(f"\n{a['filename']}")
    print(f"  Size: {a['size_bytes']:,} bytes ({a['size_bytes']/1024:.1f} KB)")
    if "pages" in a:
        print(f"  Pages: {a['pages']}")
        print(f"  Author: {a.get('author', 'N/A')}")
        print(f"  Created: {a.get('creation_date', 'N/A')}")
        print(f"  Text: {a['text_chars']:,} chars, {a['text_lines']} lines")

print(f"\n{'=' * 70}")
print(f"TOTALS: {len(artifacts)} files, {total_size:,} bytes, {total_pages} PDF pages")
print(f"{'=' * 70}")

# Document what the C-CDA Summary of Care shows (from screenshot analysis)
print("\n\nC-CDA SUMMARY OF CARE SECTIONS (from patient portal screenshot, page 8):")
sections = [
    "Patient Demographics",
    "Provider Details",
    "Patient Medical Documents",
    "Allergies",
    "Medications",
    "Problems",
    "Procedures",
    "Vital Signs",
    "Encounters",
    "Social History",
    "Family History",
    "Results (Discrete)",
]
for i, s in enumerate(sections, 1):
    print(f"  {i:2d}. {s}")
print(f"\nTotal visible C-CDA sections: {len(sections)}")

# Document the EMR Reports menu items (from screenshot, page 5)
print("\n\nEMR REPORTS MENU (from multi-patient export screenshot, page 5):")
reports = [
    "Ad Effectiveness Report",
    "Patients Processing Status",
    "Billing Sent Report",
    "Billing Stats Report",
    "Charts Created",
    "Checked In Patient Status",
    "Patient List",
    "Audit Report",
    "Public Health Surveillance Report",
    "Clinical Quality Measures Report",
    "Automated Measure Calculation Report",
    "Labs Filed Report",
    "Search Charts",
    "Export Patient Health Records",  # <-- The (b)(10) export
    "Insurance's Eligibility Status",
    "Daily Office Collection Report",
    "TCM Report",
    "RPM Report",
    "Re-Signed Chart Status Report",
]
for i, r in enumerate(reports, 1):
    marker = " <<<" if "Export" in r else ""
    print(f"  {i:2d}. {r}{marker}")

# Document EMR dashboard icons (from screenshot, page 2)
print("\n\nEMR DASHBOARD ICONS (from single patient export screenshot, page 2):")
icons = [
    "Patient Queue (3/3)",
    "Messages",
    "Notes",
    "ePrescribe/Refill/Medication Available",
    "Results",
    "Lookup Medical Records",
    "Charts",
    "Billing",
    "Immunizations",
    "Patient Registration",
    "Scheduling",
    "Census",
    "Speed Billing",
    "EMR Reports",
    "Attach Documents",
    "Settings",
    "Auditing/Medicare",
    "MIPS",
    "CCM List",
    "TCM List",
]
for i, icon in enumerate(icons, 1):
    print(f"  {i:2d}. {icon}")

# Save as JSON
output = {
    "artifacts": artifacts,
    "ccda_sections": sections,
    "emr_reports_menu": reports,
    "emr_dashboard_icons": icons,
}
with open(os.path.join(OUTPUT, "artifact_inventory.json"), "w") as f:
    json.dump(output, f, indent=2)

print(f"\n\nJSON saved to {os.path.join(OUTPUT, 'artifact_inventory.json')}")
