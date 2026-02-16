# Qualifacts Systems, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://documentation.qualifacts.com/ehi-export/?_gl=1*19zxd99*_gcl_au*NDg0MzU0Mzk3LjE2OTQwMTQ0NDc.
- CHPL IDs: 9807
- Product: CareLogic Enterprise S3

## Navigation Journal

1. **Initial probe** — `curl -sI -L` to the registered URL returned HTTP 200, Content-Type `text/html; charset=utf-8`, served via Cloudflare. The `_gl=` tracking parameter in the URL is irrelevant; the base path `https://documentation.qualifacts.com/ehi-export/` works fine.

2. **Fetched the landing page** (`/ehi-export/index.html`, 7,143 bytes). This is a Sphinx-generated documentation site covering all three Qualifacts platforms (CareLogic, Credible, InSync). The page describes that Qualifacts allows "designated agency users to create Single Patient and Patient Population Electronic Health Information (EHI) exports." It links to platform-specific sub-pages and separately to their FHIR API documentation (which is a different system — g(10), not b(10)).

3. **Followed the CareLogic link** to `platform/carelogic/carelogic-ehi-export.html` (8,597 bytes). This page contains:
   - Description of Single Patient Export and Patient Population Export processes
   - Technical documentation section with file type details and a data dictionary download link
   - Link to Terms of Use PDF

4. **Downloaded two files from the CareLogic page:**
   ```bash
   curl -sL "https://documentation.qualifacts.com/ehi-export/_downloads/CareLogic_EHI_Export_Data_Dictionary.xls" \
     -H 'User-Agent: Mozilla/5.0' \
     -o CareLogic_EHI_Export_Data_Dictionary.xls
   # Verified: Composite Document File V2, 987,648 bytes

   curl -sL "https://documentation.qualifacts.com/ehi-export/_downloads/Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf
   # Verified: PDF document, 3 pages, 148,904 bytes
   ```

5. **No further sub-pages or downloadable files exist** on the CareLogic documentation page. The Sphinx navigation shows CareLogic as a terminal page — no deeper sub-pages. No additional linked PDFs, schemas, API specs, or sample files.

## What Was Found

### Export Mechanism

CareLogic provides two export modes, both initiated by designated agency staff through the "EHI Export Batch Creation" page in the Administration menu:

- **Single Patient Export** — requested by patient or authorized representative through their provider. Qualifacts staff cannot provide these on behalf of agencies.
- **Patient Population Export** — requested by agency staff. Takes up to 30 calendar days. Only one can run at a time. Requires agreement to Qualifacts' Terms of Use.

Completed exports are accessed through "EHI Export Batch History" in CareLogic. Download links expire 30 days after the export file status is "Complete."

### Export Format

The export produces a **ZIP file containing comma-delimited text files (CSV), one file per data table.** An additional CSV file lists all attachments included in the ZIP. This is a genuine database-level bulk export — not a FHIR-based or standards-based subset. The format is straightforward: one CSV per table, with the data dictionary describing all tables and columns.

### Data Dictionary

The **CareLogic EHI Export Data Dictionary** (XLS, ~988KB, last saved 2025-11-17) is the core technical artifact. It is a single-sheet Excel workbook documenting:

- **671 tables** covering the full CareLogic data model
- **8,441 columns** total
- Each table has a name and description
- Each column has a name, description, and Oracle data type (VARCHAR2, NUMBER, TIMESTAMP, CLOB, etc.)
- Column descriptions include relationship references (e.g., "Link to client_program table"), cardinality context, and business logic explanations

The data dictionary is organized by table, with table-level rows containing the table name and description, followed by column-level rows with field details.

### Terms of Use

The Terms of Use PDF (September 2024) is a 3-page legal document governing EHI export usage. Key points: users must comply with HIPAA, may not use exports for purposes not permitted by ONC Certification Criteria, and exports are provided "as is." This is a legal document, not a technical one.

## Export Coverage Assessment

### Data Domain Coverage

This is one of the most comprehensive EHI export data dictionaries encountered. With 671 tables, CareLogic appears to export virtually its entire clinical and billing database. The domain coverage mapped against the product research:

**Clearly covered (with substantial depth):**

