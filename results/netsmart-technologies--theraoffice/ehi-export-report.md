# Netsmart Technologies — TheraOffice — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.ntst.com/lp/certifications
- CHPL ID: 11493 (15.04.04.2816.Ther.14.00.1.240628)
- Certification date: 2024-06-28
- Product: TheraOffice v14.1

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://www.ntst.com/lp/certifications"` returned HTTP 200 with `Content-Type: text/html`. This is Netsmart's shared certifications hub page for all their products.

2. **Examined the main page** — Downloaded 190KB HTML page. Searched for TheraOffice-related links and found:
   - `/lp/certifications/ehi-all-data-theraoffice` — dedicated EHI export page for TheraOffice
   - `/-/media/pdfs/certifications/theraoffice---mandatory-disclosures-statement_v4.pdf` — mandatory disclosures
   - `/-/media/pdfs/certifications/2025-real-world-testing-plan-theraoffice_11252024.pdf` — real-world testing plan (not EHI-relevant)

3. **Navigated to the EHI page** — `curl -sL "https://www.ntst.com/lp/certifications/ehi-all-data-theraoffice"` returned 175KB HTML. The page is titled "EHI (Electronic Health Information) All Data Export | TheraOffice | Netsmart" and contains:
   - A description of the EHI export functionality
   - A "CLICK HERE" link to download: `/-/media/pdfs/certifications/ehi_export_all_tables_theraoffice_2024.zip`

4. **Downloaded the ZIP** — `curl -sL "https://www.ntst.com/-/media/pdfs/certifications/ehi_export_all_tables_theraoffice_2024.zip"` — 407KB ZIP file containing a single PDF: "EHI Export All Tables - May 2024 (TheraOffice).pdf" (556KB, 30 pages).

5. **Downloaded mandatory disclosures PDF** — 356KB, 5 pages. Contains cost/fee information and certified criteria listing. No technical EHI export details beyond listing (b)(10) as a certified criterion.

6. **Examined the PDF** — Used `pdftotext` and `pdfinfo` to analyze. 30-page document authored by "Mikolajczak-Brown, Allie" on May 30, 2024. Contains a data dictionary with 19 tables and 526 total columns. No embedded URLs or attachments.

7. **Took screenshots** of the EHI page in the browser (both viewport and full-page) to document the page layout.

## What Was Found

### EHI Export Documentation (PDF, 30 pages)

Netsmart provides a dedicated EHI export page per product. For TheraOffice, the documentation consists of a single PDF titled "EHI Export: TheraOffice Form and Table Documentation" (last updated May 29, 2024).

The documentation describes a **delimited file export** — a manual, one-time export of health data for one or more patients. Each database table is exported to its own file with a filename matching the table name. The format is described as "computable, delimited file format native to TheraOffice."

The PDF provides:
- A brief overview explaining the export mechanism
- A glossary of common fields (Id, Pat_ID, MODIFIED_USER, MODIFIED_DATE, CREATED_USER, CREATED_DATE)
- Table-by-table documentation with column names, SQL Server data types, and max lengths

The documentation also notes that "some electronic health information might not be available in a table format, such as rich text documents or images. This information is referenced in the extracts created for subsequent export."

### Tables Documented (19 tables, 526 columns)

