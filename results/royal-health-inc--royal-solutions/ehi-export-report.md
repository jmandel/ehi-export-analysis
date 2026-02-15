# Royal Health, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://royalsolutionsprod.blob.core.windows.net/public/publicimages/certification/DocumentationB10FormatExport.pdf
- CHPL ID: 10770
- Product: Royal Solutions v5
- Certification date: 2021-12-29

## Navigation Journal

The registered URL is a direct link to a PDF file hosted on Azure Blob Storage.

```bash
curl -sI -L "https://royalsolutionsprod.blob.core.windows.net/public/publicimages/certification/DocumentationB10FormatExport.pdf" -H 'User-Agent: Mozilla/5.0'
# HTTP/1.1 200 OK
# Content-Type: application/pdf
# Content-Length: 284907
# Last-Modified: Thu, 09 Nov 2023 21:37:51 GMT
```

Downloaded directly:
```bash
curl -sL "https://royalsolutionsprod.blob.core.windows.net/public/publicimages/certification/DocumentationB10FormatExport.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/DocumentationB10FormatExport.pdf
```

Verified: `file` reports "PDF document, version 1.7, 10 page(s)". PDF metadata shows author "Karol Guzman", created via "Microsoft Word for Microsoft 365", dated 2023-11-09.

Also checked the vendor's mandatory disclosures / certifications page at https://www.royalsolutionsgroup.com/web/company/certifications.aspx (redirects to https://info.royalsolutionsgroup.com/certifications). That page links only to Real World Testing PDFs (2023–2025 test plans and results reports) — no additional EHI export documentation.

Attempted to list the Azure Blob container for additional certification documents, but container listing is not publicly accessible.

## What Was Found

The PDF is titled **"Royal Solutions 5.0 — B10 Electronic Health Information Export"** and is a 10-page data dictionary documenting a CSV-based export format. The document explicitly states:

> "The B10 ONC export contains the electronic health information available for the patients' records. There will be different files in comma-delimited file format. There will be one zip file containing the csv files and other zip files that contain the images/documents for each patient."

The export format is a **ZIP archive** containing:
1. Multiple CSV files (one per data domain)
2. Additional ZIP files containing images/documents for each patient

The document defines **12 CSV files** with field-level documentation (field name + description for every field):

| CSV File | Fields | Description |
|----------|--------|-------------|
| **Patients.csv** | 49 | Demographics, contact info, guarantor, employer, emergency contacts, mammography/DEXA tracking dates |
| **Appointments.csv** | ~85 | Exam scheduling, status, referring providers, insurance (primary/secondary/tertiary), authorizations, CPT codes, modality, visit notes, BI-RADS codes |
| **Transactions.csv** | 18 | Payment transactions — amounts requested/authorized/captured, payment types, transaction states, facility info |
| **Orders.csv** | 31 | Referral orders — ordering provider info, order source, exam details, form submissions, scheduling |
| **Demographics2.csv** | 14 | Previous names, previous addresses, granular race/ethnicity data, PCP |
| **Allergies.csv** | 7 | RxNorm-coded allergies with onset dates, status, SNOMED reaction codes, severity |
| **Devices.csv** | 12 | Implantable devices — UDI, device codes, manufacturing/expiration dates, lot/serial numbers |
| **Immunizations.csv** | 8 | CVX-coded vaccines with administration dates, lot numbers, manufacturer, status |
| **Medications.csv** | 8 | RxNorm-coded medications with start/end dates, frequency, route, dose |
| **Problems.csv** | 6 | SNOMED-coded problem list with dates and status |
| **Procedures.csv** | 7 | SNOMED-coded procedures with dates, status, notes, author |
| **Vitals.csv** | 15 | Vital signs — height, weight, BP, heart rate, O2, temperature, respiratory rate, BMI/weight/head percentiles |

## Export Coverage Assessment

### Data Domain Coverage

**Covered domains:**
- **Patient demographics** — comprehensive (49 fields including guarantor, employer, emergency contacts, mammography/DEXA tracking dates, smoking status, language, race, ethnicity, marital status). The Demographics2.csv adds previous names/addresses and granular race data.
- **Radiology appointments/exams** — extremely detailed (the largest file at ~85 fields). Includes accession numbers, exam codes, modality types, exam status, BI-RADS codes, referring providers, visit notes, schedule notes, admission/discharge dates, CPT codes, exam priority, resources/equipment, and insurance authorization details. This is the core operational data of a radiology RIS.
- **Insurance/billing** — covered at the appointment level with primary, secondary, and tertiary insurance data (plan, subscriber, group numbers, carrier, payer type, insured demographics). Authorization details (status, ICD codes, CPT codes, reference numbers, case numbers) are included. Financial transactions are in Transactions.csv with payment amounts, types, and states.
- **Orders/referrals** — covered with provider info, order source, form submissions, exam details, scheduling source.
- **Clinical data (standard)** — allergies (RxNorm-coded), medications (RxNorm-coded), problems (SNOMED-coded), procedures (SNOMED-coded), immunizations (CVX-coded), vitals, implantable devices (UDI). All use standard terminologies.
- **Documents and images** — mentioned in the introduction ("other zip files that contain the images/documents for each patient") but not documented with a schema. The format of these sub-ZIPs is not described.

