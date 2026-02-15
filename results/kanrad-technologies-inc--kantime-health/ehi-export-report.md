# Kanrad Technologies Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://kantime.com/wp-content/uploads/2023/11/EHI_Tool_Documentation.pdf
- CHPL IDs: 11219
- Product: KanTime Health v1.0
- Certification date: 2023-01-18

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://kantime.com/wp-content/uploads/2023/11/EHI_Tool_Documentation.pdf" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: application/pdf, Content-Length: 42570 bytes. Direct PDF download — no redirects.

### Step 2: Download and verify the PDF
```bash
curl -sL "https://kantime.com/wp-content/uploads/2023/11/EHI_Tool_Documentation.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI_Tool_Documentation.pdf
file downloads/EHI_Tool_Documentation.pdf  # PDF document, version 1.4, 1 page(s)
pdfinfo downloads/EHI_Tool_Documentation.pdf  # 1 page, 42570 bytes, produced by "Skia/PDF m121 Google Docs Renderer"
```
Confirmed: valid 1-page PDF titled "EHI Tool Documentation."

### Step 3: Extract and read the PDF text
The entire document reads:
> Electronic Health Information (EHI) Export
> Kantime Health supports the export of electronic health information (EHI) based on user roles for both clinical and billing data.
>
> **Single or Multi-Patient EHI Export**
> Users who have access to EHI export authorization will be able to export clinical data using the CCDA 2.1 Release 2 standard.
> The billing user role will facilitate the process for users to extract patient claims and payments in CSV format export.
>
> **Exported File Formats**
> - Clinical data is exported as CCDA 2.1 Release 2 USCDI v1.
> - Billing data is exported as CSV, XLSX or PDF.

No URLs, no embedded files, no attachments in the PDF.

### Step 4: Check the ONC Regulatory Compliance page for additional docs
```bash
curl -sL "https://kantime.com/care-type/onc-regulatory-compliance/" -H 'User-Agent: Mozilla/5.0' -o /tmp/kantime-onc.html
```
Found an "EHI Export Documentation" section that says: "Documentation on the 170.315 (b)(10) EHI Export output format for each Kanrad Technologies ONC Certified solutions is provided below." with a link to the same PDF. The page also links to:
- `KanTime_Patient_API.pdf` — REST API documentation for accessing patient CCDA data
- `SmartOnFHIRAPIDoc.pdf` — SMART on FHIR API documentation (66 pages, for (g)(10))
- `fhir-base-urls-1.json` — FHIR R4 endpoint Bundle
- `KanTime_Health_Patient_API_TOU.pdf` — Terms of Use (not downloaded, not EHI export content)

### Step 5: Download the Patient API PDF
```bash
curl -sL "https://kantime.com/wp-content/uploads/2024/03/KanTime_Patient_API.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/KanTime_Patient_API.pdf
```
14-page PDF (255KB). This describes a REST API for exporting clinical data as CCDA XML — the same mechanism referenced in the EHI export documentation. Endpoints include:
- `POST .../v1/Patient/authenticateuser` — authenticate with KanTime credentials
- `POST .../v1/Patient/patientsearch` — search patients by MRN, DOB, name
- `POST .../v1/Patient/patientccda` — retrieve full CCDA for a patient (with optional date range)
- `POST .../v1/Patient/patientdata/{sectionname}` — retrieve specific clinical sections

Available CCDA sections: demographics, careteam, allergies, assessments, encounters, functionalstatus, goals, healthconcerns, immunizations, medicalequipment, medications, mentalstatus, planoftreatment, problem, procedures, reasonforreferral, results, socialhistory, vitalsigns, consultationnote, progressnote, historyandphysicalnote.

### Step 6: Download FHIR-related files for context
```bash
curl -sL "https://kantime.com/wp-content/uploads/2026/02/SmartOnFHIRAPIDoc.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/SmartOnFHIRAPIDoc.pdf
curl -sL "https://kantime.com/wp-content/uploads/2026/02/fhir-base-urls-1.json" -H 'User-Agent: Mozilla/5.0' -o downloads/fhir-base-urls-1.json
```
The SMART on FHIR doc (66 pages) covers the (g)(10) FHIR API — standard US Core resources (Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Goal, Immunization, Medication, Procedure, Observation, etc.). It does NOT mention (b)(10) or EHI export. The FHIR base URLs JSON is a FHIR Bundle with 2 organization endpoints.

### Step 7: Search for additional documentation
- Checked `https://kantime.com/certifications-accreditations-and-compliance/` — no additional EHI-specific links beyond what's on the ONC page.
- Checked sitemap (`sitemap_index.xml`) — no EHI-related pages.
- `https://kantime.com/interoperability/` and `https://kantime.com/ehi/` — both return 404.
- Web search for "kantime.com EHI export documentation data dictionary" — no additional KanTime EHI docs found.
- Wayback Machine check — no archived alternative versions.

## What Was Found

The entire EHI export documentation consists of:

1. **A 1-page PDF** (`EHI_Tool_Documentation.pdf`, 42KB) that describes the export at the highest possible level: clinical data exports as CCDA 2.1 Release 2 (USCDI v1), and billing data exports as CSV, XLSX, or PDF. That is the complete content — no data dictionary, no field definitions, no schema, no examples, no instructions for how to actually perform the export.

2. **A 14-page Patient API PDF** (`KanTime_Patient_API.pdf`, 255KB) that documents a REST API for retrieving clinical data as CCDA XML. This is the technical mechanism for the clinical side of the EHI export. It provides authentication details, search parameters, and sample CCDA output. The API supports retrieving the full CCDA or specific clinical sections, with optional date range filtering. The sample response shows a standard C-CDA "Summary of Care" document. This API requires authentication (Basic Auth to get a JWT, then Bearer token for API calls).

