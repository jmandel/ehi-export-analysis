# EHI Export Analysis: eClinicalWorks, LLC

**Product**: eClinicalWorks (Versions 12.0.2 and 12.0.3)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2883.eCli.12.07.1.230613 (v12.0.2), 15.04.04.2883.eCli.12.08.1.240322 (v12.0.3)

## 1. Product Context

eClinicalWorks is a comprehensive, cloud-based ambulatory EHR and Practice Management platform — one of the largest in the U.S., serving 180,000+ providers and 110,000+ facilities. It is a unified product combining EHR, Practice Management, and Revenue Cycle Management into a single offering (not separate modules). Key capabilities relevant to export completeness:

- **Clinical**: SOAP notes with specialty templates, CPOE, problem lists, medication lists, allergy management, vital signs, clinical decision support, care plans, AI-assisted documentation (Sunoh.ai scribe)
- **Prescribing**: ePrescribing including controlled substances (EPCS), drug interaction checks, Surescripts integration
- **Labs & Imaging**: Electronic lab ordering/results, diagnostic imaging orders
- **Billing/RCM**: Integrated billing, claims creation/scrubbing/submission, denial management, payment posting, AR tracking — either self-service or fully outsourced RCM
- **Patient Engagement**: healow portal (messaging, appointments, prescriptions, payments), telehealth/TeleVisits, remote patient monitoring, automated outreach campaigns
- **Interoperability**: PRISMA health information search engine aggregating records from multiple EHRs/hospitals/payers, FHIR APIs, C-CDA exchange
- **Specialty**: Behavioral health, OB/GYN, dental, vision/ophthalmology, cardiology, orthopedics, neurology, allergy/immunology
- **Population Health**: ACO/CIN management, HEDIS reporting, HCC coding, chronic care management (CCM), care gap identification
- **Documents**: Fax management, document scanning, Image AI categorization

