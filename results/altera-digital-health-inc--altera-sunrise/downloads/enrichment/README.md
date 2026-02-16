# Enrichment: Sunrise EHI WebERDiagram Extraction

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/altera-digital-health-inc--altera-sunrise/downloads/enrichment
bun run extract-tables.ts
```

## Input Boundary

Parses all `Tbl_*.htm` files (excluding `*_Attr.htm` companion files) from the
extracted PR38 Weber diagram archive:

```
extracted/pr38-weberdiagram/EHI WebERDiagram 22.1 PR38/
├── FS WebERDiagram 22.1 PR38/Content/   (Financial System - 1 table)
├── IMG WebERDiagram 22.1 PR38/Content/  (Imaging - 7 tables)
├── MNC WebERDiagram 22.1 PR38/Content/  (Medical Necessity - 11 tables)
└── SCM WebERDiagram 22.1 PR38/Content/  (Sunrise Clinical Manager - 2728 tables)
```

## Output Files

| File | Description |
|------|-------------|
| `tables.json` | Full extraction: all tables with columns, definitions, keys, data types, PKs |
| `tables-summary.csv` | One row per table: schema, name, definition, column count, has_pk |
| `columns.csv` | One row per column: schema, table, column name, datatype, nullable, isPK, definition |

## Coverage

- **2,747 tables** discovered and parsed
- **42,849 columns** extracted
- **0 parse failures**
- All 4 schemas (FS, IMG, MNC, SCM) included

## Known Parsing Limitations

- Relationship data between tables is not extracted (the `Submodel_*_Rel.htm`
  files in PR38 are empty — no FK relationships were documented by the vendor).
- The `Tbl_*_Attr.htm` companion files contain additional column-level detail
  (extended definitions). These are not parsed separately since the summary table
  pages already include the column definition text.
- Domain references (e.g., "HVCIDdt") appear in the Domain column but the
  domain definitions themselves (`DD_*_Domains.htm`) are not cross-referenced.
