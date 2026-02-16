# EHI Export Analysis: VersaSuite

**Product**: VersaSuite 9.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.99.04.2503.Vers.09.01.1.200210 (CHPL #10299)

## 1. Product Context

VersaSuite is a monolithic, all-in-one healthcare IT platform developed by Universal Software Solutions Inc. (Austin, TX), targeting small to mid-size hospitals, critical access hospitals, specialty hospitals (surgical, behavioral health, LTAC, rehabilitation, hospice), and ambulatory clinics. It runs on a single database with a single framework, covering clinical, administrative, and financial functions.

Key modules and capabilities relevant to EHI export completeness:

- **Clinical/EHR**: Electronic health records with specialty-specific templates, CPOE, EMAR, ETAR, clinical decision support, ED workflows
- **Laboratory & Imaging**: LIMS for lab ordering/results, RIS/PACS for radiology
- **Pharmacy**: Medication management, formulary, e-prescribing
- **Practice Management & Billing**: Scheduling, registration, billing, AR, collections, POS
- **Health Information Management**: Medical records, coding (TruCode integration)
- **Patient Portal**: Patient access, FHIR API
- **Nutrition**: Clinical nutrition & food services
- **Administrative/ERP**: Accounting/GL, payroll, HR, time & attendance, employee scheduling, budgeting, facility management, procurement, inventory management
- **Public Health Reporting**: Certified for immunization registries, electronic case reporting, syndromic surveillance, cancer case reporting

The single-database architecture means a comprehensive (b)(10) export should be able to access all clinical, financial, and administrative data without crossing system boundaries. The product claims 36 integrated modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/data-dictionary/index.html` (14,838 bytes) | Main EHI export documentation page; describes export mechanism and links to 96 data dictionary pages | **High** — primary source for export mechanics |
| `downloads/data-dictionary/*.html` (96 files, ~660 KB total) | Individual HTML data dictionary pages, one per exported CSV table; each with 3-column tables (Original Column Name, Expanded Column Name, Description) | **High** — core documentation artifacts |
| `downloads/enrichment/data-dictionary.json` | Pre-parsed JSON of all 96 data dictionary HTML pages (by prior collection agent) | **Medium** — useful for cross-validation |
| `downloads/enrichment/data-dictionary-summary.json` | Summary statistics from prior agent's parse | **Medium** — cross-validated against our independent parse |
| `downloads/enrichment/extract-data-dictionary.ts` | TypeScript extraction script used by prior agent | **Low** — methodology reference only |
| `downloads/screenshot-main-page.png` | Screenshot of the main documentation page | **Low** — confirms page layout |

**No sample data files, schema files (XSD/JSON Schema/DDL), or user guides were found.** The entire documentation is the index page plus 96 HTML data dictionary pages.

## 3. Export Mechanics

- **Format**: CSV files (one per database table) plus associated images/documents in original formats
- **Mechanism**: Built-in "ehi export tool" accessible through VersaSuite's UI. Access limited to specific users or system administrators; no developer assistance required.
- **Single-patient**: Yes — exports a single patient's EHI into a patient-specific folder
- **Bulk/Population**: Yes — supports patient population export
- **Output organization**: Patient-specific folders within VersaSuite's default export folder
- **Selective export**: Tables without data for the target patient are omitted
- **Access constraints**: Limited to authorized users/system administrators; no fees mentioned
- **Documentation URL**: https://docs.versasuite.com (publicly accessible, no authentication required)

## 4. Export Content: What's In It

### Overview

The export consists of CSV files corresponding to 96 documented database tables (95 unique tables; EM_AdminHis is documented in two separate files at different detail levels). Our independent parse (see `analysis/parse_data_dictionary.py`) confirms:

- **96 HTML pages** parsed successfully (0 parse errors)
- **95 unique tables** documented
- **2,338 total columns** (after deduplicating EM_AdminHis)
- **1,901 columns (81.3%) with meaningful descriptions**
- **437 columns (18.7%) with placeholder descriptions** (generic text like "Provides information related to...")
- **42 tables** contain a `PtID` (Patient ID) field
- **18 tables** contain a `PtEncID` (Patient Encounter ID) field
- **All tables** include ZU audit fields (`ZUChkSum`, `ZUDate`, `ZULogonHisID`)

### Documentation structure

Each data dictionary page provides a 3-column HTML table:

| Column | Content |
|---|---|
| Original Column Name | Database/CSV column header |
| Expanded Column Name | Human-readable field name expansion |
| Description | Text description of field purpose |

**Not documented**: data types, nullability, max lengths, foreign key relationships, value sets/code tables, default values. No machine-readable schema.

### Placeholder description problem

437 columns (18.7%) have unhelpful placeholder descriptions following two patterns:
- "Provides information related to {field name}."
- "Contains detailed information or identifiers for the corresponding {field name}."

These placeholders are concentrated in the **most important clinical tables**:
- `HC_LabC` (lab results): 117 of 118 columns have placeholders — only 1 meaningful description
- `HC_DrugRxHis` (drug prescriptions): 84 of 88 columns have placeholders — only 4 meaningful
- `HC_DrugHisAT` (drug administration tracking): 79 of 84 columns have placeholders — only 5 meaningful
- `HC_ApptTrail` (appointment trail): 45 of 49 columns have placeholders — only 4 meaningful
- `EM_TreatAdminHis` (treatment administration): 41 of 43 columns have placeholders — only 2 meaningful

This pattern — the largest, most data-rich clinical tables having the worst documentation — strongly suggests automated description generation (likely AI) that failed to produce meaningful content for complex medical fields.

### Vendor's own content organization

The tables use naming prefixes that map to functional domains:

| Prefix | Tables | Columns | Domain |
|---|---|---|---|
| HC_ | 24 | 960 | Healthcare/Clinical (patient records, billing, labs, meds, appointments) |
| AP_ | 24 | 423 | Administrative/Patient (demographics, contacts, addresses, alerts, images) |
| AX_ | 13 | 289 | Accounting/Financial (GL, journal entries, invoices, inventory, purchase orders) |
| VE_ | 12 | 155 | EHR Exam/Template (clinical note content, template documents, EAV data storage) |
| EM_ | 7 | 258 | Encounter Management (admissions, medication administration, treatment admin) |
| FQ_ | 2 | 24 | Financial/Quality (patient earnings, patient financial info) |
| (none) | 14 | 273 | Mixed (clinical notes, encounter datasets, patient history, addresses, attachments) |

### Top 20 largest tables

| Table | Fields | Meaningful Descs | Domain |
|---|---|---|---|
| HC_LabC | 118 | 1 | Laboratory |
| EM_AdminHis | 110 | 110 | Encounter Management |
| HC_DrugRxHis | 88 | 4 | Medications/Pharmacy |
| HC_DrugHisAT | 84 | 5 | Medications/Pharmacy |
| HC_Pt | 83 | 83 | Patient Demographics/Clinical |
| HC_ApptInfoMain | 69 | 69 | Appointments |
| HC_LabSpec | 69 | 69 | Laboratory |
| HC_BlngStmtChargeForm | 60 | 60 | Billing/Financial |
| Patient_Encounter_dataset | 57 | 57 | Encounter Management |
| HC_ApptTrail | 49 | 4 | Appointments |
| EM_TreatAdminHis | 43 | 2 | Encounter Management |
| AP_Img_expanded | 42 | 42 | Administrative/Patient |
| HC_BlngStmtSummaryForm | 37 | 37 | Billing/Financial |
| HC_PHIReq | 37 | 37 | PHI Requests |
| HC_BlngStmtMainForm | 35 | 35 | Billing/Financial |
| AP_Task | 34 | 34 | Administrative/Patient |
| AX_InvtInvoiceAct | 31 | 31 | Accounting/Financial |
| AX_JEEnt | 31 | 31 | Accounting/Financial |
| AX_JE | 30 | 30 | Accounting/Financial |
| HC_Appt | 29 | 1 | Appointments |

### Key observations about the VE_Data_* tables

Nine `VE_Data_*` tables store EHR exam data in an entity-attribute-value (EAV) pattern, differentiated by data type:
- `VE_Data_DL` (date-long), `VE_Data_DT` (datetime), `VE_Data_TM` (time)
- `VE_Data_I1`, `VE_Data_I2`, `VE_Data_I4` (integers of different sizes)
- `VE_Data_T030`, `VE_Data_T100`, `VE_Data_T255` (text of different max lengths)

Each table has the same structure: primary key, `CNEntryID`, `ComEntryID`, data value, `DataFieldID`, `OldCNEntryID`, `PgEntryID`, plus `DataFieldName` and `DataFieldDesc` columns.

**Important**: The inclusion of `DataFieldName` and `DataFieldDesc` in each EAV data row means the export includes human-readable field names alongside the raw data values. This partially mitigates the opacity concern — vitals, review of systems findings, physical exam data, and other template-driven clinical data stored in these tables would include self-describing field names. However, without the template definitions themselves, understanding the hierarchical organization of the data (which template, which section, which page) still requires inference.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Richest areas** (most entities, most fields, best documentation):

1. **Billing/Financial** (8 tables, 233 columns, all with meaningful descriptions): Five `HC_BlngStmt*` tables provide detailed billing statement data (charges, charge details, date-of-service breakdowns, summaries, aging balances). `HC_PtBal` tracks patient balances. This is genuinely deep billing coverage with fields for ICD codes, CPT modifiers, insurance plan identifiers, charge amounts, payment tracking, and aging categories.

2. **Patient Demographics** (`HC_Pt` with 83 fully-described columns plus `HC_PtPrvX` with 16 columns): Comprehensive patient record including name, DOB, SSN, marital status, contact info, insurance assignment, consent dates, provider assignments, billing type, race, ethnicity, preferred language, and death information.

3. **Encounters/Admissions** (`EM_AdminHis` at 110 fully-described columns, `Patient_Encounter_dataset` at 57 columns, plus `PtHis_dataset`, `PtTransfer_dataset`, `PtTypeHis_dataset`): Very thorough coverage of admission/discharge, medication administration events, transfers, and patient history. `EM_AdminHis` includes fields for IV start/stop, medication timing, body sites, rates, volumes, response tracking, vaccine flags, and witness information.

4. **Contacts/Addresses/Communications** (multiple AP_ tables): Contact entries, phone entries, address entries with full history tracking via corresponding `*His` tables.

5. **Accounting/GL** (13 AX_ tables, 289 columns, all with meaningful descriptions): General ledger, journal entries, purchase orders, purchase requests, inventory invoices. Includes fields for debit/credit amounts, account codes, vendor information, and check numbers.

**Thinnest areas** (present but poorly documented):

1. **Laboratory**: `HC_LabC` has 118 columns but only 1 has a meaningful description. `HC_LabSpec` (specimens) has 69 well-described columns. The lab results table is essentially undocumented despite its size.

2. **Medications**: `HC_DrugRxHis` (88 columns, 4 meaningful) and `HC_DrugHisAT` (84 columns, 5 meaningful) have extensive field lists covering NDC codes, dosing, routes, frequencies, and e-prescribing — but the descriptions are almost entirely placeholders.

3. **Appointments**: `HC_ApptInfoMain` is well-documented (69 columns, all meaningful), but `HC_ApptTrail` (49 columns, only 4 meaningful) and `HC_Appt` (29 columns, only 1 meaningful) are poorly documented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `HC_Pt` (83 fields), `HC_PtPrvX` (16 fields), `PtHis_dataset` (27 fields), `Address Entry Information` (21 fields), `Patient Address Entries` (21 fields) | Thorough — name, DOB, SSN, sex, race, ethnicity, language, marital status, contacts, addresses with full history |
| Encounters / visits | ✅ Covered | `EM_AdminHis` (110 fields), `Patient_Encounter_dataset` (57 fields), `PtTransfer_dataset` (20 fields), `PtTypeHis_dataset` (14 fields) | Deep — admission/discharge, transfers, encounter types, with DRG/MDC codes |
| Problems / conditions / diagnoses | ✅ Covered | `HC_ProblemHis` (28 fields), `Patient_Encounter_dataset.DxSNOMED`, `Patient_Encounter_dataset.PrinDxSNOMED` | Adequate — problem history with SNOMED, ICD codes in billing |
| Medications / prescriptions | ⚠️ Partial | `HC_DrugRxHis` (88 fields), `HC_DrugHisAT` (84 fields), `HC_MedInfo` (8 fields), `EM_MedReviewHis` (12 fields), `EM_MedSignoffHis` (9 fields) | Extensive field coverage but 95% placeholder descriptions; includes NDC, dosing, routes, frequencies, eRx status, but meaning of many fields unknowable from documentation |
| Allergies | ✅ Covered | `AP_AllergyHis` (23 fields), `Healthcare Allergy Reconciliation History` (15 fields) | Good — allergy history plus reconciliation tracking |
| Immunizations | ⚠️ Partial | `EM_AdminHis.IsVaccine` (single flag field) | Product is certified for immunization registry reporting (f)(1) but no dedicated immunization table; vaccine data likely stored within medication administration tables |
| Vitals | ⚠️ Partial | No dedicated vitals table; likely stored in `VE_Data_*` EAV tables with `DataFieldName` self-describing the vital type | Product clearly captures vitals; data present but only accessible through generic EAV structure |
| Lab results | ✅ Covered | `HC_LabC` (118 fields), `HC_LabSpec` (69 fields) | Structurally comprehensive with HL7 fields, filler/placer order numbers, specimen details; but `HC_LabC` has only 1 meaningful description out of 118 |
| Imaging / diagnostic reports | ❌ Not covered | No radiology-specific table; `AP_Img_expanded` (42 fields) covers image/document metadata but not radiology results/reports | Product has RIS/PACS module; this is a significant gap |
| Procedures | ⚠️ Partial | `EM_TreatAdminHis.CPTCodeID`, `EM_TreatAdminHis.ProcedureIDs`; billing tables have CPT-related fields | No dedicated procedures table despite product serving surgical hospitals and ASCs |
| Clinical notes / documents | ✅ Covered | `Clinical_Notes_dataset` (20 fields), `VE_CN` (20 fields), `VE_CNEntry` (11 fields), `VE_TmplDocHis` (16 fields), 9 `VE_Data_*` tables | Good structure — notes linked to templates with EAV data storage; `DataFieldName`/`DataFieldDesc` provide self-describing clinical data |
| Care plans / goals | ⚠️ Partial | `Healthcare Behavioral Health Care Plan (HC_BHCP)` (19 fields) | Only behavioral health care plans; no general care plan table |
| Orders / referrals | ⚠️ Partial | `HC_OSInst` (15 fields, only 1 meaningful desc), `HC_Pt.NoReferal` | Order set instructions table exists but almost undocumented; no dedicated referral table |
| Insurance / coverage | ⚠️ Partial | `HC_Pt.BillingTypeID`, `HC_Pt.CLIsAssignBenefits`, `HC_Pt.PayPlanID`, `HC_ApptInfoMain.PtPriPolicy`, `HC_ApptInfoMain.PtPolicyID` | Insurance-related fields scattered across patient and appointment tables; no dedicated insurance/enrollment/coverage table |
| Claims / billing | ✅ Covered | 5 `HC_BlngStmt*` tables (total 181 fields), `HC_PtBal` (21 fields), `Patient Earnings Entry Log` (14 fields), `FQ_PtEarning` (12 fields), `FQ_PtInfo` (12 fields) | Deep — charge forms, charge details, date-of-service breakdowns, summaries, aging balances, ICD codes, CPT modifiers |
| Payments | ✅ Covered | `HC_PtBal` (21 fields with insurance/patient balance breakdowns, aging categories), billing statement tables with payment tracking | Present within billing tables |
| Consents / directives | ⚠️ Partial | `HC_Pt.DateConsent`, `HC_Pt.DateConsentExpire`, `EM_TreatAdminHis.ConsentGiven/ConsentNeeded` | Basic consent tracking but no dedicated advance directives table |
| Patient communications / portal messages | ❌ Not covered | `HC_Pt.PortalID` references portal; no table for portal messages or patient-generated content | Product has patient portal; gap in export |
| Continuity of care | ✅ Covered | `HC_ContOfCare` (17 fields) | Present with document content, creation dates, and linking |
| Specialty-specific (Behavioral Health) | ✅ Covered | `HC_BHCP` (19 fields) | Behavioral health care plan with structured fields |
| Specialty-specific (Blood Bank) | ✅ Covered | `HC_BBDonor` (10 fields), `HC_BTEvent` (9 fields), `HC_BTRuleEnt` (7 fields), `Healthcare - Blood Test Encounter Status` (7 fields) | Blood bank donor records, transfusion events, rules |
| Specialty-specific (Nutrition) | ❌ Not covered | No dietary/nutrition data table | Product has Clinical Nutrition & Food module; gap in export |

## 6. Documentation Quality

### Strengths

- **Publicly accessible** at a stable URL (https://docs.versasuite.com) with no authentication, no JavaScript rendering, and no anti-bot measures
- **Simple, machine-readable format**: Static HTML pages parseable with basic HTML parsers
- **Broad coverage**: 95 unique tables across clinical, billing, administrative, and financial domains
- **Clear export mechanism description**: The index page explains CSV format, patient-specific folders, selective export, and single/population modes
- **Good descriptions where present**: 81.3% of columns have meaningful, specific descriptions
- **Native data model export**: CSV is the actual database structure, not a standard-based projection

### Weaknesses

1. **No data types**: There is zero documentation of whether fields are integers, strings, dates, booleans, or decimals. This is a fundamental omission for a data dictionary.

2. **No value sets or code tables**: Hundreds of fields end in `ID` (e.g., `DrugRouteID`, `MedStatusID`, `BillingTypeID`, `MaritalStatus`, `BarrierID`). The lookup tables that decode these IDs are not included in the export documentation and apparently not in the export itself. Without knowing what `DrugRouteID = 5` means, the data is incomplete.

3. **No relationship documentation**: Foreign keys between tables (e.g., `PtID`, `PtEncID`, `CNEntryID`, `LabCID`) are implicit through shared column names but not formally specified. No ER diagram.

4. **No sample data**: No example CSV files or sample export archives are provided.

5. **Placeholder descriptions concentrated in the most critical clinical tables**: The lab results table (`HC_LabC`, 118 columns) has only 1 meaningful description. The drug prescription table (`HC_DrugRxHis`, 88 columns) has only 4. These are arguably the most important tables for clinical decision-making, yet they are the worst documented.

6. **Missing EAV template definitions**: While the `VE_Data_*` tables include `DataFieldName`/`DataFieldDesc` (partially self-describing), the template structure that organizes these fields into clinical forms is not documented.

### Usability assessment

A developer receiving this export documentation could:
- ✅ Understand the CSV file structure and naming
- ✅ Identify which tables contain patient data (via PtID)
- ✅ Understand the purpose of well-documented tables (billing, demographics, encounters)
- ❌ Interpret coded ID values without the reference/lookup tables
- ❌ Know the data types of any field
- ❌ Build a reliable import without significant reverse-engineering
- ❌ Understand the relationships between tables without inference

## 7. Overall Assessment

### Classification

**Partial native export**

VersaSuite exports its native database model as CSV files — this is the right approach for (b)(10) and avoids the common trap of repackaging FHIR or C-CDA as an "all EHI" export. The 95-table, 2,338-column export is genuinely broad, spanning clinical, billing, financial, and administrative domains. However, significant documentation gaps (especially the nearly-undocumented lab and medication tables), missing lookup/reference tables, absent data types, and several missing product modules (radiology results, nutrition, patient portal messages) prevent classification as "comprehensive."

### Key Findings

1. **Native CSV export with broad domain coverage is the right structural approach.** 95 tables across 6+ domains, exported directly from the database, with both single-patient and population modes. This is materially better than vendors who repackage FHIR or C-CDA.

2. **The worst documentation is on the most important clinical tables.** `HC_LabC` (118 columns, 1 meaningful description), `HC_DrugRxHis` (88 columns, 4 meaningful), and `HC_DrugHisAT` (84 columns, 5 meaningful) are the core clinical tables, yet have 95%+ placeholder descriptions. This pattern strongly suggests automated (likely AI-generated) descriptions that failed on the most complex medical content.

3. **Missing lookup/reference tables is the single largest gap.** The export includes transactional tables with hundreds of coded `*ID` fields but does not include or document the reference tables that decode those IDs. A recipient cannot interpret `DrugRouteID = 3` or `MaritalStatus = 5` without the code tables.

4. **The EAV-structured exam data includes self-describing field names** (`DataFieldName`, `DataFieldDesc`), which partially mitigates concerns about opaque template data. This is better than the prior report suggested.

5. **Several product modules have no representation in the export**: radiology/imaging results (despite RIS/PACS module), clinical nutrition (despite a dedicated module), patient portal communications, and dedicated immunization records.

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV (one file per table) + associated images/documents
Model type:      Native database tables
Entities:        95 unique tables (96 data dictionary pages)
Fields:          2,338
Descriptions:    81.3% meaningful (18.7% placeholder)
Sample data:     No
Bulk export:     Yes (single-patient and patient-population)
Domains covered: 11 of 17 applicable domains (✅ or ⚠️)
```

### Bottom Line

VersaSuite's EHI export is a genuine native-model CSV export covering clinical, billing, and financial data — structurally the right approach for (b)(10). However, a patient or provider receiving this export would struggle to interpret much of the clinical data due to nearly-undocumented lab and medication tables, missing lookup/reference tables that decode hundreds of coded ID fields, and the absence of data type information. The export covers breadth but sacrifices interpretability, making it a compliance artifact that falls short of practical data portability.
