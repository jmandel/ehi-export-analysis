# Procentive (Ensora Health) — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://ensorahealth.com/onc/procentive/
- CHPL ID: 11155
- Certification Number: 15.04.04.2214.Proc.02.01.1.221228
- Certified Date: 2022-12-28
- Developer: Procentive (now under Ensora Health / Therapy Brands)

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://ensorahealth.com/onc/procentive/" -H 'User-Agent: Mozilla/5.0'
```
HTTP/2 200. WordPress-based page hosted on Kinsta via Cloudflare. Content-Type: text/html; charset=UTF-8. No redirect — the registered URL is live.

### Step 2: Examine the page content
The page is titled "ONC - Procentive | Ensora Health" and is a single-page certification disclosure hub with the following sections:

1. **Procentive by Ensora Health** — developer/product info, certification number
2. **ONC Certification Criteria for Health IT** — standard compliance statement
3. **Attestation Disclosure** — lists certified criteria, shows certificate image
4. **Electronic Health Information (EHI) Export** — describes single-patient and population exports, links to a "File Formats" PDF
5. **FHIR Endpoints** — links to fhir.procentive.com home, API docs, and service base URL list
6. **ONC Real World Testing** — links to a separate page (not downloaded, out of scope)

### Step 3: Download the EHI File Formats PDF
```bash
curl -sL "https://ensorahealth.com/wp-content/uploads/2025/03/PDF-for-Website-on-Formats-1.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/PDF-for-Website-on-Formats-1.pdf
```
Verified: PDF document, 1 page, 112KB. Author: Catherine Baker. Created 2023-11-30 via Microsoft Word.

### Step 4: Explore FHIR documentation at fhir.procentive.com
The EHI export section on the ONC page mentions "standardized file formats" (XML, CSV, PDF) but the FHIR endpoints section links to the same FHIR server used for (g)(10). I investigated whether the FHIR API is part of the EHI export mechanism:

- **FHIR Home**: https://fhir.procentive.com/ — "DYNAMIC FHIR SERVER - 4.0.1", powered by Dynamic Health IT's ConnectEHR v4 + BulkFHIR4
- **API Documentation**: https://fhir.procentive.com/procentive/basepractice/r4/Home/ApiDocumentation — extensive 686KB HTML page documenting SMART on FHIR API, USCDI resource mapping, and Bulk Export
- **CapabilityStatement**: https://fhir.procentive.com/fhir/procentive/basepractice/r4/metadata — 19KB JSON
- **SMART Configuration**: https://fhir.procentive.com/fhir/procentive/basepractice/r4/.well-known/smart-configuration
- **Service Endpoints**: https://fhir.procentive.com/fhir/r4/endpoints — FHIR Bundle with one endpoint (Procentive base practice)

All of these were fetched and saved.

### Step 5: Screenshots
- Full-page screenshot of ONC certification page
- Viewport screenshot of FHIR API documentation page
- PDF rendered as PNG for visual confirmation

## What Was Found

### EHI Export Description (from ONC page)

The page describes two export modes:

1. **Single Patient Export**: "Procentive EHR allows a user to export electronic health information (EHI) for a single patient without developer assistance using the following standardized file formats."
2. **Patient Population Export**: "Procentive EHR can export all the data for a patient population using the following standardized formats. This export can be requested by submitting a support ticket via Salesforce."

The page notes that export content "might vary" based on: software applications in use, software version, documentation practices, configuration decisions, and whether the health system included materials not sourced from the application.

### File Formats PDF

The linked PDF (1 page) describes three "standardized computable formats" the export may include:
- **XML** — generic description of XML markup language
- **CSV** — generic description of comma-separated values
- **PDF documents** — generic description of Portable Document Format

This is the entirety of the EHI-specific (b)(10) documentation. There is no data dictionary, no field listing, no schema, no description of what tables or data elements are included, no sample files, no instructions on how to perform the export, and no description of how the XML or CSV files are structured.

### FHIR API Documentation (g)(10), also linked from EHI page)

The FHIR API documentation is provided by Dynamic Health IT's ConnectEHR platform and covers the (g)(10) SMART on FHIR API. Key details:

**USCDI-mapped FHIR Resources** (from the API documentation mapping table):
| USCDI Category | FHIR Resource |
|---|---|
| Patient Demographics | Patient |
| Problem List | Condition |
| Procedures | Procedure |
| Smoking Status | Observation |
| Vital Signs | Observation |
| Laboratory Results | Observation |
| Laboratory Tests / DiagnosticReport | DiagnosticReport |
| Goals | Goal |
| Immunizations Information | Immunization |
| Assessment and Plan of Treatment | CarePlan |
| Care Team Member(s) | CareTeam |
| Medications | MedicationRequest |
| Allergies and Intolerances | AllergyIntolerance |
| Unique Device Identifier(s) | Device |
| Clinical Notes (Consultation, Discharge Summary, H&P, Progress Note, others) | DocumentReference |
| Practitioner | Practitioner, PractitionerRole |
| Encounter | Encounter |
| Location | Location |
| Organization | Organization |

**Additional resources in CapabilityStatement** (not in USCDI mapping table):
- ClinicalImpression
- Binary
- Provenance
- Composition
- Group (for bulk export operations)

**Bulk Export Support**:
- Patient-level: `GET [fhir base]/Patient/$export`
- Group-level: `GET [fhir base]/Group/[id]/$export`
- Uses JWT-based backend authentication (client_credentials flow)
- Output format: NDJSON (application/fhir+ndjson)

The API documentation explicitly states: "Available data via the API interface is limited by the data defined by the USCDI" and "DYNAMIC FHIR API assumes the use of a cumulative C-CDA with patient data."

## Export Coverage Assessment

### Data Domain Coverage

This is a **behavioral health EHR** that stores extensive clinical, billing, scheduling, and specialty-specific data. Comparing the product research against the export documentation:

**Clearly covered by FHIR API (USCDI subset only)**:
- Patient demographics
- Problem lists / conditions (including DSM-5 diagnoses)
- Medications and prescriptions
- Allergies
- Vital signs
- Clinical notes (via DocumentReference)
- Care plans / goals
- Immunizations
- Encounters
- Lab results (if applicable)

**Missing or not mentioned in any export documentation**:
- **Billing/claims data** — charges, payments, claims, denials, appeals, EOBs. This is a core function of Procentive. No mention in export docs.
- **Treatment plans** — Procentive has Practice Planners and evidence-based treatment plan tools specific to behavioral health. These may partially map to CarePlan but the behavioral health-specific structure would be lost.
- **Bed management data** — a dedicated module tracking client stays, bed status, capacity, waitlists. Not mentioned.
- **Scheduling/appointment data** — while appointment data per se may not be part of the designated record set, encounter history is relevant and only partially covered by the FHIR Encounter resource.
- **Clinical assessments** — behavioral health assessments, intake/discharge workflows, group therapy notes. These are specialty-specific clinical data central to the product. Only generic DocumentReference is available.
- **E-prescribing records** — EPCS data for controlled substances. Only MedicationRequest is available via FHIR.
- **Portal data** — secure messages between clients and staff.
- **Reporting/census data** — clinical outcomes, utilization data.
- **Custom forms and templates** — Procentive supports customizable clinical notes and templates.

The fundamental problem: the EHI export page describes XML/CSV/PDF as possible formats but provides zero detail about what data these formats contain. The FHIR API is explicitly limited to USCDI data. There is no documentation of an export mechanism that covers data beyond USCDI — which is what (b)(10) requires.

### Export Format & Standards

The export documentation describes two distinct mechanisms that are not clearly connected:

1. **EHI Export (b)(10)**: Described as producing XML, CSV, and/or PDF files. No further detail on structure, schema, or content. No sample files.
2. **FHIR API (g)(10)**: Well-documented SMART on FHIR R4 API with Bulk Export capability. Limited to USCDI data elements.

The relationship between these two is unclear. The ONC page lists them as separate sections, suggesting the EHI export (item 1) is a separate mechanism from the FHIR API (item 2). But the EHI export mechanism has essentially no documentation beyond "it produces files in XML/CSV/PDF format."

A third party receiving an export would have no way to understand or import the XML or CSV data without additional documentation of the schema. The FHIR output is standard and well-structured but only covers USCDI.

### Documentation Quality

**EHI Export (b)(10) documentation**: Extremely minimal. One 1-page PDF that describes what XML, CSV, and PDF are in generic terms. No data dictionary. No field definitions. No schema. No sample files. No instructions for performing the export. No description of which data domains are included. A developer receiving these export files would have no reference material to understand the data structure.

**FHIR API (g)(10) documentation**: Comprehensive. The 686KB API documentation page includes complete USCDI-to-FHIR mapping, detailed search parameters, example request/response payloads for every resource type, authentication setup (SMART on FHIR + Backend Services), and Bulk Export workflow. This is a well-documented (g)(10) implementation. However, it is explicitly scoped to USCDI data only.

### Structure & Completeness

- **Field-level documentation**: None for the (b)(10) export. The FHIR API docs have complete field-level examples but only for USCDI resources.
- **Value sets/coded fields**: Not documented for (b)(10). Standard FHIR code systems referenced for (g)(10).
- **Relationships between entities**: Not documented for (b)(10). Standard FHIR references for (g)(10).
- **Data dictionary**: Does not exist for either mechanism. The FHIR mapping table is the closest thing, but it maps to standard USCDI rather than documenting Procentive-specific data structures.
- **Versioning**: No change history or versioning information.

### Summary Assessment

Procentive's EHI export documentation exemplifies the (b)(10) vs. (g)(10) confusion. The vendor has invested significantly in their FHIR API (via Dynamic Health IT's ConnectEHR platform), producing thorough (g)(10) documentation. But the actual (b)(10) export — which is supposed to cover all electronic health information including billing, behavioral health assessments, bed management, treatment plans, and other specialty-specific data — has essentially no documentation.

The EHI export section on the ONC page describes single-patient and population export capabilities that produce XML/CSV/PDF files, but the sole technical document is a 1-page PDF explaining what XML, CSV, and PDF file formats are. This represents a significant documentation gap for a product that stores extensive behavioral health, substance use recovery, billing, and practice management data.

For a behavioral health EHR that serves residential treatment facilities with bed management, EPCS, and 120+ report types, the absence of any documentation describing what data elements are included in the EHI export — and how they're structured — makes the export practically unusable for a receiving party.

## Access Summary
- Final URL (after redirects): https://ensorahealth.com/onc/procentive/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (PDF one click away; FHIR docs one click away)
- Anti-bot issues: none (Cloudflare present but not blocking)

## Obstacles & Dead Ends
- No obstacles. All URLs resolved correctly.
- The "File Formats" button on the ONC page was the only EHI-specific download link.
- The FHIR API documentation is hosted on a separate domain (fhir.procentive.com) via Dynamic Health IT's ConnectEHR platform.
- The patient population export requires "submitting a support ticket via Salesforce" — this is not a self-service export for population-level data.
