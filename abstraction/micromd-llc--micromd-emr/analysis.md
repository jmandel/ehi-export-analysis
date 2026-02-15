# EHI Export Analysis: MicroMD, LLC

**Product**: MicroMD EMR Version 20.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2753.Micr.20.07.1.230427 (CHPL #11281)

## 1. Product Context

MicroMD EMR is a 2015 Edition CEHRT ambulatory electronic medical records system developed by MicroMD, LLC (a subsidiary of Henry Schein Medical Systems). It targets small-to-medium independent practices, multi-specialty groups, community health centers (CHCs), FQHCs, and rural health centers. The product supports eight named specialties: Cardiology, Dermatology, ENT, Gastroenterology, Ob-Gyn, Pediatrics, Primary Care, and Urology.

The EMR is part of a broader product suite including:
- **MicroMD PM** (Practice Management): scheduling, registration, claims, payment posting, A/R
- **MicroMD DMS** (Document Management): scanned documents, e-faxes, pathology results
- **Secure Chart** (Patient Portal): secure messaging, appointment requests, intake forms, lab results

Key data domains the product stores (relevant for export completeness assessment):
- Clinical documentation (SOAP notes, problem lists, medication lists, allergy lists)
- E-prescribing (via Surescripts, including controlled substances via EPCS)
- Lab results (interfaces with LabCorp, Quest, etc.)
- Medical device data (ECGs, spirometry, Holter via Welch Allyn, Midmark, Burdick)
- Immunization records
- Specialty-specific clinical data (vision, hearing, diabetes, OB/GYN, pediatric, geriatric)
- Billing/superbill data (CPT, ICD-10, modifiers, insurance)
- Insurance/coverage information
- Patient demographics (including SOGI)
- Document management content
- Patient portal communications

Per ONC guidance, the (b)(10) requirement covers "all electronic health information that can be stored at the time of certification by the product, of which the Health IT Module is a part" — encompassing the full integrated suite.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `MicroMD-EMR-170.315b10-Electronic-Health-Information-export-EHI.pdf` | 17-page PDF (326 KB) dated Feb 6, 2026. Contains complete XML schema for the EHI export, listing all XML elements and attributes across 11 XML files. Created in Microsoft Word by "Creative Group." | **Primary source** — the sole technical documentation for the export |
| `screenshot-certification-page.png` | Screenshot of the MicroMD certification page at micromd.com showing the EHI export PDF link | Low — confirms the PDF is publicly linked from the certification page |
| `files.json` | Manifest of collected artifacts | Orientation only |
| `product-research.md` | Prior research on MicroMD's product capabilities | Context for coverage assessment |
| `chpl-metadata.json` | CHPL certification details | Confirms certification status and criteria |

The analysis relies entirely on the single PDF artifact. No sample data, no machine-readable schema (XSD/JSON Schema), and no data dictionary with field descriptions were provided.

## 3. Export Mechanics

- **Format**: Proprietary XML files bundled in a compressed (ZIP) archive. Not FHIR, not C-CDA.
- **Mechanism**: UI-based export within MicroMD EMR ("see user manual for instruction" — the user manual is not publicly available)
- **Scope**: Single-patient export. File naming convention: `{practiceId}.{patientChartId}.0`
- **Security**: ZIP is password-protected using the patient's date of birth in `mmddyyyy` format
- **Bulk capability**: No evidence of bulk/multi-patient export capability
- **Fees/constraints**: Not documented in the available artifact
- **DMS inclusion**: Additional files from the Document Management System are included in their original formats (PDF, DOC, RTF, CCD, XML, images, etc.)

## 4. Export Content: What's In It

The export is defined by a proprietary XML schema documented in the PDF. Based on programmatic parsing of the extracted PDF text (see `analysis/parse_schema.py`):

- **11 XML files** (10 structured data files + DMS attachments in native formats)
- **150 distinct XML element types** (entity types)
- **2,996 total attributes** (fields) across all elements
- **0 field descriptions** — no attribute has a definition, data type, or value set documented
- **0 sample data** — no example records provided
- **No XSD or machine-readable schema** — the schema is rendered as prose in the PDF

### Vendor's own content organization

The vendor organizes the export into 11 XML files. The following table shows each file with its element and attribute counts (generated from `analysis/parse_schema.py`, full inventory in `analysis/full-entity-inventory.json`):

| XML File | Elements | Attributes | Content Summary |
|---|---|---|---|
| Billing.xml | 7 | 68 | Superbills, diagnoses, procedures, modifiers, referring physicians, insurance |
| Encounters.xml | 21 | 285 | SOAP documentation, assessments, medications, plans/orders, notes (text + audio), face time |
| HealthScreening.xml | 22 | 374 | Goal monitoring, health concerns, screenings (LOINC), immunizations (CVX/NDC), risk factors, prevention |
| Histories.xml | 13 | 336 | Family/medical/social/surgical history, birth, sexual, asthma, habits, hospitalizations, consent |
| MedicalInfo.xml | 29 | 521 | Allergies, problems (ICD-10/SNOMED + cancer staging), vitals, medications, test results (LOINC), behavioral health, CDS, ultrasound, operations, treatment plans |
| Miscellaneous.xml | 7 | 141 | Attachments, letters, advance directives, patient education, referrals in, transitions of care |
| Orders.xml | 1 | 23 | Orders with category, priority, sender/receiver, status |
| Patient.xml | 10 | 312 | Demographics (SOGI, race/ethnicity), addresses, family, contacts, insurance (detailed), providers, consent |
| Schedule.xml | 1 | 15 | Appointments with status, provider, times, department, specialty |
| Specialty.xml | 18 | 287 | Vision, hearing, diabetes, pediatric developmental, genetic, geriatric, allergy testing |
| WomenHealth.xml | 21 | 634 | OB care, initial exams, OB medical history (163 fields), genetics, deliveries, prenatal, EDD, labor progress, pregnancies, gynecology, menstrual, family planning |

**Notable entities by size:**

| Element | File | Attributes | Significance |
|---|---|---|---|
| MedicalHistory (OB) | WomenHealth.xml | 163 | Extremely detailed — 40+ condition fields each with status, comment, detail, and SNOMED code sub-attributes |
| Test (Vision) | Specialty.xml | 80 | Detailed ophthalmic data: acuity, prescriptions (present/recommended), prism values |
| Demographic | Patient.xml | 69 | Comprehensive demographics including SOGI, immigration date, religion, yearly income |
| Medication (chart-level) | MedicalInfo.xml | 61 | Full medication record: NDC, RxNorm, GCN, dispensing, refills, duration, status |
| Insurance | Patient.xml | 61 | Detailed policy data including carrier, plan, policyholder demographics, copay/deductible |
| Immunization Detail | HealthScreening.xml | 54 | CVX codes, NDC, lot numbers, administration details, VIS sheets, side effects |
| Ultraspimd | MedicalInfo.xml | 49 | Fetal ultrasound: BPD, crown-rump length, femur, humerus, head circumference, amniotic fluid |
| Asthma | Histories.xml | 48 | Detailed trigger/symptom tracking, PFT values (FEV1, FVC, PEF), severity, admissions |
| Vital | MedicalInfo.xml | 45 | BP, HR, RR, temp, BMI, O2 sat, pain, head circ, peak flow, blood sugar, OB-specific vitals |

**Standard code systems referenced across the schema:**

| Code System | Attribute Names | Occurrences |
|---|---|---|
| SNOMED CT | `snocode` | 59 |
| LOINC | `loinc` | 18 |
| ICD-10/ICD | `icdcode`, `icd10code` | 14 |
| CPT | `cptcode` | 9 |
| NDC | `ndc` | 5 |
| NPI | `npi`, `NPI` | 3 |
| RxNorm | `rxnorm`, `RXNorm` | 2 |
| CVX | `cvxcode` | 1 |
| GCN Seq No | `gcnseqno` | 2 |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a genuinely broad range of data across MicroMD's product:

**Richest areas (most elements and attributes):**
- **WomenHealth.xml** (634 attributes): Extraordinarily detailed OB/GYN module — the OB MedicalHistory element alone has 163 attributes tracking 40+ conditions each with status, comment, detail, and SNOMED code. Prenatal visits, deliveries (including fetal data, labor events, complications), pregnancy history, gynecology, menstrual history, and family planning are all granular.
- **MedicalInfo.xml** (521 attributes): The clinical core — allergies, problems, vitals, medications, test results, behavioral health screenings, clinical decision support, operations/procedures, and treatment plans. Problems include cancer staging data.
- **HealthScreening.xml** (374 attributes): Goal monitoring, health concerns with care teams, LOINC-coded health screenings, detailed immunization records, risk factors, and prevention programs.
- **Histories.xml** (336 attributes): Comprehensive patient history — family, medical, social, surgical — plus specialized modules for birth, sexual, and asthma history. Hospitalization records include procedures, diagnoses, and reports.
- **Patient.xml** (312 attributes): Thorough demographics including SOGI data, multiple address types, detailed insurance policies with policyholder information.
- **Specialty.xml** (287 attributes): Specialty-specific clinical modules for vision (ophthalmology), hearing (audiology), diabetes management (including insulin pump settings), pediatric developmental assessments, genetic screenings, geriatric assessments, and allergy skin testing.

**Thinnest areas:**
- **Schedule.xml** (15 attributes): Single Appointment element — sufficient for appointment data.
- **Orders.xml** (23 attributes): Single Order element — captures the basics but limited depth.
- **Billing.xml** (68 attributes): Superbill-level billing — captures clinical billing events (CPT codes, diagnoses, modifiers, insurance) but this is encounter-level billing, not the full practice management financial lifecycle.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient.xml` → Demographic (69 fields), Current/Alternate addresses (30 each), Contact (26), FamilyMember (4) | Thorough — includes SOGI, race/ethnicity, multiple addresses, employment, language, religion |
| Encounters / visits | ✅ Covered | `Encounters.xml` → Encounters (full SOAP structure with 21 element types, 285 fields); `Schedule.xml` → Appointment (15 fields) | Deep — full SOAP documentation with assessments, subjectives, objectives, review of problems, plans |
| Problems / conditions / diagnoses | ✅ Covered | `MedicalInfo.xml` → Problem (20 fields) + Cancer (23 fields); `Encounters.xml` → Assessment (14 fields); `Histories.xml` → Medical (34 fields) | Thorough — ICD-10/SNOMED coded, includes cancer staging, chronicity, laterality |
| Medications / prescriptions | ✅ Covered | `MedicalInfo.xml` → Medication (61 fields); `Encounters.xml` → Medication (41 fields) + MedicationSig (21 fields) | Deep — NDC, RxNorm, GCN, dispensing details, multi-sig support, refill tracking, termination codes |
| Allergies | ✅ Covered | `MedicalInfo.xml` → Allergies (31 fields) | Thorough — coded types, severity, reactions, reference codes |
| Immunizations | ✅ Covered | `HealthScreening.xml` → Immunization (21 fields) + Detail (54 fields) + Info (11) + Vis (12) | Very detailed — CVX codes, NDC, lot numbers, VIS sheet tracking, side effects, refusal reasons |
| Vitals | ✅ Covered | `MedicalInfo.xml` → Vital (45 fields) | Comprehensive — includes standard vitals plus blood sugar, peak flow, O2/flow rate, OB-specific vitals, waist circumference |
| Lab results | ✅ Covered | `MedicalInfo.xml` → TestResults (28 fields) | LOINC-coded, includes abnormal flags, normal ranges, result analysis, ordering info |
| Imaging / diagnostic reports | ⚠️ Partial | `MedicalInfo.xml` → Ultraspimd (49 fields) covers fetal ultrasound only. Other imaging may be in DMS attachments | Ultrasound data is granular but limited to OB. Radiology, X-ray, etc. likely stored as DMS documents rather than structured data |
| Procedures | ✅ Covered | `MedicalInfo.xml` → Operation (19 fields) + Procedure (8) + Flow (10) + Personal (6); `Encounters.xml` → Plan with `cptcode`; `Billing.xml` → Procedure (15 fields) | Covered from multiple angles — surgical operations, encounter-level procedures, billing procedures |
| Clinical notes / documents | ✅ Covered | `Encounters.xml` → Note (12 fields) + Group (9 fields); `Miscellaneous.xml` → Attachment (25 fields), Letter (18 fields); DMS files included as attachments | Notes include text, audio recordings, and graphics. DMS files included in original formats |
| Care plans / goals | ✅ Covered | `HealthScreening.xml` → GoalMonitoring (25 fields) + Progress (25) + ProgressInstructions (6); `MedicalInfo.xml` → Treatment (26 fields) + Objective (14) + Problem (16) + Intervention (14) + Progress (14) + CareTeam (12) | Detailed — both goal monitoring and treatment plans with objectives, interventions, progress tracking, and care teams |
| Orders / referrals | ✅ Covered | `Orders.xml` → Order (23 fields); `Encounters.xml` → Plan/Order elements; `Miscellaneous.xml` → ReferralIn (29 fields) + TransitionOfCare (26 fields) | Covered — orders, referrals in, and transitions of care |
| Insurance / coverage | ✅ Covered | `Patient.xml` → Insurance (61 fields) | Very detailed — carrier, plan, policyholder demographics, copay, deductible, coinsurance, assignment, group number |
| Claims / billing | ⚠️ Partial | `Billing.xml` → Superbill (20 fields) + Procedure (15) + Diagnosis (6+8) + Modifier (5) + Insurance (7) + ReferringPhysician (7) | Superbill-level billing data is present (CPT, modifiers, diagnoses, insurance per transaction). However, the PM module stores deeper financial data — full claims lifecycle, ERA/EOB, payment posting, A/R, patient statements, collections — that is not evidenced in the export |
| Payments | ⚠️ Partial | `Billing.xml` → Superbill has `paymentmethod` attribute | Only a payment method field on superbills. No dedicated payment posting, ERA/EOB, or patient payment records |
| Consents / directives | ✅ Covered | `Miscellaneous.xml` → Directive (13 fields); `Histories.xml` → Consent (14 fields); `Patient.xml` → Consent (21 fields, including CCM consent) | Advance directives, consent history, and CCM consent all present |
| Patient communications / portal messages | ❌ Not covered | No secure messaging or portal communication entities in the schema | Product has Secure Chart patient portal with two-way messaging. Portal message data is absent from the export |
| Specialty: Vision/Ophthalmology | ✅ Covered | `Specialty.xml` → Test (80 fields) + Confrontation (43) + Tonometry (21) | Very detailed — visual acuity, present/recommended prescriptions, confrontation fields, tonometry, color vision |
| Specialty: Hearing/Audiology | ✅ Covered | `Specialty.xml` → Test (15) + Level (8) + Threshold (9) + Report (3) | Audiometric levels, thresholds, reports |
| Specialty: Diabetes | ✅ Covered | `Specialty.xml` → Diabetes (25) + BasicDose (8) + CompDose (7) + PumpBasalRate (6) | Insulin tracking, dose management, pump basal rates |
| Specialty: Pediatric | ✅ Covered | `Specialty.xml` → Pediatric (11 fields) | Developmental assessments (thin — only 11 fields) |
| Specialty: OB/GYN | ✅ Covered | `WomenHealth.xml` → 21 elements, 634 attributes | Extremely comprehensive — prenatal care, deliveries, labor progress, pregnancy history, gynecology, menstrual, family planning |
| Specialty: Geriatric | ✅ Covered | `Specialty.xml` → Geriatric (9) + Questions (9) | Geriatric assessments in questionnaire format |

## 6. Documentation Quality

**What's provided:**
- A complete enumeration of every XML element and every attribute in the export schema
- Clear hierarchical structure showing nesting relationships between elements
- Organized by XML file with logical groupings

**What's missing:**
- **No field-level descriptions**: Not a single attribute out of 2,996 is defined. `billingstatus`, `confidentiality`, `ADPType`, `bdagetype`, `gcnseqno` — all unexplained.
- **No data types**: No indication which fields are dates, integers, strings, booleans, or coded values
- **No value sets**: Coded fields like `maritalstatus`, `encountertype`, `billingstatus`, `severitylevel` lack valid value enumerations
- **No cardinality**: No indication of which elements can repeat or which attributes are required vs. optional
- **No relationships/foreign keys**: While IDs are present (`patientid`, `encounterid`, `transactionid`), the cross-file referential integrity is not documented
- **No sample data**: No example export files showing populated records
- **No machine-readable schema**: No XSD, JSON Schema, or other formal schema definition. The schema is embedded as formatted text in a PDF generated from Word.
- **No import/interpretation guide**: A developer receiving this export would need to reverse-engineer data types, value sets, and the meaning of ambiguous field names

**Developer usability assessment**: A developer could understand the *structure* of the export — which files exist, how elements nest, what attributes are available. But interpreting the *data* would require significant guesswork. Many attribute names are self-descriptive (`firstname`, `dateofbirth`, `icdcode`), but domain-specific fields (`gcnseqno`, `ADPType`, `bdagetype`, `confidentiality`, `completedstatus`, `validationerrorlevel`) would require MicroMD-specific knowledge to interpret correctly. Building a reliable import pipeline from this documentation alone would be difficult.

## 7. Overall Assessment

### Classification

**Partial native export**

The export is genuinely the vendor's native data model (proprietary XML, not FHIR/C-CDA repackaging) and covers an impressively broad range of clinical and specialty data — 150 element types across 2,996 fields, spanning clinical documentation, billing, specialty workflows, and OB/GYN. This is clearly the result of real (b)(10) work, not a compliance checkbox. However, it earns "partial" rather than "comprehensive" for two reasons: (1) documentation lacks field-level descriptions, types, and value sets for all 2,996 fields, and (2) practice management financial data beyond superbill-level billing appears absent, as do patient portal communications.

### Key Findings

1. **Genuine native data model export with exceptional breadth**: The export covers 150 element types and 2,996 attributes across 11 XML files, reflecting MicroMD's internal data model rather than a standard projection. The export spans clinical encounters, billing, specialty workflows, OB/GYN, histories, and more — well beyond what any FHIR or C-CDA export would capture.

2. **Specialty and OB/GYN depth is standout**: WomenHealth.xml alone has 634 attributes across 21 elements, with the OB MedicalHistory element containing 163 attributes tracking 40+ conditions. Vision/ophthalmology testing has 80 attributes per record. This is far more granular than typical EHI exports.

3. **Zero field-level documentation across 2,996 attributes**: Every attribute is listed by name but none have descriptions, data types, value sets, or cardinality indicators. The schema is rendered as prose in a Word-generated PDF rather than as a machine-readable XSD. This significantly limits the usability of the export.

4. **Practice management financial data is thin**: Billing.xml captures superbill-level data (CPT, modifiers, diagnoses, insurance per encounter) but the full PM module's financial lifecycle — claims adjudication, ERA/EOB processing, payment posting, A/R aging, patient statements, collections — is not represented. Given that MicroMD PM is a tightly integrated module, this is a meaningful gap.

5. **Patient portal communications absent**: Despite the Secure Chart patient portal supporting two-way messaging, appointment requests, and intake forms, no portal communication data appears in the export schema.

### Summary Stats

```
Classification:  Partial native export
Export format:   Proprietary XML (ZIP archive, password-protected)
Model type:      Native database model
Entities:        150 element types across 11 XML files
Fields:          2,996 total attributes
Descriptions:    0% (0 of 2,996 fields have descriptions)
Sample data:     No
Bulk export:     No (single-patient only)
Domains covered: 15 of 19 applicable domains (with 2 partial)
```

### Bottom Line

MicroMD's EHI export is one of the more substantive (b)(10) efforts among ambulatory EHRs — it exports the vendor's actual data model with genuine depth in clinical, specialty, and OB/GYN domains. A patient would receive a meaningfully complete clinical record. The two biggest weaknesses are the complete absence of field-level documentation (making interpretation difficult without MicroMD expertise) and the gap in practice management financial data and patient portal communications. Adding an XSD with field annotations and extending the export to cover the PM module's full financial data would elevate this from "partial" to "comprehensive."
