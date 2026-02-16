# EHI Export Analysis: Lille Group, Inc.

**Product**: escribeHOST
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.02.05.3058.LILG.01.01.1.220214 (CHPL ID 10830)

## 1. Product Context

escribeHOST is a cloud-based, ONC-certified EHR platform developed by Lille Group, Inc., a small healthcare IT company (11–50 employees) in Albany, NY. The product is purpose-built for **cardiology practices**, with a particular focus on electrophysiology and cardiac device management. The SED intended user description in CHPL metadata is "Cardiology."

Key capabilities that determine what the export should cover:

- **Clinical documentation**: Office visit encounters, procedure notes, cardiac-specific documentation
- **Medications & e-prescribing**: Full Surescripts-integrated e-prescribing workflow (prescriptions, therapies, drug-drug/drug-allergy interaction checking, formulary checking, PDMP history)
- **Lab results**: LOINC-coded lab results with reports and panels
- **Vitals, immunizations, procedures, problems, allergies**: Standard clinical data domains
- **Patient portal**: Secure messaging, document sharing, lab result delivery
- **Insurance & eligibility**: Insurance plan tracking and eligibility verification
- **Surveys & assessments**: Custom clinical surveys/assessments (likely cardiology-specific forms)
- **Cardiac device management**: Remote monitoring transmissions, device recalls, alerts — though this may reside in the separate "Cardiac Signals" platform rather than escribeHOST itself
- **Billing**: Unclear whether billing/claims are within escribeHOST or handled by external systems; the vendor describes integration with "various billing systems"
- **Scheduling**: Appointment management with reminders — but scheduling is operational, not EHI

The product has 31 ONC certification criteria, indicating a comprehensive clinical EHR. The market footprint is very small (likely a handful of cardiology practices in the Albany, NY region).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-doc.html` (478 KB) | Single-page HTML data dictionary documenting the CSV export format for escribeHOST v7.85 (dated 02/09/2026). Contains all 80 tables with 1,246 column definitions. | **Primary artifact** — this is the entirety of the EHI export documentation |
| `downloads/enrichment/ehi-tables.json` (399 KB) | Machine-parsed JSON of the full data dictionary (all 80 tables, all columns with types, descriptions, constraints). Pre-extracted by prior agent. | **High** — verified correct against HTML; used as input for analysis |
| `downloads/enrichment/ehi-tables-summary.json` (23 KB) | Table-level summary (names, descriptions, column counts, PKs, FK hints) | Useful for quick reference |
| `downloads/enrichment/extraction-report.json` (216 bytes) | Parse coverage: 80/80 tables, 1,246 columns, 0 failures | Confirms complete extraction |
| `downloads/enrichment/extract-tables.ts` (7 KB) | Bun TypeScript script used for extraction | Documents methodology |
| `downloads/enrichment/README.md` (1.4 KB) | Enrichment documentation | Contextual |
| `product-research.md` | Prior research on vendor/product capabilities | Background context |
| `ehi-export-report.md` | Prior agent's narrative analysis | Orientation; claims independently verified |

**Verification notes**: I independently verified the HTML contains exactly 80 `<h2>` elements with `id` attributes (one per table) and 1,246 `<tr class="borderBottom">` rows (one per column). These counts match the enrichment extraction exactly.

## 3. Export Mechanics

- **Format**: Comma-separated value (CSV) files, one per database table, reflecting the internal Oracle database structure. Binary files (PDFs, images) are included as separate files in the export package.
- **Model type**: Native database model — CSV files mirror the internal relational schema, not a standard projection (not FHIR, not C-CDA).
- **Mechanism**: The documentation URL (`https://ehr.escribe.com/ehr/api/ehi-export/doc`) suggests an API-based generation, but no explicit instructions for triggering the export are provided. The documentation refers to a "generated export package," implying an automated process.
- **Single-patient vs bulk**: The documentation describes exports in terms of "a patient's Electronic Health Record," suggesting single-patient export. Bulk export capability is not documented.
- **Access constraints / fees**: No login required to access the documentation. No mention of fees or access restrictions for the export itself.
- **Binary files included**: Encounter PDFs, Scanned Cards, PHR Sent Messages, PHR Received Messages, PHR Documents, CCDS Imported Documents, Patient Photos.

## 4. Export Content: What's In It

The export documentation covers **80 database tables** with **1,246 total columns**. This is a native database model export — each CSV file corresponds to an internal Oracle table.

