#!/usr/bin/env python3
"""Analyze Claimpower EHI export PDF artifacts.
Extracts text, counts pages, and summarizes content of each PDF."""

import subprocess
import json
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')

results = []
for fname in sorted(os.listdir(DOWNLOADS)):
    if not fname.upper().endswith('.PDF'):
        continue
    fpath = os.path.join(DOWNLOADS, fname)
    
    # Get page count
    info = subprocess.run(['pdfinfo', fpath], capture_output=True, text=True)
    pages = 0
    for line in info.stdout.splitlines():
        if line.startswith('Pages:'):
            pages = int(line.split(':')[1].strip())
    
    # Get text content
    text = subprocess.run(['pdftotext', '-layout', fpath, '-'], capture_output=True, text=True)
    text_content = text.stdout.strip()
    word_count = len(text_content.split())
    
    # Check for data dictionary indicators
    has_table_header = any(kw in text_content.lower() for kw in ['field name', 'column', 'data type', 'description', 'schema'])
    has_ccda_ref = 'ccda' in text_content.lower() or 'c-cda' in text_content.lower()
    has_screenshots = 'step' in text_content.lower() and '→' in text_content
    
    results.append({
        'filename': fname,
        'pages': pages,
        'word_count': word_count,
        'size_bytes': os.path.getsize(fpath),
        'has_data_dictionary_indicators': has_table_header,
        'references_ccda': has_ccda_ref,
        'is_screenshot_walkthrough': has_screenshots,
        'text_preview': text_content[:300]
    })

# Summary
print("=== Claimpower EHI Export PDF Analysis ===\n")
total_pages = sum(r['pages'] for r in results)
print(f"Total PDFs: {len(results)}")
print(f"Total pages: {total_pages}")
print(f"Any data dictionary content: {any(r['has_data_dictionary_indicators'] for r in results)}")
print(f"All reference C-CDA: {all(r['references_ccda'] for r in results)}")
print(f"All screenshot walkthroughs: {all(r['is_screenshot_walkthrough'] for r in results)}")
print()

for r in results:
    print(f"  {r['filename']}: {r['pages']} pages, {r['word_count']} words, {'screenshot walkthrough' if r['is_screenshot_walkthrough'] else 'other'}")

# Save detailed results
output_path = os.path.join(os.path.dirname(__file__), 'pdf-analysis-output.json')
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nDetailed results saved to {output_path}")
