# EHI Export Analysis: VersaSuite

**Product**: VersaSuite 9.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.99.04.2503.Vers.09.01.1.200210 (CHPL #10299)

## 1. Product Context

VersaSuite is a monolithic, all-in-one healthcare IT platform developed by Universal Software Solutions Inc. (USSI), headquartered in Austin, TX. It positions itself as a combined HIS/EHR/EPM/ERP solution running on a single database, with 36 claimed integrated modules. It primarily targets small to mid-size hospitals, critical access hospitals, specialty hospitals, and ambulatory clinics.

**Relevant capabilities for export assessment:**
- **Clinical/EHR**: EHR documentation, CPOE, EMAR, ETAR, clinical decision support, ED information system
- **Lab & Imaging**: LIMS, RIS/PACS
- **Pharmacy**: Pharmacy information management, e-prescribing
- **Practice Management & Billing**: Enterprise practice management (scheduling, registration, billing, A/R, collections), point of sale, automatic billing code transmission
- **HIM**: Health information management, document management
- **Patient Portal**: Patient access, FHIR API
- **Nutrition**: Clinical nutrition & food services
- **Administrative/ERP**: Accounting/GL, payroll, HR, time & attendance, employee scheduling, budgeting, facility management, procurement, inventory/materials management
- **Reporting**: Custom reporting, quality reporting

The single-database architecture means a comprehensive (b)(10) export should be able to access clinical, billing, administrative, and specialty data without crossing system boundaries. The product stores patient demographics, encounters, problems, medications (including MAR), labs, imaging, vitals, allergies, billing/claims, insurance, appointments, notes, care plans, behavioral health data, and more.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/data-dictionary/index.html` | Main EHI export documentation page — describes export mechanics, links to 96 data dictionary pages | **High** — primary orientation document |
| `downloads/data-dictionary/*.html` (96 files) | Individual HTML data dictionary pages, one per exported CSV table | **High** — core of the documentation |
| `downloads/screenshot-main-page.png` | Screenshot of the docs.versasuite.com landing page | **Medium** — confirms the index.html content visually |
| `files.json` | Manifest of 102 downloaded files | **Medium** — orientation |
| `product-research.md` | Prior research on VersaSuite product capabilities | **High** — establishes baseline for coverage assessment |
| `ehi-export-report.md` | Prior agent narrative | **Low** — used for orientation only; verified independently |

All 96 data dictionary HTML files were successfully parsed with zero parse errors. No PDFs, sample data files, or machine-readable schemas were provided.

## 3. Export Mechanics

- **Format**: CSV files (primary data) plus original-format images and documents
- **Mechanism**: Purpose-built "ehi export tool" within VersaSuite — described as a UI-driven tool that does not require developer assistance
- **Single-patient**: Yes — exports organized into patient-specific folders
- **Bulk/population**: Yes — the documentation explicitly describes "Patient Population EHI Export" for entire patient populations
- **Access control**: Limited to specific users or system administrators
- **Output location**: Patient-specific folders within VersaSuite's default export folder
- **Selective export**: Tables with no patient data are automatically excluded
- **Documentation link**: Each export file includes a publicly accessible hyperlink to the data dictionary (docs.versasuite.com)

## 4. Export Content: What's In It

### Overview

The export consists of **96 documented CSV tables** containing a total of **2,334 fields**. Every field (100%) has a text description. Of those, **1,876 (80%)** have meaningful, context-specific descriptions, while **458 (20%)** use generic templated patterns (e.g., "Provides information related to [field name]"). No data types, nullability constraints, value sets, foreign key relationships, or sample data are documented — only column name, expanded name, and description.

### Vendor's own content organization

The data dictionary entries are organized by internal table name prefixes that map to VersaSuite's module structure:

| Category | Entities | Fields | Notes |
|---|---|---|---|
| Encounters / Administration | 7 | 276 | Includes EM_AdminHis (110 fields), patient encounters, transfers, type history |
| Accounting / Financial (AX) | 13 | 272 | General ledger, journal entries, invoices, POs, purchase requisitions, receipts |
| Billing / Financial | 8 | 224 | Billing statements (main, charge, charge detail, DOS, summary, aging), patient balance |
| Medications | 5 | 201 | Drug Rx history (88 fields), drug admin history (84 fields), med review, med signoff, med info |
| Laboratory | 2 | 185 | Lab results (HC_LabC, 118 fields), lab specimens (HC_LabSpec, 67 fields) |
| Demographics / Contact | 9 | 169 | Address, contact, phone entries and histories, contact methods, language |
| Patient Core | 5 | 160 | HC_Pt (83 fields), patient history, patient type history, patient-provider crosswalk |
| Appointments / Scheduling | 3 | 146 | Appointment info (68 fields), appointment trail (49 fields), appointment documentation |
| EHR Exam / Clinical Notes (VE) | 12 | 145 | Clinical note structure, template doc history, data fields (text, integer, date/time, decimal) |
| Administrative / Patient | 6 | 81 | External numbers, recurring charges, report history, security profile, worklist users, concepts |
| Images / Documents | 2 | 52 | Attachments (AP_Img, 42 fields), attachment info |
| Audit | 3 | 42 | Audit log, audit trail entries, ATNA records |
| Treatment Administration | 1 | 43 | ETAR history (EM_TreatAdminHis, 43 fields) |
| Allergies | 2 | 38 | Allergy history, allergy reconciliation history |
| Clinical Notes | 2 | 37 | Clinical notes dataset, VE_CN/VE_CNEntry |
| Financial / Patient Earnings | 3 | 37 | FQHC patient earnings and patient info |
| PHI Requests | 1 | 37 | HC_PHIReq — PHI disclosure tracking |
| Tasks / Workflow | 1 | 33 | AP_Task (33 fields) |
| Problems / Conditions | 1 | 28 | HC_ProblemHis (28 fields) |
| Blood Bank / Transfusion | 3 | 26 | Blood bank donor, blood test events, blood test rules |
| Overrides | 1 | 22 | HC_OverrideHis (22 fields) |
| Behavioral Health | 1 | 19 | HC_BHCP behavioral health care plan |
| Continuity of Care | 1 | 17 | HC_ContOfCare (17 fields) |
| Orders / Instructions | 1 | 15 | HC_OSInst (15 fields) |
| Financial / Direct Deposit | 1 | 10 | Direct deposit transactions |
| Acknowledgments | 1 | 10 | AP_Ack acknowledgment records |
| Alerts | 1 | 9 | AP_AlertEntry (9 fields) |

### Representative entities (top 10 by field count)

| Entity | Fields | Described | Category |
|---|---|---|---|
| HC_LabC (Lab Results) | 118 | 118 | Laboratory |
| EM_AdminHis (Encounter Admin History) | 110 | 110 | Encounters / Administration |
| HC_DrugRxHis (Drug Rx History) | 88 | 88 | Medications |
| HC_DrugHisAT (Drug Admin History) | 84 | 84 | Medications |
| HC_Pt (Patient) | 83 | 83 | Patient Core |
| HC_ApptInfoMain (Appointment Info) | 68 | 68 | Appointments / Scheduling |
| HC_LabSpec (Lab Specimens) | 67 | 67 | Laboratory |
| HC_BlngStmtChargeForm (Billing Charges) | 57 | 57 | Billing / Financial |
| Patient_Encounter (Encounters) | 56 | 56 | Encounters / Administration |
| HC_ApptTrail (Appointment Trail) | 49 | 49 | Appointments / Scheduling |

Full inventory: see `analysis/entity-inventory-full.json` (2,334 field objects) and `analysis/entity-inventory-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

VersaSuite's export reflects its native database schema — the table names (HC_Pt, EM_AdminHis, HC_LabC, etc.) are clearly internal database table names, not FHIR resources or C-CDA sections. The export spans multiple product modules:

**Strongest coverage:**
- **Encounters/Administration** (7 entities, 276 fields): Deep encounter documentation with admin history (110 fields), patient encounters (56 fields), transfers, and type changes
- **Accounting/Financial** (13 entities, 272 fields): Comprehensive GL, journal entries, invoicing, purchase orders, purchasing requisitions — goes well beyond patient billing
- **Billing** (8 entities, 224 fields): Billing statements with 5 distinct sub-tables (main, charge, charge detail, DOS, summary), aging balances, patient balances
- **Medications** (5 entities, 201 fields): Drug prescription history (88 fields), drug administration tracking (84 fields), med review, med signoff — very deep
- **Laboratory** (2 entities, 185 fields): Lab results (118 fields) and specimens (67 fields) — exceptionally detailed

**Moderate coverage:**
- **Demographics** (9 entities, 169 fields): Addresses, contacts, phones with full history tracking
- **Patient Core** (5 entities, 160 fields): HC_Pt (83 fields) includes billing-related fields (BalanceIns, BalancePt, BillingTypeID) alongside clinical
- **EHR Exam/Clinical Notes** (12 entities, 145 fields): Structured exam data stored by data type (text, integers, dates, decimals)

**Thinner coverage:**
- **Problems/Conditions** (1 entity, 28 fields)
- **Allergies** (2 entities, 38 fields)
- **Behavioral Health** (1 entity, 19 fields): Only the care plan entity
- **Orders** (1 entity, 15 fields): HC_OSInst only

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | HC_Pt (83 fields), AP_AddrEntryHis, AP_ContactEntry/His, AP_PhoneEntry/His, AP_LangEnt, AP_ExtNo — 9 entities, 169 fields | Thorough; includes history tracking |
| Encounters / visits | ✅ Covered | EM_AdminHis (110 fields), Patient_Encounter (56 fields), PtTransfer, PtTypeHis, EM_AdminHisChg — 7 entities, 276 fields | Very deep with full administrative history |
| Problems / conditions | ✅ Covered | HC_ProblemHis (28 fields) | Adequate single table |
| Medications / prescriptions | ✅ Covered | HC_DrugRxHis (88 fields), HC_DrugHisAT (84 fields), HC_MedInfo, EM_MedReviewHis, EM_MedSignoffHis — 5 entities, 201 fields | Very thorough; covers Rx, admin, review, signoff |
| Allergies | ✅ Covered | AP_AllergyHis (20 fields), HC Allergy Reconciliation History (18 fields) | Adequate; includes reconciliation |
| Immunizations | ❌ Not covered | No immunization-specific tables in export | Product likely stores immunizations (certified for (f)(1) immunization registry reporting); **significant gap** |
| Vitals | ⚠️ Partial | VE_Data_* tables store structured exam data generically by type (integers, text, dates) — vitals likely stored here but not in a dedicated table | Vitals may be embedded in generic VE_Data tables but no dedicated vitals entity |
| Lab results | ✅ Covered | HC_LabC (118 fields), HC_LabSpec (67 fields) — 185 total fields | Exceptionally detailed |
| Imaging / diagnostic reports | ⚠️ Partial | AP_Img_expanded (42 fields) covers images/attachments, but no radiology-specific reporting table | Product has RIS/PACS; imaging results likely in generic note/doc structure |
| Procedures | ⚠️ Partial | Treatment fields (BlngStmtChargeForm has TreatProcID), but no dedicated procedures table | Procedures likely captured via billing charge codes rather than a clinical procedures entity |
| Clinical notes / documents | ✅ Covered | VE_CN, VE_CNEntry, VE_Data_* (12 entities, 145 fields), Clinical_Notes documentation, VE_TmplDocHis, AP_NoteGenEntry | Deep; structured by data type with template tracking |
| Care plans / goals | ✅ Covered | HC_BHCP (19 fields), HC_ContOfCare (17 fields) | Behavioral health care plans and continuity of care |
| Orders / referrals | ⚠️ Partial | HC_OSInst (15 fields) — order/instruction set only | Thin; product has CPOE but limited order export detail |
| Insurance / coverage | ⚠️ Partial | HC_Pt fields (BalanceIns, CLIsAssignBenefits, CLProvAssignID), billing charge InsCo/InsPlan fields | Insurance referenced across entities but no dedicated insurance/coverage table |
| Claims / billing | ✅ Covered | 8 billing entities (224 fields): HC_BlngStmt* (main, charge, charge detail, DOS, summary), HC_PtBal, HC_BlngStmtAgingBalance | Very thorough; 5-table billing statement hierarchy |
| Payments | ✅ Covered | Payment fields within billing tables (IsPayment, AmtPt, AmtIns), FQ_PtEarning, Direct Deposit | Covered across billing and earnings tables |
| Accounting / GL | ✅ Covered | 13 AX_ entities (272 fields): GL, GLSBAT, GLSHC, journal entries, invoices, POs, PRs, receipts | Goes beyond patient billing to institutional accounting — unusual depth |
| Consents / directives | ⚠️ Partial | HC_Pt has CLIsAssignBenefits, CLIsProvSignOnFile; AP_Ack tracks acknowledgments | Consent indicators exist but no dedicated advance directive/consent form entity |
| Patient communications | ❌ Not covered | No portal messaging, secure messaging, or communication log entities | If product has patient portal messaging, this is a gap |
| Behavioral health | ✅ Covered | HC_BHCP (19 fields) behavioral health care plan | Present but thin (single entity) for a product that explicitly targets behavioral health hospitals |
| Blood bank / transfusion | ✅ Covered | HC_BBDonor, HC_BTEvent, HC_BTRuleEnt (26 fields) | Niche specialty coverage |
| Nutrition | ❌ Not covered | No nutrition/dietary entities | Product has Clinical Nutrition & Food module; **gap** |
| Pharmacy | ⚠️ Partial | Drug Rx data exported but no pharmacy inventory/formulary management tables | Pharmacy operational data not exported |

## 6. Documentation Quality

**Strengths:**
- Every exported table has a dedicated HTML documentation page with field-level descriptions
- 100% of fields (2,334/2,334) have a text description
- 80% of descriptions (1,876/2,334) provide meaningful context beyond just restating the field name
- Clear export mechanics documentation on the index page
- Documentation explicitly addresses (b)(10) requirements and describes both single-patient and population export

**Weaknesses:**
- **No data types documented**: The HTML tables only have column name, expanded name, and description — no indication of whether fields are integers, strings, dates, booleans, etc.
- **No value sets or coded values**: Fields like BillingTypeID, MedStatusID, DrugRouteID reference lookup tables but no valid values are documented
- **No relationships/foreign keys**: The ~939 fields ending in "ID" clearly reference other tables, but no relationship documentation exists
- **No sample data provided**: No example CSV files or sample records
- **No machine-readable schema**: No JSON schema, XSD, or equivalent — only HTML prose
- **20% generic descriptions**: 458 fields have templated descriptions like "Provides information related to [field name]" that add no value
- **No entity-relationship documentation**: With 96 tables and hundreds of foreign keys, the lack of any ERD or relationship diagram is a significant gap

**Developer usability**: A developer could understand the general structure and identify the right tables for their use case, but building a reliable import would require significant guesswork on data types, allowable values, and table relationships. The documentation is usable but not self-sufficient.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

VersaSuite's export covers a genuinely broad range of data domains from its native database. With 96 tables and 2,334 fields spanning clinical (encounters, medications, labs, notes, problems, allergies), billing (8 entities with 224 fields), accounting (13 entities with 272 fields), behavioral health, blood bank, and patient demographics, this is clearly not a repackaged USCDI/C-CDA export. The inclusion of institutional accounting tables (general ledger, journal entries, purchase orders) goes well beyond what most vendors export and is unusual depth. However, there are some gaps: no immunization table, no dedicated vitals table, no nutrition data (despite having that module), and thin coverage of orders/CPOE data relative to the product's capabilities.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. The table names (HC_Pt, EM_AdminHis, AX_GL, HC_BlngStmtChargeForm) are native database tables, not FHIR resources or C-CDA sections. VersaSuite built a dedicated "ehi export tool" that dumps these internal tables to CSV files organized in patient-specific folders. The 96-table data dictionary at docs.versasuite.com is specific to this export. This is a native database extraction approach, similar in philosophy to Epic's TSV export or Oracle's SQL model, not a repackaged clinical exchange.

### Key Findings

1. **Genuinely purpose-built native export**: 96 CSV tables from the native database schema with 2,334 documented fields — this is a real (b)(10) effort, not a repackaged C-CDA or FHIR export.

2. **Strong billing/financial coverage**: 8 billing entities (224 fields) plus 13 accounting entities (272 fields) — the accounting depth (GL, journal entries, POs, invoices) is unusual and goes well beyond USCDI. This is a strong signal of genuine engagement with (b)(10).

3. **Lab and medication depth is exceptional**: HC_LabC has 118 fields; medication coverage spans 5 entities with 201 fields including administration tracking (EMAR/ETAR) — far exceeding what USCDI/US Core would require.

4. **Notable gaps in immunizations and vitals**: No dedicated immunization table despite the product being certified for immunization registry reporting (f)(1). Vitals appear to be stored generically in VE_Data tables rather than a dedicated vitals entity. Nutrition module data is also absent.

5. **Documentation lacks data types and relationships**: While field descriptions are comprehensive (100% coverage, 80% meaningful), the absence of data types, foreign key documentation, value sets, and sample data makes it significantly harder for a developer to actually use the exported data.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (plus original-format images/documents)
Entities:        96
Fields:          2,334
Descriptions:    100% have descriptions; 80% meaningful
Sample data:     No
Bulk export:     Yes (single patient and population)
Domains covered: 14 of 19 applicable domains (✅ or ⚠️)
```

### Bottom Line

VersaSuite has built a genuine, purpose-built EHI export that dumps 96 native database tables to CSV, covering clinical, billing, accounting, and specialty data far beyond USCDI scope. A patient or provider would receive a substantially complete copy of their data, though immunizations, vitals (as a dedicated table), and nutrition module data appear to be missing. The biggest weakness is documentation quality — the absence of data types, relationships, and value sets means the exported CSV files would be difficult to interpret without VersaSuite-specific domain expertise.
