# Medical Information Technology, Inc. (MEDITECH) — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm
- CHPL IDs: 10930, 10925, 10979, 10973, 10931, 10984, 11742, 11743, 10935, 11018, 10927, 10926, 10929, 10982, 10972, 10981

## Navigation Journal

### Step 1: Initial probe of registered URL

```bash
curl -sI -L "https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm" \
  -H 'User-Agent: Mozilla/5.0'
```

HTTP/2 200, Content-Type: text/html, 8,964 bytes. Direct static HTML page, no redirects.

### Step 2: Fetch and examine main page

```bash
curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexport-main.html
```

The main page is a lightweight overview describing MEDITECH's EHI Export as a ZIP file containing machine-readable patient data per §170.315(b)(10). It explains that content varies by product version, implemented applications, and organization configuration. It links to two configuration pages:

- **Configuration 1**: Expanse 2.2/2.1, 6.15, 6.08 Acute, C/S Acute, MAGIC Acute — uses HIM/SCN/PHM modules
- **Configuration 2**: 6.08 Ambulatory, C/S Acute & Ambulatory, MAGIC Acute & Ambulatory — uses MRI/DR modules

It also links to "Regulatory EHI Export Functionality Guides" on customer.meditech.com (login-required).

### Step 3: Fetch Configuration 1 details

```bash
curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexportconfig1.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexportconfig1.html
```

29,280 bytes. Detailed page documenting the export ZIP structure for Configuration 1 — lists files (README.txt, EHIEXPORTSCHEMA.txt, ACCOUNTS_INDEX.html/xml, Table of Contents.ndjson) and sections per product version (Electronic Chart, FHIR Resource Bundle, C-CDA documents, Financial Reports, etc.). Includes the NDJSON schema for the Table of Contents file (FHIR DocumentReference resources).

### Step 4: Fetch Configuration 2 details

```bash
curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexportconfig2.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexportconfig2.html
```

22,780 bytes. Documents the Configuration 2 export ZIP structure — contains CSV patient data files, FHIR bundle, C-CDA, clinical reports/documents, financial reports, provider messages, external documents, scanned documents. Critically, this page links to three PDF data dictionaries for the CSV tables.

### Step 5: Download CSV data dictionary PDFs

From Configuration 2 page, three PDF links for the CSV file specifications:

```bash
curl -sL "https://home.meditech.com/en/d/regulatoryresources/otherfiles/csacuteandambehiexportdrsolutionmerged.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o csacuteandambehiexportdrsolutionmerged.pdf

curl -sL "https://home.meditech.com/en/d/regulatoryresources/otherfiles/mgehiexportdrsolutionmerged.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o mgehiexportdrsolutionmerged.pdf

curl -sL "https://home.meditech.com/en/d/regulatoryresources/otherfiles/608ehiexportcsv.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o 608ehiexportcsv.pdf
```

All three verified as valid PDF documents:
- Client/Server Acute & Ambulatory: 30 pages, 262,764 bytes, last updated October 2023
- MAGIC Acute & Ambulatory: 48 pages, 363,475 bytes, last updated October 2023
- MPM 6.08 Ambulatory: 19 pages, 251,431 bytes, last updated October 2023

### Step 6: Check old EHI Export homepage

```bash
curl -sL "https://home.meditech.com/en/d/restapiresources/pages/ehiexportold.htm" \
  -H 'User-Agent: Mozilla/5.0' -o ehiexportold.html
```

27,779 bytes. This is an older version of the documentation page that contains similar content to Configuration 1. Both Config 1 and Config 2 pages link back to this "old" homepage.

### Step 7: Check customer portal (login-required)

```bash
curl -sI "https://customer.meditech.com/en/d/21stcenturycuresact/pages/ehiexport.htm" \
  -H 'User-Agent: Mozilla/5.0'
```

HTTP/2 302 → redirects to SAML authentication at accounts.meditech.com. The "Regulatory EHI Export Functionality Guides" require customer login. This is not publicly accessible.

### Step 8: Check FHIR documentation portal

Navigated to https://fhir.meditech.com/explorer/topic/USCore-patient-health-data in browser. This is a JavaScript SPA ("API Reference Library") documenting MEDITECH's FHIR R4 APIs for US Core Patient Health Data. This is their (g)(10) FHIR API documentation — it covers US Core STU3, STU4, STU6, STU7 implementation guides. The EHI export documentation references this site for the FHIR Resource Bundle component (Patient $everything using US Core STU 3.1.1), but the FHIR portal itself contains no EHI-export-specific content. Not downloaded as it documents the general FHIR API, not the (b)(10) export.

