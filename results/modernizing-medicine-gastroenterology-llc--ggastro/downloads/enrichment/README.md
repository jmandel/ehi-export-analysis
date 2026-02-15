# gGastro EHI Export Data Dictionary Enrichment

## Run Commands

```bash
# Extract text from PDFs (prerequisite)
pdftotext -layout ../gGastro-EHI-Patient-Export-Specifications.pdf main-pdf-layout.txt
pdftotext -layout ../gGastro-EHI-Patient-Export-Specifications-Additional.pdf additional-pdf-layout.txt

# Run extraction
bun run extract-data-dictionary.ts
```

## Input Boundary

- `main-pdf-layout.txt` — Text extracted from the 167-page main EHI Patient Export Specifications PDF (gGastro-EHI-Patient-Export-Specifications.pdf)
- `additional-pdf-layout.txt` — Text extracted from the 551-page Additional PDF (gGastro-EHI-Patient-Export-Specifications-Additional.pdf), which contains only two large translation tables (Occupation and Occupation Industry) that were too large for the main document

## Output Files

- **`data-dictionary.json`** — Complete structured extraction from the main PDF containing:
  - `tables`: 441 CSV file definitions with field index, name, type, length, and format/translation references
  - `relationships`: 574 parent-child relationships between tables (data schema tree)
  - `translations`: 1,157 translation/value set tables with their coded entries (from the main PDF only; the Additional PDF's Occupation/Occupation Industry tables are not included due to their extreme size)
  - `glossary`: 23 term definitions

## Known Parsing Limitations

1. **Column alignment**: The PDF layout extraction sometimes misaligns columns when field names are very long, potentially causing type or length values to be missed for some fields.
2. **Translation parsing**: Multi-line translation entries may be split or partially captured. GUID-based translations with very long values may be truncated.
3. **Additional PDF not parsed**: The Additional PDF (551 pages of Occupation and Occupation Industry lookup tables) is not included in the JSON output. These are reference code tables for patient occupation tracking and are available in the raw text file.
4. **Data Schema depth**: The tree parser calculates depth from pipe characters, which works for most entries but may be slightly off for deeply nested items where the PDF layout wraps.
5. **Some tables may report fewer fields** than the PDF shows if the field definition line format doesn't match the expected pattern (e.g., fields with very long format descriptions that wrap to the next line).
