# EHI Export Analysis: Altera Digital Health

**Product**: Sunrise Acute Care / Sunrise Acute Care for Hospital-based Providers / Sunrise Ambulatory Care
**Analysis date**: 2026-02-16
**CHPL IDs**: 11707, 11708, 11709

## 1. Product Context

Sunrise is Altera Digital Health's flagship comprehensive EHR platform for hospitals and health systems, providing a **unified patient record** across acute (inpatient), ambulatory (outpatient), and financial/revenue cycle settings. The platform evolved from the legacy Allscripts Sunrise Clinical Manager and was rebranded when N. Harris Computer Corporation acquired the product line in 2022.

Sunrise covers an extensive range of clinical and operational workflows:

- **Clinical Documentation & CPOE**: Progress notes, H&P, clinical decision support, computerized physician order entry, patient tracking boards, ambient AI-assisted note generation (Sunrise Thread AI)
- **Medication Management & Pharmacy**: e-Prescribing, medication reconciliation, barcode medication administration (BCMA), integrated pharmacy module
- **Orders & Results**: Lab ordering/results, radiology integration, order sets
- **Surgery & Perioperative**: Anesthesia records, pre-op/intra-op/post-op documentation
- **Financial Management (Sunrise Financial Manager)**: Claims, self-pay, billing, SuperBill/charge capture, appeals/denials, episode management, registration/ADT
- **Scheduling**: Appointments, resource management, patient tracking
- **Health Information Management**: Document management, scanning, audit support
- **Patient Engagement (Sunrise CarePath)**: Mobile app, appointment reminders, provider messaging, online bill pay, results access
- **Analytics & Reporting**: Clinical and financial BI, quality measures

