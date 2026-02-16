# Universal EHR, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.universalehr.com/exportdoc.aspx
- CHPL IDs: 9333
- Product: Universal EHR v2.0.0
- Certification date: 2018-03-12

## Navigation Journal

### Step 1: Probe the registered URL

```bash
curl -sI -L "https://www.universalehr.com/exportdoc.aspx" -H 'User-Agent: Mozilla/5.0'
```

Returned HTTP 200 with `Content-Type: text/html; charset=utf-8`, 878 bytes. The page is a simple ASP.NET wrapper that embeds a PDF via iframe:

```html
<iframe src=EHI_Document.pdf width=100% height=1500px ...>
```

### Step 2: Download the PDF

```bash
curl -sL "https://www.universalehr.com/EHI_Document.pdf" -H 'User-Agent: Mozilla/5.0' -o EHI_Document.pdf
```

Confirmed as a real PDF: 6 pages, 2,463,290 bytes. Created 2023-11-16 using Chrome's "Print to PDF" from the URL `https://universalehr.com/PatientExport/EHIDocument/`.

### Step 3: Examine the PDF content

Extracted text with `pdftotext` and rendered all 6 pages as images with `pdftoppm`. The PDF is a screenshot-based user guide showing the EHI export interface with annotated screenshots.

### Step 4: Check referenced URLs

The PDF footer references `https://universalehr.com/PatientExport/EHIDocument/` on every page. This page is live (16,073 bytes) and contains the same content as the PDF — it's the HTML source that was printed to PDF.

The first page states: "We use EMR Direct Interoperability Engine as our authorization server. For more information, please visit this link." The link targets EMR Direct's Open API Documentation at `https://www.interopengine.com/2021/open-api-documentation.html`.

### Step 5: Examine the EMR Direct documentation

The EMR Direct Interoperability Engine 2021 documentation describes a standard FHIR R4 API implementing the SMART App Launch Framework. It explicitly states:

- Resources conform to US Core Implementation Guide Release 3.1.1
- Supported resource types: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance
- FHIR Bulk Data Access Group export is supported
- This is external third-party infrastructure, not Universal EHR's own documentation

This is the standard (g)(10) FHIR API, not a (b)(10)-specific data export.

### Step 6: Check vendor homepage for additional documentation

The vendor homepage at `https://www.universalehr.com` links to several documents. None contained additional EHI export documentation:

- `Mandatory_Disclosure.pdf` — cost/pricing disclosure (2 pages, 2018), no EHI export content
- `Compliance_Certificate_Universal_EHR_2.0.0_122624.pdf` — compliance certificate (1 page, 2024), no EHI export content
- `D13_Description.pdf` — multi-factor authentication description (4 pages, 2021), no EHI export content
- `exportdoc.aspx` — the registered URL itself (links back circularly)

No additional EHI export data dictionary, schema file, or format specification was found anywhere on the vendor's website.

## What Was Found

The EHI export documentation consists of a single 6-page PDF that is a print-to-PDF capture of an internal documentation page. It provides:

**Export process instructions (user guide):**
1. Log into UniversalEHR
2. Click the "EHI EXPORT" link from the main patient screen
3. Select one or more patients using checkboxes (can filter by modification date/time, search by Patient ID or demographics)
4. Click "Start Export" — a "Please wait" message appears during processing
5. Click "Download all files as a ZIP file" to download

**Export format:**
- Data is exported as NDJSON (newline-delimited JSON) files containing FHIR resources
- Each patient gets a folder named by Patient ID
- Each folder contains FHIR NDJSON files for various resource types
- A `Readme.txt` points to `https://build.fhir.org/nd-json.html`
- A `Documents` subfolder contains patient document files (PDFs, images)

**FHIR resource types visible in the export screenshots (from page 4):**
- Provenance_1.ndjson
- Practitioner_1.ndjson
- Patient_1.ndjson
- Organization_1.ndjson
- Observation_1.ndjson
- MedicationRequest_1.ndjson
- Invoice_1.ndjson
- Encounter_1.ndjson
- DocumentReference_1.ndjson
- Condition_1.ndjson
- CareTeam_1.ndjson
- Appointment_1.ndjson