| Domain | Tables | Notes |
|--------|--------|-------|
| Service Documents & Assessments | ~310 tables | Enormous coverage — hundreds of `MOD_APS_*` assessment instrument tables (ASI, CAFAS, CANS, Risk Assessment, etc.), progress notes, clinical documentation modules, DWI program tables |
| Billing & Claims | ~51 tables | Activity details, claim items, EDI 835 remittance, GL export, client statements, cash sheets, collection batches, fee matrices |
| Insurance & Client Financials | ~20 tables | Payer plans, guarantors, client balances, liabilities, sliding scales, authorizations |
| Demographics & Contacts | ~8 tables | CLIENT_DEMOGRAPHICS, CLIENT_ADDRESS, CLIENT_CONTACT, CLIENT_RELATIONSHIP (46 cols!), name history |
| Medications & Allergies | ~15 tables | Allergy entries, ePrescribing (DrFirst Rcopia integration — ERX_* tables), medication entries, clinician-ordered medications |
| eMAR (Medication Administration) | ~11 tables | MAR_DOSE, MAR_DOSE_HISTORY, MAR_ENTRY, acknowledgement tracking |
| Program Enrollment | ~21 tables | CLIENT_PROGRAM (50 cols), episodes, preferences, screening, substance abuse data, triage |
| Clinical Document Exchange | ~14 tables | CCD/C-CDA import/export, external messaging |
| State Programs | ~22 tables | HAP (Indiana), MACSIS enrollment, state-specific assessment batches |
| Inpatient/Bed Management | ~4 tables | Bed status, bed stays, bed notes |
| DWI/Substance Abuse | ~12 tables | RIASI assessments, program recommendations, completions |
| Intake & Referral Tracking | ~10 tables | Intake tracking (35 cols), follow-ups, service request logs |
| Diagnoses | ~4 tables | Program codes (DSM-4/5, ICD-9/10), external diagnoses |
| DD/IDD Services | ~5 tables | Budgets, reimbursement vouchers, request items |
| Configurable Forms | ~5 tables | Custom form data capture |
| Quality Measures | ~4 tables | CQM reports, CRG batch assessments |
| Consent Records | ~1 table | Client consent with types and dates |
| Pregnancy | ~1 table | CLIENT_PREGNANCY (21 cols) |
| Education & Employment | ~2 tables | Assignment grades, class enrollment |
| Document Management | ~4 tables | Scanned documents, attachments, chart location |
| Provider/Pharmacy Relationships | ~5 tables | PCP, pharmacy, referring physicians |
| Internal Messaging | ~3 tables | Staff-to-staff messages |
| Implantable Devices | 1 table | Device tracking |
| HL7/ADT Events | ~15 tables | ADT event types A01–A38, HL7 batch processing |
| Waiver/Authorization | ~12 tables | WV_* tables for various waiver types |

**Potentially missing or ambiguous:**

- **Lab results**: No dedicated lab result tables visible. The product research noted lab integration but was unclear on whether results are stored. The export may include lab data within service documents (MOD_* tables) rather than in dedicated lab tables, or labs may be passed through via CCD import (CCD_IMPORT_* tables).
- **Immunization records**: No explicit immunization table, though the product is certified for (f)(1) immunization reporting. May be handled within service documents or assessments.
- **Vital signs**: No explicit vitals table. Likely captured within configurable service documents (MOD_* tables) rather than in a dedicated vitals table.
- **Telehealth session data**: The product includes telehealth functionality but no dedicated telehealth tables are visible in the export.
- **EVV (Electronic Visit Verification)**: Listed as a CareLogic module (add-on) but no EVV-specific tables appear in the data dictionary.
- **Patient portal data**: Portal-submitted forms, messages, and payment transactions are not explicitly separated as portal tables — they may flow into the main document/messaging tables.
- **Images/radiology**: No imaging tables, though this is less relevant for a behavioral health EHR.

**Appropriately excluded (operational/system data):**
- Audit logs are present (AUDIT_LOG, AUDIT_LOG_ARCHIVE, AUDIT_DELETE_VALUES) — these are included in the export though they're technically operational. This is a conservative/generous inclusion.
- DEBUG and API_ACCESS_HISTORY tables are also included — again, more than required.

### Export Format & Standards

