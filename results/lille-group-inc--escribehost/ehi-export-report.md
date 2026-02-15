# Lille Group, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://ehr.escribe.com/ehr/api/ehi-export/doc
- CHPL IDs: 10830
- Product: escribeHOST version 7.85
- Developer: Lille Group, Inc.

## Navigation Journal

The registered URL is a direct link to a single-page HTML data dictionary. No navigation was required.

```bash
# 1. Probe the URL
curl -sI -L "https://ehr.escribe.com/ehr/api/ehi-export/doc" -H 'User-Agent: Mozilla/5.0'
# Result: HTTP/2 200, content-type: text/html;charset=UTF-8, content-length: 478384

# 2. Download the page
curl -sL "https://ehr.escribe.com/ehr/api/ehi-export/doc" -H 'User-Agent: Mozilla/5.0' \
  -o downloads/ehi-export-doc.html
```

The page loaded directly — no JavaScript required, no login wall, no accordion navigation, no anti-bot measures. The HTML is a static, self-contained data dictionary with embedded CSS. No links to downloadable files (PDF, ZIP, CSV, etc.) were found in the page. No links to additional documentation pages were present. This is the entirety of the EHI export documentation.

## What Was Found

The registered URL serves a comprehensive, single-page HTML data dictionary titled **"escribeHOST EHI Export Format Documentation"** (478 KB). It documents the structure of CSV file exports that comprise the EHI export for a patient's record.

### Export format

The export format is described as:

> "The escribeHOST EHI Table Exports comprise electronic health information (EHI) from a patient's Electronic Health Record (EHR) in a machine-readable, comma-separated value (CSV) file format specific to escribeHOST, reflecting the internal tables structure."

This is a **genuine (b)(10) export** — not a repackaged FHIR/g(10) API. The vendor exports CSV files that mirror the internal database table structure, which is exactly the kind of approach that can cover the full designated record set.

### What the export includes

The documentation explicitly states that beyond the CSV data files, the export package also includes binary files:
- Encounter PDFs
- Scanned Cards
- PHR Sent Messages
- PHR Received Messages
- PHR Documents
- CCDS Imported Documents
- Patient Photos

### Data dictionary scope

The documentation covers **80 database tables** with **1,246 total columns**. Every column includes:
- Column name and ordinal position
- Data type (Oracle types: VARCHAR2, NUMBER, DATE, TIMESTAMP, CLOB)
- Primary key designation
- Nullability
- Text description (91% of columns have descriptions; 107 of 1246 lack descriptions, mostly in the last few columns of heavily-populated tables)
- NOT NULL and CHECK constraints

The documentation states it is current as of **02/09/2026 12:17 PM** for escribeHOST version **7.85**.

### Key tables by domain

| Domain | Tables | Columns | Notes |
|--------|--------|---------|-------|
| Demographics | 6 | 156 | PATIENTS alone has 112 columns — very comprehensive |
| Medications & Rx | 10 | 155 | Prescriptions, therapies, documented/not-documented, concerns |
| Lab Results | 6 | 128 | Tests, panels, reports, results, organizations |
| Reference/Lookup | 6 | 118 | Providers, users, locations, pharmacies, contacts |
| Drug History (RxHub) | 4 | 105 | PDMP history and evaluation |
| Vitals | 2 | 66 | Provider-recorded and patient-reported |
| Encounters | 1 | 56 | PE_PATIENT_ENCOUNTER with 56 columns |
| Orders | 2 | 52 | Orders and actions |
| Insurance/Eligibility | 3 | 46 | Insurance plans, eligibility, coverage |
| Surveys/Assessments | 6 | 44 | Custom survey forms with field definitions and values |
| Patient Portal | 4 | 36 | Messages sent/received, documents, activity |
| Documents | 4 | 33 | Snapshots, CCDs, scanned cards, PHR docs |
| Interventions | 2 | 26 | Interventions done and not done |
| Problems/Diagnoses | 2 | 25 | Problems and problem documentation |
| Research Studies | 3 | 23 | Study descriptions, members, sites |
| Devices | 1 | 22 | Miscellaneous medical devices |
| Patient Education | 3 | 21 | Resources, recipients, tracking |
| Family History | 2 | 20 | Relatives and their diseases |
| Transitions of Care | 2 | 19 | ToC requests and history log |
| Immunizations | 1 | 18 | Patient immunizations |
| Procedures | 1 | 17 | Patient procedures |
| Social History | 1 | 14 | Social history entries |
| Care Team | 2 | 11 | Providers and other contacts on care team |
| Programs | 2 | 9 | Program enrollments and specs |
| Amendments | 1 | 8 | Record amendment requests |
| Reconciliation | 1 | 7 | Medication reconciliation history |
| Imaging | 1 | 6 | Diagnostic imaging reports |
| Transfers | 1 | 5 | Patient transfers |

