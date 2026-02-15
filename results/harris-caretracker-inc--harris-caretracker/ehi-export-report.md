# Harris CareTracker, Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://harriscaretracker.com/wp-content/uploads/2024/02/CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf
- CHPL ID: 9589
- Product: Harris CareTracker, Version 9
- Certification date: 2018-07-01

## Navigation Journal

The registered URL is a direct PDF download hosted on the vendor's WordPress site.

```bash
curl -sI -L "https://harriscaretracker.com/wp-content/uploads/2024/02/CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf" -H 'User-Agent: Mozilla/5.0'
```

Response: HTTP 200, `Content-Type: application/pdf`, `Content-Length: 177610` (174 KB). No redirects, no anti-bot measures. The file was created 2023-11-15 by author "Kathiresan Palanisamy" using Acrobat PDFMaker 15 for Word. 8 pages.

Downloaded directly:
```bash
curl -sL "https://harriscaretracker.com/wp-content/uploads/2024/02/CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf
```

Verified: `file` confirms "PDF document, version 1.5". Text extraction via `pdftotext` produced clean, structured output.

## What Was Found

The document is titled **"CareTracker EHI Export: Folder Organization and Data Format Specification — v1.0"** and describes a comprehensive, custom file-based export system.

### Export Mechanism

The export supports two scenarios:
1. **Single patient export** — export all data for one patient
2. **Patient population export** — select patients by Provider, All Active Patients, All Patients, or Patients within an Encounter Range

For each patient, a dedicated folder is created (timestamped for identification). Inside, data is organized by **Data Class**, with each class exported as a file named `[Data Class Name].[Export Format]`.

### Export Formats

Three machine-readable formats are supported:
- **CSV** (Comma-Separated Values)
- **JSON** (JavaScript Object Notation)
- **XML** (Extensible Markup Language)

A dedicated "Documents" subfolder stores imported items, images, and related documents in their original storage/import format.

### Data Classes Documented

The PDF lists 38 distinct Data Classes, each with explicit column headings:

| # | Data Class | Notable Content |
|---|-----------|----------------|
| 1 | Addendum | Clinical note addenda |
| 2 | Advance Directives | Directive names, codes, paths to documents |
| 3 | Alerts | Medical alerts (same structure as advance directives) |
| 4 | Allergies and Intolerances Pending | Pending allergy entries with full detail |
| 5 | Allergies and Intolerances | Confirmed allergies with severity, reactions, dates |
| 6 | Assessments | Encounter-level clinical assessments |
| 7 | Billing History | **Very detailed**: place of service, CPT codes, ICD codes (up to 12), fees, charges, NDC codes, modifiers, prior auth, referring/billing provider details, facility info |
| 8 | Care Team Members | Team roles, status, contact info |
| 9 | Clinical Notes | **Extremely detailed**: chief complaint, HPI, ROS, PMH, meds, allergies, social/family history, physical exam, assessment, plan, vitals, tobacco use, pregnancy, vision, hearing, encounter type, images, illustrations, SNOMED codes |
| 10 | Demographic Immunization | Immunization-specific demographic data, VFC, registry consent |
| 11 | Email | Patient communications with full body text |
| 12 | Family History | Multi-level: patient-level flags, per-relation details, per-diagnosis with SNOMED/ICD-10 |
| 13 | Functional Status | Mental/functional status entries |
| 14 | Goals | Patient goals per encounter |
| 15 | Health Concerns | Per-encounter health concerns |
| 16 | Health Insurance | **Detailed**: policy/group numbers, payer/plan info, subscriber and guarantor demographics |
| 17 | HM Rules Ignored | Health maintenance rules that were declined/ignored |
| 18 | HM Rules / Immunizations | Health maintenance with full rule metadata, vaccine details, VIS info, manufacturer, lot, route, site, registry submission dates |
| 19 | Implantable Device | UDI data, manufacturer, lot/serial, MRI safety, HCT/P codes |
| 20 | Imported Items | External documents imported into chart, with paths and sign-off tracking |
| 21 | Injections | Administration details with NDC codes |
| 22 | Lab Tests | **Very detailed**: order-level, result-level, and result-detail-level data; LOINC codes, specimen info, abnormal flags, reference ranges, performing lab info, notes |
| 23 | List Problem Pending | Pending problems with ICD/SNOMED/COSTAR codes |
| 24 | List Problem | Active problems with full coding |
| 25 | Medications Pending | Pending medication entries |
| 26 | Medications | **Detailed**: prescribing info, pharmacy details, e-prescribing status, DAW, NDC, compound med details, scheduling |
| 27 | Next Of Kin | Emergency contacts and guardians |
| 28 | Occupation and Industry History | NAICS codes, SOC codes, census codes |
| 29 | Orders | Clinical orders with tracking, status, CPT/ICD codes |
| 30 | Patient Demographics | **Comprehensive**: full demographics including SSN, employer, emergency contact, race/ethnicity, language, sexual orientation, gender identity, aliases, previous addresses |
| 31 | Patient Generated Data | Patient-submitted data |
| 32 | Patient Health Information Capture | Medical alerts, directives with type/level metadata |
| 33 | Patient Record Release | Release tracking including authorization, recipient, referral info |
| 34 | Plan of Treatment | Per-encounter treatment plans |
| 35 | Procedures | CPT-coded procedures with fees and charges |
| 36 | Referrals | Referral tracking with dates, visit counts |
| 37 | Risk Factors | Patient risk factors |
| 38 | Scheduling | Appointment data including telehealth flag |
| 39 | Smoking Statuses | Tobacco use history with SNOMED codes |
| 40 | Tracked Data | Generic tracked items (item/value pairs) |
| 41 | Travel History | Travel records for public health |
| 42 | User Defined Fields | Custom field data per template |
| 43 | Vital Signs | Full vital sign panels |