### Step 9: Screenshots

Full-page screenshots taken of main page, Config 1, and Config 2 pages.

## What Was Found

MEDITECH provides substantive, well-organized EHI export documentation across a three-page HTML site with linked PDF data dictionaries. The documentation is notable for its honesty about the multi-format, multi-configuration nature of the export and for covering all five MEDITECH platform generations.

### Export Format

The EHI export produces a **ZIP file** containing multiple types of content:

**Configuration 1** (Expanse 2.2/2.1, 6.15, 6.08 Acute, C/S Acute, MAGIC Acute):
- **Electronic Chart documents** — scanned/archived patient documents organized by account/category/subcategory in folder hierarchies. File formats include PNG, JPG, TIF, BMP, and PDF.
- **FHIR Resource Bundle** — `US Core FHIR Resources.json` containing all available FHIR R4 resources using Patient $everything (US Core STU 3.1.1).
- **C-CDA documents** — all structured Consolidated-CDA documents (R2.1 or R1.1) created for the patient.
- **Financial Reports** — `FinancialEHI.txt` with patient accounting transactions; `ResidentTrustEHI.txt` for long-term care; `CostEstimation.txt` (Expanse only).
- **Supplemental sections** — Ambulatory Results (PDF), Authorization & Referral Management Reports (PDF), Immunization History (PDF), Population Health (PDF), Utilization Review (PDF), Historical Ambulatory Data, Provider Messages, Implantable Devices, Patient Notices. Content varies by platform version.
- **Machine-readable index** — `Table of Contents.ndjson` using FHIR DocumentReference resources conforming to the draft EHI Export API IG.

**Configuration 2** (6.08 Ambulatory, C/S, MAGIC with MRI/DR):
- **Patient Data CSV files** — structured tabular data organized by namespace, with one CSV per data domain. These are the most granular export artifacts and are documented by the three PDF data dictionaries.
- **FHIR Resource Bundle** — same as Config 1.
- **C-CDA documents** — same as Config 1.
- **Clinical Reports/Documents** — physician documentation, radiology reports, pathology reports, nursing image documentation. Format varies by platform (PDF, DOC, TXT, PNG).
- **Financial Reports** — `FinancialEHI.txt` with patient accounting transactions.
- **Provider and Patient Messages** — messaging data (PDF or TXT + images).
- **External Documents/Images** — scanned/imported ambulatory documents in various formats.
- **Point of Contact Scanned Documents**.
- **Machine-readable index** — `JSONTOC.txt` (ndjson format).

### Data Dictionaries

The three PDF data dictionaries are the most valuable artifacts. They document the CSV tables and columns exported in Configuration 2:

| Platform | Tables | Fields | PDF Pages |
|----------|--------|--------|-----------|
| Client/Server Acute & Ambulatory | 331 | 1,231 | 30 |
| MAGIC Acute & Ambulatory | 323 | 1,121 | 48 |
| MPM 6.08 Ambulatory | 95 | 482 | 19 |

Each PDF contains a three-column table mapping: **Field** (human-readable name) → **Table** (database table name) → **Column** (database column name). Table name prefixes reveal the data domains:

- **Adm** (Admissions/Registration): demographics, insurance, employers, guarantors, next of kin, diagnoses, clinical queries
- **Apr** (Ambulatory Patient Record): encounters, vitals, health maintenance items, questionnaires, lab/micro results, family/social history, problems
- **Arm** (Authorization/Referral Management): authorizations, referrals, services
- **Bbk** (Blood Bank): transfusions, crossmatches, specimens, units
- **Edm** (Emergency Department Management): call management, departure referrals, notes, reminders
- **Hub** (Clinical Hub): patient problems, family histories, relative conditions
- **Its** (Imaging/Transcription Services): orders, exams, findings, radiation dose data
- **Lab** (Laboratory): specimens, test results, comments
- **Mic** (Microbiology): specimens, organisms, sensitivities, procedures
- **Mri** (Medical Records): allergies (coded/uncoded), patient demographics, immunizations, implantable devices, care team, insurances
- **Nur** (Nursing): interventions, activities, vital signs, assessments, I&O, pain, wounds, restraints
- **Oe** (Order Entry): orders, order details, questionnaires, medications, diagnoses
- **Pbr** (Patient Billing/Revenue): account claims, insurance, statements, transactions, charges
- **Pha** (Pharmacy): adverse drug reactions, medication administration, IV solutions, doses
- **Pth** (Pathology): specimens, addenda, blocks, histology, pictures, tissues
- **Rad** (Radiology): exams, ACR codes, findings, patient tracking, staff, queries
- **Rxm** (Prescription Management): orders, prescriptions, medication reconciliation, prior authorizations
- **Sch** (Scheduling/Surgical): appointments, OR cases, anesthesia, implants, vital signs, medications, IVs

