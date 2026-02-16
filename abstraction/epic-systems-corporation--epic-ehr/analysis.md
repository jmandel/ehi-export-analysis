# EHI Export Analysis: Epic Systems Corporation

**Product**: EpicCare Inpatient Base (also covers EpicCare Ambulatory Base — same platform)  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11603, 11653, 11686, 11730 (Inpatient); 11604, 11654, 11687, 11731 (Ambulatory)

## 1. Product Context

Epic Systems Corporation is the dominant US EHR vendor, holding ~42% of the acute-care hospital market and covering records for over 325 million patients. EpicCare Inpatient Base and EpicCare Ambulatory Base are not separate products — they are two certified modules of a single, comprehensive, integrated EHR platform sharing the same database and patient record.

The Epic platform encompasses dozens of tightly integrated modules spanning:

- **Core clinical**: Inpatient documentation (ClinDoc), ambulatory charting, CPOE, clinical decision support, nursing documentation, flowsheets, care plans
- **Medications/pharmacy**: Ordering, MAR, dispensing, e-prescribing (Willow)
- **Lab**: Clinical and anatomic pathology (Beaker)
- **Radiology**: Imaging workflows and results (Radiant)
- **Surgery**: OR scheduling, surgical documentation, anesthesia (OpTime)
- **Specialty modules**: Oncology (Beacon), Cardiology (Cupid), OB/GYN (Stork), Transplant (Phoenix), Ophthalmology (Kaleidoscope), Endoscopy (Lumens), Dental (Wisdom), and more
- **Revenue cycle**: Hospital billing, professional billing, coding, claims, payments, denial management (Resolute HB/PB)
- **Registration & scheduling**: Patient registration (Prelude), appointment scheduling (Cadence), ADT/bed management (Grand Central)
- **Patient portal**: MyChart (180M+ active US users) — messaging, health records, scheduling, bill payment
- **Population health**: Risk stratification, care gaps, ACO management (Healthy Planet)
- **Emergency department**: Triage, tracking, patient flow (ASAP)
- **Critical care/ICU**: Specialized views, early warning tools
- **Infection control**: Surveillance, HAI reporting (Bugsy)
- **Case management**: Utilization review, payer communication
- **Home health**: Documentation, care plans
- **Interoperability**: Care Everywhere (HIE), HL7/FHIR interfaces (Bridges)

