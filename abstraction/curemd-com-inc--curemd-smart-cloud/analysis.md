# EHI Export Analysis: CureMD.com, Inc.

**Product**: CureMD SMART Cloud
**Analysis date**: 2026-02-16
**CHPL ID**: 15.07.04.2706.CURE.10.01.1.230302 (CHPL #11246)

## 1. Product Context

CureMD SMART Cloud is a comprehensive cloud-based ambulatory healthcare platform integrating EHR, practice management, patient portal, and revenue cycle management. The company claims 30,000+ practices and 109,000+ users across 44 states and 32+ medical specialties. The product is certified across 35+ ONC criteria (version 10g, certified 2023-03-02).

Key data domains the product stores — relevant to assessing export completeness:

- **Clinical**: Charting with specialty-specific templates (30+ specialties), problem lists, medications, allergies, vital signs, immunizations, lab orders/results, imaging orders/reports, clinical notes, referrals, care plans
- **E-Prescribing**: Prescriptions, controlled substances, medication reconciliation, formulary/benefit checks
- **Practice Management**: Demographics, scheduling, insurance eligibility, referral management, document management, multi-location support
- **Revenue Cycle / Billing**: Charge capture, claims scrubbing/submission, payment posting, denial management, patient balance collection, financial reporting, ERA processing
- **Patient Portal**: Secure messaging, appointment scheduling, online payments, health records access, wearable device integration
- **Specialty modules**: Oncology/chemotherapy, OB/GYN, behavioral health, chronic care management (CCM), remote patient monitoring (RPM)
- **Telehealth**: Integrated video visits with consent and payment
- **Public Health Reporting**: Immunization registries, syndromic surveillance, cancer reporting, electronic case reporting

This is a full-featured ambulatory EHR with deep billing capabilities — a proper (b)(10) export should cover clinical, billing, specialty, and administrative data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI_Export_DRS.xlsx` (101 KB) | XLSX with 2 sheets: "EHI Export" (overview of export process) and "DRS" (data dictionary with 38 data classes, 891 fields with names, SQL types, and descriptions) | **Primary artifact** — most informative |
| `downloads/ehi-export-page.html` (125 KB) | Saved HTML of https://www.curemd.com/ehi-export.asp — the (b)(10) landing page with brief description and XLSX download link | Moderately informative — confirms export format and mechanism |
| `downloads/screenshot-ehi-export-page.png` (802 KB) | Viewport screenshot of the EHI export page | Low — confirms page layout, no additional content |
| `downloads/CureMD.pdf` (1.3 MB, 20 pages) | General marketing brochure covering EHR, billing, scheduling, specialties | Low — useful only for product context, not EHI-specific |
| `downloads/enrichment/drs-data-dictionary.json` (166 KB) | Prior agent's extraction of the XLSX data dictionary | Used for reference; independently verified via own parse |

## 3. Export Mechanics

- **Format**: CSV files for structured data; documents and images in native formats; provider notes as HTML files (named `[Note Type]_[Date of Service]_[Note ID].html`). All delivered as ZIP archives.
- **Mechanism**: Built-in "EHI Export module" in the application UI. System administrators can initiate exports without developer assistance.
- **Single-patient**: Initiated through the application; once extracted, users download via a provided link.
- **Population/bulk**: Users submit a request from within the application; updates delivered via email.
- **Access constraints**: Requires system administrator role. No indication of fees for the export itself (though some certified features may require additional fees per the cost disclosure page).
- **Last updated**: November 2023 (per XLSX overview sheet).

Source: "EHI Export" sheet of `EHI_Export_DRS.xlsx` and the `ehi-export-page.html`.

## 4. Export Content: What's In It

### Data dictionary overview

The data dictionary (DRS sheet of `EHI_Export_DRS.xlsx`) defines **38 data classes** with **891 fields** (excluding 2 special classes that have no tabular fields). Every field includes:
- **Field name**: descriptive, in plain English (e.g., "Billing Provider EIN", "Allergy Name", "Chemo Plan ID")
- **SQL data type**: varchar, int, datetime, numeric, float, bit, text, nvarchar, date (9 types total)
- **Description**: Plain English explanation of the field's purpose

All 891 fields have descriptions — 100% description coverage. Descriptions are substantive (typically 1-2 sentences explaining the field's meaning), not just restating the field name.

The SQL-style data types (varchar, int, datetime, numeric, float, bit, text, nvarchar, date) confirm this is a direct mapping from the underlying relational database, not a projection into a clinical standard.

**What's NOT documented**: value sets for coded fields (e.g., valid values for "Status", "Severity", "Type"), foreign key relationships between tables (though shared fields like Patient ID, Account Number, Appointment ID serve as implicit join keys), and sample data.

### Two special data classes

- **Documents & Images**: "All documents and images attached to the patient chart will be exported in their native format and metadata." No tabular field definitions.
- **Provider Notes**: Exported as HTML files with naming convention `[Note Type]_[Date of Service]_[Note ID].html`. No tabular field definitions.

### Vendor's own content organization

The data dictionary does not group classes into categories — each class stands alone. I've organized them by domain based on content:

**Demographics & Contacts (2 classes, 91 fields)**

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Patient Demographics | 71 | 71 | varchar, int, datetime, nvarchar, float, numeric | Demographics |
| Patient Contacts | 20 | 20 | varchar, int, datetime | Demographics |

**Clinical (15 classes, 293 fields)**

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Social History | 65 | 65 | int, varchar, datetime, text | Clinical |
| Results | 29 | 29 | varchar, datetime, int | Clinical |
| Orders | 24 | 24 | varchar, datetime, int | Clinical |
| Vitals A | 23 | 23 | varchar, numeric, datetime, int | Clinical |
| Diseases History | 21 | 21 | varchar, int, datetime | Clinical |
| Immunizations | 20 | 20 | varchar, datetime, int | Clinical |
| Medications | 19 | 19 | varchar, datetime, int | Clinical |
| Diagnosis | 18 | 18 | varchar, datetime, int | Clinical |
| Surgery History | 18 | 18 | int, varchar, datetime, bit | Clinical |
| Allergies | 15 | 15 | varchar, datetime, int | Clinical |
| Family History | 12 | 12 | varchar, int, datetime, nvarchar | Clinical |
| Vitals B | 9 | 9 | varchar, int, datetime, numeric | Clinical |
| Risk | 8 | 8 | int, datetime, varchar, numeric | Clinical |
| Hospitalization History | 6 | 6 | varchar, int, datetime | Clinical |
| Complaints | 6 | 6 | varchar, datetime, int | Clinical |

**Specialty — Oncology & OB/GYN (6 classes, 130 fields)**

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| OBGYN History | 52 | 52 | int, varchar, datetime | Specialty |
| Chemo Plan Drugs | 28 | 28 | varchar, numeric, int | Specialty |
| Chemo Plan | 22 | 22 | varchar, numeric, date, int | Specialty |
| Chemo Admin | 15 | 15 | varchar, numeric, date, datetime | Specialty |
| Chemo Plan Diagnosis | 7 | 7 | varchar, numeric, int | Specialty |
| Chemo Admin IVSites | 6 | 6 | varchar, numeric | Specialty |

**Billing & Financial (5 classes, 270 fields)**

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Charges | 82 | 82 | varchar, int, datetime, numeric, float, nvarchar | Billing |
| Payments | 77 | 77 | varchar, numeric, int, datetime | Billing |
| Patient Insurances | 76 | 76 | varchar, int, datetime, numeric | Billing |
| Electronic Remittance Advice | 19 | 19 | varchar, datetime, numeric, int | Billing |
| Claims | 16 | 16 | varchar, int, datetime | Billing |

**Documents (2 classes, 0 tabular fields)**

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Documents & Images | 0 (special) | — | — | Documents |
| Provider Notes | 0 (special) | — | — | Documents |

**Administrative & Care Coordination (8 classes, 107 fields)**

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Referrals | 23 | 23 | varchar, int, nvarchar, datetime | Administrative |
| Appointments | 20 | 20 | varchar, int, datetime, nvarchar | Administrative |
| Cases | 18 | 18 | varchar, int, datetime | Administrative |
| Patient Note | 16 | 16 | varchar, int, datetime | Administrative |
| Disclosures | 11 | 11 | int, varchar, datetime | Administrative |
| Memos | 8 | 8 | varchar, int, datetime | Administrative |
| Patient Education | 6 | 6 | varchar, int, datetime | Administrative |
| Patient Consents | 5 | 5 | varchar, datetime | Administrative |

Full inventory: `analysis/entity-inventory-full.json` (891 fields with complete name, type, description for each).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized as 38 flat data classes mapping closely to database tables. The coverage is notably broad:

**Strongest areas:**
- **Billing/financial data** (5 classes, 270 fields): This is the standout. Charges (82 fields), Payments (77 fields), and Patient Insurances (76 fields) are among the largest classes. Includes claims submission tracking, ERA processing, denial management, plan balances, and write-offs. This level of billing detail is rare in EHI exports.
- **Demographics** (71 fields): Comprehensive — includes race, ethnicity, language, gender identity, sexual orientation, responsible party, multiple addresses, religion, death date, patient portal account status, balance information.
- **Social History** (65 fields): Unusually deep — covers tobacco, alcohol, drug use, sexual history, occupation, sleep, diet/exercise, and an extensive dermatology-relevant UV exposure section (tanning beds, bronzer, PUVA therapy, skin cancer, burns, etc.).
- **Specialty data** (6 classes, 130 fields): Oncology/chemotherapy data (plan, drugs, diagnosis, administration, IV sites) and OB/GYN history (52 fields covering pregnancy, screening dates, contraception, menstrual data) are genuine specialty content rarely seen in EHI exports.

**Adequate areas:**
- **Clinical data** (15 classes, 293 fields): Standard clinical domains are all represented — allergies, diagnoses, medications, orders, results, vitals, immunizations, family history, diseases history, surgery history, complaints, hospitalization history, risk assessments.
- **Documents**: Provider notes exported as HTML files; documents and images in native formats with metadata.
- **Administrative** (8 classes, 107 fields): Appointments, cases, referrals, consents, disclosures, memos, patient education, patient notes.

**Thinnest areas:**
- **Patient Consents** (5 fields): Minimal — just account number, type, status, and date range.
- **Hospitalization History** (6 fields): Basic — practice, patient ID, account number, date, unremarkable flag, comments.
- **Complaints** (6 fields): Chief complaint with description.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (71 fields), `Patient Contacts` (20 fields) | Thorough — includes race, ethnicity, language, gender identity, sexual orientation, responsible party, multiple addresses |
| Encounters / visits | ⚠️ Partial | `Appointments` (20 fields) — has dates, providers, status, check-in/out times, visit reason, telehealth flag | Appointment data present but no discrete encounter/visit record with clinical context; clinical encounters are captured via Provider Notes (HTML) |
| Problems / conditions | ✅ Covered | `Diagnosis` (18 fields) — ICD-10, ICD-9, status, onset, severity, type, chronic flag, significance | Solid |
| Medications / prescriptions | ✅ Covered | `Medications` (19 fields) — name, NDC, status, prescriber NPI, chronic flag, start/end dates, generic name | Good, though missing SIG/dosing instructions as discrete fields |
| Allergies | ✅ Covered | `Allergies` (15 fields) — RxNorm, severity, reactions, status, onset, type | Solid |
| Immunizations | ✅ Covered | `Immunizations` (20 fields) — CVX code, NDC, lot number, dosage, refusal reason, vaccine brand | Thorough |
| Vitals | ✅ Covered | `Vitals A` (23 fields) + `Vitals B` (9 fields) — BP, pulse, respiration, temp, SpO2, height, weight, BMI, BSA, pain score, peak expiratory flow, blood type/Rh | Comprehensive |
| Lab results | ✅ Covered | `Results` (29 fields) — LOINC, result value, units, range, flag, observation notes, specimen type | Solid |
| Imaging / diagnostic reports | ⚠️ Partial | `Orders` has "Radiology Result" and "Type" fields; `Results` has "Radiology Result" field | Imaging orders and results present but may be merged with lab results rather than having dedicated imaging tables |
| Procedures | ⚠️ Partial | `Surgery History` (18 fields), `Charges` has CPT codes | Procedure history documented; procedures likely also captured in Provider Notes and Charges |
| Clinical notes / documents | ✅ Covered | `Provider Notes` (HTML files), `Documents & Images` (native formats) | Notes exported as rendered HTML; documents/images in original format |
| Care plans / goals | ❌ Not covered | No dedicated care plan entity | CureMD has CCM care plans and goals; this is a gap |
| Orders / referrals | ✅ Covered | `Orders` (24 fields), `Referrals` (23 fields) | Good — includes lab, radiology, and referral orders |
| Insurance / coverage | ✅ Covered | `Patient Insurances` (76 fields) — primary, secondary, tertiary plans with subscriber info, policy numbers, group info, copay, insured party details | Exceptionally thorough |
| Claims / billing | ✅ Covered | `Charges` (82 fields), `Claims` (16 fields) | Very detailed — CPT codes, modifiers, claim status, submission dates, plan/patient balances |
| Payments | ✅ Covered | `Payments` (77 fields), `Electronic Remittance Advice` (19 fields) | Exceptionally detailed — payment methods, denial reasons, transfers, write-offs, ERA data |
| Consents / directives | ⚠️ Partial | `Patient Consents` (5 fields) — type, status, date range only | Thin — no consent content or advance directive details |
| Patient communications / portal messages | ⚠️ Partial | `Memos` (8 fields), `Patient Note` (16 fields) | These may capture some communications but no explicit secure messaging or patient portal message table despite CureMD having an active patient portal |
| Specialty — Oncology | ✅ Covered | 5 chemo-specific classes (78 fields): `Chemo Plan`, `Chemo Plan Drugs`, `Chemo Plan Diagnosis`, `Chemo Admin`, `Chemo Admin IVSites` | Strong — treatment plans, drug details, administration records, IV sites |
| Specialty — OB/GYN | ✅ Covered | `OBGYN History` (52 fields) — pregnancy history, screenings, contraception, menstrual data | Thorough |
| Specialty — Behavioral Health | ❌ Not covered | No dedicated behavioral health entity | CureMD supports behavioral health with screening tools (GAD-7, PHQ-9); these may be in Results or Provider Notes but no dedicated table |
| Risk assessments | ✅ Covered | `Risk` (8 fields) — method, level, score | Present but thin |
| Family health history | ✅ Covered | `Family History` (12 fields) — disease, family member, age at onset/death | Adequate |
| Social history | ✅ Covered | `Social History` (65 fields) — tobacco, alcohol, drugs, sexual history, occupation, education, sleep, diet, UV exposure | Exceptionally detailed |

**Summary**: Of 22 applicable domains, 14 are well covered (✅), 5 are partially covered (⚠️), and 2 are not covered (❌). One notable gap is care plans/goals — CureMD has a CCM module with care plan functionality, and this data is absent from the export. The behavioral health gap may be partially mitigated if screening results are captured in the Results class or Provider Notes. The remaining partial gaps (encounters, imaging, consents, communications) reflect data that is likely present in the system but either folded into other classes or captured in Provider Notes rather than as discrete structured fields.

## 6. Documentation Quality

**Strengths:**
- Every field (891/891 = 100%) has a plain English description explaining its purpose — this is excellent and exceeds most vendors.
- SQL data types are specified for every field, making the export schema unambiguous.
- The overview sheet clearly explains single-patient vs. population export mechanics, formats, and delivery method.
- The XLSX format is machine-readable and structured.

**Weaknesses:**
- **No value sets**: Coded fields (Status, Severity, Type, etc.) have descriptions but no enumeration of valid values. A developer would need to discover these from actual data.
- **No relationship documentation**: No foreign key definitions, no ERD, no join key documentation. Relationships must be inferred from shared field names (Patient ID, Account Number, Appointment ID).
- **No sample data**: No example CSV files or sample records provided.
- **No schema files**: No XSD, JSON Schema, DDL, or OpenAPI spec — the XLSX is the only format.
- **No worked examples**: No step-by-step guide showing an actual export or how to interpret the output files.
- **Dated**: Last updated November 2023 — over 2 years ago as of this analysis.

**Overall**: A developer could understand the data model and build an import from this documentation, though they would need to infer relationships and discover value sets from actual data. The documentation is a solid data dictionary — better than most vendors — but not a complete integration specification.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains CureMD stores. The strongest signal is the billing/financial coverage: 270 fields across 5 classes (Charges, Payments, Claims, ERA, Patient Insurances) covering charge capture, claims submission, payment posting, denial management, and remittance processing. This is exactly the kind of data that vendors typically omit when they repackage a clinical exchange export as (b)(10). Additional signals of breadth: oncology/chemo data (5 classes, 78 fields), OB/GYN history (52 fields), social history (65 fields with dermatology-specific UV exposure fields), appointments, referrals, cases, disclosures, memos, and risk assessments. The export covers the core designated record set for an ambulatory EHR comprehensively. The gaps (care plans, CCM data, RPM data, secure messaging, behavioral health assessments) are relatively minor omissions — mostly specialty module data that may be captured within Provider Notes or Results rather than as standalone tables.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. Key evidence:
1. The export format is CSV (flat files from the database), not FHIR or C-CDA.
2. The data types are SQL Server column types (varchar, int, datetime, numeric, float, bit, text, nvarchar), confirming direct database extraction.
3. The data dictionary includes billing data (Charges 82 fields, Payments 77 fields, Claims, ERA) — entirely outside USCDI/US Core scope.
4. Specialty clinical data (5 oncology classes, OB/GYN) is included — not available through (g)(10) FHIR APIs.
5. There is no mention of FHIR, Bulk Data, US Core, or C-CDA anywhere in the EHI export documentation.
6. The vendor built a dedicated "EHI Export module" in their application with separate single-patient and population-level workflows.
7. The data dictionary was purpose-written for this export, with the "DRS" (Designated Record Set) sheet explicitly named to reference the HIPAA concept.

### Key Findings

1. **Billing coverage is the standout feature.** With 270 fields across 5 billing-related classes (Charges, Payments, Claims, ERA, Patient Insurances), this is one of the more thorough financial data exports seen in (b)(10) implementations. Many vendors omit billing entirely.

2. **Specialty clinical data inclusion is notable.** Five oncology/chemotherapy classes (78 fields) and one OB/GYN class (52 fields) represent genuine specialty content that goes well beyond USCDI. The chemo data covers treatment plans, drug details, administration records, and IV sites.

3. **100% field description coverage.** All 891 fields have substantive English-language descriptions — not just restated field names. This is significantly better than most vendor data dictionaries.

4. **Notable gaps exist in newer product modules.** Care plans/goals (CCM module), remote patient monitoring data, secure messaging/portal messages, telehealth session records, and behavioral health assessments are not represented as discrete data classes. These may be partially captured in Provider Notes or Results.

5. **No value sets, relationships, or sample data.** While field-level documentation is strong, the absence of coded value enumerations, explicit foreign keys, and sample export files means a developer would need to discover these through actual data exploration.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV + native formats for documents/images + HTML for provider notes (ZIP)
Entities:        38 data classes
Fields:          891
Descriptions:    100%
Sample data:     No
Bulk export:     Yes (population-level via request)
Domains covered: 14 of 22 well-covered; 5 partial; 2 not covered
```

### Bottom Line

CureMD has built a genuine (b)(10) EHI export that covers clinical, billing, specialty (oncology, OB/GYN), and administrative data with 891 fully-described fields across 38 data classes. A patient or provider would get a substantially complete copy of their designated record set. The biggest gap is the absence of care plan/CCM data and secure messaging despite CureMD having these modules; the biggest strength is the unusually thorough billing and financial data coverage.
