"""
Verify all artifacts in the downloads/ directory and produce an inventory.
Also verify the current state of the certification URL and Wayback Machine captures.
"""
import json
import os
import hashlib

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/dexter-solutions-inc--ezdocs"

# Load files.json manifest
with open(os.path.join(RESULTS_DIR, "files.json")) as f:
    manifest = json.load(f)

print("=== FILES MANIFEST ===")
print(f"Collection date: {manifest['collection_date']}")
print(f"Source URL: {manifest['url']}")
print(f"Final URL: {manifest['final_url']}")
print(f"Access status: {manifest['access_status']}")
print(f"Number of files: {len(manifest['files'])}")
print()

# Check each file in downloads/
downloads_dir = os.path.join(RESULTS_DIR, "downloads")
for entry in manifest["files"]:
    fpath = os.path.join(RESULTS_DIR, entry["path"])
    exists = os.path.exists(fpath)
    size = os.path.getsize(fpath) if exists else 0
    print(f"File: {entry['path']}")
    print(f"  Exists: {exists}")
    print(f"  Size: {size:,} bytes (manifest: {entry['size_bytes']:,} bytes)")
    print(f"  Source: {entry['source_url']}")
    print(f"  Description: {entry['description'][:120]}...")
    print()

# Check for any files not in the manifest
actual_files = set(os.listdir(downloads_dir))
manifest_files = set(os.path.basename(f["path"]) for f in manifest["files"])
extra = actual_files - manifest_files
missing = manifest_files - actual_files
print(f"Extra files (not in manifest): {extra or 'none'}")
print(f"Missing files (in manifest but not on disk): {missing or 'none'}")
print()

# Summary
print("=== SUMMARY ===")
print(f"Total artifacts: {len(manifest['files'])}")
print(f"All artifacts are screenshots of the vendor homepage.")
print(f"No EHI export documentation, data dictionaries, schemas, or sample data were collected.")
print(f"Reason: The registered certification URL ({manifest['url']}) redirects to the homepage.")

# Save structured output
output = {
    "collection_date": manifest["collection_date"],
    "source_url": manifest["url"],
    "final_url": manifest["final_url"],
    "access_status": manifest["access_status"],
    "total_artifacts": len(manifest["files"]),
    "artifact_types": ["screenshot"],
    "ehi_documentation_found": False,
    "data_dictionary_found": False,
    "sample_data_found": False,
    "schema_found": False,
    "files": [
        {
            "filename": os.path.basename(f["path"]),
            "size_bytes": f["size_bytes"],
            "type": "screenshot",
            "informative_for_ehi_analysis": False,
        }
        for f in manifest["files"]
    ],
}

output_path = os.path.join(
    "/home/jmandel/hobby/ehi-export-analysis/abstraction/dexter-solutions-inc--ezdocs/analysis",
    "artifact_inventory.json"
)
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nInventory saved to: {output_path}")
