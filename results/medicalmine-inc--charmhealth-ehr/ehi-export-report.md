# MedicalMine Inc. (CharmHealth EHR) — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.charmhealth.com/ehr/electronic-health-information-export.html
- CHPL IDs: 9741
- Developer: MedicalMine Inc.
- Product: CharmHealth EHR v1.2
- Certification date: 2018-11-15

## Navigation Journal

**1. Initial probe:**
```bash
curl -sI -L "https://www.charmhealth.com/ehr/electronic-health-information-export.html" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200 with `Content-Type: text/html`, 10,141 bytes. Served from AmazonS3 via CloudFront. No redirects.

**2. Fetched and examined the main page:**
```bash
curl -sL "https://www.charmhealth.com/ehr/electronic-health-information-export.html" -H 'User-Agent: Mozilla/5.0' -o electronic-health-information-export.html
```
The page is a static HTML page titled "Electronic Health Information (EHI) Export". It describes three export mechanisms:
- **FHIR R4 API** for clinical data (linking to their API documentation)
- **HL7 CCDA** export (via API and via the EHR UI)
- **CSV export** for billing data (linking to resource center help pages)

**3. Downloaded the FHIR API documentation:**
```bash
curl -sL "https://www.charmhealth.com/resources/fhir/index.html" -H 'User-Agent: Mozilla/5.0' -o fhir-api-documentation.html
```
A single-page API documentation site (420KB) documenting 24 FHIR R4 resources with list/get/search operations, OAuth authentication, Bulk Export API, and CCDA export API.

**4. Downloaded encounter export instructions:**
```bash
curl -sL "https://www.charmhealth.com/resources/consultation/create-encounter.html" -H 'User-Agent: Mozilla/5.0' -o create-encounter.html
```
The "Create Encounter" resource center page includes an "Export" section with screenshots showing how to export encounters as PDF, HL7 CCDA, or Surveillance Report from the EHR UI.

**5. Downloaded export encounter screenshots from the resource center:**
```bash
curl -sL "https://www.charmhealth.com/resources/consultation/images/export-encounter.jpg" -o export-encounter.jpg
curl -sL "https://www.charmhealth.com/resources/consultation/images/export-encounter1.jpg" -o export-encounter1.jpg
```
These screenshots show the EHR encounter interface with export dropdown menus. First screenshot shows bulk export options (Export Encounters as PDF, Export Encounters as PDF (New), Export Encounters as HL7 CCDA) via the "..." (More Options) menu. Second screenshot shows per-encounter export options (Encounter as PDF, Encounter as HL7 CCDA, Surveillance Report - Registration, Encounter as PDF (New)) via the Export button.

**6. Downloaded billing documentation pages:**
```bash
curl -sL "https://www.charmhealth.com/resources/billing/reports.html" -o billing-reports.html
curl -sL "https://www.charmhealth.com/resources/analytics/analytics.html" -o analytics.html
curl -sL "https://www.charmhealth.com/resources/billing/claims.html" -o claims.html
curl -sL "https://www.charmhealth.com/resources/billing/export-encounters-as-hl7-messages-for-billing-outside-charmhealth.html" -o export-encounters-as-hl7-messages.html
```
These are resource center help pages describing how to generate and export billing reports, claims data, insurance reports, and HL7 billing messages — all as CSV or PDF.

**7. Took browser screenshots:**
- Main EHI export page (full-page screenshot)
- FHIR API documentation top section
- Bulk Export section of FHIR API docs

**8. Built enrichment script to extract structured data from FHIR API docs:**
Used Bun TypeScript to parse the 420KB HTML into a queryable JSON with all 24 resources, 68 operations, parameters, OAuth scopes, Bulk Export API details, and CCDA API details.

## What Was Found

CharmHealth documents a **multi-format EHI export approach** with three mechanisms:

### 1. FHIR R4 API (Clinical Data)

The CharmHealth API Program exposes a comprehensive FHIR R4.0.1 API at `https://ehr2.charmtracker.com/api/ehr/v2/fhir`. It supports **24 FHIR resource types**:

- AllergyIntolerance, Appointment, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, FamilyMemberHistory, Goal, Immunization, Location, MedicationAdministration, MedicationRequest, Medication, Observation, Organization, Patient, Practitioner, Procedure, Provenance, QuestionnaireResponse, RelatedPerson

