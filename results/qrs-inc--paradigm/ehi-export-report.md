# QRS, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.qrshs.info
- CHPL IDs: 11142
- Product: PARADIGM® Version 22
- Certification date: 2022-12-27

## Navigation Journal

### Step 1: Initial probe
```bash
curl -sI -L "https://www.qrshs.info" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html, 29128 bytes. Static HTML page served by nginx/1.18.0 (Ubuntu). No redirects.

### Step 2: Examine page content
The page at www.qrshs.info is titled "QRS Disclosures" and is a static compliance/disclosure hub listing several PDF documents. No JavaScript framework, no SPA, no accordion — all links are visible in the HTML source.

Documents listed on the page:
1. 2025 Real World Testing Plan Results (rwtp/RWT Results_25.pdf) — Feb 2026
2. 2024 Real World Testing Plan Results (rwtp/RWT Results_24.pdf) — Jan 2025
3. Real World Testing Plan 2025 (rwtp/RWT Plan_25_P22.pdf) — Oct 2024
4. 2023 Real World Testing Plan Results (rwtp/RWT Results_23.pdf) — Jan 2024
5. Real World Testing Plan 2024 (rwtp/RWT Plan_24_P22.pdf) — Oct 2023
6. **PARADIGM EHI Export Documentation** (rwtp/PARADIGM EHI Export Documentation.pdf) — Sept 2023
7. Real World Testing Results 2022 (rwtp/RWT Results_22.pdf) — Jan 2023
8. Privacy and Security Transparency Attestations (rwtp/Privacy and Security Transparency Attestations.pdf) — Dec 2022
9. **PARADIGM Patient API Documentation** (rwtp/PARADIGM Patient API Documentation.pdf) — Dec 2022
10. **PARADIGM FHIR API Documentation** (rwtp/PARADIGM FHIR API Documentation.pdf) — Dec 2022
11. EHR Real World Testing Plans for P17 and P22 (rwtp/RWT Plan_23_P17_Links.pdf, rwtp/RWT Plan_23_P22_Links.pdf) — Oct 2022
12. EHR Real World Testing Plan P17 (rwtp/RWT_Plan.pdf) — Nov 2021

Items 6, 9, and 10 (bolded) are directly relevant to EHI export documentation and were downloaded.

### Step 3: Download relevant PDFs
```bash
curl -sL "https://www.qrshs.info/rwtp/PARADIGM%20EHI%20Export%20Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o PARADIGM_EHI_Export_Documentation.pdf
# Verified: PDF document, version 1.5, 6 pages, 163457 bytes

curl -sL "https://www.qrshs.info/rwtp/PARADIGM%20FHIR%20API%20Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o PARADIGM_FHIR_API_Documentation.pdf
# Verified: PDF document, version 1.5, 27 pages, 279448 bytes

curl -sL "https://www.qrshs.info/rwtp/PARADIGM%20Patient%20API%20Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o PARADIGM_Patient_API_Documentation.pdf
# Verified: PDF document, version 1.5, 6 pages, 159921 bytes
```

### Step 4: Examine PDF contents
All three PDFs were extracted via `pdftotext` and visually inspected via `pdftoppm`. No embedded attachments or hidden URLs pointing to additional documentation were found. The EHI Export Documentation PDF references only the Patient Search and Patient C-CDA API endpoints (at api.qrshs.com). No links to external data dictionaries, schema files, or additional documentation.

### Step 5: Check for additional content
```bash
curl -sL "https://www.qrshs.info/rwtp/" -H 'User-Agent: Mozilla/5.0'
# Result: 403 Forbidden — directory listing not available
```
No additional pages or documents were discovered beyond those linked from the main page.

## What Was Found

### PARADIGM EHI Export Documentation (6 pages)
This is the core (b)(10) EHI export document, version 1.0, dated September 26, 2023. It describes the "PARADIGM® FHIR Data Portability module," which provides authorized EHR users the ability to export Electronic Health Information.

**Key findings from the document:**

**Export Format**: Data is exported as a ZIP file containing:
- A standard C-CDA XML document per patient (e.g., `10000.xml`)
- Additional information in JSON format (e.g., `10000_invoice history.json`)
- Files previously imported into the EHR in their original format (PDF, PNG, etc.), placed in a subdirectory (e.g., `10000_addt_files/`)

**Access Method**: The Data Portability module is accessed through "EHR System Reports" by authorized users. There is a checkbox: "include all Electronic Healthcare Information (EHI) for each patient in the set."

**API Endpoints**: The document describes two REST API endpoints:
1. `GET https://api.qrshs.com/v1/patient/search` — Patient lookup by name, birthdate, or SSN (Basic auth)
2. `GET https://api.qrshs.com/v1/patient/ccda` — Retrieve C-CDA for a patient with optional date filtering (Basic auth)

