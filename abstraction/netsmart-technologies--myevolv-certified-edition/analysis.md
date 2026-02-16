# EHI Export Analysis: Netsmart Technologies

**Product**: myEvolv Certified Edition
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2816.myEv.11.02.1.221227

## 1. Product Context

myEvolv is Netsmart Technologies' **behavioral health and human services EHR** — a fully web-based, ONC-certified electronic health record designed for organizations serving specialized populations including community mental health, child and family services, intellectual/developmental disabilities (IDD), autism/ABA programs, addiction treatment (including MAT), CCBHCs, foster care, and juvenile justice.

The product includes comprehensive modules for:

- **Clinical documentation**: configurable assessments, progress notes, treatment plans, diagnoses, medications (eMAR, e-prescribing), allergies, immunizations, labs, vitals
- **Behavioral health-specific**: ABA data collection, MST events, substance use tracking, behavioral monitoring, state-specific clinical records (NYSCRI, MSDP)
- **Human services-specific**: foster care management, adoption activities, placement tracking, permanency plan goals, legal history
- **Billing/revenue cycle**: automatic claim creation, multi-payer billing (Medicare, Medicaid, commercial), electronic claims submission, AR/AP management, integrated credit card payments
- **Case management**: scheduling, referrals, care coordination across programs
- **Patient engagement**: portal access, secure messaging, telehealth
- **Mobile**: myEvolv Anywhere for community-based documentation

This establishes that a genuine (b)(10) export must cover clinical data, behavioral health/human services specialty data, and financial/billing data. The product also includes extensive state-specific reporting forms across multiple states.

## 2. Artifacts Reviewed

| Artifact | Description | Usefulness |
|---|---|---|
| `(2) myEvolv All EHI Export Data Dictionary Crosswalk.xlsx` (11.2 MB) | Massive XLSX with 5 sheets: Info, Events (1,679 rows), Events + Columns (115,663 rows), Non-Events (250 rows), Non-Events + Columns (21,006 rows). This is the primary data dictionary. | **Most informative** — the core artifact |
| `(1) myEvolv All EHI Export Companion Guide.docx` (939 KB) | Comprehensive guide covering export configuration, usage, JSON format interpretation with annotated examples, type code legend (50+ types), and glossary of 35+ common fields. Last updated 11/04/2024. | **Highly informative** — explains export mechanics and format |
| `(3) myEvolv ALL EHI Export Queries.sql` (6 KB) | Four T-SQL queries for agencies to generate their own crosswalk including user-defined events/forms | **Informative** — shows data model and self-service capability |
| `myevolv_certification_status_letter_040425.pdf` (299 KB) | Certification status letter dated April 4, 2025 confirming (b)(10) certification, listing all 38 certified criteria, CQMs, and cost structure | **Contextual** — confirms certification and practice type |
| `ehi-export-page-screenshot.png` (715 KB) | Screenshot of the EHI export page at ntst.com | **Minimal** — just confirms the download link |
| `myevolv-all-ehi-export-documentation_v2.zip` (11.1 MB) | ZIP archive containing the above three documents | Container for the documentation package |

## 3. Export Mechanics

- **Format**: Proprietary JSON files packaged in ZIP archives. Not FHIR, C-CDA, or any standard format — this is myEvolv's native data model serialized to JSON.
- **Mechanism**: UI-driven via Reports > All EHI Exports > EHI Export. Administrator selects "Full EHI Export" print bundle template, can filter by all clients or specific clients.
- **Single-patient vs bulk**: Supports both — can export all clients or filter to specific individuals.
- **Output**: ZIP files named `EHI_Export_MMDDYYYYHHMM.zip` containing size-limited JSON files named `Bulk_Bundle_ID_N.json`. Records are grouped by event type; a single patient's data may span multiple files.
- **Delivery**: Files deposited to a configured directory (local path for self-hosted, SFTP for Netsmart-hosted agencies).
- **Processing time**: Can take significant time depending on data volume; runs asynchronously with status tracking.
- **Self-service**: Agencies can run provided SQL queries against their database to generate their own crosswalk that includes user-defined forms/events not in the standard crosswalk.
- **Access constraints**: For Netsmart-hosted agencies, SFTP access requires opening a support case with the Plexus Hosting team. No mention of additional fees for the export itself beyond the myEvolv subscription.

