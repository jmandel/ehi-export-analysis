# EHI Export Analysis: PointClickCare Technologies Inc.

**Product**: PointClickCare (v4), EHR for Practice Groups (v3)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2181.Poin.04.00.1.191231 (PointClickCare, #10246), 15.04.04.2181.Poin.03.01.1.251208 (EHR for Practice Groups, #11729)

## 1. Product Context

PointClickCare is the dominant cloud-based EHR for long-term and post-acute care (LTPAC), serving 27,000+ providers across skilled nursing facilities (SNFs), assisted living, memory care, and continuing care retirement communities. It is the #1 Long-Term Care Software Provider by KLAS Research for six consecutive years.

The platform's data footprint spans several domains relevant to EHI completeness:

- **Clinical documentation**: Point-of-care charting (vitals, allergies, immunizations, treatments), care plans, progress notes, encounter documentation, physician orders (CPOE), diagnosis management, wound care tracking, infection prevention, incident reports, and clinical assessments.
- **Medication management (QuickMAR/eMAR)**: Electronic medication administration records, bar-coded medication administration, pharmacy integration, ePrescribing with EPCS.
- **Assessments**: MDS 3.0 (Minimum Data Set — the federally mandated assessment for SNFs) with PDPM scoring, plus non-MDS clinical assessments and SDOH screening.
- **Revenue cycle management**: Claims processing (Medicare, Medicaid, private), accounts receivable, PDPM support, census management, trust fund management, billing statements.
- **Care coordination**: Secure messaging, hospital admission/readmission alerts, discharge summary exchange, insurance coverage validation.
- **Lab and imaging**: Integrated ordering and results, with attached documents.
- **Patient engagement**: Patient portal (VDT per (e)(1) certification).

The "EHR for Practice Groups" product shares the same underlying data platform and EHI export documentation as the core PointClickCare EHR.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informative? |
|---|---|---|---|
| `downloads/package.tgz` | FHIR IG NPM package — machine-readable StructureDefinitions, ValueSets, CodeSystems | 479 KB compressed; 135 JSON files including 67 StructureDefinitions | **Primary source** — most informative artifact |
| `downloads/site/index.html` | IG home page: export format, directory structure, cross-referencing mechanism with worked JSON examples | 13.6 KB | **High** — explains export mechanics |
| `downloads/site/MDS.html` | MDS 3.0 assessment CSV schema: 7 CSV files, 166 columns | 39.8 KB | **High** — detailed column documentation |
| `downloads/site/NonMDS.html` | Non-MDS assessment CSV schema: 5 CSV files, 59 columns | 20.7 KB | **High** — includes SDOH schema |
| `downloads/site/artifacts.html` | Artifacts summary listing all 71 IG artifacts with descriptions | 37.9 KB | **High** — full artifact index |
| `downloads/site/toc.html` | Table of contents | 62.2 KB | Moderate |
| `downloads/site/StructureDefinition-*.html` (57 files) | Individual HTML pages for each profile, extension, and custom resource | 72–503 KB each | Moderate — human-readable rendering of StructureDefinitions |
| `downloads/site/CodeSystem-*.html` (2 files) | Immunization status and order status code systems | ~10 KB each | Low — supplement |
| `downloads/site/ValueSet-*.html` (2 files) | Value set definitions | ~25 KB each | Low — supplement |
| `downloads/enrichment/structure-definitions.json` | Pre-extracted: 67 profiles, 2 ValueSets, 2 CodeSystems | 717 KB | **High** — used as basis for inventory parsing |
| `downloads/enrichment/csv-schemas.json` | Pre-extracted: 12 CSV schemas, 225 columns | 46 KB | **High** — used as basis for CSV inventory |

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON (Newline Delimited JSON) for clinical and billing data; CSV for MDS and non-MDS assessments; file attachments for documents, radiology images, and lab attachments.
- **Mechanism**: Encrypted compressed files. Single-patient export produces one artifact per patient; population (bulk) export can contain multiple patients per artifact. Encryption keys are obtained "through your PointClickCare documentation" (not publicly specified in the IG). The export is described as a feature of the certified EHR, but no UI screenshots or API endpoints are provided.
- **Single-patient vs bulk**: Both supported. The IG states "A single artifact is generated per patient for single export, or an artifact can contain multiple patients for population export."
- **Access constraints**: Encryption key distribution is not documented in the public IG. No fees are mentioned.

**Directory structure per patient:**
```
[Patient ID]/
  [Patient ID].json              # Patient FHIR resource
  [Patient ID]-manifest.json     # Manifest of export contents
  mds_assessments/
    [Assessment ID]/             # 7 CSV files per MDS assessment
  non_mds_assessments/
    [Assessment ID]/             # 5 CSV files per assessment
  Files/                         # Consent and advance directive documents
  radiology-attachments/         # Radiology images
  lab-attachments/               # Lab result attachments
```

Cross-references between resources use FHIR references. Index files provide lookup tables for referenced entities (e.g., Practitioner, Organization) that appear across multiple patients.

## 4. Export Content: What's In It

### Data dictionary summary

The EHI Export documentation is a formal FHIR R4 Implementation Guide (IG), built with the standard HL7 FHIR IG Publisher toolchain. The FHIR IG NPM package (`ehi-export.pointclickcare.com#0.1.0`) is downloadable and machine-readable.

**Totals (from `analysis/full-entity-inventory.json`):**
- **48 entities** (36 FHIR resource profiles + 12 CSV schemas)
  - 26 standard FHIR R4 resource profiles (constraint on existing FHIR resources)
  - 10 custom FHIR resource types (specialization — new resource types for billing, census, orders, etc.)
  - 12 CSV schemas (7 MDS + 5 non-MDS assessment files)
- **31 extensions** (PCC-specific and US Core extensions)
- **2 value sets**, **2 code systems** (ImmunizationStatus: 11 concepts, OrderStatus: 12 concepts)
- **1,572 total fields** across all entities (1,347 from FHIR profiles + 225 from CSV schemas)
  - **1,572 fields with descriptions (100%)** — every field has at least a `short` description
  - 1,490 FHIR snapshot elements across 36 profiles; 610 are vendor-defined in differentials, 880 are inherited from FHIR base
- **No sample data** provided

### Vendor's own content organization

The IG organizes content into three tiers:
1. **Standard FHIR R4 profiles** — constrained profiles on standard FHIR resources for clinical data
2. **Custom (PCC-specific) resources** — new resource types following FHIR DomainResource structure for data domains without FHIR equivalents
3. **CSV schemas** — for MDS and non-MDS assessment data

| Entity/Resource | Fields | Described | Types | Category |
|---|---|---|---|---|
| **Standard FHIR Profiles** | | | | |
| patient | 54 | 54 | yes | Demographics |
| relatedPerson | 25 | 25 | yes | Demographics |
| encounter | 72 | 72 | yes | Encounters |
| condition | 36 | 36 | yes | Problems / Conditions |
| medication | 39 | 39 | yes | Medications |
| medicationRequest | 102 | 102 | yes | Medications |
| medicationDispense | 44 | 44 | yes | Medications |
| allergy-intolerance | 56 | 56 | yes | Allergies |
| immunization | 63 | 63 | yes | Immunizations |
| observation | 49 | 49 | yes | Observations / Vitals |
| diagnostic-eport | 31 | 31 | yes | Lab / Diagnostics |
| serviceRequest | 41 | 41 | yes | Lab / Diagnostics |
| specimen | 47 | 47 | yes | Lab / Diagnostics |
| procedure | 49 | 49 | yes | Procedures |
| documentReference | 44 | 44 | yes | Clinical Notes / Documents |
| care-plan | 39 | 39 | yes | Care Plans / Goals |
| goal | 30 | 30 | yes | Care Plans / Goals |
| care-team | 28 | 28 | yes | Care Team |
| familyMemberHistory | 34 | 34 | yes | Family History |
| coverage | 49 | 49 | yes | Insurance / Coverage |
| implantable-device | 65 | 65 | yes | Medical Devices |
| practitioner | 27 | 27 | yes | Providers |
| practitionerRole | 34 | 34 | yes | Providers |
| organization | 25 | 25 | yes | Organizations |
| location | 38 | 38 | yes | Locations |
| provenance | 31 | 31 | yes | Provenance |
| **Custom PCC Resources** | | | | |
| Authorization | 18 | 18 | yes | Billing & Financial |
| BillingStatement | 18 | 18 | yes | Billing & Financial |
| InvoiceTransaction | 13 | 13 | yes | Billing & Financial |
| Claim | 29 | 29 | yes | Billing & Financial |
| Payment | 19 | 19 | yes | Billing & Financial |
| Census | 27 | 27 | yes | Census / Admissions |
| Order | 36 | 36 | yes | Orders |
| CareProfile | 13 | 13 | yes | Care Profile |
| medicalDevice | 11 | 11 | yes | Medical Devices |
| singleDevice | 11 | 11 | yes | Medical Devices |
| **MDS Assessment CSVs** | | | | |
| assessment.csv (MDS) | 90 | 90 | yes | MDS Assessments |
| sections.csv (MDS) | 9 | 9 | yes | MDS Assessments |
| sectionV.csv (MDS) | 9 | 9 | yes | MDS Assessments |
| pdpmScores.csv (MDS) | 35 | 35 | yes | MDS Assessments |
| score.csv (MDS) | 2 | 2 | yes | MDS Assessments |
| sectionVRapProfile.csv (MDS) | 6 | 6 | yes | MDS Assessments |
| responses.csv (MDS) | 15 | 15 | yes | MDS Assessments |
| **Non-MDS Assessment CSVs** | | | | |
| assessment.csv (NonMDS) | 25 | 25 | yes | Non-MDS Assessments |
| sections.csv (NonMDS) | 9 | 9 | yes | Non-MDS Assessments |
| score.csv (NonMDS) | 2 | 2 | yes | Non-MDS Assessments |
| responses.csv (NonMDS) | 9 | 9 | yes | Non-MDS Assessments |
| sdoh_and_health_status_responses.csv | 14 | 14 | yes | Non-MDS Assessments |

### Category breakdown

| Category | Entities | Fields | Fields Described |
|---|---|---|---|
| Allergies | 1 | 56 | 56 |
| Billing & Financial | 5 | 97 | 97 |
| Care Plans / Goals | 2 | 69 | 69 |
| Care Profile | 1 | 13 | 13 |
| Care Team | 1 | 28 | 28 |
| Census / Admissions | 1 | 27 | 27 |
| Clinical Notes / Documents | 1 | 44 | 44 |
| Demographics | 2 | 79 | 79 |
| Encounters | 1 | 72 | 72 |
| Family History | 1 | 34 | 34 |
| Immunizations | 1 | 63 | 63 |
| Insurance / Coverage | 1 | 49 | 49 |
| Lab / Diagnostics | 3 | 119 | 119 |
| Locations | 1 | 38 | 38 |
| MDS Assessments | 7 | 166 | 166 |
| Medical Devices | 3 | 87 | 87 |
| Medications | 3 | 185 | 185 |
| Non-MDS Assessments | 5 | 59 | 59 |
| Observations / Vitals | 1 | 49 | 49 |
| Orders | 1 | 36 | 36 |
| Organizations | 1 | 25 | 25 |
| Problems / Conditions | 1 | 36 | 36 |
| Procedures | 1 | 49 | 49 |
| Provenance | 1 | 31 | 31 |
| Providers | 2 | 61 | 61 |
| **TOTAL** | **48** | **1,572** | **1,572** |

The complete entity inventory is in `analysis/full-entity-inventory.json`.

### Notable custom resources

The 10 custom PCC resources are particularly noteworthy because they export billing, financial, and operational data that has no standard FHIR representation:

- **Claim** (29 fields): Revenue codes, HIPPS codes, service dates, charges, non-covered charges, grand totals, payer, NPI, insured info, DRG-equivalent `careLevel`, `dailyRate`. This directly exports the claims data PointClickCare generates for Medicare/Medicaid/private payers.
- **BillingStatement** (18 fields): Statement date, invoice transactions, balance due, previous balance, payments, current charges, total due.
- **InvoiceTransaction** (13 fields): Individual billing line items with effective date, description, units, unit amount, amount.
- **Payment** (19 fields): Receipt amount, trust amount, payer, posting date, check info, payment type.
- **Authorization** (18 fields): Prior authorization records with payer, insurance, start/end dates, review dates, request status, remaining days/visits.
- **Census** (27 fields): Patient census/admission tracking with action type, payer, status codes (A=Active, HP=Hospital Leave, TP=Therapeutic Leave, D=Discharged, etc.), room/bed, physician, HIPPS, qualifying hospital stay period.
- **Order** (36 fields): Non-pharmacy orders covering diet, lab, diagnostic, and immunization orders with LOINC codes, communication method, and a custom OrderStatus code system (12 statuses).
- **CareProfile** (13 fields): Patient care profile questionnaire responses.
- **medicalDevice** / **singleDevice** (11 fields each): Non-implantable medical devices.

### Extensions (31 total)

PCC defines 31 FHIR extensions, including:
- **Medication-related** (6): AdministeredBy, RouteOfAdministration, ScheduleStartDate, TimeCode, OrderCategory, OrderType
- **Allergy-related** (4): RecordedBy, RevisionBy, ResolvedDate, RevisionDate
- **Payer-related** (3): PayerType, PayerDescription, MedicareAdvantagePlan
- **Demographics** (8): US Core extensions for race, ethnicity, birth sex, sex, gender identity, tribal affiliation, pronouns, plus PCC-specific previous-name, occupation, CompanyName
- **Order-related** (3): OrderedBy, CommunicationMethod, loinc-order-codes
- **Other** (3): Context, Custodian, ProviderNumber

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

PointClickCare's EHI export is organized into three complementary formats:

**FHIR R4 NDJSON — Clinical Data (26 standard profiles):** The clinical data export uses standard FHIR R4 resources with PCC-specific extensions. This covers the full spectrum of clinical documentation: demographics (Patient, RelatedPerson), encounters, conditions, medications (including orders and dispenses), allergies, immunizations, vitals/observations, lab results (DiagnosticReport, ServiceRequest, Specimen), procedures, clinical notes (DocumentReference), care plans, goals, care team, family history, insurance coverage, and devices. The `medicationRequest` profile is the richest (102 fields) with detailed dosing, timing, indications, and pharmacy information.

**FHIR R4 NDJSON — Financial/Operational Data (10 custom resources):** This is the standout feature. PCC created purpose-built FHIR-like resources for billing and operational data with 5 dedicated billing/financial entities (Claim, BillingStatement, InvoiceTransaction, Payment, Authorization) totaling 97 fields, a Census resource for admission/discharge/transfer tracking, an Order resource for non-pharmacy orders, CareProfile for questionnaire data, and two device resources.

**CSV — Assessments (12 schemas, 225 columns):** MDS 3.0 assessments are exported as 7 CSV files per assessment with 166 total columns, including the full assessment metadata (90 columns with RUG scores, PDPM data, ADL indices, CAT triggers, CMI weights, HIPPS codes), section-level data, PDPM scoring across all five components (PT, OT, SLP, nursing, NTA — 35 columns), RAP profiles, and individual question-level responses. Non-MDS assessments use 5 CSV files (59 columns) including a dedicated SDOH and health status responses schema.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` (54 fields), `relatedPerson` (25 fields), US Core extensions for race, ethnicity, sex, gender identity, tribal affiliation, pronouns; PCC extensions for occupation, company, previous name | Thorough |
| Encounters / visits | ✅ Covered | `encounter` (72 fields) | Thorough |
| Problems / conditions / diagnoses | ✅ Covered | `condition` (36 fields) | Thorough |
| Medications / prescriptions | ✅ Covered | `medication` (39 fields), `medicationRequest` (102 fields with detailed dosing), `medicationDispense` (44 fields) | Thorough — 185 total medication fields |
| Allergies | ✅ Covered | `allergy-intolerance` (56 fields) with PCC tracking extensions | Thorough |
| Immunizations | ✅ Covered | `immunization` (63 fields) with PCC ImmunizationStatus code system (11 concepts) | Thorough |
| Vitals | ✅ Covered | `observation` (49 fields) | Thorough |
| Lab results | ✅ Covered | `diagnostic-eport` (31 fields), `serviceRequest` (41 fields), `specimen` (47 fields), plus `lab-attachments/` folder | Thorough — 119 fields across 3 entities plus attachments |
| Imaging / diagnostic reports | ✅ Covered | `diagnostic-eport`, `serviceRequest`, plus `radiology-attachments/` folder | Adequate |
| Procedures | ✅ Covered | `procedure` (49 fields) | Thorough |
| Clinical notes / documents | ✅ Covered | `documentReference` (44 fields) — covers progress notes, advanced directives, consent documents, radiology reports, skin/wound docs, therapy files; plus `Files/` folder for attachments | Thorough |
| Care plans / goals | ✅ Covered | `care-plan` (39 fields), `goal` (30 fields) | Thorough |
| Orders / referrals | ✅ Covered | Custom `Order` resource (36 fields) for non-pharmacy orders (diet, lab, diagnostic, immunization); `medicationRequest` for pharmacy orders; `serviceRequest` for service requests | Thorough |
| Insurance / coverage | ✅ Covered | `coverage` (49 fields) with PCC extensions for PayerType, PayerDescription, MedicareAdvantagePlan | Thorough |
| Claims / billing | ✅ Covered | Custom `Claim` (29 fields), `BillingStatement` (18 fields), `InvoiceTransaction` (13 fields) | Thorough — 60 fields across 3 entities covering claims end-to-end |
| Payments | ✅ Covered | Custom `Payment` (19 fields) — receipt amount, trust amount, payer, posting date, check info, payment type | Thorough |
| Prior authorizations | ✅ Covered | Custom `Authorization` (18 fields) — payer, insurance, dates, review dates, status, remaining days/visits | Thorough |
| Consents / directives | ✅ Covered | `documentReference` references consent and advance directive documents; `Files/` folder contains actual documents | Adequate |
| MDS assessments | ✅ Covered | 7 CSV schemas, 166 columns — comprehensive including PDPM scores, RUG calculations, ADL indices, CATs, section-level data, individual responses | Excellent — this is exceptionally detailed for LTPAC |
| Non-MDS assessments | ✅ Covered | 5 CSV schemas, 59 columns — includes SDOH and health status responses | Thorough |
| Census / admissions | ✅ Covered | Custom `Census` (27 fields) — admission, discharge, transfer, leave of absence, room/bed, payer, status, HIPPS | Thorough |
| Patient communications / portal messages | ❌ Not covered | No messaging resources in export | Product has Secure Conversations module; potential gap, but messaging content may be administrative rather than part of the designated record set |
| Specialty-specific (LTPAC) | ✅ Covered | MDS 3.0 assessments, PDPM scoring, wound care documents, CareProfile questionnaires, Census with LTPAC-specific fields (RUGS, HIPPS, qualifying hospital stay) | Thorough |
| Medication administration (eMAR) | ⚠️ Partial | `medicationRequest` has AdministeredBy extension and timing fields, but no dedicated `MedicationAdministration` resource for individual administration events | Product has QuickMAR/eMAR; individual administration records (timestamps, doses administered, holds, refusals) may not be fully captured |
| Family history | ✅ Covered | `familyMemberHistory` (34 fields) | Thorough |

**Summary**: 20 of 22 applicable domains are covered (✅), 1 is partially covered (⚠️), and 1 is not covered (❌). The single uncovered domain (secure messaging/portal messages) is arguable — messaging content may not be part of the designated record set depending on whether messages are used for care decisions. The partial coverage for medication administration is a more substantive gap given the importance of eMAR in LTPAC.

## 6. Documentation Quality

**Strengths:**
- **Machine-readable**: The FHIR IG NPM package (`ehi-export.pointclickcare.com#0.1.0`) is a proper, downloadable FHIR IG package. It can be loaded into FHIR tooling for validation, code generation, and automated processing. This is the gold standard for EHI export documentation.
- **100% description coverage**: All 1,572 fields across all 48 entities have at least a `short` description. The CSV assessment schemas additionally have type and nullable specifications for all 225 columns.
- **Worked examples**: The index page includes inline JSON examples showing how cross-references between resources work, with actual anonymized data demonstrating the reference resolution pattern.
- **Purpose-built custom resources**: Instead of omitting billing data or forcing it into ill-fitting FHIR resources, PCC created 10 custom resource types with proper FHIR DomainResource structure, making them parseable with standard FHIR tooling.
- **Clear directory structure**: The per-patient export layout is documented with separate folders for MDS assessments, non-MDS assessments, consent documents, radiology images, and lab attachments.
- **Recently updated**: Generated 2026-02-04, last modified 2026-02-09.

**Weaknesses:**
- **No sample export files**: Despite the worked JSON examples on the index page, the IG does not include downloadable sample data files (e.g., example NDJSON bundles, sample CSV assessment files). A developer building an import would need to work entirely from the StructureDefinitions.
- **Draft status**: Version 0.1.0 with `notForPublication: true` and "ci-build" status. This is technically a development build, not a published release.
- **No export trigger documentation**: The IG describes what comes out but not how to trigger an export (no UI guide, no API specification).
- **Encryption key process undocumented**: "Please consult your PointClickCare documentation" is the only guidance on encryption keys.
- **Sparse value sets**: Only 2 vendor-defined code systems (ImmunizationStatus, OrderStatus). Other coded fields (e.g., Census `status`, `payerOptions`) document valid values inline in `short` descriptions rather than in proper ValueSet resources.
- **Some descriptions are minimal**: A few custom resources have terse descriptions (e.g., CareProfile: "Patient CareProfile"), though their elements are adequately documented.

**Overall**: A developer with FHIR experience could build a parser/importer from these artifacts. The combination of machine-readable StructureDefinitions and clear directory structure documentation makes this one of the more developer-friendly EHI export documentation sets. The main gap is the absence of sample data.

## 7. Overall Assessment

### Classification

**Comprehensive native export** — with FHIR projection.

This is a hybrid approach: PointClickCare exports its native data model projected into FHIR R4 structures (for data that maps to standard FHIR resources) and custom FHIR-like resources (for data that doesn't, particularly billing and LTPAC-specific data). The CSV format for MDS/non-MDS assessments is a pragmatic choice for inherently tabular assessment data. The export covers clinical, billing, financial, administrative, and specialty domains comprehensively.

### Key Findings

1. **Genuine "(b)(10)" compliance, not a repackaged (g)(10):** PointClickCare has clearly invested engineering effort in a purpose-built EHI export. The 10 custom FHIR resources for billing, claims, payments, authorizations, census, and orders go well beyond what a standard FHIR API would provide. This is not a C-CDA or FHIR Bulk Data export relabeled as "(b)(10)."

2. **Exceptionally strong MDS/assessment coverage:** The MDS 3.0 export (166 columns across 7 CSV files) captures the full depth of MDS data including PDPM scores across all five components, RUG calculations, ADL indices, CAT triggers, and individual question-level responses. This is critical for LTPAC and demonstrates domain-specific expertise in the export design.

3. **End-to-end revenue cycle coverage:** Five custom resources (Claim, BillingStatement, InvoiceTransaction, Payment, Authorization) with 97 total fields cover the billing lifecycle from prior authorization through claims to payment. This is rare among EHI exports — most vendors omit billing data entirely.

4. **100% field description coverage:** All 1,572 fields across 48 entities have descriptions. Combined with FHIR data types, cardinality, and the machine-readable IG package, this is well above average documentation quality.

5. **Potential gap in medication administration records:** The absence of a dedicated `MedicationAdministration` FHIR resource is notable for a product whose eMAR (QuickMAR) is a core clinical workflow. The `AdministeredBy` extension on `MedicationRequest` partially addresses this, but individual administration events (time, dose, refusals, holds) may not be fully captured.

### Summary Stats

```
Classification:  Comprehensive native export (FHIR projection + custom resources)
Export format:   FHIR R4 NDJSON + CSV + file attachments
Model type:      Hybrid (standard FHIR + custom resources + CSV)
Entities:        48 (26 FHIR profiles + 10 custom resources + 12 CSV schemas)
Fields:          1,572
Descriptions:    100%
Sample data:     No (worked examples in docs only)
Bulk export:     Yes (population export supported)
Domains covered: 20 of 22 applicable domains (1 partial, 1 not covered)
```

### Bottom Line

PointClickCare delivers one of the strongest EHI exports among certified EHRs. It covers clinical, billing, financial, assessment, and LTPAC-specialty data with 48 entities, 1,572 fields, and 100% description coverage. The single most significant gap is the lack of a dedicated medication administration resource for individual eMAR events in a product where eMAR is a core workflow — though this data may be partially captured elsewhere. A patient or provider would get a substantially complete copy of their data from this export.
