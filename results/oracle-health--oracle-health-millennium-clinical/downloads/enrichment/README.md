# Oracle Health Millennium Data Model Enrichment

## Run Commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/oracle-health--oracle-health-millennium-clinical/downloads/enrichment
bun run extract-mysql-model.ts
```

## Input Boundary

Parses all `dms_*.html` files from the extracted MySQL data model ZIP:
`../mysql-model/html/dms_*.html` (1,422 files)

These files are the Millennium Production Data Model Reports (version 2025.4.01)
extracted from `EHI MYSQL DATA MODEL 2025401.zip`, which was inside
`single-patient-ehi-export-data-format-specifications.zip` downloaded from
https://www.oracle.com/health/certified-health-it/

## Output Files

| File | Description |
|------|-------------|
| `mysql-model-tables.json` | All tables with columns, types, definitions, subject areas. ~6,600 tables, ~129,000 columns. |
| `mysql-model-coverage.json` | Extraction accounting: files discovered, parsed, failures, subject area summary. |

## Known Parsing Limitations

- The Oracle data model ZIP (`EHI ORACLE DATA MODEL 2025401.zip`) uses the same
  HTML structure but targets Oracle DB types. Only the MySQL model is parsed here
  since the two are structurally identical (same tables, different type names).
- Table descriptions that span multiple HTML elements may lose some formatting.
- Foreign key relationships are implied via column definitions (e.g., "Foreign key
  to X table") but not extracted as a separate relationship graph.
- The `dms_pft_*` (Patient Financial Transaction) pages use the same structure
  as clinical pages and are parsed correctly.
