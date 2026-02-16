# CareLogic EHI Export Data Dictionary — Enrichment

## Run command

```bash
cd downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input boundary

- `../CareLogic_EHI_Export_Data_Dictionary.xls` — single-sheet Excel workbook
  (Composite Document File V2, 987,648 bytes, created 2025-11-07, last saved 2025-11-17)

## Output files

| File | Description |
|------|-------------|
| `data-dictionary.json` | Full structured extraction: 671 tables, 8,441 columns. Each table has name, description, domain category, and an array of columns with name, description, and data_type. |
| `coverage-report.json` | Parsing statistics: row counts, tables with no columns or descriptions, domain categorization summary with table counts per domain. |

## Known parsing limitations

- The XLS uses a two-level structure (table rows with name + description in
  columns A–B, column rows with name + description + data type in columns C–E).
  3 tables have 0 columns parsed (empty table definitions in the source).
- 5 tables have no description in the source file.
- Domain categorization is heuristic based on table name prefixes. 96 tables
  fall into "Other / Uncategorized" — these are mostly additional MOD_ assessment
  tables, state-specific tables, and miscellaneous tables not matching any
  explicit pattern.
- The data_type field is present for column rows only when column E has data.
  Most columns do have Oracle data types (NUMBER, VARCHAR2, TIMESTAMP, etc.).
