# Enrichment: myAvatar EHI Export All Tables

## Run Commands

```bash
# Prerequisites: Bun runtime, pdftotext (from poppler-utils)
# 1. Extract text from the PDF (already done, output is ../ehi-export-all-tables.txt)
pdftotext "../EHI Export All Tables - September 2023.pdf" ../ehi-export-all-tables.txt

# 2. Parse the text into structured JSON
bun run extract-tables.ts
```

## Input Boundary

- **Source PDF**: `EHI Export All Tables - September 2023.pdf` (16 MB, 7,492 pages)
- **Parsed file**: `../ehi-export-all-tables.txt` (pdftotext output, 318,819 lines)
- The script parses all table documentation entries from the text, skipping the
  Table of Contents and Glossary sections.

## Output Files

- **`tables.json`** — Array of table entries, each with:
  - `form_name`: The myAvatar form associated with the table
  - `table_name`: Fully qualified table name (schema.table)
  - `schema`, `table_short_name`: Parsed components
  - `table_description`: Table-level description (when present)
  - `columns[]`: Array of column definitions with `name`, `type`, `max_length`, `description`

- **`coverage-summary.json`** — Aggregate statistics:
  - Total table entries, unique tables, unique forms
  - Column counts and description coverage percentages
  - Schema breakdown (SYSTEM, STATEFORM, OrderEntry, etc.)
  - Data domain categorization with table counts and samples

## Known Parsing Limitations

- The pdftotext extraction inserts page numbers as standalone lines; these are
  filtered out but occasionally a description may include a stray page number.
- Some columns lack descriptions in the source PDF (18.9% have no description);
  this is not a parsing error but a source data limitation.
- Table entries appear multiple times in the PDF when the same table is
  referenced by multiple forms. The parser captures all entries (906 total)
  while the unique table count is 561.
- The TOC section includes dotted-line page references that are filtered by
  pattern matching; edge cases with unusual formatting may be missed.
- Multi-line table descriptions that span page breaks may lose whitespace.