19 of 24 resources reference US Core profiles. Each resource supports list, get-by-ID, and search operations (with some exceptions: Medication has only get-by-ID; Provenance has only get-by-ID).

Authentication uses SMART on FHIR (OAuth 2.0) with support for:
- Patient-facing applications (confidential and public clients)
- Provider-facing applications
- Backend services (JWT-based)
- API Key authentication

The API supports `.well-known/smart-configuration` and a FHIR CapabilityStatement at the metadata endpoint.

### 2. Bulk Export API (FHIR Bulk Data)

The FHIR Bulk Export API enables exporting data for groups of patients as NDJSON files:
- `GET /Group/{group_id}/$export` — initiates export
- `GET /$export-poll-status?_jobid=...` — checks export status, returns download URLs when complete
- `DELETE /$export-poll-status?_jobid=...` — cancels an export

The response includes download URLs for each resource type (e.g., `Binary/Patient/...`, `Binary/Encounter/...`).

### 3. HL7 CCDA Export

Available via:
- **API**: `GET /patients/{patient_id}/ccda` with optional date range filtering
- **UI**: From the encounter dashboard, via "Export" button → "Encounter as HL7 CCDA" or via "..." menu → "Export Encounters as HL7 CCDA"

### 4. CSV Billing Data Export

Billing data can be exported as CSV from the EHR interface:
- **Invoice & Receipts Reports**: Payment details, receipts, refunds, grouped by facility/patient/provider
- **Insurance Reports**: Patient insurance details exportable as CSV
- **Claims Reports**: Claims data including claims aging by payer, denied procedures, and detailed claim information
- **Encounter Summary Reports**: Combined view of appointments, encounters, invoices, claims, and payments
- **HL7 Billing Messages**: Encounters can be exported as HL7 messages for external billing systems

Each billing report section in the resource center describes an "Export as CSV" button with options to export all details with subtotals or selected columns.

### 5. PDF Export

Individual encounters can be exported as PDF from the UI, and billing reports can be exported as PDF with selectable layout (landscape/portrait).

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered (via FHIR API):**
- Patient demographics (Patient)
- Allergies (AllergyIntolerance)
- Conditions/diagnoses (Condition)
- Medications and prescriptions (Medication, MedicationRequest, MedicationAdministration)
- Lab results and vitals (Observation, DiagnosticReport)
- Immunizations (Immunization)
- Procedures (Procedure)
- Care plans and goals (CarePlan, Goal)
- Care teams (CareTeam)
- Encounters/visits (Encounter)
- Documents and attachments (DocumentReference)
- Family history (FamilyMemberHistory)
- Appointments (Appointment)
- Questionnaire responses (QuestionnaireResponse) — covers intake forms, pre-screening
- Related persons/contacts (RelatedPerson)
- Clinical notes (likely via DocumentReference or embedded in Encounter)

**Covered via CSV export (billing):**
- Invoices and receipts
- Insurance information
- Claims data
- Payment records
- Denied procedures
- Encounter summaries with billing details

**Potentially missing or unclear:**
- **Custom/specialty clinical data**: CharmHealth has particular traction with integrative/functional medicine practices. Drug-herb interaction data, supplement orders (FullScript integration), and custom template content may not map cleanly to standard FHIR resources. It's unclear if these specialized data types are captured in the FHIR export or only in the CCDA/PDF exports.
- **Telehealth session records**: The product includes integrated telehealth with recording capability, consent documents, and session metadata. These are not represented in any obvious FHIR resource.
- **Secure messaging (CharmConnect)**: Provider-to-provider and provider-to-patient encrypted messages are a significant data store. No FHIR resource or export mechanism is documented for this.
- **Inventory data**: Medication/supplement inventory tracking with stock levels and dispensing records — not covered in the FHIR API.
- **AI Scribe transcriptions**: CharmAI Scribe generates clinical notes from ambient recordings. The raw transcriptions and AI-suggested codes may or may not be included in DocumentReference or encounter data.
- **Images and image annotations**: The EHR supports image annotation tools, but it's unclear if annotated images are exported via DocumentReference.
- **Flowsheet data**: The product supports flowsheets for tracking vitals and lab results across visits — likely captured in Observation, but not explicitly documented.
- **Referral data**: The product has referral management; no clear export mechanism beyond what may be in DocumentReference.

