# myhELO EHI Export — Enrichment Scripts

## Overview
Extracts structured, queryable JSON from the myhELO EHI export documentation.

## Scripts

### extract-api-data.ts (v1)
Parses API examples and CapabilityStatement to produce a field-level dictionary
based on example responses.

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/myhelo-inc--myhelo/downloads/enrichment
bun run extract-api-data.ts
```

### extract-structure-defs.ts (v2 — recommended)
Parses the full FHIR StructureDefinitions extracted from the SPA JavaScript bundle.
Produces a comprehensive field-level data dictionary with cardinalities, types,
bindings, USCDI flagging, and descriptions.

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/myhelo-inc--myhelo/downloads/enrichment
bun run extract-structure-defs.ts
```

## Input Boundary (v2)
- `../structure-definitions.json` — 17 FHIR R4 StructureDefinitions extracted from the JS bundle at `https://www.myhelo.com/js.php`
- `../dataset-summaries.json` — Dataset overview metadata extracted from the same JS bundle
- `../fhir-metadata.json` — FHIR CapabilityStatement from `https://provider.myhelo.com/fhir/metadata`
- `../fhir-well-known.json` — Machine-readable API spec from `https://provider.myhelo.com/fhir/.well-known/fhir.json`

## Output Files
- `ehi-export-full-dictionary.json` (v2) — Complete data dictionary with:
  - All 17 supported FHIR resource types with US Core profile IDs
  - 921 total element definitions
  - Element-level cardinalities, types, descriptions
  - Value set bindings with strength
  - USCDI flagging (196 elements)
  - mustSupport and modifier element flagging
- `ehi-export-data-dictionary.json` (v1) — API-focused dictionary with example responses
- `extraction-report-v2.json` — Accounting of files parsed, per-resource stats
- `extraction-report.json` (v1) — Legacy extraction report

## Known Parsing Limitations
- StructureDefinitions are standard US Core STU4 profiles, not myhELO-specific custom profiles.
  The vendor states they follow US Core but does not define any vendor-specific extensions or
  custom profiles beyond what US Core provides.
- The "USCDI" flagging is based on mustSupport in the StructureDefinitions, which reflects
  US Core requirements. Elements marked `(USCDI)` in the rendered pages correspond to
  mustSupport elements.
- The StructureDefinitions were embedded in the JavaScript bundle (`/js.php`) and extracted
  via regex-based parsing of the minified JS source. The extraction was validated by
  confirming all 17 datasets parsed as valid JSON StructureDefinition resources.
