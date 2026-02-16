# TechSoft, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: http://www.mdrhythm.com/onc-compliance.html
- CHPL ID: 9797
- Product: MDRhythm Version 8
- Certification date: 2018-12-08

## Navigation Journal

1. Probed the registered URL with curl:
```bash
curl -sI -L "http://www.mdrhythm.com/onc-compliance.html" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, Content-Type: text/html, 18,297 bytes. Server: Microsoft-IIS/10.0.

2. Downloaded and examined the HTML page source. Found a static compliance page with two key document links near the bottom:
   - `MDR-FHIR-API-Documentation.pdf` — linked as "MDRhythm FHIR API Documentation"
   - `MDRhythm B10 Data Export Instructions.pdf` — linked as "MDRhythm B.10 Data Export Documentation"

3. Downloaded the B10 export documentation:
```bash
curl -sL "http://www.mdrhythm.com/MDRhythm%20B10%20Data%20Export%20Instructions.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o "MDRhythm B10 Data Export Instructions.pdf"
```
Confirmed: PDF document, version 1.5, 3 pages, 573,452 bytes. Author: Jaimin Patel, created 2023-11-27 via Microsoft Word 2010.

4. Downloaded the FHIR API documentation:
```bash
curl -sL "http://www.mdrhythm.com/MDR-FHIR-API-Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o "MDR-FHIR-API-Documentation.pdf"
```
Confirmed: PDF document, version 1.7, 240 pages, 1,155,008 bytes. Author: Parag, created 2022-12-05 via Microsoft Word 2019.

5. Saved the ONC compliance page HTML and took a full-page browser screenshot.

6. Examined all embedded URLs in both PDFs. The B10 PDF references only `https://patientdata.mdronline.net` (the export portal). The FHIR API PDF references external HL7/FHIR standard URLs and the MDRhythm FHIR API base URL `https://mdrfhirapi.mdronline.net/` — all standard g(10) infrastructure, not B10-specific.

## What Was Found

### B10 Export Documentation (3-page PDF)

The B10 document describes an "on demand Data Export" mechanism via a web-based portal called "Practice Patient Data" at `https://patientdata.mdronline.net`. The export process is:

1. A practice user logs into the portal with practice credentials.
2. They select one or more patients (max 5 per export batch).
3. They click an "Export EHR" button in the top-right corner.
4. All selected patients' data is exported into a **single PDF file**, named with a unique practice code.

The documentation explicitly lists the data included in the export:
- Patient Demographics
- Allergy Details
- Current Medication Details and Medication History
- Diagnosis and Problem Information
- Visit Note Information (organized by visit with Subjective, Objective, Assessment, and Plan sections)
- Vitals Information

The document includes two screenshots: one showing the patient selection interface (a table listing patients with checkboxes and an "Export EHR" button), and one showing an example of exported patient data in PDF format. The example export shows a visit note with demographics, allergies, medical history, a meds review, vitals, physical exam, assessment with diagnosis/procedure codes, plan with diagnostic tests and current medications, and plan of care entries.

**The export format is PDF** — a human-readable but not machine-parseable format. There is no data dictionary, no schema, no field-level documentation. The PDF shows a rendered clinical summary, not structured data.

### FHIR API Documentation (240-page PDF)

This is a standard g(10) FHIR API documentation document. It covers:
- SMART App Launch 2.0.0 with OAuth 2.0 authentication
- US Core 5.0.1 / USCDI v2 conformance
- Bulk Data 2.0.0 support
- FHIR R4 resources: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, ServiceRequest

Each resource section includes request/response examples with full JSON FHIR resource instances. The documentation is detailed for API developers.

**This is g(10) documentation, not b(10) documentation.** It is the standardized FHIR API for patient and population services, not the EHI export mechanism. The vendor has separate documentation for each.

## Export Coverage Assessment

### Data Domain Coverage

The B10 export covers a **narrow subset** of what MDRhythm stores. Based on the product research, MDRhythm is a comprehensive ambulatory EHR with integrated practice management, billing, e-prescribing, pharmacy/inventory, document management, and patient portal. The export covers:

**Clearly covered:**
- Patient demographics
- Allergies
- Medications (current and history)
- Diagnoses/problems (with ICD codes visible in the example)
- Visit notes (SOAP format with subjective, objective, assessment, plan)
- Vitals
- Procedure codes (CPT codes visible in the example export)
- Plan of care entries
- Goals (visible in the example under "Plan Of Care")

