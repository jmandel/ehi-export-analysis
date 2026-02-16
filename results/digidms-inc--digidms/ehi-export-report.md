# DigiDMS, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://digidms.com/ehr/ehi-export
- CHPL IDs: 11549
- Product: DigiDMS v25.0
- Certification date: 2024-12-12

## Navigation Journal

**1. Initial probe of the registered URL:**
```bash
curl -sI -L "https://digidms.com/ehr/ehi-export" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, Content-Type: text/html, 10,510 bytes. The page is hosted on Microsoft IIS/10.0 with ASP.NET.

**2. Fetched and examined the HTML:**
The HTML is an AngularJS SPA shell (`data-ng-app="clinicspectrum"`) with no inline content — the actual page content is loaded dynamically via `ui-router` into a `data-ui-view` div. The SPA framework is AngularJS 1.x.

**3. Located the route template:**
Downloaded `app/app.js` (69KB) and found the route definition:
```javascript
.state('Ehr.ehi-export', {
    url: '/ehi-export',
    templateUrl: "app/views/Ehr/EHIexport.html",
})
```

**4. Downloaded the EHI export template directly:**
```bash
curl -sL "https://digidms.com/app/views/Ehr/EHIexport.html" -H 'User-Agent: Mozilla/5.0'
```
This returned 1,977 bytes of HTML containing:
- A title "Electronic Health Information - Export"
- A link to the PDF: `https://digidms.com/documents/B10_EHI_Export.pdf`
- A paragraph describing the export: C-CDA format, single and bulk patient export, no developer assistance needed

**5. Downloaded the PDF:**
```bash
curl -sL "https://digidms.com/documents/B10_EHI_Export.pdf" -H 'User-Agent: Mozilla/5.0' \
  -o downloads/B10_EHI_Export.pdf
```
Confirmed: `file` reports "PDF document, version 1.7, 7 page(s)", 1,283,932 bytes. Created 2025-11-18 by "Hemant J. Patel" using "Microsoft: Print To PDF" from a Word document titled "B10 - EHI Export.docx".

**6. Attempted browser rendering:**
Navigated Chrome to `https://digidms.com/ehr/ehi-export` — the page timed out (AngularJS SPA failed to fully render). Only a "Scroll" link was visible. This is consistent with product research noting the site is "heavily JavaScript-rendered and was not accessible via standard web scraping."

**7. Checked for additional documentation:**
- Examined all AngularJS routes in `app.js` — found `Ehr.FHIR` route linking to SmartOnFHIR API docs, but these are (g)(10) FHIR API documentation, not (b)(10) EHI export documentation. The EHI export is explicitly C-CDA, not FHIR.
- Probed `/documents/` directory — returned 403 (directory listing disabled).
- Tested several plausible document filenames (DataDictionary.pdf, EHI_Export.pdf, etc.) — all returned 10,510-byte HTML (the SPA shell), confirming the server has a catch-all route. Only `B10_EHI_Export.pdf` was a genuine PDF.
- Checked the mandatory disclosures page (`/ehr/costlimitations`) — no EHI-specific cost or limitation information found.

## What Was Found

The entire EHI export documentation consists of a **single 7-page PDF** (`B10_EHI_Export.pdf`). The document describes:

### Overview (page 2)
The export uses **C-CDA format** (HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide). Users can export EHI for single patients or patient populations. The export is user-initiated (no developer/technical assistance required).

### Export Options (pages 3–4)
Two modes are documented with screenshots of the DigiDMS UI:

1. **Single patient PHI Export**: From the patient chart, a "Clinical Document Section" dialog lets users select which sections to include (Encounters, Problems, Allergies, Medications, Social History, Results, Assessment and Plan, Immunizations, Procedures, Goals, Implanted Devices, Health Concerns, Functional Status, Reason for Referral). The screenshot shows checkboxes for each section with a date range filter.

2. **Patient Population Export**: From the "Patient Screening" module, users run a query (e.g., "Diabetic patients"), view a results list, and use an "Export" dropdown with options for Excel or CCDA. The screenshot shows 11 records found for a diabetic patient query.

Access to export functionality requires granted permissions — users must "raise request for grants to specific export functionality."

### Export Format / Data Dictionary (pages 5–7)
A two-column table lists the C-CDA sections and their elements:

| Section | Elements |
|---------|----------|
| Patient | Name, Date of Birth, Sex, Race, Ethnicity, Language, Contact Information, Patient Id |
| Provider | Contact Information |
| Author | Contact Information |
| Practice | Contact Information |
| Reason for Referral | (no sub-elements listed) |
| Allergies | Substance, Reaction, Severity, Status |
| Encounters | Encounter, Location, Date, Diagnosis |
| Immunization | Vaccine, Date, Status |
| Medication | Medication, Direction, Quantity, Date |
| Health Concern | Concern, Status, Date |
| Interventions | Planned Intervention, Status, Date |
| Goals | Goal, Value, Date |
| Medical Equipments | Implant, Area, UDI |
| Problems | Condition, Effective Date, Status |
| Procedures | Procedure, Date |
| Care Plan | Observation, Date |
| Assessment | Problem, Date, Comments |
| Results | Result, Date, Interpretation, Reference Range, Remarks |
| Social History | Social History Element, Description, Effective Date |
| Vital Signs | Vital Sign, Date, Value |
| Functional Status | Criteria, Status |

