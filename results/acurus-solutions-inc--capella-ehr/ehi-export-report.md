# Acurus Solutions, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://acurussolutions.com/Certification.html
- CHPL IDs: 10807
- Product: Capella EHR v6.1
- Certification date: 2022-01-31

## Navigation Journal

1. Probed the URL with curl:
   ```bash
   curl -sI -L "https://acurussolutions.com/Certification.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: text/html, 19,236 bytes. Static HTML page, no redirects.

2. Fetched and examined the full page source. Found a tabbed interface with "Current Certification" selected by default via JavaScript. The page is a standard Bootstrap HTML page — no SPA framework, no anti-bot measures.

3. Under the "Capella EHR Documentation" section (line 249 of source), found the direct link to the (b)(10) export documentation:
   - `§170.315(b)(10) Electronic Health Information export` → `documents/170.315(b)(10) Electronic Health Information export-v3_20-09-2023.pdf`

4. Also found related API documentation links under "Capella API Services":
   - `§170.315(g)(7),§170.315(g)(9)` → `documents/170.315 g(7)_(g)(9)-API Documentation 20240717.pdf`
   - `§170.315(g)(10)` → `documents/170.315 g(10)-API Documentation 20241111.pdf`
   - API Terms and Conditions → `documents/API_Terms and Conditions (12-7-22).pdf` (not downloaded — not EHI-export-specific)

5. Downloaded all three PDFs and verified each is a valid PDF document:
   ```bash
   curl -sL "https://acurussolutions.com/documents/170.315(b)(10)%20Electronic%20Health%20Information%20export-v3_20-09-2023.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/170.315\(b\)\(10\)-EHI-export-v3.pdf
   ```

6. Took a full-page screenshot of the certification page in the browser for archival purposes.

7. Extracted text from the EHI export PDF (`pdftotext`) and rendered pages 2-4 as images to view the embedded screenshots of the export interface.

## What Was Found

### The (b)(10) EHI Export Documentation (9-page PDF, dated September 5, 2023)

The document describes Capella EHR's approach to the §170.315(b)(10) Electronic Health Information export requirement. The export mechanism is a **CCD (Continuity of Care Document) export** in two modes:

**Single Patient Export:** A "Clinical Summary" screen with checkboxes for data sections. The user selects which sections to include and clicks "Generate CCD." The output is produced in both CCD (C-CDA XML) format and Adobe PDF format. The screenshot shows the following selectable sections:
- Reason Of Visit, Vitals, Clinical Instruction, Immunizations, Mental Status
- Care Plan, Laboratory Test(s), Smoking Status, Allergy, Functional Status
- Procedure(s), Laboratory Values/Results, Encounter, Goals
- Assessment, Medication, Medications Administered During Visit, Treatment Plan
- Problem List, Reason for Referral, Implants, Health Concern
- Lab Test, Laboratory Information, Patient Decision Aids
- Diagnostics Tests Pending, Future Scheduled Tests

There is also a "Launch API" button visible in the interface, and separate buttons for "Generate Care Note" and "Generate CCD."

**Bulk Export:** A separate interface that allows selecting multiple patients by provider and/or date of service range. Users can check individual patients and click "Generate" to produce CCD exports for all selected patients. There is also an **Export Scheduler** with options for:
- Non-recurring export (specific date/time)
- Recurring export (start date, time, frequency)
- A configurable "Destination Path" for the output

The document also mentions: "Ability to download the Images / Clinical notes on demand and can be printed in Adobe PDF format."

### CCD Output Format

The document specifies the standard referenced: **§170.205(a)(4) HL7 Implementation Guide for CDA Release 2: Consolidated CDA Templates for Clinical Notes (US Realm), DSTU Release 2.1, August 2015**.

A detailed data element mapping is provided covering the following CCD sections with their CDA template IDs, XPATHs, and code systems:

| CCD Section | Code Systems Used |
|---|---|
| Patient Demographics/Information | AdministrativeGender, Race & Ethnicity CDC |
| Provider's name and office contact information | — |
| Date and Location of visit | — |
| Chief Complaint and Reason for visit | — |
| Encounters | CPT |
| Immunizations | CVX, CPT-4, NCI Thesaurus, SNOMED |
| Instructions | SNOMED |
| Treatment Plan | LOINC |
| Social History | LOINC |
| Problems | SNOMED, ICD-10 |
| Medications | RxNorm, NDC |
| Medication Allergies | RxNorm, SNOMED |
| Laboratory Tests | LOINC |
| Laboratory value(s)/result(s) | LOINC |
| Vitals | LOINC |
| Goal | — |
| Procedures | CPT-4, SNOMED, HCPCS |
| Care team member(s) | — |
| Reason for Referral | SNOMED |
| Medical Equipment (Implanted Devices) | SNOMED |
| Mental Status | SNOMED |
| Functional Status | SNOMED |
| Health Concern | SNOMED |

### API Documentation (g(7)/g(9) and g(10)) — for context only

The g(10) API doc (11 pages, dated November 2024) describes a FHIR R4 API at `https://fhir.capellaehr.com/r4` supporting US Core 3.1.1 profiles. It supports both patient-level and system-level Bulk Data export via:
- `GET [base]/Patient/[id]/$export`
- `GET [base]/Group/[id]/$export`

