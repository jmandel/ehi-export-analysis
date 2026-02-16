# myEvolv EHI Export Data Dictionary Enrichment

## Run Command
```bash
bun run extract-data-dictionary.ts
```

## Input Boundary
Parses the single XLSX file:
- `../(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx` (11.2 MB, 5 sheets)

All sheets are parsed: Info, Events, Events + Columns, Non-Events, Non-Events + Columns.

## Output Files

| File | Description | Records |
|------|-------------|---------|
| `events.json` | Event definitions with category, table, form info | 1,679 |
| `events-columns.json` | Field-level detail for all event columns | 115,663 |
| `non-events.json` | Non-event form definitions | 250 |
| `non-events-columns.json` | Field-level detail for non-event form columns | 21,006 |
| `summary.json` | Coverage/accounting: counts, categories, tables, type codes | 1 |

## Known Limitations
- The XLSX represents a "freshly installed myEvolv instance" per the Info sheet; user-defined events/forms are not included.
- Column header names in Events + Columns have a duplicate `typeCode` column (one for the main form field, one for subform fields). The xlsx library maps both to `typeCode` with the second overwriting the first; subform type codes take precedence when both exist.
- No parse failures encountered.
