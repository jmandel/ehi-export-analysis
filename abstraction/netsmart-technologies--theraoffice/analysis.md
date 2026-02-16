# EHI Export Analysis: Netsmart Technologies

**Product**: TheraOffice v14.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2816.Ther.14.00.1.240628

## 1. Product Context

TheraOffice is a specialty EMR and practice management platform designed for outpatient physical therapy, occupational therapy, and speech-language pathology practices. It is an all-in-one system combining clinical documentation, scheduling, billing/revenue cycle management, and reporting. It was acquired by Netsmart Technologies in April 2022.

Key capabilities relevant to EHI completeness:
- **Clinical documentation**: 40+ customizable templates for evaluations, daily notes, progress notes, treatment plans, and discharge summaries across PT, OT, SLP, and specialty areas (pelvic health, vestibular, lymphedema, pediatric)
- **Scheduling**: Appointment management, recurring appointments, waitlists, online patient scheduling
- **Billing & Revenue Cycle**: Fully integrated — claims processing, ERA downloads, denial tracking, payment posting, collections, fee schedules, TheraOffice Pay card processing
- **Patient portal**: Digital intake, messaging, online payments, appointment booking, record access
- **E-prescribing**: Electronic prescriptions including controlled substances (EPCS)
- **Telehealth**: Built-in virtual visits integrated with documentation and billing
- **Outcome measures**: Standardized assessment tools (LEFS, DASH, NDI, Oswestry, etc.)
- **Referral management**: Electronic referral tracking
- **Document management**: Inbound/outbound e-faxing, scanned documents

