# eMedPractice EHI Export Documentation — Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input Boundary

Parses two files from the parent `downloads/` directory:

- `ehi-data-dictionary-tables-api.json` — WordPress JSON API response for the data dictionary page
  (`https://emedpractice.com/electronic-health-information-data-dictionary-tables/`)
- `ehi-export-page-api.json` — WordPress JSON API response for the main EHI export page
  (`https://emedpractice.com/electronic-health-information-export/`)

## Output Files

| File | Description |
|------|-------------|
| `data-dictionary.json` | Structured extraction of all 3 table schemas (Patients, Insurance, Appointments) with column names, data types, defaults, and nullability |
| `ehi-export-content.json` | Structured extraction of the EHI export page prose: section headings, content items, links, and commented-out sections |
| `extraction-report.json` | Accounting output: files discovered, files parsed, parse failures, counts |

## Known Parsing Limitations

- HTML table parsing uses regex patterns, not a full DOM parser. Assumes well-formed table HTML.
- The data dictionary page contains two identical copies of the tables (one hidden via `d-none` CSS class, one visible). Deduplication is by table name + column count.
- The first table's heading in the HTML is the page title "EHI Data Dictionary Tables" rather than "Patients Table Schema" — the script renames it.
- The commented-out Section 4 (Documents) is extracted both as a commentedOutSection and as a parsed section (since the regex matches `<h3 class="sub-header">` inside HTML comments).
- Notes section appears twice in the export content due to overlapping regex matches.
