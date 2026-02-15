# Brilogy Corporation — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.axeium.com/EHI
- CHPL IDs: 11086
- Product: AXEIUM (version MU3, certified 2022-12-19)

## Navigation Journal

1. **Initial probe:** `curl -sI -L "https://www.axeium.com/EHI" -H 'User-Agent: Mozilla/5.0'` — 301 redirect from `www.axeium.com/EHI` to `axeium.com/EHI` (DNN portal alias redirect), then 200 OK with `text/html`.

2. **Fetched page:** `curl -sL "https://www.axeium.com/EHI" -H 'User-Agent: Mozilla/5.0' -o /tmp/ehi-page.html` — 29,980 bytes. DotNetNuke CMS-based site.

3. **Searched for downloadable files:** Only one document link found:
   - `/Portals/0/Documents/MU3_B10/Schema.pdf` — the EHI export schema

4. **Downloaded Schema.pdf:**
   ```
   curl -sL "https://axeium.com/Portals/0/Documents/MU3_B10/Schema.pdf" -H 'User-Agent: Mozilla/5.0' -o Schema.pdf
   ```
   Verified: `file Schema.pdf` → "PDF document, version 1.5, 62 page(s)", 1,061,219 bytes. Created by Milton Allione using Microsoft Excel 2010 on 2023-10-22.

5. **Took screenshots** of the EHI page in the browser — both viewport and full-page captures show identical content (all content above the fold).

6. **Examined HTML source for hidden content:** The page source contains a commented-out section that previously referenced FHIR Bulk Data Access and C-CDA documents as additional exchange methods. Per the HTML comments, this was removed in v3 (2023-10-25) "per guidance from kendra/sli" — suggesting they deliberately narrowed the page to focus on the native (b)(10) export rather than conflating it with (g)(10) FHIR APIs. This is a positive signal.

7. **Examined Schema.pdf:** Extracted text with `pdftotext` — the PDF is a tabular data dictionary generated from Excel with three columns: TABLE_NAME, COLUMN_NAME, and DATA_TYPE. Contains 94 unique tables and 2,818 column definitions.

## What Was Found

### EHI Export Description (from the page)

The EHI page states:

> EHI Export functionality allows system users to manually initiate an export of health data for one or more patients. The referenced schema identifies the structure and syntax of the EHI export functionality.

> The EHI Tables export contains the electronic health information available in a patient's record in a computable, tab-separated, file format the record layout for which is native to AXEIUM.

> Some electronic health information might not be available in a table format, such as rich text documents or images. This information might be referenced from the EHI Tables, but the actual files can be reviewed in a separate download in the export.

The page also notes that export content can vary based on: deployed applications, software version, external data sources, and site configuration.

### Export Format

- **Tab-separated files** in AXEIUM's native database record layout
- **Supplementary files** for rich text documents and images (referenced from the tab-separated tables)
- This is a genuine (b)(10) native database export, not a FHIR or C-CDA repackaging

### Schema.pdf — Data Dictionary

A 62-page PDF generated from Excel containing the complete schema for the export. Each row lists:
- **TABLE_NAME** — the export table name
- **COLUMN_NAME** — the field name
- **DATA_TYPE** — SQL Server data types (int, varchar, datetime, bit, money, float, decimal, image, char, date)

**94 tables, 2,818 columns** covering the following data domains:

**Patient Demographics & Registration (14 tables):**
mPatient (46 cols), mPatientAdditional (34), mPatientRegistration, mPatientDescriptor, mPatientEmployment, mPatientEthnic, mPatientRace, mPatientFamilyMember, mPatientOtherInformation, mPatientPreference, mPatientRepresentative, mPatientPortal, mPatientUPI, mChart

**Clinical Data (16 tables):**
tExam, tExamHistory, tExamSurvey, tPatientAllergy, tPatientMedicalCondition, tPatientProblemList, tPatientClinicalInfo, tPatientHealthMeasure, mPatientHealthMeasure, tPatientExternalHealthMeasure, mSCBaselinePatientValue, mSCPatient, tPatientWorksheet, tAssessmentScore, tPatientEducationList, tPatientClinicalMeasureDW

**Medications (7 tables):**
tPatientMedication (61 cols), mPatientPrescribedMedicine, tPatientMedicationLog, tPatientMedicationPending (63 cols), tPatientMedicationPrescriptionSent (34), tPatientMedicationReview, tRefill (122 cols)

