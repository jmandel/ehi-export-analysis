# Eyefinity, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.modmed.com/wp-content/uploads/2023/11/Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf
- CHPL IDs: 11088
- Product: EHR powered by EMA in Eyefinity Encompass
- Developer: Eyefinity, Inc.
- Certification date: 2022-12-19

## Navigation Journal

The registered URL is a direct link to a PDF hosted on ModMed's WordPress site.

1. **Initial probe:**
   ```bash
   curl -sI -L "https://www.modmed.com/wp-content/uploads/2023/11/Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: application/pdf, 683,823 bytes. Direct download, no redirects, no authentication.

2. **Download:**
   ```bash
   curl -sL "https://www.modmed.com/wp-content/uploads/2023/11/Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf
   ```
   Verified: `file` reports "PDF document, version 1.4", 131 pages per `pdfinfo`.

3. **PDF examination:**
   - Title: "Data Dictionary for ModMed EMA EHI Export"
   - Producer: Skia/PDF m121 Google Docs Renderer (created in Google Docs)
   - 131 pages, last updated November 2023
   - No embedded files or attachments (`pdfdetach -list` reports 0)
   - No embedded URLs in the PDF text layer

4. **Text extraction:**
   ```bash
   pdftotext Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt
   ```
   Clean text extraction (8,794 lines). The PDF is text-based, not scanned.

5. **Enrichment:** Parsed the extracted text into structured JSON using a Bun TypeScript script
   (see `downloads/enrichment/`). Result: 197 tables, 4,784 columns across 16 groupings.

## What Was Found

The registered URL points to a single 131-page PDF titled "Data Dictionary for ModMed EMA EHI Export." This is a genuine (b)(10) EHI export data dictionary — not a relabeled FHIR/(g)(10) document. It describes a bulk export of the underlying database tables in the ModMed EMA system.

### Export Format

The export produces a **ZIP file** (`ehi_export.zip`) with two folders:
- `ehi_export/xxxx_data_extract/` — **Pipe-delimited CSV files**, one per database table, containing all structured clinical and financial data
- `ehi_export/attachments/` — Human-readable files (XML, JPEG, PNG, TIFF, JSON, PDF) containing imaging results, scanned clinical documents, lab attachments, prescription attachments, etc.

The export can be run for a single patient or for multiple/all patients.

### Data Dictionary Structure

The data dictionary is organized as a large table with five columns per entry:
- **Grouping** — logical category (e.g., Patient, Visit, PM Financials)
- **Table** — database table name (snake_case)
- **Description** — prose description of the table's purpose and cardinality
- **Columns** — list of column names (snake_case)
- **Longitudinal Tracking** — flag indicating whether the table tracks history:
  - Y = longitudinally tracked (new rows per visit, immutable once finalized)
  - N = not tracked over time (most recent snapshot)
  - L = new entry per item, but changes not tracked
  - S = static lookup table

### Table Groupings and Counts

The data dictionary defines 16 populated groupings with 197 tables and ~4,784 columns:

| Grouping | Tables | Description |
|----------|--------|-------------|
| Patient | 31 | Demographics, insurance, medical/surgical/family history, allergies, medications, problem list, immunizations |
| PM Financials | 38 | Bills, charges, payments, claims, accounts receivable, refunds, statements, adjustments |
| Ophth Pretesting | 25 | Contact lenses (wearing, trials, RGP), refraction, visual acuity, keratometry, binocular vision, cover test, color vision |
| eLab | 19 | Electronic lab orders, results, panels, observations |
| Visit | 16 | Visit records, review of systems, final/original billing codes, chart notes |
| Appointment | 10 | Appointments, waitlists, reminders, authorization, recall |
| Diagnosis | 9 | Diagnoses with DDX, ADX, body locations, morphology, measurements, referrals |
| Pathology | 5 | Pathology specimens, results, notifications; cancer logs |
| Office Flow | 5 | Facility resources, utilization tracking |
| Practice | 4 | Protocol logs, referral sources, provider mappings, consent forms |
| Document Management | 5 | File attachments, document metadata |
| Prescription | 4 | Medication Rx, eyeglass Rx, contact lens Rx |
| CC/HPI | 3 | Chief complaint / history of present illness responses and metadata |
| Inventory | 3 | Package sales, itemized package items, utilization |
| Exam | 4 | Exam elements and metadata |
| Procedure | 6 | Procedures, body locations, metadata, MIPS quality measures, wRVU |

Three additional groupings are **declared in the introduction but have no table entries** in the data dictionary:
- **Lookup** — described as "static lookup tables for medical and industry codes"
- **MIPS** — described as "MIPS scores, including overall scores and measure-specific scores"
- **Medical Lookup** — described as "static lookup tables for medical content"

### Key Notes from the Documentation

- Practice Management (PM) tables are included but will be empty for practices not using PM
- All date/timestamp fields use UTC unless the field has the `_ld` suffix (local date)
- String columns with unrestricted length have Field Length = -1
- The document notes field lengths but the data dictionary itself only lists column names, not data types or lengths

## Export Coverage Assessment

### Data Domain Coverage

**Well-covered domains:**
- **Patient demographics** — comprehensive: name, DOB, sex, gender identity, sexual orientation, race/ethnicity, language, marital status, employment, emergency contacts, preferred pronouns (178 columns in the patient table alone)
- **Insurance and billing** — exceptionally detailed: 38 PM Financials tables covering bills (131 columns), charges, payments, claims, claim submissions, accounts receivable, refunds, patient statements, payer adjustments, ERA reconciliation. This is far more billing detail than most EHI exports provide.
- **Eye care specialty data** — This is where the export shines. 25 Ophth Pretesting tables cover refraction, visual acuity, keratometry, binocular vision, cover test, color vision, diagnostic drops, contact lens fitting (soft and RGP), wearing glasses and contacts data. Plus 4 Prescription tables for medication Rx, eyeglass Rx (106 columns), and contact lens Rx (79 columns). This is genuine specialty-specific clinical data that would never appear in a FHIR US Core export.
- **Lab results** — 19 eLab tables covering orders, results, panels, observations, attachments
- **Visit/encounter data** — 16 tables covering visits, review of systems, billing diagnoses, chart notes
- **Diagnoses** — 9 tables with DDX/ADX, body locations, morphology, measurements, referrals
- **Medications** — current medication list, prescriptions (including e-prescribing details), allergy data
- **Problem list, medical/surgical/family/social history** — all present
- **Appointments and scheduling** — 10 tables including waitlists, reminders, recall
- **Pathology/cancer** — 5 tables for pathology specimens, results, and cancer log
- **Immunizations** — present
- **Documents and attachments** — 5 Document Management tables plus the attachments folder for imaging, scanned documents, etc.
- **IntraMail/messaging** — patient secure messaging tables (intra_mail, intra_mail_recipient)
- **Tasks** — office workflow tasks with notes, attachments, assignees
- **Consent forms** — consent_form_patient table

**Gaps or unclear areas:**
- **Care plans** — No explicit care plan tables visible, though care planning may be embedded in visit/procedure documentation
- **Referrals** — referral_source_link and visit_referral tables exist, but outbound referral documentation/correspondence isn't clearly represented
- **Clinical decision support alerts** — No tables documenting CDS alerts or overrides
- **Implantable devices** — The product is certified for (a)(14) implantable device list, but no explicit implantable device table appears. For an ophthalmology product, IOL (intraocular lens) data might be embedded in procedure records
- **Telehealth visits** — The product supports telehealth, but no dedicated telehealth table appears (likely recorded as a visit type)
- **Lookup/reference data** — The three empty groupings (Lookup, MIPS, Medical Lookup) are concerning. Without lookup tables, coded values in the export (e.g., status codes, type codes) cannot be interpreted by a third party. This is a meaningful documentation gap.
- **Optical orders and inventory** — The product has optical lab ordering and inventory management, but only "package" sales appear (Inventory grouping). Frame/lens ordering data is not clearly represented
- **Patient portal activity** — Beyond IntraMail, no tables for portal access logs, patient-submitted forms, or patient-initiated updates

### Export Format & Standards

This is a **proprietary pipe-delimited CSV export** of the underlying database tables. It is not FHIR, C-CDA, or any standardized format. This is actually appropriate for a (b)(10) export — it captures the full breadth of data in the system rather than trying to fit everything into a clinical summary standard.

The format is straightforward:
- One CSV file per database table, pipe-delimited
- Column names match the database schema documented in the data dictionary
- Attachments (images, PDFs, etc.) preserved in their native formats
- Relationships between tables expressed through foreign keys (e.g., `patient_id`, `visit_id`, `bill_id`)

**Could a third party reconstruct the patient record?** Mostly yes. The pipe-delimited CSVs with documented column names are machine-readable. Foreign key relationships are implicit through shared ID columns. However, without the lookup tables (Lookup, MIPS, Medical Lookup — declared but empty in the data dictionary), many coded values would be opaque. A status field containing "3" is meaningless without knowing what 3 maps to.

### Documentation Quality

**Strengths:**
- The data dictionary is substantial (131 pages, ~197 tables, ~4,800 columns)
- Every table has a prose description explaining its purpose and cardinality
- Longitudinal tracking flags clearly indicate which tables are historical vs. current snapshots
- The grouping system provides logical organization
- Export format and folder structure are clearly documented
- UTC vs. local time conventions are documented

**Weaknesses:**
- **No data types or field lengths in the main table listing** — The introduction mentions a "Field Length column of the Data Dictionary sheet" but the actual table entries only show: grouping, table name, description, column names, and tracking flag. There may be a more detailed version of this data dictionary that includes data types and lengths.
- **No value set documentation** — Coded fields (status, type, category columns) are listed but their allowed values are not documented. This is compounded by the missing Lookup/MIPS/Medical Lookup tables.
- **No relationship documentation** — Foreign key relationships are not explicitly documented; they must be inferred from column naming conventions (e.g., `patient_id` references the `patient` table)
- **No sample data or example export files** — No worked examples showing what the actual pipe-delimited output looks like
- **No import/interpretation guide** — No guidance on how to reconstruct a patient's clinical picture from the exported tables
- **Created in Google Docs** — The PDF was generated from Google Docs, suggesting it's a manually maintained document rather than auto-generated from the database schema

### Structure & Completeness

The documentation provides **table-level and column-level granularity** (table names, descriptions, and column names) but lacks the deeper metadata that would make the export truly self-describing:

- Column names: **yes** — all ~4,800 columns named
- Column descriptions: **no** — only table-level descriptions
- Data types: **no** — mentioned in intro but not present in entries
- Value sets/codes: **no** — coded fields not documented
- Relationships/foreign keys: **implicit only** — inferred from naming conventions
- Cardinality: **partial** — table descriptions often note "one row per X" or "zero or more per Y"
- Versioning: **yes** — "Last updated: November 2023"
- Change history: **no**

## Narrative Assessment

This is a **genuinely good (b)(10) export** — one of the better ones in terms of data breadth. Eyefinity/ModMed has done real work here rather than simply relabeling their FHIR API. The export covers the full spectrum of data the EHR stores: clinical encounters, eye-care-specific measurements (refraction, contact lens fitting, visual acuity), billing/financial records, lab results, prescriptions, pathology, and more. The pipe-delimited CSV format with one file per table is practical and machine-readable.

The key weakness is documentation depth rather than data breadth. The data dictionary tells you *what* is in the export (table and column names) but not *how to interpret it* (data types, coded values, relationships). The three empty groupings (Lookup, MIPS, Medical Lookup) represent a significant gap — without reference tables, a recipient of this export cannot fully interpret coded fields. A developer receiving this export would be able to identify and load the tables, but would need to guess at the meaning of many coded values.

It's worth noting that this is the **ModMed EMA** data dictionary hosted on modmed.com, not an Eyefinity-specific document. The product "EHR powered by EMA in Eyefinity Encompass" uses ModMed's EMA as its underlying EHR, so this shared data dictionary makes sense. However, the Eyefinity Practice Management data (scheduling, insurance eligibility, VSP-specific claims, optical orders) may be stored in Eyefinity's own PM system rather than in EMA. The data dictionary includes PM tables (marked as "empty for practices not using PM"), but it's unclear whether the full Eyefinity PM dataset — especially VSP-specific functionality — is captured here or lives in a separate system not covered by this export.

## Access Summary
- Final URL (after redirects): https://www.modmed.com/wp-content/uploads/2023/11/Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare present but not blocking)

## Obstacles & Dead Ends

None. The URL was a direct, publicly accessible PDF download. No authentication, no JavaScript, no anti-bot measures. The simplest possible access pattern.
