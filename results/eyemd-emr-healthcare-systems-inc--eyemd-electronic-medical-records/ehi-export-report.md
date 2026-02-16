# EyeMD EMR Healthcare Systems, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.eyemdemr.com/compliance/fhir/
- CHPL IDs: 9988
- Product: EyeMD Electronic Medical Records, Version 2
- Certification date: 2019-05-01

## Navigation Journal

### Step 1: Probe registered URL
```bash
curl -sI -L "https://www.eyemdemr.com/compliance/fhir/" -H 'User-Agent: Mozilla/5.0'
```
The registered URL returns HTTP 301, redirecting from `/compliance/fhir/` to `/fhir/`. The final response is HTTP 200 with `content-type: text/html`.

### Step 2: Examine the FHIR Resource Center page
```bash
curl -sL "https://www.eyemdemr.com/fhir/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```
The page at `/fhir/` is titled "FHIR Resource Center" and is a simple WordPress/Elementor page with three items:
1. **"API Documentation"** — links to `https://fhir.myeyecarerecords.com/api`
2. **"Application Registration Request"** — links to `https://www.eyemdemr.com/fhir-app-registration/`
3. In the footer: **"ONC Costs and Considerations"** — links to `https://www.eyemdemr.com/mandatorydisclosures.pdf`

No mention of EHI, b(10), "electronic health information," bulk export, or data dictionary anywhere on this page.

### Step 3: Follow API Documentation link
```bash
curl -sI -L "https://fhir.myeyecarerecords.com/api" -H 'User-Agent: Mozilla/5.0'
```
The API documentation URL redirects (HTTP 301) to a Postman collection at:
`https://documenter.getpostman.com/view/11861301/TVewYPfd`

This is the main API documentation — a comprehensive Postman collection documenting the EyeMD EMR FHIR API.

### Step 4: Download the Postman collection JSON
```bash
curl -s "https://documenter.gw.postman.com/api/collections/11861301/TVewYPfd?segregateAuth=true&versionTag=latest" \
  -H 'User-Agent: Mozilla/5.0' -H 'Accept: application/json' \
  -o eyemd-fhir-api-postman-collection.json
```
Downloaded the full Postman collection (3.99 MB JSON). This contains the complete API documentation including endpoint definitions, descriptions, parameters, sample requests/responses, USCDI mappings, terms of use, and setup instructions with embedded screenshots.

### Step 5: Download mandatory disclosures PDF
```bash
curl -sL "https://www.eyemdemr.com/mandatorydisclosures.pdf" -H 'User-Agent: Mozilla/5.0' \
  -o mandatorydisclosures.pdf
```
Single-page PDF listing costs for certified capabilities. Mentions `170.315(b)(12,10,11)` as covering "Ability to send CCDA information to other systems via secure transmission" — notably, the mandatory disclosures describe b(10) as CCDA transmission capability, not as a comprehensive EHI export.

### Step 6: Fetch FHIR Endpoints Bundle
```bash
curl -s "https://smartonfhir.myeyecarerecords.com/fhir/Endpoint?_format=application/fhir+json&status=active&_count=1000" \
  -H 'Accept: application/fhir+json' -o fhir-endpoints-bundle.json
```
Successfully retrieved a FHIR Bundle with 37 active endpoints (production customer instances).

### Step 7: Attempt to find FHIR server metadata
Tried multiple paths on `fhir.myeyecarerecords.com` for CapabilityStatement and SMART configuration:
- `/fhir/r4/metadata` → 404
- `/fhir/metadata` → 404
- `/metadata` → 404
- `/.well-known/smart-configuration` → 404
- `/api/*` paths → all redirect to Postman docs

The FHIR server appears to require a customer-specific endpoint identifier (e.g., `smartonfhir.myeyecarerecords.com/fhir/{ENDPOINT_ID}/metadata`), making the metadata endpoint inaccessible without customer credentials.

### Step 8: Search for EHI-specific documentation
- Searched the website text for terms: "ehi", "b(10)", "electronic health information", "bulk", "export", "data dictionary" — **no results** on any page.
- WordPress search (`?s=ehi+export`) returned no results.
- Checked `/mips/` (MACRA/MIPS certification page) — contains RWT test plans but no EHI export documentation.
- Probed common paths: `/ehi/`, `/ehi-export/`, `/b10/`, `/compliance/`, `/interoperability/`, `/onc/`, `/legal/` — all redirect to existing pages or return 302/403.
- `/compliance/` redirects to `/mips/`.
- Checked Wayback Machine for archived versions — no captures found.
- Google site search for "site:eyemdemr.com EHI export b10" — no relevant results.

## What Was Found

EyeMD EMR's registered (b)(10) EHI export URL points to their **FHIR Resource Center**, which in turn links to their **FHIR API documentation** hosted as a Postman collection. There is **no separate (b)(10) EHI export documentation** — the vendor has registered their FHIR API documentation as their EHI export documentation.

