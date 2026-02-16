# EHI Export Analysis: Flatiron Health

**Product**: OncoEMR v2.8 (part of OncoCloud Suite)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3010.Onco.28.02.1.221221 (OncoEMR, ID 11115); 15.04.04.3228.Oneo.01.00.1.250516 (OneOncology HIE Integration, ID 11640)

## 1. Product Context

OncoEMR is a cloud-based, oncology-specific electronic health record system built by Flatiron Health (acquired by Roche in 2018 for $1.9B). It is the clinical EHR component of the broader **OncoCloud Suite**, which also includes OncoBilling (revenue cycle/billing), OncoAnalytics (reporting), OncoTrials (clinical trial management), and CareSpace (patient portal). The system serves approximately 275 oncology practices with ~2,500 providers across ~800 locations managing nearly one million active cancer patients.

**Data domains the product stores (baseline for completeness assessment):**

- **Clinical records**: Patient demographics, diagnoses (with AJCC staging), problem lists, medication lists, allergy lists, clinical notes, treatment plans, chemotherapy regimens and administration records, 3,000+ NCCN chemotherapy order templates
- **Orders**: CPOE for medications (including chemotherapy), lab orders, imaging orders
- **Prescriptions**: SureScripts-certified electronic prescribing
- **Lab results**: Integration with lab systems
- **Billing/financial**: Claims, remittances, EOBs, payment allocations (via OncoBilling)
- **Insurance**: Coverage, authorizations, eligibility verification, PBM data
- **Patient portal**: Health information access, secure messages, appointment scheduling, bill payment (via CareSpace)
- **Clinical trials**: Patient screening, trial matching, regulatory binder, CTMS (via OncoTrials)
- **Oncology-specific**: AJCC staging, chemotherapy dosing, regimen concordance, clinical pathways, lifetime dose tracking
- **Immunization and cancer registry reporting**

**Key context for EHI scope**: OncoEMR is certified for 30+ criteria spanning clinical, care coordination, patient portal, public health, and FHIR API categories — making it a full-featured clinical EHR, not a narrow module.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `downloads/ehi-data-dictionary.pdf` | 63-page PDF data dictionary (400 KB), title "EHI data dictionary v1.0", created from Google Sheets, last modified 9/9/2025. Tabular layout with TableName, ColumnName, Type, Nullable, and Description columns. **Primary artifact.** | ★★★★★ |
| `downloads/enrichment/data-dictionary.json` | Machine-readable JSON extraction of the PDF: 125 tables, 2,689 columns with full metadata. Created by enrichment script. | ★★★★★ |
| `downloads/enrichment/coverage-summary.json` | Tables categorized into 23 data domain categories with summary statistics. | ★★★★ |
| `downloads/certification-page.html` | OncoEMR ONC Certification page (117 KB). Lists certified criteria, relied-upon software (Snowflake, AWS Aurora/PostgreSQL, AWS ECS/S3/EMR), links to EHI data dictionary and FHIR API docs. | ★★★ |
| `downloads/certification-page-ehi-section.png` | Screenshot of the EHI Export Documentation section. Shows single link to data dictionary. | ★★ |
| `downloads/certification-page-full.png` | Full-page screenshot of the certification page. | ★ |
| `downloads/enrichment/extract-data-dictionary.ts` | Bun TypeScript script used to parse the PDF → JSON. Documents parsing methodology. | ★★★ |

**Not found**: No sample export data files, no JSON/XML schema, no entity-relationship diagram, no worked examples.

## 3. Export Mechanics

