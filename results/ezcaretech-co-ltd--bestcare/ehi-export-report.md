# ezCaretech Co., Ltd. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.ezcaretech.com/english/onc/b.10_EHI_Export.pdf
- CHPL IDs: 9665
- Product: BESTCare 2.0B
- Certification date: 2018-04-23

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://www.ezcaretech.com/english/onc/b.10_EHI_Export.pdf" \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```
Response: HTTP/2 200, Content-Type: application/pdf, Content-Length: 24829. Direct PDF download, no redirects.

### Step 2: Download and examine the PDF
```bash
curl -sL "https://www.ezcaretech.com/english/onc/b.10_EHI_Export.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o b.10_EHI_Export.pdf
```
Verified with `file` command: PDF document, version 1.5, 1 page. Author: Eunsol Lee. Created 2023-09-30 via Microsoft Word 2013.

Extracted text with `pdftotext`. The PDF is a single page with two sections:
- **I. Electronic Health Information Export** — describes single-patient and multi-patient export in CSV and Oracle DMP formats
- **II. API documentation** — a "Click Here" link

### Step 3: Extract the hyperlink from the PDF
Used `strings` on the PDF binary to find the embedded URI:
```
https://portal.ezcaretech.com:30112/baseUrls
```
This is the "Click Here" link target from the PDF's Section II.

### Step 4: Probe and navigate the API portal
```bash
curl -sI -L "https://portal.ezcaretech.com:30112/baseUrls" -H 'User-Agent: Mozilla/5.0'
```
Response: HTTP/1.1 200, Content-Type: text/html. The portal is a web application ("User Portal") with navigation links to:
- Service Base URLs
- Authorization
- Application Access API
- Single Patient API
- Multi Patient API
- Terms of Use

Navigated to each subpage in browser and via curl. The portal is an Asciidoctor-styled documentation site for "ezFHIRStation" — their FHIR server product.

### Step 5: Fetch FHIR CapabilityStatement
```bash
curl -sL "https://portal.ezcaretech.com:30122/metadata" \
  -H 'Accept: application/fhir+json' -H 'User-Agent: Mozilla/5.0'
```
Returns a valid FHIR R4 CapabilityStatement for "ezfhirstation-us-core-usa-aurora" (version 1.0, release date 2022-02-16). Lists 26 resource types — standard US Core resources.

### Step 6: Check the ONC mandatory disclosures page
```bash
curl -sL "https://www.ezcaretech.com/english/onc/onc_2015.html" -H 'User-Agent: Mozilla/5.0'
```
The ONC disclosures page links to:
- Mandatory Disclosures Letter (PDF)
- BESTCare2.0B Certified Health IT v.3.0 (PDF) — a 3-page listing of certified criteria, no technical detail about EHI export
- Real World Test Plans and Results (2022–2026)
- Multi-factor Authentication Use Case
- The same b.10_EHI_Export.pdf

Downloaded and examined the "Certified Health IT v.3.0" PDF — it is a list of 33 certified criteria and 13 CQMs with no additional information about export format, data dictionary, or mechanisms.

Checked the Mandatory Disclosures Letter — it briefly describes (b)(10) as "This capacity allows to export electronic health information (EHI)" with standard cost/fee language. No technical detail.

### Step 7: Review Multi Patient API page
The Multi Patient API Guide documents the FHIR Bulk Data Export specification:
- `/Patient/$export` — all patients
- `/Group/[id]/$export` — group of patients
- `/$export` — system-level export
- Standard Bulk Data parameters: `_outputFormat`, `_since`, `_type`, `_elements`, `includeAssociatedData`, `_typeFilter`, `patient`
- Export status polling and file download endpoints
- Output format: NDJSON (application/fhir+ndjson)

Last updated on the portal: 2023-03-03.

## What Was Found

The EHI export documentation consists of two components:

### 1. The Primary (b)(10) PDF (b.10_EHI_Export.pdf)
A single-page PDF that describes two export capabilities:
- **Single Patient Export**: Export EHI for one patient at any time without developer assistance
- **Multi-Patient Export**: Export all data for a patient population

The export uses two "standardized" file formats:
- **CSV**: Comma-separated values files
- **Oracle DMP**: Oracle database dump files (binary format)

The PDF states that "BESTCare2.0B updates all formats on a quarterly schedule unless otherwise indicated by Oracle. If a specific update or patch from Oracle is released pertaining to one of these formats, then an on-demand update is made."

**Critically, there is no data dictionary.** The PDF does not describe:
- Which tables or data categories are included in the export
- What fields/columns exist in the CSV files
- The schema of the Oracle DMP
- How many tables there are
- How relationships between tables are expressed
- Any sample data or examples
- Any instructions for performing the export (no screenshots, no workflow description)

### 2. The FHIR API Portal (portal.ezcaretech.com:30112)
The "Click Here" link in the PDF leads to a FHIR API developer portal documenting "ezFHIRStation" — their SMART on FHIR server. This includes:
- **Single Patient API**: Standard US Core FHIR R4 API with 26 resource types (AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, plus supporting types)
- **Multi Patient API**: FHIR Bulk Data Export ($export) with NDJSON output
- **Authorization**: SMART on FHIR OAuth2 with Backend Services for bulk export

The portal is named "ezfhirstation-us-core-usa-aurora" — explicitly referencing the US Core profile set and the Aurora Behavioral Healthcare deployment.

## Export Coverage Assessment

### Data Domain Coverage

**The (b)(10) PDF describes CSV and Oracle DMP export but provides zero information about what data is included.** There is no data dictionary, no table listing, no field documentation, and no schema. The phrase "all the data for a patient population" is used for multi-patient export, suggesting comprehensive coverage, but this is entirely unsubstantiated by documentation.

**The FHIR API covers only the standard US Core clinical data subset:**
- Demographics (Patient)
- Problems/conditions (Condition)
- Medications (MedicationRequest, Medication)
- Allergies (AllergyIntolerance)
- Lab results (DiagnosticReport, Observation)
- Procedures (Procedure)
- Immunizations (Immunization)
- Encounters (Encounter)
- Care plans (CarePlan, CareTeam, Goal)
- Implantable devices (Device)
- Clinical notes (DocumentReference)
- Provenance tracking (Provenance)

**The following data domains from the product research are clearly absent from the FHIR API and undocumented in the CSV/DMP export:**
- **Billing and financial records** — BESTCare has billing modules; no billing data in US Core
- **CPOE orders** (lab, imaging, procedure orders) — only medication orders are in FHIR; the product manages comprehensive CPOE across all order types
- **Pharmacy dispensing and closed-loop medication administration records** — BESTCare's CLMA (barcode/RFID verification) records are not in US Core
- **Nursing assessments and documentation** — the 3,000+ clinical templates
- **Radiology/imaging results** — DiagnosticReport covers some, but not the full imaging workflow
- **Clinical Decision Support alerts and responses** — not in US Core
- **Clinical pathway data with variance tracking** — not in US Core
- **Social services records** — not in US Core
- **CRM/patient relationship data** — not in US Core
- **Activity-based costing / financial analytics** — not in US Core
- **Clinical data warehouse extracts** — not in US Core
- **Inpatient census/bed management data** — not in US Core
- **Audit logs** — certified for (d)(2)/(d)(3), not exported
- **Behavioral health-specific documentation** — psychiatric assessments, behavioral health forms used at Aurora hospitals
- **Blood transfusion and sample tracking data** — not in US Core
- **HIE exchange records** — not in US Core

The CSV/Oracle DMP export *could* cover all of these — an Oracle DMP in particular could be a complete database dump — but without any documentation of what's included, it's impossible to assess.

### Export Format & Standards

The vendor describes two distinct export mechanisms:

1. **CSV + Oracle DMP** (the actual (b)(10) mechanism): These are appropriate formats for a comprehensive database export. An Oracle DMP could theoretically contain the entire database schema and data. However:
   - No documentation of what tables/fields are included
   - No schema documentation for the Oracle DMP
   - No column headers or data dictionary for the CSV files
   - No sample data
   - Oracle DMP is a proprietary binary format requiring Oracle tools to import — not ideal for portability

2. **FHIR Bulk Data Export** (the (g)(10) mechanism, linked from the (b)(10) PDF): Standard FHIR R4 with US Core profiles, NDJSON format. Well-documented API but only covers the standard clinical data subset (~26 resource types). This is clearly a (g)(10) implementation being cross-referenced as (b)(10) documentation.

A third party receiving a CSV export with no data dictionary would struggle to interpret the data. A third party receiving an Oracle DMP would need Oracle database tools and would have to reverse-engineer the schema. The FHIR export is interpretable but incomplete.

### Documentation Quality

**Very poor.** The core (b)(10) documentation is a single page with approximately 150 words of actual content. It:
- Does not define what data is exported
- Does not include any data dictionary or schema
- Does not provide export instructions or screenshots
- Does not describe the user workflow for initiating an export
- Does not explain how CSV files are structured (one file per table? one per resource type? one giant file?)
- Does not explain the Oracle DMP structure
- Does not provide sample files
- Does not address how to import/interpret the exported data

The FHIR API portal is adequately documented for its purpose (a (g)(10) FHIR API) but is not actually (b)(10) export documentation — it documents a different requirement.

A developer receiving this documentation could not implement an import of the CSV/DMP exported data. They would know the files are CSV and Oracle DMP, but nothing about their content or structure.

### Structure & Completeness

- **Field-level documentation**: None. Zero fields, tables, or columns are documented for the CSV/Oracle DMP export.
- **Value sets**: None documented for the native export. The FHIR API uses standard US Core value sets.
- **Relationships between entities**: Not documented for the native export.
- **Versioning**: The PDF mentions quarterly format updates aligned with Oracle releases. No version history is provided.
- **Sample data**: None.
- **Schema files**: None for the native export. The FHIR CapabilityStatement is available for the API.

### Overall Assessment

ezCaretech's (b)(10) documentation is among the most minimal possible. The one-page PDF names two export formats (CSV and Oracle DMP) but provides no data dictionary, no schema, no field definitions, no sample data, and no user instructions. The "Click Here" link to their FHIR API portal conflates the (g)(10) FHIR API requirement with (b)(10), which is a common pattern but particularly stark here because the vendor also describes a separate CSV/Oracle DMP export mechanism that is clearly distinct from the FHIR API.

The CSV/Oracle DMP approach could actually be a genuine (b)(10) implementation — a database dump is one of the most comprehensive possible export formats — but without any documentation of what the dump contains, how to interpret it, or how to initiate it, the documentation fails to make the export usable. The Oracle DMP format in particular is a proprietary binary format that requires Oracle database tools, raising portability concerns.

The FHIR API, while well-documented, covers only the US Core subset of clinical data (26 resource types) and does not address billing, administrative, behavioral health-specific, or operational data that BESTCare manages. This is a textbook example of (g)(10)/(b)(10) conflation.

## Access Summary
- Final URL (after redirects): https://www.ezcaretech.com/english/onc/b.10_EHI_Export.pdf (no redirects)
- Status: found
- Required browser: no (PDF is a direct download; API portal works in browser but curl also works)
- Navigation complexity: direct_link (PDF) + one_click (API portal linked from PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The PDF downloaded cleanly, the API portal was accessible, and the FHIR endpoint responded.
- The Single Patient API HTML page is 1.8MB due to embedded Asciidoctor CSS/JS styling, but content was extractable.
- The API portal content is embedded in styled HTML with significant CSS — browser rendering was more useful than curl text extraction for the API pages.
