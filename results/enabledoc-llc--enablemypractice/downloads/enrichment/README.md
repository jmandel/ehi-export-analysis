# EnableDoc EHI Export Data Dictionary Enrichment

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/enabledoc-llc--enablemypractice/downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input Boundary

Parses a single file:
- `../Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf` (19 pages, 476KB)

Uses `pdftotext` to extract text, then parses entity definitions, field specifications, and value sets from the structured sections of the document.

## Output Files

- `data-dictionary.json` — Complete structured extraction containing:
  - Export format descriptions (C-CDA, Attachments, Notes, Excel)
  - Excel tab names listed in the document
  - 15 entity definitions with field-level detail (224 fields total)
  - 30 value sets with 256 coded values
  - Parsing statistics and warnings

## Known Parsing Limitations

- The PDF uses inconsistent field markers: most entities use `➢` bullets, but the Medication Statement section uses bare lines without markers. Both formats are handled.
- Some fields span multiple lines in the PDF; continuation lines are joined heuristically.
- The `context` field in Medication Statement lacks a data type annotation in the source; parsed as `unknown`.
- Value set entries use varied formats ("code - display" vs "code display"); both patterns are handled.
- The SNOMED CT Clinical Findings and Vaccine Administered value sets are truncated in the source PDF (only partial lists included).