3. **A 66-page SMART on FHIR API doc** (`SmartOnFHIRAPIDoc.pdf`, 686KB) and a **FHIR base URLs JSON** (`fhir-base-urls-1.json`, 4KB) — these are (g)(10) FHIR API documentation, NOT (b)(10) EHI export docs. They cover standard US Core FHIR resources and are included for completeness but are a separate certification requirement.

**What is completely absent:**
- Any documentation of the billing data export (CSV/XLSX/PDF): what fields are included, what the columns mean, what data is covered
- A data dictionary of any kind — no table definitions, no field descriptions, no schema
- Any documentation of non-USCDI clinical data: OASIS assessments, HIS data, care plans (485s), visit notes, EVV data, HR/payroll data, intake/referral data
- Sample export files
- Instructions for how to perform the export within the KanTime UI
- Screenshots of the export interface
- Schema files (XSD, JSON Schema, etc.)

## Export Coverage Assessment

### Data Domain Coverage

KanTime Health is a comprehensive post-acute care platform storing clinical, billing, HR/payroll, scheduling, and operational data. The EHI export documentation reveals a two-track approach:

**Track 1 — Clinical data via CCDA 2.1:** The Patient API documents export of clinical data as C-CDA documents. The available sections map directly to standard USCDI v1 clinical data classes:
- Demographics, allergies, care team, encounters
- Problems/conditions, medications, immunizations, procedures
- Vital signs, lab results, goals, health concerns
- Social history, functional status, mental status
- Clinical notes (consultation, progress, H&P)
- Plan of treatment, medical equipment, assessments

This covers the standard clinical summary but is **explicitly limited to what C-CDA supports.** It does NOT address specialty-specific data that KanTime stores.

**Track 2 — Billing data via CSV/XLSX/PDF:** The 1-page EHI doc states that billing users can export "patient claims and payments." There is zero documentation of what this export contains — no field definitions, no column descriptions, no sample files.

**Major data domains from the product research that are NOT addressed in the export documentation:**

| Data Domain | Status |
|-------------|--------|
| OASIS assessments (home health) | Not mentioned — these are KanTime's core clinical assessment instruments |
| HIS data (hospice) | Not mentioned |
| Plans of care / 485s | Not mentioned (plan of treatment in CCDA is generic, not the auto-generated 485) |
| Visit notes / point-of-care documentation | Partially covered by CCDA clinical notes, but likely incomplete for the full breadth of visit documentation |
| Scheduling data | Not mentioned |
| E-prescribing records (KRx module) | Medications in CCDA, but prescribing workflow/history not documented |
| Authorization / eligibility records | Not mentioned |
| EVV data (GPS, telephony) | Not mentioned |
| Intake / referral records | Not mentioned |
| QA audit data | Not mentioned |
| HR / payroll / credential data | Not mentioned (and likely not EHI, but credential-linked care data may be) |
| Bereavement management (hospice) | Not mentioned |
| IDT meeting documentation | Not mentioned |
| Order tracking | Not mentioned |

The export appears to be a **USCDI v1 clinical summary + an undocumented billing export.** This is a significant gap for a (b)(10) certification, which requires export of ALL electronic health information — not just the USCDI clinical subset.

### Export Format & Standards

- **Clinical:** C-CDA 2.1 Release 2, USCDI v1. This is a recognized standard but is inherently limited to what C-CDA can represent. Post-acute care data (OASIS, HIS, EVV, 485 plans, specialized visit notes) does not map cleanly into C-CDA sections.
- **Billing:** CSV, XLSX, or PDF — format not documented. No schema or field definitions.
- **No bulk/batch mechanism documented:** The Patient API is a per-patient REST call. There is no documented way to export data for all patients or to perform a bulk export. The EHI PDF mentions "Single or Multi-Patient EHI Export" but provides no details on how multi-patient export works.

Could a third party reconstruct a patient record from this export? For the USCDI clinical slice — partially, yes, via the CCDA. For the full patient record as stored in KanTime — no. Billing data format is undocumented. Specialty-specific clinical data (OASIS, HIS, care plans) is not addressed at all.

### Documentation Quality

This is among the most minimal EHI export documentation one could produce:

- **The core EHI document is 1 page with 5 sentences.** It describes what formats are used but nothing about what data is included, how to access the export, or what the exported files look like.
- **No data dictionary exists** — neither for the CCDA sections nor for the billing CSV export.
- **No sample files** are provided.
- **No user instructions** for how to perform the export within the KanTime application.
- **No screenshots** of the export interface.
- The Patient API PDF is more substantive (14 pages with curl examples and sample CCDA output) but it documents the API mechanism, not the data content. It tells you how to call the API, not what clinical data you'll get back beyond section names.
- The documentation appears to be a compliance checkbox rather than a genuine effort to enable data portability.

### Structure & Completeness

- **Field-level documentation:** None. Not even table/entity names for the billing export.
- **Value sets:** Not documented. The CCDA will use standard C-CDA value sets, but any KanTime-specific coded fields are undocumented.
- **Relationships between entities:** Not documented.
- **Versioning:** The EHI PDF appears unchanged since its upload date (November 2023, modified December 2023). The Patient API PDF was uploaded March 2024.

## Access Summary
- Final URL (after redirects): https://kantime.com/wp-content/uploads/2023/11/EHI_Tool_Documentation.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- `https://kantime.com/interoperability/` — 404
- `https://kantime.com/ehi/` — 404
- WordPress uploads directory listing blocked (403)
- Sitemap mostly empty, no EHI-related page URLs found
- No additional EHI documentation found via web search
- The SmartOnFHIR API doc and FHIR base URLs are (g)(10) artifacts, not (b)(10) EHI export documentation. Downloaded for completeness but they don't document the EHI export.
