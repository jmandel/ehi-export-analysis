# EHI Export Analysis: AllegianceMD Software, Inc.

**Product**: Veracity v9.1
**Analysis date**: 2026-02-15
**CHPL ID**: 10794 (15.02.05.2672.ALLE.01.01.1.220117)

## 1. Product Context

AllegianceMD Veracity is a cloud-based, all-in-one EHR/practice management/billing platform targeting small-to-mid-sized ambulatory practices. It is sold as a single integrated system — not modular — encompassing:

- **Clinical EHR**: charting with specialty templates (50+ specialties), problem lists, medication lists, allergy lists, vitals, clinical decision support, CPOE
- **E-prescribing**: including controlled substances (EPCS), PMP integration
- **Lab/imaging**: ordering, results retrieval, HL7 interfaces
- **Practice management**: scheduling, appointment reminders, case management (workers' comp), document scanning/faxing
- **Billing/revenue cycle**: charge capture, claim creation/scrubbing/submission, clearinghouse, eligibility verification, ERA posting, denial management, collections, credit card processing, patient statements
- **Patient portal**: demographics, secure messaging, refill requests, bill payment, self-service kiosk
- **Telemedicine**: integrated video consultations
- **Quality reporting**: MACRA/MIPS, clinical quality measures
- **Chronic care management**: CCM enrollment, care plans

The product is certified for (b)(10) EHI export along with a broad ambulatory certification profile including (a)(1)–(a)(5), (b)(1)–(b)(3), (e)(1), (e)(3), (g)(7), (g)(10), (c)(1)–(c)(3), (f)(1), (f)(5).

**Baseline for completeness**: A genuine "all EHI" export should cover clinical data (encounters, problems, meds, allergies, vitals, labs, notes, immunizations), billing data (transactions, claims, payments, insurance), and administrative patient data (demographics, insurance, guarantor, messages, documents).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-documentation-page.html` (37 KB) | Main WordPress page describing CBOR export format. Contains 3 paragraphs of content. | Low — only states format and links to data structure |
| `ehi-export-documentation-page.png` | Screenshot of above page confirming content | Confirmatory |
| `ehi-export-index.html` (11 KB) | Javadoc-generated index listing all 31 entity classes | Medium — provides entity inventory |
| `ehi-export-data-structure-index.png` | Screenshot of index page confirming 31 entities | Confirmatory |
| `entity-data-dictionary.json` (69 KB) | Structured extraction of all 31 entities and 715 fields from Javadoc pages | **High — primary data source for analysis** |
| 31 individual `*Entity.html` files | Javadoc detail pages for each entity (2.7–36 KB each) | High — field-level documentation |
| `ehi-export-stylesheet.css` (31 KB) | Javadoc CSS | Not informative |

**Most informative**: The `entity-data-dictionary.json` and individual entity HTML pages provided the field-level detail needed for assessment. **Least informative**: The main documentation page (`ehi-export-documentation-page.html`) contains only 3 sentences of substantive content.

All field counts from the JSON extraction were independently verified against the 31 HTML source files using a custom parser (`analysis/verify_html_v2.py`). All 715 fields matched exactly.

## 3. Export Mechanics

- **Format**: CBOR (Concise Binary Object Representation, RFC 8949) — a binary serialization format semantically equivalent to JSON. This is unusual for healthcare; CBOR is more commonly used in IoT/constrained environments.
- **Delivery**: ZIP file containing CBOR-encoded data objects, documents/clinical data files, and `.meta` files describing each document.
- **Mechanism**: Not documented. The documentation page provides no instructions for how to request or initiate an export. No UI screenshots, API endpoints, or workflow description.
- **Single-patient vs bulk**: Not documented. The data model is patient-centric (single root `PatientEntity`), suggesting single-patient export. No evidence of bulk export capability.
- **Access constraints/fees**: Not documented in the EHI export materials. The vendor's mandatory disclosures document is referenced at a separate URL but was not part of the EHI export documentation.
- **Tools**: The vendor points to https://cbor.io/impls.html for open-source CBOR decoding tools.

## 4. Export Content: What's In It

### Data Dictionary Overview

The export is documented through a **Javadoc site** generated from Java entity classes on **2023-10-25**. It defines **31 entity types** with a total of **715 fields**.

- **164 of 715 fields (22.9%) have descriptions** — brief plain-English explanations
- **551 fields (77.1%) have only a name and Java type** — no description
- **4 entities have 100% description coverage**: PatientEntity (71 fields), CasesEntity (41 fields), InsuranceDataEntity (36 fields), InsuranceDataAuthorizationsEntity (9 fields) — together accounting for 157 of the 164 described fields
- **21 entities have 0% description coverage** — field names and types only
- **6 entities have partial coverage** (1–2 fields described each): EmrMedicationEntity, EmrPatientOrderPanelEntity, EncountersEntity, ScreeningEntity, MessagesEntity, EmrRefToProvidersEntity

### Data Architecture

The export uses a **patient-centric hierarchical model**. `PatientEntity` is the root, containing 51 scalar fields (demographics) plus 20 `List<>` fields embedding related entities. Sub-entities also nest further: `EncountersEntity` contains `List<EncountersDiagEntity>` and `List<TransactionsEntity>`; `CasesEntity` contains `List<InsuranceDataEntity>`; `InsuranceDataEntity` contains `List<InsuranceDataAuthorizationsEntity>`.

Four entities are not directly embedded in `PatientEntity` but are referenced from sub-entities or appear as standalone lookups: `GuarantorEntity` (24 fields), `PatientCareTeamEntity` (19 fields), `EmrEncounterEntity` (2 fields), `EmrVitalsCategoryEntity` (11 fields).

Field types are Java types: String (427), Date (111), Boolean (84), Double (36), Integer (21), Short/short (8), Long (1), byte[] (1).

### Vendor's Entity Inventory

| Entity | Fields | Described | Types | Domain |
|---|---|---|---|---|
| PatientEntity | 71 | 71 (100%) | yes | Demographics |
| EmrMedicationEntity | 62 | 1 (1.6%) | yes | Medications |
| EmrPatientOrderPanelEntity | 60 | 1 (1.7%) | yes | Orders/Labs |
| TransactionsEntity | 53 | 0 (0%) | yes | Billing |
| EncountersEntity | 47 | 2 (4.3%) | yes | Encounters/Billing |
| EmrInjectionEntity | 43 | 0 (0%) | yes | Immunizations |
| CasesEntity | 41 | 41 (100%) | yes | Cases (Workers' Comp) |
| InsuranceDataEntity | 36 | 36 (100%) | yes | Insurance |
| AppointmentsEntity | 25 | 0 (0%) | yes | Scheduling |
| GuarantorEntity | 24 | 0 (0%) | yes | Demographics |
| ScreeningEntity | 23 | 1 (4.3%) | yes | Screenings |
| MessagesEntity | 21 | 1 (4.8%) | yes | Communications |
| EmrImplantableDeviceEntity | 20 | 0 (0%) | yes | Devices |
| EmrPatientOrderItemEntity | 20 | 0 (0%) | yes | Orders/Labs |
| PatientCareTeamEntity | 19 | 0 (0%) | yes | Care Team |
| EmrAllergyEntity | 18 | 0 (0%) | yes | Allergies |
| EmrRefToProvidersEntity | 18 | 1 (5.6%) | yes | Referrals |
| TasksEntity | 18 | 0 (0%) | yes | Tasks |
| EmrProblemEntity | 16 | 0 (0%) | yes | Problems |
| PaymentEntity | 12 | 0 (0%) | yes | Payments |
| EmrVitalsCategoryEntity | 11 | 0 (0%) | yes | Vitals |
| PatientMedicalFormEntity | 11 | 0 (0%) | yes | Medical Forms |
| PatientPharmacyEntity | 10 | 0 (0%) | yes | Pharmacy |
| InsuranceDataAuthorizationsEntity | 9 | 9 (100%) | yes | Insurance |
| EmrVitalsEntity | 7 | 0 (0%) | yes | Vitals |
| InternalNotesEntity | 6 | 0 (0%) | yes | Internal Notes |
| TaskCommentsEntity | 4 | 0 (0%) | yes | Tasks |
| PatientCustomFieldsEntity | 3 | 0 (0%) | yes | Custom Fields |
| EncountersDiagEntity | 3 | 0 (0%) | yes | Diagnoses |
| NotesEntity | 2 | 0 (0%) | yes | Notes |
| EmrEncounterEntity | 2 | 0 (0%) | yes | Encounters |
| **TOTAL** | **715** | **164 (22.9%)** | — | — |

Full inventory with all field details saved to `analysis/full-entity-inventory.json`.

### Notable Entity Details

**TransactionsEntity** (53 fields, 0 described): Contains CPT code (`cpt`), up to 4 diagnosis codes (`diag1`–`diag4`), diagnosis pointer, charge amount, balance, modifiers, place of service, type of service, units, NDC data, and detailed insurance payment/adjustment tracking for 3 payers (`ins1Paid`/`ins1Adj`/`ins1Ded`/`ins1Copay`/`ins1Coins`/`ins1Balance`/`ins1Status` × 3), plus patient responsibility/payment/adjustment fields. This is a genuinely detailed billing line-item model — not a summary.

**EncountersEntity** (47 fields, 2 described): Contains encounter date, providers (assigned/billing), facility, charges, balance, diagnosis linkage (`List<EncountersDiagEntity>`), transaction linkage (`List<TransactionsEntity>`), hospitalization dates, prior auth, referrer, workers' comp fields (`employmentRelated`, `accidentState`, `autoAccidentRelated`), and claim-related fields (`resubmissionNumber`, `frequencyCode`, `reportTypeCode`). The description on the 2 described fields labels diagnoses as "Hold the diagnosis data" and transactions as "Hold CPT data."

**EmrProblemEntity** (16 fields, 0 described): Includes ICD-10, ICD-9, and SNOMED codes with descriptions, plus status, severity, dates, and notes. This is a well-structured problem list entity despite lacking descriptions.

**EmrInjectionEntity** (43 fields, 0 described): Contains CVX codes, CPT codes, NDC, manufacturer/lot/expiration, VIS dates, VFC status, route/site, administration details, and refusal tracking. This is comprehensive immunization data.

**EmrMedicationEntity** (62 fields, 1 described): The largest clinical entity. Field names suggest e-prescribing detail (fields likely include medication name, dosage, route, frequency, prescriber, pharmacy, refill info, etc.).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export spans clinical, billing, insurance, and administrative domains across 31 entities. The coverage is organized around a patient-centric model with these natural groupings:

**Richest domains (by field count):**
- Demographics/Patient data: 98 fields across 3 entities (PatientEntity, GuarantorEntity, PatientCustomFieldsEntity). PatientEntity alone has 71 fully-described fields covering name, DOB, SSN, address, phone, email, race, ethnicity, language, gender identity, sexual orientation, smoking status, employment, emergency contact, and collection/financial class.
- Orders/Labs: 80 fields across 2 entities (EmrPatientOrderPanelEntity with 60 fields, EmrPatientOrderItemEntity with 20 fields). Includes accession numbers, result values, abnormal flags, LOINC codes.
- Billing: 65 fields across 2 entities (TransactionsEntity with 53 fields, PaymentEntity with 12 fields). Deep CPT/diagnosis/payment tracking.
- Medications: 62 fields in 1 entity. Extensive e-prescribing data.
- Encounters: 52 fields across 3 entities. Combines clinical and billing encounter data.
- Insurance: 45 fields across 2 entities (both 100% described). Coverage details plus pre-authorizations.
- Immunizations: 43 fields in 1 entity. CVX, NDC, VIS, VFC, manufacturer, lot tracking.
- Cases: 41 fields in 1 entity (100% described). Workers' comp and case management.

**Thinnest domains:**
- Vitals: 18 fields across 2 entities — `EmrVitalsEntity` has only 7 fields (id, value, date-like fields presumably), `EmrVitalsCategoryEntity` has 11 fields defining vital sign types (LOINC codes, units, equations).
- Notes: 8 fields across 2 entities — `InternalNotesEntity` (6 fields: body, subject, author, timestamp, folder, active) and `NotesEntity` (2 fields: body, type). Very thin.
- Custom fields: 3 fields — `PatientCustomFieldsEntity` — presumably key/value pairs.
- Clinical encounter content: `EmrEncounterEntity` has only 2 fields (id, date). Clinical note *content* (the actual chart note text) does not appear to have a dedicated entity. The `EncountersEntity.note` field (String) may contain some note text, and the documentation page states "Documents and Clinical data will be included in the zip file," suggesting chart notes may be exported as document files rather than structured data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PatientEntity` (71 fields, all described), `GuarantorEntity` (24 fields), `PatientCustomFieldsEntity` (3 fields) | Thorough — includes name, DOB, SSN, address, phone, email, race, ethnicity, language, gender identity, sexual orientation, smoking status, emergency contacts |
| Encounters / visits | ✅ Covered | `EncountersEntity` (47 fields), `EmrEncounterEntity` (2 fields), `EncountersDiagEntity` (3 fields) | Encounter structure is present with dates, providers, diagnoses, and billing linkage. Clinical encounter content (chart notes) may rely on document files |
| Problems / conditions | ✅ Covered | `EmrProblemEntity` (16 fields) | ICD-10, ICD-9, SNOMED codes with descriptions, status, severity, dates |
| Medications / prescriptions | ✅ Covered | `EmrMedicationEntity` (62 fields) | Extensive — largest clinical entity, e-prescribing detail |
| Allergies | ✅ Covered | `EmrAllergyEntity` (18 fields) | Reactant name/type, RXCUI, symptom flags (anemia, asthma, hives, nausea, rash, shock), dates, status |
| Immunizations | ✅ Covered | `EmrInjectionEntity` (43 fields) | Comprehensive — CVX, CPT, NDC, manufacturer, lot, VIS, VFC, route, site, refusal tracking |
| Vitals | ⚠️ Partial | `EmrVitalsEntity` (7 fields), `EmrVitalsCategoryEntity` (11 fields) | Vitals values exist but with only 7 fields per measurement; category entity defines vital types. No descriptions to verify completeness |
| Lab results | ✅ Covered | `EmrPatientOrderPanelEntity` (60 fields), `EmrPatientOrderItemEntity` (20 fields) | Order panels with results, accession numbers, completion status; items with individual test details |
| Imaging / diagnostic reports | ⚠️ Partial | Same order entities likely cover imaging orders; `EncountersEntity.isLab` Boolean suggests lab vs imaging distinction | No dedicated imaging entity; imaging results may be included as documents in the ZIP |
| Procedures | ⚠️ Partial | `TransactionsEntity.cpt` captures procedure codes with modifiers; no dedicated procedure entity | CPT codes are billing artifacts; no clinical procedure documentation entity (operative notes, procedure details) |
| Clinical notes / documents | ⚠️ Partial | `EncountersEntity.note` (String), `InternalNotesEntity` (6 fields), `NotesEntity` (2 fields). Documentation page states "Documents and Clinical data will be included in the zip file" with `.meta` files | No structured chart note entity. Clinical note content likely exported as document files in the ZIP. The `.meta` file format is not documented |
| Care plans / goals | ❌ Not covered | No care plan or goal entity | Product offers CCM care plans (see Section 1); this is a gap |
| Orders / referrals | ✅ Covered | `EmrPatientOrderPanelEntity` (60 fields), `EmrPatientOrderItemEntity` (20 fields), `EmrRefToProvidersEntity` (18 fields) | Orders and referrals both represented |
| Insurance / coverage | ✅ Covered | `InsuranceDataEntity` (36 fields, all described), `InsuranceDataAuthorizationsEntity` (9 fields, all described) | Excellent — both entities fully documented with descriptions |
| Claims / billing | ✅ Covered | `TransactionsEntity` (53 fields), `EncountersEntity` (47 fields with claim-related fields) | Detailed line-item billing with multi-payer payment tracking. Claim lifecycle (submission/rejection/denial status) unclear from field names alone |
| Payments | ✅ Covered | `PaymentEntity` (12 fields) | Payment amount, type, check number, posting date, void tracking |
| Consents / directives | ❌ Not covered | No consent or advance directive entity | If stored by product, this is a gap |
| Patient communications | ✅ Covered | `MessagesEntity` (21 fields) | Includes body, subject, sender/recipient, folder, urgent flag, attachment info, patient read status |
| Screening assessments | ✅ Covered | `ScreeningEntity` (23 fields) | SNOMED/LOINC coded screenings with results, status, reason codes |
| Medical forms | ✅ Covered | `PatientMedicalFormEntity` (11 fields) | Patient medical history forms with results |
| Implantable devices | ✅ Covered | `EmrImplantableDeviceEntity` (20 fields) | UDI/device tracking |

## 6. Documentation Quality

**Strengths:**
- The Javadoc format provides a navigable, linked entity hierarchy — each entity page shows field names and Java types
- The 4 fully-documented entities (PatientEntity, CasesEntity, InsuranceDataEntity, InsuranceDataAuthorizationsEntity) demonstrate that good field-level descriptions are possible; descriptions are brief but clear (e.g., "Patient address active date," "Case accident state," "Patient allergy list")
- Data types are consistently documented using Java types
- Entity relationships are expressed through `List<>` type annotations, making the data architecture clear
- The data model is a genuine serialization of the application's internal Java entity classes (generated by javadoc/ClassWriterImpl), meaning the export mirrors the actual data model

**Weaknesses:**
- **77% of fields lack descriptions.** Only 164 of 715 fields have any description. For the 27 under-documented entities, a developer must guess field meanings from camelCase names alone. Many names are self-explanatory (`firstName`, `DOB`, `amount`) but others are cryptic (`pqrsQualDataCode`, `hcfa21_4`, `modifier1`, `pos`, `tos`)
- **No value sets or code system documentation.** Fields like `status`, `type`, `action`, `category` are String types with no enumeration of allowed values. Diagnosis fields (`diag1`–`diag4`) don't specify ICD-10 vs SNOMED. The `EmrProblemEntity` has both `icd10Code` and `snomedCode` which clarifies that entity, but most coded fields are ambiguous
- **No sample data.** No example CBOR files, no sample export output, no test data
- **No user guide.** No instructions for how to request, generate, or receive an export. No UI screenshots, no API documentation
- **No document metadata schema.** The main page mentions `.meta` files for documents but doesn't document their structure
- **No machine-readable schema.** The JSON data dictionary was extracted by the prior agent; the vendor provides only HTML. No JSON Schema, no OpenAPI spec, no CBOR schema
- **Static snapshot.** Generated 2023-10-25 with no version history or changelog

**Could a developer build an import?** Partially. The entity hierarchy and field types are clear enough to parse CBOR data into objects. But understanding what 77% of fields *mean*, what valid values are, and how to map them to standard terminologies would require significant reverse-engineering or vendor consultation.

## 7. Overall Assessment

### Classification

**Partial native export.** AllegianceMD exports their native Java entity model — 31 entities covering clinical, billing, insurance, and administrative data. This is genuinely a (b)(10) approach, not a repackaged FHIR or C-CDA export. However, documentation quality is inconsistent (only 23% of fields described), and there are notable coverage gaps in clinical notes (no structured chart note entity), care plans, and potentially documents (undocumented `.meta` format).

### Key Findings

1. **Genuinely (b)(10)-oriented approach**: The export serializes the vendor's internal Java data model (31 entities, 715 fields) in CBOR format, covering domains well beyond USCDI/FHIR — including billing transactions with multi-payer payment tracking, insurance authorizations, workers' comp cases, screenings, and internal staff notes. This is not a clinical summary repackaged.

2. **Deep billing coverage**: `TransactionsEntity` (53 fields) provides line-item CPT codes, diagnosis pointers, modifiers, and detailed payment/adjustment tracking across 3 insurance payers plus patient responsibility — a level of billing detail rarely seen in EHI exports.

3. **Severe documentation gap**: Only 4 of 31 entities (13%) are fully documented. The remaining 27 entities provide field names and types but no descriptions, no value sets, and no sample data. The 4 well-documented entities (PatientEntity, CasesEntity, InsuranceDataEntity, InsuranceDataAuthorizationsEntity) account for 96% of all field descriptions (157 of 164).

4. **Clinical notes structure unclear**: There is no dedicated chart note entity. `EmrEncounterEntity` has only 2 fields (id, date). Clinical note content may be exported as document files in the ZIP (per the documentation page), but the `.meta` file format describing these documents is not documented.

5. **Unusual export format**: CBOR is well-specified (RFC 8949) with broad language support, but is unprecedented in healthcare data exchange. It adds a decoding step with no practical advantage over JSON for this use case (the vendor acknowledges CBOR is "semantically equivalent" to JSON but claims it avoids "formatting issues").

### Summary Stats

```
Classification:  Partial native export
Export format:   CBOR (RFC 8949), delivered as ZIP
Model type:      Native database (Java entity serialization)
Entities:        31
Fields:          715
Descriptions:    22.9% (164 of 715 fields)
Sample data:     No
Bulk export:     Unclear
Domains covered: 13 of 17 applicable domains (✅ or ⚠️)
```

### Bottom Line

AllegianceMD took the right architectural approach — exporting their native data model rather than repackaging C-CDA or FHIR — and achieves genuinely broad domain coverage including billing, insurance, and specialty data that most vendors omit. However, the documentation is severely uneven: 4 entities are fully described while 27 have no field descriptions at all, and the unusual CBOR format combined with no sample data, no user guide, and no value set documentation would make it very difficult for a patient or developer to actually *use* this export without vendor assistance. The single biggest gap is the absence of documentation for how clinical notes and documents are exported (the `.meta` file format).
