# EHI Export Analysis: MicroMD, LLC

**Product**: MicroMD EMR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2753.Micr.20.07.1.230427

## 1. Product Context

MicroMD EMR is an ambulatory electronic medical records system developed by MicroMD, LLC (a subsidiary of Henry Schein Medical Systems). It targets small-to-medium independent practices, community health centers (CHCs/FQHCs), and multi-specialty groups across eight named specialties: Cardiology, Dermatology, ENT, Gastroenterology, OB-GYN, Pediatrics, Primary Care, and Urology.

The certified EMR module is part of a broader ecosystem that includes:
- **Practice Management (PM)** — scheduling, registration, claims/billing, payment posting, accounts receivable
- **Document Management System (DMS)** — scanned documents, e-faxes, pathology results, correspondence
- **Secure Chart patient portal** — secure messaging, appointment requests, intake forms, lab results
- **e-Prescribing** — two-way Surescripts integration including EPCS

Key clinical capabilities include: SOAP-based encounter documentation with customizable templates, problem lists (ICD-10), medication management, lab integration (LabCorp, Quest), medical device integration (ECGs, spirometry), immunization tracking, health maintenance alerts, clinical decision support, clinical quality measures/MIPS reporting, telehealth (Medpod), and specialty-specific workflows.

The PM module handles billing, claims management, EDI processing, payment posting, eligibility verification, sliding fee schedules (FQHC), and accounts receivable reporting. Under (b)(10), the export should cover "all electronic health information that can be stored at the time of certification by the product, of which the Health IT Module is a part" — which encompasses the full product ecosystem, not just the certified EMR module.

## 2. Artifacts Reviewed

| Artifact | Description | Usefulness |
|---|---|---|
| `MicroMD-EMR-170.315b10-Electronic-Health-Information-export-EHI.pdf` (326 KB, 17 pages) | The sole substantive artifact. Defines the XML schema for the EHI export across 11 XML files plus DMS attachments. Lists every XML element and attribute but provides no field-level descriptions, data types, or value sets. Dated February 6, 2026. | **Primary source** — this is the complete (b)(10) documentation |
| `screenshot-certification-page.png` (293 KB) | Screenshot of the MicroMD certification page showing the link to the EHI export PDF. | Confirms provenance only |

Only two artifacts were collected. The PDF is the entire (b)(10) documentation — there is no separate data dictionary, no sample data files, no machine-readable schema (XSD), and no supplementary documentation.

## 3. Export Mechanics

- **Format**: Custom XML files, packaged in a compressed (ZIP) file
- **Naming convention**: Practice ID and patient chart ID (`####.######.0`)
- **Password protection**: Patient date of birth (`mmddyyyy`)
- **Mechanism**: UI-driven ("see user manual for instruction") — appears to be a per-patient export triggered within the EMR
- **Single-patient vs bulk**: Documentation describes single-patient export (compressed file per patient). No mention of bulk/practice-wide export.
- **Access constraints**: No mention of fees or special access requirements
- **Additional files**: DMS attachments (pdf, doc, rtf, ccd, xml, images, etc.) are included alongside the XML files

The export produces 11 XML files per patient plus any DMS-stored documents:
1. Billing.xml
2. Encounters.xml
3. HealthScreening.xml
4. Histories.xml
5. MedicalInfo.xml
6. Miscellaneous.xml
7. Orders.xml
8. Patient.xml
9. Schedule.xml
10. Specialty.xml
11. WomenHealth.xml

## 4. Export Content: What's In It

The PDF documents an XML schema consisting of **151 entities (XML elements with attributes) across 11 XML files, containing 3,029 total fields (XML attributes)**. Additionally, DMS attachments are included as separate files.

**Documentation quality per field**: Zero fields have descriptions (0%), zero fields have explicit data types (0%), zero fields have value sets or coded value references. The documentation is purely structural — element names and attribute names only. Attribute names are descriptive enough to infer meaning in most cases (e.g., `firstname`, `dateofbirth`, `icdcode`) but there is no formal specification.