**Lab & Diagnostics (4 tables):**
tPatientLab, tLabEntry, tLabEntryGYN (44 cols — GYN-specific lab data), tLabObservation

**Immunizations (1 table):**
tPatientImmunization (45 cols)

**Dental (3 tables):**
tExamDentalPlan, tExamTooth, tCBEExam (142 cols — Clinical Breast Exam, likely repurposed for dental/clinical exams)

**Behavioral Health (2 tables):**
tBHTreatmentPlan, tPatientTreatmentPlan

**Pregnancy/Perinatal (3 tables):**
tPregnancy (214 cols — very detailed), mCPSPPatient (CPSP = Comprehensive Perinatal Services Program, 35 cols), mCPSPPatientBillingUnit

**Billing & Financial (10 tables):**
tBillingHeader, tBillingDetail, tBillingHeaderConversion, tBillingDetailConversion, tBillingPaymentDetail, tHCFAHeader (215 cols — HCFA 1500 claim form data), tARReceipt, tARCloseAgingTemp, tARCloseAgingTempDetail, tPrintStatement

**Insurance (2 tables):**
mPatientInsurance, mPatientPayerDescriptor

**Visits & Scheduling (3 tables):**
tVisit (38 cols), tVisitCHDP (186 cols — CHDP/EPSDT visit data), tEvent (60 cols)

**Documents & Imaging (2 tables):**
mScanDocument, mSignature

**Communications (3 tables):**
tEmailMessage, tSMSMessage, tPatientFax

**Referrals & Care Coordination (3 tables):**
tReferralEntry (37 cols), tPatientCase, tPatientCaseManagement

**Administrative (8 tables):**
tCallQueueItem, tTaskItem, tPatientContactActivity, tPatientDisclosure, mPatientReleaseAuthorization, tPatientLog, tPatientPrintObject, tVideoSession, tVideoSessionParticipant

**Financial Assistance (2 tables):**
mPatientNeedyMed, mPatientCDP

**Regulatory/Reporting (2 tables):**
tOSHPDException, tUDSTableInfoTemp

**Other (2 tables):**
mPatientApptTypeFee, tPurchaseOrder, tPatientForm, mPatientNote, tPatientTickle, mPatientChartInformation, mPatientProgram, tPatientAuditLog

## Export Coverage Assessment

### Data Domain Coverage

This is an unusually thorough (b)(10) export for a small vendor. The 94-table, 2,818-column schema covers substantially all of the data domains described in the product research:

**Well-covered domains:**
- **Demographics & registration** — 14 tables with extensive patient data including race, ethnicity, employment, family members, insurance, and program enrollment
- **Clinical encounters** — exam tables, visit records, clinical info, health measures
- **Medications** — 7 tables covering active medications, pending orders, prescriptions sent, refills (122 columns in the refill table alone), medication reviews and logs
- **Lab data** — lab entries, observations, and specialized GYN lab data (cervical screening, STD tracking, HPV, etc.)
- **Allergies** — dedicated table
- **Problem lists/conditions** — both medical conditions and problem list tables
- **Immunizations** — detailed 45-column table
- **Dental** — dental plans and tooth-level charting
- **Behavioral health** — treatment plans (though the product's SIRP workflow and intake assessments may be partially captured here)
- **Pregnancy/perinatal** — extremely detailed: 214-column pregnancy table plus CPSP (Comprehensive Perinatal Services Program) tables with billing units — this reflects the FQHC focus
- **Billing** — comprehensive: HCFA 1500 headers (215 columns), billing details, conversions, payment details, AR receipts, aging data, print statements
- **Insurance** — patient insurance and payer descriptors
- **Documents & images** — scan documents and signatures are referenced in the tables, with the actual files provided separately in the export
- **Referrals** — referral entries and case management
- **Communications** — email, SMS, and fax records
- **Visits** — visit records including CHDP (Child Health and Disability Prevention) visits with 186 columns
- **Regulatory reporting** — OSHPD exceptions and UDS temporary tables

**Domains with possible gaps:**
- **Vision-specific clinical data** — the product research describes refraction, tonometry, gonioscopy, anterior/posterior segment exams. These may be captured in the general `tExam` table structure or `tPatientClinicalInfo`, but there are no vision-specific tables visible in the schema. If vision data is stored in custom exam templates, it may be in generic exam fields rather than dedicated tables.
- **Clinical notes/SOAP notes** — `mPatientNote` is present, and rich text documents are described as separate file downloads. The product's AutoText/SOAP note features likely generate documents captured in `mScanDocument` or the rich text file exports.
- **Assessment scoring detail** — `tAssessmentScore` exists but behavioral health assessments with their custom questionnaire structures may be partially captured.

**Not in scope (correctly absent):**
- System configuration, provider credentialing, template definitions, and workflow queues are appropriately excluded from the export — these are operational, not part of the designated record set.
- The `tPatientAuditLog` table is included in the export, which is actually beyond what's required (audit logs are not EHI), but its inclusion is benign.

### Export Format & Standards

The export uses **tab-separated files in AXEIUM's native database layout** — essentially a structured dump of the application's SQL Server tables. This is:

- **Appropriate for (b)(10):** A native database export is exactly the right approach for exporting "all electronic health information." Unlike a FHIR or C-CDA export that would require mapping every field to a standard (and inevitably lose data), this preserves the full richness of the stored data.
- **Not standardized:** The column names are vendor-specific (e.g., `CPSPCaseManagerID`, `I40CHDPCode`). A receiving system would need the Schema.pdf to interpret the data, plus knowledge of AXEIUM's reference data (e.g., what `ServiceID` maps to).
- **Relational structure preserved:** Tables use foreign keys (e.g., `PatientID`, `ProviderID`, `ChartID`) that link records across tables. Relationships are implicit via shared ID columns but not formally documented (no foreign key documentation in the schema).

### Documentation Quality

**Strengths:**
- The Schema.pdf provides a complete, machine-generated data dictionary covering every table and column in the export
- Data types are specified for every field (SQL Server types)
- The EHI page is clear and concise about the export format and scope
- The vendor clearly understands the (b)(10) vs (g)(10) distinction — they deliberately removed references to FHIR and C-CDA from the page (per HTML comments: "del reference to FHIR and CCD as other methods to extract pt data, per guidance from kendra/sli")

**Weaknesses:**
- **No field descriptions:** The schema lists column names and data types but provides no human-readable descriptions. Many column names are self-explanatory (`FirstName`, `DateOfBirth`) but others are cryptic (`I40CHDPCode`, `BCRCOZMPA`, `mSCBaselinePatientValue`)
- **No value set documentation:** Coded fields (e.g., `ArchiveMethodID`, `BabyGenderCode`, `ClosureReason`) have no documented value sets
- **No foreign key documentation:** Relationships between tables must be inferred from shared column names
- **No sample data or examples:** No sample export files are provided
- **No export instructions beyond "contact Customer Support"**

### Structure & Completeness

- **Granularity:** Field-level with data types — this is more than table-level documentation but less than full field-level documentation (missing descriptions)
- **Completeness:** 94 tables × 2,818 columns is comprehensive. The largest tables (tHCFAHeader at 215 cols, tPregnancy at 214 cols, tVisitCHDP at 186 cols) reflect the product's FQHC specialization
- **Versioning:** The HTML source comments show version history (v1 2023-10-01, v2 2023-10-24, v3 2023-10-25). The Schema.pdf creation date is 2023-10-22
- **No formal schema file:** The schema is only available as a PDF, not as a machine-readable format (e.g., SQL DDL, JSON Schema, CSV). The PDF was generated from Excel, suggesting the underlying spreadsheet exists but is not published

### Overall Assessment

Brilogy/AXEIUM has done genuine (b)(10) work. This is a real native database export — not a repackaged FHIR API or a C-CDA summary — covering 94 tables across clinical, financial, administrative, and specialty domains. The vendor demonstrates understanding of the requirement's intent: exporting *everything* the system stores about patients, including specialty data like CPSP perinatal services, CHDP child health visits, and dental charting that would never appear in a USCDI/US Core export.

The documentation could be significantly improved with field descriptions, value set definitions, relationship diagrams, and sample exports. But the schema itself — 2,818 columns across 94 tables — represents one of the more complete (b)(10) exports from a small vendor. The tab-separated native format is practical and preserves all stored data without the lossy transformation required by standardized clinical document formats.

## Access Summary
- Final URL (after redirects): https://axeium.com/EHI
- Status: found
- Required browser: no (curl works for both the page and PDF download)
- Navigation complexity: direct_link (Schema.pdf linked directly from the EHI page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly via both curl and browser. The Schema.pdf downloaded without issues. No authentication, CAPTCHA, or anti-bot measures were encountered.
