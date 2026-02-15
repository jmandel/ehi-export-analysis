# Enrichment: Lunar EHI Export PDF Extraction

## Run Command

```bash
cd /home/jmandel/hobby/ehi-export-analysis/results/lunar-systems-inc--lunar-cloud-platform/downloads/enrichment
bun run extract-sections.ts
```

## Input Boundary

- Single file: `../EHI_Export_Jan_2026.pdf` (54-page PDF, 1.1 MB)
- Text extracted via `pdftotext` (poppler)

## Output Files

| File | Description |
|------|-------------|
| `ehi-export-sections.json` | 18 C-CDA sections with descriptions, template IDs, LOINC codes, key elements |
| `ehi-export-supplemental.json` | 3 supplemental CSV categories (Documents, Orders, Charges) with 42 field definitions |
| `extraction-stats.json` | Parse accounting: pages, sections found vs expected, failures |

## Known Parsing Limitations

- Key element descriptions may be truncated at line breaks (PDF text extraction artifacts)
- LOINC display names may contain `\n` from cross-line PDF text extraction
- Patient Summary section lacks templateId/LOINC because it uses `<recordTarget>` rather than a `<section>` with metadata
- XML examples are not extracted as separate artifacts (they are in the PDF text and available via pdftotext)
