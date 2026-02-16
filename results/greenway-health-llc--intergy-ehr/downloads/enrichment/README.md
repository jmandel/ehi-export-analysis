# Intergy EHI Export — Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-tables.ts
```

## Input Boundary

Parses all `.htm` files in `../viewer/Contracts/` (excluding `DBTOC.htm`).
These are the individual table definition pages from the Intergy EHI Export
data dictionary at `https://ehi.greenwayhealth.com/Intergy/EHI/Viewer/`.

## Output Files

- **`intergy-data-dictionary.json`** — Array of 261 table definitions, each with:
  - `name`, `description`, `last_updated`, `intergy_version`
  - `fields[]` — field name, datatype, default, null option, comment
  - `parent_tables[]` / `child_tables[]` — foreign key relationships
  - `source_file` — path to source HTML

- **`extraction-coverage.json`** — Parsing statistics:
  - Files discovered/parsed, total fields, relationships
  - Parse failures with file paths and error reasons
  - Per-table summary (field count, relationship counts)

## Known Parsing Limitations

- HTML entity decoding is basic (handles `&nbsp;`, `&amp;`, `&lt;`, `&gt;` only)
- Default values that are just "?" are normalized to null
- Relationship extraction depends on consistent HTML structure across all pages
