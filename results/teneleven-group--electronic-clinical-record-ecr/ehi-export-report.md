# TenEleven Group — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://ensorahealth.com/onc/teneleven/
- CHPL ID: 11200
- Product: electronic Clinical Record (eCR) v2.4
- Certification date: 2022-12-31
- Developer: TenEleven Group (now part of Ensora Health / Therapy Brands)

## Navigation Journal

1. **Probed the registered URL:**
   ```bash
   curl -sI -L "https://ensorahealth.com/onc/teneleven/" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200 with `text/html` content. The page is a WordPress site hosted on Cloudflare (Kinsta).

2. **Fetched and examined the page (82KB HTML):**
   ```bash
   curl -sL "https://ensorahealth.com/onc/teneleven/" -H 'User-Agent: Mozilla/5.0' -o /tmp/teneleven-page.html
   ```
   The page is the ONC certification disclosure page for TenEleven by Ensora Health. It contains:
   - Certification details (developer name, product name, version, address, contact info)
   - An "Attestation Disclosure" section listing costs and criteria
   - An **"Electronic Health Information (EHI) Export"** section with two export types described
   - A "File Formats" button linking to a PDF
   - A "FHIR Endpoints" section with three links to fhir.10e11.com
   - An "ONC Real World Testing" section (not relevant to EHI export)

3. **Downloaded the File Formats PDF:**
   ```bash
   curl -sL "https://ensorahealth.com/wp-content/uploads/2025/03/PDF-for-Website-on-Formats-2.pdf" -o downloads/PDF-for-Website-on-Formats-2.pdf
   ```
   Confirmed: 1-page PDF document, 115,988 bytes, created 2023-11-30 by Catherine Baker in Microsoft Word.

4. **Examined the FHIR API documentation site:**
   ```bash
   curl -sL "https://fhir.10e11.com/electronicclinicalrecord/basepractice/r4/Home/ApiDocumentation" -o /tmp/fhir-10e11-api.html
   ```
   A large (687KB) single-page documentation site covering FHIR API terms of use, client registration, client configuration, FHIR API mapping (USCDI-to-resource table), API URLs, methods, parameters, responses, errors, and Bulk Export.

5. **Fetched the FHIR CapabilityStatement:**
   ```bash
   curl -sL "https://fhir.10e11.com/fhir/electronicclinicalrecord/basepractice/r4/metadata" -H 'Accept: application/fhir+json'
   ```
   Confirmed supported FHIR R4 resources: Group, AllergyIntolerance, DocumentReference, CarePlan, CareTeam, Device, Binary, DiagnosticReport, Goal, Immunization, MedicationRequest, Location, Organization, Patient, Condition, Procedure, Practitioner, PractitionerRole, Encounter, ClinicalImpression, Observation, Provenance. All profiled to US Core.

6. **Fetched the endpoints list:**
   ```bash
   curl -sL "https://fhir.10e11.com/fhir/r4/endpoints" -H 'Accept: application/json'
   ```
   Returns a FHIR Bundle of Endpoint resources (5 endpoints for different agencies).

7. **Took screenshots** of the ONC disclosure page (top and EHI section) and the FHIR API documentation page.

## What Was Found

### EHI Export Description (from the disclosure page)

The page describes two export mechanisms:

1. **Single Patient Export**: Users can export EHI for a single patient "without developer assistance" using "standardized file formats."

2. **Patient Population Export**: eCR can export "all the data for a patient population." This export is requested by submitting a support ticket via Salesforce (i.e., it is not self-service).

The page includes a standard disclaimer that export content may vary based on software applications in use, software version, documentation practices, configuration decisions, and whether the health system included materials not sourced from the application.

### File Formats PDF (1-page document)

The PDF titled "Electronic Health Information (EHI) Export — File Formats" describes:

- **Single Patient: JSON** — "JavaScript Object Notation. JSON is a lightweight format for storing and transporting data. JSON is in plain text, which is readable by a person, but is meant to be parsed and understood by an application or web page. The data includes USCDI v1 data as well as other applicable data."

- **Patient Population: .bak file** — "This is a full SQL Server database backup of all data for an agency that can be restored."

That's it. The entire documentation is a single page with two bullet points. No data dictionary, no schema, no field definitions, no sample data, no instructions for interpreting the export.

### FHIR API Documentation

The FHIR API docs at fhir.10e11.com are a standard (g)(10) SMART on FHIR API documentation. Key details:
- Maps FHIR resources to USCDI v1 data classes
- Explicitly states: "Available data via the API interface is limited by the data defined by the USCDI"
- References §170.315(g)(7), (g)(9), and (g)(10) — not (b)(10)
- Supports Bulk Data export via Patient/$export and Group/$export
- All resources use US Core profiles
- USCDI categories covered: Patient Demographics, Problem List, Procedures, Smoking Status, Vital Signs, Laboratory Results/Tests, Medications, Allergies, Immunizations, Goals, Clinical Notes, Assessment/Plan, Care Plans, Care Teams, Implantable Devices, Encounters, Provenance

## Export Coverage Assessment

### Data Domain Coverage

The single patient export says "USCDI v1 data as well as other applicable data" — but there is no documentation of what "other applicable data" means. The phrase is tantalizingly vague. USCDI v1 covers a narrow subset of what this product stores.

The population export (.bak file) is described as "a full SQL Server database backup of all data for an agency" — this is actually the most honest and complete approach to (b)(10) possible. A SQL Server backup would contain everything: all clinical data, billing records, custom forms, MAT dosing data, bed management records, scheduling, and any other data in the system. However, there is **zero documentation** of the database schema. Without a data dictionary, a recipient of a .bak file would need to reverse-engineer the entire database to understand the data.

**Domains from product research vs. export coverage:**

| Data Domain | Single Patient (JSON) | Population (.bak) | Documented? |
|---|---|---|---|
| Demographics | Likely (USCDI) | Yes (full DB) | No schema |
| Diagnoses/Problems (DSM-5) | Likely (USCDI) | Yes (full DB) | No schema |
| Medications/MAT dosing | Partial (USCDI) | Yes (full DB) | No schema |
| Lab results | Likely (USCDI) | Yes (full DB) | No schema |
| Vital signs | Likely (USCDI) | Yes (full DB) | No schema |
| Allergies | Likely (USCDI) | Yes (full DB) | No schema |
| Immunizations | Likely (USCDI) | Yes (full DB) | No schema |
| Clinical notes/progress notes | Likely (USCDI) | Yes (full DB) | No schema |
| Treatment plans/goals | Likely (USCDI) | Yes (full DB) | No schema |
| Procedures | Likely (USCDI) | Yes (full DB) | No schema |
| Encounters | Likely (USCDI) | Yes (full DB) | No schema |
| **Billing/claims** | **Unknown** | Yes (full DB) | No schema |
| **Custom forms (FormLab)** | **Unknown** | Yes (full DB) | No schema |
| **Scheduling** | **Unknown** | Yes (full DB) | No schema |
| **Bed management** | **Unknown** | Yes (full DB) | No schema |
| **MAT-specific** (dosing, tapering, dispensing) | **Unknown** | Yes (full DB) | No schema |
| **Intake/referral** | **Unknown** | Yes (full DB) | No schema |
| **E-prescribing** | Partial (USCDI) | Yes (full DB) | No schema |

The single patient export is ambiguous — "USCDI v1 + other applicable data" could mean anything. The population export (.bak) should contain everything but is entirely undocumented.

### Export Format & Standards

**Single patient**: JSON format, described as including USCDI v1 data. The relationship to the FHIR API is unclear — it might be FHIR JSON (given the FHIR infrastructure), or it might be a proprietary JSON format. The documentation doesn't specify the schema, structure, or whether it's FHIR-compliant.

**Population**: SQL Server .bak file. This is a raw database backup — the most complete possible export format, but also the least portable. It requires Microsoft SQL Server to restore. There is no schema documentation, no entity-relationship documentation, and no guidance on how to interpret the tables.

The .bak approach is actually a reasonable (b)(10) strategy — it guarantees completeness — but its value is severely diminished by the complete absence of documentation.

### Documentation Quality

**Extremely poor.** The entire EHI export documentation is:
- One paragraph on the disclosure page describing two export modes
- One 1-page PDF with two bullet points describing the file formats

There is no:
- Data dictionary or schema documentation
- Field-level definitions
- Table/entity descriptions for the .bak file
- Sample data or example exports
- Instructions for performing the single patient export
- Instructions for restoring or interpreting the .bak file
- Mapping between the JSON export structure and the data it contains
- Documentation of how "other applicable data" beyond USCDI is structured
- Value sets or coded field documentation

A developer receiving either export format would have no way to programmatically parse or understand the data without reverse engineering it.

### Structure & Completeness

The documentation has essentially no structure. It is two sentences describing two file formats. There is no granularity — no tables, no fields, no data types, no relationships, no constraints, no value sets, no versioning, no change history.

The FHIR API documentation (at fhir.10e11.com) is substantially more detailed, with a full USCDI-to-FHIR resource mapping table, sample responses, and API usage instructions. But this documents the (g)(10) API, not the (b)(10) export. The disclosure page's EHI section and the FHIR section are presented as separate items — the FHIR endpoints are listed after the EHI export section under a separate heading.

### The (b)(10) vs (g)(10) Picture

This vendor has an interesting split:
- The **single patient** JSON export claims to include "USCDI v1 data as well as other applicable data" — potentially more than just (g)(10), but the extra coverage is entirely undocumented.
- The **population** export is a full SQL Server database backup — this is genuinely (b)(10) complete, covering everything in the database. But with no schema documentation, the completeness is theoretical rather than practical.
- The **FHIR API** is clearly (g)(10) and explicitly limited to USCDI data.

The vendor appears to understand the distinction between (b)(10) and (g)(10) — the .bak approach for population export is deliberately broader than the FHIR API. But the documentation of the (b)(10) mechanism is perfunctory to the point of being nearly useless.

### Notable Findings

1. **Population export requires a support ticket** — it cannot be self-initiated by the user, which adds a process barrier to what should be a straightforward export.
2. **The .bak format requires SQL Server** — a proprietary Microsoft product — to restore. This is a significant practical barrier for data portability.
3. **No documentation of behavioral-health-specific data** — for a product whose key differentiator is MAT, FormLab custom forms, bed management, and behavioral health workflows, the export documentation says nothing about how this specialty data is exported.
4. The FHIR API is branded "Therapy Brands" (the parent company's former name), suggesting shared infrastructure across the Ensora Health product portfolio.

## Access Summary
- Final URL (after redirects): https://ensorahealth.com/onc/teneleven/
- Status: found
- Required browser: no (all content accessible via curl; screenshots taken via browser)
- Navigation complexity: one_click (PDF linked from "File Formats" button)
- Anti-bot issues: none (Cloudflare present but not blocking)

## Obstacles & Dead Ends
- None significant. The page loaded cleanly, the PDF downloaded without issue, and the FHIR API documentation site was accessible. The problem is not access — it's that the documentation is extremely thin.
