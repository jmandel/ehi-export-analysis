# OT EMR, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://onetouchemr.com/OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf
- CHPL IDs: 11599
- Product: OneTouch EMR, Version 3
- Certification date: 2025-02-24

## Navigation Journal

1. **Probed the registered URL with curl headers:**
   ```
   curl -sI -L "https://onetouchemr.com/OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: application/pdf, Content-Length: 1106980 bytes. Direct PDF download — no redirects, no auth required.

2. **Downloaded the PDF:**
   ```
   curl -sL "https://onetouchemr.com/OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf
   ```
   Verified with `file` command: "PDF document, version 1.4, 8 page(s)" (pdfinfo shows 159 pages). Produced by "Skia/PDF m120 Google Docs Renderer" (Google Docs export).

3. **Extracted text and examined structure:** 159-page document with Table of Contents, covering FHIR API documentation for 18 resource types, FHIR Bulk Data Access API, error responses, OAuth security, a dedicated "Electronic Health Information (EHI) Export" section (pp. 153–157), and Terms and Conditions.

4. **Checked for embedded files:** `pdfdetach -list` returned "0 embedded files."

5. **Extracted URLs from PDF text:** All vendor-specific URLs are API endpoint examples (e.g., `https://api.onetouchemr.com/fhir/r4/...`). No links to additional documentation beyond the standard HL7/FHIR specification references.

6. **Checked mandatory disclosures page:**
   ```
   curl -sL "https://www.onetouchemr.com/mu_disclosure.html" -H 'User-Agent: Mozilla/5.0'
   ```
   The disclosures page links to the same API Documentation PDF and provides the FHIR API endpoint pattern (`https://$CUSTOMER.onetouchemr.com/fhir/r4`). No additional EHI export documentation found.

## What Was Found

The registered URL is a single 159-page PDF document titled "API Documentation — OneTouch EMR Version 3." It is a comprehensive FHIR R4 API reference that also includes a dedicated section on EHI export. Here is what the document covers:

### Document Structure

1. **Introduction & Implementation Instructions** (pp. 3–4): Overview of the FHIR R4 API, base URL pattern, SMART configuration endpoints, and general implementation guidance. States the API provides access to "all data elements of a patient's electronic health record." However, the Implementation Instructions section clarifies the API covers "USCDI v1" data.

2. **Supported Profiles/Capabilities** (pp. 4–137): Detailed documentation of 18 FHIR R4 resources, each with:
   - Resource description and US Core profile reference
   - Supported attributes table (field name + description)
   - FHIR operations (Read, Search) with HTTP methods
   - Search parameters with types and descriptions
   - Worked examples with full JSON response bodies

   **Resources documented:**
   - AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance

3. **FHIR Bulk Data Access API** (pp. 139–145): Group-level `$export` endpoint, status polling, deletion, file retrieval. Output is NDJSON. Example complete response shows all 18 resource types returned as Binary resources.

4. **FHIR API Error Responses** (pp. 145–148): Standard OperationOutcome patterns.

5. **Security and Identity Verification** (pp. 148–152): OAuth 2.0 Authorization Code Flow, Client Credentials Grant Flow (for Bulk Data), supported scopes.

6. **Electronic Health Information (EHI) Export** (pp. 153–157): The dedicated (b)(10) section. Key details:
   - **Mechanism:** "OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data."
   - **Single Patient Export:** Available via Administration > General > Single Patient Export. Users with Office Manager, Practice Administrator, or System Administrator roles can trigger the export through the UI. The user enters a patient name (autocomplete), clicks "Export," monitors job status on the same page, and receives the exported data as a zipped attachment via the internal Messaging system.
   - **Export format:** ZIP file containing NDJSON files for each FHIR resource type plus a README.txt. The README lists each resource type with its US Core profile URL. Screenshot shows 19 files: README.txt + 18 NDJSON files (one per resource type, named like `AllergyIntolerance-289.ndjson`).
   - **All Patient Export:** Same format but must be requested by contacting OneTouch EMR support due to data volume.
   - **Encoding note:** PresentedForm data for DiagnosticReport and Content Attachment Data for DocumentReference are base64-encoded.
   - Screenshots included showing: Administration menu navigation, Single Patient Export page, export job in-progress, completed export message in Messaging inbox, ZIP file contents in an archive viewer, and README.txt contents.

### Data Dictionary / Field-Level Documentation

For each of the 18 FHIR resources, the PDF documents supported attributes in a two-column table (Name | Comments). These are FHIR element names with brief descriptions — not a proprietary data dictionary. For example, for Patient: identifier, name, birthDate, gender, address, telecom, communication, extension (race, ethnicity, birthsex). The level of detail is moderate — field names and brief descriptions, but no data types, cardinality, or value set enumerations beyond what's inherent in the US Core profiles.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export is explicitly built on the FHIR Bulk Data mechanism and exports exactly the same 18 US Core resource types that the (g)(10) API serves. This is a textbook example of a vendor conflating (b)(10) with (g)(10).

