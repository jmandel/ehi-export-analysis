# Enrichment: b10 Data Dictionary Extraction

## Run Command

```bash
cd downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input

- `../b10_data_dictionary.xlsx` — The official Ontada (b)(10) EHI export data dictionary (4 sheets, ~5,679 field definitions across 249 entities)

## Output Files

- `data-dictionary.json` — Full structured extraction of all sheets into a single queryable JSON file. Contains:
  - All tables with their columns (name, data type, length, description)
  - Ontada Health collections with their fields
  - Grouped by source sheet
- `summary.json` — Coverage/accounting output with:
  - Total files discovered and parsed
  - Per-sheet table and column counts
  - Full table listing with column counts and descriptions
  - Parse failure list (empty — all rows parsed successfully)

## Parsing Notes

- All 4 sheets parsed completely: iKnowMed (236 tables, 5,275 cols), VBC (5 tables, 60 cols), Patient History (6 tables, 178 cols), Ontada Health (2 collections, 166 fields)
- The iKnowMed sheet includes TABLE_DESC and COLUMN_DESC fields; VBC and Patient History sheets lack descriptions
- The Ontada Health sheet uses a different schema (Collection/Field Name/Data Type/Description/Notes)
- No parse failures
