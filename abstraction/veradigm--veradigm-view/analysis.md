# EHI Export Analysis: Veradigm (Veradigm View / Practice Fusion)

**Product**: Veradigm View (marketed as Practice Fusion EHR)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2891.View.01.02.1.250909

## 1. Product Context

Veradigm View is the ONC-certified name for **Practice Fusion EHR**, a 100% cloud-based ambulatory EHR designed for small, independent physician practices. Practice Fusion was acquired by Allscripts (now Veradigm) in 2018 for $100M and claims over 31,000 clinician users serving approximately 5 million patient visits per month.

The product is a straightforward ambulatory EHR with integrated practice management. Key capabilities include:

- **Clinical charting**: Encounters with assessments, diagnoses, procedures, observations; problem lists; allergies; immunizations; family history; clinical worksheets; healthcare devices; care teams; goals; advance directives
- **Medications & e-prescribing**: Prescriptions (including EPCS), medication lists, drug interaction alerts, pharmacy management
- **Lab integration**: Lab orders and results with detailed observation-level data
- **Billing**: Superbills, insurance management, eligibility verification, guarantor tracking — practice-management-oriented billing (likely clearing through external clearinghouses)
- **Patient engagement**: Portal messaging, documents, questionnaires, education materials
- **Referrals**: Referral management with recipients
- **Scheduling**: Appointment management

This is a simpler product than full hospital EHRs — it doesn't do inpatient, surgical, oncology, behavioral health specialty modules, or deep revenue cycle management. The export should cover ambulatory clinical, basic billing/insurance, messaging, and referrals.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/v6-index.html` (249 KB) | V6 EHI Export Documentation index page listing all 87 TSV entities in 8 categories, with introductory description of export format and mechanism | **High** — primary structural overview |
| `downloads/v6-entities/*.html` (87 files, ~232–239 KB each) | Individual entity documentation pages, each with h2 entity name, h4 description, and field table (Field Name, Data type, Field Description) | **High** — complete data dictionary |
| `downloads/enrichment/entities-catalog.json` | Pre-extracted entity catalog from prior agent; 87 entities, 1,194 fields | **Medium** — used for cross-validation |
| `downloads/enrichment/coverage-accounting.json` | Parse statistics from prior agent | **Low** — confirmed counts only |
| `product-research.md` | Product context and capability research | **Medium** — oriented analysis |
| `ehi-export-report.md` | Prior agent's narrative analysis | **Medium** — orientation, verified claims independently |

All 87 entity HTML pages were successfully parsed with zero parse errors. Field counts were cross-validated against the prior enrichment extraction — all counts matched exactly.

## 3. Export Mechanics

- **Format**: TSV (tab-separated values) — one file per entity type, 87 entity types in V6
- **Mechanism**: Manual export triggered by the practice via the EHR UI
- **Scope**: Single patient or entire patient population in a practice
- **Access**: The index page states: "EHI Export functionality allows health systems to do a manual export of health data for a single patient or entire patient population in a practice."
- **Versioning**: Six versions released between April 2025 and January 2026 (V1–V6), with V6 being current as of January 12, 2026 — indicating active development
- **No fees or access constraints mentioned** in the documentation
- **Documentation is publicly accessible** at `veradigm.com/legal/veradigm-view-ehi-export-documentation/v6/`

## 4. Export Content: What's In It

The V6 export contains **87 TSV entity types** with **1,194 total fields**. Every field has a name, data type, and description — 100% documentation coverage.

### Data types

The 1,194 fields use 15 distinct data types:

| Type | Count | % |
|---|---|---|
| String | 599 | 50.2% |
| Guid | 212 | 17.8% |
| Guid? | 123 | 10.3% |
| DateTime | 81 | 6.8% |
| DateTime? | 60 | 5.0% |
| Boolean | 47 | 3.9% |
| DateField | 31 | 2.6% |
| Others (Decimal, Int32, Int64, Double, DateTimeOffset, nullable variants) | 41 | 3.4% |

The 335 Guid/Guid? fields indicate extensive use of foreign keys for entity relationships, though the documentation does not explicitly document relationship cardinalities.

### Vendor's own content organization

The vendor organizes the 87 entities into 8 categories:

| Category | Entities | Fields | Description |
|---|---|---|---|
| Clinical | 32 | 376 | Encounters, assessments, diagnoses, procedures, observations, allergies, immunizations, conditions, family history, goals, health concerns, devices, care teams, providers, clinical worksheets, education, advance directives, smoking status, risk scores, pinned notes |
| Billing and insurance | 12 | 286 | Superbills, insurance policies, superbill insurance details, guarantors, insurance eligibilities, encounter documents, restrictions, superbill diagnoses/procedures/modifiers/events, contact profiles |
| Labs | 15 | 187 | Lab orders (with items, diagnoses, answers, specimens, documents), lab results (with test observations, notes, observation diagnoses, specimen data, documents), lab reference data |
| Demographics | 10 | 143 | Patient demographics, appointments, contacts, communication settings, ethnicity, race, gender identity/sexual orientation, occupation/industry, financial resources, tribal affiliation |
| Medications and prescriptions | 11 | 124 | Prescriptions, medications, drug alert overrides, pharmacy data, prescription transactions, immunization VIS editions, immunization transmission history, medication history, medication history consent, encounter medications |
| Messaging | 3 | 27 | Patient messages, message recipients, message attachments |
| Patient | 2 | 27 | Patient documents, patient questionnaires |
| Referrals | 2 | 24 | Patient referrals, referral recipients |

### Top 20 entities by field count

| Entity | Fields | Category |
|---|---|---|
| patient-superbills | 70 | Billing and insurance |
| patient-insurances | 65 | Billing and insurance |
| superbill-insurances | 51 | Billing and insurance |
| patient-demographics | 50 | Demographics |
| patient-prescriptions | 38 | Medications and prescriptions |
| patient-encounter-events | 31 | Clinical |
| patient-healthcare-devices | 31 | Clinical |
| patient-immunizations | 31 | Clinical |
| patient-lab-orders | 25 | Labs |
| patient-guarantor | 22 | Billing and insurance |
| patient-lab-result-tests-observations | 22 | Labs |
| patient-encounter-assessment-plans | 21 | Clinical |
| patient-lab-results | 21 | Labs |
| patient-allergy | 20 | Clinical |
| patient-encounters | 20 | Clinical |
| patient-lab-order-item-specimens | 20 | Labs |
| patient-medications | 20 | Medications and prescriptions |
| patient-encounter-procedures | 18 | Clinical |
| patient-gender-identity-sexual-orientation | 17 | Demographics |
| superbill-procedures | 17 | Billing and insurance |

The complete entity inventory with all 1,194 fields is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export maps directly to the product's internal database entities, organized into 8 categories. The coverage is notably uniform — no category appears to be a stub.

**Deepest domains:**

- **Billing and insurance** (12 entities, 286 fields): The single richest domain by field count. The `patient-superbills` entity (70 fields) captures billing header details, performing provider, facility, patient demographics on the bill, place of service, authorization numbers, dates, referring provider, and billing status. `patient-insurances` (65 fields) has full insurance policy detail including plan names, group numbers, copays, subscriber info, and relationship codes. `superbill-insurances` (51 fields) links specific insurance details to individual superbills. This level of billing detail goes far beyond USCDI.

- **Clinical** (32 entities, 376 fields): Broad coverage of the ambulatory encounter model. Encounters are decomposed into 9 sub-entities (assessment-plans, assessments, diagnoses, documents, events, medications, observations, procedures, addendums). Additional standalone entities for conditions, diagnoses, allergies (with reactions), immunizations (with VIS tracking and registry), family history, goals, health concerns, devices, care teams, clinical worksheets, education, advance directives, and smoking status.

- **Labs** (15 entities, 187 fields): The most granular domain structurally — 15 entities covering the full lab order-to-result lifecycle including order items, item answers, item diagnoses, item specimens, order documents, result items, result notes, test observations, observation diagnoses, specimen data, and result documents.

**Thinnest domains:**

- **Messaging** (3 entities, 27 fields) and **Referrals** (2 entities, 24 fields) are smaller, but these reflect the simpler nature of these features in a small-practice EHR — messages have content, timestamps, and recipient tracking; referrals have provider details, reasons, and status.

