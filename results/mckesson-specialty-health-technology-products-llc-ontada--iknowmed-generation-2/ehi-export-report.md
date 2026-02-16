# McKesson Specialty Health Technology Products LLC (Ontada) — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.ontada.com/Providers-Solutions/EHI/
- Final URL (after redirect): https://www.ontada.com/point-of-care-solutions/ehi/
- CHPL ID: 9580 (15.04.04.2920.iKno.30.01.1.180508)
- Product: iKnowMed Generation 2, Version 3
- Certification date: 2018-05-08

## Navigation Journal

1. **Initial probe** — HTTP HEAD with curl:
   ```
   curl -sI -L "https://www.ontada.com/Providers-Solutions/EHI/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: 301 redirect from `/Providers-Solutions/EHI/` to `/point-of-care-solutions/ehi/`, then 200 OK with `text/html` content type. Site is behind Cloudflare and Imperva CDN.

2. **Fetched the page** — 72KB HTML page titled "iKnowMed® EHI Export Capabilities". The page is a simple single-page document (not an SPA) with:
   - A brief description of the EHI export format
   - A link to the (b)(10) Data Dictionary (XLSX)
   - A list of factors that affect export content variability
   - No additional sub-pages, accordions, or hidden sections

3. **Found downloadable file** — searched HTML for file links:
   ```
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json)' page.html
   ```
   Found one file: `/siteassets/documents/b10_data_dictionary.xlsx`

4. **Downloaded the data dictionary**:
   ```
   curl -sL "https://www.ontada.com/siteassets/documents/b10_data_dictionary.xlsx" -H 'User-Agent: Mozilla/5.0' -o b10_data_dictionary.xlsx
   ```
   Confirmed: `file` reports "Microsoft Excel 2007+", 240KB.

5. **Took a full-page screenshot** of the EHI page in Chrome for visual documentation.

6. **No additional documentation found.** The page contains only the description and the single data dictionary download. There are no links to export format specifications, API docs, sample data, schema files, or user guides beyond what is on the page. The two external links on the page (to healthit.gov and the ONC certification criteria) are standard regulatory references, not vendor-specific documentation.

## What Was Found

### Export Format

The EHI export from iKnowMed Generation 2 produces a **ZIP file containing pipe-delimited (|) flat files** — one file per table/entity in the export. This is a proprietary database dump format, not a standard like FHIR or C-CDA. The page explicitly states this satisfies §170.315(b)(10).

The page notes that export content varies by organization based on:
- Which iKnowMed features are in use
- Configuration decisions made by the healthcare organization
- The organization's clinical utilization of iKnowMed
- The documentation in place at the healthcare organization

### Data Dictionary (b10_data_dictionary.xlsx)

The data dictionary is a substantial Excel workbook with **4 sheets, 249 entities, and 5,679 field definitions**:

**Sheet 1: iKnowMed** — 236 tables, 5,275 columns. This is the core EHR database schema and constitutes the vast majority of the export. Each row provides: TABLE_NAME, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, TABLE_DESC, and COLUMN_DESC. The descriptions are brief (typically just the Java class name) but present for most tables. Column descriptions are more substantive, often including the Java field type and optional/required annotations.

Key table groups in the iKnowMed sheet:
- **Patient demographics**: PATIENT (57 cols), PATIENT_CONTACT, PATIENT_IDENTIFICATION, PAT_RACE, PAT_ETHNICITY, PAT_LANGUAGE, PAT_GENDER_IDENTITY
- **Clinical problems & diagnoses**: PAT_PROBLEM (36 cols), PAT_PROBLEM_INFERENCE, PROBLEM_DEF, BILLING_DIAG_DEF
- **Medications & prescribing**: MEDICATION (53 cols), PATIENT_MEDICATION, PRESCRIPTION (35 cols), MEDICATION_PREFERENCE (92 cols), DISPENSABLE (35 cols), NEWDRUGRXTEMPLATE, RXRENEWALREQUEST, RX_CHANGE_REQUEST, RX_FILL_NOTIFICATION
- **Orders & administration**: PAT_ORDER (182 cols — the largest table), PAT_ORDER_DOSE (75 cols), PAT_ORDER_ADMINISTRATION, PAT_ORDER_SESSION, PAT_ORDER_GROUP, PAT_ORDER_DISCONTINUATION, PAT_ORDER_INFERENCE
- **Treatment regimens (oncology-specific)**: PAT_REGIMEN (99 cols), PAT_REGIMEN_CYCLE_DAYS, PAT_REGIMEN_INFERENCE, PAT_REGIMEN_SEQUENCE, PAT_REGIMEN_TREATMENT_GROUP, REGIMEN_DEF (41 cols), PAT_CHEMO_TREATMENT (34 cols), DATE_CYCLE_DAY, CYCLE_DAY_DELAY, CYCLE_DAY_MOVE
- **Other oncology treatments**: PATIENT_RADIATION_TREATMENT (29 cols), PATIENT_SURGERY_TREATMENT, PAT_HOSPITAL_TREATMENT, PAT_OTHER_TREATMENT, PAT_PROCEDURE_TREATMENT, PAT_TRANSFUSN_TREATMENT, PAT_TREATMENT (49 cols), PAT_TREATMENT_HISTORY (54 cols)
- **Lab results**: PAT_RESULT_HEADER (53 cols), PAT_RESULT_VALUE (41 cols), PAT_RESULT_ATTACHMENT, LAB_ANALYTE_DEF, LAB_PANEL_DEF, EXTERNAL_RESULT_PANEL_DEF, EXTERNAL_RESULT_VALUE_DEF
- **Vitals & observations**: DAILY_VITALS, BASELINE_VITAL (28 cols), TREATMENT_VITAL (22 cols), TREATMENT_VITAL_SET, PAT_PERFORMANCE_STATUS, PATIENT_SMOKING_STATUS
- **Allergies**: PAT_ALLERGY (36 cols), PAT_ALLERGY_REACTION, PAT_ALLERGY_ALERT, ALLERGEN_DEF, ALLERGEN_REACTION_DEF, ALLERGEN_SEVERITY_DEF
- **Immunizations**: PAT_IMMUNIZATION, PAT_IMMUNIZATION_EVENT, PAT_IMMUNIZATION_REGISTRY
- **Documents & notes**: PAT_DOCUMENT (66 cols), PAT_DOCUMENT_LOB, PAT_DOCUMENT_ANNOTATION, PAT_DOCUMENT_ENTITY_REF, PAT_DOCUMENT_RECIPIENT, TRANSCRIPTION, TRANSCRIPTION_LOB, CLINICAL_NOTE_ADDENDUM, CLINICAL_NOTE_DM_STATUS, PAT_DISCHARGE_NOTE (41 cols)
- **Billing & charges**: CHARGE_HEADER, CHARGE_LINE (29 cols), CHARGE_LINE_ICD, CHARGE_LINE_NDC, CHARGE_HEADER_SENT, CHARGE_LINE_SENT, CHARGE_LINE_SENT_ICD, CHARGE_LINE_SENT_NDC, CHARGE_COMMENT, CHARGE_ERROR, CHARGE_SOURCE, BILLABLE_ITEM, BILLING_CODE_DEF, BILLING_ORG, PAT_DOS_BILLING_SESSION
- **Financial authorizations**: PAT_FIN_AUTH (26 cols), PAT_FIN_AUTH_BILLINGCODE, PAT_FIN_AUTH_ICD, PAT_FIN_AUTH_ORDER, PAT_FIN_AUTH_TEMPLATE_ORDER
- **Insurance**: INSURANCE (20 cols), PATIENT_INSURANCE (20 cols)
- **Care coordination**: PAT_CARE_PLAN, PATIENT_TRANSFER (46 cols), PATIENT_TRANSFER_PROBLEM, CCD_RECONCILIATION, CCD_MANUAL_RECONCILIATION, CQ_DOC_SEARCH_QUERY, CQ_DOC_SEARCH_RESULT, CQ_DOC_RETRIEVE_RESULT (Carequality document exchange)
- **Appointments & scheduling**: APPOINTMENT (34 cols), APPOINTMENT_RESOURCE, APPOINTMENT_SCHEDULE, APPOINTMENT_EMCODE, NURSING_APPOINTMENT_RESOURCE
- **Nursing care**: NURSINGCARE_IVACCESS (122 cols), NURSINGCARE_IVDEACCESS (68 cols), NURSINGCARE_PATIENTASSESS (55 cols), NURSINGCARE_PATIENTNOTE, NURSINGCARE_BILLABLE_ITEM
- **Patient engagement**: PAT_EDUCATION_EVENT, PAT_ED_SESSION, PATIENT_MESSAGE, MAIL_MESSAGE and related
- **Adverse events**: PATIENT_ADVERSEEVENT (27 cols), PAT_DRUGDOSE_ALERT, RXALERT
- **Clinical trials**: CLINICAL_TRIAL_DEF (28 cols), CLINICAL_TRIAL_DEF_PREF
- **Surveys & screenings**: PAT_SURVEY, PAT_SURVEY_ITEM, PAT_SURVEY_LINE_ITEM, PAT_SURVEY_TEMPLATE, PAT_SCREENING, PAT_SCREENING_EVENT, PAT_COVID19_SCREENING
- **Oncology Care Model**: PAT_OCM_EPISODE (42 cols), PAT_OCM_HEADER (38 cols), PAT_OCM_MONTHLY
- **Administrative**: PRACTICE (42 cols), PROVIDER (29 cols), LOCATION (57 cols), RESOURCES, RESOURCE_GROUP, RESOURCE_SCHEDULE
- **E-prescribing**: ERXMESSAGEQUEUEITEM, OUTBOUND_ORDER_TX
- **Implantable devices**: IMPLANTABLE_DEVICE (31 cols)
- **Files & attachments**: FILE_ATTACHMENT, FILE_ATTACHMENT_LOB
- **Other**: PATIENT_VASCULAR_ACCESS, OBGYN_HISTORY (43 cols), PAT_COGNITIVE_STATUS, PAT_DEPRESSION_STATUS, PAT_WORKFLOW_ITEM (60 cols)

**Sheet 2: VBC (Value-Based Care)** — 5 tables, 60 columns. Patient eligibility, status by program, logged tasks, and attachments related to value-based care programs. No descriptions provided.

**Sheet 3: Patient History** — 6 tables, 178 columns. Social determinants of health and patient-reported outcomes:
- G2_DISTRESS_THERMOMETER (64 cols) — oncology distress screening
- G2_SOCIALHX_INT_TRAVEL_HX — international travel history
- G2_SOCIALHX_LIFESTYLE — lifestyle factors
- G2_SOCIALHX_LIVING_ENV — living environment
- G2_SOCIALHX_SUBSTANCE_USE (34 cols) — substance use history
- G2_SOCIALHX_WORKING_ENV — working environment
All columns use VARCHAR2 data types with lengths. No descriptions.

**Sheet 4: Ontada Health** — 2 collections, 166 fields. Uses a document/collection schema (MongoDB-style) rather than relational tables:
- **conversation** (101 fields) — patient portal messaging with detailed conversation metadata, message threads, attachments, recipients, and routing
- **Patient_appointment_request** (65 fields) — appointment request tracking with scheduling preferences and slot details
Fields include Data Type and Description columns, making this sheet the most descriptive after iKnowMed.

## Export Coverage Assessment

### Data Domain Coverage

This is a **genuinely comprehensive (b)(10) export** — one of the more thorough we've seen. The data dictionary documents what appears to be a near-complete relational database dump of the iKnowMed system, not a curated subset.

**Clearly covered domains:**
- **Patient demographics** — full coverage including race, ethnicity, language, gender identity, contacts, identifications
- **Clinical problems/diagnoses** — problems, inferences, billing diagnosis mappings
- **Medications** — extensive coverage: prescriptions, external medications, medication administration, dispensing, renewal requests, Rx change requests, fill notifications, drug dose alerts, medication preferences (92 columns)
- **Orders** — the PAT_ORDER table at 182 columns is extraordinarily detailed, with associated dose, administration, inference, discontinuation, and session tables
- **Oncology treatment** — this is where iKnowMed's specialty depth shines. Chemotherapy regimens (99 columns), cycle day management, treatment groups, treatment history, radiation treatment, surgery treatment, transfusion treatment, hospitalizations, and other treatment types are all documented
- **Lab results** — result headers, values, attachments, with analyte and panel definitions
- **Vitals** — daily vitals, baseline vitals, treatment vitals
- **Allergies** — patient allergies with reactions and severity definitions
- **Immunizations** — including registry reporting tracking
- **Documents and notes** — patient documents with LOBs (large objects), annotations, recipients; transcriptions with LOBs; discharge notes; clinical note addenda
- **Billing and charges** — charge headers, lines, ICD codes, NDC codes, sent charges, errors, comments — comprehensive billing record coverage
- **Insurance** — insurance definitions and patient insurance records
- **Financial authorizations** — prior auth tracking with billing codes, ICD codes, and orders
- **Care coordination** — care plans, patient transfers, Carequality document exchange tracking, CCD reconciliation
- **Nursing care** — IV access (122 columns!), de-access, patient assessments, notes, billable items
- **Adverse events** — patient adverse events, drug dose alerts, prescription alerts
- **Social history** — substance use, living environment, working environment, lifestyle, travel history (in Patient History sheet)
- **Patient-reported outcomes** — distress thermometer (oncology screening), surveys, screenings
- **Value-based care** — patient eligibility, program status, logged tasks (VBC sheet)
- **Patient portal** — conversations, appointment requests (Ontada Health sheet)
- **Oncology Care Model** — episode, header, and monthly tracking tables
- **Clinical trials** — trial definitions and preferences
- **Implantable devices** — 31 columns of device tracking
- **Family history** — PAT_RELATIVE, PAT_RELATIVE_PROBLEM

**Domains with potential gaps or ambiguity:**
- **Cancer staging data** — While the product research describes AJCC and FIGO staging, there is no dedicated staging table. Staging information is likely embedded within PAT_PROBLEM, PAT_REGIMEN, or PAT_TREATMENT columns, but this isn't explicit from the data dictionary alone. The column descriptions in those tables could clarify this.
- **Biomarker/molecular testing** — The product research highlights biomarker ordering and precision medicine, but there's no dedicated biomarker table. These may be represented as lab results (PAT_RESULT_HEADER/PAT_RESULT_VALUE) or within the order system, but it's not obvious.
- **NCCN pathway compliance** — Clear Value Plus decision support data and pathway compliance tracking are product features, but it's unclear which tables store this. PAT_REGIMEN_INFERENCE and PAT_ORDER_INFERENCE might contain some of this.
- **Clinical decision support alerts** — The ALERT table (22 cols) and PAT_CHART_ALERT may cover CDS alerts, but specifics about drug-drug interaction alerts or BSA-related alerts aren't clearly mapped.
- **Images/imaging results** — IMAGING_DEF defines imaging types, but there's no dedicated imaging results table beyond what may be in PAT_RESULT_HEADER/VALUE or PAT_DOCUMENT.

**Not missing (correctly scoped):**
- Audit logs (not EHI) — not present, correctly excluded
- System configuration (not EHI) — not present as patient data
- Quality metrics aggregates (not EHI) — not present, correctly excluded
- Provider credentialing (not EHI) — PROVIDER table has provider info but not credentialing details

### Export Format & Standards

The export uses a **proprietary pipe-delimited flat file format** — essentially a database dump with one file per table. This is an appropriate format for a (b)(10) export because:

1. It captures the full relational data model, not a lossy projection into a standard like FHIR
2. Pipe-delimited files are straightforward to parse
3. The data dictionary provides the schema needed to interpret the files
4. The ZIP packaging makes the export portable

This is notably **not** FHIR and is completely separate from Ontada's (g)(10) FHIR API. The FHIR API (documented elsewhere) covers 30+ US Core resource types — the (b)(10) export covers 249 entities with 5,679 fields. This is a genuine (b)(10) implementation, not a repackaged (g)(10) FHIR endpoint.

The format does have limitations:
- **Relationships between tables are implicit** — foreign keys are present (columns like APPOINTMENT, PATIENT, PRACTICE reference IDs) but there's no explicit relationship documentation or ERD
- **No sample data** — there are no example export files to demonstrate the actual format
- **Value sets are undocumented** — coded fields (many columns appear to use numeric codes) don't have their value set mappings documented in the data dictionary

### Documentation Quality

**Strengths:**
- The data dictionary is substantial — 249 entities covering what appears to be the full database schema
- The main iKnowMed sheet includes both table-level and column-level descriptions
- Data types and lengths are consistently documented
- The column descriptions often include Java class type annotations (e.g., "Appointment appointment; (optional)") which reveal the object model

**Weaknesses:**
- **Minimal export instructions** — the web page provides only a brief paragraph about the export being a ZIP with pipe-delimited files. There are no step-by-step instructions for how a user actually triggers the export
- **No sample data** — no example export files are provided
- **No relationship documentation** — no entity-relationship diagram or foreign key documentation. A developer would need to reverse-engineer table relationships from column names
- **Inconsistent descriptions** — the VBC and Patient History sheets lack column descriptions entirely. The Ontada Health sheet has descriptions but in a different schema format
- **No value set documentation** — columns that contain coded values (e.g., status codes, type codes) don't document what the valid codes are or what they mean
- **Column descriptions are terse** — many descriptions are just the Java class name (e.g., "PatAllergy") which tells you the object model class but not the business meaning

A developer could construct a reasonable data import from this documentation, but would struggle with:
- Understanding which codes mean what in coded fields
- Knowing the exact relationships between tables
- Understanding the actual file format details (encoding, header rows, null representation, escaping rules for pipe characters in data)

### Structure & Completeness

**Granularity**: Field-level documentation with column names, data types, and lengths for all 5,679 fields. Column descriptions present for the iKnowMed sheet (~5,275 columns) but absent for VBC and Patient History sheets.

**Data types**: Consistently documented across sheets — NUMBER, VARCHAR2, DATE, CLOB, TIMESTAMP for relational sheets; String, Boolean, int, UUID, Array for Ontada Health collections.

**Cardinality**: Not explicitly documented, but the column descriptions often include "(optional)" annotations from the Java model.

**Relationships**: Not documented. Foreign keys must be inferred from column naming conventions (e.g., PATIENT column in most tables likely references PATIENT.ID).

**Value sets**: Not documented. This is the single biggest gap — without knowing what the coded values mean, many fields are opaque.

**Versioning**: No version number or change history on the data dictionary. The XLSX has no metadata about when it was last updated.

## Overall Assessment

Ontada's (b)(10) EHI export documentation is **above average** for the industry. The key strengths are:

1. **This is a real (b)(10) export**, not a repackaged FHIR API. The 249-table, 5,679-field data dictionary describes a comprehensive database dump that goes far beyond USCDI/US Core data classes.

2. **The oncology specialty data is well represented.** Chemotherapy regimens, cycle day management, treatment history, radiation/surgery/transfusion treatments, adverse events, nursing care (including detailed IV access documentation), distress screening, and Oncology Care Model tracking are all present. This reflects the product's deep oncology specialization.

3. **Billing data is included.** The CHARGE_* tables, financial authorization tables, insurance tables, and billing session tables demonstrate coverage of the billing domain — a common gap in other vendors' exports.

4. **Patient portal and VBC data are included.** Separate sheets for the Ontada Health patient portal (conversations, appointment requests) and Value-Based Care program data show these subsystems are exported.

The documentation falls short in:
1. **Lack of export procedure documentation** — no instructions for how to actually perform the export
2. **Missing value set definitions** — coded fields are documented structurally but not semantically
3. **No relationship documentation** — the relational model must be reverse-engineered
4. **No sample data or format specification** — the exact pipe-delimited format details (encoding, escaping, headers) are undocumented
5. **Minimal web page** — the entire export documentation is essentially one paragraph plus one XLSX file

Despite these gaps, the breadth of data documented in the data dictionary is impressive. A recipient of this export would have a nearly complete dump of the oncology EHR's database, covering clinical, billing, nursing, patient engagement, and specialty oncology data.

## Access Summary
- Final URL (after redirects): https://www.ontada.com/point-of-care-solutions/ehi/
- Status: found
- Required browser: no (curl works fine)
- Navigation complexity: direct_link (one redirect, then a single page with one download link)
- Anti-bot issues: Cloudflare and Imperva CDN present but did not block requests with standard User-Agent header

## Obstacles & Dead Ends
- The registered URL (`/Providers-Solutions/EHI/`) 301-redirects to `/point-of-care-solutions/ehi/` — appears to be a site reorganization. The redirect works cleanly.
- No obstacles encountered. The page loaded immediately, the XLSX downloaded without issues, and no authentication was required.
- `pip` was not available in the environment for `openpyxl`, but `bun` with the `xlsx` npm package worked as an alternative for parsing the Excel file.
