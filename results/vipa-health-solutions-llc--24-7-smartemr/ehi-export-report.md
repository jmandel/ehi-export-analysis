# VIPA Health Solutions, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://smartemr.readme.io/docs/electronic-health-information-export-b10
- CHPL ID: 11079
- Product: 24/7 smartEMR v7.2
- Certification date: 2022-12-16
- Developer: VIPA Health Solutions, LLC (Miami, FL)

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://smartemr.readme.io/docs/electronic-health-information-export-b10" \
  -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, `text/html; charset=utf-8`, served via Cloudflare + Render (ReadMe.io platform). No redirects.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://smartemr.readme.io/docs/electronic-health-information-export-b10" \
  -H 'User-Agent: Mozilla/5.0' -o electronic-health-information-export-b10.html
```
The page is a ReadMe.io-hosted documentation site. The main content is server-rendered in the HTML, though some interactive elements use JavaScript (SPA). The page contains the core EHI export documentation with no downloadable files (PDFs, ZIPs, etc.) linked.

### Step 3: Identify sidebar documentation pages
The ReadMe.io sidebar shows the following pages under "Guides":

**DOCUMENTATION**
- Electronic Health Information Export (the main EHI page)

**DATA IMPORT**
- Patient Demographic (PM)
- Insurance Import (PM)
- CPT and Fee Schedule
- Service Location (PM)
- Referring Physician
- Appointments

**CLINICAL DATA IMPORT (ALT)**
- Document Upload
- Problem List
- Allergy & Intolerance
- Immunization Records

All sidebar pages are *import* specifications (for onboarding/data migration), not export documentation. However, they document the data model and field specifications of what smartEMR stores, which is relevant context for assessing EHI export coverage.

### Step 4: Check API Reference section
Navigated to `https://smartemr.readme.io/reference`. This is a separate section documenting the FHIR R4 API (the g(10) certified API), covering:
- Getting started, error handling, capability statement
- SMART on FHIR launch (EHR Launch, Standalone Launch)
- OAuth 2.0 authorization flow
- FHIR resource endpoints: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation, Organization, Practitioner, Procedure

The FHIR API is entirely separate from the CDA-based EHI export described on the (b)(10) page. No bulk data or batch export endpoints are documented in the API reference.

### Step 5: Check for downloadable files
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' \
  electronic-health-information-export-b10.html
```
Result: No downloadable files found on the EHI export page or any sidebar pages. No PDFs, ZIPs, schemas, or sample data files are linked anywhere on the site.

### Step 6: Check mandatory disclosures page
Fetched `https://app.smartemr.com/smartemr_dot_com/smartemr.html`. This is a standard ONC mandatory disclosures page listing certification info. No EHI export documentation or links to additional technical documentation. Contains a link to "smartEMR v7.2 considerations" but no EHI-specific content.

### Step 7: Full-page screenshot
Captured a full-page screenshot of the EHI export page showing all content.

## What Was Found

The EHI export documentation consists of a **single page** on smartemr.readme.io describing two export mechanisms:

### 1. CDA Format Export (Clinical Document Architecture)
The primary clinical data export uses HL7 CDA format. Key characteristics:
- **Per-encounter CDA files**: Each patient encounter generates a separate CDA document
- **Consolidated CDA**: A combined CDA file amalgamating all encounters for a patient is also available
- **Access path**: Admin Panel → Export Options → Patient Data → Create a backup/export
- **Options**: Single patient or all patients; one-time or recurring schedule; filter by date of service
- **Standard**: References HL7 CDA (links to hl7.org product page)

### 2. Document Repository Export
A separate export for scanned/uploaded documents:
- **Content**: Signed encounter notes, lab results, radiology reports, and other scanned/uploaded documents
- **Formats**: PDF, JPG, PNG files
- **Organization**: Files sorted by patient chart ID number folders, with category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.)
- **Access path**: Admin Panel → Export Options → Patient Document Data (b10)
- **Selection**: Single patient or all patients; creates a "Portable" package