## 4. Export Content: What's In It

### Data Dictionary Scope

The XLSX data dictionary crosswalk represents a "freshly installed myEvolv instance" — it documents all system-provided forms and events. Agencies can extend this with custom forms/events, discoverable via the provided SQL queries.

**Parsing results** (from `analysis/parse-data-dictionary.ts`):

| Metric | Count |
|---|---|
| Total entities (unique form codes) | 1,565 |
| Event entities | 1,314 |
| Non-event entities | 251 |
| Entities with fields | 1,405 |
| Entities with 0 fields | 160 |
| Total fields | 131,109 |
| Fields with captions | 131,109 (100%) |
| Fields with type codes | 131,109 (100%) |
| Form-level fields | 41,773 |
| Subform-level fields | 62,951 |
| Assessment-level fields | 26,385 |
| Unique database tables | 88 |
| Event categories | 118 |
| Non-event form families | 18 |

The raw XLSX contains 115,663 event column rows and 21,006 non-event column rows (136,669 total). After deduplication by form code and structuring into entity+fields, this yields 1,565 entities with 131,109 fields. The discrepancy is because the XLSX has one row per column per event-definition, and multiple event definitions can share the same form.

### JSON Export Format

Each record in the export contains:
- **Identification**: `x_form_code` (form identifier), `people_id` (patient), `key_value` (unique record ID), `event_definition_id` (for events)
- **Dates**: `actual_date` (start), `end_date` (end), in ISO 8601 format
- **Foreign keys**: Both the GUID (`field_id`) and human-readable description (`field_id_desc`) and prompt (`field_id_prompt`)
- **Attachments/images**: Base64-encoded with MIME type (`field_base64`, `field_mimeType`)
- **Signatures**: Base64-encoded images (`field_sig`, `field_mimeType`)
- **Progress notes**: Nested arrays with note ID, content, author, duration, dates
- **Subforms**: Nested arrays within parent records
- **Assessments**: Nested structures with questions, answers, scores, and field type codes

### Vendor's Content Organization

The data dictionary organizes content into **118 event categories** and **18 non-event form families**. Below are the top categories by field count (full inventory in `analysis/entity-inventory-full.json`):

**Event Categories (top 25 by field count):**

| Category | Entities | Fields | Notes |
|---|---|---|---|
| Public Health Encounters | 88 | 25,407 | TB, reproductive health, immunization visits |
| Test/Assessments for People - System | 245 | 22,315 | Hundreds of assessment instruments |
| State Reporting Forms | 110 | 17,916 | State-specific forms (MA, FL, NY, OH, CO, etc.) |
| MSDP Tests and Assessments | 77 | 9,473 | Massachusetts Standardized Documentation |
| Public Health Tests/Assessments | 304 | 7,961 | Public health screening tools |
| NYSCRI Test and Assessments | 45 | 5,829 | NY State Clinical Records Initiative |
| HCBS-Activities | 45 | 4,472 | Home/community-based services |
| NYSCRI Progress Notes | 20 | 3,020 | NY-specific progress notes |
| HCBS Test/Assessments | 21 | 1,917 | HCBS assessment forms |
| State Reporting Requirements | 62 | 1,203 | Multi-state reporting |
| MST Events | 13 | 1,078 | Multisystemic Therapy |
| Lab Tests | 14 | 745 | Lab orders and results |
| Activities - Other | 4 | 633 | Misc. clinical activities |
| Medication History | 13 | 595 | Medication records |
| Incidents Header | 6 | 476 | Incident management |
| Activities | 8 | 458 | Clinical activities |
| Placement Disruptions | 6 | 407 | Foster care placements |
| CDSS Notifications | 1 | 360 | Clinical decision support |
| Incident Physical Findings | 1 | 360 | Incident documentation |
| Referrals Made | 6 | 333 | Referral tracking |
| Post Discharge Follow Ups | 1 | 300 | Discharge follow-up |
| Memberships/Placement in Profiles | 16 | 296 | Program placement |
| Benefit Assignment | 3 | 281 | Insurance/benefit data |
| Placement and Treatment History | 3 | 272 | Placement tracking |
| Immunizations | 5 | 230 | Immunization records |

