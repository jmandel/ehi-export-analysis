# Enrichment: EHR Your Way C-CDA Data Dictionary Extraction

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/adaptamed-llc--ehr-your-way/downloads/enrichment
bun run extract-ccda-dictionary.ts
```

## Input Boundary

- `../ehi-export-page.html` — the raw HTML of the EHI export documentation page at
  `https://ehryourway.com/electronic-health-information-export/`

## Output Files

- `ccda-data-dictionary.json` — structured JSON containing:
  - Export format metadata (C-CDA R2.1, ZIP packaging, export modes)
  - All 69 data element rows from the CCDA section table
  - Organized by 28 C-CDA sections with data elements, entry/XPath references, and code systems

## Known Parsing Limitations

- The extraction uses regex-based HTML parsing, which is sufficient for this simple table structure
- Whitespace in OID values (e.g., "2.16.840.1.113883. 6.238") is preserved as-is from the source HTML
- The prose content above the table (export workflow descriptions, access controls) is not extracted into JSON — it is captured in the report narrative instead
