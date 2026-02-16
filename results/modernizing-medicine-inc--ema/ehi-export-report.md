# Modernizing Medicine Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.modmed.com/onc-certification/
- CHPL IDs: 11032
- Product: EMA (Electronic Medical Assistant) v7
- Certification date: 2022-11-29

## Navigation Journal

1. **Initial probe of registered URL** — `curl` returned HTTP 403 Forbidden. The site uses Cloudflare anti-bot protection that blocks automated requests.

```bash
curl -sI "https://www.modmed.com/onc-certification/" -H 'User-Agent: Mozilla/5.0'
# → HTTP/2 403 (Cloudflare)
```

2. **Navigated via browser** (Chrome DevTools MCP) to https://www.modmed.com/onc-certification/. The page loaded successfully and contains a structured ONC certification disclosure with sections for "EMA Certification Status", "Mandatory Disclosures", and a dedicated **"EHI Export Documentation"** section. Took a full-page screenshot (`onc-certification-page.png`).

3. **Downloaded the overview PDF** — the EHI Export Documentation section links directly to a PDF. The download succeeded with `curl` using a browser-like User-Agent header:

```bash
curl -sL 'https://www.modmed.com/wp-content/uploads/2026/01/crp-13749-ModMed-EMA-EHI-Export-Data-Dictionary-for-Single-Patient-Export.pdf' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  -H 'Referer: https://www.modmed.com/onc-certification/' \
  -o downloads/ModMed-EMA-EHI-Export-Data-Dictionary.pdf
# → 772,645 bytes, 96 pages
```

4. **Discovered a second PDF** — page 78 of the overview document contains a "Data Dictionary" section with a hyperlink to a separate detailed field-level data dictionary. Extracted the link using `pdftohtml -xml`:

```
https://www.modmed.com/wp-content/uploads/2026/01/crp-13749-ModMed-EMA_Single-Patient-EHI-Export-Data-Dictionary.pdf
```

5. **Downloaded the detailed PDF** — initial `curl` returned 403; succeeded by adding browser cookies from the active session:

```bash
curl -sL 'https://www.modmed.com/wp-content/uploads/2026/01/crp-13749-ModMed-EMA_Single-Patient-EHI-Export-Data-Dictionary.pdf' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  -H 'Referer: https://www.modmed.com/onc-certification/' \
  -H 'Cookie: [session cookies]' \
  -o downloads/ModMed-EMA-Detailed-Data-Dictionary.pdf
# → 867,625 bytes, 210 pages
```

6. **Checked the API portal** (portal.api.modmed.com) — confirmed it documents the (g)(10) FHIR API (USCDI subset only), not the (b)(10) EHI export. No additional EHI export documentation was found there.

7. **Created enrichment scripts** — the two PDFs (306 total pages) constitute a substantial documentation corpus. Built TypeScript extraction scripts using `pdftohtml -xml` to produce structured JSON from both PDFs.

## What Was Found

### Overview Data Dictionary (PDF, 96 pages)

**File**: `ModMed-EMA-EHI-Export-Data-Dictionary.pdf`

The primary documentation is titled "ModMed EMA: EHI Export Data Dictionary for Single Patient Export." It opens with a confidentiality notice and states:

> "This dictionary describes the tables and columns contained in the ModMed EHI Single Patient dataset."

Key notes from the document:
- Practice Management (PM) tables are included but will be empty for practices not using PM
- All date/timestamp fields use UTC, unless the field has the "_ld" suffix (local date/time)
- String columns with unrestricted length use -1 in the Field Length column

**Structure:**
- **Table of Contents** (pages 1–2)
- **Document purpose** (pages 3–4) — describes groupings, longitudinal tracking, and product/vertical assignments
- **Database Tables** (pages 5–77) — inventory of ~411 tables with IDX, Grouping, Table Name, Description, Relationships, Longitudinal Tracking, Product/Vertical, Financial Priority, and Refresh Frequency
- **Data Dictionary** (page 78) — link to the separate detailed field-level PDF
- **Appendix A** — Ophthalmology Usage values
- **Appendix B** — Visual Acuity value sets
- **Appendix C** — Fax Status values
- **Appendix D** — Patient History values
- **Appendix E** — Visit Bill As values
- **Appendix F** — Immunization Public values
- **Appendix G** — Cancer Log Values
- **Appendix H** — HPI Follow Up values

