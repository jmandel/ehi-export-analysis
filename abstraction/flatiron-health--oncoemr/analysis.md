# EHI Export Analysis: Flatiron Health

**Product**: OncoEMR (part of OncoCloud Suite)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3010.Onco.28.02.1.221221 (OncoEMR v2.8), 15.04.04.3228.Oneo.01.00.1.250516 (OneOncology HIE Integration v1)

## 1. Product Context

OncoEMR is Flatiron Health's oncology-specific cloud-based EHR, the clinical component of the OncoCloud Suite. The suite serves ~2,500 oncology providers across ~800 locations, managing nearly one million active cancer patients. Key modules include:

- **OncoEMR** (Clinical EHR): Oncology charting, CPOE for meds/labs/imaging, 3,000+ NCCN chemotherapy templates, AJCC staging, e-prescribing, drug interaction checking, clinical notes, care coordination
- **OncoBilling**: Claims generation/scrubbing, EDI, remittance/EOB processing, payment allocation, financial reporting
- **OncoAnalytics/Flatiron Insight**: Dashboards, drug utilization, value-based care reporting
- **OncoTrials**: Clinical trial screening/matching, CTMS, regulatory binders
- **CareSpace** (Patient Portal): Health info access, bill payment, scheduling, secure messaging
- **Flatiron Assist**: Clinical decision support with pathways for 25+ disease areas

Based on these capabilities, a comprehensive EHI export should cover: demographics, diagnoses with oncology staging, medications (including chemotherapy regimens and dose calculations), orders, lab results, clinical notes, allergies, immunizations, vitals, imaging, family history, care plans, encounters, billing/charges/claims, insurance/coverage, patient portal communications, questionnaires/assessments, and treatment pathways. Clinical trial data (OncoTrials) is a potential area but may be managed separately.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-data-dictionary.pdf` | 63-page PDF data dictionary (v1.0, last modified 9/9/2025) documenting 125 tables and 2,689 fields. Generated from Google Sheets. **Primary artifact.** | ★★★★★ — the core documentation |
| `downloads/certification-page.html` | OncoEMR ONC Certification page (117 KB HTML). Lists all certified criteria, links to EHI data dictionary. | ★★★ — confirms export access method and context |
| `downloads/certification-page-ehi-section.png` | Screenshot of the EHI export section on the certification page | ★★ — visual confirmation |
| `downloads/certification-page-full.png` | Full-page screenshot of certification page | ★ — context only |
| `downloads/enrichment/data-dictionary.json` | Prior enrichment script's JSON extraction of the PDF (125 tables, 2,689 columns) | ★★★★ — used to cross-validate my own parse |
| `downloads/enrichment/coverage-summary.json` | Category-level summary from enrichment | ★★★ — cross-validation reference |

The data dictionary PDF is the sole substantive artifact. There is no sample data, no machine-readable schema (JSON/XSD/DDL), and no ER diagram. The PDF is well-structured enough to parse programmatically.

## 3. Export Mechanics

- **Format**: CSV (single-patient export), Parquet (population export), plus human-readable files (XML, JPEG, PNG, TIFF, PDF) for encounter summaries, faxes, imaging results, scanned documents
- **Mechanism**: Single patient exports are self-service via the OncoEMR UI. Population exports are requested via the UI and downloaded via UI or SFTP depending on size
- **Single-patient vs bulk**: Both supported — single-patient (CSV) and population-level (Parquet)
- **Access constraints**: Self-service; no mention of fees or special authorization beyond standard user access

This is a native database export in tabular format (CSV/Parquet), not a FHIR or C-CDA repackaging. The FHIR API (g)(10) is maintained as a separate system at `https://flatiron.my.site.com/FHIR/s/`.

## 4. Export Content: What's In It

The data dictionary documents **125 tables** with **2,689 fields**. Of these:
- **2,684 fields (99.8%)** have descriptions
- **2,689 fields (100%)** have data types specified (SQL Server types: varchar, datetime, int, bit, float, etc.)
- **121 of 125 tables (96.8%)** have table-level descriptions
- All fields have nullable flags (TRUE/FALSE)
- Only 5 fields across the entire dictionary lack descriptions (all `SYSSTARTTIMESTR` fields — SQL Server temporal table metadata)
- 4 tables lack descriptions: `Order_Message_Xref`, `QuestionnaireResponse`, `QuestionnaireResponseAnswer`, `QuestionnaireResponseInterpretation`

