# EHI Export Analysis: Netsmart Technologies

**Product**: GEHRIMED v.4.3
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2816.gEHR.04.03.1.221227

## 1. Product Context

GEHRIMED is a cloud-based EHR and practice management platform designed exclusively for long-term/post-acute care (LTPAC) practitioners — primarily geriatricians, nurse practitioners, and physician assistants who round across multiple skilled nursing facilities. It is a **physician practice EHR** (not a facility-side EHR), focused on the itinerant providers who visit patients in SNFs, assisted living, and similar settings. Acquired by Netsmart Technologies in 2021 (originally developed by Geriatric Practice Management Corp).

Key data domains the product stores:
- **Clinical documentation**: Encounter notes with structured templates, wound assessments, physical exam, ROS, assessment/plan
- **Medications**: Medication management with e-prescribing via Dr. First integration (including controlled substances, PDMP)
- **Lab orders and results**: CPOE for labs; results flow back via integrations
- **Imaging orders**: CPOE for diagnostic imaging
- **Billing/RCM**: Automated charge capture, claims submission/tracking, ERA processing, denial management, AR management (AlphaCollector tool)
- **Quality measures**: MIPS dashboard, eCQMs, ACO quality measures
- **Communication**: Secure internal messaging, encounter delivery to facilities, Carequality/CareConnect HIE
- **Patient portal**: myHealthPointe portal
- **Insurance**: Detailed insurance/coverage tracking
- **Scheduling**: Multi-facility census and appointment management

