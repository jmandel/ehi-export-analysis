# EHI Export Analysis: McKesson Specialty Health Technology Products LLC (Ontada)

**Product**: iKnowMed Generation 2, Version 3
**Analysis date**: 2026-02-16
**CHPL IDs**: 9580 (15.04.04.2920.iKno.30.01.1.180508)

## 1. Product Context

iKnowMed Generation 2 is a cloud-based EHR built exclusively for oncology and hematology practices. It is not a general-purpose EHR — it is a specialty system designed for community oncologists, with deep functionality around chemotherapy treatment planning, cancer staging (AJCC/FIGO), regimen management, precision medicine/biomarker workflows, and drug toxicity monitoring. The system serves ~2,700 oncology providers across 620+ sites of care, primarily within The US Oncology Network (one of the nation's largest community oncology networks).

Key data domains the product is expected to store:
- **Core clinical**: demographics, encounters, problems/diagnoses, medications, allergies, immunizations, vitals, lab results, clinical notes
- **Oncology-specific**: cancer staging, chemotherapy regimens and cycles, radiation/surgery/transfusion treatments, biomarker/molecular testing, treatment response assessments, adverse events, NCCN pathway compliance
- **Orders**: complex order entry with dose calculations (BSA-based), drug interactions
- **Nursing**: IV access/de-access documentation, patient assessments, treatment administration
- **Billing/Charges**: charge capture, EM coding, NDC codes, financial authorizations, insurance
- **Patient engagement**: secure patient portal (Ontada Health) with messaging and appointment requests
- **Care coordination**: transitions of care, Carequality document exchange, CCD reconciliation
- **Surveys/Screenings**: distress thermometer, COVID-19 screening, patient surveys
- **Value-based care**: OCM (Oncology Care Model) episode tracking, VBC program management
- **Clinical trials**: trial definitions and patient enrollment tracking
- **E-prescribing**: via NewCropRx/Surescripts integration

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10_data_dictionary.xlsx` (241 KB) | Official (b)(10) EHI export data dictionary. Excel workbook with 4 sheets: iKnowMed (236 tables, 5,275 fields), VBC (5 tables, 60 fields), Patient History (6 tables, 178 fields), Ontada Health (2 collections, 166 fields). Total: 249 entities, 5,679 fields. | **Primary artifact** — the core documentation of what the export contains |
| `ehi-page.html` (72 KB) | HTML source of the EHI Export Capabilities page at `https://www.ontada.com/point-of-care-solutions/ehi/`. Contains a brief description of the export format and a link to the data dictionary. | Low — only a few sentences of substance |
| `ehi-page-screenshot.png` (313 KB) | Full-page screenshot of the EHI page | Low — confirms page layout |
| `enrichment/data-dictionary.json` (1.6 MB) | Prior agent's structured extraction of the XLSX data dictionary | Cross-reference — verified against my own independent parse |
| `enrichment/summary.json` (35 KB) | Prior agent's summary statistics | Cross-reference — numbers match my independent parse |

**Verification note**: I independently parsed the XLSX using openpyxl and confirmed the prior agent's counts: 249 entities, 5,679 fields, 4 sheets. The EHI page at `https://www.ontada.com/point-of-care-solutions/ehi/` returns HTTP 200 as of 2026-02-16.

## 3. Export Mechanics

- **Format**: ZIP file containing pipe-delimited (`|`) flat files — one file per table/entity
- **Mechanism**: The EHI page states the export "enable[s] the extraction of the electronic health record (EHR) from iKnowMed" but provides no step-by-step instructions for how a user triggers the export. There is no documentation of a UI button, API endpoint, or vendor-assisted process.
- **Single-patient vs bulk**: The page describes extracting "a patient's iKnowMed record," suggesting single-patient export. No mention of bulk/multi-patient capability.
- **Access constraints**: No mention of fees. The page notes content "varies based on" which iKnowMed features are in use, configuration decisions, clinical utilization, and documentation in place.
- **Format details**: The page describes pipe-delimited files but provides no specification of encoding, header rows, null representation, or escaping rules for pipe characters in data values.

## 4. Export Content: What's In It

The export is documented via a single Excel workbook (`b10_data_dictionary.xlsx`) containing field-level schema definitions for 249 entities across 5,679 fields. This represents the vendor's native relational database model (plus two MongoDB-style document collections from the Ontada Health patient portal subsystem).

### Data dictionary structure

Each row in the relational sheets (iKnowMed, VBC, Patient History) provides:
- **TABLE_NAME** and **COLUMN_NAME** — always present
- **DATA_TYPE** — always present (NUMBER, VARCHAR2, DATE, CLOB, TIMESTAMP for relational; String, Boolean, int, UUID, Array for Ontada Health)
- **DATA_LENGTH** — always present for relational sheets
- **TABLE_DESC** — present for iKnowMed sheet (usually the Java class name, sometimes with a brief description); absent for VBC and Patient History sheets
- **COLUMN_DESC** — present for iKnowMed sheet (typically Java field type and optional/required annotation, sometimes with business-level description); absent for VBC and Patient History sheets

**Description coverage**:
- 4,814 of 5,679 fields (84.8%) have any description
- iKnowMed sheet: 4,720 of 5,275 fields (89.5%) have descriptions
- VBC sheet: 0 of 60 fields (0%) — no descriptions at all
- Patient History sheet: 0 of 178 fields (0%) — no descriptions at all
- Ontada Health sheet: 94 of 166 fields (56.6%) have descriptions

**Description quality**: Many iKnowMed field descriptions are terse Java field references (e.g., "Appointment appointment; (optional)") rather than business-level explanations. Of the 4,814 fields with descriptions, I estimate approximately 1,902 (33.5% of total) have substantive descriptions that go beyond a bare class name reference.

**Not documented**:
- No foreign key or relationship documentation
- No entity-relationship diagram
- No value set or code system definitions
- No sample data or example export files

### Vendor's own content organization

The data dictionary is organized across 4 sheets representing distinct subsystems. Below is a breakdown by my categorization of the vendor's entities (full inventory in `analysis/full-entity-inventory.json`):

| Category | Entities | Fields | Fields w/ Description |
|---|---|---|---|
| Medications / Prescriptions | 27 | 686 | 93.7% |
| Oncology Treatment / Regimens | 25 | 613 | 93.6% |
| Orders | 13 | 440 | 80.0% |
| Administrative / Reference | 15 | 346 | 91.3% |
| Documents / Notes | 18 | 339 | 71.7% |
| Demographics | 15 | 307 | 91.5% |
| Billing / Charges | 17 | 287 | 91.6% |
| Nursing Care | 6 | 278 | 93.9% |
| Lab Results | 9 | 214 | 97.7% |
| Patient Engagement / Portal | 12 | 196 | 96.4% |
| Surveys / Screenings | 11 | 196 | 79.1% |
| Social Determinants (Patient History) | 6 | 178 | 0.0% |
| Encounters / Appointments | 11 | 170 | 82.4% |
| Care Coordination | 8 | 167 | 98.2% |
| Patient Portal (Ontada Health) | 2 | 166 | 56.6% |
| Vitals / Observations | 6 | 120 | 91.7% |
| Allergies | 6 | 110 | 97.3% |
| Problems / Diagnoses | 4 | 109 | 84.4% |
| Financial Auth / Insurance | 7 | 103 | 94.2% |
| Oncology Care Model | 4 | 101 | 88.1% |
| Family / Social History | 3 | 85 | 98.8% |
| Immunizations | 4 | 61 | 68.9% |
| Value-Based Care | 5 | 60 | 0.0% |
| Clinical Trials | 2 | 44 | 95.5% |
| Devices | 1 | 31 | 87.1% |
| Adverse Events | 1 | 27 | 100.0% |
| Other / Uncategorized | 11 | 245 | 86.9% |

### 20 largest entities (representative examples)

| Entity | Fields | Described | Category |
|---|---|---|---|
| PAT_ORDER | 182 | 153 | Orders |
| NURSINGCARE_IVACCESS | 122 | 121 | Nursing Care |
| conversation | 101 | 55 | Patient Portal (Ontada Health) |
| PAT_REGIMEN | 99 | 97 | Oncology Treatment / Regimens |
| MEDICATION_PREFERENCE | 92 | 90 | Medications / Prescriptions |
| PAT_ORDER_DOSE | 75 | 73 | Orders |
| NURSINGCARE_IVDEACCESS | 68 | 66 | Nursing Care |
| PAT_DOCUMENT | 66 | 55 | Documents / Notes |
| Patient_appointment_request | 65 | 39 | Patient Portal (Ontada Health) |
| G2_DISTRESS_THERMOMETER | 64 | 0 | Social Determinants (Patient History) |
| NEWDRUGRXTEMPLATE | 60 | 56 | Medications / Prescriptions |
| PAT_WORKFLOW_ITEM | 60 | 45 | Other |
| LOCATION | 57 | 50 | Administrative / Reference |
| PATIENT | 57 | 47 | Demographics |
| NURSINGCARE_PATIENTASSESS | 55 | 54 | Nursing Care |
| PAT_TREATMENT_HISTORY | 54 | 50 | Oncology Treatment / Regimens |
| MEDICATION | 53 | 52 | Medications / Prescriptions |
| PAT_RESULT_HEADER | 53 | 52 | Lab Results |
| PATIENT_PREFERENCE | 51 | 47 | Demographics |
| PAT_TREATMENT | 49 | 44 | Oncology Treatment / Regimens |

### Notable entities

- **PAT_ORDER** (182 fields) is the largest table by far, reflecting the complexity of oncology ordering (chemotherapy dose calculations, BSA-based adjustments, etc.)
- **NURSINGCARE_IVACCESS** (122 fields) demonstrates the depth of nursing documentation for IV chemotherapy administration
- **PAT_REGIMEN** (99 fields) captures oncology regimen data including cycle management, treatment groups, and sequencing
- **G2_DISTRESS_THERMOMETER** (64 fields, 0 descriptions) is the largest entity with zero field descriptions — a oncology distress screening instrument in the Patient History sheet

### Entities with no field descriptions

26 of 249 entities (10.4%) have zero field descriptions. These include all 5 VBC tables, all 6 Patient History tables, and 15 iKnowMed tables (mostly smaller support tables like CLINICAL_NOTE_ADDENDUM, CVX_VIS_LINK, ORDER_QUEUE_NOTE). See `analysis/analysis-stats.json` for the complete list.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The data dictionary documents a near-complete relational database dump of the iKnowMed system. The export's breadth is impressive and clearly reflects the product's native data model rather than a curated clinical summary.

**Deepest coverage** (most entities and fields):
- **Medications / Prescriptions** (27 entities, 686 fields): Extremely thorough — covers the medication itself, prescriptions, dispensables, pharmacy plans, drug templates, Rx alerts, renewal requests, e-prescribing messages, and medication preferences (92 columns for preferences alone).
- **Oncology Treatment / Regimens** (25 entities, 613 fields): The product's specialty strength is well-represented — chemotherapy treatment data, regimen definitions, cycle day management, treatment history across modalities (chemo, radiation, surgery, transfusion, other).
- **Orders** (13 entities, 440 fields): PAT_ORDER at 182 fields captures extremely detailed ordering data, including dose calculations, administration records, and inference data.

**Solidly covered**:
- **Documents / Notes** (18 entities, 339 fields): Comprehensive — clinical documents, LOBs, transcriptions, discharge notes, annotations, fax records.
- **Demographics** (15 entities, 307 fields): Patient identity, contacts, race/ethnicity, language, gender identity, provider relationships, preferences.
- **Billing / Charges** (17 entities, 287 fields): Genuine billing data — charge headers/lines, ICD/NDC codes, sent charges, errors, billing organizations.
- **Nursing Care** (6 entities, 278 fields): Very detailed IV access (122 fields) and nursing assessment documentation.
- **Lab Results** (9 entities, 214 fields): Result headers, values, attachments, with analyte and panel definitions.

**Thinnest coverage**:
- **Value-Based Care** (5 entities, 60 fields, 0% described): All from the VBC sheet with no field descriptions.
- **Clinical Trials** (2 entities, 44 fields): Trial definitions and preferences, but no patient-trial enrollment/outcome data.
- **Devices** (1 entity, 31 fields): Single implantable device table.
- **Adverse Events** (1 entity, 27 fields): Single table for patient adverse events.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENT (57 fields), PATIENT_CONTACT, PATIENT_IDENTIFICATION, PAT_RACE, PAT_ETHNICITY, PAT_LANGUAGE, PAT_GENDER_IDENTITY — 15 entities, 307 fields | Thorough |
| Encounters / visits | ✅ Covered | APPOINTMENT (34 fields), APPOINTMENT_RESOURCE, PAT_ADMIN_DETAIL, PAT_VISIT_TRACKING — 11 entities, 170 fields | Solid |
| Problems / conditions / diagnoses | ✅ Covered | PAT_PROBLEM (36 fields), PAT_PROBLEM_INFERENCE, PROBLEM_DEF, BILLING_DIAG_DEF — 4 entities, 109 fields | Solid; staging likely embedded in problem/regimen fields rather than a dedicated staging table |
| Medications / prescriptions | ✅ Covered | 27 entities, 686 fields — MEDICATION (53 fields), PRESCRIPTION (35 fields), MEDICATION_PREFERENCE (92 fields), DISPENSABLE (35 fields), pharmacy/dispensing/Rx alerts/e-prescribing | Comprehensive |
| Allergies | ✅ Covered | PAT_ALLERGY (36 fields), PAT_ALLERGY_REACTION, ALLERGEN_DEF, severity definitions — 6 entities, 110 fields | Thorough |
| Immunizations | ✅ Covered | PAT_IMMUNIZATION, PAT_IMMUNIZATION_EVENT, PAT_IMMUNIZATION_REGISTRY, CVX_VIS_LINK — 4 entities, 61 fields | Solid |
| Vitals | ✅ Covered | DAILY_VITALS, BASELINE_VITAL (28 fields), TREATMENT_VITAL (22 fields), PAT_PERFORMANCE_STATUS, PATIENT_SMOKING_STATUS — 6 entities, 120 fields | Thorough; treatment-specific vitals for chemo monitoring |
| Lab results | ✅ Covered | PAT_RESULT_HEADER (53 fields), PAT_RESULT_VALUE (41 fields), PAT_RESULT_ATTACHMENT, lab analyte/panel definitions — 9 entities, 214 fields | Comprehensive |
| Imaging / diagnostic reports | ⚠️ Partial | IMAGING_DEF defines imaging types; actual imaging results likely stored via PAT_RESULT_HEADER/VALUE or PAT_DOCUMENT. No dedicated imaging results entity. | Product likely stores imaging orders/reports; representation is indirect |
| Procedures | ✅ Covered | PAT_PROCEDURE_TREATMENT, PATIENT_SURGERY_TREATMENT, PAT_TREATMENT — oncology procedures covered within the treatment framework | Solid |
| Clinical notes / documents | ✅ Covered | PAT_DOCUMENT (66 fields), PAT_DOCUMENT_LOB, TRANSCRIPTION, PAT_DISCHARGE_NOTE (41 fields), CLINICAL_NOTE_ADDENDUM — 18 entities, 339 fields | Comprehensive |
| Care plans / goals | ✅ Covered | PAT_CARE_PLAN, plus treatment regimen structures serve as de facto oncology care plans | Solid |
| Orders / referrals | ✅ Covered | PAT_ORDER (182 fields), PAT_ORDER_DOSE (75 fields), PAT_ORDER_ADMINISTRATION, PAT_ORDER_SESSION — 13 entities, 440 fields | Very comprehensive |
| Insurance / coverage | ✅ Covered | INSURANCE (20 fields), PATIENT_INSURANCE (20 fields), PAT_FIN_AUTH (26 fields) with billing code and ICD links — 7 entities, 103 fields | Solid |
| Claims / billing | ✅ Covered | CHARGE_HEADER, CHARGE_LINE (29 fields), CHARGE_LINE_ICD, CHARGE_LINE_NDC, CHARGE_HEADER_SENT, CHARGE_LINE_SENT — 17 entities, 287 fields | Comprehensive charge capture data |
| Payments | ⚠️ Partial | Charge submission data is present (CHARGE_*_SENT tables) but no dedicated payment/remittance tables visible | Product does charge capture; payment tracking may be in a separate PM system |
| Consents / directives | ⚠️ Partial | PAT_VIEW_DOWNLOAD_TRANSMIT tracks patient access; no dedicated consent or advance directive entity visible | Minor gap — product may not store structured consent data |
| Patient communications / portal messages | ✅ Covered | Ontada Health sheet: conversation (101 fields), Patient_appointment_request (65 fields); iKnowMed: MAIL_MESSAGE, PATIENT_MESSAGE, MESSAGE — 14 entities, 362 fields combined | Comprehensive |
| Specialty-specific (Oncology) | ✅ Covered | 25 oncology treatment entities (613 fields): PAT_REGIMEN (99 fields), PAT_CHEMO_TREATMENT, PATIENT_RADIATION_TREATMENT, cycle day management, treatment history; plus 4 OCM entities (101 fields), distress thermometer, adverse events | This is the product's core strength; well-represented |

### Coverage summary
- **17 of 19 domains**: ✅ Covered
- **2 of 19 domains**: ⚠️ Partial (Imaging reports — indirect representation; Payments — charge data present but no payment/remittance tables)
- **0 domains**: ❌ Not covered

## 6. Documentation Quality

### Strengths
- **Substantial data dictionary**: 249 entities and 5,679 fields across 4 sheets — this is clearly the native database schema, not a curated subset
- **Data types consistently documented**: Every field has a data type and length (for relational sheets)
- **Field descriptions present for most fields**: 84.8% overall, 89.5% for the core iKnowMed sheet
- **Machine-readable format**: XLSX is parseable and structured
- **Multiple subsystem coverage**: Separate sheets for the core EHR (iKnowMed), VBC, Patient History, and Ontada Health portal demonstrate that the export spans multiple subsystems

### Weaknesses
- **No export procedure documentation**: The web page provides a single paragraph describing the format. No screenshots, no step-by-step instructions, no information about who can trigger the export or how.
- **No sample data**: No example export files are provided. A developer has no way to verify format assumptions (header rows, null representation, pipe escaping).
- **No relationship documentation**: There is no ERD, no foreign key documentation, and no explicit relationship metadata. A developer must infer table relationships from column naming conventions (e.g., a PATIENT column of type NUMBER likely references PATIENT.ID).
- **No value set / code system documentation**: Many fields appear to use numeric codes (e.g., status fields, type fields) but the valid values and their meanings are undocumented. This is the single largest gap in documentation quality.
- **Inconsistent description depth**: The VBC and Patient History sheets have zero field descriptions. The iKnowMed sheet descriptions are often terse Java field references rather than business explanations.
- **No format specification**: No documentation of file encoding (UTF-8?), header row conventions, null value representation, or how pipe characters within data values are handled.

### Developer usability assessment
A developer could construct a basic data import from this documentation — they would know the table names, field names, and data types. However, they would struggle significantly with:
1. Understanding coded field values (what does status=3 mean?)
2. Reconstructing table relationships without foreign key documentation
3. Handling format edge cases without sample data or a format spec
4. Understanding the business semantics of fields described only by Java class names

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine (b)(10) implementation. The data dictionary documents 249 entities with 5,679 fields across the vendor's native relational database model plus a document-store subsystem. The export covers clinical, billing, nursing, oncology-specific, patient engagement, and care coordination data. It is clearly not a C-CDA or FHIR repackaging — it is separate from and far more comprehensive than Ontada's (g)(10) FHIR API (which covers ~30 US Core resource types).

### Key Findings

1. **Genuine, broad database export**: 249 entities / 5,679 fields in pipe-delimited flat files — this is the native data model, not a projection into FHIR or C-CDA. Coverage spans 17 of 19 applicable EHI domains with no major gaps.

2. **Oncology specialty data is well-represented**: 25 treatment/regimen entities (613 fields) cover chemotherapy cycles, treatment history across modalities (chemo, radiation, surgery, transfusion), and Oncology Care Model tracking. The PAT_ORDER table alone has 182 fields. This reflects the product's deep oncology specialization.

3. **Billing data is genuinely included**: 17 billing/charges entities (287 fields) plus 7 insurance/financial authorization entities (103 fields) — charge headers, line items, ICD codes, NDC codes, and sent charges are all documented. This is a common gap in other vendors' exports.

4. **Documentation quality is mixed**: While 84.8% of fields have descriptions, many are bare Java class references rather than business-level explanations. The VBC (60 fields) and Patient History (178 fields) sheets have zero descriptions. No value set definitions, no relationship documentation, no sample data.

5. **Export process is opaque**: The web page provides one paragraph about the format. There is no information about how to trigger the export, who has access, or what the actual file structure looks like. No sample data is provided.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   Pipe-delimited flat files in ZIP
Model type:      Native database (relational + document store)
Entities:        249
Fields:          5,679
Descriptions:    84.8% of fields (89.5% in core iKnowMed sheet)
Sample data:     No
Bulk export:     Unclear (described as single-patient)
Domains covered: 17 of 19 applicable domains (2 partial)
```

### Bottom Line

Ontada's (b)(10) export for iKnowMed Generation 2 is one of the more thorough EHI exports in the industry. The 249-entity, 5,679-field data dictionary documents what appears to be a near-complete dump of the oncology EHR's native database, covering clinical, billing, nursing, patient portal, and specialty oncology data. A patient or provider would receive a genuinely comprehensive copy of their data. The biggest weakness is not coverage breadth but documentation depth: no value set definitions, no relationship documentation, and no sample data make it harder than necessary for a recipient to actually interpret the exported data.
