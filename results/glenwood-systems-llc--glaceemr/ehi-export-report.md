# Glenwood Systems LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://docs.glaceemr.com/Glenwood/transparencydisclosure.html
- CHPL IDs: 9559
- Product: GlaceEMR 6.0
- Certification Date: 2018-06-29
- Developer: Glenwood Systems LLC

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to registered URL:
   ```bash
   curl -sI -L "https://docs.glaceemr.com/Glenwood/transparencydisclosure.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html, 26,890 bytes. No redirects. Last-Modified: Mon, 24 Mar 2025.

2. **Fetched and examined the HTML page** — static HTML page (not SPA), no JavaScript required for content. The page is a transparency disclosure / compliance hub for GlaceEMR 6.0 containing:
   - Certification statement and compliance certificate link
   - Modules tested listing
   - Pricing transparency section
   - Real-world testing plans and results (2022–2024) — not relevant to EHI export
   - **"EHI Data Export" section** with description of single-patient and population export capabilities
   - Link to the data dictionary PDF

3. **Found the EHI Data Export section** — located roughly 2/3 down the page, under an `<h1>` heading "EHI Data Export". The section describes:
   - Single Patient Export: exports all EHI for one patient as a ZIP file
   - Patient Population Export: exports EHI for selected patients or entire population as a ZIP
   - Export format: ZIP containing CSV, HTML, PDF, JPG, PNG, XML files
   - A single download link: **"GlaceEMR Export Data Dictionary"** pointing to `pdf/GlaceEMR Export Data Dictionary.pdf`

4. **Downloaded the data dictionary PDF**:
   ```bash
   curl -sL 'https://docs.glaceemr.com/Glenwood/pdf/GlaceEMR%20Export%20Data%20Dictionary.pdf' -H 'User-Agent: Mozilla/5.0' -o 'GlaceEMR Export Data Dictionary.pdf'
   ```
   Verified: `file` confirms "PDF document, version 1.7, 62 page(s)". 783,292 bytes.

5. **Examined the PDF** using `pdfinfo` and `pdftotext`. No embedded URLs or attachments. Author: sraj, created with Microsoft Word for Microsoft 365, dated November 29, 2023.

6. **Searched for additional files** — scanned the HTML source for all href links. Found only the data dictionary PDF and compliance certificate PDF as relevant downloads. No additional data dictionary files, schema files, or API documentation present on the page.

## What Was Found

### Export Mechanism

GlaceEMR provides a genuine (b)(10) EHI export — **not** a repackaged FHIR/g(10) API. The export produces a ZIP file with a well-defined folder structure containing CSV data files, clinical documents in HTML/PDF format, scanned documents in their original formats, patient photos, C-CDA v2 XML documents, and a reference schema folder.

The export supports both single-patient and population-level operations.

### Export Format

The ZIP file contains five top-level folders:

| Folder | Contents |
|--------|----------|
| **EMR/** | 31 CSV files covering clinical data |
| **PMS/** | 11 CSV files covering practice management/billing data |
| **Documents/** | Clinical templates (HTML+PDF), scanned documents (PNG/JPEG), C-CDA v2 XML — organized per-patient |
| **Photos/** | Patient photos in JPG format |
| **Reference/** | Schema of the exported file content (details not elaborated) |

### Data Dictionary Scope

The data dictionary documents **42 CSV files** totaling **820 columns** across the EMR and PMS folders. This is a CSV-based database dump covering both clinical and billing data.

**EMR folder (31 files):**
- Encounters, Vitals
- 13 distinct history files: Past Medical, Surgical, Family, Family Relations, Social, Substance Abuse, Contraception/Sexual, Pregnancy, Birthing, Menstrual, Occupational, Obstetric, Exposure
- Allergies (with NDC codes)
- Assessments (with ICD-9/10, SNOMED, CPT4, NDC, LOINC, RXNORM coding)
- Problem List (ICD-10, SNOMED)
- Medications (active), Inactive Medications (with NDC)
- Investigation (lab orders/results with diagnosis codes, CPT codes, result values and ranges)
- Preventive Screenings
- Coumadin dosage tracking (specialty-specific: INR/PT monitoring with daily dose schedules)
- Vaccines (with CVX codes, manufacturer details, lot numbers)
- Messages (phone/internal), Reminders
- Index files for: Patient Photos, Clinical Documents, Phone Messages, Scans/Attachments, CDA Documents

**PMS folder (11 files):**
- Patient Demographics (comprehensive: name, address, contact, guarantor, emergency contact, race, ethnicity, language, pharmacy, employer, deceased status)
- Patient Insurance (primary, secondary, tertiary — with subscriber details, copays)
- Patient Account Balance
- Transactions (procedure codes, charges, diagnosis pointers, payments, adjustments, balances)
- Payment Receipts (cash/check/card/insurance with payment/adjustment/denial codes)
- Payment Posting (linking receipts to services)
- Appointments
- Master lists: Insurance, Place of Service, Providers, Referring Providers

### Relationships Between Files

The data dictionary explicitly documents foreign key relationships between tables:
- Patient ID in all files references PMS/Patient_Demographics.csv
- Encounter ID references EMR/Encounters.csv
- Insurance IDs reference PMS/Master_Insurance_List.csv
- Provider references to PMS/Master_Provider_List.csv and PMS/Master_Referring_Provider_List.csv
- Receipt/Service ID cross-references between PMS payment files

### Documents Folder Structure

Clinical documents are organized per-patient in folders named:
`LastName,FirstName-(DOB MM-DD-YYYY)-(Account#)-[PatientID]`

Three types of documents are exported:
1. **Clinical Templates** — in both HTML and PDF formats, indexed by Clinical_Document_Index_File.csv
2. **Scanned Documents/Attachments** — in original format (PNG/JPEG/etc.), indexed by Scan_And_Attachments_Index_File.csv
3. **C-CDA v2 documents** — XML format, indexed by CDA_Document_Index_File.csv

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains:**
- Demographics (comprehensive — PMS/Patient_Demographics.csv has 50+ fields)
- Encounters and visit documentation
- Vital signs
- Extensive medical/social history (13 separate history categories — unusually granular)
- Allergies with NDC coding
- Problem lists and assessments with standard coding (ICD-9/10, SNOMED)
- Active and inactive medications with NDC codes
- Lab orders and results (Investigation.csv with result values, ranges, and status tracking)
- Immunizations/vaccines with CVX codes and manufacturer details
- Preventive screenings
- Clinical documents (progress notes, specialty templates — exported as full HTML/PDF)
- Scanned documents and attachments
- C-CDA documents
- Patient photos
- Insurance information (primary, secondary, tertiary)
- Billing transactions (charges, procedure codes, diagnosis pointers)
- Payments and payment posting (with receipt details, denial codes, adjustment codes)
- Account balances
- Appointments
- Phone/internal messages with doctor responses
- Patient reminders
- Coumadin/anticoagulation management (specialty clinical module)

**Domains from product research with unclear or missing coverage:**

- **E-Prescribing transaction data** — Medications are exported with NDC codes, but the actual e-prescribing transaction records (SureScripts messages, PDMP lookups, EPCS transactions) are not explicitly listed. The Medications.csv captures prescription content but may not capture the full prescribing workflow.

- **Behavioral health specialty data** — The product research highlights a significant behavioral health module with PHQ-9, BIMS, Mini Mental Status Exam, DSM-5 assessments, treatment plans with goals, and group therapy management. The data dictionary does not have a dedicated behavioral health file. These assessments may be captured within the Clinical Document templates (exported as HTML/PDF) or within the generic Assessment/History files, but this isn't explicitly documented.

- **Care coordination / CCM / RPM data** — Product research mentions Care Coordination Management and Remote Patient Monitoring modules. These are not represented by dedicated CSV files. Data may be in clinical documents.

- **Patient portal messages** — The Messages.csv covers phone messages and internal messages. Patient portal two-way messaging is mentioned in the product research but not clearly mapped to a specific export file.

- **Telehealth visit data** — The product mentions a comprehensive telemedicine module. Whether telehealth encounters appear in the standard Encounters.csv or have additional metadata isn't documented.

- **Referrals** — The product is certified for (b)(7)-(b)(9) transitions of care, and the export includes referring doctor information. But dedicated referral records (referral requests, status, outcomes) don't have their own CSV.

- **Care plans and goals** — The product research mentions treatment plans with goals and progress tracking. There's no dedicated care plan export file. Likely embedded in clinical documents.

- **Growth charts** — Mentioned in product features; no dedicated export file.

### Export Format & Standards

The export format is **CSV files in a ZIP archive** — a vendor-specific but highly practical format. This is appropriate for a (b)(10) export and far more comprehensive than a FHIR-only approach would be.

Key format characteristics:
- **CSV for structured data** — tabular, universally readable, no special software needed
- **HTML + PDF for clinical documents** — dual format ensures both human readability and preservation
- **C-CDA v2 XML** — standard clinical document format included alongside the CSV data
- **Original format for attachments** — scanned documents exported in their stored format (PNG/JPEG)
- **Standard coding systems** — ICD-9/10, SNOMED, NDC, CPT4, LOINC, RXNORM used where applicable

Relationships between CSV files are documented through explicit foreign key references. A recipient could reconstruct patient records by following the documented key relationships: Patient_Demographics → Encounters → Vitals/Allergies/Medications/etc., with cross-references to master lists for providers and insurance.

**Could a third party reconstruct the patient record?** Largely yes. The CSV files provide the structured data with standard codes, the clinical documents provide the full note content, and the relational structure is documented. The main gap is that some clinical content (specialty templates, behavioral health assessments) appears to be captured only within the HTML/PDF clinical documents rather than as structured CSV data, which limits computability for those domains.

### Documentation Quality

The data dictionary is **well-structured and reasonably detailed**:
- Clear file-by-file organization with consistent format
- Column names, data types, and descriptions for all fields
- Foreign key relationships explicitly documented with cross-references
- Possible values / value sets documented for coded fields (e.g., allergy types, encounter status, payment types, coding systems)
- Consistent audit trail columns (Created By/On, Last Modified By/On) across all files
- File naming conventions for documents folder clearly specified with examples

**Weaknesses:**
- Many columns have empty Description and Comments fields — the column name is the only documentation
- No worked examples or sample CSV rows
- No formal schema files (no JSON Schema, XSD, or similar machine-readable constraint definitions) — though the "Reference" folder in the export is described as containing schemas
- Data types are loosely specified (many fields are just "String" without length or format constraints)
- No documentation of date/time formats used in the CSV files
- No change history beyond Version 1.0
- Version 1.0 dated November 2023 — no updates in 2+ years

**Could a developer implement an import?** Yes, for the CSV data — the column names and types are clear enough to build a parser, and the foreign key relationships enable record linking. The clinical documents (HTML/PDF) would be harder to systematically import as structured data.

### Structure & Completeness

**Granularity:** Field-level documentation for all 42 files. Column names, data types, and some constraints (possible values, foreign keys) are documented. Not all fields have descriptions.

**Coded fields:** Value sets are partially documented. Some fields list possible values (e.g., Allergy Type, Encounter Status, Payment Type, Coding System names). Others (e.g., Encounter Type, Appointment Type) are left undocumented. The coding system names (ICD-9, ICD-10, SNOMED, etc.) are well-documented.

**Relationships:** Foreign key relationships between entities are explicitly documented with references to the master file. This is a strong point — a recipient knows exactly how to link records across files.

**Versioning:** Single version (1.0) with no change history beyond the initial release.

### Overall Assessment

GlaceEMR's EHI export represents a **genuine (b)(10) effort** that goes well beyond a FHIR-only approach. The export covers both clinical (EMR) and billing/practice management (PMS) data in a flat CSV format that is both comprehensive and accessible. The inclusion of 13 separate history categories, full billing transaction detail, payment posting, and clinical documents in their original formats demonstrates a commitment to exporting the complete designated record set.

The data dictionary is a serious document — 62 pages covering 42 files and 820 columns with foreign key relationships. It is clearly purpose-built for the (b)(10) requirement rather than repurposed from another certification criterion.

The main gaps are:
1. **Specialty clinical data** (behavioral health assessments, treatment plans, care coordination) appears to be captured within clinical documents (HTML/PDF) rather than as structured CSV data. This means the data is exported but may require human reading rather than programmatic extraction.
2. **Some product modules** (telehealth, patient portal messaging, RPM/CCM) lack explicit representation in the export documentation.
3. **Documentation polish** — many column descriptions are empty, there are no sample files, and data format specifications (date formats, encoding) are missing.

Despite these gaps, this is one of the more thorough (b)(10) implementations among small-to-mid-size EHR vendors. The vendor clearly understands the distinction between (b)(10) and (g)(10), and the CSV-based approach with a relational structure is pragmatic and appropriate.

## Access Summary
- Final URL (after redirects): https://docs.glaceemr.com/Glenwood/transparencydisclosure.html
- Status: found
- Required browser: no
- Navigation complexity: one_click (scroll to EHI section, click PDF link)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The URL returned 200 immediately, the page is static HTML, and the PDF downloaded cleanly on the first attempt. No authentication, no JavaScript rendering needed, no anti-bot measures encountered.
