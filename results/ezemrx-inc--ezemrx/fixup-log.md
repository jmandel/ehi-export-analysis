# Fixup Log

**Date**: 2026-02-17
**Issue**: GitHub Issue #1 — Missed PDF embedded in Wix PDF Viewer Pro widget

## Diagnosis
- Root cause stage: **2 (download)**
- Problem: The Wix PDF Viewer Pro widget on the ezEMRx EHI export page loads its PDF dynamically via a Firebase cloud function after the Wix TPA framework initializes. The original download agent inspected the DOM and found an empty iframe (`src` attribute blank), concluding no PDF was configured. In reality, the widget's `src` is populated asynchronously after full page rendering — the PDF exists and has since at least April 2024 (document version 2.0).

## Changes Made
- Downloaded `ehi-export-data-dictionary.pdf` (189 KB, 9 pages) from the Wix PDF Viewer Pro widget's Google Cloud Storage backend
- Extracted text to `ehi-export-data-dictionary.txt` via pdftotext
- Created `downloads/enrichment/` with:
  - `extract-data-dictionary.ts` — enrichment script extracting structured JSON from the PDF
  - `data-dictionary.json` — structured extraction: 4 file categories, 2 CSV schemas, 24 total columns
  - `README.md` — enrichment documentation
- Updated `files.json` with all new artifacts
- Rewrote `ehi-export-report.md`:
  - Updated navigation journal section 4 (PDF viewer finding)
  - Replaced "no documentation found" assessment with full coverage analysis
  - Updated access summary and obstacles sections
- Archived original downloads to `downloads.pre-fixup/`

## Cascade
- Stage 2 (download): Fixed — PDF downloaded, enrichment built, report rewritten
- Stage 3 (analysis) and Stage 4 (summary): Not yet cascaded — no existing abstraction directory for this vendor

## Verification
- PDF is valid: `file` reports "PDF document, version 1.6"
- Text extraction works: pdftotext produces 9 pages of readable content
- Enrichment script runs successfully: `bun run extract-data-dictionary.ts` produces valid JSON
- files.json includes all 8 artifacts (3 original + 5 new)
- ehi-export-report.md contains complete coverage assessment based on PDF content