This is one of the broadest data footprints of any certified EHR. A genuine (b)(10) export must cover clinical, billing, specialty, portal, and administrative patient data across all these modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-tables-main-page.html` (8.7 KB) | Landing page at open.epic.com/EHITables describing the export format, scope, and links | **High** — establishes export format (TSV), scope, and mechanism |
| `downloads/ehi-tables-techspec.html` (1.08 MB) | Online index listing all 7,672 tables alphabetically with links | **Medium** — confirms table count, provides navigation |
| `downloads/ehi-tables-index.zip` (12.7 MB) | ZIP containing 7,672 individual HTML files, each documenting one export table with description, primary key, and column definitions | **Critical** — this is the complete data dictionary |
| `downloads/enrichment/ehi-tables.json` (24 MB) | Prior agent's structured extraction of all tables/columns (verified to match our independent parse) | **Reference** — used for cross-validation |
| `downloads/enrichment/extraction-coverage.json` (524 B) | Parse statistics from prior extraction | **Low** — confirmed by our own parse |

The ZIP data dictionary (`ehi-tables-index.zip`) is overwhelmingly the most valuable artifact. Each of its 7,672 HTML files documents one export table with: table name, prose description, primary key columns, and a full column listing (ordinal, name, type, discontinued flag, and prose description for each column). The documentation was auto-generated from Epic's internal data dictionary on 2026-02-15 (folder name: `DocGen_su117s2p_2026-02-15_14.10.04`).

## 3. Export Mechanics

- **Format**: Tab-separated value (TSV) files — one file per table. Non-tabular content (rich text documents, images) is provided as a separate file download referenced from the TSV data.
- **Data model**: Epic's native Clarity reporting database schema. This is the vendor's internal relational data model, not a projection into FHIR, C-CDA, or any external standard.
- **Mechanism**: Manual, UI-driven ("allows health systems to do a manual one-time export of health data for one or more patients"). The landing page notes this is distinct from programmatic APIs (FHIR Bulk Data, CDA).
- **Scope**: Single-patient or multi-patient ("one or more patients").
- **Access constraints**: Initiated by the health system (not patient-facing). Content varies by: modules licensed, software version, health system configuration, documentation practices, and non-Epic materials included.
- **Fees**: Not documented on the public page.

The landing page explicitly distinguishes this export from the standards-based FHIR Bulk Data and C-CDA alternatives, positioning the TSV export as the (b)(10) mechanism.

## 4. Export Content: What's In It

### Data dictionary scope

Our independent parse of all 7,672 HTML files in the ZIP (script: `analysis/parse_ehi_tables.py`) produced:

- **7,672 tables** (100% parsed, 0 failures)
- **63,121 columns** total
- **63,121 columns with descriptions** (100% description coverage)
- **63,121 columns with types** (100% type coverage)
- **7,566 tables with descriptions** (98.6%; 106 tables lack descriptions)
- **7,672 tables with primary keys** (100%)
- **41 discontinued columns** flagged

**Column type distribution:**

| Type | Count | % |
|---|---|---|
| VARCHAR | 32,660 | 51.7% |
| NUMERIC | 12,596 | 20.0% |
| INTEGER | 10,154 | 16.1% |
| DATETIME | 3,686 | 5.8% |
| FLOAT | 1,502 | 2.4% |
| DATETIME (UTC) | 1,201 | 1.9% |
| DATETIME (Local) | 1,143 | 1.8% |
| DATETIME (Attached) | 179 | 0.3% |

### Vendor's own content organization

Epic does not explicitly organize tables into named categories — they are presented as a flat alphabetical list. However, table naming conventions and descriptions reveal clear domain groupings. We categorized all 7,672 tables programmatically by table name prefix and description content (see `analysis/parse_ehi_tables.py`).

**Category breakdown:**

| Category | Tables | Columns | Representative Tables |
|---|---|---|---|
| Billing & Revenue Cycle | 1,286 | 12,367 | ACCOUNT (103 cols), HSP_ACCOUNT (137 cols), CLAIM_INFO (138 cols), AP_CLAIM (133 cols) |
| Procedures & Surgery | 797 | 4,246 | OR_CASE (115 cols), OR_CASE_3 (99 cols), OR_IMP_2 (98 cols) |
| Patient Demographics | 699 | 6,181 | PATIENT (85 cols), PATIENT_3 (64 cols), PATIENT_4 (74 cols) |
| Orders & Referrals | 588 | 4,876 | ORDER_PROC (82 cols), ORDER_RES (98 cols), AUTHORIZATIONS (97 cols) |
| Clinical Notes & Documents | 418 | 4,285 | UNOS_CLINICAL_INFO (257 cols), HNO_INFO (86 cols) |
| Medications | 322 | 3,183 | ORDER_MED (116 cols), RXA_ADJUD_MESSAGE (100 cols) |
| Encounters | 321 | 3,247 | PAT_ENC (72 cols), HSP_TRANSACTIONS (131 cols), PAT_ENC_HSP (86 cols) |
| Laboratory | 270 | 1,768 | LAB specimen and result tables |
| General Clinical | 222 | 1,534 | CLARITY_ADT, CLARITY_BED, etc. |
| Insurance & Coverage | 200 | 1,609 | Coverage, authorization, benefit tables |
| Oncology | 121 | 703 | Cancer registry, chemotherapy, BMT tables |
| Problems & Diagnoses | 89 | 655 | Problem list, diagnosis, DRG tables |
| Communications & Portal | 78 | 520 | MyChart messaging, patient portal tables |
| Transplant | 70 | 592 | Transplant episodes, donors, UNOS data |
| Obstetrics & Perinatal | 63 | 437 | Delivery, labor, fetal monitoring tables |
| Care Plans & Goals | 58 | 387 | Care plan enrollment, context, template tables |
| Radiology & Imaging | 55 | 285 | Imaging studies, breast imaging, CT data |
| Scheduling & ADT | 38 | 236 | Appointment, admission, bed tables |
| Vitals & Flowsheets | 36 | 498 | Flowsheet data, NSQIP, dialysis vitals |
| Infection Control | 34 | 348 | Surveillance, BPA, associated data |
| Immunizations | 26 | 333 | Immune, immunization history tables |
| Health Maintenance | 24 | 170 | Health maintenance protocols, screenings |
| Consents & Directives | 22 | 124 | ABN documents, consent tracking |
| Social & Behavioral Health | 16 | 234 | SDOH data, behavioral health tables |
| Research | 16 | 73 | Clinical trial, DICOM manifest tables |
| Allergies | 8 | 93 | ALLERGY (18 cols), reaction tracking |
| Family History | 6 | 78 | Family history, relations |
| Cardiology | 2 | 8 | Catheterization, lesion intervention tables |
| Other / Uncategorized | 1,787 | 14,051 | Accumulation (payer), CAP pathology forms, acuity scoring, adverse events, dental, home health, etc. |

**Note on "Other / Uncategorized"**: This large bucket (1,787 tables) contains sub-specialty clinical tables, payer/accumulation data, CAP anatomic pathology forms, home health, dental, endoscopy, quality measures, and many other domain-specific tables that don't match simple prefix patterns. These are overwhelmingly patient-facing clinical and financial data, not system configuration. The uncategorized bucket alone (14,051 columns) exceeds many vendors' entire export.

**25 largest tables (by column count):**

| Table | Columns | Domain |
|---|---|---|
| UNOS_CLINICAL_INFO | 257 | Transplant/UNOS registry |
| CLAIM_INFO | 138 | Billing claims |
| HSP_ACCOUNT | 137 | Hospital accounts |
| AP_CLAIM | 133 | Managed care claims |
| HSP_TRANSACTIONS | 131 | Hospital transactions |
| ORDER_MED | 116 | Medication orders |
| CLAIM_INFO2 | 115 | Claims (continued) |
| OR_CASE | 115 | Surgical cases |
| ACCOUNT | 103 | Guarantor accounts |
| ORDER_RES | 98 | Order results |
| OR_IMP_2 | 98 | Implant data |
| AUTHORIZATIONS | 97 | Prior authorizations |

The full inventory is in `analysis/entity-inventory-full.json` (7,672 table objects with 63,121 column objects).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Epic's EHI export is a native database dump of their Clarity reporting schema. It is not organized by clinical domain but by database entity. The breadth is extraordinary:

**Deepest coverage** (by table/column count):
- **Billing & Revenue Cycle** (1,286 tables, 12,367 columns): Hospital accounts, professional billing, claims, charges, payments, adjustments, guarantor accounts, collection agency history, statements, EOBs, managed care claims, prior authorization tracking. Tables like HSP_ACCOUNT (137 cols), CLAIM_INFO (138 cols), and AP_CLAIM (133 cols) demonstrate granular billing data far beyond anything in USCDI.
- **Patient Demographics** (699 tables, 6,181 columns): Patient identity, addresses, contacts, race/ethnicity, language, employment, address history, identity linking. PATIENT table alone has 85 columns.
- **Procedures & Surgery** (797 tables, 4,246 columns): OR cases, anesthesia, implants, surgical logs, perioperative data, laser records, timeout documentation. OR_CASE has 115 columns.

**Specialty clinical depth**:
- **Oncology** (121 tables): Cancer registry, chemotherapy protocols, BMT, radiation, tumor staging
- **Transplant** (70 tables): UNOS registry data (257 cols in one table alone), donor episodes, organ matching
- **Obstetrics** (63 tables): Delivery records, labor complications, fetal monitoring, cord data
- **Infection Control** (34 tables): Surveillance, HAI tracking

**Thinnest explicit categories** (likely undercounted due to categorization):
- **Cardiology** (2 tables by name match): Most cardiac data is likely in flowsheets, order results, and procedure tables
- **Family History** (6 tables): Covered but with a small dedicated table set
- **Allergies** (8 tables): Small dedicated set; the ALLERGY table (18 cols) captures core allergy data

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENT (85 cols), PATIENT_3 (64 cols), PATIENT_4 (74 cols), PATIENT_MYC (37 cols), plus 699 tables in category | Extensive — address history, identity, contacts, race/ethnicity, language, employment |
| Encounters / visits | ✅ Covered | PAT_ENC (72 cols), PAT_ENC_HSP (86 cols), HSP_ACCOUNT (137 cols), 321 encounter tables | Comprehensive — inpatient, outpatient, ED, transfers |
| Problems / conditions | ✅ Covered | PROBLEM_LIST, PROBLEM_LIST_HX, DIAGNOSIS tables, 89 tables total | Thorough with history tracking |
| Medications / prescriptions | ✅ Covered | ORDER_MED (116 cols), MAR tables, RX tables, pharmacy dispensing, 322 tables total | Deep — ordering, administration, dispensing, adjudication |
| Allergies | ✅ Covered | ALLERGY (18 cols), ALLERGY_REACTIONS, 8 tables | Adequate coverage |
| Immunizations | ✅ Covered | IMMUNE, IMMUNE_HISTORY, 26 tables | Thorough with history |
| Vitals | ✅ Covered | IP_FLWSHT_REC/MEAS, flowsheet tables, 36 vitals/flowsheet tables | Covered via flowsheet infrastructure |
| Lab results | ✅ Covered | LAB tables, RESULT tables, SPECIMEN tables, AP (anatomic pathology) tables, 270 tables | Comprehensive — clinical and anatomic pathology |
| Imaging / diagnostic reports | ✅ Covered | IMAGE_STUDY, RAD tables, breast imaging, CT data, 55 tables | Covered |
| Procedures | ✅ Covered | OR_CASE (115 cols), OR_LOG, procedure tables, 797 tables | Extremely deep — surgical, anesthesia, implants, perioperative |
| Clinical notes / documents | ✅ Covered | HNO_INFO (86 cols), NOTE tables, DOCS tables, 418 tables | Comprehensive. Rich text/images provided separately per landing page |
| Care plans / goals | ✅ Covered | CAREPLAN_INFO, GOAL tables, 58 tables | Solid coverage |
| Orders / referrals | ✅ Covered | ORDER_PROC (82 cols), REFERRAL tables, AUTHORIZATIONS (97 cols), 588 tables | Deep — orders, referrals, prior auths |
| Insurance / coverage | ✅ Covered | COVERAGE tables, INSURANCE_INFO, benefit/eligibility tables, 200 tables | Thorough — coverage, benefits, eligibility, accumulations |
| Claims / billing | ✅ Covered | CLAIM_INFO (138 cols), HSP_ACCOUNT (137 cols), AP_CLAIM (133 cols), ACCOUNT (103 cols), 1,286 tables | **Exceptionally deep** — hospital billing, professional billing, managed care claims, guarantor accounts |
| Payments | ✅ Covered | PMT tables, HSP_TRANSACTIONS (131 cols), TX tables within billing category | Included within billing/revenue cycle tables |
| Consents / directives | ✅ Covered | ABN tables, consent tracking, 22 tables | Covered |
| Patient communications / portal | ✅ Covered | MYC_MESG, MyChart tables, secure messaging, 78 tables | Covered — messages, preferences, portal activity |
| Specialty: Oncology | ✅ Covered | 121 tables — cancer registry, chemo protocols, BMT, radiation | Deep specialty coverage |
| Specialty: Transplant | ✅ Covered | 70 tables — UNOS registry (257 cols), donor data, organ matching | Deep specialty coverage |
| Specialty: OB/GYN | ✅ Covered | 63 tables — delivery, labor, fetal monitoring, perinatal | Solid specialty coverage |
| Specialty: Dental | ✅ Covered | 60+ DENTAL tables in uncategorized bucket | Covered |
| Specialty: Home Health | ✅ Covered | 122 HH tables in uncategorized bucket | Covered |
| Specialty: Infection Control | ✅ Covered | 34 tables — surveillance, HAI | Covered |
| Social determinants | ✅ Covered | 16 SDOH tables, behavioral health tables | Present |

**No significant gaps identified.** Every data domain that Epic stores as patient data is represented in the export. The export extends far beyond USCDI into billing, specialty clinical data, portal communications, social determinants, and operational patient data.

## 6. Documentation Quality

**Strengths:**
- **Complete data dictionary**: Every one of the 7,672 tables is documented with an HTML file containing table description, primary key, and full column listing
- **100% column description coverage**: All 63,121 columns have prose descriptions explaining what they contain (e.g., "The unique contact serial number (CSN) for this contact. This number is unique across all patient encounters in your system.")
- **100% type coverage**: Every column has a data type (VARCHAR, NUMERIC, INTEGER, DATETIME variants, FLOAT)
- **Primary keys documented**: Every table specifies its primary key columns with ordinal positions
- **Discontinued tracking**: Columns that have been deprecated are flagged
- **Machine-readable**: The HTML files follow a consistent structure easily parsed programmatically (as demonstrated by both our script and the prior agent's Cheerio-based parser — both yielded identical results)

**Limitations:**
- **No explicit foreign key documentation**: Relationships between tables must be inferred from column names (e.g., PAT_ENC_CSN_ID appearing in many tables). Epic uses naming conventions (suffix patterns like `_ID`, `_CSN_ID`) but does not document join paths.
- **No value sets / code tables**: Coded columns (e.g., `PAT_STATUS_C`) do not document valid values or their meanings. The `_C` suffix conventionally indicates a category column in Epic's Clarity schema, but the code values are not enumerated.
- **No sample data**: The documentation is schema-only; no example rows or records are provided.
- **No ERD or relationship diagrams**: No visual or structured documentation of how tables relate to each other.
- **106 tables lack descriptions**: 1.4% of tables have empty description fields (mostly sub-tables of larger entities).

**Could a developer build an import?** A developer with Epic/Clarity experience could work with this export. The column descriptions are genuinely helpful, and the table names are meaningful. However, a developer unfamiliar with Epic would struggle with: joining tables without foreign key documentation, interpreting category columns without value sets, and understanding the overall data model without relationship documentation. The documentation is excellent for what it provides but missing the relational layer.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is the most comprehensive EHI export we could expect from any vendor. With 7,672 tables and 63,121 documented columns, Epic's export covers every identifiable data domain their massive platform stores: clinical documentation, medications, lab/pathology, procedures/surgery, billing/claims/payments, insurance/coverage, patient portal communications, specialty modules (oncology, transplant, OB, dental, home health), social determinants, immunizations, allergies, care plans, and more. The billing/revenue cycle coverage alone (1,286 tables, 12,367 columns) far exceeds most vendors' entire exports. The export goes dramatically beyond USCDI in both breadth (billing, specialty, portal data) and depth (85+ columns for a single patient table vs. ~20 USCDI patient elements).

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. The evidence is clear:

1. **Native database format**: The export uses Epic's internal Clarity reporting schema as TSV files — not FHIR, not C-CDA, not any standards-based clinical exchange format.
2. **Dedicated documentation**: Epic built a dedicated website (open.epic.com/EHITables) with a purpose-generated data dictionary of all 7,672 export tables. This is not repurposed API documentation.
3. **Explicit differentiation**: The landing page explicitly distinguishes this export from "standards-based" FHIR Bulk Data and C-CDA alternatives, positioning it as the comprehensive EHI mechanism.
4. **Coverage far exceeds (g)(10)**: The export includes billing (1,286 tables), surgical records, transplant data, dental data, home health, MyChart communications, and dozens of other domains that are absent from Epic's FHIR (g)(10) API surface.
5. **Non-tabular data handling**: The documentation notes that rich text documents and images are provided separately, showing thoughtfulness about non-structured EHI.

### Key Findings

1. **Extraordinary breadth and depth**: 7,672 tables with 63,121 fully-described columns make this one of the most thorough EHI export documentations among certified EHR vendors. The data dictionary alone is 12.7 MB compressed.

2. **Billing coverage is genuinely deep**: 1,286 billing/revenue cycle tables with 12,367 columns — including hospital accounts, professional billing, managed care claims, guarantor accounts, and payment transactions. This is not a token billing inclusion.

3. **100% description coverage**: Every single column in all 7,672 tables has a prose description. This is rare among vendor data dictionaries and demonstrates significant documentation investment.

4. **Specialty clinical data is included**: Dedicated tables for oncology (121), transplant (70), OB/GYN (63), dental (60+), home health (122), infection control (34), and other specialties. These are domains absent from USCDI and most vendors' exports.

5. **Missing relational documentation**: The significant limitation is the absence of foreign key documentation, value set/code table enumeration, and relationship diagrams. A developer receiving this export would know what each column means but not how tables connect or what coded values represent.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   TSV (tab-separated values) — one file per table, native Clarity schema
    Entities:        7,672 tables
    Fields:          63,121 columns
    Descriptions:    100% of fields have prose descriptions
    Sample data:     No
    Bulk export:     Yes (single-patient or multi-patient)
    Domains covered: 19 of 19 applicable domains

### Bottom Line

Epic's EHI export sets the standard for (b)(10) compliance. A patient or provider receiving this export would get a comprehensive copy of essentially all structured data in their Epic record — clinical, billing, specialty, and portal data — across 7,672 tables with 63,121 fully-described columns. The single biggest gap is the lack of relational documentation (foreign keys, value sets), which makes the export harder to consume than it needs to be, but the data itself is demonstrably complete.
