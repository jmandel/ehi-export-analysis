"""
Analyze all artifacts in the Office Practicum EHI export downloads folder.
Produces hard counts and inventory for the analysis.
"""
import os
import json
import re
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/office-practicum--office-practicum/downloads")
RESULTS = Path("/home/jmandel/hobby/ehi-export-analysis/results/office-practicum--office-practicum")

# 1. Inventory of all downloaded files
print("=" * 60)
print("ARTIFACT INVENTORY")
print("=" * 60)
files = sorted(DOWNLOADS.iterdir())
for f in files:
    size_kb = f.stat().st_size / 1024
    print(f"  {f.name:50s} {size_kb:8.1f} KB")

# 2. Parse files.json for source URLs
print("\n" + "=" * 60)
print("SOURCE URLS")
print("=" * 60)
with open(RESULTS / "files.json") as fj:
    manifest = json.load(fj)
for entry in manifest["files"]:
    print(f"  {entry['path']:55s} <- {entry.get('source_url', 'N/A')}")

# 3. Extract EHI export text from HTML
print("\n" + "=" * 60)
print("EHI EXPORT DOCUMENTATION TEXT (from onc-certification-page.html)")
print("=" * 60)
html = (DOWNLOADS / "onc-certification-page.html").read_text(errors="ignore")

# Find the EHI section
ehi_match = re.search(
    r'Electronic Health Information Export.*?</div>',
    html, re.DOTALL | re.IGNORECASE
)
if ehi_match:
    raw = ehi_match.group()
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = re.sub(r'\s+', ' ', text).strip()
    word_count = len(text.split())
    print(f"  Word count: {word_count}")
    print(f"  Text:\n  {text}")
else:
    print("  EHI section not found!")

# 4. Check for any linked documents (PDFs, ZIPs, XLSX, etc.)
print("\n" + "=" * 60)
print("LINKED DOCUMENTS IN HTML PAGES")
print("=" * 60)
for html_file in ["onc-certification-page.html", "onc-certification-info-disclosures.html"]:
    content = (DOWNLOADS / html_file).read_text(errors="ignore")
    links = re.findall(r'href="([^"]*(?:\.pdf|\.zip|\.xlsx|\.csv|\.json|\.xml)[^"]*)"', content, re.IGNORECASE)
    # Filter out common non-EHI links
    ehi_links = [l for l in links if not any(x in l.lower() for x in ['font', 'style', 'script', 'icon', 'transparency'])]
    if ehi_links:
        print(f"  {html_file}:")
        for l in ehi_links:
            print(f"    -> {l}")
    else:
        print(f"  {html_file}: No document links found (excluding style/transparency)")

# 5. Summary statistics
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Total artifacts downloaded: {len(files)}")
print(f"  HTML pages: {len([f for f in files if f.suffix == '.html'])}")
print(f"  PDFs: {len([f for f in files if f.suffix == '.pdf'])}")
print(f"  Screenshots: {len([f for f in files if f.suffix == '.png'])}")
print(f"  Data dictionaries: 0")
print(f"  Sample data files: 0")
print(f"  Schema files: 0")
print(f"  Entities/tables documented: 0")
print(f"  Fields documented: 0")