### The FHIR API Documentation

The Postman collection is comprehensive as FHIR API documentation goes. It covers:

**FHIR Resources supported (approximately 25 resource types):**
AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, Medication, MedicationRequest, MedicationDispense, Observation, Organization, Patient, Practitioner, Procedure, Provenance, QuestionnaireResponse, RelatedPerson, ServiceRequest, Specimen

**Bulk Data Export:**
There is an "Export" section with two endpoints:
- `GET /Group/{id}/$export` — Start Group Export (FHIR Bulk Data)
- `GET /_operations/export/{id}/{uuid}/{ResourceType}-{n}.ndjson` — Get Export File

These endpoints have no descriptions or documentation beyond the URL patterns. No documentation about what resource types are included in the export, whether it covers all data or just USCDI, or how to interpret the output files.

**USCDI v3 Mappings:**
The documentation includes a complete USCDI v3 mapping table showing how each USCDI data class/element maps to US Core profiles and FHIR resources. This covers the standard clinical data classes: Allergies, Assessment/Plan, Care Team, Clinical Notes, Clinical Tests, Diagnostic Imaging, Encounters, Goals, Health Insurance, Health Status/Assessments, Immunizations, Laboratory, Medications, Patient Demographics, Problems, Procedures, Provenance, Unique Device Identifiers, and Vital Signs.

**CCD Generation:**
There's a `DocumentReference?patient={id}&type=ALLDATA` endpoint that "outputs a CCDA R2 Continuity of Care Document, encoded in base64 format." This appears to be the closest thing to a comprehensive patient data export, but it's a CCD — a clinical summary format — not a complete EHI export.

**Architecture:**
Each EyeMD EMR customer operates in a "partitioned and isolated data environment" with a unique service base URL (e.g., `smartonfhir.myeyecarerecords.com/fhir/{ENDPOINT_ID}`). The system uses a "Fog & Edge Computing" desktop architecture where the EMR runs locally, with a gateway server that connects to the cloud FHIR API. Practices must configure port forwarding and have EyeMD configure the FHIR API server.

**Fees:**
- Patients: Free
- Practices: $300 one-time FHIR setup fee
- Application Vendors: $3,000 one-time registration fee; 300 API requests per endpoint per day limit

## Export Coverage Assessment

### Data Domain Coverage

The product research reveals EyeMD EMR stores a rich set of ophthalmology-specific data across multiple modules. The FHIR API documentation covers only the standard USCDI/US Core clinical data classes. Here is the gap analysis:

**Clearly covered (via FHIR API / USCDI mappings):**
- Patient demographics (standard fields)
- Allergies and intolerances
- Conditions/problems
- Medications (requests and dispense)
- Immunizations
- Lab results and diagnostic reports
- Vital signs
- Procedures
- Care plans and care teams
- Clinical notes (via DocumentReference)
- Encounters
- Health insurance/coverage
- Implantable devices
- Provenance
- Goals
- SDOH assessments (QuestionnaireResponse)
- Related persons

**Clearly missing or undocumented:**
- **Ophthalmic examination data** — slit lamp findings, visual acuity measurements, intraocular pressure (IOP), refraction data, optical mathematical formulas. This is the core clinical data for an ophthalmology EMR and there is no documentation of how it would be exported. These are likely represented as Observations but no ophthalmology-specific coding or mapping is documented.
- **Diagnostic imaging data** — OCT scans, fundus photographs, visual fields, B-scan ultrasound, HRT, ICG/ICGA, autofluorescence images. The product integrates with devices from Zeiss, iCare, iTrace, Heidelberg, Topcon, and Oculus. None of this imaging data appears in the export documentation. DICOM images are not mentioned.
- **Imaging progression/history** — a key clinical feature, not documented for export.
- **Practice management data** — appointment schedules, waitlists, recall lists. Only Encounter is documented, which is a clinical concept, not scheduling.
- **Billing and claims data** — insurance claims, claim tracking, patient financial responsibility, payments, eStatements. The Coverage resource covers insurance information, but actual billing/claims transactions are absent.
- **Optical shop data** — frame/contact lens inventory, optical orders, lab orders, point-of-sale transactions, financial reporting. Entirely absent.
- **Patient engagement data** — digital intake forms, consent documents, two-way messages, appointment reminders, marketing/prequalification data. Only QuestionnaireResponse covers some intake; the rest is absent.
- **E-prescribing details** — while MedicationRequest and MedicationDispense are present, ophthalmology-specific prescriptions (optical Rx transmitted to optical shop) are not distinguished.
- **Surgical documentation** — procedure records exist but specialty surgical documentation (e.g., cataract surgery parameters, IOL calculations) is not specifically addressed.
- **Business intelligence/reporting data** — the product's BI dashboard data is not exportable.
- **Fax records** — the built-in fax system's inbound/outbound records are not mentioned.
- **Audit logs** — not mentioned in the export documentation.
- **Custom templates and clinical verbiage** — the product supports extensive customization, but this configuration data is not exportable.
- **E&M coding data** — automated E&M code suggestions are a product feature but not represented in exports.

