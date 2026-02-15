# InSync EHI Export Data Dictionary — Enrichment

## Run command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/qualifacts-systems-llc--insync-emr-pm/downloads/enrichment
bun install
bun run extract-data-dictionary.ts
```

## Input boundary

- `../InSync_EHI_Export_Data_Dictionary.xls` — the vendor-published XLS data dictionary (84 sheets, 1.5 MB)
- Skipped sheets: Confidential Notice, INDEX, Changelogs (metadata only; changelog data is included in output)

## Output files

- `data-dictionary.json` — complete extraction of all 81 data sections with 960 fields. Each section includes: sheet name, section name, description, category (EMR/PM), module, and an array of fields with column name, data type, nullable flag, description, and remarks. Also includes parsed changelog entries.
- `extraction-stats.json` — accounting: total sheets, sheets parsed, parse failures (with file paths and errors), and per-section summary with field counts.

## Known parsing limitations

- Sheet names in the XLS are truncated at 31 characters (Excel limit). The script resolves full section names via the INDEX sheet.
- A few sections have empty category/module fields due to minor mismatches between the INDEX sheet names and the sheet tab names.
- The "Remarks" column is sparsely populated in the original XLS; most fields have empty remarks.
- Date serial numbers in the Changelogs sheet are converted to ISO date strings.
