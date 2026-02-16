# Medi-EHR, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: http://medi-ehr.com/compliance
- Final URL: https://medi-ehr.com/compliance/
- CHPL IDs: 10831
- Product: Medi-EHR v2.1
- Certification date: 2022-02-15

## Navigation Journal

### Step 1: Initial probe

```bash
curl -sI -L "http://medi-ehr.com/compliance" -H 'User-Agent: Mozilla/5.0'
```

HTTP 301 → `https://medi-ehr.com/compliance` → 301 (WordPress trailing slash redirect) → `https://medi-ehr.com/compliance/` → HTTP 200. Content-Type: text/html; charset=UTF-8. WordPress site on PHP/8.4.17, Apache server.

### Step 2: Examine compliance page

The compliance page is a WordPress page (page ID 8827, last modified 2026-01-17) with two sections:

**Section I: Electronic Health Information Export**
- **Single Patient Export**: "Medi-EHR allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance using the following standardized file formats explained below"
- **Multi-Patient Export**: "Medi-EHR can export all the data for a patient population in our standardized format explained below"
- **File Formats**: "These are standardized formats. Medi-EHR updates all formats on a quarterly schedule unless otherwise indicated."
  - **CSV**: Generic description of CSV format (no data dictionary, no field list)
  - **HTML**: Generic description of HTML format (no details on structure)

**Section II: API documentation**
- A "Click Here" link to `https://proda.mediemr.net:8443/pls/htmldb/f?p=300:10`

That's the entire EHI export documentation on the compliance page. No downloadable files (PDF, ZIP, CSV, etc.), no data dictionary, no schema, no sample data.

### Step 3: Follow API documentation link

The "Click Here" link leads to an Oracle APEX application (developer portal). Page 10 contains an embedded iframe loading a pre-rendered Swagger UI page from:

```
https://proda.mediemr.net:8443/i/mediemr/API_Document.html
```

This is the "MediEHR Patient Access" API (v2.1) — a proprietary REST API (not FHIR, not any standard) with 4 endpoints:

1. **POST /mediehrlogintest.php** — Test login credentials (OFFICE, ACCESS_TOKEN, USERNAME)
2. **POST /mediehrgetpatient.php** — Search for patient by demographics, returns XML with MRN, name, address, phone, email
3. **POST /mediehrrotatetokens.php** — Rotate access/refresh tokens
4. **POST /mediehrgetpatientdata.php** — Export patient data in C-CDA 2.1 format by MRN, with date range and 19 selectable sections

The C-CDA export endpoint accepts these toggleable sections (S=show, H=hide):
- PAT_ALLERGY, PAT_MEDS, PAT_PROBLEM, PAT_ENCOUNTER, PAT_IMMUNIZATION, PAT_VITALS, PAT_SOCHX, PAT_PROCEDURES, PAT_LABS, PAT_IMPLANTABLEDEVICES, PAT_GOALS, PAT_FUNCTIONALSTATUS, PAT_COGNITIVESTATUS, PAT_REFERRAL, PAT_ASSESSMENT, PAT_CARETEAM, PAT_HEALTH_CONCERNS, PAT_PLANOFTREAT, PAT_DI_REPORT

The API returns XML for all responses (application/xml). The C-CDA export endpoint response is a complete `<ClinicalDocument>` in HL7 CDA format.

Authentication uses a proprietary access/refresh token scheme (not OAuth 2.0, not SMART on FHIR). Tokens are obtained by registering on the developer portal and getting approval from the office/facility.

### Step 4: Check other links

- **Custom Export page** (`/custom-export/`): Marketing/sales page for a paid "Custom Export" service. Not EHI export documentation — it's about custom data extraction services for practices.
- **Public FHIR API page** (`/public-fhir-api/`): Links to InteropEngine sandbox FHIR R4 server and FHIR documentation. Production endpoints listed as "Coming Soon." Points to `interopengine.com/2021/open-api-documentation.html` for FHIR R4 docs with disclaimer "some details on our partner integration documentation may not apply to us." This is the (g)(10) standardized FHIR API, separate from the (b)(10) export.
- **FHIR Service Base URL Bundle** (`MEDIDATA.GEN_FHIR_JSON_FOR_ALL_OFFICES`): JSON FHIR Bundle with sandbox endpoint (`sandbox-r4.interopengine.com/fhir/r4/medi-ehr/`) and one Organization resource. Confirms the FHIR API is handled by InteropEngine.
- **Developer Portal Home** (`f?p=300:1`): Requires login (redirects to login page 101). The API Documentation page (page 10) is publicly accessible without login.
- **Term, Termination and Return of Data FAQ**: Page renders with only navigation, no visible body content (appears to be an empty WordPress page).
- **ONC Certification and Costs**: Standard transparency disclosure with criteria list and cost information. No EHI export details.

### Step 5: Downloads

Downloaded the API document HTML, compliance page, screenshots, and FHIR bundle JSON. Ran enrichment script to extract structured API data.

## What Was Found

Medi-EHR's EHI export documentation is minimal. It consists of:

1. **A brief compliance page** (3 paragraphs) stating that the system can export EHI for single patients and multi-patient populations in CSV and HTML formats. No data dictionary, no field definitions, no schema, and no sample data are provided. The CSV and HTML descriptions are generic definitions of those file formats ("a comma-separated values file is a delimited text file...") — not descriptions of what data fields or tables are included in the export.

2. **A proprietary REST API** (4 endpoints) accessible through an Oracle APEX developer portal. The primary export endpoint (`/mediehrgetpatientdata.php`) returns patient data in C-CDA 2.1 XML format with 19 selectable clinical sections. This API uses proprietary token-based authentication (not OAuth 2.0 or SMART on FHIR). There is no OpenAPI/Swagger JSON spec — only a pre-rendered static HTML version of Swagger UI.

3. **A separate FHIR API** powered by InteropEngine (third-party) for the (g)(10) standardized API requirement. This is distinct from the (b)(10) EHI export. Production endpoints are listed as "Coming Soon" as of the collection date.

The compliance page mentions CSV and HTML export formats but the API documentation only shows C-CDA 2.1 XML output. It's unclear whether:
- The CSV/HTML exports are performed through a different mechanism (UI-based export within the application)
- The CSV/HTML exports use the same API with different parameters
- The compliance page description is aspirational or refers to a different feature

There is no documentation explaining how to perform the CSV or HTML exports, what data fields they contain, or how they differ from the C-CDA API export.

## Export Coverage Assessment

### Data Domain Coverage

The C-CDA 2.1 export via the API covers **19 clinical sections**, which map to standard C-CDA content:

| API Parameter | C-CDA Section | Coverage |
|---|---|---|
| PAT_ALLERGY | Allergies and Adverse Reactions | Clinical |
| PAT_MEDS | Medications | Clinical |
| PAT_PROBLEM | Problems / Diagnoses | Clinical |
| PAT_ENCOUNTER | Encounters | Clinical |
| PAT_IMMUNIZATION | Immunizations | Clinical |
| PAT_VITALS | Vital Signs | Clinical |
| PAT_SOCHX | Social History | Clinical |
| PAT_PROCEDURES | Procedures | Clinical |
| PAT_LABS | Laboratory Results | Clinical |
| PAT_IMPLANTABLEDEVICES | Implantable Devices | Clinical |
| PAT_GOALS | Goals | Clinical |
| PAT_FUNCTIONALSTATUS | Functional Status | Clinical |
| PAT_COGNITIVESTATUS | Cognitive Status | Clinical |
| PAT_REFERRAL | Referrals | Clinical |
| PAT_ASSESSMENT | Assessment | Clinical |
| PAT_CARETEAM | Care Team Members | Clinical |
| PAT_HEALTH_CONCERNS | Health Concerns | Clinical |
| PAT_PLANOFTREAT | Plan of Treatment | Clinical |
| PAT_DI_REPORT | Diagnostic and Imaging Reports | Clinical |

**Clearly missing from the documented export:**

- **Billing data**: Medi-EHR has an integrated billing/practice management module with superbills, claims, payments, insurance verification, and revenue cycle management. None of this is represented in the C-CDA export. Billing records (charges, claims, payments) are core EHI — part of the designated record set.
- **Prescription history**: While PAT_MEDS covers current medications, e-prescribing history (Surescripts transmissions, controlled substance prescriptions via EPCS, refill history) is not explicitly documented as a distinct export.
- **Clinical notes/documents**: C-CDA can contain clinical notes but no specific section for clinical documentation (progress notes, H&P, discharge summaries, specialty templates) is listed. The 19 sections are structured data categories, not free-text document exports.
- **Patient portal data**: Secure messages, prescription refill requests, patient intake forms, bill payments — none documented.
- **Consent forms**: Medi-EHR has a dedicated Consent Module; consent records are not represented.
- **Workers' compensation / no-fault claims**: A specialized module exists for workers' comp and no-fault claims processing. This specialty data is not documented.
- **Behavioral health data**: The product has a dedicated behavioral health module for mental health and substance abuse treatment. No behavioral health-specific assessments or treatment plans are documented beyond what generic C-CDA sections might cover.
- **ASC surgical data**: The ambulatory surgery center module includes pre-op/post-op management and surgical scheduling. Operative notes, anesthesia records, and surgical-specific data are not documented.
- **Residential treatment data**: Addiction and mental health residential treatment tracking, bed management — not documented.
- **Scanned documents and images**: Document management features are described in the product; no mechanism for exporting attached documents or images is documented.
- **Telemedicine records**: Video visit records and virtual encounter documentation are not explicitly documented.
- **Insurance/enrollment information**: Benefits verification data, insurance records — not documented beyond what demographics might include.

### Export Format & Standards

The documented export mechanism is a **proprietary REST API returning C-CDA 2.1 XML** documents. C-CDA is a recognized standard (HL7 CDA R2 with specific templates), which is positive for clinical data exchange. However:

- C-CDA is fundamentally a **clinical document** standard. It has no native support for billing data, claims, administrative records, or many specialty-specific data types. Using C-CDA as the sole export format structurally limits what can be exported.
- The compliance page also mentions **CSV and HTML** exports, which could theoretically cover billing and other non-clinical data — but there is zero documentation about what these exports contain.
- The API uses **proprietary authentication** (custom access/refresh tokens), not SMART on FHIR or OAuth 2.0. A developer would need to register on the portal, get facility approval, and manage tokens manually.
- The API base URL is `https://proda.mediemr.net/patient/v1` — this appears to be a production server (not sandbox).
- There is **no bulk/multi-patient export endpoint** documented in the API. The API only has `mediehrgetpatientdata.php` which takes a single PATIENT_MRN. The compliance page mentions multi-patient export capability but no API mechanism for it is documented.

### Documentation Quality

The documentation quality is **poor**:

- **No data dictionary**: There is no field-level documentation for any export format. For the C-CDA export, we know the 19 section categories but not what specific data elements, codes, or templates are used within each section.
- **No sample data**: No example export files, sample C-CDA documents, or test data are provided.
- **No schema**: No XSD, JSON Schema, or template IDs for the C-CDA output are documented. The API docs show a truncated C-CDA response (`...CCDA Document...`) without actual content.
- **No CSV/HTML format documentation**: The compliance page mentions these formats but provides zero information about their structure, fields, or how to obtain them.
- **No export instructions**: No user-facing documentation about how to perform the export from the UI. The API docs describe programmatic access but not the end-user workflow.
- **Generic format descriptions**: The CSV and HTML descriptions on the compliance page are dictionary definitions of the file formats, not descriptions of the export data. Saying "CSV is a delimited text file that uses a comma to separate values" tells a developer nothing about the export schema.
- **Copy-paste errors**: The API documentation has a duplicated USERNAME parameter in the patient data endpoint, and the `mediehrgetpatientdata.php` block reuses the HTML `id` from `mediehrrotatetokens.php`.
- **No versioning or change history**: The compliance page states formats are "updated quarterly" but provides no version history or changelog.

A developer attempting to import this data would have significant difficulty. They would know the API endpoints and authentication flow, but they would not know the detailed structure of the C-CDA output, what coded values to expect, or what the CSV/HTML exports contain.

### Structure & Completeness

- **Granularity**: Section-level only (19 named sections). No field-level, data type, or cardinality documentation.
- **Value sets**: Not documented. No information about coded fields, terminologies used, or custom codes.
- **Relationships**: Not applicable — C-CDA is a document standard with its own structure. No relational data model is documented.
- **Coverage of product capabilities**: The export covers standard clinical C-CDA sections (~USCDI-level data) but does not address the substantial billing, administrative, and specialty-specific data that Medi-EHR stores. This is a classic (b)(10)/(g)(10) conflation — the documented export covers clinical summary data appropriate for (g)(10), not the full designated record set required for (b)(10).

### Summary Assessment

Medi-EHR's EHI export documentation is a **compliance checkbox** rather than a substantive technical resource. The vendor has a proprietary C-CDA export API that covers standard clinical data categories, which likely serves double duty for (b)(10) and (g)(10) requirements. However:

1. The export covers only **clinical summary data** in C-CDA format — approximately the USCDI data set. This is appropriate for (g)(10) but insufficient for (b)(10), which requires export of **all** electronic health information in the designated record set.

2. The product stores substantial data beyond clinical summaries: billing/claims, workers' comp records, behavioral health assessments, ASC surgical data, residential treatment records, consent forms, patient portal messages, and scanned documents. None of this is documented as part of the export.

3. The CSV and HTML export formats mentioned on the compliance page could potentially cover the missing data domains, but they are completely undocumented — no field lists, no samples, no instructions for how to produce them.

4. The documentation provides no mechanism for multi-patient bulk export via the API, despite the compliance page claiming this capability.

5. There is no data dictionary at any level of granularity — not even table names or field counts.

This vendor appears to be a small operation (no public reviews, estimated small install base) that has met the letter of certification requirements but has not invested in comprehensive EHI export documentation. The export mechanism exists (C-CDA via API + claimed CSV/HTML), but the documentation is too sparse for a third party to meaningfully assess coverage or implement data import.

## Access Summary
- Final URL (after redirects): https://medi-ehr.com/compliance/
- Status: found
- Required browser: no (curl works for HTML pages; browser helpful for Swagger UI visualization)
- Navigation complexity: one_click (compliance page → "Click Here" for API docs)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The Custom Export page (`/custom-export/`) is a marketing page for a paid service, not EHI export documentation
- The Developer Portal home page (`f?p=300:1`) requires login, but the API docs page (`f?p=300:10`) is publicly accessible
- The FHIR API documentation points to InteropEngine's generic docs with a disclaimer that "some details on our partner integration documentation may not apply to us"
- The "Term, Termination and Return of Data FAQ" page appears to have no body content
- No OpenAPI/Swagger JSON spec is available — only a pre-rendered static HTML version of Swagger UI
- The API document HTML is a browser-saved page (includes Chrome extension artifacts like youtube-seek scripts), suggesting it was manually saved rather than served directly
- Production FHIR endpoints listed as "Coming Soon" as of collection date
