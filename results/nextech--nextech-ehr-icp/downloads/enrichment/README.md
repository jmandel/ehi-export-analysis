# Nextech EHI Export Data Dictionary Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/nextech--nextech-ehr-icp/downloads/enrichment
bun run extract-data-dictionaries.ts
```

## Input Boundary

Parses the three XLSX data dictionary files from `../`:

- `nextech-ehr-icp-ehi-data-dictionary.xlsx` — IntelleChartPRO (ICP) platform
- `srspro-ehi-data-dictionary.xlsx` — SRSPro platform
- `nextech-select-nexcloud-ehi-data-dictionary.xlsx` — Nextech Select/NexCloud platform

Each XLSX file contains multiple sheets, one per data entity/export file type.

## Output Files

- `data-dictionaries.json` — Complete extraction of all three data dictionaries into a single queryable JSON structure containing:
  - Per-platform metadata (source file, sheet count, entity count, field count)
  - Per-entity breakdown (entity name, export format, fields with name/description/note)
  - Summary statistics (totals, breakdown by platform, export formats used)
  - Accounting of parse successes and failures

## Known Parsing Limitations

- Some sheet names don't follow the `EntityName (Format)` pattern consistently (e.g., "Patient Tasks", "Specialty Medications", "DSI feedback", "Vitals (XML) 2"), resulting in `unknown` export format. The data is still extracted correctly.
- Header row detection uses a simple heuristic (looks for "field" or "description" in the first 5 rows). Complex sheets with merged cells or sub-sections may have minor over/under-counting.
- Trailing whitespace and `\r\n` in XLSX cell values is preserved in `field_name` and `description` fields. Consumers should trim as needed.
- The SRSPro "Encounter Data Capture (XMLs)" sheet has nested XML structure documentation with sub-fields in columns 3-4; only the primary field name and description (columns 0-1) are extracted. Similarly for "Vitals (XML)" and "Results(XML)".
