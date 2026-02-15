# EHI Export Analysis: Netsmart Technologies

**Product**: GEHRIMED v.4.3
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2816.gEHR.04.03.1.221227

## 1. Product Context

GEHRIMED is a cloud-based EHR and practice management platform designed exclusively for long-term/post-acute care (LTPAC) physicians, nurse practitioners, and physician assistants who round across multiple skilled nursing facilities, assisted living communities, and similar settings. Originally developed by Geriatric Practice Management (GPM) Corp and acquired by Netsmart Technologies in 2021, it was the first LTPAC EHR to receive ONC certification.

**Key data domains the product stores:**
- **Clinical documentation**: Encounter notes with customizable templates, wound assessments, physical exam findings, review of systems, assessment and plan
- **Medications**: Medication lists plus integrated e-prescribing (via Dr. First)
- **Lab/imaging orders and results**: Certified for CPOE lab (a)(2) and imaging (a)(3)
- **Billing/RCM**: Automated billing and charge capture, claims submission/tracking, ERA processing, denial management, AR management, AlphaCollector automation
- **Quality measures**: MIPS dashboard, eCQMs, ACO measures
- **Communications**: Secure internal messaging, automated encounter delivery to facilities
- **Interoperability**: PointClickCare bi-directional integration, Carequality, C-CDA transitions of care
- **Patient portal**: myHealthPointe for view/download/transmit

This product is a full EHR + practice management system, so a complete EHI export should cover clinical, billing/financial, and administrative domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `EHI Export All Tables - November2023 (GEHRIMED).pdf` (947 KB, 90 pages) | Data dictionary documenting all 36 database tables and 912 columns in the EHI export. Primary artifact. | **High** — the core documentation |
| `ehi_export_all-tables_gehrimed_2023.zip` (619 KB) | ZIP containing the PDF above | Wrapper only |
| `ehi_export_all_tables_gehrimed_2023.txt` (72 KB) | Plain text extraction of the PDF via pdftotext | Useful for programmatic parsing |
| `screenshot-ehi-landing-page.png` / `screenshot-ehi-landing-page-full.png` | Screenshots of the EHI export landing page at ntst.com | Useful for verifying landing page content |
| Landing page (verified live 2026-02-15) | HTML page at `ntst.com/lp/certifications/ehi-all-data-gehrimed` describing the export and linking to the ZIP | Confirmed accessible; describes export mechanics |

No sample data files, no machine-readable schemas (JSON Schema, XSD, DDL), and no relationship diagrams were provided.

## 3. Export Mechanics

- **Format**: Delimited flat files (one file per database table), in a format "native to GEHRIMED." File names match table names from the documentation.
- **Mechanism**: Manual UI-initiated export ("allows organizations to do a manual one-time export of health data for one or more patients"). The landing page explicitly distinguishes this from their FHIR API/Developer Portal.
- **Single-patient vs bulk**: Supports "one or more patients" per the landing page text.
- **Binary content**: Rich text documents and images "might not be available in a table format" but are "referenced in the extracts created for subsequent export." The `Attachments` table has an `ActualFile` column of type `image` and `Document` has a `Doc` column of type `varbinary`, suggesting binary content may be included or linked.
- **Access constraints**: No fees or special access mentioned. Documentation is publicly downloadable.
- **Organization-specific variation**: The landing page notes that "content included in the export might vary" based on the organization's version, custom development, and configuration. The export tool generates organization-specific documentation at runtime.

## 4. Export Content: What's In It

### Data dictionary overview

The PDF data dictionary (dated November 8, 2023, authored by "Mikolajczak-Brown, Allie") documents:

- **36 database tables** (prior report claimed 35; verified count is 36 by parsing all `Table Name:` entries after the table of contents)
- **912 total columns** (prior report claimed 876; the discrepancy is due to 36 columns starting at page boundaries with form feed characters that were missed by the prior grep-based count)
- **12 columns with descriptions (1.3%)** — all 12 are in the `aspnet_Users` table; the remaining 35 tables have zero column-level descriptions
- **912 columns with data types (100%)** — every column has a `ColumnType` and `Max Length`
- **0 value set definitions** — no documentation of what specific enum/code values mean, though `EnumTypes` and `EnumValues` reference tables are included in the export itself
- **0 relationship diagrams** — foreign keys are implicit via shared ID columns (PatientID, DictationID, GroupID) and a glossary of common fields

The document begins with an Overview section and a Glossary of Terms explaining 8 common field patterns (Id, PatientID, LastModifiedBy, LastModifiedDate, CreatedBy, AddedBy, DictationID, AddedDate).

### Vendor's own content organization

The vendor organizes tables by their native database names without explicit domain categories. Each table has a brief description. Below is the complete inventory:

