# Epic Systems Corporation — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://open.epic.com/EHITables
- CHPL IDs: 11603, 11686, 11653, 11730 (EpicCare Inpatient Base); 11604, 11654, 11687, 11731 (EpicCare Ambulatory Base)
- Developer: Epic Systems Corporation

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://open.epic.com/EHITables"` returned HTTP 200, Content-Type `text/html; charset=utf-8`, 8,742 bytes. No redirects.

2. **Fetched main page** — `curl -sL "https://open.epic.com/EHITables" -o ehi-tables-main-page.html`. The page is titled "EHI Tables Export" and describes the export format and scope. Two key links identified:
   - `/EHITables/TechSpec` — the EHI Tables index (data dictionary)
   - `/EHITables/Download` — downloadable ZIP of the full index

3. **Downloaded ZIP** — `curl -sL "https://open.epic.com/EHITables/Download" -o ehi-tables-index.zip`. Server returned `Content-Disposition: attachment; filename="Epic EHI Tables.zip"`, Content-Type `application/x-zip-compressed`, 12,664,974 bytes. Verified: `file` reports "Zip archive data". Contains 7,674 files (7,672 table docs + `_index.htm` + `CRStyleSheet.css`).

4. **Downloaded TechSpec page** — `curl -sL "https://open.epic.com/EHITables/TechSpec" -o ehi-tables-techspec.html`. 1,077,591 bytes. This is the online version of the index — lists all table names A–W with links to individual table documentation.

5. **Extracted and parsed all 7,672 table definitions** — Extracted the ZIP (Python, due to backslash path separators), then ran a Bun/TypeScript enrichment script using cheerio to parse every `.htm` file into structured JSON. Result: 7,672 tables, 63,121 columns, 0 parse failures.

No other documentation links were found on the EHI Tables page. The page does reference FHIR Bulk Data Access and CCD/C-CDA as "standards-based" alternatives but explicitly positions the EHI Tables export as the (b)(10) mechanism.

## What Was Found

### Export Format

Epic's EHI export uses **tab-separated value (TSV) files** — one TSV file per table. The page states: "The EHI Tables export contains the electronic health information available in a patient's Epic record in a computable, tab-separated value (TSV) file format native to Epic."

This is a genuine (b)(10) export — not a repackaged FHIR API. The export is a database-style dump of Epic's Clarity reporting database tables, filtered to a specific patient. The format is proprietary to Epic and maps directly to their internal data model rather than any external standard.

### Documentation Scope

The data dictionary is remarkably comprehensive:

- **7,672 tables** documented with descriptions
- **63,121 columns** across all tables, each with name, data type, and description
- **Primary keys** specified for every table
- **Column types**: VARCHAR (32,660), NUMERIC (12,596), INTEGER (10,154), DATETIME (3,686), FLOAT (1,502), plus DATETIME UTC/Local/Attached variants
- **Discontinued column tracking**: each column has a discontinued flag

The documentation was generated 2026-02-15 from the "February 2026" release version. It is clearly auto-generated from Epic's internal data dictionary (the ZIP folder is named `DocGen_su117s2p_2026-02-15_14.10.04`).

### Data Domains Covered

Based on table name analysis and content review, the export covers an extraordinarily broad range of data:

| Domain | Tables | Examples |
|--------|--------|---------|
| Orders/procedures | 682+ (OR_ prefix) + 241 (ORDER) | OR_LOG, ORDER_MED, ORD_SPEC_QUEST |
| Anatomic pathology/specimens | 434+ (AP_ prefix) + 140 (SPEC) | AP_CLAIM_DETAILS, SPEC_RESULTS |
| Clinical documents/notes | 317+ (DOCS prefix) + 165 (NOTE) | DOCS_RCVD_RESULTS, NOTE_ENC_INFO |
| Patient demographics | 310+ (PAT_ prefix) | PATIENT, PAT_ENC, PAT_ACCT |
| Hospital/inpatient | 276+ (HSP_ prefix) | HSP_ACCOUNT, HSP_ADMIT_DIAG |
| Medications/pharmacy | 217 (MED) + 187 (RX) | MED_ADMIN, RX_PHR, CLARITY_MEDICATION |
| Claims/billing | 435 (CLAIM) + 16 (BILLING) + 23 (CHARGE) | CLM_VALUES, CHARGE_CODES |
| Lab results | 64 (LAB) + 41 (RESULT) | LAB_RESULTS, RESULT_COMPONENTS |
| Problem lists/diagnoses | 34 (PROBLEM) + 8 (DIAGNOSIS) | PROBLEM_LIST, DIAGNOSIS_INFO |
| Referrals | 65 (REFERRAL) + 48 (RFL) | REFERRAL, REFERRAL_SOURCE |
| Dental | 60 (DENTAL) | DENTAL_PROCEDURES, DENTAL_SURFACE |
| Transplant | 51 (TXP) | TXP_EPISODE, TXP_DONOR |
| Home health | 122 (HH) | HH_PAT_PLAN_CARE, HH_EPISODES |
| MyChart/patient portal | 65 (MYC) | MYC_MESG, MYC_PT_PREFERENCES |
| Allergies | 5 | ALLERGY, ALLERGY_REACTIONS |
| Immunizations | 1 | IMMUNIZATIONS |
| Vitals | 2 | IP_FLWSHT_REC (flowsheet data) |
| Imaging | 12 | IMAGE_STUDY, IMAGE_PROCEDURE |
| Insurance | 3 | INSURANCE_INFO |

### Non-tabular Data

