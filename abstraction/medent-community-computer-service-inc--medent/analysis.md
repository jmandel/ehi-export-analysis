# EHI Export Analysis: MEDENT (Community Computer Service, Inc.)

**Product**: MEDENT v23.7
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.1840.MEDE.23.02.1.230918 (CHPL #11347)

## 1. Product Context

MEDENT is an integrated ambulatory EHR, practice management, and patient engagement platform developed by Community Computer Service, Inc. of Auburn, NY. It serves 11,000+ providers across 37 states, primarily in independent practices, multi-specialty groups, and FQHCs. The product covers 30+ specialties.

**Key data domains relevant to EHI completeness:**
- **Clinical charting**: Problem lists, diagnoses, medications, allergies, vitals, immunizations, lab results, orders, procedures, clinical notes, care plans/goals, screenings/assessments
- **Practice management & billing**: Scheduling, CPT/HCPCS coding, fee schedules, claims submission, ERA processing, A/R management, patient payments
- **Specialty modules**: Ophthalmology/optometry (eye/contact prescriptions), OB/GYN (prenatal episodes, delivery outcomes), surgical booking
- **Patient engagement**: Patient portal with messaging, document access, online payments, telehealth/e-visits
- **Interoperability**: C-CDA exchange, FHIR API (g)(10), Direct messaging, Carequality/CommonWell connections
- **Referral management**: Referral tracking with comprehensive date/status workflows
- **Document management**: Scanned documents, faxes, imaging

This breadth means a genuine (b)(10) export should cover clinical, billing/financial, specialty, insurance, and document data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi_pdfs/EHI_Setup_and_File_Format_Specification.pdf` (3 pages) | Master document describing export architecture, filters, format options | **High** — explains export mechanics, UI navigation, data feed selection |
| `downloads/ehi_pdfs/Patient_File_Specification.pdf` | Demographics: 80 fields including SDOH, gender identity, pronouns, birth info | **High** — most detailed entity spec |
| `downloads/ehi_pdfs/Medication_File_Specification.pdf` | Medications: 43 fields with NDC, RxNorm, SIG, refills, administration | **High** |
| `downloads/ehi_pdfs/Result_File_Specification.pdf` | Lab results: 39 fields with LOINC, reference ranges, flags | **High** |
| `downloads/ehi_pdfs/EyeContactScriptFileSpec.pdf` | Ophthalmology prescriptions: 56 fields (keratometry, sphere, cylinder, axis, prism) | **High** — specialty data beyond USCDI |
| `downloads/ehi_pdfs/Screening_and_Assessment_Specification.pdf` | Screenings/assessments: 43 fields (tobacco, SDOH, risk, health maintenance) | **High** |
| `downloads/ehi_pdfs/Order_File_Specification.pdf` | Orders: 31 fields (lab, DI, general) | **High** |
| `downloads/ehi_pdfs/Procedures_File_Specification.pdf` | Procedures: 30 fields with CPT, SNOMED, body site, outcome, complications | **High** |
| `downloads/ehi_pdfs/Immunization_File_Specification.pdf` | Immunizations: 29 fields with CVX, lot, manufacturer, VIS | **Medium** |
| `downloads/ehi_pdfs/Referral_File_Specification.pdf` | Referrals: 26 fields with comprehensive tracking | **Medium** |
| `downloads/ehi_pdfs/Allergy_File_Specification.pdf` | Allergies: 21 fields with SNOMED, reactions, severity | **Medium** |
| `downloads/ehi_pdfs/HIPAAFileSpecification.pdf` | HIPAA consent/communication preferences: 21 fields | **Medium** |
| `downloads/ehi_pdfs/GoalsFileSpecification.pdf` | Patient goals: 19 fields | **Medium** |
| `downloads/ehi_pdfs/Progress_Note_Listing_File_Specification.pdf` | Note metadata: 13 fields | **Medium** |
| `downloads/ehi_pdfs/Financial_File_Specification.pdf` | Financial header (4 fields) + reference to ASCII Field List | **Medium** — thin on its own but critical pointer |
| `downloads/ehi_pdfs/OBEpisode_File_Specification.pdf` | OB episodes: 12 fields (EDD, gestational age, risk) | **Medium** — specialty data |
| `downloads/ehi_pdfs/OBOutcome_File_Specification.pdf` | Delivery outcomes: 11 fields | **Medium** |
| 15 additional PDF specs | Encounter, Diagnosis, Document Listing, Vital, Provider, Location, PatientPlan, InsurancePlan, CareTeam, SocialHistory, MedicalHistory, SurgicalHistory, Exchanged Files, Appointment, ProblemList | **Medium** |
| `downloads/asciifieldlistinter.html` (370 KB) | HTML manual page: 750 configurable financial/billing export fields across 17 data areas | **High** — demonstrates deep billing coverage |
| `downloads/screenshots/onc-page-ehi-section.png` | Screenshot showing all 33 PDF links on ONC page | **Low** — confirms availability |
| `downloads/screenshots/ascii-field-list-full.png` | Full-page screenshot of ASCII Field List | **Low** — visual confirmation |
| `downloads/enrichment/ehi-specs.json` | Pre-extracted field data from all PDFs (648 fields) | **High** — used for validation |
| `downloads/enrichment/ascii-field-list.json` | Pre-extracted ASCII field list (750 fields) | **High** — structured data source |

**Total**: 33 PDF specifications + 1 HTML field list page + 2 screenshots + 4 enrichment artifacts.

## 3. Export Mechanics

- **Format**: Delimited text files (CSV or pipe-delimited, with or without quotes — configurable). Documents, triages, and todos exported as HL7 C-CDA 2.1 Unstructured Documents containing Base64-encoded PDFs, zipped together.
- **Mechanism**: UI-driven via **Medical Records > Data Export/Import/Connection Table > Electronic Health Information Export**. Four operational areas: Setup (configure filters/feeds), Create (generate data), Send (transmit/download), Control File (format settings).
- **Single-patient vs bulk**: Supports both. Patient population can be filtered by provider, location, PCP, age, insurance, race, ethnicity, sex, status, or narrowed to specific patients. Can also be scoped by date range (appointment or e-superbill based).
- **Scheduling**: Supports autorun for overnight batch processing.
- **Output**: ZIP file containing per-entity delimited text files + zipped C-CDA document bundles.
- **Access constraints**: Requires MEDENT security clearance for "Data Export/Import/Connection Table" and "Electronic Health Information Export."
- **Fees**: Not mentioned in documentation.

## 4. Export Content: What's In It

### Data Dictionary Overview

The export is documented through **33 PDF specifications** covering 31 data entities (plus 2 metadata/setup documents), totaling **648 structured data fields** across the EHI specs. Additionally, the **ASCII Field List** provides **750 configurable financial/billing fields** across 17 data areas, for a combined total of approximately **1,398 documented fields**.

- **648 EHI spec fields**: 627 (96.8%) have descriptions with example output
- **750 ASCII financial fields**: All have descriptive names; 178 have additional notes
- **Types**: Not formally declared (no "string"/"date"/"integer" designations), but inferrable from examples
- **Relationships**: Cross-entity via shared identifiers (`patient_mrn`, `MEDENT_id`, `encounter_id`, `provider_id`, `location_id`, `plan_id`)
- **Value sets**: Some documented inline (e.g., verification_status values) but not comprehensively enumerated
- **Machine-readable schema**: None (PDF-only documentation)

### Vendor's own content organization

| Entity/Table | Fields | Category |
|---|---|---|
| Patient | 80 | Demographics |
| EyeContactScript | 56 | Specialty - Ophthalmology |
| Medication | 43 | Clinical - Medications |
| Screening_and_Assessment | 43 | Clinical - Screenings/Assessments |
| Result | 39 | Clinical - Lab Results |
| Order | 31 | Clinical - Orders |
| Procedures | 30 | Clinical - Procedures |
| Immunization | 29 | Clinical - Immunizations |
| Referral | 26 | Clinical - Referrals |
| Allergy | 21 | Clinical - Allergies |
| HIPAA | 21 | Consent / HIPAA |
| Goals | 19 | Clinical - Goals |
| Provider | 18 | Reference - Providers |
| Vital | 15 | Clinical - Vitals |
| Appointment | 15 | Scheduling |
| ProblemList | 14 | Clinical - Problems |
| Encounter | 14 | Clinical - Encounters |
| Diagnosis | 13 | Clinical - Diagnoses |
| Progress_Note_Listing | 13 | Clinical - Notes |
| Exchanged_Patient_Level_Files | 13 | Data Exchange |
| Document_Listing | 12 | Clinical - Documents |
| OBEpisode | 12 | Specialty - OB/GYN |
| OBOutcome | 11 | Specialty - OB/GYN |
| MedicalHistory | 9 | Clinical - Medical History |
| SocialHistory | 9 | Clinical - Social History |
| SurgicalHistory | 9 | Clinical - Surgical History |
| PatientPlan | 9 | Insurance |
| Location | 9 | Reference - Locations |
| CareTeam_and_Resources | 8 | Clinical - Care Team |
| InsurancePlan | 6 | Insurance |
| Financial (header) | 1 | Billing / Financial |
| **Financial_ASCII_FieldList** | **750** | **Billing / Financial** |

The ASCII Field List (750 fields) is organized into 17 data areas:

| Area | Code | Fields | Description |
|---|---|---|---|
| Patient | P | 260 | Patient demographics and account data |
| History/Activity | HA | 143 | Historical financial transaction data |
| Primary Patient | PP | 55 | Primary patient/guarantor data |
| Referral | R | 42 | Referral tracking data |
| Surgical Booking | SB | 40 | Surgical scheduling data |
| Referring Doctor | RD | 39 | Referring physician details |
| Appointment/Scheduling | OA | 34 | Scheduling and appointment data |
| Lab | L | 29 | Laboratory data |
| Orders | O | 25 | Order data |
| Diagnostic Imaging | DI | 25 | Imaging order data |
| Immunization | I | 19 | Immunization records |
| Activity | A | 18 | Current financial charges |
| Recall | RC | 7 | Patient recall data |
| Practice Information | PI | 6 | Practice/organization data |
| Immunization CPT | CC | 6 | Immunization CPT codes |
| History | H | 1 | History record flag |

Full inventory saved to `analysis/entity-inventory-full.json` (1,398 fields) and summary to `analysis/entity-inventory-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

MEDENT's EHI export covers an unusually broad range of data domains:

**Richest areas:**
- **Demographics** (80 fields): Extensive — includes SDOH indicators (homelessness, migrant, veteran status), gender identity, sexual orientation, pronouns, education level, employment, income, birth location/time, multiple birth indicator, previous address history. Goes far beyond USCDI requirements.
- **Billing/Financial** (750+ configurable fields): The ASCII Field List covers charges, payments, adjustments, denial codes, insurance details, claim data, referring doctor information, and transaction history across 17 data areas. This is genuinely deep financial coverage.
- **Specialty data**: Ophthalmology/optometry (56 fields for eye/contact prescriptions including keratometry, sphere, cylinder, axis, prism, add power for both eyes) and OB/GYN (23 fields across prenatal episodes and delivery outcomes). These are EHR-specific clinical data that would never appear in a standard FHIR or C-CDA exchange.
- **Medications** (43 fields): Includes NDC, RxNorm, SIG, route, refills, D/C reason, DEA schedule, and administration values.
- **Screenings/Assessments** (43 fields): Tobacco use, SDOH, risk assessments, medication reconciliation, health maintenance items with SNOMED/LOINC codes.
- **Lab Results** (39 fields): Full results with LOINC, reference ranges, abnormal flags, priority, specimen details.

**Adequate areas:**
- Orders (31 fields), Procedures (30 fields), Referrals (26 fields), Immunizations (29 fields), Allergies (21 fields), HIPAA consent (21 fields), Goals (19 fields), Vitals (15 fields), Encounters (14 fields), Diagnoses (13 fields), Problem List (14 fields), Notes (13 fields + C-CDA documents), Documents (12 fields + C-CDA wrapped PDFs).

**Notable inclusions beyond USCDI:**
- HIPAA consent/communication preferences (21 fields)
- Data exchange records (13 fields tracking sent packages)
- Surgical booking data (40 fields in ASCII list)
- Recall data (7 fields)
- Surgical history and medical history as separate entities

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (80 fields) — SDOH, gender identity, pronouns, education, income, birth details | Thorough; exceeds USCDI significantly |
| Encounters / visits | ✅ Covered | `Encounter` (14 fields) — E-Superbill encounters with providers, NPIs, locations | Adequate |
| Problems / conditions | ✅ Covered | `ProblemList` (14 fields) — SNOMED codes, onset/resolved, chronic indicator, rank | Good |
| Medications / prescriptions | ✅ Covered | `Medication` (43 fields) — NDC, RxNorm, SIG, route, refills, DEA schedule, administration | Thorough |
| Allergies | ✅ Covered | `Allergy` (21 fields) — SNOMED, RxNorm, UNII, reactions, severity, criticality | Good |
| Immunizations | ✅ Covered | `Immunization` (29 fields) — CVX, CPT, lot, manufacturer, VIS dates, route, site | Good |
| Vitals | ✅ Covered | `Vital` (15 fields) — LOINC codes, remote monitoring flag, units | Good |
| Lab results | ✅ Covered | `Result` (39 fields) — LOINC, reference ranges, flags, priority, status | Thorough |
| Imaging / diagnostic reports | ✅ Covered | `Order` includes DI orders (31 fields total); DI area in ASCII list (25 fields) | Adequate |
| Procedures | ✅ Covered | `Procedures` (30 fields) — CPT, SNOMED, modifiers, body site, outcome, complications | Thorough |
| Clinical notes / documents | ✅ Covered | `Progress_Note_Listing` (13 fields metadata) + `Document_Listing` (12 fields) + actual documents as C-CDA wrapped PDFs | Good — metadata structured, content as PDF |
| Care plans / goals | ✅ Covered | `Goals` (19 fields) — short-term/long-term goals, achievement dates, status, comments | Good |
| Orders / referrals | ✅ Covered | `Order` (31 fields) + `Referral` (26 fields) — lab/DI/general orders; comprehensive referral tracking | Thorough |
| Insurance / coverage | ✅ Covered | `PatientPlan` (9 fields) + `InsurancePlan` (6 fields) — policy numbers, dates, billing order, payer IDs | Good |
| Claims / billing | ✅ Covered | `Financial` + ASCII Field List (750 fields) — charges, payments, adjustments, denial codes, claim data | **Thorough** — 750+ configurable fields |
| Payments | ✅ Covered | Included in ASCII Field List (History/Activity area, 143 fields) | Part of financial export |
| Consents / directives | ✅ Covered | `HIPAA` (21 fields) — consent preferences, communication channels; `Patient` has advance_directive_ind | Good |
| Patient communications | ⚠️ Partial | Triages exported as C-CDA wrapped PDFs (mentioned in setup doc); no structured message fields | Triages/todos exported as PDFs, but portal messages may not be structured |
| Specialty - Ophthalmology | ✅ Covered | `EyeContactScript` (56 fields) — keratometry, refraction, contact lens Rx | Thorough specialty data |
| Specialty - OB/GYN | ✅ Covered | `OBEpisode` (12 fields) + `OBOutcome` (11 fields) — prenatal episodes, delivery outcomes | Good specialty data |

**Gap Analysis Summary:**
- **Patient communications**: The setup document mentions exporting triages and todos as C-CDA Unstructured Documents (PDFs), which covers some messaging. However, structured portal message data (sender, recipient, thread, timestamps) does not appear as a dedicated entity. This is a minor gap — the content is exportable but not in structured form.
- **Telehealth-specific data**: No dedicated telehealth entity, though the Appointment spec includes encounter types that may cover e-visits.
- **Scanned images**: Exported via the C-CDA Unstructured Document wrapping mechanism rather than as raw image files. Metadata is in Document_Listing.
- All other major domains the product stores are represented in the export.

## 6. Documentation Quality

**Strengths:**
- Every data file has its own PDF specification with field names, plain-English descriptions, and example output values
- Field names are consistent snake_case identifiers matching actual export column headers
- Descriptions reference specific MEDENT UI screens and data sources, making mappings traceable (e.g., "Provider number from the Patient info for the RDr field")
- Standard code systems explicitly identified: SNOMED CT, LOINC, RxNorm, CVX, NDC, CPT/HCPCS, ICD-10, UNII
- The main Setup document provides clear workflow instructions with exact navigation paths
- The Info file provides export metadata with criteria used and per-file record counts
- The 750-field ASCII Field List is comprehensive and organized by logical data area

**Weaknesses:**
- **No machine-readable schema** — all documentation is PDF-only, no JSON Schema, XSD, or similar
- **No formal data types** — field types (string, date, integer, etc.) are not declared, though inferrable from examples
- **Value sets not enumerated** — coded fields reference standard terminologies but don't list valid values (e.g., what are the valid `status` values?)
- **No cardinality specification** — which fields are required vs. optional is not stated
- **No formal relationship diagram** — cross-entity relationships are implied through shared field names rather than documented FK references
- **Financial spec indirection** — the Financial File Specification delegates its field list to a separate HTML manual page, requiring an extra navigation step

**Overall**: A developer could build an import from this documentation with reasonable effort. The field names, descriptions, and examples provide enough context to understand the data model. The main limitation is the lack of machine-readable artifacts — everything requires manual interpretation of PDFs.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

MEDENT's export covers virtually every data domain the product stores. The 31 data entities across the EHI specs address clinical (problems, meds, allergies, vitals, labs, orders, procedures, notes, immunizations, screenings), demographic (80 fields with SDOH), insurance, and administrative data. The 750-field ASCII Financial Field List provides deep billing/revenue cycle coverage including charges, payments, adjustments, and denial codes. Specialty data for ophthalmology (56 fields) and OB/GYN (23 fields) goes well beyond USCDI. The only minor gaps are structured portal message data and telehealth-specific fields. For an ambulatory EHR, this export demonstrably covers the breadth of what the product stores.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built EHI export, not a repackaged FHIR or C-CDA exchange:
- It has its own dedicated UI path (Medical Records > Data Export/Import/Connection Table > Electronic Health Information Export)
- It uses a native delimited text format (CSV/pipe) mapped directly to MEDENT's internal data structures, not projected into FHIR or C-CDA
- It includes data domains (billing, specialty ophthalmology, OB/GYN, HIPAA consent, surgical booking) that would never appear in a (g)(10) FHIR API or C-CDA exchange
- The 33 separate field specifications are product-specific documentation, not references to generic standards
- The FHIR API is documented separately on the same ONC page, confirming these are distinct capabilities
- Documents/triages/todos use C-CDA 2.1 Unstructured Documents as a container format for PDFs, but the structured data export is entirely native

### Key Findings

1. **Genuinely comprehensive export with deep billing coverage**: The 750-field ASCII Financial Field List plus 648 structured EHI fields across 31 entities represents one of the more complete ambulatory EHR exports. Financial data is not an afterthought — it has more documented fields than all clinical entities combined.

2. **Specialty clinical data exported**: Ophthalmology (56 fields for eye/contact prescriptions with keratometry readings) and OB/GYN (prenatal episodes, delivery outcomes) are exported as structured data. This is a strong signal of genuine (b)(10) engagement — these data types exist only in the EHR's internal model and have no USCDI/FHIR equivalent.

3. **Demographics exceed USCDI significantly**: The 80-field Patient specification includes SDOH indicators (homelessness, migrant, veteran status), gender identity, sexual orientation, pronouns, education level, employment status, income, birth location/time, multiple birth indicator, and previous address history.

4. **Documentation is thorough but not machine-readable**: Every entity has a PDF spec with field names, descriptions, and examples. However, there are no JSON Schemas, formal type declarations, or relationship diagrams. A developer could work from these docs but would need to manually translate them.

5. **Minor gap in structured messaging**: Portal messages and triages are exported as C-CDA wrapped PDFs rather than structured data with metadata fields (sender, recipient, timestamps, thread IDs).

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV/pipe-delimited + C-CDA 2.1 Unstructured Documents (for PDFs)
Entities:        32 (31 EHI data files + Financial ASCII Field List)
Fields:          ~1,398 (648 EHI spec fields + 750 financial fields)
Descriptions:    96.8% of EHI fields; 100% of ASCII fields have descriptive names
Sample data:     No (examples in documentation, but no sample export files)
Bulk export:     Yes (supports patient population filters + autorun scheduling)
Domains covered: 18 of 19 applicable domains (patient communications partially covered)
```

### Bottom Line

MEDENT has built a genuine, purpose-specific EHI export that covers the breadth of what their ambulatory EHR stores — clinical, billing, insurance, specialty, and administrative data. The ~1,398 documented fields across 32 entities with per-entity PDF specifications, plus deep financial coverage via the 750-field ASCII Field List, make this one of the more complete (b)(10) implementations for an ambulatory EHR vendor. The single biggest strength is the inclusion of specialty clinical data (ophthalmology, OB/GYN) and deep billing coverage that clearly exceeds anything available through FHIR or C-CDA exchange.