### Documentation quality per field

- **1,139 of 1,246 fields (91.4%) have text descriptions** beyond just a column name
- **107 fields (8.6%) lack descriptions** — concentrated in the tail columns of larger tables (see breakdown below)
- **All 1,246 fields have data types** documented (Oracle types: VARCHAR2, NUMBER, DATE, TIMESTAMP, CLOB)
- **All fields have nullability** documented
- **All primary keys** are explicitly marked
- **38 fields have CHECK constraint value sets** (e.g., `STATUS IN ('APPROVED', 'DENIED', 'PENDING')`)
- **No explicit foreign key documentation** — relationships must be inferred from column naming conventions (`*_ID` columns)
- **No sample data** is provided
- **No value set documentation** beyond CHECK constraints

### Vendor's own content organization

The vendor does not organize tables into named categories; the data dictionary presents all 80 tables alphabetically. The categorization below is my own, based on table names and descriptions. The full inventory is in `analysis/full-entity-inventory.json`.

#### Category breakdown

| Category | Tables | Fields | Described | Description % |
|---|---|---|---|---|
| Medications & Allergies | 11 | 162 | 143 | 88.3% |
| Demographics | 7 | 161 | 149 | 92.5% |
| Lab Results | 6 | 128 | 123 | 96.1% |
| Reference / Lookup | 5 | 113 | 104 | 92.0% |
| Drug History (PDMP) | 4 | 105 | 105 | 100.0% |
| Vitals | 2 | 66 | 60 | 90.9% |
| Encounters | 1 | 56 | 51 | 91.1% |
| Orders | 2 | 52 | 45 | 86.5% |
| Insurance & Eligibility | 3 | 46 | 43 | 93.5% |
| Patient Portal | 5 | 46 | 43 | 93.5% |
| Surveys & Assessments | 6 | 44 | 23 | 52.3% |
| Interventions | 2 | 26 | 21 | 80.8% |
| Problems / Diagnoses | 2 | 25 | 22 | 88.0% |
| Documents | 3 | 23 | 23 | 100.0% |
| Research Studies | 3 | 23 | 19 | 82.6% |
| Devices | 1 | 22 | 22 | 100.0% |
| Patient Education | 3 | 21 | 21 | 100.0% |
| Family History | 2 | 20 | 20 | 100.0% |
| Transitions of Care | 2 | 19 | 19 | 100.0% |
| Immunizations | 1 | 18 | 18 | 100.0% |
| Procedures | 1 | 17 | 12 | 70.6% |
| Social History | 1 | 14 | 14 | 100.0% |
| Care Team | 2 | 11 | 11 | 100.0% |
| Programs | 2 | 9 | 9 | 100.0% |
| Amendments | 1 | 8 | 8 | 100.0% |
| Imaging | 1 | 6 | 6 | 100.0% |
| Transfers | 1 | 5 | 5 | 100.0% |

#### Representative entities (20 largest tables)

| Entity | Columns | Described | Category | Notes |
|---|---|---|---|---|
| PATIENTS | 112 | 100 | Demographics | Core patient record: name, DOB, SSN, sex, marital status, language, preferred contact, etc. |
| RXHUB_DRUG_HISTORY | 89 | 89 | Drug History (PDMP) | PDMP/RxHub medication history with drug details, pharmacy, prescriber, quantities |
| PE_PATIENT_ENCOUNTER | 56 | 51 | Encounters | Patient encounters with location, examiner, dates, status, linked lab reports |
| VITALS | 56 | 50 | Vitals | Vital signs: BP, HR, temp, weight, height, BMI, O2 sat, pain, with linked office visits |
| ORDERS | 44 | 37 | Orders | Clinical orders with CPT codes, ordering/signing provider, results, AUC |
| PROVIDERS | 44 | 41 | Reference / Lookup | Provider demographics, NPI, DEA, specialties, Surescripts IDs |
| LAB_PANELS | 39 | 34 | Lab Results | Lab test panels with reference ranges, source labs, battery/section info |
| MED_RXS | 38 | 33 | Medications & Allergies | Prescriptions with drug, dose, route, frequency, pharmacy, provider, EPCS |
| MED_THERAPIES | 33 | 29 | Medications & Allergies | Medication therapy tracking with status, start/stop dates, refill info |
| USERS | 33 | 29 | Reference / Lookup | EHR system users (linked to PHR patient IDs where applicable) |
| LAB_TEST_RESULTS | 32 | 32 | Lab Results | Individual lab test result values with reference ranges, units, abnormal flags |
| PATIENT_ELIGIBILITY_INFO | 28 | 27 | Insurance & Eligibility | Insurance eligibility details: PBM, formulary, copay, coverage |
| MED_CONCERNS | 22 | 21 | Medications & Allergies | Allergies/adverse reactions with severity, reaction type, onset, status |
| MISC_DEVICES | 22 | 22 | Devices | Medical devices: UDI, brand, model, implant/explant dates, MRI safety |
| LAB_ORGANIZATION | 18 | 18 | Lab Results | Lab organization reference data |
| PATIENT_IMMUNIZATIONS | 18 | 18 | Immunizations | Immunization records with CVX codes, lot, manufacturer, site, route |
| PROBLEMS | 18 | 15 | Problems / Diagnoses | Patient problem list with ICD/SNOMED codes, onset, status, severity |
| LAB_REPORTS | 17 | 17 | Lab Results | Lab report headers with patient, provider, location, status |
| LAB_REPORT_LOCATIONS | 17 | 17 | Lab Results | Lab report location details |
| LOCATIONS | 17 | 15 | Reference / Lookup | Practice location reference data |

