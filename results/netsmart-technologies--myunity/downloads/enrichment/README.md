# myUnity EHI Export Data Dictionary Enrichment

## Run Command

```bash
bun run extract-data-dictionary.ts
```

## Input

- `../ehi_export_all_files_myunity_fall_2024.pdf` — 64-page PDF data dictionary
- Text extraction via `pdftotext` (poppler-utils)

## Output Files

- `data-dictionary.json` — Structured JSON with all 23 export files and their field definitions (404 fields total)
- `coverage-accounting.json` — Extraction statistics and notes

## Known Parsing Limitations

- `pdftotext` sometimes merges separator lines with the first field name (e.g., `-------------Name: PatientSys`); the parser handles this explicitly
- Multi-line field descriptions are concatenated; line breaks within descriptions may not be perfectly preserved
- The CCD file lists C-CDA sections rather than individual fields (it exports an XML CCD document)
- The Attachments file has no field definitions — it exports raw files (pdf, doc, jpg, etc.)
- Page numbers embedded in the text are filtered out but occasionally may be adjacent to content
