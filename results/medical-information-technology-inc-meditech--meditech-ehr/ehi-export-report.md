# Medical Information Technology, Inc. (MEDITECH) — EHI Export Documentation

Collected: 2026-02-17

## Source
- Registered URL: https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm
- CHPL IDs: 10925, 10926, 10927, 10929, 10930, 10931, 10935, 10972, 10973, 10979, 10981, 10982, 10984, 11018, 11742, 11743

## Navigation Journal

### Step 1: Initial probe of registered URL

```bash
curl -sI -L "https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```

Result: HTTP 200, Content-Type: text/html, 8964 bytes. No redirects. The page loads directly as static HTML — no JavaScript rendering required.

### Step 2: Fetch and examine the main page

```bash
curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexport-main.html
```

The main page is a MEDITECH "Web Utility" site with a clean HTML structure. It describes the EHI Export as producing a zip file containing machine-readable patient data. The page presents a table with two export configurations and links to detail pages.

### Step 3: Follow links to Configuration 1 and Configuration 2 detail pages

```bash
curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexportconfig1.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexportconfig1.html

curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexportconfig2.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexportconfig2.html
```

Both pages loaded successfully. Configuration 1 provides detailed section-by-section documentation of the export zip structure. Configuration 2 similarly documents its format and links to three PDF data dictionaries.

### Step 4: Check the "Regulatory EHI Export Functionality Guides" link

The main page links to `https://customer.meditech.com/en/d/21stcenturycuresact/pages/ehiexport.htm`. This URL redirects to a SAML authentication endpoint (Keycloak at accounts.meditech.com), indicating it is a customer-only portal requiring login. The documentation is not publicly accessible.

```bash
curl -sI -L "https://customer.meditech.com/en/d/21stcenturycuresact/pages/ehiexport.htm"
# Returns HTTP 302 -> Keycloak SAML login page
```

### Step 5: Download CSV data dictionary PDFs from Configuration 2

Configuration 2 links to three PDF data dictionaries:

```bash
curl -sL "https://home.meditech.com/en/d/regulatoryresources/otherfiles/608ehiexportcsv.pdf" -o 608ehiexportcsv.pdf
curl -sL "https://home.meditech.com/en/d/regulatoryresources/otherfiles/csacuteandambehiexportdrsolutionmerged.pdf" -o csacuteandambehiexportdrsolutionmerged.pdf
curl -sL "https://home.meditech.com/en/d/regulatoryresources/otherfiles/mgehiexportdrsolutionmerged.pdf" -o mgehiexportdrsolutionmerged.pdf
```

All three downloaded as valid PDF documents:
- `608ehiexportcsv.pdf`: 19 pages, 251 KB — MPM 6.08 Ambulatory CSV data dictionary
- `csacuteandambehiexportdrsolutionmerged.pdf`: 20 pages, 263 KB — Client/Server Acute & Ambulatory CSV data dictionary
- `mgehiexportdrsolutionmerged.pdf`: 20 pages, 364 KB — MAGIC Acute & Ambulatory CSV data dictionary

### Step 6: Fetch the "old" EHI Export page

Config pages reference `/en/d/restapiresources/pages/ehiexportold.htm` as the original EHI Export homepage. Fetched and saved; it contains essentially the same information as the current Config 1 page (same section structure, same descriptions).

### Step 7: Take screenshots

Navigated to each of the three main pages in Chrome and captured full-page screenshots.

## What Was Found

MEDITECH's EHI export documentation is well-structured, covering **four generations of their platform** across **16 certified products** under a single registered URL. The documentation describes a zip-file-based export mechanism explicitly designed for §170.315(b)(10) compliance — this is clearly a purposeful (b)(10) implementation, not a repackaged FHIR API.

### Export Architecture

MEDITECH uses **two export configurations** depending on the platform and which internal modules are deployed:

**Configuration 1** (Expanse 2.2, Expanse 2.1, 6.15, 6.08 Acute, Client/Server Acute, MAGIC Acute):
- Uses Health Information Management (HIM) and Scanning & Archiving with eChart (SCN)
- Produces a zip containing:
  - **Electronic Chart documents** — scanned/electronic documents organized by account, category, and subcategory (images: PNG, JPG, TIF, BMP; documents: PDF)
  - **US Core FHIR Resources.json** — Patient $everything bundle (FHIR R4, US Core STU 3.1.1)
  - **C-CDA documents** — Consolidated-CDA documents (R2.1 or R1.1)
  - **Financial reports** — Patient accounting transactions (FinancialEHI.txt), resident trust (Expanse/6.1x), cost estimation (Expanse only)
  - **Supplemental sections** varying by version: ambulatory results, authorization/referral management, immunization history, population health, utilization review, provider messages, implantable devices, patient notices, historical ambulatory data, ambulatory order summary

**Configuration 2** (MPM 6.08 Ambulatory, Client/Server Acute & Ambulatory, MAGIC Acute & Ambulatory):
- Uses Medical Records (MRI) and Data Repository (DR)
- Produces a zip containing:
  - **Patient Data CSV files** — structured tabular data with named columns, one file per namespace
  - **FHIR Resources.json** — Patient $everything bundle
  - **C-CDA documents**
  - **Clinical Reports/Documents** — physician documentation, radiology, pathology, nursing images
  - **Provider and Patient Messages**
  - **Financial Reports** (FinancialEHI.txt)
  - **External Documents/Images** — scanned/imported documents
  - **Point of Contact Scanned Documents**

### Export Metadata

Both configurations include machine-readable metadata:
- **README.txt** — Table of contents with folder/file descriptions
- **EHIEXPORTSCHEMA.txt** (Config 1) / **SCHEMA.txt** (Config 2) — Documentation URL and product version
- **Table of Contents.ndjson** (Config 1) / **JSONTOC.txt** (Config 2) — NDJSON file containing FHIR DocumentReference resources conforming to the Argonaut EHI Export API IG (draft). Each entry describes a file in the zip with its content type, path, size, creation date, encounter reference, and time period.
- **ACCOUNTS_INDEX.html/xml** (Config 1) — Browser-viewable index for human readability

### CSV Data Dictionaries (Configuration 2 only)

Three PDF data dictionaries document the tables/columns exported as CSV:

| Platform | Tables | Fields |
|----------|--------|--------|
| MPM 6.08 Ambulatory | 97 | 482 |
| Client/Server Acute & Ambulatory | 333 | 1,231 |
| MAGIC Acute & Ambulatory | 322 | 1,121 |

Key table name prefixes and the domains they represent:
- **Adm** (Admissions): demographics, insurance, next of kin, diagnoses, employers, guarantors, clinical queries, discharge info
- **Sch** (Scheduling/Care): vital signs, appointments, assessments, interventions
- **Mri** (Medical Records): chart documents, medical records data
- **Nur** (Nursing): nursing documentation, interventions, assessments
- **Pha** (Pharmacy): pharmacy orders, dispensing, medication records
- **Apr** (Ambulatory/Practice): encounters, messages, vitals, problem lists, tasks, health maintenance
- **Rxm** (Prescriptions): prescriptions, medication orders, queries
- **Arm** (Authorization/Referral Management): authorizations, referrals, insurance eligibility
- **Its** (Interface Transaction Services): likely interoperability/exchange data
- **Bbk** (Blood Bank): blood bank/transfusion data
- **Pth** (Pathology): pathology reports, specimens
- **Edm** (ED Management): emergency department data
- **Lab** (Laboratory): lab results, tests
- **Mic** (Microbiology): microbiology cultures, sensitivities
- **Pbr** (Patient Billing/Records): billing records, financial data
- **Oe** (Order Entry): orders
- **Rad** (Radiology): radiology exams, reports (MAGIC)
- **Eps** (E-Prescribing): electronic prescribing (MAGIC)
- **Hub** (Hub): interoperability hub data (C/S)

## Export Coverage Assessment

### Data Domain Coverage

MEDITECH has taken the (b)(10) requirement seriously. The export is clearly distinct from their (g)(10) FHIR API — while it includes a US Core FHIR bundle, it goes well beyond that with supplemental data exports in multiple formats.

