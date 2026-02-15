# escribeHOST EHI Export Documentation — Enrichment

## Run command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/lille-group-inc--escribehost/downloads/enrichment
bun run extract-tables.ts
```

## Input boundary

- Single file: `../ehi-export-doc.html` (478 KB)
- The HTML is the complete EHI Export Format Documentation page from
  `https://ehr.escribe.com/ehr/api/ehi-export/doc`, fetched 2026-02-15.
- Contains 80 database table definitions with column-level documentation.

## Output files

| File | Description |
|------|-------------|
| `ehi-tables.json` | Full structured data dictionary — all 80 tables with columns, data types, nullability, descriptions, constraints, and PK indicators |
| `ehi-tables-summary.json` | Table-level summary: name, description, column count, primary keys, foreign key hints |
| `extraction-report.json` | Parsing accounting: files discovered, parsed, failures, total columns |

## Known parsing limitations

- 107 of 1246 columns (~8.6%) have empty descriptions in the source HTML; these are faithfully represented as empty strings in the output.
- HTML entity references (e.g. `&#39;`) are preserved as-is in description text rather than decoded.
- The script relies on `<h2 id="...">` tags to identify table boundaries and `<tr class="borderBottom">` to identify column definition rows. Changes to the HTML structure would break parsing.
