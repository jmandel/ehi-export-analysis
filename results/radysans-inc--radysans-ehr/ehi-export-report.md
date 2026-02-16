# Radysans, Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: http://radysans.com/Radysans/ONCcertification.html
- CHPL IDs: 10253
- Product: Radysans EHR v5.0
- Certification date: 2019-12-31

## Navigation Journal

1. Probed the registered URL with curl:
   ```bash
   curl -sI -L "http://radysans.com/Radysans/ONCcertification.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: text/html, 17,123 bytes. Server: Microsoft-IIS/10.0. No redirects.

2. Fetched and examined the full HTML page. It is a static HTML certification page with table-based layout (very old-school web design, Dreamweaver-era). The page contains:
   - Certification boilerplate text
   - Links to Mandatory Disclosure Statement PDF
   - Links to Real World Test Plans/Results (2022–2025)
   - **A direct link to the (b)(10) EHI Export document**: `images/B-10-Documentation.pdf`
   - FHIR API documentation (g)(10) terms and conditions PDF
   - FHIR endpoint bundle link

3. Downloaded the (b)(10) document:
   ```bash
   curl -sL "http://radysans.com/Radysans/images/B-10-Documentation.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/B-10-Documentation.pdf
   ```
   Verified: PDF document, version 1.7, 1 page, 61,032 bytes.

4. Downloaded the (g)(10) API documentation (for reference, since the b(10) doc references it):
   ```bash
   curl -sL "http://radysans.com/Radysans/images/G10ApplicationAccessTermsandCondition.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/G10ApplicationAccessTermsandCondition.pdf
   ```
   Verified: PDF document, version 1.6, 311,460 bytes.

5. Downloaded the Mandatory Disclosure Statement:
   ```bash
   curl -sL "http://radysans.com/Radysans/images/RadysansEHRCostsandLimitations.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/RadysansEHRCostsandLimitations.pdf
   ```
   Verified: PDF document, version 1.7, 2 pages, 581,581 bytes.

6. Fetched the FHIR endpoint bundle:
   ```bash
   curl -sL "https://ehrwebapi.cutecharts.com/radywebapi/endpoint" -H 'Accept: application/fhir+json' -o downloads/fhir-endpoint-bundle.json
   ```
   Verified: Valid FHIR Bundle JSON containing one Endpoint resource and one Organization resource.

7. Took a full-page screenshot of the certification page via browser.

## What Was Found

### The (b)(10) Document: B-10-Documentation.pdf

This is a single-page PDF titled "Documentation for Export of Electronic Health Information — 170.315(b)(10) Electronic Health Information Export." It describes two export formats:

**1. C-CDA Export**
The product supports "bulk export of HL7 CCDA xml files which comply to United States Core Data for Interoperability (USCDI), Version 1 requirements." The document lists 22 C-CDA sections exported:
- Allergies, Adverse Reactions, Alerts
- Assessment Plan
- Chief Complaint
- Cognitive Status
- Demographics
- Reason for Visit / Encounters
- Family History
- Functional Status
- Goals
- Health Concerns
- Immunizations
- Instructions
- Lab Results
- Medical Equipment UDI
- Medications
- Plan of Care
- Problem List
- Procedures
- Reason for Referral
- Social History
- Plan of Treatment
- Vitals

The document references the HL7 C-CDA specification for format details.

**2. FHIR Export**
The document states: "Radysans EHR also supports HL7® Version 4.0.1 FHIR® Release 4, October 30, 2019, FHIR® US Core Implementation Guide STU V3.1.1, HL7 FHIR Bulk Data export." It then directs the reader to the 170.315(g)(10) documentation for details.

### The (g)(10) API Documentation: G10ApplicationAccessTermsandCondition.pdf

This is a detailed (~20+ pages) PDF documenting the FHIR R4 API. It covers:
- OAuth 2.0 authorization flow (PKCE-based)
- Token endpoints
- All supported FHIR resources with URLs, parameters, and sample JSON responses:
  - AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance

The API base URL is `https://ehrwebapi.cutecharts.com/radywebapi/`. Sample outputs show US Core-profiled FHIR resources with coded data (SNOMED, LOINC, RxNorm).

### Mandatory Disclosure Statement: RadysansEHRCostsandLimitations.pdf

Relevant finding: Under "Data Portability" it states: "This capability will allow extraction of data" with a cost of "One-time fee per provider upon request of data extraction." This confirms there is a fee for EHI export.

### FHIR Endpoint Bundle

A valid FHIR Bundle containing a single Endpoint resource pointing to `https://ehrwebapi.cutecharts.com/radywebapi` and an Organization resource for Radysans Inc.

## Export Coverage Assessment

### Data Domain Coverage

The (b)(10) export documentation is a textbook example of the (b)(10)/(g)(10) conflation problem. The vendor describes their EHI export as consisting of two mechanisms — C-CDA documents and FHIR Bulk Data — both of which are standards-based clinical data exchange formats that cover only the USCDI/US Core data classes.

