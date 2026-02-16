# Nth Technologies, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.nablemd.com/certification2015.html
- CHPL IDs: 11118
- Product: nAbleMD 6.0c
- Certification date: 2022-12-21

## Navigation Journal

1. **Initial probe:**
   ```bash
   curl -sI -L "https://www.nablemd.com/certification2015.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: text/html, 36,088 bytes. No redirects.

2. **Downloaded and examined the page:**
   ```bash
   curl -sL "https://www.nablemd.com/certification2015.html" -H 'User-Agent: Mozilla/5.0' -o certification-page.html
   ```
   The page is a standard compliance/mandatory disclosures page with sections for: certification details, costs and requirements, MFA, API documentation, **Electronic Health Information Export**, and Real World Testing.

3. **Found the EHI Export section** — a dedicated `<h2>` heading "Electronic Health Information Export" near the bottom of the page, containing a single link:
   - [nAbleMD 6.0c export guide and data dictionary](https://docs.google.com/spreadsheets/d/11Yj6cH8GsXPnTuxDDIvYwgoF5sgM6zrwy4Ql6OEdWRQ/edit?gid=1058514257#gid=1058514257)

4. **Examined the Google Sheets data dictionary.** The spreadsheet is publicly accessible (view-only). It has the title "CSV Export Format Documentation - External" and contains 109 tabs:
   - "Read Me" — export creation process, documentation for .zip format, .csv format, document repository, and guide overview
   - "Revision History" — version tracking (v1.0 11/30/2023, v1.0.1 12/12/2023)
   - "Table of Contents" — index of ~107 data tables
   - 106 individual data table tabs, each documenting one CSV export file with FieldName and Description columns

5. **Downloaded all 109 sheets as CSV** using the Google Sheets gviz/tq endpoint:
   ```bash
   curl -sL "https://docs.google.com/spreadsheets/d/11Yj6cH8GsXPnTuxDDIvYwgoF5sgM6zrwy4Ql6OEdWRQ/gviz/tq?tqx=out:csv&gid=GID" -H 'User-Agent: Mozilla/5.0' -o FILENAME.csv
   ```
   All 109 files verified as valid CSV (not HTML error pages). The direct XLSX export endpoint returned HTML auth walls, so per-sheet CSV via the gviz endpoint was used instead.

6. **Noted important context from the "Costs and Requirements" section** on the certification page:
   > "While this product-version is certified for Data Portability to generate a set of export summaries of all patients; photographs, scanned images, faxes, other uploaded documents as well as medical documentation not included in the Common Data Set are not included in the export summaries. A one-time fee will be charged for the bulk export of these images, documents and documentation."

   This indicates that the standard export covers structured data, while binary documents/images require a separate fee-based bulk export.

## What Was Found

### Export Mechanism

The nAbleMD EHI export is a **CSV-based bulk export** with an accompanying document repository. The export produces an encrypted 7-zip archive containing:

1. **CSV files** — one per data table (106+ tables), with UTF-8 encoding, comma-separated, first row as headers
2. **A document repository folder** — containing scanned documents, DICOM files, HL7 messages, faxes, and other attachments referenced by the Document CSV table

### How to Perform the Export

Per the "Read Me" tab:
- **Authorization**: An administrator must grant the user access to the Data Export screen under System Configuration. The user must also enable 2FA on their account.
- **Single patient export**: PM Home → System Configuration → Data Export → select patient → "Request Download" → enter encryption password. Takes ~5 minutes per patient.
- **Full export**: Same screen, but click "Request Download" without selecting a patient. Duration depends on total data volume.
- **Retrieval**: Completed exports show checksums and download links. Each zip volume is ~10GB. Files retained for 7 days.

### Export Format Details

- **Archive format**: 7-zip with AES-256 encryption, split into ~10GB volumes (.zip.001, .zip.002, etc.)
- **CSV format**: Standard CSV with UTF-8 encoding. No distinction between empty string and NULL. Strings containing commas, newlines, or quotes are enclosed in double quotes with standard escaping.
- **Document repository**: Files referenced by the Document table's filename column. Includes:
  - Documents/images: .pdf, .png, .jpg, .gif, .tif, .doc, .docx
  - ANSI claim/EDI messages: .835, .837, .277, .277FE, .271, .271.xml, .DPR, .EBR
  - HL7 messages: .hl7 (.orm.hl7 for results, .oru.hl7 for orders)
  - DICOM: .dcm (image or Structured Report data)

### Data Dictionary Structure

Each of the 106 data table tabs follows a consistent format:
- **Table Description** — 1-2 sentences describing the table's purpose and primary key
- **FieldName / Description** — two-column listing of every exported field with plain-English descriptions

Field descriptions include data types implicitly (dates described as "Date when...", boolean fields as "Indicates if/whether...", foreign keys identified as "identifier for..." or "Map with patientkey"). No explicit data types, constraints, or value set enumerations are provided, though some descriptions note format details (e.g., "comma separated if multiple", gender codes "M:Male F:Female U:Unknown X:Undifferentiated Blank:Undocumented").

### Data Tables (106 tables organized by domain)

**Patient Demographics & Registration:**
- Patients (extensive — ~170 fields covering demographics, addresses, contacts, insurance, fertility-specific fields like blood type, Rh factor, partner info, custom fields 1-10)
- PatientContact, PatientAllowedContacts, PatientGlobal, PatientNote, Relative, EmrBiologicalFamily

**Clinical Documentation:**
- ChartNote (chart notes with form content, signatures, cosigning, patient portal release)
- CosignNote, EmrNotes, EmrEncounterReport, EmrEncounterReportAddendum
- EmrHpi (History of Present Illness)
- EmrChiefComplaint
- EmrReviews (Review of Systems)
- EmrAssessment
- EmrPlan
- EmrChecklistItem
- EmrAnswerDetail

**Encounters & Visits:**
- Visit (~75 fields including ICD codes 1-12, claim ID, place of service, provider, charting/approval status)
- Appointment, AppointmentWaitlist, Action

**Problems, Medications & Allergies:**
- EmrProblem (diagnoses/problems with ICD codes, onset dates, status)
- EmrVisitProblem (visit-specific problems)
- NewcropDrug (medications via NewCrop integration — ~50 fields)
- NewcropAllergy (allergies via NewCrop)
- EmrHealthConcern
- EmrMedicalHistory

**Billing & Financial:**
- Procedure (CPT/HCPCS codes, modifiers, fees)
- ProcedureCharge
- LedgerItem
- Payment, VisitPayment, PrePayment
- Insurance (~80 fields — subscriber info, group numbers, authorization details)
- PriorAuth (prior authorizations)
- CryoBilling (IVF-specific billing)
- IvfQuote (IVF treatment quotes)

**Immunizations:**
- ImmunizationRecord (~35 fields — vaccine codes, lot numbers, manufacturer, VIS dates, administration details)
- ImmunizationSchedule

**IVF/Fertility-Specific (extensive):**
- EmrCycle (~200+ fields — comprehensive IVF cycle data)
- EmrCycleHistory, EmrCycleIntents, EmrCycleDrugPlan, EmrCycleScheduleDay, EmrCycleScheduleRow, EmrCycleScheduleAlert
- EmrCycleNote, EmrCycleEducation, EmrCycleBirth, EmrCycleCulture
- EmrOocyte, EmrOocyteDay (oocyte tracking)
- EmrIvfSample (specimen/sample tracking)
- EmrIvfSemenAnalysis (~75 fields)
- EmrIvfFollicularUs (follicular ultrasound)
- EmrIvfObUs (OB ultrasound)
- EmrSemenMeasurement
- EmrDonor (~70 fields), DonorEducation, DonorEmployment, DonorFamily, DonorFamilyDeceased, DonorAnswer
- EmrDonorPatrequest, CultureMedia
- EmrInfertilityTreatment, CycleTypeHistory
- DailyWorklist (embryology daily tasks)
- EmrContraception

**OB/GYN:**
- EmrObHistory, EmrObHistoryPreg, EmrObgynhc
- EmrPregnancy, EmrPregnancyPlan, EmrEstimatedDueDate, EmrMultiBirth
- EmrObUltrasound

**Surgical:**
- EmrSurgery, EmrSurghis (surgical history)
- EmrDvtRisk (DVT risk assessment)

**Vitals & Measurements:**
- EmrMeasurement (~45 fields — vital signs, anthropometric data)

**Lab Orders:**
- EmrLabOrder

**Documents & Images:**
- Document (~60 fields — comprehensive document metadata including MIME types, categories, patient portal release, fax tracking)
- EmrChartDocument

**Patient Portal & Communication:**
- PatMail (patient messaging)
- SmsnaviConsent, SmsnaviMessages, SmsNaviNotification (SMS communications)
- PatientSurvey, KioskAnswer, KioskPregOutcomeAnswer (patient-entered data)
- PatientRequestAmendment, PatientRequestCallback, PatientRequestForm, PatientRequestOnline, PatientRequestRecall

**Care Plans & Wellness:**
- EmrWellnessPlan
- EmrDisclosureInfo

**Consent & Transfers:**
- ConsentFormCompleted
- EmrTransfer

**Tasks:**
- task, TaskAssigned

**Access Control:**
- EmrRestrictRecordAllow (restricted record permissions)
- EmrEncounterProvider

## Export Coverage Assessment

### Data Domain Coverage

This is an exceptionally thorough EHI export. The data dictionary documents **106 distinct data tables** covering virtually every data domain identified in the product research. This is a genuine (b)(10) export — not a FHIR/USCDI repackaging.

**Clearly covered:**
- Patient demographics and registration (extensive — ~170 fields in the Patients table alone)
- Clinical documentation (chart notes, encounter reports, HPI, assessments, plans)
- Problems/diagnoses with ICD codes
- Medications (via NewCrop integration)
- Allergies (via NewCrop)
- Lab orders
- Vital signs and measurements
- Immunizations (with full vaccine administration details)
- Appointments and scheduling
- **Billing and financial data** — Procedure, ProcedureCharge, LedgerItem, Payment, Insurance, PriorAuth. This is a critical domain that many vendors miss.
- **IVF/Fertility-specific data** — This is where nAbleMD's specialty focus really shows. The export includes ~25+ IVF-specific tables covering cycles, oocytes, semen analysis, follicular ultrasound, donor records, cryostorage billing, embryology worklists, culture media, and more. This is exactly the kind of specialty-specific clinical data that distinguishes a real (b)(10) export.
- **OB/GYN data** — pregnancy history, OB ultrasound, estimated due dates, birth records
- Documents and images (with repository of actual files)
- Patient portal communications and messaging
- SMS communications
- Consent forms
- Surgical history
- Care plans and wellness plans
- Patient surveys and kiosk-entered data
- Referrals and transfers
- EDI/claims data (835, 837, 277 messages in the document repository)

**Potentially missing or unclear:**
- **e-Prescribing transmission records** — NewcropDrug covers medication data, but transmission/fill status details are unclear. The NewCrop integration likely handles this on the NewCrop side.
- **Clinical decision support data** — No dedicated CDS table, though CDS rules may be system configuration rather than patient data.
- **Quality measure data** — No explicit CQM results table, though the underlying clinical data that feeds CQMs is present.
- **Explicit radiology/imaging results** — EmrLabOrder covers lab orders but there's no dedicated radiology report table. DICOM files are included in the document repository and imaging results may be stored as documents.

These gaps are minor. The export comprehensively covers the designated record set.

### Export Format & Standards

The export uses a **proprietary CSV-based format** — not FHIR, not C-CDA, not any standardized healthcare interchange format. This is actually appropriate for a (b)(10) export of this scope:

- **CSV is universal.** Any system can read it. No FHIR parsing libraries required.
- **The relational structure is preserved.** Tables reference each other via key fields (patientkey, visitkey, etc.), maintaining the database's relational integrity.
- **Binary data is included.** The document repository preserves original file formats (PDF, DICOM, HL7, images, EDI messages) rather than trying to force everything into a text format.
- **The format matches the data model.** Unlike trying to squeeze 106 tables into FHIR resources (many of which have no FHIR equivalent — EmrOocyteDay? CryoBilling? EmrCycleDrugPlan?), the CSV export simply mirrors the database schema.

A third party could reconstruct a reasonably complete patient record from this export, given the data dictionary documentation. The key relationships (patientkey → other tables) are documented. The main limitation is that relationships are documented implicitly through key name matching rather than an explicit schema definition.

### Documentation Quality

**Strengths:**
- The data dictionary is comprehensive — 106 tables, each with field-level descriptions
- Export process instructions are clear and specific (which screens, which buttons, in what order)
- Format documentation explains CSV encoding, ZIP encryption, and document repository structure
- The Google Sheets format makes it easy to navigate between tables
- Field descriptions are meaningful — not just column names repeated, but actual explanations of what the data represents
- Revision history is maintained (though only 2 entries so far)
- The Table of Contents provides a quick index

**Weaknesses:**
- **No explicit data types.** Fields are described in prose but there's no column for "string", "integer", "date", "boolean", etc. You can usually infer types from descriptions ("Date when..." = date, "Indicates if..." = boolean), but a developer would need to examine actual export data to confirm.
- **No value set enumerations.** Coded fields (like gender, marital status, place of service) mention codes in passing within descriptions but don't provide exhaustive value set lists.
- **No cardinality or constraint documentation.** Which fields are required? What's the max length of string fields? Not specified.
- **No sample data or worked examples.** A sample export file would help developers understand the actual format.
- **No explicit foreign key documentation.** Key relationships are mentioned in descriptions (e.g., "Map with patientkey") but there's no formal entity-relationship diagram or schema definition.
- **The XLSX export doesn't work** — the Google Sheets direct export endpoint requires authentication, so the spreadsheet can only be accessed via browser or the gviz CSV endpoint. This could be an accessibility concern for some users.

### Structure & Completeness

**Granularity:** Field-level documentation for every column in every exported table. This is more granular than many vendors provide.

**Breadth:** 106 data tables covering every major data domain. The IVF/fertility tables are remarkably detailed — the EmrCycle table alone has ~200+ fields documenting every aspect of an IVF treatment cycle. This is specialty-specific clinical data that most EHR vendors would never think to include in an EHI export.

**The (b)(10) vs (g)(10) distinction:** nAbleMD gets this right. The EHI export section is separate from the FHIR API documentation section on the certification page. The export is a bulk CSV dump of the entire database, not a FHIR endpoint. The data dictionary documents tables that have no FHIR equivalent — this is genuine (b)(10) work, not (g)(10) relabeled.

**Notable disclosure:** The certification page explicitly states that "photographs, scanned images, faxes, other uploaded documents as well as medical documentation not included in the Common Data Set are not included in the export summaries" and that "a one-time fee will be charged for the bulk export of these images, documents and documentation." This means the standard export covers structured data, while binary content requires an additional fee. The document repository is described in the data dictionary documentation, so the capability exists — it's just priced separately.

### Overall Assessment

This is one of the more thorough EHI export implementations encountered. Nth Technologies has done genuine (b)(10) work:

1. **They built a real export mechanism** — not just a FHIR endpoint relabeled, but a purpose-built CSV bulk export with encryption, volume splitting, and document repository support.
2. **They documented it comprehensively** — 106 tables with field-level descriptions in a well-organized Google Sheets workbook.
3. **They include specialty-specific data** — the extensive IVF/fertility tables demonstrate that they're exporting data that goes far beyond USCDI/US Core.
4. **They include billing data** — Procedure, Payment, Insurance, LedgerItem, PriorAuth — a critical domain many vendors omit.
5. **They include documents** — the document repository handles PDFs, DICOM, HL7, EDI, images, and faxes.

The documentation could be improved with explicit data types, value sets, sample data, and an ERD. But the substance is strong. A developer receiving this export and data dictionary would have a reasonable chance of importing the data into another system — which is the fundamental purpose of (b)(10).

## Access Summary
- Final URL (after redirects): https://www.nablemd.com/certification2015.html
- Status: found
- Required browser: no (page is static HTML; Google Sheet requires gviz endpoint workaround for CSV download)
- Navigation complexity: one_click (EHI section is a single link on the certification page)
- Anti-bot issues: none for the main page; Google Sheets direct XLSX export requires authentication but gviz CSV endpoint works without it

## Obstacles & Dead Ends
- The Google Sheets XLSX export endpoint (https://docs.google.com/spreadsheets/d/.../export?format=xlsx) returns an HTML auth wall rather than the file. The gviz/tq CSV endpoint works fine as an alternative.
- Getting all 109 sheet GIDs required fetching the htmlview version of the spreadsheet and parsing the JavaScript initialization code for gid-to-name mappings. The edit view doesn't update the URL hash when clicking tabs in read-only mode.
- No issues accessing the main certification page (standard Apache server, no WAF/Cloudflare).