#### Tables with weakest description coverage

| Entity | Missing | Total | Category |
|---|---|---|---|
| PATIENTS | 12 | 112 | Demographics |
| MEDS_NOT_ORDERED | 9 | 17 | Medications & Allergies |
| ORDERS | 7 | 44 | Orders |
| SURVEY_FORM_TYPES | 6 | 11 | Surveys & Assessments |
| VITALS | 6 | 56 | Vitals |
| SURVEY_FORM_TYPE_BLOCKS | 4 | 4 | Surveys & Assessments |
| SURVEY_FORM_TYPE_TEXT_BLOCKS | 3 | 3 | Surveys & Assessments |

The Surveys & Assessments category is notably thin on descriptions (52.3% overall), with three tables having zero or near-zero description coverage. These are the form structure definition tables (`SURVEY_FORM_TYPE_BLOCKS`, `SURVEY_FORM_TYPE_TEXT_BLOCKS`, `SURVEY_FORM_TYPES`). The actual survey response data (`SURVEY_FIELD_VALUES`) also has 4/8 fields undescribed.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a genuinely broad set of patient data domains from the native database:

**Richest areas** (most entities, most fields):
- **Medications & Allergies** (11 tables, 162 fields): Comprehensive coverage of active meds, prescriptions, therapies, allergies/concerns, documented/not-documented medication tracking, and medication reconciliation history. This is the deepest domain, reflecting the product's Surescripts e-prescribing integration.
- **Demographics** (7 tables, 161 fields): The PATIENTS table alone has 112 columns — an exceptionally detailed patient record. Supported by separate tables for addresses, previous names, race, ethnicity, and contacts.
- **Lab Results** (6 tables, 128 fields): Full lab workflow from reports to panels to individual results, with lab organization reference data.
- **Drug History / PDMP** (4 tables, 105 fields): RXHUB_DRUG_HISTORY (89 columns) provides prescription drug monitoring data with extensive detail per fill record.

**Moderate coverage**:
- **Vitals** (2 tables, 66 fields): Both provider-recorded and patient-reported vitals.
- **Encounters** (1 table, 56 fields): Single encounter table with comprehensive fields.
- **Orders** (2 tables, 52 fields): Orders with CPT codes and action tracking.
- **Insurance & Eligibility** (3 tables, 46 fields): Insurance plans, eligibility checks, and coverage details.
- **Patient Portal** (5 tables, 46 fields): Messages sent/received, documents, activity log, communications.

**Thinner but present**:
- **Surveys & Assessments** (6 tables, 44 fields): Custom survey forms with definitions and responses — likely captures cardiology-specific assessments, but description coverage is poor (52%).
- **Problems/Diagnoses**, **Interventions**, **Devices**, **Immunizations**, **Procedures**, **Family History**, **Social History**, **Care Team**, **Imaging**, **Transitions of Care**, **Patient Education**, **Amendments**, **Research Studies**, **Programs**, **Transfers** — all present with appropriate entity counts.

