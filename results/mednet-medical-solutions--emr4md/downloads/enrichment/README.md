# MedNet Medical Solutions — Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/mednet-medical-solutions--emr4md/downloads/enrichment
bun run extract-api-docs.ts
```

## Input Boundary

Parses all HTML files in `../`:
- `interopengine-2017-open-api-documentation.html` — EMR Direct Interoperability Engine 2017 Open API docs (FHIR STU3)
- `interopengine-2026-open-api-documentation.html` — EMR Direct Interoperability Engine 2026 Open API docs (FHIR R4)
- `mednet-open-api-page.html` — MedNet's registered Open API page
- `mednet-2015-cures-update.html` — MedNet's ONC Certified HIT / Cures Update page

PDF metadata extracted manually (not parsed programmatically):
- `Price_Transparency_emr4MD_v9.10.pdf` — Cost and Considerations document

## Output Files

- `api-documentation-extracted.json` — Structured extraction of all API documentation including:
  - FHIR resource mappings for both API versions (2017 STU3 and 2026 R4)
  - Search parameters and data type choices
  - Authentication methods and OAuth endpoints
  - EHI export entry from Price Transparency document
  - Certified criteria list
  - Additional software dependencies

- `coverage-accounting.json` — File processing accounting:
  - Total files discovered, parsed, and any parse failures
  - Per-file size and processing status
  - Summary counts of extracted entities

## Known Parsing Limitations

- The 2026 API docs do not include an explicit CCDS-to-FHIR-resource mapping table (they reference US Core IG directly). Resource types are extracted from the resource search parameter table instead.
- The Price Transparency PDF is not parsed programmatically; the EHI export entry was extracted manually and hardcoded.
- HTML table parsing uses regex-based extraction which may miss tables with unusual nesting or malformed HTML.
