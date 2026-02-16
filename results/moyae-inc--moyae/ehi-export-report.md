# Moyae, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.moyae.com/disclosures-and-costs
- CHPL IDs: 11331
- Certification Date: August 16, 2023
- Product: Moyae, Version 1
- CHPL Number: 15.05.05.3141.MOYA.01.01.1.230816

## Navigation Journal

### Step 1: Probe the registered URL

```bash
curl -sI -L "https://www.moyae.com/disclosures-and-costs" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```

Response: HTTP/2 200, `Content-Type: text/html; charset=utf-8`, served via Cloudflare (Webflow-hosted site). No redirects.

### Step 2: Fetch and examine the page

```bash
curl -sL "https://www.moyae.com/disclosures-and-costs" \
  -H 'User-Agent: Mozilla/5.0' -o disclosures-and-costs.html
```

The page is a static Webflow-hosted compliance disclosures page. Key content:

- ONC certification boilerplate
- Developer: Moyae, Inc. / Product: Moyae / Version 1
- Certification number and date
- Criteria certified: (a)(3), (a)(5), (a)(14), (b)(1), (b)(10), (b)(11), (d)(1-9,12,13), (g)(3-7,9,10)
- **EHI Export Format**: "New-line delimited JSON export of FHIR data: https://www.hl7.org/fhir/R4/nd-json.html"
- Links to Real World Testing plans/results (2024, 2025)
- Costs disclosures (per-user billing, eRx add-on, data migration costs)
- Relied-upon software: MaxMD, Rcopia/DrFirst eRX, Auth0, ID.me, Postman

No link to a dedicated EHI export data dictionary, schema, or user guide on this page. The only technical export artifact is the Postman API documentation link, which is embedded elsewhere on the page (linked from the criteria section).

### Step 3: Locate the Postman API documentation

The CHPL listing links to: `https://documenter.getpostman.com/view/15917486/UyxojQMd#a24aa40c-fe15-478e-a555-3c2cb10d56c9`

This is a JavaScript SPA rendered by Postman. The underlying collection data was retrieved programmatically:

```bash
curl -sL "https://documenter.getpostman.com/api/collections/15917486/UyxojQMd" \
  -H 'User-Agent: Mozilla/5.0' -o moyae-fhir-api-postman-collection.json
```

This returned the full Postman collection JSON (2.5MB).

### Step 4: Fetch the FHIR CapabilityStatement

The Postman collection references the FHIR Base URL. The CapabilityStatement was publicly accessible:

```bash
curl -s "https://fg93b2lt5i.execute-api.us-east-1.amazonaws.com/dev/tenant/sitetenant/metadata" \
  -H 'Accept: application/fhir+json' -o fhir-capability-statement.json
```

This returned a valid FHIR R4 CapabilityStatement (1.2MB) listing 146 resource types.

### Step 5: Fetch SMART configuration

```bash
curl -s "https://fg93b2lt5i.execute-api.us-east-1.amazonaws.com/dev/tenant/sitetenant/.well-known/smart-configuration" \
  -H 'Accept: application/json' -o smart-configuration.json
```

Valid SMART configuration with OAuth2 endpoints (Auth0-based).

### Step 6: Visual evidence

Screenshots were taken of:
- The disclosures page (full page)
- The Postman API documentation (overview and Export section)

## What Was Found

Moyae's EHI export documentation consists of two artifacts:

1. **A single line on the disclosures page** stating the export format is "New-line delimited JSON export of FHIR data" with a link to the NDJSON specification.

2. **A Postman collection** titled "Moyae FHIR API Documentation" that documents 954 endpoints across 122 folders covering 118 FHIR resource types, plus a system-level `$export` endpoint, authentication, CCDA, and metadata endpoints.

### The Export Mechanism

The EHI export uses the FHIR Bulk Data `$export` operation at the system level:

- **Endpoint**: `{{API_URL}}/$export`
- **Parameters**:
  - `_outputFormat=ndjson` — Output as Newline Delimited JSON
  - `_since` — Date filter for incremental exports
  - `_type` — Resource type filter (e.g., `Patient`)
- **Authentication**: Bearer token (Cognito/Auth0) + API key header
- **Job management**: Status polling at `$export/:jobId`, cancellation via DELETE
- **Output format**: NDJSON (one FHIR resource JSON object per line)

### The FHIR Server

