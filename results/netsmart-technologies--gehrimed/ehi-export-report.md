# Netsmart Technologies (GEHRIMED) — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.ntst.com/lp/certifications/ehi-all-data-gehrimed
- CHPL ID: 11136
- CHPL Product Number: 15.04.04.2816.gEHR.04.03.1.221227
- Product: GEHRIMED v.4.3
- Certification Date: 2022-12-27

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://www.ntst.com/lp/certifications/ehi-all-data-gehrimed"` returned HTTP 200 with `Content-Type: text/html; charset=utf-8` (174,793 bytes). No redirects.

2. **Page examination** — The page title is "EHI (Electronic Health Information) All Data Export | Netsmart." The page is a static HTML landing page (not a SPA) with a clear heading "EHI (Electronic Health Information) All Data Export for GEHRIMED" and descriptive text about the export.

3. **Link discovery** — Searched the HTML for downloadable files:
   ```
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/netsmart-page.html
   ```
   Found one download link: `/-/media/pdfs/certifications/ehi_export_all-tables_gehrimed_2023.zip`

4. **Downloaded ZIP** —
   ```
   curl -sL "https://www.ntst.com/-/media/pdfs/certifications/ehi_export_all-tables_gehrimed_2023.zip" -o ehi_export_all-tables_gehrimed_2023.zip
   ```
   File verified as `Zip archive data` (619,192 bytes).

5. **Extracted ZIP** — Contains a single file: `EHI Export All Tables - November2023 (GEHRIMED).pdf` (947,078 bytes, 90 pages).

6. **Examined PDF** — Used `pdfinfo` and `pdftotext` to analyze. The PDF is a Word-generated document authored by "Mikolajczak-Brown, Allie" dated November 8, 2023. It contains a data dictionary with 35 database tables and 876 columns documenting the complete EHI export schema.

7. **Took screenshots** of the landing page for the archive.

## What Was Found

### Landing Page Content

The landing page clearly describes the EHI export as a **manual one-time export of health data for one or more patients**, distinct from the vendor's FHIR API and other integration options. Key text:

> "The EHI Tables export contains the electronic health information available in a patient's GEHRIMED record in a computable, delimited file format native to GEHRIMED. Each table will be exported to its own file with a filename matching the table name outlined in the documentation."

The page explicitly distinguishes the EHI export from the vendor's FHIR APIs:

> "This schema is intended for EHI export functionality. If you are working with a Netsmart customer and want to understand different options on integrating with our solutions, please visit our Netsmart Developer Portal for documentation regarding our FHIR API's and connection information."

The page also notes caveats:
- Content may vary based on the organization's version of GEHRIMED
- Configuration decisions and customizations affect content
- Some electronic health information (rich text documents, images) "might not be available in a table format" but is "referenced in the extracts created for subsequent export"

### Data Dictionary (PDF, 90 pages)

The PDF documents **35 database tables** with **876 columns**. Each table includes:
- Table name and description
- Column name, data type (`ColumnType`), and max length for every field
- Brief descriptions for many (but not all) columns

The document begins with an Overview section and a Glossary of Terms explaining common field patterns (Id, PatientID, LastModifiedBy, DictationID, etc.).

#### Tables Documented

