"""
Inventory all artifacts in the downloads/ directory and extract key metrics.
Produces artifact-inventory.json with metadata for each file.
"""
import json
import os
import subprocess

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/claimpower-inc--claimpower-mobile-emr/downloads"
OUTPUT = os.path.join(os.path.dirname(__file__), "artifact-inventory.json")

artifacts = []
for fname in sorted(os.listdir(DOWNLOADS)):
    fpath = os.path.join(DOWNLOADS, fname)
    size = os.path.getsize(fpath)
    info = {"filename": fname, "size_bytes": size}
    
    if fname.upper().endswith(".PDF"):
        # Get page count
        result = subprocess.run(["pdfinfo", fpath], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("Pages:"):
                info["pages"] = int(line.split(":")[1].strip())
            if line.startswith("Author:"):
                info["author"] = line.split(":")[1].strip()
            if line.startswith("CreationDate:"):
                info["creation_date"] = line.split(":", 1)[1].strip()
        
        # Extract text and count words
        result = subprocess.run(["pdftotext", "-layout", fpath, "-"], capture_output=True, text=True)
        text = result.stdout
        info["word_count"] = len(text.split())
        info["has_substantive_text"] = len(text.strip()) > 100
    
    artifacts.append(info)

# Summary
total_pages = sum(a.get("pages", 0) for a in artifacts)
total_files = len(artifacts)

summary = {
    "total_files": total_files,
    "total_pdf_pages": total_pages,
    "artifacts": artifacts,
    "observations": [
        "All 4 files are PDFs containing screenshot walkthroughs of C-CDA export",
        "All created on same date (Aug 28, 2023) by Rohan Thadani (CEO)",
        "Main PDF (9 pages) contains all 3 sub-documents inline",
        "No data dictionary, schema, sample data, or technical documentation found",
        "Export format is exclusively C-CDA Summary of Care Records",
        "No evidence of billing, practice management, or custom data export"
    ]
}

with open(OUTPUT, "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