**Patient documents visible in the export screenshots (from page 6):**
- Mammogram results (PDFs)
- OCM records (PDFs)
- Lab reports (PDFs)
- Referral documents (PDFs)
- Various other clinical documents

**What is NOT provided:**
- No data dictionary or field-level documentation
- No schema files (no XSD, JSON Schema, or OpenAPI spec)
- No sample export data
- No explanation of how data maps between the EHR's internal tables and FHIR resources
- No documentation of value sets or coded fields
- No description of what data goes into each FHIR resource type
- No mention of billing data, charges, claims, or financial records in the export
- No mention of specialty-specific clinical data beyond what FHIR US Core covers

## Export Coverage Assessment

### Data Domain Coverage

The export produces FHIR NDJSON files corresponding to a subset of FHIR resource types. Based on the screenshots and the EMR Direct documentation, the covered FHIR resources map to US Core / USCDI data classes:

**Clearly covered (evidenced by NDJSON files in screenshots):**
- Patient demographics (Patient)
- Conditions/Problems (Condition)
- Medications (MedicationRequest)
- Observations/Vitals/Labs (Observation)
- Encounters (Encounter)
- Care Teams (CareTeam)
- Clinical documents (DocumentReference + Documents subfolder with actual PDFs/images)
- Provenance
- Practitioner/Organization reference data
- Appointments (Appointment — interesting, this goes slightly beyond US Core)
- Invoices (Invoice_1.ndjson — this is notable as Invoice is not a US Core resource)

