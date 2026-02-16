# Compulink Healthcare Solutions — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.compulinkadvantage.com/wp-content/uploads/2023/10/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf
- CHPL ID: 15.04.04.2701.Comp.12.00.1.171106 (8873)
- Product: Compulink Advantage, Version 12
- Certification date: 2017-11-06
- Documentation version date: September 20, 2023

## Navigation Journal

**Step 1: Probe the URL**
```bash
curl -sI -L "https://www.compulinkadvantage.com/wp-content/uploads/2023/10/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: application/pdf. Direct download — no redirects, no anti-bot challenges.

**Step 2: Download the PDF**
```bash
curl -sL "https://www.compulinkadvantage.com/wp-content/uploads/2023/10/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf
```
Verified: `file` confirms PDF document, 7 pages, 267,108 bytes. Author: Steven Polk. Created via Microsoft Word for Microsoft 365, October 5, 2023.

**Step 3: Check for additional materials**
- Extracted text from PDF: no embedded URLs, no references to external documentation sites.
- `pdfdetach -list`: 0 embedded files.
- Fetched the certification/mandatory disclosures page at `https://www.compulinkadvantage.com/about-compulink/certification/` (required full browser User-Agent to avoid 403):
  ```bash
  curl -sL "https://www.compulinkadvantage.com/about-compulink/certification/" \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  ```
- Found the following document links on that page:
  - COMPULINK-PHIEXPORT-DOCUMENTATION.pdf ← same file, already downloaded
  - Compulink FHIR API documentation (separate g(10) endpoint, not referenced by the EHI export PDF)
  - CBS DICOM Conformance Statement (not relevant)
  - HIPAA Readiness Statement (not relevant)
  - IHE Integration Statement (not relevant)
  - Real World Testing reports/plans (not relevant)
- No additional EHI export documentation found.

## What Was Found

A single 7-page PDF titled "ONC 21st Century Cures Edition Certification — 170.315(b)(10) Electronic Health Information (EHI) Export." The document describes the export mechanism at a structural/format level, not a field-level data dictionary level.

### Export Mechanism

The export produces a **password-protected ZIP file** containing:

1. **CSV files** — one per database table, with flat tabular data. Naming convention: `P###_TABLENAME.csv` where `###` is the patient ID and `TABLENAME` is the database table name. For bulk exports of all patients, the prefix is `P0_` and all patients appear in one file per table.

2. **Image files** — in native format (PDF, PNG, JPG, etc.). Naming convention: `P###_E/D###_####.ext` where `E` = exam document, `D` = demographics document, and the final number is the image's unique identifier.

3. **FLD files** — text files with `.FLD` extension that serve as field-level data dictionaries. Each `.FLD` file accompanies a CSV file and contains rows with `Name: FIELDNAME, Description: field description` entries. These are generated dynamically based on the practice's configuration, because the software allows "comprehensive customization."

### File Relationships

The document explains how exported files link together:
- **Demographics/Billing tables**: Linked by `PATUNIQUE` (patient identifier). These are CSV files whose table name does NOT start with "EXAM."
- **Exam tables**: Linked by `EXAMUNIQUE` (exam identifier). These are CSV files whose table name starts with "EXAM." The main exam table is `*_EXAM.csv` and sub-tables like `*_EXAMDIAG.csv` link back to it.
- **Demographics images (D)**: Image unique ID matches `DOCUNIQUE` in the `DOCUMENT` table CSV.
- **Exam images (E)**: Image unique ID matches `IMAGUNIQUE` in the `EXAMIMAG` table CSV.

### What the PDF Does NOT Contain

- **No complete list of tables** — the document names a few example tables (PATIENT, EXAM, EXAMDIAG, DOCUMENT, EXAMIMAG) but does not enumerate all tables in the export.
- **No complete field-level data dictionary** — the `.FLD` files are described as the data dictionary mechanism, but they are only available as part of an actual export, not published statically. Only 3 example fields are shown (ERXCONSENT, GENDERIDENTITYNOTE, SEXUALORIENTATIONNOTE from the PATIENT table).
- **No sample export files** — no examples of actual CSV content, FLD content, or ZIP structure.
- **No schema or relationship diagram** — relationships are described in prose only.
- **No data types, cardinality, or value set documentation**.

The remaining pages (6-7) are usage terms, liability clauses, and contact information.

## Export Coverage Assessment

### Data Domain Coverage

The PDF describes the export as containing "patient demographics, medical records, billing records, images, and more" — which sounds comprehensive in principle. The two-category structure (Demographics/Billing files + Exam files) and inclusion of images suggests the export is a genuine database dump rather than a USCDI-only subset.

**Potentially covered** (based on the CSV-per-table approach and the categories mentioned):
- Patient demographics (PATIENT table explicitly mentioned)
- Exam/encounter data (EXAM* tables explicitly mentioned)
- Diagnoses (EXAMDIAG table explicitly mentioned)
- Documents and images (DOCUMENT table, EXAMIMAG table, actual image files)
- Billing records (mentioned in the "Demographics/Billing" category)

