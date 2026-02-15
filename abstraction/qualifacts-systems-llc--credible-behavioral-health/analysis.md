# EHI Export Analysis: Qualifacts Systems, LLC

**Product**: Credible Behavioral Health, Version 11
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3124.Cred.11.01.1.221230

## 1. Product Context

Credible Behavioral Health is a comprehensive, cloud-based EHR platform designed for behavioral health and human services organizations. Developed by Credible Behavioral Health Inc. (founded 2000) and now part of Qualifacts Systems, LLC, it targets large enterprise agencies, multi-site behavioral health organizations, and Certified Community Behavioral Health Clinics (CCBHCs).

The product is a full-featured EHR encompassing:
- **Clinical documentation**: Configurable forms, assessments (PHQ-9, CANS, ASAM, DLA-20), treatment planning, progress notes, clinical decision support
- **ePrescribing**: Including EPCS and PDMP integration
- **Billing & RCM**: Integrated HIPAA-compliant billing, claim scrubbing, denial management, state-specific billing rules
- **Residential/inpatient management**: Facility whiteboard, duty logs, room assignments, census
- **Client engagement**: Patient portal, telehealth (via OnCall integration), secure messaging
- **Scheduling**: Appointment scheduling with provider matching
- **Analytics**: Customizable dashboards, BI tools, quality measures

