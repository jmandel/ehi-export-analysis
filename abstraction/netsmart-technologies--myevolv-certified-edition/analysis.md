# EHI Export Analysis: Netsmart Technologies

**Product**: myEvolv Certified Edition  
**Analysis date**: 2026-02-17  
**CHPL IDs**: 11131 (15.04.04.2816.myEv.11.02.1.221227)

## 1. Product Context

myEvolv is Netsmart Technologies' **behavioral health and human services EHR** — a web-based, ONC-certified system serving community mental health, child and family services, intellectual/developmental disabilities (IDD), autism/ABA programs, addiction treatment (including MAT), Certified Community Behavioral Health Clinics (CCBHCs), foster care, and juvenile justice organizations. Netsmart is the largest vendor focused on behavioral health IT, serving 500,000+ users across 24,000+ organizations.

**Clinical capabilities**: Configurable clinical templates, structured assessments, progress notes, treatment planning, medication management (eMAR + e-prescribing via OrderConnect), immunization tracking, lab integration, vital signs, clinical decision support, and outcome tracking. Heavy emphasis on state-specific clinical documentation (NYSCRI for New York, MSDP for Massachusetts, BSAS for Massachusetts substance use, FASAMS for Florida, etc.).

**Billing/financial**: Automatic claim creation from clinical notes, multi-payer billing (Medicare, Medicaid, commercial), accounts receivable/pending, electronic claims submission, coordination of benefits, and integrated credit card payments. Revenue cycle management is a core selling point.

**Patient engagement**: Patient portal (certified (e)(1), (e)(3)) via myHealthPointe, secure messaging via CareConnect Inbox, appointment scheduling and reminders.

**Specialty capabilities**: ABA data collection (via RethinkBH), foster care management (milestones, certifications, placements), incident management (including restraints), substance use tracking, group therapy, and public health encounters.

