#!/bin/bash
# Script to inventory and verify all artifacts in the CorrecTek downloads folder
# Produces a summary of what was collected and key facts about each file

DOWNLOADS="/home/jmandel/hobby/ehi-export-analysis/results/correctek--spark/downloads"

echo "=== Artifact Inventory ==="
echo ""
echo "Files in downloads/:"
ls -la "$DOWNLOADS/"
echo ""

echo "=== File contents summary ==="
echo ""

echo "--- cost-disclosure-page-text.txt ---"
echo "Size: $(wc -c < "$DOWNLOADS/cost-disclosure-page-text.txt") bytes"
echo "Lines: $(wc -l < "$DOWNLOADS/cost-disclosure-page-text.txt")"
echo ""
echo "b(10) text extracted:"
grep -A2 "b)(10)" "$DOWNLOADS/cost-disclosure-page-text.txt"
echo ""

echo "--- fhirR4endpoints-umc.json ---"
echo "Size: $(wc -c < "$DOWNLOADS/fhirR4endpoints-umc.json") bytes"
echo "Content:"
cat "$DOWNLOADS/fhirR4endpoints-umc.json"
echo ""
echo ""

echo "--- Screenshots ---"
for f in screenshot-ehi-section.png screenshot-ehi-text.png screenshot-full-page.png; do
  echo "$f: $(wc -c < "$DOWNLOADS/$f") bytes"
done
echo ""

echo "=== Key findings ==="
echo "Total artifacts: $(ls "$DOWNLOADS/" | wc -l)"
echo "Documentation files (text/JSON): 2"
echo "Screenshots: 3"
echo "Data dictionaries: 0"
echo "Sample data files: 0"
echo "Schema files: 0"
echo "PDF documentation: 0"