| Table | Columns | Domain |
|-------|---------|--------|
| PAT_PROFILE | 80 | Patient demographics (name, address, contact, insurance IDs, custom fields, portal info) |
| PAT_PROFILE_CORE | 22 | Core patient attributes (language, sexual orientation, birth sex, disabilities, smoking status, previous address) |
| PAT_PROFILE_CORE_ETHNICITY | 3 | Patient ethnicity (coded) |
| PAT_PROFILE_CORE_GENDER | 3 | Patient gender identity (coded) |
| PAT_PROFILE_CORE_RACE | 3 | Patient race (coded) |
| PAT_PROFILE_USCDI_ALLERGIES | 18 | Allergies (name, type, reaction, severity, status, SNOMED/RxNorm/MED-RT codes) |
| PAT_PROFILE_USCDI_FAMILY_HISTORY | 13 | Family health history conditions (SNOMED/ICD-10 coded) |
| PAT_PROFILE_USCDI_FAMILY_MEMBER | 30 | Family member details (contact info, relationship, conditions) |
| PAT_PROFILE_USCDI_GOALS | 12 | Patient goals (description, due date, status) |
| PAT_PROFILE_USCDI_IMMUNIZATIONS | 52 | Immunization records (vaccine, administration details, lot, guardian info) |
| PAT_PROFILE_USCDI_IMMUNIZATIONS_ACKNOWLEDGEMENT | 3 | Immunization acknowledgement text |
| PAT_PROFILE_USCDI_IMPLANTDEVS | 22 | Implantable devices (UDI, serial, manufacturer, MRI safety) |
| PAT_PROFILE_USCDI_LABS | 94 | Laboratory results (comprehensive: order info, specimen, facility, provider, results) |
| PAT_PROFILE_USCDI_MEDICATIONS | 18 | Medications (name, RxNorm, dosage, frequency, route, provider) |
| PAT_PROFILE_USCDI_PROBLEMS | 12 | Problem list (SNOMED/ICD-10 coded conditions) |
| PAT_PROFILE_USCDI_PROCEDURES | 13 | Procedures (code, name, date, notes) |
| PAT_PROFILE_USCDI_PROGRAM_ADMISSION | 11 | Program admissions (admission/discharge dates, disposition, reason, type codes) |
| PAT_PROFILE_USCDI_VITALSIGNS | 26 | Vital signs (height, weight, BMI, BP, HR, respiratory rate, O2, temperature, pediatric percentiles) |
| PTCASE | 91 | Patient cases — the core clinical/billing unit (diagnosis codes ICD-9/ICD-10, insurance references, providers, co-pay, fee schedule, guarantor, billing sequence) |

## Export Coverage Assessment

### Data Domain Coverage

The export covers the USCDI/US Core clinical data classes reasonably well:

**Clearly covered:**
- Patient demographics (extensive — 80 columns including 25 custom fields)
- Allergies (with standard coded terminologies)
- Problems/conditions (SNOMED/ICD-10)
- Medications (with RxNorm)
- Lab results (extensive — 94 columns with specimen, facility, and provider details)
- Vital signs (comprehensive PT-relevant vitals including pediatric percentiles)
- Immunizations (very detailed — 52 columns)
- Procedures (CPT-coded)
- Goals
- Family health history
- Implantable devices (UDI data)
- Program admissions/encounters (admission/discharge with coded disposition)
- Some billing/case data via PTCASE (diagnosis codes, insurance references, co-pay, fee schedule, guarantor)

**Notably missing or absent from documentation:**
- **Clinical documentation / therapy notes** — This is the most significant gap. TheraOffice's core value proposition is clinical documentation for physical, occupational, and speech therapy. The product has 40+ customizable templates for evaluations, daily notes, progress notes, and treatment plans. None of these appear in the export tables. The documentation mentions that "rich text documents or images" are "referenced in the extracts" — but there is no table documenting how note content is exported, what format it takes, or what metadata accompanies it.
- **Scheduling/appointments** — Not exported (though this is generally operational data, appointment data linked to encounters may be EHI)
- **Claims and billing detail** — PTCASE has some billing metadata (insurance IDs, fee schedule type, diagnosis codes, billing sequence), but there are no tables for individual charges, CPT codes billed per visit, payment postings, ERA/remittance data, denial records, or collections data. TheraOffice is a fully integrated billing system — the billing detail is conspicuously absent.
- **E-prescribing records** — The medications table captures active medications but there are no prescription/order tables with prescriber details, pharmacy, dispense instructions, refill history, or controlled substance tracking.
- **Referral data** — PAT_PROFILE has REFERRALSOURCE_ID but there's no referral detail table (referring physician, authorization numbers, visit limits).
- **Insurance/coverage detail** — PTCASE references INSURANCE1/2/3 as integer IDs but there's no insurance detail table with plan name, subscriber info, group numbers, policy dates.
- **Documents and attachments** — No table for stored documents (scanned records, incoming faxes, uploaded files, correspondence).
- **Telehealth visit records** — No mention despite TheraOffice supporting built-in telehealth.
- **Patient portal communications** — No messaging or intake form submission data.
- **Outcome measures and assessments** — PT practices extensively use standardized outcome measures (LEFS, DASH, NDI, Oswestry, etc.). These are not represented.
- **Care plans and treatment plans** — Beyond the generic GOALS table, there's no structured treatment plan data.

### The (b)(10) vs (g)(10) Assessment

The table naming convention is revealing: 16 of the 19 tables are prefixed with `PAT_PROFILE_USCDI_*`, and the export documentation is organized on a page titled "EHI All Data Export." However, the data scope aligns almost perfectly with USCDI v1/v3 data classes rather than with "all electronic health information."

