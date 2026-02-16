# Benchmark EHR Export Schema Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-export-schema.ts
```

## Prerequisites

- [Bun](https://bun.sh/) runtime
- `pdftotext` from `poppler-utils` on PATH

## Input

- `../b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf` — the 28-page (b)(10) self-attestation document

## Output

- `benchmark-ehr-export-schema.json` — structured JSON with all 47 export entity definitions, field lists, descriptions, and metadata

## What It Does

Extracts the "Detailed Description of the Data Export Contents" section from the PDF using `pdftotext`, then parses each numbered entity (1–47) to extract:

- Entity name and number
- Description text
- Database column-level field names (from quoted field lists)
- Whether the entity includes file attachments
- Whether it's billing-only (requires billing module)
- Notes about export constraints (active-only, latest encounter, etc.)

## Known Parsing Limitations

- 11 of 47 entities lack explicit quoted field lists in the PDF:
  - Document-type entities (#18–21: Legal Documents, Other Documents, Enc Attach Docs, Old Progress Notes) — described in prose with file path conventions but no DB column list
  - CCD (#28) — references HTML/XML file paths, no column list
  - All Vitals (#37) — described as "Vitals for all Encounters" but uses same fields as Vitals (#24)
  - Patient Notes (#40), Patient Alert (#41), Past Appointments (#42) — brief descriptions only
  - Billing Ledger (#43), Statements (#47) — brief descriptions only
- Smart/curly quotes (U+201C/U+201D) in the PDF are normalized to ASCII before regex matching
- Page headers/footers ("147 Crossings Centre Drive | Forest, Virginia 24551") are stripped
- The Referring Doctor (#3) field list spans a page break; the script handles this via fallback quoted-string extraction
