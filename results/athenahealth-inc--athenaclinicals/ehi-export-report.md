# athenahealth, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://docs.athenahealth.com/athenaone-dataexports/
- CHPL IDs: 11714 (athenaClinicals), 11613 (athenaClinicals for Hospitals and Health Systems)
- Developer: athenahealth, Inc.
- Certification dates: 2025-03-21 (hospital), 2025-10-28 (ambulatory)

## Navigation Journal

### Initial probe
```bash
curl -sI -L "https://docs.athenahealth.com/athenaone-dataexports/" -H 'User-Agent: Mozilla/5.0'
# → HTTP 200, Content-Type: text/html; charset=utf-8, 1849 bytes
```

The registered URL returns a thin HTML shell (1849 bytes) — a JavaScript SPA using athenahealth's internal "nimbus" CDN bundle loader (`document-portal-ui` v1.3.9). No meaningful content is available without JavaScript execution.

### Browser rendering
Navigated in Chrome. The SPA renders a dedicated "Data Exports" documentation portal with:
- Top nav: Documentation | Support
- Left sidebar: Overview, Ambulatory EHI Exports (Clinical, Collector), Inpatient EHI Exports (Clinical, Collector), Updates (Release Notes)

### Discovering the content API
Inspecting network requests revealed the SPA fetches content from a Contentful-backed API:
- `GET /v1/api/portalNavigation/exports-getting-started` → site navigation structure
- `GET /v1/api/entries/microsite?entryId=athenaone-dataexports&include=4` → microsite config
- `GET /v1/api/entries/freeformPage?urlAlias=<path>&include=5` → page content (rich text JSON)

All API endpoints are publicly accessible without authentication. This allowed downloading the full structured content directly:
```bash
curl -sL "https://docs.athenahealth.com/v1/api/entries/freeformPage?urlAlias=%2Fambulatory%2Fclinical-ehi-export&include=5" -o api-ambulatory-clinical.json
```

### PDF downloads
Each of the four export type pages (ambulatory clinical, ambulatory collector, inpatient clinical, inpatient collector) has a downloadable PDF data dictionary. The PDF URLs are embedded in the Contentful entry data as `downloadableFile` entries pointing to `assets.ctfassets.net`:
```bash
curl -sL --compressed "https://assets.ctfassets.net/uazigsvtldjw/6M0ojDEj3TVXbTHn7B9qRv/832b5a8bd00812cf7e610c96d29191de/2_Ambulatory_Clinical_EHI_Exports__1_.pdf" -o ambulatory-clinical-ehi-export.pdf
```

All 4 PDFs downloaded successfully. All created Sep 22, 2023.

### Pages visited
1. **Welcome/Overview**: `https://docs.athenahealth.com/athenaone-dataexports/` → introduces EHI export, describes use cases (bulk, single/multi-patient), mentions both ambulatory and inpatient settings
2. **Ambulatory Clinical EHI Export**: `.../ambulatory/clinical-ehi-export` → 64 datasets, NDJSON format, PDF download
3. **Ambulatory Collector EHI Export**: `.../ambulatory/collector-ehi-export` → 15 datasets, NDJSON format, PDF download
4. **Inpatient Clinical EHI Export**: `.../inpatient/clinical-ehi-export` → 38 datasets, HTML format, PDF download (37 pages)
5. **Inpatient Collector EHI Export**: `.../inpatient/collector-ehi-export` → 16 datasets, NDJSON format, PDF download
6. **Release Notes**: `.../guides/release-notes` → empty page, still says "set to be released within 2023"
7. **Support**: `.../support` → contact info, one FAQ, links to athenahealth Client and Partner support portals

## What Was Found

### Export Architecture

athenahealth's EHI export is structured into **four distinct export modules**, organized by care setting (ambulatory vs. inpatient) and data domain (clinical vs. collector/billing):

| Module | Setting | Data Domain | Format | Datasets |
|--------|---------|-------------|--------|----------|
| Ambulatory Clinical | Outpatient | Clinical/EHR data | NDJSON | 64 |
| Ambulatory Collector | Outpatient | Demographics, billing, scheduling | NDJSON | 15 |
| Inpatient Clinical | Hospital | Clinical/EHR data | HTML | 38 |
| Inpatient Collector | Hospital | Demographics, billing, scheduling | NDJSON | 16 |