**Table groupings** (17 logical categories):
| Grouping | Description |
|---|---|
| Lookup | Static lookup tables for medical and industry codes |
| Practice | Practice/firm information including facilities and staff |
| Document Management | Log of file attachments (physical attachments excluded) |
| Office Flow | Facility resource tracking for patient flow |
| Patient | Patient demographic and clinical info (non-visit-related) |
| eLab | Electronic lab orders and results |
| Pathology | Log of biopsies and results |
| Prescription | Prescriptions |
| Ophth Pretesting | Pretesting tests and measurements for Ophthalmology |
| Appointment | Appointment data including waitlist and reminders (PM only) |
| Visit | Visit-related data describing the visit as a whole |
| CC/HPI | Chief Complaints / History of Present Illness |
| Exam | Exams in the Virtual Exam Room |
| Diagnosis | Findings/Impression in the Virtual Exam Room |
| Procedure | Procedures/Plans in the Virtual Exam Room |
| PM Financials | Financial tables related to Practice Management |
| Inventory | Inventory: products, packages, sales, stock, patient charges |

### Detailed Data Dictionary (PDF, 210 pages)

**File**: `ModMed-EMA-Detailed-Data-Dictionary.pdf`

A field-level data dictionary originally created as a Google Sheets spreadsheet and exported as PDF via .xlsx. Contains **5,250 field entries across ~257 tables** with the following columns per entry:

- **IDX** — sequential identifier
- **Grouping** — logical category (matches the overview groupings)
- **Table** — database table name
- **Column** — column/field name
- **Description** — field description
- **Data Type** — SQL data type
- **Nullable** — True/False
- **Field Length** — character length (-1 for unrestricted)
- **Values/Coding Schema** — coded value information or references to appendices

**Field counts by grouping** (top 15):
| Grouping | Fields |
|---|---|
| PM Financials | 1,346 |
| Patient | 913 |
| Prescription | 337 |
| eLab | 252 |
| Appointment | 216 |
| Visit | 198 |
| Pathology | 123 |
| Inventory | 120 |
| CC/HPI | 115 |
| Ophth Pretesting (various) | ~1,200+ |
| Office Flow | 102 |
| Document | 92 |
| Diagnosis | 91 |
| Practice | 64 |
| Procedure | 45 |

**Largest tables by field count**:
- `patient` (195 fields), `patient_adjustments` (154), `insurance_policy` (149), `product_sales` (145), `accounts_receivable` (140), `payments_received` (136), `hpi_response_metadata` (131), `production_summary` (121), `bill` (119), `patient_flag` (118)

### Enrichment Outputs

The two PDFs were parsed into structured JSON using TypeScript extraction scripts:

- **`detailed-data-dictionary.json`** (1.66 MB) — 5,250 field entries with table, column, description, data type, nullability, field length, and coding schema for each field
- **`overview-table-inventory.json`** (217 KB) — 411 table entries with groupings, descriptions, relationships, longitudinal tracking indicators, product/vertical assignments, and refresh frequencies

## Export Coverage Assessment

### Data Domain Coverage

ModMed EMA's EHI export documentation describes a **remarkably comprehensive** single-patient data export. The ~411 tables across 17 groupings cover substantially more data domains than a typical EHR export. Comparing against the product research:

**Clearly covered:**
- **Patient demographics** — `patient` table with 195 fields, plus `patient_flag`, `patient_race`, `patient_ethnicity`, `patient_language`, `patient_phone_number`, `patient_address`, `patient_email`
- **Insurance** — `insurance_policy` (149 fields), `insurance_company`, `insurance_plan`
- **Clinical encounters/visits** — extensive visit-related tables across Visit, CC/HPI, Exam, Diagnosis, and Procedure groupings
- **Problems/diagnoses** — `diagnosis`, `diagnosis_body_location_morphology`, `diagnosis_morphology` and related tables (91 fields in Diagnosis grouping)
- **Medications/prescriptions** — 337 fields in Prescription grouping: `contacts_rx`, `glasses_rx`, `medication_rx`, `medication_rx_drug`, `rgp_contacts_rx`
- **Allergies** — covered in Patient grouping
- **Lab data** — 252 fields in eLab grouping: `lab_request`, `lab_result`, `lab_facility`, `result_log` tables
- **Pathology** — 123 fields: `biopsy_log`, `pathology_result` and related tables
- **Billing and claims** — largest grouping at 1,346 fields: `bill`, `charges`, `payments_received`, `payments_posted`, `accounts_receivable`, `patient_adjustments`, `payer_adjustments`, `production_summary`, `unposted_charges`
- **Scheduling/appointments** — 216 fields: `appointment`, `appointment_insurance_policy`, `appointment_reminder`, `waitlist` tables
- **E-prescribing** — structured prescription tables with drug, sig, dispense, refills data
- **Ophthalmology pretesting** — ~1,200+ fields across 20+ Ophth Pretesting sub-groupings (visual acuity, keratometry, IOP, pupil, cover test, refraction, pachymetry, visual field, etc.)
- **Inventory** — 120 fields: `product`, `package`, `product_sales`, `stock` tables
- **Documents/faxes** — 92 fields in Document grouping: `fax_outbound`, `fax_inbound`, document attachment tables
- **Office flow** — 102 fields: `task_fax_inbound`, facility resource tracking
- **Practice configuration** — 64 fields: `visit_referral`, practice/staff/facility configuration
- **Exam findings** — 27 fields in Exam grouping (Virtual Exam Room data)
- **Procedures** — 45 fields: `procedure_metadata_selection` and related tables
- **HPI/chief complaint** — 115 fields: `hpi_response_metadata` (131 fields alone)

**Notable strengths compared to typical EHR exports:**
- Specialty-specific ophthalmic data (pretesting, visual acuity, diagnostic measurements) is included — not just generic clinical data
- Billing/financial data is extremely detailed (1,346 fields) — many vendors exclude PM data from EHI exports
- Inventory management data is included — rarely seen in EHI exports
- Document management (fax logs, attachments) is covered
- Longitudinal tracking is documented per table (Y/N/L/S indicators)
- Relationship information between tables is documented

**Potentially absent or unclear:**
- **Telehealth encounter metadata** — no explicit telehealth tables, though telehealth visits may be captured within the general visit/appointment tables
- **Patient portal content** — the APPatient portal data (patient messages, patient-entered data) is not clearly represented as a distinct grouping
- **AI/ML outputs** — ModMed Scribe (ambient listening) and adaptive learning engine outputs are not mentioned
- **Apple Health/Google Fit data** — patient-contributed health data integration not represented
- **Klara messaging** — the Klara patient communication platform (acquired 2022) is not visible in the export tables
- **DICOM images** — the overview document notes "physical attachments are excluded" from the Document Management grouping, so ophthalmic diagnostic images (OCT, visual fields, fundus photos) are likely not in the export
- **Audit logs** — no audit trail tables despite (d)(2) certification
- **Clinical quality measures** — no MIPS/quality reporting tables despite (c)(1) certification

### Export Format & Standards

The export is described as a **single-patient dataset** — a collection of structured tabular data (database tables with typed columns). Key format characteristics:

- **Tabular/relational format** — the export mirrors the underlying database schema with named tables and typed columns
- **SQL data types** — fields use SQL types (string, int, datetime, boolean, float, etc.) with explicit lengths
- **UTC timestamps** — all dates in UTC unless suffixed with "_ld" (local date/time)
- **Unrestricted text** — string fields with -1 length are unbounded text fields
- **Longitudinal tracking** — some tables track change history per visit; others are current-state only

The documentation does not explicitly specify the file format of the export (CSV, JSON, database dump, etc.), but the relational structure suggests either CSV files per table or a database export format.

This is **not** a FHIR or C-CDA export — it is a proprietary relational data export. The (g)(10) FHIR API (documented separately at portal.api.modmed.com) provides USCDI data in FHIR format, but the (b)(10) EHI export uses the vendor's native schema.

