# PCIS GOLD — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://fhir.pcisgold.com/ehiexport/
- CHPL IDs: 11137
- Product: PCIS GOLD EHR v2.6
- Developer: PCIS GOLD (DHI Computing Service, Inc.)
- Certification date: 2022-12-22

## Navigation Journal

**Step 1: Initial probe**
```bash
curl -sI -L "https://fhir.pcisgold.com/ehiexport/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html, 534,594 bytes. Microsoft-IIS/10.0 server. No redirects — the URL served content directly.

**Step 2: Fetch and examine**
```bash
curl -sL "https://fhir.pcisgold.com/ehiexport/" -H 'User-Agent: Mozilla/5.0' -o ehi-export-data-table-definitions.html
```
The page is a single, self-contained HTML document titled "EHI Export Data Table Definitions." It contains a complete data dictionary for the EHI export, with no external links to additional documentation, no downloadable files (PDF, ZIP, etc.), and no links to FHIR APIs or other standards documentation.

**Step 3: Search for additional artifacts**
No downloadable files (PDF, ZIP, CSV, JSON, XLSX) were linked from the page. No links to external documentation, FHIR endpoints, or additional pages. The page is entirely self-contained.

**Step 4: Screenshot**
Took a browser screenshot of the page for the record. The page renders as a clean HTML document with a table-of-contents index at the top, followed by 309 table definitions.

## What Was Found

The registered URL hosts a **comprehensive data dictionary** for PCIS GOLD's EHI export. The documentation describes a **tab-delimited file export** — not a FHIR API, not a C-CDA export, not a standardized format. This is a genuine (b)(10) export of the product's underlying database tables.

### Export Format
The introductory text states:

> "The EHI Export zip file contains a file for each of the following data tables. The individual files are formatted using tab-delimited fields. The fields are defined for each of the data tables below. The EHI Export zip file also contains a folder named *Files* that contains related patient files. The files are named with an identifier that matches the Id field in the EHI_T_BlobData data table."

Key format details:
- **Format**: ZIP archive containing tab-delimited text files, one per table
- **Attached files**: A `Files/` folder in the ZIP contains binary attachments (documents, images, etc.) referenced by the `T_BlobData` table
- **Number of tables**: 309
- **Total fields documented**: 4,481

### Export Mechanism
The documentation describes how to run the export:

> "A patient EHI export can be run by using the EHI Export tool from the tools menu and using the Add Patient button to search for and select one or more patients. An export for a patient population can be done by using the EHI Export button on the patient queries screen."

This indicates both single-patient and population-level export capabilities, initiated from within the EHR application.

### Data Dictionary Structure
Each table definition includes:
- **Table name** (e.g., `T_Patients`, `Trans`, `Allergy_Antigen`)
- **Table description** (brief, e.g., "Clinical Patient List", "Account Transactions")
- **Field list** with three columns per field:
  - **Name**: Column/field name
  - **Type**: SQL data type (int, varchar, datetime, binary, bit, etc.)
  - **Description**: Human-readable description of the field

The documentation uses two naming conventions reflecting the product's evolution:
1. **Legacy tables** (e.g., `Accounts`, `Trans`, `Visits`): Use abbreviated 4-6 character field names like `ACINST`, `TDTYPE`, `ASACOND` — reminiscent of IBM AS/400 or legacy mainframe naming
2. **Newer tables** (prefixed `T_`): Use descriptive names like `PatientId`, `StartDate`, `Description`

### Document Metadata
- **Last Updated**: 10/27/2023 1:21:38 PM
- This is roughly 10 months after the product's certification date (December 2022), suggesting the documentation has been maintained post-certification.

## Export Coverage Assessment

### Data Domain Coverage

This is an exceptionally thorough EHI export. The 309 tables span virtually every data domain the product manages, going far beyond USCDI/US Core. Here is a domain-by-domain assessment:

**Clearly covered:**
- **Demographics & patient identity**: `T_Patients` (42 fields), `Patients` (legacy, 71 fields), demographics tables for ethnicity, race, gender identity, sexual orientation, language, plus `T_PatientAddress`, `T_PatientPhones`, `T_PatientEmergencyContact`, `T_PatientNextOfKin`
- **Allergies**: `T_PatientAllergy` (21 fields), `T_PatientAllergyReactions`, `T_PatientAlertAllergies` — plus an extensive allergy immunotherapy module with 20 tables covering antigens, concentrations, vials, skin tests, mixing lab records, and treatment schedules
- **Medications & e-prescribing**: `T_PatientMedication` (72 fields), `T_PatientERxDetails`, `T_PatientErxChange`, `T_PatientErxCancelDetails`, `T_PatientMedicationSigChange`, `T_PatientRxHistory`, `T_PatientPrintRxDetails`, `T_RenewalRequests`
- **Problems/diagnoses**: 7 tables including `Problem_Problem`, `Problem_Codes`, `Problem_CodeTypes`, `Problem_Group`, `Problem_Links`, `Problem_External`, `Problem_ProblemSeverity`
- **Lab results**: `Lab_CompletedOrders`, `Lab_CompletedTests`, `Lab_CompletedObservations`, `Lab_CompletedTestsLinks`, `Lab_TestComments`, `Lab_TestViews`
- **Vitals**: 20 tables covering vital signs data, templates, modifiers, conditions, and unit types
- **Immunizations**: 8 tables including `T_PatientImmunizations`, evaluation/forecast data, VIS records, registry info, and manufacturer references
- **Visits/encounters**: 48 tables — the largest domain. Covers visit notes, addenda, amendments, sections, diagnoses, procedures, HPI data, physical exam data, vital modifiers, attachments, ink/sketch data, checkout workflows, and more
- **Clinical notes**: `T_VisitNote`, `T_VisitNoteAddendum`, `T_VisitNoteAmendment`, `T_VisitNotesSection`, `T_VisitDataSectionText`, `T_PatientSectionNotes`
- **Procedures/CPT codes**: `T_VisitProcedures` (27 fields) with CPT codes, modifiers, diagnosis links, standing orders
- **Orders**: `Orders` (legacy), `T_OrderTracking`, `T_OrderTrackingStatus`, `T_OrderTrackingComment`, `T_OrderTrackingLinks`
- **Billing & financial**: `Trans` (156 fields — the largest table), `AllocatedTrans`, `ClaimHistory`, `EOBRecs`, `EstimateDtl`, `EstimateHdr`, `Statements`, `PaymentPlans`, `DunningMessages`
- **Insurance**: `T_Insurance` reference table, plus insurance fields within patient and account records
- **Family history**: 7 tables covering conditions, persons, relationships, and patient-specific family history
- **Referrals**: 8 tables covering referral tracking, status, comments, and links
- **Implantable devices**: `T_PatientImplantableDevice`, `T_VisitImplantableDeviceIncludeInNote`
- **Documents & attachments**: `T_BlobData` (23 fields), `T_BlobData_Category`, plus the `Files/` folder in the export ZIP for binary content
- **Patient portal & messaging**: `T_PatientPortalInfo`, `T_PatientPortalMessages`, `T_CommunicationPreferences`
- **E-tasking / internal messaging**: 7 tables covering task items, recipients, senders, statuses, and HR links
- **Screening & assessments**: `PatientScreening`, `PatientScreeningAnswer`, `ScreeningDef`, `ScreeningQuestionChoice`, `ScreeningQuestionDef`
- **Cognitive & functional status**: `T_PatientCognitiveStatus`, `T_PatientFunctionalStatus`
- **Cancer/oncology**: 5 tables — `T_PatientCancerDiagnosis`, `T_PatientCancerEvent`, planned encounters, meds, and procedures
- **Ophthalmology/eye care**: 14 tables covering IOP, refraction, keratometry, visual acuity, contact lenses, dilation, current Rx, ocular history — reflecting the product's use by eyecare practices
- **Custom data**: `ColBased_*` tables (5 tables) providing a column-based extensibility mechanism for custom clinical data collection including images
- **Flowsheets**: `T_Flowsheets`, `T_FlowsheetColumns`, `T_FlowsheetHistory`, `T_FlowsheetComments`
- **Transitions of care**: `TOC_Entries`, `TOC_Attachments`, `TOC_EntryComments`, `T_PatientTransitionsOfCare`
- **Information release**: `InfoRelease`, `InfoReleaseDetail`
- **Fax**: `T_Faxes`, `T_FaxStatus`
- **Device integration**: `MidmarkReportInfo`, `MidmarkReportsBlobData` (Midmark clinical device data)
- **Smoking status**: `T_SmokingStatus`
- **Patient education**: `T_PatientEducationDocuments`
- **Patient forms**: `PatientFormResponse`, `PatientFormResponseQuestions`
- **Record requests**: `T_PatientRecordRequests`, `RecordRequest_Methods`
- **HIPAA**: `PatientHIPAA`
- **Patient consent**: `Demo_PatConsent`

**Not explicitly present but likely covered through other mechanisms:**
- **Radiology results**: The product has `T_VisitRadOutboundInfo` for outbound radiology info, and imaging reports may be stored as blob data in `T_BlobData`. Lab-side results appear in `Lab_CompletedTests`.
- **Patient education content**: `T_PatientEducationDocuments` tracks which education was provided.

**Absent but not necessarily required:**
- No audit log tables (correctly excluded — these are not part of the designated record set)
- No system configuration tables (correctly excluded)
- No scheduling/appointment tables — these are operational/administrative and generally not part of the designated record set. The export captures the visit itself (`T_Visits`) rather than the scheduling workflow leading to it.

### Export Format & Standards

The export format is a **vendor-specific tab-delimited flat file dump** with a companion folder for binary attachments. This is not a standardized format (not FHIR, not C-CDA, not HL7v2), but it is entirely appropriate for (b)(10) compliance. Key characteristics:

- **Relationships between tables** are maintained through integer foreign keys (e.g., `PatientId`, `VisitId`, `AccountId`). The data dictionary documents these relationships informally through field descriptions (e.g., "The visit ID for visit procedures") rather than through a formal schema or ERD.
- **Data types** are SQL-native types reflecting the underlying database: `int`, `varchar`, `datetime`, `binary`, `bit`, `decimal`, etc. The mix of `Character`/`Binary`/`Number` (legacy tables) and `int`/`varchar`/`datetime` (newer tables) reflects two database systems — likely an AS/400 backend for practice management and a SQL Server backend for the EHR clinical module.
- **Binary attachments** (documents, images, scribble drawings) are exported as actual files in a companion folder, linked by the `T_BlobData.Id` field. This is a practical approach that preserves binary content without base64 encoding.
- A third party could reconstruct a patient record from this export, though it would require understanding the foreign key relationships and value coding. The documentation provides enough context for most tables, though some abbreviated legacy field names (e.g., `TDTYPE` = "TRANSACTION TYPE (C,P,A, T)") leave the value domain underspecified.

This is **not** a (g)(10) FHIR export repackaged as (b)(10). The vendor has done genuine (b)(10) work: they export their internal database structure with all its domain-specific tables, not a filtered view through FHIR US Core resources.

### Documentation Quality

**Strengths:**
- The documentation is comprehensive — 309 tables, 4,481 fields, covering all major data domains
- Every table has a description (though some are terse)
- Every field has a name, SQL data type, and description
- The HTML format is clean, well-structured, and navigable with a table-of-contents index
- The introductory text clearly explains the export format, file structure, and how to run the export
- The documentation has been updated post-certification (October 2023 vs December 2022 certification)

**Weaknesses:**
- **No formal schema**: There is no machine-readable schema (XSD, JSON Schema, DDL, ERD). The data dictionary is HTML only. A developer would need to parse the HTML to build an import tool.
- **Abbreviated legacy field names**: Many fields in legacy tables use 4-6 character abbreviations (e.g., `ACINST`, `TDVSIT`, `ASOCCC`) that are not self-documenting. The descriptions help but are sometimes terse (e.g., "KEY-INSTITUTION", "OCCURRANCE CODE").
- **Missing value sets**: Coded fields list their type but not their allowed values. For example, `TDTYPE` is described as "TRANSACTION TYPE (C,P,A, T)" which hints at four codes but doesn't explain what each means. Many bit/flag fields lack documentation of what 0 vs 1 represents.
- **Inconsistent description quality**: Newer T_ tables generally have better descriptions ("The ID of the patient receiving the medication") while legacy tables often have ALL-CAPS terse labels ("KEY-RECORD TYPE - 15"). Some fields have empty descriptions entirely.
- **No sample data or examples**: There are no worked examples, sample export files, or sample records.
- **No explicit relationship documentation**: Foreign keys are inferred from field names and descriptions, not formally documented. A developer would need to figure out that `T_VisitDiags.VisitID` links to `T_Visits.Id` by convention.

### Structure & Completeness

- **Granularity**: Field-level documentation with names, types, and descriptions for all 4,481 fields across 309 tables. This is well above average.
- **Coded field documentation**: Weak. Value sets and code meanings are rarely specified.
- **Relationship documentation**: Implicit only. Foreign keys are recognizable by naming convention but not formally declared.
- **Versioning**: The page has a "Last Updated" timestamp but no change history.

### Overall Assessment

PCIS GOLD has produced one of the more thorough (b)(10) EHI export implementations. Rather than repackaging a FHIR API or exporting a clinical summary, they export their actual database — all 309 tables across clinical, billing, specialty (ophthalmology, allergy immunotherapy, oncology), and administrative domains. The tab-delimited format with companion binary files is pragmatic and complete.

The export appears to cover essentially everything the product stores about patients: demographics, clinical notes, vitals, medications, allergies, labs, procedures, billing transactions, claims, insurance, referrals, family history, immunizations, screening assessments, specialty clinical data (eye care, cancer), custom data fields, documents/attachments, portal messages, and more.

The main limitations are in documentation quality rather than scope: the lack of formal schema, incomplete value set documentation, and abbreviated legacy field names would make it challenging (though not impossible) for a third party to build an automated import. A developer with SQL experience could work with this data, but they would need to invest effort in understanding the relationship model and decoding legacy field names.

For a small vendor (14-28 employees) serving a niche market, this is a notably serious effort at (b)(10) compliance — far more comprehensive than many larger vendors that simply point to their FHIR Bulk Data API.

## Access Summary
- Final URL (after redirects): https://fhir.pcisgold.com/ehiexport/
- Status: found
- Required browser: no (curl works fine)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL returned a 200 OK with the full data dictionary. No redirects, no login wall, no JavaScript required, no anti-bot measures. The page is a clean, static HTML document served from IIS.
