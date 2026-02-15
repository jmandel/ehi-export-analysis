# Medplum EHI Export Documentation — Enrichment

## Overview

These scripts extract structured, queryable JSON from the Medplum FHIR documentation artifacts downloaded as part of the EHI export documentation collection.

## Scripts

### `extract-schemas.ts`

Extracts resource type schemas from the Medplum CapabilityStatement and OpenAPI spec.

**Run:**
```bash
cd enrichment && bun run extract-schemas.ts
```

**Input:**
- `../capability-statement.json` — FHIR CapabilityStatement from `https://api.medplum.com/fhir/R4/metadata`
- `../openapi.json` — OpenAPI 3.1 spec from `https://api.medplum.com/openapi.json`

**Output:**
- `resources.json` — All resource types with fields, search parameters, interactions, and Patient Compartment membership
- `coverage.json` — Extraction statistics and accounting

**What it extracts:**
- 165 resource types (146 FHIR R4 + 19 Medplum custom types)
- 4006 total fields across all resources
- 68 resources in the FHIR Patient Compartment (these are what `$patient-everything` returns)
- Search parameters, supported interactions, and field type information

### `extract-html-docs.ts`

Attempts to parse the downloaded Medplum Docusaurus HTML pages for resource documentation.

**Run:**
```bash
cd enrichment && bun run extract-html-docs.ts
```

**Input:**
- `../fhir-resources/*.html` — 146 resource documentation pages
- `../fhir-datatypes/*.html` — 41 data type documentation pages

**Output:**
- `html-docs.json` — Parsed page metadata (titles and descriptions)
- `html-docs-coverage.json` — Parse statistics

**Known limitation:** The Medplum documentation site is built with Docusaurus (React). The field definition tables are rendered client-side by JavaScript, so the static HTML downloaded via curl contains empty table containers. Field-level data is better obtained from the OpenAPI spec (`resources.json`).

## Key Output Files

| File | Description |
|------|-------------|
| `resources.json` | **Primary artifact.** Complete resource type catalog with fields, types, descriptions, search params, and Patient Compartment mapping. |
| `coverage.json` | Extraction statistics: counts, parse failures, Patient Compartment resource listing. |
| `html-docs.json` | Page-level metadata from HTML docs (names, descriptions, source URLs). |
| `html-docs-coverage.json` | HTML parsing statistics. |

## Patient Compartment

The `$patient-everything` operation (Medplum's EHI export mechanism) returns all resources in the FHIR R4 Patient Compartment plus referenced Organizations, Practitioners, PractitionerRoles, Locations, Medications, and Devices. The `resources.json` file marks each resource with `inPatientCompartment: true/false` and lists the search parameters that link it to a Patient.
