# Enrichment: Infinx EHR (iMedEMR) EHI Export Data Dictionary

## Run Commands

```bash
# Extract PDF text (prerequisite)
pdftotext ../IMED-EHI-Export-Documentation.pdf ehi-export-doc.txt

# Run enrichment
bun run extract-data-dictionary.ts
```

## Input Boundary

- **Source file**: `IMED-EHI-Export-Documentation.pdf` (13-page PDF)
- **Intermediate**: `ehi-export-doc.txt` (pdftotext output, 1363 lines)
- Single PDF document covering the entire EHI export data dictionary

## Output Files

- `data-dictionary.json` — Structured JSON containing:
  - Export format description (ZIP container with CSV, XML, PDF files)
  - Export instructions (single patient vs bulk)
  - 15 patient data tables with field-level definitions
  - 248 total fields across all tables
  - Schema/data type info where available
  - Value set definitions where documented

## Known Parsing Limitations

- The PDF text extraction (pdftotext) breaks table columns across lines
  unpredictably, especially for the multi-column tables (Field Name /
  Description / Schema). Rather than attempting fragile regex-based parsing,
  the fields were defined explicitly from careful reading of the extracted text.
- The `schedules` table has ~35 fields listed without descriptions in the
  source PDF — these are included with "(no description in source)" notes.
- The `patientinfo` table lacks Schema column in the PDF; only Field Name
  and Description are provided.
- Some tables (ob, patient_letters, patient_referrals) have simple two-column
  layouts (Field Name / Description) without Schema types.