**Total: 133 documented datasets** (with some overlap between ambulatory and inpatient collector modules).

### Export Use Cases
The documentation describes three use cases:
1. **Single patient export** — for individual patient requests or referrals
2. **Multi-patient export** — for selected patients
3. **Bulk/all-patient export** — for practice detachment or termination from athenahealth

### Export Format

**Ambulatory Clinical**: Newline Delimited JSON (NDJSON). Each dataset produces a `.json` file. Supporting files (encounter summaries, imaging results, scanned documents) are included as XML, JPEG, PNG, TIFF, or PDF. Each JSON line includes patient identifiers (FIRSTNAME, LASTNAME, DOB, SSN, ATHENA PATIENT ID, ENTERPRISE ID, MOBILE PHONE, HOME PHONE, ADDRESS) for matching.

**Ambulatory Collector**: Same NDJSON format with supporting image/PDF files for insurance cards, claim attachments, etc.

**Inpatient Clinical**: HTML format — human-readable HTML files viewable in a browser. The documentation notes: "If you are a Customer who has an ambulatory department or has ambulatory information, in addition to the HTMLs, we also provide a structured Clinical EHI Export comparable to Ambulatory Clinical EHI Export."

**Inpatient Collector**: NDJSON format (same as ambulatory collector).

### Data Dictionary / Field Specifications

The ambulatory clinical datasets reference **athenahealth's public API documentation** for field-level specifications. Each dataset links to either:
- A proprietary REST API endpoint doc at `docs.athenahealth.com/api/api-ref/...` (e.g., allergies → `/api/api-ref/allergy#Get-patient's-allergies`)
- A FHIR R4 resource doc at `docs.athenahealth.com/api/fhir-r4/...` (e.g., encounters → `/api/fhir-r4/encounter`)

Two datasets have **inline field specifications** on the export documentation page itself:
- **Care Plan Events**: 2 input params, 11 output fields (careevents, chartid, eventid, lastmodified, eventtime, createdby, type, summary, duration, lastmodifiedby, created)
- **Eye Care Measurements**: 5 sections per encounter (Vision correction, Eye dilation, Intraocular pressure, Visual acuity elements)

The **inpatient clinical PDF** (37 pages) is the most detailed document. It provides HTML template-level field specifications for all 38 hospital datasets, documenting each field with its HTML structure, data type, and description. This includes hospital-specific sections not found in the ambulatory export.

### Ambulatory Clinical Datasets (64)

Admin Documents, Allergies, Assessment and Plan, Cancer Cases, Care Plan, Care Plan Events, Care Team Members, Chief Complaint, Clinical Documents (includes Mental Health Consult), Corrective Lens, Default Clinical Providers (Lab, Imaging, Pharmacy), Devices/Medical Equipment, DME Orders, Encounter Documents, Encounters, Encounter Phone Call Checklists, Encounter Summary, Eye Care Specific Measurements, Family History, Goals, GYN History, Health Concerns (Conditions & Problems), History of Present Illness, Imaging Results, Immunizations, Interpretations, Lab Results, Letters, Letter Action Notes, Medical Record Documents, Medications (includes Procedure Medications, Denied Medications, Prescribed Vaccines), OB Episodes, OB Episode Summary, OB Episode Summary Documents, OB History, Observations (includes Vital Measurements), Office Notes, Orders (Labs, Imaging, Consult & Procedures), Other CCDAs, Past Medical History, Patient Cases, Perinatal History, Physical Exam, Physician Authorization, Prescription Documents, Procedures, Procedures Documentation, Procedure Roles, Procedure Times, Procedure Timeout Checklist, Procedure Vitals, Pre-sedation Assessment, PT Episode, Review of Systems, Screening, Social History, Surgery Action Notes, Surgical History, Surgical Orders, Surgical Results, Topic of Discussion, Vitals.

Of these, 16 datasets include supporting document/attachment files.

### Ambulatory Collector Datasets (15)

