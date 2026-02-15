# EHI Export Analysis: Practice Fusion

**Product**: Practice Fusion EHR v3.7
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2924.Prac.37.01.1.240826 (CHPL #11507)

## 1. Product Context

Practice Fusion is a cloud-based ambulatory EHR serving ~30,000 small/independent medical practices across 53+ specialties. Now a Veradigm Network solution (formerly Allscripts), it offers four tiers: standalone EHR, EHR with billing software, EHR with billing services (managed RCM), and standalone ePrescribing. Key capabilities relevant to export completeness:

- **Clinical charting**: SOAP-note encounters, 130+ customizable templates, clinical worksheets, encounter events/observations/procedures. Supports virtual visits.
- **CPOE**: Medication, lab, and imaging orders.
- **E-prescribing**: Full EPCS with drug interaction checking, formulary support, and prescription transaction history.
- **Lab integration**: 500+ lab/imaging centers; detailed order and result management including specimens, observations, and linked documents.
- **Billing**: Superbill-centric — the EHR captures superbills with diagnoses, procedures, modifiers, and insurance assignments. Full claims lifecycle (submissions, denials, A/R) is handled externally via clearinghouse or managed billing service.
- **Insurance**: Detailed payer information, eligibility checking, guarantor management.
- **Patient portal**: Via FollowMyHealth (separate Veradigm product) — secure messaging, intake forms, questionnaires.
- **Referrals, immunizations, care teams, advance directives, goals, health concerns**.
- **Public health reporting**: Immunization registries, electronic case reporting.

The product stores data primarily about ambulatory clinical encounters, prescriptions, labs, billing (superbill layer), insurance, and patient communications. It does **not** store inpatient data, full claims lifecycle data, or imaging content (only orders/results).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/v9-data-dictionary.json` | Structured extraction of all 85 tables and 1,165 fields with names, types, and descriptions. Parsed from HTML subpages. **Primary analytical source.** | ★★★★★ |
| `downloads/v9-index.html` (48 KB) | v9 index page listing all 85 TSV files organized in 8 categories with one-line descriptions per file. Contains the export format description. | ★★★★ |
| `downloads/v9-pages/` (86 HTML files, 3.0 MB total) | Individual data dictionary pages, one per TSV file. Each contains an HTML table with Field Name, Data Type, and Field Description columns. | ★★★★★ |
| `downloads/ehi-export-documentation-main.html` (34 KB) | Landing page listing all 9 versions (v1–v9, Nov 2023–Jan 2026). No procedural export instructions. | ★★ |
| `downloads/screenshot-v9-index.png` | Full-page screenshot of v9 index — confirms HTML rendering matches parsed data. | ★★ |
| `downloads/screenshot-v9-patient-demographics.png` | Screenshot of patient-demographics page — 50 fields visible, confirms parsed data accuracy. | ★★ |
| `downloads/screenshot-v9-patient-superbills.png` | Screenshot of patient-superbills page — 70 fields visible, confirms parsed data accuracy. | ★★ |
| `ehi-export-report.md` | Prior agent's narrative analysis. Useful for orientation; verified against primary sources. | ★★★ |
| `product-research.md` | Product research establishing baseline of what Practice Fusion stores. | ★★★★ |
| `chpl-metadata.json` | CHPL certification details; confirms (b)(10) certification dated 2024-08-26. | ★★★ |

## 3. Export Mechanics

- **Format**: Tab-separated value (TSV) files — one file per data entity, with header rows. 85 TSV files documented in v9.
- **Mechanism**: Manual export from within the EHR ("EHI Export functionality allows health systems to do a manual export of health data"). No API-based export described. No step-by-step procedure documented in the public materials.
- **Scope**: Supports both **single-patient** and **entire patient population** exports (per v9 index page description).
- **Access constraints/fees**: Not documented in the EHI export documentation itself. The mandatory disclosures page references separate cost and API fee documents.
- **Format details**: GUIDs serve as primary and foreign keys linking tables. Data types include nullable indicators (e.g., `DateTime?`, `Guid?`). 15 distinct data types used.

This is **not** a FHIR or C-CDA repackaging. The export uses the vendor's native relational data model with internal identifiers and table structures that mirror database schema — a genuine (b)(10) implementation.

## 4. Export Content: What's In It

### Summary Statistics

Parsed from `v9-data-dictionary.json` (see `analysis/parse_data_dictionary.py`):

- **85 tables** (TSV files)
- **1,165 total fields**
- **1,164 fields (99.9%)** have plain-English descriptions
- **1,164 fields (99.9%)** have data types documented
- **1 field** has neither (a single empty entry in `patient-drug-alert-overrides.tsv`)
- **36 shared GUID field names** appear across multiple tables, representing implicit foreign key relationships
- **11 fields** explicitly reference code systems (e.g., LOINC, SNOMED, CPT)
- **0 fields** document enumerated value sets in their descriptions

### Tables by Category

| Category | Tables | Fields |
|---|---|---|
| Demographics | 10 | 143 |
| Patient Documents | 2 | 27 |
| Clinical | 32 | 365 |
| Billing and Insurance | 12 | 286 |
| Medications and Prescriptions | 11 | 125 |
| Labs | 15 | 187 |
| Referrals | 2 | 24 |
| Messaging | 3 | 27 |
| **Total** | **85** | **1,165** |

### Largest Tables

| Table | Fields | Domain |
|---|---|---|
| patient-superbills.tsv | 70 | Billing |
| patient-insurances.tsv | 65 | Insurance |
| superbill-insurances.tsv | 51 | Billing |
| patient-demographics.tsv | 50 | Demographics |
| patient-prescriptions.tsv | 38 | Medications |
| patient-encounter-events.tsv | 31 | Encounters |
| patient-healthcare-devices.tsv | 31 | Devices |
| patient-immunizations.tsv | 31 | Immunizations |
| patient-lab-orders.tsv | 25 | Labs |

### Key Table Details

**patient-encounters.tsv** (20 fields): Full SOAP note content (Subjective, Objective, Assessment, Plan fields), chief complaint, chart note type, virtual visit flag, psychotherapy note flag, snapshot of diagnoses and medications at time of signing. Links to provider, facility.

**patient-superbills.tsv** (70 fields): Complete billing header — patient demographics (denormalized), rendering/supervising/referring provider details, facility, place of service, authorization numbers, accident/injury details, onset dates, billing status. Links to 5 related tables: `superbill-diagnosis`, `superbill-procedures`, `superbill-procedure-modifiers`, `superbill-insurances`, `superbill-events`.

**patient-insurances.tsv** (65 fields): Comprehensive payer data including subscriber info, copay amounts, worker's comp/PI attorney details, employer info, secondary subscriber data, order of benefits, relationship to insured.

**patient-encounters + related tables** (8 tables, ~128 fields total): Encounters link to addendums, diagnoses, events, medications, observations, procedures, and documents — a rich encounter-level data model.

**Labs** (15 tables, 187 fields): Exceptionally granular lab coverage: orders → order items → item diagnoses/specimens/answers/documents; results → tests/observations → observation diagnoses/notes; result documents/notes; specimen data. This is one of the most detailed lab data models seen in any EHI export.

**patient-clinical-worksheet-detail.tsv** (7 fields): Custom clinical form responses with question text, answer text, and LOINC codes — captures specialty-specific and customized assessment data.

### Complete Entity Table

See `analysis/entity_table.md` for the full table of all 85 entities with field counts, description coverage, type coverage, and domain classification.

## 5. Coverage Assessment

### Domains Covered

| Domain | Status | Evidence |
|---|---|---|
| **Demographics** | ✅ Covered | 10 tables, 143 fields. Includes race, ethnicity, SOGI, tribal affiliation, occupation/industry, financial resources, previous names, preferred language, pronouns. Exceptionally thorough. |
| **Encounters / visits** | ✅ Covered | `patient-encounters.tsv` (20 fields) + 7 related tables (addendums, diagnoses, events, medications, observations, procedures, documents). Full SOAP notes. Virtual visit support. |
| **Problems / conditions** | ✅ Covered | `patient-conditions.tsv` (no-known-condition flags), `patient-diagnoses.tsv` (14 fields with ICD codes, SNOMED codes, onset/resolution dates, severity). |
| **Medications / prescriptions** | ✅ Covered | `patient-medications.tsv` (20 fields), `patient-prescriptions.tsv` (38 fields), `prescription-transactions.tsv` (10 fields), `patient-med-history.tsv`, `patient-medication-history-consent.tsv`, `patient-encounter-medications.tsv`. Current and historical. |
| **Allergies** | ✅ Covered | `patient-allergy.tsv` (20 fields), `patient-allergy-reactions.tsv` (8 fields). Coded reactions with severity. |
| **Immunizations** | ✅ Covered | `patient-immunizations.tsv` (31 fields), `patient-immunization-registry.tsv`, `patient-immunization-transmission-history.tsv`, `immunization-vis-editions.tsv`. Includes registry/reporting data. |
| **Vitals** | ✅ Covered | Via `patient-encounter-events.tsv` (31 fields) and `patient-encounter-observations.tsv` (12 fields). Vital sign codes, measurement sites, result values. |
| **Lab results** | ✅ Covered | 15 tables, 187 fields. Orders and results with granular test/observation/specimen/diagnosis linkage. One of the most thorough lab data models observed. |
| **Imaging / diagnostic reports** | ⚠️ Partially covered | Imaging orders are handled through the encounter events model. No dedicated imaging results/reports table, though results may arrive via lab result tables for integrated centers. |
| **Procedures** | ✅ Covered | `patient-encounter-procedures.tsv` (18 fields), `superbill-procedures.tsv` (17 fields) with CPT/HCPCS codes and modifiers. |
| **Clinical notes / documents** | ✅ Covered | `patient-encounters.tsv` (full SOAP text), `patient-encounter-addendums.tsv`, `patient-documents.tsv` (12 fields with metadata, type, storage GUID), `pinned-notes.tsv` (note text included). |
| **Care plans / goals** | ✅ Covered | `patient-goals.tsv` (11 fields with SNOMED codes), `patient-health-concerns.tsv` (11 fields with SNOMED codes). |
| **Orders / referrals** | ✅ Covered | `patient-referrals.tsv` (13 fields), `patient-referral-recipients.tsv` (11 fields). Lab/med orders covered separately. |
| **Insurance / coverage** | ✅ Covered | `patient-insurances.tsv` (65 fields), `patient-insurance-eligibilities.tsv` (13 fields), `patient-restrictions.tsv` (11 fields). Extremely detailed. |
| **Claims / billing** | ⚠️ Partially covered | Superbill layer is comprehensive (70 fields + 5 related tables = ~162 fields total across billing). However, downstream claims lifecycle (submissions, denials, payments, A/R) is processed externally by clearinghouse or managed billing service — not stored in Practice Fusion EHR. This is a product boundary, not an export gap. |
| **Payments** | ❌ Not covered | No payment/remittance tables. Consistent with product boundary — payment processing occurs outside the EHR in external billing systems. |
| **Consents / directives** | ✅ Covered | `patient-advance-directives.tsv`, `patient-medication-history-consent.tsv`. |
| **Patient communications** | ✅ Covered | `patient-messages.tsv` (13 fields), `patient-message-recipients.tsv`, `patient-message-attachments.tsv`. Portal messaging data included. |
| **Custom assessments** | ✅ Covered | `patient-clinical-worksheet-detail.tsv` captures question/answer pairs with LOINC codes from 130+ customizable clinical templates. `patient-questionnaire.tsv` (15 fields) captures patient questionnaire responses with coded systems. |
| **Family history** | ✅ Covered | `patient-family-medical-history.tsv` (10 fields), `patient-family-history-diagnoses.tsv` (9 fields). |
| **Smoking / social history** | ✅ Covered | `patient-smokingstatus.tsv` (8 fields). |
| **Drug alert overrides** | ✅ Covered | `patient-drug-alert-overrides.tsv` (13 fields) — CDS interaction audit trail. |

### Coverage Summary

Of the data domains relevant to an ambulatory EHR like Practice Fusion:
- **18 domains fully covered** with dedicated tables and substantial field depth
- **2 domains partially covered** (imaging results, claims lifecycle) — both reflect genuine product boundaries rather than export omissions
- **1 domain not covered** (payments) — again a product boundary; Practice Fusion does not store payment data internally

The export is **not missing any data the EHR actually stores**. The "gaps" correspond to data processed by external systems (clearinghouse billing, FollowMyHealth portal internals).

### Document Content

One area of uncertainty: `patient-documents.tsv` includes a `DocumentStorageGuid` field described as "Filename of the corresponding binary content for this document," along with `FileSizeBytes` and `OriginalFileExtension`. This suggests document binary content may be exported via referenced files, but the documentation does not explicitly confirm whether the actual document files (PDFs, images) are included in the export package alongside the TSV files.

## 6. Documentation Quality

### Strengths

- **Complete field-level coverage**: 1,164 of 1,165 fields (99.9%) have both a data type and a human-readable description.
- **Meaningful descriptions**: No descriptions shorter than 10 characters. Descriptions are generally specific (e.g., "UTC date and time when Encounter event started," "Code system of the procedure code (e.g. SNOMED, CPT, HCPCS)") rather than just restating the field name.
- **Typed with nullable indicators**: 15 distinct data types with `?` suffix indicating nullable fields — useful for developers building import logic.
- **Well-organized**: 8 clear functional categories matching the product's domain model.
- **Actively maintained**: 9 versions in 26 months (Nov 2023–Jan 2026), roughly quarterly. The v8→v9 transition included substantive changes (lab table consolidation, new specimen/observation tables), not cosmetic updates.
- **Publicly accessible**: No login, no JavaScript required, clean static HTML. Fully crawlable.
- **Implicit relationships visible**: 36 shared GUID field names across tables make foreign key relationships inferrable (e.g., `EncounterGuid` appears in 14 tables, `BillingHeaderGuid` in 6).

### Weaknesses

- **No value set documentation**: String fields like `BillingStatus`, `EventCategory`, `Status`, `DisplayOption`, `ChartNoteType`, `OrderOfBenefits`, and `RelationshipToInsured` have descriptions but do not enumerate valid values. Only 1 of 1,165 fields mentions possible values in its description. A developer would have to infer valid values from sample data.
- **No explicit relationship documentation**: No ERD, no foreign key specification, no relationship diagram. Relationships must be inferred from matching GUID field names — feasible but not explicit.
- **No sample data**: No example TSV files, no sample export records, no indication of typical data shapes or volumes.
- **No export procedure**: Documentation describes the output format and content but not how to trigger an export within the EHR UI.
- **No encoding/delimiter specification**: TSV format is described generically (with a Wikipedia link) but charset encoding, line endings, and escaping rules for special characters are not specified.
- **Code system fields reference systems by name but don't document valid values**: Fields like `EventReasonCodeSystem` say "System used for Event Reason Code" — useful to know the column exists, but valid code system names and their associated codes are undocumented.

### Developer Usability

A developer building an import system could work from this documentation, but would face significant challenges:
1. **Reconstructing relationships**: The relational model is reconstructable from GUID naming patterns, but requires detective work.
2. **Interpreting coded fields**: Without value sets, coded/enum fields require sample data or vendor consultation.
3. **Handling binary content**: Whether document files are exported alongside TSV metadata is unclear.

The documentation is sufficient for understanding *what data exists* but insufficient for fully automated, unambiguous import without access to sample data.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

Practice Fusion exports its native relational data model — 85 tables with 1,165 fields across clinical, billing, insurance, medications, labs, messaging, referral, and demographic domains. This is not a C-CDA or FHIR repackaging. The export covers virtually all data the EHR stores, with the only "gaps" corresponding to data handled by external systems (claims lifecycle in clearinghouse, patient portal internals in FollowMyHealth).

### Key Findings

1. **Genuine database-level export**: 85 TSV files map directly to the product's internal data model with GUID-based primary and foreign keys. This is one of the more thorough (b)(10) implementations — the export structure clearly mirrors the EHR's database schema.

2. **Near-complete field documentation**: 99.9% of fields (1,164/1,165) have both data types and plain-English descriptions. This level of documentation completeness is rare among EHI exports.

3. **Exceptionally detailed in key domains**: Labs (15 tables, 187 fields), billing/insurance (12 tables, 286 fields), and encounters (8 tables, ~128 fields) show real depth — not token coverage.

4. **Active maintenance**: 9 documentation versions in 26 months with substantive schema evolution (lab table consolidation in v9) indicates ongoing investment, not a compliance checkbox.

5. **Documentation gaps are in value sets and relationships, not coverage**: The weakness is not *what* is exported but *how well the exported values are explained*. Coded fields lack value enumerations, relationships lack formal specification, and no sample data is provided.

### Bottom Line

A patient or provider requesting an EHI export from Practice Fusion would receive a comprehensive, structured copy of their data across all major clinical and administrative domains the EHR stores. The export includes clinical notes, diagnoses, medications, lab results, billing/superbill data, insurance details, messages, and custom assessment data — well beyond a USCDI clinical summary. The biggest gap is documentation quality for coded fields (no value sets), which would make automated import challenging without sample data, but the raw data coverage is strong.