This sets the baseline: a genuine (b)(10) export should cover clinical documentation, medications, labs, imaging, billing/claims, quality tracking, messaging, insurance, and scheduling.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI Export All Tables - November2023 (GEHRIMED).pdf` | 90-page data dictionary documenting 36 database tables and 912 columns. Authored 2023-11-08. | **Primary artifact** — defines the entire export schema |
| `downloads/ehi_export_all_tables_gehrimed_2023.txt` | Plain-text extraction of the PDF via `pdftotext` (71,736 bytes) | Used for programmatic parsing |
| `downloads/ehi_export_all-tables_gehrimed_2023.zip` | ZIP archive containing the PDF (619,192 bytes) | Container only |
| `downloads/screenshot-ehi-landing-page-full.png` | Full-page screenshot of the EHI export landing page | Confirms export mechanics and vendor intent |
| `downloads/screenshot-ehi-landing-page.png` | Viewport screenshot of the landing page | Supplementary |

The PDF data dictionary is the sole substantive artifact. There is no sample data, no machine-readable schema, and no additional documentation beyond the landing page text.

## 3. Export Mechanics

- **Format**: Delimited flat files (one file per database table), native to GEHRIMED's internal data model
- **Mechanism**: Manual one-time export initiated by the organization ("allows organizations to do a manual one-time export of health data for one or more patients")
- **Scope**: Single-patient or multi-patient ("for one or more patients")
- **Access constraints**: Not stated; appears to be a built-in tool available to organizations
- **Fees**: Not mentioned
- **Distinction from FHIR**: The landing page explicitly separates this from the FHIR Developer Portal: "This schema is intended for EHI export functionality. If you are working with a Netsmart customer and want to understand different options on integrating with our solutions, please visit our Netsmart Developer Portal."
- **Caveats**: Content may vary based on organization's version, configuration, and customizations. Rich text documents and images "might not be available in a table format" but are "referenced in the extracts created for subsequent export."

## 4. Export Content: What's In It

### Data dictionary structure

The PDF documents **36 database tables** with **912 total columns** (verified by parsing — the prior report's claim of "35 tables and 876 columns" was slightly off). Every column has:
- Column name ✅
- Data type (`ColumnType`) ✅ (100% coverage)
- Max length ✅

However, column-level descriptions are extremely sparse:
- **12 of 912 fields (1.3%)** have inline descriptions, all within the `aspnet_Users` table
- **82 additional fields** match the glossary terms (Id, PatientID, LastModifiedBy, etc.) documented at the top of the PDF, giving them implicit descriptions
- **Effective description coverage**: ~94 of 912 fields (10.3%) have any kind of description
- **No value sets** are documented for coded fields
- **No foreign key relationships** are formally documented (though implicit via shared ID column names)
- **No sample data** is provided
- **35 of 36 tables** have a table-level description (though most are generic, e.g., "GEHRIMED Patient detail.")

### Vendor's own content organization

The vendor does not organize tables into explicit categories; the PDF lists them alphabetically. I assigned categories based on table names and content. Full inventory in `analysis/entity-inventory-full.json`.

| Table | Columns | Described | Category |
|---|---|---|---|
| aspnet_Users | 53 | 12 | User / System |
| Attachments | 16 | 0 | Attachments / Documents |
| Companyinfo | 32 | 0 | Organization |
| Dictation_ICD | 22 | 0 | Clinical Notes / Encounters |
| Dictation_Items | 11 | 0 | Clinical Notes / Encounters |
| Dictation_Roles | 2 | 0 | Clinical Notes / Encounters |
| Dictations | 59 | 0 | Clinical Notes / Encounters |
| Document | 20 | 0 | Clinical Notes / Encounters |
| EnumTypes | 2 | 0 | Reference / Lookup |
| EnumValues | 4 | 0 | Reference / Lookup |
| groups | 63 | 0 | User / System |
| HL7_Patient | 45 | 0 | Demographics |
| HL7_PatientInsurance | 72 | 0 | Insurance |
| Interfaces | 8 | 0 | Interfaces / Integration |
| Interfaces_Outbound | 7 | 0 | Interfaces / Integration |
| LabOrder | 43 | 0 | Laboratory |
| LabResult | 36 | 0 | Laboratory |
| LabSpecimen | 49 | 0 | Laboratory |
| Patient_Assessments | 13 | 0 | Assessments |
| Patient_History | 6 | 0 | Family History |
| Patient_Imaging | 15 | 0 | Imaging |
| Patient_ImmunizationDetails | 17 | 0 | Immunizations |
| Patient_Immunizations | 40 | 0 | Immunizations |
| Patient_Labs | 64 | 0 | Laboratory |
| Patient_MedicationAllergy | 23 | 0 | Medications |
| Patient_Medications | 39 | 0 | Medications |
| Patient_ProblemList | 21 | 0 | Problems / Diagnoses |
| Patient_Procedures | 12 | 0 | Procedures |
| Patient_Relationships | 8 | 0 | Demographics / Relationships |
| Patient_Schedule | 16 | 0 | Scheduling |
| Patient_Vitals | 13 | 0 | Vitals |
| PatientImplantableDevice | 20 | 0 | Implantable Devices |
| Patientinfo | 46 | 0 | Demographics |
| Patientinfo_Smoking | 8 | 0 | Smoking / Social History |
| SmokingCessation | 2 | 0 | Smoking / Social History |
| SmokingStatus | 5 | 0 | Smoking / Social History |

**Category summary:**

| Category | Tables | Fields |
|---|---|---|
| Laboratory | 4 | 192 |
| Clinical Notes / Encounters | 5 | 114 |
| User / System | 2 | 116 |
| Demographics | 3 | 99 |
| Insurance | 1 | 72 |
| Medications | 2 | 62 |
| Immunizations | 2 | 57 |
| Organization | 1 | 32 |
| Problems / Diagnoses | 1 | 21 |
| Implantable Devices | 1 | 20 |
| Attachments / Documents | 1 | 16 |
| Scheduling | 1 | 16 |
| Interfaces / Integration | 2 | 15 |
| Imaging | 1 | 15 |
| Assessments | 1 | 13 |
| Vitals | 1 | 13 |
| Procedures | 1 | 12 |
| Smoking / Social History | 3 | 15 |
| Demographics / Relationships | 1 | 8 |
| Reference / Lookup | 2 | 6 |
| Family History | 1 | 6 |

The deepest areas are Laboratory (192 fields across 4 tables), Clinical Notes/Encounters (114 fields across 5 tables), and Insurance (72 fields in one large table).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export reflects GEHRIMED's native database schema — a genuine dump of internal tables rather than a projection into a standard format. The strongest areas:

- **Laboratory**: 4 tables (`LabOrder`, `LabResult`, `LabSpecimen`, `Patient_Labs`) with 192 total fields — very deep coverage of the lab ordering and results lifecycle including specimen tracking
- **Clinical encounters**: `Dictations` (59 fields) is the core encounter table with rich text content, CPT codes, signature workflows, QA state; supported by `Dictation_ICD` (22 fields for encounter diagnoses), `Dictation_Items` (template data), and `Document` (binary document storage)
- **Insurance**: `HL7_PatientInsurance` has 72 fields — detailed plan, subscriber, group, authorization, and policy data
- **Demographics**: Between `HL7_Patient` (45 fields) and `Patientinfo` (46 fields), comprehensive demographic data including gender identity, sexual orientation, race, ethnicity, preferred language
- **Medications and allergies**: `Patient_Medications` (39 fields) and `Patient_MedicationAllergy` (23 fields) cover the medication list and allergy data
- **Immunizations**: 57 fields across 2 tables with CVX codes and administration details

Thinner areas:
- **Family history** (`Patient_History`): only 6 fields
- **Assessments** (`Patient_Assessments`): 13 fields — slim for a product that supports clinical assessments
- **Procedures** (`Patient_Procedures`): 12 fields
- **Vitals** (`Patient_Vitals`): 13 fields

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patientinfo` (46 fields), `HL7_Patient` (45 fields), `Patient_Relationships` (8 fields), `Patientinfo_Smoking` (8 fields) | Thorough — two complementary demographics tables with extensive detail |
| Encounters / visits | ✅ Covered | `Dictations` (59 fields), `Dictation_Items` (11 fields), `Dictation_Roles` (2 fields) | Core encounter data with rich text documents, CPT codes, and signature workflows |
| Problems / conditions | ✅ Covered | `Patient_ProblemList` (21 fields), `Dictation_ICD` (22 fields) | Both longitudinal problem list and encounter-level diagnoses with ICD-10 codes |
| Medications / prescriptions | ✅ Covered | `Patient_Medications` (39 fields) | RxNorm-coded medications with dosage, SIG, frequency, prescriber info |
| Allergies | ✅ Covered | `Patient_MedicationAllergy` (23 fields) | Coded allergies with reactions and severity |
| Immunizations | ✅ Covered | `Patient_Immunizations` (40 fields), `Patient_ImmunizationDetails` (17 fields) | Detailed with CVX codes, lot numbers, manufacturer, site, route |
| Vitals | ✅ Covered | `Patient_Vitals` (13 fields) | Present but relatively thin for vital signs data |
| Lab results | ✅ Covered | `Patient_Labs` (64 fields), `LabResult` (36 fields), `LabSpecimen` (49 fields), `LabOrder` (43 fields) | Very deep — 192 total fields across 4 tables covering the full lab lifecycle |
| Imaging / diagnostic reports | ✅ Covered | `Patient_Imaging` (15 fields) | Orders, results, CPT codes, instructions |
| Procedures | ✅ Covered | `Patient_Procedures` (12 fields) | Procedure codes and descriptions present |
| Clinical notes / documents | ✅ Covered | `Dictations` (59 fields — includes `Document` rich text field), `Document` (20 fields — binary storage), `Attachments` (16 fields — includes `ActualFile` image column) | Rich text notes, binary documents, and patient attachments |
| Care plans / goals | ⚠️ Partial | No dedicated care plan table; care plan content likely embedded in encounter notes (`Dictations.Document`) | GEHRIMED is primarily a documentation/encounter system; care plans may not be stored as discrete data |
| Orders / referrals | ⚠️ Partial | `LabOrder` (43 fields) and `Patient_Imaging` (15 fields) for lab/imaging orders; no referral-specific table | Lab and imaging orders covered; no distinct referral tracking table |
| Insurance / coverage | ✅ Covered | `HL7_PatientInsurance` (72 fields) | Detailed plan, subscriber, group, authorization, and policy data |
| Claims / billing | ❌ Not covered | CPT codes appear on `Dictations.PrimaryCPT` and `Dictation_ICD.Charged`; `groups` has billing config fields. No claims, charges, payments, or AR tables. | **Significant gap** — GEHRIMED has a full billing/RCM module (AlphaCollector, claims submission, ERA processing, denial management, AR management). None of this downstream billing lifecycle data is in the export. |
| Payments | ❌ Not covered | No payment or remittance tables | **Gap** — product processes ERA/remittances but does not export them |
| Consents / directives | ❌ Not covered | No advance directive or consent table | May be captured in encounter notes or assessments, but not as discrete data |
| Patient communications | ❌ Not covered | No messaging or communication table | **Gap** — product has secure internal messaging feature but it is absent from the export |
| Family health history | ✅ Covered | `Patient_History` (6 fields) | Present but thin |
| Implantable devices | ✅ Covered | `PatientImplantableDevice` (20 fields) | UDI and device identifier data |
| Assessments | ✅ Covered | `Patient_Assessments` (13 fields) | Coded assessments with ValueSetOIDs |
| Smoking / social history | ✅ Covered | `Patientinfo_Smoking` (8 fields), `SmokingStatus` (5 fields), `SmokingCessation` (2 fields) | SNOMED-coded smoking status |
| Scheduling | ✅ Covered | `Patient_Schedule` (16 fields) | Appointment/schedule data present |
| Specialty-specific (LTPAC/geriatrics) | ⚠️ Partial | Wound data referenced in `Attachments.WoundID`; clinical templates in `Dictation_Items`; no dedicated wound assessment table or geriatric-specific assessment tables | GEHRIMED has wound assessment with historical tracking as a feature; only wound photo attachments are in the export, not structured wound assessment data |