The breadth of this product means a genuine (b)(10) export should cover clinical data, financial/billing data, scheduling, documents, pharmacy, surgery, and ambulatory-specific workflows. The three certified products (Acute Care, Acute Care for Hospital-based Providers, Ambulatory Care) all share the same underlying database.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-weberdiagram-22-1-pr38.zip` (13.7 MB) | Latest WebER data dictionary (Apr 2025) with 4 schemas, 2,747 tables, 42,849 columns. **Primary artifact.** | ⭐⭐⭐⭐⭐ |
| `sunrise-ehi-export-definition-22-1pr23.zip` (12.5 MB) | Earliest version (Nov 2023), SCM-only | Historical context only |
| `sunrise-ehi-weberdiagram-22-1-pr24-1.zip` (12.5 MB) | Second release | Historical context only |
| `sunrise-ehi-export-definition-22-1-pr27.zip` (12.7 MB) | Mid-cycle update | Historical context only |
| `ehi-weberdiagram-22-1-pr28.zip` (12.7 MB) | Updated release | Historical context only |
| `enrichment/tables.json` (14.6 MB) | Prior extraction of PR38 into structured JSON (2,747 tables, 42,849 columns). Used for cross-validation. | ⭐⭐⭐⭐ |
| `enrichment/columns.csv` (7.8 MB) | One-row-per-column CSV extract | ⭐⭐⭐ |
| `enrichment/tables-summary.csv` (375 KB) | One-row-per-table summary | ⭐⭐⭐ |
| `enrichment/extract-tables.ts` | Bun/TypeScript extraction script (reference for parsing approach) | ⭐⭐ |

The PR38 WebER archive is overwhelmingly the most informative artifact — it is a complete, static HTML site documenting every table and column in the Sunrise database that is part of the EHI export. I extracted and independently parsed all 2,747 HTML table files from this archive using my own Python script (`analysis/parse-weber.py`), producing results that exactly match the enrichment extraction.

## 3. Export Mechanics

- **Format**: SQL Server database export. The documentation describes SQL Server table schemas (dbo schema, SQL Server data types: `int`, `varchar`, `datetimeoffset`, `uniqueidentifier`, `nvarchar`, `varbinary(max)`, `bit`, etc.). The export is the vendor's native data model — not FHIR, not C-CDA, not any external standard.
- **Mechanism**: The Altera compliance page states: "Click on the links below to download the EHI Export Documentation zip file to your local machine. Click on the index.html file in the extracted files folder to view the EHI Export definition in your web browser." No user-facing export workflow or API is documented — the documentation describes the schema of what would be exported, but the actual export mechanism (UI button, admin tool, vendor-assisted) is not specified.
- **Single-patient vs bulk**: Not specified in the documentation. The schema supports both — tables have patient-linking columns (e.g., `ClientGUID`, `ClientVisitGUID`).
- **Access constraints or fees**: Not documented in the artifacts. The Altera compliance page has a separate "Cost & Limitations" section, but details about export fees were not part of the downloaded artifacts.
- **Documentation versioning**: 5 versions published over ~18 months (PR23 Nov 2023 → PR38 Apr 2025), showing active maintenance. The latest version expanded from 1 schema (SCM) to 4 schemas (FS, IMG, MNC, SCM).

## 4. Export Content: What's In It

### Overview

The PR38 data dictionary documents **2,747 tables** with **42,849 columns** across 4 database schemas:

| Schema | Full Name | Tables | Columns | Description |
|---|---|---|---|---|
| **SCM** | Sunrise Clinical Manager | 2,728 | 42,581 | Core clinical, billing, and operational database |
| **MNC** | Medical Necessity Checking | 11 | 160 | Medical necessity / ABN configuration |
| **IMG** | Imaging | 7 | 104 | Document imaging and binary object storage |
| **FS** | Financial System | 1 | 4 | EHI-specific view into imaging file storage |

### Documentation Quality per Field

- **42,849 of 42,849 columns (100%)** have non-empty descriptions
- **42,849 of 42,849 columns (100%)** have documented data types
- **2,747 of 2,747 tables (100%)** have table-level definitions
- **3,499 columns** are explicitly marked as foreign keys (with FK indicator in HTML)
- **0 parse errors** across all 2,747 table files

Descriptions are genuinely meaningful — they explain business context, not just repeat column names. For example: *"Information about the user that last updated the row. This will typically be the UserID (IDCode from CV3User table) and may be prefixed with an environment identifier followed by an underscore."*

### Vendor's Own Content Organization

The tables follow a consistent naming convention that reveals their functional domain. Using prefix-based categorization:

| Domain (by table prefix) | Tables | Columns | Key Examples |
|---|---|---|---|
| Revenue Cycle / Billing (`SXARCM*`) | 917 | 13,105 | Claims, charges, payments, denials, appeals, fee schedules, payer configs, ERA transactions, SuperBill |
| Other Sunrise Application (`SXA*`) | 447 | 6,347 | Cross-cutting application tables, referrals, transport, rules, batch processing |
| Core Clinical (`CV3*`) | 386 | 8,871 | Patient data, visits, orders, observations, medications, notes, flowsheets, alerts |
| Ambulatory Care (`SXAAMB*`, `SXAAM*`) | 348 | 4,913 | Ambulatory visits, prescriptions, scheduling, referrals, patient communications |
| Medication Management (`SXAMM*`) | 163 | 2,724 | Drug catalog, dosing, dispensing, storage, pharmaceutical products |
| Surgery / Perioperative (`SXASRG*`) | 146 | 1,994 | Surgical cases, anesthesia, case indicators, perioperative records |
| Scheduling / Enterprise Services (`SXAES*`) | 92 | 1,384 | Appointments, booking, scheduling templates, equipment, locations |
| Clinical Documentation / eICR (`SXACDE*`, `SXACD*`) | 88 | 1,208 | Clinical documents, exchange documents, eICR reporting |
| Health Management (`SXAHM*`) | 41 | 587 | Vaccine tracking, event management, consent types |
| Enterprise Service Mgmt (`SXAESM*`) | 37 | 443 | Templates, notifications, service management |
| Clinical Record Tracking (`SXACRT*`) | 29 | 404 | Tile configurations, problem list tracking, IV drips |
| SCM Configuration (`SCM*`) | 22 | 406 | Observation coded values, flowsheet configurations |
| Medical Necessity (`SXAMNC*`) | 11 | 160 | ABN forms, medical necessity checking rules |
| Immunization Management (`SXAIMM*`) | 9 | 138 | Immunization queries, VFC eligibility |
| Imaging / Documents (`SXAIMG*`) | 7 | 104 | Document types, binary objects, elements |
| Other | 4 | 61 | Miscellaneous |

The full entity inventory is available in `analysis/entity-inventory-full.json` (2,747 table objects with all 42,849 column definitions).

### Notable Entity Examples

The **20 largest tables** (by column count) reveal the depth of clinical and operational data:

| Table | Columns | Domain |
|---|---|---|
| `CV3EnterpriseVisitData` | 163 | Core Clinical |
| `CV3EnterpriseChartData` | 163 | Core Clinical |
| `CV3EnterpriseClientData` | 162 | Core Clinical (patient master) |
| `CV3OutpatientOrder` | 118 | Orders |
| `CV3Order` | 118 | Orders |
| `CV3ObsCatalogMasterItem` | 108 | Observations |
| `CV3OrderAddnlInfo` | 100 | Orders |
| `SXAAMBClientPrescription` | 98 | Ambulatory prescriptions |
| `CV3MedicationExtension` | 95 | Medications |
| `CV3OrderCatalogMasterItem` | 94 | Order catalog |
| `SXARCMEDITransactionControl` | 77 | Revenue Cycle EDI |
| `CV3Location` | 75 | Locations/facilities |
| `CV3AlertRepository` | 70 | Clinical alerts |
| `SXAAMBPharmacy` | 69 | Ambulatory pharmacy |
| `SXAESAppointment` | 67 | Scheduling |
| `CV3BasicObservation` | 66 | Vitals/observations |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around the Sunrise database's native schemas and table naming conventions:

**Revenue Cycle / Billing (917 tables, 13,105 columns)** — This is the single largest domain, comprising 33% of all tables and 31% of all columns. It includes claims (`SXARCMClaim*`), charges (`SXARCMCharge*`), payments, adjustments, denials and appeals (`SXARCMAppeal*`, `SXARCMDenial*`), fee schedules, payer configurations, ERA/EDI transactions (`SXARCMEDITransaction*`), SuperBill data, and episode management. This is a genuinely deep billing export — most vendors omit billing entirely.

**Core Clinical (386 tables, 8,871 columns)** — The `CV3*` prefix covers the legacy Sunrise Clinical Manager tables: patient records (`CV3Person*`, `CV3EnterpriseClientData`), visits (`CV3ClientVisit`, `CV3EnterpriseVisitData`), orders (`CV3Order*` — 118 columns each), medications (`CV3MedicationExtension` — 95 columns), observations/vitals (`CV3BasicObservation` — 66 columns, `CV3ObsCatalogMasterItem` — 108 columns), flowsheets (`CV3FlowsheetVersion*`), notes, alerts, and clinical documents.

**Ambulatory Care (348 tables, 4,913 columns)** — Ambulatory-specific data including prescriptions (`SXAAMBClientPrescription` — 98 columns), pharmacy management, referrals, patient communications, and ambulatory scheduling.

**Medication Management (163 tables, 2,724 columns)** — Drug catalogs, dosing rules, dispensing records, medication storage, pharmaceutical products, and BCMA data.

**Surgery / Perioperative (146 tables, 1,994 columns)** — Surgical cases, anesthesia records, case indicators, surgical items, and perioperative documentation.

**Scheduling (92 tables, 1,384 columns)** — Appointments, booking rules, equipment, locations, and scheduling templates.

**Clinical Documentation (88 tables, 1,208 columns)** — Clinical documents, exchange documents, and electronic initial case reports (eICR).

**Health Management & Immunizations (50 tables, 725 columns)** — Vaccine tracking, immunization registry data, VFC eligibility, and event management.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `CV3Person*` (5+ tables), `CV3EnterpriseClientData` (162 cols), `CV3Address*`, contact tables | Deeply covered — 162-column patient master includes extensive demographics |
| Encounters / visits | ✅ Covered | `CV3ClientVisit`, `CV3EnterpriseVisitData` (163 cols), 89+ visit-related tables | Comprehensive — visit data is one of the richest areas |
| Problems / conditions / diagnoses | ✅ Covered | `SXASCLProblem`, `SXASCLVisitSOSProblem`, `CV3DiagnosisList*`, condition tables | Problem lists and diagnoses documented |
| Medications / prescriptions | ✅ Covered | 163 medication management tables + 5 `CV3Med*` tables + `SXAAMBClientPrescription` (98 cols) | Deeply covered across inpatient and ambulatory |
| Allergies | ✅ Covered | 27+ allergy tables: `CV3AllergyDeclaration`, `SXAAMBAllergyClass`, `SXAAllergyInteraction*` | Includes allergens, reactions, severity, and interactions |
| Immunizations | ✅ Covered | 32 immunization tables: `SXAHMVaccine*`, `SXAIMMImmunization*`, VFC data | Registry reporting, vaccine tracking, manufacturer data |
| Vitals | ✅ Covered | `CV3BasicObservation` (66 cols), 20+ observation tables, flowsheet tables | Vitals stored in generic observation model with 108-column observation catalog |
| Lab results | ✅ Covered | 129+ lab-related tables: `CV3SpecimenType`, results tables, lab integration | Specimens, results, observations all documented |
| Imaging / diagnostic reports | ✅ Covered | 7 IMG schema tables + radiology-related `CV3*` tables | Document imaging, binary objects, radiology results |
| Procedures | ✅ Covered | Surgery tables (146), plus procedure-related order tables | Deeply covered for surgical/perioperative |
| Clinical notes / documents | ✅ Covered | 225+ document/note-related tables, clinical documentation tables | Extensive — covers notes, charts, documents, annotations |
| Care plans / goals | ⚠️ Partial | `SXACCClientCareGoal` (1 table); no explicit care plan tables | Goals present but care plans as a distinct entity are thin |
| Orders / referrals | ✅ Covered | `CV3Order` (118 cols), `CV3OrderCatalogMasterItem` (94 cols), 69+ order tables, referral tables | Deeply covered — orders are among the richest entities |
| Insurance / coverage | ✅ Covered | 76+ insurance-related tables within SXARCM* (payer configs, eligibility, plans) | Part of the revenue cycle domain |
| Claims / billing | ✅ Covered | 917 SXARCM* tables covering claims, charges, payments, adjustments, denials, appeals, ERA/EDI | **Exceptionally deep** — 33% of all tables |
| Payments | ✅ Covered | Payment, adjustment, and remittance tables within SXARCM* domain | Included in revenue cycle tables |
| Consents / directives | ⚠️ Partial | `SXAHMConsentType`, `SXAHMOccurrenceConsentDocXREF`, `SXACDExchangeDocumentSharedConsent` | Consent types documented but thin (3 tables) |
| Patient communications / portal | ⚠️ Partial | `SXAAMContactPatientCommunication`, messaging tables; no explicit portal data tables | Some patient communication tables but no obvious portal-specific data |
| Specialty — Surgery/Perioperative | ✅ Covered | 146 `SXASRG*` tables covering surgical cases, anesthesia, indicators | Deep surgical/perioperative data |
| Specialty — Pharmacy | ✅ Covered | 163 `SXAMM*` tables + `SXAAMBPharmacy` (69 cols) | Comprehensive pharmacy management |
| Specialty — Radiology | ✅ Covered | IMG schema + radiology-related clinical tables | Imaging and radiology data included |
| Scheduling | N/A | 113+ scheduling tables | Scheduling is operational data, not EHI per se, but included |

**Key gaps relative to product capabilities:**
- **Patient portal data (CarePath)**: Sunrise includes a patient engagement app (CarePath) with messaging, bill pay, and results access. Portal-specific interaction data is not prominently visible in the schema, though `SXAAMContactPatientCommunication` may capture some messaging.
- **Care plans**: The product supports clinical decision support and care coordination, but explicit care plan entities are thin (1 goal table, no dedicated care plan tables).
- **Advance directives**: Only 2 tables with "Advanced" in the name, and they relate to visit list definitions rather than patient directives.

## 6. Documentation Quality

**Strengths:**
- **Completeness**: 2,747 tables and 42,849 columns with 100% description coverage — every field has a meaningful business definition, not just a column name.
- **Consistency**: Every table follows the same HTML template: qualified name, definition, columns with types, nullable flags, PK indicators, and descriptions.
- **Active maintenance**: 5 releases over 18 months (Nov 2023 – Apr 2025), with expanding scope (PR38 added 3 new schemas).
- **Machine-readable**: While delivered as HTML, the consistent structure allows automated parsing. Both the enrichment script and my own Python parser achieved 0 parse errors across all 2,747 files.
- **Honest approach**: The vendor documents the actual database schema rather than a sanitized or abstracted summary.

**Weaknesses:**
- **No export procedure documentation**: There are no user guides, screenshots, or instructions for how to actually perform the export. The compliance page says to "view the EHI Export definition in your web browser" but provides no workflow.
- **No sample data**: No example export files, sample records, or test data are provided.
- **No FK relationship diagrams**: Despite using an ER diagram tool (WebER), the relationship pages in PR38 are empty — no foreign key relationships are explicitly documented as diagrams. However, 3,499 columns are marked with FK indicators in the table HTML, and column definitions frequently reference related tables by name.
- **No value set enumeration**: Coded fields reference domain tables (e.g., `CV3AllergyConfLevel`) but valid values are not listed.
- **Version mismatch**: Documentation is for version 22.1 (with patch releases through PR38), but the certified product is version 25.1. The schema may have changed between 22.1 and 25.1.
- **No format specification**: The documentation describes the schema but does not specify the actual export file format (CSV? SQL dump? Flat file?).

**Could a developer build an import?** Partially. The column-level documentation is detailed enough to understand the meaning of each field, and the data types are fully specified. However, the lack of explicit FK relationships (requiring inference from naming conventions and column definitions), the absence of value set documentation, and the missing export format specification would make reconstruction challenging without Altera support. A developer would need significant domain expertise to navigate 2,747 tables.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is one of the most comprehensive (b)(10) implementations encountered. The export covers **2,747 tables across clinical, financial, imaging, and administrative domains**. The 917 revenue cycle/billing tables (13,105 columns) alone demonstrate that this goes far beyond USCDI or any clinical summary export. The export includes:
- Deep clinical data (386 core CV3 tables with 8,871 columns)
- Extensive billing/revenue cycle data (917 tables — the single largest domain)
- Surgery/perioperative (146 tables)
- Medication management (163 tables)
- Ambulatory care workflows (348 tables)
- Scheduling, immunizations, imaging, and clinical documentation

The only areas where coverage appears thin relative to the product's capabilities are patient portal data (CarePath), explicit care plan structures, and advance directives — these are relatively minor gaps given the overall breadth.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. Key indicators:
1. The export is a **native database schema dump** — not FHIR, not C-CDA, not any standard clinical exchange format.
2. It covers **917 billing/revenue cycle tables** — data that no FHIR API or C-CDA export would include.
3. It includes **4 database schemas** (SCM, FS, IMG, MNC) covering the full breadth of the Sunrise platform.
4. The documentation explicitly labels it as "170.315 (b)(10) EHI Export" and is completely separate from the product's FHIR API or C-CDA capabilities.
5. The FS schema was created specifically for EHI export (its only table is `SXAEHISXAIMGBinaryObject_Blob`, described as "specifically for EHI export").
6. The documentation has evolved through 5 releases, showing ongoing investment beyond a compliance checkbox.

### Key Findings

1. **Exceptionally deep billing data**: 917 revenue cycle tables (33% of all tables) make this one of the richest billing exports seen. This includes claims, charges, payments, denials, appeals, fee schedules, payer configurations, and EDI transactions — data that most vendors omit entirely.

2. **100% documentation coverage**: Every one of 42,849 columns has a meaningful business description, and every table has a definition. This is extremely rare — most vendors document column names and types but leave descriptions blank or sparse.

3. **Native database schema approach**: The vendor documents their actual SQL Server schema rather than projecting into a standard format. This provides maximum transparency about what data exists, at the cost of requiring significant domain expertise to navigate.

4. **Active version maintenance**: 5 releases over 18 months, with expanding scope (adding FS, IMG, and MNC schemas in PR38), demonstrates genuine ongoing investment in the export.

5. **Procedural gaps**: Despite excellent schema documentation, there are no export execution instructions, no sample data, no format specification, and no value set documentation. A patient or provider requesting their data would still need Altera's cooperation to actually obtain and interpret it.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   SQL Server database schema (native)
    Entities:        2,747 tables (across 4 schemas)
    Fields:          42,849
    Descriptions:    100% (all fields have meaningful descriptions)
    Sample data:     No
    Bulk export:     Unclear (no export procedure documented)
    Domains covered: 17 of 19 applicable domains (care plans and portal data are thin)

### Bottom Line

Sunrise's EHI export is among the most comprehensive (b)(10) implementations available, documenting 2,747 database tables with 42,849 fully-described columns spanning clinical, financial, surgical, pharmaceutical, and administrative domains. The 917-table billing/revenue cycle coverage is particularly notable — a domain most vendors omit. The primary weakness is operational: despite excellent schema documentation, there are no export execution instructions, sample data, or format specifications, leaving a gap between what is documented and what a patient could actually obtain.