**Domains clearly covered:**
- **Demographics & patient data**: Extensive coverage via Adm tables (admissions, visits, insurance, employers, next of kin, guarantors) and FHIR Patient resource
- **Clinical notes & documentation**: Electronic chart documents (Config 1), physician/nursing documentation (Config 2), radiology/pathology reports
- **Diagnoses & problems**: AdmVisitDiagnoses, problem lists in FHIR bundle and ambulatory data
- **Medications & prescriptions**: Rxm (prescription) tables, Pha (pharmacy) tables, FHIR MedicationRequest
- **Lab results**: Lab tables, FHIR Observation/DiagnosticReport, ambulatory results PDFs
- **Imaging/Radiology**: Rad tables (MAGIC), radiology reports in clinical documents
- **Pathology**: Pth tables, pathology report documents
- **Blood bank**: Bbk tables (C/S, MAGIC)
- **Microbiology**: Mic tables
- **Immunizations**: Dedicated section with immunization history
- **Allergies**: Via FHIR AllergyIntolerance resource
- **Vital signs**: Sch vital signs tables, FHIR Observation
- **Financial/billing data**: FinancialEHI.txt with patient accounting transactions, ResidentTrustEHI.txt, CostEstimation.txt, insurance data
- **Authorization & referral management**: ARM reports (Expanse/6.x), Arm tables (legacy)
- **Provider/patient messages**: Provider Messages section (C/S, MAGIC), Patient Notices (6.08)
- **C-CDA documents**: All structured clinical documents created by the system
- **Implantable devices**: Dedicated section (C/S, MAGIC)
- **Population health**: External aggregated data (Expanse/6.x)
- **Utilization review**: Case management utilization reviews (Expanse/6.x)
- **Care coordination**: Care Compass data via population health section
- **Scanned/external documents**: AmbScans, Point of Contact scans, Electronic Chart document images
- **ED-specific data**: Edm tables, encounter data
- **Nursing documentation**: Nur tables (C/S, MAGIC)
- **Order entry**: Oe tables
- **Ambulatory-specific data**: AprEnc encounter data, AprPat patient data, ambulatory results, historical ambulatory data

**Domains with potential gaps or ambiguity:**
- **Specialty clinical data** (oncology, mental health, L&D, surgical services, critical care, dietary): The product research shows MEDITECH stores extensive specialty-specific data across many modules (Oncology, Mental Health, Labor & Delivery, Surgical Services, Critical Care, Dietary). The export documentation does not specifically mention these specialty modules. The Electronic Chart documents and FHIR bundle might capture some of this, but there is no explicit mention of specialty-specific data exports (e.g., oncology treatment protocols, mental health assessments, L&D records).
- **Home health and hospice**: MEDITECH offers Home Health and Hospice modules, but the export documentation does not reference them.
- **Telehealth visit records**: Not mentioned in the export documentation.
- **Patient portal content** (beyond provider messages): MyHealth portal data beyond provider messages is not explicitly documented.
- **Care plan data**: The FHIR bundle may include CarePlan resources via US Core, but there is no explicit mention of detailed care plan exports.

**Not expected in export (correctly scoped):**
- System configuration, audit logs, quality metrics, provider credentialing, staff scheduling, template definitions — these are correctly excluded as non-EHI.

### Export Format & Standards

MEDITECH uses a multi-format approach that is well-suited to the breadth of data:

- **CSV files** (Config 2): Tabular data from the Data Repository. The format is well-documented with three PDF data dictionaries listing every table name, field label, and database column. However, the documentation does **not** include data types, value sets, cardinality, or relationships between tables.
- **FHIR R4 JSON** (both configs): US Core STU 3.1.1 Patient $everything bundle. This covers standard clinical data (conditions, medications, allergies, observations, etc.). Documentation points to fhir.meditech.com for resource-level details.
- **C-CDA XML** (both configs): Consolidated-CDA documents (R2.1 or R1.1). Standard clinical document format.
- **PDF/TXT/image files** (both configs): Clinical reports, financial reports, immunization records, pathology reports, and scanned documents in various formats.
- **NDJSON metadata** (both configs): FHIR DocumentReference resources indexing every file in the zip, conforming to the Argonaut EHI Export API IG draft.

The multi-format approach is reasonable — MEDITECH is exporting each data type in the format most natural to it rather than forcing everything into a single standard. CSV for structured tabular data, FHIR for US Core clinical data, C-CDA for clinical documents, and native formats for reports/images.

A third party could reconstruct a substantial portion of the patient record from this export, though the CSV data lacks relationship documentation — a consumer would need to infer foreign key relationships from naming conventions (e.g., column names ending in "ID").

