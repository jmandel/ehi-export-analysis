# PCE Systems — EHI Export Documentation

Collected: 2025-07-14

## Source
- Registered URL: https://www.pcesystems.com/g10APIInfo.html
- CHPL ID: 11045
- Product: PCE Care Management v9.4
- Developer: PCE Systems (Farmington Hills, MI)

## Navigation Journal

The registered URL is a simple static HTML page that loaded immediately without JavaScript.

```bash
# 1. Probe the URL
curl -sI -L "https://www.pcesystems.com/g10APIInfo.html" -H 'User-Agent: Mozilla/5.0'
# → HTTP 200, Content-Type: text/html, 2268 bytes

# 2. Fetch and examine
curl -sL "https://www.pcesystems.com/g10APIInfo.html" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```

The page titled "PCE Care Management Version 9.4 - API and EHI Export Information" contains:
- Base URLs for the (g)(10) FHIR API (test and production endpoints at w3.pcesecure.com)
- A link to the API documentation PDF
- A link to the EHI Export (b)(10) documentation PDF

Both links are clearly labeled and directly downloadable:

```bash
# 3. Download the EHI Export (b)(10) documentation
curl -L -H 'User-Agent: Mozilla/5.0' -o b10_documentation.pdf 'https://www.pcesystems.com/b10_documentation.pdf'
# → 889,642 bytes, PDF document, 3 pages

# 4. Download the API documentation (includes data element definitions)
curl -L -H 'User-Agent: Mozilla/5.0' -o PIX_9_4_API_Documentation.pdf 'https://www.pcesystems.com/PIX_9_4_API_Documentation.pdf'
# → 1,888,837 bytes, PDF document, 87 pages

# 5. Download the FHIR CapabilityStatement (machine-readable)
curl -s -H 'User-Agent: Mozilla/5.0' -H 'Accept: application/json' \
  'https://w3.pcesecure.com/cgi-bin/WebObjects/HIEAdmin.woa/MUPIX/v2/Capability' \
  -o capability-statement.json
# → 42,557 bytes, valid JSON
```

## What Was Found

### EHI Export (b)(10) Documentation — 3 pages

The b(10) documentation is a concise 3-page PDF (dated November 20, 2023) describing the export format at a structural level. Key details:

**Export mechanism:** The export is initiated by "authorized EHR users" and can export data per patient or for all patients. This is a purpose-built export function, not a repurposed FHIR Bulk Data endpoint.

**Export format:** Password-protected ZIP files containing:
1. `meta.json` — metadata about the export process (who ran it, when)
2. `documentation.json` — a self-describing JSON schema containing all resource definitions, property names, data types, and descriptions
3. `Patient_[EHRPatientId]/` subdirectories — one per patient, each containing:
   - NDJSON files for each resource type (one file per resource, only present when data exists)
   - A `Files/` subdirectory with non-computable files (scanned documents, PDFs, etc.)

**Data types supported:** CLOB, DATE, DECIMAL, INTEGER, RESOURCE (cross-references between resources), STRING, TIMESTAMP.

**Critical design decision:** The actual data dictionary — the list of resources and their fields — is **not** in the public documentation. It's embedded in the `documentation.json` file within the export ZIP itself. The public documentation describes the *format* of the schema but not the *content*. This means the specific resources, field names, and data types are only knowable by performing an actual export.

The documentation explicitly mentions cross-references between resources via the RESOURCE data type (which contains a `resource` name and `id` for linking), and file references via `fileName` or `imageName` properties that map to files in the `Files/` subdirectory.

### API Documentation — 87 pages

The API documentation (updated April 23, 2025) covers the (g)(10) FHIR API. While this is not the (b)(10) export, it provides the only publicly visible enumeration of data elements PCE stores. The API exposes these FHIR resources:

- AllergyIntolerance, CarePlan, CareTeam, Claim, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, HealthcareService, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance

Plus a "Message" data element listed separately.

The Data Elements section (pages 65-78) provides field-level definitions for each resource: attribute name, data type, and description. These conform to US Core profiles.

Notably, the API also includes **Claim** and **Coverage** resources, which go beyond the standard USCDI v1 data classes — suggesting PCE does store and expose billing/insurance data.

### FHIR CapabilityStatement (machine-readable)

The production CapabilityStatement at the live endpoint confirms the same resource set. It declares conformance to US Core Server and FHIR Bulk Data CapabilityStatements.

## Export Coverage Assessment

### Data Domain Coverage

This is where PCE's approach has a fundamental gap. The (b)(10) documentation describes the export *container format* but deliberately defers the data dictionary to the export artifact itself (`documentation.json`). This makes a public coverage assessment nearly impossible.

**What we can infer from the FHIR API (which is the (g)(10) system, not (b)(10)):**

The API covers standard USCDI v1 clinical data classes plus Claims and Coverage. However, the product research reveals PCE Care Management stores significantly more:

**Likely covered (based on FHIR API resources):**
- Patient demographics
- Allergies and intolerances
- Conditions/problems
- Medications
- Immunizations
- Procedures
- Vital signs, lab results, smoking status
- Clinical notes and documents (including scanned files)
- Care plans and care teams
- Goals
- Encounters
- Claims and insurance coverage
- Provider/organization/location data

**Likely missing or uncertain (based on product research):**
- **Treatment plans** — behavioral health-specific individualized treatment plans (beyond the FHIR CarePlan structure)
- **Clinical assessments** — MichiCANS and other structured assessment instruments that are core to behavioral health practice
- **Intake and discharge records** — formal admission/discharge documentation
- **Incident reports** — required by CMH agencies for safety reporting
- **Consent directives** — the eConsent Management System for 42 CFR Part 2 and Michigan Mental Health Code, which is a major feature of the system
- **PIX/HIE exchange records** — cross-agency data sharing logs
- **Audit logs** — system access and activity logs
- **Scheduling/appointments** — referenced in the ONC Brightspot case study
- **Messages** — the API docs mention a Message data element but it's not in the FHIR CapabilityStatement
- **Social service referrals** — PCE signed MiHIN's Interoperable Referrals Pledge
- **Authorization/prior-auth workflows** — expected for Medicaid behavioral health services

The key uncertainty is: **we don't know if the (b)(10) export includes all of these**. The export documentation says the `documentation.json` file contains "a list of all possible resource definitions" — the word "all" is encouraging, but without seeing the actual file, we can't verify this. The (b)(10) export could export far more than the FHIR API exposes, or it could be essentially the same set.

The explicit inclusion of a `Files/` subdirectory for non-computable content (scanned documents, PDFs) is a positive sign — it shows PCE thought about data that doesn't fit into structured NDJSON.

### Export Format & Standards

PCE has made a **good design choice** for (b)(10): they use their own structured format (NDJSON in ZIP files with a self-describing JSON schema) rather than repurposing their FHIR API. This is appropriate because:

- The FHIR API is constrained to US Core profiles, which can't represent behavioral health-specific data
- A vendor-native format can include every table and field in the system
- NDJSON is computable and processable
- The self-describing `documentation.json` schema means the export is self-documenting
- Cross-references between resources are supported via the RESOURCE type
- Non-computable files are included in a separate directory

The format is not a recognized standard, but it's well-designed for its purpose. A developer could parse the NDJSON files using the schema definitions in `documentation.json` and reconstruct relationships between entities.

### Documentation Quality

This is where PCE falls short. The public documentation is:

- **3 pages** describing only the container format
- **No data dictionary** — no enumeration of resources, fields, types, or descriptions
- **No sample data** — no example `documentation.json` or sample NDJSON records
- **No user guide** — no instructions for how to initiate the export, who can run it, or how long it takes
- **No screenshots** of the export interface

The documentation essentially says "the export is a ZIP file with NDJSON and a schema — run it and find out what's in it." This is a self-describing format, which has technical merit, but it means a third party cannot evaluate the export's completeness without actually running it.

The API documentation (87 pages) is substantially better — it has field-level definitions, data types, descriptions, and instructions. But that's (g)(10), not (b)(10).

### Structure & Completeness

The *format specification* is complete: data types, directory structure, file naming, cross-reference mechanism, and non-computable file handling are all documented.

The *content specification* is entirely absent from public documentation. There are:
- No resource names listed
- No field definitions
- No value sets or coded field documentation
- No relationship diagrams
- No change history beyond the single revision date

PCE's approach — embedding the schema in the export itself — is technically sound (it means the schema always matches the data), but it fails the transparency test. A patient, provider, or third-party developer cannot assess what the export contains without having an export in hand.

### Overall Assessment

PCE Systems has built a **thoughtful (b)(10) export mechanism** — a self-describing, structured format with NDJSON, cross-references, and non-computable file support. This is better engineering than many vendors who simply repackage their FHIR Bulk Data API.

However, the **public documentation is minimal to the point of opacity**. Three pages describing only the container format, with zero enumeration of what data is actually exported. The self-describing nature of `documentation.json` is a partial mitigation (the schema travels with the data), but it doesn't help anyone evaluate coverage before performing an export.

The vendor clearly understands the distinction between (b)(10) and (g)(10) — they have separate documentation and separate mechanisms. But the (b)(10) documentation needs substantial expansion: a public data dictionary (even a summary), sample files, and user instructions would transform it from a format spec into actual export documentation.

## Access Summary
- Final URL (after redirects): https://www.pcesystems.com/g10APIInfo.html (no redirects)
- Status: found
- Required browser: no
- Navigation complexity: direct_link (two clearly labeled PDF links on the landing page)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The page loaded cleanly, both PDFs downloaded without issues, and the FHIR CapabilityStatement was publicly accessible. The only obstacle is the deliberate decision to not publish the data dictionary publicly — it's embedded in the export artifact itself.