- **Format**: Single-patient exports use **CSV** files; population exports use **Parquet** files. Additional human-readable files (XML, JPEG, PNG, TIFF, PDF) are included for encounter summaries, faxes, imaging results, and scanned clinical documents.
- **Mechanism**: Single-patient exports are **self-service via the OncoEMR UI**. Population exports are **requested via the OncoEMR UI** and downloaded via UI or SFTP (depending on size).
- **Single-patient vs bulk**: Both are supported — single-patient (CSV) and population-level (Parquet).
- **Access constraints**: No fees mentioned. No API endpoint — exports are UI-initiated.
- **Relied-upon software**: The (b)(10) certification relies on Snowflake, AWS Aurora (PostgreSQL 13.9), AWS ECS, AWS S3, and AWS S3 Batch Operations — indicating the export pipeline pulls from a cloud data warehouse.

## 4. Export Content: What's In It

### Data dictionary scope

The EHI data dictionary documents **125 tables** containing **2,689 columns** across **23 vendor-defined categories**.

- **2,684 of 2,689 columns (99.8%) have descriptions** — plain-English descriptions typically 1–3 sentences long
- **All 2,689 columns have data types** — SQL Server types (varchar, datetime, int, bit, float, binary, etc.) with precision noted (e.g., `varchar(25)`, `varchar(50)`)
- **All but 4 columns have nullable flags** documented (TRUE/FALSE)
- **121 of 125 tables have table-level descriptions** explaining the purpose of each table
- **141 columns are explicitly marked as deprecated** (with explanation: "Data table is longer in use for recording new patient data")
- **2 tables have 0 columns**: `EncounterDocumentReference` and `ExternalEncounter_History` (appear in the dictionary header only)
- **119 tables include a `PARTITION_NAMESPACE` column** (multi-tenant practice identifier)

### Discrepancy from prior report

The prior agent report stated `Patient_Insurance_History` has 189 columns. The actual count from both the parsed JSON and direct PDF inspection is **208 columns**. This is the largest table in the export.

### Vendor's own content organization

The vendor organizes data into tables following a `*_History` naming convention for temporal/versioned patient records. Based on the enrichment's categorization of the 125 tables:

| Category | Tables | Fields | Described | Key Entities |
|----------|--------|--------|-----------|-------------|
| Medications & Orders | 18 | 536 | 536 (100%) | `Order_History` (72), `Medication_History` (61), `Order_Charge_History` (52), `DoseCalculationHistory` (48) |
| Insurance | 10 | 383 | 382 (99.7%) | `Patient_Insurance_History` (208), `Patient_Guarantor_History` (34), `Patient_PBM_History` (30) |
| Clinical Notes & Documents | 14 | 208 | 208 (100%) | `Document_History` (47), `Visit_Note_Assessment_And_Plan` (13), `Data_History` (18) |
| Demographics | 8 | 190 | 190 (100%) | `Demographics_History` (82), `Contact_History` (30), `Address_History` (21) |
| Billing & Financial | 6 | 174 | 174 (100%) | `Transaction_History` (52), `Invoice_History` (44), `Charge_History` (26) |
| Messaging & Tasks | 9 | 158 | 158 (100%) | `Message_History` (31), `SureScripts_Message_History` (22), `Tasks` (18) |
| Other | 9 | 128 | 128 (100%) | `Patient_Information_History` (14), `PatientAssistanceActivityDetail` (16), `Patient_Request_History` (16) |
| Clinical Trials & Pathways | 6 | 116 | 116 (100%) | `Treatment_Current_History` (27), `Treatment_Previous_History` (22), `Pathways_History` (19) |
| Immunizations | 3 | 103 | 103 (100%) | `Immunization_History` (59), `Immunization_Registry_History` (22), `Immunization_Eval_Forecast_History` (22) |
| Family History | 5 | 97 | 97 (100%) | `FamilyHist_Observation_History` (24), `FamilyHist_Person_History` (24) |
| Diagnoses & Conditions | 4 | 91 | 91 (100%) | `Diagnosis_History` (35), `Diagnosis_Staging_History` (20), `Diagnosis_Factors_History` (20) |
| Encounters | 10 | 89 | 88 (98.9%) | `Encounter` (21), `EncounterParticipant` (13), `EncounterDiagnosticReport` (10) |
| Labs & Results | 3 | 79 | 79 (100%) | `Test_History` (32), `Lab_Result_History` (31), `Test_AOE_History` (16) |
| Care Plans & Goals | 4 | 62 | 62 (100%) | `Care_Plan_Item_History` (21), `Care_Plan_History` (16), `PatientGoals` (12) |
| Allergies | 2 | 47 | 47 (100%) | `Allergy_History` (31), `Allergy_Reaction_History` (16) |
| Appointments | 3 | 43 | 43 (100%) | `Appointment_History` (17), `Appointment_Detail_History` (13) |
| Questionnaires | 3 | 36 | 36 (100%) | `QuestionnaireResponse` (15), `QuestionnaireResponseAnswer` (13) |
| Care Team | 3 | 36 | 33 (91.7%) | `CareTeamParticipant` (15), `CareTeamProvenance` (11), `CareTeam` (10) |
| Devices | 1 | 28 | 28 (100%) | `ImplantableDevice_History` (28) |
| Staging (Oncology) | 1 | 26 | 26 (100%) | `Staging_History` (26) |
| Imaging | 1 | 23 | 23 (100%) | `Image_History` (23) |
| Vital Signs | 1 | 22 | 22 (100%) | `Vital_Sign_History` (22) |
| Prescriptions | 1 | 14 | 14 (100%) | `Preferred_Pharmacy_History` (14) |