| Table | Fields | Descriptions | Types | Table Description |
|---|---|---|---|---|
| aspnet_Users | 53 | 12 (23%) | ✅ | GEHRIMED User Account Information |
| Attachments | 16 | 0 | ✅ | GEHRIMED Patient Attachment Information |
| Companyinfo | 32 | 0 | ✅ | GEHRIMED company/facility detail |
| Dictation_ICD | 22 | 0 | ✅ | GEHRIMED Encounter diagnosis data |
| Dictation_Items | 11 | 0 | ✅ | GEHRIMED encounter template data |
| Dictation_Roles | 2 | 0 | ✅ | GEHRIMED encounter roles |
| Dictations | 59 | 0 | ✅ | GEHRIMED Encounter Information |
| Document | 20 | 0 | ✅ | GEHRIMED Document Information |
| EnumTypes | 2 | 0 | ✅ | GEHRIMED Enum type definitions |
| EnumValues | 4 | 0 | ✅ | GEHRIMED Enum value definitions |
| groups | 63 | 0 | ✅ | GEHRIMED group/practice detail |
| HL7_Patient | 45 | 0 | ✅ | GEHRIMED patient information |
| HL7_PatientInsurance | 72 | 0 | ✅ | GEHRIMED Patient Insurance information |
| Interfaces | 8 | 0 | ✅ | GEHRIMED integration |
| Interfaces_Outbound | 7 | 0 | ✅ | GEHRIMED outbound integration |
| LabOrder | 43 | 0 | ✅ | GEHRIMED Lab Order detail |
| LabResult | 36 | 0 | ✅ | GEHRIMED Lab Result detail |
| LabSpecimen | 49 | 0 | ✅ | GEHRIMED lab specimen detail |
| Patient_Assessments | 13 | 0 | ✅ | GEHRIMED Patient Assessments |
| Patient_History | 6 | 0 | ✅ | GEHRIMED Patient History |
| Patient_Imaging | 15 | 0 | ✅ | GEHRIMED Patient imaging data |
| Patient_ImmunizationDetails | 17 | 0 | ✅ | GEHRIMED Immunization detail |
| Patient_Immunizations | 40 | 0 | ✅ | GEHRIMED Patient Immunization data |
| Patient_Labs | 64 | 0 | ✅ | GEHRIMED Patient Lab data |
| Patient_MedicationAllergy | 23 | 0 | ✅ | GEHRIMED Patient allergy data |
| Patient_Medications | 39 | 0 | ✅ | GEHRIMED Patient Medication data |
| Patient_ProblemList | 21 | 0 | ✅ | GEHRIMED Patient Problem List data |
| Patient_Procedures | 12 | 0 | ✅ | GEHRIMED Patient Procedures |
| Patient_Relationships | 8 | 0 | ✅ | GEHRIMED Patient Relationship data |
| Patient_Schedule | 16 | 0 | ✅ | GEHRIMED Patient Schedule data |
| Patient_Vitals | 13 | 0 | ✅ | GEHRIMED Patient Vitals data |
| PatientImplantableDevice | 20 | 0 | ✅ | GEHRIMED Patient Implantable Device data |
| Patientinfo | 46 | 0 | ✅ | GEHRIMED Patient detail |
| Patientinfo_Smoking | 8 | 0 | ✅ | GEHRIMED Patient smoking detail |
| SmokingCessation | 2 | 0 | ✅ | GEHRIMED Smoking Cessation reference |
| SmokingStatus | 5 | 0 | ✅ | GEHRIMED Smoking Status reference |

### Notable tables by size

The largest tables by column count:
1. **HL7_PatientInsurance** — 72 fields (insurance/subscriber data in HL7 IN1 segment format)
2. **Patient_Labs** — 64 fields (consolidated lab results with OBR/OBX-style fields)
3. **groups** — 63 fields (practice group configuration including extensive billing settings)
4. **Dictations** — 59 fields (encounter records with clinical content, workflow state, CPT coding)
5. **aspnet_Users** — 53 fields (user/provider information, the only table with descriptions)
6. **LabSpecimen** — 49 fields (lab specimen detail)
7. **Patientinfo** — 46 fields (core patient demographics including gender identity, sexual orientation)
8. **HL7_Patient** — 45 fields (patient demographics in HL7-derived format)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Grouping the 36 tables by domain (see `analysis/domain-summary.json`):

