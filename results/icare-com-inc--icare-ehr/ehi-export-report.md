# iCare.com, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://icare.com/developers/ehi_export/
- CHPL IDs: 10314
- Product: iCare EHR Version 2
- Certification Date: 2020-02-20

## Navigation Journal

1. **HTTP probe of registered URL:**
   ```bash
   curl -sI -L "https://icare.com/developers/ehi_export/" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200 with Content-Type `text/html; charset=UTF-8`. WordPress site (Divi theme). The `Link` header revealed a WP JSON API endpoint at `https://icare.com/wp-json/wp/v2/pages/1286`.

2. **Fetched page content via WP REST API** (cleaner than parsing the Divi-wrapped HTML):
   ```bash
   curl -sL "https://icare.com/wp-json/wp/v2/pages/1286" -H 'User-Agent: Mozilla/5.0'
   ```
   This returned the full rendered content of the EHI Export page — a single HTML page with no downloadable file attachments.

3. **Searched page for downloadable files:**
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json).*"' /tmp/icare-ehi-page.html
   ```
   No downloadable files (PDF, ZIP, CSV, etc.) are linked from the EHI export page itself.

4. **Checked the parent Developers page** (`https://icare.com/developers/`) which links to:
   - `iCare.com-Application-Programming-Interface-Guide.pdf` (67-page API guide)
   - The EHI export page
   - An Inferno test results page

5. **Downloaded the API Guide PDF:**
   ```bash
   curl -sL "https://icare.com/wp-content/uploads/2023/09/iCare.com-Application-Programming-Interface-Guide.pdf" \
     -H 'User-Agent: Mozilla/5.0' -o downloads/iCare-API-Guide.pdf
   ```
   Verified: `file` confirms PDF document, 67 pages, 355 KB. Copyright 2020.

6. **Probed the sandbox FHIR endpoint** referenced on the EHI page:
   ```bash
   curl -sL "https://sandbox-r4.interopengine.com/fhir/r4/icare/metadata" \
     -H 'Accept: application/fhir+json'
   ```
   Returned a CapabilityStatement from "EMR Direct Interoperability Engine" (version 2026). Instantiates US Core Server and Bulk Data CapabilityStatements. Only declares Group/$export operation — no individual resource-level interactions beyond SearchParameter.

7. **Checked SMART configuration:**
   ```bash
   curl -sL "https://sandbox-r4.interopengine.com/fhir/r4/icare/.well-known/smart-configuration"
   ```
   Standard SMART-on-FHIR configuration with launch-ehr, launch-standalone, and client capabilities.

8. **Checked WordPress media library** for any additional files:
   ```bash
   curl -sL "https://icare.com/wp-json/wp/v2/media?per_page=100"
   ```
   No data dictionary files, schema documents, or EHI-related exports found. Only the API Guide PDF and marketing images.

9. **Checked certification page** (`https://icare.com/certification/`):
   The (b)(10) entry says: "Enable a user to export electronic health information for a single patient and provide a method to export electronic health information for a population of patients. Included with iCare subscription fee." It links back to the EHI export page. No additional documentation files.

10. **Took a full-page screenshot** of the EHI export page in Chrome.

## What Was Found

The EHI export documentation is a single web page at the registered URL describing three export methods:

### Method 1: CCD/HIM Export (In-App, Single Patient)
A user with proper privileges can:
- Generate a CCD (Continuity of Care Document) from within a patient chart: Reports > Clinical Summary > Continuity of Care and Referral Notes
- Export Clinical Assessments and Notes: Patient Info > HIM Request

No further detail is provided about the format, scope, or contents of these exports beyond what the names imply.

### Method 2: CSC Request for Full Data Export (Population)
The page states: "You may make a CSC request for export of the entirety of your organization's clinical data. The files will be provided via SFTP or other requested means and will include a description of the data file formats and data dictionary."

This is the most promising method for true (b)(10) compliance — a bulk data dump with a data dictionary — but **no data dictionary, file format specification, or any further documentation is provided on this page or anywhere on the site.** The data dictionary is apparently only delivered with the actual export files on request.

### Method 3: FHIR REST API Export (Single Patient, Population, Group)
The bulk of the page documents a FHIR R4 API hosted at `sandbox-r4.interopengine.com/fhir/r4/icare/`. It describes:

- **Single Patient**: `Patient/id/$export` or resource-specific queries
- **Population**: `Patient/$export` (Bulk Data)
- **Group**: `Group/GroupID/$export` (Bulk Data)
- **Authorization**: OAuth2 token via `/oauth/icare/token`

The FHIR API section lists the following "Data Elements" (FHIR resource types) with example query URIs:
1. CarePlan
2. AllergyIntolerance
3. CareTeam
4. Condition
5. Device
6. DiagnosticReport (LAB category only)
7. DocumentReference (contains assessments, notes, and documents)
8. Goal
9. Immunization
10. MedicationRequest
11. Observation (example uses LOINC 2708-6 only)
12. Procedure
13. Encounter

**Note at bottom of page:** "Items related to psychotherapy will not be included in any data export."

### The API Guide PDF (67 pages, 2020)
This is a separate, older document (Copyright 2020) describing the iCare proprietary REST API at `ehr.icare.com/iCareEHRWeb/rest/`. It predates the FHIR-based approach on the EHI export page. It covers:
- Login/token authentication
- Patient search
- Encounters
- Criteria Data Requests for 15 clinical categories: patient, careTeam, smokingStatus, problem, medication, medAllergy, labTest, labResult, vital, procedure, immunization, device, planOfTreatment, assessment, goal, healthConcern
- An "All Criteria Data Request" that returns a C-CDA XML document
- Output format: FHIR R4 JSON for individual criteria, C-CDA XML for the all-criteria request

