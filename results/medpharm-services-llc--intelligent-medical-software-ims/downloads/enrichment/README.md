# Enrichment: Meditab FHIR API Specification Extraction

## Run Commands

```bash
bun run extract-fhir-specs.ts
```

## Input Boundary

- `../fhir-specifications.html` — raw HTML of the FHIR specifications page (SPA, 3.3 MB)
- `fhir-resources-browser-extract.json` — structured data extracted via Chrome DevTools browser automation (the HTML is a client-rendered SPA and cannot be parsed statically)

## Output Files

- `fhir-resources.json` — deduplicated, structured FHIR resource definitions (16 resources, 131 unique fields, search parameters)
- `extraction-stats.json` — coverage/accounting: resource counts, field counts per resource, parse failures

## Known Parsing Limitations

- The source HTML is a Duda website builder SPA; all content is rendered client-side. Static HTML parsing yields no content. The extraction relies on browser-captured JSON from Chrome DevTools `evaluate_script`.
- Response code tables (standard HTTP codes) are not extracted as they contain no IMS-specific information.
- The page documents each resource's Read and Search interactions with separate field tables; deduplication merges these into a single field list per resource.
- The FHIR specifications page documents only standard US Core FHIR R4 resources — this is the g(10) API documentation, not a comprehensive b(10) data dictionary.