| Domain | Tables | Fields |
|---|---|---|
| Demographics | 3 | 99 |
| Encounters / Clinical Notes | 4 | 94 |
| Lab Results | 4 | 192 |
| Organization / Facility | 2 | 95 |
| Insurance / Coverage | 1 | 72 |
| Immunizations | 2 | 57 |
| User / Provider Info | 1 | 53 |
| Medications | 1 | 39 |
| Documents / Attachments | 2 | 36 |
| Allergies | 1 | 23 |
| Problems / Diagnoses | 1 | 21 |
| Implantable Devices | 1 | 20 |
| Scheduling | 1 | 16 |
| Smoking Status | 3 | 15 |
| Imaging / Diagnostic Reports | 1 | 15 |
| Interfaces / Integration | 2 | 15 |
| Vitals | 1 | 13 |
| Assessments | 1 | 13 |
| Procedures | 1 | 12 |
| Patient History | 1 | 6 |
| Reference Data | 2 | 6 |

**Strongest coverage**: Lab data (192 fields across 4 tables — `LabOrder`, `LabResult`, `LabSpecimen`, `Patient_Labs`), demographics (99 fields across `Patientinfo`, `HL7_Patient`, `Patient_Relationships`), encounters/clinical notes (94 fields across `Dictations`, `Dictation_Items`, `Dictation_Roles`, `Dictation_ICD`), and insurance (72 fields in `HL7_PatientInsurance`).