- **Patient** (2 entities, 27 fields) covers documents and questionnaire responses. The `patient-questionnaire` entity (15 fields) captures form responses, which is notable as custom form data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient-demographics` (50 fields), `patient-contacts` (15), `patient-race` (7), `patient-ethnicity` (7), `patient-gender-identity-sexual-orientation` (17), `tribal-affiliation` (5), `occupation-industry` (9), `communication-settings` (12), `patient-financial-resources` (6) | Thorough — 10 entities, 143 fields total. Includes USCDI v3 elements (race, ethnicity, SOGI, tribal affiliation) plus extended demographics |
| Encounters / visits | ✅ Covered | `patient-encounters` (20 fields), plus 9 sub-entities for encounter details (assessment-plans, assessments, diagnoses, documents, events, medications, observations, procedures, addendums) | Rich decomposition — encounter data spread across 10 entities |
| Problems / conditions | ✅ Covered | `patient-conditions` (6 fields), `patient-diagnoses` (14 fields), `patient-encounter-diagnoses` (6 fields) | Three entities distinguish standalone conditions, patient-level diagnoses, and encounter-specific diagnoses |
| Medications / prescriptions | ✅ Covered | `patient-medications` (20 fields), `patient-prescriptions` (38 fields), `prescription-transactions` (10), `patient-encounter-medications` (6), `patient-med-history` (5), `patient-medication-history-consent` (3) | Full lifecycle from current meds to prescriptions to transaction tracking |
| Allergies | ✅ Covered | `patient-allergy` (20 fields), `patient-allergy-reactions` (8 fields) | Detailed with separate reaction tracking |
| Immunizations | ✅ Covered | `patient-immunizations` (31 fields), `immunization-vis-editions` (8), `patient-immunization-registry` (11), `patient-immunization-transmission-history` (7) | 4 entities covering immunizations, VIS tracking, and registry reporting |
| Vitals | ✅ Covered | `patient-encounter-observations` (12 fields) | Observations within encounters capture vitals |
| Lab results | ✅ Covered | 15 entities including `patient-lab-results` (21), `patient-lab-result-tests-observations` (22), `lab-result-item-specimen-data` (13), plus notes and documents | Most granular domain — comprehensive order-to-result model |
| Imaging / diagnostic reports | ⚠️ Partial | `patient-documents` (12 fields) may contain imaging reports; `patient-lab-orders` could cover imaging orders | No dedicated imaging entities; imaging results likely stored as documents. Appropriate for a small-practice ambulatory EHR that doesn't do in-house imaging |
| Procedures | ✅ Covered | `patient-encounter-procedures` (18 fields), `superbill-procedures` (17 fields) | Both clinical and billing procedure records |
| Clinical notes / documents | ✅ Covered | `patient-documents` (12 fields), `patient-encounter-documents` (8), `patient-encounter-addendums` (7), `pinned-notes` (5) | Multiple document types including encounter notes, addendums, and clinical sticky notes |
| Care plans / goals | ✅ Covered | `patient-goals` (11 fields), `patient-health-concerns` (11), `patient-advance-directives` (5), `care-team` (8), `care-team-profiles` (7), `patient-encounter-assessment-plans` (21) | Rich care planning with goals, health concerns, advance directives, care teams, and assessment plans |
| Orders / referrals | ✅ Covered | `patient-lab-orders` (25 fields) + 5 sub-entities; `patient-referrals` (13), `patient-referral-recipients` (11) | Lab orders deeply modeled; referrals with recipient tracking |
| Insurance / coverage | ✅ Covered | `patient-insurances` (65 fields), `patient-insurance-eligibilities` (13), `patient-guarantor` (22), `patient-financial-resources` (6) | Deep — 65-field insurance entity with eligibility and guarantor |
| Claims / billing | ✅ Covered | `patient-superbills` (70 fields), `superbill-diagnosis` (9), `superbill-procedures` (17), `superbill-procedure-modifiers` (8), `superbill-events` (7), `superbill-insurances` (51) | Practice-level billing (superbills) with full decomposition into diagnoses, procedures, modifiers, events, and insurance linkage. Not full claims adjudication, but appropriate for a small-practice product |
| Payments | ⚠️ Partial | `patient-superbills` has `BillingStatus` field; no dedicated payment/ledger entities | Billing status tracked but no granular payment posting or patient ledger |
| Consents / directives | ✅ Covered | `patient-advance-directives` (5 fields), `patient-medication-history-consent` (3 fields), `patient-restrictions` (11 fields) | Advance directives, medication history consent, and service restrictions |
| Patient communications | ✅ Covered | `patient-messages` (13 fields), `patient-message-recipients` (6), `patient-message-attachments` (8) | In-app messaging with full thread tracking |
| Specialty-specific | N/A | Product is a general ambulatory EHR, not specialty-focused | No specialty modules to export |

**Domains covered**: 15 of 17 applicable domains (✅ or ⚠️)
**Full coverage**: 14 domains
**Partial coverage**: 2 domains (imaging, payments)
**Not applicable**: 1 domain (specialty-specific)

## 6. Documentation Quality

**Strengths:**

- **Complete field-level documentation**: Every one of the 1,194 fields has a name, data type, and plain-English description — 100% coverage
- **Clear entity organization**: 8 logical categories that map to clinical workflow domains
- **Entity descriptions**: Every entity has an h4 description explaining what it represents (e.g., "Data representing a patient's demographics in the Practice Fusion EHR")
- **Consistent data types**: 15 well-defined types including nullable variants (Guid?, DateTime?, Boolean?)
- **Publicly accessible**: No authentication, no paywall, clean URL structure
- **Active maintenance**: Six versions in 10 months (V1 through V6), latest January 2026

**Weaknesses:**

- **No relationship documentation**: The 335 Guid/Guid? fields clearly serve as foreign keys linking entities (e.g., `EncounterGuid` in `patient-encounter-diagnoses` links to `patient-encounters`), but these relationships are not formally documented. A developer would need to infer them from naming conventions
- **No value sets/code systems**: Fields like `BillingStatus`, `Gender`, `OrderStatus` are typed as String with no enumerated values or code system references
- **No sample data**: No example TSV files or sample records are provided
- **No machine-readable schema**: The documentation is HTML only — no JSON Schema, XML Schema, or other parseable format
- **Some descriptions are terse**: A few field descriptions are near-tautological (e.g., a field named `Status` described as "Status of the record"), though most are informative

**Overall**: A developer could build a working import pipeline from this documentation. The entity names, field names, and types are sufficiently clear to map the data model. The lack of explicit relationships and value sets would require some trial-and-error with actual export files.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of what Practice Fusion / Veradigm View stores. The 87 TSV entities span clinical encounters, medications, labs, billing/superbills, insurance, patient messaging, referrals, documents, questionnaires, and detailed demographics. The billing domain is particularly notable — 12 entities and 286 fields covering superbills, insurance policies, eligibility, guarantors, and billing procedure details. This goes well beyond USCDI, which doesn't address billing, insurance details, superbills, patient messaging, questionnaires, or referral workflows. For a small-practice ambulatory EHR, this is a credibly complete designated record set export. The only minor gaps (imaging as a standalone domain, granular payment posting) reflect features the product likely handles minimally or externally.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. The evidence is clear:
1. The export format (87 TSV files) maps directly to the product's internal database entities, not to any standard clinical exchange format
2. Entity names reference "Practice Fusion EHR" internally, confirming these are native data model entities
3. The export includes 12 billing/insurance entities (286 fields) and 3 messaging entities — data domains entirely absent from the product's (g)(10) FHIR API or C-CDA exchange
4. The data dictionary has 1,194 product-specific fields with product-specific types (Guid, Guid?, DateField) — not FHIR resource mappings or C-CDA section templates
5. Six versions in 10 months indicates genuine, ongoing engineering investment in the export

### Key Findings

1. **Genuine purpose-built EHI export with exceptional documentation coverage**: 87 entities, 1,194 fields, 100% of fields documented with name, type, and description. This is among the most thoroughly documented (b)(10) exports in ambulatory EHR products.

2. **Billing data is the deepest domain**: The 3 largest entities are all billing — `patient-superbills` (70 fields), `patient-insurances` (65 fields), `superbill-insurances` (51 fields). This decisively demonstrates the export goes beyond clinical exchange.

3. **Lab data model is exceptionally granular**: 15 entities covering the full order-to-result lifecycle with specimen tracking, observation-level diagnoses, and attached documents — more granular than most ambulatory EHR exports.

4. **Active development trajectory**: V1 (April 2025) → V6 (January 2026) shows continuous improvement, with the product adding entities and refining documentation over time.

5. **Missing formal relationships and value sets**: The 335 Guid-type fields clearly form an entity relationship graph, but these relationships are not documented, and coded fields lack enumerated value sets. This is the primary documentation gap.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   TSV (tab-separated values), 87 files
    Entities:        87
    Fields:          1,194
    Descriptions:    100% of fields have descriptions
    Sample data:     No
    Bulk export:     Yes (single patient or entire practice population)
    Domains covered: 15 of 17 applicable domains

### Bottom Line

Veradigm View / Practice Fusion delivers one of the stronger (b)(10) EHI exports among ambulatory EHR products. A patient or provider would get a usable, comprehensive copy of their data spanning clinical encounters, medications, labs, billing/superbills, insurance, messaging, and referrals — all in documented TSV format. The biggest gap is the lack of explicit entity relationships and value set documentation, which would make programmatic use of the data more challenging, but the structural coverage of the designated record set is credibly complete for this product's scope.