## Export Coverage Assessment

### Data Domain Coverage

**Well covered:**

- **Demographics** — The PATIENTS table alone has 112 columns covering name, sex, date of birth, SSN, marital status, language, ethnicity/race (separate tables), addresses, previous names, contacts, preferred communication methods, and much more. This is exceptionally thorough.
- **Medications and prescribing** — 10 tables covering active meds, documented/not-documented status, prescriptions (MED_RXS with 38 columns), therapies, and medication concerns (allergies). The product research highlighted e-prescribing via Surescripts, and the export includes the full prescription workflow data.
- **Allergies** — Covered via MED_CONCERNS, MED_CONCERNS_DOCUMENTED, and MED_CONCERNS_NKA_STATUS tables.
- **Problems/diagnoses** — PROBLEMS and PROBLEMS_DOCUMENTED tables.
- **Lab results** — Comprehensive coverage with 6 tables and 128 columns: lab tests, panels, reports, results, organizations, and report locations.
- **Vitals** — Both provider-recorded (VITALS, 56 columns) and patient-reported vitals.
- **Immunizations** — PATIENT_IMMUNIZATIONS with 18 columns.
- **Procedures** — PATIENT_PROCEDURES with 17 columns.
- **Clinical encounters** — PE_PATIENT_ENCOUNTER with 56 columns.
- **Documents and images** — The export includes encounter PDFs, scanned cards, patient photos, PHR documents, and imported CCDs both as referenced table data and as actual binary files in the export package.
- **Patient portal communications** — PHR sent/received messages and documents.
- **Family health history** — PATIENT_RELATIVES and PATIENT_RELATIVE_DISEASES.
- **Social history** — SOCIAL_HISTORY_ENTRIES with 14 columns.
- **Insurance and eligibility** — 3 tables covering insurance plans, eligibility, and coverage details.
- **Medical devices** — MISC_DEVICES with 22 columns covering implantable/miscellaneous devices.
- **Care team** — Health care team providers and other contacts.
- **Orders** — ORDERS (44 columns) and ORDERS_ACTIONS.
- **Interventions** — Including interventions not done (with reasons).
- **Drug history** — RxHub/PDMP drug history with 89 columns, plus evaluation records.
- **Surveys and assessments** — 6 tables covering custom survey forms, their structure (blocks, fields), and patient responses. This is important because the product research noted cardiology-specific assessments — these survey tables likely capture custom clinical data that wouldn't fit into standard FHIR resources.
- **Transitions of care** — Request and history tracking.
- **Research studies** — Study descriptions, site information, and patient enrollment.
- **Patient education** — Resources, recipients, and tracking.
- **Reconciliation** — Medication reconciliation history.
- **Record amendments** — Amendment request tracking.

**Possibly missing or ambiguous:**