**Notably included**:
- Binary files (encounter PDFs, scanned cards, patient photos, portal messages/documents, imported CCDs) are explicitly listed as part of the export package.
- MISC_DEVICES table (22 fields) covers UDI, implant/explant dates, and MRI safety — relevant for cardiac device patients.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENTS (112 fields), PATIENT_ADDRESSES, PATIENT_PREVIOUS_NAMES, PATIENT_RACE, PATIENT_ETHNICITY, PC_PATIENT_CONTACTS, ETHNICITIES | Exceptionally thorough |
| Encounters / visits | ✅ Covered | PE_PATIENT_ENCOUNTER (56 fields) + encounter PDFs as binary files | Solid; encounter PDFs provide clinical narratives |
| Problems / conditions | ✅ Covered | PROBLEMS (18 fields), PROBLEMS_DOCUMENTED (7 fields) | ICD/SNOMED coded, with documentation tracking |
| Medications / prescriptions | ✅ Covered | MEDS, MED_RXS, MED_THERAPIES, MEDS_DOCUMENTED, MEDS_NOT_DOCUMENTED, MEDS_NOT_ORDERED, MEDS_NO_KNOWN, RECONCILIATION_HISTORY (11 tables, 162 fields) | Very deep; includes full Rx workflow |
| Allergies | ✅ Covered | MED_CONCERNS (22 fields), MED_CONCERNS_DOCUMENTED, MED_CONCERNS_NKA_STATUS | Drug allergy/concern tracking with NKA status |
| Immunizations | ✅ Covered | PATIENT_IMMUNIZATIONS (18 fields) | CVX coded, with lot/manufacturer/site |
| Vitals | ✅ Covered | VITALS (56 fields), PATIENT_REPORTED_VITALS (10 fields) | Both provider and patient-reported |
| Lab results | ✅ Covered | 6 tables, 128 fields (LABORATORY_TESTS, LAB_REPORTS, LAB_PANELS, LAB_TEST_RESULTS, LAB_REPORT_LOCATIONS, LAB_ORGANIZATION) | Full lab workflow |
| Imaging / diagnostic reports | ✅ Covered | DIAGNOSTIC_IMAGING_REPORTS (6 fields) | Thin but present; encounter PDFs may supplement |
| Procedures | ✅ Covered | PATIENT_PROCEDURES (17 fields) | CPT coded |
| Clinical notes / documents | ✅ Covered | DOCUMENT_SNAPSHOTS (5 fields) + Encounter PDFs + CCDS_IMPORTED_DOCUMENTS + SCANNED_CARDS | Notes stored as PDFs rather than structured text |
| Care plans / goals | ⚠️ Partial | No dedicated care plan table; PATIENT_PROGRAM_ENROLLMENTS and PATIENT_PROGRAM_SPECS (9 fields) may capture some program-based care planning | Product may not have a formal care plan module; gap significance uncertain |
| Orders / referrals | ✅ Covered | ORDERS (44 fields), ORDERS_ACTIONS (8 fields) | Includes AUC (appropriate use criteria) fields |
| Insurance / coverage | ✅ Covered | PATIENT_INSURANCE (12 fields), PATIENT_ELIGIBILITY_INFO (28 fields), PATIENT_ELIGIBILITY_COVERAGE (6 fields) | Insurance plans, eligibility, coverage detail |
| Claims / billing | ❌ Not covered | No claims, charges, superbills, or billing transaction tables in the export | Unclear if product stores billing data — vendor describes integration with external billing systems. If billing is external, this is N/A rather than a gap |
| Payments | ❌ Not covered | No payment tables | Same as billing — likely external |
| Consents / directives | ⚠️ Partial | AMENDMENT_REQUESTS (8 fields) tracks record amendment requests; no dedicated advance directive or consent table | Product may not have a formal consent management module |
| Patient communications / portal messages | ✅ Covered | PHR_SENT_MESSAGES, PHR_RECEIVED_MESSAGES, PHR_DOCUMENTS, PHR_PATIENT_COMMUNICATIONS, PHR_ACTIVITY_LOG (5 tables, 46 fields) | Comprehensive portal communication export including binary message attachments |
| Specialty-specific (Cardiology) | ⚠️ Partial | MISC_DEVICES (22 fields) covers implantable devices with UDI. SURVEYS tables (6 tables, 44 fields) likely capture cardiology-specific assessment forms. No dedicated cardiac device monitoring/transmission tables. | The Cardiac Signals platform (remote monitoring transmissions, alerts, device recalls) appears to be a separate product. If cardiac monitoring data resides in Cardiac Signals rather than escribeHOST, this is correctly scoped. If any transmission data is stored in escribeHOST, it's missing. |

