# Enable Healthcare Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://provider.ehiehr.com/EHI_DATA_EXPort_GUIDE.pdf
- CHPL IDs: 10247
- Product: MDnet V10
- Developer: Enable Healthcare Inc.

## Navigation Journal

**Step 1: Probe the registered URL.**
```bash
curl -skI -L "https://provider.ehiehr.com/EHI_DATA_EXPort_GUIDE.pdf" \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```
Result: HTTP 200, Content-Type: application/pdf, Content-Length: 904203. Direct PDF download. Note: the SSL certificate has issues (curl exits 60 without `-k`), but the content is served correctly over HTTPS.

**Step 2: Download the PDF.**
```bash
curl -sk -L "https://provider.ehiehr.com/EHI_DATA_EXPort_GUIDE.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/EHI_DATA_EXPort_GUIDE.pdf
```
Verified: `file` confirms "PDF document, version 1.7, 9 page(s)", 904,203 bytes.

**Step 3: Extract and read PDF text.**
```bash
pdftotext downloads/EHI_DATA_EXPort_GUIDE.pdf -
```
Title: "DATA INTEROPERABILITY & EHI DATA EXPORT GUIDE", published by Enable Healthcare Inc., Copyright 2023. Author: Rahul Dewan. Created: 2023-12-28. 9 pages.

**Step 4: Follow referenced data dictionary URL.**
The PDF references a CSV data dictionary at `https://emr.ehiconnect.com/docs/`. This URL returns HTTP 404. Tried variations (`/docs`, `/doc/`, root) — all 404 or 403. Checked Wayback Machine CDX API — no captures exist. The data dictionary referenced in the documentation is not publicly accessible.

**Step 5: Check FHIR portal.**
The PDF references `https://fhir.ehiconnect.com/ehifhirportal/` for FHIR API registration, documentation, and testing sandbox. This loads a React SPA with three cards: Testing Sandbox, Registration, and Documentation. The Documentation link points to `https://ehifire.ehiconnect.com/ehi/basepractice/r4/Home/ApiDocumentation`.

**Step 6: Check FHIR API documentation page.**
Navigated to the documentation page. It is a "Dynamic FHIR" branded page (by Dynamic Health IT, apparently a third-party FHIR platform). Contains standard FHIR R4 API documentation: SMART on FHIR authorization, resource endpoints, and Bulk Export client configuration. The supported FHIR resources (from the CapabilityStatement) are the standard US Core set: Patient, Condition, Procedure, Observation, DiagnosticReport, Goal, Immunization, CarePlan, CareTeam, MedicationRequest, AllergyIntolerance, Device, DocumentReference, Binary, Practitioner, PractitionerRole, Encounter, Location, Organization, Group, ClinicalImpression, Provenance, ServiceRequest, RelatedPerson, Specimen, Coverage, MedicationDispense. This is the (g)(10) Standardized API, not a dedicated (b)(10) EHI export mechanism.

**Step 7: Download FHIR CapabilityStatement.**
```bash
curl -sk "https://ehifire.ehiconnect.com/fhir/ehi/basepractice/r4/metadata" \
  -H 'Accept: application/fhir+json' \
  -o downloads/fhir-capability-statement.json
```
Confirms FHIR R4 (4.0.1), 27 resource types — all standard US Core.

**Step 8: Check for additional documentation.**
- `provider.ehiehr.com/` root is a default IIS Windows Server page
- Probed common paths on provider.ehiehr.com: `/ehi`, `/docs`, `/export`, `/b10`, `/compliance`, `/data-dictionary` — all 404
- `emr.ehiconnect.com/` root returns 403; no alternative paths work
- `www.ehiehr.com` is a Wix-based marketing site; no EHI export documentation found
- No Wayback Machine captures exist for any of these URLs

## What Was Found

The primary artifact is a 9-page PDF titled "DATA INTEROPERABILITY & EHI DATA EXPORT GUIDE" (dated December 2023). It describes the scope and methods of EHI export from MDnet V10.0.

### Scope Statement
The document states the export covers:
- **Health data** stored in MDNet v10.0 captured by the practice or received electronically related to a medical record
- **Financial data** stored in MDNet v10.0 captured by the practice or received electronically, including "claim, adjudication and all other related data sets"

This is a notable and positive scope statement — it explicitly includes financial data alongside clinical data.

