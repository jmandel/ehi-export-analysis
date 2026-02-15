# EHI Export Analysis: Juno Health

**Product**: Juno EHR v24
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2925.Juno.23.02.1.240809 (Listing #11497)

## 1. Product Context

Juno EHR is a cloud-native EHR from Juno Health (a division of Document Storage Systems, Inc.), positioned primarily for acute care hospitals (especially critical access and rural), behavioral health facilities, state mental health systems, and public health agencies. Juno was ranked #1 EHR vendor for rural hospitals by Black Book Market Research in 2025.

The product suite comprises multiple certified modules:
- **Juno EHR** — core EHR with clinical documentation, orders, CPOE, flowsheets, assessments
- **RxTracker** — e-prescribing module with Surescripts integration, EPCS, BCMA, eMAR
- **ConnectEHR** — data exchange/interoperability module (C-CDA, FHIR)
- **CQMsolution** — clinical quality measure reporting
- **JESS** — emergency department solution
- **Patient Portal** — patient-facing portal with secure messaging

Key data domains the product stores (baseline for completeness assessment):
- **Clinical**: demographics, problems, medications, allergies, immunizations, vitals, lab results, clinical notes (400+ templates), assessments, care plans, imaging studies
- **Behavioral health**: treatment plans with goals/objectives/interventions ("Golden Thread"), group therapy notes, 150+ behavioral health assessments, legal status/criminal charge tracking
- **Surgical/perioperative**: AORN-compliant perioperative documentation
- **Pharmacy**: comprehensive medication management (from DSS's VA heritage)
- **Revenue cycle**: integrated billing with charge posting, claim submission, ERA processing
- **Public health**: immunization registry, disease surveillance
- **Patient engagement**: portal messages, appointment requests, prescription refills

## 2. Artifacts Reviewed

| Artifact | Source | Description | Informativeness |
|---|---|---|---|
| `main-ehiexport-page.html` (70 KB) | junohealth.com/ehiexport | Landing page describing EHI export as CSV files of native database + non-tabular files. Links to 4 component-specific docs. | Medium — establishes export format and structure |
| `jehr-data-dictionary.html` (201 KB) | ehiexports.junohealth.com/jehr/ | Index page listing 1,256 database tables with links to individual documentation pages | **High** — primary data dictionary index |
| 1,256 individual table pages (downloaded) | ehiexports.junohealth.com/jehr/*.html | Per-table documentation with description, primary/foreign keys, and column-level details | **High** — field-level documentation for every table |
| `rtvx-data-dictionary.html` (17 KB) | ehiexports.junohealth.com/rtvx/ | Index page listing 66 RxTracker tables | High — separate pharmacy module dictionary |
| `connectehr-cqmsolution-page.html` (84 KB) | junohealth.com/ehiexport/connectehr-cqmsolution | Describes ConnectEHR C-CDA 2.1 export and CQMsolution QRDA I export; both certified to (b)(10) under "limited ePHI USCDIv1 definition" | Medium — process docs, no data dictionary |
| `patient-portal-page.html` (85 KB) | junohealth.com/ehiexport/juno-patient-portal | Describes Patient Portal C-CDA export; certified to (b)(10) under "USCDIv1 definition" | Low — brief process description only |
| Screenshots (6 files) | Various | Visual captures of pages above | Low — confirmatory only |

## 3. Export Mechanics

Juno Health provides **four separate export mechanisms**, one per certified module:

### Primary: Juno EHR CSV Table Export
- **Format**: CSV files reflecting the native database schema, plus non-tabular files (images, PDFs, XML, text) exported alongside
- **Mechanism**: Manual one-time export via UI for one or more patients
- **Scope**: Single-patient and multi-patient
- **Access**: Requires enhanced permissions; configuration enables features
- **Documentation**: Comprehensive HTML data dictionary at ehiexports.junohealth.com/jehr/ with 1,256 individually documented tables

### Secondary: RxTracker CSV Table Export
- **Format**: CSV files (same approach as Juno EHR)
- **Documentation**: Separate data dictionary at ehiexports.junohealth.com/rtvx/ with 66 tables

### Supplementary: ConnectEHR C-CDA Export
- **Format**: C-CDA 2.1 XML
- **Mechanism**: UI-based; navigate to Administration > Data Export > Data Export. Single-patient, specific patients, or all patients. Can be scheduled or on-demand.
- **Scope**: Explicitly described as "limited ePHI USCDIv1 definition" — a clinical summary, not full EHI
- **Also supports**: FHIR DocumentReference and Bulk Data Export

### Supplementary: Patient Portal C-CDA Export
- **Format**: C-CDA standardized format
- **Mechanism**: Organization > Reports > Regulatory Reports > Electronic Health Information Request. Select patients, enter 30-day report period, process report.
- **Scope**: USCDIv1 definition

### Supplementary: CQMsolution QRDA I Export
- **Format**: QRDA I XML (patient-level clinical quality data)
- **Scope**: "Contains all EHI stored in Juno CQMsolution for each patient" — limited to quality measure data

**No fees** are mentioned. **Bulk export** is supported (multi-patient selection in the primary CSV export and bulk data export in ConnectEHR).

## 4. Export Content: What's In It

### 4a. Juno EHR Data Dictionary (Primary Export)

I downloaded and parsed all 1,256 individual table documentation pages from ehiexports.junohealth.com/jehr/. Every page was accessible (0 returned 404 errors). Each page provides:

- **Table description**: narrative explaining what the table stores (1,242 of 1,256 tables = 98.9% have descriptions)
- **Primary key**: column(s) identified
- **Foreign keys**: documented with hyperlinks to referenced tables
- **Column details**: ordinal position, column name, SQL data type (INT, NVARCHAR, DATETIME, BIT, DECIMAL, etc.), and text description

**Summary statistics:**
- **Tables**: 1,256
- **Total columns/fields**: 9,045
- **Fields with descriptions**: 9,045 (100%)
- **Fields with data types**: 9,045 (100%)
- **Tables with table-level descriptions**: 1,242 (98.9%)
- **Entity tables (non-lookup)**: 710 tables, 6,467 columns
- **Lookup/reference tables**: 546 tables, 2,578 columns

**Column count distribution:**
- Min: 0 (2 trace/debug tables)
- Median: 4
- 75th percentile: 7
- Max: 260 (RCMUB04CLAIM — UB-04 claim form)
- Mean: 7.2

### 4b. Vendor's Content Organization

The data dictionary is organized alphabetically (A–V), not by clinical domain. I categorized all 1,256 tables by function. The table below shows the domain breakdown:

| Domain Category | Tables | Columns | % Described |
|---|---|---|---|
| Lookup Tables (LK*) | 544 | 2,574 | 100% |
| Pharmacy / Prescriptions (AU_*) | 60 | 986 | 100% |
| Billing / Revenue Cycle | 20 | 703 | 100% |
| Encounter / Visit | 52 | 498 | 100% |
| Medication | 67 | 479 | 100% |
| Questionnaire / Assessment | 44 | 424 | 100% |
| Order | 43 | 323 | 100% |
| Patient Demographics | 28 | 255 | 100% |
| Goal / Intervention | 42 | 243 | 100% |
| Surgery / Procedure | 22 | 212 | 100% |
| Document / Notes | 19 | 182 | 100% |
| Schedule / Appointment | 17 | 168 | 100% |
| Observation / Vitals | 24 | 150 | 100% |
| Item (Charge Definition) | 17 | 149 | 100% |
| Care Plan / Treatment Plan | 26 | 148 | 100% |
| Nutrition Request | 26 | 134 | 100% |
| Procedure | 18 | 107 | 100% |
| Allergy | 9 | 96 | 100% |
| Location / Organization | 7 | 94 | 100% |
| Condition / Problem | 15 | 92 | 100% |
| Immunization | 14 | 79 | 100% |
| Release of Information | 8 | 76 | 100% |
| Coverage / Insurance | 6 | 75 | 100% |
| Imaging | 13 | 71 | 100% |
| Diagnostic Report | 16 | 70 | 100% |
| Laboratory / Specimen | 10 | 61 | 100% |
| Legal Status (Behavioral Health) | 6 | 57 | 100% |
| Medical Coding | 7 | 54 | 100% |
| Media | 8 | 52 | 100% |
| Healthcare Service | 15 | 50 | 100% |
| Group (Session) | 5 | 43 | 100% |
| Account | 5 | 41 | 100% |
| Service Request / Referral | 8 | 40 | 100% |
| Device | 4 | 33 | 100% |
| Task | 4 | 26 | 100% |
| Other (Practitioner, Timing, Address, etc.) | 20+ | ~150 | 100% |

The full inventory of all 1,256 tables is in `analysis/full-entity-inventory.csv` and `analysis/jehr_full_inventory.json`.

### 4c. Representative Large Tables

| Table | Columns | Description |
|---|---|---|
| RCMUB04CLAIM | 260 | UB-04 institutional claim form |
| RCM1500CLAIM | 116 | CMS-1500 professional claim form |
| BILLINGITEM | 115 | Chargeable/billable transactions |
| AU_PRESCRIPTION | 113 | Prescription records (VA heritage) |
| AU_NON-VERIFIED_ORDERS | 103 | Non-verified pharmacy orders |
| AU_PHARMACY_PATIENT_UNIT_DOSE | 102 | Unit dose medication records |
| AU_PHARMACY_PATIENT_IV | 71 | IV medication records |
| ENCOUNTER | 59 | Patient-provider interactions |
| IMPLANTABLEDEVICEINTRAOPERATIVE | 59 | Implantable devices used in surgery |
| ENCOUNTERINSURANCE | 54 | Insurance information per encounter |
| ALLERGY | 51 | Allergy assessments |
| PATIENT | 50 | Patient demographics |
| CONDITION | 44 | Diagnoses/problems/conditions |
| SCHEDULE | 43 | Scheduling records |
| DRUG | 41 | Drug definitions (FDB, RxNorm) |
| CHARGEITEMDEFINITION | 39 | Billing code properties and rules |
| CAREPLAN | 31 | Care plan/treatment plan records |
| IMMUNIZATION | 30 | Immunization events |
| NOTE | 30 | Clinical notes with attribution |
| INTERVENTION | 29 | Goal interventions (behavioral health) |

### 4d. RxTracker Data Dictionary

The RxTracker module has a separate data dictionary with **66 tables** covering pharmacy-specific workflows:
- PRESCRIPTIONS, MEDICATION_ORDERS, OUTPATIENT_MEDICATIONS, HOSPITAL_MEDICATIONS, INPATIENT_MEDICATIONS
- PATIENTS, PERSONS, ENCOUNTERS, VISITS
- PERSONS_ALLERGIES, PERSONS_PROBLEMS, PERSONS_RECONCILIATIONS
- RECONCILIATIONS (with sub-tables for allergies, med orders, signatures)
- DOCUMENTS, VISITS_NOTES, SESSIONS
- PATIENT_DISCHARGE_REQUESTS, TRANSFER_ORDERS

### 4e. ConnectEHR and Patient Portal Exports

These are C-CDA 2.1 exports with no vendor-specific data dictionary. ConnectEHR explicitly states it is certified to (b)(10) under the "limited ePHI USCDIv1 definition." The Patient Portal similarly notes "USCDIv1 definition." These are standard clinical summary exports that complement the primary CSV export but do not add additional EHI content beyond what USCDIv1 C-CDA covers.

### 4f. CQMsolution Export

QRDA I XML files containing patient-level clinical quality measure data. No separate data dictionary — the format is the QRDA I standard.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The Juno EHR CSV export is remarkably deep. Key observations:

**Pharmacy/medication coverage is exceptional** (127 tables, 1,465 columns across AU_* and MEDICATION* tables). This reflects DSS's VA heritage — the AU_ prefix tables derive from VA FileMan data structures and cover prescriptions, refills, pharmacy patients, unit dose, IV, CMOP events, activity logs, and reject info in extraordinary detail. Drug definitions include FDB identifiers and RxNorm codes.

**Billing/revenue cycle coverage is genuinely comprehensive** (20+ tables, 700+ columns). The RCMUB04CLAIM table alone has 260 columns representing every field on the UB-04 institutional claim form. RCM1500CLAIM (116 columns) covers the CMS-1500 professional claim. BILLINGITEM (115 columns) captures chargeable transactions. ChargeItemDefinition tables define billing code properties. Medical coding tables track DRG calculations and coded diagnoses/procedures.

**Behavioral health coverage is purpose-built** (6 legal status tables, behavioral health conflict tables, group session tables, 42 goal/intervention tables, 26 care plan/treatment plan tables, 44 questionnaire tables). The "Golden Thread" concept is visible in the data model: CAREPLAN → GOAL → INTERVENTION → INTERVENTIONPROGRESS tables form a continuous chain from treatment plan to outcomes.

**Clinical documentation is broad**: 19 document/notes tables, 26 nutrition request tables, 13 imaging tables, 16 diagnostic report tables, 8 media tables (images/video/audio), plus the 44 questionnaire tables for configurable assessments.

**Thinnest areas**: Communication tables (3 tables, 11 columns) and consent-related data (no dedicated consent tables found, though ORDERCOVERAGE has a pre-authorization field and RELEASEOFINFORMATION tables handle ROI consent tracking).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PATIENT` (50 fields), `PATIENTLANGUAGE`, `PATIENTRACE`, `PATIENTADDRESS`, `RELATEDPERSON` (17 fields), `MEDICALRECORDNUMBER`, `ADDRESS` (13 fields) — 28 tables, 255 columns | Thorough; covers name, DOB, gender, race, ethnicity, language, contacts, identifiers, marital status, religion, veteran status, housing |
| Encounters / visits | ✅ Covered | `ENCOUNTER` (59 fields), `ENCOUNTERINSURANCE` (54 fields), `ENCOUNTERLOCATION`, `ENCOUNTERDIAGNOSIS`, `ENCOUNTERPARTICIPANT`, `EPISODEOFCARE` — 52 tables, 498 columns | Thorough; admits/discharges/transfers, billing info, diagnoses, participants |
| Problems / conditions | ✅ Covered | `CONDITION` (44 fields), `CONDITIONBODYSITE`, `CONDITIONCODING`, `CONDITIONEVIDENCE`, `CONDITIONSTAGE` — 15 tables, 92 columns | Thorough; clinical status, verification, severity, body site, evidence, staging |
| Medications / prescriptions | ✅ Covered | 60 AU_* tables (986 cols), 67 MEDICATION* tables (479 cols), `DRUG` (41 cols), `DOSAGE` (16 cols) — 127+ tables, 1,465+ columns | Exceptional; VA-heritage pharmacy model covers prescriptions, refills, unit dose, IV, eMAR, BCMA, reconciliation |
| Allergies | ✅ Covered | `ALLERGY` (51 fields), `ALLERGYREACTION`, `ALLERGYCODING`, `ALLERGYMANIFESTATIONCODING` — 9 tables, 96 columns | Thorough |
| Immunizations | ✅ Covered | `IMMUNIZATION` (30 fields), `IMMUNIZATIONEDUCATION`, `IMMUNIZATIONELIGIBILITY`, `IMMUNIZATIONFORECAST`, `IMMUNIZATIONREACTION` — 14 tables, 79 columns | Thorough; includes forecasting, eligibility, education, lot tracking |
| Vitals / observations | ✅ Covered | `OBSERVATION` (26 fields), `OBSERVATIONCOMPONENT`, `OBSERVATIONVALUE`, `REFERENCERANGE` — 24 tables, 150 columns | Solid |
| Lab / diagnostic reports | ✅ Covered | `DIAGNOSTICREPORT` + 15 related tables (70 cols), `LABORATORY` (10 cols), `SPECIMEN*` (10 tables, 61 cols) — 26 tables, 131 columns | Solid; diagnostic reports, specimen definitions, laboratory test links |
| Imaging | ✅ Covered | `IMAGINGSTUDY` (21 fields), `IMAGINGSTUDYSERIES` (13 fields), `IMAGINGSTUDYINTERPRETATION`, `IMAGINGSTUDYREASON` — 13 tables, 71 columns | Solid; DICOM study/series/instance model documented |
| Procedures | ✅ Covered | 18 `PROCEDURE*` tables (107 cols), 22 surgery tables (212 cols) including `SURGERYCASERECORD`, `SURGERYPROCEDURE`, `IMPLANTABLEDEVICEINTRAOPERATIVE` (59 cols) — 40 tables, 319 columns | Thorough; perioperative records, implantable devices, anesthesia types |
| Clinical notes / documents | ✅ Covered | `NOTE` (30 fields), `NOTEADDENDUM`, `NOTECOSIGNATURE`, `DOCUMENT*` tables, `FILESTORAGE` (14 fields for images/docs), `MEDIA` (27 fields) — 27 tables, 234 columns | Thorough; notes with addenda/cosignatures, file storage, media records |
| Care plans / goals | ✅ Covered | `CAREPLAN` (31 fields), 26 care plan tables (148 cols), 23 `GOAL*` tables, 42 intervention tables (243 cols) — 91 tables, 391+ columns | Exceptional; behavioral health "Golden Thread" model (problem → goal → intervention → progress → outcome) |
| Orders / referrals | ✅ Covered | 43 `ORDER*` tables (323 cols), 8 `SERVICEREQUEST*` tables (40 cols), `TASK` (4 tables, 26 cols) — 55 tables, 389 columns | Thorough; CPOE orders, service requests, detected issues (drug safety checks) |
| Insurance / coverage | ✅ Covered | `COVERAGE` (26 fields), `COVERAGECLASS`, `COVERAGECOSTTOBENEFICIARY`, `ENCOUNTERINSURANCE` (54 fields), `MSPQUESTIONNAIRE` — 6 tables, 75 columns | Solid |
| Claims / billing | ✅ Covered | `RCMUB04CLAIM` (260 fields), `RCM1500CLAIM` (116 fields), `BILLINGITEM` (115 fields), `CHARGEITEMDEFINITION` (39 fields), `MEDICALCODING*` tables — 20+ tables, 700+ columns | Exceptional; complete UB-04 and CMS-1500 claim forms, charge capture, medical coding with DRG |
| Payments | ⚠️ Partial | Lookup tables `LKPAYMENTMETHOD` (4 cols), claim status tables, ERA references in billing — but no dedicated payment transaction table | Product processes ERA (electronic remittance); payment detail tables may be thin |
| Consents / directives | ⚠️ Partial | `RELEASEOFINFORMATION` (25 fields) + 7 related tables (76 cols total) cover ROI consent tracking. No dedicated advance directive or general consent tables found | ROI is well-covered; advance directives and general consents appear absent |
| Patient communications | ⚠️ Partial | `COMMUNICATION` (2 cols), `COMMUNICATIONPAYLOAD` (2 cols) — very thin at 4 total columns. Patient Portal has separate C-CDA export | The core EHR communication tables are minimal; portal messages likely in the Patient Portal's own data |
| Specialty: Behavioral health | ✅ Covered | `LEGALSTATUS` (15 fields), `BEHAVIORALHEALTHPATIENTPRACTITIONERCONFLICT`, `GROUP*` (5 tables for group therapy), 150+ assessment templates via `QUESTIONNAIRE*` (44 tables, 424 cols) | Purpose-built; legal status, criminal charges, group sessions, treatment plans |
| Specialty: Surgery/perioperative | ✅ Covered | 22 tables, 212 columns including case records, procedures, blood products, implant sources, personnel, charge items | Solid AORN-aligned coverage |
| Specialty: Nutrition | ✅ Covered | `NUTRITIONREQUEST` + 25 related tables (134 cols) covering enteral formula, oral diet, supplements, restrictions | Notably deep for dietary orders |

## 6. Documentation Quality

### Strengths
- **Comprehensive data dictionary**: Every one of 1,256 tables has its own HTML page with consistent structure. 100% of 9,045 fields have descriptions and data types. This is one of the most thorough EHI export data dictionaries observed.
- **Foreign key documentation**: Relationships between tables are explicitly documented with hyperlinked cross-references, allowing a recipient to reconstruct the relational model.
- **Table descriptions**: 98.9% of tables have narrative descriptions explaining what they store (only 14 tables lack descriptions, most of which are minor — 2 trace tables have 0 columns).
- **SQL data types**: Every column specifies its type (INT, NVARCHAR, DATETIME, BIT, DECIMAL, FLOAT, UNIQUEIDENTIFIER, etc.), enabling accurate import schema creation.
- **Dedicated hosting**: The data dictionary is hosted on a dedicated subdomain (ehiexports.junohealth.com) with static HTML on Azure blob storage, suggesting deliberate investment rather than an afterthought.
- **Descriptions are meaningful**: Not just column names restated — e.g., PATIENT.SEASONALWORKER is described as "Indicates if the patient is a seasonal worker"; PATIENT.UNAUTHORIZEDACCESSALERT as "Determines if alert will trigger when there is unauthorized access to this patient record."

### Weaknesses
- **No sample data**: No example CSV exports or worked examples are provided. A developer would have to request an actual export to see the data format.
- **No value set enumeration**: Coded fields reference lookup (LK*) tables (544 of them) but the allowed values are not listed inline. You know LKMARITALSTATUS exists but not what values it contains (unless you also receive the lookup table CSVs in the export, which the documentation implies you would).
- **No explicit schema file**: No JSON Schema, SQL DDL, or machine-readable schema definition — the documentation is human-readable HTML only.
- **No versioning or changelog**: The dictionary was last modified 2026-01-23, but there's no indication of what changed or version tracking.
- **Alphabetical organization only**: Tables are listed A–Z with no domain/category grouping. A developer must infer clinical domains from table naming conventions.
- **Nullable/constraint info absent**: No documentation of which fields are nullable, max lengths for NVARCHAR fields, or uniqueness constraints beyond primary keys.

### Developer usability assessment
A competent developer could build an import system from this documentation. The table descriptions, column descriptions, data types, and foreign key relationships provide sufficient semantic and structural information to understand the data model. The main challenge would be interpreting coded values without sample data or value set documentation — but the inclusion of lookup tables in the export largely mitigates this.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

Juno Health's primary EHI export (Juno EHR CSV tables) is a genuine native database export with 1,256 documented tables, 9,045 fields, and 100% field-level descriptions. It covers clinical, billing, pharmacy, behavioral health, surgical, imaging, and administrative data domains. The export reflects the actual database schema rather than a projection into a standard format, preserving all vendor-specific data without lossy transformation. The supplementary C-CDA and QRDA I exports from ConnectEHR, Patient Portal, and CQMsolution provide additional standard-format access but are explicitly scoped to USCDIv1 (ConnectEHR transparently acknowledges "limited ePHI USCDIv1 definition").

### Key Findings

1. **Exceptionally thorough data dictionary**: 1,256 tables with 9,045 fields, all with descriptions and data types. This is among the most detailed EHI export documentation observed. Every table has its own HTML page with primary keys, foreign keys, and column-level detail.

2. **Genuine billing/revenue cycle coverage**: The RCM tables (RCMUB04CLAIM at 260 columns, RCM1500CLAIM at 116 columns, BILLINGITEM at 115 columns) demonstrate this is not a clinical-only export. Complete UB-04 and CMS-1500 claim forms are exported with medical coding and charge capture data.

3. **Deep pharmacy heritage**: 60 AU_* tables with 986 columns reflect DSS's VA origins. The pharmacy data model is unusually comprehensive, covering prescriptions, refills, unit dose, IV medications, CMOP events, and activity logs — far exceeding what typical EHR exports include.

4. **Behavioral health purpose-built**: The care plan → goal → intervention → progress chain (91+ tables, 391+ columns) implements the "Golden Thread" concept. Legal status tracking, group therapy sessions, and 44 questionnaire tables support behavioral health workflows.

5. **Honest scope labeling**: The vendor transparently distinguishes between the comprehensive CSV export (Juno EHR) and the limited standard-format exports (ConnectEHR/Patient Portal), explicitly stating the latter are certified under "limited ePHI USCDIv1 definition." This is unusually candid.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (native database tables) + non-tabular files (images, PDFs, XML, text)
Model type:      Native database
Entities:        1,256 tables (Juno EHR) + 66 tables (RxTracker) = 1,322 total
Fields:          9,045 (Juno EHR primary dictionary)
Descriptions:    100% of fields have descriptions
Sample data:     No
Bulk export:     Yes (multi-patient selection)
Domains covered: 17 of 19 applicable domains (consent and payments are partial)
```

### Bottom Line

Juno Health's EHI export is one of the strongest implementations of (b)(10) observed. A patient or provider would receive a comprehensive, native-format export of virtually all data the EHR stores — not just clinical summaries but billing claims, pharmacy records, behavioral health treatment plans, and specialty data. The only notable gaps are thin coverage of payment transactions and advance directive/consent data. The 1,256-table data dictionary with 100% field-level descriptions demonstrates genuine investment in export completeness and documentation quality.