- **Format**: CSV files in a ZIP archive, one CSV per database table. This is a straightforward, vendor-specific database dump format.
- **Standards**: Not standards-based (not FHIR, not C-CDA, not any recognized exchange format). This is appropriate — CSV dumps are arguably better for (b)(10) compliance than trying to force everything into FHIR.
- **Data types**: Oracle database types (NUMBER, VARCHAR2, TIMESTAMP, CLOB). These are documented in the data dictionary.
- **Relationships**: Foreign key relationships are documented in column descriptions (e.g., "Link to client_program table"), though there's no formal relationship diagram or foreign key specification file.
- **Reconstruction feasibility**: A third party could reconstruct the patient record from this export. The table/column descriptions are detailed enough to understand the data model. Relationships are expressed informally through "Link to [table]" descriptions. The main challenge would be understanding code/descriptor values — many columns reference descriptor tables (DESCRIPTOR_ID, etc.) which presumably have their own coded values.

### Documentation Quality

- **Readability**: The data dictionary is well-organized in a standard table/column format. Table descriptions are informative, often explaining the business context (e.g., "This table is used when the staff creates an appointment in the schedule module...").
- **Field-level definitions**: Good. Almost all columns have descriptions explaining their purpose. Data types are consistently documented with Oracle precision (e.g., NUMBER(12), VARCHAR2(200), TIMESTAMP(6)).
- **Value sets**: Partially documented. Some column descriptions mention valid values or link to descriptor tables, but there's no standalone value set or code table export. A developer would need to cross-reference descriptor/code tables to understand coded fields.
- **Examples/samples**: None. No sample export files, no worked examples.
- **Maintenance**: The XLS was last saved on 2025-11-17 by "Rob Sipe," suggesting active maintenance. The CareLogic EHI export page is copyright 2024.
- **Developer implementability**: A developer could implement an import with some effort. The schema is clear, relationships are inferrable, but coded values and descriptor lookups would require the actual data or additional documentation.

### Structure & Completeness

- **Granularity**: Excellent. Field-level documentation with data types for all 8,441 columns.
- **Coded fields**: Partially documented. Many columns reference descriptor tables (DESCRIPTOR_ID patterns), but the code values themselves are not listed in the documentation.
- **Relationships**: Informally documented via column descriptions. No formal ER diagram or foreign key constraint specification.
- **Versioning**: No explicit version number on the data dictionary, but the file metadata shows creation and save dates.

### Narrative Assessment

Qualifacts has done genuine (b)(10) work with CareLogic. This is not a repackaged FHIR API or a clinical summary subset — it is a full database-level CSV export of 671 tables spanning the entire CareLogic data model. The export clearly covers far more than US Core / USCDI: billing tables, claim processing, state program integrations, hundreds of behavioral health assessment instruments, medication administration records, bed management, intake tracking, configurable forms, and more.

The separation between their FHIR API (g(10)) and EHI export (b(10)) is clean — the documentation page explicitly links to the FHIR API page as a separate system and describes the EHI export as its own CSV-based mechanism.

The data dictionary is the sole technical artifact, and it is substantial (nearly 1MB, 9,116 rows). It provides table-level and column-level documentation with Oracle data types. The main gaps are: no sample export files, no formal relationship documentation (ERD), no value set/code table listings, and no detailed export format specification (e.g., CSV delimiter, encoding, date formats, null handling). The documentation tells you *what* data is exported but doesn't provide enough detail about *how* to parse it (quoting rules, escape characters, etc.).

For a behavioral health EHR serving 2,500+ agencies, this is a strong (b)(10) implementation. The scope is appropriate, the documentation is usable, and the export mechanism (CSV per table) is practical and transparent.

## Access Summary
- Final URL (after redirects): https://documentation.qualifacts.com/ehi-export/
- CareLogic-specific page: https://documentation.qualifacts.com/ehi-export/platform/carelogic/carelogic-ehi-export.html
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (landing page → CareLogic platform page → downloads)
- Anti-bot issues: Cloudflare present but not blocking; User-Agent header recommended

## Obstacles & Dead Ends

None. The documentation was straightforward to access:
- The registered URL loaded successfully
- The CareLogic-specific page was one click away
- Both downloadable files (XLS data dictionary, PDF terms of use) downloaded without issues
- No login walls, no JavaScript-only content, no accordion hiding
- The Sphinx-generated site renders cleanly in curl without a browser