**Clearly missing from the export documentation:**
- **Billing and financial data** — No claims, charges, payments, insurance information, prior authorizations. This is particularly notable because MDRhythm's practice management/billing system is the *original core* of the product, predating the EMR component.
- **Lab results** — The B10 documentation does not mention lab results or diagnostic reports as exported data categories, though the sample shows a "Diagnostic Tests" reference under Plan.
- **Immunization records** — Not listed as an export category.
- **Prescriptions / e-prescribing history** — The medication list is included, but detailed prescription data (EPCS records, dispensing records, pharmacy communications) appears absent.
- **Pharmacy/inventory data** — For practices using in-house dispensing, this data is not mentioned.
- **Documents and images** — Scanned documents, faxes, transcription records are not mentioned.
- **Device data** — Implantable device (UDI) information is not listed.
- **Encounter history** — While visit notes are included, structured encounter data (encounter types, durations, facility information) beyond visit date/provider is unclear.
- **Care team information** — Not mentioned.
- **Patient portal data** — Portal messages, appointment requests, refill requests are not mentioned.
- **Public health reporting data** — Immunization registry submissions, syndromic surveillance data are not mentioned.

### Export Format & Standards

The export is a **PDF file** — the least computable format possible. This is essentially a printed clinical summary rendered as a document. There is:
- No structured data format (no JSON, CSV, XML, FHIR, C-CDA)
- No machine-readable schema
- No ability to programmatically parse or import the data
- No data dictionary
- No field definitions or data types
- No coded value sets (though the example shows ICD and CPT codes inline in the PDF text)

A third party could not reconstruct the patient record from this export without manual human review and re-entry. The PDF format makes this export essentially a printout, not a data exchange mechanism.

The FHIR API (g(10)) provides structured FHIR R4 JSON for the US Core subset, but that is a different mechanism covering only USCDI data classes — it does not address the full-scope b(10) requirement.

### Documentation Quality

The B10 documentation is **minimal** — 3 pages including a blank page, two screenshots, and a bullet list of 6 data categories. There is:
- No data dictionary
- No field-level documentation
- No export format specification (beyond "PDF")
- No sample export files (only a screenshot of one)
- No documentation of data types, value sets, or constraints
- No versioning or change history
- No error handling or troubleshooting guidance

A developer could not implement an import of this data based on the documentation because the export is an unstructured PDF with no schema. The documentation reads as a minimal compliance checkbox — "here's how to click the button and here's roughly what comes out."

The FHIR API documentation, by contrast, is thorough (240 pages with full request/response examples), but it documents a different system (the g(10) API).

### Structure & Completeness

- **Granularity:** The B10 documentation provides only category names (e.g., "Allergy Details", "Vitals Information") with no further breakdown of fields, data types, or structures within those categories.
- **Value sets:** Not documented at all for the B10 export.
- **Relationships:** Not documented — the PDF is a flat rendering, so inter-entity relationships are implicit in the layout.
- **Versioning:** No version number on the B10 document. Created 2023-11-27.

### Summary Assessment

TechSoft's approach to b(10) EHI export is one of the weakest possible implementations:

1. **PDF export format** makes the data essentially non-computable. A PDF of clinical notes is better than nothing but fails the spirit of enabling data portability.
2. **Limited data scope** — only 6 categories of clinical data, with no billing, scheduling, lab results, immunizations, documents, or specialty data. For a product whose *original core* is billing/practice management, the complete absence of financial data from the "all EHI" export is a significant gap.
3. **Minimal documentation** — 3 pages (one blank) with no schema, no data dictionary, no format specification.
4. **Max 5 patients per export** — the batch limit of 5 patients at a time makes bulk export of a full practice's records extremely cumbersome.
5. **Separate web portal** — the export doesn't happen within the EHR itself but through a separate web application (`patientdata.mdronline.net`), adding an additional access point.

The vendor has clearly invested more effort in their g(10) FHIR API (240 pages of documentation) than in their b(10) EHI export (3 pages). The b(10) implementation appears to be a minimal compliance effort.

## Access Summary
- Final URL (after redirects): http://www.mdrhythm.com/onc-compliance.html
- Status: found
- Required browser: no (direct PDF links work with curl)
- Navigation complexity: direct_link (two PDF links on the compliance page)
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The page loaded successfully, both PDF links worked with standard curl requests, and the documents were genuine PDFs (not HTML error pages). No authentication, Cloudflare, or other barriers.
