# TRIARQ QSuite EHI Export — Data Dictionary Enrichment

## Run command

```bash
bun run extract-data-dictionary.ts
```

## Input boundary

- `../main.js` — the compiled Angular bundle from `https://ehi.myqone.com/main.82861f638e42f48d.js` (408,111 bytes)

The EHI documentation site is an Angular SPA that embeds the complete data dictionary
in two JS arrays within the main bundle:
- `resourceList` — 27 CSV export resource types with descriptions
- `ehiexportdocs` — 777 field definitions (name, type, description) grouped by module

## Output files

- `data-dictionary.json` — Complete structured data dictionary with:
  - 32 entities (27 resource types + 5 sub-entities for Patient Cases and Prior Authorization)
  - 777 field definitions with name, type, and description
  - 4 non-CSV export format categories (CCDA, PDF, Word, Image) with 19 document types
- `resource-list.json` — Flat list of 27 resource types with IDs and descriptions
- `extraction-report.json` — Parsing accounting (totals, failures, coverage)

## Known limitations

- PDF, Word, and Image export types are listed as categories only (no field-level specs).
  These are document files included in the export package, not structured data.
- `DMS Document(Index)` and `Patient Cases` are listed as resource types but have
  no field definitions — they serve as parent categories. Their sub-entities
  (Patient Cases - Diagnosis, etc.) do have fields.
- CCDA export format is described only by reference to external HL7 standards
  (C-CDA R2.1 Companion Guide Release 4.1, USCDI v3). No vendor-specific
  CCDA profile or customization documentation is provided.
