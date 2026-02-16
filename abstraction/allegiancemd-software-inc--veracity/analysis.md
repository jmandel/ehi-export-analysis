# EHI Export Analysis: AllegianceMD Software, Inc.

**Product**: Veracity v9.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2672.ALLE.01.01.1.220117

## 1. Product Context

Veracity is a cloud-based, all-in-one ambulatory EHR, practice management, and billing platform from AllegianceMD Software, Inc. (Tulsa, OK). It targets small-to-mid-sized physician practices across 50+ specialties. The product is sold as a single integrated system — not modular — encompassing:

- **Clinical EHR**: charting with customizable templates, CPOE, e-prescribing (EPCS), clinical decision support, problem/medication/allergy lists, vitals, lab ordering and results, imaging results
- **Practice Management**: scheduling, patient registration, case management (workers' comp), document management, faxing
- **Billing/Revenue Cycle**: charge capture, electronic claims submission, clearinghouse, eligibility verification, ERA/EOB posting, denial management, patient statements, collections, credit card processing
- **Patient Engagement**: patient portal (demographics, messaging, refill requests, lab results, bill pay), self-service kiosk, appointment reminders, online scheduling
- **Telemedicine**: virtual visits integrated with EHR workflow
- **Quality/Reporting**: MACRA/MIPS dashboard, immunization registry reporting, cancer case reporting
- **Chronic Care Management**: CCM program with care plans

This product scope establishes the baseline: a comprehensive (b)(10) export should cover clinical data, billing/claims, insurance, scheduling, patient communications, and case management.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-documentation-page.html` (37 KB) | Main documentation page describing CBOR export format | **Medium** — brief, gives format and links to data structure |
| `ehi-export-index.html` (11 KB) | Javadoc index listing all 31 entity classes | **High** — complete entity inventory |
| `entity-data-dictionary.json` (69 KB) | Pre-extracted JSON of all 31 entities and 715 fields | **High** — structured reference |
| 31 individual `*Entity.html` files (2.7–35.8 KB each) | Javadoc detail pages for each entity with field names, types, and some descriptions | **High** — primary source for field-level analysis |
| `ehi-export-documentation-page.png` (156 KB) | Screenshot of main documentation page | **Low** — visual confirmation only |
| `ehi-export-data-structure-index.png` (113 KB) | Screenshot of Javadoc entity index | **Low** — visual confirmation only |
| `ehi-export-stylesheet.css` (31 KB) | Javadoc CSS | **None** — styling only |

The Javadoc entity HTML pages are the primary source of truth. Each page uses a standard Javadoc "Field Summary" table with columns: Modifier and Type, Field, Description.

## 3. Export Mechanics

- **Format**: CBOR (Concise Binary Object Representation, RFC 8949) — a binary encoding semantically equivalent to JSON. This is unusual; most EHR vendors use CSV, JSON, or FHIR. The vendor links to [cbor.io/impls.html](https://cbor.io/impls.html) for open-source parsing tools.
- **Delivery**: ZIP file containing CBOR-encoded data objects plus documents and clinical data files. Each document has a corresponding `.meta` file describing it.
- **Data model**: Patient-centric. `PatientEntity` is the root object containing 20 nested entity lists (allergies, medications, encounters, etc.) plus scalar demographic fields. Some entities are further nested (e.g., `EncountersEntity` contains `TransactionsEntity` and `EncountersDiagEntity`; `CasesEntity` contains `InsuranceDataEntity`).
- **Mechanism**: Not explicitly documented — no UI screenshots, API endpoints, or workflow instructions are provided. The documentation only describes the data format and structure.
- **Single-patient vs bulk**: Not stated. The patient-centric data model (one root `PatientEntity`) suggests single-patient export.
- **Access constraints/fees**: Not documented.

## 4. Export Content: What's In It

### Data Dictionary Overview

The export is documented via a Javadoc-generated data dictionary covering **31 entities** with **715 total fields**. All 715 fields have data types documented. Only **164 fields (22.9%)** have descriptions beyond the field name.

Description coverage is highly uneven: 4 entities have 100% descriptions (PatientEntity, CasesEntity, InsuranceDataEntity, InsuranceDataAuthorizationsEntity — totaling 157 of 164 described fields), while the remaining 27 entities have almost none (7 described fields total among them).

Field types are Java types: String (427), Date (111), Boolean (84), Double (36), Integer (21), Short (8), Long (1), byte[] (1), plus 24 `List<*Entity>` references for nested relationships.

### Vendor's own content organization

The entity names reflect the vendor's internal data model. There is no explicit vendor-provided categorization, but entity naming reveals clear domain groupings:

| Entity | Fields | Described | Types | Domain |
|---|---|---|---|---|
| PatientEntity | 71 | 71 (100%) | yes | Demographics (root) |
| EmrMedicationEntity | 62 | 1 (2%) | yes | Medications |
| EmrPatientOrderPanelEntity | 60 | 1 (2%) | yes | Orders/Labs |
| TransactionsEntity | 53 | 0 (0%) | yes | Billing |
| EncountersEntity | 47 | 2 (4%) | yes | Encounters |
| EmrInjectionEntity | 43 | 0 (0%) | yes | Immunizations |
| CasesEntity | 41 | 41 (100%) | yes | Cases |
| InsuranceDataEntity | 36 | 36 (100%) | yes | Insurance |
| AppointmentsEntity | 25 | 0 (0%) | yes | Scheduling |
| GuarantorEntity | 24 | 0 (0%) | yes | Insurance/Guarantor |
| ScreeningEntity | 23 | 1 (4%) | yes | Screenings |
| MessagesEntity | 21 | 1 (5%) | yes | Communications |
| EmrPatientOrderItemEntity | 20 | 0 (0%) | yes | Orders/Labs |
| EmrImplantableDeviceEntity | 20 | 0 (0%) | yes | Devices |
| PatientCareTeamEntity | 19 | 0 (0%) | yes | Care Team |
| EmrAllergyEntity | 18 | 0 (0%) | yes | Allergies |
| EmrRefToProvidersEntity | 18 | 1 (6%) | yes | Referrals |
| TasksEntity | 18 | 0 (0%) | yes | Tasks |
| EmrProblemEntity | 16 | 0 (0%) | yes | Problems |
| PaymentEntity | 12 | 0 (0%) | yes | Billing/Payments |
| PatientMedicalFormEntity | 11 | 0 (0%) | yes | Medical Forms |
| EmrVitalsCategoryEntity | 11 | 0 (0%) | yes | Vitals (categories) |
| InsuranceDataAuthorizationsEntity | 9 | 9 (100%) | yes | Insurance/Auth |
| EmrVitalsEntity | 7 | 0 (0%) | yes | Vitals |
| InternalNotesEntity | 6 | 0 (0%) | yes | Notes |
| PatientPharmacyEntity | 10 | 0 (0%) | yes | Pharmacy |
| TaskCommentsEntity | 4 | 0 (0%) | yes | Tasks |
| PatientCustomFieldsEntity | 3 | 0 (0%) | yes | Custom Fields |
| EncountersDiagEntity | 3 | 0 (0%) | yes | Diagnoses |
| NotesEntity | 2 | 0 (0%) | yes | Notes |
| EmrEncounterEntity | 2 | 0 (0%) | yes | Encounters |

### Category Breakdown

| Category | Entities | Fields | Fields Described |
|---|---|---|---|
| Demographics | 5 | 114 | 71 (62%) |
| Clinical - Orders/Labs | 2 | 80 | 1 (1%) |
| Insurance | 3 | 69 | 45 (65%) |
| Billing | 2 | 65 | 0 (0%) |
| Clinical - Medications | 1 | 62 | 1 (2%) |
| Clinical - Encounters | 2 | 49 | 2 (4%) |
| Clinical - Immunizations | 1 | 43 | 0 (0%) |
| Cases | 1 | 41 | 41 (100%) |
| Scheduling | 1 | 25 | 0 (0%) |
| Clinical - Screenings | 1 | 23 | 1 (4%) |
| Tasks | 2 | 22 | 0 (0%) |
| Communications | 1 | 21 | 1 (5%) |
| Clinical - Devices | 1 | 20 | 0 (0%) |
| Clinical - Allergies | 1 | 18 | 0 (0%) |
| Clinical - Vitals | 2 | 18 | 0 (0%) |
| Clinical - Referrals | 1 | 18 | 1 (6%) |
| Clinical - Problems | 1 | 16 | 0 (0%) |
| Notes | 2 | 8 | 0 (0%) |
| Clinical - Diagnoses | 1 | 3 | 0 (0%) |

### Data Model Structure

The export is patient-centric with a hierarchical structure:

```
PatientEntity (root, 71 fields)
├── allergyList → EmrAllergyEntity (18)
├── medicationList → EmrMedicationEntity (62)
├── problemList → EmrProblemEntity (16)
├── vitalsList → EmrVitalsEntity (7)
├── injectionAndImmunizationList → EmrInjectionEntity (43)
├── deviceList → EmrImplantableDeviceEntity (20)
├── ordersList → EmrPatientOrderPanelEntity (60)
│   └── itemsList → EmrPatientOrderItemEntity (20)
├── encountersEntities → EncountersEntity (47)
│   ├── encountersDiagEntities → EncountersDiagEntity (3)
│   └── transactionsEntities → TransactionsEntity (53)
├── caseList → CasesEntity (41)
│   └── insuranceDataList → InsuranceDataEntity (36)
│       └── insuranceDataAuthorizationsList → InsuranceDataAuthorizationsEntity (9)
├── outgoingReferralList → EmrRefToProvidersEntity (18)
├── screenings → ScreeningEntity (23)
├── appointmentsEntityList → AppointmentsEntity (25)
├── messagesEntities → MessagesEntity (21)
├── paymentEntities → PaymentEntity (12)
├── tasksList → TasksEntity (18)
│   └── taskCommentsEntities → TaskCommentsEntity (4)
├── medicalForms → PatientMedicalFormEntity (11)
├── patientPharmacyEntities → PatientPharmacyEntity (10)
├── patientCustomFieldsList → PatientCustomFieldsEntity (3)
├── alertNotes → NotesEntity (2)
└── internalNotesEntities → InternalNotesEntity (6)
```

Four entities are not directly referenced in this hierarchy but exist in the data model: `EmrEncounterEntity` (2 fields — minimal, possibly a linking table), `EmrVitalsCategoryEntity` (11 fields — vitals type definitions), `GuarantorEntity` (24 fields — responsible party), and `PatientCareTeamEntity` (19 fields — care team members). These likely appear elsewhere in the CBOR structure or as reference data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a genuinely broad set of data domains from the product's internal data model:

**Strong coverage:**
- **Demographics** (114 fields across 5 entities): PatientEntity alone has 71 fields with 100% descriptions — includes demographics, contact info, preferred pharmacy, custom fields, medical forms, and care team. This is the best-documented area.
- **Insurance** (69 fields, 3 entities): InsuranceDataEntity (36 fields, 100% described) covers coverage details; InsuranceDataAuthorizationsEntity (9 fields, 100% described) covers prior authorizations; GuarantorEntity (24 fields) captures responsible party info.
- **Cases** (41 fields, 100% described): Workers' comp and other case types with full field descriptions.
- **Billing** (65 fields, 2 entities): TransactionsEntity (53 fields) includes CPT codes, diagnoses, amounts, insurance payments, adjustments. PaymentEntity (12 fields) captures payment records. No descriptions, but field names are self-explanatory (e.g., `cpt`, `amount`, `balance`, `insurancePaid`).
- **Medications** (62 fields): Comprehensive prescription data including drug details, dosing, pharmacy, prescriber info.
- **Orders/Labs** (80 fields, 2 entities): Lab/imaging order panels with results data.

**Moderate coverage:**
- **Encounters** (49 fields across 2 entities): EncountersEntity has 47 fields mixing clinical and billing data (place of service, referring provider, charges). EmrEncounterEntity is minimal (2 fields).
- **Immunizations** (43 fields): Detailed injection/immunization records.
- **Referrals** (18 fields): Outgoing referral tracking.
- **Screenings** (23 fields): Patient screening assessments.
- **Messages** (21 fields): Patient-related communications.

**Thin but present:**
- **Vitals** (18 fields, 2 entities): Basic vital sign measurements and category definitions.
- **Allergies** (18 fields), **Problems** (16 fields), **Devices** (20 fields): Present but no descriptions.
- **Notes** (8 fields, 2 entities): Internal and alert notes, very thin.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PatientEntity` (71 fields, 100% described), `PatientCustomFieldsEntity` (3 fields), `PatientCareTeamEntity` (19 fields) | Thorough — includes contact info, custom fields, care team |
| Encounters / visits | ✅ Covered | `EncountersEntity` (47 fields), `EmrEncounterEntity` (2 fields) | Good breadth with 47 fields mixing clinical and billing encounter data |
| Problems / conditions / diagnoses | ✅ Covered | `EmrProblemEntity` (16 fields), `EncountersDiagEntity` (3 fields) | Present; no descriptions but field names adequate |
| Medications / prescriptions | ✅ Covered | `EmrMedicationEntity` (62 fields) | Deep — 62 fields for prescription/medication data |
| Allergies | ✅ Covered | `EmrAllergyEntity` (18 fields) | Present with 18 fields |
| Immunizations | ✅ Covered | `EmrInjectionEntity` (43 fields) | Thorough — 43 fields for injection/immunization records |
| Vitals | ✅ Covered | `EmrVitalsEntity` (7 fields), `EmrVitalsCategoryEntity` (11 fields) | Present; basic measurement data plus category definitions |
| Lab results | ✅ Covered | `EmrPatientOrderPanelEntity` (60 fields), `EmrPatientOrderItemEntity` (20 fields) | Solid — 80 fields for orders and results |
| Imaging / diagnostic reports | ⚠️ Partial | Orders may include imaging (same entity as labs); no dedicated imaging entity | Product supports imaging results viewing; may be captured in order entities but unclear |
| Procedures | ⚠️ Partial | `TransactionsEntity` includes CPT codes; `EncountersEntity` has procedure-related fields | Procedures likely captured via billing transactions and encounters, no dedicated entity |
| Clinical notes / documents | ✅ Covered | Documentation states "Documents and Clinical data will be included in the zip file" with `.meta` files; `InternalNotesEntity` (6 fields), `NotesEntity` (2 fields) | Documents included as files; notes entities are thin but supplementary |
| Care plans / goals | ⚠️ Partial | No dedicated care plan entity; product has CCM module with care plans | Product offers Chronic Care Management with care plan building; no export entity for this |
| Orders / referrals | ✅ Covered | `EmrPatientOrderPanelEntity` (60 fields), `EmrRefToProvidersEntity` (18 fields) | Orders and referrals both have dedicated entities |
| Insurance / coverage | ✅ Covered | `InsuranceDataEntity` (36 fields, 100% described), `InsuranceDataAuthorizationsEntity` (9 fields, 100% described), `GuarantorEntity` (24 fields) | Strong — 69 fields across 3 entities with good descriptions |
| Claims / billing | ✅ Covered | `TransactionsEntity` (53 fields) — CPT codes, diagnoses, amounts, insurance payments, adjustments | Genuine billing data, not just clinical summaries |
| Payments | ✅ Covered | `PaymentEntity` (12 fields) | Dedicated payment entity |
| Consents / directives | ❌ Not covered | No consent or advance directive entity | Minor gap — product may store these as scanned documents |
| Patient communications / portal messages | ✅ Covered | `MessagesEntity` (21 fields) | Present with 21 fields |
| Scheduling | ✅ Covered | `AppointmentsEntity` (25 fields) | Present with 25 fields |
| Screenings / assessments | ✅ Covered | `ScreeningEntity` (23 fields) | Health status assessments included |
| Medical devices | ✅ Covered | `EmrImplantableDeviceEntity` (20 fields) | Dedicated device entity |
| Cases (workers' comp) | ✅ Covered | `CasesEntity` (41 fields, 100% described) | Thorough case management data |
| Custom forms | ✅ Covered | `PatientMedicalFormEntity` (11 fields), `PatientCustomFieldsEntity` (3 fields) | Custom/specialty-specific data captured |

**Coverage: 17 of 19 applicable domains covered; 2 partial; 1 not covered (consents)**

## 6. Documentation Quality

**Strengths:**
- The Javadoc-based data dictionary is machine-readable and structured: every field has a name and Java type, making it parseable.
- The hierarchical data model is clear — PatientEntity as root with nested entity lists makes the relationships explicit.
- Four key entities (PatientEntity, CasesEntity, InsuranceDataEntity, InsuranceDataAuthorizationsEntity) have 100% field descriptions — these are the best-documented areas.
- CBOR format choice, while unusual, is well-specified (RFC 8949) and has open-source tooling.

**Weaknesses:**
- **77.1% of fields lack descriptions.** Most clinical entities (medications, labs, encounters, allergies, vitals, immunizations) have field names only — a developer must guess what `dispensed`, `adjDate`, `ackStatus`, or `holdStatus` mean.
- **No value sets or code systems documented.** Fields like `status`, `type`, `tobaccoRecode` are undocumented strings/integers with no enumeration of valid values.
- **No sample data.** No example CBOR output, no example patient record, nothing to validate parsing against.
- **No foreign key documentation.** Relationships are only visible through `List<*Entity>` type annotations — no explanation of which IDs link to what.
- **No export workflow documentation.** How to initiate an export, who can do it, what parameters are available, what the ZIP file looks like — none of this is documented.
- **No schema file.** The Javadoc is the only schema reference; there's no JSON Schema, CBOR schema, or formal specification.

**Could a developer build an import?** With significant effort, yes. The entity structure and field types are clear enough to deserialize CBOR into objects. But without descriptions on 77% of fields, without value sets, and without sample data, interpreting the data semantically would require substantial reverse engineering.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains that Veracity stores. The 31 entities span demographics, clinical data (problems, medications, allergies, vitals, labs, immunizations, devices), billing (transactions with CPT codes, payments), insurance (coverage, authorizations, guarantors), case management, referrals, scheduling, messages, screenings, and custom forms. Critically, the export includes billing/transaction data (TransactionsEntity with 53 fields including `cpt`, `amount`, `insurancePaid`, `adjustmentAmount`) and insurance data — these are domains that repackaged clinical exchanges never include. The hierarchical structure nesting billing transactions under encounters, and insurance data under cases, reflects the product's actual data model. The inclusion of entities like `PatientCustomFieldsEntity`, `PatientMedicalFormEntity`, and `ScreeningEntity` shows coverage of specialty-specific and custom data beyond standard clinical summaries. The only notable gap is care plan data (the product has a CCM module but no corresponding export entity) and consents/directives.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange. Key evidence:
1. **CBOR format** — this is not C-CDA, FHIR, or any standard clinical exchange format. It's a custom binary serialization of the vendor's internal Java entity model.
2. **Native data model** — the 31 entities are Java classes from the vendor's codebase (Javadoc-generated documentation), not a projection into a standard.
3. **Billing and insurance data** — TransactionsEntity, PaymentEntity, InsuranceDataEntity, and GuarantorEntity go far beyond what any (g)(10) FHIR API or C-CDA export would include.
4. **Non-USCDI domains** — scheduling (AppointmentsEntity), messages (MessagesEntity), internal notes (InternalNotesEntity), tasks (TasksEntity), cases (CasesEntity), custom fields, and medical forms are all present — none of these appear in USCDI or standard clinical exchanges.

### Key Findings

1. **Genuinely broad export with billing data.** The 31 entities and 715 fields cover clinical, billing, insurance, scheduling, communications, and case management — this is not a relabeled clinical summary. TransactionsEntity (53 fields with CPT codes, charges, and payment details) and InsuranceDataEntity (36 fully described fields) demonstrate real billing coverage.

2. **Severely uneven documentation quality.** Only 164 of 715 fields (22.9%) have descriptions. Four entities are fully described (PatientEntity, CasesEntity, InsuranceDataEntity, InsuranceDataAuthorizationsEntity); the other 27 entities have almost no descriptions. This means most clinical data (medications, labs, encounters) requires guesswork to interpret.

3. **Unusual CBOR format creates adoption friction.** CBOR is a valid, well-specified format, but it's atypical for healthcare data exchange. Patients and downstream systems expecting CSV, JSON, or FHIR will need additional tooling to decode the export.

4. **No sample data or workflow documentation.** The documentation describes what the data *looks like* structurally but provides no example output, no instructions for initiating an export, and no value set definitions for coded fields.

5. **Hierarchical patient-centric model is well-designed.** The nesting of entities under PatientEntity (with billing under encounters, insurance under cases) reflects genuine EHR data architecture rather than a flat clinical dump.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CBOR (RFC 8949, binary) in ZIP with document files
Entities:        31
Fields:          715
Descriptions:    22.9% (164 of 715 fields)
Sample data:     No
Bulk export:     Unclear
Domains covered: 17 of 19 applicable domains (2 partial, 1 not covered)
```

### Bottom Line

AllegianceMD built a genuine purpose-built EHI export that covers the breadth of what Veracity stores — clinical, billing, insurance, scheduling, communications, and case management data across 31 entities and 715 fields. The biggest weakness is documentation quality: only 23% of fields have descriptions, there's no sample data, and no value set definitions, making the export structurally complete but difficult to interpret without reverse engineering. A patient would get a comprehensive data file; a developer trying to import it would struggle with the undocumented 77% of fields and the unusual CBOR format.