The full inventory of all 125 entities and 2,689 fields is in `analysis/full-entity-inventory.json`.

### Notable entries

- **Patient_Insurance_History** (208 columns): Exceptionally detailed insurance record covering primary/secondary/tertiary payer details, PBM data, authorization tracking, coverage verification, eligibility, copay/coinsurance amounts, and plan identifiers
- **Demographics_History** (82 columns): Comprehensive demographics including DOB, gender, race, ethnicity, language, marital status, deceased status, tribal affiliation, sexual orientation, gender identity, birth order
- **DoseCalculationHistory** (48 columns): Oncology-specific chemotherapy dosing calculations — BSA, dose reductions, actual vs planned doses
- **Order_History** (72 columns): Full order lifecycle including creation, signing, collection, delivery, and signoff tracking
- **visit_note_vendor_writeback** (12 columns): AI-generated clinical note integration — tracks attempts by an external vendor to write back AI-generated content to Oncoforms

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around the vendor's native database tables, using a `*_History` suffix convention that indicates temporal/versioned records. The deepest categories are:

1. **Medications & Orders** (18 tables, 536 fields): This is by far the richest domain, reflecting OncoEMR's focus on chemotherapy order management. It covers the full order lifecycle: creation (`Order_History`), details (`Order_Details_History`), charges (`Order_Charge_History`), collection (`Order_Collection_History`), delivery (`Order_Delivery_History`), signoff (`Order_SignOff_History`), dose calculations (`DoseCalculationHistory`), drug interactions (`Drug_Rule_Action_History`), inventory dispensing (`Inventory_Dispense_History`), lifetime doses (`Patient_LifetimeDoses_History`), and order sets (`OrderSet_History`).

2. **Insurance** (10 tables, 383 fields): Extremely thorough. `Patient_Insurance_History` alone has 208 columns. Includes eligibility verification (`Patient_Eligibility_History`, `Apm_Eligibility`), authorization tracking (`Insurance_Authorization_History`, `Insurance_Authorization_Detail_History`), guarantor information (`Patient_Guarantor_History`), PBM data (`Patient_PBM_History`), and alternative payment model episodes (`Apm_Episode`, `Apm_Program`).

3. **Billing & Financial** (6 tables, 174 fields): Genuine billing records including charges (`Charge_History`), invoices (`Invoice_History`, 44 fields), transactions (`Transaction_History`, 52 fields), claim adjustments (`Claim_Adjustment_History`), billing visits (`Billing_Visit_History`), and insurer credits (`InsurerCredits`).