The product is used by 900+ rehabilitation practices and was certified on June 28, 2024 (Drummond Group). The breadth of its billing, clinical documentation, and specialty features sets the baseline for what a complete (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi_tables/EHI Export All Tables - May 2024 (TheraOffice).pdf` | 30-page PDF data dictionary documenting 19 tables and 526 columns. Primary artifact. | **Most informative** — the entire data dictionary |
| `downloads/ehi_export_all_tables_theraoffice_2024.zip` | ZIP archive containing the PDF above (407 KB) | Container only |
| `downloads/theraoffice-mandatory-disclosures-statement_v4.pdf` | 5-page mandatory disclosures letter (July 2025). Lists certified criteria and costs — (b)(10) included in subscription, no additional fee. | Confirms no extra cost for EHI export |
| `downloads/ehi-page-screenshot-full.png` | Full-page screenshot of the vendor's EHI export page | Confirms manual one-time export mechanism, notes that "some electronic health information might not be available in a table format, such as rich text documents or images" |
| `downloads/enrichment/tables-catalog.json` | Prior automated extraction of the PDF (19 tables, 526 columns) | Used for cross-validation of my own parse |

## 3. Export Mechanics

- **Format**: Delimited flat files (one file per database table). Described as "computable, delimited file format native to TheraOffice." The delimiter character is not specified in the documentation. Column definitions use SQL Server data types (varchar, int, smalldatetime, etc.).
- **Mechanism**: Manual UI-driven export ("allows organizations to do a manual one-time export of health data for one or more patients"). The export tool is built into TheraOffice.
- **Scope**: Single-patient or multi-patient ("one or more patients").
- **Access constraints**: Included in TheraOffice subscription at no additional cost (confirmed in mandatory disclosures). No separate API or vendor-assisted process described.
- **Organization-specific documentation**: The vendor states the export tool "will also generate documentation specific to that organization's environment," suggesting the actual export may include additional context (e.g., value set mappings, reference tables) not in the generic public documentation.
- **Non-tabular data**: The documentation notes "some electronic health information might not be available in a table format, such as rich text documents or images. This information is referenced in the extracts created for subsequent export." No further detail is provided on how this works.

## 4. Export Content: What's In It

The export is documented in a single PDF containing definitions for **19 tables** with **526 total columns**. Column definitions include name, SQL Server data type, and max length. Only 6 fields have descriptions (the glossary entries for Id, Pat_ID, MODIFIED_USER, MODIFIED_DATE, CREATED_USER, CREATED_DATE). No other fields have descriptions, value set definitions, or relationship documentation.

### Vendor's own content organization

The vendor does not provide explicit categories — tables are listed sequentially. However, the naming convention reveals the structure: 16 of 19 tables use the prefix `PAT_PROFILE_USCDI_*`, directly mapping to USCDI data classes. The remaining 3 are `PAT_PROFILE`, `PAT_PROFILE_CORE`, and `PTCASE`.

| Entity/Table | Fields | Described | Types | Inferred Category |
|---|---|---|---|---|
| PAT_PROFILE | 80 | 2 (PAT_ID, glossary) | yes | Demographics |
| PAT_PROFILE_CORE | 22 | 1 (PAT_ID) | yes | Demographics |
| PAT_PROFILE_CORE_ETHNICITY | 3 | 1 (PAT_ID) | yes | Demographics |
| PAT_PROFILE_CORE_GENDER | 3 | 1 (PAT_ID) | yes | Demographics |
| PAT_PROFILE_CORE_RACE | 3 | 1 (PAT_ID) | yes | Demographics |
| PAT_PROFILE_USCDI_ALLERGIES | 18 | 1 (PAT_ID) | yes | Allergies |
| PAT_PROFILE_USCDI_FAMILY_HISTORY | 13 | 1 (PAT_ID) | yes | Family Health History |
| PAT_PROFILE_USCDI_FAMILY_MEMBER | 30 | 1 (PAT_ID) | yes | Family Health History |
| PAT_PROFILE_USCDI_GOALS | 12 | 1 (PAT_ID) | yes | Goals |
| PAT_PROFILE_USCDI_IMMUNIZATIONS | 52 | 3 (PAT_ID + audit) | yes | Immunizations |
| PAT_PROFILE_USCDI_IMMUNIZATIONS_ACKNOWLEDGEMENT | 3 | 1 (PAT_ID) | yes | Immunizations |
| PAT_PROFILE_USCDI_IMPLANTDEVS | 22 | 3 (PAT_ID + audit) | yes | Implantable Devices |
| PAT_PROFILE_USCDI_LABS | 94 | 3 (PAT_ID + audit) | yes | Laboratory Results |
| PAT_PROFILE_USCDI_MEDICATIONS | 18 | 3 (PAT_ID + audit) | yes | Medications |
| PAT_PROFILE_USCDI_PROBLEMS | 12 | 3 (PAT_ID + audit) | yes | Problems / Conditions |
| PAT_PROFILE_USCDI_PROCEDURES | 13 | 3 (PAT_ID + audit) | yes | Procedures |
| PAT_PROFILE_USCDI_PROGRAM_ADMISSION | 11 | 3 (PAT_ID + audit) | yes | Encounters / Admissions |
| PAT_PROFILE_USCDI_VITALSIGNS | 26 | 3 (PAT_ID + audit) | yes | Vital Signs |
| PTCASE | 91 | 2 (PAT_ID + audit) | yes | Case / Billing |

**Category breakdown by field count** (from `analysis/entity-inventory-summary.json`):

| Category | Tables | Fields |
|---|---|---|
| Demographics | 5 | 111 |
| Laboratory Results | 1 | 94 |
| Case / Billing | 1 | 91 |
| Immunizations | 2 | 55 |
| Family Health History | 2 | 43 |
| Vital Signs | 1 | 26 |
| Implantable Devices | 1 | 22 |
| Allergies | 1 | 18 |
| Medications | 1 | 18 |
| Procedures | 1 | 13 |
| Goals | 1 | 12 |
| Problems / Conditions | 1 | 12 |
| Encounters / Admissions | 1 | 11 |

**Notable details about PTCASE** (91 fields): This is the only table that goes beyond USCDI. It contains case-level billing metadata: up to 12 diagnosis codes in both ICD-9 (`DIAG1_V9` through `DIAG12_V9`) and ICD-10 (`DIAG1_V10` through `DIAG12_V10`) formats, insurance references (`INSURANCE1`/`2`/`3` as integer IDs), co-pay amount, fee schedule type, guarantor ID, billing sequence, payer type, place of service, and provider IDs for up to 5 disciplines. However, these are case-level summaries — there are no charge-line, claim, payment, or remittance tables.

**Data type distribution**: varchar (238), int (116), smalldatetime (66), tinyint (55), bit (30), decimal (12), datetime (4), smallint (2), uniqueidentifier (2), char (1).

**Coded fields without value sets**: 57 tinyint/smallint fields are clearly coded values (e.g., ALLERGY_TYPE, REACTION, SEVERITY, STATUS, GENDER, SMOKING_STATUS, BILLINGSEQUENCE, PAYER) but no value set mappings are provided anywhere in the documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized almost entirely around USCDI data classes. The `PAT_PROFILE_USCDI_*` naming convention makes this explicit — the vendor built tables that map one-to-one to USCDI categories: allergies, family history, goals, immunizations, implantable devices, labs, medications, problems, procedures, program admissions, and vital signs.

The **Demographics** section (PAT_PROFILE + PAT_PROFILE_CORE + ethnicity/gender/race) is the richest area at 111 fields, including 25 custom fields, portal engagement fields, and comprehensive demographic attributes. The **Labs** table is the deepest USCDI table at 94 fields, covering order info, specimen details, facility, provider, and results.

The **PTCASE** table (91 fields) is the only table that ventures beyond USCDI, containing case-level billing metadata. However, it is a single summary table — not the detailed billing/claims/payment data that TheraOffice's integrated billing module manages.

**Critical absence**: There are zero tables for clinical notes, therapy documentation, treatment plans, evaluations, daily notes, or discharge summaries — the core product of a physical therapy EMR. The vendor acknowledges this obliquely by noting that "rich text documents or images" are "referenced in the extracts" but provides no documentation for how this works, what format the notes take, or what metadata accompanies them.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PAT_PROFILE` (80 fields), `PAT_PROFILE_CORE` (22 fields), plus ethnicity/gender/race tables (111 fields total) | Thorough — includes custom fields, portal info, previous addresses |
| Encounters / visits | ⚠️ Partial | `PAT_PROFILE_USCDI_PROGRAM_ADMISSION` (11 fields) has admission/discharge dates and disposition. `PTCASE` has case creation/discharge dates | No visit-level encounter data; cases are episodic, not per-visit |
| Problems / conditions | ✅ Covered | `PAT_PROFILE_USCDI_PROBLEMS` (12 fields) with SNOMED/ICD-10 codes | Reasonable for USCDI scope |
| Medications / prescriptions | ⚠️ Partial | `PAT_PROFILE_USCDI_MEDICATIONS` (18 fields) with RxNorm | Active medication list only. No prescription orders, pharmacy, dispense details, refill history, or EPCS records despite the product supporting e-prescribing |
| Allergies | ✅ Covered | `PAT_PROFILE_USCDI_ALLERGIES` (18 fields) with SNOMED/RxNorm/MED-RT codes | Adequate |
| Immunizations | ✅ Covered | `PAT_PROFILE_USCDI_IMMUNIZATIONS` (52 fields) | Very detailed including guardian info, lot numbers, administration details |
| Vitals | ✅ Covered | `PAT_PROFILE_USCDI_VITALSIGNS` (26 fields) | Includes standard vitals plus pediatric percentiles |
| Lab results | ✅ Covered | `PAT_PROFILE_USCDI_LABS` (94 fields) | Extensive — specimen, facility, provider, results |
| Imaging / diagnostic reports | ❌ Not covered | No imaging tables | Product may receive imaging results via C-CDA transitions of care; unclear if stored natively |
| Procedures | ✅ Covered | `PAT_PROFILE_USCDI_PROCEDURES` (13 fields) | Basic procedure records with codes |
| Clinical notes / documents | ❌ Not covered | No tables for notes, evaluations, daily treatment records, progress notes, or discharge summaries | **Most significant gap.** TheraOffice's core value is 40+ clinical documentation templates for PT/OT/SLP. The documentation vaguely says rich text is "referenced in the extracts" but provides no detail. |
| Care plans / goals | ⚠️ Partial | `PAT_PROFILE_USCDI_GOALS` (12 fields) | Goals only. No structured treatment plans, exercise programs, or care plan documentation |
| Orders / referrals | ❌ Not covered | PAT_PROFILE has `REFERRALSOURCE_ID` (integer only); no referral detail table | Product supports referral management and CPOE; no order or referral tables exported |
| Insurance / coverage | ⚠️ Partial | PTCASE has `INSURANCE1`/`2`/`3` as integer IDs, `FEESCHEDULE_TYPE`, `PAYER` | IDs only — no plan names, subscriber info, group numbers, policy dates, authorization data. Reference tables not exported |
| Claims / billing | ⚠️ Partial | PTCASE has case-level billing metadata (91 fields including diagnosis codes, fee schedule, guarantor, billing sequence) | Case-level summary only. No charge lines, CPT codes per visit, claim submissions, denial records, or collections data despite fully integrated billing |
| Payments | ❌ Not covered | No payment tables | Product has payment posting, ERA downloads, card processing (TheraOffice Pay) — none exported |
| Consents / directives | ❌ Not covered | PTCASE has `HIPAA_ENABLED` and `HIPAA_COMMENTS` only | No consent forms, advance directives |
| Patient communications | ❌ Not covered | No messaging or portal communication tables | Product has patient portal with messaging capability |
| Specialty-specific (PT/OT/SLP) | ❌ Not covered | No outcome measure tables, no therapy-specific assessment data, no exercise programs | **Critical gap.** The product's differentiator is PT/OT/SLP-specific clinical content (McKenzie, pelvic health, vestibular, lymphedema, pediatric assessments). None are in the export |

## 6. Documentation Quality

The documentation is **structurally adequate but substantively minimal**:

- **Strengths**: The PDF is cleanly formatted, well-organized with a table of contents, and covers every column in every table with its SQL Server data type and max length. The 30-page document is easy to navigate. All 526 columns were successfully parsed.
- **Field descriptions**: Effectively absent. Only 6 fields (the glossary entries for Id, PAT_ID, and audit columns) have descriptions. The remaining 520 fields (98.9%) have names and types only.
- **Value sets**: Completely undocumented. There are 57 coded fields (tinyint/smallint) like `ALLERGY_TYPE`, `REACTION`, `SEVERITY`, `GENDER`, `SMOKING_STATUS`, `BILLINGSEQUENCE`, `PAYER` — none have value mappings. A developer would have no way to interpret these coded values.
- **Relationships**: Not formally documented. Tables are linked by `PAT_ID`. PTCASE references `INSURANCE1`/`2`/`3`, `PROVIDER_ID`, `GUARANTOR_ID`, `REF_PHYSICIAN` as integer foreign keys, but the referenced tables are not in the export.
- **Sample data**: None provided.
- **Machine-readable schema**: None. The data dictionary is a PDF only.
- **Import feasibility**: A developer could load the delimited files into a database, but interpreting the data would require significant reverse engineering. Coded fields, foreign key references to non-exported tables, and absent field descriptions make the export difficult to use in isolation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers USCDI data classes adequately but misses the majority of what TheraOffice actually stores. The most significant gap is the complete absence of clinical documentation — therapy notes, evaluations, treatment plans, daily notes, and discharge summaries — which is the core product of a physical therapy EMR. Billing data is represented only at the case summary level (PTCASE), with no charge-line, claim, payment, ERA, or collections data despite TheraOffice being a fully integrated billing system. E-prescribing records, referral details, patient portal communications, telehealth records, outcome measures, and specialty-specific PT/OT/SLP assessments are all absent.

The `PAT_PROFILE_USCDI_*` table naming convention is the clearest possible signal: 16 of 19 tables were built by mapping USCDI data classes to flat files. The export covers what's needed for (g)(10) FHIR API compliance, not what's in the designated record set. The vendor's own EHI page distinguishes between their "FHIR API's and connection information" (for integration) and the "EHI Tables export" — yet the table content is essentially a USCDI projection.

**Axis 2 — Export approach: Repackaged existing export**

The export is a flat-file projection of the same USCDI data classes that the product's (g)(10) FHIR API exposes. The table names make this explicit: `PAT_PROFILE_USCDI_ALLERGIES`, `PAT_PROFILE_USCDI_MEDICATIONS`, `PAT_PROFILE_USCDI_PROBLEMS`, etc. The only table that goes beyond USCDI is `PTCASE`, which adds case-level billing metadata. While the format (delimited files vs. FHIR) is different, the data scope is the same USCDI footprint. There is no evidence of a purpose-built EHI export covering therapy documentation, detailed billing, specialty assessments, or other data domains that TheraOffice stores.

### Key Findings

1. **USCDI repackaged as EHI**: 16 of 19 tables are explicitly named `PAT_PROFILE_USCDI_*`, confirming the export was built by mapping USCDI data classes to flat files rather than exporting the product's actual data model. This is the clearest example of (g)(10)/(b)(10) conflation (`downloads/ehi_tables/EHI Export All Tables - May 2024 (TheraOffice).pdf`).

2. **Therapy documentation completely absent**: TheraOffice's core value proposition — 40+ customizable clinical templates for PT/OT/SLP evaluations, daily notes, progress notes, treatment plans, and discharge summaries — is not represented by any table in the export. The vendor obliquely acknowledges this by noting "rich text documents or images" are "referenced in the extracts" but provides zero documentation on how this works (`downloads/ehi-page-screenshot-full.png`).

3. **Billing data is a stub**: Despite TheraOffice being a fully integrated billing system (claims, ERA, payments, denials, collections, card processing), billing is represented only by PTCASE — a case-level summary table. No charge lines, claims, payments, remittance records, or collections data are exported.

4. **Documentation lacks interpretability**: 98.9% of fields (520 of 526) have no descriptions. 57 coded fields have no value set mappings. Foreign keys reference tables not included in the export. No sample data is provided.

5. **No cost barrier**: The mandatory disclosures confirm that (b)(10) export is included in the TheraOffice subscription at no additional cost (`downloads/theraoffice-mandatory-disclosures-statement_v4.pdf`).

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   Delimited flat files (SQL Server schema)
Entities:        19 tables
Fields:          526
Descriptions:    1.1% (6 of 526 fields, glossary entries only)
Sample data:     No
Bulk export:     Yes (one or more patients)
Domains covered: 7 of 17 applicable domains fully covered; 4 partial; 6 not covered
```

### Bottom Line

TheraOffice's EHI export is a USCDI clinical summary repackaged as "(b)(10) all data." For a physical therapy EMR whose primary value is clinical documentation and integrated billing, the complete absence of therapy notes, treatment plans, outcome measures, detailed billing records, and specialty assessments means patients would receive their demographic and clinical summary data but not the clinical documentation and billing records that constitute the majority of their designated record set. The `PAT_PROFILE_USCDI_*` naming convention is the clearest possible indicator that this export was built to USCDI specifications, not to the (b)(10) "all EHI" requirement.
