#!/usr/bin/env python3
"""
Analyze SPAC EHI export documentation artifacts.

This product has extremely minimal documentation — a single 1-page PDF with 6 sentences.
This script extracts and verifies the PDF content and produces summary artifacts.
"""

import json
import subprocess
import os

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(os.path.dirname(WORK_DIR), "downloads")

def analyze_pdf():
    """Extract and analyze the sole documentation artifact."""
    pdf_path = os.path.join(DOWNLOADS, "SPAC-Export.pdf")
    
    # Get PDF metadata
    info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True)
    info_lines = info.stdout.strip().split("\n")
    metadata = {}
    for line in info_lines:
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    
    # Extract text
    text = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    full_text = text.stdout.strip()
    
    # Count sentences (rough)
    sentences = [s.strip() for s in full_text.replace("\n", " ").split(".") if s.strip()]
    
    # Count words
    words = full_text.split()
    
    results = {
        "artifact": "SPAC-Export.pdf",
        "pages": int(metadata.get("Pages", 0)),
        "file_size_bytes": int(metadata.get("File size", "0").replace(" bytes", "")),
        "created": metadata.get("CreationDate", ""),
        "modified": metadata.get("ModDate", ""),
        "producer": metadata.get("Producer", ""),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "full_text": full_text,
        "key_claims": [
            "Export contains data from patient's chart",
            "Multiple file formats used",
            "Export is a ZIP file",
            "Contains C-CDA documents and PDF attachments",
            "C-CDAs are in nested ZIP archives",
            "One C-CDA per patient encounter",
        ],
        "what_is_missing": [
            "No data dictionary",
            "No field-level documentation",
            "No C-CDA section specification",
            "No schema or profile reference",
            "No sample data",
            "No export instructions (UI/API)",
            "No description of PDF attachment types",
            "No value sets or code systems",
            "No relationship documentation",
        ]
    }
    
    return results

def main():
    results = analyze_pdf()
    
    output_path = os.path.join(WORK_DIR, "pdf-analysis-output.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"PDF Analysis Results:")
    print(f"  Pages: {results['pages']}")
    print(f"  Words: {results['word_count']}")
    print(f"  Sentences: ~{results['sentence_count']}")
    print(f"  Key claims extracted: {len(results['key_claims'])}")
    print(f"  Documentation gaps: {len(results['what_is_missing'])}")
    print(f"\nFull text:")
    print(results['full_text'])
    print(f"\nOutput saved to: {output_path}")

if __name__ == "__main__":
    main()