### NDJSON Schema

Both configurations include a machine-readable table of contents using FHIR DocumentReference resources. The schema is well-documented on the Config 1 page with a pseudo-JSON example showing all fields: resourceType, id, meta (with EHI Export API IG profile), status, docStatus, type, subject (Patient reference), date, description, content (attachment with contentType, url, size, title), and context (encounter reference, period).

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains:**

MEDITECH's EHI export demonstrates genuine (b)(10) effort. The export goes significantly beyond USCDI/US Core by including:

- **Demographics & Registration** (Adm* tables) — insurance, employers, guarantors, next of kin, clinical queries
- **Clinical Documentation** — both structured (C-CDA, FHIR) and unstructured (scanned documents, images)
- **Laboratory** (Lab*, Mic*) — specimen results, microbiology organisms, sensitivities
- **Radiology/Imaging** (Its*, Rad*) — orders, exams, findings, radiation dose data, ACR codes
- **Pathology** (Pth*) — specimens, histology, tissue, specimen pictures
- **Blood Bank** (Bbk*) — transfusions, crossmatches, issued units
- **Pharmacy/Medications** (Pha*, Rxm*) — adverse drug reactions, medication administration, prescriptions, prior authorizations, medication reconciliation
- **Nursing** (Nur*) — interventions, assessments, vital signs, I&O, pain, wounds, restraints
- **Order Entry** (Oe*) — CPOE orders, questionnaires, medication orders
- **Billing/Revenue Cycle** (Pbr*) — claims, insurance, statements, transactions, charge details — this is a critical (b)(10) domain that many vendors miss
- **Scheduling/Surgical** (Sch*) — OR cases with detailed surgical documentation including implants, anesthesia, IV solutions, vital signs during surgery
- **Emergency Department** (Edm*) — call management, notes, reminders, departure referrals
- **Ambulatory** (Apr*) — encounters, vitals, health maintenance, family/social history
- **Authorization/Referral Management** (Arm*) — authorizations, referral notes
- **Immunizations** — both in FHIR bundle and separate export sections
- **Implantable Devices** — standalone section
- **Care Team** — MriPatientCareTeamMembers
- **Population Health** — aggregated external vendor data
- **Utilization Review** — case management data
- **Patient/Provider Messages** — communications
- **Financial Data** — patient accounting transactions, resident trust, cost estimates

**Domains with potential gaps or ambiguity:**

- **Oncology** — MEDITECH has a separately certified Oncology module (chemotherapy regimens, cancer staging), but no oncology-specific tables appear in the CSV data dictionaries. Oncology data may be captured within the Electronic Chart documents or C-CDA, but this is not explicit.
- **Mental Health/Behavioral Health** — no explicitly named behavioral health tables in the CSV exports. May be embedded in clinical documentation.
- **Home Health & Hospice** — no dedicated home health or hospice tables visible. These are separate MEDITECH modules and their data may not be included.
- **Long-Term Care** — the `ResidentTrustEHI.txt` file (Expanse/6.1 only) suggests some LTC coverage, but no dedicated LTC clinical tables are visible.
- **Labor & Delivery** — no OB-specific tables visible in the CSV dictionaries.
- **Dietary** — no nutrition/dietary tables.
- **Critical Care/ICU** — no ICU-specific tables, though nursing data (Nur*) may cover bedside documentation.
- **Genomics/Precision Medicine** — no genomics tables; this is a newer Expanse feature.
- **Telehealth** — no telehealth-specific data.
- **Care Plans** — no explicit care plan tables.
- **Patient Portal Activity** — no MyHealth portal interaction data (beyond messages).

**Important caveat:** The CSV data dictionaries only apply to **Configuration 2** platforms (older C/S, MAGIC, 6.08 Ambulatory). For **Configuration 1** platforms (Expanse, 6.15, 6.08 Acute, C/S Acute, MAGIC Acute), there is **no corresponding field-level data dictionary**. The export contents are described only at the section level (Electronic Chart documents, FHIR bundle, C-CDA, financial reports, etc.), with no field-level documentation for what's inside those sections beyond the FHIR US Core profile and C-CDA standards.

### Export Format & Standards