### The (b)(10) vs (g)(10) Question

CharmHealth's EHI export page explicitly references the (b)(10) criterion and describes a **combined approach**: FHIR API for clinical data, CSV for billing data. This is **better than many vendors** because:

1. They acknowledge that clinical FHIR data alone is insufficient for EHI export
2. They separately document billing data export via CSV
3. The resource list extends beyond strict US Core (includes Appointment, FamilyMemberHistory, MedicationAdministration, QuestionnaireResponse)

However, the FHIR API portion is essentially the same as what would serve (g)(10) — the 24 resources documented are standard US Core resources plus a few extras. The "EHI-specific" part is the billing CSV export, which is documented only as user guide instructions for running reports from the UI, not as a programmatic bulk export mechanism.

The Bulk Export API appears to export only the 24 FHIR resource types, not billing or other non-clinical data. So the true (b)(10) export for a complete patient record would require:
1. Running a FHIR Bulk Export (or individual patient API calls) for clinical data
2. Manually running multiple billing reports from the UI and exporting as CSV
3. Possibly exporting CCDA for any data not in the FHIR resources

This is not a unified "export all EHI" button — it's a collection of separate mechanisms that together could cover most data.

### Export Format & Standards

- **Clinical data**: FHIR R4.0.1 (JSON), conformant to US Core STU3.1.1 profiles for most resources. The API returns standard FHIR Bundle responses. Bulk export uses NDJSON per the FHIR Bulk Data spec.
- **CCDA**: HL7 CCDA v2.1 XML export for clinical summaries
- **Billing data**: CSV files from the UI (no programmatic API for billing data export)
- **Encounters**: PDF export available from the UI

The FHIR format is appropriate for the clinical data it covers. The CSV billing export is ad-hoc (report-by-report, not a unified schema).

### Documentation Quality

**Strengths:**
- The FHIR API documentation is comprehensive and well-structured — a single-page doc with 24 resources, clear API URLs, parameter tables, request/response examples, and authentication flows
- Sample responses include realistic FHIR JSON with actual field values
- OAuth/SMART documentation is thorough with multiple client types
- The EHI export landing page clearly links to all relevant documentation
- Screenshots show the actual UI export interface

**Weaknesses:**
- No formal data dictionary — the documentation relies on standard FHIR resource definitions without documenting CharmHealth-specific extensions, value sets, or constraints
- No sample export files (no example NDJSON from bulk export, no example CSV billing export)
- Billing export documentation is user-guide-style help pages, not technical specifications — there's no schema for the CSV files, no column definitions, no data type specifications
- No documentation of relationships between the FHIR data and the billing CSV data
- The FHIR API documentation doesn't describe what data from CharmHealth maps to which FHIR fields, making it impossible to know if all stored data is represented

### Structure & Completeness

- **FHIR resources**: Documented at the API operation level (list/get/search) with query parameters, but not at the field level. The actual FHIR resource structure is documented only through sample responses. A developer would need to rely on the US Core profiles and sample responses to understand the data structure.
- **Billing CSV**: No column definitions, no schema, no data types. Only described as "you can export as CSV" in the help pages.
- **Value sets**: Not documented. Standard FHIR/US Core value sets are implicitly used but not enumerated.
- **Relationships**: Not explicitly documented. FHIR resource references (e.g., Encounter referencing Patient) follow standard patterns but aren't called out.
- **No versioning or change history** in the documentation.

Overall, a developer could implement a FHIR API integration to pull clinical data based on this documentation (relying on standard FHIR/US Core knowledge), but could not implement a billing data import without seeing actual CSV export files and reverse-engineering the schema.

## Access Summary
- Final URL: https://www.charmhealth.com/ehr/electronic-health-information-export.html (no redirects)
- Status: found
- Required browser: no (static HTML, all content in page source)
- Navigation complexity: one_click (main page links directly to all documentation)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. All pages loaded cleanly via curl. No authentication required. No JavaScript rendering needed for content (though the FHIR API page uses JS for syntax highlighting and accordion navigation, all content is present in the HTML source). Export screenshot images were served as PNG despite .jpg filenames.