Appointments, Appointment Ticklers & Reminders, Claim Attachments, Claim Details, Claim Notes, Claim Transactions, Demographics, Patient Billing Statements and Summaries, Payment History (includes Patient Refunds), Patient Insurance, Patient Outstanding Balance & Patient Unapplied, Payment Plans, Pre-payment Plans, Referral/Auth, Return to Office.

### Inpatient Clinical Datasets (38)

Patient Demographics, Admin Documents, Admission H&P, Admission Order, Clinical Documents, Consult Notes, Discharge Planning Audit, Discharge Planning Notes, Discharge Summary, ED Course, ED Nursing Initial Assessment Notes, ED Provider Assessment, ED Provider Notes, ED Triage Notes, Flowsheet ADL, Flowsheet ADLs, Flowsheet Airways, Flowsheet Drains, Flowsheet Head to Toe, Flowsheet Intake & Output, Flowsheet Lines, Flowsheet Measurements, Flowsheet Vitals, Hospital Notes, Imaging Results, Lab Results, Medication Administration Record, Nursing Admission Notes, Nursing Care Plan, Nursing Notes, Nursing Tasks, Orders, Paper Forms, Patient Discharge Instructions, Respiratory Tasks, Surgical Pre-Op Notes, Therapy Tasks, Transfer Orders.

### Inpatient Collector Datasets (16)

Same as ambulatory collector (15 datasets) plus **Visits and Charge Details** (hospital-specific).

## Export Coverage Assessment

### Data Domain Coverage

**Comprehensively covered:**
- Demographics, contacts, insurance/enrollment
- Clinical documentation (encounters, notes, H&P, discharge summaries, consult notes)
- Problem lists / conditions
- Medications (active, prescribed, denied, procedure-related, vaccines)
- Allergies
- Lab results and imaging results
- Vital signs / observations
- Immunizations
- Procedures (including surgical, with roles, times, timeout checklists, pre-sedation assessments)
- Care plans and goals
- Family history, social history, medical history, surgical history
- OB/GYN-specific data (OB episodes, GYN history, perinatal history)
- Eye care measurements (specialty-specific)
- Physical therapy episodes
- Cancer cases
- Screening questionnaires
- Devices / medical equipment
- Clinical documents, medical records, admin documents, letters, office notes
- Encounter summaries, CCDAs
- Prescription documents, physician authorizations, DME orders
- Hospital-specific: ED documentation (triage, assessment, course, provider notes), nursing documentation (admission, notes, tasks, care plan), flowsheets (vitals, ADLs, I&O, airways, drains, lines, measurements), discharge planning, medication administration records, respiratory tasks, therapy tasks, transfer orders, surgical pre-op notes

**Billing/financial data (well-covered):**
- Claims (details, transactions, notes, attachments)
- Payments (history, refunds)
- Patient billing statements and summaries
- Patient insurance
- Outstanding balance / unapplied payments
- Payment plans and pre-payment plans
- Referral/authorization
- Appointments and ticklers/reminders
- Hospital visits and charge details (inpatient)
- Demographics

**Potentially missing or ambiguous:**
- **Patient portal messages / secure messaging**: Not listed as a standalone dataset. The product research notes that athenaCommunicator provides secure HIPAA-compliant messaging between patients and providers. If these messages are part of the patient's designated record set (they could affect care decisions), their absence from the export would be a gap.
- **Telehealth visit records/transcripts**: athenaTelehealth provides live closed captions and transcripts — not clearly covered.
- **Digital intake form submissions**: athenaCommunicator captures pre-visit intake forms. Not clearly mapped to a specific export dataset, though some data may flow into demographics or encounter records.
- **Population health outreach records**: Campaign/outreach records from athenaCommunicator — likely operational, not part of the designated record set.
- **Clinical decision support alerts**: Epocrates-driven alerts — likely operational/system data, not EHI.

Overall, the export covers a remarkably broad set of clinical and billing data domains. The 64 ambulatory clinical + 15 collector + 38 inpatient clinical + 16 inpatient collector datasets represent one of the more comprehensive EHI export dataset lists among EHR vendors. The separation between clinical and billing data (Clinicals vs. Collector modules) ensures both domains are addressed.

