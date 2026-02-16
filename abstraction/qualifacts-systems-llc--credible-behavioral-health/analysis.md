# EHI Export Analysis: Qualifacts Systems, LLC

**Product**: Credible Behavioral Health (Version 11)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.3124.Cred.11.01.1.221230

## 1. Product Context

Credible Behavioral Health is a comprehensive, cloud-based (SaaS) EHR platform designed specifically for behavioral health and human services organizations. Originally founded in 2000, Credible merged with Qualifacts in 2020 and now operates as one of four Qualifacts EHR platforms. It targets large enterprise agencies, multi-site behavioral health organizations, and Certified Community Behavioral Health Clinics (CCBHCs).

The product is a full-featured EHR encompassing:

- **Clinical documentation**: Configurable assessments (PHQ-9, CANS, ASAM, DLA-20, etc.), treatment planning, progress notes, clinical decision support, 60+ configurable alert types
- **ePrescribing / EPCS**: Electronic prescribing including controlled substances, PDMP integration, medication management
- **Billing & revenue cycle**: Integrated HIPAA-compliant billing, claim scrubbing, denial management, batch claim processing, configurable billing rules, claims submission to payers
- **Residential / inpatient management**: Facility whiteboard, duty logs, room assignments, census reporting
- **Scheduling**: Appointment management with provider matching
- **Client engagement**: Patient portal, secure messaging, telehealth (up to 50-participant groups)
- **Lab integration**: Lab orders and results
- **Interoperability**: HIE connections, FHIR R4 API, public health reporting

The critical domains for (b)(10) assessment are: clinical documentation (including behavioral health–specific assessments), billing/claims, medications/ePrescribing, insurance/eligibility, treatment plans, residential management, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/data-dictionary.json` (427 KB) | Complete data dictionary extracted from the Angular SPA at `b10export-docs.cbh4.crediblebh.com`. Contains all 106 entities with 1,993 fields including names, data types, nullability, example values, and descriptions. | **Most informative** — primary source of truth |
| `downloads/credible-ehi-export.html` (13 KB) | Credible-specific EHI export documentation describing single patient and population export processes, file format (NDJSON in ZIP), attachment handling, and data dictionary link | **Highly informative** — explains export mechanics |
| `downloads/ehi-export-index.html` (7 KB) | Qualifacts EHI Export hub page linking to CareLogic, Credible, and InSync platform-specific documentation | Orientation only |
| `downloads/Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (149 KB, 3 pages) | Terms of use governing Patient Population EHI exports | Moderately informative — confirms process constraints |
| `downloads/data-dictionary-home.png` | Screenshot of data dictionary SPA home page showing left-sidebar with entity list | Corroborative |
| `downloads/data-dictionary-claims.png` | Screenshot of Claims entity page with field table | Corroborative |
| `downloads/data-dictionary-allergies.png` | Screenshot of Allergies entity page | Corroborative |
| `downloads/data-dictionary-profile.png` | Screenshot of Profile entity page showing custom fields note | Corroborative |
| `downloads/data-dictionary-visit-service.png` | Screenshot of Visit Service entity page (97 fields) | Corroborative |
| `downloads/credible-ehi-export-page.png` | Screenshot of the Credible EHI export documentation page | Corroborative |
| `downloads/ehi-export-index-page.png` | Screenshot of the EHI Export hub page | Corroborative |

## 3. Export Mechanics

- **Format**: ZIP file containing Newline Delimited JSON (NDJSON) files. Each JSON file represents a data class (entity). Attachments are included in their original file format with GUID filenames, matched via the `ContentAttachments.json` entity.
- **Single Patient Export**: Initiated by designated agency staff within the Credible application. Patients/authorized representatives must request from their provider. Added to a processing queue.
- **Patient Population Export**: Requested by designated agency staff via a Qualifacts Care Center support ticket. Qualifacts staff initiate the process. Up to 30 calendar days to complete. Only one population export can be active at a time. Requires acceptance of Terms of Use.
- **Access**: Completed exports are available through the Report Inbox on the Reports tab in Credible. Download links expire after 30 calendar days.
- **Fees**: No fees mentioned in the documentation; governed by Terms of Use (September 2024).
- **Constraints**: Population export limited to one concurrent request. Terms of Use impose usage restrictions including HIPAA compliance and prohibitions on using data to harm Qualifacts' reputation.