**Non-Event Form Families (with fields):**

| Form Family | Entities | Fields | Notes |
|---|---|---|---|
| Personal Information | 81 | 19,270 | Demographics, state-specific variants |
| State Reporting Personal Information | 4 | 608 | State reporting demographics |
| Public Health Formset Forms | 11 | 408 | Public health forms |
| Person Face Sheet and Reports | 3 | 280 | Face sheets |
| API Personal Information | 1 | 124 | API integration forms |
| People Maintenance | 1 | 50 | People record maintenance |
| Sliding Fee Eligibility | 1 | 38 | Financial eligibility |
| Front Desk - Client Information | 2 | 16 | Front desk forms |

**20 Largest Entities:**

| Entity | Form Code | Type | Category | Fields |
|---|---|---|---|---|
| BSAS Standard Intake/Enrollment Form | BSAS_STAND_IE | event | State Reporting Forms | 2,142 |
| PH RH Nurse Visit | PH_RH_NURSE_VISIT | event | Public Health Encounters | 1,885 |
| PH RH BCC Prescriber Visit | PH_RH_BCC_PR_VISIT | event | Public Health Encounters | 1,875 |
| PH RH Prescriber Visit | PH_RH_PRESCR_VISIT | event | Public Health Encounters | 1,584 |
| BSAS Standard Disenrollment Form | BSAS_STAND_DISENROLL | event | State Reporting Forms | 1,484 |
| PH Tuberculosis Main - Visit | PH_TB_VISIT | event | Public Health Encounters | 1,242 |
| Ohio OHBH Personal Information | OHBH_PERSONAL | non-event | Personal Information | 1,000 |
| BSAS Residential Intake/Enrollment | BSAS_RESI_IE | event | State Reporting Forms | 930 |
| NYSCRI Comprehensive Assessment V2 | NYSCRI_COMP_ASSESS_2 | event | NYSCRI Test/Assessments | 825 |
| BSAS Residential Disenrollment | BSAS_RESI_DISENROLL | event | State Reporting Forms | 765 |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers an extraordinarily broad set of data domains, reflecting myEvolv's dual role as a clinical EHR and a human services platform. The coverage can be grouped into several tiers:

**Tier 1 — Deep coverage (hundreds to thousands of fields):**
- **State reporting forms** (110 entities, 17,916 fields): Comprehensive state-specific documentation for MA (BSAS, EICS, ESP), NY (OASAS, NYSCRI), OH (OHBH, OBHIS), FL (FASAMS), CO (DACODS), PA (MHX, CCRI), WI, WA, AK, NE, KY, MI, and many more
- **Tests/assessments** (245+ system assessments, 22,315+ fields): Massive library of behavioral health assessment instruments
- **Demographics/personal information** (81 state-specific variants, 19,270 fields): From basic client demographics to complex state-specific intake forms
- **Public health encounters** (88 entities, 25,407 fields): Tuberculosis, reproductive health, immunization visits

**Tier 2 — Solid coverage (moderate field counts):**
- **Medications**: 13 history forms (595 fields), 5 administration forms (83 fields), standing orders
- **Labs**: 14 forms (745 fields)
- **Incidents**: 6 header + physical findings + restraints + medications (>1,000 fields total)
- **Treatment/service plans**: 6 forms (80 fields) plus service plan development, addendum
- **Referrals**: Made (6 forms, 333 fields), to agency (3 forms, 183 fields), status tracking
- **Benefit assignments/insurance**: 3 forms (281 fields) including self-pay
- **ABA/autism services**: Data collection (4 forms, 91 fields), sessions (90 fields)
- **MST events**: 13 forms (1,078 fields)
- **Foster care**: Adoption activities, placement disruptions (6 forms, 407 fields), permanency plan goals, placement/treatment history
- **Income information**: 2 forms (64 fields), monthly income (3 forms, 105 fields)

