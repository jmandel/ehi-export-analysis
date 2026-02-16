# TRIARQ Practice Services — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://ehi.myqone.com/
- CHPL IDs: 10709
- Product: QSuite (version "Manistee")
- Certification date: 2021-11-05

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://ehi.myqone.com/" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200 with `Content-Type: text/html`, served by nginx on Google Cloud. The page is 6,952 bytes.

2. **HTML inspection**: The page is an Angular SPA (`<app-root>`) with all content rendered client-side via `main.82861f638e42f48d.js`. The raw HTML contains no documentation content.

3. **Browser navigation**: Loaded `https://ehi.myqone.com/` in Chrome. The page rendered immediately with a well-organized EHI export documentation page containing sections for CCDA, CSV, PDF, Word, and Image export formats. Took full-page screenshot.

4. **CSV detail pages**: Clicking any CSV category (e.g., "Allergy") navigates to `/syntax?ResourceType=Allergy&ResourceDescription=...` which displays a table of field definitions (Name, Description, Type). There are 27 CSV categories, each with its own detail page.

5. **JS bundle analysis**: Downloaded `main.82861f638e42f48d.js` (408 KB). Found the complete data dictionary embedded as two JavaScript arrays:
   - `resourceList`: 27 CSV export resource types with IDs and descriptions
   - `ehiexportdocs`: 777 field definitions with module, field name, type, and description

6. **Enrichment extraction**: Built a Bun TypeScript script to parse these arrays from the JS bundle into structured JSON. Extracted 32 entities (27 resource types plus 5 sub-entities for Patient Cases and Prior Authorization) with 777 total field definitions.

7. **Mandatory Disclosures PDF**: Downloaded from `https://files.triarqclouds.com/TRIARQ%20QSuite%20Disclosure%20Transparency%20Statement%2012%2007%2017.pdf` (linked in footer). 7-page document dated December 2024 listing certification criteria and costs. Lists (b)(10) in the criteria table but provides no additional EHI export technical details.

8. **Non-CSV export categories**: The PDF, Word, and Image sections on the main page list document/file types but have no field-level specifications and are not clickable — they describe which document formats are included in the export package, not structured data schemas.

## What Was Found

TRIARQ has built a dedicated Angular web application at `ehi.myqone.com` to document their EHI export. This is notably more effort than most vendors put into (b)(10) documentation.

### Export Format

The EHI Export produces a multi-format package:

1. **CCDA XML files** — HL7 C-CDA documents compliant with USCDI v3, using C-CDA R2.1 Companion Guide Release 4.1. These contain the standard clinical summary data (problems, medications, allergies, labs, vitals, immunizations, etc.).

2. **CSV files** — 27 structured data categories exported as CSV, each with a defined schema. This is the bulk of the export and covers data domains beyond what CCDA/USCDI includes. Categories span clinical, billing, administrative, and document management data.

3. **PDF files** — 8 document types exported as PDF: Patient Messages, Lab Orders Documents, Exam Notes, Patient Letters, Patient Consent, Patient Order Templates, Nurse Notes, Patient Education.

4. **Word files** — 6 document types exported as Word: Exam Notes, Nurse Notes, Billing Statements, Collections, Triage Templates, Patient Forms.

5. **Image files** — 4 image types: Driver License, Insurance Card, DMS Documents, Other.

The documentation states: "The EHI Export feature also supports generating single-patient ePHI exports as well as bulk data exports for larger patient populations. This functionality is available in QSuite Manistee v12.12 and later."

### Data Dictionary Detail

The CSV data dictionary provides field-level documentation for 777 fields across 30 modules (plus 2 parent-only categories). Each field has:
- **Name**: Column name (e.g., `PatientID`, `VisitDate`, `NDCCode`)
- **Description**: Human-readable description (e.g., "Patient Identifier", "Visit Date", "NDC Code")
- **Type**: Data type — `numeric`, `text`, or `date`

The largest entity is **Demographic** with 105 fields, covering extensive patient demographics including name, address, SSN, race, ethnicity, language, emergency contacts, employer information, and more. **Medication** has 52 fields, **Immunization** has 51, **Vitals** has 48, and **OB Vitals** has 43.

The **Patient Cases** resource type is actually a parent grouping for 4 sub-entities: Patient Cases - Master (24 fields), Patient Cases - Diagnosis (6 fields), Patient Cases - Insurance Plan (6 fields), and Patient Cases - Prior Authorization Master (20 fields). Similarly, **Prior Authorization** (16 fields) has a related **Prior Authorization Master** (20 fields) entity.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered clinical domains:**
- Demographics (105 fields — very comprehensive)
- Allergies (25 fields, including SNOMED codes and NDC codes)
- Problems/Diagnoses (21 fields)
- Medications (52 fields, including drug database IDs, NDC codes, dosages)
- Immunizations (51 fields, including CVX codes, lot numbers, manufacturer)
- Vitals (48 fields, covering standard vital signs)
- OB Vitals (43 fields — specialty-specific pregnancy data)
- Medical devices/equipment (22 fields)
- History (27 fields — past medical/surgical/family/social history)
- Care teams (33 fields)
- Primary Care Physician (33 fields)
- Lab orders documents (exported as PDF)
- Exam Notes (exported as both PDF and Word)
- Nurse Notes (exported as both PDF and Word)