For EHI export assessment, the key data domains this product stores include: demographics, diagnoses, medications/prescriptions, allergies, immunizations, vitals, lab results, clinical notes, treatment plans, behavioral health assessments, billing/claims/payments, insurance/coverage, care plans, care coordination, attachments/documents, and residential/facility management data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `data-dictionary.json` (427 KB) | Complete data dictionary extracted from the Angular SPA's JavaScript bundle. Contains all 106 entities with 1,993 fields including field names, data types, nullability, example values, and descriptions. | **Primary artifact** — most informative |
| `credible-ehi-export.html` (13 KB) | Credible-specific EHI export documentation page describing Single Patient and Patient Population export processes, file format (NDJSON in ZIP), attachment handling, and data dictionary link. | **High** — describes export mechanics and format |
| `Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (149 KB, 3 pages) | Legal terms governing Patient Population EHI export requests. Dated September 2024. | **Low** — legal/administrative, no technical content |
| `ehi-export-index.html` (7 KB) | Qualifacts EHI Export hub page linking to platform-specific docs (CareLogic, Credible, InSync). Notes that FHIR API is a separate capability. | **Low** — navigation only |
| `data-dictionary-home.png` (147 KB) | Screenshot of data dictionary home page showing left sidebar with all entity menu items. | **Medium** — confirms entity count and navigation |
| `data-dictionary-claims.png` (200 KB) | Screenshot of Claims entity page showing sample JSON, field table with types, examples, descriptions. | **Medium** — confirms data dictionary format |
| `data-dictionary-allergies.png` (220 KB) | Screenshot of Allergies entity page — representative of clinical data documentation. | **Medium** — confirms format |
| `data-dictionary-profile.png` (159 KB) | Screenshot of Profile entity showing custom-fields-only entity. | **Medium** — confirms custom field handling |
| `data-dictionary-visit-service.png` (236 KB) | Screenshot of Visit Service entity — largest entity with 97 fields. | **Medium** — confirms format |
| `credible-ehi-export-page.png` (358 KB) | Full-page screenshot of Credible EHI export documentation. | **Low** — duplicate of HTML content |
| `ehi-export-index-page.png` (205 KB) | Screenshot of hub page. | **Low** — duplicate of HTML content |

## 3. Export Mechanics

**Format**: ZIP file containing Newline Delimited JSON (NDJSON) files. Each JSON file represents one data class (entity), with naming convention `Content{EntityName}.json` (e.g., `ContentClaims.json`, `ContentAllergies.json`). Attachments (documents, images) are included in their original file format with GUID filenames that map to records in `ContentClientAttachments.json`.

**Mechanism**: Two modes:
1. **Single Patient Export**: Initiated by designated agency staff within the Credible application after a patient/authorized representative requests it. Requests enter a processing queue. Qualifacts staff cannot perform this on behalf of agencies.
2. **Patient Population Export**: Requested by submitting a ticket through Qualifacts Care Center. Qualifacts staff initiate the process. Up to 30 calendar days to complete. Only one can be requested at a time. Requires agreement to Terms of Use.

**Access**: Completed exports are accessed via the Report Inbox on the Reports tab within Credible. Download links expire after 30 calendar days.

**Bulk capability**: Yes — Patient Population Export covers all patients.

**Fees/constraints**: Not stated in documentation. Terms of Use (September 2024, 3 pages) impose legal conditions including indemnification and liability limitations, but no fees are mentioned.

## 4. Export Content: What's In It

The data dictionary documents **106 entities** with **1,993 fields** in a vendor-native NDJSON format. This is not FHIR, C-CDA, or any standard — it is Credible's internal data model exported directly.

### Data dictionary quality metrics

| Metric | Value |
|---|---|
| Total entities | 106 |
| Total fields | 1,993 |
| Fields with any description | 1,993 (100%) |
| Fields with meaningful descriptions (beyond field name restatement) | 792 (39%) |
| Fields with tautological descriptions (restate field name) | 1,201 (60%) |
| Fields with example values | 1,991 (99.9%) |
| Data types documented | Yes (SQL-style: varchar, integer, datetime, decimal, etc.) |
| Nullability documented | Yes (1,352 nullable, 641 non-nullable) |
| Foreign key/relationships documented | No (implicit via shared ID fields; 97 of 106 entities have `Client Id`) |
| Value sets/code systems | No |
| Custom fields supported | 6 entities (3 custom-only, 3 with standard + custom fields) |

### Data type distribution

| Data Type | Count |
|---|---|
| varchar | 680 |
| integer | 345 |
| datetime | 207 |
| decimal | 165 |
| string | 125 |
| smallint | 87 |
| boolean | 74 |
| smalldatetime | 70 |
| bit | 62 |
| char | 62 |
| Other (tinyint, datetime2, nvarchar, date, double, float, etc.) | 116 |

### Vendor's own content organization

The data dictionary presents entities as a flat list without explicit categories. I have organized them by functional domain based on entity names and field content. The full inventory of all 106 entities is in `analysis/full-entity-inventory.json`.

**Domain breakdown**:

| Domain | Entities | Fields | Notes |
|---|---|---|---|
| Billing / Financial | 12 | 382 | Includes Liability (164 fields — the largest single entity), Claims, Payments, Statements |
| Medications / Prescribing | 10 | 293 | eRx Messages (101 fields), EMAR, medication management |
| Demographics / Profile | 14 | 226 | Including custom-only Profile and Profile Extended, family data |
| Clinical | 10 | 179 | Diagnoses, allergies, immunizations, implantable devices, procedures |
| Treatment Planning / BH | 16 | 178 | ASAM, Credible Plan, Treatment Plan, Questionnaires, Episodes |
| Administrative | 12 | 174 | Authorization, orders, enrollment, attachments |
| Visits / Encounters | 6 | 173 | Visit Service (97 fields with custom), encounters, scheduling |
| Insurance / Coverage | 5 | 126 | Insurance (50 fields), Eligibility (48 fields), payers |
| Communication / Messaging | 9 | 85 | Portal, Direct messages, notifications |
| Clinical / Labs | 2 | 47 | Lab Report, Lab Test Results |
| Residential / Facility | 3 | 43 | Foster Home, Bed Board notes |
| Clinical / Vitals | 1 | 40 | Medical Profile with height, weight, BMI, BP, pulse, temp, respiration |
| Notes / Documentation | 4 | 33 | Notes, amendments, warnings |
| Clinical / Notes | 1 | 8 | Clinical Notes |
| Clinical / Outcomes | 1 | 6 | Outcomes |

**Top 10 largest entities**:

| Entity | Fields | Domain | Meaningful Descriptions |
|---|---|---|---|
| Liability | 164 | Billing / Financial | 74 (45%) |
| eRx Messages | 101 | Medications / Prescribing | 39 (39%) |
| Visit Service | 97 | Visits / Encounters | 0 (0%) |
| Insurance | 50 | Insurance / Coverage | 5 (10%) |
| Eligibility | 48 | Insurance / Coverage | 2 (4%) |
| Medical Profile | 40 | Clinical / Vitals | 17 (43%) |
| Lab Test Results | 40 | Clinical / Labs | 10 (25%) |
| EMAR | 40 | Medications / Prescribing | 19 (48%) |
| Family Medical History | 39 | Demographics / Profile | 2 (5%) |
| Client Diagnosis | 37 | Clinical | 2 (5%) |

**Notable: 6 entities with 0 meaningful descriptions** (all descriptions restate field names):
- Visit Service (97 fields) — the 3rd largest entity
- Visit Service Claim Note (34 fields)
- 277 Response (9 fields)
- Visit Service Approval (7 fields)
- Visit Service Insurance (5 fields)
- Eligibility Message Details (2 fields)

**Custom fields**: Three entities are custom-only (Profile, Profile Extended, Episode) — their fields are agency-configurable and vary per installation. Three more entities (Medical Profile, Visit Service, Employee) include both standard and custom fields. The documentation correctly notes that custom fields cannot be pre-documented since they are defined by each agency's administrator.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around 106 data entities spanning the full breadth of Credible's data model. The strongest coverage areas are:

**Billing / Financial (12 entities, 382 fields)**: This is the deepest single domain. The Liability entity alone has 164 fields covering fee schedules, discounts, copays, deductibles, and payment calculations. Claims, Payments, PaymentPlan, Statement Header/Detail, and 277 Response provide thorough revenue cycle coverage. Bed Board Billing and Bed Board Billing Header cover residential billing.

**Medications / Prescribing (10 entities, 293 fields)**: Comprehensive ePrescribing coverage with eRx Messages (101 fields), EMAR and EMAR Reconciliation, Medication History, Request, Verification, Prior Authorization, and Notes.

**Treatment Planning / BH (16 entities, 178 fields)**: Reflects the behavioral health focus — ASAM Assessment, multiple treatment plan variants (Treatment Plan, Treatment Plan Plus with Details and Extended), Credible Plan (Header, Component, Custom Extended, Documentation, Signature), Questionnaire system, and Episodes. This is specialty-specific clinical data that would be absent from a FHIR-only export.

**Demographics / Profile (14 entities, 226 fields)**: Thorough demographics including profile history (previous addresses, previous names), family relationships, family medical history with detail records, education, contacts, and geographic area.

**Insurance / Coverage (5 entities, 126 fields)**: Deep insurance coverage including Insurance (50 fields), Eligibility (48 fields), Insurance Subscriber, Payer, and Insurance Visit Type.

**Thinnest areas**: Care Plan (1 field — just a reference), Care Team (3 fields), Immunizations (5 fields), Clinical Procedure (5 fields). These appear to be minimally-used features in the behavioral health context rather than documentation oversights.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Profile [custom], Profile Extended [custom], Contact (22), Family (31), Profile Previous Address (7), Profile Previous FullName (6), Education (36), Links (11) | Thorough; custom fields allow agency-specific demographic capture |
| Encounters / visits | ✅ Covered | Visit Service (97 fields +custom), Encounters (20), Visit Service Transportation (29), Visit Service Approval (7) | Very thorough; Visit Service is the primary encounter entity |
| Problems / conditions / diagnoses | ✅ Covered | Client Diagnosis (37), Client Diagnosis Detail (25), Visit Service Diagnosis (30), Medical Profile Conditions (9) | 101 fields across 4 entities — comprehensive |
| Medications / prescriptions | ✅ Covered | Medication Request (24), Medication History (34), eRx Messages (101), eRx Eligibility (20), EMAR (40), EMAR Reconciliation (23), Medication Verification (13), Medication Notes (5), Medication Prior Authorization (17), Medication List Reconciliation (16) | 293 fields across 10 entities — very thorough |
| Allergies | ✅ Covered | Allergies (16 fields: severity, reaction SNOMED, onset, created/discontinued dates) | Adequate for behavioral health |
| Immunizations | ⚠️ Partial | Immunizations (5 fields) | Minimal but reasonable for behavioral health — not a primary clinical workflow |
| Vitals | ✅ Covered | Medical Profile (40 fields: height, weight, BMI, BP systolic/diastolic in 3 positions, pulse, respiration, temperature, head circumference, percentiles) | Thorough vital signs coverage embedded in Medical Profile |
| Lab results | ✅ Covered | Lab Test Results (40 fields), Lab Report (7 fields) | 47 fields — solid coverage |
| Imaging / diagnostic reports | ⚠️ Partial | Overview Image (8 fields) | Limited but behavioral health has minimal imaging needs; N/A for most installations |
| Procedures | ⚠️ Partial | Clinical Procedure (5 fields) | Thin, but behavioral health is not procedure-heavy |
| Clinical notes / documents | ✅ Covered | Clinical Notes (8), Notes (9), Amendments (10), Warnings (9), Credible Plan Documentation (6), Attachments (13) | Notes content plus attachment system for documents |
| Care plans / goals | ✅ Covered | Care Plan (1), Care Team (3), Clinical Goal (24), Treatment Plan (13), Treatment Plan Plus (20+12+8), Credible Plan (Header 19 + Component 17 + Custom Extended 9 + Documentation 6 + Signature 11) | 143 fields across 12 entities — deep treatment planning, reflecting BH specialty |
| Orders / referrals | ✅ Covered | Orders (35), Order Notes (5), Authorization (33), Authorization Provider (3), Authorization Visit Type (3) | 79 fields — adequate |
| Insurance / coverage | ✅ Covered | Insurance (50), Insurance Subscriber (17), Insurance Visit Type (3), Payer (8), Eligibility (48), Enrollment (17) | 143 fields across 6 entities — very thorough |
| Claims / billing | ✅ Covered | Claims (19), Liability (164), Payments (20), PaymentPlan (18), Statement Header (32), Statement Detail (16), 277 Response (9), Funding Activity (13), Bed Board Billing (31), Bed Board Billing Header (21), Visit Service Claim Note (34), Visit Service Insurance (5) | 382 fields across 12 entities — exceptionally thorough |
| Payments | ✅ Covered | Payments (20), PaymentPlan (18), Statement Header/Detail (48) | Included within billing domain |
| Consents / directives | ❌ Not covered | No dedicated consent entity | Product likely captures consents as attachments or within portal; may be a minor gap |
| Patient communications / portal messages | ✅ Covered | Messaging (21), PortalQuestionnaire (11), Portal Questionnaire Signature (7), Direct Sent Message (14), Direct Received Message (11), Notification (6), Appointment Notification (9) | 79 fields across 7 entities — thorough |
| Specialty-specific (Behavioral Health) | ✅ Covered | ASAM Assessment (8), Questionnaire (11), Questionnaire Category (29), Questionnaire Signature (10), Outcomes (6), Episode [custom] (1), Treatment Plan Plus variants (40), Credible Plan variants (62), Bed Board Shift Notes (12), Bed Board Whiteboard Notes (6), FosterHome (25) | Deeply specialized for behavioral health — assessments, treatment planning, residential/facility, configurable questionnaires |

**Summary**: 14 of 18 domains are fully covered, 3 are partially covered (Immunizations, Imaging, Procedures — all appropriate for the behavioral health specialty), and 1 (Consents) is not explicitly represented. No significant EHI gaps exist relative to what this product stores.

## 6. Documentation Quality

**Strengths**:
- Purpose-built Angular SPA data dictionary at `b10export-docs.cbh4.crediblebh.com` with clean sidebar navigation across all 106 entities
- Every entity shows example JSON demonstrating exact output format
- Every field (1,993/1,993) has a data type, nullability flag, example value, and description
- Version-stamped (V20251217.1, dated December 17, 2025) indicating active maintenance
- Export format clearly documented: NDJSON in ZIP, with attachment handling for both Credible-hosted and partner-hosted files
- Custom fields handling is explicitly documented

**Weaknesses**:
- **Description quality is mixed**: 60% of descriptions (1,201 of 1,993) are tautological — they simply restate the field name (e.g., field "Batch Date" described as "Batch Date"). Only 39% (792) provide genuinely informative descriptions beyond the field name.
- **Visit Service** (97 fields, the 3rd largest entity) has **zero** meaningful descriptions — every description merely restates its field name.
- **No value set documentation**: Coded fields (e.g., claim statuses, visit types, severity levels) provide no enumeration of valid values. A developer would have to infer valid values from actual export data.
- **No relationship/foreign key documentation**: Entities share ID fields (97 of 106 entities have `Client Id`; many share `Visit Id`, `Claim Id`, etc.) but there is no explicit entity-relationship diagram or foreign key map. Relationships must be inferred from naming conventions.
- **No machine-readable schema**: No JSON Schema, OpenAPI spec, or XSD is provided. The data dictionary SPA is the only documentation source (with no download/export option — the JSON was extracted from the JavaScript bundle by the collection agent).
- **Date format inconsistency noted**: Some fields use ISO format (`2023-09-06T10:54:00`), others use US format (`5/3/2021 2:18:00 PM`).
- **No sample export ZIP**: No downloadable sample export is provided for developers to test against.

**Could a developer build an import?** Mostly yes, with effort. The human-readable field names (e.g., "Insurance Policy Number" rather than cryptic codes) and JSON format make the export accessible. The main challenges would be: (1) reconstructing entity relationships without explicit FK documentation, (2) interpreting coded fields without value sets, and (3) handling inconsistent date formats.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine (b)(10) export of Credible's native data model, not a repackaging of FHIR or C-CDA. Key evidence:
1. Uses vendor-defined NDJSON schema with SQL-style data types (varchar, smallint, decimal) — not FHIR resources
2. 106 entities with 1,993 fields — far beyond USCDI/US Core's ~20 resource types
3. Deep billing coverage (382 fields across 12 entities, including 164-field Liability entity)
4. Behavioral health specialty data (ASAM assessments, Credible Plans, questionnaires, residential/bed board) that has no FHIR equivalent
5. Custom agency-configurable fields are exported
6. The FHIR API is explicitly referenced as a separate capability on the hub page

### Key Findings

1. **Genuinely comprehensive export**: 106 entities with 1,993 fields covering clinical, billing, medications, insurance, behavioral health specialty, residential, and administrative data. This is one of the more thorough (b)(10) implementations, with particular depth in billing (382 fields) and medications (293 fields).

2. **Description quality is the main weakness**: While 100% of fields have descriptions, 60% are tautological (merely restating the field name). The Visit Service entity — the 3rd largest with 97 fields — has zero meaningful descriptions. This makes the documentation look more complete than it functionally is.

3. **No value sets or relationship documentation**: Coded fields lack enumeration of valid values, and entity relationships are implicit (via shared ID fields) rather than documented. This forces developers to reverse-engineer relationships and code meanings from actual export data.

4. **Behavioral health specialization is well-represented**: Treatment planning (16 entities, 178 fields), ASAM assessments, configurable questionnaires, residential facility management, and agency-specific custom fields demonstrate genuine EHI export rather than a generic clinical summary.

5. **Export process is functional but slow**: Single Patient export is self-service. Patient Population export requires a support ticket and up to 30 calendar days — a meaningful operational constraint for bulk data requests.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   NDJSON (Newline Delimited JSON) in ZIP
Model type:      Native database model
Entities:        106
Fields:          1,993
Descriptions:    100% have descriptions; 39% are meaningful (non-tautological)
Sample data:     No (example values in data dictionary, but no sample export ZIP)
Bulk export:     Yes (Patient Population Export via support ticket, up to 30 days)
Domains covered: 14 of 18 applicable domains fully covered; 3 partial; 1 not covered
```

### Bottom Line

Credible Behavioral Health provides a genuinely comprehensive EHI export covering its full native data model across clinical, billing, medications, insurance, and behavioral health specialty domains. A patient or provider would receive a substantially complete copy of their data. The main weaknesses are documentation quality (60% tautological descriptions, no value sets, no relationship documentation) rather than export completeness — the data is there, but the documentation doesn't fully explain it.
