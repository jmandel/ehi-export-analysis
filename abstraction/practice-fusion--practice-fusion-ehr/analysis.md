# EHI Export Analysis: Practice Fusion

**Product**: Practice Fusion EHR v3.7
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2924.Prac.37.01.1.240826 (CHPL #11507)

## 1. Product Context

Practice Fusion is a cloud-based ambulatory EHR serving ~30,000 small/independent medical practices, over 112,000 healthcare professionals, and 5 million patients monthly. Owned by Veradigm (formerly Allscripts), it is the #1 cloud-based ambulatory EHR in the US by market share among solo/small practices (12% of the 1–3 clinician segment).

The product supports 53+ medical specialties with 130+ customizable clinical templates. It is offered in four tiers: EHR with managed billing services (white-glove RCM), EHR with billing software, standalone EHR, and standalone ePrescribe.

**Key data domains the export should cover:**
- **Clinical**: encounters (SOAP notes), problem lists/diagnoses, medications, allergies, immunizations, vitals, labs (orders and results), procedures, clinical worksheets (custom assessments), family history, advance directives, care plans/goals, patient education, smoking status, healthcare devices
- **Billing/Insurance**: superbills (the clinical-to-billing handoff), insurance policies, eligibility, guarantors, procedures with billing codes
- **Prescriptions**: e-prescribing including EPCS, prescription transactions, drug alert overrides, pharmacy management
- **Lab integration**: orders and results from 500+ lab/imaging centers
- **Patient engagement**: portal messages (via FollowMyHealth), documents, questionnaires
- **Referrals**: referral records and recipients
- **Scheduling**: appointments

Note: Full claims lifecycle processing (submissions, denials, payments, A/R) occurs outside Practice Fusion — either in its managed billing service or external billing software. The EHR captures the superbill layer (clinical-to-billing handoff), not downstream claims.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `downloads/v9-data-dictionary.json` | Extracted structured data dictionary: 85 tables, 1,165 fields with names, types, descriptions. Parsed from all 85 HTML subpages. | **Primary source** — machine-readable, comprehensive |
| `downloads/v9-index.html` (48,342 bytes) | v9 index page listing all 85 TSV files organized in 8 categories | **Key** — provides category structure and export format description |
| `downloads/v9-pages/` (86 HTML files, 3.0 MB total) | Individual data dictionary pages, one per TSV file, each with a field-level table | **Reference** — used to verify JSON accuracy |
| `downloads/ehi-export-documentation-main.html` (33,892 bytes) | Landing page listing 9 versioned releases (v1–v9, Nov 2023–Jan 2026) | **Moderate** — version history and publication dates |
| `downloads/screenshot-v9-index.png` (1.2 MB) | Full-page screenshot of v9 index | **Supplemental** — visual confirmation of category layout |
| `downloads/screenshot-v9-patient-demographics.png` (671 KB) | Screenshot of patient-demographics field table | **Supplemental** — verified 50 fields |
| `downloads/screenshot-v9-patient-superbills.png` (951 KB) | Screenshot of patient-superbills field table | **Supplemental** — verified 70 fields |
| `downloads/screenshot-main-page.png`, `screenshot-main-page-full.png` | Landing page screenshots | **Low** — navigation context only |

**Verification notes**: I independently parsed several HTML pages (`patient-demographics.html`, `patient-superbills.html`, `patient-drug-alert-overrides.html`) and confirmed the field counts match the extracted JSON: 50, 70, and 13 fields respectively. The JSON data dictionary accurately reflects the HTML source.

## 3. Export Mechanics

- **Format**: Tab-separated values (TSV) — one file per data entity, with header rows
- **Encoding**: Not explicitly documented (presumed UTF-8)
- **Mechanism**: Manual export from EHR UI. The v9 index states: *"EHI Export functionality allows health systems to do a manual export of health data for a single patient or entire patient population in a practice."*
- **Scope**: Supports both single-patient and bulk (entire practice population) export
- **Relationship model**: Tables linked via GUID-based foreign keys (e.g., `PatientPracticeGuid` appears in 76 of 85 tables; `EncounterGuid` links 14 tables)
- **Access constraints/fees**: Not documented in the export documentation itself
- **Export instructions**: Not provided — the documentation describes output format only, not how to trigger the export

This is a genuine database-model export, not a repackaging of the FHIR API or C-CDA. The TSV structure with GUID foreign keys reflects the underlying relational data model.

## 4. Export Content: What's In It

### Summary statistics

| Metric | Value |
|---|---|
| Total entities (TSV files) | 85 |
| Total fields | 1,165 |
| Fields with descriptions | 1,164 (99.9%) |
| Fields with data types | 1,164 (99.9%) |
| Fields without descriptions | 1 (`etc.` — an HTML parsing artifact in `patient-drug-alert-overrides.tsv`) |
| Distinct data types | 15 (including nullable variants) |
| Categories | 8 |
| Table-level descriptions | 0 (no entity-level descriptions; only field-level) |

The single "missing" description is actually a parsing artifact: in the `patient-drug-alert-overrides.tsv` HTML page, the InteractionReason field's example values list ("'Not clinically important', 'Drug could be life-saving for patient', etc.") caused the word "etc." to be extracted as a spurious 13th field. The effective description coverage is 100%.

### Data types used

| Type | Count | Notes |
|---|---|---|
| String | 591 | Includes coded/enumerated values without documented value sets |
| Guid | 203 | Non-nullable foreign/primary keys |
| Guid? | 115 | Nullable foreign keys |
| DateTime | 77 | Non-nullable timestamps |
| DateTime? | 60 | Nullable timestamps |
| Boolean | 46 | Non-nullable flags |
| DateField | 31 | Date-only fields (no time component) |
| Decimal? | 9 | Nullable monetary/numeric values |
| Boolean? | 7 | Nullable flags |
| Int32 | 7 | Non-nullable integers |
| DateTimeOffset? | 6 | Nullable timestamps with timezone |
| Int32? | 6 | Nullable integers |
| Int64? | 2 | Nullable large integers |
| Decimal | 2 | Non-nullable decimal values |
| Double? | 2 | Nullable floating-point values |

### Vendor's own content organization

The data dictionary is organized into 8 categories. Full inventory saved to `analysis/full-entity-inventory.json`.

| Category | Tables | Fields | Described | % Described |
|---|---|---|---|---|
| Demographics | 10 | 143 | 143 | 100.0% |
| Patient (documents/questionnaires) | 2 | 27 | 27 | 100.0% |
| Clinical | 30 | 346 | 346 | 100.0% |
| Billing and insurance | 12 | 286 | 286 | 100.0% |
| Medications and prescriptions | 11 | 125 | 124 | 99.2% |
| Labs | 15 | 187 | 187 | 100.0% |
| Referrals | 2 | 24 | 24 | 100.0% |
| Messaging | 3 | 27 | 27 | 100.0% |
| **Total** | **85** | **1,165** | **1,164** | **99.9%** |

### Representative entities (20 largest by field count)

| Entity | Fields | Category |
|---|---|---|
| patient-superbills.tsv | 70 | Billing and insurance |
| patient-insurances.tsv | 65 | Billing and insurance |
| superbill-insurances.tsv | 51 | Billing and insurance |
| patient-demographics.tsv | 50 | Demographics |
| patient-prescriptions.tsv | 38 | Medications and prescriptions |
| patient-encounter-events.tsv | 31 | Clinical |
| patient-healthcare-devices.tsv | 31 | Clinical |
| patient-immunizations.tsv | 31 | Clinical |
| patient-lab-orders.tsv | 25 | Labs |
| patient-guarantor.tsv | 22 | Billing and insurance |
| patient-lab-result-tests-observations.tsv | 22 | Labs |
| patient-lab-results.tsv | 21 | Labs |
| patient-allergy.tsv | 20 | Clinical |
| patient-encounters.tsv | 20 | Clinical |
| patient-lab-order-item-specimens.tsv | 20 | Labs |
| patient-medications.tsv | 20 | Medications and prescriptions |
| patient-encounter-procedures.tsv | 18 | Clinical |
| superbill-procedures.tsv | 17 | Billing and insurance |
| patient-gender-identity-sexual-orientation.tsv | 17 | Demographics |
| patient-lab-order-items.tsv | 16 | Labs |

### Notable content details

**Encounter documentation is rich**: `patient-encounters.tsv` (20 fields) captures full SOAP notes (Subjective, Objective, Assessment, Plan), chief complaint, chart note type, signing provider/date, virtual visit flag, and a psychotherapy note flag. Related tables capture encounter-level diagnoses, medications, events, observations, procedures, addendums, and documents — 8 encounter-linked tables totaling 128 fields.

**Billing data is superbill-centric**: The largest single table is `patient-superbills.tsv` (70 fields) with rendering/supervising/referring provider details, facility info, POS codes, authorization numbers, accident details, and onset dates. Supporting tables cover linked diagnoses (ICD-10), procedures (CPT/HCPCS with NDC), procedure modifiers, and insurance assignments. This represents the clinical-to-billing handoff — not full claims lifecycle.

**Insurance is deeply modeled**: `patient-insurances.tsv` (65 fields) includes payer details, subscriber info, copay amounts, attorney details (workers' comp/personal injury), employer info, and secondary subscriber data. `superbill-insurances.tsv` (51 fields) captures insurance assignments per superbill. `patient-insurance-eligibilities.tsv` (13 fields) tracks verification results with deductible, copay, and coinsurance amounts.

**Labs are exceptionally granular**: 15 tables with 187 fields spanning orders, order items, item diagnoses, item specimens, item answers, order documents, results, result tests/observations, observation diagnoses, observation notes, result documents, result item notes, and specimen data. This is among the most detailed lab modeling in any EHI export.

**Clinical worksheets capture custom assessments**: `patient-clinical-worksheet-summaries.tsv` (9 fields) and `patient-clinical-worksheet-detail.tsv` (7 fields) export question-answer pairs with LOINC codes and computed scores — this covers specialty-specific assessments (PHQ-9, GAD-7, etc.).

**Document metadata but not content**: `patient-documents.tsv` (12 fields) tracks document name, type, status, file extension, file size, and a `DocumentStorageGuid` described as "Filename of the corresponding binary content." Whether the actual binary files are included in the export is not documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Demographics (10 tables, 143 fields)**: Comprehensive patient identity including demographics (50 fields), race, ethnicity, gender identity/sexual orientation (17 fields), tribal affiliation, occupation/industry, financial resources, communication settings, contacts, and appointments.

**Clinical (30 tables, 346 fields)**: The largest category. Covers encounters with SOAP documentation, diagnoses (problem list and encounter-level), allergies with reactions, conditions, clinical worksheets (custom assessments with LOINC-coded Q&A), family history with diagnoses, immunizations with registry data, goals, health concerns, healthcare devices (UDI), advance directives, smoking status, risk scores, pinned notes, patient education, care team, provider/user profiles, and facilities.

**Billing and insurance (12 tables, 286 fields)**: The second-largest category by field count. Superbills (70 fields) with linked diagnoses, procedures (with CPT/HCPCS codes, NDC, billing amounts), procedure modifiers, and insurance assignments. Insurance policies (65 fields), eligibility verification (13 fields), guarantors (22 fields), patient restrictions, contact profiles, and encounter documents.

**Medications and prescriptions (11 tables, 125 fields)**: Current medication list (20 fields), medication history, prescriptions (38 fields) with pharmacy links, prescription transactions, encounter-level medications, medication history consent, drug alert overrides, pharmacies, preferred pharmacies, immunization VIS editions, and immunization transmission history.

**Labs (15 tables, 187 fields)**: Lab orders with granular item-level detail (items, diagnoses, specimens, answers, documents), lab results with test observations (including diagnoses, notes, specimen data), and lab reference data.

**Referrals (2 tables, 24 fields)**: Referrals with referring reason and linked diagnosis, and referral recipients.

**Messaging (3 tables, 27 fields)**: Patient messages with thread/conversation tracking, message recipients, and message attachments.

**Patient (2 tables, 27 fields)**: Document metadata and questionnaire responses.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient-demographics` (50 fields), `patient-race`, `patient-ethnicity`, `patient-gender-identity-sexual-orientation` (17 fields), `tribal-affiliation`, `occupation-industry`, `patient-financial-resources`, `patient-contacts`, `communication-settings` — 10 tables, 143 fields | Thorough. Includes SOGI, tribal affiliation, occupation/industry, and financial resources beyond USCDI baseline. |
| Encounters / visits | ✅ Covered | `patient-encounters` (20 fields, full SOAP notes), `patient-encounter-addendums`, `patient-encounter-events` (31 fields with coded events/vitals), `patient-encounter-observations` (12 fields with LOINC-coded values), plus encounter-level diagnoses, medications, procedures, documents — 8 tables, 128 fields | Thorough. Full SOAP note text, event detail, observations with code systems. |
| Problems / conditions / diagnoses | ✅ Covered | `patient-diagnoses` (14 fields, ICD-9/10/SNOMED codes, acuity, start/stop dates), `patient-encounter-diagnoses` (6 fields), `patient-conditions` (6 fields — "no known" conditions) | Good. Problem list with coded diagnoses and encounter-level linkage. |
| Medications / prescriptions | ✅ Covered | `patient-medications` (20 fields), `patient-prescriptions` (38 fields), `patient-med-history`, `patient-encounter-medications`, `prescription-transactions`, `patient-medication-history-consent` — 6 tables | Thorough. Current list, history, prescriptions with NDC, and transaction tracking. |
| Allergies | ✅ Covered | `patient-allergy` (20 fields with severity, SNOMED codes, drug class, substance), `patient-allergy-reactions` | Good. Category, severity, onset, SNOMED coding, and granular reactions. |
| Immunizations | ✅ Covered | `patient-immunizations` (31 fields), `patient-immunization-registry`, `patient-immunization-transmission-history`, `immunization-vis-editions` — 4 tables | Thorough. Includes registry data and VIS edition tracking. |
| Vitals | ✅ Covered | Via `patient-encounter-events` (31 fields, `VitalSignCode` field) and `patient-encounter-observations` (12 fields, LOINC-coded observations) | Good. Vitals captured as encounter events and observations with code systems. |
| Lab results | ✅ Covered | `patient-lab-results` (21 fields), `patient-lab-result-tests-observations` (22 fields), plus observation diagnoses, notes, documents, item notes, specimen data — 9 result tables | Thorough. Exceptionally granular with observation-level detail. |
| Imaging / diagnostic reports | ⚠️ Partial | Lab orders include imaging orders (Practice Fusion integrates with imaging centers). `patient-lab-order-documents` and `patient-lab-result-documents` track associated documents. No dedicated imaging entity. | Product supports imaging orders through the same lab integration pathway; imaging reports likely appear as lab results or documents. No separate imaging-specific tables. |
| Procedures | ✅ Covered | `patient-encounter-procedures` (18 fields with CPT/SNOMED/HCPCS codes, order/perform status), `superbill-procedures` (17 fields with billing codes/amounts) | Good. Both clinical and billing views of procedures. |
| Clinical notes / documents | ✅ Covered | Full SOAP notes in `patient-encounters` (Subjective, Objective, Assessment, Plan fields), `patient-encounter-addendums` (7 fields), `patient-documents` (12 fields — metadata), `pinned-notes` (5 fields with NoteText) | Good. Note text is directly exported. Document binary content availability is unclear. |
| Care plans / goals | ✅ Covered | `patient-goals` (11 fields with SNOMED codes), `patient-health-concerns` (11 fields), `patient-advance-directives` (5 fields), `patient-clinical-worksheet-summaries/detail` (16 fields total) | Good. Goals, health concerns, advance directives, and assessment worksheets. |
| Orders / referrals | ✅ Covered | Lab orders: `patient-lab-orders` (25 fields) + 5 order detail tables. Referrals: `patient-referrals` (13 fields) + `patient-referral-recipients` | Good. Granular order tracking. |
| Insurance / coverage | ✅ Covered | `patient-insurances` (65 fields), `patient-insurance-eligibilities` (13 fields), `superbill-insurances` (51 fields) — 3 tables, 129 fields | Thorough. Among the most detailed insurance modeling seen in an EHI export. |
| Claims / billing | ⚠️ Partial | `patient-superbills` (70 fields), `superbill-diagnosis` (9 fields), `superbill-procedures` (17 fields), `superbill-procedure-modifiers`, `superbill-events`, `superbill-insurances` (51 fields) — 6 tables | Superbill layer is deep (the clinical-to-billing handoff). Downstream claims processing (submissions, denials, remittances, A/R) happens in external billing services. This is not a gap in the export — it reflects the product's architecture. |
| Payments | ❌ Not covered | No payment-specific entity | Practice Fusion captures superbills; payment posting happens in external billing software/service. Not a gap in the EHR's data. |
| Consents / directives | ✅ Covered | `patient-advance-directives` (5 fields), `patient-medication-history-consent` (medication history consent tracking), `patient-restrictions` (11 fields — data restrictions per entity) | Adequate. |
| Patient communications / portal messages | ✅ Covered | `patient-messages` (13 fields with thread/conversation tracking), `patient-message-recipients`, `patient-message-attachments` — 3 tables, 27 fields | Good. Messages with thread structure, sender/recipient tracking, and attachments. |
| Patient-reported data | ✅ Covered | `patient-questionnaire` (questionnaire responses), `patient-clinical-worksheet-detail` (Q&A with LOINC codes) | Good. |
| Drug alert overrides (CDS) | ✅ Covered | `patient-drug-alert-overrides` (13 fields — alert level, category, message, interaction reason, primary/secondary drug with NDC) | Notable inclusion — CDS override tracking is uncommon in EHI exports. |

**Domains covered**: 16 of 17 applicable domains (94%). The single "not covered" domain (Payments) is not stored in the EHR itself — payment processing is external.

## 6. Documentation Quality

**Strengths:**
- **Near-complete field descriptions**: 1,164 of 1,165 fields have descriptions (99.9%). Descriptions are plain-English and generally useful (e.g., `RelationshipToInsured`: "Type of relationship between the insured patient and the insurance plan (e.g., Self)").
- **Typed with nullable indicators**: All fields have data types using a consistent system with nullable variants (`Guid?`, `DateTime?`, `Boolean?`), making it clear which fields are optional.
- **Well-organized categories**: 8 categories matching the product's functional areas, logically grouping tables.
- **Version history**: 9 versions in ~26 months (Nov 2023–Jan 2026) with substantive evolution — the v8→v9 transition consolidated lab result tables and added specimen/observation note tables, demonstrating active maintenance.
- **Publicly accessible**: No login required, no JavaScript needed for content, clean static HTML.

**Weaknesses:**
- **No value set documentation**: ~167 String fields likely contain enumerated values (e.g., `BillingStatus`, `EventCategory`, `AllergenCategory`, `Severity`, `ChartNoteType`, `ProcedureStatus`) but no valid values are documented. Some descriptions give examples (e.g., `Severity`: "Mild, Moderate, Severe"; `AllergenCategory`: "Drug, Food, Environment") but most just describe the concept.
- **No relationship/FK documentation**: Foreign key relationships must be inferred from matching GUID field names across tables. There is no entity-relationship diagram and no explicit FK documentation. For example, `EncounterGuid` appears in 14 tables, but the documentation doesn't state which table is the primary.
- **No table-level descriptions**: None of the 85 tables have entity-level descriptions — only field-level documentation exists.
- **No sample data**: No example TSV files or sample export records are provided.
- **No export trigger instructions**: Documentation describes the output format but not how to initiate the export in the EHR.
- **No cardinality or constraint info**: No indication of field cardinality, maximum lengths, or which fields are always populated vs. commonly null.
- **Document binary content unclear**: `patient-documents.tsv` has a `DocumentStorageGuid` field but it's unclear whether actual document files are included in the export.

**Usability assessment**: A developer could build a reasonable import from this documentation — the field names are descriptive, types are clear, and relationship GUIDs follow consistent naming conventions. However, coded fields would require reverse-engineering from sample data, and the lack of an ERD means relationships must be inferred.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

Practice Fusion exports its native relational data model as TSV files — 85 tables with 1,165 fields spanning clinical, billing, messaging, lab, referral, and demographic data. This is not a repackaging of FHIR or C-CDA. The export covers the vast majority of data domains the product stores, with field-level documentation for essentially every field.

### Key Findings

1. **Genuine database-model export with near-complete documentation**: 85 TSV tables, 1,165 fields, 99.9% with descriptions and data types. This is a real (b)(10) implementation, not a clinical summary repackaged. The export uses GUID-based foreign keys preserving the relational structure of the underlying database.

2. **Billing coverage is appropriately scoped**: The export includes 12 billing/insurance tables with 286 fields, including the detailed superbill layer (70-field superbills, 65-field insurance records, 51-field superbill-insurance assignments). Downstream claims processing (submissions, denials, payments) is not in the export because it's not in the EHR — it happens in external billing services/software. This is a correct architectural boundary, not a coverage gap.

3. **Lab data is exceptionally granular**: 15 tables with 187 fields covering orders, order items (with diagnoses, specimens, answers), results, result observations (with diagnoses, notes), and specimen data. This is among the most detailed lab modeling in EHI exports.

4. **Active maintenance demonstrated**: 9 documentation versions in 26 months, with substantive changes (v9 consolidated lab result tables and added new entities). This is not a compliance checkbox.

5. **Main documentation gap is value sets**: ~167 String fields likely contain enumerated values (status codes, categories, types) that are not documented. A developer would need sample data to decode these. No sample data, ERD, or export instructions are provided.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   TSV (tab-separated values)
Model type:      Native database model
Entities:        85
Fields:          1,165
Descriptions:    99.9% (1,164 of 1,165)
Sample data:     No
Bulk export:     Yes (single-patient and entire practice population)
Domains covered: 16 of 17 applicable domains
```

### Bottom Line

Practice Fusion's EHI export is one of the stronger (b)(10) implementations. A patient or provider would get a substantially complete copy of their data — clinical notes, diagnoses, medications, labs, allergies, immunizations, billing/superbills, insurance, messages, referrals, and more — in a practical, machine-readable format. The biggest gap is not in the data itself but in documentation: coded fields lack value set definitions, relationships aren't formally specified, and there's no sample data to guide developers. The export itself, however, is broad and genuine.
