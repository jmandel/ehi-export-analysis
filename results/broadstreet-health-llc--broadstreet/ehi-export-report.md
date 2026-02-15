# BroadStreet Health LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://broadstreetcare.com/docs/ehi-export
- CHPL ID: 11410 (15.05.05.3161.BRDS.01.00.1.231222)
- Product: BroadStreet, Version 1
- Certification date: 2023-12-22

## Navigation Journal

1. **Initial probe of registered URL:**
   ```bash
   curl -sI -L "https://broadstreetcare.com/docs/ehi-export" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html, 4194 bytes. The page is a SvelteKit single-page application — the server-rendered HTML contains only a spinner placeholder; actual content loads via JavaScript.

2. **Browser navigation:** Navigated to `https://broadstreetcare.com/docs/ehi-export` in Chrome. The page rendered with full content after JS hydration. The page title is "BroadStreet - EHI Export." Took a full-page screenshot (`ehi-export-page.png`).

3. **Content extraction:** Used browser DevTools `evaluate_script` to extract the rendered `<article class="md">` innerHTML. Saved as `ehi-export-page-rendered.html`.

4. **Sidebar navigation:** The docs site has a sidebar with these sections:
   - Overview
   - FHIR (expandable, with sub-pages: Overview, Resources → 23 individual resource pages)
   - Secure Health Transport
   - **EHI Export** (current page)
   - QRDA
   - Patient and Population Health
   - Automated Measure Calculations
   - NTP Synchronization
   - Terms of Use

5. **FHIR resource documentation:** Examined the FHIR section by fetching the JS chunks directly:
   - `/_app/immutable/chunks/md.ab4e7ff9.js` — the doc tree builder, listing all markdown pages
   - `/_app/immutable/chunks/index.0e3af201.js` — FHIR Resources index page
   - `/_app/immutable/chunks/Patient.900354e1.js` — Patient resource page
   - `/_app/immutable/chunks/Observation.9cbebfd7.js` — Observation resource page
   - `/_app/immutable/chunks/Condition.a25fff12.js` — Condition resource page
   - `/_app/immutable/chunks/overview.3159c741.js` — FHIR Overview/API integration page

   The FHIR resource pages are **standard (g)(10) FHIR API documentation** — each page lists US Core profiles, search parameters, CRUD endpoints at `https://portal.broadstreetcare.com/api/fhir/[type]/[id]`, and HTTP error codes. These are not (b)(10)-specific export documentation. Took screenshot of the resources index (`fhir-resources-page.png`).

6. **FHIR Resources listed:**
   - Clinical Information: AllergyIntolerance, CarePlan, CareTeam, Condition, DiagnosticReport, Encounter, Goal, Immunization, Medication, MedicationRequest, Observation, Procedure
   - Resources and References: DocumentReference, Device, Location, Organization, Patient, Practitioner, PractitionerRole, Provenance, QuestionnaireResponse, RelatedPerson, ServiceRequest

7. **Mandatory disclosures page:** Fetched `https://broadstreetcare.com/onc-health-it-certification`. Contains the certified criteria table (confirms (b)(10) certification), CQMs, additional software note (EMR Direct), and a Real World Testing section linking to a 2025 RWT Plan PDF.

8. **RWT Plan PDF:** Downloaded from:
   ```bash
   curl -sL "https://broadstreetcare.com/documents/BST%202025%20RWT%20Plan%20SLI%20ONC_Final.pdf" -H 'User-Agent: Mozilla/5.0' -o BST-2025-RWT-Plan.pdf
   ```
   15 pages, authored by Laura Ivanoski, created 2024-11-27. Contains Test Case 4 specifically for (b)(10) EHI Export.

## What Was Found

The EHI export documentation page describes three export formats:

### 1. CDA 2.1 (Clinical Document Architecture)
A general description of the CDA 2.1 standard — structured documents with headers (patient, author, document type metadata) and bodies (clinical sections with entries for diagnoses, observations, medications). The page states: "Our system exports patient data in the form of CDA documents that adhere to the CDA 2.1 standard." Links to external HL7 CDA documentation. No BroadStreet-specific CDA template, profile, or section list is provided.

