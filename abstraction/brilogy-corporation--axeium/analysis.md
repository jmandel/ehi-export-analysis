# EHI Export Analysis: Brilogy Corporation

**Product**: AXEIUM  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.05.05.1171.BRIL.02.01.1.221219

## 1. Product Context

AXEIUM is a full-featured, multi-specialty EHR and practice management system purpose-built for Federally Qualified Health Centers (FQHCs) and community health centers. It was developed through a grant-funded consortium effort in Orange County, California. The product integrates four clinical service lines — **medical, dental, vision, and behavioral health** — under a single platform, alongside practice management and billing functionality.

Key data domains the product stores (relevant to export completeness assessment):

- **Patient demographics** (extensive: name, DOB, contacts, languages, race/ethnicity, employment, income, family, program enrollment)
- **Medical clinical data** (problems/diagnoses with SNOMED/ICD, medications with Lexicomp/Surescripts, allergies with RxNorm, labs with LOINC, immunizations, vitals, clinical exams with configurable templates, SOAP/progress notes, CDS alerts)
- **Dental** (tooth charting, periodontal charting, treatment plans, CDT procedures, imaging integration)
- **Vision** (refraction, Rx history, anterior/posterior segment, tonometry, gonioscopy)
- **Behavioral health** (intake assessments, SIRP workflow, treatment plans with goals)
- **Pregnancy/OB** (CPSP prenatal program tracking, full pregnancy records)
- **Billing** (HCFA 1500, PM-160 for FQHCs, superbills, electronic billing, CPT/ICD codes)
- **Administrative** (scheduling, check-in/out, task management, referrals, patient communications)
- **Documents** (scanned documents, clinical images, annotations)
- **Reporting** (eCQMs, UDS, OSHPD)

