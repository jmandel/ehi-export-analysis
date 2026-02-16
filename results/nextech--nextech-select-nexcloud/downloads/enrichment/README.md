# Nextech Select/NexCloud EHI Data Dictionary Enrichment

## Run Command

```bash
cd downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input Boundary

- **Source file**: `../Nextech_Select_NexCloud_EHI_Export_Data_Dictionary_2025.xlsx`
- All 16 sheets in the workbook are parsed

## Output Files

- `data-dictionary.json` — Complete data dictionary with all entities (CSV exports, EMN PDF, DSI feedback) and their field definitions. Each entity includes sheet name, export format, derived export filename, and an array of fields with name, description, and optional notes.
- `extraction-summary.json` — Accounting output: total sheets discovered vs. parsed, parse failures (if any), per-entity field counts, and total field count.

## Known Parsing Limitations

- The "DSI feedback" sheet has no format indicator in its name (no parenthetical like "(CSV)"), so its `export_format` is recorded as "Unknown".
- The EMN (PDF) sheet describes fields that appear in customizable encounter PDFs; field presence varies per practice configuration. The data dictionary documents "best practice" fields, not a fixed schema.
- The "Custom (CSV)" export has only 7 generic fields because custom field names/values are entirely practice-specific.
- No data types are specified in the source XLSX — all fields have name + description + optional note only.