### Vendor's own content organization

The data dictionary presents tables alphabetically without explicit vendor-defined categories. Based on table names and descriptions, the tables organize into 23 data domains. The full inventory is in `analysis/entity-inventory-full.json`; below is the breakdown by category and the 20 largest entities.

**Category Breakdown:**

| Category | Tables | Fields |
|---|---|---|
| Medications & Orders | 19 | 554 |
| Insurance & Coverage | 10 | 383 |
| Demographics | 12 | 246 |
| Clinical Notes & Documents | 16 | 230 |
| Billing & Financial | 6 | 174 |
| Messaging & Tasks | 9 | 158 |
| Diagnoses & Staging | 5 | 117 |
| Treatment & Pathways | 6 | 116 |
| Immunizations | 3 | 103 |
| Family History | 5 | 97 |
| Encounters | 10 | 89 |
| Labs & Results | 3 | 79 |
| Care Plans & Goals | 4 | 62 |
| Allergies | 2 | 47 |
| Appointments | 3 | 43 |
| Care Team | 3 | 36 |
| Questionnaires | 3 | 36 |
| Devices | 1 | 28 |
| Imaging | 1 | 23 |
| Vital Signs | 1 | 22 |
| Patient Assistance | 1 | 16 |
| Patient Requests | 1 | 16 |
| Prescriptions / E-Prescribing | 1 | 14 |

**20 Largest Entities:**

| Entity | Fields | Category |
|---|---|---|
| Patient_Insurance_History | 208 | Insurance & Coverage |
| Demographics_History | 82 | Demographics |
| Order_History | 72 | Medications & Orders |
| Medication_History | 61 | Medications & Orders |
| Immunization_History | 59 | Immunizations |
| Order_Charge_History | 52 | Billing & Financial |
| Transaction_History | 52 | Billing & Financial |
| DoseCalculationHistory | 48 | Medications & Orders |
| Document_History | 47 | Clinical Notes & Documents |
| Order_Details_History | 46 | Medications & Orders |
| Invoice_History | 44 | Billing & Financial |
| Order_Delivery_History | 40 | Medications & Orders |
| Order_Collection_History | 39 | Medications & Orders |
| Diagnosis_History | 35 | Diagnoses & Staging |
| Inventory_Dispense_History | 34 | Medications & Orders |
| Patient_Guarantor_History | 34 | Insurance & Coverage |
| OrderSet_History | 32 | Medications & Orders |
| Test_History | 32 | Labs & Results |
| Allergy_History | 31 | Allergies |
| Lab_Result_History | 31 | Labs & Results |

**Notable entities:**

- **Patient_Insurance_History** (208 fields) is exceptionally detailed — covers primary/secondary payer details, authorization tracking, eligibility verification, PBM data, prior auth details, copay/coinsurance, coordination of benefits, and more
- **DoseCalculationHistory** (48 fields) captures oncology-specific chemotherapy dosing calculations including BSA, creatinine clearance, AUC, dose caps, and rounding rules
- **Order_History** (72 fields) covers the full order lifecycle from creation through signoff, including drug interaction override tracking
- **Treatment_Current_History** and **Treatment_Previous_History** track oncology treatment regimens
- **Pathways_History** and **RegimenConcordance** capture clinical pathway adherence data
- **Patient_LifetimeDoses_History** tracks cumulative drug dosing (critical for oncology)
- **Visit_Note_Vendor_Writeback** tracks AI-generated content being written back to notes

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is structured as a direct database dump — all tables use `_History` suffixes and SQL Server data types, reflecting the production schema. Coverage is deep across most domains:

**Strongest areas:**
- **Medications & Orders** (19 tables, 554 fields): Most richly documented domain. Covers the full order lifecycle — creation (`Order_History`), details (`Order_Details_History`), collection/delivery/signoff, dose calculations (`DoseCalculationHistory`), inventory dispensing, drug interaction rules, substitution logging, and order sets. This is the depth expected from an oncology system where medication orders are central to care.
- **Insurance & Coverage** (10 tables, 383 fields): Extraordinarily detailed. `Patient_Insurance_History` alone has 208 fields covering every aspect of payer relationships, authorization, eligibility, PBM data, and coordination of benefits. Includes APM (Alternative Payment Model) program/episode/eligibility tables and CDG enrollment.
- **Billing & Financial** (6 tables, 174 fields): Substantial — covers charges (`Order_Charge_History`, 52 fields), invoices (`Invoice_History`, 44 fields), transactions (`Transaction_History`, 52 fields), claim adjustments, and insurer credits.
- **Clinical Notes & Documents** (16 tables, 230 fields): Covers document history, visit note assessment and plans, assessed diagnoses, concurrency tracking, required fields reporting, and vendor writeback (AI-generated content). Includes document assignment workflows.

**Adequate areas:**
- **Demographics** (12 tables, 246 fields): `Demographics_History` (82 fields) is thorough, covering standard demographics plus race/ethnicity granularity, tribal affiliation, sex parameters, and preferred language. Separate tables for address, contact, phone, and email history.
- **Diagnoses & Staging** (5 tables, 117 fields): Includes oncology-specific staging (`Diagnosis_Staging_History`, `Diagnosis_Factors_History`, `Staging_History`) beyond standard problem list data.
- **Treatment & Pathways** (6 tables, 116 fields): Oncology-specific — treatment current/previous history, pathways results, regimen concordance factors. This is data that would NOT appear in a USCDI-only export.

