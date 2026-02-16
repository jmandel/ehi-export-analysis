# EHI Export Analysis: McKesson Specialty Health Technology Products LLC (Ontada)

**Product**: iKnowMed Generation 2 (Version 3)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2920.iKno.30.01.1.180508 (CHPL #9580)

## 1. Product Context

iKnowMed Generation 2 is a cloud-based electronic health record built exclusively for oncology and hematology practices. Developed by McKesson Specialty Health (operating as Ontada), it serves ~2,700 oncology providers across 620+ sites of care, primarily within The US Oncology Network — one of the nation's largest community oncology networks caring for roughly one in five US cancer patients.

As a specialty oncology EHR, iKnowMed stores:
- **Core clinical data**: demographics, encounters, problems/diagnoses, medications, labs, vitals, allergies, immunizations, clinical notes, procedures
- **Oncology-specific data**: cancer staging (AJCC/FIGO), chemotherapy regimen management, cycle day scheduling, treatment planning, biomarker/molecular test ordering, NCCN pathway compliance, drug toxicity monitoring, BSA dosing calculations, radiation/surgery/transfusion treatments
- **Nursing care**: IV access/de-access documentation (extremely detailed), patient assessments, nursing notes
- **Billing & charges**: charge capture, charge lines with ICD/NDC codes, billing sessions, billing organizations
- **Insurance & financial auth**: insurance records, prior authorization tracking
- **Patient engagement**: patient portal (Ontada Health) with secure messaging, appointment requests, education events
- **Care coordination**: care plans, patient transfers, Carequality document exchange, CCD reconciliation
- **Quality & value-based care**: Oncology Care Model episode tracking, VBC program participation
- **Social history & screenings**: distress screening, substance use, living/working environment, OB/GYN history, cognitive/depression status
- **Clinical trials**: trial definitions and patient enrollment
- **E-prescribing**: via NewCropRx/Surescripts integration

The (b)(10) export should cover all of these domains to be comprehensive.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Value |
|---|---|---|---|
| `downloads/b10_data_dictionary.xlsx` | Official (b)(10) data dictionary — Excel workbook with 4 sheets | 241 KB; 249 entities, 5,679 fields | **Primary artifact** — most informative |
| `downloads/ehi-page.html` | HTML source of the EHI Export Capabilities page at ontada.com | 72 KB | Confirms export format (pipe-delimited ZIP) and links to dictionary |
| `downloads/ehi-page-screenshot.png` | Full-page screenshot of the EHI page | 313 KB | Visual confirmation of page content |
| `downloads/enrichment/data-dictionary.json` | Prior agent's extraction of the XLSX | 1.6 MB | Used for orientation; independently verified |
| `downloads/enrichment/summary.json` | Prior agent's summary stats | 35 KB | Verified against own parsing |
| `downloads/enrichment/extract-data-dictionary.ts` | Prior agent's Bun/TypeScript parser | 8 KB | Reviewed approach; wrote independent Python parser |

The data dictionary XLSX is the single significant artifact. No sample data, no export format specification, no user guide, no API documentation for the (b)(10) export. The EHI web page is a brief paragraph with a download link.

## 3. Export Mechanics

- **Format**: ZIP file containing pipe-delimited (`|`) flat files — one file per table/entity
- **Mechanism**: Not documented on the EHI page. No instructions for how a user or administrator triggers the export. The page says only that iKnowMed's "EHI Export Capabilities enable the extraction of the electronic health record."
- **Single-patient vs bulk**: The page refers to "a patient's iKnowMed record," suggesting single-patient export
- **Access constraints**: Not documented. No mention of fees, administrative approval, or turnaround time
- **Content variability**: The page explicitly states content varies based on: (1) which iKnowMed features are in use, (2) configuration decisions, (3) clinical utilization patterns, and (4) documentation practices

## 4. Export Content: What's In It

The export is documented through a single Excel workbook (`b10_data_dictionary.xlsx`) containing **249 entities** with **5,679 fields** across 4 sheets:

| Sheet | Entities | Fields | Fields w/ Descriptions | Description Quality |
|---|---|---|---|---|
| iKnowMed | 236 | 5,275 | 4,720 (89.5%) | Java model annotations (type, required/optional) |
| VBC | 5 | 60 | 0 (0%) | Column names only — no descriptions, no types beyond generic |
| Patient History | 6 | 178 | 0 (0%) | Column names + Oracle types — no descriptions |
| Ontada Health | 2 | 166 | 94 (56.6%) | Human-readable descriptions for ~57% of fields |
| **Total** | **249** | **5,679** | **4,814 (84.8%)** | |

### Data dictionary structure

The iKnowMed sheet (the core — 93% of all fields) provides for each column:
- `TABLE_NAME`, `COLUMN_NAME`: always present
- `DATA_TYPE`: Oracle types (VARCHAR2, NUMBER, DATE, TIMESTAMP, CLOB)
- `DATA_LENGTH`: present for VARCHAR2 columns
- `TABLE_DESC`: Java class name, occasionally with a human-readable sentence (e.g., "Represents patient appointment visit or resource appointment")
- `COLUMN_DESC`: Java field annotations like `String firstName; (required)` or `Activity activity; (optional)` — these convey type and nullability but rarely semantic meaning

The VBC sheet has only `table_name`, `column_name`, and `data_type` — no descriptions at all.

The Patient History sheet has Oracle metadata (`DATA_TYPE`, `DATA_LENGTH`, `DATA_PRECISION`, `DATA_SCALE`, `CHAR_USED`) but no descriptions.

The Ontada Health sheet uses a MongoDB-style schema (`Collection`, `Field Name`, `Data Type`, `Description`, `Notes`) with the most human-readable descriptions of any sheet.

### What's NOT documented:
- **Foreign key relationships**: Not specified. Must be inferred from naming conventions (e.g., `PATIENT` column likely references `PATIENT.ID`)
- **Value sets / code systems**: Coded fields have no enumeration of valid values
- **Sample data**: No example export files provided
- **File format details**: No specification of encoding, header rows, null representation, or pipe-character escaping

### Vendor's own content organization

The vendor organizes the data dictionary into 4 sheets without further sub-categorization within sheets. The following table shows the 20 largest entities:

| Entity | Fields | Described | Types | Sheet |
|---|---|---|---|---|
| PAT_ORDER | 182 | 153 | yes | iKnowMed |
| NURSINGCARE_IVACCESS | 122 | 121 | yes | iKnowMed |
| conversation | 101 | 55 | yes | Ontada Health |
| PAT_REGIMEN | 99 | 97 | yes | iKnowMed |
| MEDICATION_PREFERENCE | 92 | 85 | yes | iKnowMed |
| PAT_ORDER_DOSE | 75 | 56 | yes | iKnowMed |
| NURSINGCARE_IVDEACCESS | 68 | 67 | yes | iKnowMed |
| PAT_DOCUMENT | 66 | 57 | yes | iKnowMed |
| G2_DISTRESS_THERMOMETER | 64 | 0 | yes | Patient History |
| Patient_appointment_request | 65 | 39 | yes | Ontada Health |
| PAT_WORKFLOW_ITEM | 60 | 54 | yes | iKnowMed |
| PATIENT | 57 | 47 | yes | iKnowMed |
| LOCATION | 57 | 48 | yes | iKnowMed |
| NURSINGCARE_PATIENTASSESS | 55 | 54 | yes | iKnowMed |
| PAT_TREATMENT_HISTORY | 54 | 51 | yes | iKnowMed |
| MEDICATION | 53 | 50 | yes | iKnowMed |
| PAT_RESULT_HEADER | 53 | 49 | yes | iKnowMed |
| PATIENT_PREFERENCE | 51 | 44 | yes | iKnowMed |
| PAT_TREATMENT | 49 | 45 | yes | iKnowMed |
| OTHER_SERVICE_DEF_PREFERENCE | 46 | 46 | yes | iKnowMed |

The complete inventory (all 249 entities) is in `analysis/entity-inventory-full.json`; summary statistics in `analysis/entity-inventory-summary.json`.

### Functional domain breakdown (derived from entity naming analysis)

| Domain | Entities | Fields | Key Tables |
|---|---|---|---|
| Oncology Treatments & Regimens | 22 | 570 | PAT_REGIMEN (99), PAT_TREATMENT_HISTORY (54), PAT_TREATMENT (49), PAT_CHEMO_TREATMENT (34) |
| Medications & Prescriptions | 19 | 553 | MEDICATION_PREFERENCE (92), MEDICATION (53), PRESCRIPTION (35), DISPENSABLE (35) |
| Orders & Administration | 15 | 467 | PAT_ORDER (182), PAT_ORDER_DOSE (75), PAT_ORDER_SESSION (17) |
| Patient Portal & Communication | 15 | 373 | conversation (101), Patient_appointment_request (65), MAIL_MESSAGE (20) |
| Administrative / Reference | 15 | 359 | LOCATION (57), PRACTICE (42), ACTIVITY (39), AUDIO_RECORDING (33) |
| Documents & Notes | 14 | 290 | PAT_DOCUMENT (66), PAT_DISCHARGE_NOTE (41), TRANSCRIPTION (32) |
| Billing & Charges | 17 | 284 | CHARGE_LINE (29), CHARGE_HEADER (17), CHARGE_LINE_ICD (9), BILLABLE_ITEM (10) |
| Lab Results & Diagnostics | 12 | 282 | PAT_RESULT_HEADER (53), PAT_RESULT_VALUE (41), LAB_ANALYTE_DEF (22) |
| Nursing Care | 5 | 268 | NURSINGCARE_IVACCESS (122), NURSINGCARE_IVDEACCESS (68), NURSINGCARE_PATIENTASSESS (55) |
| Social History / SDOH | 9 | 256 | G2_DISTRESS_THERMOMETER (64), OBGYN_HISTORY (43), G2_SOCIALHX_SUBSTANCE_USE (34) |
| Patient Demographics & Identity | 9 | 186 | PATIENT (57), PATIENT_CONTACT (31), PATIENT_IDENTIFICATION (14) |
| Value-Based Care / Quality | 9 | 161 | PAT_OCM_EPISODE (42), PAT_OCM_HEADER (38), vbc_patient (17) |
| Surveys & Screenings | 7 | 144 | PAT_SURVEY (44), PAT_SCREENING (22), PAT_SURVEY_ITEM (21) |
| Problems / Diagnoses | 7 | 138 | PAT_PROBLEM (36), PROBLEM_DEF (28), BILLING_DIAG_DEF (23) |
| Vitals & Observations | 6 | 120 | BASELINE_VITAL (28), TREATMENT_VITAL (22), DAILY_VITALS (17) |
| Care Coordination & Referrals | 5 | 113 | PATIENT_TRANSFER (46), PAT_CARE_PLAN (32), CCD_RECONCILIATION (16) |
| Allergies | 6 | 110 | PAT_ALLERGY (36), ALLERGEN_DEF (20), ALLERGEN_SEVERITY_DEF (16) |
| Encounters & Appointments | 6 | 92 | APPOINTMENT (34), APPOINTMENT_RESOURCE (14), NURSING_APPOINTMENT_RESOURCE (13) |
| Adverse Events & Alerts | 5 | 89 | PATIENT_ADVERSEEVENT (27), ALERT (22), PAT_CHART_ALERT (15) |
| Insurance & Financial Auth | 5 | 80 | PAT_FIN_AUTH (26), INSURANCE (20), PATIENT_INSURANCE (20) |
| Immunizations | 3 | 46 | PAT_IMMUNIZATION (20), PAT_IMMUNIZATION_EVENT (14) |
| Clinical Trials | 2 | 44 | CLINICAL_TRIAL_DEF (28), CLINICAL_TRIAL_DEF_PREF (16) |
| Other/Miscellaneous | 36 | 654 | PAT_WORKFLOW_ITEM (60), PATIENT_PREFERENCE (51), PAT_ADMIN_DETAIL (34) |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized into 4 data sources that together represent a near-complete dump of iKnowMed's database:

**iKnowMed (236 tables, 5,275 fields)**: The core EHR database. This is exceptionally deep in oncology-specific data — the PAT_ORDER table alone has 182 columns tracking every aspect of medication/treatment orders. Treatment regimens (PAT_REGIMEN at 99 columns, plus 21 associated tables) capture the full complexity of chemotherapy cycle management. The nursing care tables (NURSINGCARE_IVACCESS at 122 columns) are remarkably detailed, documenting IV access procedures at a granularity unusual even for specialty EHRs.

Billing coverage is genuine — 17 tables covering charge headers, charge lines with ICD and NDC code mappings, sent charges, errors, comments, and billing sessions. Insurance and financial authorization tables are present with prior auth tracking.

**VBC (5 tables, 60 fields)**: Value-Based Care program data — patient eligibility, program status, logged tasks. Thin documentation (no descriptions) but represents real programmatic data.

**Patient History (6 tables, 178 fields)**: Social determinants and patient-reported data — distress thermometer (64 columns of oncology distress screening), substance use, lifestyle, living/working environment, international travel. No descriptions but comprehensive column coverage.

**Ontada Health (2 collections, 166 fields)**: Patient portal data — secure messaging conversations (101 fields) and appointment requests (65 fields). Best-documented sheet with human-readable descriptions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENT (57 fields), PATIENT_CONTACT (31), PATIENT_IDENTIFICATION (14), PAT_RACE (7), PAT_ETHNICITY (5), PAT_LANGUAGE (5), PAT_GENDER_IDENTITY (9) | Thorough — 9 entities, 186 fields |
| Encounters / visits | ✅ Covered | APPOINTMENT (34 fields), APPOINTMENT_RESOURCE (14), APPOINTMENT_SCHEDULE (11), APPOINTMENT_EMCODE (15) | Adequate — includes EM coding linkage |
| Problems / conditions | ✅ Covered | PAT_PROBLEM (36 fields), PROBLEM_DEF (28), PAT_PROBLEM_INFERENCE (13), PAT_PROBLEM_BILLING_DIAG_DEF (7) | Thorough — includes inference tracking and billing diagnosis mapping |
| Medications / prescriptions | ✅ Covered | MEDICATION (53), PRESCRIPTION (35), MEDICATION_PREFERENCE (92), DISPENSABLE (35), PAT_PHARMACY_DISPENSE (24), RXRENEWALREQUEST, RX_CHANGE_REQUEST, RX_FILL_NOTIFICATION | Very deep — 19 entities, 553 fields covering the full medication lifecycle |
| Allergies | ✅ Covered | PAT_ALLERGY (36), ALLERGEN_DEF (20), ALLERGEN_REACTION_DEF (15), ALLERGEN_SEVERITY_DEF (16), PAT_ALLERGY_ALERT (7), PAT_ALLERGY_REACTION (16) | Thorough — includes reaction definitions and severity tracking |
| Immunizations | ✅ Covered | PAT_IMMUNIZATION (20), PAT_IMMUNIZATION_EVENT (14), PAT_IMMUNIZATION_REGISTRY (12) | Adequate — includes registry reporting |
| Vitals | ✅ Covered | BASELINE_VITAL (28), DAILY_VITALS (17), TREATMENT_VITAL (22), TREATMENT_VITAL_SET (8), PAT_PERFORMANCE_STATUS (28), PATIENT_SMOKING_STATUS (17) | Thorough — includes oncology-specific treatment vitals and performance status |
| Lab results | ✅ Covered | PAT_RESULT_HEADER (53), PAT_RESULT_VALUE (41), LAB_ANALYTE_DEF (22), LAB_PANEL_DEF (9), EXTERNAL_RESULT_PANEL_DEF (14), EXTERNAL_RESULT_VALUE_DEF (9) | Deep — includes both internal and external lab definitions |
| Imaging / diagnostic reports | ⚠️ Partial | IMAGING_DEF (15) — definitions only; imaging results likely in PAT_RESULT_HEADER/VALUE or PAT_DOCUMENT | Product stores imaging orders/results; no dedicated imaging results entity |
| Procedures | ✅ Covered | Via oncology treatment tables: PATIENT_SURGERY_TREATMENT, PAT_PROCEDURE_TREATMENT, plus PAT_ORDER for procedural orders | Covered through treatment-centric model |
| Clinical notes / documents | ✅ Covered | PAT_DOCUMENT (66), PAT_DOCUMENT_LOB (6), TRANSCRIPTION (32), TRANSCRIPTION_LOB (6), PAT_DISCHARGE_NOTE (41), CLINICAL_NOTE_ADDENDUM (12) | Deep — includes LOB storage for full document content |
| Care plans / goals | ✅ Covered | PAT_CARE_PLAN (32) | Present but single table |
| Orders / referrals | ✅ Covered | PAT_ORDER (182 fields — the largest entity), PAT_ORDER_DOSE (75), PAT_ORDER_SESSION (17), PAT_ORDER_GROUP (5), multiple order sub-tables | Exceptionally detailed |
| Insurance / coverage | ✅ Covered | INSURANCE (20), PATIENT_INSURANCE (20), PAT_FIN_AUTH (26), PAT_FIN_AUTH_BILLINGCODE (6), PAT_FIN_AUTH_ICD (6) | Includes prior authorization tracking |
| Claims / billing | ✅ Covered | CHARGE_HEADER (17), CHARGE_LINE (29), CHARGE_LINE_ICD (9), CHARGE_LINE_NDC (7), CHARGE_HEADER_SENT (8), CHARGE_LINE_SENT (6), CHARGE_COMMENT (10), CHARGE_ERROR (8), CHARGE_SOURCE (8) | Genuine billing coverage — 17 entities, 284 fields including sent charges and errors |
| Payments | ❌ Not covered | No payment/remittance tables | Product has billing integration; payment tracking may be in downstream PM system rather than iKnowMed itself — may not be a true gap |
| Consents / directives | ⚠️ Partial | No dedicated consent table; may be captured as PAT_DOCUMENT types | No explicit consent entity |
| Patient communications | ✅ Covered | conversation (101 fields), MAIL_MESSAGE (20), MAIL_MSG_BODY (6), MAIL_MSG_ATTACHMENT (9), PATIENT_MESSAGE (12), EMAIL_CONTACT (10) | Deep — includes portal messaging and internal mail |
| Specialty: Oncology | ✅ Covered | PAT_REGIMEN (99), PAT_CHEMO_TREATMENT (34), PATIENT_RADIATION_TREATMENT (29), PATIENT_SURGERY_TREATMENT (7), PAT_TREATMENT (49), PAT_TREATMENT_HISTORY (54), REGIMEN_DEF (41), CYCLE_DAY_DELAY (11), DATE_CYCLE_DAY (9), and 13 more treatment tables | **Exceptional** — 22 entities, 570 fields. This is the product's core domain and the export reflects it |
| Specialty: Nursing care | ✅ Covered | NURSINGCARE_IVACCESS (122), NURSINGCARE_IVDEACCESS (68), NURSINGCARE_PATIENTASSESS (55), NURSINGCARE_PATIENTNOTE (18), NURSINGCARE_BILLABLE_ITEM (5) | Remarkably detailed IV access documentation |
| Social history / SDOH | ✅ Covered | G2_DISTRESS_THERMOMETER (64), G2_SOCIALHX_SUBSTANCE_USE (34), G2_SOCIALHX_LIFESTYLE, G2_SOCIALHX_LIVING_ENV, G2_SOCIALHX_WORKING_ENV, G2_SOCIALHX_INT_TRAVEL_HX | 6 dedicated tables in Patient History sheet |
| Clinical trials | ✅ Covered | CLINICAL_TRIAL_DEF (28), CLINICAL_TRIAL_DEF_PREF (16) | Trial definitions present; patient-trial enrollment linkage unclear |
| Adverse events | ✅ Covered | PATIENT_ADVERSEEVENT (27), PAT_DRUGDOSE_ALERT (15), RXALERT (25) | Includes drug safety alerts |
| Value-based care / quality | ✅ Covered | PAT_OCM_EPISODE (42), PAT_OCM_HEADER (38), PAT_OCM_MONTHLY (9), plus 5 VBC tables (60 fields) | Oncology Care Model and VBC program data |

**Notable observations:**
- **Cancer staging**: No dedicated staging table. Staging data is likely embedded within PAT_PROBLEM, PAT_REGIMEN, or PAT_TREATMENT columns, but this isn't explicitly broken out. Given iKnowMed's deep AJCC/FIGO staging support, this data is almost certainly present in the export but not self-documenting.
- **Biomarker/molecular testing**: No dedicated biomarker entity. These likely flow through the lab results system (PAT_RESULT_HEADER/VALUE) or orders (PAT_ORDER), but without value set documentation, it's impossible to confirm.
- **Payments**: No payment/remittance tables. iKnowMed handles charge capture but may rely on external PM systems for payment posting — this may not be a gap if the product doesn't store payment data.

## 6. Documentation Quality

**Strengths:**
- The data dictionary is substantial: 249 entities, 5,679 fields — clearly a database schema export, not a curated summary
- 84.8% of fields have some form of description (4,814 of 5,679)
- Data types are consistently documented across all sheets
- The iKnowMed sheet's Java annotations convey type information and required/optional status

**Weaknesses:**
- **Column descriptions are Java model annotations, not business definitions**: `String absoluteDoseUnit; (optional)` tells you the Java field type but not what dose unit values are valid or what the field means clinically. A developer would need to guess at semantics.
- **No value set documentation**: This is the most significant gap. Fields that clearly contain coded values (status codes, type indicators, category codes) have no enumeration of valid values. Without this, the export data is partially opaque.
- **No relationship documentation**: Foreign keys must be inferred from naming conventions. No ERD or explicit FK declarations.
- **VBC and Patient History sheets have zero descriptions**: 238 fields (4.2% of total) across 11 entities have no documentation beyond column names and data types.
- **No sample data**: No example export files to demonstrate format, encoding, null handling, or actual field values.
- **No export procedure documentation**: The EHI web page provides no instructions for triggering the export. Users must presumably contact Ontada or navigate an undocumented UI.
- **No format specification**: Encoding (UTF-8?), header rows, null representation, escaping of pipe characters in data — all undocumented.

**Could a developer build an import?** Partially. The table/column structure is clear enough to parse files into database tables. But interpreting the data — understanding what code values mean, how tables relate, what clinical concepts fields represent — would require significant reverse-engineering and access to sample data. The Java-style descriptions help identify data types but rarely convey clinical semantics.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains iKnowMed stores. The 249-entity, 5,679-field data dictionary represents a near-complete database dump — not a clinical summary. Critical evidence:
- Oncology-specific data is deeply represented (22 treatment/regimen tables, 570 fields) — this is the product's core and the export treats it accordingly
- Billing data is genuinely present (17 tables covering charges, ICD/NDC codes, billing sessions, errors)
- Insurance and financial authorization are included
- Patient portal data is exported from a separate data store (Ontada Health / MongoDB collections)
- Value-based care and Oncology Care Model data are included via dedicated sheets
- Social history, nursing care, clinical trials, adverse events, surveys, and screenings are all represented
- The export goes far beyond USCDI — it includes billing, specialty oncology data, nursing workflows, patient portal data, VBC program data, and many operational patient-record domains that USCDI doesn't address

The only notable gaps are around payments (likely handled by external PM systems) and the absence of explicit cancer staging tables (staging data is almost certainly embedded within existing treatment tables but isn't self-documenting).

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged FHIR or C-CDA endpoint. Key evidence:
- The export format is pipe-delimited flat files — a native database dump, completely separate from Ontada's FHIR R4 API (which covers ~30 US Core resource types)
- The data dictionary documents 249 entities vs. the ~30 FHIR resource types in the (g)(10) API
- The export includes data domains (billing, nursing care, VBC, patient portal, clinical trials, social history) not covered by the FHIR API
- The data dictionary file is named `b10_data_dictionary.xlsx` — explicitly built for the (b)(10) requirement
- The EHI web page references §170.315(b)(10) specifically and describes the pipe-delimited format

### Key Findings

1. **Genuinely comprehensive database dump**: 249 entities with 5,679 fields across 4 data sources (iKnowMed relational DB, VBC system, Patient History, Ontada Health portal). This is one of the more thorough (b)(10) exports among certified products — the vendor clearly engaged seriously with the requirement.

2. **Exceptional oncology specialty depth**: 22 treatment/regimen entities with 570 fields cover chemotherapy cycle management, radiation treatment, surgery, transfusions, treatment history, and regimen definitions. PAT_ORDER at 182 fields and PAT_REGIMEN at 99 fields demonstrate domain-appropriate granularity for a specialty oncology system.

3. **Real billing coverage**: 17 billing/charge entities (284 fields) with ICD code, NDC code, and sent-charge tracking prove the export goes beyond clinical summaries. Insurance and financial authorization tables add another 80 fields.

4. **Documentation quality is a mixed bag**: While the data dictionary is structurally complete (84.8% of fields have descriptions), the descriptions are Java model annotations rather than clinical/business definitions. The complete absence of value set documentation means coded fields are partially opaque without sample data or supplementary documentation.

5. **No sample data or format specification**: The export is documented through a single XLSX file and a brief web page. No example files, no format spec, no relationship diagram. A recipient would know what tables and columns to expect but would struggle to interpret coded values or navigate inter-table relationships.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   Pipe-delimited flat files (ZIP)
    Entities:        249
    Fields:          5,679
    Descriptions:    84.8% (4,814 of 5,679; iKnowMed sheet: 89.5%, VBC/Patient History: 0%)
    Sample data:     No
    Bulk export:     Unclear (page implies single-patient)
    Domains covered: 19 of 21 applicable domains (payments and consents partial/absent)

### Bottom Line

Ontada's iKnowMed (b)(10) export is a serious, purpose-built database dump that covers oncology clinical data, billing, nursing care, patient portal communications, and value-based care — far beyond what a repackaged FHIR or C-CDA export would provide. The biggest weakness is not coverage breadth but documentation depth: value sets are undocumented, relationships are implicit, and there's no sample data, making the export harder to consume than its comprehensive structure deserves.
