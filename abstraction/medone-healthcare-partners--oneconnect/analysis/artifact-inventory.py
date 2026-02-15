#!/usr/bin/env python3
"""Inventory all artifacts in the downloads directory and summarize findings."""

import json
import os
import subprocess

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/medone-healthcare-partners--oneconnect/downloads"
FILES_JSON = "/home/jmandel/hobby/ehi-export-analysis/results/medone-healthcare-partners--oneconnect/files.json"

def get_pdf_info(path):
    """Extract page count and metadata from a PDF."""
    result = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    info = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def get_pdf_text(path):
    """Extract full text from PDF."""
    result = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    return result.stdout

def main():
    # Load files manifest
    with open(FILES_JSON) as f:
        manifest = json.load(f)
    
    inventory = []
    
    for entry in os.listdir(DOWNLOADS):
        path = os.path.join(DOWNLOADS, entry)
        size = os.path.getsize(path)
        ext = os.path.splitext(entry)[1].lower()
        
        item = {
            "filename": entry,
            "size_bytes": size,
            "extension": ext,
        }
        
        if ext == ".pdf":
            info = get_pdf_info(path)
            item["pages"] = int(info.get("Pages", 0))
            item["title"] = info.get("Title", "")
            item["created"] = info.get("CreationDate", "")
            text = get_pdf_text(path)
            item["word_count"] = len(text.split())
            item["char_count"] = len(text)
        elif ext == ".json":
            with open(path) as f:
                data = json.load(f)
            item["type"] = data.get("resourceType", "unknown")
            if "entry" in data:
                item["entry_count"] = len(data["entry"])
        elif ext == ".png":
            item["type"] = "screenshot"
        
        inventory.append(item)
    
    # Print summary
    print("=" * 60)
    print("ARTIFACT INVENTORY")
    print("=" * 60)
    for item in sorted(inventory, key=lambda x: x["filename"]):
        print(f"\n{item['filename']}")
        print(f"  Size: {item['size_bytes']:,} bytes")
        if "pages" in item:
            print(f"  Pages: {item['pages']}")
            print(f"  Title: {item['title']}")
            print(f"  Word count: {item['word_count']}")
        if "type" in item:
            print(f"  Type: {item['type']}")
        if "entry_count" in item:
            print(f"  Entries: {item['entry_count']}")
    
    # EHI Export PDF analysis
    print("\n" + "=" * 60)
    print("EHI EXPORT PDF - FULL TEXT")
    print("=" * 60)
    ehi_text = get_pdf_text(os.path.join(DOWNLOADS, "EHI-Export.pdf"))
    print(ehi_text)
    
    # Count sentences in EHI export
    sentences = [s.strip() for s in ehi_text.replace("\n", " ").split(".") if s.strip()]
    print(f"\nSentence count: {len(sentences)}")
    
    # FHIR API - list resource types documented
    print("\n" + "=" * 60)
    print("FHIR API - RESOURCE TYPES DOCUMENTED")
    print("=" * 60)
    fhir_text = get_pdf_text(os.path.join(DOWNLOADS, "FHIR-API-Specifications.pdf"))
    resources = []
    for line in fhir_text.splitlines():
        if line.strip().startswith("Request"):
            cleaned = line.split("...")[0].strip()
            if cleaned and cleaned != "Request":
                resources.append(cleaned)
    for r in sorted(set(resources)):
        print(f"  {r}")
    print(f"\nTotal unique resource sections: {len(set(resources))}")
    
    # Save inventory as JSON
    output_path = os.path.join(os.path.dirname(__file__), "artifact-inventory.json")
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nInventory saved to {output_path}")

if __name__ == "__main__":
    main()
