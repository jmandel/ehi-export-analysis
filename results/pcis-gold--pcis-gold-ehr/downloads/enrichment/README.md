# PCIS GOLD EHI Export Data Dictionary — Enrichment

## Run command

```bash
cd results/pcis-gold--pcis-gold-ehr/downloads/enrichment
bun run extract-tables.ts
```

## Input boundary

Single file: `../ehi-export-data-table-definitions.html` (534 KB)
— the complete HTML page from https://fhir.pcisgold.com/ehiexport/

## Output files

| File | Description |
|------|-------------|
| `tables.json` | Full table + field definitions: 309 tables, 4,481 fields. Each entry has `name`, `anchor`, `description`, and `fields[]` with `name`, `type`, `description`. |
| `table-index.json` | Lightweight index: table name, description, field count. |
| `coverage-stats.json` | Parsing statistics: totals, failures, type distribution, domain categories. |

## Known parsing limitations

- One field (`T_PatientPortalMessages.InReplyTo`) has an empty type and description in the source HTML — carried through as-is.
- The source HTML uses two different naming conventions: legacy tables (e.g., `Accounts`, `Visits`) use abbreviated field names (e.g., `ACINST`, `ACCLNT`) while newer tables (prefixed `T_`) use descriptive names (e.g., `Id`, `LastName`). Both are parsed identically.
- Domain categorization in `coverage-stats.json` is heuristic based on table name prefixes and may miscategorize some tables.