## 6. Documentation Quality

**Strengths:**
- The export is clearly a purpose-built database dump, explicitly distinguished from the FHIR API
- Every column has a data type and max length documented
- Every table has a brief description
- A glossary explains common field patterns (Id, PatientID, DictationID, etc.)
- The landing page provides clear, honest caveats about content variability

**Weaknesses:**
- **Column descriptions are almost nonexistent**: only 12 of 912 fields (1.3%) have inline descriptions, all in the `aspnet_Users` table. Even counting glossary coverage, only ~10% of fields have any description.
- **No value sets**: Coded fields like `Status`, `JobState`, `UserType` have no documentation of valid values. The `EnumTypes` and `EnumValues` tables are included in the export itself (so consumers get the lookup data), but the PDF doesn't enumerate them.
- **No foreign key documentation**: Relationships between tables are only implicit via shared ID column names. No ERD or relationship diagram.
- **No sample data** or example export files
- **No machine-readable schema**: No JSON Schema, XSD, DDL, or CSV data dictionary — only a PDF
- **PDF-only format**: The data dictionary is locked in a non-programmatic format
- **Dated November 2023**: Over 2 years old at time of analysis

A developer working with this export could identify the tables and column types but would need significant reverse engineering to understand what many columns mean, what valid values are for coded fields, and how tables relate. The inclusion of `EnumTypes`/`EnumValues` in the export itself partially compensates for missing value set documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers the core clinical domains well — encounters, medications, labs, imaging, immunizations, allergies, problems, vitals, procedures, demographics, insurance, attachments, and implantable devices. This goes meaningfully beyond USCDI by including insurance details (72 fields), lab specimens, imaging orders, patient scheduling, and the full encounter data model with QA workflows.

