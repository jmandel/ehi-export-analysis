# VersaSuite — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://docs.versasuite.com
- CHPL ID: 10299 (VersaSuite 9.0, certified 2020-02-10)
- Developer: VersaSuite (Universal Software Solutions Inc.)

## Navigation Journal

**Step 1: Initial probe**

```bash
curl -sI -L "https://docs.versasuite.com" -H 'User-Agent: Mozilla/5.0'
```

Result: HTTP/2 200, Content-Type: text/html, 14,838 bytes. Served by Microsoft-IIS/10.0 with ASP.NET. Last modified 2025-10-10. No redirects.

**Step 2: Fetch and examine the page**

```bash
curl -sL "https://docs.versasuite.com" -H 'User-Agent: Mozilla/5.0' -o page.html
```

The page is a single static HTML document titled "VersaSuite - Electronic Health Information Export Documentation." It contains:
1. An introductory section explaining the EHI export in the context of §170.315(b)(10)
2. A description of the export tool and its CSV-based output format
3. A data dictionary index listing 96 individual HTML pages, each documenting one exported CSV table

**Step 3: Download all linked data dictionary pages**

Each link is a relative URL to an HTML file on the same domain (e.g., `HC_Pt.html`, `AP_ContactEntry.html`). Downloaded all 96 linked pages:

```bash
# For each file linked from the index:
curl -sL "https://docs.versasuite.com/{filename}" -H 'User-Agent: Mozilla/5.0' -o "{filename}"
```

All 96 pages downloaded successfully (97 total including index). No anti-bot measures, no JavaScript required, no authentication. Total download size: ~660 KB.

**Step 4: No additional documentation found**

The site is purely the index page with data dictionary links. There are no:
- Downloadable PDFs, ZIPs, or other file formats
- Subpages or navigation beyond the data dictionary
- API documentation endpoints
- User guides or instructional materials beyond the brief overview on the index page
- Schema files (XSD, JSON Schema, DDL)
- Sample export files

## What Was Found

### Export Mechanism

VersaSuite's EHI export tool produces a **CSV-based export** organized into patient-specific folders within a default export directory. The export includes:

1. **CSV files** — one per database table, containing structured tabular data
2. **Images and documents** — associated patient files exported in their original format (images, scanned documents, etc.)
3. **Selective export** — tables without patient data for a given patient are omitted

The export supports both single-patient and patient-population modes, as described on the main page.

### Data Dictionary

The documentation consists of 96 HTML pages, each documenting one CSV table that may appear in an export. Each page provides a three-column table:

| Column | Content |
|--------|---------|
| Original Column Name | The CSV column header (database field name) |
| Expanded Column Name | A human-readable expansion of the abbreviation |
| Description | A text description of the field's purpose |

**No data types are documented** — there is no indication of whether fields are integers, strings, dates, booleans, or coded values. **No value sets are documented** — for fields that reference coded values (e.g., `BillingTypeID`, `MaritalStatus`, `MedStatusID`), the valid values are not listed. **No foreign key relationships are formally documented** — while many tables share `PtID` and `PtEncID` columns, the cross-table relationships are not explicitly stated.

### Table Prefixes and Domains

The 96 tables span six naming prefixes that map to functional domains:

| Prefix | Count | Domain |
|--------|-------|--------|
| HC_ | 25 | Healthcare/Clinical — patient records, billing, labs, medications, problems, appointments |
| AP_ | 24 | Administrative/Patient — demographics, contacts, addresses, alerts, images, tasks |
| AX_ | 13 | Accounting/Financial — general ledger, journal entries, invoices, purchase orders, inventory |
| VE_ | 12 | EHR Exam/Template — clinical note entries, template documents, data storage tables |
| EM_ | 7 | Encounter Management — admissions, treatment administration, medication review |
| FQ_ | 2 | Financial/Quality — patient earnings, patient financial info |
| (none) | 13 | Mixed — clinical notes, encounter docs, patient history, billing statements, attachments |

### Key Statistics

- **96 tables** documented across all domains
- **2,381 total columns** across all tables
- **42 tables** (44%) contain a `PtID` (Patient ID) field
- **18 tables** (19%) contain a `PtEncID` (Patient Encounter ID) field
- **All tables** include ZU audit fields (`ZUChkSum`, `ZUDate`, `ZULogonHisID`)

### Description Quality

- **86 tables** (90%) have "good" quality descriptions — meaningful, specific text
- **10 tables** (10%) have "poor" quality descriptions — dominated by placeholder text
- **458 of 2,381 columns** (19.2%) use placeholder descriptions like "Provides information related to..." or "Contains detailed information or identifiers for the corresponding..."

The placeholder descriptions are concentrated in the larger clinical tables (HC_DrugRxHis at 88 columns, HC_LabC at 118 columns, HC_DrugHisAT at 84 columns) — ironically the most data-rich tables have the worst documentation.

## Export Coverage Assessment

### Data Domain Coverage

