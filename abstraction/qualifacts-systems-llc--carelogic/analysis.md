# EHI Export Analysis: Qualifacts Systems, LLC

**Product**: CareLogic Enterprise S3
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.3124.Care.S3.00.1.181220 (CHPL #9807)

## 1. Product Context

CareLogic Enterprise is a cloud-based EHR platform designed specifically for **behavioral health and human services** organizations. It targets enterprise-level agencies — community mental health centers, CCBHCs (Certified Community Behavioral Health Clinics), substance abuse treatment facilities, IDD/autism providers, and multi-site behavioral health agencies. Qualifacts claims to serve over 2,500 agencies representing ~75,000 providers and 6 million patients.

Key capabilities relevant to export completeness:

- **Clinical documentation**: Configurable service documents, treatment planning with goal/objective tracking, clinical assessments (library of evidence-based instruments), progress notes, SOAP notes, clinical decision support
- **Medications**: ePrescribing, medication management, eMAR (electronic medication administration records)
- **Billing & revenue cycle**: Claim validation, claims scrubbing, direct-to-carrier submission, eligibility inquiries, payment tracking, accounts receivable, state-specific billing rules (88+ state reports)
- **Insurance**: Payer plan management, prior authorizations, sliding fee schedules, patient assistance
- **Intake & referral**: Configurable intake forms, appointment tracking, referral management
- **Patient portal**: Mobile-friendly portal with form assignments, eSignature, payments, messaging, telehealth
- **Specialty modules**: IDD services, DWI/substance abuse programs, inpatient/bed management, EVV (electronic visit verification)
- **State reporting**: Extensive state-specific reporting (MACSIS, GA Connect, IL Registry, etc.)
- **Orders**: Lab orders, medication orders, radiology, dietary, DME, admit/discharge/transfer, seclusion/restraint, consult, EKG, transportation
- **Configurable forms**: Custom form builder for intake, consent, specialty-specific assessments

This is a **full-featured behavioral health EHR with integrated billing**, not a lightweight charting tool. A genuine (b)(10) export should cover clinical documentation, medications, billing/claims, insurance, orders, assessments, treatment plans, state reporting data, and specialty modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/carelogic-ehi-export.html` (8.6 KB) | CareLogic-specific EHI export documentation page. Describes single-patient and population export processes, file format (CSV in ZIP), and links to data dictionary. | **High** — primary process documentation |
| `downloads/CareLogic_EHI_Export_Data_Dictionary.xls` (988 KB) | Excel workbook with one sheet documenting 671 tables and 8,441 columns with names, descriptions, and Oracle data types. | **Highest** — the core technical artifact |
| `downloads/Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (149 KB) | 3-page legal document governing EHI export usage and HIPAA compliance. | **Low** — legal boilerplate, no technical content |
| `downloads/index.html` (7.1 KB) | Landing page linking to CareLogic, Credible, and InSync export docs. | **Low** — navigation only |
| `downloads/enrichment/data-dictionary.json` (1.5 MB) | Prior agent's structured extraction of the XLS data dictionary. | **Reference** — used for comparison; my own parse is primary |
| `downloads/enrichment/coverage-report.json` (24 KB) | Prior agent's domain categorization summary. | **Reference** |

The **data dictionary XLS** is by far the most important artifact. It is a genuine, detailed, product-specific data dictionary — not a reference to a standard specification.

## 3. Export Mechanics

- **Format**: CSV files (comma-delimited text), one file per database table, packaged in a ZIP archive. An additional CSV file lists all attachments included in the ZIP.
- **Mechanism**: UI-based. Designated agency staff initiate the export through the **EHI Export Batch Creation** page in CareLogic's Administration menu.
- **Single-patient export**: Available. Patients/authorized representatives request from their provider; staff initiate in the application. Qualifacts staff cannot perform single-patient exports on behalf of agencies.
- **Bulk/population export**: Available. Only one population export can run at a time. Takes up to **30 calendar days** to complete. Requires agreement to Terms of Use.
- **Access**: Completed exports are accessed through **EHI Export Batch History** in CareLogic. Download links expire 30 days after the export completes.
- **Fees**: Not mentioned in the documentation. The Terms of Use don't reference fees.

## 4. Export Content: What's In It

### Data Dictionary Overview

The data dictionary (`CareLogic_EHI_Export_Data_Dictionary.xls`) documents **671 tables** with **8,441 fields (columns)**. This is the vendor's native Oracle database model — not a projection into a standard like FHIR or C-CDA.

**Documentation quality per field:**
- **8,437 of 8,441 fields (>99.9%) have descriptions** — only 4 fields lack descriptions
- **8,439 of 8,441 fields (>99.9%) have Oracle data types** documented (e.g., `NUMBER(12)`, `VARCHAR2(20)`, `DATE`, `CLOB`)
- **666 of 671 tables (99.3%) have table-level descriptions**
- 3 tables have zero columns (likely junction/linking tables with only an ID)

This is exceptionally thorough documentation. Nearly every field has both a human-readable description and a typed Oracle data type.

### Vendor's own content organization

The data dictionary is organized by table name, not by explicit vendor categories. Tables are named with prefixes that indicate their domain (e.g., `CLIENT_DEMO_*`, `ORD_*`, `PAYMENT_*`, `MOD_*`). I categorized all 671 tables by prefix-based domain analysis.

**Domain breakdown (sorted by field count):**

| Domain | Tables | Fields | Described | Desc % |
|---|---|---|---|---|
| Service Documents & Assessments | 310 | 3,737 | 3,734 | 99.9% |
| Orders | 41 | 541 | 541 | 100% |
| State Programs (HAP/MACSIS) | 22 | 335 | 335 | 100% |
| Insurance & Client Billing | 20 | 333 | 333 | 100% |
| Billing & Claims | 31 | 314 | 314 | 100% |
| Medications & Allergies | 15 | 273 | 273 | 100% |
| Program Enrollment | 21 | 267 | 267 | 100% |
| Waiver / Authorization | 12 | 248 | 248 | 100% |
| Medication Administration (eMAR) | 11 | 246 | 246 | 100% |
| Other / Uncategorized | 21 | 225 | 224 | 99.6% |
| Clinical Document Exchange | 14 | 166 | 166 | 100% |
| Intake & Referral | 10 | 152 | 152 | 100% |
| DWI / Substance Abuse | 12 | 152 | 152 | 100% |
| HL7 / ADT Events | 15 | 136 | 136 | 100% |
| Demographics & Contacts | 8 | 128 | 128 | 100% |
| State Reporting | 14 | 118 | 118 | 100% |
| Payments | 8 | 114 | 114 | 100% |
| Audit & Access | 7 | 69 | 69 | 100% |
| DD/IDD Services | 5 | 68 | 68 | 100% |
| Provider & Pharmacy | 5 | 68 | 68 | 100% |
| Portal & Patient Access | 5 | 68 | 68 | 100% |
| Document Management | 7 | 66 | 66 | 100% |
| Staff & Payroll | 6 | 53 | 53 | 100% |
| Service Document Config | 3 | 52 | 52 | 100% |
| Quality Measures | 4 | 48 | 48 | 100% |
| Mobile Sync | 2 | 44 | 44 | 100% |
| MICP Integration | 2 | 42 | 42 | 100% |
| Inpatient / Bed Management | 4 | 37 | 37 | 100% |
| Alerts & Notifications | 2 | 31 | 31 | 100% |
| Auto-Processing | 1 | 30 | 30 | 100% |
| Administration | 2 | 29 | 29 | 100% |
| Client Access & Follow-up | 2 | 28 | 28 | 100% |
| Authorizations | 5 | 26 | 26 | 100% |
| Configurable Forms | 5 | 25 | 25 | 100% |
| Diagnoses | 4 | 25 | 25 | 100% |
| Client Messages | 1 | 21 | 21 | 100% |
| Pregnancy Records | 1 | 21 | 21 | 100% |
| Clinical Decision Support | 2 | 19 | 19 | 100% |
| Education & Employment | 2 | 17 | 17 | 100% |
| Internal Messaging | 3 | 16 | 16 | 100% |
| Consent Records | 1 | 12 | 12 | 100% |
| Inventory | 1 | 12 | 12 | 100% |
| Task Management | 1 | 12 | 12 | 100% |
| Implantable Devices | 1 | 10 | 10 | 100% |
| Case Audit | 1 | 4 | 4 | 100% |
| Encounter Details | 1 | 3 | 3 | 100% |

### Representative large tables (top 10 by field count)

| Table | Fields | Domain | Description |
|---|---|---|---|
| `MACSIS_ENROLLMENT_FORM` | 60 | State Programs | Ohio MACSIS enrollment form data |
| `MOD_CCAR_SECTION_ENTRY` | 58 | Service Documents | Colorado Client Assessment Record entries |
| `MOD_APS_HIGH_INT_2` | 55 | Service Documents | High Intensity Assessment Part 2 |
| `MACSIS_ADM_DIS` | 52 | State Programs | MACSIS admission/discharge data |
| `MEDICATION_ENTRY` | 52 | Medications & Allergies | Medication order/prescription entries |
| `CLIENT_PAYER_PLAN` | 51 | Insurance & Client Billing | Client insurance payer plan details |
| `MOD_PCP_PIP` | 51 | Service Documents | Person-Centered Plan Prevention Intervention |
| `CLIENT_ASSIST` | 50 | Insurance & Client Billing | Client assistance/patient assistance program data |
| `CLIENT_PROGRAM` | 50 | Program Enrollment | Client program enrollment with 50 fields of enrollment context |
| `MOD_APS_HIGH_INT_1` | 49 | Service Documents | High Intensity Assessment Part 1 |

### Notable patterns

**Service Documents domination**: 310 of 671 tables (46%) are `MOD_*` tables representing individual service document modules (assessments, forms, clinical instruments). These include state-specific instruments (CCAR for Colorado, MACSIS for Ohio, DARTS, CAFAS), clinical scales (CIWA-AR, MINI), treatment plans, lab results, immunizations, and many more. This reflects CareLogic's configurable form builder — each assessment type gets its own database table. Examples:
- `MOD_IMMUNE` (43 fields) — immunization data
- `MOD_LAB_RESULT_DTL` (26 fields) — lab result details
- `MOD_TX_PLAN_ENTITY` (33 fields) — treatment plan problems, goals, objectives
- `MOD_CIWA_AR` (22 fields) — Clinical Institute Withdrawal Assessment
- `MOD_EVAL_MANAGEMENT` (30 fields) — evaluation and management documentation
- `MOD_CONSENT_CONFIG` (24 fields) — HIE consent configuration

**Deep orders coverage**: 41 tables covering lab orders (`ORD_LAB` with 31 fields, `ORD_LAB_DET` with 16 fields), medication orders (`ORD_MEDICATION` with 31 fields), admit/discharge orders, consult orders, DME orders, EKG orders, radiology orders, dietary orders, seclusion/restraint orders, transportation orders, and precaution orders.

**Full billing pipeline**: 31 tables for billing/claims (`CLAIM_*`, `ACTIVITY_DETAIL`, `COLLECTION_*`, `EDI_835`, `EDI_270`, `FFS_*`, `STMT_*`, `CASH_SHEET`) plus 20 tables for client-level insurance/billing (`CLIENT_PAYER_*`, `CLIENT_GUARANTOR`, `CLIENT_SLIDING_*`) plus 8 payment tables (`PAYMENT_POST` with 34 fields, `PAYMENT_ENTRY` with 12 fields, `REFUND` with 14 fields).

The full entity inventory is saved in `analysis/entity-inventory-full.json` (671 tables, 8,441 fields).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a **native database dump** of CareLogic's Oracle database tables. The breadth is remarkable:

**Richest domains:**
- **Service Documents & Assessments** (310 tables, 3,737 fields): This is CareLogic's core — every clinical form, assessment instrument, treatment plan module, and configurable document gets its own table. This captures the full depth of behavioral health clinical documentation.
- **Orders** (41 tables, 541 fields): Comprehensive order types from lab to DME to seclusion/restraint — reflecting inpatient and outpatient behavioral health workflows.
- **Insurance & Billing** (51 tables combined across Insurance & Client Billing + Billing & Claims, 647 fields): Full revenue cycle from payer plans through claims to payment posting and refunds.
- **Medications** (26 tables combined across Medications & Allergies + eMAR, 519 fields): Prescription, medication management, and electronic medication administration records.

**Specialty/behavioral health domains:**
- **DWI / Substance Abuse** (12 tables, 152 fields): Dedicated substance abuse program tracking
- **DD/IDD Services** (5 tables, 68 fields): Intellectual/developmental disability service data
- **Pregnancy Records** (1 table, 21 fields): Pregnancy tracking
- **State Programs** (22 tables, 335 fields): Ohio MACSIS, HAP enrollment, and other state-specific data
- **Waiver / Authorization** (12 tables, 248 fields): Prior authorization and waiver management

**Thinnest domains:**
- **Encounter Details** (1 table, 3 fields): Surprisingly thin, though encounters are likely tracked through `ACTIVITY_DETAIL` and service documents
- **Diagnoses** (4 tables, 25 fields): Compact but present — diagnoses are also embedded in many `MOD_*` assessment tables
- **Implantable Devices** (1 table, 10 fields): Present but minimal — appropriate for a behavioral health EHR

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `CLIENT_DEMO_*` (8 tables, 128 fields): names, addresses, contacts, relationships, demographics | Thorough for behavioral health context |
| Encounters / visits | ⚠️ Partial | `ENCOUNTER_DETAILS` (3 fields) is thin, but `ACTIVITY_DETAIL` tables and `DOCUMENT*` tables (11 tables) capture visit-level data | Encounter data is distributed across activity and service document tables rather than a dedicated encounter model |
| Problems / diagnoses | ✅ Covered | `DIAGNOSIS*` (4 tables, 25 fields) + diagnosis data in `MOD_TX_DIAG_AXIS` (25 fields), `MOD_MAN_INT_EXT_DIAG` (24 fields), `CLIENT_EXTERNAL_LINK` (12 fields) | Adequate |
| Medications / prescriptions | ✅ Covered | `MEDICATION_ENTRY` (52 fields), `MEDICATION_*` (15 tables), `ORD_MEDICATION` (31 fields), `ERX_*` tables for ePrescribing | Deep coverage including prescription, dispensing, and reconciliation |
| Allergies | ✅ Covered | `CLIENT_ALLERGY`, `CLIENT_MED_ALLERGY`, `ALLERGY_*`, `NO_ALLERGY_LOG` (12 fields) | Thorough including "no known allergies" tracking |
| Immunizations | ✅ Covered | `MOD_IMMUNE` (43 fields) | Solid — 43 fields for immunization records |
| Vitals | ⚠️ Partial | No dedicated `VITAL*` table visible; vitals likely captured within service document modules (e.g., `MOD_PCP_*` tables) | Vitals appear embedded in clinical assessments rather than standalone — reasonable for behavioral health |
| Lab results | ✅ Covered | `ORD_LAB` (31 fields), `ORD_LAB_DET` (16 fields), `ORD_LAB_CLINICIAN` (7 fields), `ORD_LAB_CLINICIAN_TEST` (4 fields), `MOD_LAB_RESULT_DTL` (26 fields), `MOD_COAL_METABOLIC_LABS` (32 fields) | Deep coverage — orders, results, and clinician associations |
| Imaging / diagnostic reports | ✅ Covered | `ORD_RADIO` (21 fields), `ORD_EKG` (17 fields) | Present for radiology and EKG orders |
| Procedures | ✅ Covered | Captured across order tables and `CLIENT_AUTH_PROCEDURE` (9 fields), `SRBD_PROC_UNIT` (4 fields) | Adequate for behavioral health scope |
| Clinical notes / documents | ✅ Covered | 310 `MOD_*` service document tables (3,737 fields) + `DOCUMENT*` tables (11 tables) + `ADDENDUM` | **Exceptionally deep** — every assessment, progress note, and clinical form type has dedicated structured storage |
| Care plans / goals | ✅ Covered | `MOD_TX_PLAN` (23 fields), `MOD_TX_PLAN_ENTITY` (33 fields), `MOD_TPLAN_ENTITY` (23 fields), `MOD_PCP_*` (Person-Centered Plan tables) | Strong treatment planning coverage |
| Orders / referrals | ✅ Covered | 41 order tables (541 fields): lab, med, radiology, dietary, DME, admit, discharge, transfer, consult, seclusion/restraint, transportation | **Exceptionally deep** |
| Insurance / coverage | ✅ Covered | `CLIENT_PAYER_PLAN` (51 fields), `CLIENT_PAYER_*` (multiple tables), `CLIENT_GUARANTOR`, `CLIENT_SLIDING_*` | Thorough — payer plans, guarantors, sliding fee schedules |
| Claims / billing | ✅ Covered | `CLAIM_*` tables, `ACTIVITY_DETAIL`, `EDI_835`, `EDI_270`, `BILLING_*`, `FFS_*`, `COLLECTION_*`, `STMT_*` (31 tables, 314 fields) | **Deep** — full claims lifecycle from submission through EDI remittance |
| Payments | ✅ Covered | `PAYMENT_POST` (34 fields), `PAYMENT_ENTRY` (12 fields), `PAYMENT_DETAIL` (9 fields), `PAYMENT_ACTIVITY` (6 fields), `PAYMENT_LINE` (26 fields), `PAYMENT_CLAIM_ADJUSTMENT` (8 fields), `REFUND` (14 fields), `REFUND_ACTIVITY` (5 fields) | Deep payment and refund tracking |
| Consents / directives | ✅ Covered | `CLIENT_CONSENT` (12 fields), `MOD_CONSENT_CONFIG` (24 fields) | Present |
| Patient communications / portal | ✅ Covered | `CLIENT_MESSAGE` (21 fields), `PORTAL_ACCESS_HISTORY` (11 fields), `PORTAL_USER_CLIENT_MAP` (18 fields), `MY_HEALTH_ACCESS_HISTORY` (12 fields), `PAT_ED_RESOURCE_*` (27 fields) | Adequate — portal access, messaging, patient education resource tracking |
| Specialty: Behavioral health | ✅ Covered | Extensive `MOD_*` assessment tables: CIWA-AR (withdrawal), CAFAS (child functional), CCAR (Colorado assessment), BPS (biopsychosocial), risk assessments, DDAP, MINI, ratings scales | **Core strength** — dozens of behavioral health-specific instruments |
| Specialty: Substance abuse | ✅ Covered | `DWI_*` (12 tables, 152 fields) for DWI/substance abuse programs | Dedicated module |
| Specialty: IDD/DD | ✅ Covered | `CLIENT_DD_*` (5 tables, 68 fields), `CLIENT_UMDAP` | Present |
| Specialty: Inpatient | ✅ Covered | `BED_*` (4 tables, 37 fields), `ORD_ADMIT` (23 fields), `ORD_DISCHARGE` (24 fields), `ORD_SECLUSION` (15 fields) | Adequate for behavioral health inpatient |

**Domains present that go beyond USCDI:**
- Billing & claims (31 tables, 314 fields)
- Payments & refunds (8 tables, 114 fields)
- Insurance/payer management (20 tables, 333 fields)
- Prior authorizations (5 tables, 26 fields) + Waiver/authorization (12 tables, 248 fields)
- State-specific program data (36 tables, 453 fields across State Programs + State Reporting)
- DWI/substance abuse (12 tables, 152 fields)
- DD/IDD services (5 tables, 68 fields)
- Configurable forms infrastructure (5 tables, 25 fields)
- Portal access/patient education (5 tables, 68 fields)
- eMAR/medication administration (11 tables, 246 fields)

## 6. Documentation Quality

**Strengths:**
- The data dictionary is **exceptionally well-documented**: 99.9% of fields have descriptions and data types. This is among the highest documentation rates across EHR vendors.
- Descriptions are genuinely useful, not just auto-generated field name expansions. Examples:
  - `PAYMENT_POST.ORIGINAL_TOTAL_CHARGE_AMOUNT`: "For Payments that have been reversed, amount reflects the original total charges posted."
  - `ORD_SECLUSION.REASON_FOR_RESTRAINT`: "Reason for the seclusion/restraint being requested."
  - `MOD_CIWA_AR.TOTAL_SCORE`: "Sum of all 10 questions."
- Table-level descriptions provide context for what each table stores and how it relates to the workflow.
- Oracle data types (`NUMBER(12)`, `VARCHAR2(255)`, `DATE`, `CLOB`) provide precise type information.

**Limitations:**
- **No foreign key documentation**: While descriptions mention "Link to [table]" relationships, there is no formal FK/relationship schema. A developer would need to infer relationships from naming conventions and description text.
- **No value sets/code systems**: Coded fields (e.g., `EVERY_PERIOD_TYPE` described as "period (days, week, months)") don't have formal enumeration of valid values.
- **No sample data**: No example export files are provided.
- **No ERD or relationship diagram**: The flat table-per-row format doesn't convey the data model's structure.
- **Single flat sheet**: All 671 tables are in one worksheet with no grouping or categorization by the vendor.

**Usability assessment**: A developer could build a reasonable import system from this documentation. The table/column names follow consistent conventions (e.g., `*_ID` for keys, `CREATED_BY`/`CREATED_DATE`/`MODIFIED_BY`/`MODIFIED_DATE` for audit fields), descriptions explain business meaning, and types are precise. The main challenge would be reconstructing relationships between tables.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains CareLogic stores. It is not limited to clinical summaries — it includes 671 tables spanning clinical documentation (310 assessment/service document tables), medications (26 tables), full billing/claims pipeline (31 tables), payments (8 tables), insurance (20 tables), orders of all types (41 tables), state-specific program data (36 tables), behavioral health specialties (DWI, IDD), inpatient bed management, portal/patient access, and more. The coverage goes well beyond USCDI: billing, claims, payments, insurance details, state reporting, prior authorizations, eMAR, configurable forms, and specialty modules are all present. Given that CareLogic is a behavioral health EHR (not a general acute care hospital system), the export appears to cover essentially the entire patient-facing designated record set.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange. The telltale signs:
1. **Native database tables**: The export is CSV files mirroring CareLogic's 671 Oracle database tables — not C-CDA sections or FHIR resources.
2. **Product-specific data dictionary**: The XLS data dictionary documents vendor-specific table/column names with Oracle data types — not references to USCDI, US Core, or any standard specification.
3. **Coverage far beyond (g)(10)**: The export includes billing, claims, payments, state programs, eMAR, configurable forms, and operational data that would never appear in a FHIR Bulk Data or C-CDA export.
4. **Dedicated UI workflow**: The EHI Export Batch Creation page in the Administration menu is a purpose-built feature, not repurposed from another export mechanism.
5. **No mention of FHIR, C-CDA, or USCDI** in the export documentation — it references only the internal data model.

### Key Findings

1. **Exceptionally well-documented native database export**: 671 tables, 8,441 fields, with >99.9% description and type coverage. This is one of the most thoroughly documented EHI exports among certified products.

2. **Deep clinical documentation**: 310 service document/assessment module tables (3,737 fields) capture the full depth of behavioral health clinical instruments, treatment plans, and configurable forms. This is the product's core strength reflected in its export.

3. **Full billing lifecycle included**: The export covers the complete revenue cycle — from payer plans (`CLIENT_PAYER_PLAN`, 51 fields) through claims (`CLAIM_*`, 31 tables) to payment posting (`PAYMENT_POST`, 34 fields) and refunds. This is a significant differentiator from vendors who omit billing.

4. **Comprehensive order system**: 41 order tables covering lab, medication, radiology, EKG, dietary, DME, admit, discharge, transfer, consult, seclusion/restraint, and transportation orders — unusually broad for a behavioral health platform.

5. **Minor gaps are appropriate to scope**: Vitals don't have a dedicated table (embedded in assessments), and encounter details are thin (3 fields) — but these reflect behavioral health's documentation patterns rather than missing data.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV (comma-delimited text files in ZIP)
    Entities:        671 tables
    Fields:          8,441
    Descriptions:    99.95% of fields have descriptions
    Sample data:     No
    Bulk export:     Yes (Patient Population Export, up to 30 days)
    Domains covered: 19 of 19 applicable domains (all ✅ or ⚠️ partial)

### Bottom Line

CareLogic's EHI export is one of the strongest implementations of (b)(10) among certified products. A patient or provider would receive a comprehensive, well-documented copy of their data covering clinical records, medications, orders, billing, payments, insurance, and behavioral health-specific assessments across 671 database tables with 8,441 fields. The only notable limitation is the absence of sample data and formal relationship documentation — but the field-level documentation is near-perfect, and the export scope clearly represents the full designated record set, not a clinical summary repackaged.
