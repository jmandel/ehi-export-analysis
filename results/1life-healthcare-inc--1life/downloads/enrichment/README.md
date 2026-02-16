# Enrichment: One Medical (1Life) EHI Export Documentation

## Run Commands

```bash
cd downloads/enrichment
bun run extract-fhir-resources.ts
```

## Input Boundary

The script parses all HTML files downloaded from `https://apidocs.onemedical.io/`:

- `../ehi-export-overview.html` — EHI Export overview page
- `../fhir/resources/*.html` — 22 FHIR resource documentation pages
- `../fhir/extensions.html` — FHIR extensions documentation
- `../fhir/terminology.html` — One Medical custom terminology codes
- `../fhir/overview.html` — FHIR API overview
- `../fhir/capability-statement.html` — FHIR CapabilityStatement info
- `../ccda/patient-continuity-of-care-document.html` — C-CDA API documentation

Total: 28 HTML files.

## Output Files

- **`fhir-resources.json`** — Structured extraction of all 22 FHIR resource pages.
  Each resource includes: resourceType, source URL, field tables with name/type/cardinality/description.
  629 total fields across all resources.

- **`ehi-export-summary.json`** — Combined extraction including:
  - EHI export format description (FHIR JSON + C-CDA XML)
  - List of FHIR resource types in the EHI export
  - List of C-CDA sections in the EHI export
  - C-CDA API endpoint details and request parameters
  - FHIR extensions used by One Medical (11 extensions)
  - Custom terminology codes (3 codes across Consent and Communication)

- **`extraction-report.json`** — Accounting output: files discovered, parsed,
  failures, and per-resource field counts.

## Known Parsing Limitations

- HTML entity decoding handles common entities but may miss rare ones
- Extension descriptions are truncated to 500 characters
- The C-CDA parameter extraction misses the `patient_id` parameter (it's in a row
  with different HTML structure than the optional params)
- Resource type capitalization from filenames may not perfectly match FHIR conventions
  (e.g., "Diagnosticreport" vs "DiagnosticReport")
