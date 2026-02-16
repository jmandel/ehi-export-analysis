# Enrichment: PointClickCare EHI Export IG

## Run Commands

```bash
cd downloads/enrichment
bun run extract-structure-definitions.ts
bun run extract-csv-schemas.ts
```

## Input Boundary

- `extract-structure-definitions.ts`: Parses all JSON files in `../package/package/` (the FHIR IG NPM package). 72 JSON files total.
- `extract-csv-schemas.ts`: Parses `../site/MDS.html` and `../site/NonMDS.html` for CSV schema tables.

## Output Files

- `structure-definitions.json` — All 67 StructureDefinition profiles (26 standard FHIR resource profiles, 10 custom resources, 31 extensions), 2 ValueSets, 2 CodeSystems. Includes element-level detail (path, type, cardinality, short description, bindings).
- `csv-schemas.json` — 12 CSV schema definitions (7 MDS + 5 non-MDS assessment schemas) with 225 total columns. Each column has name, type, nullable, and description.

## Known Parsing Limitations

- Extension extraction from differential elements may miss extensions defined only in snapshot.
- Element list is truncated at depth 3 (path segments) to keep output manageable; deeper nested elements in complex types are omitted.
- CSV schema extraction relies on regex matching of HTML table structure; if the vendor changes HTML structure, extraction may fail silently.
