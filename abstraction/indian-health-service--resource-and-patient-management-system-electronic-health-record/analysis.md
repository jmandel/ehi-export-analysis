# EHI Export Analysis: Indian Health Service

**Product**: Resource and Patient Management System Electronic Health Record (RPMS EHR)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.1673.RPMS.02.05.1.251124

## 1. Product Context

RPMS EHR is a comprehensive, government-built health information system developed by the Indian Health Service (IHS) for approximately 2.6 million American Indian/Alaska Native patients across 574 federally recognized tribes. It runs on MUMPS/FileMan (related to the VA's VistA) and has been in continuous use since ~1984.

RPMS is not a narrow ambulatory charting tool — it is a full-spectrum EHR covering:

- **Clinical**: Patient Care Component (PCC) with V-file architecture for visits, diagnoses, procedures, vitals, labs, radiology; pharmacy (outpatient, controlled substances, e-prescribing); laboratory across all pathology areas; immunization tracking; clinical notes (TIU); adverse reaction tracking; consult/referral management; orders
- **Specialty modules**: Behavioral health (MHSS — encounters, treatment plans, case management, suicide screening); dental; women's health/OB (prenatal, delivery, reproductive factors); diabetes management; HIV management; elder care; optometry; emergency department; community health representative
- **Administrative/Financial**: Patient registration and demographics; ADT; scheduling; third-party billing (Medicare, Medicaid, private — CMS-1500, UB-04, X12 837); accounts receivable; pharmacy point-of-sale claims; contract/purchased referred care (CHS)
- **Population health**: GPRA clinical performance measures; iCare population management; eCQM engine; data warehouse exports
- **Interoperability**: C-CDA generation; HL7 interfaces; FHIR API (g)(10); immunization registry exchange; Direct messaging

The breadth is exceptionally large — approximately 50–100 software packages on a shared database. This sets a high bar for what a (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `IHS_EHI_Schema_Definition.pdf` (7 pages, 241 KB) | User manual for the BREH EHI Export package. Describes purpose, JSON format, schema mechanism, and scope (all EHI except images). | **High** — establishes export mechanics and intent |
| `BREH_OIT_20250714.txt` (5.7 MB) | Latest (2025) national EHI export schema in JSON. Defines 301 patient files with 8,415 field definitions and 548 pointer/reference files. | **Highest** — this IS the data dictionary |
| `BREH_OIT_20240703.txt` (5.7 MB) | 2024 schema version (298 files, ~8,274 fields). | Moderate — useful for version tracking |
| `BREH_OIT_20230607.txt` (5.6 MB) | 2023 schema version (296 files, ~8,221 fields). | Moderate — initial version baseline |
| `enrichment/files-catalog.json` (3.5 MB) | Prior agent's parse of the 2025 schema into structured JSON. | Reference — used to cross-check my parse |
| `enrichment/schema-summary.json` | Summary of all 3 schema versions with counts. | Reference |
| `enrichment/coverage-stats.json` | Domain categorization of all 301 files into 11 categories. | Reference |
| `enrichment/field-types.json` | Field type distribution across the 2025 schema. | Reference |
| `enrichment/schema-diff.json` | Diffs between schema versions (2023→2024, 2024→2025). | Moderate — shows active maintenance |

The schema files (`BREH_OIT_*.txt`) are by far the most informative artifacts — they are machine-readable, complete data dictionaries that define every file and field in the export.

## 3. Export Mechanics

- **Format**: JSON (JavaScript Object Notation). Each patient's data is exported as a JSON document structured according to the national schema.
- **Mechanism**: The BREH package provides an in-application export function. Authorized users "manually generate an EHI export using a predefined national schema for a single patient or a patient population" (PDF, p. 1).
- **Single-patient and bulk**: Both are supported — the documentation explicitly says "a single patient or a patient population."
- **Schema customization**: Sites can create custom schemas based on the national schema, potentially adding or excluding files. The national schema is the baseline.
- **Access**: The export is generated within the RPMS system by authorized users. The schema is publicly downloadable from the IHS website. No fees are mentioned.
- **Exclusions**: Images are explicitly excluded ("Imaging links/data are presented but not the images themselves"). Psychotherapy notes and litigation compilations are excluded per statutory carve-outs.
- **Active development**: The schema has been updated annually (2023 → 2024 → 2025), with files added each year: +2 files (2023→2024), +3 files (2024→2025), and field-level additions across existing files.

## 4. Export Content: What's In It

The export is defined by a national schema (`BREH_OIT_20250714.txt`) that specifies exactly which RPMS FileMan files and fields are included. The schema is a machine-readable JSON document that acts as both the export definition and the data dictionary.

### Summary statistics

- **301 patient files/tables** (entities)
- **8,415 field definitions** across all files
- **548 pointer/reference files** used to resolve foreign-key references
- **1,411 fields** (16.8%) have explicit coded value lists (SET OF CODES) with 4,383 total coded values
- **2,291 fields** (27.2%) are typed as POINTER TO A FILE (foreign key references to other tables)
- **724 fields** (8.6%) are WORD PROCESSING (free-text/narrative content)
- **0 fields** have prose descriptions — field names are the only documentation

The schema provides field names, data types (FREE TEXT, DATE/TIME, NUMERIC, POINTER TO A FILE, SET OF CODES, WORD PROCESSING, COMPUTED, VARIABLE-POINTER), value lists for coded fields, pointer targets for reference fields, and FileMan metadata (global, node, piece). It does not provide human-readable field descriptions.

### Vendor's own content organization

The schema does not use explicit categories — files are listed flat. I categorized them based on FileMan naming conventions and IHS module naming (e.g., V-files are PCC clinical data, MHSS files are behavioral health, 3P/A/R files are billing). The full inventory is in `analysis/entity-inventory-full.json`.

#### Category breakdown

| Category | Entities | Fields |
|---|---|---|
| Administrative - Billing | 35 | 1,552 |
| Administrative - Community Health | 13 | 326 |
| Administrative - Insurance/Coverage | 9 | 46 |
| Administrative - Legal/Privacy | 5 | 79 |
| Administrative - Registration | 36 | 1,182 |
| Administrative - Scheduling | 10 | 145 |
| Clinical - Behavioral Health | 28 | 560 |
| Clinical - Care Plans | 2 | 34 |
| Clinical - Dental | 4 | 41 |
| Clinical - Documents/Notes | 4 | 96 |
| Clinical - Elder Care | 1 | 16 |
| Clinical - Emergency | 2 | 134 |
| Clinical - Immunizations | 7 | 98 |
| Clinical - Laboratory | 7 | 201 |
| Clinical - Orders/Consults | 4 | 240 |
| Clinical - Other | 55 | 859 |
| Clinical - PCC V-files | 43 | 1,416 |
| Clinical - Pharmacy | 17 | 568 |
| Clinical - Problems/Allergies | 6 | 155 |
| Clinical - Radiology | 3 | 100 |
| Clinical - Women's Health/OB | 4 | 390 |
| Imaging | 6 | 177 |
| **Total** | **301** | **8,415** |

#### Top 20 entities by field count

| Entity | Fields | Category |
|---|---|---|
| VA PATIENT | 436 | Registration |
| BW PROCEDURE | 277 | Women's Health/OB |
| ABSP LOG OF TRANSACTIONS | 239 | Billing |
| 3P BILL | 201 | Billing |
| 3P CLAIM DATA | 198 | Billing |
| PATIENT | 194 | Registration |
| A/R BILL/IHS | 181 | Billing |
| PRESCRIPTION | 155 | Pharmacy |
| MHSS RECORD | 143 | Behavioral Health |
| RCIS REFERRAL | 138 | Other (Referral) |
| BILL/CLAIMS | 131 | Billing |
| NON-VERIFIED ORDERS | 101 | Orders/Consults |
| ER VISIT | 100 | Emergency |
| DRUG ACCOUNTABILITY TRANSACTION | 96 | Pharmacy |
| LAB DATA | 93 | Laboratory |
| VISIT | 89 | PCC V-files |
| CHR RECORD | 81 | Community Health |
| PAF | 78 | Other |
| REPRODUCTIVE FACTORS | 76 | Women's Health/OB |
| TIU DOCUMENT | 75 | Documents/Notes |

#### Notable entities

- **VA PATIENT** (436 fields): The largest entity — the core patient registration file inherited from VistA, with demographics, military/veteran status, eligibility, insurance, race/ethnicity, and hundreds of administrative fields.
- **PATIENT** (194 fields): IHS-specific patient demographics including tribal enrollment, Indian eligibility, benefits tracking.
- **3P BILL** (201 fields) and **3P CLAIM DATA** (198 fields): Third-party billing with revenue codes, diagnosis codes, provider NPIs, claim status, accident types — genuinely deep billing data.
- **MHSS RECORD** (143 fields): Behavioral health encounter records with 18 additional MHSS-prefixed files covering treatment plans, problems, intake, case dates, suicide screening — a comprehensive behavioral health module.
- **PCC V-files** (43 files, 1,416 fields): The core clinical data — visits, diagnoses (V POV), procedures (V CPT), labs (V LAB), medications (V MEDICATION), vitals (V MEASUREMENT), immunizations (V IMMUNIZATION), radiology (V RADIOLOGY), dental (V DENTAL), and specialty-specific files like V ANTICOAGULATION, V AMI, V STROKE, V ELDER CARE, V TELEHEALTH.
- **BW PROCEDURE** (277 fields): Women's health procedures — surprisingly the second-largest entity, reflecting deep OB/GYN tracking.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export reflects a native database dump of the RPMS FileMan data model. It covers the full breadth of RPMS's clinical, administrative, and financial data stores:

**Deepest coverage (most entities/fields)**:
- **Billing/Revenue cycle** (35 entities, 1,552 fields): Third-party billing (3P BILL, 3P CLAIM DATA), accounts receivable (A/R BILL/IHS, A/R TRANSACTIONS/IHS), pharmacy point-of-sale (ABSP LOG OF TRANSACTIONS), Medicare/Medicaid/private insurance claims, eligibility data. This is genuinely deep billing data — not a token representation.
- **PCC Clinical V-files** (43 entities, 1,416 fields): The heart of clinical data — every V-file that links to the VISIT file, covering encounters, diagnoses, procedures, labs, vitals, medications, radiology, immunizations, and specialty observations.
- **Patient registration** (36 entities, 1,182 fields): VA PATIENT (436 fields) and IHS PATIENT (194 fields) together provide exceptionally detailed demographics, eligibility, enrollment, and administrative data.

**Solid coverage**:
- **Behavioral health** (28 entities, 560 fields): Treatment plans, goals, methods, intake, case management, suicide screening — a dedicated module, not just a diagnosis code.
- **Pharmacy** (17 entities, 568 fields): Prescriptions (155 fields), drug accountability, controlled substance audit logs, medication refill requests.
- **Women's health/OB** (4 entities, 390 fields): BW PROCEDURE (277 fields), reproductive factors (76 fields), prenatal problems, delivery records (V DELIVERY added in 2025).
- **Community health** (13 entities, 326 fields): Community Health Representative records, Purchased/Referred Care (CHS) data.
- **Orders/Consults** (4 entities, 240 fields): Non-verified orders (101 fields), request/consultation tracking, radiology orders.

**Thinner but present**:
- **Scheduling** (10 entities, 145 fields): Appointments, wait lists, scheduled visits.
- **Documents/Notes** (4 entities, 96 fields): TIU DOCUMENT (75 fields), external data links, problem links, multiple signatures.
- **Dental** (4 entities, 41 fields): Dental procedure, patient, follow-up, deferred services.
- **Care plans** (2 entities, 34 fields): CARE PLAN and TREATMENT PLAN.
- **Elder care** (1 entity, 16 fields): Single file.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | VA PATIENT (436 fields), PATIENT (194 fields), PATIENT NAME CHANGES, PATIENT ENROLLMENT | Exceptionally thorough — two detailed patient files with tribal/eligibility-specific data |
| Encounters / visits | ✅ Covered | VISIT (89 fields), OUTPATIENT ENCOUNTER, INPATIENT data, ER VISIT (100 fields), ER ADMISSION (34 fields) | Deep — visit file links all PCC V-file data |
| Problems / conditions | ✅ Covered | PROBLEM (59 fields), V POV (68 fields), OUTPATIENT DIAGNOSIS, INPATIENT DIAGNOSIS | Multiple problem/diagnosis files covering outpatient and inpatient |
| Medications / prescriptions | ✅ Covered | PRESCRIPTION (155 fields), V MEDICATION, PHARMACY PATIENT, PHARMACY ARCHIVE, BCMA MEDICATION LOG, DRUG ACCOUNTABILITY TRANSACTION (96 fields) | Deep — includes medication administration, refill history, pharmacy audit |
| Allergies | ✅ Covered | PATIENT ALLERGIES, ADVERSE REACTION ASSESSMENT, ADVERSE REACTION REPORTING | Dedicated allergy and adverse reaction tracking |
| Immunizations | ✅ Covered | BI PATIENT, BI PATIENT IMMUNIZATIONS DUE, BI PATIENT CONTRAINDICATIONS, V IMMUNIZATION, IZ EXPORTS | Deep — RPMS immunization tracking is a flagship module |
| Vitals | ✅ Covered | V MEASUREMENT (part of PCC V-files) | Standard vital signs through PCC |
| Lab results | ✅ Covered | LAB DATA (93 fields), V LAB (58 fields), V MICROBIOLOGY (57 fields), V PATHOLOGY, LAB ORDER ENTRY, BLS LOINC EXPORT | Comprehensive lab coverage including microbiology |
| Imaging / diagnostic reports | ✅ Covered | RAD/NUC MED ORDERS, RAD/NUC MED REPORTS, V RADIOLOGY, IMAGE (metadata only — images excluded), PACS MESSAGE | Imaging metadata and reports present; actual images explicitly excluded |
| Procedures | ✅ Covered | V CPT, V PROCEDURE, BW PROCEDURE (277 fields), DAY SURGERY, INPATIENT PROCEDURE | Deep — especially women's health procedures |
| Clinical notes / documents | ✅ Covered | TIU DOCUMENT (75 fields), V NARRATIVE TEXT, GMR TEXT, TIU EXTERNAL DATA LINK | Template-based notes and narrative text |
| Care plans / goals | ✅ Covered | CARE PLAN, TREATMENT PLAN, PATIENT GOALS, MHSS PATIENT TREATMENT PLANS | Present but relatively thin (34 fields for care plan) |
| Orders / referrals | ✅ Covered | ORDER (24 fields), NON-VERIFIED ORDERS (101 fields), REQUEST/CONSULTATION (62 fields), RCIS REFERRAL (138 fields), V REFERRAL | Deep referral tracking especially for purchased/referred care |
| Insurance / coverage | ✅ Covered | PERSONAL POLICY, POLICY HOLDER, GUARANTOR, MEDICARE ELIGIBLE, MEDICAID ELIGIBLE, PRIVATE INSURANCE ELIGIBLE, ABSP COMBINED INSURANCE, ABSP ELIGIBILITY | Multiple insurance/eligibility files across payer types |
| Claims / billing | ✅ Covered | 3P BILL (201 fields), 3P CLAIM DATA (198 fields), A/R BILL/IHS (181 fields), BILL/CLAIMS (131 fields), ABSP LOG OF TRANSACTIONS (239 fields), CLAIMS TRACKING, plus Medicare/Medicaid/Private/Railroad claims files | **Genuinely deep** — 35 entities, 1,552 fields. Not a token billing representation |
| Payments | ✅ Covered | A/R TRANSACTIONS/IHS, A/R PREPAYMENT, A/R FLAT RATE POSTING | Accounts receivable with payment tracking |
| Consents / directives | ✅ Covered | ADVANCE DIRECTIVE, NOTICE OF PRIVACY PRACTICES, PATIENT'S LEGAL DOCS, ACCESS RESTRICTIONS | Privacy and consent tracking |
| Patient communications | ⚠️ Partial | BPHR MED REFILL REQUEST (added 2025), AG MESSAGE TRANSACTIONS, ALERT TRACKING | Med refill requests present; no patient portal messaging threads visible |
| Specialty: Behavioral health | ✅ Covered | 28 MHSS-prefixed entities (560 fields): intake, treatment plans, goals, methods, case dates, problem lists, suicide screening, Navajo referral form | **Exceptionally deep** — dedicated behavioral health module with its own data model |
| Specialty: Dental | ⚠️ Partial | DENTAL PATIENT, DENTAL PROCEDURE, DENTAL FOLLOWUP, DENTAL DEFERRED SVCS REGISTER, V DENTAL | Present but thin (4+1 entities, 41 fields). RPMS has a Dental Data System module that may store more |
| Specialty: Women's health/OB | ✅ Covered | BW PROCEDURE (277 fields), REPRODUCTIVE FACTORS (76 fields), BJPN PRENATAL PROBLEMS, V DELIVERY, BW PATIENT, BW NOTIFICATION | Deep — prenatal, delivery, reproductive tracking |
| Specialty: Emergency | ✅ Covered | ER VISIT (100 fields), ER ADMISSION (34 fields), V EMERGENCY VISIT RECORD | Dedicated ER module |
| Specialty: Diabetes | ⚠️ Partial | BCDM PATIENT (chronic disease management patient file) | Single patient-level file; RPMS has a Diabetes Management System that may store more |
| Specialty: Community health | ✅ Covered | CHR RECORD (81 fields), CHR POV, CHR EDUCATION PROVIDED, CHS files, CDMIS files | Community health representative and purchased/referred care data |
| Patient-reported outcomes | ⚠️ Partial | V HEALTH FACTORS, MHSS intake/assessments, V WELL CHILD | Health factors and behavioral health assessments present; no dedicated PRO infrastructure |

**Domains N/A to this product**: Oncology-specific data (staging, tumor registries), wound care tracking — these are not known RPMS modules.

## 6. Documentation Quality

**Strengths**:
- The schema files are fully machine-readable JSON — they can be parsed programmatically to enumerate every file and field in the export.
- Every field has a defined type (FREE TEXT, DATE/TIME, NUMERIC, POINTER TO A FILE, SET OF CODES, WORD PROCESSING, COMPUTED, VARIABLE-POINTER).
- SET OF CODES fields include explicit value lists (1,411 fields with 4,383 total coded values), enabling interpretation of coded data.
- POINTER fields identify their target reference file (2,291 foreign key references to 548 pointer files), documenting relationships.
- The schema includes FileMan metadata (global name, node, piece) enabling direct mapping to the MUMPS database structure.
- Three versions published (2023, 2024, 2025) showing active maintenance with incremental additions.

**Weaknesses**:
- **No prose descriptions**: Zero fields have human-readable descriptions. A developer must infer meaning from field names alone (e.g., "1U4N" in VA PATIENT has no explanation).
- **No sample data**: No example exports are published to show what the JSON output looks like with real patient data.
- **Minimal user documentation**: The PDF is only 7 pages and explains the concept but provides no data dictionary walkthrough, no field-level documentation, and no guidance on interpreting the JSON output.
- **No ERD or relationship documentation**: While pointer fields identify their target files, there's no entity-relationship diagram or documentation of how files relate to each other (e.g., how V-files link to VISIT).

**Verdict**: A developer familiar with MUMPS/FileMan and RPMS could work with this schema productively — the field names are largely self-documenting for domain experts (e.g., "ACCIDENT TYPE", "REVENUE CODE", "DATE OF BIRTH"). But a developer without RPMS expertise would struggle significantly with the lack of descriptions, especially for cryptic names like "PAF", "OPC", "1U4N", "RCIS".

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is one of the most thorough (b)(10) exports encountered. With 301 patient files and 8,415 fields spanning clinical, administrative, financial, and specialty domains, RPMS's EHI export covers the genuine breadth of what the product stores. Key indicators:

1. **Billing is deeply covered**: 35 entities with 1,552 fields — third-party billing, claims (Medicare/Medicaid/private/railroad), accounts receivable, pharmacy point-of-sale transactions. This is not a token billing representation.
2. **Specialty clinical data is included**: 28 behavioral health entities (560 fields), 4 women's health/OB entities (390 fields), dedicated emergency department, dental, immunization, community health, and elder care files.
3. **The export goes far beyond USCDI**: USCDI covers ~26 FHIR resource types with ~94 data elements. This export has 301 entities with 8,415 fields including billing claims, behavioral health treatment plans, community health representative records, purchased/referred care, pharmacy point-of-sale, and insurance eligibility — none of which are in USCDI.
4. **Active evolution**: Files added each year (296→298→301), fields added to existing files (e.g., MHSS RECORD grew from 122 to 143 fields; PATIENT from 171 to 194 fields), and new specialty files added (V DELIVERY in 2025).

Minor gaps: dental coverage is thin relative to the product's Dental Data System module; diabetes management has only a patient-level file despite a dedicated module; patient portal messaging is minimal. But overall, relative to the product's known capabilities, coverage is comprehensive.

**Axis 2 — Export approach: Purpose-built EHI export**

IHS built a dedicated export package (BREH) specifically for (b)(10) compliance. Several indicators confirm this:

1. **Dedicated software package**: BREH (RPMS Electronic Health Information Export) is a purpose-built RPMS package, not a reuse of C-CDA generation (BCCD), HL7 interfaces (BHL/GIS), or FHIR API (g)(10).
2. **Native database model**: The export uses the RPMS FileMan data model directly — the 301 files are RPMS's own data files, not a projection into a standard like FHIR or C-CDA. This means the export captures the full depth of each file rather than mapping to a limited standard template.
3. **National schema with site customization**: The schema is defined nationally and published publicly, with a mechanism for sites to create custom schemas — this is an EHI-specific governance model.
4. **Explicit EHI scope**: The export type is defined as "EHI" (with separate "4DW PAMPI" and "4DW ALL" modes for data warehouse purposes), and the documentation explicitly references 45 CFR 171.102 and the Designated Record Set definition.
5. **JSON output**: The export produces JSON, not C-CDA or FHIR — a purpose-specific format for bulk EHI export.

### Key Findings

1. **Exceptionally deep native database export**: 301 entities and 8,415 fields from the RPMS FileMan database, covering clinical, billing, behavioral health, women's health, community health, pharmacy, and administrative domains. This is one of the most comprehensive (b)(10) exports reviewed.

2. **Genuine billing coverage**: 35 billing entities with 1,552 fields — including 3P BILL (201 fields), 3P CLAIM DATA (198 fields), ABSP LOG OF TRANSACTIONS (239 fields), and separate files for Medicare, Medicaid, private insurance, and railroad claims. This is not a compliance checkbox.

3. **Specialty-specific clinical data well represented**: Behavioral health has 28 entities (560 fields) covering treatment plans, intake, case management, and suicide screening. Women's health has 390 fields across 4 entities. These go far beyond what any standard clinical exchange format would include.

4. **No field-level descriptions**: Despite 8,415 field definitions with types, value lists, and pointer references, zero fields have prose descriptions. Field names are the sole documentation, which is adequate for RPMS experts but challenging for external use.

5. **Active maintenance and growth**: The schema has evolved across three annual versions (2023→2025), adding 5 new files and expanding existing files. The 2025 schema added V DELIVERY (obstetric deliveries), BPHR MED REFILL REQUEST (patient health record), and BLRAU ANTIMICROBIAL USE LOG — showing ongoing attention to completeness.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   JSON (native FileMan data model)
    Entities:        301
    Fields:          8,415
    Descriptions:    0% (field names only, no prose descriptions)
    Sample data:     No
    Bulk export:     Yes (single patient or population)
    Domains covered: 19 of 21 applicable domains (dental and diabetes management thin but present)

### Bottom Line

IHS built one of the strongest (b)(10) exports reviewed. The BREH package exports 301 native FileMan tables with 8,415 fields in JSON format, covering clinical data, billing/claims, behavioral health, women's health, pharmacy, community health, and administrative records — far exceeding USCDI scope. The main weakness is documentation quality: despite rich structural metadata (types, value sets, pointer references), there are no prose descriptions for any field, making the export difficult to interpret without RPMS domain expertise.
