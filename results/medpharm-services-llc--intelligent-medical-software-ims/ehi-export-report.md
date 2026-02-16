# MedPharm Services LLC (Meditab) — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.meditab.com/company/ehi-export
- Final URL (after redirects): https://www.meditab.com/company/ehi-export (no redirect)
- CHPL IDs: 9739
- Product: Intelligent Medical Software (IMS), Version 14.0 SP 1
- Certification date: 2018-11-13

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.meditab.com/company/ehi-export" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200, content-type `text/html;charset=utf-8`. No redirect.

2. **Page fetch**: `curl -sL "https://www.meditab.com/company/ehi-export" -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html` — 325 KB file. However, the page is built with Duda website builder and renders entirely client-side via JavaScript. Static HTML has no visible text content.

3. **Browser rendering**: Navigated to URL in Chrome via DevTools MCP. Page loaded successfully. Took accessibility snapshot revealing the full page content. The page is a single-screen document with heading "EHI Export" and subtitle "170.315(b)(10) Electronic Health Information Export".

4. **Page content (from browser snapshot)**: The page describes two export formats — C-CDA and FHIR. For C-CDA, it lists 19 data sections. For FHIR, it links to an internal specifications page at `https://www.meditab.com/fhir/specifications` and references HL7 FHIR R4, US Core STU 3.1.1, and FHIR Bulk Data STU 1.0.1.

5. **FHIR Specifications page**: Navigated to `https://www.meditab.com/fhir/specifications`. This is a large single-page document (3.3 MB HTML, 125 tables, 218 headings) titled "Meditab FHIR API Specification Overview." It documents 16 FHIR resource types with field-level detail, search parameters, and response codes. Also rendered as a Duda SPA — required browser-based extraction.

6. **Screenshot capture**: Full-page screenshot of the EHI export page saved. Viewport screenshot of the FHIR specifications page saved.

7. **Structured extraction**: Used Chrome DevTools `evaluate_script` to extract all table data from the FHIR specifications page, producing structured JSON with 16 resources and 131 deduplicated fields. Saved to enrichment directory with extraction script and README.

8. **No downloadable files found**: Neither page offers PDF, ZIP, CSV, JSON schema, or any other downloadable documentation files. All content exists only as rendered web pages. No download buttons, no "Export data dictionary" links.

## What Was Found

### EHI Export Page Content

The registered URL is a brief single-page description of Meditab's EHI export capability. The entirety of substantive content is:

**C-CDA Format:** IMS supports bulk export of HL7 C-CDA XML files compliant with USCDI v1. The page lists 19 C-CDA sections included in the export:
- Assessment, Clinical Notes, Durable Medical Equipment, Encounters, Family History, Functional Status, Goals, Health Concerns, Immunization, Laboratory Values/Results, Medications, Medication Allergies, Payer, Plan of Treatment, Problems, Procedures, Reason for Referral, Smoking Status and Tobacco Use, Vital Signs

**FHIR Format:** IMS also supports FHIR R4 (v4.0.1), US Core STU 3.1.1, and FHIR Bulk Data export STU 1.0.1. The page directs to their FHIR API specifications at `https://www.meditab.com/fhir/specifications` and states: "For detailed specifications, please refer to 170.315(g)(10) for the Standardized API for patient and population services."

This last sentence is telling — the vendor explicitly labels the FHIR documentation as their g(10) certification, not their b(10) export.

### FHIR Specifications Page Content

The FHIR specifications page is a comprehensive FHIR API reference documenting 16 standard US Core resource types:

1. AllergyIntolerance (6 fields)
2. Patient (13 fields)
3. Encounter (10 fields)
4. Immunization (11 fields)
5. Goal (7 fields)
6. Condition (8 fields)
7. Organization (7 fields)
8. MedicationRequest (12 fields)
9. Provenance (4 fields)
10. Procedure (6 fields)
11. Device (11 fields)
12. Practitioner (6 fields)
13. CarePlan (7 fields)
14. CareTeam (6 fields)
15. Observation (7 fields)
16. DiagnosticReport (10 fields)

Each resource has:
- A description paragraph
- Read interaction (by resource ID) with request/response structure
- Search interaction with query parameters
- Resource content table (field name, data type, description, required/optional)
- Standard HTTP response codes

The documentation is moderately detailed at the field level but purely describes standard FHIR US Core resources. There are no custom profiles, no IMS-specific extensions, no vendor-proprietary resource types, and no documentation of data outside the US Core resource set.

### What is NOT Present

- **No data dictionary** for the IMS database (Sybase SQL Anywhere)
- **No documentation of billing data export** — no claims, charges, payments, superbills
- **No specialty-specific clinical data** — despite IMS supporting 40+ specialties with dedicated modules, the export documentation makes no mention of specialty-specific templates, custom forms, or clinical assessments
- **No documentation of e-prescribing data, prescription history, or PDMP data**
- **No documentation of referral/authorization data**
- **No documentation of document/image export**
- **No documentation of patient portal data, secure messages, or telemedicine records**
- **No sample data or example export files**
- **No schema files** (XSD, JSON Schema, OpenAPI spec)
- **No user guide or instructions** for actually performing the export
- **No mention of export format beyond C-CDA sections and FHIR resources**

## Export Coverage Assessment

### Data Domain Coverage

IMS is a comprehensive all-in-one EHR with integrated practice management, billing, e-prescribing, patient portal, and 40+ specialty modules, all running on a single Sybase SQL Anywhere database. The EHI export documentation covers only a fraction of what the product stores:

**Clearly covered (via C-CDA sections + FHIR resources):**
- Demographics (Patient)
- Allergies (AllergyIntolerance)
- Conditions/Problems (Condition)
- Medications/Prescriptions (MedicationRequest)
- Immunizations (Immunization)
- Lab results and diagnostic reports (Observation, DiagnosticReport)
- Vital signs (Observation)
- Procedures (Procedure)
- Encounters (Encounter)
- Care plans and care teams (CarePlan, CareTeam)
- Goals (Goal)
- Clinical notes (via C-CDA "Clinical Notes" section)
- Family history (via C-CDA "Family History" section)
- Smoking status (via C-CDA section)
- Insurance/Payer info (via C-CDA "Payer" section — FHIR does not include Coverage or payer resources)

**Clearly missing (data IMS stores but the export does not document):**
- **Billing and revenue cycle data**: Claims, charges, superbills, payment records, denial management, insurance posting — IMS is described as "a biller's dream" by users and has deep billing functionality. No billing data appears in the export.
- **Specialty-specific clinical data**: IMS supports 40+ specialties with dedicated modules (CosmetiSuite, FertilityEHR, dental charts, behavioral health assessments, oncology protocols, etc.). None of this specialty data appears in the export — only generic US Core clinical resources.
- **E-prescribing data**: Full prescription history, EPCS data, prior authorization status, drug interaction alerts, PDMP queries. Only basic MedicationRequest is exported.
- **Referral and authorization management**: IMS has referral tracking and authorization management. Not in the export.
- **Documents and images**: IMS has document management with imaging capabilities. The C-CDA has no "Documents" section; FHIR has DocumentReference but only with basic metadata.
- **Patient portal data**: Secure messages, portal activity, medication refill requests, uploaded documents.
- **Telemedicine/Televisit records**: IMS has built-in telemedicine. Not in the export.
- **Quality/reporting data**: MIPS/MACRA, HEDIS, UDS, HCC coding data.
- **Patient communications**: InTouch messaging, fax communications.

**Ambiguous:**
- **Durable medical equipment**: Listed as a C-CDA section but unclear what data is included beyond basic DME orders.
- **Functional status and health concerns**: C-CDA sections listed but no field-level detail.

### Export Format & Standards

The export uses two standard formats:
1. **HL7 C-CDA XML** — compliant with USCDI v1. This is a patient summary format, not a bulk data format. C-CDA is inherently limited to clinical summary data classes.
2. **FHIR R4** via Bulk Data export — 16 US Core resource types. This is explicitly their g(10) FHIR API, repackaged as the b(10) export.

Neither format is capable of carrying the full breadth of data IMS stores. C-CDA is a clinical summary standard — it has no representation for billing records, specialty-specific assessments, custom forms, or operational data. FHIR US Core is similarly limited to standard clinical data classes.

The vendor has not described any proprietary export format (CSV dump, SQL export, etc.) that would cover data outside these standard formats. This is a classic example of the b(10)/g(10) conflation described in the ONC requirements: the vendor is presenting their standardized FHIR API (designed for the g(10) criterion) as their complete EHI export mechanism.

### Documentation Quality

**Poor.** The EHI export page is a single screen with a bulleted list of C-CDA sections and a link to the FHIR API docs. There is:
- No data dictionary mapping IMS data to export fields
- No instructions for performing an export
- No sample data or examples
- No schema files (XSD, OpenAPI, JSON Schema)
- No documentation of how C-CDA bulk export actually works (API? UI button? Batch job?)
- No mention of export file naming, packaging, or delivery mechanism
- No discussion of what happens to data that doesn't fit into C-CDA or FHIR
- No versioning or change history

The FHIR specifications page is more detailed (125 tables documenting field-level structure for 16 resources) but is standard US Core API documentation — it tells you the shape of FHIR resources, not what IMS-specific data populates them or how IMS maps its internal data model to these resources.

A developer trying to import data from an IMS EHI export would have:
- A list of 19 C-CDA section names with no field-level detail
- 16 FHIR resource schemas that are essentially standard US Core with no IMS customization
- No understanding of how billing, specialty, or operational data is exported (or whether it is)
- No way to know what data they're NOT getting

### Structure & Completeness

- **Field-level documentation**: Moderate for FHIR (data types and descriptions for each field). Absent for C-CDA (only section names listed).
- **Value sets**: Not documented. The FHIR specs reference standard value sets (SNOMED, LOINC, RxNorm) but don't enumerate specific IMS-supported values.
- **Relationships**: Basic FHIR references (subject → Patient, encounter → Encounter) but no entity-relationship documentation.
- **Versioning**: None apparent. Publication date in page source is January 2026.

## Access Summary
- Final URL (after redirects): https://www.meditab.com/company/ehi-export
- Status: found
- Required browser: yes (Duda SPA, no static content)
- Navigation complexity: one_click (main page + one link to FHIR specs)
- Anti-bot issues: none (page loads fine with standard User-Agent)

## Obstacles & Dead Ends

1. **SPA rendering**: Both pages are built with Duda website builder and render entirely via JavaScript. `curl` retrieves only the JavaScript shell with no visible content. Browser automation was required to extract page content.

2. **No downloadable files**: Neither page offers any downloadable artifacts (PDF, ZIP, CSV, etc.). All documentation exists only as rendered web pages.

3. **Large FHIR specs page**: The FHIR specifications page is 3.3 MB of HTML with 125 tables. Browser snapshot exceeded tool limits (438K characters). Required JavaScript evaluation to extract structured data.

4. **No C-CDA detail**: The C-CDA sections are listed by name only — no field-level documentation, no sample C-CDA documents, no CDA template references. There is no way to assess what data actually populates each section without access to a real export.
