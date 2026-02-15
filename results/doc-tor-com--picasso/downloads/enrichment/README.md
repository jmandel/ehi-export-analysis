# Enrichment: Picasso EHI Export Data Classes

## Run Command
```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/doc-tor-com--picasso/downloads/enrichment
bun run extract-data-classes.ts
```

## Input Boundary
Parses two PDF data dictionaries found in the parent `downloads/` directory:
- `Picasso-EHI-Export-Documentation-V1_0-1.pdf` — Picasso-specific EHI export (3 pages, CSV format, 21 data classes)
- `Picasso-EHI-Export-Documentation-V1_0-1-1.pdf` — Amazing Charts EHI export (8 pages, CSV/JSON/XML format, 44 data classes)

A third file (`PAA_API_documentation.pdf`) was noted but not structured, as it documents a USCDI/CCD-style API rather than the (b)(10) EHI export.

## Output Files
- `picasso-data-classes.json` — Structured extraction of the Picasso-specific data dictionary (21 data classes, ~441 columns)
- `amazing-charts-data-classes.json` — Structured extraction of the Amazing Charts data dictionary (44 data classes, ~1094 columns)
- `extraction-summary.json` — Accounting of files discovered, parsed, and any failures

## Known Parsing Limitations
- Data classes and columns were manually transcribed from pdftotext output because the PDF table structure is lost during text extraction. The pdftotext output merges class names and column headers when they span table rows.
- Column counts are exact per manual verification against the PDF.
- No data types, descriptions, or value sets are provided in the source PDFs — only column names.
- The "HM Rules" and "Immunizations" data classes in the Amazing Charts document share a merged row in the PDF; they are combined as "HM Rules / Immunizations" in the extraction.