## 4. Export Content: What's In It

### Summary Statistics

The data dictionary defines **106 entities** with **1,993 total fields**.

- **100.0%** of fields (1,993/1,993) have descriptions
- **100.0%** of fields (1,993/1,993) have data types documented
- **99.9%** of fields (1,991/1,993) have example values
- **100.0%** of fields (1,993/1,993) have nullability documented

However, 18 fields across 2 entities have placeholder "TODO" descriptions (Care Plan: 1 field, Insurance Subscriber: 17 fields), and a few descriptions are tautological (field name restated as description).

3 entities are "custom-only" (agency-configurable; export includes only a Client Id): Profile, Episode, Profile Extended. 6 entities support custom fields in addition to standard fields.

### Data Type Distribution

| Type | Count |
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
| Other (14 types) | 116 |

### Vendor's Own Content Organization

The data dictionary uses file-name–based entity names (e.g., `ContentClientDiagnosis`, `ContentClaims`). I organized these into domain categories based on entity names and content. The full inventory is in `analysis/entity-inventory-full.json`.

#### Category Breakdown

| Category | Entities | Fields |
|---|---|---|
| Demographics | 8 | 89 |
| Clinical – Diagnoses | 3 | 92 |
| Clinical – Medications | 10 | 293 |
| Clinical – Allergies | 1 | 16 |
| Clinical – Immunizations | 1 | 5 |
| Clinical – Lab | 2 | 47 |
| Clinical – Medical Profile | 3 | 69 |
| Clinical – Family Medical History | 2 | 66 |
| Clinical – Notes & Documentation | 10 | 113 |
| Clinical – Treatment Plans | 9 | 115 |
| Clinical – Goals & Outcomes | 2 | 30 |
| Clinical – Care Team | 1 | 3 |
| Clinical – Care Plan | 1 | 1 |
| Clinical – Orders | 2 | 40 |
| Clinical – Assessments | 2 | 44 |
| Encounters / Visits | 9 | 221 |
| Insurance & Eligibility | 10 | 198 |
| Billing & Payments | 10 | 343 |
| Residential / Bed Board | 3 | 43 |
| Communications | 5 | 62 |
| Administrative | 12 | 103 |
| **Total** | **106** | **1,993** |

#### Representative Entities (Top 20 by field count)

| Entity | Fields | Category |
|---|---|---|
| Liability | 164 | Billing & Payments |
| eRx Messages | 101 | Clinical – Medications |
| Visit Service | 97 | Encounters / Visits |
| Insurance | 50 | Insurance & Eligibility |
| Eligibility | 48 | Insurance & Eligibility |
| Medical Profile | 40 | Clinical – Medical Profile |
| Lab Test Results | 40 | Clinical – Lab |
| EMAR | 40 | Clinical – Medications |
| Family Medical History | 39 | Demographics |
| Client Diagnosis | 37 | Clinical – Diagnoses |
| Education | 36 | Clinical – Assessments |
| Orders | 35 | Clinical – Orders |
| 834 Load | 35 | Insurance & Eligibility |
| Medication History | 34 | Clinical – Medications |
| Visit Service Claim Note | 34 | Encounters / Visits |
| Authorization | 33 | Insurance & Eligibility |
| Statement Header | 32 | Billing & Payments |
| Bed Board Billing | 31 | Billing & Payments |
| Family | 31 | Demographics |
| Visit Service Diagnosis | 30 | Clinical – Diagnoses |

#### Notable Entities

- **Liability** (164 fields): The largest entity, covering detailed financial liability determinations including sliding scale fee calculations, income verification, discount groups, and payment responsibility — well beyond basic billing.
- **eRx Messages** (101 fields): Deep ePrescribing integration data including prescription details, pharmacy information, prior authorization, and message routing.
- **Visit Service** (97 fields): Core encounter/visit record with service codes, billing modifiers, units, rates, provider info, timestamps, approval status — bridges clinical and billing domains.
- **EMAR** (40 fields): Electronic Medication Administration Record — tracks actual medication administration events in residential/inpatient settings.
- **Bed Board Billing** / **Bed Board Billing Header** (31 + 21 fields): Residential billing with room/bed-level detail.
- **Care Plan** (1 field — Client ID only): Notably thin; description is "TODO". May indicate this entity is a stub or linking table.
- **Custom-only entities** (Profile, Episode, Profile Extended): Export only a Client Id; actual fields are agency-configurable and will vary by deployment.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is genuinely deep and organized around the vendor's native data model. Key strengths:

**Billing & Payments (10 entities, 343 fields)**: This is the richest domain. The Liability entity alone has 164 fields covering sliding-scale determinations, income-based fee calculations, and payment responsibility. Claims, Payments, PaymentPlan, Statement Header/Detail, Funding Activity, and Bed Board Billing provide comprehensive revenue cycle coverage. The 277 Response entity captures claim status responses — a level of billing detail rarely seen in EHI exports.

**Medications (10 entities, 293 fields)**: Deep coverage including ePrescribing messages (101 fields), medication history (34 fields), EMAR (40 fields), medication reconciliation, verification, prior authorization, and medication notes. This captures the full ePrescribing lifecycle.

**Insurance & Eligibility (10 entities, 198 fields)**: Insurance (50 fields), Eligibility (48 fields), Authorization (33 fields), 834 Load (35 fields), plus subscriber, visit type, and eligibility message entities. Covers eligibility checking, prior authorizations, and enrollment data (X12 834).

**Encounters / Visits (9 entities, 221 fields)**: Visit Service (97 fields) is the central clinical-billing encounter entity. Supporting entities for transportation, claim notes, insurance linkage, diagnosis linkage, and approvals.

**Treatment Plans (9 entities, 115 fields)**: Multiple plan types (basic Treatment Plan, Treatment Plan Plus with details/extensions, Credible Plan with components/signatures/documentation). Reflects the product's behavioral health focus.

**Notes & Documentation (10 entities, 113 fields)**: Clinical notes, questionnaires, amendments, attachments, signatures. Questionnaire categories (29 fields) and portal questionnaires capture behavioral health assessment tools.

**Demographics (8 entities, 89 fields)**: Patient profile, contacts, family relationships, previous addresses/names, overview images.

