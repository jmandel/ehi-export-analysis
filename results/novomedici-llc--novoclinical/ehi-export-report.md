# NovoMedici, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://s3.amazonaws.com/novoclinical.miscellaneous/Novoclinical+Data+Export+Format.pdf
- CHPL IDs: 10805
- Product: NovoClinical v1.0 (certified 2022-01-31)

## Navigation Journal

**1. Initial probe of the registered URL:**
```bash
curl -sI -L "https://s3.amazonaws.com/novoclinical.miscellaneous/Novoclinical+Data+Export+Format.pdf" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, Content-Type: application/pdf, Content-Length: 129544 bytes. Direct PDF download from Amazon S3. Last-Modified: 2023-10-08.

**2. Downloaded the PDF:**
```bash
curl -sL "https://s3.amazonaws.com/novoclinical.miscellaneous/Novoclinical+Data+Export+Format.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/Novoclinical-Data-Export-Format.pdf
```
Verified with `file` command: confirmed as "PDF document, version 1.7, 1 page(s)". Created with Microsoft Word for Microsoft 365 on 2023-10-07.

**3. Extracted text and rendered the PDF visually:**
The PDF is a single page. It contains:
- A title: "Novoclinical Data Export Format"
- Two bullet points describing the export formats (C-CDA and CSV)
- Navigation instructions for performing the export
- A screenshot of the export interface in NovoClinical

**4. Checked the vendor's mandatory disclosures page:**
Navigated to https://www.novomedici.com/meaningful-use/ in a browser. The page lists several links:
- "Novoclinical V1 Mandatory Disclosures and Costs" — regulatory disclosure PDF, not EHI-specific
- "Application access" / "Patient selection" — (g)(7) documentation
- "NovoClinical API terms of use" — API terms
- Footer link "EMR Data Export" — points to the same PDF already downloaded

**5. Checked the API documents page:**
Navigated to https://www.novomedici.com/api-documents/. This page only contains FHIR API base URLs and Smart-on-FHIR configuration links — this is (g)(10) API documentation, not EHI export documentation.

**6. Conclusion:** The entire EHI export documentation is the single one-page PDF.

## What Was Found

The EHI export documentation consists of a single one-page PDF that describes the export mechanism in three short sentences:

> **C-CDA (Consolidated Clinical Document Architecture)** — Each patient will have a C-CDA document in the exported data.
>
> **CSV** — Comma separated value, used for patient demography, Appointments.
>
> Data export can be done by clinic administrators by navigating to Communication > Data Export. The below page opens and let you choose the specific patient export or group export of all or multiple patients. Once exported administrator will be able to export the data in a ZIP file which will contact the CCD-A, CSV file.

The PDF includes a screenshot of the export interface, which shows:
- A "Data Export" page with a "Patient Export" tab selected
- Patient selection fields (patient name, date range options)
- An "Export Data" button and a "Reset" button
- The NovoClinical navigation bar showing modules: Clinical, Billing, Reporting, Reports, Admin, Templates, Scheduler

That is the entirety of the documentation. There is no data dictionary, no field-level documentation, no schema, no sample files, no format specification for the CSV files, and no description of what C-CDA sections or templates are used.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, NovoClinical is an all-in-one ambulatory EHR and practice management system that stores:
- Clinical data (charting, problem lists, medications, allergies, labs, vitals, immunizations, implantable devices, clinical notes)
- Prescribing data (e-prescriptions, medication history)
- Scheduling data (appointments, check-ins, referrals)
- Billing/RCM data (claims, billing codes, payments, DME billing, statements)
- Patient portal data (messages, patient-entered history, e-signed documents)
- Telemedicine data (virtual visit records)
- Chronic care management data (care plans, monitoring)
- Communication records (e-faxes, text messages, direct messages)
- Public health reporting data (immunization registries, syndromic surveillance, cancer case reports)

The export documentation explicitly mentions only:
- **C-CDA documents**: These would cover a standard clinical summary — problems, medications, allergies, lab results, vitals, immunizations, procedures, and possibly some clinical notes. However, C-CDA is a clinical summary standard; it does not cover the full breadth of data an EHR stores.
- **CSV for "patient demography, Appointments"**: Demographics and appointment scheduling data only.

**Clearly missing or unaddressed domains:**
- **Billing and financial data** — claims, charges, payments, statements, coding. This is a core function of the product (it's marketed as "Medical Billing Software for Small Business") and there is no mention of billing data in the export.
- **Clinical notes beyond C-CDA summaries** — progress notes, H&P, specialty-specific documentation. C-CDA may carry some notes, but the documentation doesn't specify which sections are populated.
- **Prescribing data** — e-prescribing history beyond what C-CDA might include.
- **Patient portal data** — secure messages, patient-entered forms, e-signatures.
- **Telemedicine records** — virtual visit documentation.
- **Chronic care management data** — care plans, monitoring records.
- **Communication records** — faxes, text messages, direct messages.
- **Referrals and care coordination data**.
- **Custom templates and specialty-specific clinical data**.
- **Documents, images, and attachments** in the patient record.
- **Lab and imaging orders** (as distinct from results in C-CDA).

The export appears to be a narrow clinical summary (C-CDA) plus basic demographics and scheduling (CSV), covering perhaps 20-30% of what the product actually stores. This is a significant gap for a (b)(10) EHI export requirement.

### Export Format & Standards

The export uses two formats:
- **C-CDA**: A recognized HL7 standard for clinical document exchange. However, the documentation does not specify which C-CDA document type (CCD, Discharge Summary, etc.), which template versions, or which optional sections are populated. Without this information, a recipient cannot know what data to expect.
- **CSV**: For demographics and appointments. No column definitions, delimiter specifications, encoding details, or sample files are provided.

The output is delivered as a ZIP file containing C-CDA XML and CSV files.

The format choice is partially appropriate — C-CDA handles standard clinical data reasonably well, but it cannot represent billing records, custom clinical forms, communications, or many other data domains the product stores. A true (b)(10) export would need additional formats (database dump, additional CSV files for billing tables, etc.) to cover the full designated record set.

### Documentation Quality

The documentation is extremely minimal — arguably the bare minimum that could be called "documentation." Specific deficiencies:

- **No data dictionary**: There are no field definitions for either the C-CDA content or the CSV files.
- **No schema or format specification**: The CSV columns are not defined. The C-CDA template constraints are not documented.
- **No sample files**: No example exports are provided.
- **No value sets or coded field documentation**: No indication of what coding systems are used or how coded values map.
- **No relationship documentation**: No description of how the C-CDA and CSV files relate to each other.
- **No import guidance**: A developer could not implement an import of this data based on this documentation alone.

A developer receiving this export would have to reverse-engineer the file formats entirely from actual export files.

### Structure & Completeness

- **Granularity**: The documentation operates at the format level only ("C-CDA" and "CSV"). There is no table-level, field-level, or element-level documentation.
- **Value sets**: Not documented.
- **Relationships**: Not documented.
- **Versioning**: The PDF has no version number. The Last-Modified date on S3 is October 2023.

This is among the most minimal EHI export documentation possible — a single page that names two file formats and shows a screenshot of how to trigger the export. It does not meet the informational needs of anyone trying to understand, verify, or use the exported data.

## Access Summary
- Final URL (after redirects): https://s3.amazonaws.com/novoclinical.miscellaneous/Novoclinical+Data+Export+Format.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The mandatory disclosures page (https://www.novomedici.com/meaningful-use/) uses Brotli compression that prevented direct curl text extraction; browser rendering was needed to read the page. However, the page contained no additional EHI export documentation.
- The API documents page (https://www.novomedici.com/api-documents/) was checked but only contains FHIR/Smart-on-FHIR API links relevant to (g)(10), not (b)(10) EHI export.
- No additional documentation was found anywhere on the vendor's site.
