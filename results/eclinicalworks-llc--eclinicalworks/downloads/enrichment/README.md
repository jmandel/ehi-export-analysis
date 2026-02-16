# Enrichment: eClinicalWorks EHI Export Schema

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/eclinicalworks-llc--eclinicalworks/downloads/enrichment
bun run extract-tables.ts
```

## Input Boundary

- **Source files**: `../tables/*.html` — 1466 HTML files, each documenting one database table from the eClinicalWorks EHI Export Schema
- **Index page**: `../tableindex.html` — master index listing all table names with links

## Output Files

- **`tables.json`** — Array of 1466 table definitions. Each entry contains:
  - `name`: Table name
  - `description`: Human-readable table description
  - `columns`: Array of column definitions (name, dataType, description)
  - `sourceFile`: Relative path to source HTML file
- **`summary.json`** — Coverage/accounting stats: total files discovered, parsed, failures, column counts

## Known Parsing Limitations

- Two HTML formats exist in the corpus: a class-based format (majority) and an inline-style format (11 `ip_rh_*` files). Both are handled.
- The inline-style format has malformed HTML (`" !important;">` outside style attributes); the parser accommodates this.
- Column descriptions are extracted as plain text; any embedded HTML formatting is stripped.
