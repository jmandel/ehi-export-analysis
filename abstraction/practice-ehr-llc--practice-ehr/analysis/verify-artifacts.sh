#!/bin/bash
# Script to verify and document all artifacts in the Practice EHR downloads folder
# Produces hard numbers for the analysis

DOWNLOADS="/home/jmandel/hobby/ehi-export-analysis/results/practice-ehr-llc--practice-ehr/downloads"

echo "=== Artifact Inventory ==="
echo ""

echo "--- PDF: Practice-EHR-B10-Electronic-Health-Information-Export.pdf ---"
pdfinfo "$DOWNLOADS/Practice-EHR-B10-Electronic-Health-Information-Export.pdf"
echo ""
echo "Text content (word count):"
pdftotext -layout "$DOWNLOADS/Practice-EHR-B10-Electronic-Health-Information-Export.pdf" - | wc -w
echo ""
echo "Text content (line count, excluding blank lines):"
pdftotext -layout "$DOWNLOADS/Practice-EHR-B10-Electronic-Health-Information-Export.pdf" - | grep -c '[^ ]'
echo ""

echo "--- Screenshot: data-export-page.png ---"
file "$DOWNLOADS/data-export-page.png"
identify "$DOWNLOADS/data-export-page.png" 2>/dev/null || echo "(identify not available)"
echo "Size: $(stat -c %s "$DOWNLOADS/data-export-page.png") bytes"
echo ""

echo "=== Summary ==="
echo "Total files: $(ls -1 "$DOWNLOADS" | wc -l)"
echo "Total size: $(du -sh "$DOWNLOADS" | cut -f1)"
echo ""

echo "=== PDF Full Text ==="
pdftotext -layout "$DOWNLOADS/Practice-EHR-B10-Electronic-Health-Information-Export.pdf" -