### Export Format & Standards

The export uses **FHIR R4** with **US Core v1/STU6.1 profiles** via a **FHIR Bulk Data Export** (`$export`) endpoint producing **NDJSON** files. This is a standard, well-understood format.

However, this is explicitly the **(g)(10) standardized API**, not a purpose-built (b)(10) EHI export. The documentation itself states: "The API meets the requirements of the Standardized API for Patient and Population Services criterion §170.315(g)(10)." There is no mention of §170.315(b)(10) anywhere in any of the documentation.

The FHIR format is appropriate for the USCDI clinical data it covers but is fundamentally inadequate for the ophthalmology-specific data that makes this product unique: high-resolution diagnostic images, complex optical measurements, surgical parameters, and specialty-specific clinical documentation. A FHIR US Core export of an ophthalmology EMR captures the generic clinical layer but misses the specialty-specific layer that constitutes the bulk of the clinical value.

The CCD generation endpoint (`type=ALLDATA`) produces a C-CDA document, which is even more constrained than the FHIR API — it's a clinical summary format, not a comprehensive data export.

### Documentation Quality

The FHIR API documentation is **well-structured and reasonably detailed** as API documentation for a (g)(10) FHIR API:
- Each resource type has search parameters documented with types and descriptions
- There are setup instructions with embedded screenshots
- Authentication (SMART on FHIR / OAuth2) is documented
- Error handling and pagination are explained
- USCDI v3 mapping tables are comprehensive
- Terms of use are thorough

However, as EHI export documentation, it is **fundamentally inadequate**:
- There is no data dictionary — no field-level documentation of what the EMR stores vs. what the API exposes
- There are no value sets or coded field definitions specific to ophthalmology
- The Bulk Data Export endpoints have zero documentation (no descriptions, no example output, no list of included resource types)
- There is no discussion of data completeness or what data is NOT included
- There is no mention of (b)(10), EHI, or "all electronic health information"
- No sample export files or example data

### Structure & Completeness

The documentation is structured as a Postman collection with folders per resource type. Each folder typically contains Search and Get operations with parameter tables. The USCDI mapping section provides a crosswalk from USCDI data classes to FHIR resources.

**What's present:**
- Resource-level documentation (which resources are supported)
- Search parameter tables (parameter name, type, description)
- USCDI v3 to FHIR resource mapping
- Authentication and authorization flow
- Setup instructions for patients, practices, and vendors

**What's absent:**
- No field-level data dictionary (what specific data elements populate each FHIR resource)
- No ophthalmology-specific documentation (how specialty data maps to FHIR)
- No export documentation (what the $export endpoint actually produces)
- No value sets or terminology bindings
- No sample data or example responses for export files
- No documentation of custom FHIR extensions (though the Endpoints bundle shows they use custom extensions like `endpoint-environment` and `emr-version`)
- No versioning or change history for the export

## Overall Assessment

EyeMD EMR has registered their FHIR API documentation — which is clearly their (g)(10) standardized API — as their (b)(10) EHI export documentation. This is a textbook case of the (b)(10) vs. (g)(10) conflation. The documentation explicitly references §170.315(g)(10) and USCDI/US Core, and never mentions (b)(10) or EHI.

For a specialty ophthalmology EMR that stores diagnostic imaging, complex optical measurements, surgical documentation, optical shop inventory, and practice management data, a FHIR US Core API covers perhaps 20-30% of the data the product actually stores. The most clinically and operationally valuable data — the ophthalmology-specific content — has no documented export path.

The FHIR API itself appears functional (37 active production endpoints) and the documentation is adequate for its purpose as a (g)(10) API. But as (b)(10) EHI export documentation, it fails to describe how to export the vast majority of data the system stores.

The mandatory disclosures PDF is particularly telling: it describes capabilities `170.315(b)(12,10,11)` collectively as "Ability to send CCDA information to other systems via secure transmission" — equating the EHI export requirement with CCDA transmission, which is actually the (b)(1) transitions of care capability, not (b)(10).

## Access Summary
- Final URL (after redirects): https://www.eyemdemr.com/fhir/
- API docs URL: https://documenter.getpostman.com/view/11861301/TVewYPfd
- Status: found
- Required browser: no (curl works for all content)
- Navigation complexity: one_click (main page → Postman docs)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The FHIR server at `fhir.myeyecarerecords.com` requires customer-specific endpoint identifiers; standard paths like `/metadata` return 404. Could not retrieve a CapabilityStatement directly.
- The `/compliance/` path redirects to `/mips/`, not to a compliance hub.
- No Wayback Machine captures of the registered URL.
- Website search for "ehi export" returns no results.
- Google site search found no EHI-specific documentation.