- **Cardiac device monitoring data** — The product research identified cardiac device management (remote monitoring, transmission management, device recalls, alerts, billing status) as a core specialty feature. The MISC_DEVICES table covers implantable devices, but there is no dedicated table for cardiac device *transmissions*, *monitoring alerts*, or *remote monitoring sessions*. This may be because the Cardiac Signals platform is a separate product that stores this data independently, or because the cardiac monitoring workflow data is captured via the SURVEYS or PE_PATIENT_ENCOUNTER tables. This is the most notable potential gap given the product's cardiology specialty focus.
- **Billing data** — The product research noted uncertainty about whether escribeHOST has a built-in billing module or relies on external systems. The export includes insurance/eligibility data (coverage, plans) and ORDERS with fields that may include billing codes, but there are no explicit claims, charges, payments, or billing transaction tables. If billing is handled by an external system, this is correctly scoped. If any billing data resides in escribeHOST, it may be underrepresented.
- **Clinical notes text** — The PE_PATIENT_ENCOUNTER table has 56 columns and likely contains encounter-level clinical data, and DOCUMENT_SNAPSHOTS stores document snapshots. The export also includes encounter PDFs as binary files. However, there's no dedicated clinical notes table (like a PROGRESS_NOTES or ENCOUNTER_NOTES table). Clinical narrative may be stored within encounter records or exclusively as PDFs.
- **Scheduling/appointments** — Not exported, but this is correctly omitted — appointment scheduling data is generally operational, not part of the designated record set.
- **Clinical decision support data** — The product is certified for CDS, but no CDS-specific tables appear. CDS interventions may be transient/operational rather than part of the patient record.

### Export Format & Standards

The export uses **vendor-specific CSV files** that mirror the internal Oracle database table structure. This is a pragmatic and appropriate format for a (b)(10) export:

- **Format**: CSV (comma-separated values), machine-readable
- **Structure**: One CSV file per database table, reflecting the relational schema
- **Relationships**: Tables share key columns (PATIENT_ID, ACCOUNT_NAME, etc.) enabling reconstruction of the full patient record via joins
- **Binary files**: PDFs, images, and other documents are included as separate files in the export package
- **Not FHIR**: This is not a repackaged g(10) API — it's a direct database export, which is the correct approach for comprehensive EHI coverage

A third party could reconstruct the patient record from this export given the data dictionary. The relational structure is clearly documented with primary keys, foreign key hints (columns ending in _ID), and table descriptions.

### Documentation Quality

**Strengths:**
- The documentation is a single, self-contained HTML page — easy to access, no navigation required
- Every table has a description explaining its purpose
- 91% of columns have text descriptions
- Data types, nullability, and constraints are specified for every column
- Primary keys are clearly marked
- The page includes a table of contents with links to each table
- The documentation is dated (02/09/2026) and versioned (7.85), showing active maintenance
- The export format (CSV + binary files) is clearly explained upfront
- The list of binary file types included in the export is documented

**Weaknesses:**
- No sample data or example export files are provided
- No explicit foreign key relationship documentation — relationships must be inferred from column names
- No value set documentation for coded fields (e.g., what are valid values for SEX, STATUS, TYPE columns?)
- No documentation of the CSV file naming convention or directory structure of the export package
- No API documentation (the export appears to be a generated package, not an API-driven process)
- 107 columns (~9%) lack descriptions, mostly in the tail end of larger tables
- No export instructions or user guide for initiating the export

### Structure & Completeness

- **Granularity**: Field-level documentation with column names, data types, descriptions, constraints, and PK indicators. This is much more detailed than many vendors provide.
- **Coded fields**: Data types are Oracle database types (VARCHAR2, NUMBER, DATE, TIMESTAMP, CLOB). No value set/enum documentation for coded string fields.
- **Relationships**: Implicit via shared key columns. No explicit foreign key constraint documentation, but the naming convention (e.g., PATIENT_ID appears across most tables) makes relationships discoverable.
- **Versioning**: The page states the documentation is for version 7.85 as of 02/09/2026.
- **Schema formality**: No formal schema files (XSD, JSON Schema, DDL). The HTML data dictionary is the sole format.

## Access Summary
- Final URL (after redirects): https://ehr.escribe.com/ehr/api/ehi-export/doc
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL worked on the first try with a simple curl request. No authentication, no JavaScript rendering, no anti-bot measures, no redirects. This is a model of how EHI export documentation should be made accessible.
