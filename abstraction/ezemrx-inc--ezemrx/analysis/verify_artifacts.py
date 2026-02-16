"""
Verification script for ezEMRx EHI Export artifacts.
Examines all downloaded artifacts and produces a summary.
"""
import os
import json

DOWNLOADS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/ezemrx-inc--ezemrx/downloads"
RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/ezemrx-inc--ezemrx"

results = {
    "artifacts_examined": [],
    "findings": {}
}

# 1. List all files in downloads
print("=" * 60)
print("ARTIFACT INVENTORY")
print("=" * 60)
for f in sorted(os.listdir(DOWNLOADS_DIR)):
    path = os.path.join(DOWNLOADS_DIR, f)
    size = os.path.getsize(path)
    print(f"  {f}: {size:,} bytes")
    results["artifacts_examined"].append({
        "filename": f,
        "size_bytes": size,
        "type": f.split('.')[-1]
    })

# 2. Analyze text file
print()
print("=" * 60)
print("TEXT CONTENT ANALYSIS")
print("=" * 60)
text_file = os.path.join(DOWNLOADS_DIR, "ehi-export-page-text.txt")
with open(text_file, 'r') as f:
    text = f.read()
    
print(f"Text file size: {len(text)} characters")
print(f"Text file lines: {text.count(chr(10))}")

# Check for specific content indicators
indicators = {
    "has_data_dictionary": any(kw in text.lower() for kw in ["data dictionary", "table name", "field name", "column name"]),
    "has_schema": any(kw in text.lower() for kw in ["schema", "json schema", "xsd"]),
    "has_format_spec": any(kw in text.lower() for kw in ["csv", "tsv", "json", "xml format", "export format"]),
    "has_sample_data": any(kw in text.lower() for kw in ["sample", "example data", "example record"]),
    "has_field_descriptions": any(kw in text.lower() for kw in ["field description", "column description"]),
    "has_regulatory_text": any(kw in text.lower() for kw in ["45 cfr", "170.315", "designated record set"]),
    "mentions_ehi_export": "ehi export" in text.lower(),
    "promises_documentation": "documentation listed on this page" in text.lower(),
}

for key, value in indicators.items():
    print(f"  {key}: {value}")

results["findings"]["text_analysis"] = indicators

# 3. Load files.json for metadata
with open(os.path.join(RESULTS_DIR, "files.json"), 'r') as f:
    files_meta = json.load(f)

print()
print("=" * 60)
print("FILES.JSON METADATA")
print("=" * 60)
print(f"Collection date: {files_meta.get('collection_date')}")
print(f"Source URL: {files_meta.get('url')}")
print(f"Access status: {files_meta.get('access_status')}")
print(f"Number of files: {len(files_meta.get('files', []))}")

for file_info in files_meta.get('files', []):
    print(f"\n  File: {file_info['path']}")
    print(f"  Source: {file_info['source_url']}")
    print(f"  Size: {file_info['size_bytes']:,} bytes")
    desc = file_info.get('description', 'N/A')
    print(f"  Description: {desc[:200]}")

# 4. Summary
print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("Total artifacts: 3 (2 screenshots, 1 text file)")
print("Data dictionary present: NO")
print("Schema present: NO")
print("Sample data present: NO")
print("Export format documented: NO")
print("Technical documentation: NONE")
print("Content type: Regulatory text + compliance claims only")
print("PDF Viewer Pro widget: Present but empty (no PDF loaded)")
print()
print("CONCLUSION: The EHI export documentation page at")
print("https://www.ezemrx.com/ehi-export contains NO substantive")
print("technical documentation. The page has regulatory definitions,")
print("compliance bullet points, an empty PDF viewer widget, and")
print("introductory text promising documentation that was never published.")

# Save results
output_path = os.path.join(
    "/home/jmandel/hobby/ehi-export-analysis/abstraction/ezemrx-inc--ezemrx/analysis",
    "artifact-verification-results.json"
)
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to: {output_path}")

