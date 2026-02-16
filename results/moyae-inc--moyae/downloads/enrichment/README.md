# Moyae EHI Export Documentation Enrichment

## Run Commands

```bash
bun run extract-postman-api.ts
bun run extract-capability-statement.ts
```

## Input Boundary

- `../moyae-fhir-api-postman-collection.json` — Postman collection (2.5MB, 122 folders, 954 endpoints)
- `../fhir-capability-statement.json` — FHIR R4 CapabilityStatement from live server (1.2MB, 146 resource types)

## Output Files

- `postman-api-summary.json` — Structured summary of all API endpoints, resource type folders, export endpoints, CCDA endpoints, and per-folder endpoint details
- `capability-statement-summary.json` — Structured summary of supported FHIR resources categorized by clinical/financial/administrative domains, search parameters, operations, and security configuration

## Known Parsing Limitations

- Postman collection descriptions are HTML; only the length is recorded, not parsed content
- The collection uses Postman variables (`{{API_URL}}`, `{{COGNITO_TOKEN}}`) which are preserved as-is
- No sample response bodies are included in the Postman collection (all endpoints have empty responses)
