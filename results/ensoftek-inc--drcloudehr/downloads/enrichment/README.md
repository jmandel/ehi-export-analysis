# DrCloudEHR Schema Enrichment

## Run Commands

```bash
cd downloads/enrichment
bun run extract-schema.ts
```

## Input Boundary

Parses one file:
- `../drcloudehr.FHIR.xml` — SchemaSpy XML export of the DrCloudEHR (OpenEMR-derived)
  database schema, containing all 128 exported tables with column definitions,
  data types, remarks, and foreign key relationships.

## Output Files

- **`schema.json`** — Complete queryable JSON with all tables, columns
  (name, type, size, nullable, autoUpdated, defaultValue, remarks),
  parent/child relationships, primary keys, and indexes.
- **`coverage-report.json`** — Accounting: total tables, total columns,
  remark coverage percentages, parse failures.

## Known Parsing Limitations

- Uses regex-based XML parsing (no DOM parser). Handles both self-closing
  (`<column ... />`) and open/close (`<column ...>...</column>`) column
  elements, plus `<parent>` and `<child>` relationship refs.
- Attribute values containing `"` would break parsing (none present in this corpus).
- Index column references are parsed separately from data columns to avoid
  double-counting.
