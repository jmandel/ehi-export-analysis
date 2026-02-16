# TheraOffice EHI Export — Enrichment

## Run command

```bash
bun run extract-tables.ts
```

Requires `pdftotext` (from poppler-utils) on PATH.

## Input boundary

- `../ehi_tables/EHI Export All Tables - May 2024 (TheraOffice).pdf` — the single
  PDF from the vendor's EHI export documentation ZIP.

## Output files

- **tables-catalog.json** — structured JSON with all 19 tables and 526 columns,
  including column names, SQL Server data types, and max lengths.
- **coverage-accounting.json** — parse statistics: tables expected vs parsed,
  columns documented vs parsed, any parse failures.

## Known parsing limitations

- The PDF uses a simple three-column layout (Name / Data type / Max length) with
  no field-level descriptions beyond what the glossary provides for common fields
  (Pat_ID, MODIFIED_USER, etc.). The script extracts column metadata but there are
  no per-column descriptions to extract.
- Value sets for coded fields (tinyint/smallint enums) are not documented in the
  PDF and therefore not present in the extracted JSON.