### Documentation Quality

**Strengths:**
- The HTML documentation is well-organized with separate pages for each configuration
- The platform-specific section matrix clearly shows what each product version exports
- The export zip structure is documented down to folder names and file naming conventions
- The NDJSON table-of-contents schema is documented with field-level descriptions
- The CSV data dictionaries are comprehensive — 752 tables, 2,834 fields across three platform PDFs

**Weaknesses:**
- CSV data dictionaries list only Field (human label), Table name, and Column name. There are **no data types, value sets, cardinality constraints, or field descriptions**. A consumer knows that `AdmVisits.RaceID` exists but not what values it can take or what its type is.
- **No sample data or example export files** are provided. A developer has no concrete example of what the zip file looks like or what the CSV content looks like.
- Relationships between tables are not documented. The CSV tables clearly have foreign-key relationships (columns ending in "ID"), but these are not described.
- The Configuration 1 documentation describes sections at a high level (e.g., "Electronic Chart contains documents organized by category/subcategory") but has **no data dictionary** — it's entirely a folder/file format description. The actual clinical data content for Config 1 is largely described only as "US Core FHIR resources" and "C-CDA documents."
- The "Regulatory EHI Export Functionality Guides" that would provide implementation guidance are behind a customer login wall.

### Structure & Completeness

- **Config 2 CSV data dictionaries**: Granular at the field level (table + column), but lack data types, descriptions, value sets, and relationships. This is a data dictionary in name but effectively just a column listing.
- **Config 1**: No comparable data dictionary at all. The export content beyond FHIR/C-CDA is described only in terms of folder structure and file types.
- **FHIR bundle**: Documented by reference to US Core STU 3.1.1 and fhir.meditech.com — standard and well-understood.
- **C-CDA documents**: Documented by reference to C-CDA R2.1/R1.1 — standard.
- **No versioning or change history** on the documentation itself (PDFs note "Last Updated: October 2023").

### The (b)(10) vs (g)(10) Assessment

MEDITECH's approach clearly demonstrates awareness of the distinction between (b)(10) and (g)(10):

1. The export is explicitly labeled as §170.315(b)(10) and described as producing a zip file (not an API endpoint)
2. The export includes financial data, provider messages, scanned documents, pathology, blood bank, nursing documentation, and other data that goes well beyond US Core/USCDI
3. The FHIR bundle is included as one component alongside other exports, not as the sole mechanism
4. The CSV data dictionaries for legacy platforms document hundreds of database tables covering clinical, administrative, and financial domains

This is **not** a repackaged (g)(10) FHIR API. MEDITECH has built a genuine (b)(10) bulk export that attempts to cover the designated record set.

The primary concern is **completeness for Configuration 1 platforms** (Expanse, 6.x). For these newer platforms, the export relies heavily on the Electronic Chart (scanned/electronic documents) plus FHIR plus C-CDA. There are no CSV data dictionaries or structured tabular exports for Config 1. This may mean that data stored in structured database tables — beyond what US Core covers — is only exported as rendered documents (PDFs, images) rather than as structured data. A scanned lab result image is less useful than a structured lab result table.

For Configuration 2 (legacy platforms), the CSV export with 300+ tables provides genuinely comprehensive structured data coverage.

## Access Summary
- Final URL (after redirects): https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm (no redirects)
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (main page links to two config pages, config 2 links to PDFs)
- Anti-bot issues: none

## Obstacles & Dead Ends

- **Customer portal**: The "Regulatory EHI Export Functionality Guides" at `customer.meditech.com/en/d/21stcenturycuresact/pages/ehiexport.htm` requires SAML authentication. This documentation is not publicly accessible, which may violate the public accessibility expectation for (b)(10) documentation. The guides likely contain implementation instructions for healthcare organizations performing the export.
- **No data dictionary for Config 1**: The newer platforms (Expanse, 6.x) under Configuration 1 have no equivalent of the CSV data dictionaries. The documentation for these platforms is limited to describing the folder/file structure and referencing FHIR/C-CDA standards.
- **PDF text extraction**: The data dictionary PDFs use layout-based table rendering. Text extraction with `pdftotext -layout` works well, but the column structure requires careful parsing.