### Vendor's own content organization

The vendor organizes the export into 11 XML files. Below is a summary by file, with representative entities:

| XML File | Entities | Fields | Category |
|---|---|---|---|
| Billing.xml | 7 | 68 | Billing & Insurance |
| Encounters.xml | 21 | 318 | Clinical - Encounters |
| HealthScreening.xml | 22 | 374 | Clinical - Screening & Prevention |
| Histories.xml | 13 | 336 | Clinical - Histories |
| MedicalInfo.xml | 29 | 521 | Clinical - Medical Information |
| Miscellaneous.xml | 7 | 141 | Documents & Communications |
| Orders.xml | 1 | 23 | Clinical - Orders |
| Patient.xml | 10 | 312 | Demographics & Insurance |
| Schedule.xml | 1 | 15 | Scheduling |
| Specialty.xml | 18 | 287 | Specialty Clinical Data |
| WomenHealth.xml | 21 | 634 | Women's Health / OB-GYN |
| DMS (attachments) | 1 | 0 | Documents |
| **TOTAL** | **151** | **3,029** | |

**Largest entities** (by field count):
- `WomenHealth.xml/MedicalHistory` — 163 fields (OB medical history with ~30 condition categories, each with status/comment/detail/SNOMED code)
- `Specialty.xml/Test` (Vision) — 80 fields (ophthalmic measurements)
- `Patient.xml/Demographic` — 69 fields
- `MedicalInfo.xml/Medication` — 61 fields
- `Patient.xml/Insurance` — 61 fields
- `HealthScreening.xml/Detail` (Immunization details) — 54 fields
- `MedicalInfo.xml/Ultraspimd` (Fetal ultrasound) — 49 fields
- `MedicalInfo.xml/Vital` — 45 fields

**Billing.xml** includes: Superbill (18 fields: billing source, CPT code, status, payment method, dates, etc.), Diagnosis (assessment codes, SNOMED, ICD), Procedure (amounts, modifiers, service dates, performed by), Modifier, ReferringPhysician, and Insurance linkage. This represents superbill-level billing data with procedure-level detail.

**Encounters.xml** is the clinical encounter record with: encounter metadata (42 fields including dates, status, type, provider, recording method), Reasons, Assessments (with detail descriptors), Subjectives/Objectives (SOAP note components with descriptors), ReviewProblems, Medications (administered medications with full sig detail), Plans (orders, referrals, vaccines, instructions), FaceTime tracking, Notes (encounter notes with text), and Groups.

**Patient.xml** covers demographics (69 fields: name, address, DOB, gender identity, sexual orientation, race, ethnicity, language, employment, income, religion, marital status, immigration date, confidentiality settings), addresses (current/alternate), family members, emergency contacts, insurance policies (61 fields with full policyholder details, plan information, co-pay/deductible), providers (practice and referring), and consent records.

**MedicalInfo.xml** contains: allergies (33 fields), problems/conditions (including a Cancer sub-entity with staging data — 22 fields), vitals (45 fields including pregnancy-related vitals), medications (61 fields), test results (lab results with LOINC codes, abnormal flags), behavioral health questionnaires, clinical decision support alerts, fetal ultrasound measurements, operations (surgical records with procedures, diagnoses, medications, flow, personnel), and treatment/care plans (with objectives, problems, medications, interventions, progress notes, care team).

**HealthScreening.xml** includes: goal monitoring with progress tracking, health concerns with care teams, structured health screenings (questionnaire-based with questions/answers/sections/results/follow-up), immunizations (with detailed administration records including VIS tracking, lot numbers, NDC codes), risk assessments, and prevention programs.

**Histories.xml** covers: family history, medical history, social history, surgical history, birth history, sexual history, asthma history (48 fields — a specialty-specific deep record), habits, hospitalization records (with procedures, diagnoses, and reports), and consent history.

