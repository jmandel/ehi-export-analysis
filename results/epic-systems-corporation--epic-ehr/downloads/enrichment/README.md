# Epic EHI Tables Enrichment

## Run commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/epic-systems-corporation--epic-ehr/downloads/enrichment
bun run extract-ehi-tables.ts
```

## Input boundary

Parses all `.htm` files (excluding `_index.htm`) from the extracted ZIP at:
`../ehi-tables-extracted/DocGen_su117s2p_2026-02-15_14.10.04/`

Source ZIP: `../ehi-tables-index.zip` downloaded from https://open.epic.com/EHITables/Download

## Output files

- **`ehi-tables.json`** — Array of table definitions, each containing:
  - `table_name`: Table identifier
  - `source_file`: Original `.htm` filename
  - `description`: Table-level description
  - `primary_key`: Array of `{name, ordinal_position}`
  - `columns`: Array of `{ordinal, name, type, discontinued, description}`

- **`extraction-coverage.json`** — Parsing statistics:
  - File counts (discovered, parsed, failed)
  - Table/column counts with description coverage
  - Column type distribution

## Results (2026-02-16)

- 7,672 tables parsed, 0 failures
- 63,121 total columns
- 100% description coverage (tables and columns)
- Column types: VARCHAR (32,660), NUMERIC (12,596), INTEGER (10,154),
  DATETIME (3,686), FLOAT (1,502), DATETIME UTC/Local/Attached variants

## Known parsing limitations

- Cheerio-based parsing; relies on consistent HTML class names (`Header2`,
  `KeyValue`, `SubHeader3`, `List`, `SubList`). If Epic changes their doc
  generator's CSS class names, the parser would need updating.
- Encoding artifacts: some descriptions contain `�` (UTF-8 mojibake for
  curly quotes/apostrophes from the source HTML's cp1252 encoding).
- Does not extract cross-table foreign key relationships (these are
  sometimes mentioned in column descriptions but not structurally encoded).
