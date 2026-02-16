# TriMed Complete — Enrichment Scripts

## Run Commands

```bash
cd downloads/enrichment
bun run extract-patient-api.ts
bun run extract-fhir-api.ts
bun run extract-ccda-sections.ts
```

## Input Boundary

| Script | Input Files |
|--------|-------------|
| `extract-patient-api.ts` | `../patientapi-homepage.html` — Single-page HTML documentation for the SOAP Patient Data API |
| `extract-fhir-api.ts` | `../fhir-capability-statement.json`, `../swagger-api-spec.json` — FHIR server metadata |
| `extract-ccda-sections.ts` | `../xml-samples/*.xml` — 9 C-CDA XML sample responses |

## Output Files

| File | Description |
|------|-------------|
| `patient-api-methods.json` | Structured extraction of 10 SOAP API methods with request/response parameters |
| `fhir-resources.json` | 26 FHIR R4 resources from CapabilityStatement with interactions and search params |
| `fhir-api-coverage.json` | 92 OpenAPI endpoints from Swagger spec |
| `ccda-sections.json` | C-CDA sections and template IDs from XML sample responses |
| `database-schema-from-sql.json` | 18 Oracle database tables/columns extracted from SQL queries embedded in API docs (manually curated from browser-extracted hidden "Internal Use Only" sections) |

## Known Parsing Limitations

- **Patient API SQL queries**: The underlying SQL is in hidden DOM sections labeled "Internal Use Only." The automated script (`extract-patient-api.ts`) parses the static HTML, which does not include these hidden sections. The `database-schema-from-sql.json` was manually curated from browser-extracted content.
- **C-CDA sections**: Some XML samples (immunizations, lab results, medications, problem list, vitals) use flat response structures rather than nested CDA section/component elements, so the section extractor finds 0 sections for those files. The data is still present in the XML, just structured differently.
- **FHIR API**: The Swagger spec has minimal schema definitions (empty `{}` objects for request/response bodies), so field-level detail is limited.