This is a comprehensive, all-in-one system for safety-net health organizations, so the EHI export should span clinical, dental, vision, behavioral health, billing, and administrative domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Schema.pdf` (1.04 MB, 62 pages) | Data dictionary listing all 94 tables and 2,879 columns in the export. Three columns: TABLE_NAME, COLUMN_NAME, DATA_TYPE. Generated from Excel by Milton Allione on 2023-10-22. | **Most informative** — defines the full export schema |
| `downloads/ehi-page.html` (29 KB) | HTML source of axeium.com/EHI. Describes export as tab-separated files in AXEIUM's native record layout with separate handling for rich text and images. Links to Schema.pdf. Includes HTML comments showing version history (v1-v3, Oct 2023) where FHIR/C-CDA references were deliberately removed. | **Informative** — describes export mechanics |
| `downloads/screenshot-ehi-page.png` / `screenshot-ehi-page-full.png` (471 KB each) | Browser screenshots of the EHI page confirming visible content matches HTML source. | Confirmatory |

No sample data files, no machine-readable schemas (JSON/XML), no FHIR or C-CDA documentation were provided.

## 3. Export Mechanics

- **Format**: Tab-separated value (TSV) files in AXEIUM's native database layout — one file per table. Rich text documents and images are exported separately as binary files.
- **Mechanism**: Manual initiation by system users via the application UI ("EHI Export functionality allows system users to manually initiate an export"). No API-based export documented.
- **Single-patient vs bulk**: Documentation says "one or more patients" — both single and bulk export appear supported.
- **Access constraints**: No fees mentioned. The page notes content variability based on software applications in use, software version, external data sources, and site configuration decisions.
- **Notable**: HTML comments in the EHI page (v3, 2023-10-25) show the vendor deliberately removed references to FHIR Bulk Data and C-CDA as alternative extraction methods, "per guidance from kendra/sli." This indicates the vendor considered and intentionally distinguished their (b)(10) export from their existing clinical exchange capabilities.

## 4. Export Content: What's In It

### Data dictionary structure

The Schema.pdf provides a flat listing of all tables and columns with three metadata elements per column:
- **TABLE_NAME**: 94 unique tables
- **COLUMN_NAME**: 2,879 total columns
- **DATA_TYPE**: SQL Server types (varchar, int, datetime, bit, money, etc.)

**No field descriptions** are provided beyond column names. **No value sets**, no foreign key relationships, no nullability constraints, no sample data. The column names are generally descriptive (e.g., `PatientID`, `BloodPressure`, `DiagnosisCode1`), making many fields self-documenting, but some are opaque (e.g., `MH1` through `MH35` in the pregnancy table, `A1A` through `A15D` in the HCFA table, `I31A` through `I41Fee` in CHDP).

### Data type distribution

| Type | Count | % |
|---|---|---|
| varchar | 1,411 | 49.0% |
| int | 602 | 20.9% |
| datetime | 409 | 14.2% |
| bit | 351 | 12.2% |
| money | 85 | 3.0% |
| Other (decimal, float, xml, image, char, varbinary, uniqueidentifier, date) | 21 | 0.7% |

### Vendor's own content organization

The schema uses table name prefixes (`m` for master/reference tables, `t` for transactional tables) but does not provide explicit categories. Below is a categorization based on table names and field content, with all 94 tables accounted for.

#### Category summary

| Category | Tables | Fields | Key Tables |
|---|---|---|---|
| Billing | 6 | 355 | tHCFAHeader (219), tBillingDetail (33), tBillingHeaderConversion (27) |
| Medications | 7 | 336 | tRefill (125), tPatientMedicationPending (64), tPatientMedication (62) |
| Patient Demographics & Chart | 15 | 267 | mPatient (47), mPatientAdditional (35), mPatientCDP (25) |
| Pregnancy / OB | 1 | 218 | tPregnancy (218) |
| CHDP (Child Health) | 1 | 190 | tVisitCHDP (190) |
| Clinical Breast Exam | 1 | 145 | tCBEExam (145) |
| Laboratory | 4 | 127 | tLabEntryGYN (45), tLabEntry (31), tLabObservation (26) |
| Patient Communications | 4 | 96 | tSMSMessage (32), tEmailMessage (23), tPatientFax (22) |
| Scheduling / Events | 1 | 61 | tEvent (61) |
| Health Measures / Vitals | 2 | 50 | tPatientHealthMeasure (34), mPatientHealthMeasure (16) |
| CPSP (Prenatal/Perinatal) | 2 | 49 | mCPSPPatient (36), mCPSPPatientBillingUnit (13) |
| Immunizations | 1 | 46 | tPatientImmunization (46) |
| UDS Reporting | 1 | 46 | tUDSTableInfoTemp (46) |
| Telehealth | 2 | 44 | tVideoSession (28), tVideoSessionParticipant (16) |
| Accounts Receivable | 2 | 42 | tARCloseAgingTemp (21), tARReceipt (21) |
| Visits / Encounters | 1 | 39 | tVisit (39) |
| Insurance | 2 | 38 | mPatientInsurance (28), mPatientPayerDescriptor (10) |
| Referrals | 1 | 38 | tReferralEntry (38) |
| Dental | 2 | 32 | tExamDentalPlan (17), tExamTooth (15) |
| Case Management | 2 | 32 | tPatientCase (18), tPatientCaseManagement (14) |
| Vitals / Clinical Info | 1 | 32 | tPatientClinicalInfo (32) |
| Clinical Exams | 2 | 29 | tExamHistory (17), tExam (12) |
| Behavioral Health | 1 | 25 | tBHTreatmentPlan (25) |
| Documents | 1 | 24 | mScanDocument (24) |
| Patient Portal | 1 | 24 | mPatientPortal (24) |
| Treatment Plans | 1 | 18 | tPatientTreatmentPlan (18) |
| Patient Education | 1 | 18 | tPatientEducationList (18) |
| Allergies | 1 | 19 | tPatientAllergy (19) |
| Problems / Diagnoses | 1 | 19 | tPatientProblemList (19) |
| Disclosures | 1 | 21 | tPatientDisclosure (21) |
| Patient Assistance Programs | 1 | 19 | mPatientNeedyMed (19) |
| Consents & Authorizations | 1 | 14 | mPatientReleaseAuthorization (14) |
| Clinical Notes | 1 | 14 | mPatientNote (14) |
| Other (signatures, forms, worksheets, etc.) | 14 | 145 | Various small tables |

Full inventory of all 94 entities with all 2,879 fields is in `analysis/entity-inventory-full.json`.

### Notable tables

- **tHCFAHeader** (219 fields): Deeply models the HCFA 1500 claim form with procedure codes, fees, diagnosis codes, charges, payments, adjustments, CHDP codes, and demographic snapshots. This is genuine billing data.
- **tPregnancy** (218 fields): Exhaustively models prenatal care — LMP, EDD calculation methods, obstetric history (GTPAL), genetic history flags (MH1-MH35), substance use, medical history, birth outcome, delivery details. This is deep specialty clinical data.
- **tVisitCHDP** (190 fields): Child Health and Disability Prevention program visit data with procedure codes, fees, and screening results.
- **tCBEExam** (145 fields): Clinical breast examination with detailed anatomical findings.
- **tRefill** (125 fields): Prescription refill workflow with Surescripts integration fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export reflects AXEIUM's native database structure, covering the system's core clinical and administrative domains:

**Deepest coverage (>100 fields):**
- Billing/HCFA claims (355 fields across 6 tables) — genuinely deep modeling of FQHC billing including HCFA 1500, payment details, billing conversions
- Medications (336 fields across 7 tables) — active meds, pending meds, refills with Surescripts e-prescribing integration, prescription history, medication review
- Pregnancy/OB (218 fields) — comprehensive prenatal record with obstetric history, EDD calculations, medical history, delivery details
- CHDP child health visits (190 fields) — screening results, procedure codes, fees

**Moderate coverage (20-100 fields):**
- Patient demographics (267 fields across 15 tables) — extensive socioeconomic data appropriate for FQHC population
- Laboratory (127 fields across 4 tables) — lab orders, results, GYN-specific labs, observations
- Patient communications (96 fields) — email, SMS, fax, call queue
- Immunizations (46 fields) — detailed vaccination record

**Thinner coverage (< 20 fields):**
- Dental (32 fields, 2 tables) — tooth charting and dental treatment plans are present but thin relative to the dental module's described capabilities (no periodontal charting table visible)
- Behavioral health (25 fields, 1 table) — only the BH treatment plan; assessment scoring is present but the SIRP workflow and intake forms are not distinctly represented
- Vision — **no dedicated vision tables** in the schema
- Clinical notes (14 fields, 1 table) — mPatientNote is small; rich text documents are said to be exported separately

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | mPatient (47), mPatientAdditional (35), mPatientEmployment (16), mPatientEthnic (10), mPatientRace (10), + 10 more tables | Thorough — 15 tables, 267 fields covering demographics, employment, language, race/ethnicity, family, preferences |
| Encounters / visits | ✅ Covered | tVisit (39 fields) with visit date, provider, facility, billing status, program | Adequate single table with key encounter metadata |
| Problems / conditions | ✅ Covered | tPatientProblemList (19 fields) with SNOMED_CID, SNOMED_FSN, ICD codes, severity, status, resolution | Good — coded diagnoses with SNOMED |
| Medications / prescriptions | ✅ Covered | 7 tables, 336 fields — active meds, pending, refills, prescription sends, medication review, logs | Deep — includes e-prescribing integration |
| Allergies | ✅ Covered | tPatientAllergy (19 fields) with allergy groups, reactions, LexiComp severity codes | Good — coded with severity |
| Immunizations | ✅ Covered | tPatientImmunization (46 fields) | Thorough |
| Vitals | ✅ Covered | tPatientClinicalInfo (32 fields) — height, weight, BP, pulse, temp, RR, HbA1c, blood sugar; also tPatientHealthMeasure (34) and mPatientHealthMeasure (16) | Good |
| Lab results | ✅ Covered | tLabEntry (31), tLabEntryGYN (45), tLabObservation (26), tPatientLab (25) | Good — 4 tables, 127 fields including GYN-specific |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging table; mScanDocument (24) may capture some imaging references | Product integrates with DEXIS and Planmeca; imaging data may be stored externally |
| Procedures | ⚠️ Partial | Procedure codes in billing tables (tHCFAHeader, tBillingDetail) but no standalone procedures table | Procedures are captured through billing, not as a discrete clinical entity |
| Clinical notes / documents | ✅ Covered | mPatientNote (14 fields) + mScanDocument (24 fields) + separate rich text/image export | EHI page explicitly mentions separate download for rich text documents and images |
| Care plans / goals | ✅ Covered | tPatientTreatmentPlan (18), tBHTreatmentPlan (25) | Treatment plans present for general and BH |
| Orders / referrals | ✅ Covered | tReferralEntry (38 fields) | Referral tracking present; medication orders via tPatientMedicationPending |
| Insurance / coverage | ✅ Covered | mPatientInsurance (28 fields) with policy/group numbers, payer IDs, copay, guarantor, dates | Good |
| Claims / billing | ✅ Covered | tHCFAHeader (219), tBillingDetail (33), tBillingHeader (27), tBillingPaymentDetail (21), tBillingDetailConversion (28), tBillingHeaderConversion (27) | **Exceptionally deep** — 6 tables, 355 fields covering HCFA 1500 claims, payments, adjustments, conversions |
| Payments | ✅ Covered | tBillingPaymentDetail (21), tARReceipt (21), tARCloseAgingTemp (21) | A/R and payment tracking present |
| Consents / directives | ✅ Covered | mPatientReleaseAuthorization (14 fields) | Basic consent/release tracking |
| Patient communications | ✅ Covered | tEmailMessage (23), tSMSMessage (32), tPatientFax (22), tCallQueueItem (19) | Good — 4 channels, 96 fields |
| Specialty: Dental | ⚠️ Partial | tExamTooth (15), tExamDentalPlan (17) | **Gap**: Product has full dental module with periodontal charting, CDT coding, imaging integration — only tooth charting and treatment plans exported (32 fields for an entire dental module is thin) |
| Specialty: Vision | ❌ Not covered | No vision-related tables in schema | **Significant gap**: Product has a vision module (refraction, Rx, anterior/posterior segment, tonometry, gonioscopy) but no vision data appears in the export |
| Specialty: Behavioral Health | ⚠️ Partial | tBHTreatmentPlan (25), tAssessmentScore (18) | **Gap**: Product has SIRP workflow, intake forms, assessment management — only treatment plan and assessment scores exported |
| Specialty: Pregnancy/OB | ✅ Covered | tPregnancy (218 fields), mCPSPPatient (36), mCPSPPatientBillingUnit (13) | **Exceptionally deep** — comprehensive prenatal record |
| Specialty: Child Health (CHDP) | ✅ Covered | tVisitCHDP (190 fields) | Deep — full CHDP screening form |
| Family health history | ✅ Covered | mPatientFamilyMember (13 fields) | Present |
| Telehealth | ✅ Covered | tVideoSession (28), tVideoSessionParticipant (16) | Video visit tracking |
| Patient portal | ✅ Covered | mPatientPortal (24 fields) | Portal account data |

## 6. Documentation Quality

**Strengths:**
- The Schema.pdf provides a complete inventory of all 94 exported tables and 2,879 columns with data types
- The EHI page clearly describes the export format (TSV), export mechanism (manual initiation), and that rich text/images are handled separately
- Column names are largely self-documenting for standard clinical fields

**Weaknesses:**
- **No field descriptions**: The schema provides only column names and SQL types — no prose descriptions, no business definitions
- **No value sets or code systems**: Fields like `SeverityID`, `StatusID`, `GenderID`, `RaceID` reference lookup tables but those tables are not documented
- **No foreign key documentation**: Relationships between tables (e.g., `PatientID`, `VisitID`) are inferable but not explicitly documented
- **No sample data**: No example export files provided
- **No machine-readable schema**: Only a PDF generated from Excel
- **Opaque field names**: Many fields use abbreviated naming (e.g., `MH1`-`MH35` in tPregnancy, `A1A`-`A15D` in tHCFAHeader, `GH1`-`GH18` in tPregnancy) that cannot be understood without additional documentation
- **No lookup/reference tables**: The export appears to include only patient-record tables; the associated reference tables (for coded values like `GenderID`, `RaceID`, `SeverityID`) are not listed

**Usability assessment**: A developer could understand the basic structure and load the TSV files, but would struggle with coded fields lacking value set documentation. Reconstructing the full data model would require reverse-engineering foreign key relationships. The opaque abbreviated fields in the pregnancy and CHDP tables would be essentially unusable without reference documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers a meaningful breadth of what AXEIUM stores but has notable gaps in specialty modules. The billing domain is exceptionally well-represented (355 fields, 6 tables — genuine claim-level data, not just summary charges). Demographics, medications, labs, and pregnancy/OB are deep. However, the **vision module is completely absent** from the export despite being a core product capability. Dental coverage (32 fields for an entire dental module with charting, perio, CDT coding) is thin. Behavioral health shows only treatment plans and assessment scores, missing the SIRP workflow. These specialty gaps prevent a "Comprehensive" rating — for a product whose differentiator is multi-service-line integration (medical + dental + vision + behavioral health), exporting three of four service lines incompletely or not at all is a meaningful shortfall.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange format. Key evidence:
1. The export uses AXEIUM's native database table structure (94 tables as TSV), not FHIR or C-CDA
2. It includes billing data (HCFA 1500 claims, A/R), patient communications (email, SMS, fax), case management, telehealth sessions, and other non-USCDI domains
3. HTML comments in the EHI page show the vendor deliberately removed references to FHIR and C-CDA from the (b)(10) documentation (v3, 2023-10-25), distinguishing this export from clinical exchange
4. The schema covers 94 tables with 2,879 columns — far exceeding what any clinical exchange standard would include
5. No reference to USCDI, US Core, or clinical exchange standards in the export documentation

### Key Findings

1. **Purpose-built with genuine billing depth**: The export includes 6 billing tables with 355 fields covering HCFA 1500 claims, payment details, and accounts receivable — this is real financial data, not a token billing section. The vendor clearly engaged with (b)(10) requirements beyond clinical summaries.

2. **Vision module completely missing**: AXEIUM markets a dedicated vision module (refraction, Rx history, tonometry, gonioscopy, segment documentation), but no vision-related tables appear in the 94-table export schema. This is the largest gap.

3. **Dental export is thin**: Only 2 tables (tExamTooth, tExamDentalPlan) with 32 fields for an entire dental module that includes periodontal charting, CDT coding, imaging integration. The product's dental charting capabilities appear significantly under-represented.

4. **No field descriptions or value sets**: The 62-page Schema.pdf provides only column names and SQL data types. No descriptions, no value set definitions, no foreign key documentation. Dozens of fields use opaque abbreviations (MH1-MH35, GH1-GH18, A1A-A15D) that are unusable without additional reference material.

5. **Pregnancy/OB is exceptionally deep**: The tPregnancy table alone has 218 fields covering the full prenatal record. Combined with CPSP tables (49 fields) and CHDP (190 fields), maternal/child health is the export's strongest domain — reflecting AXEIUM's FQHC focus.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   TSV (tab-separated values) + separate rich text/image files
Entities:        94 tables
Fields:          2,879
Descriptions:    0% (names and types only, no descriptions)
Sample data:     No
Bulk export:     Yes (one or more patients)
Domains covered: 17 of 21 applicable domains (vision missing; dental and behavioral health partial)
```

### Bottom Line

AXEIUM built a genuine (b)(10) export that dumps its native database tables as TSV files, covering clinical, billing, communications, and administrative data across 94 tables and 2,879 fields. The export is strongest in billing (HCFA 1500 claims), pregnancy/OB, and medications, and weakest in the specialty modules that define the product — vision is entirely absent, and dental and behavioral health are significantly under-represented. The documentation provides structure (table/column/type) but no field descriptions or value sets, making opaque fields in large tables unusable without vendor assistance.