**Tier 3 — Present but thin:**
- **Allergies**: 7 forms (96 fields)
- **Diagnoses**: 6 forms (198 fields)
- **Problems/needs**: 2 forms (34 fields)
- **Vitals/physical characteristics**: 2 forms (43 fields)
- **Immunizations**: 5 forms (230 fields)
- **Consents**: 7 forms (110 fields) + 19 system consents (195 fields)
- **Smoking status**: 1 form (17 fields)
- **Pregnancy**: 1 form (20 fields)
- **Substance use**: 1 form (25 fields)
- **Letters/documents**: 1 form each (3 fields each — likely just metadata with base64 content)

**Financial/billing-adjacent data present:**
- `Client Billing Information` (CLI_BILL_INFO): 72 fields (non-event)
- `Benefit Assignment` / `Self Pay` / `Benefit Assignment - This Agency`: 281 fields
- `Authorization Requests`: 30 fields
- `Income Information`: 64 fields
- `Monthly Income`: 105 fields
- `Sliding Fee Eligibility`: 38 fields
- `Resources and Liabilities`: 25 fields

**Notably absent from the export:**
- No explicit claims, charges, payments, or accounts receivable tables. While the product has extensive billing/revenue cycle capabilities (automatic claim creation, multi-payer billing, AR/AP management), the export contains billing-adjacent data (authorizations, benefit assignments, income, sliding fee eligibility) but not the actual transactional billing records (claims submitted, charges, payments received, remittance data, EOBs).
- `Person Claims Balance`, `Person Claims on File`, `Person Claims on File 90 Days`, and `Person Invoices on File` entities exist in the data dictionary but have **0 fields** — they are empty form stubs.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 81 Personal Information forms (19,270 fields), state-specific variants for 15+ states | Exceptionally thorough; includes race, ethnicity, language, contacts, identifiers |
| Encounters / visits | ✅ Covered | Events are inherently encounter-based; 88 Public Health Encounters (25,407 fields), Activities (458 fields), HCBS-Activities (4,472 fields) | All clinical events include encounter metadata (dates, staff, location) |
| Problems / conditions / diagnoses | ✅ Covered | Diagnosis (6 forms, 198 fields), Problems/Needs (34 fields) | Solid coverage |
| Medications / prescriptions | ✅ Covered | Medication History (13 forms, 595 fields), Medication Administration (5 forms, 83 fields), Standing Orders (4 fields), plus Public Health Medication Administration (119 fields) | Good depth including administration records |
| Allergies | ✅ Covered | Allergies (7 forms, 96 fields) with subforms for reactions/symptoms | Well-structured |
| Immunizations | ✅ Covered | Immunizations (5 forms, 230 fields) plus Public Health immunization encounters | Good coverage |
| Vitals | ✅ Covered | Physical Characteristics (2 forms, 43 fields); companion guide example shows height, weight, BMI, BP, pulse, respiration, temperature, SpO2, blood glucose, pain scale, O2 flow | Detailed vital signs |
| Lab results | ✅ Covered | Lab Tests (14 forms, 745 fields) | Good coverage |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging entity; may be captured via Received Documents or clinical notes | Product likely has limited imaging; not a major gap for BH/HS |
| Procedures | ⚠️ Partial | No dedicated procedures table; clinical procedures likely captured within Activities events | BH/HS has fewer discrete procedures than acute care |
| Clinical notes / documents | ✅ Covered | NYSCRI Progress Notes (20 forms, 3,020 fields), Care Manager Notes (140 fields), Letters (3 fields), Received Documents (3 fields); progress notes embedded as nested arrays in all events | Thorough — notes are woven into the event model |
| Care plans / goals | ✅ Covered | Treatment/Service Plans (6 forms, 80 fields), Service Plan Development (12 fields), Service Plan Addendum (9 fields), Permanency Plan Goals (20 fields) | Solid for BH/HS model |
| Orders / referrals | ✅ Covered | Referrals Made (6 forms, 333 fields), Referrals to Agency (3 forms, 183 fields), Referral Status (18 fields), Authorization Requests (30 fields) | Good coverage |
| Insurance / coverage | ✅ Covered | Benefit Assignment (3 forms, 281 fields), Client Billing Information (72 fields), Sliding Fee Eligibility (38 fields), state-specific insurance forms | Covers enrollment and eligibility well |
| Claims / billing | ⚠️ Partial | Authorization Requests (30 fields), Client Billing Information (72 fields); but no claims, charges, payments, remittance, or AR/AP tables. `Person Claims Balance`, `Person Claims on File`, `Person Invoices on File` entities exist but have 0 fields | **Significant gap** — product has extensive billing/RCM capabilities but transactional billing records appear absent |
| Payments | ❌ Not covered | No payment, remittance, or EOB entities | Product handles payments (CardConnect integration); gap |
| Consents / directives | ✅ Covered | Consents (7 forms, 110 fields), System Consents (19 forms, 195 fields), Disclosures (2 forms, 32 fields) | Thorough |
| Patient communications / portal messages | ❌ Not covered | No portal messages, secure messaging, or patient communication entities | Product has myHealthPointe portal and messaging; gap but may not be part of designated record set |
| Specialty: Behavioral Health | ✅ Covered | Hundreds of BH assessments, MST events (1,078 fields), state-specific clinical records, progress notes | **Exceptional** — the core strength |
| Specialty: Substance Use/Addiction | ✅ Covered | Substance Use (25 fields), MAT demographics (190 fields), BSAS forms (MA), CalOMS (CA), multiple state-specific addiction forms | Deep coverage |
| Specialty: ABA/Autism | ✅ Covered | ABA Data Collection (4 forms, 91 fields), ABA Session (90 fields), ABA Service (20 fields) | Purpose-built for ABA workflows |
| Specialty: Foster Care/Child Services | ✅ Covered | Adoption Activities, Placement Disruptions (407 fields), Placement and Treatment History (272 fields), Permanency Plan Goals (20 fields), Family Case Activities (137 fields) | Deep child welfare coverage |
| Specialty: IDD/HCBS | ✅ Covered | HCBS Activities (45 forms, 4,472 fields), HCBS Assessments (21 forms, 1,917 fields), prior authorizations | Good HCBS coverage |
| Specialty: Public Health | ✅ Covered | 88 PH Encounter forms (25,407 fields), 304 PH Assessments (7,961 fields), PH Activities (114 fields), PH Medication Administration (119 fields) | Very deep |