### What is NOT documented
- No data dictionary or field-level schema for the CDA export
- No sample CDA files or example output
- No specification of which CDA sections are included
- No mapping between smartEMR data fields and CDA elements
- No documentation of what specific clinical data elements are included in each CDA section
- No schema files (XSD, JSON Schema, etc.)
- No description of the export file/folder structure beyond the document repository
- No API or programmatic access documentation for the export
- No versioning or format version history

### Additional context from sidebar pages
While the sidebar pages document data *import* (not export), they reveal the data model of what smartEMR stores. These pages provide field-level specifications with data types, max lengths, required flags, and validation rules for:
- Patient demographics (30 fields: MRN, name, DOB, SSN, address, phone, gender, insurance info)
- Insurance payer directory (6 fields)
- CPT/Fee schedule (2 fields: procedure code, fee amount)
- Service locations (10 fields: name, address, NPI, Medicare, CLIA)
- Referring physicians (3 fields: name, NPI)
- Appointments (6 fields: patient ID, type, reason, resource, date, comments)
- Document uploads (12 fields: patient ID, document metadata, category, file content)
- Problem lists (5 fields: patient ID, ICD-10 code, date, active status, provider)
- Allergy & intolerance (11 fields: patient ID, substance, reaction, severity with RxNorm/SNOMED mappings)
- Immunization records (page exists but is empty — no content)

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered by the CDA export:**
- Clinical encounter documentation (one CDA per encounter)
- Whatever structured clinical data is included in the CDA sections (unspecified)

**Covered by the Document Repository export:**
- Signed encounter notes (as scanned/uploaded documents)
- Lab results (as documents)
- Radiology reports (as documents)
- Other scanned/uploaded documents

**Likely missing or undocumented:**
- **Billing data**: SmartEMR is explicitly marketed as a combined EMR + billing system with Superbill generation, electronic claims, and revenue cycle management. The EHI export documentation makes no mention of billing data, claims, charges, payments, or Superbill exports. This is a significant gap — billing records are squarely within the designated record set.
- **Medications/prescriptions**: SmartEMR integrates with Surescripts for e-prescribing. While medication data might be embedded in CDA encounter documents, there is no explicit documentation that prescription history, medication lists, or e-prescribing records are included.
- **Insurance/enrollment data**: The import specs show 30+ fields of patient demographic and insurance data. Whether this is included in the CDA export is not documented.
- **Scheduling/appointment data**: Import specs show appointment fields. Not documented in export. (Note: appointment data is generally operational, not EHI, so this is a minor concern.)
- **Clinical quality measure data**: The product is certified for 14 CQMs. CQM calculations are likely not EHI, but the underlying clinical data used in CQM reporting should be exported.
- **Specialty-specific clinical data**: The product markets itself for many specialties (cardiology, dermatology, pediatrics, orthopedics, etc.) with "specialty-specific" templates. Whether specialty-specific clinical data beyond standard CDA sections is captured in the export is not documented.

**Critical unknown — the CDA content question:**
The fundamental problem with this documentation is that it says the export uses CDA format but never specifies which CDA sections, templates, or data elements are included. A CDA document can range from a minimal discharge summary to a comprehensive C-CDA with dozens of sections. Without knowing the CDA template or section inventory, it's impossible to assess whether the export covers the full breadth of data smartEMR stores.

### Export Format & Standards

**Format**: HL7 CDA (Clinical Document Architecture) for structured clinical data, plus raw document files (PDF/JPG/PNG) for the document repository.

**Assessment**: CDA is a recognized healthcare interoperability standard, which is a positive choice. However:
- CDA is fundamentally a *clinical document* format. It is well-suited for encounter summaries, clinical notes, and US Core-style clinical data. It is **not** well-suited for billing data, claims, fee schedules, or administrative data that SmartEMR stores.
- The documentation does not specify whether this is a C-CDA (Consolidated CDA with specific templates like CCD, Discharge Summary, etc.) or a generic CDA document with custom sections.
- No CDA template OIDs, implementation guide references, or conformance claims are provided.
- The choice of CDA strongly suggests this export covers **clinical encounter data only**, not the full designated record set. A vendor doing true (b)(10) export of *everything* would need a format that handles billing, administrative, and operational patient data — areas where CDA has no standard sections.

