# Enrichment: RevolutionEHR EHI Export Data Dictionary

## Run command

```bash
cd downloads/enrichment
bun run extract-openapi-schemas.ts
```

## Input boundary

- `../openapiServices.json` — the OpenAPI 3.0.1 specification published by RevolutionEHR as their b(10) EHI export data dictionary (46 KB, 35 schemas, 279 fields)

## Output files

- `schemas.json` — Complete extraction of all schemas with fields, types, descriptions, required flags, inter-schema relationships, and cross-references
- `coverage-accounting.json` — Parse statistics: total schemas discovered, parsed, field counts, and root Patient schema field listing

## Known parsing limitations

- The OpenAPI spec uses a single `patient/export` POST endpoint returning the `Patient` root schema. All data is nested under this root. The extraction preserves this hierarchy.
- Field descriptions in the source are minimal (often just the field name restated). The extraction preserves these as-is.
- No value sets or coded value enumerations are present in the source spec; fields like `severity`, `status`, `smokingStatus` are typed as plain `string` with no constraints documented.
