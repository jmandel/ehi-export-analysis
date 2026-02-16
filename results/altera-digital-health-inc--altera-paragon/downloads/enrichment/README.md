# Enrichment: Paragon EHI Export Documentation

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/altera-digital-health-inc--altera-paragon/downloads/enrichment
bun run extract-capability-statement.ts
```

## Input Boundary

- `../paragon-25-1/CapabilityStatement.json` — FHIR R4 CapabilityStatement documenting all 48 resource types in the EHI export
- `../paragon-25-1/Extension-Details.xlsx` — 826 custom extension definitions across 33 resource types

## Output Files

- `capability-statement-extracted.json` — Structured extraction of all resources, their standard elements, custom extensions, and search parameters
- `extension-details-extracted.json` — All 826 extension definitions grouped by resource type with keys, names, and definitions
- `coverage-summary.json` — Summary with resource counts, data domain mapping, and parse accounting

## Known Limitations

- The CapabilityStatement uses a non-standard approach: FHIR element references and custom extensions are listed as `extension` entries on each resource, rather than using proper `supportedProfile` or `searchRevInclude`. This is a vendor-specific documentation convention, not a standard FHIR CapabilityStatement.
- Extension definitions include natural-language descriptions only; no formal StructureDefinition or data type constraints are provided.
- The CapabilityStatement does not include operation definitions ($export, $everything, etc.), so the actual export mechanism is not documented in these files.
