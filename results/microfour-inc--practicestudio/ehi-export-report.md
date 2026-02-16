# MicroFour, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.practicestudio.net/Company/CompanyInformation/ExportProcess.aspx
- CHPL IDs: 9590
- Product: PracticeStudio X20
- Certification date: 2018-08-10

## Navigation Journal

### 1. Initial probe
```bash
curl -sI -L "https://www.practicestudio.net/Company/CompanyInformation/ExportProcess.aspx" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, `text/html; charset=utf-8`, ASP.NET page, 85,476 bytes.

### 2. Page examination
The page rendered successfully. The entire export documentation consists of a single paragraph under the heading "Export Process":

> In the case where a user needs to export all medical records for their entire user base, they only need to contact MicroFour technical support who will help them to do a mass export. The export will produce CCD documents for each patient.

No download links, no data dictionary, no schema files, no additional documentation links on this page.

### 3. Screenshots
Captured viewport and full-page screenshots of the export process page.

### 4. Related pages investigated
- **Certifications page** (`/Company/CompanyInformation/Certifications.aspx`): Lists certified criteria including 170.315(b)(10). No additional EHI export documentation found.
- **Interoperability education page** (`/Education/Questions/Interoperability.aspx`): Documents CCD sections (16 sections) and links to FHIR API documentation. Lists that CCDs contain: Advance Directives, Alerts, Encounters, Family History, Functional Status, Immunizations, Medical Equipment, Medications, Payers, Plan of Care, Problems, Procedures, Purpose, Results, Social History, Vital Signs.
- **FHIR API Documentation** (`https://oauth.patientwebportal.com/Fhir/Documentation`): This is the (g)(10) FHIR API, not the (b)(10) export. Downloaded for reference. Covers 16 FHIR resources: AllergyIntolerance, CarePlan, CareTeam, Condition, DiagnosticReport, DocumentReference, Encounter, Goals, Immunization, Medication, Observation, Organization, Patient, Practitioner, Procedure, Provenance.
- **FHIR R4 Endpoints Bundle** (`/Fhir/DownloadBundle`): Downloaded JSON Bundle with FHIR endpoint URLs.
- **Developer Portal Terms PDF** (`/Interoperability/MicroFourDeveloperPortalTermsOfUseAndFhirApiLicenseAgreement.pdf`): Returned HTML instead of PDF (appears to require authentication or is broken).

### 5. Additional verification
- **Wayback Machine**: No archived captures found for the export process page.
- **Web search**: Searched for `site:practicestudio.net EHI export data dictionary` and `MicroFour PracticeStudio "b(10)" OR "170.315(b)(10)" export CCD` — no additional EHI export documentation found. Web results confirm the product is certified for (b)(10) but reveal no technical documentation beyond the ExportProcess.aspx page.
- **micro4.com**: Checked the parent company site (`micro4.com/ProductsServices/PracticeStudio`) — marketing content only, no export documentation.
- **support.practicestudio.net**: Support portal exists but requires authentication — no public-facing export documentation.

## What Was Found

The EHI export documentation is **extremely minimal**. The entire (b)(10) export documentation is a single sentence stating that users must contact MicroFour technical support to perform a mass export, and that the export produces CCD (Continuity of Care Document) files for each patient.

### Export Format
The export produces **CCD documents** (HL7 C-CDA Continuity of Care Documents). Based on the interoperability page, PracticeStudio's CCDs contain 16 standard sections:
1. Advance Directives
2. Alerts (Allergies)
3. Encounters
4. Family History
5. Functional Status
6. Immunizations
7. Medical Equipment
8. Medications
9. Payers
10. Plan of Care
11. Problems
12. Procedures
13. Purpose
14. Results
15. Social History
16. Vital Signs

### Export Process
The export is not self-service. Users must contact MicroFour technical support, who will assist with the mass export. There is no documented user-facing export interface, no API endpoint for bulk export, and no instructions for the user to perform the export independently.

### Separate FHIR API (g)(10)
PracticeStudio also has a FHIR R4 API at `api.practicestudio.net` with SMART on FHIR authorization, documented at `oauth.patientwebportal.com/Fhir/Documentation`. This is the (g)(10) standardized API, not the (b)(10) EHI export. It covers standard US Core resources and is patient-scoped (not bulk export).

## Export Coverage Assessment

### Data Domain Coverage

The CCD-based export is fundamentally limited. Comparing against PracticeStudio's known data domains from the product research:

**Likely covered by CCD sections:**
- Demographics (Patient section)
- Diagnoses/Problem lists (Problems)
- Medications/prescriptions (Medications)
- Allergies (Alerts)
- Lab results (Results)
- Vital signs (Vital Signs)
- Immunizations (Immunizations)
- Procedures (Procedures)
- Encounters (Encounters)
- Care plans (Plan of Care)
- Family history (Family History)
- Social history (Social History)
- Advance directives (Advance Directives)
- Insurance/payer info (Payers)

**Missing or not documented as included:**
- **Billing data** — charges, claims, remittances, patient ledger. CCDs are clinical documents and do not include billing/financial records. PracticeStudio is an integrated EHR + PM system where billing is a major data domain.
- **Clinical notes** — SOAP notes, narrative reports, provider notes. While CCDs can include narrative sections, there's no indication that full encounter notes are exported. PracticeStudio has dedicated charting and narrative report functionality.
- **Documents & media** — uploaded images, documents, and media files. CCDs can reference but typically don't embed large documents/images.
- **Scheduling/appointment data** — appointment history, recurring schedules.
- **Patient portal messages** — secure two-way communications.
- **Inventory/point-of-sale data** — for practices that stock products.
- **Custom/specialty-specific clinical data** — PracticeStudio supports specialty-specific templates (cardiology, chiropractic, dermatology, etc.) with customizable charting forms. CCD sections are generic and unlikely to capture specialty-specific assessment data.
- **Treatment forms** — custom clinical forms are a key PracticeStudio feature not captured by standard CCD sections.
- **ePrescribing history** — detailed prescription routing, benefits/formulary data from Surescripts.
- **Lab orders** — orders placed (not just results received).
- **Clinical quality measure data** — 30 certified CQMs.

### Export Format & Standards

The export uses CCD (HL7 C-CDA Continuity of Care Document), which is a recognized clinical document standard. However:

- CCD is designed as a **clinical summary document**, not a comprehensive data export format. It captures a snapshot of a patient's clinical state, not the full longitudinal record.
- There is no documentation of how the CCD maps to PracticeStudio's internal data model. No data dictionary, no field mapping, no schema documentation.
- No information about how coded data (ICD-10, CPT, SNOMED, RxNorm) is represented or whether all coded fields use standard terminologies.
- No sample CCD files are provided.
- CCD is an **inappropriate format** for billing data, appointment data, custom forms, and other non-clinical data that PracticeStudio stores. The choice of CCD as the sole export format inherently limits the export to clinical data only.

### Documentation Quality

The documentation quality is **extremely poor**:
- The entire export documentation is one sentence.
- No data dictionary exists.
- No field-level definitions, no data types, no value sets, no constraints.
- No sample export files or worked examples.
- No instructions for performing the export — users are told to call support.
- No description of what data is included or excluded.
- A developer could not implement an import of this data based on the documentation alone. They would need to obtain a sample CCD and reverse-engineer the structure.
- The documentation appears to be a bare minimum compliance checkbox, not a genuine attempt to facilitate data portability.

### Structure & Completeness

- **Granularity**: Zero field-level documentation. Only the 16 CCD section names are listed, with no description of what fields or data elements appear within each section.
- **Coded fields**: Not documented. No value sets described.
- **Relationships**: Not documented.
- **Versioning**: No change history.

### Key Finding: (b)(10) vs (g)(10) Gap

MicroFour has two separate mechanisms:
1. **FHIR API (g)(10)**: Reasonably well-documented with 17 resource pages, example requests/responses, and authorization documentation. Covers standard US Core clinical data.
2. **CCD Export (b)(10)**: One sentence of documentation. No technical detail.

The FHIR API covers roughly the same clinical data domains as the CCD export. Neither mechanism appears to cover the full scope of EHI — particularly billing/financial data, custom clinical forms, specialty-specific data, documents/images, and other practice management data that PracticeStudio stores.

This is a textbook example of the (b)(10) vs (g)(10) confusion, with an added twist: instead of just pointing to their FHIR API as the EHI export, MicroFour chose CCD (an older clinical summary standard) as the export format. The result is even more limited than a FHIR-based export would be, since FHIR at least has resource types for some non-clinical data.

## Access Summary
- Final URL (after redirects): https://www.practicestudio.net/Company/CompanyInformation/ExportProcess.aspx
- Status: found
- Required browser: no (content renders server-side in ASP.NET)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- Developer Portal Terms PDF (`/Interoperability/MicroFourDeveloperPortalTermsOfUseAndFhirApiLicenseAgreement.pdf`) returned HTML instead of PDF content — appears broken or requires authentication.
- No Wayback Machine captures found for this page.
- No additional EHI export documentation found anywhere on the site beyond the single paragraph.
