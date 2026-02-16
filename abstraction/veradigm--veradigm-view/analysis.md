# EHI Export Analysis: Veradigm (Veradigm View / Practice Fusion)

**Product**: Veradigm View (Practice Fusion EHR)
**Analysis date**: 2026-02-16
**CHPL ID**: 11697 (15.04.04.2891.View.01.02.1.250909)

## 1. Product Context

Veradigm View is the ONC-certified product name for **Practice Fusion EHR**, a 100% cloud-based ambulatory EHR designed for small, independent physician practices. Veradigm (formerly Allscripts) acquired Practice Fusion in 2018. The product targets solo practitioners and small clinics, with over 31,000 clinicians and approximately 5 million patient visits per month.

Key data domains the product stores (relevant to export completeness assessment):

- **Clinical documentation**: Encounter charting with assessments, diagnoses, procedures, observations, medications, addendums; problem lists/conditions; customizable templates
- **Medications & e-prescribing**: Medication lists, prescriptions (including EPCS), pharmacy management, drug interaction alerts
- **Lab integration**: Lab orders and results with observation-level detail
- **Billing & insurance**: Superbills, insurance eligibility, claims management, guarantor info — described as "comprehensive" billing with clearinghouse integration
- **Patient engagement**: Patient portal (via FollowMyHealth), messaging, questionnaires, documents
- **Immunizations**: Immunization management with registry reporting
- **Referrals**: Referral management
- **Scheduling**: Basic appointment scheduling

