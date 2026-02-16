# myhELO, Inc. — EHI Export Documentation

Collected: 2026-02-15 (updated 2026-02-16)

## Source
- Registered URL: https://www.myhelo.com/api_export_format/
- CHPL IDs: 9930
- CHPL Product Number: 15.05.05.2637.MOXE.01.00.1.190305
- Certification Date: 2019-03-05

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.myhelo.com/api_export_format/" -H 'User-Agent: Mozilla/5.0'` — returned HTTP 200 with `Content-Type: text/html; charset=UTF-8`.

2. **Fetch page source**: `curl -sL "https://www.myhelo.com/api_export_format/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html` — returned only 1153 bytes. Examination revealed an empty `<body>` tag with all content loaded client-side via `/js.php` (a 3.3MB JavaScript bundle called "The Rocket JavaScript library"). This is a Single Page Application — curl cannot render the content.

3. **Browser navigation**: Navigated to `https://www.myhelo.com/api_export_format/` in Chrome. Page rendered successfully showing:
   - Title: "Data Dictionary for myhELO EHI Export"
   - Subtitle: "Ambulatory Clinical EHI Export"
   - Introduction text explaining the EHI export
   - Table listing 17 dataset specifications with links to individual pages

4. **Dataset specification pages**: Each of the 17 links (e.g., `index.php?dataset=AllergyIntolerance`) leads to a detailed FHIR R4 resource definition page with:
   - Resource overview and description
   - US Core profile reference
   - Definitions table (field name, modifier, summary, cardinality, type, description & constraints)
   - Detailed definitions section with per-field descriptions, comments, and requirements

5. **API documentation**: Found a separate "API Docs" link in the footer pointing to `https://www.myhelo.com/api/`. This page (also JS-rendered) contains:
   - API access instructions
   - Terms and conditions
   - Full API reference with read and search endpoints for each resource type
   - Example FHIR JSON responses for every resource type
   - A link to a machine-readable API spec: `https://provider.myhelo.com/fhir/.well-known/fhir.json`

6. **Machine-readable artifacts downloaded**:
   - `curl -sL "https://provider.myhelo.com/fhir/.well-known/fhir.json"` — 98KB JSON file containing the full API specification with example responses (the same data rendered on the API Docs page)
   - `curl -sL "https://provider.myhelo.com/fhir/metadata" -H 'Accept: application/fhir+json'` — FHIR CapabilityStatement (JSON) documenting all supported resources, interactions, and search parameters. Reports FHIR version 4.0.1, software name "myhELO" version 3.14, release date 2022-12-15.

7. **JavaScript bundle data extraction**: Discovered that the 3.3MB `/js.php` bundle embeds all page data as JSON objects within JavaScript prototype methods `get_summary_contents_json()` (overview metadata) and `get_data_json()` (full FHIR StructureDefinitions). Extracted all 17 StructureDefinitions and dataset summaries via regex parsing of the minified JS source. This yielded machine-readable data far richer than the rendered HTML pages.

## What Was Found

### EHI Export Documentation Structure

myhELO provides a dedicated "Data Dictionary for myhELO EHI Export" page at the registered URL. The documentation explicitly uses the term "Electronic Health Information (EHI) Export" and describes an ambulatory clinical data export capability.

**Introduction text** (verbatim): "The Electronic Health Information (EHI) Export for myhELO allows customers in the ambulatory setting to easily export clinical or healthcare data from patient records. Examples of datasets that can be exported are allergies, encounters, lab results, procedures, etc. Customers can choose to export all or selected myhELO EHI datasets for a single patient, multiple patients, or all patients in the practices."

**Key statement**: "For convenience, the export format follows FHIR standards."

### Export Format

The EHI export uses **FHIR R4 JSON** format. The FHIR server is at `https://provider.myhelo.com/fhir` and supports SMART-on-FHIR OAuth2 authentication. The CapabilityStatement confirms:
- FHIR version: 4.0.1
- Format: JSON only
- Authentication: SMART-on-FHIR (authorize, token, revoke endpoints)
- Bulk export: Group/$export endpoint available

### Supported FHIR Resources (17 in EHI Export + 2 additional)

The EHI export data dictionary documents 17 FHIR resource types:

| Resource | US Core Profile | Key Data |
|----------|----------------|----------|
| AllergyIntolerance | US Core AllergyIntolerance | Allergies and intolerances with clinical/verification status, reactions |
| CarePlan | US Core CarePlan | Care plans with status, intent, category, narrative text |
| CareTeam | US Core CareTeam | Care team members with roles |
| Condition | US Core Condition | Diagnoses and conditions with clinical status |
| Device | US Core ImplantableDevice | Implantable devices with UDI carrier info |
| DiagnosticReport | US Core DiagnosticReport | Lab and radiology reports (with PDF attachments) |
| DocumentReference | US Core DocumentReference | Clinical documents (notes, discharge summaries as PDFs) |
| Encounter | US Core Encounter | Visit records with type, period, participants, location |
| Goal | US Core Goal | Patient goals with lifecycle status |
| Immunization | US Core Immunization | Vaccination records with vaccine codes |
| MedicationRequest | US Core MedicationRequest | Medication orders with dosage instructions |
| Observation | US Core Observation | Clinical observations (vitals, social history, labs) |
| Organization | US Core Organization | Practice/facility information |
| Patient | US Core Patient | Demographics, race, ethnicity, birth sex, addresses |
| Practitioner | US Core Practitioner | Provider information with NPI |
| Procedure | US Core Procedure | Procedures with CPT coding |
| Provenance | US Core Provenance | Data provenance (author, transmitter) |

The CapabilityStatement also lists **Group** (for bulk export) and **Location** resources not documented in the EHI data dictionary.

### Field-Level Documentation

Each dataset page provides element-level definitions following the FHIR R4 structure definition pattern:
- **Definitions table**: Field name, modifier flag, summary flag, cardinality, FHIR data type, description with value set bindings
- **Detailed definitions**: Per-element description, cardinality, type, binding (with strength), comments, and requirements
- **USCDI tagging**: Elements marked with "(USCDI)" indicating US Core Data for Interoperability coverage
- **Value set bindings**: Standard FHIR value sets referenced with binding strength (required, extensible, preferred, example)

The v2 enrichment script parsed all 17 StructureDefinitions and found:
- **921 total element definitions** across 17 resources
- **196 elements** flagged as USCDI (via mustSupport)
- **203 elements** with value set bindings
- **105 required elements** (min > 0)

### Example Data

The API documentation provides example FHIR JSON responses for 17 of the 19 resources. Examples include realistic-looking test data (patient "Bob Fhir", practitioner "Joe Provider", organization at "8450 NORTHWEST BLVD, INDIANAPOLIS, IN"). Examples show:
- Coded data using SNOMED CT, LOINC, CPT, CVX, and ICD systems
- References between resources (e.g., Encounter references Patient, Practitioner, Organization)
- PDF document attachments (base64 encoded) for clinical notes and diagnostic reports
- US Core extensions for race, ethnicity, and birth sex on Patient

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered** (documented in EHI export with field-level specs):
- Patient demographics (name, DOB, gender, address, phone, race, ethnicity, birth sex)
- Allergies and intolerances (with reactions and manifestations)
- Problems/conditions (diagnoses with SNOMED coding)
- Medications (prescription orders with dosage)
- Immunizations (vaccine codes, dates, status reasons)
- Vital signs and lab results (via Observation)
- Clinical notes and documents (via DocumentReference, as PDFs)
- Diagnostic reports (lab, radiology, cardiology, pathology — with PDF attachments)
- Procedures (CPT-coded)
- Care plans and goals
- Care team membership
- Encounters (visit records with type, participants, location, reason)
- Implantable devices (UDI carrier info)
- Provider and organization information
- Data provenance tracking

**Missing or not documented** — significant gaps for a product that stores:
- **Billing/financial data**: myhELO has a full RCM module with AI-powered coding, claims, charges, payments, denial management, and insurance verification. None of this appears in the EHI export. There is no Claim, Coverage, ExplanationOfBenefit, or any billing-related resource type.
- **E-prescribing data**: While MedicationRequest covers orders, there is no documentation of prescription fill status, pharmacy information, prior authorization records, or renewal histories.
- **Patient portal/engagement data**: Secure messages, intake form submissions, patient-reported outcomes — none documented in the export.
- **Scheduling data**: Despite myhELO having multi-device scheduling and OR resource management, appointment/scheduling data is absent.
- **Telehealth visit records**: myhELO offers telehealth with video visits, but telehealth-specific data (session records, shared files) is not documented.
- **Surgical templates**: myhELO emphasizes customizable surgical templates for orthopedic procedures — these specialty-specific clinical data structures are not reflected in the export.
- **Medical images**: While DiagnosticReport can include PDF attachments, there's no specific documentation of how the built-in medical image viewing/storage/sharing capability exports image data (DICOM, etc.).

### Export Format & Standards