The EHI export should cover clinical, billing, specialty, patient engagement, and interoperability data stored across all of these functional areas.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/tableindex.html` (134 KB) | Main index page listing all 1,466 database tables with links to detail pages. Contains header text explaining (b)(10) certification, export scope, and usage notes. Last reviewed 01/27/2026. | **High** — defines scope, confirms single-patient and bulk export |
| `downloads/tables/*.html` (1,466 files) | Individual data dictionary pages for each table, with table description, column names, data types, and column descriptions | **High** — primary source of truth for export content |
| `product-research.md` | Prior research on eClinicalWorks product capabilities | **Medium** — establishes baseline for coverage assessment |
| `ehi-export-report.md` | Prior agent's narrative about the export documentation | **Medium** — useful for orientation, verified against source data |
| `files.json` | Manifest of downloaded artifacts | **Low** — administrative |
| `metadata.json` | CHPL certification details | **Low** — confirms certification status |

The 1,466 individual HTML table pages are the core artifacts. No PDFs, sample data files, downloadable schemas, or API documentation were found — the entire data dictionary is presented as static HTML.

## 3. Export Mechanics

- **Format**: Proprietary relational database dump — SQL table structures exported directly from the eClinicalWorks database. Not FHIR, C-CDA, or any health data standard. Scanned documents are stated to be "included in a separate folder apart from the database tables."
- **Mechanism**: The index page states: eClinicalWorks "enables a defined set of users to create an export of all EHI stored in the eClinicalWorks EHR for a single patient, or to initiate a request for export of all EHI stored in the eClinicalWorks EHR for an entire patient population." Specific UI steps or API details are not documented on this site; users are directed to the Mandatory Disclosures page at `www.eclinicalworks.com/resources/certified-ehr-technology` for more details.
- **Single-patient**: Yes (explicitly stated)
- **Bulk/population**: Yes (explicitly stated — "entire patient population")
- **Access constraints**: The page notes that "the data extract must be carefully reviewed and excluded before sharing it with individuals outside of the practice" due to sensitive data (e.g., SSN). The export may also contain third-party proprietary codes (e.g., CPT) with usage restrictions.
- **Fees**: Not addressed in the documentation.
- **Last reviewed**: 01/27/2026

## 4. Export Content: What's In It

### Overview

The export comprises **1,466 database tables** with **21,143 total columns/fields**. This is a direct database export reflecting eClinicalWorks' internal data model.

**Documentation quality per field**:
- **21,094 of 21,143 fields (99.8%)** have human-readable descriptions beyond just a column name
- **1,455 of 1,466 tables** have table-level descriptions explaining what the table stores
- **82 foreign key references** are documented in column descriptions (e.g., "This column refers to the UID column in the user table")
- **81 columns** are explicitly marked as "not being used"
- **2 tables** have zero columns parsed (appear to be backup/empty tables: `encdashboard_bkp`, `ip_homemedication_additionalinfo`)
- All fields include SQL data types (int, varchar, datetime, smallint, char, text, tinyint, decimal, etc.)

### Vendor's own content organization

The export data dictionary does not use explicit vendor-defined categories — tables are listed alphabetically. The categorization below is derived from table names, prefixes, and descriptions. A complete machine-readable inventory is in `analysis/entity-inventory-full.json`; a summary in `analysis/entity-inventory-summary.json`.

**Category breakdown** (sorted by field count):

| Category | Tables | Fields | Fields w/ Descriptions |
|---|---|---|---|
| Billing / Revenue Cycle | 161 | 4,279 | 4,279 |
| Other / Miscellaneous | 226 | 2,601 | 2,585 |
| Encounters | 120 | 1,215 | 1,201 |
| Inpatient / Hospital | 92 | 1,158 | 1,158 |
| Vision / Ophthalmology | 77 | 1,107 | 1,107 |
| Medications / Prescriptions | 42 | 939 | 938 |
| Patient Demographics | 58 | 793 | 787 |
| Ambulatory Surgery Center | 78 | 764 | 764 |
| Dental | 33 | 634 | 634 |
| Clinical Notes / Documents | 65 | 590 | 589 |
| Insurance / Coverage | 13 | 568 | 568 |
| Inventory Management | 22 | 504 | 504 |
| Allergies | 38 | 453 | 452 |
| Referrals / Orders | 26 | 417 | 412 |
| Chronic Care Management | 30 | 409 | 409 |
| Immunizations | 28 | 379 | 379 |
| Problems / Diagnoses | 28 | 339 | 339 |
| Behavioral Health | 38 | 324 | 324 |
| Procedures | 19 | 300 | 299 |
| Interoperability (PRISMA) | 21 | 295 | 295 |
| Patient Portal | 16 | 279 | 279 |
| Lab Results | 17 | 263 | 263 |
| Messages / Communication | 7 | 243 | 243 |
| OB/GYN | 17 | 220 | 216 |
| Care Plans / Goals | 26 | 198 | 198 |
| Flowsheets | 7 | 192 | 192 |
| Correctional Health | 7 | 187 | 187 |
| Scheduling | 15 | 152 | 152 |
| Occupational Health | 17 | 150 | 150 |
| Dermatology | 13 | 137 | 137 |
| Vitals | 12 | 124 | 124 |
| Vascular | 9 | 91 | 91 |
| Lifestyle Medicine | 6 | 91 | 91 |
| Consents / Directives | 6 | 89 | 89 |
| Tasks / To-Do | 12 | 87 | 87 |
| Templates / Forms | 10 | 87 | 87 |
| Quality / Value-Based Care | 9 | 78 | 78 |
| Documents / Attachments | 6 | 76 | 76 |
| FHIR / Interoperability | 12 | 73 | 73 |
| Cardiology | 4 | 73 | 73 |
| Case Management | 5 | 68 | 68 |
| Remote Patient Monitoring | 9 | 63 | 63 |
| Sports Medicine | 5 | 28 | 28 |
| Anticoagulation Management | 3 | 22 | 22 |
| Imaging / Radiology | 1 | 4 | 4 |

### 20 largest tables (representative examples)

| Table | Columns | Category | Description |
|---|---|---|---|
| `nycompboardc43` | 218 | Billing / Revenue Cycle | NY Workers' Compensation Board claim form C-4.3 |
| `nycompboardc42` | 196 | Billing / Revenue Cycle | NY Workers' Compensation Board claim form C-4.2 |
| `nycompboard` | 170 | Billing / Revenue Cycle | NY Workers' Compensation Board claim form |
| `insurance` | 166 | Insurance / Coverage | Patient insurance information |
| `dental_print` | 162 | Dental | Dental claim print data |
| `mcaid_co` | 162 | Billing / Revenue Cycle | Colorado Medicaid claim form |
| `mcaid_or` | 159 | Billing / Revenue Cycle | Oregon Medicaid claim form |
| `mcaid_ny` | 157 | Billing / Revenue Cycle | New York Medicaid claim form |
| `hcfa` | 153 | Billing / Revenue Cycle | HCFA/CMS-1500 claim form data |
| `massform5` | 152 | Billing / Revenue Cycle | Massachusetts claim form |
| `dental_predet_printxml` | 150 | Dental | Dental predetermination print XML |
| `nycompaddinfoc43` | 146 | Insurance / Coverage | NY Workers' Comp additional info |
| `patients_correctional` | 146 | Correctional Health | Correctional health patient demographics |
| `mcaid_il_478_1210` | 138 | Billing / Revenue Cycle | Illinois Medicaid claim form |
| `nycompaddinfoc42` | 137 | Billing / Revenue Cycle | NY Workers' Comp additional info (C-4.2) |
| `surescript_requestlog` | 136 | Medications / Prescriptions | Surescripts e-prescribing request log |
| `patients` | 130 | Patient Demographics | Core patient demographics table |
| `edi_ub92` | 127 | Billing / Revenue Cycle | UB-92/UB-04 institutional claim form |
| `inventory_product` | 112 | Inventory Management | Product inventory details |
| `x271respdetails` | 112 | Insurance / Coverage | X12 271 eligibility response details |

The billing tables are notably large because they include state-specific claim form fields (NY Workers' Comp, various Medicaid forms, etc.), reflecting the depth of the revenue cycle integration.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is exceptionally broad, reflecting eClinicalWorks' position as a unified EHR+PM+RCM platform. Key strengths:

**Billing / Revenue Cycle (161 tables, 4,279 fields)**: The deepest single category. Includes HCFA/CMS-1500 claim forms, UB-92/UB-04 institutional claims, state-specific Medicaid forms (CO, OR, NY, IL, MA), Workers' Compensation forms, adjustment postings, ERA/remittance, charge posting, collections, payment records, and EDI transaction tables. This is genuinely comprehensive billing coverage — far beyond what any FHIR or C-CDA export would include.

**Encounters (120 tables, 1,215 fields)**: Extensive encounter documentation including the core `enc` table (implied to be very large based on FK references throughout), encounter types, encounter-level billing, dashboard data, and workflow state.

**Specialty-specific data**: The export includes dedicated tables for at least 10 clinical specialties:
- Vision/Ophthalmology: 77 tables (visual acuity, refraction, slit lamp, tonometry, IOP measurements)
- Behavioral Health: 38 tables (BH encounters, BH-specific billing, addendums)
- Dental: 33 tables (dental charts, dental claims, predeterminations)
- Ambulatory Surgery Center: 78 tables (anesthesia plans, surgical orders, device test data, belongings tracking)
- OB/GYN: 17 tables (obstetric history, prenatal records)
- Dermatology: 13 tables
- Occupational Health: 17 tables (employment records, occupational health assessments)
- Correctional Health: 7 tables (correctional facility patient demographics — 146 fields)
- Vascular: 9 tables
- Cardiology: 4 tables
- Sports Medicine: 5 tables
- Lifestyle Medicine: 6 tables
- Anticoagulation Management: 3 tables

**Patient engagement (16 portal tables, 7 messaging tables, 9 RPM tables)**: Includes patient portal records, messaging, and remote patient monitoring data.

**Interoperability (21 PRISMA tables, 12 FHIR tables)**: Includes PRISMA health information aggregation records and FHIR integration data.

**Chronic Care Management (30 tables, 409 fields)**: CCM encounter records, care management workflows.

**Thinnest areas**: Imaging/Radiology has only 1 table (4 fields), though imaging may be partially captured within encounter or order tables. Cardiology has only 4 tables, which seems thin for a product advertising cardiology workflows.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (130 fields), `patients_correctional` (146 fields), `additionaladdress`, `users`, `users_additionalinfo`, 58 tables total | Thorough — includes contact info, addresses, guardians, insurance demographic data |
| Encounters / visits | ✅ Covered | 120 tables, 1,215 fields including core encounter data, encounter types, encounter workflows | Comprehensive |
| Problems / conditions / diagnoses | ✅ Covered | 28 tables, 339 fields including ICD-coded diagnoses, problem lists | Solid |
| Medications / prescriptions | ✅ Covered | 42 tables, 939 fields including prescriptions, e-prescribing (Surescripts), drug interactions, formulary data, dispensing | Very thorough |
| Allergies | ✅ Covered | 38 tables, 453 fields including allergy shots, vial management, allergen formulations, allergy-specific billing | Exceptionally detailed |
| Immunizations | ✅ Covered | 28 tables, 379 fields including immunization records, registries, VFC (Vaccines for Children), antigen bottles/recipes | Comprehensive |
| Vitals | ✅ Covered | 12 tables, 124 fields | Adequate |
| Lab results | ✅ Covered | 17 tables, 263 fields including lab orders, results, panels | Solid |
| Imaging / diagnostic reports | ⚠️ Partial | Only 1 dedicated imaging table (4 fields); imaging orders may be in order/encounter tables | Product does imaging ordering; dedicated imaging tables are thin |
| Procedures | ✅ Covered | 19 tables, 300 fields | Solid |
| Clinical notes / documents | ✅ Covered | 65 tables, 590 fields; scanned documents stated to be "included in a separate folder" | Comprehensive; includes progress notes, letters, addendums, electronic case reports |
| Care plans / goals | ✅ Covered | 26 tables, 198 fields | Adequate |
| Orders / referrals | ✅ Covered | 26 tables, 417 fields | Solid |
| Insurance / coverage | ✅ Covered | 13 tables, 568 fields including `insurance` (166 fields), X12 270/271 eligibility transactions | Very thorough |
| Claims / billing | ✅ Covered | 161 tables, 4,279 fields — HCFA, UB-92, state Medicaid, Workers' Comp, EDI transactions | Exceptionally comprehensive — the standout strength of this export |
| Payments | ✅ Covered | Included in billing tables — payment posting, adjustment posting, ERA/remittance, patient balance, copay records | Thorough |
| Consents / directives | ✅ Covered | 6 tables, 89 fields including advance directives and consent records | Adequate |
| Patient communications / portal messages | ✅ Covered | 7 messaging tables (243 fields), 16 patient portal tables (279 fields) | Solid |
| Telehealth | ⚠️ Partial | No dedicated telehealth tables identified by name; telehealth visits may be captured as encounter types | Product offers TeleVisits; unclear if separately tracked in export |
| Remote Patient Monitoring | ✅ Covered | 9 RPM tables, 63 fields | Present |
| Behavioral Health | ✅ Covered | 38 tables, 324 fields | Specialty-specific coverage |
| Dental | ✅ Covered | 33 tables, 634 fields | Specialty-specific, includes dental claims |
| Vision / Ophthalmology | ✅ Covered | 77 tables, 1,107 fields | Exceptionally detailed specialty coverage |
| OB/GYN | ✅ Covered | 17 tables, 220 fields | Specialty-specific |
| Ambulatory Surgery | ✅ Covered | 78 tables, 764 fields | Deep ASC-specific coverage |
| Correctional Health | ✅ Covered | 7 tables, 187 fields | Specialty-specific |

## 6. Documentation Quality

**Strengths**:
- **Near-complete field descriptions**: 99.8% of all 21,143 fields have human-readable descriptions. This is exceptionally high — descriptions are typically full sentences explaining the field's purpose, not just restating the column name.
- **Table-level descriptions**: 1,455 of 1,466 tables (99.2%) have descriptions explaining what the table stores and how it relates to the application.
- **Foreign key documentation**: While not a formal ERD, column descriptions frequently reference related tables (e.g., "This column refers to the UID column in the user table"), providing navigable relationship information.
- **Data types**: Every column includes its SQL data type.
- **Value set hints**: Many descriptions include example values or enumeration of allowed values (e.g., "1 - structured/coded allergy, 2 - unstructured/uncoded allergy"; "Two statuses are stored in this column 'Active' or 'Inactive'").

**Weaknesses**:
- **No formal schema**: No machine-readable schema (XSD, JSON Schema, SQL DDL) is provided — only HTML pages.
- **No sample data**: No sample export files or example records are available.
- **No ERD or relationship diagram**: Relationships must be inferred from description text; no formal foreign key schema.
- **No comprehensive value set documentation**: While some descriptions mention example values, there's no systematic enumeration of coded value sets.
- **No export procedure documentation**: The data dictionary doesn't explain how to initiate or use the export; users are directed to the Mandatory Disclosures page.
- **81 "not being used" columns**: Some columns are documented as not in active use but remain in the schema.

**Overall**: A developer could understand the structure and semantics of the export from this documentation. The descriptions are detailed enough to build an import or transformation pipeline, though the lack of formal schemas and sample data would slow the process. The documentation is among the most detailed data dictionaries seen in EHI export compliance — the field-level descriptions alone represent significant effort.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is one of the most comprehensive EHI exports analyzed. The export covers 1,466 tables across virtually every data domain the product stores. The standout evidence:

- **Billing is deeply covered** (161 tables, 4,279 fields) — this alone distinguishes it from repackaged clinical exports. The billing tables include state-specific claim forms for at least 5 states, Workers' Compensation forms, EDI transactions, ERA/remittance, and collections data.
- **10+ clinical specialties** have dedicated table sets: vision/ophthalmology (77 tables), dental (33 tables), behavioral health (38 tables), ASC (78 tables), OB/GYN (17 tables), dermatology, occupational health, correctional health, vascular, cardiology, sports medicine, and lifestyle medicine.
- **Patient engagement** data (portal, messaging, RPM) is included.
- **Interoperability data** (PRISMA, FHIR integration records) is included.
- The only notable gaps are thin imaging/radiology coverage (1 table) and unclear telehealth-specific data, though these may be captured within encounter structures.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. Evidence:

- The export is a **direct database dump** of 1,466 internal tables — the vendor's native data model, not a FHIR or C-CDA projection.
- There is **no mention of FHIR, C-CDA, US Core, or USCDI** anywhere in the documentation. This is entirely separate from the vendor's (g)(10) FHIR API.
- The export includes **billing, claims, insurance, Workers' Compensation, state Medicaid forms, inventory management, and administrative data** — none of which would be in a standard clinical exchange format.
- A dedicated documentation site (`ehi.eclinicalworks.com/ehiexport/`) was built specifically for this purpose with 1,466 individual data dictionary pages.
- The index page explicitly describes (b)(10) certification and states the export covers "all EHI stored in the eClinicalWorks EHR."

### Key Findings

1. **Exceptionally comprehensive billing coverage**: 161 tables with 4,279 fields dedicated to billing/revenue cycle — including state-specific claim forms, Workers' Comp, EDI, and ERA data. This is the deepest billing coverage seen in any EHI export and is strong evidence of genuine (b)(10) engagement.

2. **Extensive specialty clinical data**: 10+ clinical specialties have dedicated table sets, with vision/ophthalmology alone having 77 tables and 1,107 fields. This goes far beyond any USCDI-scoped export.

3. **Near-universal field documentation**: 99.8% of 21,143 fields have descriptive text, and 99.2% of tables have table-level descriptions. This represents significant documentation effort.

4. **No sample data or machine-readable schema**: Despite excellent documentation, the absence of sample export files, SQL DDL, or formal schemas means developers must work from HTML pages alone. No ERD or relationship diagram is provided.

5. **Scanned documents included separately**: The index page states "Scanned documents are included in a separate folder apart from the database tables," confirming that document/image data is part of the export.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   Database dump (proprietary relational tables) + separate document folder
    Entities:        1,466 tables
    Fields:          21,143
    Descriptions:    99.8% of fields have descriptions
    Sample data:     No
    Bulk export:     Yes (single-patient and population-level)
    Domains covered: 23 of 24 applicable domains (imaging/radiology thin; telehealth unclear)

### Bottom Line

eClinicalWorks delivers one of the strongest (b)(10) EHI exports examined. With 1,466 tables covering 21,143 fields across clinical, billing, specialty, and administrative domains — all with near-universal field-level documentation — this is a genuine, purpose-built database-level export that goes far beyond USCDI or clinical exchange requirements. The biggest gap is the absence of sample data and machine-readable schemas, which would make the export easier to consume; the data coverage itself is exemplary.
