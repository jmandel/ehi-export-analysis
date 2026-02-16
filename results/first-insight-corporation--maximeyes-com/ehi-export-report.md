# First Insight Corporation — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://customer.first-insight.com/downloads/forms/MaximEyes-EHI-Export-Documentation.pdf
- CHPL IDs: 10470
- Product: MaximEyes.com v1.1
- Certification date: 2020-10-14

## Navigation Journal

1. **Probed the registered URL** with a HEAD request:
   ```bash
   curl -sI -L "https://customer.first-insight.com/downloads/forms/MaximEyes-EHI-Export-Documentation.pdf" -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
   ```
   Returned HTTP 200 with `Content-Type: application/pdf`, 293,314 bytes. Direct PDF download — no redirects, no auth wall, no SPA needed.

2. **Downloaded the EHI Export Documentation PDF** (4 pages, created 2025-03-17):
   ```bash
   curl -sL "https://customer.first-insight.com/downloads/forms/MaximEyes-EHI-Export-Documentation.pdf" -o downloads/MaximEyes-EHI-Export-Documentation.pdf
   ```

3. **Extracted text and inspected** with `pdftotext`. The PDF contains export instructions, screenshots of the EHI export interface in MaximEyes.com, API parameters for the bulk export endpoint, query parameters (`_since`, `_type`), the "Scope of EHI" list, and two follow-on links for format details.

4. **Page 4 "Scope of EHI" lists these data categories:**
   - Patient Demographic, Social History, Problems, Medications, Allergies and Reactions, Diagnostic Results, Vital signs, Encounter Diagnoses, Procedures, Care team members, Immunizations, Assessment and plan of treatment, Goals, Insurance Providers, Accounts

5. **Followed the two referenced links** from the EHI export PDF:
   - `https://customer.first-insight.com/downloads/forms/MaximEyes-FHIR-APIDocumentation.pdf` — **404 Not Found** (the URL in the PDF text had a line-break artifact that dropped the hyphen between "API" and "Documentation").
   - Corrected URL: `https://customer.first-insight.com/downloads/forms/MaximEyes-FHIR-API-Documentation.pdf` — **200 OK**, 572,084 bytes, PDF (40 pages, created 2025-03-17). Downloaded.
   - `https://fhir.maximeyes.com/index.html` — **200 OK**, 1,456 bytes, Swagger UI page. It loads the OpenAPI spec from `/swagger/v1/swagger.json`.

6. **Downloaded the OpenAPI/Swagger spec**:
   ```bash
   curl -sL "https://fhir.maximeyes.com/swagger/v1/swagger.json" -o downloads/swagger-v1.json
   ```
   Valid JSON, 447,712 bytes. Contains the full OpenAPI 3.0.1 specification for the MaximEyes FHIR API.

7. **Examined the FHIR API Documentation PDF** (40 pages). It documents SMART on FHIR authorization workflows (patient apps, provider apps, system/backend apps), all supported FHIR R4 resource endpoints, search parameters, scopes, PKCE support, and base URLs. Each FHIR resource section maps to USCDI data classes.

8. **Examined the Swagger JSON** for the full list of API endpoints. Found these FHIR resource types exposed:
   - Standard US Core: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance
   - **Beyond US Core** (present in Swagger but not documented in the FHIR API PDF): **Account**, **ChargeItem**, **Coverage**
   - Export-specific endpoints: Patient/Export, Export (system-level), Group/{Id}/$export, Status, Download

## What Was Found

The EHI export documentation consists of three artifacts:

### 1. EHI Export Documentation PDF (4 pages)
A brief document that describes how to perform the export. Key points:
- The export uses **FHIR R4 NDJSON** format via the FHIR Bulk Data API
- It supports **single-patient** and **all-patient** exports
- Users navigate to **Reports → Incentive Programs → Electronic Health Information** in MaximEyes.com
- Includes screenshots of the EHI export UI showing patient selection, encounter filtering, and Schedule/Download buttons
- Files are downloaded as a ZIP containing NDJSON files named `PatientID_Date_ResourceType`
- The programmatic export uses `GET /api/{customerName}/R4/Patient/Export` with JWK token authentication
- Query parameters: `_since` (incremental export), `_type` (resource type filter)
- **Scope of EHI** is listed as 15 categories (see above)