## Export Coverage Assessment

### Data Domain Coverage

This is a notably comprehensive export for an ambulatory EHR/PM product. The export addresses data domains well beyond the typical USCDI/US Core clinical subset:

**Well covered:**
- **Clinical data**: Problems, medications, allergies, vital signs, lab results, immunizations, clinical notes, assessments, plans of treatment, goals, health concerns, functional status, smoking status, family history, advance directives, implantable devices — all with field-level detail
- **Billing/financial data**: The Billing History class is remarkably detailed with CPT codes, ICD codes (up to 12 per claim), fees, charges, NDC codes, modifiers, prior authorization, billing/referring provider details, and facility information. This is rare — most EHI exports omit billing entirely.
- **Insurance data**: Health Insurance class includes policy details, payer/plan information, subscriber and guarantor demographics
- **Scheduling data**: Appointments with telehealth flags and booking metadata
- **Administrative data**: Patient demographics (comprehensive including SSN, employer, race/ethnicity, language, sexual orientation, gender identity), next of kin, patient record releases
- **Communications**: Email correspondence between providers and patients
- **Documents**: Imported items exported in original format, with sign-off tracking
- **Occupational data**: Occupation and industry history with NAICS/SOC codes
- **Travel history**: For public health reporting purposes
- **Custom data**: User-defined fields and tracked data capture practice-specific information
- **Health maintenance**: Both rule compliance and ignored rules, providing audit context

**Potentially missing or unclear:**
- **Audit logs**: No explicit audit trail or access log data class. The product stores user activity (who entered/edited records is tracked in many fields), but a dedicated audit log export is absent.
- **Patient portal activity**: Email messages are exported, but portal-specific interactions (login history, document views, appointment requests, prescription renewal requests, online payments) appear absent as discrete data classes.
- **Claims adjudication data**: While billing is covered, there's no explicit ERA/remittance data class or denial management data, which the product tracks per the research.
- **Collections data**: The product has a collections module, but no dedicated collections data class appears in the export.
- **Practice analytics/reporting data**: Dashboards, eCQM results, and MIPS/MVP submission data are not represented.
- **Patient satisfaction surveys**: Data from InteliChart integration is not mentioned.
- **Automated communication logs**: CareTracker Connect/Connect Pro automated messages (SMS/email/voice reminders) are not in the export.
- **Telehealth session data**: Scheduling has a telehealth flag, but no session/encounter-specific telehealth data appears.

### Export Format & Standards

The export uses a **proprietary, vendor-defined flat-file format** — not FHIR, not C-CDA, not any recognized healthcare standard. This is entirely appropriate for a (b)(10) export. The three format options (CSV, JSON, XML) with consistent column naming provide good flexibility.

This is clearly a purpose-built (b)(10) export, not a repackaged (g)(10) FHIR API. Key indicators:
- The data classes are vendor-specific, not FHIR resource types
- Billing data is prominently included — FHIR US Core doesn't cover billing
- Column names reflect internal data model naming (e.g., "COSTAR" codes, "QuickAddWhoPrescribed")
- The export includes pending items (pending allergies, pending medications, pending problems) as separate classes — this represents in-progress clinical workflow state
- No mention of FHIR, US Core, or USCDI anywhere in the document

The folder-per-patient structure with timestamped folders and Data Class-named files is practical and navigable. Relationships between entities are implicit via PatientID (present in every class) and EncounterDate fields, but there are no explicit foreign keys or relationship documentation.

### Documentation Quality

**Strengths:**
- Clear, well-structured document with consistent formatting
- Every data class lists its complete set of column headings
- The introductory text clearly explains the folder structure and naming conventions
- Export supports both single-patient and population-level export with flexible selection criteria
- Three format options (CSV, JSON, XML) accommodate different consumer needs

**Weaknesses:**
- **No data type information**: Column headings are listed but data types (string, date, integer, boolean, etc.) are not specified
- **No value set documentation**: Coded fields (e.g., Chronicity, ERXstatus, DispenseAsWritten, TobaccoUseName) don't document their allowed values
- **No field descriptions**: Column names are generally self-explanatory but some are opaque (e.g., "COSTAR", "NP001Description", "NP001FriendlyName", "XLinkProviderID", "Miscellaneous1-4")
- **No sample data or examples**: No worked examples showing what an actual export looks like
- **No cardinality documentation**: The relationship between classes (one-to-many, many-to-many) is not specified
- **No schema files**: No machine-readable schema (XSD, JSON Schema, CSV header spec)
- **Typos present**: "Assesments" (sic), "Signetur" (sic), "OrderTypeDescriptin" (sic), "BillingProvideerState" (sic), "ReferProvideerState" (sic) — these suggest the column headings may reflect actual field names in the export files
- **No versioning or change history**: Document is v1.0 with no changelog

A developer could parse the export files using these column headings, but implementing a robust import would require trial-and-error to determine data types, handle coded values, and understand field semantics for the more obscure columns.

### Structure & Completeness

The documentation provides **field-name-level granularity** across all 38+ data classes but stops there. It is essentially a column listing — useful for understanding the breadth of the export, but insufficient as a complete data dictionary. The absence of data types, value sets, descriptions, and relationships means this is a field inventory, not a specification.

That said, the field names are largely self-descriptive and follow consistent patterns (e.g., `FirstName`/`LastName` pairs, `Date*` prefixes for dates, `Is*` prefixes for booleans). An experienced developer could make reasonable inferences about most fields.

## Access Summary
- Final URL (after redirects): https://harriscaretracker.com/wp-content/uploads/2024/02/CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL was a direct, publicly accessible PDF download with no authentication, redirects, or anti-bot measures. The file downloaded and extracted cleanly.
