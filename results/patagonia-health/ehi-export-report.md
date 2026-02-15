# Patagonia Health — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://patagoniahealth.com/onc-certified-hit
- CHPL IDs: 11147
- Product: Patagonia Health EHR Version 6
- Certification date: 2022-12-27

## Navigation Journal

### Step 1: Initial probe
```bash
curl -sI -L "https://patagoniahealth.com/onc-certified-hit" -H 'User-Agent: Mozilla/5.0'
```
HTTP/2 200. Content-Type: text/html; charset=UTF-8. Hosted on HubSpot CMS behind Cloudflare. No redirects — the registered URL is a live HubSpot-hosted page.

### Step 2: Fetch and examine page
```bash
curl -sL "https://patagoniahealth.com/onc-certified-hit" -H 'User-Agent: Mozilla/5.0' -o /tmp/patagonia-page.html
```
50,851 bytes. Static HTML page (not a SPA). The page is the vendor's ONC certification information page containing sections on Meaningful Use, Drummond Group certification, and EHI Export. The EHI Export section appears near the bottom, under its own `<h2>` heading.

### Step 3: Identify downloadable files
Extracted all `href` links. Found the following relevant downloadable files:
- `/hubfs/Certifications/PatientHealth-Data-API-Documentation-v1.1.pdf` — Patient Health Data API Documentation v1.1
- `/hubfs/SmartOnFHIR-API-Documentation.pdf` — SmartOnFHIR API Documentation (67 pages)
- `/hubfs/FHIRBaseURL.json` — FHIR Service Base URLs (JSON Bundle)
- `/hubfs/Certifications/PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf` — Supplemental costs and limitations
- `/hubfs/Certifications/Compliance%20Certificate%20Patagonia%20Health%20EHR%206%20122924.pdf` — Compliance certificate (not downloaded — no EHI export content)

### Step 4: Browser screenshots
Navigated to the page in Chrome, scrolled to the "Electronic Health Information (EHI) Export" section, and took screenshots capturing the full EHI documentation section.

### Step 5: Downloaded all linked files
```bash
curl -sL "https://patagoniahealth.com/hubfs/Certifications/PatientHealth-Data-API-Documentation-v1.1.pdf" -o PatientHealth-Data-API-Documentation-v1.1.pdf
curl -sL "https://patagoniahealth.com/hubfs/SmartOnFHIR-API-Documentation.pdf" -o SmartOnFHIR-API-Documentation.pdf
curl -sL "https://patagoniahealth.com/hubfs/FHIRBaseURL.json" -o FHIRBaseURL.json
curl -sL "https://patagoniahealth.com/hubfs/Certifications/PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf" -o PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf
```
All files verified with `file` command — confirmed actual PDF documents and valid JSON.

## What Was Found

### EHI Export Documentation (on the web page)

The EHI export documentation lives entirely inline on the ONC certification page, under the heading "Electronic Health Information (EHI) Export." There is no separate PDF, data dictionary, or downloadable spec for the EHI export itself — the documentation is approximately 400 words of inline HTML describing the export workflow.

**Export mechanism:** The EHI export is accessed within the EHR's Reports section:
- **Single Patient:** Reports > Medical Practice Reports > Select Electronic Health Information (EHI) Export. The user selects a provider (or all), optionally sets date ranges, searches for a specific patient, selects the record, and clicks "EHI Export." The export file is generated and downloaded locally.
- **Multi-Patient:** Same path but using a "Multi Patients" button. The user sets a scheduled date/time for execution; the export runs asynchronously with status tracking (Queued → Completed).

**Clinical data format:** CCDA 2.1 Release 2, USCDI v1 (XML).

**Billing data:** Handled separately. For single-patient billing: Dashboard > Billing > Search > Claims. For multi-patient billing: Dashboard > Billing > Reports > Claim > Detail, with options to set Claim Receive Date, Claim Service Date, and Claim Submitted Date to "All." Billing data exports in CSV, XLSX, or PDF.