The CapabilityStatement reveals that Moyae runs a full FHIR R4 server (version "1.0.0") supporting **146 resource types** — essentially the entire FHIR R4 resource catalog. Every resource type supports create, read, update, delete, vread, and search-type interactions. Each resource also has comprehensive search parameter support.

The server declares a single operation: `export` (referencing `http://hl7.org/fhir/uv/bulkdata/OperationDefinition/export`), confirming it implements the FHIR Bulk Data specification for export.

### What's Notable

The API is **not** limited to US Core / USCDI resources. The 146 supported resource types include:

- **Clinical**: Patient, Condition, Observation, Procedure, MedicationRequest, MedicationStatement, MedicationAdministration, AllergyIntolerance, Immunization, DiagnosticReport, CarePlan, CareTeam, Encounter, DocumentReference, VisionPrescription, ImagingStudy, Media, and many more
- **Financial/Billing**: Claim, ClaimResponse, ExplanationOfBenefit, Coverage, Account, ChargeItem, Invoice, PaymentNotice, PaymentReconciliation, InsurancePlan
- **Administrative**: Organization, Practitioner, PractitionerRole, Location, Appointment, Schedule, Slot

This breadth is atypical — most EHR vendors only expose a small subset of FHIR resources. Moyae appears to have deployed a generic FHIR R4 server that supports the full specification.

### What's Missing from the Documentation

- **No data dictionary**: There is no document that maps Moyae's internal data model to FHIR resources. We know the API *supports* 146 resource types, but there is no documentation of which resource types Moyae actually *populates* with data, which fields are used, or how ophthalmology-specific data is represented.
- **No custom profiles or extensions**: No StructureDefinitions, Implementation Guide, or documentation of custom FHIR extensions. For an ophthalmology EHR, specialty-specific clinical data (IOP measurements, visual acuity, retina drawings, injection series) would require custom extensions or profiles — none are documented.
- **No sample data or worked examples**: The Postman collection has no example response bodies for any endpoint.
- **No export user guide**: No instructions on how a clinic administrator or patient would initiate an EHI export.
- **No field-level documentation**: The API documentation shows endpoint URLs and HTTP methods, but provides no description of what data each resource type contains, what search parameters are meaningful, or what coded values are used.

## Export Coverage Assessment

### Data Domain Coverage

Moyae is an ophthalmology/optometry EHR that stores:
- Patient demographics
- Ophthalmic examination data (IOP, visual acuity, refraction, anterior/posterior segment findings)
- Retina drawings
- Intravitreal injection records
- Implantable device records
- Diagnostic imaging orders
- Care plans and encounter notes
- Diagnostic codes (ICD)
- E-prescribing data
- Quality/registry data (IRIS, MIPS)

The FHIR server supports 146 resource types with a system-level `$export`, which *in theory* could export all data stored about patients. The presence of financial resources (Claim, ClaimResponse, ExplanationOfBenefit, Coverage, ChargeItem, Invoice) alongside clinical resources suggests that if the export is fully populated, it could cover both clinical and billing data.

**However, the key question is unanswerable from the documentation**: Which of these 146 resource types does Moyae actually use to store patient data? Supporting a FHIR resource type in the API does not mean data is stored there. The full FHIR R4 catalog includes resource types that no ophthalmology EHR would use (e.g., MedicinalProductPharmaceutical, SubstanceNucleicAcid, ResearchElementDefinition). The API appears to be a generic FHIR server that mechanically supports every resource type, without documenting which ones contain actual patient data.

**Likely covered** (based on product functionality):
- Demographics (Patient)
- Conditions/Diagnoses (Condition)
- Medications/Prescriptions (MedicationRequest)
- Encounters (Encounter)
- Observations (Observation — could include IOP, visual acuity)
- Procedures (Procedure)
- Devices (Device — implantable devices)
- Documents (DocumentReference — could include clinical notes)
- Imaging orders (ImagingStudy, DiagnosticReport)

**Unclear/likely gaps**:
- **Ophthalmology-specific data**: How are IOP measurements, refraction data, anterior/posterior segment findings, retina drawings, and intravitreal injection series represented in FHIR? Standard FHIR Observation can handle some of this, but retina drawings and specialty exam findings typically require custom extensions. No documentation exists.
- **Billing data**: The API supports financial resource types, but Moyae partners with AdvancedMD for billing/practice management. It's unclear whether billing data actually lives in Moyae's FHIR server or resides in AdvancedMD. If billing data is in AdvancedMD, the (b)(10) export from Moyae would not include it.
- **Quality/registry data**: IRIS/MIPS reporting data is not addressed in the export documentation.

