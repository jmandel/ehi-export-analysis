# Enrichment: NextGen Enterprise EHI Data Dictionary

## Run Commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/nextgen-healthcare--nextgen-enterprise-ehr/downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input Boundary

- Source: `../DD_Complete_EHI_20250627.pdf` (29 MB, 10,875 pages)
- Intermediate: `dd-raw.txt` — pdftotext plain-text extraction

## Output Files

- **`data-dictionary.json`** — Array of table objects, each with `table` name and `columns` array containing `{ name, dataType, default, notNull }`. 5,290 tables, 283,279 columns.
- **`summary.json`** — Extraction statistics and sample tables.

## Known Parsing Limitations

- The PDF contains only column names, SQL Server data types, defaults, and not-null indicators — no field descriptions, value sets, or relationship/FK documentation.
- `notNull` is always `false` because pdftotext cannot reliably extract checkbox state from the PDF.
- Default value assignment may occasionally misalign if the PDF layout varies.
- Some column names with special characters or spaces may be missed by the `[a-zA-Z_][a-zA-Z0-9_]*` regex.
- 1,386 columns (0.5%) lack a data type, likely due to parsing edge cases at page boundaries.