The export should cover: clinical data (assessments, notes, medications, vitals, labs), behavioral health specialty data (ABA, substance use, foster care, incidents), billing/claims/payments, patient communications, treatment plans, and demographics/enrollment.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx` (11.2 MB) | 5-sheet XLSX: Events (1,679 rows), Events + Columns (115,663 rows), Non-Events (250 rows), Non-Events + Columns (21,006 rows), Info. **Primary artifact.** | ⭐⭐⭐ Most informative |
| `(1) myEvolv All EHI Export Companion Guide.docx` (939 KB) | 531-paragraph guide with configuration instructions, JSON format documentation, worked examples, glossary (42 field definitions), and type code legend (67 type codes). | ⭐⭐⭐ Most informative |
| `(3) myEvolv ALL EHI Export Queries.sql` (6.5 KB) | Four T-SQL queries agencies can run to generate their own data dictionary including custom forms/events. | ⭐⭐ Valuable |
| `myevolv_certification_status_letter_040425.pdf` (299 KB) | Certification status letter dated April 4, 2025. Lists certified criteria, costs, and additional software requirements. | ⭐ Supporting |
| `ehi-export-page-screenshot.png` (715 KB) | Screenshot of the EHI export landing page at ntst.com. | ⭐ Supporting |

## 3. Export Mechanics

- **Format**: JSON files packaged in ZIP archives. Files named `Bulk_Bundle_ID_N.json` within `EHI_Export_MMDDYYYYHHMM.zip`.
- **Mechanism**: UI-driven. Navigate to Reports > All EHI Exports > EHI Export, select the "Full EHI Export" template, choose parameters (all clients or specific clients), and run. The process is asynchronous and can take significant time.
- **Output delivery**: ZIP files deposited to a configured directory (local path for self-hosted, SFTP for Netsmart-hosted cloud instances).
- **Single-patient vs bulk**: Both supported. The UI allows filtering to specific client(s) or exporting all clients.
- **Access constraints**: Requires myEvolv subscription (priced by average daily census) plus one-time implementation fee. No separate cost for (b)(10) export — it's included in the base subscription.
- **Data model**: The export uses myEvolv's native "Print Bundle" infrastructure. A preconfigured template lists all eligible events and forms. Agencies can run a utility (`Populate EHI Export Print Bundle`) to automatically add any newly defined forms/events.

**JSON structure details** (from companion guide):
- Foreign key fields include both the GUID value (`field_id`) and human-readable description (`field_id_desc`), making data interpretable without access to the source system
- Attachments/images: base64-encoded with MIME type (`field_base64`, `field_mimeType`)
- Signatures: base64-encoded signature images
- Progress notes: nested arrays with note ID, content, author, duration, dates
- Subforms: nested arrays within parent records
- Assessments: nested structures with questions, answers, scores, and type codes

## 4. Export Content: What's In It

The XLSX data dictionary crosswalk is the definitive artifact. After deduplication (see methodology below), it documents:

- **1,565 unique entities** (form_codes): 1,314 event-type + 251 non-event-type
- **29,348 unique data concepts**: 3,114 database columns (across 83 tables) + 5,608 unique subform fields + 20,626 unique assessment questions
- **100%** of fields have captions (human-readable labels)
- **100%** of fields have type codes
- **97.3%** of fields have JSON property names (the remainder are assessment questions identified by GUID)

### Data model (per companion guide)

The companion guide describes two types of records in the JSON export:

1. **Event-based records** — date-based clinical encounters (allergies, vitals, medications, assessments, etc.). Each event is stored in a specific database table (e.g. `contacts`, `test_header`, `medication_history`). Identified by `event_definition_id`. A patient may have many records of the same event type.

2. **Form-based records (non-events)** — static, non-date-based records (demographics, addresses, insurance). Stored in the `people` table. No `event_definition_id`. Typically one per patient per form type.

Both types can embed:
- **Subforms**: nested child data arrays (e.g., Reactions/Symptoms within an Allergy record). Each subform is a reusable component identified by `subFormCode`.
- **Assessments (Tests)**: structured questionnaires with questions and answers, nested in the same pattern as subforms. Each question identified by `assessmentQuestionID`.

### Form/table relationship

Forms are *views* over database tables. The XLSX data dictionary crosswalk organizes data by form_code, but multiple forms can be different UI views over the same underlying table:

- **Event Category** (118 unique) → **Event Definition** (1,679 total) → **Form** (1,314 unique form_codes) → **Table** (83 unique)
- 107 of 1,314 forms are shared across 2+ event definitions
- 709 assessment form_codes all write to `test_header` (227 unique columns)
- 82 forms write to `contacts` (253 unique columns)
- **Non-events** (251 forms) are all views over the `people` table (217 unique columns)
- The XLSX repeats columns for each event_definition_id, and subforms/assessments are embedded in multiple parent forms, so raw row counts (136,669) far exceed unique data concepts (29,348)

### Deduplication methodology

The raw XLSX has 115,663 rows in Events + Columns and 21,006 in Non-Events + Columns (136,669 total). However:
1. When multiple event definitions share a form (e.g., BSAS_STAND_IE is used by 14 enrollment event types), fields are repeated N times
2. The Non-Events SQL query uses a UNION that can include print-bundle duplicates

The parse script (`analysis/parse-data-dictionary.ts`) deduplicates at three levels:
1. **Cross-event-definition**: filters to one event_definition_id per form_code (multiple event definitions share the same form)
2. **Cross-form table sharing**: many forms are *views* over the same database table (e.g., 707 assessment forms all write to `test_header`). Form-level fields are deduplicated by unique (table_name, jsonPropertyName) pairs
3. **Cross-entity subform/assessment sharing**: subforms and assessments are reusable components embedded in multiple parent forms; deduplicated by (subFormCode, subFormJsonPropertyName) and assessmentQuestionID respectively

This yields **29,348 unique data concepts**: 3,114 database columns (across 83 tables) + 5,608 unique subform fields + 20,626 unique assessment questions.

For reference, the intermediate counting levels show how duplication accumulates:
- Raw XLSX rows: 136,669
- After event-definition dedup (per-entity sum): 93,152
- After form-code scoping (but before table dedup): 53,469
- After full dedup to unique data concepts: **29,348**

### Unique data concepts by layer

| Layer | Unique Count | Methodology |
|---|---|---|
| Database columns | 3,114 | Unique (table_name, jsonPropertyName) across 83 tables |
| Subform fields | 5,608 | Unique (subFormCode, subFormJsonPropertyName) |
| Assessment questions | 20,626 | Unique assessmentQuestionID |
| **Total** | **29,348** | |

### Per-entity field level distribution (before cross-entity dedup)

| Level | Count | % |
|---|---|---|
| Form-level fields | 27,235 | 29.2% |
| Subform-level fields | 40,819 | 43.8% |
| Assessment-level fields (questions) | 25,098 | 27.0% |

### Type code distribution (top 10)

| Type Code | SQL Type | Count | % |
|---|---|---|---|
| FK (Foreign Key) | uniqueidentifier | 41,373 | 44.4% |
| TESTS (Assessment question) | — | 25,098 | 26.9% |
| L (Logical/Boolean) | bit | 5,701 | 6.1% |
| S (String) | varchar | 5,412 | 5.8% |
| D (Date Only) | datetime | 4,367 | 4.7% |
| DT (DateTime) | datetime | 2,593 | 2.8% |
| REMARKS | varchar(max) | 1,517 | 1.6% |
| N (Numeric) | float | 1,269 | 1.4% |
| INT (Integer) | int | 1,114 | 1.2% |
| TD (Time Duration) | int | 1,007 | 1.1% |

### Vendor's own content organization

#### Event categories (top 20 by field count)

| Category | Entities | Fields | Description |
|---|---|---|---|
| Test/Assessments for People - System | 245 | 21,388 | Standardized assessments (PHQ-9, GAD-7, CAGE, AUDIT, etc.) |
| Public Health Encounters | 88 | 14,256 | Public health clinic visits (reproductive health, cancer screening, maternal care) |
| State Reporting Forms | 110 | 10,650 | State-specific reporting (IL IMCANS, FL FASAMS, NY OASAS, etc.) |
| MSDP Tests and Assessments | 77 | 8,624 | Massachusetts Standardized Documentation Project assessments |
| Public Health Tests/Assessments for People | 304 | 7,961 | Public health screening tools |
| NYSCRI Test and Assessments | 45 | 5,279 | New York State Clinical Records Initiative assessments |
| HCBS-Activities | 45 | 3,562 | Home and Community-Based Services activities |
| NYSCRI Progress Notes | 20 | 1,826 | NYSCRI-formatted progress notes |
| State Reporting Requirements | 62 | 1,203 | State reporting data requirements |
| HCBS Test/Assessments | 21 | 1,100 | HCBS-specific assessments |
| MST Events | 13 | 975 | Multisystemic Therapy events |
| Medication History | 13 | 492 | Medication orders, prescriptions, reconciliation |
| Incidents Header | 6 | 476 | Incident reports and investigations |
| Activities | 8 | 458 | Clinical service activities |
| Referrals Made (to Programs or Out) | 6 | 333 | Outbound referrals |
| Lab Tests | 14 | 300 | Laboratory tests and results |
| Benefit Assignment | 3 | 281 | Insurance/benefit enrollment |
| Memberships/Placement in Profiles | 16 | 282 | Group/program memberships |
| Immunizations | 5 | 230 | Immunization records |
| System Consents | 19 | 195 | Consent records for data sharing |

*Full breakdown of all 118 event categories and 18 non-event form families available in `analysis/entity-inventory-summary.json`.*

#### Non-event form families (by field count)

| Form Family | Entities | Fields |
|---|---|---|
| Personal Information | 83 | 9,460 |
| State Reporting Personal Information | 6 | 304 |
| Public Health Formset Forms | 14 | 204 |
| Person Face Sheet and Reports | 29 | 140 |
| API Personal Information | 1 | 62 |
| People Maintenance | 1 | 25 |
| Sliding Fee Eligibility | 1 | 19 |
| Front Desk - Client Information | 2 | 8 |

#### Representative largest entities

| Form Code | Form Name | Fields | Category |
|---|---|---|---|
| IL_IMCANS_V3 | IL IMCANS V3 | 492 | State Reporting Forms |
| IL_IMCANS_V2 | IL IMCANS V2 | 461 | State Reporting Forms |
| WV_CC_V2 | WV CareConnection V2 | 378 | Test/Assessments |
| OHBH_PERSONAL | Ohio OHBH Personal Information | 366 | Personal Information (non-event) |
| MA_CA_3FINAL | MA Comprehensive Assessment V3 | 352 | MSDP Tests |
| PH_RH_PRESCR_VISIT | PH RH Prescriber Visit | 289 | Public Health Encounters |
| PA_CCRI | PA CCRI Dynamic | 262 | Personal Information (non-event) |
| BSAS_SEC35_IE | BSAS Section 35 Intake/Enrollment | 172 | State Reporting Forms |
| BSAS_STAND_IE | BSAS Standard Intake/Enrollment | 153 | State Reporting Forms |

#### Entities with 0 fields: presentation-layer panels, not data stubs

Of the 1,565 entities, **160 have zero fields** (1,405 have fields). These are **not** incomplete data forms — they are presentation-layer UI panels that display data aggregated from other tables rather than owning database columns themselves. They fall into two categories (per `analysis/entity-inventory-summary.json`):

1. **146 entities** are listed in the Non-Events sheet but excluded from the Non-Events + Columns query entirely (they don't match the `list_program='eventform.asp'` / `is_active=1` / `is_print_bundle=0` filter). Most are Public Health face sheets (100), Person Face Sheet panels (19), and other navigation/report forms.

2. **14 entities** appear in the Columns sheet but every row has `jsonPropertyName=NULL` — their `form_lines` are UI-only elements (FK lookup displays, hyperlinks, labels) that render data from other tables without mapping to a database column.

The significance for EHI completeness is not that these forms are "stubs waiting to be filled in," but that **the underlying data tables they display are not exported through any other form or event**. Notable examples:

| Form Code | Form Name | What it displays | Why it matters |
|---|---|---|---|
| PERS_MESSAGES | Person Messages | Messages from a messaging table | Product has patient portal (myHealthPointe) and CareConnect Inbox — message content is not exported |
| PERS_CLAIMS | Person Claims on File | Claims from billing tables | Product has extensive billing/RCM — claims data is not exported |
| PERS_CLAIMS_BALANCE | Person Claims Balance | Claim balances | Same billing gap |
| PERS_CLAIMS_90 | Person Claims on File 90 Days | Recent claims | Same billing gap |
| PERS_INV | Person Invoices on File | Invoices from AR tables | Invoice/payment data is not exported |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around myEvolv's native data model: **event-based records** (date-stamped clinical events) and **form-based records** (static demographic/administrative data).

**Strongest coverage areas:**
- **Assessments and screenings** (21,388 + 8,624 + 7,961 + 5,279 + 1,100 = 44,352 fields across 692 assessment entities): This is the deepest area, reflecting myEvolv's role as a behavioral health system with extensive standardized assessment instruments. Includes PHQ-9, GAD-7, AUDIT, CAGE, DAST, IMCANS, CANS, and hundreds of state-specific tools.
- **State reporting** (10,650 + 1,203 = 11,853 fields across 172 entities): Deep state-specific reporting forms for IL, FL, NY, MA, OH, CO, WA, WV, NH, PA, NE, IA, MS, KY, NM, AK, OR.
- **Public health** (14,256 + 7,961 = 22,217 fields across 392 entities): Comprehensive public health encounter and screening forms.
- **Demographics** (9,460 fields across 83 personal information entities): State-specific demographic forms with extensive fields.

**Well-covered clinical domains** (all counts from `analysis/entity-inventory-summary.json` domain_breakdown):
- Medications: 13 medication history entities (492 fields), 5 medication administration entities (83 fields), 3 PH medication administration (57 fields), 1 standing orders (4 fields) — note: the "Medication Adminstration" category has a typo in myEvolv's data model
- Allergies: 7 entities, 96 fields
- Immunizations: 5 entities, 230 fields
- Lab tests: 14 entities, 300 fields
- Vitals (Physical Characteristics): 2 entities, 43 fields
- Diagnoses: 6 entities, 132 fields
- Problems/Needs: 2 entities, 34 fields
- Treatment/Service Plans: 9 entities across 3 categories (67 fields total)
- Consents: 26 entities (7 general + 19 system), 287 fields
- Progress notes: 21 entities, 1,861 fields (20 NYSCRI progress notes + Care Manager Notes, plus nested progress note arrays in all events)

**Specialty behavioral health coverage:**
- ABA: 6 entities, 201 fields (data collection, sessions, services)
- Incident management: 10 entities across 5 categories, 518 fields
- Substance use: 1 entity, 25 fields
- Foster care/adoption: 12 entities across 4 categories, 174 fields (placement disruptions 6/96, placement history 3/58, permanency plan goals 2/20, adoption activities 1/0)
- MST events: 13 entities, 975 fields
- HCBS: 66 entities across 2 categories, 4,662 fields (45 activities + 21 assessments)

**Billing-adjacent coverage (present but limited):**
- Authorization requests: 1 entity, 30 fields
- Benefit assignments: 3 entities, 281 fields
- Income: 5 entities across 2 categories, 142 fields (2 income information + 3 monthly income)
- Sliding fee eligibility: 1 entity, 19 fields
- Client billing information: 1 non-event entity, 36 fields

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 83 Personal Information entities (9,460 fields), state-specific forms | Thorough: includes extensive state-specific demographic data |
| Encounters / visits | ✅ Covered | Activities (13 entities, 555 fields), Public Health Encounters (88 entities, 14,256 fields); all events inherently document encounters | Events are the core data model; comprehensive |
| Problems / conditions | ✅ Covered | Problems/Needs (2 entities, 34 fields), Diagnosis (6 entities, 132 fields) | Adequate |
| Medications / prescriptions | ✅ Covered | Medication History (13 entities, 492 fields), Medication Administration (5 entities, 83 fields), Standing Orders (1 entity, 4 fields) | Thorough: orders, administration, reconciliation |
| Allergies | ✅ Covered | 7 entities, 96 fields | Adequate |
| Immunizations | ✅ Covered | 5 entities, 230 fields | Thorough |
| Vitals | ✅ Covered | Physical Characteristics (2 entities, 43 fields); companion guide example shows height, weight, BMI, BP, pulse, respiration, temperature, SpO2 | Adequate |
| Lab results | ✅ Covered | 14 entities, 300 fields | Thorough |
| Procedures | ⚠️ Partial | No dedicated "procedures" category; procedures may be captured as Activities or within state reporting forms | No standalone procedures table; behavioral health systems typically have fewer procedure-centric workflows |
| Clinical notes / documents | ✅ Covered | Progress notes (21 entities, 1,861 fields), Letters (1 entity), Received Documents (1 entity); nested progress note arrays in all events | Notes embedded in events; document attachments base64-encoded |
| Care plans / goals | ✅ Covered | Treatment/Service Plans (9 entities, 67 fields across 3 categories), Permanency Plan Goals (2, 20 fields) | Adequate for BH treatment planning |
| Orders / referrals | ✅ Covered | Referrals (10 entities, 534 fields), Authorization Requests (1, 30 fields) | Thorough |
| Insurance / coverage | ⚠️ Partial | Benefit Assignment (3 entities, 281 fields), Sliding Fee Eligibility (1, 19 fields) | Benefit assignments capture payer info; no standalone insurance/coverage entity |
| Claims / billing | ❌ Not covered | PERS_CLAIMS, PERS_CLAIMS_BALANCE, PERS_CLAIMS_90 are presentation panels with 0 data columns — the underlying billing tables are not exported | **Significant gap.** Product has extensive billing/RCM capabilities (claims, AR/AP, payments). |
| Payments | ❌ Not covered | PERS_INV (Person Invoices) is a presentation panel with 0 data columns — the invoicing/AR tables are not exported | **Significant gap.** Product supports credit card payments and AR. |
| Consents / directives | ✅ Covered | 26 consent entities (287 total fields) | Thorough: includes treatment, info release, photo, electronic communication, HIE consents |
| Patient communications | ❌ Not covered | PERS_MESSAGES is a presentation panel with 0 data columns — the messaging table is not exported. Communication Log (8 fields) is a basic activity log, not threaded messages. CLIENT_LOGIN (8 fields) tracks portal enrollment status only. | **Genuine gap.** Product has patient portal (myHealthPointe), CareConnect Inbox secure messaging. Message content is not exported. |
| Specialty: Behavioral health assessments | ✅ Covered | 692 assessment entities across 5 categories (44,352 fields): system (245/21,388), MSDP (77/8,624), PH (304/7,961), NYSCRI (45/5,279), HCBS (21/1,100) | Exceptionally thorough |
| Specialty: Substance use treatment | ✅ Covered | Substance Use (1 entity, 25 fields), BSAS forms (enrollment/discharge), Smoking Status (1, 17 fields) | Thorough |
| Specialty: ABA / autism | ✅ Covered | ABA (6 entities, 201 fields): data collection, sessions, services | Thorough |
| Specialty: Foster care | ✅ Covered | 12 entities, 174 fields: Placement Disruptions (6/96), Placement History (3/58), Permanency Plan Goals (2/20), Adoption Activities (1/0 — presentation panel) | Good |
| Specialty: Incident management | ✅ Covered | 10 entities across 5 categories (518 total fields) covering header, medical exam, medications, physical findings, restraints | Thorough |

## 6. Documentation Quality

**Excellent.** This is among the best-documented EHI exports reviewed.

**Strengths:**
- The **companion guide** (531 paragraphs) provides step-by-step configuration, JSON format documentation with color-coded worked examples, a glossary of 42 common field names with definitions, and a type code legend mapping 67 type codes to SQL data types
- The **data dictionary crosswalk** (29,348 unique data concepts across 1,405 entities with fields) is machine-readable and provides field names, captions (human-readable labels), and type codes for every field
- The **SQL queries** allow agencies to generate their own crosswalk including custom forms, making the documentation extensible
- Foreign key fields in the export include `_desc` suffixes with human-readable values, making the JSON self-documenting
- Documentation explicitly dated (11/04/2024) and versioned ("_v2")

**Weaknesses:**
- No field-level **descriptions** beyond the caption (label). Captions are useful but not definitions — `severity_id` with caption "Allergic Reaction Severity" tells you the label but not valid values
- No **value sets or code lists** are documented. FK fields reference lookup tables but valid values are not enumerated
- No **relationship diagram** (ERD). Relationships are implicit through naming conventions (`belongs_to_event`, `service_track_event_id`) and the glossary, but not formalized
- No **sample export file** is provided as a standalone artifact (examples are embedded in the DOCX)
- The XLSX represents a "freshly installed" system — agency-specific customizations require running the SQL queries

**Could a developer build an import?** Largely yes. The combination of the JSON format documentation, type code legend, glossary, and data dictionary provides enough structure to parse and interpret most of the export. The main challenge would be resolving FK values without access to lookup tables.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export is impressively broad within its clinical and behavioral health domains — 1,405 entities with fields and 29,348 unique data concepts covering demographics, clinical encounters, medications, assessments, specialty BH data (ABA, substance use, incidents, foster care), and state reporting. However, there are **significant gaps in billing and patient communications**:

- Claims, charges, payments, and invoices: The export includes presentation-layer panels (PERS_CLAIMS, PERS_CLAIMS_BALANCE, PERS_INV) that display billing data in the UI, but these panels have no data columns — they render data from underlying billing tables that are not themselves included in the export. The product has extensive billing/RCM capabilities (claims creation, AR/AP, payments via CardConnect), making this a genuine gap in the designated record set.
- Patient messaging: PERS_MESSAGES is similarly a presentation panel that displays messages from a messaging table that is not exported. The product has a patient portal (myHealthPointe) and secure messaging (CareConnect Inbox).

The export covers billing-adjacent data well (authorization requests, benefit assignments, income, sliding fee eligibility) but omits the actual transactional billing records. This makes it "partial" rather than "comprehensive" — the clinical side is genuinely comprehensive, but billing and communications are missing.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange:
- Uses a **proprietary JSON format** that mirrors myEvolv's native data model (events, forms, subforms, assessments) — not FHIR or C-CDA
- Coverage vastly exceeds USCDI: 118 event categories, 88 database tables, specialty behavioral health data, state-specific reporting forms, foster care, ABA, incident management
- The EHI export page explicitly distinguishes this from their FHIR APIs
- Dedicated "Print Bundle" infrastructure with a purpose-built configuration template
- Base64-encoded binary data (images, documents, signatures) — not typical of clinical exchange exports
- SQL queries provided for agencies to extend the dictionary with custom forms

### Key Findings

1. **Massive, well-documented purpose-built export**: 1,405 entities with fields (29,348 unique data concepts across 83 database tables), plus a companion guide, glossary (42 terms), type code legend (67 types), and SQL queries for customization. This represents genuine (b)(10) effort.

2. **Billing records are not exported**: The UI has panels (PERS_CLAIMS, PERS_CLAIMS_BALANCE, PERS_CLAIMS_90, PERS_INV) that display billing data from underlying tables, but these are presentation-layer forms with no data columns — the actual billing/claims/invoice tables are excluded from the export entirely. Only billing-adjacent data (authorizations, benefit assignments, income) is included.

3. **Patient messaging is not exported**: PERS_MESSAGES is a presentation panel that displays messages, but the underlying messaging table is not exported. The product has patient portal (myHealthPointe, certified (e)(1)/(e)(3)) and secure messaging (CareConnect Inbox), but message content is excluded.

4. **Behavioral health specialty coverage is exceptional**: ABA (6 entities, 201 fields), incident management (10 entities, 518 fields), substance use, foster care (12 entities, 174 fields), MST therapy (13 entities, 975 fields), HCBS (66 entities, 4,662 fields), and state-specific reporting for 15+ states are all included with deep field coverage.

5. **Deduplication matters**: The raw XLSX has ~137K rows, but duplication exists at three levels: (a) shared forms across event definitions, (b) multiple forms viewing the same database table, (c) shared subforms/assessments across parent forms. The actual unique data concepts number 29,348 — about 21% of the raw row count. Analysts using the raw XLSX without deduplication would significantly overcount.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   JSON (proprietary, native data model)
    Entities:        1,565 (1,405 with fields; 1,314 event + 251 non-event)
    Fields:          29,348 unique data concepts (3,114 DB columns + 5,608 subform fields + 20,626 assessment questions)
    Descriptions:    100% have captions; 0% have narrative descriptions or value sets
    Sample data:     No (examples embedded in DOCX only)
    Bulk export:     Yes (all clients or filtered)
    Domains covered: 16 of 19 applicable domains

### Bottom Line

myEvolv's EHI export is a genuinely purpose-built, deeply documented system that excels at exporting clinical and behavioral health specialty data — 29,348 unique data concepts across 83 database tables and 1,405 form-level entities far exceeds what any clinical exchange standard provides. A patient or provider would get a thorough clinical record including assessments, medications, treatment plans, and specialty BH data. The biggest gaps are billing/claims/payment records and patient communications — the product stores this data (and even has UI panels to display it), but the underlying tables are excluded from the export.