### 2. FHIR R4
A general description of the FHIR R4 standard with a list of resource types: Patient, Observation, Medication, Practitioner, Encounter, Procedure, Condition, Immunization, AllergyIntolerance, MedicationRequest, CarePlan, Device, DiagnosticReport, Appointment, Organization. The page states: "When exporting data in FHIR format, our system provides a bundle of FHIR resources." Links to external HL7 FHIR R4 documentation. No BroadStreet-specific FHIR profiles, extensions, or bundle structure is documented.

The separate FHIR docs section (`/docs/fhir/`) provides per-resource API documentation with US Core STU 5.0.1 profiles, search parameters, and REST endpoints at `portal.broadstreetcare.com/api/fhir/`. This is clearly (g)(10) standardized API documentation, not (b)(10) bulk export documentation.

### 3. BroadStreet Notes (HTML)
The most specific section: describes the structure of clinical notes exported as HTML. Fields documented:
- **Physician Information:** Physician Name, Sent by, Date
- **Visit and Patient Details:** Date of Service, Type (e.g., H&P), Patient Name, Date of Birth, Gender, Advance Directive Code
- **Medical Concerns:** Allergies, Primary Concern
- **Social History:** Smoking Status
- **Treatment Review:** (described as "typically include past and ongoing treatments")
- **Vital Examination:** Blood Pressure, Pulse, Weight
- **Assessment Plan:** Diagnosis Code (ICD), Assessment
- **Visit Details:** Next Appointment, Reason for Next Visit
- **Additional Notes:** Physician remarks
- **Signature:** Electronically Signed By

This is the only BroadStreet-specific data structure documentation on the page.

### RWT Plan (b)(10) Test Case
The 2025 Real World Testing Plan includes Test Case 4 for (b)(10), which describes:
- Testing in a production environment at an assisted living facility
- Tracking frequency and completion times of export requests via logs
- Both individual and population-level EHI exports
- Compatibility verification by importing exported data into external systems
- Expected outcome: "consistently generate and export EHI for both individual patients and populations, ensuring the data is complete, accurate, and properly formatted"

The RWT Plan mentions the system supports "multiple specialties across Post Acute, Long Term Care, and community-based settings."

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation is remarkably thin on specifics about what data domains are actually included in the export. Here is the assessment against what's known about the product:

**Domains apparently covered (based on FHIR resource list and Notes structure):**
- Patient demographics
- Conditions/problems
- Medications (Medication, MedicationRequest)
- Allergies (AllergyIntolerance)
- Immunizations
- Observations (vitals, labs, social history, SDOH)
- Procedures
- Encounters
- Care plans and goals
- Care teams
- Diagnostic reports
- Devices (implantable)
- Clinical notes (via HTML export)
- Documents (DocumentReference)
- Appointments
- Service requests (orders)
- Questionnaire responses

**Domains with no mention or documentation:**
- **Billing and claims data** — completely absent. No mention of charges, payments, claims, or billing codes anywhere in the export documentation. The product research suggests billing may be handled externally, but this is not clarified.
- **Medication administration records (eMAR)** — not mentioned, despite being critical for post-acute care settings where medication administration tracking is a core workflow.
- **Nursing assessments (MDS, OASIS)** — not documented, despite being fundamental to the post-acute care workflow. MDS assessments are mandatory for SNF residents.
- **Family health history** — certified for (a)(12) but not listed in FHIR resources or EHI export documentation.
- **Clinical quality measure data** — certified for CQMs but no mention in the export.
- **Scheduling data** — Appointment is listed on the EHI export page's FHIR resources list but not in the actual FHIR API resources page, suggesting inconsistency.

### Export Format & Standards

The export uses three formats:
1. **CDA 2.1** — a recognized standard, but no BroadStreet-specific template or section list is provided. It's impossible to tell which CDA sections are populated or how complete the document is.
2. **FHIR R4** — a recognized standard using US Core STU 5.0.1 profiles. The resource list is essentially the standard US Core set. This strongly suggests the FHIR export is the same as the (g)(10) API — covering USCDI data classes, not all EHI.
3. **HTML Notes** — a proprietary format for clinical notes with a defined field structure.

