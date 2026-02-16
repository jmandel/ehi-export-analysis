# OmniMD Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://omnimd.com/rwt/
- CHPL IDs: 11354 (v20, certified 2023-10-24), 10784 (v18.0, certified 2022-01-10)
- Developer: OmniMD Inc., Hawthorne, NY
- Contact: Dr. Giriraj Tosh Purohit (DrGPurohit@OmniMD.com)

## Navigation Journal

### Step 1: Initial probe of registered URL
```bash
curl -sI -L "https://omnimd.com/rwt/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200 OK, Content-Type: text/html (WordPress site). Page titled "Real World Testing Plan and Results."

### Step 2: Fetch and examine the page
```bash
curl -sL "https://omnimd.com/rwt/" -H 'User-Agent: Mozilla/5.0' -o /tmp/omnimd-rwt.html
```
The page is a WordPress page (350KB) with the title "Real World Testing Plan and Results." It contains two sections:

- **OMNIMD V18.0**: Links to RWT plans (2022–2025 XLS files) and results (2022–2024 DOC files).
- **OMNIMD V20**: Links to a 2025 RWT plan (XLS), 2024 RWT result (DOC), and — crucially — a button labeled **"ELECTRONIC HEALTH INFORMATION (EHI) EXPORT"** linking to a Word document.

The EHI export documentation is a single button placed under the V20 section at the bottom of the page, co-located with real-world testing materials.

### Step 3: Download the EHI export document
```bash
curl -sL "https://omnimd.com/wp-content/uploads/2025/10/ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc
```
Verified: Microsoft Word 2007+ format (docx), 38,616 bytes. No tables, no images other than a logo.

### Step 4: Check footer links for additional documentation
The page footer contains an "Open-API" link. Navigated to `https://omnimd.com/open-api/`, which contains:
- API terms and conditions
- A "Reference for Open API" button linking to `https://prod.omnixchange.com/openapiui` (interactive API docs)
- A "Download PDF" button linking to `https://omnimd.com/wp-content/uploads/2025/10/OpenApi.pdf`

### Step 5: Download Open API documentation
```bash
curl -sL "https://omnimd.com/wp-content/uploads/2025/10/OpenApi.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/OpenApi.pdf
```
Verified: PDF document, 9 pages, 295,467 bytes. Created 2024-05-10 with Microsoft Word for Microsoft 365.

### Step 6: Download interactive API docs
```bash
curl -sL "https://prod.omnixchange.com/openapiui" -H 'User-Agent: Mozilla/5.0' -o downloads/openapiui.html
curl -sL "https://prod.omnixchange.com/openAPI/Help" -H 'User-Agent: Mozilla/5.0' -o downloads/openapi-help.html
```
Both returned 200 OK. The interactive UI is a single-page app with documentation for the OpenAPI v1.0. The Help page is a standard ASP.NET Web API Help page listing all endpoints with "No documentation available" for each.

### Step 7: Search for additional documentation
- Checked `https://omnimd.com/onc-transparency-and-costs/` — regulatory/cost disclosures, no EHI export content.
- Checked `https://omnimd.com/interoperability/` — marketing page for OmniXchange interoperability services, no EHI export details.
- Probed common paths (`/fhir/`, `/api/`, `/bulk-data/`, `/smart/`, `/ehi/`, `/data-dictionary/`) on both omnimd.com and prod.omnixchange.com — all 404 except the paths already discovered.
- Queried the WordPress REST API (`/wp-json/wp/v2/pages`) to enumerate all 108 pages. No additional EHI export, data dictionary, or schema pages found.
- Checked the EHI export Word document for embedded hyperlinks — found only external standards references (HL7 C-CDA, USCDI, FHIR US Core).
- Checked the OpenApi PDF for embedded files — 0 embedded files.

No FHIR server, bulk data endpoint, or SMART configuration was found on either domain.

## What Was Found

### Primary EHI Export Documentation (Word document)
The EHI export documentation is a single-page Word document titled "OmniMD 170.315(b)(10) Electronic Health Information Export Version 1.0." It describes two export mechanisms:

**1. C-CDA Export (primary)**
OmniMD supports "bulk export of HL7 CCDA XML files" compliant with USCDI Version 1. The document states export is available for both a single patient and for the patient population. The following C-CDA sections are listed:

1. Advance Directives
2. Allergies, Adverse Reactions, Alerts
3. Assessments
4. Encounters
5. Family History
6. Functional Status
7. Immunizations
8. Instructions
9. Medical Equipment
10. History of Medication
11. Medication Administered
12. Insurance Providers
13. Treatment Plan
14. Problem List
15. Procedures
16. Progress Note
17. Chief Complaint and Reason for Visit
18. Lab Results
19. Social History
20. Vital Signs

**2. FHIR Bulk Data (secondary, by reference)**
The document also states OmniMD supports "HL7 Version 4.0.1 FHIR Release 4, FHIR US Core Implementation Guide STU V3.1.1, HL7 FHIR Bulk Data export" and refers to the 170.315(g)(10) standardized API specification. No additional FHIR-specific documentation was found beyond this reference.

### Open API Documentation (PDF and interactive UI)
The OpenApi.pdf (9 pages) documents OmniMD's REST API (version 1.0), which is the (g)(7)/(g)(9) API, not the (b)(10) export. However, it is relevant because:
- The `POST api/Patient/GetPatientData` endpoint can retrieve patient data as CDA XML 2.1, with selectable sections matching the EHI export sections
- The `POST api/Patient/DownloadCDAPatient` endpoint provides CDA download
- The API explicitly states it satisfies "CEHRT Regulations § 170.315(g)(7) and § 170.315(g)(9)"

The API documentation describes the `GetPatientData` endpoint with toggleable boolean parameters for each C-CDA section (AdvanceDirective, Allergy, Assessment, Encounter, FamilyHistory, etc.), date range filters, and returns CDA 2.1 XML.

The interactive API UI at `https://prod.omnixchange.com/openapiui` provides the same information in web format with example calls and responses. The help page at `https://prod.omnixchange.com/openAPI/Help` lists all API endpoints (Account, User, Patient, Practice, Values, Audit, Role) but with "No documentation available" for each individual endpoint.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export covers 20 C-CDA sections — a clinical data subset that maps closely to USCDI v1 data classes. Based on the product research, OmniMD stores a significantly broader set of data than what is covered:

**Clearly covered by the export:**
- Demographics (implicit in C-CDA patient header)
- Problem lists / diagnoses
- Medications (history and administered)
- Allergies and adverse reactions
- Lab results
- Vital signs
- Immunizations
- Procedures
- Clinical encounter notes (via Progress Note, Assessments sections)
- Care plans (via Treatment Plan section)
- Advance directives
- Family history
- Social history
- Functional status
- Insurance providers (Payer section)

**Absent or not mentioned in the export:**
- **Billing data** — Claims, charges, payments, denial records, CPT/ICD coding data. OmniMD has extensive RCM/billing functionality (built-in billing software, claim scrubbing, denial management, revenue analytics). The "Insurance Providers" (Payer) C-CDA section captures payer identity, not billing transactions. This is a significant gap.
- **Prescription/e-prescribing records** — While "History of Medication" and "Medication Administered" are exported, detailed prescription transaction records, pharmacy network interactions, controlled substance prescribing history (EPCS), and medication reconciliation data may not be fully captured in C-CDA medication sections.
- **Patient portal data** — Secure messages between patients and providers, appointment requests, and online payment transactions are not covered by C-CDA export.
- **Telehealth/RPM data** — Video consultation records, remote monitoring device data, and RPM encounter documentation are not mentioned.
- **Documents and attachments** — Scanned documents, faxes, patient-uploaded files, and external records incorporated into the chart are not described in the export.
- **Referrals and care coordination** — While "Reason for Referral" is a parameter in the API, there is no mention of referral tracking data in the export sections.
- **Specialty-specific clinical data** — OmniMD claims support for 40+ medical specialties with specialty-specific templates. These specialty templates, custom forms, and clinical assessments likely generate data beyond what standard C-CDA sections capture.
- **AI-generated documentation** — AI Scribe ambient documentation and AI Clinician decision support outputs are not addressed.

