# EHI Export Analysis: CompuGroup Medical US

**Product**: CGM APRIMA  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2700.Apri.19.01.1.221228

## 1. Product Context

CGM APRIMA is a comprehensive ambulatory EHR and practice management system serving 70+ medical specialties, from solo practitioners to multi-physician groups. It is the successor to Aprima Medical Software (originally iMedica, founded 1998), acquired by eMDs in 2019 and then by CompuGroup Medical in 2020.

The product includes:
- **Clinical EHR**: Adaptive learning templates, structured clinical documentation, clinical decision support, e-prescribing (EPCS, ePA, PDMP), lab ordering, immunization tracking, vitals, problem lists, allergies, family/social history, medical history
- **Practice Management / Billing**: Integrated billing, claims management, eMEDIX clearinghouse integration, eligibility verification, ERA posting, superbill management; optional ARIA RCM outsourced revenue cycle
- **Patient Portal**: Bilingual (English/Spanish) portal with messaging, appointment requests, prescription refills, lab results
- **Scheduling**: Integrated appointment scheduling
- **Telehealth**: Virtual visits and remote patient monitoring
- **Quality Reporting**: MIPS/CQM dashboards via CGM MEASURES
- **Public Health Reporting**: Immunization registry, syndromic surveillance, cancer case reporting, eCR
- **FQHC/CHC Features**: Sliding fee scale, encounter-based billing, UDS/UDS+ reporting

For EHI export completeness, the baseline expectation includes: demographics, encounters, clinical notes, problems, medications, allergies, immunizations, vitals, labs, imaging, procedures, family/social history, insurance/coverage, billing/claims/payments, referrals, care plans, and patient portal communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `cgm-aprima-electronic-health-information-export-user-guide.pdf` (328 KB, 28 pages) | Primary (b)(10) EHI export documentation. Contains complete data dictionary for 22 CSV files with field names, SQL data types, and descriptions. Dated 2023-11-02. | **Primary source** — most informative artifact |
| `enrichment/ehi-data-dictionary.json` (64 KB) | Machine-readable JSON extraction of the data dictionary from the PDF. Contains 22 CSV file definitions. Has parsing errors at page boundaries (10 fields dropped, 2 descriptions misaligned). | Useful starting point; required corrections |
| `enrichment/extract-data-dictionary.ts` (11 KB) | Bun TypeScript script used to extract the data dictionary from the PDF | Context on extraction method |
| `fhir-api-documentation-guide.pdf` (498 KB, 76 pages) | Separate (g)(10) FHIR R4 API documentation covering US Core resources. Not the EHI export. | Background context only |
| `certifications-expanded-screenshot.png` (250 KB) | Screenshot of CGM APRIMA certifications section showing EHI export documentation link | Confirms download provenance |
| `ehi-export-link-screenshot.png` (145 KB) | Screenshot of the EHI export link on the vendor's product page | Confirms download provenance |

## 3. Export Mechanics

- **Format**: ZIP file per patient containing CSV files, image folders, a USCDI/C-CDA XML file (with bundled `EEHR_ChartViewer.exe`), and a Complete Patient Chart PDF
- **Mechanism**: In-application batch process: Tools menu → Batch Process Management → EHI Export → Batch Process Summary → View Batch Detail → download ZIP (PDF page 28)
- **Single-patient vs bulk**: Both. Supports individual patient export and "total population of patient records" (PDF page 28)
- **Access constraints**: Requires application access (CGM APRIMA user account). No fees mentioned. No API endpoint — this is a UI-driven export.
- **ZIP naming**: `EHIExtract_LastName FirstName MiddleName_ExtractCreationDateTime.zip`

## 4. Export Content: What's In It

The export contains four components:

1. **22 CSV files** with structured tabular data — the core of the export
2. **Image folders** organized by encounter (e.g., `Radiology/08-16-2023_8_Chest.jpg`)
3. **USCDI XML file** — C-CDA-style clinical summary for EHR portability
4. **Complete Patient Chart PDF** — full chart print covering all visits

### Data Dictionary Summary

After independent verification against the raw PDF text (correcting 10 fields dropped and 2 misaligned descriptions in the enrichment JSON):

