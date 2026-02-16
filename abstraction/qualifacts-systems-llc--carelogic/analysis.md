# EHI Export Analysis: Qualifacts Systems, LLC

**Product**: CareLogic Enterprise S3
**Analysis date**: 2026-02-16
**CHPL IDs**: 9807 (15.04.04.3124.Care.S3.00.1.181220)

## 1. Product Context

CareLogic Enterprise is a cloud-based (SaaS) EHR platform designed specifically for **behavioral health and human services organizations**. It serves over 2,500 customer agencies (75,000+ providers, 6M+ patients) across all 50 states, targeting enterprise-level organizations including Certified Community Behavioral Health Clinics (CCBHCs), community mental health centers, substance abuse treatment facilities, and IDD/autism services providers.

Key data domains the product stores:

- **Clinical documentation**: Configurable service documents, progress notes, treatment plans with goals/objectives, hundreds of evidence-based behavioral health assessments (ASI, CAFAS, CANS, LOCUS, etc.), mental status exams
- **Medications**: ePrescribing (via DrFirst Rcopia integration), medication management, eMAR for inpatient/residential
- **Billing & revenue cycle**: Claims processing, EDI 835/270, eligibility, payment posting, accounts receivable, sliding scale fees, state-specific billing
- **Insurance**: Payer plans, authorizations, guarantors, fee matrices
- **Scheduling**: Provider and room scheduling, appointment tracking
- **Patient portal**: Digital forms, telehealth, payments, messaging
- **Specialty modules**: DWI programs, IDD/DD services, EVV (add-on), substance abuse assessments, state program integrations (Indiana HAP, Ohio MACSIS)
- **Inpatient/residential**: Bed management, admit/discharge/transfer
- **Reporting**: CQMs, MIPS, state compliance (88+ state reports)

