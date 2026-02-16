"""
Analyze all artifacts in the TenEleven eCR EHI export downloads directory.
Produces a structured JSON inventory of what was found and key metrics.
"""
import json
import os
import subprocess

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/teneleven-group--electronic-clinical-record-ecr/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/teneleven-group--electronic-clinical-record-ecr/analysis"

def analyze_pdf(path):
    """Extract metadata and text from a PDF."""
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    return {
        "metadata": info.strip(),
        "text": text.strip(),
        "text_length_chars": len(text.strip()),
        "text_length_words": len(text.strip().split()),
    }

def analyze_image(path):
    """Get basic image info."""
    size = os.path.getsize(path)
    return {"size_bytes": size}

results = {
    "analysis_date": "2026-02-16",
    "artifacts": [],
    "summary": {}
}

for fname in sorted(os.listdir(DOWNLOADS)):
    fpath = os.path.join(DOWNLOADS, fname)
    size = os.path.getsize(fpath)
    artifact = {
        "filename": fname,
        "size_bytes": size,
        "type": None,
        "details": {}
    }

    if fname.endswith(".pdf"):
        artifact["type"] = "PDF"
        artifact["details"] = analyze_pdf(fpath)
    elif fname.endswith(".png"):
        artifact["type"] = "screenshot"
        artifact["details"] = analyze_image(fpath)
    else:
        artifact["type"] = "unknown"

    results["artifacts"].append(artifact)

# Summary statistics
results["summary"] = {
    "total_artifacts": len(results["artifacts"]),
    "pdfs": sum(1 for a in results["artifacts"] if a["type"] == "PDF"),
    "screenshots": sum(1 for a in results["artifacts"] if a["type"] == "screenshot"),
    "total_size_bytes": sum(a["size_bytes"] for a in results["artifacts"]),
    "data_dictionary_present": False,
    "sample_data_present": False,
    "schema_present": False,
    "entities_documented": 0,
    "fields_documented": 0,
    "export_formats": ["JSON (single patient)", ".bak SQL Server backup (population)"],
    "documentation_artifacts": 1,  # just the 1-page PDF
    "documentation_total_words": sum(
        a["details"].get("text_length_words", 0)
        for a in results["artifacts"]
        if a["type"] == "PDF"
    ),
}

out_path = os.path.join(OUTPUT_DIR, "artifact-inventory.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results["summary"], indent=2))
print(f"\nFull inventory saved to {out_path}")
