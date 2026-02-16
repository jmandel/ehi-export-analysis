# EHI Export Analysis: Practice Fusion

**Product**: Practice Fusion EHR v3.7
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2924.Prac.37.01.1.240826

## 1. Product Context

Practice Fusion is a cloud-based ambulatory EHR serving ~30,000 small/independent medical practices and 5 million patients/month. Now owned by Veradigm (formerly Allscripts), it targets solo and small practices across 53+ specialties. It is offered in four tiers: standalone EHR, EHR with billing software, EHR with billing services (managed RCM), and standalone ePrescribe.

Key capabilities relevant to export completeness:

- **Clinical charting**: 130+ customizable templates, SOAP/simple encounters, encounter events/observations/procedures, addendums, clinical worksheets, pinned notes
- **CPOE**: Medication, lab, and imaging orders
- **ePrescribing**: Full EPCS-certified prescribing with pharmacy integration, drug interaction alerts
- **Labs**: Integration with 500+ lab/imaging centers; detailed order and result management
- **Billing/Revenue Cycle**: Superbill generation, insurance management, eligibility verification, guarantor tracking. Full claims processing happens in external billing services/clearinghouse — Practice Fusion captures the clinical-to-billing handoff (superbills) but not downstream claims lifecycle data
- **Patient portal**: Via Veradigm FollowMyHealth (separate product) — secure messaging, questionnaires
- **Referral management**: Referral records with recipient tracking
- **Immunizations**: Registry reporting, VIS tracking, transmission history
- **Demographics**: Extensive — race, ethnicity, gender identity, sexual orientation, tribal affiliation, occupation/industry, financial resources
- **Scheduling**: Multi-provider appointment management

Practice Fusion does not appear to have deep specialty-specific modules (e.g., oncology staging, OB flowsheets, dental charting) — it serves diverse specialties with general-purpose templates rather than specialty-specific clinical models.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `downloads/ehi-export-documentation-main.html` (33.9 KB) | Landing page listing 9 versioned EHI export documentation releases (v1–v9). v9 is current (Jan 12, 2026). | Low — just version links |
| `downloads/v9-index.html` (48.3 KB) | v9 index page: describes export format (TSV), lists all 85 tables organized in 8 categories with per-table descriptions | **High** — primary structural reference |
| `downloads/v9-pages/` (86 HTML files, 3.0 MB total) | Individual data dictionary pages for each of 85 TSV files plus index. Each contains an HTML table of Field Name, Data Type, and Field Description | **High** — field-level documentation source |
| `downloads/v9-data-dictionary.json` (210 KB) | Pre-extracted structured JSON of all 85 tables and 1,165 fields (prior agent) | High — validated against our own parse; confirmed accurate except one "etc." parse artifact |
| `downloads/screenshot-*.png` (5 files, ~3.4 MB total) | Screenshots of main page, v9 index, patient-demographics page, patient-superbills page | Low — visual reference only |

**Most informative**: The 85 individual HTML pages in `v9-pages/` are the definitive source. Each provides complete field-level documentation for one TSV file.

## 3. Export Mechanics

- **Format**: Tab-separated values (TSV), one file per data entity, with header rows
- **Scope**: Single-patient or entire practice population
- **Mechanism**: Described as "manual export" via EHI Export functionality in the EHR UI. No API-based export documented.
- **Access constraints**: No fees or access restrictions documented on the EHI export documentation pages. The documentation is publicly accessible at `https://www.practicefusion.com/ehi-export-documentation/`.
- **Versioning**: 9 versions published since Nov 2023, with active iteration (most recent: Jan 12, 2026). This cadence indicates ongoing investment.
- **Encoding**: Not explicitly documented; presumed UTF-8
- **Relationships**: Tables are linked via GUID foreign keys (e.g., `PatientPracticeGuid`, `EncounterGuid`, `BillingHeaderGuid`). 88 distinct GUID field names appear across the 85 tables, with `EncounterGuid` used in 14 tables, `DiagnosisGuid` in 7, and `BillingHeaderGuid` in 6.

## 4. Export Content: What's In It

The export contains **85 TSV files** with **1,164 total fields** (after correcting for one HTML parse artifact). All 1,164 fields have both data types and descriptions documented — 100% coverage.

Data types used: `String` (591), `Guid` (203), `Guid?` (115), `DateTime` (77), `DateTime?` (60), `Boolean` (46), `DateField` (31), `Decimal?` (9), `Boolean?` (7), `Int32` (7), `Int32?` (6), `DateTimeOffset?` (6), `Int64?` (2), `Decimal` (2), `Double?` (2). Nullable types (marked with `?`) indicate careful modeling.

### Vendor's own content organization

The vendor organizes the export into 8 categories:

| Category | Tables | Fields | Notes |
|---|---|---|---|
| Demographics | 10 | 143 | Patient identity, contacts, appointments, race/ethnicity/gender/tribal/occupation/financial |
| Patient | 2 | 27 | Documents and questionnaires |
| Clinical | 30 | 346 | Encounters, diagnoses, allergies, immunizations, vitals, devices, care team, goals, etc. |
| Billing and insurance | 12 | 286 | Superbills, insurances, guarantors, eligibilities, encounter documents |
| Medications and prescriptions | 11 | 124 | Medications, prescriptions, transactions, pharmacy, drug alerts, immunization VIS |
| Labs | 15 | 187 | Lab orders (5 sub-tables), lab results (8 sub-tables), labs reference |
| Referrals | 2 | 24 | Referrals and referral recipients |
| Messaging | 3 | 27 | Messages, recipients, attachments |

#### 15 largest entities (representative examples)

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
| patient-medications.tsv | 20 | Medications and prescriptions |

The full inventory of all 85 entities and 1,164 fields is in `analysis/entity-inventory-full.json`.

#### Notable depth

- **Billing (286 fields)**: The billing category alone has 12 tables with deeply modeled superbill data — `patient-superbills.tsv` (70 fields) includes rendering/supervising/referring provider GUIDs, facility info, place of service codes, authorization numbers, accident details, onset dates, and billing status. `superbill-insurances.tsv` (51 fields) captures subscriber details, copay amounts, and claims-relevant insurance data. `superbill-procedures.tsv` has CPT codes, modifiers, units, and charges.
- **Labs (187 fields)**: 15 tables model the full lab lifecycle: orders → order items → item diagnoses → item specimens → item answers → order documents, and results → tests/observations → observation diagnoses → observation notes → result notes → result documents → specimen data.
- **Insurance (65 fields)**: `patient-insurances.tsv` captures subscriber info, copay amounts, attorney details (workers' comp/PI), employer info, and secondary subscriber data.
- **Demographics (50 fields)**: Includes preferred name, previous names, pronouns, SSN, preferred language, death date/time — well beyond USCDI minimums.
- **Encounters (20 fields + sub-tables)**: SOAP note content (Subjective, Objective, Assessment, Plan fields), linked through 6 encounter sub-tables (addendums, diagnoses, events, medications, observations, procedures).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Using the vendor's categories:

- **Demographics** (10 tables, 143 fields): Exceptionally thorough. Beyond core demographics, includes tribal affiliation, occupation/industry, financial resources, gender identity, sexual orientation, communication settings. The `patient-demographics.tsv` alone has 50 fields including preferred name, previous names, pronouns, and preferred language.
- **Clinical** (30 tables, 346 fields): The largest and deepest category. Full encounter documentation with SOAP notes, encounter events with coded reason/result systems and vital signs, encounter observations, procedures with CPT-level detail, diagnoses, allergies with reaction detail, immunizations (31 fields), healthcare devices (31 fields), family history, goals, health concerns, advance directives, clinical worksheets, smoking status, risk scores, care team, and provider profiles.
- **Billing and insurance** (12 tables, 286 fields): Genuinely deep superbill-level billing data — this is not token billing coverage. Superbills, superbill procedures with modifiers, superbill diagnoses, superbill events, superbill insurances, patient insurances (65 fields), insurance eligibilities, guarantors, and patient restrictions. Note: this covers the clinical-to-billing handoff (superbill layer) rather than downstream claims lifecycle, which aligns with Practice Fusion's architecture where claims processing happens in external services.
- **Medications and prescriptions** (11 tables, 124 fields): Comprehensive medication lifecycle — current medications, medication history, prescriptions (38 fields including dosage, refills, DAW, DEA schedule), prescription transactions, pharmacy data, drug alert overrides, medication history consent, immunization VIS editions, and immunization transmission history.
- **Labs** (15 tables, 187 fields): Notably detailed. Models both the order and result lifecycle with multiple sub-entity tables for specimens, diagnoses, observations, notes, and documents.
- **Referrals** (2 tables, 24 fields): Basic but adequate — referral records with recipient details, linked to encounters.
- **Messaging** (3 tables, 27 fields): Patient messages with thread structure, recipients (provider/patient/contact identifiers), and attachments with MIME types and sizes.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient-demographics` (50 fields), `patient-race`, `patient-ethnicity`, `patient-gender-identity-sexual-orientation`, `tribal-affiliation`, `occupation-industry`, `patient-financial-resources`, `communication-settings`, `patient-contacts` (10 tables, 143 fields) | Thorough — well beyond USCDI |
| Encounters / visits | ✅ Covered | `patient-encounters` (20 fields), `patient-encounter-events` (31 fields), `patient-encounter-addendums`, `patient-encounter-diagnoses`, `patient-encounter-medications`, `patient-encounter-observations`, `patient-encounter-procedures` (7 tables) | Deep — SOAP notes, coded events, procedures, observations all captured |
| Problems / conditions / diagnoses | ✅ Covered | `patient-conditions` (6 fields), `patient-diagnoses` (14 fields), `patient-encounter-diagnoses` (6 fields) | Adequate — problem list plus encounter-level diagnoses with ICD/SNOMED coding |
| Medications / prescriptions | ✅ Covered | `patient-medications` (20 fields), `patient-prescriptions` (38 fields), `prescription-transactions` (10 fields), `patient-encounter-medications` (6 fields), `patient-med-history` (5 fields) | Deep — full prescription lifecycle including transactions and drug alert overrides |
| Allergies | ✅ Covered | `patient-allergy` (20 fields), `patient-allergy-reactions` (8 fields) | Thorough — allergy with detailed reactions |
| Immunizations | ✅ Covered | `patient-immunizations` (31 fields), `patient-immunization-registry` (11 fields), `patient-immunization-transmission-history` (7 fields), `immunization-vis-editions` (8 fields) | Deep — includes registry integration and VIS tracking |
| Vitals | ✅ Covered | Captured within `patient-encounter-events` (31 fields) and `patient-encounter-observations` (12 fields) — events include VitalSignCode, MeasurementValue, MeasurementUnit, MeasurementSiteCode fields | Adequate — embedded in encounter events rather than standalone vitals table |
| Lab results | ✅ Covered | `patient-lab-results` (21 fields), `patient-lab-result-tests-observations` (22 fields), plus 6 additional result sub-tables (15 tables, 187 fields total for Labs) | Exceptionally detailed |
| Imaging / diagnostic reports | ⚠️ Partial | Lab ordering supports imaging orders (per CPOE certification for `(a)(3)` imaging orders), but no dedicated imaging results tables. Documents (`patient-documents.tsv`) could contain imaging reports | Product supports imaging orders; results may be stored as documents rather than structured data |
| Procedures | ✅ Covered | `patient-encounter-procedures` (18 fields) — includes CPT codes, performing/ordering providers, linked encounter events | Adequate |
| Clinical notes / documents | ✅ Covered | `patient-encounters` has Subjective/Objective/Assessment/Plan text fields; `patient-encounter-addendums` (7 fields); `patient-documents` (12 fields); `pinned-notes` (5 fields) | Thorough — SOAP notes, addendums, uploaded documents, pinned notes |
| Care plans / goals | ✅ Covered | `patient-goals` (11 fields), `patient-health-concerns` (11 fields), `patient-advance-directives` (5 fields) | Adequate |
| Orders / referrals | ✅ Covered | `patient-lab-orders` (25 fields) + 4 sub-tables; `patient-referrals` (13 fields), `patient-referral-recipients` (11 fields); prescription orders in `patient-prescriptions` | Thorough for labs and referrals |
| Insurance / coverage | ✅ Covered | `patient-insurances` (65 fields), `patient-insurance-eligibilities` (13 fields), `superbill-insurances` (51 fields) | Exceptionally detailed — subscriber info, copays, attorney details, employer data |
| Claims / billing | ✅ Covered | `patient-superbills` (70 fields), `superbill-procedures` (17 fields), `superbill-procedure-modifiers` (8 fields), `superbill-diagnosis` (9 fields), `superbill-events` (7 fields) (12 tables, 286 fields) | Deep at the superbill layer. No downstream claims lifecycle data (claims submission, EOBs, payments), but this aligns with PF's architecture — claims processing is external |
| Payments | ❌ Not covered | No payment or remittance tables in export | Practice Fusion's managed billing services handle payment posting externally; the EHR itself may not store payment records. Minor gap if billing software tier stores payments |
| Consents / directives | ✅ Covered | `patient-advance-directives` (5 fields), `patient-medication-history-consent` (3 fields) | Adequate |
| Patient communications / portal messages | ✅ Covered | `patient-messages` (13 fields), `patient-message-recipients` (6 fields), `patient-message-attachments` (8 fields) | Good — thread structure with sender/recipient tracking and attachments |
| Specialty-specific data | N/A | No specialty-specific entities. Product uses general-purpose templates (130+ customizable) rather than specialty-specific clinical models | Not a gap — PF serves diverse specialties via generic charting, not specialty modules |
| Family health history | ✅ Covered | `patient-family-medical-history` (10 fields), `patient-family-history-diagnoses` (9 fields) | Thorough |
| Patient education | ✅ Covered | `patient-education` (6 fields) | Adequate |
| Questionnaires | ✅ Covered | `patient-questionnaire` (15 fields), `patient-clinical-worksheet-detail` (7 fields), `patient-clinical-worksheet-summaries` (9 fields) | Good — both portal questionnaires and clinical worksheets |
| Scheduling | ✅ Covered | `patient-appointments` (15 fields) | Adequate |

## 6. Documentation Quality

**Excellent.** The documentation is among the best-structured EHI export documentation encountered:

- **Completeness**: 100% of fields (1,164/1,164) have descriptions. 100% have typed data types including nullable indicators.
- **Accessibility**: Entirely HTML-based — no PDF parsing required, no downloadable files to hunt for. Each of 85 tables has its own dedicated page with a clean HTML table.
- **Versioning**: 9 published versions with dates since Nov 2023, showing active maintenance and iteration (most recently Jan 12, 2026).
- **Organization**: Clear 8-category taxonomy matching the product's functional areas.
- **Machine readability**: While not provided as a JSON schema or OpenAPI spec, the HTML structure is regular and trivially parseable (as demonstrated by our extraction script). The pre-extracted `v9-data-dictionary.json` validated against our independent parse.
- **Relationships**: Foreign keys are implicit via GUID naming conventions (e.g., `EncounterGuid` appears in 14 tables) but not formally documented as relationship diagrams or FK constraints. A developer would need to infer relationships from field names, which is straightforward but not explicit.
- **Value sets**: Not documented. Fields like `BillingStatus`, `RelationshipToInsured`, `DestinationTypeCode` have string types but no enumerated values or code system references. Some descriptions give examples (e.g., drug alert levels: "'Mild', 'Severe', etc.") but this is informal.
- **Sample data**: Not provided.

A developer could build an import from this documentation, but would need sample data or trial exports to resolve value set ambiguities and confirm relationship patterns.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

Practice Fusion's export covers the full breadth of what this product stores. It's not just USCDI clinical data — the export includes 12 billing/insurance tables with 286 fields (patient-superbills alone has 70 fields), messaging, referrals, questionnaires, appointments, and extensive demographics beyond USCDI. The billing coverage extends to superbill-level detail including procedure modifiers, insurance linkage, and authorization numbers — this is the product's actual billing data model, not a token gesture. The only notable absence is downstream payment/claims lifecycle data, but this is architecturally consistent: Practice Fusion captures the superbill handoff, while claims processing occurs in external billing services. The 85 TSV files map closely to the product's internal data model, not to any standards-based clinical summary format.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange. Key signals:
1. **Format**: TSV files mapping to internal database tables — not C-CDA sections or FHIR resources
2. **Scope**: 85 entities covering billing, messaging, referrals, appointments, drug alert overrides, clinical worksheets, immunization transmission history — none of these would appear in a (g)(10) FHIR export
3. **Depth**: Fields like `AccidentAutoState`, `AuthorizationNumber`, `SupervisingProviderProfileGuid` in superbills, or `AttorneyFirstName`/`AttorneyPhone` in insurances, are internal EHR data that would never appear in clinical exchange formats
4. **Active iteration**: 9 versions in ~26 months, with v9 consolidating lab result tables — this reflects ongoing engineering investment, not a one-time compliance checkbox
5. **Documentation investment**: 85 dedicated HTML pages with 100% field-level descriptions — far beyond what a repackaged export would receive

### Key Findings

1. **Exceptionally well-documented**: 85 tables, 1,164 fields, 100% with descriptions and types. HTML-based documentation is clean, parseable, and actively maintained across 9 versions. This is a top-tier documentation effort.
2. **Genuine billing coverage**: 12 billing/insurance tables with 286 fields — `patient-superbills.tsv` (70 fields) and `patient-insurances.tsv` (65 fields) demonstrate that Practice Fusion exports its actual billing data model, not a USCDI-scoped subset.
3. **Deep lab lifecycle modeling**: 15 lab tables with 187 fields covering the full order-to-result pipeline with sub-entity tables for specimens, diagnoses, observations, notes, and documents.
4. **Missing value sets**: Despite excellent field-level documentation, no enumerated values or code system references are provided for coded fields. This is the primary documentation gap.
5. **No sample data**: The documentation would benefit from sample TSV files or a downloadable sample export to complement the data dictionary.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   TSV (tab-separated values)
    Entities:        85
    Fields:          1,164
    Descriptions:    100% (1,164/1,164)
    Sample data:     No
    Bulk export:     Yes (single-patient or entire practice population)
    Domains covered: 17 of 18 applicable domains (only Payments not covered; architecturally external)

### Bottom Line

Practice Fusion delivers one of the stronger (b)(10) implementations: a purpose-built TSV export of 85 internal database tables with 1,164 fully documented fields spanning clinical, billing, messaging, and administrative domains. The export reflects the product's actual data model rather than a clinical exchange repackaging. The main limitation is the absence of downstream payment/claims data, but this is consistent with the product's architecture where claims processing is handled externally.