## 6. Documentation Quality

The documentation is **exceptionally well-structured** and among the best EHI export documentation reviewed:

**Strengths:**
- **Companion guide** is thorough: 29+ pages covering configuration, usage, JSON format, worked examples with color-coded annotations, complete type code legend (50+ types with SQL equivalents), and glossary of 35+ common field names
- **Data dictionary crosswalk** is massive (136,669 raw rows) with 100% of fields having captions and type codes
- **Self-service SQL queries** allow agencies to generate their own crosswalk including custom content — this is a rare and valuable feature
- **JSON export format** is well-designed: foreign keys include both GUIDs and human-readable descriptions (`_desc`), attachments are base64-encoded with MIME types, subforms and assessments are properly nested
- **Documentation is current** (last updated November 2024)

**Weaknesses:**
- **No field-level descriptions** beyond captions — fields have names and type codes but no prose descriptions of what they contain or their business meaning (beyond the 35-field glossary)
- **No value sets or coded values** documented — foreign key fields reference lookup tables but the valid values are not enumerated
- **No sample data files** included in the documentation package
- **No entity relationships** documented beyond what's implicit in subform nesting and foreign keys
- **No ERD or data model diagram**
- The crosswalk represents a "fresh install" — actual deployments will have additional user-defined content

**Could a developer build an import?** Partially. The combination of the companion guide, type code legend, glossary, and the massive crosswalk provides enough context to parse the JSON and understand most fields. However, the lack of value set documentation for foreign keys, and the absence of explicit relationship documentation, would require significant reverse-engineering for a complete import. The self-service SQL queries are a useful workaround for agencies with database access.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export covers an impressive breadth of data domains reflecting myEvolv's position as a behavioral health and human services EHR. With 1,405 entities containing 131,109 fields across 88 database tables, the export extends far beyond USCDI into specialty clinical data (ABA, MST, substance use, foster care, HCBS, public health), administrative data (referrals, enrollment, authorizations, placements), and state-specific reporting forms for 15+ states. The sheer volume of assessment instruments (245+ system assessments with 22,315 fields) reflects the deep behavioral health focus of the product.

