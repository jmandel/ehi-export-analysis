# OpenEMR EHI Export Documentation Enrichment

## Run Commands

```bash
cd enrichment
bun run extract-schema.ts
bun run extract-html-comments.ts
```

## Input Boundary

### extract-schema.ts
- **Input**: `../openemr.openemr.xml` — SchemaSpy XML export of the OpenEMR database schema
- **Output**: `schema.json` (full structured schema), `coverage.json` (parsing accounting)

### extract-html-comments.ts
- **Input**: `../tables/*.html` — 318 SchemaSpy-generated HTML table documentation pages
- **Output**: `html-comments.json` (table/column comments from HTML), `html-coverage.json` (parsing accounting)

## Output Files

| File | Description |
|------|-------------|
| `schema.json` | Complete database schema: 322 tables, 4941 columns, with types, relationships, indexes, and remarks |
| `coverage.json` | Parsing statistics for XML extraction |
| `html-comments.json` | Column-level comments extracted from HTML pages (captures 3125+ comments not present in XML) |
| `html-coverage.json` | Parsing statistics for HTML extraction |

## Known Parsing Limitations

- The XML parser uses regex-based extraction rather than a proper XML parser. It handles all structures in the SchemaSpy output but is not a general-purpose XML parser.
- The HTML column extractor matches the specific 6-column table row layout used by SchemaSpy. If the SchemaSpy version changes its HTML output format, this script may need updating.
- 4 tables in the XML lack column definitions (appear as self-closing `<table/>` tags). These are tables with 0 rows and 0 columns in the schema.
- HTML extraction finds 4489 columns vs XML's 4941 — the difference is due to SchemaSpy HTML rendering choices (some tables are rendered differently or the regex doesn't match variant layouts).