This is a textbook example of the (b)(10)/(g)(10) conflation. The export appears to have been built by creating flat-file equivalents of the USCDI data classes that would also be exposed via the (g)(10) FHIR API — demographics, allergies, medications, problems, labs, vitals, immunizations, procedures, goals, implantable devices. The `PAT_PROFILE` and `PAT_PROFILE_CORE` tables add some additional demographic detail, and `PTCASE` adds case/billing metadata, but the overall shape is "patient clinical summary" not "complete designated record set."

For a physical therapy EMR, the most critical clinical data is the therapy-specific documentation — evaluations, daily treatment notes, progress reports, discharge summaries, functional outcome measures, exercise programs. This is the data that directly drives care decisions, insurance authorization, and billing. Its absence from the export is a significant gap.

### Export Format & Standards

- **Format**: Delimited flat files (one file per table), with a SQL Server-derived schema (varchar, int, smalldatetime, etc.)
- **Standard**: Proprietary/native format — not FHIR, C-CDA, or any recognized health data standard
- **Encoding**: Not documented; presumably follows SQL Server defaults
- **Delimiter**: Not specified in the documentation (described only as "computable, delimited file format")
- **Relationships**: Tables are linked by `PAT_ID` (integer patient identifier). No explicit foreign key documentation. PTCASE has references to insurance and provider IDs but the lookup tables are not exported.
- **Terminology**: Some SNOMED, ICD-10, and RxNorm codes are included inline. Value sets for coded fields (tinyint enums like ALLERGY_TYPE, REACTION, SEVERITY) are not documented.
- **Reconstructability**: A third party could reconstruct basic patient demographics and clinical summaries. Without the reference/lookup tables for coded fields (insurance, providers, facilities, coded enums), the export would contain many integer IDs that are uninterpretable. The documentation says the tool "will also generate documentation specific to that organization's environment" — suggesting the actual export may include additional context not in this generic documentation.

### Documentation Quality

- **Readability**: The PDF is clean, well-structured, and easy to navigate with a table of contents.
- **Field definitions**: Minimal. The glossary defines 5 common fields (Id, Pat_ID, MODIFIED_USER, MODIFIED_DATE, CREATED_USER, CREATED_DATE). All other fields have no descriptions — only name, data type, and max length.
- **Value sets**: Not documented. Numerous tinyint/smallint fields are clearly coded values (ALLERGY_TYPE, REACTION, SEVERITY, STATUS, GENDER, RACE, etc.) but no value set mappings are provided.
- **Examples**: None. No sample export files or worked examples.
- **Import feasibility**: A developer could read the delimited files into a database, but without value set definitions, field descriptions, or relationship documentation, interpretation would require significant reverse engineering or access to the organization-specific documentation mentioned in the overview.

### Structure & Completeness

- **Granularity**: Column-level with data types and max lengths — the minimum for a data dictionary.
- **Descriptions**: Absent for individual columns (only 5 glossary entries for common fields).
- **Value sets**: Absent.
- **Relationships**: Implicit via naming convention (PAT_ID) but not formally documented.
- **Versioning**: Dated (May 29, 2024) but no change history.

## Narrative Assessment

Netsmart's TheraOffice EHI export documentation represents a minimal-effort compliance approach. The positive aspects are real: the export uses native delimited files (not just a FHIR repackaging), there's a dedicated documentation page, the PDF is well-organized, and the data dictionary covers 19 tables with 526 columns.

However, the export has two fundamental problems:

**First, scope.** For a product whose entire purpose is physical therapy clinical documentation, the absence of therapy notes, evaluations, treatment plans, and outcome measures from the export is a critical gap. The `PAT_PROFILE_USCDI_*` naming convention reveals the approach: the vendor built the export around USCDI data classes rather than around the data their product actually stores. The PTCASE table adds some billing context, but it's a single-table summary, not the detailed billing/claims data that TheraOffice manages. This is a USCDI clinical summary repackaged as an "all data" export, not a genuine (b)(10) export of the designated record set.

**Second, interpretability.** Even for the data that is exported, the documentation lacks the context needed to use it. Coded fields have no value set definitions. Integer foreign keys reference tables not included in the export. The delimiter character isn't specified. No examples are provided. The documentation says the export tool generates "documentation specific to that organization's environment" — which may fill some of these gaps at export time, but that organization-specific documentation is not publicly available for assessment.

## Access Summary
- Final URL: https://www.ntst.com/lp/certifications/ehi-all-data-theraoffice
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (main certifications page links to product-specific EHI page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None significant. The page and downloads were straightforward and publicly accessible.
- The ZIP contained Mac OS metadata files (`__MACOSX/`) which were ignored.