**Access control:** Role-based. A Practice Administrator enables "EHI Export & Schedule Data Export" permissions for specific users under Practice Administration > Staff Management > Edit Selected User. A separate billing role is needed for financial data extraction.

### Patient Health Data API Documentation v1.1 (PDF, 7 pages)

A REST API for patient data access, dated April 2018. This is a proprietary (non-FHIR) API that returns CCDA XML embedded in JSON responses. Endpoints:
- `authenticateuser` — authenticate with Basic auth, returns a TokenID
- `patientsearch` — search by MRN, DOB, first/last name (returns up to 30 patients)
- `patientCCDA` — get full CCDA for a patient by MRN, with optional date range
- `patientData` — get specific CCDA sections by name (demographics, allergies, assessments, encounters, goals, immunizations, medications, problems, procedures, results, vitals, etc.)

Base URL: `https://phapi.patagoniaemr.com:31015/PatientService.svc/`

This API predates the FHIR (g)(10) requirement and appears to be the vendor's original data access mechanism. The data returned is limited to what CCDA 2.1 can represent.

### SmartOnFHIR API Documentation (PDF, 67 pages)

This is the (g)(10) Standardized API documentation, not the (b)(10) EHI export. It documents the SMART on FHIR implementation with OAuth 2.0 authorization and FHIR R4 resources. Resources covered:
- Patient, AllergyIntolerance, CarePlan, CareTeam, Condition (Problems/Health Concerns), Device, DiagnosticReport, DocumentReference, Goal, Immunization, Medication, MedicationDispense, Observation (labs, vitals, smoking status), Organization, Procedure, Provenance, ServiceRequest, Coverage, Specimen, RelatedPerson

FHIR endpoint: `https://fhir.phemr.co:9443/fhirserver/fhir/`
Auth server: `https://oauth.phemr.co/`

Supports standalone, EHR-embedded, and backend services (bulk) launch types. This is standard US Core / USCDI scope — not a comprehensive EHI export.

### FHIR Base URLs (JSON, 4.8 KB)

A FHIR Bundle of type "collection" containing Endpoint and Organization resources for two test/sample organizations. This is the service base URL listing required by the (g)(10) API — not EHI export-specific.

### Supplemental Costs and Limitations (PDF)

Dated May 2018. Documents costs and technical limitations for MU Stage 3 capabilities (Direct Messaging, transitions of care, etc.). Not directly related to EHI export.

## Export Coverage Assessment

### Data Domain Coverage

Patagonia Health EHR is a comprehensive platform for public health departments and behavioral health agencies, storing clinical, administrative, billing, and specialty-specific data across many domains. The EHI export documentation reveals a significant gap between what the product stores and what the export covers.

**What the clinical export covers (via CCDA 2.1 / USCDI v1):**
- Demographics
- Problems/conditions
- Medications
- Allergies
- Immunizations
- Lab results
- Vital signs
- Procedures
- Encounters
- Care plans/goals
- Clinical notes (to the extent CCDA supports them)
- Social history
- Assessments, functional status, mental status

**What the billing export covers (separate CSV/XLSX workflow):**
- Claims data
- Financial/billing records

**What appears to be missing or undocumented:**
- **Behavioral health assessments** — The product stores psychiatric evaluations, DSM-5 coded diagnoses, treatment plans, progress notes, group therapy notes, and case management notes. CCDA 2.1 has limited support for behavioral health-specific structured data. There is no mention of how these specialty assessments are represented in the export.
- **Public health program data** — Communicable disease surveillance records, contact tracing data, immunization registry data, vaccine inventory tracking, community outreach records, program eligibility determinations. This is core to the product's public health market. None of this is addressed in the export documentation.
- **Custom clinical templates** — The product advertises configurable templates matching paper forms. How custom form data is exported (or whether it is) is not documented.
- **Document uploads** — The product supports document uploads to patient charts. No mention of these in the export.
- **Patient portal data** — Secure messages, patient-completed questionnaires, consent forms.
- **Scheduling and referrals** — Appointment records, referral tracking, case management records.
- **E-prescribing history** — Prescription transmission records beyond medication lists.
- **Lab orders** — The CCDA may capture results but order details and interface messages are not discussed.
- **Telehealth encounter data** — Virtual visit recordings or session metadata.