This is a full-featured behavioral health EHR with integrated billing — the export should cover clinical, billing, specialty, and patient-facing data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `carelogic-ehi-export.html` (8,597 bytes) | CareLogic-specific EHI export documentation page describing export mechanics, file types, and linking to data dictionary | **High** — primary process documentation |
| `index.html` (7,143 bytes) | Qualifacts EHI Export landing page (Sphinx-generated), covers all three platforms | **Low** — mostly navigation |
| `CareLogic_EHI_Export_Data_Dictionary.xls` (988 KB) | Single-sheet Excel workbook: 671 tables, 8,441 columns with names, descriptions, and Oracle data types | **Critical** — the core technical artifact |
| `Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (149 KB, 3 pages) | Legal terms governing EHI export usage, HIPAA compliance, disclaimers | **Low** — legal document, not technical |
| `enrichment/data-dictionary.json` (1.5 MB) | Prior agent's JSON parse of the XLS data dictionary | **High** — validated against my own independent parse |
| `enrichment/coverage-report.json` (24 KB) | Domain categorization summary from prior agent | **Medium** — useful for cross-reference |

The XLS data dictionary is overwhelmingly the most important artifact. There are no sample data files, no JSON/XML schemas, no ERD diagrams, and no additional technical documentation beyond the HTML page and the XLS.

## 3. Export Mechanics

- **Format**: ZIP file containing comma-delimited text files (CSV), one file per database table. An additional CSV file lists all attachments included in the ZIP.
- **Mechanism**: UI-based, initiated by designated agency staff through the "EHI Export Batch Creation" page in CareLogic's Administration menu.
- **Single-patient export**: Available. Must be requested by the patient or authorized representative through their provider. Qualifacts staff cannot provide these on behalf of agencies.
- **Bulk/population export**: Available ("Patient Population Export"). Takes up to 30 calendar days. Only one can run at a time. Requires agreement to Qualifacts' Terms of Use.
- **Access**: Completed exports accessed via "EHI Export Batch History" in CareLogic. Download links expire 30 days after completion.
- **Fees**: Not mentioned in documentation; Terms of Use do not reference fees.
- **Constraints**: Population exports are one-at-a-time with 30-day processing window.

This is a genuine database-level bulk export — not a FHIR API or C-CDA wrapper. The separation from their FHIR API (g(10)) is explicit: the landing page links to FHIR API documentation separately.

## 4. Export Content: What's In It

### Data Dictionary Overview

The CareLogic EHI Export Data Dictionary (`CareLogic_EHI_Export_Data_Dictionary.xls`) is a single-sheet Excel workbook with 9,116 rows documenting:

- **671 tables** (668 with columns; 3 empty: `ADM_ACTIVITY_DETAIL_ID`, `MOD_EXT_CONSENT_CONFIG`, `MOD_NUTRI_SCREENING`)
- **8,441 columns** total
- **8,437 columns (100.0%) have descriptions** (only 4 lack descriptions)
- **8,439 columns (100.0%) have data types** (Oracle types: NUMBER, VARCHAR2, DATE, TIMESTAMP, CLOB, etc.)
- **1,909 foreign key references** documented via "Link to [table]" in column descriptions
- **666 of 671 tables (99.3%) have table-level descriptions** (5 lack: `CLIENT_DD_REQUEST`, `CSO_ORDER`, `MOD_EXT_CONSENT_CONFIG`, `MOD_MAN_INT_EXT_MED`, `MOD_NUTRI_SCREENING`)

### Vendor's Own Content Organization

The data dictionary is organized by table, not by explicit vendor categories. The table names and descriptions reveal the domain structure. Based on my independent parse (see `analysis/parse_data_dictionary.py` and `analysis/full-entity-inventory.json`), I categorized all 671 tables into functional domains. Below are the largest/most significant groupings:

| Domain | Tables | Fields | Representative Tables |
|---|---|---|---|
| Other Clinical Modules | 142 | 1,701 | `MOD_CRS`, `MOD_CCAR_SECTION_ENTRY` (58 cols), `MOD_PCP_PIP` (51 cols), `MOD_CPMS_ENROLLMENT` (40 cols) |
| Behavioral Health Assessments | 86 | 970 | `MOD_APS_HIGH_INT_2` (55 cols), `MOD_APS_HIGH_INT_1` (49 cols), `MOD_BPS_RISK_HARM` (42 cols), `MOD_APS_ASI`, `MOD_CAFAS_SCORING_SUM` |
| Orders (Clinical) | 38 | 487 | `ORD_LAB`, `ORD_MEDICATION`, `ORD_ADMIT`, `ORD_DISCHARGE`, `ORD_RADIO`, `ORD_DME`, `ORD_SECLUSION` |
| Billing & Claims | 33 | 322 | `ACTIVITY_DETAIL` (36 cols), `EDI_835_SERVICE`, `CLAIM_ITEM_LINE`, `GL_DETAIL`, `COLLECTION_BATCH_CLAIM` |
| Service Documents & Assessments | 25 | 272 | `DOCUMENT` (25 cols), `DOCUMENT_SIGNATURE`, `DOCUMENT_DIAGNOSIS`, `ADDENDUM` |
| State Programs (HAP/MACSIS) | 22 | 335 | `MACSIS_ENROLLMENT_FORM` (60 cols), `MACSIS_ADM_DIS` (52 cols), `HAP_ELIGIBILITY_ADDITION` (45 cols) |
| Medications & Allergies | 21 | 373 | `MEDICATION_ENTRY` (52 cols), `ERX_PRESCRIPTION`, `CLIENT_ALLERGY`, `ERX_MEDICATION` |
| Program Enrollment | 21 | 267 | `CLIENT_PROGRAM` (50 cols), `CLIENT_EPISODE`, `CLIENT_EPISODE_SUBABUSE` |
| Insurance & Coverage | 20 | 333 | `CLIENT_PAYER_PLAN` (51 cols), `CLIENT_ASSIST` (50 cols), `CLIENT_GUARANTOR`, `CLIENT_LIABILITY` |
| Treatment Plans / Care Plans | 19 | 200 | `MOD_TPLAN_ENTITY`, `MOD_TX_PLAN`, `MOD_TX_PLAN_NOTE`, `MOD_REC_GOAL` |
| Substance Abuse Assessments | 18 | 239 | `MOD_SUBSTANCE_ABUSE`, `MOD_CAGE_AID`, `MOD_CIWA_AR`, `MOD_DDAP_ASSESSMENT` |
| HL7 / ADT Events | 15 | 136 | `ADT_A01` through `ADT_A38`, `HL7_BATCH_CLIENT` |
| Clinical Document Exchange | 14 | 178 | `CCD_IMPORT_CLIENT_ALLERGY`, `CCD_IMPORT_CLIENT_MED`, `CCDA_EXPORT_BATCH_PARAMS` |
| DWI Programs | 12 | 152 | `DWI_RIASI_ASSESS`, `DWI_PROGRAM_RECOMMEND`, `DWI_PART_COMPLETE` |
| Medication Modules | 12 | 167 | `MOD_MEDICATION`, `MOD_MED_RECON`, `MOD_MED_CONSENT`, `MOD_ALLERGY_RECON` |
| Waiver / Authorization | 12 | 248 | `WV_ACC` (38 cols), `WV_APS_HDR`, `WV_AUTH`, `WV_BUDG` |
| Intake & Referral | 11 | 159 | `INTAKE_TRACKING`, `CLIENT_SRL` (Service Request Log), `APPOINTMENT_TRACKING` |
| Medication Administration (eMAR) | 10 | 212 | `MAR_DOSE_HISTORY` (38 cols), `MAR_ENTRY`, `MAR_DOSE`, `MAR_ALERT` |
| Demographics & Contacts | 8 | 128 | `CLIENT_DEMOGRAPHICS` (23 cols), `CLIENT_RELATIONSHIP` (46 cols), `CLIENT_ADDRESS`, `CLIENT_CONTACT` |
| Payments | 7 | 106 | `PAYMENT_ENTRY`, `PAYMENT_POST` (34 cols), `PAYMENT_DETAIL`, `PAYMENT_LINE` |
| Diagnosis Modules | 5 | 79 | `MOD_TX_DIAG`, `MOD_DIAGNOSIS_RECON`, `MOD_TX_DX` |
| DD/IDD Services | 5 | 68 | `CLIENT_DD_BUDGET`, `CLIENT_DD_REIMBURSE`, `CLIENT_UMDAP` |
| Provider & Pharmacy | 5 | 68 | `CLIENT_PCP`, `CLIENT_PHARMACY`, `CLIENT_PROVIDER` |
| Consent / ROI Documents | 5 | 54 | `MOD_ROI`, `MOD_ROI_DATA`, `MOD_CONSENT_CONFIG`, `MOD_WITHDRAW_ROI` |
| Configurable Forms | 5 | 25 | `CF_EDIT`, `CF_EDIT_DTL`, `CF_FINAL`, `CF_AUTOSAVE` |
| Immunizations | 3 | 60 | `MOD_IMMUNE` (43 cols), `MOD_IMMUNE_DET`, `MOD_IMMUNE_EXT_VAC_SRC` |
| Implantable Devices | 3 | 32 | `IMPLANTABLE_DEVICE`, `MOD_IMPLANTABLE_DEVICE`, `MOD_IMPLANTABLE_DEVICE_DET` |
| Patient Portal | 3 | 41 | `PORTAL_ACCESS_HISTORY`, `PORTAL_USER_CLIENT_MAP`, `MY_HEALTH_ACCESS_HISTORY` |
| Lab Results | 2 | 30 | `MOD_LAB_RESULT` (4 cols), `MOD_LAB_RESULT_DTL` (26 cols) |
| Imaging / Diagnostic Reports | 1 | 15 | `MOD_DIAG_IMG_RPT` |

The full inventory of all 671 tables is available in `analysis/full-entity-inventory.json`.

### 20 Largest Tables by Column Count

| Table | Columns | Domain |
|---|---|---|
| MACSIS_ENROLLMENT_FORM | 60 | State Programs |
| MOD_CCAR_SECTION_ENTRY | 58 | Other Clinical Modules |
| MOD_APS_HIGH_INT_2 | 55 | Behavioral Health Assessments |
| MACSIS_ADM_DIS | 52 | State Programs |
| MEDICATION_ENTRY | 52 | Medications & Allergies |
| CLIENT_PAYER_PLAN | 51 | Insurance & Coverage |
| MOD_PCP_PIP | 51 | Other Clinical Modules |
| CLIENT_ASSIST | 50 | Insurance & Coverage |
| CLIENT_PROGRAM | 50 | Program Enrollment |
| MOD_APS_HIGH_INT_1 | 49 | Behavioral Health Assessments |
| CLIENT_RELATIONSHIP | 46 | Demographics & Contacts |
| HAP_ELIGIBILITY_ADDITION | 45 | State Programs |
| MOD_CCAR_OUTCOME | 45 | Other Clinical Modules |
| MOD_IMMUNE | 43 | Immunizations |
| MOD_BPS_RISK_HARM | 42 | Behavioral Health Assessments |
| MOD_PCP_SIGNATURE | 41 | Other Clinical Modules |
| MOD_CPMS_ENROLLMENT | 40 | Other Clinical Modules |
| MICP_RESPONSE_DTL | 39 | MICP Integration |
| MAR_DOSE_HISTORY | 38 | eMAR |
| WV_ACC | 38 | Waiver / Authorization |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

CareLogic exports its **native Oracle database model** as CSV files — 671 tables spanning virtually the entire application. The export is exceptionally deep in behavioral health-specific areas:

**Richest areas (by field count):**
- **Clinical modules** (142 tables, 1,701 fields): This is the core of CareLogic. Hundreds of `MOD_*` tables capture every type of service document module — from treatment plans (`MOD_TX_PLAN_*`) to crisis prevention (`MOD_CRISIS_PREVENTION`) to community outreach services (`MOD_COMM_OUTREACH_SERV`).
- **Behavioral health assessments** (86 tables, 970 fields): Dedicated tables for specific instruments — ASI (Addiction Severity Index), CAFAS, CANS, LOCUS, CIWA-AR, CAGE-AID, Bio-Psycho-Social assessments, Risk Assessments, Mental Status Exams, and more. Each instrument has its own table(s) with instrument-specific fields.
- **Orders** (38+ tables, 487+ fields): Full clinical ordering — lab orders (`ORD_LAB`), medication orders (`ORD_MEDICATION`), radiology (`ORD_RADIO`), admit/discharge/transfer (`ORD_ADMIT`, `ORD_DISCHARGE`), seclusion (`ORD_SECLUSION`), DME, dietary, and transportation orders.
- **Billing & payments** (40 tables, 428 fields combined): Activity details, claims, EDI 835 remittance data, GL details, collection batches, client statements, payment entries and posting. Covers the full revenue cycle.
- **Insurance & coverage** (20 tables, 333 fields): Payer plans, fee matrices, guarantors, sliding scales, liabilities, authorizations, financial assistance.

**Notably thorough specialty areas:**
- **Substance abuse** (30 tables, 391 fields across DWI and substance abuse assessment categories): DWI-specific programs (RIASI assessment, program recommendations, completions), plus substance abuse assessments (CAGE-AID, CIWA-AR, DDAP, DACODS).
- **State program integrations** (22 tables, 335 fields): Indiana HAP eligibility/enrollment/ANSA/CANS, Ohio MACSIS enrollment/admit-discharge — reflecting CareLogic's deep state-level compliance.
- **eMAR** (10 tables, 212 fields): Full medication administration record with dose tracking, history, signatures, alerts.

**Thinnest areas:**
- **Lab results** (2 tables, 30 fields): `MOD_LAB_RESULT` (4 cols) and `MOD_LAB_RESULT_DTL` (26 cols). Present but thin — consistent with behavioral health EHRs that integrate with external labs rather than storing detailed lab data natively.
- **Imaging** (1 table, 15 fields): `MOD_DIAG_IMG_RPT` — minimal, appropriate for behavioral health.
- **Encounter details** (1 table, 3 fields): `ENCOUNTER_DETAIL` is sparse, but encounter information is primarily captured in `ACTIVITY_DETAIL` (36 cols) and `DOCUMENT` (25 cols).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `CLIENT_DEMOGRAPHICS` (23 fields), `CLIENT_ADDRESS`, `CLIENT_CONTACT`, `CLIENT_RELATIONSHIP` (46 fields), `CLIENT_NAME_HISTORY`, `CLIENT_PICTURE`, `CLIENT_MISC` — 8 tables, 128 fields | Thorough |
| Encounters / visits | ✅ Covered | `ACTIVITY_DETAIL` (36 fields), `DOCUMENT` (25 fields), `ENCOUNTER_DETAIL`, plus hundreds of `MOD_*` service document tables | Very thorough — encounters are the backbone of the clinical data model |
| Problems / conditions / diagnoses | ✅ Covered | `CLIENT_PROGRAM_CODE` (DSM-4/5, ICD-9/10), `CLIENT_EXTERNAL_DIAG*`, `MOD_APS_DIAGNOSIS*`, `MOD_TX_DIAG*`, `MOD_DIAGNOSIS_RECON`, `DOCUMENT_DIAGNOSIS` — 9+ tables | Thorough, with diagnosis reconciliation |
| Medications / prescriptions | ✅ Covered | `MEDICATION_ENTRY` (52 fields), `ERX_PRESCRIPTION`, `ERX_MEDICATION`, `CLIENT_MEDICATION`, `CLINICIAN_ORD_MEDICATION`, `ORD_MEDICATION`, `MOD_MEDICATION`, `MED_RECON*` — 33+ tables | Very thorough — includes ePrescribing (DrFirst/Rcopia integration), medication reconciliation |
| Allergies | ✅ Covered | `CLIENT_ALLERGY`, `CLIENT_MED_ALLERGY`, `ALLERGY_ENTRY`, `ERX_ALLERGY`, `CLINICIAN_ALLERGY_ENTRY`, `MOD_ALLERGY*`, `NO_ALLERGY_LOG` — 7+ tables | Thorough |
| Immunizations | ✅ Covered | `MOD_IMMUNE` (43 fields), `MOD_IMMUNE_DET`, `MOD_IMMUNE_EXT_VAC_SRC` — 3 tables, 60 fields | Good coverage including external vaccine sources |
| Vitals | ✅ Covered | `MOD_VITALS` (31 fields) — includes BP systolic/diastolic, pulse, temperature, height, weight, BMI, O2 sat, respiration | Thorough for a behavioral health EHR |
| Lab results | ⚠️ Partial | `MOD_LAB_RESULT` (4 fields), `MOD_LAB_RESULT_DTL` (26 fields) — 2 tables, 30 fields | Present but thin. Consistent with behavioral health model where labs are integrated from external systems. Detail table has order number, test performed, result value, units, reference range, abnormal flag |
| Imaging / diagnostic reports | ⚠️ Partial | `MOD_DIAG_IMG_RPT` (15 fields) — 1 table | Minimal, appropriate for behavioral health (not a primary imaging EHR) |
| Procedures | ✅ Covered | `MOD_EXT_PROCEDURE`, `ORD_*` tables (various order types), `ACTIVITY_DETAIL` | Covered via clinical orders and activity detail |
| Clinical notes / documents | ✅ Covered | `DOCUMENT` (25 fields), `DOCUMENT_SIGNATURE`, `DOCUMENT_STATUS`, `ADDENDUM`, `DOCUMENT_AUDIT`, plus 310+ `MOD_*` tables for service document modules | Exceptionally thorough — hundreds of document module tables |
| Care plans / goals | ✅ Covered | `MOD_TPLAN_*` (5 tables), `MOD_TX_PLAN*` (12 tables), `MOD_REC_GOAL`, `MOD_GOALS_ADDR_SUMMARY` — 19 tables, 200 fields | Thorough — treatment plans are central to behavioral health |
| Orders / referrals | ✅ Covered | `ORD_*` (38 tables), `MOD_REFERRAL`, `MOD_TX_REFER`, `CSO_ORDER*` — 42+ tables | Comprehensive — lab, medication, admit, discharge, transfer, radiology, DME, dietary, seclusion orders |
| Insurance / coverage | ✅ Covered | `CLIENT_PAYER_PLAN` (51 fields), `CLIENT_ASSIST` (50 fields), `CLIENT_GUARANTOR*`, `CLIENT_LIABILITY*`, `CLIENT_SLIDING_SCALE`, `CLIENT_PAYER_AUTH*`, `CLIENT_PAYER_FEE*` — 20 tables, 333 fields | Very thorough |
| Claims / billing | ✅ Covered | `ACTIVITY_DETAIL` (36 fields), `CLAIM_*`, `EDI_835_*`, `EDI_270_*`, `COLLECTION_BATCH_*`, `CS_BATCH_*`, `STMT_BATCH_*`, `GL_DETAIL`, `FFS_BATCH_*` — 33 tables, 322 fields | Comprehensive — full revenue cycle including EDI, statements, GL |
| Payments | ✅ Covered | `PAYMENT_ENTRY`, `PAYMENT_DETAIL`, `PAYMENT_LINE`, `PAYMENT_POST` (34 fields), `PAYMENT_ACTIVITY`, `PAYMENT_CLAIM_ADJUSTMENT`, `REFUND*` — 7 tables, 106 fields | Thorough |
| Consents / directives | ✅ Covered | `CLIENT_CONSENT` (12 fields), `MOD_ROI*`, `MOD_CONSENT_CONFIG`, `MOD_WITHDRAW_ROI`, `CCD_EXCLUSION_CONSENT`, `CCD_REQUEST_CONSENT` — 6+ tables | Good coverage including Release of Information |
| Patient communications / portal | ⚠️ Partial | `CLIENT_MESSAGE` (21 fields), `PORTAL_ACCESS_HISTORY`, `PORTAL_USER_CLIENT_MAP`, `MY_HEALTH_ACCESS_HISTORY` — 4 tables | Portal access tracking present, but no dedicated portal message content tables visible |
| Specialty: Behavioral health assessments | ✅ Covered | 86+ dedicated assessment tables — ASI, CAFAS, CANS, LOCUS, CIWA-AR, CAGE-AID, BPS, MSE, MGAF, CFARS, Risk Assessment, person-centered planning, and many more | **Exceptionally thorough** — this is the product's core strength |
| Specialty: Substance abuse / DWI | ✅ Covered | 30 tables — DWI RIASI assessments, program recommendations/completions, substance abuse history, DDAP assessments, DACODS modality | Very thorough |
| Specialty: IDD/DD services | ✅ Covered | `CLIENT_DD_BUDGET`, `CLIENT_DD_REIMBURSE`, `CLIENT_DD_REQUEST*`, `CLIENT_UMDAP` — 5 tables, 68 fields | Present |
| Specialty: Inpatient/residential | ✅ Covered | `BED_NOTE`, `BED_STATUS*`, `BED_STAY`, `ORD_ADMIT`, `ORD_DISCHARGE`, `MOD_ADMISSION_DATA*`, `MOD_ADMIT*`, eMAR tables — 15+ tables | Good coverage |

**Domains not applicable to this product:**
- **N/A**: Specialty surgical data, oncology protocols, dental charts — CareLogic is a behavioral health EHR

## 6. Documentation Quality

**Strengths:**
- **Completeness**: 100.0% of columns (8,437/8,441) have descriptions. 100.0% have data types. This is exceptional.
- **Table descriptions**: 666 of 671 tables have descriptions explaining their business purpose.
- **Foreign key documentation**: 1,909 columns include "Link to [table]" references, making relationships navigable.
- **Data types**: Consistent Oracle types with precision (e.g., `NUMBER(12)`, `VARCHAR2(200)`, `TIMESTAMP(6)`).
- **Business context**: Descriptions often explain the business context, not just the field name. Example: `ACTIVITY_DETAIL` description: "This table is used when the staff creates an appointment in the schedule module and then selects an activity for the client."
- **Descriptor references**: Many fields reference descriptor tables for coded values, documenting the indirection even if the descriptor values themselves aren't listed.

**Weaknesses:**
- **No sample data**: No sample export files are provided. A developer cannot see what the actual CSV output looks like.
- **No formal ERD**: Relationships are documented informally in column descriptions ("Link to X table") but there's no entity-relationship diagram or formal FK specification.
- **No value sets**: Coded values and descriptor tables are referenced but not enumerated. A developer would need the actual export to know what `DESCRIPTOR_ID` values mean.
- **No CSV format specification**: No documentation on CSV quoting rules, escape characters, encoding, date formats, null representation, or delimiter details beyond "comma-delimited."
- **No explicit versioning**: No version number on the data dictionary. File metadata shows last save date 2025-11-17 by "Rob Sipe."

**Developer implementability**: A developer could build an import with moderate effort. The schema is clear and nearly fully documented. The main barriers are: (1) unknown CSV formatting details, (2) unknown descriptor/coded values, and (3) no sample data to validate against. These are addressable with access to an actual export.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

CareLogic provides a genuine database-level export of 671 tables (8,441 columns) in CSV format, covering clinical, billing, insurance, behavioral health assessments, substance abuse, IDD, inpatient, and administrative domains. This is not a standards-based projection — it is the vendor's native Oracle data model exported directly. The documentation quality is exceptional (100% field descriptions, 100% data types).

### Key Findings

1. **Exceptionally broad native export**: 671 tables with 8,441 columns across the full CareLogic data model. This is among the most comprehensive EHI exports, covering far more than clinical summaries. The export includes billing (33 tables), insurance (20 tables), payments (7 tables), and hundreds of behavioral health assessment instruments.

2. **Outstanding documentation quality**: Virtually all columns (8,437/8,441 = 100.0%) have descriptions, and all have data types. Table descriptions provide business context. 1,909 foreign key relationships are documented. This is well above average for EHI data dictionaries.

3. **Deep behavioral health specialty coverage**: 86 dedicated assessment instrument tables (ASI, CAFAS, CANS, LOCUS, CIWA-AR, etc.) plus 18 substance abuse assessment tables and 12 DWI program tables. These are the product's core differentiators, and they are fully represented in the export.

4. **No sample data or format specification**: The export's only weakness is the absence of sample files, CSV format documentation, and value set/code table listings. A developer would need an actual export to validate their import implementation.

5. **Clean separation from FHIR**: The EHI export is explicitly separate from CareLogic's FHIR API (g(10)). The landing page links to FHIR documentation independently, and the export uses CSV format with native table names — no confusion about whether this is a repackaged standard.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (comma-delimited text files in ZIP)
Model type:      Native database (Oracle)
Entities:        671 tables
Fields:          8,441
Descriptions:    100.0% of fields have descriptions
Sample data:     No
Bulk export:     Yes (Patient Population Export, up to 30 days)
Domains covered: 18 of 19 applicable domains (all major domains covered; patient portal content is partial)
```

### Bottom Line

CareLogic's EHI export is one of the strongest (b)(10) implementations reviewed. A patient or provider would receive a comprehensive copy of their data spanning clinical records, billing, insurance, medications, assessments, and specialty behavioral health data — exported as the vendor's native database model with near-complete field-level documentation. The single biggest gap is the lack of sample data and CSV format specification, which would make import implementation easier but does not reduce the export's scope or completeness.
