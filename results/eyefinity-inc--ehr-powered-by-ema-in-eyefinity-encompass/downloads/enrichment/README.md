# Enrichment: ModMed EMA EHI Export Data Dictionary

## Run command

```bash
# Prerequisite: extract text from PDF (only needed once)
pdftotext ../Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf ../Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt

# Run extraction
cd downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input boundary

- Single file: `../Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt`
  (plain-text extraction of the 131-page PDF via `pdftotext`)

## Output files

| File | Description |
|------|-------------|
| `data-dictionary.json` | Array of table definitions: grouping, table_name, description, columns[], longitudinal_tracking |
| `coverage-summary.json` | Accounting: total tables/columns, per-grouping breakdown, parse notes |

## Known parsing limitations

- The PDF is a single large table rendered across 131 pages. `pdftotext` interleaves
  text from the Description and Columns visual columns on the same line. The parser
  uses snake_case pattern matching to separate column names from description prose,
  which catches ~99% of cases but may occasionally misclassify a column name that
  looks like an English word (e.g., `status`, `name`, `type` — these ARE valid column
  names and are kept; obviously wrong ones like `information`, `table` are filtered).
- Three groupings declared in the PDF intro (Lookup, MIPS, Medical Lookup) have no
  table entries in the actual data dictionary — these are noted as "declared but empty."
- Column-level data types, field lengths, and value sets are NOT present in this PDF
  (the data dictionary only has: grouping, table name, description, column names,
  and longitudinal tracking flag).