**Note**: The PDF title page says "DigiDMS and 22.0" (version 22.0) while the current certified version is 25.0 and the web page text references "DigiDMS 25.0". The PDF was created November 2025 — it appears the version number on the title page was not updated, but the document was newly created for the current certification.

## Export Coverage Assessment

### Data Domain Coverage

The export covers **standard clinical summary data** that maps to C-CDA sections. Comparing against what the product research identified DigiDMS stores:

**Covered (clinical data matching C-CDA sections):**
- Demographics (name, DOB, sex, race, ethnicity, language, contact info)
- Problems/diagnoses
- Medications
- Allergies
- Vital signs
- Immunizations
- Lab results (Results section)
- Procedures
- Encounters
- Social history
- Care plans and goals
- Functional status
- Implantable devices (UDI)
- Health concerns
- Assessments
- Reason for referral

**Not covered / absent from the export documentation:**

- **Billing and financial data**: DigiDMS is an integrated EHR + billing system with claim scrubbing, HCFA/CMS-1500 forms, ICD-10 coding, eligibility verification, invoices, insurance forms, and payment records. None of this billing data is mentioned in the export. This is a significant gap — billing records are squarely within the HIPAA designated record set and are EHI.

- **Insurance/enrollment information**: Patient insurance details are part of the designated record set but are not represented in the C-CDA export sections.

- **Clinical notes / narrative documentation**: While "Assessment" includes "Comments", there is no explicit mention of clinical notes, progress notes, H&P, discharge summaries, or other narrative documentation. C-CDA can carry notes in a Notes section, but the data dictionary doesn't list one.

- **Documents and attachments**: DigiDMS has a document management module (OCR, version control, annotations, metadata tagging). Scanned documents, uploaded files, and their metadata are not addressed in the export.

- **Patient portal communications**: Secure messages between patients and providers are part of the patient record. Not mentioned in the export.

- **Referral requests and medication refill requests**: These are documented through the patient portal but not included in the export.

- **Prescription/e-prescribing details**: While "Medication" is listed, e-prescribing transaction details (pharmacy, fill status, prior authorization) are not mentioned.

- **Orders**: DigiDMS is certified for CPOE (a)(1), (a)(2), (a)(3). Order data (lab orders, medication orders, diagnostic imaging orders) is not mentioned in the export.

### Export Format & Standards

The export uses **C-CDA** (HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide), referenced as § 170.205(a)(4). This is a recognized, standardized format. C-CDA is appropriate for clinical summary data.

However, using C-CDA as the sole (b)(10) export format is a **red flag for completeness**. C-CDA is designed for clinical summaries and transitions of care. It was not designed to carry billing data, document management metadata, secure messages, or the full breadth of data in a typical EHR database. The sections listed in the data dictionary are essentially the standard C-CDA sections — this looks like the same clinical summary that would be generated for (b)(1) transitions of care, repackaged as the (b)(10) export.

This is a classic case of **(b)(10) / (g)(10) / (b)(1) conflation**: the vendor appears to be using their clinical summary export (which is designed for transitions of care) as their EHI export. The (b)(10) requirement is to export **all** electronic health information, not just the clinical summary subset.

A third party receiving this export could reconstruct a clinical summary of the patient, but could **not** reconstruct the full patient record — billing data, communications, documents, and orders would be missing.

### Documentation Quality

The documentation is **minimal but functional** for what it covers:

- The PDF is 7 pages including a cover page
- Screenshots show the actual export UI, which is helpful
- The data dictionary is a simple two-column table (Section / Elements) with no data types, value sets, cardinality, or constraints
- No sample export files or examples are provided
- No schema files (XSD, etc.) are provided — the standard is referenced by citation only
- No worked examples showing what the exported C-CDA XML looks like
- A developer could implement an import only by consulting the C-CDA R2.1 specification independently; the documentation alone would not be sufficient

### Structure & Completeness

The field-level documentation is **very shallow**:
- Only section names and element names are listed
- No data types specified
- No value sets or code systems documented (e.g., what codes are used for allergy severity? What coding system for diagnoses?)
- No cardinality (are allergies 0..*, 1..*, etc.?)
- No relationships between entities documented
- No versioning or change history
- The document title page says version 22.0 while the current product is version 25.0

### Overall Assessment

DigiDMS's EHI export documentation represents a **compliance checkbox approach**. The vendor has documented a C-CDA clinical summary export — which is functionality they already needed for transitions of care certification (b)(1) — and presented it as their (b)(10) EHI export. The documentation is a brief PDF with screenshots and a high-level data element listing.

The fundamental issue is scope: the export covers approximately the USCDI/clinical summary subset of data, not "all electronic health information." For a product that includes integrated billing, document management, e-prescribing, patient portal messaging, and practice management, the C-CDA export omits substantial categories of EHI including billing records, financial data, documents/attachments, orders, and patient communications. These are all part of the HIPAA designated record set and therefore EHI.

## Access Summary
- Final URL (after redirects): https://digidms.com/ehr/ehi-export (no redirects)
- Status: found
- Required browser: no (PDF downloadable via curl; page content available via direct template fetch)
- Navigation complexity: one_click (PDF link on the page template)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The AngularJS SPA failed to render in the browser (timeout). Content was accessible by directly fetching the route template HTML from `app/views/Ehr/EHIexport.html`.
- The IIS server returns the SPA shell HTML (10,510 bytes) for any URL path that doesn't match a real file, making it impossible to probe for documents by guessing filenames — every request returns HTTP 200 with HTML regardless of whether the resource exists.
- The `/documents/` directory listing is disabled (403).