The product is separately certified for FHIR R4 API access (g)(10), transitions of care (b)(1)–(b)(3), immunization registry (f)(1), and cancer registry (f)(5) reporting.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/v6-index.html` (249 KB) | V6 EHI Export Documentation index page — lists all 87 TSV entities organized into 8 categories, includes export format description | **High** — primary structural overview |
| `downloads/v6-entities/*.html` (87 files, ~233 KB each) | Individual entity documentation pages — each contains TSV filename, entity description, and field-level data dictionary (name, type, description) | **High** — field-level documentation for all 1,194 fields |
| `downloads/enrichment/entities-catalog.json` (233 KB) | Machine-parsed catalog of all 87 entities and 1,194 fields, extracted from the HTML pages | **High** — structured parse verified against HTML source |
| `downloads/enrichment/coverage-accounting.json` | Parse statistics: field counts by entity and category | Medium — summary stats |
| `product-research.md` | Prior research on Veradigm/Practice Fusion product capabilities and market position | Medium — product context |
| `ehi-export-report.md` | Prior agent's analysis of the export documentation | Medium — orientation (verified independently) |

**No sample export files, JSON schemas, or machine-readable artifacts were provided** — the documentation is HTML-only.

## 3. Export Mechanics

- **Format**: TSV (tab-separated values) — one file per entity type, 87 files total in V6
- **Mechanism**: Manual export triggered by the practice ("EHI Export functionality allows health systems to do a manual export")
- **Scope**: Single patient or entire patient population in a practice
- **Access**: The index page states the export is performed within the EHR; no API-based or self-service patient-facing mechanism is documented
- **Versioning**: Six versions published (V1 through V6, April 2025 to January 2026), suggesting active development
- **Fees/constraints**: Not documented in the available artifacts
- **Documentation access**: Publicly accessible HTML pages at `veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/`, no authentication required

This is a **genuine (b)(10) export** — not a repackaged FHIR or C-CDA feed. The TSV format maps directly to database entities, and the 87 entity types with 1,194 fields far exceed what USCDI or US Core would cover.

## 4. Export Content: What's In It

### Data dictionary overview

The V6 documentation provides field-level documentation for all 87 TSV entity types:

- **87 entities** across 8 vendor-defined categories
- **1,194 total fields**
- **1,194 fields (100%) have descriptions** — every field has a description
- **1,192 fields (99.8%) have meaningful descriptions** — only 2 trivial descriptions (`EventResultName` → "Event Result", `VitalSignCode` → "Vital Sign")
- **Data types documented** for every field: String (599), Guid (212), Guid? (123), DateTime (81), DateTime? (60), Boolean (47), DateField (31), Decimal? (9), Boolean? (7), Int32 (7), DateTimeOffset? (6), Int32? (6), others
- **No value sets or code enumerations** documented — coded fields (e.g., `BillingStatus`, `DestinationTypeCode`) list the field name and type but not valid values
- **No explicit foreign key documentation** — relationships are implicit through shared Guid field names (e.g., `PatientPracticeGuid` appears in 78 entities, `EncounterGuid` in 15)
- **No sample data** provided

### Vendor's own content organization

The vendor organizes entities into 8 categories. Full inventory saved to `analysis/full-entity-inventory.json`.

| Category | Entities | Fields | Key Entities |
|---|---|---|---|
| Clinical | 32 | 376 | `patient-encounters` (20), `patient-encounter-events` (31), `patient-allergy` (20), `patient-immunizations` (31), `patient-healthcare-devices` (31), `patient-encounter-assessment-plans` (21), `patient-encounter-procedures` (18) |
| Billing and insurance | 12 | 286 | `patient-superbills` (70), `patient-insurances` (65), `superbill-insurances` (51), `patient-guarantor` (22), `superbill-procedures` (17) |
| Labs | 15 | 187 | `patient-lab-orders` (25), `patient-lab-result-tests-observations` (22), `patient-lab-results` (21), `patient-lab-order-item-specimens` (20) |
| Demographics | 10 | 143 | `patient-demographics` (50), `patient-gender-identity-sexual-orientation` (17), `patient-appointments` (15), `patient-contacts` (15) |
| Medications and prescriptions | 11 | 124 | `patient-prescriptions` (38), `patient-medications` (20), `patient-drug-alert-overrides` (12), `pharmacies` (11) |
| Patient | 2 | 27 | `patient-questionnaire` (15), `patient-documents` (12) |
| Messaging | 3 | 27 | `patient-messages` (13), `patient-message-attachments` (8), `patient-message-recipients` (6) |
| Referrals | 2 | 24 | `patient-referrals` (13), `patient-referral-recipients` (11) |

Numbers in parentheses are field counts per entity.

### Representative entities (top 10 by field count)

| Entity | Fields | Category | Description |
|---|---|---|---|
| `patient-superbills` | 70 | Billing and insurance | Super bill header data — billing status, provider, facility, patient info, dates, amounts, payer info |
| `patient-insurances` | 65 | Billing and insurance | Insurance data — plan details, subscriber info, group numbers, copays, effective dates |
| `superbill-insurances` | 51 | Billing and insurance | Insurance details linked to specific superbills — payer info, authorization, amounts |
| `patient-demographics` | 50 | Demographics | Full patient record — name variants, DOB, SSN, address, phone, email, language, marital status |
| `patient-prescriptions` | 38 | Medications and prescriptions | Prescription details — medication, route, strength, frequency, refills, DAW, pharmacy, dates |
| `patient-encounter-events` | 31 | Clinical | Encounter events — vitals, results, dates, coded values, negation flags |
| `patient-healthcare-devices` | 31 | Clinical | UDI-tracked devices/implants — device identifiers, production identifiers, lot/serial, dates |
| `patient-immunizations` | 31 | Clinical | Immunization records — vaccine codes, dates, manufacturer, lot, route, site, provider, registry status |
| `patient-lab-orders` | 25 | Labs | Lab orders — order number, provider, facility, diagnoses, status, dates |
| `patient-guarantor` | 22 | Billing and insurance | Financial guarantor — name, address, relationship, SSN, employer info |

### Notable structural observations

- **Encounter model is rich**: 10 encounter sub-entities (`encounter-assessments`, `encounter-assessment-plans`, `encounter-diagnoses`, `encounter-events`, `encounter-medications`, `encounter-observations`, `encounter-procedures`, `encounter-addendums`, `encounter-documents`) with the parent `patient-encounters` entity
- **Lab model is the deepest domain**: 15 entities covering orders and results at the observation level, with specimen data, notes, and documents
- **Billing is substantive**: 12 entities totaling 286 fields — superbills, insurance, guarantor, eligibility, procedure-level billing detail with modifiers
- **Guid-based relationships**: `PatientPracticeGuid` links nearly all entities to a patient (78/87 entities); `EncounterGuid` connects 15 encounter-related entities; `OrderGuid` connects 9 lab entities

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's 8 categories provide broad coverage of an ambulatory EHR data model:

**Richest categories:**
- **Billing and insurance** (12 entities, 286 fields): Genuinely deep — superbills alone have 70 fields covering billing status, rendering/referring providers, facility, ICD codes, amounts, dates, and payer details. Insurance entities capture plan details, subscriber demographics, group/policy numbers, copays, and authorization data. This goes well beyond a token billing presence.
- **Clinical** (32 entities, 376 fields): Comprehensive encounter model with assessments, procedures, observations, and events. Also covers allergies (20 fields + reactions), immunizations (31 fields), healthcare devices/implants (31 fields), conditions, diagnoses, goals, health concerns, care team, advance directives, clinical worksheets, family history, smoking status, risk scores, and patient education.
- **Labs** (15 entities, 187 fields): Most granular domain — orders decomposed into items with diagnoses, answers, and specimens; results decomposed into observations with specimen data, notes, and documents.

**Adequate categories:**
- **Demographics** (10 entities, 143 fields): 50-field patient record plus separate entities for race, ethnicity, gender identity/sexual orientation, tribal affiliation, occupation/industry, financial resources, contacts, appointments, and communication settings.
- **Medications and prescriptions** (11 entities, 124 fields): Full prescription lifecycle including drug alert overrides, medication history consent, pharmacy directory, VIS editions, and transmission history for immunization reporting.

**Thinnest categories:**
- **Patient** (2 entities, 27 fields): Documents and questionnaires only.
- **Messaging** (3 entities, 27 fields): Messages, recipients, and attachments.
- **Referrals** (2 entities, 24 fields): Referrals and referral recipients.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient-demographics` (50 fields), `patient-contacts` (15), `patient-race` (7), `patient-ethnicity` (7), `patient-gender-identity-sexual-orientation` (17), `occupation-industry` (9), `tribal-affiliation` (5), `communication-settings` (12), `patient-financial-resources` (6) | Thorough — includes USCDI v3+ demographics (SOGI, tribal affiliation, occupation) |
| Encounters / visits | ✅ Covered | `patient-encounters` (20), plus 10 encounter sub-entities covering assessments, diagnoses, procedures, observations, events, medications, addendums, documents | Rich encounter model with multiple sub-entities |
| Problems / conditions / diagnoses | ✅ Covered | `patient-conditions` (6), `patient-diagnoses` (14), `patient-encounter-diagnoses` (6) | Both standing problem list and encounter-level diagnoses |
| Medications / prescriptions | ✅ Covered | `patient-medications` (20), `patient-prescriptions` (38), `patient-encounter-medications` (6), `patient-med-history` (5), `patient-medication-history-consent` (3), `prescription-transactions` (10), `pharmacies` (11), `preferred-pharmacy` (4), `patient-drug-alert-overrides` (12) | Full lifecycle including e-prescribing transactions and CDS override tracking |
| Allergies | ✅ Covered | `patient-allergy` (20), `patient-allergy-reactions` (8) | Detailed — separate reaction entity |
| Immunizations | ✅ Covered | `patient-immunizations` (31), `immunization-vis-editions` (8), `patient-immunization-registry` (11), `patient-immunization-transmission-history` (7) | Comprehensive — includes VIS tracking and registry reporting data |
| Vitals | ✅ Covered | Captured within `patient-encounter-events` (31 fields) — includes `VitalSignCode`, `ResultValue`, `ResultUnit` | Stored as encounter events rather than a separate vitals entity |
| Lab results | ✅ Covered | 15 entities: `patient-lab-orders` (25), `patient-lab-results` (21), `patient-lab-result-tests-observations` (22), `patient-lab-order-items` (16), `patient-lab-order-item-specimens` (20), `patient-lab-result-item-notes` (6), `labs` (12), plus 8 more | Most detailed domain — observation-level granularity |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging entity; imaging orders may be captured through `patient-lab-orders` or results if routed through the lab workflow; `patient-documents` (12 fields) may contain imaging reports | Product is ambulatory-focused with lab integration; no PACS or dedicated imaging module expected |
| Procedures | ✅ Covered | `patient-encounter-procedures` (18) | Encounter-level procedures documented |
| Clinical notes / documents | ✅ Covered | `patient-documents` (12), `patient-encounter-documents` (8), `patient-encounter-addendums` (7), `patient-encounter-assessment-plans` (21), `patient-encounter-assessments` (9), `pinned-notes` (5), `patient-clinical-worksheet-summaries` (9), `patient-clinical-worksheet-detail` (7) | Multiple note/document entities; clinical worksheets appear to cover custom forms |
| Care plans / goals | ✅ Covered | `patient-goals` (11), `patient-health-concerns` (11), `patient-advance-directives` (5), `care-team` (8), `care-team-profiles` (7) | Goals, health concerns, advance directives, and care team all present |
| Orders / referrals | ✅ Covered | `patient-referrals` (13), `patient-referral-recipients` (11), `patient-lab-orders` (25) | Referrals and lab orders; no general CPOE order entity, but the product likely routes orders through encounter procedures/lab orders |
| Insurance / coverage | ✅ Covered | `patient-insurances` (65), `patient-insurance-eligibilities` (13), `superbill-insurances` (51) | Deep — 65 fields for insurance plans, eligibility verification, payer-level detail per superbill |
| Claims / billing | ✅ Covered | `patient-superbills` (70), `superbill-diagnosis` (9), `superbill-procedures` (17), `superbill-procedure-modifiers` (8), `superbill-events` (7), `superbill-insurances` (51) | Substantive — superbills with procedure-level detail, modifiers, and insurance linkage |
| Payments | ⚠️ Partial | `patient-superbills` includes payment-related fields (amounts, billing status) but no dedicated payment/transaction entity | Product may rely on external clearinghouse for payment processing; superbill captures charges but not payment receipts |
| Consents / directives | ✅ Covered | `patient-advance-directives` (5), `patient-medication-history-consent` (3) | Basic — advance directives and medication history consent |
| Patient communications / portal messages | ✅ Covered | `patient-messages` (13), `patient-message-recipients` (6), `patient-message-attachments` (8) | In-product messaging; FollowMyHealth portal data is a separate certified product |
| Family history | ✅ Covered | `patient-family-medical-history` (10), `patient-family-history-diagnoses` (9) | Family member records with per-member diagnoses |
| Smoking status | ✅ Covered | `patient-smokingstatus` (8) | Dedicated entity |
| Patient education | ✅ Covered | `patient-education` (6) | Education materials provided to patients |
| Questionnaires | ✅ Covered | `patient-questionnaire` (15) | Patient questionnaire responses |
| Healthcare devices | ✅ Covered | `patient-healthcare-devices` (31) | UDI-compliant device tracking |

**Summary**: 17 of 19 applicable domains are covered; 2 are partially covered (imaging and payments). No applicable domains are entirely missing. The partial gaps are reasonable for a small-practice ambulatory EHR — imaging is typically routed through lab workflows or external PACS, and payment processing is often handled by clearinghouses.

## 6. Documentation Quality

**Strengths:**
- **Complete field-level documentation**: All 1,194 fields across 87 entities have descriptions — 100% documentation rate
- **Meaningful descriptions**: 99.8% of descriptions go beyond restating the field name (e.g., "Unique identifier of the medication this prescription is for," "Destination for this prescription - PRINT/RECORD/SEND," "The status code reported by the lab (F=final, C=corrected, etc.)")
- **Consistent structure**: Every entity page follows the same format — TSV filename, entity description, field table with Name/Type/Description
- **Clear categorization**: 8 functional categories organize the 87 entities logically
- **Active maintenance**: Six published versions in 10 months (V1–V6, April 2025 to January 2026)
- **Publicly accessible**: No authentication required; clean URL structure

**Weaknesses:**
- **No sample data**: No example TSV files or records to validate the documentation against actual output
- **No machine-readable schema**: No JSON Schema, XSD, DDL, or other parseable format — documentation is HTML-only
- **No value sets or code enumerations**: Coded fields like `BillingStatus`, `DestinationTypeCode`, `EncounterStatus` don't document valid values
- **No explicit relationship documentation**: Foreign keys must be inferred from matching Guid field names (e.g., `PatientPracticeGuid`, `EncounterGuid`). No ERD or relationship diagram
- **No data type constraints**: Types are high-level (`String`, `Guid`, `Integer`) with no length limits or precision specifications
- **No export procedure documentation**: How to trigger the export, what the output looks like, file naming conventions, etc. are not documented in these artifacts

**Developer usability**: A developer could build a reasonable import from this documentation. The entity/field structure is clear, relationships are inferrable from Guid naming conventions, and descriptions provide enough context to understand what each field represents. The main challenge would be coded fields where valid values aren't documented, and the lack of sample data to validate assumptions.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native data model export with solid documentation across all major data domains. The 87 TSV entities with 1,194 fully-described fields map directly to the Practice Fusion database model, covering clinical, billing, lab, medication, demographic, messaging, and referral data. This is clearly not a repackaged FHIR or C-CDA export.

### Key Findings

1. **Genuine (b)(10) implementation**: 87 native database entities exported as TSV files — far exceeding the ~20 USCDI resources that a FHIR/C-CDA repackaging would provide. The export covers data domains (billing, drug alert overrides, prescription transactions, immunization registry history) that are entirely absent from standard clinical exchange formats.

2. **100% field-level documentation**: Every one of the 1,194 fields has a description, and 99.8% are meaningful (not just restating the field name). This is among the highest documentation rates in EHI exports.

3. **Billing data is substantive, not token**: 12 billing/insurance entities with 286 fields — including 70-field superbills, 65-field insurance records, and procedure-level billing detail with modifiers. This represents real billing data, not just a few invoice fields.

4. **Lab domain is exceptionally granular**: 15 entities decompose lab orders and results down to the observation level with specimen data, notes, and documents — the most detailed lab model among typical ambulatory EHR exports.

5. **Supporting artifacts are absent**: No sample data, no machine-readable schemas, no value set documentation, no relationship diagrams, and no export procedure documentation. The data dictionary is solid, but developers would need to do significant inference work to build a reliable import.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   TSV (tab-separated values)
Model type:      Native database model
Entities:        87
Fields:          1,194
Descriptions:    100% (99.8% meaningful)
Sample data:     No
Bulk export:     Yes (single patient or entire practice population)
Domains covered: 17 of 19 applicable domains (2 partial: imaging, payments)
```

### Bottom Line

Veradigm View / Practice Fusion provides a strong (b)(10) implementation that exports the product's native data model across clinical, billing, lab, medication, and demographic domains. A patient or provider would get a comprehensive, usable copy of their data covering essentially all EHI the product stores. The biggest gap is not in data coverage but in supporting artifacts — the absence of sample data, value set documentation, and machine-readable schemas means developers must do significant inference work to reliably consume the export.