4. **Clinical Trials & Pathways** (6 tables, 116 fields): Oncology-specific treatment tracking — current and previous treatments, clinical pathway history, pathway results, regimen concordance, and regimen concordance factors. This covers the treatment pathway component, though not the clinical trial enrollment/screening/CTMS component that OncoTrials provides.

5. **Thinnest categories**: Prescriptions (1 table, 14 fields — just pharmacy preferences), Vital Signs (1 table, 22 fields), Imaging (1 table, 23 fields).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|--------|----------|----------------|--------------|
| Demographics | ✅ Covered | `Demographics_History` (82 fields), `Address_History` (21), `Contact_History` (30), `EmailAddress_History` (17), `PhoneNumber_History` (14), `PatientOtherNames` (6), `SexParameter` (8), `Patient_Location_History` (12) | Thorough — includes race, ethnicity, tribal affiliation, sexual orientation, gender identity, language preferences |
| Encounters / visits | ✅ Covered | `Encounter` (21), `EncounterParticipant` (13), `EncounterLocation` (9), `EncounterStatus` (6), `EncounterClass` (6), `ExternalEncounter` (9), `Billing_Visit_History` (20), `Appointment_History` (17) | Solid — includes encounter classification, participants, locations, and external encounters |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis_History` (35), `Diagnosis_Staging_History` (20), `Diagnosis_Factors_History` (20), `Diagnosis_Staging_Migration_Log` (16), `Staging_History` (26) | Excellent — includes AJCC staging factors, staging history, and migration tracking. Oncology-appropriate depth. |
| Medications / prescriptions | ✅ Covered | `Medication_History` (61), `Order_History` (72), `Order_Details_History` (46), `DoseCalculationHistory` (48), `Patient_LifetimeDoses_History` (13), `Inventory_Dispense_History` (34), `SureScripts_Message_History` (22) | Very thorough — covers medication history, full order lifecycle, chemotherapy dose calculations, lifetime dosing, e-prescribing |
| Allergies | ✅ Covered | `Allergy_History` (31), `Allergy_Reaction_History` (16) | Complete — includes FDB concept IDs, allergy types, reactions, verification dates |
| Immunizations | ✅ Covered | `Immunization_History` (59), `Immunization_Registry_History` (22), `Immunization_Eval_Forecast_History` (22) | Thorough — includes registry submissions, evaluation/forecast |
| Vitals | ✅ Covered | `Vital_Sign_History` (22) | Adequate — covers height, weight, blood pressure, with units and normal ranges; used for BSA/BMI dosing calculations |
| Lab results | ✅ Covered | `Lab_Result_History` (31), `Test_History` (32), `Test_AOE_History` (16) | Good — includes ask-at-order-entry data, test results, lab results |
| Imaging / diagnostic reports | ⚠️ Partial | `Image_History` (23), `EncounterDiagnosticReport` (10), `RadiologyOrderInformation` (19) | Orders and image metadata covered; actual DICOM images not in tabular export (may be in additional file formats per export spec) |
| Procedures | ✅ Covered | Procedures are tracked within `Order_History` and `Order_Details_History` (documented as covering medication, lab, and imaging orders); `Treatment_Current_History` (27), `Treatment_Previous_History` (22) | Covered through order and treatment tables rather than a standalone procedure table |
| Clinical notes / documents | ✅ Covered | `Document_History` (47), `Document_SignOff_History` (15), `DocumentSignoffRequest` (16), `Visit_Note_Assessment_And_Plan` (13), `Visit_Note_Assessed_Diagnoses` (13), `Data_History` (18), `DataNew_History` (14), `visit_note_vendor_writeback` (12), additional human-readable files (XML, PDF) | Good coverage including signoff workflows, AI-generated note writeback, and raw document attachments |
| Care plans / goals | ✅ Covered | `Care_Plan_History` (16), `Care_Plan_Item_History` (21), `Care_Plan_Text_History` (13), `PatientGoals` (12) | Complete |
| Orders / referrals | ✅ Covered | `Order_History` (72), `Order_Details_History` (46), `Order_Codes` (13), `Patient_Request_History` (16) | Thorough order management; referrals partially covered via patient requests |
| Insurance / coverage | ✅ Covered | `Patient_Insurance_History` (208), `Patient_Eligibility_History` (15), `Apm_Eligibility` (11), `Apm_Episode` (18), `Apm_Program` (6), `Insurance_Authorization_History` (27), `Insurance_Authorization_Detail_History` (19), `Patient_Guarantor_History` (34), `Patient_PBM_History` (30), `Patient_CDGEnrollment_History` (15) | Exceptionally thorough — 10 tables, 383 fields |
| Claims / billing | ✅ Covered | `Charge_History` (26), `Invoice_History` (44), `Transaction_History` (52), `Claim_Adjustment_History` (18), `Billing_Visit_History` (20), `InsurerCredits` (14) | Genuine billing data — charges, invoices, transactions, adjustments, credits |
| Payments | ✅ Covered | `Transaction_History` (52), `InsurerCredits` (14) | Payment transactions and insurer credits documented |
| Consents / directives | ⚠️ Partial | No dedicated consent table; consent may be captured in `Document_History` or `Data_History` | Product likely captures consents as documents rather than structured data; not a major gap for an oncology EHR |
| Patient communications / portal messages | ⚠️ Partial | `Message_History` (31), `MsgsToSend_History` (20), `LinkClick_History` (19), `Reminder_History` (17) | Messages and reminders present, but no dedicated CareSpace portal-specific tables (portal interactions, patient-initiated messages, appointment requests via portal, bill payment records). Product has CareSpace patient portal; portal-specific data may be partially captured in these messaging tables |
| Specialty-specific (Oncology) | ✅ Covered | `DoseCalculationHistory` (48), `Diagnosis_Staging_History` (20), `Staging_History` (26), `Treatment_Current_History` (27), `Treatment_Previous_History` (22), `Pathways_History` (19), `Pathways_Results_History` (19), `RegimenConcordance` (18), `RegimenConcordanceFactors` (11), `Patient_LifetimeDoses_History` (13), `PatientAssistanceActivityDetail` (16), `Diagnosis_Factors_History` (20) | Excellent oncology-specific depth — AJCC staging, chemotherapy dosing, treatment pathways, regimen concordance, lifetime dose tracking, patient assistance programs |

### Notable gaps

1. **Clinical trial data**: OncoTrials is a marketed product module with patient screening, trial matching, and CTMS functionality. The export contains treatment pathway and regimen data but **no dedicated clinical trial enrollment, screening, or CTMS tables**. This is a gap if OncoTrials data is stored in the same database as OncoEMR.

2. **Patient portal (CareSpace) data**: CareSpace supports secure messaging, appointment scheduling, and bill payment. While `Message_History` may capture some portal messages, there are no dedicated portal interaction tables for patient-initiated appointment requests, portal login history, or bill payment records.

3. **Cancer registry submissions**: OncoEMR is certified for cancer registry reporting (f)(4), but no dedicated cancer registry submission/response tables are visible in the export beyond immunization registry.

## 6. Documentation Quality

**Strengths:**
- **Near-complete field descriptions**: 2,684 of 2,689 columns (99.8%) have descriptions — this is among the best description coverage of any vendor
- **Data types with precision**: All fields include SQL Server types with precision (e.g., `varchar(25)`, `nvarchar(100)`, `datetime`, `int`, `bit`, `float`)
- **Nullable documentation**: TRUE/FALSE for nearly all fields
- **Table-level descriptions**: 121 of 125 tables have a "Table Description" entry explaining the purpose of each table
- **Deprecated field flagging**: 141 fields explicitly marked as deprecated with explanation
- **Active maintenance**: Last modified 9/9/2025
- **Practical format choices**: CSV for single-patient (universally readable), Parquet for population (efficient for large datasets)

**Weaknesses:**
- **PDF-only delivery**: The data dictionary is only available as a PDF generated from Google Sheets. No machine-readable version (CSV, JSON, DDL, XSD) is provided by the vendor
- **No formal schema**: No SQL DDL, no CREATE TABLE statements, no JSON Schema
- **No entity-relationship diagram**: Foreign key relationships are implicit through naming conventions (`sPatientID`, `sRowID`, `sGroupID`) and description text, but never formally documented
- **No sample data**: No example export files provided; a developer cannot preview what an export looks like
- **No value set enumerations**: Coded fields describe possible values narratively (e.g., `sAllergyType`: "The vast majority of these values are Drug. NULL is the second biggest value set") rather than listing all valid values
- **No export directory structure documentation**: No information about file naming conventions, directory layout, or how to correlate CSV files across tables
- **No Parquet schema documentation**: No documentation of how the Parquet population export differs structurally from the CSV single-patient export

**Developer usability**: A developer could understand the data model and build a basic importer from this documentation. The descriptions are generally clear and informative. However, the lack of explicit foreign keys, value sets, and sample data would require significant trial-and-error to build a complete reconstruction. The naming convention (`s` prefix for strings, `d` for dates, `i` for integers, `b` for booleans, `f` for floats) helps but is not formally documented.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine (b)(10) implementation — a database-level export of OncoEMR's native data model, not a repackaged FHIR or C-CDA export. With 125 tables and 2,689 fields covering clinical, billing, insurance, oncology-specific, and operational domains, it represents a thorough commitment to EHI export. The near-complete field descriptions (99.8%) and thoughtful format choices (CSV/Parquet) set it apart from most vendors.

### Key Findings

1. **Genuine native export, not a standard repackaging**: The export uses OncoEMR's internal database tables with SQL Server data types, not FHIR resources or C-CDA sections. The FHIR API (documented separately at `flatiron.my.site.com/FHIR/s/`) is correctly maintained as a separate (g)(10) implementation. This is what (b)(10) should look like.

2. **Exceptionally detailed insurance model**: `Patient_Insurance_History` has 208 columns — likely the most detailed insurance table of any vendor. Combined with 9 additional insurance-related tables (383 total fields), this reflects the financial complexity of oncology care including prior authorizations, PBM data, and alternative payment models.

3. **Strong oncology-specific depth**: The export includes dedicated tables for chemotherapy dose calculations, AJCC staging, treatment pathways, regimen concordance, and lifetime dose tracking — data that would be completely absent from a standard C-CDA or FHIR export.

4. **Near-universal descriptions but no machine-readable schema**: 99.8% of fields have descriptions (only 5 of 2,689 are blank), which is outstanding. However, the entire data dictionary is delivered only as a PDF with no JSON Schema, DDL, or sample data — making automated processing unnecessarily difficult.

5. **Clinical trial gap**: OncoTrials is a key product module, but no trial-specific tables appear in the export. If OncoTrials data is stored alongside OncoEMR data, this is a meaningful gap in EHI coverage.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (single-patient), Parquet (population), plus XML/JPEG/PNG/TIFF/PDF for documents
Model type:      Native database
Entities:        125
Fields:          2,689
Descriptions:    99.8% (2,684 / 2,689)
Sample data:     No
Bulk export:     Yes (population-level via Parquet + SFTP)
Domains covered: 15 of 18 applicable domains (✅ or ⚠️)
```

### Bottom Line

Flatiron Health's OncoEMR EHI export is one of the stronger implementations: a genuine database-level export with 125 tables, 2,689 fields, and near-complete descriptions covering clinical, billing, insurance, and oncology-specific domains. The biggest gap is the absence of clinical trial data despite OncoTrials being a marketed product module. The main documentation weakness is PDF-only delivery with no machine-readable schema or sample data — outstanding content, suboptimal format.