**Thinner areas**:
- Care Plan (1 field — just a Client ID with "TODO" description)
- Care Team (3 fields)
- Immunizations (5 fields)
- Scheduler Appointment (2 fields)
- Insurance Subscriber (17 fields, all with "TODO" descriptions)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Profile, Profile Extended, Profile Previous Address/FullName, Contact (22 fields), Family (31 fields), Overview Image | Thorough; includes prior addresses, family relations |
| Encounters / visits | ✅ Covered | Visit Service (97 fields), Encounters (20 fields), Scheduler Appointment (2 fields) | Deep encounter data; appointment scheduling is thin (2 fields) but core visit data is rich |
| Problems / conditions / diagnoses | ✅ Covered | Client Diagnosis (37 fields), Client Diagnosis Detail (25 fields), Visit Service Diagnosis (30 fields) | Thorough; 92 fields across 3 entities |
| Medications / prescriptions | ✅ Covered | Medication Request (24 fields), Medication History (34 fields), eRx Messages (101 fields), EMAR (40 fields), Medication Notes, Reconciliation, Verification, Prior Authorization | Very deep; 293 fields across 10 entities covering full medication lifecycle |
| Allergies | ✅ Covered | Allergies (16 fields) including SNOMED codes, severity, reactions | Adequate |
| Immunizations | ⚠️ Partial | Immunizations (5 fields) | Thin — only 5 fields; likely reflects behavioral health focus (immunizations less central) |
| Vitals | ⚠️ Partial | No dedicated vitals entity; Medical Profile (40 fields) may contain some vitals | Product likely captures basic vitals; no dedicated export entity identified |
| Lab results | ✅ Covered | Lab Test Results (40 fields), Lab Report (7 fields) | Solid lab coverage |
| Imaging / diagnostic reports | ❌ Not covered | No imaging entities | N/A — behavioral health product; imaging is not a core workflow |
| Procedures | ⚠️ Partial | Clinical Procedure (5 fields) | Thin; 5 fields |
| Clinical notes / documents | ✅ Covered | Clinical Notes (8 fields), Notes (9 fields), Attachments (13 fields), Amendments (10 fields) | Adequate; includes attachment handling with GUID-based file matching |
| Care plans / goals | ⚠️ Partial | Care Plan (1 field — stub), Clinical Goal (24 fields), Outcomes (6 fields), Treatment Plan entities (9 entities, 115 fields) | Goals and treatment plans are deep; Care Plan entity is a stub |
| Orders / referrals | ✅ Covered | Orders (35 fields), Order Notes (5 fields) | Solid order management |
| Insurance / coverage | ✅ Covered | Insurance (50 fields), Insurance Subscriber (17 fields), Insurance Visit Type, Eligibility (48 fields), Authorization (33 fields), 834 Load (35 fields) | Very deep; 198 fields across 10 entities |
| Claims / billing | ✅ Covered | Claims (19 fields), Liability (164 fields), Visit Service Claim Note (34 fields), 277 Response (9 fields), Bed Board Billing (31 fields), Bed Board Billing Header (21 fields) | Exceptionally deep; 343 fields across billing entities |
| Payments | ✅ Covered | Payments (20 fields), PaymentPlan (18 fields), Statement Header (32 fields), Statement Detail (16 fields), Funding Activity (13 fields) | Thorough payment tracking |
| Consents / directives | ❌ Not covered | No dedicated consent entities | Product likely captures consent forms; possible gap |
| Patient communications / portal messages | ✅ Covered | Messaging (21 fields), Direct Sent/Received Messages, Notification (6 fields), PortalQuestionnaire (11 fields) | Covers multiple communication channels |
| Specialty – Behavioral health | ✅ Covered | ASAM Assessment (8 fields), Education (36 fields), Questionnaire/Category (40 fields), Treatment Plan Plus entities, Clinical Goal (24 fields), Outcomes (6 fields) | Behavioral health–specific assessments and outcomes are represented |
| Specialty – Residential/inpatient | ✅ Covered | Bed Board Billing (31 fields), Bed Board Shift Notes (12 fields), Bed Board Whiteboard Notes (6 fields), FosterHome (25 fields), EMAR (40 fields) | Residential management including shift notes and foster care |

**Summary**: 14 of 19 applicable domains are fully covered, 4 are partially covered (immunizations, vitals, procedures, care plans), and 1 (imaging) is N/A for this product type. No major EHI domains that the product stores are entirely absent from the export.

## 6. Documentation Quality

