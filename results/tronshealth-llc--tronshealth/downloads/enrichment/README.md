# TronsHealth EHI Export Data Dictionary Enrichment

## Run command
```bash
bun run extract-data-dictionary.ts
```

## Input boundary
Single PDF file: `../170.315b10-Electronic-Health-Information-Export-EHI.pdf` (27 pages, 739KB)

## Output files
- `data-dictionary.json` — Structured JSON with all entities and fields extracted from the PDF data dictionary tables
- `extraction-stats.json` — Summary statistics: entity counts, field counts, missing sections

## Approach
Uses `pdftotext -layout` to preserve spatial column alignment from the PDF tables, then parses Field / Data Type / Detail columns using regex patterns that match the column-separated layout.

## Known limitations
- The PDF itself is **truncated**: the Table of Contents references sections 3.15 (Provider Note, page 27) and 3.18 (Encounter, page 32) but the document only has 27 pages with page 27 blank. These sections are missing from the extraction.
- Some field names from the PDF contain OCR/rendering artifacts like `f` ligature splits (e.g., "Suf f ixLookupID" instead of "SuffixLookupID"). These are preserved as-is from the PDF text layer.
- Multi-line field names that span across page breaks may not be fully captured.
- The Documents & Images entity has a single synthetic "Document" field since it has no field table in the PDF.
