# Juno Health — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.junohealth.com/ehiexport
- CHPL IDs: 11497
- Product: Juno EHR v24
- Certification date: 2024-08-09

## Navigation Journal

### Step 1: Probe the registered URL

```bash
curl -sI -L "https://www.junohealth.com/ehiexport" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200 with `Content-Type: text/html; charset=UTF-8`. The page is hosted on HubSpot CMS, served via Cloudflare CDN. No redirects.

### Step 2: Examine the main page

The page title is "EHI Tables Export | Juno Health." The page describes:
- EHI Export as a manual one-time export of health data for one or more patients
- The export format is CSV files reflecting native database structures of Juno EHR
- Non-tabular data (images, PDFs, XML, text documents) are exported as files alongside the CSVs
- Content varies based on software applications in use, version, documentation practices, configuration decisions, and materials not sourced from Juno

The page contains four CTA buttons linking to component-specific documentation:
1. **JUNO EHR** — links to ehiexports.junohealth.com/jehr/
2. **JUNO RXTRACKER** — links to ehiexports.junohealth.com/rtvx/
3. **JUNO CONNECTEHR & JUNO CQMSOLUTION** — links to /ehiexport/connectehr-cqmsolution
4. **JUNO PATIENT PORTAL** — links to /ehiexport/juno-patient-portal

### Step 3: Follow each CTA link

The CTA buttons use HubSpot CTA redirect URLs. I resolved each:

```bash
# CTA 1: Juno EHR
curl -sI "https://cta-redirect.hubspot.com/cta/redirect/20122396/b3b31fc8-87ba-4ee1-84dc-b0c1faf4d3ac" -H 'User-Agent: Mozilla/5.0'
# → x-amz-website-redirect-location: https://ehiexports.junohealth.com/jehr/

# CTA 2: RxTracker
curl -sI "https://cta-redirect.hubspot.com/cta/redirect/20122396/c28f0214-cc82-40e9-a291-627b54cfcacc" -H 'User-Agent: Mozilla/5.0'
# → x-amz-website-redirect-location: https://ehiexports.junohealth.com/rtvx/

# CTA 3: ConnectEHR & CQMsolution
curl -sI "https://cta-redirect.hubspot.com/cta/redirect/20122396/31d75a6c-f811-422e-ac6c-5ae11ca998ad" -H 'User-Agent: Mozilla/5.0'
# → x-amz-website-redirect-location: https://www.junohealth.com/ehiexport/connectehr-cqmsolution

