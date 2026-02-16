# Enrichment: Azalea Health EHI Export Data Extraction

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/azalea-health--azalea-ehr/downloads/enrichment
bun run extract-export-mappings.ts
```

## Input Boundary

Parses the following files from `../`:
- `ambulatory-export.html` — Ambulatory EHI Export Guide (EHR concept → FHIR resource mappings)
- `hospital-export.html` — Hospital EHI Export Guide (EHR concept → FHIR resource mappings)
- `ambulatory-capability-statement.json` — Ambulatory FHIR CapabilityStatement
- `hospital-capability-statement.json` — Hospital FHIR CapabilityStatement
- All `.html` files in `../` for inventory

## Output Files

- `export-mappings.json` — Complete extraction containing:
  - `ambulatoryExportMappings`: 57 EHR concept → FHIR resource mappings
  - `hospitalExportMappings`: 45 EHR concept → FHIR resource mappings
  - `ambulatoryCapabilityResources`: 50 FHIR resource definitions with interactions, operations, search params
  - `hospitalCapabilityResources`: 36 FHIR resource definitions
  - `fileInventory`: all HTML files with sizes
  - `summary`: parse accounting (files discovered, parsed, failures)

## Known Parsing Limitations

- Export mapping tables are extracted via regex matching Bootstrap grid `col-md-*` divs.
  If Azalea changes their HTML structure, the regex will need updating.
- Only the export guide pages contain the EHR concept → FHIR resource mapping tables.
  Other pages (resources, profiles, extensions) are downloaded but not deeply parsed
  for field-level detail since that information is in the CapabilityStatements.