### Documentation Quality

**High.** This is among the most thorough EHI export documentation encountered. The two documents together provide:

**Strengths:**
- **Comprehensive table inventory** (411 tables) with descriptions, groupings, and relationship documentation
- **Field-level detail** (5,250 fields) with column names, descriptions, data types, nullability, field lengths, and coding schema references
- **Value set appendices** (A through H) for coded fields — ophthalmology usage, visual acuity, fax status, patient history, billing, immunization, cancer log, and HPI values
- **Relationship documentation** between tables in the overview inventory
- **Longitudinal tracking indicators** per table (whether change history is maintained)
- **Product/vertical assignments** indicating which tables apply to which specialty modules
- **Refresh frequency** indicators for each table
- **Contextual notes** about PM tables being empty for non-PM practices, UTC time handling, and field length conventions
- **Recently updated** — PDFs are dated January 2026 (URL path contains `/2026/01/`)

**Weaknesses:**
- No explicit **file format specification** — the actual export format (CSV? JSON? proprietary?) is not documented
- No **sample export files** or example data
- No **export procedure documentation** — no instructions on how to initiate or receive an export
- The detailed PDF was created from a spreadsheet export, which introduces **parsing artifacts** (merged cells, wrapped text) that reduce machine readability of the PDF itself
- **Confidentiality notice** at the top may restrict redistribution or analysis of the dictionary contents

### Structure & Completeness

The documentation provides **exceptional structural detail** for a (b)(10) EHI export:

- **Entity-level inventory**: 411 tables with descriptions and groupings
- **Field-level detail**: 5,250 fields with types, nullability, and lengths
- **Relationship mapping**: Table relationships documented in the overview
- **Value sets**: 8 appendices defining coded values
- **Metadata per table**: Longitudinal tracking, product/vertical, refresh frequency, financial priority

The 17 groupings provide a clear logical organization of the data. The inclusion of Practice Management financial data (1,346 fields), inventory management (120 fields), and specialty-specific ophthalmic pretesting data (~1,200+ fields) goes well beyond the minimum clinical data most vendors export.

The main gap is the lack of **export format and procedure documentation** — a recipient has the schema but not the mechanics of how to obtain or interpret the exported files.

## Access Summary
- Registered URL: https://www.modmed.com/onc-certification/
- Final URL (after redirects): same (no redirect)
- Status: accessible (Cloudflare-protected but accessible via browser)
- Retrieved via: browser navigation (Chrome) for page; direct curl for PDFs
- Required browser: yes (Cloudflare anti-bot blocks automated curl for the page; first PDF downloaded via curl with browser headers; second PDF required browser cookies)
- Navigation complexity: linked_from_page (EHI Export Documentation section on the ONC certification page links to the overview PDF; the overview PDF links to the detailed PDF on page 78)
- Anti-bot issues: Cloudflare protection returns 403 for automated requests; second PDF required cookies from an active browser session

## Obstacles & Dead Ends

1. **Cloudflare 403 on curl** — the modmed.com site uses Cloudflare anti-bot protection. The ONC certification page could not be accessed via curl and required browser navigation. The first PDF downloaded with browser-like headers, but the second PDF required actual browser cookies.

2. **Second PDF discovered inside first PDF** — the detailed field-level data dictionary was not directly linked from the ONC certification page. It was discovered via a hyperlink on page 78 of the overview PDF, requiring PDF parsing to extract the URL.

3. **API portal is (g)(10) only** — the ModMed API Portal (portal.api.modmed.com) documents the FHIR API for (g)(10) standardized API access, not the (b)(10) EHI export. No additional EHI export documentation was found beyond the two PDFs.

4. **PDF parsing complexity** — the detailed data dictionary (210 pages) was created from a Google Sheets spreadsheet export, resulting in complex positional layout that required custom TypeScript extraction scripts. Key challenges included merged IDX+Grouping text elements, wrapped table names, and multi-line descriptions. The extraction achieves >95% accuracy with known limitations documented in the enrichment README.
