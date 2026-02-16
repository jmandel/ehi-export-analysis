# CharmHealth FHIR API Documentation Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/medicalmine-inc--charmhealth-ehr/downloads/enrichment
bun run extract-fhir-api.ts
```

## Input Boundary

- `../fhir-api-documentation.html` — the single-page FHIR API documentation from
  https://www.charmhealth.com/resources/fhir/index.html (420KB HTML)

## Output Files

- `fhir-api-extracted.json` — structured extraction of all FHIR resources,
  operations, parameters, OAuth scopes, Bulk Export API, and CCDA API details

## What Is Extracted

- 24 FHIR resource types with their operations (list, get, search)
- Query/path parameters for each operation
- US Core profile references where documented
- OAuth scope tables (patient, user, system)
- Bulk Export API (start, status, delete operations)
- CCDA export API details
- Parsing statistics and failure accounting

## Known Limitations

- Request/response examples are extracted as plain text (HTML tags stripped)
- The script does not extract inline JSON sample responses with full structure
  preservation; they are flattened to text strings
- Provenance resource only has a "get" operation (no list/search) per the source docs
- Medication resource only has a "get" operation per the source docs
