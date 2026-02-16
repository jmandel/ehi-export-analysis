# EHNOTE, INC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://ehnote.com/certification/ehi-export
- CHPL IDs: 11356 (15.04.04.3171.EHNO.01.00.1.231025)
- Certification date: 2023-10-25
- Product: EHNOTE v1.0

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://ehnote.com/certification/ehi-export" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, `Content-Type: text/html`, served via Cloudflare. No redirects. Last-Modified: 2025-06-03.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://ehnote.com/certification/ehi-export" -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html
```
Result: 31,265 bytes of static HTML. AngularJS-based page (`ng-app="myapp"`) but the EHI export content is rendered server-side in the HTML — no dynamic content loading required.

### Step 3: Search for downloadable files
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' ehi-export-page.html
```
Result: **No downloadable files found.** The page contains zero links to PDFs, ZIPs, CSVs, JSON schemas, or any other downloadable documentation artifacts. The only outbound link is to the terms and conditions page (`https://ehnote.com/certification/openapi-terms-conditions`).

### Step 4: Check the mandatory disclosures / certification page
```bash
curl -sL "https://ehnote.com/certification/certification-link.html" -H 'User-Agent: Mozilla/5.0' -o cert-page.html
```
Result: 24,291 bytes. Contains links to Real-World Testing PDFs, a compliance certificate, and a risk mitigation PDF — none related to EHI export documentation, data dictionaries, or export format specifications.

