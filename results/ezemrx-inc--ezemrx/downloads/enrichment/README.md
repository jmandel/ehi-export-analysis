# ezEMRx EHI Export Data Dictionary Enrichment

## Run Command

```bash
bun run extract-data-dictionary.ts
```

## Input Boundary

Parses one file from `../`:

| File | Description |
|------|-------------|
| `ehi-export-data-dictionary.pdf` | 9-page EHI Export data dictionary (v2.0, April 2024) |

## Output Files

- `data-dictionary.json` — Structured extraction of file categories, CSV column
  schemas, file naming conventions, and metadata.

## Structure

The PDF documents 4 export file categories:

1. **Patient Demographics and Clinical Data** — C-CDA R2.1 XML+HTML pairs
2. **Patient Billing and Claims Data** — CSV (17 columns)
3. **Adhoc Patient Notes** — CSV (7 columns)
4. **Scanned Records** — CDA XML with Base64-encoded documents

## Known Parsing Limitations

- The PDF is only 9 pages with simple prose structure (no complex tables that
  need layout-aware parsing). Column definitions were extracted manually into
  the script rather than parsed heuristically, since the PDF table layout is
  inconsistent (duplicate column numbers, varying whitespace).
- The PDF references HL7 C-CDA R2.1 for clinical data and scanned records but
  provides no field-level detail for those categories — only the CSV files have
  column-level documentation.