### 2. FHIR API Documentation PDF (40 pages)
The comprehensive FHIR API reference covering:
- SMART App Launch 1.0.0 / OAuth 2.0 / Bulk Data 1.0.1 authorization
- Three auth flows: Patient App, Provider App, System/Backend App
- Base URLs: `https://FHIRDEHR.maximeyes.com` (desktop EHR), `https://fhirwehr.maximeyes.com` (cloud)
- 21 supported FHIR R4 resource types with search parameters
- Supported scopes at patient/user/system levels
- PKCE support (S256)
- All resources map to USCDI v3.1.1 data classes

### 3. OpenAPI/Swagger Specification (JSON)
A machine-readable OpenAPI 3.0.1 spec with full endpoint definitions. Notably includes three resource types (**Account**, **ChargeItem**, **Coverage**) not documented in the PDF, which are billing-related resources that go beyond standard US Core.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export's "Scope of EHI" (page 4 of the EHI export PDF) lists 15 data categories. The Swagger API additionally exposes Account, ChargeItem, and Coverage resources, bringing the total to roughly 18 resource types. Here is the assessment against the product research:

**Clearly covered:**
- Patient demographics (Patient resource)
- Problems/diagnoses (Condition)
- Medications and prescriptions (MedicationRequest, Medication)
- Allergies (AllergyIntolerance)
- Vital signs (Observation — vital-signs category)
- Lab results / diagnostic results (Observation — laboratory, DiagnosticReport)
- Immunizations (Immunization)
- Procedures (Procedure)
- Clinical notes (DocumentReference — Consultation, Discharge Summary, H&P, Progress Notes)
- Care plans / assessment and plan of treatment (CarePlan)
- Goals (Goal)
- Care team members (CareTeam)
- Encounter information (Encounter)
- Implantable devices (Device — for IOLs)
- Insurance providers (Coverage, Organization)
- Accounts (Account — billing accounts)
- Charge items (ChargeItem — individual billing charges)

**Missing or not mentioned — significant gaps:**
- **Structured ophthalmic/optometric exam data**: MaximEyes is an eye care-specific EHR that stores detailed structured findings (visual acuity, intraocular pressure, slit lamp, fundus exam, refraction, etc.). There is no indication these specialty-specific structured clinical fields are exported. They would not map neatly to standard FHIR US Core resources. They might be partially captured in DocumentReference as clinical notes, but the structured data itself appears absent.
- **Optical retail / point-of-sale data**: Frame orders, contact lens orders, lab orders, spectacle prescriptions, inventory data — a major module of MaximEyes with patient-relevant data. Not mentioned.
- **Eyeglass and contact lens prescriptions (Rx, CLX scripts)**: These are clinical documents specific to eye care. Not covered.
- **Diagnostic images**: OCT scans, fundus photographs, visual field results — the product stores these in cloud storage. The export mentions DocumentReference (which could reference images) but there's no explicit discussion of image export or how binary attachments are handled.
- **E-prescribing history**: The product integrates with DrFirst Rcopia for e-prescribing. MedicationRequest captures some of this, but the full prescription workflow data may not be included.
- **Patient portal activity / secure messages**: EyeClinic.net portal data is not mentioned in the export scope.
- **Referral data**: Not explicitly mentioned.
- **Scanned documents / intake forms**: Not explicitly mentioned beyond clinical notes in DocumentReference.
- **Family health history**: Listed as a certified criteria (a)(12) but not in the "Scope of EHI" list on page 4 and not visible as a distinct export resource.
- **Social history**: Listed in the Scope of EHI but the FHIR API documentation only covers Smoking Status as a social history element. The product may store more detailed social/ocular history.
- **Claims and ERA/EOB data**: The Account and ChargeItem resources are a start, but the full billing cycle (claims submissions, ERA/EOB auto-posting, accounts receivable) may not be fully captured.

### Export Format & Standards

The export uses **FHIR R4 NDJSON** via the **Bulk Data 1.0.1** protocol. This is a standard, well-documented format. FHIR resources conform to **US Core 3.1.1** profiles.

