# MEDHOST FHIR Extension Fields Enrichment

## Run Command

```bash
cd downloads/enrichment && bun run extract-extension-fields.ts
```

## Input Boundary

- Single file: `../MEDHOST-FHIR-Extension-Fields.xlsx` (138 KB, 45 sheets)
- Skipped sheets: `MEDHOST` (vendor description), `_reference` (internal reference)

## Output Files

- `extension-fields.json` — Full parsed data from all 43 resource/field sheets. Array of objects, each containing sheet name, mapped FHIR resource type, headers, and all data rows.
- `extraction-summary.json` — Accounting output: sheet counts, field counts per resource, parse errors, unique FHIR resource types.

## Known Parsing Limitations

- The "Directions" and "Main" sheets have non-standard headers (they contain JSON structure examples and notes rather than field definitions). They are included in the output but their data structure differs from the field-definition sheets.
- Database column references (Enterprise, EDIS, Y) are included as-is; some contain "N/A" or "N/A/" values.
- Some header names vary slightly between sheets (e.g., "Field Description" vs "Field Description/Definition").