**Domains that appear missing or under-documented:**

- **Radiology reports** — Surprisingly, there is no dedicated CSV for radiology report content (dictated/finalized report text). The Appointments.csv has `ExamResultsStatus` (Final, Addendum, Dictated, Prelim) and `ExamFinalizedDate`, but not the actual report text. For a radiology RIS, the diagnostic report text is perhaps the single most important clinical record. It may be included in the images/documents ZIP, but this is not documented.
- **Clinical notes** — The product is certified for (a)(4) clinical decision support and stores clinical notes. There is no CSV for clinical/progress notes. Again, these may be in the documents ZIP.
- **Mammography and lung screening tracking records** — Only `LastMammoDate`, `LastDexaDate`, `LastCompletedMammoDate`, `LastCompletedDexaDate` fields appear in Patients.csv, and `BiradCode` in Appointments.csv. The product has dedicated mammography and lung screening tracking modules, but there's no dedicated export of tracking records, follow-up recommendations, or recall status.
- **Patient portal interactions** — Secure messages, portal activity, patient-submitted documents, pre-registration forms — none of these have a dedicated CSV.
- **Claims detail** — While Transactions.csv covers payment transactions, there is no dedicated claims CSV with line-item billing detail (charge amounts per CPT, adjustments, denials, EOBs). The insurance and CPT data is embedded in Appointments.csv but claims lifecycle data is limited.
- **Care plans, goals, referral tracking** — Not present (though these may be minimal for a radiology-focused product).
- **Family health history** — The product is certified for (a)(12) but no family history data appears in the export.
- **Patient education materials** — Not present (not necessarily required as EHI).

### Export Format & Standards

The export uses a straightforward **CSV-in-ZIP** approach — a practical, computable format that is entirely appropriate for a radiology information system. This is a genuine (b)(10) export, not a repackaged FHIR API:

- The format is **vendor-specific CSV**, not FHIR or C-CDA
- Clinical fields use **standard terminologies** where applicable (RxNorm for medications/allergies, SNOMED for problems/procedures/reactions, CVX for immunizations, UDI for devices)
- Relationships between records are maintained through **PatientMRN** (linking all CSVs to a patient) and **AccessionNumber** (linking appointments to transactions and orders)
- The format includes extensive **radiology-specific operational data** (modality types, exam codes, BI-RADS, accession numbers, exam resources, scheduling) that would never appear in a USCDI/US Core export — a clear sign this is genuine (b)(10) work
- The inclusion of **billing/insurance data** (three tiers of insurance, authorization details, CPT codes, payment transactions) further confirms this goes well beyond (g)(10)
- Patient images/documents are included as separate ZIP files per patient — a reasonable approach for DICOM and scanned documents

A third party could substantially reconstruct most of the patient record from this export, with the notable exception of radiology report text (if it's not in the documents ZIP) and the undocumented structure of the image/document sub-archives.

### Documentation Quality

**Strengths:**
- Clean, well-structured PDF with consistent field/description table format
- Every field in every CSV is documented with a description
- Descriptions are substantive — not just restating the field name but explaining the business meaning (e.g., explaining when Subscriber# will be null, what ExamResultsStatus values look like, how ExamCode is derived)
- The document clearly states the export format (ZIP of CSVs + document ZIPs)
- Standard terminology codes are identified (RxNorm, SNOMED, CVX)

**Weaknesses:**
- **No data types specified** — fields are described but there's no indication of data types (string, date, integer, boolean), lengths, or formats. Are dates ISO 8601? MM/DD/YYYY? Unknown.
- **No value sets documented** — coded fields like `ExamStatus`, `EligibilityStatus`, `AuthorizationStatus`, `VisitStatus`, `State` (in Transactions) mention example values inline but don't provide exhaustive value sets.
- **No sample data or example files** — there are no worked examples, sample CSVs, or example records.
- **The documents/images ZIP structure is undocumented** — mentioned in the introduction but no schema for how images and documents are organized within the per-patient ZIPs.
- **No encoding specification** — CSV delimiter is stated as comma, but character encoding (UTF-8?), quoting conventions, and line endings are not specified.
- **No versioning or change history** — the document was created 2023-11-09 and there's no indication of revision tracking.

### Structure & Completeness

The documentation provides **field-level granularity** (field names + text descriptions) for 12 CSV files covering approximately 260 total fields. This is a genuine data dictionary, not a high-level summary. However, it stops at the description level — there are no data types, cardinality indicators, constraints, or formal value set bindings. It's sufficient for a human to understand the export but would require trial-and-error for a developer to implement a reliable import parser.

For a small radiology-focused vendor, this is above-average documentation. The CSV format is practical and the field coverage reflects the product's actual operational data (not just USCDI). The main gap is the lack of radiology report text in the documented CSV structure — for a RIS, this is a significant omission if the report content isn't included in the undocumented documents/images archive.

## Access Summary
- Final URL (after redirects): https://royalsolutionsprod.blob.core.windows.net/public/publicimages/certification/DocumentationB10FormatExport.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The registered URL worked as a direct PDF download with no authentication, redirects, or anti-bot measures required.