However, there are significant gaps relative to what GEHRIMED stores:
- **Billing/RCM data is entirely absent.** GEHRIMED has a full billing module (AlphaCollector, claims submission/tracking, ERA processing, denial management, AR management), yet the export contains zero billing lifecycle tables. Only encounter-level CPT codes are present.
- **Secure messaging** is a documented product feature but has no export table.
- **Quality measure tracking** (MIPS, eCQMs) is a key product feature but not exported.
- **Wound assessment** structured data (a specialty feature for LTPAC) appears absent; only wound photo attachments are represented.

The clinical core is solid, but the billing gap is notable for a product that markets RCM as a major capability.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged FHIR or C-CDA export:
- The export is a native database table dump in delimited flat files
- The landing page explicitly distinguishes it from the FHIR Developer Portal
- The data dictionary documents internal database tables (e.g., `aspnet_Users`, `Dictation_ICD`, `HL7_PatientInsurance`) — not FHIR resources or C-CDA sections
- The column names, types, and structures reflect the actual application schema, not a standards mapping
- Coverage extends beyond USCDI into areas like insurance details, lab specimens, imaging orders, scheduling, and attachments

### Key Findings

1. **Purpose-built native database export with 36 tables and 912 fields** — genuinely distinct from the vendor's FHIR API. The landing page explicitly separates the two, and the data dictionary documents internal database tables, not FHIR resources. (`EHI Export All Tables - November2023 (GEHRIMED).pdf`)

2. **Billing/RCM data is entirely missing despite being a major product capability.** GEHRIMED markets AlphaCollector (AR automation), claims submission, ERA processing, and denial management. The export contains encounter-level CPT codes but zero tables for claims, payments, remittances, or accounts receivable. This is the single largest gap.

3. **Column-level documentation is extremely thin.** Only 12 of 912 fields (1.3%) have descriptions; all are in the `aspnet_Users` table. The remaining 900 fields have only a column name, data type, and max length. No value sets, no foreign key documentation, no sample data.

4. **Laboratory coverage is notably deep** — 192 fields across 4 tables (`LabOrder`, `LabResult`, `LabSpecimen`, `Patient_Labs`) covering the full lab lifecycle from orders through specimens to results.

5. **Insurance data is thorough** — `HL7_PatientInsurance` has 72 fields covering plan details, subscriber info, group numbers, authorization, and policy data. This goes well beyond USCDI's basic coverage requirements.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   Delimited flat files (one per table)
    Entities:        36 tables
    Fields:          912
    Descriptions:    1.3% of fields (10.3% including glossary terms)
    Sample data:     No
    Bulk export:     Yes (one or more patients)
    Domains covered: 15 of 19 applicable domains

### Bottom Line

GEHRIMED's EHI export is a genuine purpose-built database dump that covers clinical data well — encounters, medications, labs, imaging, immunizations, allergies, insurance, and more. However, the complete absence of billing/RCM data (claims, payments, AR) despite the product having full billing capabilities is a significant gap. Documentation quality is poor: 99% of fields have no description, there are no value sets, no relationship diagrams, and no sample data — making the export hard to interpret without reverse engineering.
