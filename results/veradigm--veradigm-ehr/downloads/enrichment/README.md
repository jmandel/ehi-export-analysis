# Veradigm View V6 EHI Export Documentation Enrichment

## Run command

```bash
bun run extract-view-entities.ts
```

## Input boundary

Parses all 88 HTML files in `../veradigm-view-v6/*.html` (including `index.html`).
These pages document the TSV files produced by the Veradigm View (Practice Fusion EHR) EHI Export.

Each entity HTML page contains a single table with columns: Field Name, Data type, Field Description.

## Output files

- `view-entities-catalog.json` — Complete catalog of all 87 TSV definitions with 1194 fields. Each entity includes page title, TSV filename, entity description, source file, and field definitions.
- `view-coverage-accounting.json` — Parse accounting: files discovered, files parsed, entities extracted, fields extracted, parse failures, and per-entity summary.

## Known limitations

- HTML parsing uses simple regex extraction rather than a full DOM parser. If Veradigm changes the HTML table structure, the extraction may need adjustment.
- The index page has no entity tables and produces 0 entities (expected behavior).
- The pages reference "Practice Fusion EHR" — Veradigm View appears to be the rebranded documentation for Practice Fusion's EHI export, not the Veradigm EHR product.
