#!/bin/bash
# Parse ZoomMD EHI Export Format Specification PDF
# Extracts text and metadata from the sole documentation artifact

PDF="../downloads/ZoomMD_EHI_Export_Format_Specification.pdf"

echo "=== PDF Metadata ==="
pdfinfo "$PDF"

echo ""
echo "=== Full Text Extraction ==="
pdftotext -layout "$PDF" -

echo ""
echo "=== Analysis ==="
TEXT=$(pdftotext -layout "$PDF" -)
echo "Total lines: $(echo "$TEXT" | wc -l)"
echo "Total words: $(echo "$TEXT" | wc -w)"
echo "Contains 'data dictionary': $(echo "$TEXT" | grep -ci 'data dictionary')"
echo "Contains 'field': $(echo "$TEXT" | grep -ci 'field')"
echo "Contains 'schema': $(echo "$TEXT" | grep -ci 'schema')"
echo "Contains 'table': $(echo "$TEXT" | grep -ci 'table')"
echo "Contains 'billing': $(echo "$TEXT" | grep -ci 'billing')"
echo "Contains 'insurance': $(echo "$TEXT" | grep -ci 'insurance')"
echo "Contains 'C-CDA': $(echo "$TEXT" | grep -ci 'c-cda')"
echo "Contains 'FHIR': $(echo "$TEXT" | grep -ci 'fhir')"
echo "Contains 'USCDI': $(echo "$TEXT" | grep -ci 'uscdi')"
