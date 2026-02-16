# EHI Export Analysis: Harris CareTracker

**Product**: Harris CareTracker  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.1569.Harr.09.00.1.180701 (ID 9589)

## 1. Product Context

Harris CareTracker is a cloud-based, integrated EHR and Practice Management (PM) platform targeting ambulatory/outpatient practices, including independent physicians, small-to-mid-size groups, and medical billing companies. It combines:

- **Clinical/EHR**: Demographics, encounters, problem lists, medications, allergies, immunizations, vitals, lab orders/results, e-prescribing (EPCS), clinical notes with specialty templates, clinical decision support, and care team management.
- **Practice Management**: Appointment scheduling, online patient self-scheduling, automated reminders, no-show tracking.
- **Billing & Revenue Cycle Management (RCM)**: Integrated charge capture, electronic claim submission with scrubbing, eligibility verification, ERA posting, denial management, patient statements, collections, and A/R aging. The vendor emphasizes billing as a core strength — over 1,600 medical billing companies use the platform.
- **Patient Portal/Engagement**: Secure messaging, prescription renewals, appointment requests, intake forms, bill viewing, online payments.
- **Interoperability**: C-CDA exchange, FHIR APIs, Direct messaging, immunization/syndromic surveillance/cancer registry reporting.
- **Specialty support**: Orthopedics, podiatry, pain management, psychiatry, gastroenterology, PT, chiropractic, mental health, and more.