**Could a third party reconstruct the record?** Partially. The document repository export provides raw files with folder organization. But without a data dictionary for the CDA content, a receiver would need to parse the CDA and hope the sections are well-structured. Billing and administrative data appear to be absent entirely.

### Documentation Quality

**Very sparse.** The entire EHI export documentation is a single page with approximately 200 words of content. Key deficiencies:

- **No data dictionary**: The import pages have detailed field specifications, but the export page has none. There is no mapping between stored data fields and export output.
- **No sample files**: No example CDA documents, no sample directory listings, no example output of any kind.
- **No schema or template specification**: The CDA standard allows enormous variation. Without specifying the CDA template, sections, or coded entries, the documentation is essentially saying "we export CDA" without saying what's in it.
- **No technical depth**: No information about file encoding, character sets, naming conventions, file sizes, or error handling.
- **No versioning**: The page was "Updated 11 months ago" but there is no version history or changelog.
- **Minimal user guidance**: The export paths (Admin Panel → Export Options → ...) provide the navigation steps but no screenshots, no explanation of options, no troubleshooting guidance.

A developer attempting to build an import for this export would have almost no useful technical information to work from. They would need to obtain a sample export and reverse-engineer the CDA structure.

### Structure & Completeness

**Field-level documentation**: None for the export. The import pages document 85 fields across 9 data models, but there is no equivalent documentation for what the export produces.

**Value sets and coded fields**: Not documented for the export. The import pages reference ICD-10-CM, RxNorm, and SNOMED CT for clinical coding, suggesting the system uses these standards, but the export documentation does not specify which code systems appear in the CDA output.

**Relationships between entities**: Not documented.

**Overall assessment**: This is a compliance checkbox rather than genuine export documentation. The vendor has certified for (b)(10) and registered a URL, but the documentation provides almost no technical substance about what the export actually contains. The import pages on the same site show the vendor is capable of producing detailed field specifications — the asymmetry between the import documentation (detailed, structured, with data types and validation rules) and the export documentation (a few sentences) is striking.

### (b)(10) vs (g)(10) Assessment

This vendor does **not** appear to be conflating (b)(10) with (g)(10). The FHIR API documentation is in a separate "API Reference" section and is clearly labeled as the FHIR R4 API. The EHI export page explicitly references §170.315(b)(10) and describes a CDA-based export that is distinct from the FHIR API.

However, the CDA export may still only cover US Core-equivalent clinical data (the same scope as what the FHIR API provides, just in a different format). Without a data dictionary or section inventory for the CDA export, it's unclear whether it goes beyond the standard clinical summary data that would be available via the (g)(10) FHIR API. The absence of any mention of billing data, claims, or administrative records in the export is a red flag that this may be a clinical-only export rather than a true "all EHI" export.

## Access Summary
- Final URL: https://smartemr.readme.io/docs/electronic-health-information-export-b10 (no redirects)
- Status: found
- Required browser: no (content is server-rendered, though some pages need JS for full rendering)
- Navigation complexity: direct_link (single page, no expandable sections)
- Anti-bot issues: none (Cloudflare present but does not block curl with User-Agent)

## Obstacles & Dead Ends
- The FHIR sandbox endpoint (`https://ezedev.smartemr.com/fhir_sburl/metadata`) timed out when attempting to fetch the CapabilityStatement. This is the (g)(10) API and not directly relevant to the (b)(10) export.
- The Immunization Records page under "Clinical Data Import" exists in the sidebar but has no content (empty page).
- No downloadable files (PDFs, schemas, sample data) are available anywhere on the site.
- The mandatory disclosures page at `https://app.smartemr.com/smartemr_dot_com/smartemr.html` contains only standard certification info, no EHI-specific documentation.
