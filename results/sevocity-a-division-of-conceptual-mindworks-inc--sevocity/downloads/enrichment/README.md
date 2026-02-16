# Sevocity FHIR API OpenAPI Spec Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-openapi-schemas.ts
```

## Input Boundary

Parses all YAML files from the Sevocity FHIR API documentation at `fhirapi-docs.sevocity.com`:
- `../openAPIDocs.yml` — main OpenAPI 3.0.1 spec
- `../fhir-api-docs/components/schemas/*.yml` — 52 resource schemas (read + search variants)
- `../fhir-api-docs/paths/*.yml` — 52 API endpoint definitions
- `../fhir-api-docs/examples/*.yml` — 26 example FHIR resources

## Output Files

- `sevocity-fhir-api-extracted.json` — complete structured extraction containing:
  - Resource schemas with nested field definitions (name, type, isArray, children)
  - API endpoints with methods, parameters, certification status
  - Example FHIR resources (full content)
  - Coverage accounting (files discovered, parsed, failures)

## Known Parsing Limitations

- Field type extraction is limited to 4 levels of nesting depth
- The `FHIR-JSON-RESOURCE` schema is a generic passthrough with no fields
- Search schemas wrap resources in Bundle structure; field counts include the Bundle wrapper
- Some example files contain Bundle search results rather than individual resources