Given this breadth, a genuine (b)(10) export should cover clinical data, billing/claims, insurance, scheduling, patient communications, custom forms, and specialty-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf` | 8-page PDF (v1.0, created 2023-11-15). Documents folder organization and column headings for all exported data classes. Lists 38 data classes with their field names. | **Primary artifact** — sole source of export documentation. |
| `product-research.md` | Background research on Harris CareTracker's capabilities and market position. | Useful for establishing expected data scope. |
| `chpl-metadata.json` | CHPL certification details confirming (b)(10) certification. | Confirms certification status. |

Only one downloadable artifact exists: a single 8-page PDF. No sample data files, no machine-readable schemas, no JSON/XML examples, no separate data dictionary with types or descriptions.

## 3. Export Mechanics

- **Format**: CSV, JSON, or XML (user-selectable export format per the documentation).
- **Mechanism**: UI-driven export from within CareTracker. The documentation describes an "EHI Export feature" with no indication of an API-based mechanism.
- **Single-patient and bulk**: Supports both. Single-patient export creates a timestamped folder. Population export allows selection by Provider, All Active Patients, All Patients, or Encounter Range.
- **Structure**: Each patient gets a dedicated folder with files named `[DataClassName].[format]` (e.g., `Medications.csv`). A `Documents` subfolder holds imported items, images, and related documents in their original format.
- **Access constraints/fees**: Not documented in the available artifacts.

## 4. Export Content: What's In It

The PDF documents **44 distinct data classes** (after correcting for multi-line names in the PDF layout), containing a total of **1,102 fields**. The documentation provides **only field names** — no field types, no descriptions, no value sets, no relationships/foreign keys, no sample data.

### Documentation quality per field

- Fields with names: 1,102 (100%)
- Fields with data types: 0 (0%)
- Fields with descriptions: 0 (0%)
- Fields with value sets/enumerations: 0 (0%)
- Fields with foreign key/relationship info: 0 (0%)

### Vendor's own content organization

The PDF organizes data as a flat list of "Data Classes." Below is the complete inventory (44 data classes after merging multi-line names), categorized by functional domain:

#### Demographics (3 entities, 93 fields)

| Entity | Fields |
|---|---|
| Patient Demographics | 62 |
| Next Of Kin | 17 |
| Occupation and Industry History | 14 |

#### Clinical (13 entities, 182 fields)

| Entity | Fields |
|---|---|
| Clinical Notes | 89 |
| Vital Signs | 28 |
| Smoking Statuses | 12 |
| Travel History | 7 |
| Addendum | 6 |
| FunctionalStatus | 6 |
| Assesments | 5 |
| Goals | 5 |
| Health Concerns | 5 |
| Plan of Treatment | 5 |
| Risk Factors | 5 |
| Tracked Data | 5 |
| User Defined Fields | 4 |

#### Problems & Diagnoses (2 entities, 35 fields)

| Entity | Fields |
|---|---|
| List Problem Pending | 18 |
| List Problem | 17 |

#### Medications (3 entities, 102 fields)

| Entity | Fields |
|---|---|
| Medications | 50 |
| Medications Pending | 38 |
| Injections | 14 |

#### Allergies (2 entities, 51 fields)

| Entity | Fields |
|---|---|
| Allergies and Intolerances Pending | 26 |
| Allergies and Intolerances | 25 |

#### Immunizations (4 entities, 171 fields)

| Entity | Fields |
|---|---|
| HM Rules | 86 |
| HM Rules Ignored | 40 |
| Immunizations | 37 |
| Demographic Immunization | 8 |

#### Lab & Results (1 entity, 126 fields)

| Entity | Fields |
|---|---|
| Lab Tests | 126 |

#### Orders & Referrals (2 entities, 36 fields)

| Entity | Fields |
|---|---|
| Orders | 24 |
| Referrals | 12 |

#### Procedures (1 entity, 15 fields)

| Entity | Fields |
|---|---|
| Procedures | 15 |

#### Devices (1 entity, 19 fields)

| Entity | Fields |
|---|---|
| Implantable device | 19 |

#### Documents & Records (6 entities, 101 fields)

| Entity | Fields |
|---|---|
| Patient Record Release | 26 |
| Patient Health Information Capture | 17 |
| Imported Items | 16 |
| Advance Directives | 14 |
| Alerts | 14 |
| Patient Generated Data | 14 |

#### Billing & Insurance (2 entities, 113 fields)

| Entity | Fields |
|---|---|
| Billing History | 74 |
| Health Insurance | 39 |

#### Care Team (1 entity, 13 fields)

| Entity | Fields |
|---|---|
| Care Team Members | 13 |

#### Family History (1 entity, 20 fields)

| Entity | Fields |
|---|---|
| FamilyHistory | 20 |

#### Scheduling (1 entity, 14 fields)

| Entity | Fields |
|---|---|
| Scheduling | 14 |

#### Communications (1 entity, 11 fields)

| Entity | Fields |
|---|---|
| Email | 11 |

### Notable observations

- **Billing History** (74 fields) is genuinely detailed, including CPT codes, ICD codes (up to 12 per procedure), modifiers, NDC codes, facility details, billing/referring provider details, and prior authorization numbers. This is not a repackaged clinical summary — it reflects the product's native billing data model.
- **Lab Tests** (126 fields) is the most field-rich entity, covering the full lifecycle: order metadata, specimen details, result details, result observations with LOINC codes, abnormal flags, reference ranges, and lab notes. This is granular, internal-model data.
- **Clinical Notes** (89 fields) includes structured sections (CC, HPI, ROS, PMH, PE, Assessment, Plan), vitals, images, tobacco history fields, pregnancy data, vision/hearing, and encounter type — reflecting the product's structured note template rather than a C-CDA projection.
- **Medications** distinguishes between active and pending medications with 50 and 38 fields respectively, including e-prescribing status, SureScripts transmission status, DAW flags, and compound medication fields.
- **HM Rules** (86 fields) is unusually detailed, combining immunization administration records with the underlying clinical decision rules (recommended ages, intervals, risk factors, vaccine details). This is clearly internal data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers clinical, billing, insurance, scheduling, and communications data using what appears to be the product's native data model. The field names (e.g., `PendingFlag`, `Migrated`, `SentBySureScripts`, `PharmacyTransmitFailed`, `HowMigrated`) are clearly internal database column names, not standardized labels.

**Richest areas**: Lab Tests (126 fields), Clinical Notes (89 fields), HM Rules (86 fields), Billing History (74 fields), Patient Demographics (62 fields), Medications (50 fields). These represent deep exports of internal tables.

**Thinnest areas**: Tracked Data (5 fields), Goals (5 fields), Health Concerns (5 fields), Plan of Treatment (5 fields), User Defined Fields (4 fields). Several of these are simple note-type entries (PatientID, EncounterDate, Provider, free-text content).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (62 fields), `Next Of Kin` (17 fields), `Occupation and Industry History` (14 fields) | Thorough — includes race, ethnicity, language, gender identity, sexual orientation, SSN, employer, emergency contact, maiden name, previous address |
| Encounters / visits | ⚠️ Partial | Encounter dates appear in `Clinical Notes`, `Billing History`, and other entities but there is no standalone Encounter/Visit entity | Encounter metadata (type, duration, status, discharge disposition) is partially embedded in Clinical Notes via `EncounterTypeName` but not independently tracked |
| Problems / conditions | ✅ Covered | `List Problem` (17 fields), `List Problem Pending` (18 fields) | Includes ICD codes, SNOMED codes, chronicity, resolution dates, source tracking |
| Medications / prescriptions | ✅ Covered | `Medications` (50 fields), `Medications Pending` (38 fields), `Injections` (14 fields) | Deep — includes e-prescribing metadata, pharmacy details, DAW, NDC, compound med info |
| Allergies | ✅ Covered | `Allergies and Intolerances` (25 fields), `Allergies and Intolerances Pending` (26 fields) | Includes severity, reactions, confirmation tracking, date ranges |
| Immunizations | ✅ Covered | `Immunizations` (37 fields), `HM Rules` (86 fields), `Demographic Immunization` (8 fields) | Extensive — includes VIS info, lot numbers, registry submission dates, vaccine details |
| Vitals | ✅ Covered | `Vital Signs` (28 fields) | Includes BP, HR, RR, temp, SpO2, weight, height, BMI, pain, pulmonary function, head circumference, vision, hearing, pregnancy-related vitals |
| Lab results | ✅ Covered | `Lab Tests` (126 fields) | Very deep — full order/result/observation lifecycle with LOINC codes, specimen details, reference ranges, abnormal flags |
| Imaging / diagnostic reports | ⚠️ Partial | `Imported Items` can contain imaging documents; `Orders` may capture imaging orders | No dedicated imaging/radiology entity; imaging results likely come through as imported documents |
| Procedures | ✅ Covered | `Procedures` (15 fields) | Includes CPT codes, NDC codes, charges, units, appeal flags |
| Clinical notes / documents | ✅ Covered | `Clinical Notes` (89 fields), `Addendum` (6 fields), `Imported Items` (16 fields) | Very detailed structured notes; imported documents preserved in original format |
| Care plans / goals | ⚠️ Partial | `Plan of Treatment` (5 fields), `Goals` (5 fields), `Health Concerns` (5 fields) | Present but thin — each is essentially PatientID + date + provider + free text |
| Orders / referrals | ✅ Covered | `Orders` (24 fields), `Referrals` (12 fields) | Orders include CPTs, ICDs, status, tracking comments; referrals include visit counts and dates |
| Insurance / coverage | ✅ Covered | `Health Insurance` (39 fields) | Includes policy/group numbers, subscriber details, guarantor info, payor/plan details |
| Claims / billing | ✅ Covered | `Billing History` (74 fields) | Deep billing export — CPTs, ICDs (12 slots), modifiers, NDC, facility/provider details, prior auth numbers, referring provider |
| Payments | ❌ Not covered | No payment/remittance entities | Product handles ERA posting and patient payments per product research; this data is absent from the export |
| Consents / directives | ✅ Covered | `Advance Directives` (14 fields), `Patient Generated Data` (14 fields), `Patient Health Information Capture` (17 fields) | Includes directive codes, active/inactive status, document paths |
| Patient communications | ⚠️ Partial | `Email` (11 fields) | Covers email messages but not patient portal messages/secure messaging threads, prescription renewal requests, or appointment requests documented in the product |
| Scheduling | ✅ Covered | `Scheduling` (14 fields) | Includes appointment date, visit type, duration, telehealth flag, booking details |
| Family history | ✅ Covered | `FamilyHistory` (20 fields) | Includes relation details, diagnoses with SNOMED/ICD-10, cause of death |
| Specialty-specific data | ⚠️ Partial | `User Defined Fields` (4 fields), some specialty vitals in Clinical Notes (vision, hearing, pregnancy) | User Defined Fields has only 4 fields (PatientId, FieldValue, Template, DateEntered) — very thin for specialty assessments |

## 6. Documentation Quality

**Strengths**:
- The documentation clearly defines the export structure: per-patient folders, standardized file naming, choice of CSV/JSON/XML formats.
- Field names are enumerated for every data class — 1,102 total fields across 38 entities.
- The field names are reasonably descriptive (e.g., `BillingProviderNPI`, `ResultDetailLoincTestCode`, `TobaccoStatusStartDate`).
- Both single-patient and bulk population export are described.

**Weaknesses**:
- **No data types**: Not a single field has a documented type (string, date, integer, boolean, etc.).
- **No descriptions**: Not one of the 1,102 fields has a description beyond its name.
- **No value sets**: Fields like `Chronicity`, `MedSource`, `OrderStatus`, `ICDType`, `Severity` have no enumerated valid values.
- **No relationships**: No foreign keys, no entity relationships documented. Fields like `ProblemId` in Medications hint at relationships but they're not specified.
- **No sample data**: No example files in any format.
- **No machine-readable schema**: The only artifact is a PDF with text tables.
- **Version 1.0 from November 2023**: No updates since initial publication.

A developer could understand *what fields exist* from this documentation but could not reliably build an import without significant guesswork about types, formats, value sets, and relationships. The field names provide reasonable hints (e.g., `DateOfService` is clearly a date, `IsOpen` is likely boolean), but edge cases would require trial and error.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers a genuinely broad set of domains — clinical data, billing, insurance, scheduling, medications, labs, immunizations, communications — going well beyond USCDI. The inclusion of `Billing History` with 74 fields and `Health Insurance` with 39 fields demonstrates coverage of financial data, which many vendors omit. However, there are meaningful gaps relative to what the product stores:

- **Payments/remittance data**: The product handles ERA posting, patient payments, and collections, but no payment or remittance entities appear in the export.
- **Claims workflow data**: While billing history captures charges, there's no evidence of claim submission status, denial tracking, or A/R data — core features of the product's RCM module.
- **Patient portal interactions**: The product has a full patient portal with appointment requests, prescription renewals, intake forms, and secure messaging. Only `Email` (11 fields) captures communications; portal-specific interactions are absent.
- **Encounters as a standalone entity**: No dedicated encounter/visit table despite encounters being a core organizing concept.

The export is notably stronger than a USCDI-only clinical summary, but falls short of comprehensive coverage of the product's billing and engagement capabilities.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged C-CDA or FHIR API:

1. **Native data model**: Field names like `PendingFlag`, `Migrated`, `HowMigrated`, `SentBySureScripts`, `PharmacyTransmitFailed`, `PracticeFacilityCode` are internal database column names, not standardized labels.
2. **44 product-specific entities**: These don't map to C-CDA sections or FHIR resources — they map to the product's own tables (e.g., `HM Rules`, `HM Rules Ignored`, `Tracked Data`, `User Defined Fields`).
3. **Billing data included**: The `Billing History` entity with 74 fields goes well beyond anything in C-CDA or FHIR (g)(10).
4. **Dedicated export feature**: The documentation describes a purpose-built UI for single-patient and population export with folder organization and format selection.

### Key Findings

1. **Purpose-built export with real billing depth**: The `Billing History` entity (74 fields) and `Health Insurance` (39 fields) demonstrate genuine engagement with (b)(10) beyond USCDI. This is the product's native billing model, not a clinical summary.

2. **Documentation is field-name-only**: Despite covering 44 entities and 1,102 fields, the documentation provides zero descriptions, zero types, zero value sets, and zero relationship information. This is the minimum viable documentation — a developer gets a column header list but nothing else.

3. **Lab Tests entity is impressively granular**: At 126 fields covering orders, specimens, results, observations, notes, and performing lab details, this entity alone demonstrates the export reflects the internal data model, not a standards-based projection.

4. **Missing payment/claims workflow data is the biggest gap**: The product's core RCM capabilities (ERA posting, denial management, collections, A/R aging) are not represented in the export. Given that billing is arguably the product's strongest feature (per user reviews), this is a significant omission.

5. **Single PDF artifact with no updates since November 2023**: The entire documentation consists of one 8-page PDF. No sample data, no schemas, no interactive documentation. Version 1.0 with no revisions suggests minimal ongoing investment.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   CSV, JSON, or XML (user-selectable)
Entities:        44
Fields:          1,102
Descriptions:    0%
Sample data:     No
Bulk export:     Yes (population export by provider, active patients, or encounter range)
Domains covered: 14 of 18 applicable domains (with several partial)
```

### Bottom Line

Harris CareTracker built a genuine purpose-specific EHI export that goes meaningfully beyond USCDI, with particular strength in billing (74-field Billing History) and lab data (126-field Lab Tests). However, the documentation is bare-minimum (field names only — no types, descriptions, or value sets for any of the 1,102 fields), and important revenue cycle data (payments, ERA, denial tracking, collections) is missing despite being a core product capability. A patient would get a broad but not complete copy of their data, and a developer would face significant guesswork interpreting the export without better documentation.