**Possibly missing or undocumented:**
- **Billing/claims data**: The Invoice NDJSON file is a positive signal, but there is no documentation of what billing fields are captured. The product research indicates the system handles claims, billing, superbills, charge capture, and collections. Whether the Invoice resource captures all of this is unknown.
- **Prescriptions/e-prescribing history**: MedicationRequest is present, but the full e-prescribing workflow (prescription status, pharmacy information, refill history) is unclear.
- **Lab orders**: Only Observation is visible; DiagnosticReport and ServiceRequest for lab ordering workflows are not visible in the export screenshots.
- **Allergies**: AllergyIntolerance is listed in EMR Direct's supported resources but not visible in the export screenshot file listing.
- **Immunizations**: Similarly supported by EMR Direct but not visible in the export.
- **Care Plans/Goals**: CarePlan and Goal are not visible in the export.
- **Procedures**: Not visible in the export screenshots.
- **Device information**: Not visible.
- **Diagnostic images (EKGs, etc.)**: The product stores diagnostic device data (EKG graphs automatically filed in charts). These may be in the Documents subfolder as image files, but this is not documented.
- **Custom specialty templates**: The product offers customizable templates for OB/GYN, cardiology, pediatrics, internal medicine, and other specialties. There is no documentation of how specialty-specific clinical data is exported. Standard FHIR US Core resources likely cannot capture the full structure of these specialty templates.
- **Messages**: Provider-to-patient (Doctor Direct) and provider-to-provider (Physician's Portal) messages are a feature of the product. No communication resource is visible in the export.

### Export Format & Standards

The export uses **FHIR R4 NDJSON** format, which is a recognized standard. However:

- The Readme.txt in the export simply points to `https://build.fhir.org/nd-json.html` — a generic FHIR spec page, not custom documentation.
- The EMR Direct Interoperability Engine documentation confirms US Core 3.1.1 profiles, but this is the (g)(10) API documentation, not (b)(10)-specific documentation.
- The presence of `Invoice_1.ndjson` and `Appointment_1.ndjson` is interesting — these are not US Core resources. This suggests the vendor may have extended beyond pure (g)(10) exports for some resource types, but there is zero documentation of what fields are populated in these non-US-Core resources.
- Patient documents (PDFs, images) are included as actual files in a Documents subfolder — this is a good approach for document-heavy records.

**Critical question**: Could a third party reconstruct the patient record from this export? **Partially.** The FHIR NDJSON provides structured clinical data in a standard format, and the Documents subfolder provides the actual clinical documents. However, without a data dictionary or field mapping, there is no way to know what data is being omitted. There is no schema documentation to understand the Invoice or Appointment resources, and specialty-specific clinical data is unaccounted for.

### Documentation Quality

The documentation is **very minimal** — a 6-page screenshot walkthrough of the export UI, with no technical detail about the exported data itself.

- **No data dictionary**: There are no table definitions, field listings, or schema descriptions.
- **No data type or value set documentation**: The only FHIR profile information comes from EMR Direct's generic (g)(10) API docs, which cover standard US Core resources.
- **No worked examples or sample data**: The screenshots show a Notepad++ window with MedicationRequest NDJSON, but this is a redacted screenshot, not a downloadable sample file.
- **No developer documentation**: A developer trying to import this data would need to reverse-engineer the NDJSON content with no vendor guidance on what to expect.
- **Clearly a compliance checkbox**: The documentation was created in November 2023 as a quick Chrome "Print to PDF" of an internal page with screenshots. It took minimal effort and addresses only the "how do I click the button" question, not the "what data is in the export" question.

### Structure & Completeness

- **Granularity**: The documentation provides only the names of NDJSON files (resource type names). There is no field-level documentation whatsoever.
- **Coded fields**: Not documented. The EMR Direct API docs reference US Core value sets generically.
- **Relationships between entities**: Not documented. The FHIR references between resources (e.g., MedicationRequest.subject -> Patient) follow FHIR conventions, but there's no vendor-specific documentation.
- **Versioning/change history**: None. The document was created 2023-11-16 and does not appear to have been updated.

### The (b)(10) vs (g)(10) Assessment

This appears to be a **classic case of (g)(10) repackaged as (b)(10)**. The evidence:

1. The documentation page links directly to EMR Direct's Interoperability Engine, which is their (g)(10) FHIR API infrastructure.
2. The FHIR resource types in the export closely mirror the (g)(10) US Core resource list.
3. There is no mention of billing data, specialty-specific clinical data, or any data beyond USCDI.
4. No data dictionary exists to describe what fields are exported or how the EHR's internal data model maps to FHIR.

**However**, two elements suggest the vendor may have gone slightly beyond pure (g)(10):
- `Invoice_1.ndjson` — Invoice is not a US Core resource and suggests some billing data export
- `Appointment_1.ndjson` — Appointment is not a US Core resource
- The Documents subfolder with actual patient documents (mammograms, labs, referrals) provides real clinical content

These additions are positive but undocumented. Without field-level documentation of the Invoice resource content, it's impossible to assess whether billing coverage is meaningful or token.

### Overall Assessment

Universal EHR's EHI export documentation represents a **minimal compliance effort** from a very small vendor. The export mechanism itself appears to work (the screenshots show a functional UI), and the choice of FHIR NDJSON plus a documents folder is reasonable. But the documentation provides zero technical detail about the exported data. For a product that stores specialty-specific clinical templates, billing/claims data, e-prescribing records, diagnostic device data (EKGs), and provider-patient messaging, the documentation makes no attempt to describe how any of this is (or isn't) included in the export. A developer, patient, or health information exchange partner would have no way to assess the completeness of an export without actually running one and inspecting the output.

## Access Summary
- Final URL (after redirects): https://www.universalehr.com/exportdoc.aspx (no redirects)
- Status: found
- Required browser: no (direct PDF download from HTML wrapper)
- Navigation complexity: direct_link (page embeds PDF via iframe, PDF is directly downloadable)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The URL returned 200 immediately and the PDF was directly downloadable.
- The EMR Direct Interoperability Engine documentation at `https://www.interopengine.com/2021/open-api-documentation.html` was accessible but is third-party (g)(10) infrastructure documentation, not Universal EHR-specific (b)(10) documentation.
- No additional EHI-specific documentation was found anywhere on the vendor's website despite checking the homepage, mandatory disclosure, compliance certificate, and certification information pages.
