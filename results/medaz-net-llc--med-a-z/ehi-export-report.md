# MedAZ.Net, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://medaz.com/certificationinfo.html
- CHPL IDs: 11300
- Product: Med A-Z (version 202001)
- Certification date: June 16, 2023

## Navigation Journal

1. **Initial probe** — HTTP HEAD to `https://medaz.com/certificationinfo.html` returned HTTP 200 with Content-Type `text/html`, 15,010 bytes, served by Microsoft-IIS/10.0. Last modified April 24, 2025.

2. **Fetched and examined the page** — Static HTML page with jQuery-loaded header/footer. The page contains certification information, costs, and a "Data Exchange/Extraction" section. No JavaScript SPA, no accordion. All content is in the HTML source.

3. **Found documentation links** — The "Data Exchange/Extraction" section contains:
   - Standards Referenced: links to HL7 standards and HL7 FHIR (external standards — not downloaded)
   - Documentation:
     - Single Patient: `https://fhirapi.mhealthaz.com/swagger/index.html`
     - Bulk exports: `https://fhirbulk.mhealthaz.com/swagger/index.html`
   - FHIR Endpoints:
     - Single Patient: `https://fhir.mhealthaz.com/fhirsingle.xml`
     - Bulk exports: `https://fhir.mhealthaz.com/fhirsystosys.xml`
   - Preferred Formats: QRDA-1, CCD-A

4. **Downloaded FHIR endpoint XMLs** — Both are FHIR Bundles containing Endpoint resources that list the available FHIR resource types and their API URLs.

5. **Fetched OpenAPI/Swagger specs** — The Swagger UI pages are SPAs that load JSON specs. HEAD requests return 405 (the server allows GET but not HEAD for the SPA). Found the underlying OpenAPI 3.0.1 specs at `/swagger/v2/swagger.json`:
   - Single Patient API: 531 KB, titled "Med A-Z FHIR", 90 paths, 106 schema definitions
   - Bulk API: 272 KB, titled "Med A-Z FHIRBulk", 37 paths, 94 schema definitions

6. **Fetched FHIR CapabilityStatements** — Both endpoints return live CapabilityStatements at `/metadata`:
   - Both describe "MEDAZ FHIR for US Core Implementation Guide v3.1.1"
   - FHIR version 4.0.1
   - 20 resource types, all using standard US Core profiles

7. **Searched for additional EHI-specific documentation** — Checked:
   - Site navigation (via `header.html`): No separate EHI export page. Navigation links: Home, About, Products (EHR features, Certification Info, Real World Testing, Billing, Practice Management, Inpatient Management, MED A-Z Complete), Services, Contact.
   - Probed common paths: `/ehi`, `/ehi-export`, `/b10`, `/export`, `/datadictionary`, `/data-dictionary`, `/interoperability` — all returned 404.
   - No robots.txt or sitemap.xml found (both 404).
   - No downloadable PDF, ZIP, CSV, or other documentation files linked from the certification page.

8. **Took screenshots** of the certification page and both Swagger UI pages.

## What Was Found

MedAZ's EHI export documentation consists entirely of their FHIR API documentation. There is no separate (b)(10) EHI export documentation, no data dictionary, no export format specification, and no description of how to export "all electronic health information" from the system.

### The certification page

The page at `certificationinfo.html` is a static HTML page containing:
- Certification disclaimer and basic product info
- Full list of certified criteria (including (b)(10))
- Clinical Quality Measures certified
- Cost disclosures (notably: "Data extraction in custom formats" has fees, but "no fees for extraction in ONC certified formats like QRDA1, CCD, etc.")
- A "Data Exchange/Extraction" section with links to FHIR API documentation

The (b)(10) criterion is listed among the certified criteria but has no dedicated section, no separate documentation, and no description of the EHI export process.

### The FHIR APIs

Two Swagger/OpenAPI documented FHIR APIs:

**Single Patient API** (`fhirapi.mhealthaz.com`):
- 90 API paths covering CRUD operations on FHIR resources
- Standard US Core resource types: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance
- Application registration/consent management endpoints (`/myapplication/*`)
- Search, pagination, and history endpoints for each resource

**Bulk Export API** (`fhirbulk.mhealthaz.com`):
- 37 API paths
- Group-level export via `/Group/{id}/$export`
- Export poll status, download, and content location endpoints
- Same resource types as single patient API
- Appears to implement the FHIR Bulk Data Access specification

### FHIR Endpoint XML files

Both `fhirsingle.xml` and `fhirsystosys.xml` are FHIR Bundle resources containing Endpoint entries. Each Endpoint lists one resource type and its API URL. Both files list the same 19 resource types (same as the CapabilityStatement minus PractitionerRole). These are essentially service discovery documents for the FHIR APIs. Last modified September 21, 2022.

### CapabilityStatements

Both APIs return live CapabilityStatements describing US Core Implementation Guide v3.1.1 compliance with FHIR R4 (4.0.1). All 20 resource types use standard US Core profiles. No custom profiles or extensions are defined.

## Export Coverage Assessment

### Data Domain Coverage

This is a textbook case of (b)(10)/(g)(10) conflation. The vendor's "EHI export" documentation points exclusively to their FHIR APIs, which implement the US Core/USCDI data set — the same API that satisfies (g)(10). There is no evidence of a separate mechanism to export all electronic health information stored in the system.

