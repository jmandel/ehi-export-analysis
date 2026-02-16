# InPracSys — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: http://www.inpracsys.com/disclosure
- Final URL (after redirects): https://inpracsys.com/disclosure/
- CHPL ID: 10194 (15.05.05.2762.INPS.01.00.1.191206)
- Developer: InPracSys (Innovative Practice Systems, Inc.)
- Product: InPracSys EHR, Version 9.0
- Certification date: December 6, 2019

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "http://www.inpracsys.com/disclosure" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 301 → https://www.inpracsys.com/disclosure → 301 → https://inpracsys.com/disclosure/ → HTTP 200. WordPress-based page (PHP/7.4.33, LiteSpeed server).

### Step 2: Examine the disclosure page
```bash
curl -sL "https://inpracsys.com/disclosure/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```
The page contains:
1. An embedded PDF viewer (EmbedPress plugin) displaying `Disclosure-EHR-Inpracsys_NewV6.1.pdf` (3 pages)
2. Two download links below the PDF:
   - "Download EHI export format here." → links to https://inpracsys.com/fhir
   - "Download Service URL Bundle here." → links to https://inpracsys.com/wp-content/uploads/2024/12/FhirServiceBaseBundleV10.json

### Step 3: Download the embedded PDF
```bash
curl -sL "https://inpracsys.com/wp-content/uploads/2025/12/Disclosure-EHR-Inpracsys_NewV6.1.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/Disclosure-EHR-Inpracsys_NewV6.1.pdf
```
Confirmed: PDF document, 3 pages, 192,354 bytes. Author: Sandeep Kataria. Created: 2025-12-20.

### Step 4: Download the FHIR Service Bundle JSON
```bash
curl -sL "https://inpracsys.com/wp-content/uploads/2024/12/FhirServiceBaseBundleV10.json" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/FhirServiceBaseBundleV10.json
```
Confirmed: JSON text data, 3,982 bytes. A FHIR Bundle containing an Endpoint resource and two Organization resources pointing to `sfp-proxy23604.azurewebsites.net/fhir`.

### Step 5: Follow the "EHI export format" link to the FHIR page
```bash
curl -sL "https://inpracsys.com/fhir/" -H 'User-Agent: Mozilla/5.0' -o downloads/fhir-api-documentation-page.html
```
This is a comprehensive FHIR API documentation page (691 KB HTML). It documents individual FHIR resource endpoints for:
- Patient (search, retrieve)
- Smoking Status (Observation)
- Condition (Problem)
- Medication (MedicationStatement)
- Allergy or Intolerance
- Laboratory Result DiagnosticReport (Lab Orders)
- Laboratory Result Observations (DiagnosticOrder)
- Vital Signs (Observation)
- Procedure
- Care Team (Practitioner via CarePlan)
- Immunization
- Implantable Devices/UDI (Device)
- Assessment and Plan of Treatment (CarePlan)
- Goal
- Health Concern (HealthcareService/Condition)

Each resource section includes: API endpoint URL, request parameters, response field definitions with cardinality and data types, sample JSON output, and expected exceptions.

### Step 6: Screenshots taken
- Disclosure page (top with embedded PDF): `screenshot-disclosure-page.png`
- Disclosure page (bottom with download links): `screenshot-disclosure-bottom.png`
- FHIR documentation page: `screenshot-fhir-page.png`

## What Was Found

### The Disclosure PDF (3 pages)
The PDF is a formal mandatory disclosure letter addressed to SLI Compliance for version 9.0. It contains:
- **Page 1**: Cost disclosure table for various modules (lab interfaces, e-prescribing, public health reporting, patient portal, direct messaging) — standard ONC transparency requirements.
- **Page 2**: Product identification (developer, product, version, CHPL number, certification date) and a complete list of all 35+ certified criteria.
- **Page 3**: The critical b(10) section titled "INPRACSYS EHR B(10) DISCLOSURES" which states:

> "InPracSys EHR provides authorized users export of electronic health information (EHI) for a single patient as well as for the patient population in the export format contained in this link in full compliance with 170.315(b)(10) Electronic Health Information."

> "The EHI export contains available electronic health information for a single patient or multiple patients in computable file format. The export(s) can be downloaded as a zip file containing .xml file(s)."

The PDF indicates the export format is XML files packaged in a ZIP archive, and links to the FHIR page for details.

### The FHIR API Documentation Page
This is the primary "export format" documentation. It documents a custom FHIR API hosted at `fhirips.azurehealthcareapis.com` (Azure-hosted). Key characteristics:

- **FHIR version**: Claims FHIR R4, but the API structure and resource shapes are heavily non-standard
- **Authentication**: OAuth 2 with Bearer tokens
- **API pattern**: Individual resource-type endpoints queried by patient ID (`?pid=...`)
- **Response format**: JSON, but using a non-standard serialization with properties like `ValueElement`, `SystemElement`, `CodeElement` (appears to be a C# FHIR library's internal object structure serialized directly, rather than standard FHIR JSON)
- **Covered resource types**: Patient, SmokingStatus, Condition, Medication, AllergyIntolerance, LabOrders (CarePlan), DiagnosticOrder, Observation (Vitals), Procedures, Practitioner (CareTeam), Immunization, Device, CarePlan (Assessment/Plan), Goal, HealthcareService (Health Concerns)

### The Service URL Bundle
A FHIR Bundle with:
- One Endpoint resource pointing to `sfp-proxy23604.azurewebsites.net/fhir`
- Two sample Organization resources ("Health Clinic 1" and "Health Clinic 2") with placeholder data

## Export Coverage Assessment

### Data Domain Coverage

The FHIR API documentation covers approximately the same data domains as a standard US Core / USCDI implementation. Based on the product research, which identified InPracSys EHR as a urology-specific product with extensive modules, the following assessment applies:

**Domains clearly covered by the FHIR API documentation:**
- Patient demographics
- Problems/conditions (including health concerns)
- Medications
- Allergies
- Lab results and orders
- Vital signs
- Procedures
- Immunizations
- Implantable devices
- Smoking status
- Care team/practitioners
- Goals
- Assessment and plan of treatment

**Domains clearly MISSING from the export documentation:**
- **Billing/financial data** — InPracSys has a billing module with superbill generation, E/M coding, claims management, and anatomical pathology billing. None of this appears in the export.
- **Clinical notes/encounter documentation** — The FastCharting module is the product's primary differentiator, generating full encounter notes (HPI, ROS, exam, assessment/plan). No DocumentReference or clinical note export is documented.
- **E-prescribing records** — DoseSpot integration data, prescription history beyond the medication list
- **Care Pathways / PRACTICE iQ data** — Stepped therapy programs, pre-authorization records, drug program qualifications. This is described as a major revenue feature.
- **Risk Management alerts** — Urology-specific CDS rules (stent tracking, missed ultrasounds). Related to the separate RiskAssistMD product.
- **Patient portal data** — Messages, correspondence, account management records
- **Quality/compliance data** — CQM/PQRS measures, Meaningful Use attestation data
- **Syndromic surveillance / electronic case reporting data** — Certified under (f)(2) and (f)(5)
- **Audit logs** — Certified under (d)(2), (d)(3), (d)(10)
- **Clinical trial candidate identification data** — A documented module
- **Data mining/analytics outputs**
- **Scheduling/appointment data**
- **Urology-specific clinical data** — Urine analysis workflows, bladder scan results, TRUS data, cystoscopy images — the specialty-specific data that distinguishes this product
- **Family health history** — Certified under (a)(12) but not in the FHIR API
- **Social determinants of health** — Certified under (a)(15) but not in the FHIR API
- **Referral records** — Certified under (b)(3) but not in the FHIR API
- **Scanned documents/images** — Unclear if the product stores these, but common in urology

**This is a textbook example of the (b)(10) vs (g)(10) confusion.** The export documentation is essentially the vendor's (g)(10) FHIR API documentation repurposed as the (b)(10) EHI export. The FHIR API covers only the standard USCDI clinical data classes — the same data that would be available through any (g)(10)-certified API. There is no evidence that the export includes "all electronic health information" as required by (b)(10). The billing module, the specialty urology data, the care pathway records, the risk management alerts, and all administrative/operational data appear entirely absent.

### Export Format & Standards

The export is described as XML files in a ZIP, but the documentation page documents a FHIR JSON API. There is a contradiction: the disclosure PDF says "zip file containing .xml file(s)" while the FHIR page documents JSON responses from a REST API. It's unclear whether:
1. The actual b(10) export produces XML files (undocumented format), or
2. The b(10) export is the FHIR API itself and the PDF description is inaccurate, or
3. There is a separate export mechanism that bundles the FHIR API output into XML/ZIP

The FHIR API itself uses a non-standard JSON serialization. The sample outputs show C#-style property names like `ValueElement`, `SystemElement`, `CodeElement`, `DisplayElement`, `StatusElement` — this appears to be a direct serialization of the HAPI FHIR or Firely .NET FHIR library's internal object model rather than standard FHIR JSON. A third party attempting to parse these outputs as standard FHIR JSON would fail. The API endpoint paths are also non-standard (e.g., `/SmokingStatus`, `/LabOrders`, `/Procedures` instead of standard FHIR resource types).

### Documentation Quality

**Positive aspects:**
- The FHIR page is reasonably comprehensive for what it covers — each resource type has endpoint URLs, parameter tables, field definitions with cardinality and data types, and sample JSON output
- Field descriptions include value set references (though pointing to older DSTU2/Argonaut-era URLs)
- The documentation is clearly structured and navigable

**Negative aspects:**
- The documentation conflates the (g)(10) FHIR API with the (b)(10) EHI export without acknowledging the difference
- Sample JSON outputs use non-standard FHIR serialization that would confuse developers expecting standard FHIR
- The FHIR version claim of "V4" contradicts the Argonaut/DSTU2-era resource structures and references (DAF profiles, Argonaut IG)
- No data dictionary for the actual export format (if it really is XML in a ZIP, what does that XML look like?)
- No schema files (XSD, JSON Schema, OpenAPI) are provided
- No sample export files or example ZIP downloads
- No documentation of what "all electronic health information" means in context — no mapping from EHR data domains to export contents
- The value sets referenced are often DSTU2-era URLs
- There is no export procedure documentation — no user guide explaining how to trigger the export from the EHR UI

### Structure & Completeness

The field-level documentation is reasonably granular for the covered resources — field names, FHIR data types, cardinality, and descriptions are provided. However:
- No machine-readable schema files
- Coded fields reference value sets by URL but don't enumerate the actual codes used by InPracSys
- Relationships between entities are implicit (patient references) but not explicitly documented as a data model
- No versioning or change history
- The documentation appears to be largely static content written once, not actively maintained

## Access Summary
- Registered URL: http://www.inpracsys.com/disclosure
- Final URL: https://inpracsys.com/disclosure/
- Status: found
- Required browser: no (curl works, but browser needed to see embedded PDF)
- Navigation complexity: one_click (disclosure page → FHIR page link for export format details)
- Anti-bot issues: none

## Obstacles & Dead Ends

No significant obstacles. The page loads cleanly, files download without issues, and no authentication is required. The main challenge is interpretive rather than technical: understanding what the documentation actually describes and how it relates to the (b)(10) requirement.

The contradiction between "zip file containing .xml file(s)" in the PDF and the JSON FHIR API on the linked page is confusing and unresolved. There may be a separate XML-based export mechanism that is not publicly documented.