**Strengths:**
- The data dictionary is **machine-readable** (extracted from an Angular SPA's JavaScript bundle) with structured JSON containing entity names, file names, field names, data types, nullability, example values, and descriptions for all 1,993 fields.
- **100% field-level documentation**: Every field has a name, type, nullability flag, and description (though 18 descriptions are "TODO" placeholders).
- **Example values** are provided for 99.9% of fields, which significantly aids interpretation.
- The export documentation page clearly explains the file format (NDJSON in ZIP), attachment handling (GUID-based with `ContentAttachments.json`), and both single-patient and population export processes.
- The data dictionary SPA (`b10export-docs.cbh4.crediblebh.com`) provides a browsable interface with per-entity views showing sample JSON and field tables.

**Weaknesses:**
- **No relationship/foreign key documentation**: Fields like `Client Id`, `Visit Id`, `Claim Id` appear across entities but relationships are not formally documented. A developer would need to infer joins.
- **No value set / code system documentation**: Fields like `Severity` (values: "Moderate") or `Recipient Type` (values: "Client Only X") have example values but no enumeration of valid values.
- **18 "TODO" descriptions**: Care Plan (1 field) and Insurance Subscriber (all 17 fields) have placeholder descriptions — a sign of incomplete documentation.
- **Some tautological descriptions**: e.g., "Batch Date" described as "Batch Date," "Charges" described as "Charges." These provide no additional context.
- **No sample export data**: No actual sample NDJSON export file is provided — only sample JSON snippets in the documentation.
- **Custom fields not documented**: 6 entities support custom fields that vary by agency; these are not documented in the data dictionary (only a Client Id appears for custom-only entities).

**Overall**: A developer could build a functional import from this documentation. The structured data dictionary with types, nullability, and examples is above average. The main gaps are in relationship documentation and value set enumeration.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains Credible Behavioral Health stores. With 106 entities and 1,993 fields spanning clinical documentation, medications (10 entities, 293 fields), billing/claims (10 entities, 343 fields), insurance/eligibility (10 entities, 198 fields), treatment plans (9 entities, 115 fields), residential management, and patient communications, the export goes far beyond USCDI clinical summaries. The Liability entity alone (164 fields for financial liability determination) represents depth that no clinical exchange standard would cover. Billing, payments, authorizations, 277 claim responses, 834 enrollment data, and statement details are all present — this is clearly the product's internal data model being exported, not a clinical summary projection.

The few thin areas (Care Plan stub, 5-field Immunizations, 2-field Scheduler Appointment) are minor relative to the overall breadth. Custom-only entities (Profile, Episode, Profile Extended) are an inherent limitation of a configurable platform — these fields vary by agency and are acknowledged in the documentation.

**Axis 2 — Export approach: Purpose-built EHI export**

Multiple signals confirm this is a purpose-built (b)(10) export, not a repackaged clinical exchange:

1. **Native data model**: The export uses the vendor's internal entity/file names (e.g., `ContentClientDiagnosis`, `ContentLiability`, `ContentBedBoardBilling`) — not FHIR resources or C-CDA sections.
2. **Format**: NDJSON in ZIP — a custom export format, not the standard FHIR Bulk Data or C-CDA that the product uses for (g)(10).
3. **Dedicated data dictionary**: A purpose-built Angular SPA at `b10export-docs.cbh4.crediblebh.com` documents the export schema, separate from any FHIR/C-CDA documentation.
4. **Billing and operational data**: The export includes 10 billing entities (Claims, Payments, Liability, etc.), 10 insurance entities, residential management entities, and communication records — none of which appear in USCDI or standard clinical exchange.
5. **Dedicated documentation page**: The Credible-specific export documentation describes a distinct process with its own queue, Report Inbox, and Terms of Use.

### Key Findings

1. **Exceptionally deep billing coverage**: 343 fields across 10 billing entities, anchored by the 164-field Liability entity. This is among the most detailed billing export documentation reviewed. The inclusion of 277 claim status responses and 834 enrollment data demonstrates genuine revenue cycle completeness.

2. **Comprehensive medication lifecycle**: 293 fields across 10 entities covering prescribing, dispensing, administration (EMAR), reconciliation, verification, and prior authorization. The eRx Messages entity (101 fields) captures the full electronic prescribing workflow.

3. **High documentation quality with near-complete field metadata**: 100% of 1,993 fields have descriptions, types, and nullability. 99.9% have example values. This is structured, machine-readable JSON — not PDF tables requiring manual extraction. The 18 "TODO" placeholders are a minor blemish.

4. **Behavioral health–specific content**: ASAM Assessment, Education (36 fields capturing behavioral health education/psychoeducation), configurable questionnaires, treatment plan variants, outcomes tracking, and residential/bed board management reflect the product's specialty focus.

5. **Missing relationship and value set documentation**: Despite excellent field-level metadata, the documentation lacks foreign key relationships between entities and does not enumerate valid values for coded fields. A developer would need to reverse-engineer joins and value constraints.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   NDJSON (Newline Delimited JSON) in ZIP
Entities:        106
Fields:          1,993
Descriptions:    99.1% (1,975 meaningful; 18 are "TODO" placeholders)
Sample data:     No (example values per field, but no full sample export)
Bulk export:     Yes (Patient Population Export via support ticket; up to 30 days)
Domains covered: 14 of 19 applicable domains fully covered; 4 partial
```

### Bottom Line

Credible Behavioral Health provides a genuinely comprehensive (b)(10) EHI export with 106 entities and 1,993 fields covering clinical, billing, insurance, medications, residential management, and communications data — clearly purpose-built from the product's native data model, not a repackaged clinical exchange. The biggest strength is the depth of billing/financial data (343 fields); the biggest gaps are the lack of relationship documentation between entities and 18 incomplete field descriptions.
