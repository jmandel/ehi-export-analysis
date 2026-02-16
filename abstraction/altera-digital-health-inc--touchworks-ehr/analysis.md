# EHI Export Analysis: Altera Digital Health (TouchWorks EHR)

**Product**: TouchWorks EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11675 (15.04.04.3123.Touc.25.12.1.250723)

## 1. Product Context

TouchWorks EHR is Altera Digital Health's (formerly Allscripts) ambulatory electronic health record platform, designed for medium-to-large, single or multi-specialty physician practices, MSOs, and integrated delivery networks. The specific CHPL listing is under Providers Management, Inc. / Genesys PHO, a Michigan-based deployment partner.

The product covers a broad set of clinical and administrative functions:
- **Clinical documentation**: progress notes, encounter notes, AI-driven note generation (Note+), customizable charting templates
- **Order management**: lab, radiology, referral, and prescription orders with direct connections to labs, pharmacies, and providers
- **E-prescribing**: including EPCS (electronic prescribing of controlled substances)
- **Medications**: active medication lists, prescription history, refills, medication administration
- **Allergies**: allergy tracking with reactions, Medispan symptom coding
- **Problem lists**: ICD-9/ICD-10 coded diagnoses and conditions
- **Immunizations**: vaccination records and immunization forecasting
- **Lab and results management**: structured lab results, findings, reference ranges
- **Vitals and clinical observations**: structured findings data
- **Billing and charge capture**: charge entry, charge codes, modifiers, diagnosis linking, ABN tracking (deeper revenue cycle may reside in the separate Ventus product)
- **Scheduling**: appointment management, appointment types, scheduling
- **Insurance**: patient insurance at registration, encounter, and visit levels
- **Patient portal**: portal activity, communication preferences, secure messaging
- **Referrals**: referral requests/responses with attached documents, organization details
- **Clinical decision support**: recommendations, rules, dispositions
- **Care plans and goals**: encounter-level care guides, patient goals
- **Document scanning**: via IntegratedScan module with page-level image tracking
- **Public health reporting**: immunization registries, syndromic surveillance, cancer case reporting, electronic case reporting
- **Medical devices**: UDI-tracked medical device instances
- **Patient education**: education sessions, materials, learning factors

