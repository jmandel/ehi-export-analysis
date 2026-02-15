# EHI Export Analysis: Brilogy Corporation

**Product**: AXEIUM  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.05.05.1171.BRIL.02.01.1.221219 (CHPL listing 11086)

## 1. Product Context

AXEIUM is a full-featured, multi-specialty EHR and practice management system built specifically for Federally Qualified Health Centers (FQHCs) and community health centers. Developed by Brilogy Corporation (Santa Ana, CA) through a decade-long grant-funded consortium effort, it is purpose-built for safety-net organizations that deliver **medical, dental, vision, and behavioral health** services under one roof.

Key data domains the product stores:

- **Patient demographics**: extensive registration data including race/ethnicity, language, employment, family, insurance, poverty scale, program enrollment
- **Medical clinical data**: problem lists (SNOMED/ICD), medications (Lexicomp), allergies (RxNorm), vitals, lab orders/results (LOINC), immunizations, clinical exams, SOAP notes, CDS alerts, health maintenance
- **Dental**: tooth charting, periodontal charting, treatment plans, CDT codes
- **Vision**: refraction, tonometry, gonioscopy, anterior/posterior segments
- **Behavioral health**: intake assessments, SIRP documentation, treatment plans
- **Pregnancy/perinatal**: detailed pregnancy tracking, CPSP (Comprehensive Perinatal Services Program)
- **Billing**: HCFA 1500, PM-160 (FQHC-specific), electronic billing, superbills, AR
- **Documents**: scanned documents, clinical images, annotations
- **Administrative**: scheduling, check-in/out, referrals, communications, task management