**Thinnest coverage**: Patient history (6 fields in `Patient_History`), reference data (6 fields total in `EnumTypes`/`EnumValues`).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patientinfo` (46 fields), `HL7_Patient` (45 fields), `Patient_Relationships` (8 fields) — name, DOB, gender, gender identity, sexual orientation, race, ethnicity, language, contacts, address | Thorough; two complementary demographic tables |
| Encounters / visits | ✅ Covered | `Dictations` (59 fields) — DOS, clinical document, signatures, CPT coding, workflow state; `Dictation_Items` (11 fields) for structured template data; `Dictation_ICD` (22 fields) for encounter diagnoses | Comprehensive encounter representation |
| Problems / conditions / diagnoses | ✅ Covered | `Patient_ProblemList` (21 fields) with ICD codes, description, onset date, status; also `Dictation_ICD` for encounter-level diagnoses | Adequate |
| Medications / prescriptions | ✅ Covered | `Patient_Medications` (39 fields) with RxNorm codes, SIG, dosage, frequency, prescriber info | Good depth |
| Allergies | ✅ Covered | `Patient_MedicationAllergy` (23 fields) with allergy codes, reaction, severity, type | Adequate |
| Immunizations | ✅ Covered | `Patient_Immunizations` (40 fields) + `Patient_ImmunizationDetails` (17 fields) with CVX codes, lot, manufacturer, site, route | Comprehensive; 57 total fields |
| Vitals | ✅ Covered | `Patient_Vitals` (13 fields) | Present but column names not described |
| Lab results | ✅ Covered | `LabOrder` (43), `LabResult` (36), `LabSpecimen` (49), `Patient_Labs` (64) — 192 fields total covering orders, results, specimens, and consolidated patient lab data | Exceptionally thorough |
| Imaging / diagnostic reports | ✅ Covered | `Patient_Imaging` (15 fields) with order requests, results, CPT codes | Present |
| Procedures | ✅ Covered | `Patient_Procedures` (12 fields) with procedure codes, descriptions, dates | Adequate |
| Clinical notes / documents | ✅ Covered | `Dictations.Document` (nvarchar, rich text), `Document` table (20 fields, varbinary), `Attachments` (16 fields, image type) | Rich text + binary documents included |
| Care plans / goals | ❌ Not covered | No care plan or goals table in export | Product may embed care plan content in encounter notes; no discrete care plan data exported |
| Orders / referrals | ⚠️ Partial | `LabOrder` (43 fields) and `Patient_Imaging` (15 fields) cover lab and imaging orders; no general orders or referrals table | Lab/imaging orders present, but general referrals absent |
| Insurance / coverage | ✅ Covered | `HL7_PatientInsurance` (72 fields) — insurer details, group numbers, plan dates, subscriber info, authorization, policy limits, coordination of benefits | Very detailed |
| Claims / billing | ⚠️ Partial | `Dictations.PrimaryCPT`, `Dictation_ICD.Charged` flag, `groups` table with billing configuration (63 fields including billing-related fields). No dedicated claims, charges, payments, or AR tables | **Significant gap**: Product has full RCM (claims submission, ERA, denial management, AlphaCollector AR automation) but export only includes CPT codes on encounters, not the billing lifecycle |
| Payments | ❌ Not covered | No payment, remittance, or ERA tables | Product processes ERA/payments; not exported |
| Consents / directives | ❌ Not covered | No advance directives or consent tables | May be captured in encounter notes or assessments but no discrete data |
| Patient communications / portal messages | ❌ Not covered | No secure messaging or portal communication tables | Product has secure messaging and myHealthPointe portal; messaging data not exported |
| Specialty-specific (geriatric/LTPAC) | ⚠️ Partial | `Patient_Assessments` (13 fields) with assessment codes and value set OIDs; wound data referenced via `Attachments.WoundID`; `Dictation_Items` for template data | Assessments present but thin (13 fields); wound assessment data partially covered via attachments linkage |

**Summary**: 12 of 19 applicable domains are fully covered, 3 are partially covered, and 4 are not covered. The most significant gaps are in claims/billing lifecycle data and secure messaging, both of which are core product capabilities.

## 6. Documentation Quality

**Strengths:**
- Comprehensive table-level coverage: all 36 tables are documented with table descriptions
- Every column has a data type and max length specified (100% structural coverage)
- Glossary of common field patterns aids interpretation of recurring fields
- The landing page clearly distinguishes EHI export from FHIR API
- The export tool generates organization-specific documentation at runtime

**Weaknesses:**
- **Near-total absence of column descriptions**: Only 12 of 912 columns (1.3%) have descriptions, and all 12 are in the `aspnet_Users` table. The remaining 900 columns are documented only by name and type. The prior report's characterization of "brief descriptions for many (but not all) columns" is significantly overstated.
- **No value set documentation**: Fields like `PatientStatus`, `Jobstate`, `CodingState`, `AttachmentType` are integer enums with no documented values. The `EnumTypes` and `EnumValues` tables are exported (good), but undocumented in the PDF.
- **No sample data or example export files**: A developer has no way to see what the delimited files actually look like.
- **No relationship documentation**: No ERD, no foreign key listing, no explicit documentation of how tables relate. Relationships must be inferred from shared column names (PatientID, DictationID, etc.).
- **No machine-readable schema**: PDF only — no JSON Schema, XSD, DDL, CSV data dictionary, or other structured format.
- **Documentation is over 2 years old**: Dated November 2023 for a product that has continued development.

**Developer usability**: A competent developer could reconstruct the data model from the column names and types, but significant inference would be required. Column names like `IN1_CoordBenPriority`, `PCID`, `TigerID`, `ESID`, `pcare`, `hospice` (bit), and `patkey` provide no context without descriptions. The HL7-prefixed naming convention on insurance fields (IN1 segment) helps somewhat for those familiar with HL7v2.

## 7. Overall Assessment

### Classification

**Partial native export**

This is a genuine native data model export — not a C-CDA or FHIR repackaging — that covers most clinical domains well. However, it has two significant limitations: (1) the billing/RCM lifecycle data is absent despite being a major product capability, and (2) the documentation quality is poor, with only 1.3% of columns having descriptions.

### Key Findings

1. **Genuine native export, not a standards repackaging.** The export provides 36 database tables in a delimited flat-file format native to GEHRIMED. The landing page explicitly distinguishes this from their FHIR API. This is a proper (b)(10) implementation in structure.

2. **Billing lifecycle is the biggest content gap.** GEHRIMED includes comprehensive billing/RCM capabilities (claims submission, ERA processing, denial management, AR management with AlphaCollector), but the export contains no claims, payments, remittance, or AR tables. Only CPT codes attached to encounters are exported. This is a meaningful gap for a product whose billing module is a major selling point.

3. **Documentation is almost entirely undescribed at the field level.** Only 12 of 912 columns (1.3%) have descriptions — all in a single table (`aspnet_Users`). The remaining 35 tables provide column names and types but no descriptions, value sets, or relationship documentation. This makes the export significantly harder to use than it needs to be.

4. **Clinical domain coverage is solid.** Demographics, encounters, medications, allergies, immunizations, labs (exceptionally detailed with 192 fields across 4 tables), imaging, procedures, vitals, problem lists, implantable devices, assessments, and insurance are all represented with dedicated tables.

5. **Secure messaging and quality measure data are absent.** The product features secure internal messaging and MIPS/eCQM tracking, neither of which appears in the export.

### Summary Stats

```
Classification:  Partial native export
Export format:   Delimited flat files (one file per table)
Model type:      Native database
Entities:        36 tables
Fields:          912
Descriptions:    1.3% (12 of 912 columns)
Sample data:     No
Bulk export:     Yes (one or more patients)
Domains covered: 12 of 19 fully, 3 partial (15 of 19 at least partially)
```

### Bottom Line

GEHRIMED's EHI export is a structurally sound native database export covering clinical data well, but it falls short in two ways: the billing/RCM lifecycle data is entirely absent despite being a core product capability, and the documentation is extremely thin — 98.7% of columns lack descriptions. A patient would receive most of their clinical data but would miss billing/claims history, secure messages, and quality measure tracking. The single biggest gap is the missing claims and payment data from a product that handles full revenue cycle management.
