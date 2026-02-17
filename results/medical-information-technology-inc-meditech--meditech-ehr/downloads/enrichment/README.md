# MEDITECH EHI Export CSV Data Dictionary Enrichment

## Run Command

```bash
bun run extract-csv-data-dictionaries.ts
```

Requires: `pdftotext` (from `poppler-utils`).

## Input Boundary

Parses three PDF files from `../`:

| File | Platform |
|------|----------|
| `608ehiexportcsv.pdf` | MPM 6.08 Ambulatory |
| `csacuteandambehiexportdrsolutionmerged.pdf` | Client/Server Acute & Ambulatory |
| `mgehiexportdrsolutionmerged.pdf` | MAGIC Acute & Ambulatory |

These PDFs document the tables and columns included in MEDITECH's EHI Export
Patient Data CSV files (Configuration 2 — legacy platforms using Medical Records/
Data Repository).

## Output Files

- `csv-data-dictionaries.json` — Complete extraction of all tables, fields, and
  columns from all three PDFs, plus extraction statistics.

## Structure

```
{
  "extractionDate": "YYYY-MM-DD",
  "stats": { totalFilesDiscovered, totalFilesParsed, parseFailures },
  "dictionaries": [
    {
      "sourceFile": "filename.pdf",
      "platform": "...",
      "lastUpdated": "October 2023",
      "tables": [
        {
          "tableName": "AdmVisits",
          "fields": [
            { "field": "Home Phone", "table": "AdmVisits", "column": "HomePhone" }
          ]
        }
      ],
      "totalFields": N,
      "totalTables": N,
      "parseErrors": []
    }
  ]
}
```

## Known Parsing Limitations

- Uses `pdftotext -layout` which depends on PDF text layer positioning. Complex
  table layouts with wrapped cells may occasionally misparse.
- Table headers (section headers) are identified as single-segment lines in the
  PDF. If a table name contains spaces matching the column separator width, it
  could be misidentified.
- Page numbers and repeated headers are filtered heuristically.
- The PDFs only cover Configuration 2 platforms (legacy). Configuration 1
  (Expanse, 6.x) does not have equivalent CSV data dictionaries — those
  platforms use a different export format (electronic chart documents, FHIR, C-CDA).
