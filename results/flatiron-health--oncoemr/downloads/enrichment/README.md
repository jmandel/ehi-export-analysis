# Enrichment: Flatiron Health EHI Data Dictionary

## Run Command

```bash
bun run extract-data-dictionary.ts
```

## Input

- `../ehi-data-dictionary.pdf` — 63-page PDF data dictionary (400 KB), title "EHI data dictionary v1.0", created from Google Sheets, last modified 9/9/2025.

## Output Files

- `data-dictionary.json` — Complete structured extraction of all tables and columns from the PDF. Contains export format metadata, table definitions with descriptions, and column-level detail (name, type, nullable, description).
- `coverage-summary.json` — Tables categorized by clinical/billing data domain, with summary statistics.

## Extraction Method

Uses `pdftotext -layout` to preserve the tabular structure, then parses the fixed-width layout to extract TableName, ColumnName, Type, Nullable, and Description columns. Handles multi-line descriptions, repeated headers across pages, and PARTITION_NAMESPACE entries (lowercase table name variants).

## Known Parsing Limitations

- 5 columns (out of 2689) have empty descriptions — these are typically system-managed fields or continuation artifacts
- 4 columns have null nullable values — due to layout wrapping edge cases
- Some table descriptions may have minor text artifacts from PDF column alignment
- The `CDG_EnrollmentData_History` table is categorized under clinical_notes_documents but could also be considered insurance/enrollment