**Specialty.xml** has deep specialty-specific content: Vision (ophthalmic tests with 80 fields, confrontation fields, tonometry), Hearing (tests, levels, thresholds, reports), Diabetes (insulin management with basal rates, doses, targets), Pediatric development, Genetic screening, Geriatric assessments, and Allergy testing (skin test/allergen data).

**WomenHealth.xml** is the largest file (634 fields) with: obstetric care records, initial exams, comprehensive OB medical history (163 fields), genetics, deliveries (with events, fetus records, problems), prenatal visits, estimated delivery dates, progress of labor (Bishop score, contractions, vitals), pregnancy history (with fetus details), gynecology, menstrual history, and family planning.

**Miscellaneous.xml** includes: attachments (with metadata including LOINC, category, format), letters/correspondence, advance directives, patient education, referrals-in (with authorization tracking), and transitions of care.

The full entity inventory is available at `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized across 11 XML files that map naturally to the product's functional areas:

**Deepest coverage areas:**
- **Women's Health/OB-GYN** (634 fields): Exceptionally deep. The OB medical history entity alone has 163 fields covering ~30 medical conditions with status, comments, details, and SNOMED codes. Prenatal visits, deliveries, labor progress, fetal ultrasounds, menstrual history, and family planning are all comprehensively represented.
- **Medical Information** (521 fields): Strong clinical depth with allergies, problems (including cancer staging), vitals, medications with full sig detail, lab results, behavioral health assessments, surgical operations, and care plans.
- **Health Screening & Prevention** (374 fields): Good coverage of health maintenance, immunizations (with VIS tracking), goal monitoring, health concerns, and structured questionnaires.
- **Histories** (336 fields): Comprehensive patient history including family, medical, social, surgical, birth, sexual, asthma, hospitalizations, and consent history.
- **Encounters** (318 fields): Full SOAP encounter documentation with assessments, orders, medications, notes.
- **Demographics & Insurance** (312 fields): Thorough patient demographics (69 fields) and insurance (61 fields per policy).

**Thinnest coverage areas:**
- **Billing** (68 fields): Present but limited to superbill-level data. Contains CPT codes, diagnoses, procedures, modifiers, and insurance linkage — but this is the clinical-facing side of billing (charges generated from encounters). There is no evidence of full revenue cycle data: no claims submission records, no payment posting/remittance, no accounts receivable, no patient statements, no collections data.
- **Orders** (23 fields): A single entity with basic order metadata. Thin relative to what an EMR typically stores for order management.
- **Schedule** (15 fields): Single appointment entity with basic booking information.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient.xml/Demographic` (69 fields), `Addresses` (current/alternate), `Contact`, `FamilyMember` | Thorough — includes gender identity, sexual orientation, race, ethnicity, language, income |
| Encounters / visits | ✅ Covered | `Encounters.xml` (21 entities, 318 fields) — full SOAP encounter with assessments, subjectives, objectives, plans, notes | Deep coverage of clinical encounter content |
| Problems / conditions | ✅ Covered | `MedicalInfo.xml/Problem` + `Cancer` (staging data); encounter-level assessments | Includes cancer staging — exceeds typical depth |
| Medications / prescriptions | ✅ Covered | `MedicalInfo.xml/Medication` (61 fields), `Encounters.xml/Medication` (administered), sig detail | Comprehensive — covers both ongoing and encounter-administered |
| Allergies | ✅ Covered | `MedicalInfo.xml/Allergies` (33 fields) + `Specialty.xml/Allergy` (allergen testing) | Includes allergy testing data (skin tests) — specialty depth |
| Immunizations | ✅ Covered | `HealthScreening.xml/Immunization` + `Detail` (54 fields) + `Info` + `Vis` | Deep — includes VIS tracking, lot numbers, NDC, refusal reasons |
| Vitals | ✅ Covered | `MedicalInfo.xml/Vital` (45 fields) — BP, pulse, temp, O2, BMI, pain, head circumference, peak flow, blood sugar, pregnancy-related vitals | Comprehensive |
| Lab results | ✅ Covered | `MedicalInfo.xml/TestResults` with LOINC codes, abnormal flags, result values | Present; single entity (could be richer if structured) |
| Imaging / diagnostic reports | ⚠️ Partial | `Histories.xml/Report` (hospital reports), `MedicalInfo.xml/Ultraspimd` (fetal US); DMS attachments may contain imaging reports | No dedicated radiology/imaging entity; fetal US is specialty-specific |
| Procedures | ✅ Covered | `Encounters.xml/Plan` (procedures/orders), `MedicalInfo.xml/Operation` (surgical records with flow, personnel), `Histories.xml/Procedure` | Surgical operations are deeply covered |
| Clinical notes / documents | ✅ Covered | `Encounters.xml/Note` + `Group` (encounter notes), `Miscellaneous.xml/Letter`, DMS attachments | Notes stored as text; DMS provides supplemental documents |
| Care plans / goals | ✅ Covered | `MedicalInfo.xml/Treatment` (care plans with objectives, problems, interventions, progress, care team), `HealthScreening.xml/GoalMonitoring` | Well-structured care plan model |
| Orders / referrals | ✅ Covered | `Orders.xml/Order` (23 fields), `Miscellaneous.xml/ReferralIn`, `Encounters.xml/Plan` (orders) | Orders entity is thin (1 entity) but referrals and encounter-level plans supplement |
| Insurance / coverage | ✅ Covered | `Patient.xml/Insurance` (61 fields), `Billing.xml/Insurance` | Detailed — includes policyholder demographics, plan details, co-pay/deductible |
| Claims / billing | ⚠️ Partial | `Billing.xml/Superbill` + `Procedure` + `Diagnosis` + `Modifier` (68 fields total) | Superbill/charge data only. Product has full PM module with claims, payments, A/R — those are absent |
| Payments | ❌ Not covered | No payment entities | Product PM module handles payment posting, remittance, patient payments — significant gap |
| Consents / directives | ✅ Covered | `Miscellaneous.xml/Directive`, `Histories.xml/Consent`, `Patient.xml/Consent` | Multiple consent types tracked |
| Patient communications | ❌ Not covered | No portal messages or communication logs | Product has Secure Chart portal with two-way messaging — gap |
| Specialty: OB-GYN | ✅ Covered | `WomenHealth.xml` (21 entities, 634 fields) — obstetric care, prenatal, delivery, labor, gynecology, menstrual, family planning | Exceptionally deep specialty coverage |
| Specialty: Vision/ENT | ✅ Covered | `Specialty.xml/Vision` (80 fields), `Hearing` tests/levels/thresholds | Deep specialty-specific clinical data |
| Specialty: Diabetes | ✅ Covered | `Specialty.xml/Diabetes` with insulin management, pump basal rates | Specialty-specific management data |
| Specialty: Pediatrics | ⚠️ Partial | `Specialty.xml/Pediatric` — single entity with minimal fields | Thin for a named specialty |
| Specialty: Geriatrics | ✅ Covered | `Specialty.xml/Geriatric` with assessment questions | Present |
| Specialty: Genetics | ✅ Covered | `Specialty.xml/Genetic`, `WomenHealth.xml/Genetics` | Screening results with family linkage |