The one notable gap is **transactional billing data** — while billing-adjacent records (authorizations, benefit assignments, income, sliding fee eligibility) are present, actual claims, charges, payments, and AR/AP records are absent despite the product having extensive billing capabilities. The presence of empty form stubs for `Person Claims Balance`, `Person Claims on File`, and `Person Invoices on File` (0 fields each) suggests these were considered but not implemented. This is a meaningful gap but does not outweigh the extraordinary clinical and specialty data coverage.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built EHI export. Key indicators:
1. **Proprietary JSON format** that directly reflects myEvolv's internal data model (events, forms, subforms, assessments) — not FHIR, C-CDA, or any existing clinical exchange format
2. **Dedicated export tool** (Print Bundle-based) with its own configuration, UI, and asynchronous processing
3. **Coverage extends far beyond USCDI/g(10)** — 118 event categories vs. the ~20 USCDI data classes; includes foster care, ABA, incidents, MST, state reporting, HCBS, and other domains never present in clinical exchange
4. **Data dictionary crosswalk** is product-specific (136,669 rows mapping to myEvolv's internal schema)
5. **Self-service SQL queries** for agency-specific customization
6. The documentation explicitly names this "All EHI Export" and describes it as exporting "all forms and events potentially entered onto a patient's chart"

### Key Findings

1. **Exceptionally deep behavioral health and human services coverage**: 1,405 entities with 131,109 fields across 88 tables — this is one of the most comprehensive EHI data dictionaries reviewed. The export covers ABA data collection, MST therapy, foster care/adoption, HCBS, public health, and state-specific reporting for 15+ states.

2. **Purpose-built export with well-designed documentation**: The companion guide, massive XLSX crosswalk, type code legend, glossary, and self-service SQL queries form a coherent, professional documentation package. The JSON format preserves human-readable descriptions alongside GUIDs, making the export interpretable without access to the source system.

3. **Billing gap despite billing-adjacent data**: The product has extensive billing/RCM capabilities, but the export omits actual claims, charges, payments, and AR/AP records. Empty form stubs (`Person Claims Balance`, `Person Claims on File`, `Person Invoices on File` with 0 fields) suggest this gap was noticed but not addressed.

4. **State-specific forms are a significant portion of the export**: 110 state reporting forms with 17,916 fields — this reflects myEvolv's deployment across behavioral health agencies in many states and demonstrates the product truly exports the full breadth of its clinical documentation.

5. **No sample data or value set documentation**: While field names and types are fully documented, the absence of sample data files, value set enumerations, and explicit relationship documentation limits the export's usability for data migration purposes.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   JSON (proprietary, ZIP-packaged)
Entities:        1,565 (1,405 with fields)
Fields:          131,109
Descriptions:    100% have captions and type codes; 0% have prose descriptions
Sample data:     No
Bulk export:     Yes (all clients or filtered)
Domains covered: 18 of 20 applicable domains
```

### Bottom Line

myEvolv's EHI export is a genuine, purpose-built effort that covers the extraordinary breadth of a behavioral health and human services EHR — from ABA session data to foster care placements to state-specific reporting forms across 15+ states. The 131,109-field data dictionary is among the most comprehensive reviewed. The primary gap is transactional billing data (claims, charges, payments), which is absent despite the product's billing capabilities — a meaningful but not disqualifying omission given the strength of the clinical and specialty coverage.
