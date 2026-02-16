# ModMed EMA EHI Export Data Dictionary — Enrichment

## Run commands

```bash
# Prerequisites: Bun v1.3+, pdftohtml (from poppler-utils)

# 1. Generate XML from PDFs (if not already done)
pdftohtml -xml -stdout ../ModMed-EMA-Detailed-Data-Dictionary.pdf > ../detailed-dd-xml.xml
pdftohtml -xml -stdout ../ModMed-EMA-EHI-Export-Data-Dictionary.pdf > ../overview-dd-xml.xml

# 2. Extract structured JSON
bun run extract-detailed-dd.ts
bun run extract-overview-dd.ts
```

## Input files

| File | Description |
|------|-------------|
| `../ModMed-EMA-EHI-Export-Data-Dictionary.pdf` | 96-page overview: table inventory, groupings, relationships, appendices with value sets |
| `../ModMed-EMA-Detailed-Data-Dictionary.pdf` | 210-page field-level data dictionary (from Google Sheets .xlsx export) |
| `../detailed-dd-xml.xml` | pdftohtml XML of the detailed dictionary (intermediate) |
| `../overview-dd-xml.xml` | pdftohtml XML of the overview dictionary (intermediate) |

## Output files

| File | Description |
|------|-------------|
| `detailed-data-dictionary.json` | 5,250 field entries across ~257 tables with column names, data types, nullability, field lengths, and coding schemas |
| `overview-table-inventory.json` | 411 table entries with groupings, descriptions, relationships, and refresh frequencies |

## Known parsing limitations

1. **Word-wrapped text merging**: pdftohtml sometimes merges the IDX number with the Grouping text into a single `<text>` element (e.g., `"2533 eLab"`). The parser handles this by splitting on the leading number.

2. **Very long table/column names**: Table names like `central_retinal_thickness` that wrap across two lines in the PDF can cause the second line fragment (e.g., `ss`) to be misclassified as the table name for subsequent fields. This affects roughly 2-3% of entries (tables with names >25 characters in the PDF's narrow column).

3. **Overview grouping merge**: In the overview extraction, some grouping entries include fragments of the table name or description due to the complex multi-column layout. The detailed extraction is more reliable.

4. **Nullable/dataType alignment**: For a small number of entries, the data type and nullable columns may be shifted (description text bleeds into dataType, dataType into nullable). This affects rows where the description is very long.

The vast majority (>95%) of the 5,250 field entries parse correctly with accurate table, column, description, data type, and nullability values.
