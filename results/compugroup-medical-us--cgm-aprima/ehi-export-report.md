# CompuGroup Medical US — CGM APRIMA — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.cgm.com/usa_en/products/electronic-health-records/cgm-aprima.html
- CHPL ID: 11167
- CHPL Product Number: 15.04.04.2700.Apri.19.01.1.221228
- Certification Date: 2022-12-28

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.cgm.com/usa_en/products/electronic-health-records/cgm-aprima.html" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200 with Content-Type text/html. The URL is the CGM APRIMA product marketing page hosted on a Neos CMS behind Cloudflare.

2. **Page examination**: The 141KB HTML page is the main CGM APRIMA product page with marketing content, feature descriptions, case studies, and a "Certifications" section near the bottom. Searched for downloadable files:
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
   ```
   Found 14 PDF links including the key EHI export documentation.

3. **Found EHI export documentation link**: In the Certifications section (accessible via `#certifications` anchor), under a "CGM APRIMA" accordion, there is a button labeled "EHI EXPORT DOCUMENTATION" linking directly to a PDF:
   ```
   https://www.cgm.com/_Resources/Persistent/5e4d9033152348c8ccb98d51844c94b49aaec1c0/cgm-aprima-electronic-health-information-export-user-guide.pdf
   ```

4. **Downloaded EHI Export User Guide PDF** (327,836 bytes, 28 pages):
   ```bash
   curl -sL "https://www.cgm.com/_Resources/Persistent/5e4d9033152348c8ccb98d51844c94b49aaec1c0/cgm-aprima-electronic-health-information-export-user-guide.pdf" -o cgm-aprima-electronic-health-information-export-user-guide.pdf
   ```
   Verified: PDF document, version 1.7. Author: Jennifer Sandberg. Created: 2023-11-02.

5. **Downloaded FHIR API Documentation Guide PDF** (497,853 bytes, 76 pages):
   ```bash
   curl -sL "https://www.cgm.com/_Resources/Persistent/aaa2e921f29934f6e308b73daadaf3e94a3b21d5/fhir-api-documentation-guide.pdf" -o fhir-api-documentation-guide.pdf
   ```
   Verified: PDF document, version 1.6. Author: McKesson (legacy). Created: 2024-04-26. This is the (g)(10) FHIR API documentation, not the (b)(10) EHI export, but downloaded for completeness.

6. **Checked for additional artifacts**: No embedded files or attachments in the EHI export PDF. The only URL in the PDF text is the standard USCDI reference link (healthit.gov). No additional data dictionary downloads, schema files, or sample data were found on the page.

7. **Took screenshots** of the expanded certifications section showing the "EHI EXPORT DOCUMENTATION" button alongside other certification links (API Terms of Use, CHPL Listing, Costs, FHIR API Documentation, Real World Testing Plans/Results).

8. **Built enrichment**: Created a Bun TypeScript script to parse the PDF's data dictionary into structured JSON. Extracted 22 CSV file definitions with 383 fields total.

## What Was Found

### The EHI Export Mechanism

CGM APRIMA implements a dedicated (b)(10) EHI export as a **batch process within the application** (Tools menu > Batch Process Management > EHI Export). The export generates a ZIP file per patient, named `EHIExtract_LastName FirstName MiddleName_ExtractCreationDateTime.zip`. It supports both individual patient exports and total population exports.

### Export Contents

The ZIP file contains four types of content:

1. **CSV files** (22 file types documented): Structured tabular data covering clinical, demographic, insurance, billing, and administrative domains. Each CSV has a header row followed by data rows.

2. **Image folders**: Clinical images organized by encounter, stored in folders (e.g., Radiology/) with a naming convention: `<date added to encounter><ID><description>.<extension>`.

3. **USCDI file**: An XML file containing ePHI in a standardized format, viewable with a bundled `EEHR_ChartViewer.exe` viewer application. This provides C-CDA-style portability between EHR systems.

4. **Complete Patient Chart**: A PDF document containing information from every visit chart created for the patient — essentially a print of the full chart.

### Data Dictionary

The documentation provides a comprehensive field-level data dictionary for all 22 CSV files. Each field is documented with:
- Column heading name
- SQL data type with length (e.g., `char(255)`, `datetime`, `money`, `bit`)
- Human-readable description

The 22 CSV files are:

| CSV File | Fields | Description |
|----------|--------|-------------|
| Audit Trail | 5 | Changes made to patient records |
| Contacts | 14 | Patient contacts (emergency, POA, HIPAA release) |
| Active Medication | 23 | Prescribed medications with NDC, strength, dosage |
| Allergies | 14 | Drug/non-drug allergies with SNOMED codes |
| Appointment Information | 16 | Appointments with type, status, location |
| Family History | 13 | Family disease history with relationships |
| Immunization | 15 | Vaccines with CPT, lot, manufacturer |
| Medical History | 17 | Medical/surgical history with ICD-9/10 codes |
| Patient Demographics | 39 | Full demographics: name, address, phones, language, race, ethnicity, marital status |
| Patient Insurance | 22 | Primary and secondary insurance |
| Problem List | 15 | Diagnoses with ICD-9/10 codes, onset/resolved dates |
| Responsible Party | 20 | Decision-making parties with demographics |
| Results | 19 | Lab results with codes, values, ranges, flags |
| Social History | 13 | Social history as question/answer pairs |
| Visit Comments | 5 | Provider comments organized by visit and section |
| Vitals | 15 | Vital signs with values, units, positions |
| Eligibility | 25 | Insurance eligibility inquiries with deductibles, copays |
| Employment | 7 | Employment history |
| Patient Ledger | 58 | Financial transactions: superbills, payments, adjustments, balances |
| Patient Referrals | 14 | Referrals with procedures and dates |
| Providers | 7 | Patient's care team providers with roles and specialties |
| Response Report | 7 | Clinical decision support responses |

**Total: 383 documented fields across 22 CSV files.**

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains:**
- **Demographics**: Comprehensive — 39 fields including name, address, 4 phone numbers, 2 emails, language, race, ethnicity, marital status, AKA names, SSN, death date, PCP.
- **Problems/Diagnoses**: Full problem list with ICD-9 and ICD-10 codes, onset/resolved dates.
- **Medications**: Active medications with NDC codes, strength, formulation, route, frequency, duration, refills.
- **Allergies**: Drug and non-drug allergies with SNOMED codes.
- **Lab Results**: Results with lab codes, attribute names, values, reference ranges, abnormal flags, units.
- **Vital Signs**: Named vitals with values, units, and positions.
- **Immunizations**: Vaccines with CPT codes, lot numbers, manufacturers, dosages, administration sites.
- **Medical/Surgical History**: Procedures with ICD-9/10 and procedure codes.
- **Family History**: Conditions by relationship.
- **Social History**: Question/answer format covering lifestyle factors.
- **Insurance**: Primary and secondary insurance with member/group IDs.
- **Billing/Financial**: Extremely detailed Patient Ledger (58 fields) with superbill data, procedure codes, diagnosis codes, amounts billed/due/paid/adjusted, insurance vs. patient portions, liability balances. Also Eligibility data (25 fields) with deductibles, copays, coinsurance.
- **Appointments**: Full appointment data with types, statuses, locations.
- **Referrals**: Referral records with procedures and provider roles.
- **Clinical Notes**: Visit Comments (by section) plus the Complete Patient Chart PDF.
- **Documents/Images**: Clinical images exported in encounter-organized folders.
- **Audit Trail**: Record change history.
- **Contacts**: Emergency contacts, POA, HIPAA release permissions.
- **Employment**: Current and historical employment.
- **Providers/Care Team**: Patient's providers with roles and specialties.
- **Clinical Decision Support**: Response Report captures HM rule alerts and provider decisions.

**Domains with potential gaps:**
- **Prescribing details**: Active Medications are exported, but prescription transmission details (e-prescribing confirmations, prior authorization records, PDMP query results) are not separately documented. The medication export captures the order-side data well.
- **Care plans/Goals**: No dedicated CSV for care plans or patient goals. These may be captured in Visit Comments or the Complete Patient Chart PDF, but are not structured.
- **Encounter/Visit data**: There is no dedicated Encounters/Visits CSV listing all encounters with dates, types, providers, and diagnoses. Visit data is embedded in other files (Visit Comments, Patient Ledger superbills, Appointment Information).
- **Orders**: No dedicated lab or imaging order file — only Results. If orders were placed but results not yet returned, those may not appear.
- **Telehealth data**: Despite the product supporting telehealth/RPM, no telehealth-specific data appears in the export.
- **SDOH assessments**: Mentioned in the v19.4 release notes but not represented in the export CSV files.
- **Documents metadata**: Images are exported but there's no CSV cataloging document types, dates, and descriptions.

### (b)(10) vs (g)(10) Assessment

**This is a genuine (b)(10) export, not a repackaged (g)(10) FHIR API.** The evidence is strong:

1. **Separate mechanism**: The EHI export is a dedicated batch process within the application (Tools > Batch Process Management > EHI Export), completely distinct from the FHIR API.
2. **CSV format**: The export uses flat CSV files, not FHIR resources. This is a pragmatic format that maps directly to the product's underlying database.
3. **Billing data included**: The Patient Ledger CSV (58 fields) provides detailed financial data — superbills, payment amounts, insurance vs. patient portions, adjustments, liability balances. This goes far beyond USCDI/US Core.
4. **Insurance eligibility data**: 25 fields covering eligibility inquiries, deductibles, copays, coinsurance — not available through FHIR US Core.
5. **Employment data**: A separate CSV with employer, occupation, industry — operational data not in FHIR US Core.
6. **Audit trail**: Change tracking with user, workstation, and description — not a FHIR resource.
7. **Complete Patient Chart PDF**: A full chart print capturing everything including encounter notes across all visits.
8. **USCDI file alongside CSVs**: The export includes a separate USCDI/C-CDA file for standards-based portability, but the CSVs provide the comprehensive dataset.

The FHIR API Documentation Guide (76 pages) is a separate document for the (g)(10) certified API, covering standard US Core resources (AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance). The EHI export covers significantly more data domains than the FHIR API.

### Export Format & Standards

- **Format**: ZIP file containing CSV files, image files, XML (USCDI/C-CDA), and PDF.
- **Standard**: Proprietary CSV format with SQL-typed columns. The USCDI XML file uses C-CDA standards for the clinical summary portion.
- **Relationships**: CSV files share patient identifiers (PatientID, Patient ID, External ID) but no explicit foreign key documentation. The Patient Ledger references SuperbillID, AccountID, DepositUid, and ResponsiblePartyUid with uniqueidentifier types, suggesting relational linkage.
- **Reconstruction feasibility**: A developer could reconstruct the patient record reasonably well from the CSVs. The consistent use of patient identifiers allows cross-referencing. The Complete Patient Chart PDF provides a human-readable failsafe.

### Documentation Quality

- **Readability**: Good. The 28-page PDF is well-organized with a clear table of contents and consistent formatting.
- **Data dictionary completeness**: Field-level documentation with column names, SQL data types (with lengths), and descriptions for all 383 fields. This is above average for EHI export documentation.
- **Value sets**: Not documented. Coded fields (e.g., Gender Code, Race Code, Appointment Type Code) show the data type but not the allowed values.
- **Examples**: One brief CSV example showing medication data. No sample export files or complete example records.
- **Export instructions**: Minimal — three steps on the last page. No screenshots of the export UI.
- **Maintenance**: The document is dated November 2, 2023 (about 11 months after certification). It appears to be a single version with no revision history.

### Structure & Completeness

- **Granularity**: Field-level with data types — this is the right level of detail.
- **Value sets**: Missing. Coded fields need enumeration of valid values.
- **Relationships**: Not explicitly documented. The data model must be inferred from shared identifiers.
- **Versioning**: No version history or change log.

## Overall Assessment

CGM APRIMA has done real (b)(10) work. The EHI export is a dedicated, purpose-built mechanism that exports a comprehensive dataset of patient clinical, demographic, insurance, and financial data in a practical CSV format. The inclusion of a 58-field Patient Ledger with detailed billing data, insurance eligibility records, employment data, audit trails, and clinical images distinguishes this from vendors that simply repackage their FHIR API.

The documentation quality is solid — 383 fields documented with SQL types and descriptions across 22 CSV files. The main gaps are:
1. No value set documentation for coded fields
2. No explicit relationship/foreign key documentation
3. Care plans and goals are not structured in the export
4. Encounter-level data is implicit rather than having a dedicated file
5. No sample export files provided

For an ambulatory EHR serving 70+ specialties, the export covers the core designated record set well: clinical data (problems, medications, allergies, labs, vitals, immunizations, history), billing data (patient ledger with superbills and payments), insurance (coverage and eligibility), demographics, and documents/images. The Complete Patient Chart PDF ensures even data that doesn't map neatly to CSV columns is captured.

## Access Summary
- Final URL: https://www.cgm.com/usa_en/products/electronic-health-records/cgm-aprima.html (no redirects)
- Status: found
- Required browser: no (direct PDF download via curl)
- Navigation complexity: one_click (expand accordion in Certifications section, click "EHI EXPORT DOCUMENTATION")
- Anti-bot issues: none (Cloudflare present but not blocking; standard User-Agent header sufficient)

## Obstacles & Dead Ends
- The Certifications section uses an accordion UI that is collapsed by default. The content is in the HTML DOM but hidden with CSS. The EHI export link is accessible without JavaScript by following the direct PDF URL found in the HTML source.
- The mandatory disclosures URL in CHPL metadata points to the same product marketing page (not a separate compliance page), which is unusual but the certification documentation links are all present in the Certifications accordion.
- No obstacles to downloading. Both PDFs downloaded cleanly with curl.