- **22 CSV files** (entities)
- **393 total fields** (corrected from enrichment's 383 — see `analysis/build_corrected_inventory.py` for details)
- **391 fields (99.5%) have descriptions**
- **393 fields (100%) have SQL data types** (e.g., `char(255)`, `datetime`, `money`, `bit`, `uniqueidentifier`)
- **2 fields lack descriptions**: `Eligibility.Authorize Assignment` and `Patient Ledger.glDate`
- **No value sets** documented for any coded fields
- **No foreign key relationships** explicitly documented (inferred from shared identifiers like PatientID)
- **No sample export files** provided (one brief CSV example in the PDF only)

### Vendor's own content organization

All 22 CSV files are presented in a flat list in the PDF (no vendor-defined categories). I assigned categories based on content domain. Full field-level details are in `analysis/full-entity-inventory.json`.

| Entity/Table | Fields | Described | Types | Category (assigned) |
|---|---|---|---|---|
| Patient Ledger | 60 | 59 | yes | Billing / Financial |
| Patient Demographics | 40 | 40 | yes | Demographics |
| Eligibility | 27 | 26 | yes | Insurance / Coverage |
| Active Medication | 23 | 23 | yes | Clinical |
| Patient Insurance | 23 | 23 | yes | Insurance / Coverage |
| Responsible Party | 21 | 21 | yes | Demographics |
| Results | 19 | 19 | yes | Clinical |
| Appointment Information | 17 | 17 | yes | Administrative |
| Medical History | 17 | 17 | yes | Clinical |
| Immunization | 15 | 15 | yes | Clinical |
| Problem List | 15 | 15 | yes | Clinical |
| Vitals | 15 | 15 | yes | Clinical |
| Patient Referrals | 15 | 15 | yes | Clinical |
| Contacts | 14 | 14 | yes | Demographics |
| Allergies | 14 | 14 | yes | Clinical |
| Family History | 13 | 13 | yes | Clinical |
| Social History | 13 | 13 | yes | Clinical |
| Employment | 7 | 7 | yes | Demographics |
| Providers | 7 | 7 | yes | Clinical |
| Response Report | 7 | 7 | yes | Clinical Decision Support |
| Audit Trail | 6 | 6 | yes | Administrative |
| Visit Comments | 5 | 5 | yes | Clinical |

### Category Summary

| Category | Entities | Fields |
|---|---|---|
| Clinical | 12 | 171 |
| Demographics | 4 | 82 |
| Billing / Financial | 1 | 60 |
| Insurance / Coverage | 2 | 50 |
| Administrative | 2 | 23 |
| Clinical Decision Support | 1 | 7 |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a broad range of patient data across clinical, demographic, financial, and insurance domains:

**Clinical (12 entities, 171 fields)**: The richest area. Medications (23 fields with NDC, strength, formulation, route, frequency, duration, refills), lab results (19 fields with lab codes, attribute names, values, reference ranges, abnormal flags), problem list (15 fields with ICD-9/10 codes, onset/resolved dates), vitals (15 fields), immunizations (15 fields with CPT, lot numbers, manufacturers), medical/surgical history (17 fields with ICD-9/10 and procedure codes), allergies (14 fields with SNOMED codes), family history (13 fields), social history (13 fields as question/answer pairs), visit comments (5 fields with visit date, section, and comment text), referrals (15 fields), and care team providers (7 fields).

**Demographics (4 entities, 82 fields)**: Very thorough. Demographics (40 fields including 4 phone numbers with types, 2 emails, language, race, ethnicity, marital status, AKA names, SSN, death date, PCP), contacts (14 fields for emergency contacts, POA, HIPAA release), responsible party (21 fields), and employment (7 fields).

**Billing / Financial (1 entity, 60 fields)**: Genuinely deep. The Patient Ledger is the largest entity at 60 fields, covering superbill data (ID, status, procedure codes, 4 diagnosis codes), amounts (billed, due, paid, adjusted — broken out by insurance vs. patient), payment tracking (last patient/insurance payment dates and amounts), void status, financial center, service site, and responsible party information.

**Insurance / Coverage (2 entities, 50 fields)**: Patient Insurance (23 fields with primary and secondary insurance names, member IDs, group IDs) plus Eligibility (27 fields with deductibles, copays, coinsurance amounts for in-network and out-of-network, eligibility status, and request timestamps).

**Administrative (2 entities, 23 fields)**: Appointments (17 fields with type, status, location, reason, provider) and audit trail (6 fields tracking record changes).

**Clinical Decision Support (1 entity, 7 fields)**: Response Report captures HM rule alerts and provider decisions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (40 fields), `Contacts` (14 fields), `Responsible Party` (21 fields), `Employment` (7 fields) | Thorough — name variants, 4 phone numbers, language, race/ethnicity, SSN, death date |
| Encounters / visits | ⚠️ Partial | No dedicated Encounters CSV. Visit data implicit in `Appointment Information` (17 fields), `Visit Comments` (5 fields with VisitId), and `Patient Ledger` (serviceDate). Complete Patient Chart PDF covers all visits. | No structured encounter entity with visit-level diagnoses, providers, and dispositions. Encounter data is scattered across other files. |
| Problems / conditions / diagnoses | ✅ Covered | `Problem List` (15 fields) with ICD-9/10 codes, onset/resolved dates, notes | Solid |
| Medications / prescriptions | ✅ Covered | `Active Medication` (23 fields) with NDC, strength, formulation, route, frequency, duration, refills | Good for active meds. Discontinued meds via InactiveDate field. No separate prescription transmission records (e-Rx confirmations, ePA). |
| Allergies | ✅ Covered | `Allergies` (14 fields) with SNOMED codes | Solid |
| Immunizations | ✅ Covered | `Immunization` (15 fields) with CPT codes, lot numbers, manufacturers, dosages | Solid |
| Vitals | ✅ Covered | `Vitals` (15 fields) with name/value/unit/position | Solid |
| Lab results | ✅ Covered | `Results` (19 fields) with lab codes, attribute names, values, reference ranges, abnormal flags, units, collection/result dates | Solid |
| Imaging / diagnostic reports | ⚠️ Partial | Clinical images exported in encounter-organized folders. No structured radiology/imaging report CSV. | Images present but no structured report data (impressions, findings) |
| Procedures | ✅ Covered | `Medical History` (17 fields) with procedure codes, ICD-9/10 codes, and `Patient Ledger` procedure codes/descriptions | Procedures covered in both clinical and billing contexts |
| Clinical notes / documents | ✅ Covered | `Visit Comments` (5 fields) structured by visit and section, plus Complete Patient Chart PDF with all visit charts | Notes captured two ways: structured CSV and comprehensive PDF |
| Care plans / goals | ❌ Not covered | No care plan or goal CSV. May be embedded in Visit Comments or Complete Patient Chart PDF but not structured. | Product likely stores care plans (certified for (a)(12) care plan). Structured care plan data absent from export. |
| Orders / referrals | ⚠️ Partial | `Patient Referrals` (15 fields) with procedure codes, dates, status. No separate lab/imaging order entity — only `Results` for completed labs. | Pending/unfulfilled orders not captured |
| Insurance / coverage | ✅ Covered | `Patient Insurance` (23 fields) with primary/secondary carrier, member/group IDs. `Eligibility` (27 fields) with deductibles, copays, coinsurance. | Thorough |
| Claims / billing | ✅ Covered | `Patient Ledger` (60 fields) with superbill data, procedure/diagnosis codes, amounts billed/due/paid/adjusted, insurance vs. patient breakdown | Genuinely deep billing data |
| Payments | ✅ Covered | Embedded in `Patient Ledger`: PaymentAmount, AMTPAID, lastPatientPaymentAmount, lastInsurancePaymentAmount, PatientPayment, InsurancePayment, TotalPayment, PayerCredits | Thorough |
| Consents / directives | ⚠️ Partial | `Contacts` includes HIPAA Release and Power of Attorney flags. No dedicated advance directive or consent entity. | Basic consent indicators present but no structured advance directive content |
| Patient communications / portal messages | ❌ Not covered | No secure messaging or portal communication CSV | Product has patient portal with messaging (per product-research.md). Significant gap. |
| Specialty-specific data | ⚠️ Partial | The product supports 70+ specialties with adaptive templates. Export uses generic structures (Visit Comments, Problem List, Medical History) rather than specialty-specific entities. | Specialty template data may be captured in Visit Comments or Complete Patient Chart PDF but not in structured, queryable form. |

## 6. Documentation Quality

**Strengths:**
- Complete data dictionary covering all 22 CSV files with field names, SQL data types, and descriptions (99.5% of fields described)
- SQL data types are specific and useful (e.g., `char(255)`, `money`, `uniqueidentifier`, `bigint`, `smallint`, `bit`)
- Well-organized 28-page PDF with table of contents
- Clear export mechanism documentation (albeit brief — 3 steps on page 28)
- ZIP structure documentation including image naming conventions

**Weaknesses:**
- **No value sets**: Coded fields like Gender Code, Race Code, Ethnicity Code, Appointment Type Code, Appointment Status Code have data types but no enumeration of valid values
- **No relationship documentation**: No foreign key documentation. Relationships must be inferred from shared identifiers (PatientID, VisitId, SuperbillID, AccountID, DepositUid, ResponsiblePartyUid)
- **No sample export**: Only one brief CSV snippet showing 2 medication records. No complete sample ZIP
- **No machine-readable schema**: The data dictionary is only in the PDF. The enrichment JSON was created by an automated agent, not provided by the vendor
- **2 undescribed fields**: `Authorize Assignment` (Eligibility) and `glDate` (Patient Ledger) have no descriptions in the PDF

**Developer usability**: A developer could build a reasonable import from this documentation. Field names are mostly self-documenting, types are specific enough for schema creation, and descriptions clarify ambiguous names. The main impediment would be reconstructing relationships between entities (e.g., linking Visit Comments to Patient Ledger entries) and interpreting coded values without value sets.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

### Key Findings

1. **Genuine (b)(10) effort**: This is a purpose-built EHI export, not a repackaged FHIR API or C-CDA. The dedicated batch process, CSV format mapped to internal database columns, and inclusion of billing data (60-field Patient Ledger) clearly distinguish it from the separate (g)(10) FHIR API documented in `fhir-api-documentation-guide.pdf`.

2. **Strong billing coverage**: The Patient Ledger (60 fields) is the largest entity and provides detailed financial data — superbills, 4 diagnosis codes per line item, amounts billed/due/paid/adjusted broken out by insurance vs. patient, payment tracking, void status, and responsible party. Combined with Eligibility (27 fields with deductible/copay/coinsurance data), this goes well beyond typical clinical summary exports.

3. **Near-complete field documentation**: 391 of 393 fields (99.5%) have descriptions, and all 393 have SQL data types. This is above average for EHI export documentation, though it lacks value sets and relationship documentation.

4. **Moderate coverage gaps**: Care plans (no structured entity despite (a)(12) certification), patient portal messages (no secure messaging CSV despite portal features), and encounters (no dedicated encounter entity — visit data scattered across Appointment Information, Visit Comments, and Patient Ledger) are the notable gaps.

5. **Multi-format failsafe**: The inclusion of a Complete Patient Chart PDF alongside structured CSVs means even data not captured in the CSV schema (e.g., specialty template content, care plans documented in notes) has some representation in the export, though not in structured/queryable form.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV + PDF + USCDI XML + images (in ZIP)
Model type:      Native database projection (CSV with SQL column types)
Entities:        22 CSV files
Fields:          393 (corrected from enrichment's 383)
Descriptions:    99.5% (391/393 fields)
Sample data:     No (one brief excerpt only)
Bulk export:     Yes (individual or total population)
Domains covered: 13 of 17 applicable domains (✅ or ⚠️)
```

### Bottom Line

CGM APRIMA delivers a solid, purpose-built EHI export that covers the core designated record set well — demographics, clinical data, billing, insurance, and most ancillary domains are represented with field-level documentation. The most significant gaps are the absence of structured care plan data and patient portal messages, and the lack of a dedicated encounter entity. A patient or provider would get a substantially complete copy of their clinical and financial data, with the Complete Patient Chart PDF serving as a catch-all for anything not captured in the 22 structured CSVs.