**Clearly covered billing/financial domains:**
- Charges, Payments, and Adjustments (21 fields)
- Denials (14 fields)
- Refunds (11 fields)
- Reserves (8 fields)
- Insurance/eligibility (39 fields for Insurances + 16 for Eligibility)
- Guarantor (22 fields)
- Prior Authorization (16 + 20 fields across two related entities)
- Patient Cases (56 fields across 4 sub-entities)
- Billing Statements (exported as Word)
- Collections (exported as Word)

**Clearly covered administrative/communication domains:**
- Patient-Provider Messages (5 fields + PDF export)
- Referrals (33 fields)
- Appointments (15 fields)
- Pharmacy (26 fields)
- Patient Alerts (4 fields)
- Patient Consent (PDF export)
- Patient Education (PDF export)
- Patient Letters (PDF export)
- Patient Forms (Word export)
- Triage Templates (Word export)

**Clearly covered document/image domains:**
- DMS Document Index (CSV listing of all documents)
- DMS Documents (image export)
- Driver License images
- Insurance Card images
- Patient Order Templates (PDF export)

**Audit trail:**
- Audit Trail (11 fields) — included in the export, though audit logs are not strictly EHI

**Potentially missing or unclear domains:**
- **E-prescribing details**: While Medication has 52 fields, there's no separate e-prescribing or prescription history entity capturing EPCS transactions, pharmacy responses, or Surescripts data
- **Lab results (structured)**: Lab Orders Documents are exported as PDFs, but there's no CSV entity for structured lab result values. If lab results are captured as structured data in QSuite (which is likely given their lab integration features), exporting only PDFs loses queryability
- **Clinical notes content**: Exam Notes and Nurse Notes are exported as PDF and Word documents, but there's no structured CSV entity for note metadata or content — this is reasonable for free-text notes but means note metadata (author, date, note type, status) may not be separately queryable
- **QScribe AI-generated notes**: No specific mention of how AI-generated clinical notes are handled in the export
- **QPathways referral network data**: The Referrals CSV has 33 fields, but the broader QPathways care coordination data (if stored) is not specifically mentioned
- **QInsights analytics/reporting data**: No mention of exported dashboards or custom reports — though this is analytics data, not necessarily EHI
- **Patient portal access/activity data**: No entity for portal interaction data beyond Patient-Provider Messages

### Export Format & Standards

The multi-format approach is thoughtful and well-suited to the data:

- **CCDA for clinical summaries**: Appropriate use of the standard for the USCDI clinical data slice
- **CSV for structured tabular data**: Good choice for the broader data — billing, scheduling, administrative data that doesn't map well to FHIR or CCDA. CSV is widely accessible and importable.
- **PDF/Word for documents**: Appropriate for clinical notes, letters, forms, and other document-centric content
- **Images for scanned documents**: Driver licenses, insurance cards, DMS documents as image files

This is a genuine (b)(10) implementation, not a (g)(10) FHIR API relabeled. The export goes well beyond USCDI to include billing (charges, denials, refunds, reserves), insurance, prior authorization, patient cases, appointments, pharmacy, and document management data. The use of CSV for structured data and PDF/Word for documents shows the vendor understands the distinction between structured and unstructured health information.

The data types in the dictionary are limited to `numeric`, `text`, and `date` — no distinction between integer/decimal, no string length constraints, and no explicit foreign key documentation. Relationships between entities must be inferred from field naming conventions (e.g., `PatientID` appears across most entities).

### Documentation Quality

**Strengths:**
- Purpose-built web application for the documentation — not a buried PDF or afterthought
- Field-level data dictionary with 777 fields across 30+ entities
- Clear descriptions for each entity and field
- Data types specified for every field
- Searchable interface with sidebar navigation
- Comprehensive coverage of both CSV entities and non-CSV export file types

**Weaknesses:**
- Data types are coarse (`numeric`, `text`, `date`) — no precision on numeric types, no string length limits, no datetime format specification
- No value set documentation — coded fields (e.g., `HistoryStatus`, `HistoryCategory`, `Reaction`) don't list valid values
- No relationship/foreign key documentation — you must infer joins from matching field names like `PatientID` and `VisitID`
- No sample data or example export files
- No export instructions or user guide for performing the export
- CCDA export documented only by reference to HL7 standards — no vendor-specific customizations or constraints documented
- No documentation of file naming conventions, directory structure, or packaging of the export
- No documentation of how documents are associated with patients in the DMS export (only an index CSV plus image files)

### Structure & Completeness

The data dictionary is well-structured with consistent field definitions across all entities. Each field has a name, description, and type. The granularity is at the field level (column names and types), which is the right level for a CSV export format. However, the documentation stops short of being truly implementation-ready due to the lack of:

1. Value set documentation for coded fields
2. Foreign key/relationship documentation
3. Export packaging documentation (directory structure, file naming)
4. Sample data

A developer attempting to import this data could build a reasonable schema from the field definitions, but would need to reverse-engineer relationships and valid values from actual export data.

## Access Summary
- Final URL: https://ehi.myqone.com/
- Status: found
- Required browser: yes (Angular SPA, content rendered via JavaScript)
- Navigation complexity: direct_link (main page has everything; CSV detail pages are one click deep)
- Anti-bot issues: none

## Obstacles & Dead Ends

- The site is an Angular SPA, so `curl` of the HTML returns only the shell. The data dictionary is embedded in the compiled JavaScript bundle (`main.82861f638e42f48d.js`), not fetched from an API. This required parsing the JS bundle to extract structured data.
- No API endpoints detected — all data is compiled into the client-side bundle.
- The PDF, Word, and Image export categories list document types but provide no field-level or format-level specifications. This is expected since these are unstructured file exports.
