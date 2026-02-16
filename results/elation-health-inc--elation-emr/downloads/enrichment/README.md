# Enrichment: Elation EHI Export Data Dictionary

## Run Command

```bash
cd downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input

- `../elation-designated-record-set-ehi-export.pdf` — Elation's Designated Record Set PDF (7 pages, dated 2/6/2024)
- Requires `pdftotext` (from poppler-utils) on PATH

## Output Files

- `data-dictionary.json` — Array of all data elements with fields:
  - `data_element`: field/element name
  - `data_description`: human-readable description
  - `section`: inferred data category (e.g., "Patient Demographics", "Billing - Bills")
  - `export_formats`: which export formats include this element (`computable_pdf`, `xml`, `json`, `csv`)

- `coverage-summary.json` — Aggregate statistics:
  - Element counts by section
  - Element counts by export format
  - Elements with no export format specified
  - Parse metadata (line counts, etc.)

## Parsing Approach

The PDF is a Google Sheets–generated table with 4 export format columns. Column positions shift between pages. The parser:

1. Detects header rows ("Data Element ... Data Description ... Computable PDF Export ... XML Export ... JSON ... CSV Export")
2. Records column start positions from each header
3. For data rows, finds isolated "X" markers and classifies them into columns based on header positions
4. Infers sections from known element name transitions

## Known Limitations

- Section assignment is heuristic based on element name patterns; a few elements near section boundaries may be miscategorized
- Multi-line data descriptions (text wrapping across lines) in the PDF are not joined; the second line may be skipped if it lacks X markers
- The "Lab Order, Imaging Order, Pulmonary Order, Cardiac Order, Sleep Order" row has a very long element name that wraps in the PDF; only the first line is captured
