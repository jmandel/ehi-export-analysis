# MEDITECH EHI Export Data Dictionary Enrichment

## Run Commands

```bash
cd downloads/enrichment
bun run extract-csv-data-dictionaries.ts
```

## Input Boundary

Parses three PDF data dictionary files from MEDITECH's Configuration 2 EHI export documentation:

- `csacuteandambehiexportdrsolutionmerged.pdf` — Client/Server Acute & Ambulatory (30 pages)
- `mgehiexportdrsolutionmerged.pdf` — MAGIC Acute & Ambulatory (48 pages)
- `608ehiexportcsv.pdf` — MPM 6.08 Ambulatory (19 pages)

These PDFs document the CSV file tables and columns exported in EHI Configuration 2.

## Output Files

- `csv-data-dictionaries.json` — Full structured extraction: array of platform dictionaries, each containing table groups with field/table/column mappings
- `extraction-stats.json` — Coverage accounting: files processed, tables/fields per platform, parse errors

## Known Parsing Limitations

- PDFs use a 3-column table layout (Field, Table, Column) extracted via `pdftotext -layout`. The parser splits on 2+ whitespace characters, which works well but may fail on fields with very long names that compress column spacing.
- Table header rows (bold blue in PDF) appear as standalone lines with no column separators. The parser detects these as lines without multi-column spacing.
- A small number of parse errors (~1-2 per file) occur where PDF layout extraction produces malformed rows, typically at table boundaries or where the PDF has unusual formatting.
- Page numbers appearing as standalone integers are filtered out, which could theoretically remove a single-digit table name (none observed).