### Export Format & Standards

- **Format**: FHIR R4 NDJSON via the Bulk Data `$export` operation
- **FHIR Version**: 4.0.1
- **Standard**: HL7 FHIR Bulk Data Access (referenced in CapabilityStatement)
- **Profiles**: None documented. The API uses base FHIR R4 — no US Core, no custom ophthalmology profiles.
- **Extensions**: None documented, despite ophthalmology data requiring them.

The format choice (FHIR NDJSON) is appropriate for bulk export. The breadth of resource types (146) goes far beyond US Core, which is a positive signal for (b)(10) coverage. However, without knowing which resource types are populated with data, the format's suitability can't be fully assessed.

A third party receiving this export would need to understand standard FHIR R4 to parse the data. However, without custom profile or extension documentation, ophthalmology-specific data fields could be opaque or misinterpreted.

### Documentation Quality

**Very sparse.** The EHI export documentation consists of:
1. A single sentence on the disclosures page ("New-line delimited JSON export of FHIR data")
2. A Postman API collection showing endpoint URLs, HTTP methods, authentication requirements, and query parameters — but no descriptions, no examples, no field-level documentation

There is:
- No data dictionary mapping the product's data model to FHIR resources
- No documentation of custom extensions for ophthalmology data
- No worked examples or sample exports
- No user guide for initiating an export
- No description of which resource types contain data vs. which are just supported by the server
- No value set documentation
- No documentation of relationships between resources

A developer implementing an import of this data would have the FHIR R4 specification to work from, but would have no vendor-specific guidance on how to interpret the data. For standard clinical data (demographics, conditions, medications), this might be sufficient. For ophthalmology-specific data, it would be inadequate.

### Structure & Completeness

- **Granularity**: The documentation provides only endpoint-level information (URLs and HTTP methods). There is no field-level documentation.
- **Coded fields**: Not documented. No value sets are specified.
- **Relationships**: Not documented beyond what's implicit in the FHIR specification.
- **Versioning**: The Postman collection has no version history. The CapabilityStatement includes a date but no formal versioning.

The documentation looks like a compliance checkbox — the minimum needed to have "something" to point to for the (b)(10) certification. The FHIR server itself is potentially capable of exporting all data, but the lack of documentation means there's no way to verify completeness or understand the data model.

### The (b)(10) vs (g)(10) Question

This is an interesting case. Moyae appears to use the **same** FHIR server and `$export` endpoint for both (b)(10) EHI export and (b)(11)/(g)(10) API access. However, unlike many vendors who conflate these, Moyae's FHIR server supports 146 resource types — far exceeding the ~20 US Core resource types required for (g)(10).

The system-level `$export` endpoint can theoretically export everything in the FHIR server, not just USCDI data. If the server is properly populated with all patient data (including billing, specialty clinical data, etc.), this could genuinely satisfy (b)(10).

The concern is that supporting 146 resource types in the API doesn't prove that data actually lives in those resource types. A generic FHIR server that mechanically supports every resource type but only populates Patient, Condition, Observation, and a handful of others would still effectively be a (g)(10)-level export masquerading as (b)(10).

Without a data dictionary or documentation of which resources are populated, this question remains open.

## Access Summary
- Final URL (after redirects): https://www.moyae.com/disclosures-and-costs
- Status: found
- Required browser: no (page is static HTML; Postman docs need JS but underlying JSON was accessible via API)
- Navigation complexity: one_click (disclosures page links to Postman; Postman API docs also have a direct JSON endpoint)
- Anti-bot issues: none (Cloudflare CDN but no blocking)

## Obstacles & Dead Ends

- **No obstacles encountered.** The disclosures page, Postman API collection, FHIR CapabilityStatement, and SMART configuration were all publicly accessible.
- The `site.moyae.com` domain serves the login page for the EHR application itself (React SPA) — not useful for documentation.
- The Postman documentation SPA renders in the browser but the underlying collection JSON is accessible at `documenter.getpostman.com/api/collections/15917486/UyxojQMd`, which was the preferred computable artifact.
- No downloadable PDFs, data dictionaries, or schema files were found beyond the Real World Testing plans (which are regulatory filings, not export documentation).