**Gap Summary**:
- **Payments/Revenue cycle**: Product has a PM module with payment posting, remittance, A/R, patient statements, collections — none of this appears in the export beyond superbill charges.
- **Patient portal communications**: Product has Secure Chart with two-way messaging — no portal message export.
- **Claims submission/tracking**: PM module handles EDI claims processing — not in export.

## 6. Documentation Quality

The documentation is a **17-page PDF that lists the XML element and attribute structure** for each of the 11 export files. It serves as a structural schema reference.

**Strengths:**
- Covers 151 entities with 3,029 fields — this is not a stub
- XML hierarchy is clear (parent-child relationships visible)
- Attribute names are generally self-documenting (e.g., `firstname`, `icdcode`, `dateperformed`)

**Weaknesses:**
- **No field descriptions**: Zero of 3,029 attributes have explanatory descriptions
- **No data types**: No indication of whether a field is string, date, integer, boolean, or coded
- **No value sets**: No enumeration of valid values for coded fields (e.g., what are valid values for `billingstatus`, `encountertype`, `allergyseverity`?)
- **No relationships documented**: Foreign key relationships exist (e.g., `encounterid`, `patientid`, `transactionid`) but are not formally described
- **No sample data**: No example XML files showing populated data
- **No machine-readable schema**: No XSD or JSON Schema — only the PDF
- **No size/length constraints**: No max length, nullability, or cardinality information