**Clearly covered** (via US Core FHIR resources):
- Patient demographics
- Allergies
- Conditions/problems
- Medications (MedicationRequest)
- Immunizations
- Lab results (DiagnosticReport, Observation)
- Vital signs (Observation)
- Procedures
- Care plans and care teams
- Goals
- Encounters
- Implantable devices
- Clinical notes (DocumentReference)
- Provenance

**Clearly missing** — based on the product research, Med A-Z stores significant data categories with no apparent export mechanism:
- **Billing and claims data** — The product has an integrated "Billing Plus" module with claims, HCFA forms, payment processing, revenue cycle data. None of this appears in the FHIR API.
- **Scheduling/appointment data** — "Practice Plus" includes patient scheduling. No Schedule or Appointment FHIR resources.
- **Insurance information** — Unlimited insurance plan configuration is a feature. No Coverage or InsurancePlan resources.
- **Drug interaction alerts and clinical decision support data** — The product checks drug-drug, drug-allergy, and drug-procedure interactions. These alerts/records are not in the export.
- **E-prescribing transaction history** — Surescripts integration data beyond what's in MedicationRequest.
- **Lab interface data** — HL7 interface data with Quest/LabCorp beyond what's represented in DiagnosticReport.
- **Audit logs** — The product is certified for (d)(2) auditable events and (d)(10) auditing actions. Audit data is not available via the FHIR API.
- **Patient education materials** — Tracked and logged per the EHR features, not in the export.
- **Clinical quality measures data** — CQM recording/reporting is certified but not represented in the FHIR API.
- **Referral correspondence** — Referral letter preparation is a feature, not in the export.
- **Office workflow/patient tracking data** — Real-time floor plan, check-in/checkout status tracking.
- **Cardiovascular risk assessments** — Framingham calculations, not in the export.
- **Coding data** — Under/over-coding detection, procedure-diagnosis linking beyond standard resources.
- **HCFA forms** — Generated billing forms.

The export covers approximately the standard USCDI clinical data — roughly 30-40% of the data domains the product actually manages. The entire administrative, financial, and operational layer is absent.

### Export Format & Standards

- **Format**: FHIR R4 (4.0.1), US Core Implementation Guide v3.1.1
- **Standard**: Fully standardized — this is the (g)(10) API, not a custom EHI export
- **Resources**: 20 standard US Core resource types, no custom profiles or extensions
- **Bulk mechanism**: FHIR Bulk Data Access (Group-level $export) with poll/download endpoints
- **Single patient**: Standard FHIR RESTful API with search and pagination

The format is appropriate for the clinical data it covers, but it is structurally incapable of representing the billing, scheduling, insurance, and administrative data that constitutes a large portion of what this integrated EHR/PM/Billing product stores. A FHIR US Core API can never satisfy (b)(10) for a product that stores billing data, scheduling data, and practice management data — those data domains don't map to US Core resources.

### Documentation Quality

- **Readability**: The Swagger/OpenAPI documentation is machine-generated and functional. The API endpoints are clearly listed with parameters and response schemas.
- **Data dictionary**: None. There is no field-level data dictionary for the export. The FHIR resource definitions serve as implicit documentation for the clinical data structure, but only by reference to external FHIR specifications.
- **Data types and value sets**: Inherited from US Core profiles, not documented locally.
- **Examples**: No sample data or example export files are provided.
- **Import feasibility**: A developer could implement a FHIR client to consume this API based on the Swagger docs combined with standard FHIR/US Core knowledge. However, they would only receive the clinical subset of data.
- **Maintenance**: The FHIR endpoint XML files were last modified September 2022. The certification page was last modified April 2025. The CapabilityStatements appear to be generated live.

The documentation is minimal — it's an API specification, not export documentation. There are no instructions for initiating an EHI export, no description of what data is included, no explanation of how this satisfies (b)(10), and no acknowledgment that the product stores data beyond what the FHIR API exposes.

### Structure & Completeness

- **Granularity**: Resource-level only (via FHIR resource types). No field-level documentation specific to this vendor's implementation.
- **Value sets**: Not documented; relies entirely on US Core defaults.
- **Relationships**: Expressed through standard FHIR references. No documentation of vendor-specific data relationships.
- **Versioning**: The OpenAPI spec is "v2", CapabilityStatement version is "202001.001". No change history.

### Overall Assessment

MedAZ has pointed their (b)(10) EHI export certification to their (g)(10) FHIR API. This is a common pattern among smaller EHR vendors who may not fully understand the distinction between the two requirements. The FHIR API is functional and reasonably well-documented via Swagger, but it covers only the standardized US Core clinical data subset.

For a product that explicitly markets itself as an integrated EHR + Practice Management + Billing suite, the absence of any mechanism to export billing data, scheduling data, insurance information, and other administrative records is a significant gap. The costs section on the certification page mentions "Data extraction in custom formats" as a paid service, which hints that the vendor may have internal capabilities to extract more data — but this is not documented as part of the EHI export, and it suggests that accessing the full EHI may require a fee, which is relevant to the (b)(10) requirement that export be available at no charge.

## Access Summary
- Final URL (after redirects): https://medaz.com/certificationinfo.html
- Status: found
- Required browser: no (for main page; Swagger UI is SPA but OpenAPI JSON specs are directly downloadable)
- Navigation complexity: direct_link (all documentation links are on the single certification page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- Swagger UI pages return HTTP 405 for HEAD requests (the server rejects HEAD but accepts GET) — not a real obstacle, just unusual
- No robots.txt or sitemap.xml
- No separate EHI export documentation exists anywhere on the site
- The `/swagger/v1/swagger.json` path returns 0 bytes; the actual specs are at `/swagger/v2/swagger.json`
