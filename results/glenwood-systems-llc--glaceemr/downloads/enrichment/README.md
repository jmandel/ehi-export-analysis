# GlaceEMR Data Dictionary Enrichment

## Run Command

```bash
bun run extract-data-dictionary.ts
```

## Input Boundary

- `data-dictionary.txt` — pdftotext output of `GlaceEMR Export Data Dictionary.pdf` (62 pages, 783 KB PDF)
- Generated via: `pdftotext "GlaceEMR Export Data Dictionary.pdf" data-dictionary.txt`

## Output Files

- `data-dictionary.json` — structured JSON containing all 42 documented CSV file schemas with 820 total columns, including data types, descriptions, possible values, primary/foreign key relationships, and cross-file references.

## Structure

The JSON contains:
- Document metadata (version, release date, author)
- Export folder structure (EMR, PMS, Documents, Photos, Reference)
- File listings for EMR (31 files) and PMS (11 files) folders
- Detailed column-level schemas for all 42 CSV files
- Extraction statistics

## Known Parsing Limitations

- The schemas were constructed by human reading of the PDF rather than automated table extraction, because pdftotext output of tabular data is unreliable for structured parsing. The script encodes the schemas directly from thorough reading of all 62 pages.
- The `data-dictionary.txt` intermediate file is included for reference/verification.
- Some columns in the PDF have ambiguous descriptions or empty Description/Comments cells; these are faithfully represented as empty strings.
- The "Reference" folder mentioned in the PDF (described as "Contains the schema of the Exported file content") has no further detail in the document.