| Table | Description | Key Fields |
|-------|------------|------------|
| aspnet_Users | User account information | UserId, UserName, Firstname, LastName, email, Signature, NPI-related fields |
| Attachments | Patient attachments | FileName, FileExtension, ActualFile (image type), WoundID, PatientID |
| Companyinfo | Facility/company information | Company details, BillingReportEmail, billing report configs |
| Dictation_ICD | Encounter diagnosis/problem list | ICDCode, ICD10, Dictation_CPT_ID, Charged, HCCFactor, DiagnosisText |
| Dictation_Items | Encounter template data | DictationID, data (clinical content), notes |
| Dictation_Roles | Encounter roles | (small table) |
| Dictations | Core encounter records | PatientID, DOS, Document (rich text), PrimaryCPT, CodingState, signatures, QA workflow |
| Document | Document storage | Doc (binary), DocFileName, PageCount, HashCode |
| EnumTypes | Enum type definitions | (reference table) |
| EnumValues | Enum value definitions | (reference table) |
| groups | Practice group info | NPI, TaxID, BillingICD, Billing_HL7InterfaceID, billing config fields |
| HL7_Patient | Patient demographics (HL7 format) | Extensive: name, DOB, SSN, address, phone, race, ethnicity, language, marital status, religion, PCP, etc. |
| HL7_PatientInsurance | Insurance information | Extensive: insurer details, group numbers, plan dates, subscriber info, authorization, policy details |
| Interfaces | Integration interfaces | Connection info |
| Interfaces_Outbound | Outbound interfaces | Connection config |
| LabOrder | Lab orders | OrderNumber, CPTCode, specimen info, ordering provider |
| LabResult | Lab results | TestName, Result, ResultUnit, NormalRange, AbnormalFlag, ObservationDate |
| LabSpecimen | Lab specimens | Specimen details, collection info |
| Patient_Assessments | Clinical assessments | AssessmentCode, ResultCode, ValueSetOID, Comment |
| Patient_History | Patient history | (family/social/medical history) |
| Patient_Imaging | Imaging orders | OrderRequest, OrderResults, CPTCode, Instructions |
| Patient_ImmunizationDetails | Immunization detail | CVXCode, lot, manufacturer, site, route |
| Patient_Immunizations | Immunization records | VaccineName, AdministeredDate, refusal info |
| Patient_Labs | Lab records (consolidated) | TestName, Result, ResultUnit, NormalRange, AbnormalFlag, SpecimenType, 60+ columns |
| Patient_MedicationAllergy | Allergies | AllergyCode, Reaction, Severity, AllergyType |
| Patient_Medications | Medications | MedicationName, RxNormCode, SIG, Dosage, Frequency, prescriber info |
| Patient_ProblemList | Problem list | ICDCode, ICD10, Description, OnsetDate, Status |
| Patient_Procedures | Procedures | ProcedureCode, Description, DateOfService |
| Patient_Relationships | Patient contacts/relationships | Name, RelationshipTypeID |
| Patient_Schedule | Scheduling | (appointment data) |
| Patient_Vitals | Vital signs | (vital sign measurements) |
| PatientImplantableDevice | Implantable devices | UDI info, device identifiers |
| Patientinfo | Core patient demographics | Name, DOB, Gender, GenderIdentity, SexualOrientation, Race, Ethnicity, facility, status |
| Patientinfo_Smoking | Smoking status | SmokingStatusID, cessation info |
| SmokingCessation | Smoking cessation reference | Description values |
| SmokingStatus | Smoking status reference | Description, SNOMEDCode |

### Export Format

- **Format**: Delimited flat files (one file per table), native to GEHRIMED
- **Not FHIR**: The export is explicitly a database table dump, not a FHIR or C-CDA export
- **Rich text and images**: Referenced in the table extracts but may not be directly inline — the Attachments table includes an `ActualFile` column of type `image` suggesting binary content is included, and the Document table has a `Doc` column of type `varbinary`
- **File naming**: Each exported file matches the table name in the documentation

## Export Coverage Assessment

### Data Domain Coverage

**Well-covered clinical domains:**
- **Demographics**: Comprehensive via `Patientinfo` and `HL7_Patient` tables — name, DOB, gender, gender identity, sexual orientation, race, ethnicity, preferred language, address, contact info
- **Encounters/clinical notes**: `Dictations` table with rich text Document field, date of service, signatures, QA workflow; `Dictation_Items` for structured template data
- **Diagnoses**: `Dictation_ICD` (encounter-level) and `Patient_ProblemList` (longitudinal) — both with ICD-10 codes
- **Medications**: `Patient_Medications` with RxNorm codes, dosage, SIG, frequency
- **Allergies**: `Patient_MedicationAllergy` with coded allergies and reactions
- **Lab orders and results**: `LabOrder`, `LabResult`, `LabSpecimen`, `Patient_Labs` — comprehensive with test names, results, units, normal ranges, abnormal flags, specimen data
- **Immunizations**: `Patient_Immunizations` and `Patient_ImmunizationDetails` with CVX codes
- **Vital signs**: `Patient_Vitals`
- **Procedures**: `Patient_Procedures` with procedure codes
- **Imaging**: `Patient_Imaging` with orders, results, CPT codes
- **Assessments**: `Patient_Assessments` with coded assessments and value set OIDs
- **Implantable devices**: `PatientImplantableDevice`
- **Insurance**: `HL7_PatientInsurance` — very detailed with plan, subscriber, and policy information
- **Attachments/documents**: `Attachments` (with actual file content), `Document` (with binary document storage)
- **Patient relationships/contacts**: `Patient_Relationships`
- **Smoking status**: `Patientinfo_Smoking`, `SmokingCessation`, `SmokingStatus` with SNOMED codes
- **Patient history**: `Patient_History`
- **Scheduling**: `Patient_Schedule`