**Clearly covered (via C-CDA + FHIR):**
- Patient demographics
- Problems/conditions
- Medications
- Allergies
- Lab results (via DiagnosticReport, Observation)
- Vital signs
- Immunizations
- Procedures
- Encounters
- Care plans and care teams
- Goals
- Social history
- Family history
- Medical devices/UDI
- Clinical notes (via DocumentReference)
- Provenance

**Missing or not mentioned — based on product research:**
- **Billing/claims data**: The product has a full eBilling module with charge capture, claim scrubbing, electronic claims submission, denial tracking, EOB/ERA processing, payment posting. None of this appears in the export.
- **Appointment/scheduling data**: The PMS module includes enterprise scheduling across multiple locations and providers. Not in the export.
- **Patient registration data**: Scanned documents (photos, insurance cards, regulatory documents). Not in the export.
- **Referral and pre-authorization records**: The product has referral management. The C-CDA has a "Reason for Referral" section, but this is the clinical reason, not the administrative referral tracking data.
- **Audit trails**: The product's security page mentions audit trails with user identification, date/time stamps. Not in the export.
- **Message/task routing data**: The "Message Manager" workflow/task routing module data is absent.
- **Business intelligence/reports**: KPI data, no-show/cancellation tracking, user productivity metrics — none exported.
- **Transcription records**: The product offers transcription services with long-term storage. Not in the export.
- **Insurance eligibility data**: Captured by the PMS. Not exported.
- **Patient portal activity data**: Login records, patient representative access. Not exported.
- **Clinical decision support configurations**: Alert settings, order sets, protocols. Not exported.

The export covers roughly the USCDI v1 clinical data subset — perhaps 30-40% of what the product actually stores. The administrative, financial, and operational data that makes up a significant portion of the system's data holdings is entirely absent.

### Export Format & Standards

The export uses two standard clinical data formats:
- **C-CDA** (HL7 Consolidated Clinical Document Architecture) — XML documents per patient with 22 sections
- **FHIR R4** with US Core STU 3.1.1 profiles — 18 resource types via Bulk Data API

Both are well-recognized interoperability standards, but they are designed for clinical data exchange, not comprehensive data export. Neither format has a natural way to represent billing claims, appointment schedules, audit logs, insurance eligibility records, or most administrative data.

The FHIR resource types map exactly to the US Core required resources — this is the (g)(10) certified API being repurposed as the (b)(10) export mechanism. There are no custom FHIR profiles, no extensions for vendor-specific data, and no non-US-Core resources.

A third party could reconstruct the clinical summary from this export, but could not reconstruct the full patient record including billing history, appointment history, referrals, or administrative data.

### Documentation Quality

**The (b)(10) document itself is minimal** — a single page listing C-CDA sections and a pointer to the FHIR API docs. There is no data dictionary, no field-level documentation, no schema beyond "C-CDA" and "FHIR US Core."

**The (g)(10) API document is more detailed** — it includes endpoint URLs, parameter lists, and full sample JSON responses for each FHIR resource type. A developer could use this to implement a FHIR client. However, this is (g)(10) documentation, not (b)(10)-specific documentation.

There are no:
- Worked examples of the C-CDA bulk export process
- Instructions for how to initiate or receive the export
- Data dictionaries mapping internal fields to export fields
- Sample export files
- Schema files (no XSD for C-CDA output, no FHIR StructureDefinitions)
- Documentation of what data is NOT included in the export

The mandatory disclosure statement mentions a "one-time fee per provider upon request of data extraction" for Data Portability, which suggests the export may be a manual/on-request process rather than a self-service feature.

### Structure & Completeness

The documentation is extremely thin for a (b)(10) compliance artifact:
- **Granularity**: Section/resource names only. No field-level documentation for the C-CDA export. The FHIR documentation shows sample outputs which implicitly document field structure, but only via examples, not formal definitions.
- **Value sets**: Not documented beyond what's visible in FHIR sample data (standard terminologies: SNOMED, LOINC, RxNorm, CVX).
- **Relationships**: Not explicitly documented. The FHIR resources contain references to each other (e.g., Encounter references in MedicationRequest), following standard FHIR patterns.
- **Versioning**: The document references "Radysans EHR v 5.0" and was created November 27, 2023 (per PDF metadata). No change history.

This looks like a compliance checkbox rather than a genuine effort to document comprehensive EHI export. The vendor has certified their existing C-CDA and FHIR capabilities as the (b)(10) mechanism, which satisfies the letter of having "export documentation" but falls far short of covering all electronic health information the system stores.

## Access Summary
- Final URL (after redirects): https://radysans.com/Radysans/ONCcertification.html
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (PDF linked directly from certification page)
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The page loaded cleanly, all PDF links worked, and the FHIR endpoint responded with valid JSON. The main issue is not accessibility but substance — the documentation is minimal and doesn't address comprehensive EHI export.
