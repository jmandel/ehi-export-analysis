# Canvas Medical EHI Export Documentation Enrichment

## Run Commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/canvas-medical-inc--canvas-medical/downloads/enrichment/
bun run extract-fhir-api.ts
bun run extract-sdk-models.ts
```

## Input Boundary

### FHIR API Pages
- Source: `../api-pages/*.html`
- 31 HTML files (29 FHIR resource pages + 2 infrastructure pages)
- Downloaded from `https://docs.canvasmedical.com/api/{resource}/`

### SDK Data Model Pages
- Source: `../sdk-data-pages/data-*.html`
- 52 HTML files (51 data model pages + 1 index page)
- Downloaded from `https://docs.canvasmedical.com/sdk/data-{model}/`

## Output Files

### `fhir-api-resources.json`
Structured extraction of the FHIR R4 API documentation. Contains:
- 29 FHIR resources with their operations (CRUD endpoints)
- Field-level attributes for each operation (name, type, required, description, value options)
- Endpoint paths and HTTP methods

### `sdk-data-models.json`
Structured extraction of the Canvas SDK internal data models. Contains:
- 51 data model pages describing Canvas's internal object model
- 136 model definitions with field names and types
- 57 enumeration definitions with values and labels
- Filterable field lists

## Known Parsing Limitations

1. **FHIR API nested fields**: The apidoc__object__children hierarchy is flattened
   in the extraction. Child fields are included but without explicit parent-child
   nesting structure.
2. **SDK data model relationships**: Foreign key relationships (e.g., `Patient` type
   in a field) are captured as type strings but not resolved to links.
3. **Code examples**: Request/response JSON examples embedded in the API pages are
   not extracted (they are in hidden DOM elements toggled by JavaScript).
4. **Value set expansions**: Some enum options in the FHIR API are extracted from
   inline text and may include extra whitespace tokens.