The fundamental issue is that the clinical EHI export is **CCDA 2.1 constrained to USCDI v1**, which is essentially the same data the (g)(10) FHIR API already provides. This is a textbook case of the (b)(10) vs (g)(10) confusion: the vendor is using their clinical summary document (CCDA) as the EHI export, which only covers the standard clinical data subset. The billing data export is handled separately in a different workflow, which at least acknowledges that EHI is broader than clinical summaries — but the overall approach still leaves many data domains undocumented or unexported.

### Export Format & Standards

**Clinical data:** CCDA 2.1 Release 2, USCDI v1 (XML). This is a well-understood standard, but it constrains the export to clinical summary data. A CCDA cannot represent vaccine inventory, disease surveillance records, program eligibility data, custom form data, or the many other data types this public health / behavioral health EHR stores.

**Billing data:** CSV, XLSX, or PDF. No schema, field definitions, or data dictionary is provided for the billing export. The documentation merely says claims data "can then be downloaded" in these formats.

**Appropriateness:** For a general ambulatory EHR, CCDA might cover most clinical data. For a public health and behavioral health EHR with extensive specialty data (communicable disease tracking, behavioral health assessments, DSM-5 coding, program compliance), CCDA is a poor fit. A database dump or structured CSV export of all tables would be far more appropriate for capturing the breadth of data this product manages.

A third party receiving this export would get a standard patient clinical summary and raw billing CSV files, but would not be able to reconstruct the full patient record as it exists in the system.

### Documentation Quality

The EHI export documentation is minimal — roughly 400 words of inline text on a certification page. There is:
- **No data dictionary** — no description of what fields/tables are included in the export
- **No schema or format specification** for the billing CSV/XLSX exports
- **No worked examples** or sample export files
- **No field-level documentation** — nothing about data types, value sets, cardinality, or constraints beyond "CCDA 2.1 Release 2 USCDI v1"
- **No description of what CCDA sections are included** in the EHI export specifically (the Patient Health Data API doc lists sections, but this is a different mechanism)

A developer trying to import this data would need to: (1) understand CCDA 2.1 for clinical data (feasible but the vendor provides no custom profile info), and (2) reverse-engineer the billing CSV/XLSX format with no documentation at all.

The documentation reads as procedural instructions for EHR users ("click here, then here") rather than technical documentation of the export format and content. It looks like a compliance checkbox rather than a genuine attempt to document data portability.

### Structure & Completeness

- **Granularity:** The documentation provides zero field-level detail. No table names, no column names, no data types, no value set documentation.
- **Relationships:** No description of how clinical and billing data relate, or how to correlate records across the two separate export workflows.
- **Versioning:** No version or change history for the export documentation itself. The Patient Health Data API doc is labeled v1.1 (April 2018), but the EHI export section has no date or version.
- **Coded fields:** No documentation of value sets, code systems, or coding conventions used in the billing exports.

## Access Summary
- Final URL (after redirects): https://patagoniahealth.com/onc-certified-hit
- Status: found
- Required browser: no (all content is in static HTML; browser used for screenshots only)
- Navigation complexity: one_click (EHI section is inline on the page, scroll to find it)
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends

None significant. The page loaded cleanly via curl and in the browser. All linked files downloaded without authentication or special headers. The only complication is that the EHI export documentation is entirely inline on the page rather than in a downloadable document, making it easy to miss among the other certification content. There are no images embedded in the EHI section (no screenshots of the export interface), though the text describes the UI workflow steps.