The API guide is better documented than the web page, with input/output examples for each category, but covers essentially the same clinical data domains.

### FHIR CapabilityStatement
The sandbox server is powered by "EMR Direct Interoperability Engine" (a third-party interoperability platform), not iCare's own infrastructure. The CapabilityStatement declares:
- FHIR R4 (4.0.1)
- US Core Server conformance
- Bulk Data conformance
- Group/$export operation
- SMART-on-FHIR and UDAP security

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation covers a **narrow subset of US Core / USCDI clinical data**, not "all electronic health information" as (b)(10) requires.

**Domains clearly covered** (via FHIR API):
- Patient demographics
- Problems/conditions
- Medications
- Allergies/intolerances
- Lab results and diagnostic reports
- Vitals/observations
- Immunizations
- Procedures
- Care plans and goals
- Care team
- Implanted devices
- Clinical notes/documents (via DocumentReference)
- Encounters
- Smoking status
- Health concerns

**Domains clearly absent from the documented export:**
- **Billing and financial data** — iCare has an integrated RCM module (insurance verification, claims, payments, denials, coding), but none of this appears in any export method
- **Scheduling data** — appointment, procedure, and surgery schedules are core functionality but not exportable via the documented methods
- **Patient portal data** — secure messages, portal interactions, patient-submitted forms
- **Administrative data** — user roles, audit logs, configuration data
- **E-prescribing transaction data** — prescription tracking, EPCS records, Surescripts transactions
- **Document management** — the broader document vault (charts, forms, images, correspondence) beyond what DocumentReference captures
- **Public health reporting data** — syndromic surveillance, reportable lab results
- **Behavioral health data** — explicitly excluded ("items related to psychotherapy will not be included")
- **Inpatient-specific data** — nursing documentation, MAR, bed management
- **Order data** — CPOE orders beyond what maps to MedicationRequest

The "CSC request" method for bulk data export is described as covering "the entirety of your organization's clinical data," but no documentation, data dictionary, or format specification is publicly available for this method. It cannot be assessed for coverage.

### Export Format & Standards

The documented export uses **two formats**:
1. **FHIR R4 JSON** — for individual resource queries and bulk export. The resource types are standard US Core resources. No custom profiles or extensions are documented.
2. **C-CDA XML** — for the "All Criteria Data Request" in the older API. This is a standard clinical document format.

Both formats are **appropriate for the USCDI clinical data they cover**, but they are fundamentally **insufficient for a true (b)(10) export**. Neither FHIR US Core nor C-CDA can represent billing data, scheduling data, administrative records, audit logs, or many other data domains that iCare stores.

This is a classic case of **(g)(10) documentation repurposed as (b)(10) documentation**. The FHIR API described is essentially the same as what would satisfy the standardized API requirement under §170.315(g)(10). The 13 FHIR resource types listed map directly to US Core resources. There is no evidence of custom FHIR resources, extensions, or non-FHIR export formats to cover the remaining data.

The third-party infrastructure (EMR Direct Interoperability Engine) further confirms this — it's a standard interoperability middleware, not a custom (b)(10) export tool.

### Documentation Quality

**Poor.** The EHI export page is a single web page with:
- No data dictionary
- No field-level definitions
- No schema files
- No sample data or example export files
- No format specifications beyond naming FHIR resource types
- No documentation of the CSC bulk export method beyond its existence
- Repetitive, copy-paste structure for each resource type (every resource section repeats the same `Patient/id/$export` URI regardless of the resource type, which appears to be an error)

The API Guide PDF (2020) is somewhat better — it includes input/output examples for each data category, with JSON response samples. However, it's 6 years old and documents a different (proprietary REST) API than what the EHI page describes (FHIR Bulk Data).

The documentation has copy-paste errors: the "Encounter" section's example URI is for Procedure, and most resource sections list the Patient/$export endpoint rather than the resource-specific endpoint.

### Structure & Completeness

- **Field-level documentation**: None for the FHIR export. The page lists resource types but not fields, data types, constraints, or value sets. The older API guide shows example JSON responses which provide implicit field documentation.
- **Value sets**: Not documented.
- **Relationships between entities**: Not documented.
- **Versioning**: The WP JSON metadata shows the page was last modified 2025-10-18. The API guide PDF is from 2020.
- **Sample data**: No sample export files provided. The API guide has example JSON responses.

**Overall assessment:** iCare has documented what appears to be their (g)(10) FHIR API and labeled it as their (b)(10) EHI export. The documented export covers only US Core clinical data — roughly 15 resource types covering the standard USCDI data classes. Major data domains known to exist in the product (billing, scheduling, administrative, e-prescribing) are absent. The single most interesting export method — the CSC bulk data request that allegedly covers "the entirety of your organization's clinical data" — has no public documentation whatsoever. A developer receiving an export via this method would apparently get a data dictionary with the files, but there is no way to assess this method's coverage or format from the public documentation.

## Access Summary
- Final URL (after redirects): https://icare.com/developers/ehi_export/
- Status: found
- Required browser: no (content available via WP REST API and curl)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The WordPress site uses the Divi theme which wraps content in heavy JavaScript, but the WP REST API (`/wp-json/wp/v2/pages/1286`) provides clean access to the rendered content.
- The WP JSON API for parent page 86 (`/developers/`) sometimes returned empty responses; direct HTML fetch worked.
- No data dictionary, schema files, or downloadable documentation were found despite checking the WordPress media library, the certification page, and all linked pages.
- The FHIR CapabilityStatement at the sandbox endpoint is minimal — only declares Group/$export, not the individual resource interactions documented on the page.