**Terms and Conditions**: Pages 1-4 of the 6-page document are entirely terms and conditions / legal boilerplate. Only pages 5-6 contain actual technical documentation about the export.

**What's notably absent**: No data dictionary. No field-level documentation. No list of what data elements are included in the C-CDA or JSON files. No specification of the JSON format. No sample data. No schema. The "invoice history.json" example is mentioned in passing but never defined.

### PARADIGM FHIR API Documentation (27 pages)
This is the (g)(10) FHIR API documentation, separate from the EHI export. It documents a FHIR R4 API at `https://api.qrshs.com/fhir/` using OAuth 2.0 with PKCE. The API supports the following US Core resource types (read-only):

- Patient (demographics)
- AllergyIntolerance
- CarePlan
- CareTeam
- Condition (problem list)
- Device (implantable devices)
- DiagnosticReport (lab results)
- DocumentReference (clinical notes as C-CDA)
- Goal
- Immunization
- MedicationRequest
- Observation (vitals, labs, smoking status)
- Procedure
- Encounter
- Provenance
- Location, Organization, Practitioner, PractitionerRole (supporting resources)

Each resource type includes request parameters, response parameters, and example JSON responses. This is a standard US Core / USCDI FHIR API — it covers the (g)(10) certification requirement, not the broader (b)(10) EHI export.

### PARADIGM Patient API Documentation (6 pages)
This document describes a non-FHIR REST API for patient search and C-CDA retrieval, using Basic authentication at `https://api.qrshs.com/v1/`. It has the same two endpoints as described in the EHI export document (patient search and patient C-CDA). Pages 1-4 are the same terms and conditions boilerplate; pages 5-6 are the actual API documentation.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation claims to export data in C-CDA format plus supplemental JSON files. Based on the product research, PARADIGM stores a wide range of clinical and billing data. Here is the assessment:

**Partially covered (via C-CDA):**
- Demographics — standard C-CDA section
- Problem lists / conditions — standard C-CDA section
- Medications / prescriptions — standard C-CDA section
- Allergies — standard C-CDA section
- Immunizations — standard C-CDA section
- Procedures — standard C-CDA section
- Lab results — standard C-CDA section
- Vital signs — standard C-CDA section
- Clinical notes — via DocumentReference in the FHIR API; likely as C-CDA narrative
- Encounters — standard C-CDA section

**Mentioned but unspecified (via JSON supplements):**
- Invoice/billing history — the doc mentions `10000_invoice history.json` as an example, suggesting billing data is exported as JSON. However, the JSON format is completely undocumented. No schema, no field definitions, no sample structure.

**Mentioned but unspecified (via attached files):**
- Imported documents (PDFs, images) — the doc mentions an `_addt_files` directory for files imported into the EHR. This could cover scanned documents, external records, voice recordings (.wav files), and faxes.

**Likely missing or undocumented:**
- Family health history (certified (a)(12)) — no mention in export docs
- Implantable device list (certified (a)(14)) — no mention in export-specific docs
- E-prescribing details beyond basic medication data
- Scheduling/appointment data
- Insurance/eligibility/enrollment data
- Claims management data (beyond the vague "invoice history" mention)
- ERA/electronic remittance data
- Patient portal messages
- Referral data
- Care plans and goals (available via FHIR API but not mentioned in EHI export)
- Care team information (available via FHIR API but not mentioned in EHI export)
- Specialty-specific clinical data (the product supports 50+ specialties)

**Critical gap — the (b)(10) vs (g)(10) confusion is partially at play here.** The EHI export document is titled "FHIR Data Portability module" and its API endpoints use the same base URL (api.qrshs.com) as the FHIR API. However, QRS appears to have made some effort beyond pure (g)(10): the export produces a ZIP with C-CDA + JSON + attached files, and specifically mentions an "invoice history" JSON file and an EHI checkbox. This suggests awareness that billing data needs to be included beyond what C-CDA covers. The problem is that none of the supplemental formats are documented.