The export uses **FHIR R4 JSON** following **US Core profiles**. This is a well-structured, standards-based approach. The 17 resource types map directly to the US Core Implementation Guide resource set, which strongly suggests this is a **g(10) FHIR API repackaged as b(10) EHI export documentation**.

Evidence for this assessment:
1. The 17 resource types are exactly the US Core resource set — no more, no less
2. All profiles referenced are standard US Core profiles — no custom profiles or extensions for vendor-specific data
3. The CapabilityStatement shows this is the same FHIR server used for g(10) API access
4. There is a Group/$export endpoint (Bulk Data Access) — this is the g(10) mechanism
5. The API Docs page documents the standard SMART-on-FHIR API — the same endpoint serves both g(10) and is claimed as b(10)
6. No billing data, specialty clinical data, or product-specific data domains are represented — only USCDI clinical data

The vendor's statement that they export data "for convenience" in FHIR format is technically accurate but obscures the gap: FHIR US Core covers the USCDI clinical data subset, not the full designated record set that b(10) requires.

### Documentation Quality

**Strengths**:
- Clean, navigable web-based documentation with a clear index page
- Field-level definitions with cardinality, data types, and value set bindings
- Example FHIR JSON responses for nearly all resources
- Machine-readable CapabilityStatement and API spec available
- USCDI elements explicitly tagged in the definitions
- Full FHIR StructureDefinitions embedded in the JS bundle, providing computable element-level metadata

**Weaknesses**:
- All pages are JavaScript-rendered (SPA) — content is not accessible to screen readers or simple HTTP clients
- No downloadable artifacts (no PDF, no ZIP, no schema files)
- No documentation of the export process itself (how does a user initiate an export? what UI?)
- No documentation of export scope selection (the intro mentions "all or selected datasets" but doesn't explain how)
- No sample export files showing what a complete patient export looks like
- Documentation is entirely FHIR standard boilerplate — there is very little vendor-specific content explaining how myhELO's data maps to these FHIR resources

### Structure & Completeness

- **Granularity**: Field-level definitions with cardinality, types, and bindings — this is detailed
- **Value sets**: Standard FHIR value sets referenced with binding strengths
- **Relationships**: References between resources are documented (e.g., AllergyIntolerance.patient → Patient)
- **Versioning**: CapabilityStatement shows software version 3.14, release date 2022-12-15 — but the data dictionary pages have no visible version or last-updated date
- **Custom data**: No custom extensions, profiles, or vendor-specific elements documented — this raises the question of how product-specific data (surgical templates, billing, RCM) would be exported

### Overall Assessment

myhELO has built a technically competent FHIR R4 API with US Core profile conformance and has presented it as their EHI export mechanism. The documentation is well-organized with field-level definitions and example data. However, **this appears to be their g(10) FHIR API documentation relabeled as b(10) EHI export documentation**. The export covers only the USCDI clinical data subset — approximately the same 17 US Core resource types that every certified EHR must expose via g(10).

For a product that bills itself as a "Healthcare Operating System" with integrated EMR, scheduling, RCM, patient portal, e-prescribing, and telehealth, the absence of billing data, scheduling data, patient engagement data, specialty clinical data (surgical templates), and telehealth records from the EHI export represents a significant coverage gap. The designated record set for myhELO's users (orthopedic practices and ASCs) would include procedure-specific clinical data, surgical planning records, billing/claims data, and patient-reported outcomes — none of which appear in this export.

## Access Summary
- Final URL (after redirects): https://www.myhelo.com/api_export_format/
- Status: found
- Required browser: yes (JavaScript SPA — content not accessible via curl)
- Navigation complexity: direct_link (main page) + one_click (dataset specs)
- Anti-bot issues: none (but JS rendering required)

## Obstacles & Dead Ends
- All pages on myhelo.com are JS-rendered SPAs using a 3.3MB JavaScript library ("Rocket"). The HTML source for every page contains only analytics scripts and an empty `<body>` tag. Browser rendering is required to see any content.
- The FHIR well-known endpoint (`provider.myhelo.com/fhir/.well-known/fhir.json`) returns the full API spec as structured JSON — this was the most valuable machine-readable artifact found.
- No downloadable files (PDF, ZIP, CSV, schema) were found anywhere on the site.
- The API Docs page footer links to the same `/api/` URL as the footer of the EHI export pages, suggesting these are part of the same documentation site.
- All 17 FHIR StructureDefinitions were successfully extracted from the embedded JS bundle data using regex parsing, yielding computable metadata more useful than the rendered HTML pages.
