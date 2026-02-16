# myhELO EHI Export — Enrichment Scripts

## Overview
Extracts structured, queryable JSON from the myhELO EHI export documentation.

## Run Commands

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/myhelo-inc--myhelo/downloads/enrichment
bun run extract-api-data.ts
```

## Input Boundary
- `../fhir-metadata.json` — FHIR CapabilityStatement from `https://provider.myhelo.com/fhir/metadata`
- `../fhir-well-known.json` — Machine-readable API spec from `https://provider.myhelo.com/fhir/.well-known/fhir.json`
- `../api-docs.html` — Rendered API documentation from `https://www.myhelo.com/api/`

## Output Files
- `ehi-export-data-dictionary.json` — Complete data dictionary with:
  - All 19 supported FHIR resource types
  - API endpoints (read, search, export)
  - Search parameters with types
  - Fields extracted from example responses
  - USCDI field flagging
- `extraction-report.json` — Accounting of files parsed, resources found, errors

## Known Parsing Limitations
- Field definitions are extracted from example responses (via fhir-well-known.json), not from the
  full FHIR profile definitions on the dataset spec pages. This means field cardinality, modifier
  status, and value set bindings are not captured here — those are on the per-resource HTML pages
  in `../datasets/*.html`.
- The Organization and Group resources don't have example responses in the well-known JSON.
- The well-known JSON uses display names (e.g., "Allergy Intolerance") mapped to FHIR types
  (e.g., "AllergyIntolerance") — this mapping is hardcoded.
- The dataset spec pages (`../datasets/`) are JS-rendered and contain detailed FHIR R4 element
  definitions with cardinalities, bindings, and US Core profile conformance. These are saved as
  rendered HTML and not further parsed into JSON by this script.
