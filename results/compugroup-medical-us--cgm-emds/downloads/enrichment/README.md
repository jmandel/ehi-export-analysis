# CGM eMDs EHI Export Data Dictionary Enrichment

## Run Command

```bash
bun run extract-ehi-data-dictionary.ts
```

## Input

- `../cgm-emds-electronic-health-information-export-user-guide.pdf` — the single-source PDF containing the EHI export documentation (14 pages, December 2023)

## Output

- `ehi-data-dictionary.json` — Complete structured extraction of:
  - 27 document categories that may appear in the export ZIP
  - 5 export files with field-level documentation (162 total fields across 28 sections)
  - Export format metadata (ZIP container, file naming convention, text standards)
  - Coverage statistics (which document categories map to which export files)

## Known Parsing Limitations

- The PDF tables were manually transcribed into the TypeScript source because the PDF is only 14 pages with clean, well-structured tables. Automated PDF table extraction (e.g., via tabula or pdfplumber) was not needed for this volume.
- The "Entire Patient Chart Report.xlsx" section in the PDF describes the file's contents at a high level (visit notes, allergies, medications, etc.) rather than listing individual column headers. The extraction reflects this level of granularity.
- The "Tests and Procedures" section in Health Summary Report.xlsx is listed as a heading in the PDF but no individual fields are enumerated beneath it.
