# MEDENT EHI Export Documentation Enrichment

## Scripts

### extract-ehi-specs.ts
Extracts structured field definitions from the 33 EHI export PDF specifications.

**Run:** `bun run extract-ehi-specs.ts`
**Requires:** `pdftotext` (from poppler-utils) on PATH
**Input:** `../ehi_pdfs/*.pdf` (33 PDF files)
**Outputs:**
- `ehi-specs.json` — Queryable JSON with field names, descriptions, titles, and example presence indicators for each file spec
- `ehi-specs-raw.json` — Full extracted text from each PDF for reference
- `extraction-report.json` — Coverage/accounting: files discovered, parsed, failures, field counts

### extract-ascii-fields.ts
Extracts the 750-field ASCII Field List from the MEDENT HTML manual page, which documents all financial/billing data export fields available through the Data Export Module.

**Run:** `bun run extract-ascii-fields.ts`
**Input:** `../asciifieldlistinter.html`
**Output:** `ascii-field-list.json` — All 750 fields with format number, area code, area description, field name, and notes

## Known Limitations

- PDF extraction via `pdftotext -layout` can sometimes merge or split two-column table content incorrectly, especially for fields with long descriptions that wrap across lines
- The EHI Setup PDF and Info File PDF are configuration/overview documents (not field specs) and return 0 fields — this is expected
- The Financial File Specification PDF has only 1 field extracted because it references the external ASCII Field List for its field definitions
- The ASCII field list HTML is a JavaScript SPA; we downloaded and parsed the static HTML which contains the data table