The FHIR resources listed are standard US Core: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation, Organization, Practitioner, Procedure, Provenance.

This is relevant context because it shows the vendor has both a CCD-based (b)(10) export AND a FHIR-based (g)(10) API, and they are documented separately, suggesting the vendor understands these are different requirements.

## Export Coverage Assessment

### Data Domain Coverage

The (b)(10) export uses the C-CDA CCD format, which is a clinical document standard. Comparing against what the product research says Capella EHR stores:

**Clearly covered (documented in CCD sections):**
- Patient demographics (name, sex, DOB, race, ethnicity, language)
- Problem lists (SNOMED + ICD-10)
- Medications (RxNorm + NDC)
- Medication allergies (RxNorm + SNOMED)
- Lab orders and results (LOINC)
- Vitals (LOINC)
- Immunizations (CVX + CPT-4)
- Procedures (CPT-4 + SNOMED + HCPCS)
- Encounters (CPT)
- Social history / smoking status (LOINC)
- Care plans and goals
- Care team members
- Implantable devices (SNOMED)
- Mental status assessments
- Functional status assessments
- Health concerns
- Clinical instructions and treatment plans
- Referral reasons

**Absent from the export documentation — significant gaps:**
- **Billing and claims data** — The product research identifies Capella EHR as an "EHR + Practice Management" system with Revenue Cycle Management, HCC coding, and claims/referral management. None of this financial data appears in the CCD export. Billing records are part of the designated record set and are EHI.
- **Clinical notes** — The document mentions "Ability to download the Images / Clinical notes on demand" in the overview, but clinical notes (progress notes, H&P, consult notes, etc.) are not represented as a section in the CCD data mapping. The "Generate Care Note" button is visible in the screenshot but separate from the CCD export. It's unclear if narrative clinical documentation is included in the CCD or only available through the separate "on demand" download mechanism.
- **Family health history** — Certified under (a)(12) but not listed in the CCD sections.
- **E-prescribing data** — Prescription history beyond the medication list (e.g., pharmacy information, fill status, prior authorizations).
- **Patient portal messages / secure messaging** — Certified under (e)(1) and (h)(1).
- **Documents and images** — The overview mentions "download the Images / Clinical notes on demand" but this appears to be a separate mechanism from the CCD export, and the documentation provides no detail on format, scope, or how this integrates with the bulk export.
- **AI-generated data** — In Akido Care deployments, ScopeAI generates clinical reports, preliminary diagnoses, and treatment plans. Whether these are captured in the CCD export sections (like Assessment or Treatment Plan) is unclear.

### Export Format & Standards