**Cannot verify coverage of** (because no table list is provided):
- Medications and prescriptions (e-prescribing data via Surescripts)
- Lab orders and results
- Allergies
- Immunizations
- Vital signs
- Clinical notes (progress notes, H&P, etc.)
- Care plans and referrals
- Optical/POS data (frames, lenses, sales)
- ASC/surgical center data (case schedules, anesthesia records, preference cards)
- Specialty-specific clinical data (ophthalmic exams, glaucoma flowsheets, etc.)
- Patient engagement data (portal, digital forms, consents)
- Claims, payments, denial management records
- Insurance information

This is a major gap: Compulink Advantage is an extensive all-in-one platform covering EHR, practice management, billing, optical POS, ASC management, and patient engagement across 13+ specialties. The documentation provides zero insight into how much of this data actually appears in the export. It's entirely possible the export includes all of these tables — or only a subset. Without a table listing, it's unknowable from this documentation alone.

### Export Format & Standards

- **Format**: Flat CSV files + native image files, delivered as a password-protected ZIP.
- **Standard**: No recognized standard — this is an ad-hoc vendor database dump format.
- **Appropriateness**: A CSV dump of all database tables is actually one of the best possible approaches for (b)(10) compliance, since it can capture everything the system stores. The format is simple, widely readable, and doesn't force clinical data into ill-fitting standard profiles.
- **Reconstructability**: Partially. A third party could read the CSVs and understand individual tables, but would need the FLD files (only available in the export itself) to interpret field meanings. Cross-table relationships are described only in prose in this PDF. Without a complete entity-relationship diagram, reconstructing a full patient record from the CSVs would require significant reverse-engineering.

### Documentation Quality

**Poor.** This is a 7-page document where 3 pages are title/blank/TOC, 2 pages are legal terms, and only 2 pages contain substantive technical content. The technical content describes the *structure* of the export (file naming conventions, how files link together) but provides essentially no detail about the *content* (what tables exist, what fields they contain, what values are valid).

The document explicitly acknowledges that the real data dictionary is the FLD files generated with each export, because "comprehensive customization" means fields vary per installation. This is understandable but means the publicly-available documentation tells a developer almost nothing about what data to expect. The FLD files themselves are not published anywhere — they exist only within actual exports.

A developer attempting to build an import for this data would need:
1. An actual export to examine (to discover the table inventory and FLD files)
2. Significant reverse-engineering of field names and relationships
3. No documentation of data types, coded value sets, or constraints

### Structure & Completeness

- **Table-level documentation**: Missing. No list of tables. Only 5 example table names.
- **Field-level documentation**: Missing from the PDF. Deferred to FLD files in the export.
- **Data types**: Not documented.
- **Value sets/coded fields**: Not documented.
- **Relationships**: Described in prose for the top-level join keys only (PATUNIQUE, EXAMUNIQUE, DOCUNIQUE, IMAGUNIQUE). No ER diagram.
- **Versioning**: Document is versioned (v 09.20.2023) but no change history.
- **Examples**: Three field name snippets shown from the PATIENT.FLD file. No CSV content examples.

### Overall Assessment

Compulink's approach to (b)(10) is structurally sound: a CSV dump of all database tables, with native images, accompanied by auto-generated field description files. This is exactly the kind of comprehensive export that satisfies the "all electronic health information" requirement — in theory.

However, the public documentation is a compliance checkbox, not a technical specification. It tells you how to read the file naming conventions and how tables link together at a high level, but provides no insight into the actual data content. The real documentation (the FLD files) is only available inside an actual export, making it impossible for a third party to assess coverage or prepare for import without first obtaining an export from a Compulink practice.

For a product that spans 13+ medical specialties and includes EHR, practice management, billing, optical POS, ASC management, and patient engagement, the 2 pages of technical content are strikingly thin. The export mechanism itself may well be excellent — but the documentation gives no way to verify that.

## Access Summary
- Final URL (after redirects): https://www.compulinkadvantage.com/wp-content/uploads/2023/10/COMPULINK-PHIEXPORT-DOCUMENTATION.pdf
- Status: found
- Required browser: no (direct curl download works)
- Navigation complexity: direct_link
- Anti-bot issues: The certification page requires a browser-like User-Agent header (returns 403 with basic curl User-Agent), but the PDF itself downloads without issues.

## Obstacles & Dead Ends
- The certification page at `https://www.compulinkadvantage.com/about-compulink/certification/` returns HTTP 403 with a basic curl User-Agent. A full browser-style User-Agent string is required.
- Browser navigation to the certification page timed out, suggesting Cloudflare or similar protection.
- No additional EHI export documentation was found beyond the single PDF.