**The core problem:** This export is essentially a C-CDA patient summary — which is the same data that a (g)(10) FHIR API would expose. It covers the USCDI clinical data classes well but does not address the (b)(10) requirement to export **all** electronic health information in the designated record set. The export covers roughly the same scope as the vendor's (g)(10) certification.

### Export Format & Standards

- **Format**: HL7 C-CDA XML (CDA version 2.1), compliant with USCDI v1
- **Standard**: Well-recognized, widely implemented clinical document standard
- **FHIR alternative**: Referenced but not independently documented; appears to be the (g)(10) FHIR Bulk Data API
- **Appropriateness**: C-CDA is appropriate for the clinical data it covers, but inappropriate as the sole export format for a product that stores billing, scheduling, telehealth, RPM, and AI-generated data. These data types do not map to C-CDA sections.
- **Reconstructability**: A third party could import the clinical summary from these C-CDA documents using standard tools, but could not reconstruct the full patient record including billing history, portal interactions, telehealth records, or specialty-specific assessments.

### Documentation Quality

- **Readability**: The EHI export document is a single page, easy to read but extremely thin. It is essentially a bulleted list of C-CDA sections with no explanatory detail.
- **Data dictionary**: None. There is no field-level documentation, no table definitions, no description of what each section contains beyond the section name.
- **Data types, value sets, constraints**: Not specified. The document points to the HL7 C-CDA specification for format details.
- **Worked examples**: None in the EHI export doc. The OpenApi PDF and interactive UI provide some example API calls with JSON authentication responses and describe parameters, but do not show example C-CDA output.
- **Developer implementability**: A developer would need to refer to the HL7 C-CDA specification to understand the export format. The OmniMD documentation alone does not provide enough detail to implement an import.
- **Maintenance**: The EHI export document is Version 1.0. The PDF was created 2024-05-10. The documentation appears to be a compliance checkbox — minimal content created to satisfy the certification requirement.

### Structure & Completeness

- **Granularity**: Section names only. No field-level detail, no data types, no cardinality, no constraints.
- **Coded fields**: Not documented. C-CDA sections use coded values (ICD-10, SNOMED, LOINC, RxNorm) but the documentation does not describe which code systems are used or what value sets apply.
- **Relationships**: Not documented. The C-CDA format inherently expresses some relationships (e.g., medication linked to encounter), but the documentation does not describe how OmniMD structures these.
- **Versioning**: Listed as Version 1.0. No change history.

## Access Summary
- Final URL (after redirects): https://omnimd.com/rwt/ (no redirect)
- Status: found
- Required browser: no (direct download link in HTML)
- Navigation complexity: one_click (EHI export button at bottom of RWT page)
- Anti-bot issues: none

## Obstacles & Dead Ends

- The registered URL (https://omnimd.com/rwt/) is a "Real World Testing Plan and Results" page. The EHI export documentation is placed as a single button at the bottom, co-located with RWT artifacts rather than on a dedicated EHI export page. This is an unusual placement that could cause users to overlook it.
- The WordPress REST API was accessible and confirmed no additional EHI/export/data-dictionary pages exist on the site.
- No FHIR server or bulk data endpoint was discoverable at omnimd.com or prod.omnixchange.com, despite the EHI export document referencing FHIR Bulk Data as a secondary export mechanism.
- The OpenAPI Help page (`/openAPI/Help`) lists all API endpoints with "No documentation available" — a default ASP.NET Web API scaffold that was never populated with descriptions.
- The interactive API UI at `prod.omnixchange.com/openapiui` explicitly states it satisfies (g)(7)/(g)(9), not (b)(10), confirming this is a separate API from the EHI export mechanism.
