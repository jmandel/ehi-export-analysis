# Enrichment: Amazing Charts EHI Export Data Dictionary

## Run Command

```bash
cd results/caretracker-inc--amazing-charts/downloads/enrichment
bun run extract-data-dictionary.ts
```

## Input

- `../Amazing-Charts-EHI-Export-Documentation-V1_0-1-1.pdf` — the sole EHI export documentation PDF (8 pages, 195 KB)
- Text is extracted at runtime via `pdftotext`

## Output

- `data-dictionary.json` — queryable JSON with all data classes and their column headings

### JSON Schema

```json
{
  "source": "filename.pdf",
  "version": "v1.0",
  "export_formats": ["csv", "json", "xml"],
  "extraction_date": "YYYY-MM-DD",
  "total_data_classes": 43,
  "total_columns": 1101,
  "expected_data_classes": 44,
  "parse_failures": [{ "name": "...", "reason": "..." }],
  "data_classes": [
    {
      "name": "Data Class Name",
      "columns": ["Col1", "Col2", ...],
      "column_count": N
    }
  ]
}
```

## Known Parsing Limitations

1. **"HM Rules" data class (1 of 44)** — This data class name appears on its own line in the PDF with no columns following it before "Immunizations" starts. In the PDF's visual layout, "HM Rules" and "Immunizations" share a combined column listing. pdftotext flattens this, so all 122 columns are attributed to "Immunizations". The HM Rules columns (RuleName, RecommendedAge, etc.) appear at the tail of the Immunizations column list.

2. **No data types or value sets** — The PDF only documents column headings (names), not data types, constraints, value sets, or relationships. The extraction reflects this limitation of the source document.

3. **Spelling preserved as-is** — Typos in the original PDF are preserved (e.g., "Assesments", "FristName", "Signetur", "BillingProvideerState"). These match the actual export column names.
