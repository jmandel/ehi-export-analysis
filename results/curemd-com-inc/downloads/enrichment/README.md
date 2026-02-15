# CureMD EHI Export Data Dictionary Enrichment

## Run Command
```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/curemd-com-inc/downloads/enrichment
bun run extract-drs.ts
```

## Input
- `../EHI_Export_DRS.xlsx` — CureMD's EHI Export Designated Record Set data dictionary (2 sheets: "EHI Export" overview + "DRS" field definitions)

## Output Files
- `drs-data-dictionary.json` — Full data dictionary with all data classes, fields, data types, and descriptions
- `drs-summary.json` — Summary with data class names, field counts, field name lists, and data type sets
- `extraction-log.json` — Extraction metadata: row counts, parse failures, processing notes

## Known Limitations
- The "Documents & Images" and "Provider Notes" data classes have only 1 field each (likely just a reference/pointer rather than full field breakdowns)
- Data class names span multiple rows in column A; the script carries forward the last non-empty class name
- No value sets or coded field enumerations are provided in the source XLSX