The format choice has a critical consequence for this product: **FHIR US Core was designed for general clinical data, not specialty ophthalmology/optometry data.** There are no standard FHIR profiles for ophthalmic exam findings (visual acuity scales, slit lamp findings, fundus exam schemas, refraction data, etc.). This means the most clinically distinctive data that MaximEyes stores — the specialty eye care data that makes it different from a general EHR — likely has no representation in this export.

The Swagger API does include **Account**, **ChargeItem**, and **Coverage** resources, which demonstrates some effort to go beyond US Core for billing data. However, the FHIR API PDF (40 pages) does not document these three resources at all — they appear only in the Swagger spec, suggesting they may be added but not yet formally documented.

A third party could reconstruct a general clinical summary from this export (demographics, problems, meds, allergies, vitals, labs, notes, procedures, immunizations). But they could not reconstruct the specialty-specific eye care record — the very data that distinguishes this product.

### Documentation Quality

The documentation is **functional but thin**:
- The EHI export PDF (4 pages) provides basic instructions and screenshots. It does not explain what specific FHIR resources or fields are included for each listed scope category.
- The FHIR API PDF (40 pages) provides API reference documentation with search parameters and USCDI data class mappings. It is adequate for a developer to build a FHIR client. However, it is really a **(g)(10) FHIR API document**, not a **(b)(10) EHI export data dictionary**.
- There are **no sample export files, worked examples, or sample NDJSON records**.
- There is **no data dictionary** — no field-level documentation of what specific data elements are included in each resource type, what coded values are used, or how MaximEyes-specific data maps to FHIR elements.
- The OpenAPI/Swagger spec is machine-readable but contains only endpoint definitions, not data schemas (response schemas are absent — all 200 responses just say "Success").
- The documentation shows no mention of how the export handles data that doesn't map to standard FHIR resources.

### Structure & Completeness

- **Granularity**: Resource-type level only. The "Scope of EHI" is a 15-item bulleted list with no field-level detail. The FHIR API documentation maps USCDI data classes to FHIR resources but does not document field mappings, extensions, or value sets.
- **Coded fields**: Not documented. The documentation mentions SNOMED, LOINC, and ICD codes in search parameter examples but does not specify which code systems are used for which fields.
- **Relationships**: Not documented beyond FHIR's built-in references.
- **Value sets**: Not documented.
- **Versioning**: Both PDFs are dated 03/17/25 (Revised). No change history.

### The (b)(10) vs (g)(10) Confusion

This is a textbook case of **(g)(10) documentation repackaged as (b)(10)**. The signs:

1. The FHIR API PDF footer reads "MaximEyes **FHIR API** Documentation" on every page — it was written for the FHIR API certification, not for EHI export.
2. The documented FHIR resources exactly match the US Core resource set required for (g)(10).
3. The supported scopes are US Core scopes.
4. The export uses the same FHIR Bulk Data endpoint as the (g)(10) API.
5. The "Scope of EHI" on page 4 lists USCDI data classes, not the full data domains the product stores.
6. There is no mention of billing, optical retail, specialty eye care data, images, or any data that goes beyond USCDI.

The Swagger API's inclusion of Account, ChargeItem, and Coverage is a modest step beyond (g)(10), but these three resources are undocumented and cover only a fraction of the product's billing/financial data.

**Bottom line**: The export covers the USCDI/US Core clinical data slice — perhaps 30-40% of the designated record set for an eye care practice using MaximEyes. The entirety of the specialty ophthalmology/optometry clinical data (structured exam findings, optical orders, specialty prescriptions), diagnostic images, and most billing workflow data appear to be outside the export scope.

## Access Summary
- Final URL: https://customer.first-insight.com/downloads/forms/MaximEyes-EHI-Export-Documentation.pdf (no redirects)
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The EHI export PDF contains a link to the FHIR API documentation PDF with a broken URL (`MaximEyes-FHIR-APIDocumentation.pdf` — missing a hyphen, likely due to a line-break artifact in the PDF). The correct URL is `MaximEyes-FHIR-API-Documentation.pdf`. This would prevent a user from following the link directly.
- The Swagger UI at fhir.maximeyes.com is functional and publicly accessible.
- No enrichment step was needed — the documentation corpus consists of two short PDFs and one JSON file, all directly queryable.