### Export Methods
The document describes **eight** export methods:

1. **FHIR APIs** — Standard FHIR R4 API at `https://fhir.ehiconnect.com/ehifhirportal/`. This is the (g)(10) certified API covering US Core resources.

2. **C-CDA R2.1 bulk or single export** — An integrated "CCDA Export Tracker" in MDnet allows authorized users to set up one-time or scheduled exports. Options include full set, partial date-based, partial segment-based, or incremental updates. The C-CDA covers 20 clinical sections: Allergy, Assessment, Encounters, Family History, Functional Status, Cognitive Status, Immunizations, Medical Equipment, Medications, Lab Results, Problems, Procedures, Reason for Visit, Referrals, Social History, Vitals, Care Plan, Goal, Health Concern, Clinical Instructions.

3. **CSV full data set export** — MDnet allows authorized users to request "detailed export of health, activity and financial data related to a specific patient or all patients" in CSV format. The document references a data dictionary at `https://emr.ehiconnect.com/docs/` — but this URL is dead (404).

4. **HL7 2.x/3.x ADT** — Real-time patient chart creation and demographic/payer updates.

5. **HL7 2.x SIU** — Real-time appointment scheduling updates.

6. **HL7 2.x DFT** — Real-time financial transaction updates (note: the document description appears to repeat the SIU description for DFT — likely a copy-paste error).

7. **JSON-based exchange for scanned documents** — Real-time exchange of scanned documents, faxes, and custom reports using JSON with BASE-64 encoded content.

8. **EDI 837P and 835 Claims files** — Continuous feed of claim and remittance files.

### Optional Data Exchange Service
Pages 5–9 describe an optional "Announce & Deliver" data exchange service using C-CDA R2.1 with incremental updates. It supports multiple transport mechanisms (VPN P2P tunnels, SFTP, web services) and includes a detailed use case walkthrough showing how incremental C-CDA updates work as patient data changes over time.

### What's Missing
- **The CSV data dictionary** — the most important artifact for understanding the (b)(10) export — is referenced but the URL returns 404. No alternative location was found.
- **No schema files** — no XSD, JSON Schema, OpenAPI specs, or other machine-readable format definitions
- **No sample export files** — no example CSVs, C-CDAs, or JSON payloads
- **No screenshots of the export interface** — the document references "training videos embedded into MDNet" but these are behind authentication

## Export Coverage Assessment

### Data Domain Coverage

Enable Healthcare's documentation is notably broad in *stated* scope. The PDF explicitly says the export covers both health data and financial data, which is the right framing for (b)(10). However, the documentation quality varies dramatically by export method:

**Clearly covered (via C-CDA R2.1):**
- Allergies, Problems, Medications, Immunizations, Lab Results, Procedures, Vitals, Encounters — standard clinical data
- Care Plans, Goals, Health Concerns, Referrals, Social History, Family History — broader clinical context
- Assessment, Functional Status, Cognitive Status, Clinical Instructions — less commonly documented
- Medical Equipment (implantable devices) — per (a)(14) certification

**Claimed but undocumented (via CSV export):**
- "Health, activity and financial data" — the CSV export is described as covering everything, but the data dictionary URL is dead. Without the data dictionary, there's no way to verify what fields, tables, or data domains the CSV export actually includes.

**Covered via specialized mechanisms:**
- Claims data (EDI 837P/835) — billing/financial data via dedicated EDI feed
- Scanned documents and faxes — via JSON-based exchange
- Scheduling data — via HL7 SIU messages
- Demographics and payer data — via HL7 ADT messages

**Likely missing or unclear:**
- **Audit logs** — no mention in any export method, despite being stored per (d) criteria certification
- **Patient portal messages** — secure messaging between patients and providers not mentioned
- **Care coordination data** — CCM, RPM, population health program data not specifically addressed
- **Telehealth session data** — not mentioned
- **Clinical quality measure data** — not mentioned
- **E-prescribing transaction history** — prescriptions are in C-CDA medications section, but the full e-prescribing workflow data (pharmacy responses, fill status, etc.) is unclear
- **User/provider activity data** — login history, workflow data
- **Practice management data** — beyond scheduling (check-in status, queue management, etc.)

### Export Format & Standards

The export uses a **multi-format approach**, which is both a strength and a weakness:

- **C-CDA R2.1** for clinical data — a recognized standard, widely implementable. The 20 listed sections are comprehensive for clinical data. However, C-CDA inherently cannot represent all the data MDnet stores (billing, audit logs, administrative data).
- **CSV** for the complete dataset — this would be the most appropriate format for a true (b)(10) export covering everything. But the data dictionary is inaccessible, making the CSV export essentially undocumented.
- **EDI 837P/835** for claims — standard billing format, appropriate for financial data
- **HL7 v2 messages** (ADT, SIU, DFT) — these are real-time transaction feeds, not bulk export formats. They're more suited for ongoing data exchange than a point-in-time export of all records.
- **JSON** for scanned documents — proprietary format with BASE-64 encoded content

The multi-format approach means a data consumer would need to integrate 5+ different formats to reconstruct a complete patient record. There's no single export mechanism that produces everything.

A third party could plausibly reconstruct the clinical record from C-CDA exports and piece together billing data from EDI files, but there's no documentation of how these different export streams relate to each other or how to correlate records across formats.

### Documentation Quality

The documentation is **mediocre to poor** overall:

- **Strengths:** The PDF provides a useful high-level overview of all available export methods. The C-CDA incremental update use case (pages 6-9) is genuinely helpful in explaining how the incremental data exchange works. The scope statement explicitly mentioning financial data is good.
- **Weaknesses:**
  - The most critical artifact — the CSV data dictionary — is missing (404 URL). Without field-level documentation of the CSV export, the claimed "full data set" export is unverifiable.
  - No sample files or examples for any format
  - No machine-readable schemas
  - The HL7 DFT section appears to be a copy-paste error (repeats the SIU description)
  - Training videos are behind authentication in MDNet
  - The document reads more like a sales/implementation overview than technical export documentation
  - Created in December 2023 from a Word document — appears to be a one-time compliance artifact, not maintained documentation

### Structure & Completeness

- **C-CDA sections** are listed by name (20 sections) but not documented at the field level — the vendor relies on the C-CDA R2.1 standard specification
- **CSV export** has no accessible field-level documentation at all
- **No value sets** documented for coded fields
- **No relationship mapping** between the different export formats
- **No versioning or change history**
- **No data type specifications** beyond what's implicit in the format standards (C-CDA, EDI)

### Overall Assessment

Enable Healthcare has made a credible attempt at addressing (b)(10) EHI export — the scope statement is correct, they've described multiple export mechanisms including one (CSV) that could cover everything, and they've included financial data alongside clinical data. This puts them ahead of vendors who simply point to their FHIR API.

However, the execution falls short in a critical way: the CSV data dictionary that would validate the "full data set" claim is inaccessible. The primary documentation is a 9-page overview PDF that describes capabilities at a high level without providing the technical detail needed to actually consume the exports. A developer receiving these files would need substantial back-and-forth with Enable Healthcare to understand the CSV structure, field definitions, and how to correlate data across the multiple export formats.

The reliance on multiple specialized formats (C-CDA for clinical, EDI for billing, HL7 v2 for ADT/scheduling, JSON for documents) rather than a single comprehensive export also increases implementation complexity. Each format covers a slice of the data, but there's no unified view.

## Access Summary
- Final URL (after redirects): https://provider.ehiehr.com/EHI_DATA_EXPort_GUIDE.pdf
- Status: found
- Required browser: no (direct PDF download via curl with -k flag for SSL)
- Navigation complexity: direct_link
- Anti-bot issues: SSL certificate issue (curl requires -k flag), otherwise none

## Obstacles & Dead Ends
- **SSL certificate issue**: `curl` without `-k` fails with exit code 60. The certificate is accepted by browsers but not by curl's default CA bundle. Using `-k` (insecure) flag works.
- **Dead data dictionary URL**: `https://emr.ehiconnect.com/docs/` returns HTTP 404. This is the most significant obstacle — the CSV export data dictionary referenced in the main PDF is not accessible. Tried variations of the URL and Wayback Machine — no captures exist.
- **No Wayback Machine captures**: Neither provider.ehiehr.com nor emr.ehiconnect.com/docs/ have any Wayback Machine captures.
- **Wix-based marketing site**: ehiehr.com is rendered client-side via Wix, making it difficult to search for additional documentation programmatically. No EHI-specific content was found.