**Covered domains (via US Core FHIR resources):**
- Patient demographics (Patient)
- Allergies (AllergyIntolerance)
- Conditions/problems/diagnoses (Condition — problem-list-item, encounter-diagnosis, health-concern)
- Medications (MedicationRequest)
- Lab results (Observation — laboratory category)
- Vital signs (Observation — vital-signs category)
- Immunizations (Immunization)
- Procedures (Procedure)
- Encounters (Encounter)
- Care plans and goals (CarePlan, Goal)
- Care team members (CareTeam)
- Implantable devices (Device)
- Clinical notes and documents (DiagnosticReport for notes/labs, DocumentReference)
- Provider and organization info (Practitioner, Organization, Location)
- Provenance tracking (Provenance)

**Domains likely stored by OneTouch EMR but NOT covered by the export:**
- **Billing and claims data** — OneTouch EMR includes integrated medical billing, eClaims, ERA processing, eligibility verification, denial management, and payment processing. None of this maps to US Core FHIR resources. There are no Claim, ClaimResponse, Coverage, ExplanationOfBenefit, or other financial FHIR resources in the export. This is a significant gap.
- **Prescriptions / e-prescribing detail** — While MedicationRequest captures prescription orders, the EPCS workflow details, pharmacy routing, and prescription fill status are likely richer than what MedicationRequest alone conveys. MedicationDispense is absent.
- **Clinical images and annotations** — OneTouch EMR features iPad photo capture and a "Free Draw" annotation tool for clinical images. While DocumentReference can reference attachments, the export documentation doesn't clarify whether actual clinical photos and annotated images are included or just metadata references.
- **Patient portal communications** — Secure messages between patients and providers, telemedicine session records. These don't have a natural US Core FHIR mapping.
- **Patient-submitted forms** — Online check-in forms, intake forms completed by patients. No mention in the export.
- **Scheduling/appointment data** — While not strictly EHI in most cases, appointment data linked to encounters could be relevant. Not exported.
- **Fax/document management** — Integrated fax and document management beyond what's captured in DocumentReference.
- **Clinical quality measure data** — CQM calculations and submissions (certified for (c)(1)-(c)(3)).
- **Public health reporting data** — Immunization registry and electronic case reporting submissions.

### Export Format & Standards

- **Format:** FHIR R4 NDJSON, delivered as a ZIP file
- **Standard:** US Core STU3 Release 3.1.1 profiles (based on FHIR R4)
- **Version:** FHIR R4
- The format is well-structured and standards-based, but it's the wrong scope for (b)(10). FHIR US Core covers approximately the USCDI v1 clinical data classes. A comprehensive EHI export needs to include billing data, custom clinical content, portal communications, and other data that doesn't fit neatly into US Core.
- A third party could reconstruct a reasonable clinical summary from this export, but they would be missing billing/financial records, rich document content, and any proprietary clinical data structures.

### Documentation Quality

- **Readability:** Good. The PDF is well-organized with a clear table of contents, consistent formatting, and logical structure.
- **Field-level documentation:** Moderate. Each resource has an attributes table, but descriptions are brief and often just restate the FHIR element definition. No proprietary field mappings or data transformations are documented.
- **Examples:** Excellent. Every resource type has worked examples with full JSON request/response pairs. The EHI Export section includes screenshots of the UI workflow.
- **Implementability:** A developer could implement a FHIR R4 client to consume this API based on the documentation. The EHI export section clearly shows how an admin user triggers the export through the UI.
- **Maintenance:** The PDF was last modified 2023-11-14 (per HTTP headers). The product was certified 2025-02-24. The document appears to have been written for the FHIR API certification and the EHI export section was added to address the (b)(10) requirement.

### Structure & Completeness

- **Granularity:** Resource-level and element-level documentation for all 18 FHIR resources. No data type specifications beyond what's implied by the US Core profiles.
- **Value sets:** Referenced by URL to US Core / HL7 terminology but not enumerated in the document itself.
- **Relationships:** Expressed through FHIR references (e.g., Patient references in clinical resources, Provenance targets). No ER diagram or formal relationship documentation.
- **Versioning:** No version history or changelog in the document. The title says "Version 3" matching the product version.

### Key Finding: (b)(10) / (g)(10) Conflation

This is a clear case where the vendor has repackaged their (g)(10) FHIR API as their (b)(10) EHI export. The EHI Export section states plainly: "OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data." The export produces exactly the same 18 US Core resource types that the Bulk Data API serves. The README.txt inside the export ZIP lists only US Core profile URLs.

The vendor has built a nice UI wrapper around Bulk Data export — the admin panel Single Patient Export page with patient search, job monitoring, and message delivery is thoughtful. But the underlying data scope is the standard USCDI/US Core clinical subset, not "all electronic health information."

For a product that includes integrated medical billing, claims processing, ERA/remittance handling, e-prescribing with EPCS, clinical image annotation, patient portal messaging, and document management, the FHIR US Core export captures perhaps 40-50% of the designated record set. The billing and financial data alone represents a major gap, as does specialty clinical content stored in proprietary formats.

## Access Summary
- Final URL (after redirects): https://onetouchemr.com/OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The PDF was directly accessible at the registered URL with no authentication, redirects, or anti-bot measures. Cloudflare is in the path but did not block access.