### Export Format & Standards

The export uses a **hybrid approach**:

- **Ambulatory data**: Structured NDJSON files. Field specifications are documented via references to athenahealth's public API documentation — both proprietary REST API docs and FHIR R4 resource docs. This is a pragmatic format: machine-readable, well-documented through the API reference, and suitable for programmatic import.

- **Inpatient data**: HTML files for clinical data (human-readable but harder to programmatically parse), NDJSON for billing/collector data. The HTML format is less ideal for data portability — a third party would need to parse HTML to reconstruct structured records.

- **Supporting files**: Images, PDFs, XMLs are included as separate files with reference links in the JSON data.

The use of FHIR R4 resources for some ambulatory datasets (encounters, conditions, medications, immunizations, observations, procedures, care plan, care team, goals, devices) shows alignment with standards, but the majority of datasets use athenahealth's proprietary API format rather than FHIR.

This is **not** a (g)(10)-style FHIR Bulk Data export repackaged as (b)(10). The export goes well beyond USCDI/US Core data, including specialty-specific clinical data (eye care, OB/GYN, cancer, physical therapy), detailed procedure documentation, extensive billing data, and hospital-specific sections. This is genuine (b)(10) work.

### Documentation Quality

**Strengths:**
- Dedicated documentation portal with clear structure and navigation
- Four separate, well-organized sections for each export module
- Each dataset is named and linked to field-level API documentation
- Downloadable PDF data dictionaries available for all four modules
- Clear file format descriptions (NDJSON, HTML)
- Detailed folder structure and naming conventions for all three export use cases (single, multi, bulk)
- Instructions for reconciling datasets using patient identifiers and reference elements
- The inpatient clinical PDF (37 pages) provides unusually detailed HTML template-level field specs

**Weaknesses:**
- Field-level documentation for ambulatory datasets is **by reference** — you must follow links to the API documentation (docs.athenahealth.com/api/) to see actual field definitions. The API docs are a separate system and could change independently of the export documentation.
- The Release Notes page has been empty since 2023, suggesting the documentation may not be actively maintained.
- No sample export files or worked examples are provided.
- No machine-readable schema files (JSON Schema, OpenAPI) for the export format itself.
- The PDFs are dated September 2023 and may not reflect recent changes (certification was in 2025).
- The inpatient clinical format (HTML) is documented at the template level but lacks formal schema documentation.
- No versioning or change history for the export format.

### Structure & Completeness

**Granularity:**
- Dataset-level: Very good — 133 named datasets across four modules
- Field-level: Varies. Ambulatory datasets link to API docs with full field definitions. Inpatient clinical datasets have inline HTML template specs. Two datasets (Care Plan Events, Eye Care Measurements) have inline field tables in the web documentation.
- Data types: Documented in the API reference (by reference) and in the inpatient PDF (inline)
- Value sets/codes: Some documented in the inpatient PDF (e.g., Marital Status values). Otherwise referenced through API docs.
- Relationships: Documented via reconciliation instructions — JSON files include patient identifiers and cross-referencing fields (encounter IDs, document IDs, etc.)

**What a developer would need additionally:**
- Machine-readable schema for the NDJSON files (JSON Schema or similar)
- Sample export files to validate parsing
- Explicit versioning and change log for the export format
- More detail on how FHIR R4 resources in the export differ from the standard (g)(10) FHIR API output — are there additional custom fields?

## Access Summary
- Final URL (after redirects): https://docs.athenahealth.com/athenaone-dataexports/
- Status: found
- Required browser: Yes (JavaScript SPA), but API endpoints are accessible via curl
- Navigation complexity: multi_page (6 content pages across 2 sections)
- Anti-bot issues: none — public API, no auth required

## Obstacles & Dead Ends
- The HTML page returns only a 1849-byte JS loader shell. Content requires either browser rendering or discovery of the underlying Contentful API endpoints.
- The `Content-Encoding: gzip` header on PDF downloads from `assets.ctfassets.net` required `--compressed` flag for curl — without it, the downloaded file was gzip-compressed rather than PDF.
- The Release Notes page has been empty/placeholder since 2023.