**Thinner but present areas:**
- **Labs & Results** (3 tables, 79 fields): Adequate coverage with lab results, tests, and ask-at-order-entry (AOE) data
- **Vital Signs** (1 table, 22 fields): Single table covering standard vital signs with units and normal ranges
- **Imaging** (1 table, 23 fields): Basic image history plus `RadiologyOrderInformation` (in Medications & Orders, 19 fields) for AUC compliance data

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics_History` (82 fields), `Address_History`, `Contact_History`, `PhoneNumber_History`, `EmailAddress_History`, `SexParameterForClinicalUse`, `PatientOther_History` | Thorough — includes race/ethnicity, tribal affiliation, sex parameters for clinical use |
| Encounters / visits | ✅ Covered | `Encounter` (17 fields), `EncounterParticipant`, `EncounterLocation`, `EncounterDiagnosticReport`, plus 6 more encounter tables | Full encounter model with participants, locations, and diagnostic reports |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis_History` (35 fields), `Diagnosis_Staging_History`, `Diagnosis_Factors_History`, `Staging_History` | Includes oncology-specific AJCC staging; goes well beyond USCDI |
| Medications / prescriptions | ✅ Covered | `Medication_History` (61 fields), `Order_History` (72 fields), `Order_Details_History` (46 fields), plus 16 more tables | Extremely deep — full order lifecycle, dose calculations, drug interactions, inventory |
| Allergies | ✅ Covered | `Allergy_History` (31 fields), `Allergy_Reaction_History` (16 fields) | Includes FDB concept IDs, reaction severity, verification status |
| Immunizations | ✅ Covered | `Immunization_History` (59 fields), `Immunization_Registry_History`, `Immunization_Eval_Forecast_History` | Thorough including registry submission history |
| Vitals | ✅ Covered | `Vital_Sign_History` (22 fields) | Standard vitals with units and normal ranges |
| Lab results | ✅ Covered | `Lab_Result_History` (31 fields), `Test_History` (32 fields), `Test_AOE_History` (16 fields) | Includes ask-at-order-entry data |
| Imaging / diagnostic reports | ✅ Covered | `Image_History` (23 fields), `RadiologyOrderInformation` (19 fields), `EncounterDiagnosticReport` | Basic imaging history plus AUC compliance data |
| Procedures | ⚠️ Partial | Procedures appear embedded in `Order_History` and `Order_Details_History`; no dedicated procedure table | Oncology procedures are likely captured through orders/treatments, but there's no explicit procedure-specific table |
| Clinical notes / documents | ✅ Covered | `Document_History` (47 fields), plus 15 more clinical note tables | Extensive note workflow including assessed diagnoses, required fields, concurrency, AI writeback |
| Care plans / goals | ✅ Covered | `Care_Plan_History`, `Care_Plan_Item_History`, `Care_Plan_Text_History`, `PatientGoals` (62 fields total) | Adequate |
| Orders / referrals | ✅ Covered | `Order_History` (72 fields), `OrderSet_History` (32 fields), `Patient_Request_History` (16 fields) | Full order lifecycle; referrals may be captured through orders or patient requests |
| Insurance / coverage | ✅ Covered | `Patient_Insurance_History` (208 fields), `Patient_Eligibility_History`, `Patient_Guarantor_History`, plus 7 more tables | Exceptionally detailed — the deepest insurance schema seen in any EHI export |
| Claims / billing | ✅ Covered | `Order_Charge_History` (52 fields), `Invoice_History` (44 fields), `Transaction_History` (52 fields), `Claim_Adjustment_History`, `InsurerCredits_History`, `Billing_Visit_History` | Substantial billing data covering charges, invoices, transactions, claims, and adjustments |
| Payments | ✅ Covered | `Transaction_History` (52 fields) covers payment transactions | Part of the billing/financial tables |
| Consents / directives | ❌ Not covered | No consent or advance directive tables found | Product likely stores consent data (standard for oncology practice), but no dedicated tables in export. Minor gap. |
| Patient communications / portal messages | ⚠️ Partial | `Message_History`, `MsgsToSend_History`, plus task/reminder tables (9 tables, 158 fields total) | Message tables present, but unclear if these capture CareSpace portal messages specifically or are internal messaging only |
| Specialty-specific (Oncology) | ✅ Covered | `DoseCalculationHistory` (48 fields), `Treatment_Current_History`, `Treatment_Previous_History`, `Pathways_History`, `Pathways_Results_History`, `RegimenConcordance`, `RegimenConcordanceFactors`, `Patient_LifetimeDoses_History`, `Diagnosis_Staging_History`, `PatientAssistanceActivityDetail` | This is where the export truly distinguishes itself — deep oncology-specific data including chemo dosing, staging, treatment pathways, regimen concordance, and lifetime doses |
| Family history | ✅ Covered | `FamilyHist_History`, `FamilyHist_Person_History`, `FamilyHist_Observation_History`, `FamilyHist_Relative_History`, `FamilyHist_Condition_History` (97 fields total) | Full family history model |
| Questionnaires / assessments | ✅ Covered | `QuestionnaireResponse`, `QuestionnaireResponseAnswer`, `QuestionnaireResponseInterpretation` (36 fields total) | Structured assessment data with answers and interpretations |
| Devices | ✅ Covered | `ImplantableDevice_History` (28 fields) | Covers implantable devices including UDI data |
| Care team | ✅ Covered | `CareTeam`, `CareTeamParticipant`, `CareTeamProvenance` (36 fields total) | Standard care team model |
| Clinical trials | ❌ Not covered | No clinical trial tables in export | Product has OncoTrials module for trial screening/matching/CTMS. This data is absent from the export. Moderate gap for sites using OncoTrials. |

**Coverage: 19 of 21 applicable domains covered (✅ or ⚠️), 2 domains not covered.**

## 6. Documentation Quality

**Strengths:**
- **Near-complete field-level documentation**: 99.8% of fields have descriptions (2,684 of 2,689). Descriptions are practical and informative, e.g., `sAllergyType`: "What is this type of Allergen. The vast majority of these values are Drug. NULL is the second biggest value set."
- **Explicit deprecated field marking**: Fields no longer in use are clearly documented as "Deprecated: Data table is longer in use for recording new patient data."
- **Data types and nullability for every field**: SQL Server types with precision (e.g., `varchar(25)`, `datetime2`)
- **Table-level descriptions**: 121 of 125 tables have descriptions explaining what the table stores
- **Active maintenance**: Last modified 9/9/2025, showing the documentation is not stale