The export uses **C-CDA (Consolidated CDA) Release 2.1** — a well-established clinical document standard. This is a legitimate choice for a (b)(10) export, and notably it is NOT simply a repackaging of the FHIR API. The vendor has separate documentation for (b)(10) and (g)(10), which is a good sign.

However, C-CDA is fundamentally a **clinical summary document standard**, not a database export format. It was designed for transitions of care, not for exporting "all electronic health information." While it covers clinical data well, it has structural limitations:

- No native support for billing/financial data
- Limited ability to represent practice management data (scheduling, referrals, RCM)
- Clinical notes may be embedded as narrative text sections but lose structured data
- Custom/specialty data that doesn't map to standard C-CDA sections is likely omitted

The CCD output maps to standard CDA template IDs and uses standard code systems (SNOMED, ICD-10, LOINC, RxNorm, CVX, CPT-4, HCPCS, NDC), which is good for interoperability.

A third party could reconstruct the core clinical record from this export, but not the full patient record including billing, documents, and practice management data.

### Documentation Quality

The documentation is **adequate but minimal**:

- The PDF is 9 pages including cover/TOC, with 2 pages of screenshots and 5 pages of data element mapping tables.
- The data dictionary provides field-level detail with XPATHs, CDA template OIDs, and code systems — this is enough for a developer familiar with C-CDA to understand the output structure.
- There are no sample export files or worked examples.
- The screenshots of the export interface are helpful for understanding the user workflow.
- The Export Scheduler feature (recurring/non-recurring) is shown in the Bulk Export screenshot but not described in the text.
- There is no documentation of the "Images / Clinical notes on demand" download capability beyond the single sentence in the overview.
- The document is dated September 2023, with a version label of "v3," suggesting it has been updated at least twice.

A developer who understands C-CDA could work with this documentation, but someone without CDA expertise would need to reference the HL7 Implementation Guide extensively. The vendor provides the standard reference but no implementation-specific guidance beyond the data mapping table.

### Structure & Completeness

- **Granularity:** Field-level documentation with data element names, CDA XPATHs/template OIDs, code system OIDs, and code system names. This is reasonably granular for a standards-based format.
- **Value sets:** Code systems are identified (e.g., SNOMED, LOINC, RxNorm) but specific value set bindings beyond the code system are not documented. For example, the vitals section says "LOINC" but doesn't specify which LOINC codes are used for which vital signs.
- **Relationships:** Implicitly defined by the CDA document structure; not explicitly documented.
- **Cardinality:** Not specified — the document doesn't indicate which fields are required vs. optional.
- **Versioning:** Document is labeled "v3" with date "05-Sep-2023."

### Overall Assessment

Capella EHR's (b)(10) export is a **C-CDA CCD export that covers the standard clinical data domains well but does not address the full scope of EHI**. The most significant gap is the complete absence of billing and practice management data from the export, despite the product being marketed as an "integrated EHR + Practice Management" system with RCM capabilities. Billing records are squarely within the HIPAA designated record set.

The vendor deserves credit for:
1. Having a genuinely separate (b)(10) mechanism (CCD export) distinct from their (g)(10) FHIR API
2. Providing a scheduling mechanism for recurring bulk exports
3. Including a data dictionary with field-level CDA mappings
4. Mentioning an "on demand" capability for images and clinical notes

But the export appears to be constrained by the CCD format's inherent limitations — it exports what fits in a C-CDA document rather than everything the EHR stores. A more complete (b)(10) implementation would supplement the CCD with additional export mechanisms for data that doesn't fit the clinical document model (billing, documents, images, custom data).

## Access Summary
- Final URL (after redirects): https://acurussolutions.com/Certification.html
- Status: found
- Required browser: no (static HTML, all links work with curl)
- Navigation complexity: one_click (documentation link is directly on the certification page under "Capella EHR Documentation")
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The page loaded without issues, all PDF links were directly accessible via curl with a standard User-Agent header. No JavaScript rendering, login walls, or anti-bot measures were encountered.