VersaSuite is documented as a comprehensive HIS/EHR/EPM/ERP platform with 36 integrated modules running on a single database. Comparing the product research against the 96 exported tables:

**Clearly covered domains:**
- **Patient demographics** — `HC_Pt` (83 columns) is comprehensive: name, DOB, SSN, sex, marital status, contact info, insurance assignment, consent dates, provider assignments
- **Patient encounters/admissions** — `EM_AdminHis` (110 columns, the largest table) covers admission/encounter details; `Patient_Encounter_dataset_documentation` (56 columns) provides encounter-level data; `PtTransfer_dataset_documentation` covers transfers
- **Medications/prescriptions** — `HC_DrugRxHis` (88 columns) covers drug prescription history including NDC codes, dosing, routes, frequencies, e-prescribing status; `EM_TreatAdminHis` (43 columns) covers treatment administration
- **Laboratory** — `HC_LabC` (118 columns, second largest) covers lab results in detail; `HC_LabSpec` (69 columns) covers lab specimens
- **Clinical notes** — `Clinical_Notes_dataset_documentation` (20 columns) covers note metadata; `VE_CN` and `VE_CNEntry` cover clinical note content; `VE_TmplDocHis` covers template documents
- **Problems/diagnoses** — `HC_ProblemHis_documentation` (28 columns) covers problem history
- **Allergies** — `AP_AllergyHis_Documentation` (23 columns) and `Healthcare Allergy Reconciliation History` (15 columns)
- **Patient billing/balances** — `HC_PtBal_documentation` (21 columns) with aging balances; 5 `HC_BlngStmt*` tables covering billing statements in detail (charge forms, DOS, summaries, aging balances)
- **Appointments** — `HC_ApptInfoMain` (69 columns), `HC_Appt_Documentation` (29 columns), `HC_ApptTrail_Documentation` (49 columns)
- **Contacts/addresses** — `AP_ContactEntry`, `AP_PhoneEntry`, `Address Entry Information`, plus history tables for each
- **Images/documents** — `AP_Img_expanded` (42 columns) covers image/document metadata; `Attachment Information` (11 columns)
- **Behavioral health** — `HC_BHCP` (19 columns) covers behavioral health care plans
- **Blood bank** — `HC_BBDonor` (10 columns), `Healthcare - Blood Test Encounter Status` (7 columns)
- **Continuity of care** — `HC_ContOfCare` (17 columns)
- **Accounting/GL** — `AX_GL` (27 columns), `AX_JE` (30 columns), `AX_JEEnt` (31 columns) and related financial tables
- **Inventory/procurement** — `AX_InvtInvoice`, `AX_InvtInvoiceAct`, `AX_ItemPO`, `AX_ItemPR`
- **PHI requests** — `HC_PHIReq` (37 columns) covers patient health information disclosure requests
- **Medication administration** — `EM_MedReviewHis`, `EM_MedSignoffHis`, `HC_DrugHisAT` (84 columns for medication administration tracking)
- **Payroll/direct deposit** — `Direct Deposit Transactions Data Dictionary` (10 columns)
- **EHR exam data** — 9 `VE_Data_*` tables storing different data types (dates, integers, text of various lengths, timestamps)

**Notable gaps or unclear coverage:**
- **Vital signs** — No dedicated vitals table is documented. Vital signs may be stored in the generic `VE_Data_*` tables (which store EHR exam template data by data type), but this is not explicitly documented.
- **Immunizations** — No immunization-specific table despite the product being certified for (f)(1) immunization registry reporting. Immunization data may be within the medication or encounter tables, but is not separately identified.
- **Procedures/surgical records** — No dedicated procedures table. The product is used by surgical hospitals and ambulatory surgical centers, yet there is no explicit surgical/procedure documentation.
- **Radiology/imaging results** — Despite having a RIS/PACS module, there is no radiology-specific table in the data dictionary. Imaging results may be in the generic encounter or template data tables.
- **Care plans** — Only behavioral health care plans (`HC_BHCP`) are documented. No general care plan table exists.
- **Referrals** — No referral-specific table, though `HC_Pt.NoReferal` tracks referral counts.
- **Insurance/enrollment** — While billing balances and claim-related fields exist in `HC_Pt`, there is no dedicated insurance coverage or enrollment table.
- **Patient portal data** — `HC_Pt.PortalID` references the portal, but there is no table for portal communications or patient-generated data.
- **Nutrition/dietary** — Despite a Clinical Nutrition & Food module, no dietary data table appears.
- **E-prescribing details** — The drug prescription table has eRx flags, but no separate e-prescribing transaction table.

**Important note on the VE_Data_* tables:** The EHR exam data is stored in a generic entity-attribute-value (EAV) pattern across 9 tables differentiated by data type (`VE_Data_DL` for date-long, `VE_Data_DT` for date-time, `VE_Data_I1`/`I2`/`I4` for integers of different sizes, `VE_Data_T030`/`T100`/`T255` for text of different lengths, `VE_Data_TM` for time). These tables each have the same structure: `DataID`, `TmplDocHisID`, `ObjectID`, `Value`, plus audit fields. This EAV structure means that much of the clinical examination data (likely including vitals, review of systems, physical exam findings, assessment/plan) is stored in these generic tables — but without the template definitions that map `ObjectID` to specific clinical concepts, the data is essentially opaque. The template definitions themselves are NOT included in the export documentation.