### Export Format & Standards

- **Primary format**: C-CDA XML (standard, well-defined)
- **Supplemental format**: JSON files for "additional information" — completely undocumented
- **Attached files**: Original format (PDF, PNG, etc.) for imported documents
- **Packaging**: ZIP archive per patient or patient set
- **API authentication**: Basic auth for the v1 Patient API; OAuth 2.0 with PKCE for the FHIR API

The C-CDA format is appropriate for clinical data that maps to standard CDA sections. The JSON supplement is potentially a good approach for data that doesn't fit C-CDA (billing, custom data), but without any documentation of its structure, a third party cannot interpret or import this data reliably.

**Could a third party reconstruct the patient record?** Partially. The C-CDA is a recognized standard, so the clinical data it contains would be interpretable. But the JSON files (which likely contain billing/financial data and possibly other non-clinical data) are opaque without documentation. The attached files (scanned documents, images) would be usable but without metadata about what each file represents.

### Documentation Quality

The documentation quality is **poor**. Key issues:

1. **Overwhelming legal boilerplate**: The 6-page EHI export document dedicates 4 pages (67%) to terms and conditions. Only 2 pages describe the actual export.
2. **No data dictionary**: There is no listing of what fields, tables, or data elements are included in the export. No field names, data types, or value sets are specified.
3. **Undocumented JSON format**: The supplemental JSON files are mentioned as an example filename ("invoice history.json") but their structure is never defined. A developer receiving this export would have to reverse-engineer the JSON.
4. **No sample data**: No example export files, no sample C-CDA, no sample JSON.
5. **No schema files**: No XSD, JSON Schema, or any machine-readable specification.
6. **No screenshots**: No visual guide to the export interface or the checkbox mentioned.
7. **Minimal instructions**: "Access through EHR System Reports, click the checkbox" is the entire usage guide.
8. **Version 1.0, never updated**: The document is dated September 2023 and appears to have never been revised.

The FHIR API documentation (27 pages) is significantly more detailed, with request/response parameters and example JSON for each resource type. But that document serves the (g)(10) requirement, not the (b)(10) EHI export.

### Structure & Completeness

- **Granularity**: The EHI export documentation provides no field-level documentation whatsoever. It describes the export at a high level (ZIP containing C-CDA + JSON + files) but never specifies what data elements are in any of those files.
- **Coded fields**: Not documented.
- **Relationships between entities**: Not documented.
- **Value sets**: Not documented.
- **Versioning**: Version 1.0 with no change history.

### Overall Assessment

QRS has made a minimal effort toward (b)(10) compliance. The positive signs are:
1. They have a dedicated EHI export module (the "FHIR Data Portability module")
2. They produce a ZIP with C-CDA + supplemental JSON + attached files — suggesting they understand that EHI goes beyond clinical summaries
3. The "include all EHI" checkbox suggests awareness of the full-record requirement
4. The mention of "invoice history" JSON files shows billing data is included

However, the execution is severely lacking:
1. The documentation is 67% legal boilerplate with only 2 pages of technical content
2. The supplemental JSON format (which likely carries the most important non-clinical data) is completely undocumented
3. No data dictionary, no schema, no sample data
4. No way for a third party to understand or import the non-C-CDA portions of the export
5. Many data domains that PARADIGM stores (specialty-specific data, insurance data, claims, referrals, care plans) are neither confirmed present nor documented in the export
6. The product stores data for 50+ specialties but there's no indication of how specialty-specific clinical data is exported

This appears to be a compliance checkbox exercise rather than a genuine effort to make patient data portable. A practice receiving an EHI export request would produce a ZIP file, but the recipient would struggle to interpret much of the non-C-CDA content.

## Access Summary
- Final URL (after redirects): https://www.qrshs.info (no redirects)
- Status: found
- Required browser: no
- Navigation complexity: direct_link (one click from main page to PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The rwtp/ directory listing returns 403 Forbidden, so there's no way to discover unlisted files
- The vendor's main website (qrshs.com) has an expired SSL certificate (noted in product research), but the disclosure site (qrshs.info) works fine
- No additional documentation was found beyond the three PDFs and the main page