**Weaknesses:**
- **PDF-only format**: No machine-readable schema (JSON, XSD, DDL, CSV). The PDF originated from Google Sheets but the sheet is not published. This means consumers must parse a PDF to understand the schema programmatically.
- **No formal relationships**: Foreign keys are implied through naming conventions (`sPatientID`, `sRowID`, `sGroupID`) and descriptions, but there's no formal ER diagram or FK declarations
- **Value sets are narrative**: Coded fields describe possible values in prose rather than enumerating them (e.g., "The vast majority of these values are Drug" rather than a list of valid values)
- **No sample data**: No example export files are provided
- **No directory structure documentation**: How files are organized in the actual export is undocumented
- **No documentation of Parquet vs CSV structural differences**

**Could a developer build an import from this documentation alone?** Largely yes. The table/column naming is clear and consistent, data types are specified, and descriptions are informative. The main challenge would be reconstructing relationships between tables (implicit via `sPatientID`, `sRowID` patterns) and interpreting coded fields without enumerated value sets.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of what OncoEMR stores. It goes well beyond USCDI clinical data to include:
- **Billing & financial data** (6 tables, 174 fields) — charges, invoices, transactions, claim adjustments
- **Insurance & coverage** (10 tables, 383 fields) — exceptionally detailed payer data
- **Oncology-specific clinical data** — chemotherapy dosing calculations, AJCC staging, treatment pathways, regimen concordance, lifetime cumulative doses
- **Operational clinical data** — order lifecycle tracking, document workflows, messaging, patient assistance programs

The only notable gaps are clinical trial data (OncoTrials module) and advance directives/consents. Given that OncoTrials may be a separate system and consent data is a minor domain, this is a genuinely comprehensive export for an oncology EHR.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. Key signals:
- **Native database schema**: The export uses SQL Server data types and `_History` table naming conventions — this is a direct export of the production database schema, not a translation to a standard format
- **Separate from (g)(10)**: The FHIR API is maintained as a separate system at a different URL, and the certification page distinguishes between them
- **Data breadth far exceeds USCDI**: Billing, insurance (208 fields in a single table), oncology-specific treatment data, dose calculations, pathway concordance — none of this would appear in a USCDI/FHIR (g)(10) export
- **Export format choices** (CSV for single-patient, Parquet for population) are optimized for data portability, not clinical exchange
- **125 tables vs ~26 FHIR resource types** — the scope is an order of magnitude beyond what a repackaged clinical exchange export would provide

### Key Findings

1. **Exceptionally deep insurance documentation**: `Patient_Insurance_History` has 208 fields — the most detailed insurance/coverage table seen in any EHI export analysis. This alone signals genuine engagement with (b)(10) rather than a checkbox exercise.

2. **Strong oncology-specific coverage**: The export includes data domains unique to oncology EHRs — chemotherapy dose calculations (BSA, AUC, creatinine clearance), AJCC staging factors, treatment pathway concordance, lifetime cumulative doses, and patient assistance program tracking. These are not found in any standard clinical exchange format.

3. **Near-perfect documentation quality**: 99.8% of fields have descriptions (only 5 missing), all fields have types and nullable flags, and 96.8% of tables have table-level descriptions. This is among the best-documented EHI exports.

4. **Clinical trial data gap**: Despite OncoTrials being a marketed module of the OncoCloud Suite, no clinical trial tables appear in the export. This may be because OncoTrials is a separate system/database, but it's worth noting.

5. **OneOncology HIE Integration undocumented**: The second certified product (CHPL 11640) has no EHI export documentation at the registered URL. The certification page covers only OncoEMR.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV (single-patient), Parquet (population), plus native-format attachments
    Entities:        125
    Fields:          2,689
    Descriptions:    99.8% of fields
    Sample data:     No
    Bulk export:     Yes (population export via Parquet/SFTP)
    Domains covered: 19 of 21 applicable domains

### Bottom Line

OncoEMR's EHI export is one of the strongest (b)(10) implementations seen — a genuine, purpose-built database export covering 125 tables and 2,689 fields across clinical, billing, insurance, and oncology-specific domains, with near-complete field-level documentation. A patient or provider would receive a comprehensive copy of their data. The only meaningful gaps are clinical trial data (OncoTrials module) and the undocumented OneOncology HIE Integration product.