The export uses a **hybrid multi-format approach**:
- FHIR R4 (US Core STU 3.1.1) for structured clinical data
- C-CDA R2.1/R1.1 for clinical document exchange
- CSV files for tabular database data (Config 2 only)
- PDF/TXT for reports (financial, clinical, administrative)
- Image files (PNG, JPG, TIF, BMP) for scanned documents
- NDJSON (FHIR DocumentReference) for the table of contents/index

This is a thoughtful approach that combines standards-based formats (FHIR, C-CDA) with raw database exports (CSV) and document archives (images, PDFs). The FHIR component is explicitly US Core / USCDI-scoped via Patient $everything, while the supplemental sections (financial reports, CSV tables, scanned documents) extend coverage beyond USCDI.

The NDJSON table of contents using FHIR DocumentReference resources is a notable design choice — it provides machine-readable metadata for navigating the export contents, conforming to the draft Argonaut EHI Export API IG.

A third party could reasonably reconstruct a patient record from this export, though the mix of formats would require handling multiple parsers. The CSV tables (Config 2) provide the most granular, machine-processable data. The Config 1 export relies more heavily on documents (scanned charts, C-CDA, FHIR bundle) which, while comprehensive, may be harder to extract discrete data from.

### Documentation Quality

**Strengths:**
- Well-organized three-tier documentation (overview → configuration → data dictionary)
- Clear differentiation by platform version — each product line's export contents are enumerated
- Machine-readable NDJSON schema is documented with pseudo-JSON examples
- CSV data dictionaries provide field-level mappings for 749 tables and 2,834 fields across three platforms
- File naming conventions and folder structures are clearly documented
- Last updated dates are provided (October 2023)

**Weaknesses:**
- **No data dictionary for Configuration 1** — the Expanse and 6.15 platforms (the modern, most-deployed versions) lack field-level documentation. A developer receiving an Expanse EHI export would know the folder structure and that it contains a FHIR bundle and C-CDA documents, but would not have MEDITECH-specific field documentation beyond the standard specs.
- **No sample export files** — no example ZIP, sample CSV, sample FHIR bundle, or sample C-CDA provided
- **No data type definitions** — the CSV data dictionaries list Field/Table/Column but not data types, constraints, cardinality, or value sets
- **No relationship documentation** — no entity-relationship diagrams or foreign key documentation for the CSV tables
- **Financial report format undocumented** — `FinancialEHI.txt`, `ResidentTrustEHI.txt`, and `CostEstimation.txt` are mentioned but their internal format/schema is not documented
- **"Regulatory EHI Export Functionality Guides" are login-required** — the customer portal contains additional guides that are not publicly accessible, which is problematic for a (b)(10) requirement that should be publicly documented

### Structure & Completeness

The documentation provides:
- **Table-level granularity** for CSV exports (749 tables across platforms)
- **Field-level granularity** limited to field name, source table, and column name — no data types, descriptions, or constraints
- **No coded value sets** — fields ending in "ID" (e.g., DispositionID, RelationshipID, InsuranceID) are clearly coded values, but their allowed values are not documented
- **No relationship mappings** — tables share naming conventions (e.g., AdmVisits/AdmVisitDiagnoses/AdmVisitNextOfKin) suggesting parent-child relationships, but these are not formally documented
- **No versioning** beyond "Last Updated: October 2023" — no changelog or version history

## Access Summary
- Final URL (after redirects): https://home.meditech.com/en/d/restapiresources/pages/ehiexport.htm
- Status: found
- Required browser: no (static HTML, but browser used for screenshots and FHIR portal check)
- Navigation complexity: one_click (main page links to two configuration sub-pages)
- Anti-bot issues: none

## Obstacles & Dead Ends

1. **Customer portal login wall** — The "Regulatory EHI Export Functionality Guides" at `customer.meditech.com/en/d/21stcenturycuresact/pages/ehiexport.htm` redirect to SAML authentication. Additional EHI export documentation may exist behind this login that is not publicly accessible.

2. **FHIR portal is SPA** — `fhir.meditech.com` is a JavaScript SPA that cannot be scraped with curl. However, inspection via browser confirmed it contains standard US Core FHIR API documentation, not EHI-export-specific content.

3. **No downloadable export samples** — Despite thorough documentation of the export structure, no sample/example export files are provided anywhere on the public site.

4. **Missing Configuration 1 data dictionary** — The most deployed platforms (Expanse 2.2, Expanse 2.1) lack the field-level CSV data dictionary that exists for the older Configuration 2 platforms. This is the most significant documentation gap. Configuration 1's export is document-based (Electronic Chart + FHIR + C-CDA + supplemental reports) rather than table-based (CSV), so a field-level dictionary would need to describe the FHIR resource contents and report formats rather than CSV columns.