### Step 5: Check footer links for related content
The footer of the EHI export page includes a "Compliances" section with links to:
- Certifications (certification-link page)
- FHIR END POINT (fhir-endpoints)
- SMART ON FHIR (fhir-api)
- API Documentation (https://openapi.ehnote.com/ — a Postman collection for FHIR API)
- FHIR API Terms and Conditions
- Developer Login (https://interop.ehnote.com/admin/console/auth — login wall)
- EHI Export (this page)

The API documentation at openapi.ehnote.com is a Postman-hosted FHIR API collection — this is for the (g)(10) standardized FHIR API, not the (b)(10) EHI export. The FHIR API page makes no mention of EHI or b(10) export.

### Step 6: Browser verification
Loaded the page in Chrome to verify no JavaScript-rendered content was missed. The page renders identically to the curl-fetched HTML. No expandable sections, accordions, or dynamically loaded content. Screenshots captured.

## What Was Found

The entire EHI export documentation consists of a single static HTML page at the registered URL. There are no downloadable files, no data dictionary, no schema, no API specification, and no sample export files.

### Export Format

The export produces **individual files per patient**, downloaded when the user clicks an "export and download" button in the EHR. The exported files are:

1. **PDF case sheets** — One PDF per appointment per patient, containing the clinical history for that visit. Naming convention: `CaseSheet_{BranchId}P{PatientId}_A{AppointmentDate}.pdf`
   - Example: `CaseSheet_731P518612_A2023-12-08.pdf`
   - Content described as: "Name of the clinic, patient demographics, Chief complaints, Review of systems, Assessments, Medications and other clinical data part of the appointment"

2. **Image files (PNG/JPEG)** — Companion images exported alongside PDFs. These represent investigations, surgery consents, referrals, and authorization documents. Naming convention: `{PatientName}_P{PatientId}_{Date}.{ext}`
   - Example: `Alice_P2546_2023-01-08.PNG`

### File Categories

The documentation lists these categories of exported data:
- **Investigations** — image files (JPEG/PNG)
- **Surgery consents** — image files (JPEG/PNG)
- **Referrals** — image files (JPEG/PNG)
- **Billings and Authorization files** — image files (JPEG/PNG)
- **Case history / Case sheets** — PDF files

### Data Fields

The documentation explicitly states: *"There is no 'one size fits all' set of fields in the software because of the extensive customization that is possible."* It describes PDF field content only at a very high level: "each row will have a field names that related to the case history along with the clinical data represented."

The DATA section for PDFs is described as containing: "Name of the clinic, patient demographics, Chief complaints, Review of systems, Assessments, Medications and other clinical data part of the appointment."

### Linking Mechanism

Files for the same patient are linked by a shared `P####` patient identifier in the filename. Files for the same appointment share both the patient ID and appointment date in the naming convention.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, EHNOTE stores extensive data across clinical, administrative, billing, optical retail, patient engagement, telemedicine, and analytics domains. The EHI export documentation describes a very narrow subset:

**Mentioned in the export documentation:**
- Patient demographics (mentioned in case sheet PDF content)
- Chief complaints (mentioned)
- Review of systems (mentioned)
- Assessments (mentioned)
- Medications (mentioned)
- Clinical visit data ("other clinical data part of the appointment")
- Surgery consents (as image files)
- Investigations / diagnostic data (as image files)
- Referrals (as image files)
- Billing / authorization files (as image files — though the documentation is vague about what "billing" content is actually exported)

**Absent or not mentioned from the product's known data domains:**
- **Ophthalmic-specific data**: Visual acuity measurements, IOP readings, refraction data, DICOM images, anatomical drawings — the core specialty data for this ophthalmology-focused EHR is not specifically addressed
- **Prescriptions / e-prescribing records**: No mention of prescription data export
- **Lab results / diagnostic reports**: Not specifically mentioned (may fall under "Investigations" but unclear)
- **Immunization records**: Not mentioned
- **Problem lists / allergy lists**: Not specifically mentioned (may be in case sheet PDFs)
- **Care plans / goals**: Not mentioned
- **Patient portal communications**: Secure messages, patient-submitted forms/images
- **Telemedicine session records**: Not mentioned
- **Optical retail / POS data**: Inventory, orders, lens prescriptions not mentioned
- **Insurance / enrollment data**: Not specifically addressed
- **Claims / financial transactions**: The documentation says "Billings and Authorization files" exist but provides no detail on format or content
- **ASC surgical documentation**: Pre-op, intra-op, post-op, anesthesia records not specifically mentioned (surgery "consents" are mentioned, but not the full surgical record)
- **Specialty module data**: Dental charts, gynecology records, pediatric growth charts
- **Patient CRM data**: Lead tracking, counseling notes, quotations

The core concern is that this export appears to be appointment-centric PDFs and related images — essentially a printout of the visit record. There is no indication that it exports the full breadth of structured data the system stores.

### Export Format & Standards

The export uses **PDFs and image files** — the least computable format possible. This is essentially a "print to PDF" export of clinical encounter records plus scanned/attached document images.

- No structured data format (no FHIR, no C-CDA, no CSV, no JSON, no XML, no SQL dump)
- No machine-readable schema or data dictionary
- No API endpoint for bulk data extraction
- The PDF format means that extracting individual data elements (diagnoses, medications, vitals, etc.) requires OCR or PDF parsing — the structured data that exists in the EHR database is flattened into rendered documents
- A third party could not reconstruct a patient record programmatically from this export; they could only read PDFs and look at images

The (b)(10) requirement asks for export of all electronic health information. While there's no format mandate, exporting only as PDFs means the structured nature of the data is lost. A medication list in a PDF is fundamentally less useful than a structured medication list in any computable format.

### Documentation Quality

The documentation is **minimal and vague**:

- **No data dictionary**: There is no field-level documentation of what data is in the exported PDFs or images. The documentation explicitly acknowledges this gap: "There is no 'one size fits all' set of fields."
- **No schema or format specification**: Beyond the file naming convention, there is no specification of what the PDFs contain or how they are structured.
- **No sample export files**: No examples of what an exported PDF looks like or what data fields are included.
- **No export instructions**: The documentation says files are "downloaded individually once the export and download button is clicked" but provides no step-by-step guide, screenshots of the export interface, or user workflow documentation.
- **No worked examples**: Beyond the file naming examples, there are no examples of actual export content.
- The documentation reads as a compliance checkbox rather than a practical technical guide. A developer or data analyst receiving these exported PDFs would have essentially no guidance on what data to expect or how to process it.

### Structure & Completeness

- **Field-level documentation**: None. The documentation only names broad categories (demographics, complaints, assessments, medications) without defining specific fields, data types, value sets, or structures.
- **Value sets / coded fields**: Not documented at all.
- **Relationships between entities**: Described only by filename convention (patient ID links files together).
- **Versioning**: None visible. The page was last modified 2025-06-03.
- **Completeness**: The documentation is essentially a 2-page description of file naming conventions plus legal boilerplate (terms of use, liability, etc.). The substantive technical content is approximately 500 words.

### Overall Assessment

EHNOTE's EHI export documentation is among the most minimal possible. The export itself appears to be a per-patient, per-appointment PDF dump with associated image attachments — essentially what you would get if you printed the patient chart to PDF. While this captures the rendered clinical information visible to users, it:

1. **Loses all structure**: Structured data (diagnoses coded in ICD-11, medications, vitals, etc.) becomes unstructured text in a PDF
2. **Covers only clinical encounters**: There's no evidence that billing records, optical retail data, patient portal content, telemedicine sessions, or specialty-specific structured data (visual acuity measurements, IOP trends, etc.) are included
3. **Provides no data dictionary**: The documentation explicitly acknowledges the lack of standardized field definitions due to "extensive customization"
4. **Has no computable artifacts**: No schema, API spec, CSV template, or any machine-readable documentation

This is a small vendor (200+ practices) with a certification from October 2023. The export approach and documentation appear to represent minimal compliance effort rather than a thoughtful approach to health information portability.

## Access Summary
- Final URL (after redirects): https://ehnote.com/certification/ehi-export
- Status: found
- Required browser: no (static HTML works with curl)
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare in pass-through mode, no challenge)

## Obstacles & Dead Ends
- No obstacles encountered accessing the documentation
- The `/certification/` index page returns "You do not have permission to view this directory or page" — but the specific EHI export URL works fine
- The certification disclosures page was checked for additional EHI-related links — none found
- The openapi.ehnote.com Postman API documentation was verified to be FHIR (g)(10) API docs, not related to the (b)(10) EHI export
- No downloadable files exist on the EHI export page — the entire documentation is inline HTML text