**Partially covered / notable observations:**
- **Billing/charges**: The export includes `PrimaryCPT` on `Dictations`, `Charged` flag and `Dictation_CPT_ID` on `Dictation_ICD`, and `CPTCode` on `Patient_Imaging` and `LabOrder`. The `groups` table has billing configuration fields. However, there are **no dedicated claims, charges, payments, or accounts receivable tables**. Given that GEHRIMED includes a full billing/RCM module (AlphaCollector, claims submission/tracking, ERA processing, denial management, AR management), the absence of claims-level billing data from the export is a notable gap. The export captures CPT codes tied to encounters but not the downstream billing lifecycle (claims submitted, payments received, denials, adjustments).
- **E-prescriptions**: Medications are documented but the Dr. First e-prescribing integration data (PDMP results, real-time benefit checks, prescription transmission details) is not explicitly represented as a separate table. Prescription data likely flows through `Patient_Medications`.
- **Secure messages**: The product supports secure internal messaging, but there is no messages/messaging table in the export.
- **MIPS/quality measures**: The product tracks MIPS data and eCQMs, but no quality measure tracking tables appear in the export.
- **Care plans/goals**: No explicit care plan or goal table, though clinical plan content may be embedded in encounter notes (Dictations.Document).
- **Advance directives**: Not represented as a separate table, though they may be captured in assessments or encounter notes.

**Missing domains (relative to product capabilities):**
- **Claims/billing lifecycle data** — GEHRIMED stores claims, remittances, AR data, and denial management information. None of this appears in the export.
- **Secure messaging** — internal messaging is a documented product feature but absent from the export.
- **MIPS/quality tracking** — reported as a key feature but not exported.

### (b)(10) vs (g)(10) Assessment

This is a **genuine (b)(10) implementation**. Netsmart has clearly distinguished the EHI export from their FHIR API:
- The export is a native database table dump, not FHIR
- The landing page explicitly separates EHI export from the FHIR Developer Portal
- The data dictionary reflects the actual database schema, not USCDI/US Core mappings
- Coverage extends well beyond the USCDI data classes (includes insurance, attachments, imaging orders, lab specimens, etc.)

This is one of the better (b)(10) approaches seen — it exports the raw data model rather than trying to repackage a FHIR API.

### Export Format & Standards

- **Format**: Proprietary delimited flat files — one file per database table
- **Standard**: None — this is a direct database export, not mapped to any interoperability standard
- **Relationships**: Tables are linked by foreign keys (PatientID, DictationID, GroupID, etc.) documented in the glossary. A developer could reconstruct relationships from the ID columns, though there is no formal schema file (no XSD, JSON Schema, or ERD).
- **Appropriateness**: For LTPAC physician practice data, a database dump is appropriate. FHIR US Core would miss much of the specialty-specific content. The format reasonably captures the breadth of clinical data.
- **Reconstruction**: A competent developer could reconstruct most of a patient record from these tables, though the lack of an explicit relationship diagram and incomplete column descriptions would require some inference.

### Documentation Quality

**Strengths:**
- Comprehensive table-level and column-level documentation for all 35 tables
- Every column has a data type and max length
- Glossary of common field patterns helps interpretation
- Clear distinction between EHI export and other integration options
- Honest caveats about content variation across deployments

**Weaknesses:**
- Many columns lack descriptions — you get `Column Name: PriorityLevel / ColumnType: tinyint` with no explanation of what the values mean
- **No value set documentation** for coded fields — EnumTypes and EnumValues tables are included in the export (which is good), but the documentation doesn't enumerate what enum values exist for fields like Status, JobState, UserType, etc.
- No sample data or example export files
- No relationship/ERD diagram showing how tables connect
- No machine-readable schema (no XSD, JSON Schema, DDL, or similar)
- PDF-only format — no CSV data dictionary, no HTML, no structured format
- Documentation dated November 2023 for a product certified December 2022 — reasonably current but over 2 years old now

### Structure & Completeness

- **Granularity**: Column-level documentation with types and lengths — good structural detail
- **Coded fields**: Enum/reference tables (EnumTypes, EnumValues, SmokingStatus, SmokingCessation) are included in the export itself, which partially compensates for the lack of value set documentation in the PDF
- **Relationships**: Documented implicitly through shared ID columns (PatientID, DictationID, GroupID) and the glossary. No explicit foreign key documentation or ERD.
- **Versioning**: Dated November 2023, no change history

## Access Summary
- Final URL (after redirects): https://www.ntst.com/lp/certifications/ehi-all-data-gehrimed
- Status: found
- Required browser: no (curl works fine)
- Navigation complexity: one_click (single "CLICK HERE" link to ZIP)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly, the ZIP downloaded without issues, and the PDF extracted correctly. This was one of the most straightforward EHI documentation pages encountered.