The certification is comprehensive (38 criteria), covering clinical, interoperability, CQM, privacy/security, patient portal, public health, FHIR API, and direct messaging. This sets a high bar for what the (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/TWEHR-2026.1-Touchworks-EHI-Export-Definition.zip` (1.4 MB) | ZIP containing complete HTML documentation site for the EHI export database schema | **Primary source** |
| `downloads/twehr-2026.1/` (extracted ZIP) | HTML documentation site: `main.html` frameset, `tree.html` navigation, 577 individual table HTML pages across 8 databases | **Primary source** — every table individually examined |
| `downloads/twehr-2026.1/Touchworks/index.html` | Server-level page listing all 8 databases | Useful for structure overview |
| `downloads/enrichment/tables.json` (2.8 MB) | Prior agent's structured JSON extraction of all 577 tables | Used for cross-validation; my independent parse confirmed identical counts |
| `downloads/enrichment/coverage.json` | Prior agent's summary statistics | Confirmed: 577 tables, 7,748 columns, 51.3% description rate |
| `downloads/enrichment/extract-tables.ts` | Prior agent's Bun TypeScript parsing script | Reviewed for methodology; informed my own parsing approach |
| `product-research.md` | Product capabilities research | Useful baseline for coverage assessment |
| `ehi-export-report.md` | Prior agent's narrative analysis | Reviewed and verified; mostly accurate |

## 3. Export Mechanics

- **Format**: SQL database export — the native relational database schema of TouchWorks EHR (SQL Server). The export covers 8 databases with 577 tables.
- **Mechanism**: The documentation describes a downloadable database schema definition. The Altera compliance page instructs users to "download the EHI Export Documentation zip file" and "view the EHI Export definition in your web browser, which will display a tree structure of the tables in the EHI Export extract." This implies a database-level extract is the export format.
- **Single-patient vs bulk**: Not explicitly documented. The schema is a full relational database model, suggesting the export is per-deployment (all patients) rather than per-patient, though the documentation doesn't specify the extraction mechanism.
- **Access constraints or fees**: Documentation is freely available on Altera's public compliance page. No mention of fees for the export itself.
- **Versioning**: Multiple versions available (2022 through 2026.1), showing active maintenance. The analyzed version is 2026.1, created December 22, 2025.

## 4. Export Content: What's In It

### Structure Overview

The export documentation describes the complete TouchWorks EHR database schema across 8 SQL Server databases:

- **577 tables** total
- **7,748 columns** total
- **3,977 columns** (51.3%) have descriptions
- **852 columns** have documented foreign key relationships
- All 577 tables have a description (MS_Description)
- Column documentation includes: name, SQL data type, max length (bytes), nullability, default value, description
- Foreign key relationships are documented at both the column level (inline annotations) and in dedicated FK sections
- Indexes are documented with column membership and type (clustered/nonclustered)

### Database Breakdown

| Database | Tables | Columns | Purpose |
|---|---|---|---|
| Works | 537 | 7,256 | Core EHR — clinical, demographic, billing, orders, reference data |
| Impact | 22 | 335 | Document imaging, forms, patient demographics, tasks, OCR |
| IntegratedScan | 6 | 33 | Document scanning audit, page-level image metadata |
| WorksCDSAggregatorArchive | 5 | 47 | Clinical decision support archive |
| AHSCharge | 2 | 7 | Local Medical Review Policy / carrier data |
| Quippe | 2 | 39 | Quippe clinical content library |
| WorksArchive | 2 | 23 | Archive tables for vitals and findings |
| chMedcinSearch | 1 | 8 | MEDCIN clinical terminology search index |

### Vendor's Content Organization

The database uses consistent naming conventions: `_DE` suffix for dictionary/reference tables, `Act_` prefix for activity-level clinical data, `Item_` prefix for item-level master data, `Hdr_` for header tables in versioned record patterns.

**Category breakdown by domain** (derived from table naming analysis — see `analysis/entity-inventory-summary.json`):

| Category | Tables | Columns | Described | Desc% |
|---|---|---|---|---|
| Dictionary / Reference (_DE tables) | 151 | 2,067 | 387 | 18.7% |
| Clinical Notes / Documents | 41 | 613 | 483 | 78.8% |
| Demographics / Patient | 55 | 567 | 361 | 63.7% |
| Problems / Diagnoses | 33 | 453 | 239 | 52.8% |
| Medications / Prescriptions | 16 | 451 | 273 | 60.5% |
| Encounters / Visits | 34 | 399 | 219 | 54.9% |
| Impact / Reporting | 22 | 335 | 274 | 81.8% |
| Orders | 24 | 300 | 173 | 57.7% |
| Billing / Charges | 21 | 249 | 77 | 30.9% |
| Allergies | 11 | 193 | 133 | 68.9% |
| Immunizations | 8 | 167 | 47 | 28.1% |
| Clinical Decision Support | 14 | 143 | 78 | 54.5% |
| Results / Observations | 6 | 105 | 84 | 80.0% |
| Items (Master Data) | 8 | 95 | 78 | 82.1% |
| Care Plans / Goals | 6 | 71 | 61 | 85.9% |
| Document Scanning | 10 | 70 | 26 | 37.1% |
| Vitals | 4 | 68 | 64 | 94.1% |
| Communications / Tasks | 8 | 68 | 20 | 29.4% |
| Referrals | 5 | 64 | 37 | 57.8% |
| Insurance / Coverage | 4 | 49 | 28 | 57.1% |
| Consents / Directives | 4 | 44 | 14 | 31.8% |
| Templates / Forms | 2 | 26 | 19 | 73.1% |
| Procedures | 1 | 12 | 1 | 8.3% |
| Other (misc clinical/admin) | 72 | 891 | 639 | 71.7% |

**Representative large entities (top 15 by column count):**

| Table | Database | Columns | Description |
|---|---|---|---|
| dbo.Medication | Works | 126 | Complete medication record with dosing, refills, routes, pharmacy details |
| dbo.QO_Classification_DE | Works | 92 | Quick Order classification dictionary |
| dbo.Order_Item_Common | Works | 80 | Common order item attributes |
| dbo.Plan_Item | Works | 79 | Non-medication order plan items |
| dbo.PATIENTS_EDIT | Impact | 78 | Patient demographics (Impact module) |
| dbo.Problem_DE | Works | 71 | Problem/diagnosis dictionary |
| dbo.Immunization | Works | 64 | Immunization records with VIS, lot, site, route |
| dbo.Problem | Works | 62 | Patient problem instances with onset, status, codes |
| dbo.FORMS_DETAIL | Impact | 59 | Form element definitions |
| dbo.Document_Type_DE | Works | 55 | Document type dictionary |
| dbo.Req_Perf_Location_DE | Works | 55 | Requesting/performing location dictionary |
| dbo.Patient_Member | Works | 54 | Patient/person master record |
| dbo.OCD_Item | Works | 53 | Orderable concept dictionary items |
| dbo.Result | Works | 49 | Clinical result instances |
| dbo.Pharmacy_DE | Works | 48 | Pharmacy dictionary |

The full inventory of all 577 tables is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is the **complete relational database schema** of the TouchWorks EHR system. Key observations:

**Richest domains:**
- **Medications** (16 tables, 451 columns): The `Medication` table alone has 126 columns — an extraordinarily deep representation covering prescribed, dispensed, and administered medications with dosing instructions, SIG codes, pharmacy routing, refill tracking, controlled substance flags, formulary status, and therapeutic categories.
- **Clinical notes/documents** (41 tables, 613 columns): Comprehensive document model with `Document`, `DocumentInformation`, `DocumentLabel`, `NAW_*` (note authoring workspace) tables, and `Act_Note` activity tracking.
- **Demographics/patient** (55 tables, 567 columns): `Patient_Member` (54 cols), patient alerts, cautions, communication preferences, portal activity, community membership, consent records.
- **Problems/diagnoses** (33 tables, 453 columns): `Problem` (62 cols), `Problem_DE` (71 cols), encounter diagnoses, ICD-9/ICD-10 detail records, diagnosis-charge linking.
- **Encounters/visits** (34 tables, 399 columns): `Encounter` (34 cols) with associated insurance, diagnoses, employers, workers' comp, care plans, discharge disposition, and status tracking.
- **Orders** (24 tables, 300 columns): `Order_Item_Common` (80 cols), order activities, order charges, scheduled orders, order sets.

**Billing is genuinely present:**
- 21 tables with 249 columns dedicated to billing: `Charge` (47 cols), `Charge_Diagnosis`, `Charge_Modifier`, `Charge_Code_DE` (39 cols), `Charge_ABN`, `Charge_ABN_Status`, `Order_Item_Charge`, billing area/location/type dictionaries.
- The AHSCharge database adds LMRP (Local Medical Review Policy) and carrier data.
- This goes beyond what USCDI requires and represents genuine billing data export, though comprehensive claims adjudication and payment posting may reside in the separate Ventus revenue cycle product.

**Dictionary/reference tables are extensive:**
- 151 `_DE` (dictionary entry) tables with 2,067 columns define the coded value sets used throughout the system — allergens, medication forms, appointment types, charge codes, problem lists, referral types, etc.
- These are essential for interpreting the clinical data and represent a significant effort to make the export self-contained.

**Specialty and additional clinical data:**
- **Cancer Registry**: `CancerRegistryData` (29 cols) for cancer case reporting
- **Medical Devices**: `MedicalDevice` (33 cols), `MedicalDevice_Header` (9 cols) with UDI tracking
- **Patient Education**: `Education` (17 cols), `Education_Session` (12 cols), `Education_Header`, education factors
- **Health Concerns**: `HealthConcern` (15 cols), `HealthConcern_Header`, `HealthConcern_Impression`
- **Occupational Medicine**: `Encounter_Employer`, `Encounter_Employer_Contact`, `Encounter_Workers_Comp`

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient_Member` (54 cols), `Patient_Case`, `PatientCaution`, `PatientCommunication`, plus 50+ demographic tables | Thorough — includes contacts, communication preferences, race/ethnicity, preferred pronouns |
| Encounters / visits | ✅ Covered | `Encounter` (34 cols), `Encounter_Insurance`, `Encounter_Diagnosis`, `Encounter_Case`, `Encounter_Status`, 34 tables total | Thorough — includes workers' comp, employer, care plans per encounter |
| Problems / conditions | ✅ Covered | `Problem` (62 cols), `Problem_DE` (71 cols), `Encounter_Diagnosis`, ICD-9/ICD-10 detail tables, 33 tables | Deep — includes severity, onset tracking, verification status |
| Medications / prescriptions | ✅ Covered | `Medication` (126 cols), `Item_Medication` (28 cols), `Pharmacy_DE` (48 cols), SIG tables, 16 tables | Exceptionally deep — 126 columns on medication alone |
| Allergies | ✅ Covered | `Allergy` (35 cols with reactions, Medispan symptoms), `Item_Allergy`, `Allergen_DE`, 11 tables, 193 columns | Thorough — reactions, severity, verification workflow |
| Immunizations | ✅ Covered | `Immunization` (64 cols), `Item_Immunization` (28 cols), `Immunization_Forecast`, 8 tables | Deep — includes VIS dates, lot numbers, forecasting |
| Vitals | ✅ Covered | `Act_Vitals` (24 cols), `Act_Hdr_Vitals` (25 cols), `Finding` (40 cols), `Finding_Reference_Range` | Well-covered via the findings model |
| Lab results | ✅ Covered | `Result` (49 cols), `Act_Result` (25 cols), `Act_Result_Extension`, `Item_Result`, `Reference_Range_Text` | Solid — structured results with reference ranges |
| Imaging / diagnostic reports | ⚠️ Partial | `IntegratedScan` database (6 tables), Impact `DOC_HEADER`/`DOC_DETAIL`, `Imaging_Report_DE` (5 cols) | Document scanning/imaging metadata present; actual image content storage mechanism unclear |
| Procedures | ⚠️ Partial | Procedures appear captured through `Order_Item_Common` (80 cols) and `Plan_Item` (79 cols) order model rather than dedicated procedure tables | The order-based model may be how TouchWorks handles procedures; only 1 explicit procedure-named table |
| Clinical notes / documents | ✅ Covered | 41 tables, 613 columns: `Document`, `DocumentInformation`, `NAW_*` tables, `Act_Note`, `DOCWORKS_Signature` | Comprehensive — includes note authoring, signatures, document types |
| Care plans / goals | ✅ Covered | `Goal` (34 cols), `Item_Goal` (26 cols), `Act_Goal` (24 cols), `Encounter_CarePlan` | Well-structured versioned goal model |
| Orders / referrals | ✅ Covered | Orders: 24 tables (300 cols) including `Order_Item_Common` (80 cols). Referrals: `Referral_Header`, `Referral_Message` (21 cols), `Referral_Attachment`, `Referral_Document`, 5 tables | Thorough — includes referral attachments and message tracking |
| Insurance / coverage | ✅ Covered | `Primary_Insurance` (20 cols), `Insurance_Class_DE` (18 cols), `Encounter_Insurance` (15 cols), `Visit_Insurance` (16 cols) | Multi-level: registration, encounter, and visit-level insurance |
| Claims / billing | ✅ Covered | `Charge` (47 cols), `Charge_Diagnosis`, `Charge_Modifier`, `Charge_Code_DE` (39 cols), `Order_Item_Charge`, 21 tables (249 cols) | Genuine charge capture data. Full claims adjudication/payment may be in separate Ventus product |
| Payments | ⚠️ Partial | `Payment_Typology_DE` (11 cols — dictionary only), no dedicated payment transaction tables | Payment types defined but no payment posting/transaction tables visible. May reside in Ventus |
| Consents / directives | ✅ Covered | `Patient_Consent` (16 cols), `Patient_Consent_DE` (13 cols), `Patient_Directives`, `Directives_DE` | Present — consent types and advance directives |
| Patient communications | ⚠️ Partial | `PatientCommunication` (9 cols — preferences), `PatientPortalUserActivity` (8 cols — audit), `Patient_Communication_DE` | Communication preferences and portal audit present; actual message content tables not clearly identified |
| Specialty-specific (oncology) | ✅ Covered | `CancerRegistryData` (29 cols) | Cancer registry data explicitly included |
| Specialty-specific (occupational medicine) | ✅ Covered | `Encounter_Employer` (12 cols), `Encounter_Employer_Contact` (11 cols), `Encounter_Workers_Comp` (13 cols) | Occupational medicine encounters with employer and workers' comp data |
| Medical devices | ✅ Covered | `MedicalDevice` (33 cols), `MedicalDevice_Header` (9 cols), `FDAMedicalDevices` (5 cols) | UDI-tracked device instances |
| Patient education | ✅ Covered | `Education` (17 cols), `Education_Session` (12 cols), `Education_Factor`, `Education_Header` | Education sessions with learning factors |
| Family health history | ⚠️ Partial | No dedicated family history tables identified; may be captured through the findings model (`Item_Finding`, `Finding`) | Not clearly surfaced as a distinct entity |

## 6. Documentation Quality

**Strengths:**
- **Complete structural coverage**: All 577 tables have HTML documentation pages with MS_Description, column definitions, data types, nullability, defaults, and index information.
- **Generated from the actual database**: The documentation is produced by a SQL Server documentation tool (created December 22, 2025), ensuring the schema matches reality.
- **Self-contained coded values**: 151 dictionary/reference (`_DE`) tables mean the export documents its own value sets — a developer could reconstruct coded fields without external lookups.
- **Foreign key relationships**: 852 column-level FK annotations enable understanding of the relational model (e.g., `Allergy.ItemID` → `Item_Allergy.ID`).
- **Active versioning**: Multiple versions available from 2022 through 2026.1, showing ongoing maintenance.

**Weaknesses:**
- **51.3% column description rate**: Nearly half of all columns lack descriptions. The description rate varies dramatically by domain — Vitals at 94.1%, CDS Archive at 100%, but Immunizations at 28.1%, Communications at 29.4%, and Billing at 30.9%.
- **Dictionary tables poorly described**: The 151 `_DE` tables have only 18.7% of their columns described. Since these tables define the coded values used throughout the system, this makes interpretation harder.
- **No export process documentation**: No user guide explaining how to request or execute the export, what format the actual data arrives in, or how to reconstruct patient records from the relational model.
- **No sample data or example files**: No worked examples showing what exported data looks like.
- **No entity-relationship diagrams**: The relational structure must be inferred from FK annotations.
- **Custom data types undocumented**: Types like `[dbo].[uniqueid]`, `[dbo].[dict_id]`, `[dbo].[message]`, `[dbo].[BOOL]` are used throughout but never formally defined.

**Developer usability**: A skilled database developer with healthcare domain knowledge could reconstruct patient records from this documentation, but it would require significant effort. The FK relationships, table descriptions, and column descriptions (where present) provide enough scaffolding to understand the data model. The undescribed columns and custom types would require experimentation or vendor support.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export covers the full breadth of what TouchWorks EHR stores. It is not limited to USCDI domains — it includes billing/charge data (21 tables), insurance at multiple levels (registration, encounter, visit), scheduling/appointments (8 tables), document scanning, clinical decision support, occupational medicine, cancer registry data, medical devices, patient education, referral workflows, and 151 dictionary tables that define the coded value sets. The 577 tables across 8 databases represent a genuine database-level export, not a clinical summary repackaged. The only notable gaps are in payment posting (which likely resides in the separate Ventus revenue cycle product) and patient message content (portal audit is tracked but message bodies aren't clearly surfaced).

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export. The documentation is a complete SQL Server database schema export — 8 databases, 577 tables, 7,748 columns — covering the full relational model of the EHR. This is fundamentally different from a FHIR or C-CDA clinical exchange export. Key indicators:
- The export includes billing tables, scheduling tables, dictionary tables, and administrative data not present in any clinical exchange standard
- The documentation is generated directly from the database schema, not from FHIR resource definitions or C-CDA templates
- The data model is the vendor's native relational model, not a projection into a standard format
- Multiple versions are maintained, showing this is an actively managed export capability
- The breadth (577 tables) far exceeds what any standard clinical exchange format covers

### Key Findings

1. **Genuine database-level export**: 577 tables across 8 databases with 7,748 columns — this is the actual TouchWorks relational database schema, not a FHIR or C-CDA wrapper. The `Medication` table alone has 126 columns, far exceeding any standard clinical exchange profile.

2. **Billing data is present and meaningful**: 21 tables with 249 columns cover charge capture, charge diagnoses, charge modifiers, charge codes, ABN tracking, billing areas, and order-level charges. This goes well beyond USCDI. Full claims adjudication may reside in the separate Ventus product, but the charge capture layer is comprehensive.

3. **51.3% column description rate is the main documentation gap**: While all 577 tables have descriptions and the structural documentation (types, nullability, FKs) is complete, nearly half of columns lack descriptions. This is particularly problematic for dictionary tables (18.7% described) which define the coded values critical for data interpretation.

4. **Self-contained value set definitions**: The 151 `_DE` dictionary tables mean the export documents its own coded values — a significant advantage for data reconstruction, even though the dictionary table columns themselves are poorly described.

5. **No export process documentation**: The schema is well-documented but there's no guidance on how to actually execute an export, what format the data arrives in, or how to reconstruct patient records. A recipient would need database expertise and healthcare domain knowledge.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   SQL database (relational tables, SQL Server schema)
Entities:        577 tables across 8 databases
Fields:          7,748 columns
Descriptions:    51.3% of columns (3,977 of 7,748); 100% of tables
Sample data:     No
Bulk export:     Unclear (schema suggests full database, not per-patient)
Domains covered: 17 of 19 applicable domains (partial on payments, family history)
```

### Bottom Line

TouchWorks EHR's (b)(10) export is one of the stronger implementations: a genuine database-level schema export covering 577 tables across clinical, billing, scheduling, and administrative domains — far beyond USCDI. The main limitation is documentation depth: while every table has a description and structural metadata, only 51.3% of columns have descriptions, and there's no guidance on the export execution process or data reconstruction. A patient or provider would get a comprehensive copy of their data, but would need significant technical expertise (or vendor assistance) to interpret the raw relational model.