**The (b)(10) vs (g)(10) confusion is present here.** The FHIR resource list on the EHI export page maps closely to the standard US Core resource set. The separate FHIR API documentation confirms these are the same resources served by the (g)(10) endpoint at `portal.broadstreetcare.com/api/fhir/`. The documentation does not describe how the EHI export goes beyond what the (g)(10) API provides. There is no mention of exporting data that doesn't fit into FHIR US Core — no billing data, no specialty-specific post-acute care assessments, no custom data structures.

The CDA export likely produces C-CDA documents (given the (b)(1) Transitions of Care certification and SVAP update to C-CDA R2.1 Companion Guide Release 3), which would cover a similar scope to the FHIR resources — standard clinical summaries, not comprehensive EHI.

### Documentation Quality

**Very poor.** The EHI export page is largely a textbook description of the CDA and FHIR standards themselves, not documentation of BroadStreet's specific implementation. Key deficiencies:

- **No data dictionary** — no table/field definitions, no schema, no column listings
- **No export format specification** — no description of the actual file structure, bundle format, or packaging of the export
- **No export instructions** — no user guide for performing an export (how to trigger it, what options are available, what files are produced)
- **No sample data or examples** — no example export files, sample records, or test data
- **No machine-readable artifacts** — no JSON Schema, XSD, OpenAPI spec, or any other computable format description
- **No value set or coded field documentation** — coded fields like diagnosis codes are mentioned but value sets are not specified
- **No relationship documentation** — how entities relate to each other in the export is not described

The BroadStreet Notes (HTML) section is the only part that documents BroadStreet-specific data structure, and even that is a simple field list without data types, constraints, or examples.

The FHIR resource documentation in the separate `/docs/fhir/` section is more structured (with search parameters, profiles, and endpoints), but this is (g)(10) API documentation, not (b)(10) export documentation.

### Structure & Completeness

- **Granularity:** The EHI export page provides resource-level descriptions only (e.g., "Patient: Information about an individual receiving care"). No field-level detail for the FHIR or CDA formats. The Notes HTML section provides field-level names but no data types or constraints.
- **Coded fields:** Diagnosis Code is described as "ICD code" — no further specification of code systems, value sets, or terminology mappings.
- **Relationships:** Not documented at all.
- **Versioning:** No version history or change tracking.

## Overall Assessment

BroadStreet's EHI export documentation reads as a minimal compliance checkbox rather than a genuine attempt to document how their system exports all electronic health information. The page primarily restates general descriptions of the CDA and FHIR standards, with almost no BroadStreet-specific implementation detail. The export appears to conflate (b)(10) with (g)(10) — the FHIR resource list is the standard US Core set, and the FHIR API documentation confirms these are served via the same standardized API endpoint.

For a post-acute care EHR that should store nursing assessments (MDS), medication administration records, and other specialty-specific clinical data, the documented export covers only the standard USCDI clinical summary — a significant gap. The only genuinely (b)(10)-specific artifact is the HTML Notes export structure, which describes a clinical note format but not comprehensive EHI.

The RWT Plan at least confirms that EHI export is being tested in production environments with real data at assisted living facilities, but the test case description is similarly vague about what data is actually exported.

This is consistent with the profile of an early-stage startup (1-10 employees) with limited deployment — the product may have a functional export, but the documentation does not adequately describe it.

## Access Summary
- Final URL (after redirects): https://broadstreetcare.com/docs/ehi-export
- Status: found
- Required browser: yes (SvelteKit SPA — content loads via JavaScript, server-rendered HTML is a spinner)
- Navigation complexity: direct_link (content is on the registered URL, rendered after JS hydration)
- Anti-bot issues: none (standard User-Agent sufficient for curl; browser needed for rendered content)

## Obstacles & Dead Ends
- The SvelteKit SPA required browser-based rendering — curl returns only the app shell with a spinner placeholder. Content was extracted via Chrome DevTools `evaluate_script`.
- No downloadable files (PDF, ZIP, CSV, JSON, etc.) were linked from the EHI export page itself.
- The FHIR resource documentation is (g)(10) API docs, not (b)(10) export docs — this was confirmed by examining the JS chunks and the rendered pages showing US Core profiles and REST API endpoints.