The landing page notes: "Some electronic health information might not be available in a table format, such as rich text documents or images. This information might be referenced from the EHI Tables, but the actual files can be reviewed in a separate download in the export." This indicates the TSV export is accompanied by a separate file download for documents and images.

### Caveats Documented by Epic

The page lists several factors that may cause export content to vary:
1. Software applications in use at the health system
2. Software version in use
3. Documentation and software use practices
4. Configuration decisions by the health system
5. Materials not sourced from Epic

## Export Coverage Assessment

### Data Domain Coverage

This is one of the most comprehensive EHI exports documented by any vendor. With 7,672 tables and 63,121 columns, Epic's export covers essentially every data domain their platform stores:

**Clearly covered:**
- Demographics, contacts, insurance (PATIENT, PAT_*, COVERAGE_*, INSURANCE_*)
- Diagnoses, problem lists (PROBLEM_LIST, DIAGNOSIS_*, DX_*)
- Medications, prescriptions, MAR (MED_*, RX_*, CLARITY_MEDICATION, ORDER_MED)
- Lab results, pathology (LAB_*, RESULT_*, AP_*, SPEC_*)
- Vital signs, flowsheets (IP_FLWSHT_*, FLWSHT_*)
- Allergies (ALLERGY, ALLERGY_*)
- Immunizations (IMMUNIZATIONS)
- Procedures, surgical records (OR_*, PROCEDURE_*, ORD_*)
- Clinical notes (DOCS_*, NOTE_*, HNO_*)
- Billing, charges, claims (ACCOUNT*, CLM_*, CHARGE_*, ARPB_*, HSP_TRANSACTIONS)
- Specialty clinical data: dental (DENTAL_*), transplant (TXP_*), oncology (case/treatment tables), cardiology (ACCCATH*), OB (OB_*)
- Documents, images (DOCS_*, IMAGE_*, DOCUMENT_*)
- Referrals (REFERRAL_*, RFL_*)
- Home health (HH_*)
- MyChart/patient portal (MYC_*)
- Care plans, goals (PATIENT_GOALS, PAT_PLAN_*)

**Not obviously present but may be embedded in generic tables:**
- Telehealth encounter data (may be in PAT_ENC with encounter type flags)
- Specific oncology chemotherapy protocols (may be in ORDER_MED or specialty tables)

This is emphatically **not** a (g)(10) FHIR API repackaged as (b)(10). This is a raw database export covering the full breadth of Epic's data model. The presence of 435 claims-related tables alone demonstrates genuine (b)(10) intent — FHIR US Core has no claims resources.

### Export Format & Standards

- **Format**: Tab-separated values (TSV), one file per table
- **Standard**: Proprietary Epic format mapping to Clarity/Caboodle data warehouse schema
- **No FHIR, no C-CDA**: This is explicitly not a standards-based export. Epic offers FHIR Bulk Data and C-CDA separately for standards-based exchange, but the EHI export uses their native format.
- **Relationships**: Tables reference each other via ID columns (e.g., `PAT_ID`, `PAT_ENC_CSN_ID`, `ORDER_ID`). Foreign key relationships are described in column descriptions (e.g., "This column is frequently used by other tables to link to PATIENT") but are not formally specified in a separate relationship document.
- **Reconstructability**: A competent developer with this data dictionary could reconstruct patient records from the TSV files. The ID-based linking is consistent and well-documented. However, understanding the full relational model requires reading thousands of column descriptions — there is no ER diagram or formal relationship specification.

### Documentation Quality

**Strengths:**
- Auto-generated from the live system, ensuring it matches the actual export
- Every table has a description explaining what it stores
- Every column has a name, type, and description
- Primary keys are explicitly specified
- Discontinued columns are flagged
- Generated from the current release version with a timestamp
- Available as both an online web page and a downloadable ZIP
- Publicly accessible with no login required

**Weaknesses:**
- No ER diagram or formal relationship model between tables
- No value set/code system documentation (columns are described as "category value" without listing valid values)
- No sample export files or example data
- No export instructions (how to trigger the export, what the output directory looks like)
- No file format specification beyond "TSV" (encoding, delimiter details, quoting rules, null representation)
- Descriptions sometimes say "May contain organization-specific values: Yes" without elaboration
- Some encoding artifacts (curly quotes rendered as `�` due to cp1252/UTF-8 mismatch)
- No changelog or versioning beyond the generation timestamp

### Structure & Completeness

**Granularity**: Excellent at the table and column level — field names, data types, ordinal positions, descriptions, and discontinued status are all present. This is one of the most granular EHI export data dictionaries in the industry.

**Coded fields**: Documented with "category value" labels (e.g., `STATE_C_NAME` described as "The category value corresponding to the state") but the actual code values are not listed. This is a significant gap — a consumer of the export would know a column contains a coded value but not what the valid codes are.

**Relationships**: Implicitly documented in column descriptions ("This column is frequently used by other tables to link to PATIENT") but not formally specified. No foreign key constraints or relationship graph.

**Versioning**: The documentation includes a generation timestamp ("2/15/2026 at 2:10 PM CT") and release version ("February 2026") but no change history relative to prior versions.

## Access Summary
- Final URL (after redirects): https://open.epic.com/EHITables
- Status: found
- Required browser: no
- Navigation complexity: one_click (main page → Download link)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The documentation was straightforward to access:
- No login required
- No JavaScript rendering needed (static HTML)
- No anti-bot measures
- Direct file download via content-disposition header
- The only minor issue was backslash path separators in the ZIP (Windows-style), requiring Python extraction instead of `unzip`.