The FQHC specialization means extensive support for California-specific programs (CHDP, CPSP, CDP, OSHPD) and safety-net workflows (sliding fee scale, financial assistance, NeedyMeds).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Schema.pdf` (1,061,219 bytes, 62 pages) | Data dictionary for the EHI export — generated from Excel by Milton Allione on 2023-10-22. Lists TABLE_NAME, COLUMN_NAME, and DATA_TYPE for every table/column in the export. **94 tables, 2,879 columns.** | **Primary artifact** — the core of the analysis |
| `downloads/ehi-page.html` (29,980 bytes) | HTML source of axeium.com/EHI. Describes the export as tab-separated files in AXEIUM's native record layout. Contains HTML comments showing version history and deliberate removal of FHIR/C-CDA references. | **Important** — establishes export mechanics and vendor intent |
| `downloads/screenshot-ehi-page.png` (471,279 bytes) | Browser screenshot of the EHI page confirming visible content. | Confirmatory |
| `downloads/screenshot-ehi-page-full.png` (471,279 bytes) | Full-page screenshot — identical to viewport screenshot (all content above fold). | Confirmatory |

The Schema.pdf is by far the most informative artifact. The EHI page is a single-page description with one linked document.

## 3. Export Mechanics

- **Format**: Tab-separated files in AXEIUM's native database record layout, with separate file downloads for rich text documents and images referenced from the tables
- **Mechanism**: System users can manually initiate an export for one or more patients via the application UI. The EHI page says: "If you need assistance, please contact Customer Support."
- **Single-patient vs bulk**: The page says "one or more patients," indicating both single and multi-patient export are supported
- **Access constraints/fees**: No fees mentioned on the EHI page. The vendor's Certifications page (referenced in CHPL metadata) discloses pricing for the system itself but not for exports specifically
- **Standards relationship**: The HTML source contains a commented-out section (removed in v3, 2023-10-25, "per guidance from kendra/sli") that previously referenced FHIR Bulk Data Access and C-CDA as additional exchange methods. The deliberate removal of these references indicates the vendor correctly distinguishes the native (b)(10) export from the standards-based (g)(10) API

## 4. Export Content: What's In It

### Data dictionary structure

The Schema.pdf provides three columns per field:
- **TABLE_NAME**: the export table/file name
- **COLUMN_NAME**: the field name
- **DATA_TYPE**: SQL Server data type (varchar, int, datetime, bit, money, float, decimal, xml, image, char, varbinary, uniqueidentifier, date)

There are **no field descriptions, no value set definitions, no foreign key documentation, and no sample data**. The schema is purely structural: names and types.

### Verified counts

- **94 tables** (confirmed by independent parsing of PDF text extraction)
- **2,879 columns** total (the prior report stated 2,818 — the discrepancy of 61 columns is due to form-feed characters at PDF page boundaries causing `grep` to miss lines; my parsing script handles these correctly)
- **0 fields with descriptions** (0%) — only names and data types are provided
- **Data types**: varchar (1,411), int (602), datetime (409), bit (351), money (85), decimal (6), float (4), xml (3), image (3), char (2), varbinary (1), uniqueidentifier (1), date (1)

### Vendor's own content organization

The schema does not include vendor-defined categories — tables are listed in alphabetical order. The categorization below is based on table naming conventions and column content analysis. A full inventory of all 94 tables with their columns is saved in `analysis/full-entity-inventory.json`.

**Category breakdown** (18 categories, 94 tables, 2,879 fields):

| Category | Tables | Fields | Key Tables |
|---|---|---|---|
| Patient Demographics & Registration | 15 | 266 | mPatient (47), mPatientAdditional (35), mPatientOtherInformation (27) |
| Clinical Data | 18 | 449 | tCBEExam (145), tPatientHealthMeasure (34), tPatientClinicalInfo (32) |
| Medications | 7 | 336 | tRefill (125), tPatientMedicationPending (64), tPatientMedication (62) |
| Lab & Diagnostics | 4 | 127 | tLabEntryGYN (45), tLabEntry (31), tLabObservation (26) |
| Immunizations | 1 | 46 | tPatientImmunization (46) |
| Dental | 2 | 32 | tExamDentalPlan (17), tExamTooth (15) |
| Behavioral Health | 2 | 43 | tBHTreatmentPlan (25), tPatientTreatmentPlan (18) |
| Pregnancy / Perinatal | 3 | 267 | tPregnancy (218), mCPSPPatient (36), mCPSPPatientBillingUnit (13) |
| Billing & Financial | 11 | 451 | tHCFAHeader (219), tBillingDetail (33), tPurchaseOrder (30) |
| Insurance | 2 | 38 | mPatientInsurance (28), mPatientPayerDescriptor (10) |
| Visits & Scheduling | 3 | 290 | tVisitCHDP (190), tEvent (61), tVisit (39) |
| Documents & Imaging | 2 | 37 | mScanDocument (24), mSignature (13) |
| Communications | 3 | 77 | tSMSMessage (32), tEmailMessage (23), tPatientFax (22) |
| Referrals & Care Coordination | 3 | 70 | tReferralEntry (38), tPatientCase (18), tPatientCaseManagement (14) |
| Administrative | 10 | 188 | tVideoSession (28), tTaskItem (26), tPatientAuditLog (22) |
| Financial Assistance | 2 | 44 | mPatientCDP (25), mPatientNeedyMed (19) |
| Regulatory / Reporting | 2 | 60 | tUDSTableInfoTemp (46), tOSHPDException (14) |
| Other | 4 | 58 | mPatientNote (14), mPatientProgram (14), etc. |

### Notable tables

**Largest tables (reflecting FQHC specialization):**

- **tHCFAHeader** (219 columns): Complete HCFA 1500 claim form data with diagnosis codes, procedure codes (up to 41 line items: A1–A41 with ProcCode, Fee, Modifier fields), payer information, and billing totals
- **tPregnancy** (218 columns): Extremely detailed pregnancy tracking including LMP, EDC, delivery data, newborn data, prenatal visits, genetic screening, ultrasound findings, labor/delivery complications, anesthesia consent, and tubal ligation consent
- **tVisitCHDP** (190 columns): Child Health and Disability Prevention visit form — a California-specific well-child visit with developmental screening, immunization tracking, lab results, and up to 41 procedure line items
- **tCBEExam** (145 columns): **Clinical Breast Exam** form (note: the prior report misidentified this as dental; column names like `PCLump`, `BFMass`, `CBEResult`, `BCHMotherAge` clearly indicate breast cancer screening) — includes family history, presenting complaints, breast findings, diagnostic mammography, lymph nodes, and follow-up
- **tRefill** (125 columns): Surescripts e-prescribe refill requests with full pharmacy, prescriber, patient, prescribed drug, and dispensed drug details

**Correction from prior report**: The prior report categorized `tCBEExam` as a dental table. It is actually a Clinical Breast Exam table — a women's health screening form consistent with California's Cancer Detection Programs (CDP) that FQHCs participate in. The `mPatientCDP` table (25 columns) contains related CDP enrollment data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers an unusually broad range of domains for a small vendor, reflecting AXEIUM's integrated EHR+PM design for FQHCs:

**Deepest coverage (most tables/fields):**
- **Billing & Financial** (11 tables, 451 fields): The most thoroughly represented domain. The tHCFAHeader table alone has 219 columns capturing the complete HCFA 1500 claim form. Includes billing headers/details, payment details, AR receipts, aging data, and purchase orders.
- **Clinical Data** (18 tables, 449 fields): Broad clinical coverage including exams, allergies, problem lists, conditions, health measures, clinical info (vitals), assessment scores, clinical breast exams, worksheets, and education.
- **Medications** (7 tables, 336 fields): Deep medication tracking — active meds, pending orders, prescriptions sent, refills (with full Surescripts e-prescribe data), medication logs, and medication reviews.
- **Visits & Scheduling** (3 tables, 290 fields): Visit records with specialized CHDP visit forms (190 columns for well-child visits) and event/appointment data.
- **Pregnancy / Perinatal** (3 tables, 267 fields): Exceptionally detailed — the tPregnancy table has 218 columns covering the full pregnancy lifecycle. CPSP enrollment and billing units are separate tables.
- **Patient Demographics** (15 tables, 266 fields): Comprehensive demographics with separate tables for race, ethnicity, employment, family members, preferences, portal status, representatives, and USCDI v1 fields (sexual orientation, gender identity in mPatientAdditional).

**Moderate coverage:**
- **Lab & Diagnostics** (4 tables, 127 fields): Lab entries, observations, and a specialized GYN lab form (45 columns for cervical screening, STD tracking, HPV).
- **Communications** (3 tables, 77 fields): Email, SMS, and fax records to patients.
- **Referrals** (3 tables, 70 fields): Referral entries with full details and case management.
- **Immunizations** (1 table, 46 fields): Detailed immunization table with CVX codes, VIS dates, lot numbers, and registry submission fields.
- **Financial Assistance** (2 tables, 44 fields): NeedyMeds pharmaceutical assistance and California Cancer Detection Programs enrollment.
- **Insurance** (2 tables, 38 fields): Patient insurance and payer descriptors.

**Thinnest coverage:**
- **Dental** (2 tables, 32 fields): Only dental treatment plans and tooth-level charting. The product's periodontal charting module (probe depths, mobility, periodontitis) is not visible as a dedicated table — it may be stored in the general exam structure or may be a gap.
- **Behavioral Health** (2 tables, 43 fields): Treatment plans exist but the product's SIRP workflow, intake assessments, and assessment questionnaire structures are not represented as dedicated tables. Assessment scores are captured in `tAssessmentScore` (18 columns) under Clinical Data, but the assessment content/questions are not.
- **Documents** (2 tables, 37 fields): Document metadata (scan references, signatures) — actual documents are provided as separate file downloads per the EHI page.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 15 tables (266 fields): mPatient, mPatientAdditional (with USCDI v1 fields), mPatientRace, mPatientEthnic, mPatientEmployment, etc. | Thorough — includes SOGI, language, family, programs |
| Encounters / visits | ✅ Covered | tVisit (39 fields), tVisitCHDP (190 fields), tEvent (61 fields), tExam (12 fields) | Thorough — specialized CHDP visits are very detailed |
| Problems / conditions / diagnoses | ✅ Covered | tPatientProblemList (19 fields, SNOMED+ICD), tPatientMedicalCondition (17 fields) | Adequate — SNOMED CID and FSN captured |
| Medications / prescriptions | ✅ Covered | 7 tables (336 fields): tPatientMedication (62), tRefill (125), tPatientMedicationPending (64), tPatientMedicationPrescriptionSent (35) | Thorough — full e-prescribe cycle with Surescripts data |
| Allergies | ✅ Covered | tPatientAllergy (19 fields) with AllergyGroupID, Allergy, AllergyReaction, CodesetValue, SeverityCodeLexiComp | Adequate |
| Immunizations | ✅ Covered | tPatientImmunization (46 fields) with CVX codes, lot numbers, VIS dates, funding source, manufacturer | Thorough |
| Vitals | ✅ Covered | tPatientClinicalInfo (32 fields) includes Height, Weight, Pulse, BloodPressure, Temperature, RespiratoryRate, HbA1c, blood sugar | Adequate — stored as part of clinical info, not a dedicated vitals table |
| Lab results | ✅ Covered | 4 tables (127 fields): tPatientLab, tLabEntry, tLabObservation, tLabEntryGYN (45 fields for cervical/STD screening) | Thorough — includes specialized GYN lab form |
| Imaging / diagnostic reports | ⚠️ Partial | mScanDocument (24 fields) references scanned/imported images; tCBEExam references imaging dates. Actual image files provided as separate downloads. No DICOM or radiology report tables. | Product integrates with DEXIS and Planmeca Romexis for dental imaging. Imaging metadata is limited to document references; imaging integration data may be stored externally. Minor gap. |
| Procedures | ✅ Covered | Procedure codes captured in tHCFAHeader (A1–A41 ProcCode fields), tVisitCHDP (I1–I41 ProcCode fields), tExamDentalPlan, mCPSPPatientBillingUnit | Procedures are embedded in billing/visit records rather than a dedicated procedures table |
| Clinical notes / documents | ✅ Covered | mPatientNote (14 fields), mScanDocument (24 fields), tExamHistory (17 fields for structured exam data). Rich text documents and images provided as separate file downloads per EHI page. | Adequate — notes stored as structured references + separate file downloads |
| Care plans / goals | ✅ Covered | tBHTreatmentPlan (25 fields), tPatientTreatmentPlan (18 fields) — both include LongTermGoal, NextReviewDate, PlanStatus, CompletedDate | Adequate for treatment plans; general care plans may not have dedicated structure |
| Orders / referrals | ✅ Covered | tReferralEntry (38 fields), tPatientCase (18), tPatientCaseManagement (14), tLabObservation (26 — includes order data) | Adequate |
| Insurance / coverage | ✅ Covered | mPatientInsurance (28 fields), mPatientPayerDescriptor (10 fields) | Adequate |
| Claims / billing | ✅ Covered | 11 tables (451 fields): tHCFAHeader (219 fields — complete HCFA 1500), tBillingHeader, tBillingDetail, tBillingPaymentDetail, tARReceipt, etc. | Thorough — the deepest domain in the export |
| Payments | ✅ Covered | tBillingPaymentDetail (21 fields), tARReceipt (21 fields), tARCloseAgingTemp (21), tARCloseAgingTempDetail (12) | Thorough |
| Consents / directives | ✅ Covered | mPatientAdditional contains AdvancedDirectiveCode/Desc/Date; mPatientReleaseAuthorization (14 fields); tPatientDisclosure (21 fields — accounting of disclosures) | Adequate |
| Patient communications / portal messages | ✅ Covered | tEmailMessage (23), tSMSMessage (32), tPatientFax (22), mPatientPortal (24 — portal status), tVideoSession (28 — telehealth) | Thorough — includes email, SMS, fax, and video visit data |
| Specialty: Dental | ⚠️ Partial | tExamDentalPlan (17 fields), tExamTooth (15 fields) | Product has periodontal charting (probe depths, mobility, gingivitis/periodontitis). No dedicated periodontal table is visible. May be in general exam structure or may be a gap. |
| Specialty: Vision | ⚠️ Partial | No vision-specific tables. May be stored in tExam/tExamHistory/tPatientClinicalInfo | Product stores refraction, tonometry, gonioscopy, anterior/posterior segment data. No dedicated vision tables exist — likely captured via configurable exam templates. Without sample data, cannot confirm coverage. |
| Specialty: Behavioral Health | ⚠️ Partial | tBHTreatmentPlan (25), tPatientTreatmentPlan (18), tAssessmentScore (18) | Product has SIRP workflow and customizable intake forms. Treatment plans and scores are covered, but assessment content/questionnaire structure is not separately exported. |
| Specialty: Pregnancy/Perinatal | ✅ Covered | tPregnancy (218 fields), mCPSPPatient (36), mCPSPPatientBillingUnit (13) | Exceptionally thorough — 267 fields covering full pregnancy lifecycle and CPSP program |
| Specialty: Women's Health Screening | ✅ Covered | tCBEExam (145 fields), tLabEntryGYN (45 fields), mPatientCDP (25 fields) | Thorough — clinical breast exam, GYN labs, Cancer Detection Program enrollment |

## 6. Documentation Quality

**Strengths:**
- The Schema.pdf is a complete, machine-generated inventory of every table and column in the export — nothing is hidden or omitted
- Data types are specified for all 2,879 fields using SQL Server types
- The EHI page is clear and concise about the export format, scope, and variability
- The vendor demonstrates understanding of (b)(10) vs (g)(10) — they deliberately removed FHIR/C-CDA references from the page (HTML comments show this was done "per guidance from kendra/sli")
- The export is correctly scoped as a native database dump, not a repackaged standards-based export

**Weaknesses:**
- **No field descriptions** (0% of 2,879 fields described): Many column names are self-explanatory (`FirstName`, `DateOfBirth`, `DiagnosisCode1`) but many are cryptic (`BCRCOZMPA`, `I40CHDPCode`, `mSCBaselinePatientValue`, `PCNippleSkinC`). Approximately 59% of field names contain recognizable keywords; 41% require domain knowledge to interpret.
- **No value set documentation**: Coded fields (e.g., `ArchiveMethodID`, `BabyGenderCode`, `ClosureReason`, `SeverityID`, `StatusID`, `RefusedCode`) have no documented valid values
- **No foreign key documentation**: Tables share ID columns (`PatientID`, `VisitID`, `ProviderID`, `ExamID`) but relationships are implicit, not documented
- **No sample data or export examples**: No sample export files are provided anywhere
- **No export workflow documentation**: Beyond "contact Customer Support," there are no instructions on how to initiate an export, what the output looks like, or how files are organized
- **PDF-only format**: The schema is only available as a PDF generated from Excel. No machine-readable schema (SQL DDL, JSON Schema, CSV) is published, though the underlying spreadsheet presumably exists

**Could a developer build an import from this documentation?** Partially. The table and column names provide enough structure to parse the tab-separated files, and data types allow basic type mapping. However, without value sets, foreign key documentation, or sample data, a developer would need significant reverse-engineering effort to interpret coded fields and understand inter-table relationships.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native database export covering 94 tables and 2,879 fields across clinical, billing, administrative, and specialty domains. It is not a repackaged FHIR API or C-CDA summary. The vendor deliberately separated this from their FHIR/C-CDA capabilities and exports the full internal data model. Coverage spans nearly all data domains the product stores, with only partial gaps in some specialty areas (dental periodontal, vision, behavioral health assessment content).

### Key Findings

1. **Genuine (b)(10) effort with broad coverage**: 94 tables across 18 domain categories covering demographics, clinical data, medications, labs, immunizations, billing (the largest domain at 451 fields), insurance, visits, documents, communications, referrals, and multiple specialty areas. The vendor correctly chose native export over standards repackaging.

2. **Unusually deep FQHC-specific and women's health data**: The export includes California-specific program tables (CPSP, CHDP, CDP, OSHPD, NeedyMeds) that reflect the product's safety-net specialization. The tPregnancy table (218 columns) and tCBEExam (145 columns for clinical breast exams) are more detailed than almost any comparable vendor's export.

3. **Documentation is structurally complete but descriptively empty**: Every table and column is listed with its data type, but 0% of fields have human-readable descriptions, no value sets are documented, and no foreign keys are specified. The schema tells you *what* is exported but not *what it means*.

4. **Specialty clinical data may be partially captured via generic structures**: Vision, dental periodontal, and behavioral health assessment content likely flow through configurable exam templates (tExam, tExamHistory, tExamSurvey) rather than dedicated tables. Without sample data, the actual coverage of these specialties cannot be fully verified.

5. **Prior report contained a factual error**: The `tCBEExam` table (145 columns) was misidentified as dental; it is a Clinical Breast Exam screening form. This correction moves the table from the Dental category to Clinical Data and slightly reduces the apparent dental coverage.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   TSV (tab-separated values) + separate file downloads for documents/images
Model type:      Native database
Entities:        94 tables
Fields:          2,879 columns
Descriptions:    0% (names and types only)
Sample data:     No
Bulk export:     Yes (one or more patients)
Domains covered: 15 of 17 applicable domains fully covered; 3 specialty domains partially covered
```

### Bottom Line

AXEIUM's EHI export is one of the more complete (b)(10) implementations from a small vendor. A patient or provider would get a genuinely broad copy of their data — clinical records, billing, medications, labs, immunizations, pregnancy data, and more — in a structured, parseable format. The single biggest weakness is documentation quality: the schema has no field descriptions, no value sets, and no sample data, which means a receiving party would need significant domain expertise to interpret the export. The single biggest strength is breadth: 94 tables covering billing, clinical, and FQHC-specific specialty data that would be entirely absent from a C-CDA or FHIR-based export.