# CTA 4: Patient Portal
curl -sI "https://cta-redirect.hubspot.com/cta/redirect/20122396/f186372b-618b-401a-b5d7-e4466bf21021" -H 'User-Agent: Mozilla/5.0'
# → x-amz-website-redirect-location: https://www.junohealth.com/ehiexport/juno-patient-portal
```

### Step 4: Download the Juno EHR data dictionary

```bash
curl -sL "https://ehiexports.junohealth.com/jehr/" -H 'User-Agent: Mozilla/5.0' -o jehr-data-dictionary.html
```
This is a 201 KB static HTML page served from Azure blob storage (x-ms-version: 2018-03-28), last modified 2026-01-23. It's an index page listing 1,256 table documentation pages, each linked as individual `.html` files (e.g., `./AU_PRESCRIPTION.html`). Each section is organized alphabetically (A through V, with J/K/U/W/X/Y/Z having no tables).

I also downloaded a sample individual table page:
```bash
curl -sL "https://ehiexports.junohealth.com/jehr/AU_PRESCRIPTION.html" -H 'User-Agent: Mozilla/5.0'
```
This is 97 KB and documents a single table with 113 columns. Each table page includes: table description, primary key, foreign keys (with links to referenced tables), and column-level detail (ordinal position, column name, data type, and description).

### Step 5: Download the RxTracker data dictionary

```bash
curl -sL "https://ehiexports.junohealth.com/rtvx/" -H 'User-Agent: Mozilla/5.0' -o rtvx-data-dictionary.html
```
This is a 17 KB static HTML page with the same structure as the Juno EHR dictionary, listing 66 table documentation pages. Same field-level documentation format.

### Step 6: Examine ConnectEHR & CQMsolution page

```bash
curl -sL "https://www.junohealth.com/ehiexport/connectehr-cqmsolution" -H 'User-Agent: Mozilla/5.0' -o connectehr-cqmsolution-page.html
```
This HubSpot page describes:
- **ConnectEHR**: Exports single-patient and bulk data in C-CDA 2.x format. Can be scheduled or on-demand. Certified to (b)(10) under "limited ePHI USCDIv1 definition." Also supports FHIR API for DocumentReference and Bulk Data Export.
- **CQMsolution**: Exports patient-level data as QRDA I XML files (computable XML containing patient-level clinical quality data). Claims this QRDA I output "contains all EHI stored in Juno CQMsolution for each patient."

No separate data dictionary is provided for these components.

### Step 7: Examine Patient Portal page

```bash
curl -sL "https://www.junohealth.com/ehiexport/juno-patient-portal" -H 'User-Agent: Mozilla/5.0' -o patient-portal-page.html
```
This HubSpot page describes:
- Patient Portal exports single-patient and patient population downloads in C-CDA standardized format
- Certified to (b)(10) under "USCDIv1 definition"
- On-demand reports accessed via Organization > Reports > Regulatory Reports > Electronic Health Information Request

No separate data dictionary is provided.

## What Was Found

Juno Health's EHI export documentation is structured around **four certified software components**, each with its own export mechanism:

### 1. Juno EHR — CSV Table Export (Primary)

This is the core EHI export. It produces CSV files reflecting the native database schema of Juno EHR. The documentation is a comprehensive, multi-page HTML data dictionary hosted at `ehiexports.junohealth.com/jehr/`.

**Scope:** 1,256 documented database tables covering virtually every data domain in the product. The alphabetical index spans letters A through V. Each table links to an individual HTML page documenting:
- Table description (narrative explaining what the table stores)
- Primary key column(s)
- Foreign key relationships (with hyperlinks to referenced tables)
- Column-level information: ordinal position, column name, SQL data type (INT, NVARCHAR, DATETIME, etc.), and a text description

**Data domains represented** (approximate table counts by category):
- Pharmacy/Prescription: 60 tables (AU_PRESCRIPTION and related)
- Patient Demographics: 72 tables
- Billing/Financial: 72 tables (accounts, charges, claims, coverage, payments)
- Encounter/Visit: 63 tables (admissions, discharges, transfers)
- Care Plan/Treatment Plan: 59 tables
- Order management: 60 tables
- Schedule: 57 tables
- Questionnaire: 49 tables
- Observation/Vitals/Labs: 48 tables
- Document/Notes: 44 tables
- Surgery/Procedure: 36 tables
- Immunization: 33 tables
- Condition/Problem: 32 tables
- Behavioral Health: 19 tables (group sessions, behavioral health conflicts)
- Allergy: 18 tables
- Medication: 84 tables
- Radiology: 2 tables (lookup tables)
- Other/Admin: 448 tables (lookup tables, configuration, reference data)

The export includes non-tabular data (images, PDFs, XML, text documents) as files alongside the CSVs, with naming conventions linking them to references in the EHI tables.

### 2. Juno RxTracker — CSV Table Export

RxTracker (the e-prescribing module) has its own data dictionary at `ehiexports.junohealth.com/rtvx/`. Same format as the Juno EHR dictionary, covering 66 tables specific to the pharmacy/prescribing workflow:
- Patient and person records, encounters, visits
- Prescriptions, medication orders, outpatient medications
- Allergies, problems, reconciliations
- Diagnoses, procedures, labs
- Sessions, documents, notes
- Discharge requests, transfer orders

### 3. Juno ConnectEHR — C-CDA Export

ConnectEHR exports data in HL7 C-CDA 2.x format. This is explicitly described as certified to (b)(10) under the "limited ePHI USCDIv1 definition." This is essentially a USCDI-scoped clinical data export. No field-level data dictionary is provided — the format is C-CDA, which is a well-known standard.

### 4. Juno Patient Portal — C-CDA Export

Similar to ConnectEHR, the Patient Portal exports in C-CDA format. Certified to (b)(10) under "USCDIv1 definition." No separate data dictionary.

### 5. Juno CQMsolution — QRDA I XML Export

The CQM module exports patient-level data as QRDA I XML files. The documentation claims these files "contain all EHI stored in Juno CQMsolution for each patient."

## Export Coverage Assessment

### Data Domain Coverage

Juno Health's approach is notably comprehensive for the core Juno EHR component. The 1,256-table data dictionary is one of the largest and most granular EHI export schemas observed. It reflects a genuine database-level export rather than a FHIR or C-CDA translation layer.

**Clearly covered domains:**
- **Clinical records**: Conditions, observations, vital signs, lab results, diagnostic reports — extensive table coverage
- **Medications & pharmacy**: 60 AU_PRESCRIPTION tables plus 84 medication-related tables in the main EHR, plus 66 RxTracker tables — extremely thorough pharmacy coverage consistent with DSS's VA pharmacy heritage
- **Orders**: 60 order-related tables covering drug orders, non-drug orders, lab orders
- **Allergies**: 18 allergy tables with reactions, manifestations, coding
- **Immunizations**: 33 tables including forecasting, eligibility, education, lot tracking, vaccine inventory
- **Surgery/procedures**: 36 tables including perioperative records, anesthesia types, surgical case records
- **Care plans/treatment plans**: 59 tables with goals, interventions, signatures — important for behavioral health "Golden Thread"
- **Behavioral health**: 19 tables for group sessions, patient-practitioner conflicts, and behavioral health-specific data
- **Billing/financial**: 72 tables covering accounts, billing items, charges, claims, coverage, payers — genuine RCM data
- **Documents/notes**: 44 tables for clinical notes, amendment requests, document references
- **Questionnaires**: 49 tables for configurable assessments (significant for behavioral health's 400+ templates)
- **Scheduling**: 57 tables for appointments, slots, provider schedules
- **Patient demographics**: 72 tables including contact info, addresses, guardians, identifiers
- **Encounters**: 63 tables including admissions, transfers, discharges, bed status, waitlists

**Domains with some coverage but potentially incomplete:**
- **Radiology**: Only 2 lookup tables (LKRADIOLOGYOPTION, LKRADIOLOGYOPTIONTYPE). If the product integrates with external PACS, the imaging data itself may not be in the EHR database, but orders/results would be covered under the order and observation tables.
- **Public health surveillance**: The product research mentions disease surveillance and outbreak response tools. Some of this may be covered under immunization, condition, and observation tables, but specific public health reporting or syndromic surveillance tables are not immediately apparent in the index.
- **Audit logs**: No explicit audit/audit trail tables were found in the index. The product research mentions the (d)(1)-(d)(9) certifications which require audit logging. Activity logs exist within the pharmacy tables (AU_PRESCRIPTION_ACTIVITY_LOG), but a comprehensive system-wide audit trail table is not documented.
- **AI Scribe data**: The product has an AI clinical scribe feature. Whether transcription data, audio references, or AI-generated notes are captured in the export is unclear.

**Domains that appear well-covered despite initial concern:**
- **Emergency department**: While no "ED_" prefix tables exist, ED data likely resides in the encounter, observation, and clinical note tables
- **Patient portal data**: The Patient Portal has its own C-CDA export covering its data separately

### Export Format & Standards

The primary Juno EHR export is a **native database dump in CSV format** — this is arguably the most honest approach to (b)(10) compliance. Rather than mapping data through a standardized but lossy transformation (like FHIR or C-CDA), the vendor exports the raw database tables with their original column names, data types, and relationships.

**Strengths of this approach:**
- CSV is universally readable and computable
- The native schema preserves all data without lossy translations
- Foreign key documentation lets a recipient reconstruct relational data
- Field descriptions provide semantic context
- With 1,256 tables, this is clearly aiming for "everything" rather than a curated subset

**Challenges:**
- The schema is proprietary — a recipient needs the data dictionary to interpret the CSVs
- Relationships between tables must be reconstructed from foreign key documentation
- Lookup table values (the 448+ "LK" prefix tables) are documented but coded values require the lookup tables to be meaningful
- No sample data or example export files are provided

The ConnectEHR and Patient Portal C-CDA exports are secondary mechanisms with narrower scope (USCDIv1). The CQMsolution QRDA I export is limited to clinical quality measure data.

### Documentation Quality

**Juno EHR data dictionary (excellent):**
- 1,256 individual table documentation pages
- Consistent structure: description, primary key, foreign keys, column information
- Data types specified for every column (INT, NVARCHAR, DATETIME, BIT, DECIMAL, etc.)
- Natural-language descriptions for tables and columns
- Foreign key relationships with hyperlinked cross-references
- Alphabetical index with jump navigation
- Hosted on a dedicated subdomain (ehiexports.junohealth.com) suggesting deliberate investment

**RxTracker data dictionary (good):**
- Same format and quality as the Juno EHR dictionary
- 66 tables with full field-level documentation
- Descriptions are sometimes minimal ("Patients" for the PATIENTS table) but column-level descriptions are present

**ConnectEHR/CQMsolution page (minimal):**
- Describes the export process at a high level
- States C-CDA 2.x and QRDA I formats
- No field-level documentation — relies on the C-CDA and QRDA I standards themselves
- Notes "limited ePHI USCDIv1 definition" which is a useful transparency about scope

**Patient Portal page (minimal):**
- Brief process description (navigate to Reports > Regulatory Reports)
- States C-CDA format
- No data dictionary — format is the standard

**Missing elements across all:**
- No sample export files or worked examples
- No explicit value set documentation (coded fields reference lookup tables but the allowed values aren't enumerated in the dictionary)
- No versioning or changelog for the data dictionary
- No explicit mapping between table names and clinical concepts (e.g., which tables correspond to "treatment plans" vs. "care plans" is inferred from naming)

### Structure & Completeness

The Juno EHR data dictionary is remarkably granular:
- **Field-level documentation**: Yes — column name, ordinal position, data type, description for every field
- **Data types**: Specified (INT, NVARCHAR, DATETIME, BIT, DECIMAL, FLOAT, etc.)
- **Relationships**: Foreign keys documented with linked references
- **Descriptions**: Present for both tables and columns, though quality varies (some are detailed multi-sentence explanations, others are terse)
- **Cardinality/constraints**: Not explicitly documented (no nullable flags, max lengths, or cardinality indicators)
- **Value sets**: Coded fields reference lookup (LK) tables but the valid values aren't listed inline
- **Versioning**: Not documented — the dictionary was last modified 2026-01-23

The VistA heritage is evident in the AU_ prefix tables (which appear to derive from VA FileMan data structures), while the newer tables (CAREPLAN, ENCOUNTER, IMMUNIZATION) use a more modern naming convention suggesting a hybrid database architecture.

## Access Summary
- Final URL (after redirects): https://www.junohealth.com/ehiexport (no redirect)
- Data dictionary URLs: https://ehiexports.junohealth.com/jehr/ and https://ehiexports.junohealth.com/rtvx/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (main page → CTA buttons → data dictionaries)
- Anti-bot issues: none

## Obstacles & Dead Ends

None significant. The documentation was straightforward to access:
- The main page loaded cleanly with curl
- CTA redirect URLs resolved to final destinations via the `x-amz-website-redirect-location` header
- The data dictionary site (ehiexports.junohealth.com) serves static HTML from Azure blob storage with no authentication
- No JavaScript rendering required for the data dictionaries
- The HubSpot-hosted subpages (ConnectEHR, Patient Portal) also loaded cleanly with curl

The only minor complexity was that the CTA buttons on the main page use HubSpot tracking redirects rather than direct links, requiring resolution of the redirect chain to find the actual URLs.
