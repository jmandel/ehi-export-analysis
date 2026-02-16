# WebChart EHI Export Documentation Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-schema.ts
```

## Input Boundary

- `../ehi-export-technical-details.md` — markdown source of the EHI Export Technical Details page (492KB)
- `../sample-single-patient-export.json` — sample single-patient JSON export extracted from the documentation (482KB)

## Output Files

- `drs-data-dictionary.json` — 99 DRS (Designated Record Set) objects with names and descriptions, parsed from the HTML table in the markdown
- `export-schema.json` — field-level schema for the JSON export format, inferred from the sample export; includes patient scalar fields, nested object schemas with field types and sample values
- `extraction-report.json` — coverage/accounting: counts of objects parsed, objects with/without descriptions, coverage gaps between DRS table and sample export

## Known Parsing Limitations

- The DRS table uses simple `<tr><td>` HTML in markdown; the regex parser handles this well but would break on nested HTML
- Schema inference is based on a single sample patient record; fields that are empty/null in the sample won't have type information beyond "null"
- 18 of 99 DRS objects have no description in the source documentation (mostly escript_* and incident_* tables)
- 73 DRS objects are not represented as nested arrays in the sample export (they're either the patient record itself, lookup tables, or simply empty for this patient)
- 3 objects appear in the sample export but not in the DRS table: `audit_log_chart`, `patient_warning_dismiss`, `patient_warnings`
