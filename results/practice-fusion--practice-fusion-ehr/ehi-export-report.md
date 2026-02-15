# Practice Fusion — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.practicefusion.com/ehi-export-documentation/
- CHPL ID: 11507 (15.04.04.2924.Prac.37.01.1.240826)
- Product: Practice Fusion EHR v3.7
- Developer: Practice Fusion (a Veradigm Network solution)
- Certification date: 2024-08-26

## Navigation Journal

**Step 1: Probe the registered URL**
```bash
curl -sI -L "https://www.practicefusion.com/ehi-export-documentation/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html, 33,892 bytes. Static HTML served from S3/CloudFront. No redirects. Last-Modified: 2026-02-06.

**Step 2: Examine the landing page**
The main page lists 9 versioned releases of the EHI Export Documentation:
- v9 (Jan 12, 2026) — current
- v8 (Nov 4, 2025)
- v7 (Sep 17, 2025)
- v6 (Jul 7, 2025)
- v5 (Jun 16, 2025)
- v4 (Nov 7, 2024)
- v3 (Jul 16, 2024)
- v2 (Feb 8, 2024)
- v1 (Nov 27, 2023)

Each version links to `/ehi-export-documentation/vN/index/`. No downloadable file links (PDF, ZIP, etc.) on the page itself — the documentation is entirely HTML-based across individual subpages.

**Step 3: Navigate to v9 index**
```bash
curl -sL "https://www.practicefusion.com/ehi-export-documentation/v9/index/" -H 'User-Agent: Mozilla/5.0'
```
Result: 48,342-byte HTML page. Contains a description of the export format (TSV files), organized into 8 categories with 85 linked subpages — one per TSV file in the export.

**Step 4: Download all 85 subpages**
Each subpage (e.g., `/ehi-export-documentation/v9/patient-demographics/`) contains an HTML table with Field Name, Data type, and Field Description columns. All 85 subpages were downloaded.

**Step 5: Extract structured data dictionary**
Parsed all 85 HTML pages to extract field-level metadata into a single JSON file (`v9-data-dictionary.json`). Result: 85 tables, 1,165 total fields.

**Step 6: Version comparison**
Compared v8 to v9: v9 consolidated separate "electronic" and "manual" lab result tables into unified lab result tables, and added `lab-result-item-specimen-data.tsv` and `lab-result-tests-observation-notes.tsv` (net +3 tables: 83 in v8, 86 slugs in v9 including `index`).

## What Was Found

### Export Format
Practice Fusion exports EHI as **tab-separated value (TSV) files** — one file per data entity. The export supports both single-patient and entire-practice-population exports. This is a genuine (b)(10) implementation — a database-dump-style export of all data the EHR stores, not a repackaging of the FHIR API.

The export format is:
- **Format**: TSV (tab-separated values)
- **Encoding**: Not explicitly documented, presumed UTF-8
- **Structure**: One TSV file per data entity, with header rows
- **Relationships**: Foreign key GUIDs link tables (e.g., `PatientPracticeGuid`, `EncounterGuid`, `BillingHeaderGuid`)
- **Primary keys**: GUID-based identifiers throughout

### Data Dictionary Structure
The documentation is organized into **8 categories** containing **85 TSV files** with **1,165 total fields**:

| Category | Tables | Fields |
|----------|--------|--------|
| Demographics | 10 | 143 |
| Patient (documents/questionnaires) | 2 | 27 |
| Clinical | 30 | 346 |
| Billing and Insurance | 12 | 286 |
| Medications and Prescriptions | 11 | 125 |
| Labs | 15 | 187 |
| Referrals | 2 | 24 |
| Messaging | 3 | 27 |

### Field-Level Documentation
Each field is documented with:
- **Field Name**: The column header in the TSV file (e.g., `PatientPracticeGuid`, `BirthDate`, `EventReasonCodeSystem`)
- **Data type**: Typed with nullable indicators — types include `String`, `Guid`, `Guid?`, `DateTime`, `DateTime?`, `DateTimeOffset?`, `Boolean`, `Boolean?`, `Int32`, `Int32?`, `Int64?`, `Decimal`, `Decimal?`, `Double?`, `DateField`
- **Field Description**: Plain-English description of what the field contains

Data types used: `Boolean`, `Boolean?`, `DateField`, `DateTime`, `DateTime?`, `DateTimeOffset?`, `Decimal`, `Decimal?`, `Double?`, `Guid`, `Guid?`, `Int32`, `Int32?`, `Int64?`, `String`.

### Notable Tables

**Demographics (50 fields in patient-demographics alone)**: Comprehensive patient identity including name prefix/suffix, preferred name, previous names with end dates, SSN, death date/time, pronouns, and preferred language.

**Billing (patient-superbills.tsv — 70 fields)**: The largest single table. Includes full billing header data with rendering/supervising/referring provider details, facility info, POS codes, authorization numbers, accident details, and onset dates.

**Insurance (patient-insurances.tsv — 65 fields)**: Detailed payer information including copay amounts, attorney details (for workers' comp/personal injury), employer info, and secondary subscriber data.

**Labs (15 tables, 187 fields)**: Notably detailed lab coverage spanning orders, items, item diagnoses, item specimens, item answers, order documents, results, result tests/observations, observation diagnoses, observation notes, result documents, result item notes, result notes, and specimen data. v9 consolidated previously separate "electronic" and "manual" lab result tables.

**Encounter Events (31 fields)**: Captures clinical events with coded reason/result systems (EventReasonCodeSystem, EventResultCodeSystem), vital sign codes, measurement sites, and clinical worksheet linkage.

## Export Coverage Assessment

### Data Domain Coverage

Practice Fusion's EHI export is one of the more comprehensive (b)(10) implementations encountered. It clearly exports the **full contents of the EHR database**, not just the USCDI/US Core slice. Specific coverage:

**Clearly covered domains:**
- Patient demographics (including SOGI, race, ethnicity, tribal affiliation, occupation, financial resources)
- Clinical encounters with full event detail, observations, procedures, diagnoses, addendums
- Problem list / conditions and diagnoses
- Allergies with reactions
- Medications (current list, history, consent, encounter-level)
- Prescriptions with transaction history
- Drug alert overrides (clinical decision support audit trail)
- Immunizations with registry data and transmission history
- Lab orders (with granular item-level detail: diagnoses, specimens, answers, documents)
- Lab results (with test observations, observation diagnoses, notes, specimen data, documents)
- Vitals and clinical observations (via encounter events/observations)
- Family medical history with diagnoses
- Advance directives
- Health concerns and patient goals
- Patient education records
- Clinical worksheets (custom form responses)
- Healthcare devices (UDI tracking)
- Smoking status
- Risk scores
- Billing/superbills with diagnosis-procedure linkage, procedure modifiers, insurance assignments
- Insurance coverage (detailed payer, subscriber, attorney, employer info)
- Insurance eligibility checks
- Patient guarantor data
- Referrals with recipients
- Patient messages with recipients and attachments
- Patient documents
- Patient questionnaire responses
- Scheduling/appointments
- Care team assignments and profiles
- Provider and user profiles
- Facility information
- Pharmacies and preferred pharmacy designations

**Potentially missing or ambiguous domains:**
- **Audit logs**: No explicit audit/access log table is present. The `LastModifiedByProfileGuid` and `LastModifiedDateTimeUtc` fields on many tables provide modification tracking, but there is no dedicated access audit trail (who viewed what, when).
- **Pinned notes content**: The `pinned-notes.tsv` has only 5 fields — it's unclear whether note content is exported or just metadata.
- **Document content**: `patient-documents.tsv` tracks document metadata but it's unclear whether actual document files (PDFs, images) are included in the export or only metadata references.
- **FollowMyHealth portal data**: The patient portal (FollowMyHealth) is a separate Veradigm product. Patient portal-specific data (self-scheduling, portal access logs) may not be captured.
- **Billing services data**: For practices using Practice Fusion's managed billing service, claims lifecycle data (claims submissions, denials, payments, A/R) is processed externally. The export captures the superbill layer (the clinical-to-billing handoff) but not downstream billing operations.
- **Configuration and preference data**: Practice-level settings, template configurations, user preferences, and custom form definitions are not explicitly represented.

### Export Format & Standards

The TSV export is a pragmatic, appropriate choice for a (b)(10) EHI export:
- **Not FHIR**: This is not a repackaging of the (g)(10) FHIR API — it's a genuine database-level export
- **Relational structure**: Tables are linked via GUID foreign keys, preserving entity relationships
- **Self-describing**: TSV files with header rows are immediately usable in spreadsheets, databases, or any data processing tool
- **Complete**: 85 tables cover clinical, administrative, billing, messaging, and scheduling data

The format is well-suited to the data. A third party could reconstruct the patient record with reasonable effort, though:
- Coded fields (e.g., `EventReasonCodeSystem`, `EventReasonCode`) reference external code systems without documenting valid values
- No explicit entity-relationship diagram or foreign key documentation
- Relationships must be inferred from matching GUID field names across tables

### Documentation Quality

**Strengths:**
- Comprehensive: Every table and every field is documented
- Well-organized: 8 clear categories matching the product's functional areas
- Versioned: 9 versions since Nov 2023, with regular updates (~quarterly)
- Typed: Data types include nullable indicators (`DateTime?`, `Guid?`)
- Accessible: No login required, no JavaScript needed, clean static HTML
- Descriptions are generally useful and specific

**Weaknesses:**
- **No value set documentation**: String fields like `BillingStatus`, `EventCategory`, `Status`, `DisplayOption`, `OrderOfBenefits`, `RelationshipToInsured` are typed as `String` with descriptions like "Indicates the current billing status" — but no enumeration of valid values
- **No code system documentation**: Fields referencing code systems (`EventReasonCodeSystem`, `EventResultCodeSystem`, `VitalSignCode`) don't specify which code systems are used or what codes are valid
- **No relationship documentation**: Foreign key relationships must be inferred from matching GUID field names; there is no ERD, no explicit FK documentation
- **No sample data**: No example TSV files or sample export records are provided
- **No export instructions**: The documentation describes the output format but not how to trigger the export (presumably an EHR admin function, but the steps are not documented here)
- **No size or cardinality information**: No indication of typical row counts, file sizes, or field cardinality (which fields are always populated vs. usually null)

### Structure & Completeness

**Granularity**: Field-level documentation with data types and descriptions for all 1,165 fields across 85 tables. This is substantially more granular than most (b)(10) implementations.

**What's present**: Table names, field names, data types (with nullable indicators), field descriptions.

**What's absent**: Value sets for coded fields, entity-relationship diagrams, sample data, export procedure documentation, cardinality constraints, maximum field lengths, encoding specifications.

**Versioning**: Active maintenance with 9 versions in ~26 months. The v8-to-v9 transition shows substantive evolution (consolidation of lab result tables, addition of specimen and observation note tables), not just cosmetic updates.

### Overall Assessment

Practice Fusion has produced one of the better (b)(10) EHI export implementations. The export is a genuine, comprehensive database dump in a practical format (TSV), not a repackaging of the FHIR API. The documentation covers 85 entities spanning clinical, administrative, billing, messaging, and scheduling data — well beyond the USCDI clinical subset.

The main gaps are in documentation quality rather than coverage: coded fields lack value set documentation, relationships aren't formally specified, and there are no sample files or export instructions. These are meaningful gaps for a developer trying to import this data, but the raw coverage of the export itself is strong.

The regular versioning cadence (9 versions in 26 months) and the lab table restructuring in v9 demonstrate active maintenance, not a "compliance checkbox" exercise.

## Access Summary
- Final URL (after redirects): https://www.practicefusion.com/ehi-export-documentation/ (no redirect)
- Status: found
- Required browser: no (static HTML, all content accessible via curl)
- Navigation complexity: one_click (main page links to versioned index, index links to per-table subpages)
- Anti-bot issues: none

## Obstacles & Dead Ends
- Browser navigation timeouts when loading pages (slow third-party scripts: Drift chat widget, Google Tag Manager, HubSpot), but page content is fully accessible via curl
- No downloadable file formats (PDF, ZIP, CSV) — documentation is HTML-only, so we extracted the structured data into JSON ourselves
- No direct download link for the complete data dictionary — it's spread across 85 individual HTML pages