**Summary**: 14 of 19 applicable domains are fully covered. 3 are partially covered (care plans, consents, specialty cardiac data). 2 are not covered (claims/billing, payments) — but these may be handled by external systems.

## 6. Documentation Quality

**Strengths:**
- The documentation is a single, well-structured HTML page — no navigation required, no login wall, directly accessible at a stable URL
- **91.4% of fields have text descriptions** — well above average for EHI export documentation
- Every field has data type, nullability, and primary key designation
- **38 fields have CHECK constraints** with explicit value sets (e.g., `STATUS IN ('APPROVED', 'DENIED', 'PENDING')`) — rare and valuable
- Table descriptions explain each table's purpose
- Documentation is dated (02/09/2026) and versioned (v7.85), showing active maintenance
- Binary file types included in the export package are explicitly listed

**Weaknesses:**
- **No sample data** or example export files
- **No explicit foreign key documentation** — relationships must be inferred from `*_ID` column naming conventions. While discoverable, this requires effort from a developer
- **No value set documentation** for most coded fields — the 38 CHECK constraints cover a small fraction of fields that likely have constrained value sets (e.g., SEX, STATUS, TYPE columns throughout)
- **No export initiation instructions** — how does a user or administrator trigger the export?
- **No CSV file naming convention** or directory structure documentation for the export package
- **Survey form structure tables** are poorly described (52% description coverage) — a developer would struggle to understand the assessment form model
- **107 fields (8.6%) lack descriptions entirely** — concentrated in tail columns of larger tables

**Could a developer build an import?** Mostly yes. The relational structure is clear, data types are documented, and most fields have descriptions. The main obstacles would be: (1) inferring foreign key relationships from naming conventions, (2) understanding coded value semantics for fields without CHECK constraints, and (3) reconstructing the survey/assessment model from the poorly-described form definition tables.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine (b)(10) export of the vendor's native database model. The export uses CSV files that mirror the internal Oracle table structure, covers 80 tables with 1,246 fields across all major clinical data domains, includes binary files (PDFs, images, portal messages), and is documented with a detailed data dictionary. This is not a C-CDA or FHIR repackaging — it's a direct database export with field-level documentation.

### Key Findings

1. **Genuine native database export**: 80 tables, 1,246 fields exported as CSV files reflecting internal Oracle schema. This is the correct approach for comprehensive (b)(10) compliance, not a standard-based projection. (`downloads/ehi-export-doc.html`)

2. **Strong documentation quality**: 91.4% of fields have text descriptions, all have data types and nullability, 38 fields have CHECK constraint value sets. Documentation is dated, versioned, and actively maintained. This is well above the typical level of EHI export documentation.

3. **Broad domain coverage**: 14 of 19 applicable EHI domains are fully covered, including demographics (112-column PATIENTS table), medications (11 tables), labs (6 tables), encounters, vitals, portal messages, and insurance/eligibility. Binary files (encounter PDFs, scanned cards, patient photos) are explicitly included.

4. **Billing data is absent but may be correctly scoped**: No claims, charges, or payment tables are exported. However, the vendor describes integration with external billing systems, suggesting billing may not be stored in escribeHOST. This is the most significant potential gap but cannot be confirmed as a gap from available evidence.

5. **Cardiac device monitoring data may be in a separate system**: Despite escribeHOST being cardiology-focused, there are no dedicated cardiac device transmission/monitoring tables. The Cardiac Signals platform appears to be a separate product that handles this data. The MISC_DEVICES table covers implantable device reference data but not monitoring workflows.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (one file per table) + binary files (PDFs, images)
Model type:      Native database (Oracle tables exported as CSV)
Entities:        80 tables
Fields:          1,246
Descriptions:    91.4% of fields have descriptions
Sample data:     No
Bulk export:     Unclear (documentation describes single-patient export)
Domains covered: 14 of 19 applicable domains fully covered; 3 partial; 2 absent (likely external)
```

### Bottom Line

This is one of the better (b)(10) implementations. A patient or provider would receive a genuinely comprehensive export of their clinical data — demographics, medications, labs, vitals, encounters, portal messages, documents, and more — in a machine-readable CSV format with a detailed data dictionary. The main uncertainty is whether billing and cardiac device monitoring data are stored in escribeHOST or in separate systems; if the former, those would be significant gaps. The documentation is practical, accessible, and well-maintained.