### Export Format & Standards

The export is a **proprietary CSV format** — not FHIR, not C-CDA, not any recognized healthcare data standard. This is appropriate and actually better-suited for a (b)(10) export than a FHIR-only approach would be, because:

1. CSV can represent any tabular data, not just data that maps to FHIR resources
2. The export appears to be a near-direct dump of database tables, which preserves the full data model
3. It includes financial/accounting data (AX_ tables) that would not fit FHIR

However, the CSV export has significant limitations for data portability:
- **No formal schema** — no DDL, XSD, or JSON Schema. The data dictionary HTML pages are the only structural documentation.
- **No data types** — column types (string, integer, date, boolean, decimal) are not documented
- **No value sets** — coded values (IDs referencing lookup tables) are unexplained. Many fields end in `ID` (e.g., `DrugRouteID`, `MedStatusID`, `BillingTypeID`) but the valid values and their meanings are not documented.
- **No relationship documentation** — foreign keys between tables are implicit (shared column names like `PtID`, `PtEncID`) but not formally specified
- **No lookup/reference tables** — the export includes transactional tables but appears to omit the reference/lookup tables that decode ID values. Without knowing what `DrugRouteID = 3` means, the data is incomplete.

This is a **critical gap**: the export gives you data with hundreds of coded ID fields, but doesn't export the code tables that give those IDs meaning. A third party receiving this export could see that a patient has `DrugRouteID = 5` but would have no way to know if that means oral, intravenous, subcutaneous, etc.

### Documentation Quality

**Strengths:**
- The documentation is publicly accessible at a stable URL with no authentication
- The static HTML format is simple and machine-readable
- 90% of tables have good-quality descriptions
- The index page clearly explains the export mechanism (CSV + images/documents, patient-specific folders)
- Coverage of 96 tables is relatively broad

**Weaknesses:**
- **No data types documented** — this is a fundamental omission for a data dictionary
- **No value sets or code tables** — makes the export data incomplete without the source system
- **No relationship documentation** — table joins must be inferred from column naming conventions
- **No sample data** — no example export files are provided
- **No export procedure documentation** — the index page mentions the "ehi export tool" but provides no instructions, screenshots, or step-by-step guide for performing an export
- **Placeholder descriptions** — 19.2% of all columns have unhelpful template descriptions, concentrated in the most complex clinical tables (labs, medications, drug administration)
- **The largest, most important clinical tables have the worst documentation** — HC_LabC (118 cols), HC_DrugRxHis (88 cols), HC_DrugHisAT (84 cols) all have "poor" description quality
- **No documentation of the EAV template structure** — the VE_Data_* tables store much clinical exam data, but without template definitions, the data is unusable
- **The HTML pages lack consistent structure** — some have `<html>` wrappers, some are bare fragments, with inconsistent formatting

### Structure & Completeness

- **Granularity**: Field-level documentation with column names and descriptions, but missing data types and constraints
- **Coded fields**: Extensively used (hundreds of `*ID` columns) but value sets are completely undocumented
- **Relationships**: Implicit through shared column names only; no ER diagram or relationship specification
- **Versioning**: Last-modified date on the server (2025-10-10) but no version number or change history in the documentation itself

### Overall Assessment

VersaSuite has made a genuine effort at (b)(10) compliance. The export is CSV-based (not just repackaged FHIR), covers clinical, administrative, and financial data domains, and the documentation is publicly accessible. The breadth of 96 tables across 6 functional domains reflects the product's single-database architecture.

However, the documentation has significant gaps that would prevent a third party from fully interpreting the exported data:

1. **The absence of lookup/reference tables** means that coded values throughout the export cannot be decoded. This is the single largest gap.
2. **The missing template definitions** for the EAV-structured exam data (`VE_Data_*` tables) means a substantial portion of clinical data would be opaque.
3. **No data types, no value sets, no formal schema** makes automated import essentially impossible without significant reverse-engineering.
4. **Placeholder descriptions in the most important clinical tables** undermine the documentation's utility where it matters most.

The documentation reads as a compliance artifact that was generated (likely with AI assistance, given the templated description patterns) rather than a carefully maintained data dictionary designed for interoperability. It satisfies the letter of the (b)(10) requirement (publicly accessible format documentation) but falls short of enabling practical data portability.

## Access Summary
- Final URL (after redirects): https://docs.versasuite.com
- Status: found
- Required browser: no
- Navigation complexity: direct_link (single index page with 96 linked data dictionary pages)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The documentation was straightforward to access and download. No authentication, no JavaScript rendering, no anti-bot measures, no broken links.
