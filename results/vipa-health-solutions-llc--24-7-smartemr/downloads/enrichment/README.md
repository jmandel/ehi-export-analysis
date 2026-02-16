# smartEMR Documentation Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-data-models.ts
```

## Input Boundary

Parses all `.html` files in `../` (the downloads directory), which are pages
downloaded from `smartemr.readme.io`:

- `electronic-health-information-export-b10.html` — the main EHI export page
- 10 data import/schema pages documenting field specifications

## Output Files

- `smartemr-data-models.json` — Structured field specifications for each data
  import page (patient demographics, insurance, CPT codes, service locations,
  referring physicians, appointments, document uploads, problem lists, allergies).
  Each model includes: page name, title, category, description, field specs
  (name, description, data type, max length, required flag, validation rule),
  import capabilities, technical guidelines, accepted file formats.

- `smartemr-ehi-export.json` — Structured description of the EHI export
  mechanism: format (CDA + document repository), single-patient and population
  export workflows, document repository organization.

- `extraction-stats.json` — Accounting: total files discovered, parsed,
  parse failures, models and fields extracted.

## Known Parsing Limitations

- The HTML pages are rendered by a ReadMe.io SPA; the field specification
  tables are embedded in the server-rendered HTML but the table markup is
  somewhat inconsistent across pages.
- The immunization records page has no content (empty page on the vendor's
  site), so no model is extracted for it.
- The allergy page has a mixed table format (includes a "Standard" column
  instead of "Max Length"), which is handled but the mapping is approximate.