**Could a developer build an import?** With significant effort and guesswork. The structural schema provides enough to parse the XML, but interpreting coded fields, understanding relationships between files, and handling edge cases would require reverse-engineering from actual export data. The documentation is necessary but not sufficient.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data domains with impressive depth — especially OB-GYN (634 fields), clinical encounters, medications, histories, specialty clinical data (vision, hearing, diabetes), and health screening. It also includes superbill-level billing data (charges, CPT codes, diagnoses), insurance information, and DMS attachments. This goes well beyond USCDI/C-CDA clinical summaries.

However, MicroMD's product ecosystem includes a Practice Management module with full revenue cycle capabilities (claims management, EDI processing, payment posting, remittance, patient statements, collections, accounts receivable) and a patient portal (Secure Chart) with two-way messaging. The export captures the clinical-facing side of billing (superbills) but not the downstream revenue cycle data, and omits portal communications entirely. These are meaningful gaps given the product's capabilities.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged C-CDA or FHIR export. Evidence:
- Uses MicroMD's native data model (proprietary XML schema mapping to internal tables)
- 151 entities and 3,029 fields far exceed what any standard clinical exchange format would contain
- Includes domains entirely outside USCDI: billing superbills, surgical operations with flow/personnel, asthma history (48 fields), fetal ultrasound measurements, allergy skin testing, diabetes pump management, OB medical history (163 fields), labor progress, hearing tests
- The schema clearly reflects the product's internal data structures
- DMS attachments are included alongside structured data
- No reference to C-CDA, FHIR, or USCDI in the documentation

### Key Findings

1. **Genuine purpose-built export with deep clinical coverage**: 151 entities, 3,029 fields across 11 XML files represent MicroMD's native data model. The specialty-specific depth (OB-GYN at 634 fields, vision at 80+ fields, diabetes management, asthma tracking) demonstrates real engagement with (b)(10) requirements.

2. **Revenue cycle data is limited to superbills**: Despite MicroMD's PM module handling full claims lifecycle, payments, and A/R, the export only includes superbill-level charge data (68 fields). Downstream billing — claims, remittance, payments, statements, collections — is absent.

3. **Zero field-level documentation**: None of the 3,029 attributes have descriptions, data types, value sets, or relationship documentation. The schema is structurally complete but semantically opaque. No sample data or machine-readable schema (XSD) is provided.

4. **Patient portal communications are missing**: The Secure Chart portal supports two-way messaging, appointment requests, and intake forms — none of which appear in the export.

5. **Single-patient export only**: The export appears limited to individual patient exports (one ZIP file per patient). No bulk/practice-wide export mechanism is documented.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   XML (compressed ZIP, password-protected)
    Entities:        151
    Fields:          3,029
    Descriptions:    0%
    Sample data:     No
    Bulk export:     No (single-patient)
    Domains covered: 16 of 20 applicable domains

### Bottom Line

MicroMD built a genuine purpose-built EHI export that covers clinical data with impressive specialty-specific depth — particularly OB-GYN, vision, hearing, diabetes, and asthma tracking — far exceeding what a repackaged C-CDA or FHIR export would provide. The most significant gaps are the absence of downstream revenue cycle data (payments, claims, A/R) despite the product's PM module capabilities, missing patient portal communications, and the complete lack of field-level documentation (no descriptions, types, or value sets for any of the 3,029 fields).
