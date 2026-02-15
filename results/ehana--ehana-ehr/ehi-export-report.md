# eHana — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.ehana.com/certification-documentation
- CHPL ID: 10200
- CHPL Product Number: 15.04.04.2594.eHan.19.00.1.191206
- Developer: eHana
- Product: eHana EHR, v2019-MU
- Certification Date: 2019-12-06

## Navigation Journal

**1. Initial probe:**
```bash
curl -sI -L "https://www.ehana.com/certification-documentation" -H 'User-Agent: Mozilla/5.0'
```
HTTP/2 200, Content-Type: text/html;charset=utf-8, hosted on Squarespace. Page is 70KB of HTML.

**2. Page structure:** The Certification Documentation page is a single Squarespace-hosted page with four main sections:
- **Costs** — software cost disclosures
- **Real World Testing** — links to RWT plans and results PDFs (2022–2025)
- **Security Assertion Markup Language (SAML)** — MFA/SSO documentation
- **Additional Certification Documentation** — contains FHIR API docs and the EHI Export link

**3. Found EHI Export link:** In the "Additional Certification Documentation" section at the bottom of the page, a single link to the EHI export PDF:
```html
<a href="/s/EHI_Export.pdf">EHI Export: Electronic patient health information is available for export</a>,
in XML format, using the Consolidated-Clinical Document Architecture (CCDA). eHana updates the CCDA
in accordance with the HL7 Clinical Document Architecture standard
```

**4. Downloaded the EHI Export PDF:**
```bash
curl -sL "https://www.ehana.com/s/EHI_Export.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI_Export.pdf
```
File verified as PDF document, version 1.7, 15 pages, 1,479,253 bytes. Created 2023-05-10 by author "maralee.mies" via "Microsoft: Print To PDF" from a Google Doc titled "Electronic Health Information (EHI) Export."

**5. Also downloaded for context:**
- `SmartOnFHIR-API-Doc.pdf` (68 pages, the (g)(10) FHIR API documentation — separate from the EHI export)
- `fhir-base-urls.csv` (FHIR endpoint URLs — not EHI-export-specific)
- Full-page screenshot of the certification documentation page

**6. No other EHI export artifacts found.** No data dictionary CSV, no schema files, no sample export files, no ZIP archives. The EHI export documentation consists solely of the single 15-page PDF.

## What Was Found

### The EHI Export PDF

The EHI Export PDF is a 15-page document that describes eHana's (b)(10) EHI export mechanism. Key findings:

**Format:** The export uses CDA R2 format — specifically, Consolidated Clinical Document Architecture (C-CDA) XML. The document explicitly states: "eHana supports the export of electronic health information (EHI) in accordance with §170.315(b)(10) - Electronic Health Information export of the ONC 2015 Edition Cures Update Certification Criteria using the CDA R2 format."

**Structure:** The document is organized as a catalog of "Resource Types and Elements" included in the export. For each section, it shows:
- A brief "Overview" description of the data
- An "HTML Element" screenshot showing how the data appears in the eHana UI
- An "XML Element" showing the corresponding C-CDA XML markup with sample data

**Sections covered (18 total):**
1. Electronic Chart / Patient Data — demographics (name, DOB, sex, race, ethnicity, language, address/telecom)
2. Vital Signs — vitals manually entered for the client
3. Immunization — immunizations given or reported
4. Allergies, Adverse Reactions, Alerts — allergy records
5. History of Medication Use — prescribed and concurrent medications
6. Instructions — clinician-entered instructions during encounters
7. Functional and Cognitive Status — functional/cognitive status assessments
8. Chief Complaint/Reason For Visit — reason for visit text
9. Problem List — diagnoses captured during encounters
10. Social History — smoking status and birth gender
11. Encounters — encounter records with associated problems
12. Results — lab and test results
13. Procedures — scheduled and performed procedures
14. Reason for Referral — referral documentation
15. Implantable Devices — UDI and device descriptions
16. Health Concerns — documented health concerns
17. Assessment and Plan — clinician assessment and care plan
18. Goals — client goals documented during encounters

**Sample data:** Each section includes XML snippets with synthetic sample data (patient "Alice Newman", DOB May 1, 1970). These use standard C-CDA templates with OIDs (e.g., 2.16.840.1.113883.10.20.22.4.14 for procedures) and standard code systems (SNOMED-CT, LOINC, RxNorm, CDC Race/Ethnicity).

### The SMART on FHIR API Doc (for context)

The 68-page SmartOnFHIR-API-Doc.pdf is eHana's (g)(10) FHIR API documentation — a completely separate system from the (b)(10) EHI export. It documents OAuth2/SMART App Launch authentication and FHIR R4 resource access for standard US Core resources (Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Immunization, MedicationRequest, Observation, Procedure, etc.). This is not the EHI export mechanism.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export covers a **narrow clinical summary subset** of the data eHana stores. The 18 sections in the export PDF map closely to standard C-CDA sections — which is to say, they cover roughly the same data as a Continuity of Care Document (CCD). This is a patient clinical summary, not a comprehensive export of all electronic health information.

**Covered domains:**
- Patient demographics (name, DOB, sex, race, ethnicity, language, address, phone)
- Vital signs
- Immunizations
- Allergies
- Medications
- Problem list / diagnoses
- Lab/test results
- Procedures
- Encounters
- Functional/cognitive status
- Social history (smoking, birth sex)
- Health concerns
- Goals
- Assessment and plan
- Instructions
- Reason for referral
- Implantable devices
- Chief complaint

**Missing domains — significant gaps for a behavioral health EHR:**

- **Billing and claims data** — eHana processes 837/835 claims, manages eligibility, and has comprehensive billing dashboards. None of this is in the export.
- **Clinical documentation / service notes** — eHana generates 600,000+ documents per month (progress notes, clinical assessments, treatment plans). The export includes "Assessment and Plan" and "Instructions" as C-CDA sections, but the rich behavioral health service documentation (the core of what a behavioral health EHR stores) is not represented as structured data.
- **Scheduling data** — client appointments, employee scheduling — absent.
- **Staff/workforce data** — employee demographics, supervision, productivity, timesheets — absent.
- **Scanned documents** — OCR-processed scanned documents filed into client charts — absent.
- **Secure messaging** — staff and patient portal messages — absent.
- **Audit/compliance data** — activity logs, QA records, utilization review — absent.
- **Incident reports** — incident logging and reporting — absent.
- **E-prescribing details** — PDMP queries, EPCS records — absent (only medication history is included).
- **Program enrollment data** — eHana tracks multi-program client enrollment (outpatient, residential, ACCS, ESP/MCI, etc.) — absent.
- **CANS assessments** — Child and Adolescent Needs and Strengths — absent as structured data.
- **Care coordination records** — cross-program notifications, referral tracking — absent.
- **Custom forms and templates** — customizable documentation templates — absent.

This is a classic case of a vendor using a clinical summary standard (C-CDA) as their (b)(10) export, which by definition cannot capture "all electronic health information." C-CDA was designed for clinical summaries in transitions of care — it has no sections for billing, scheduling, audit logs, program enrollment, or the rich behavioral health documentation that is eHana's primary function.

### Export Format & Standards

- **Format:** CDA R2 / Consolidated CDA (C-CDA) XML
- **Standard version:** Not explicitly stated, but the template OIDs correspond to C-CDA R2.1
- **Code systems used:** SNOMED-CT, LOINC, RxNorm, CDC Race/Ethnicity, HL7 AdministrativeGender
- **Appropriateness:** C-CDA is a reasonable format for the clinical data it contains, but it is fundamentally a clinical summary format. For a behavioral health EHR that stores extensive service documentation, billing data, program enrollment, and specialty assessments, C-CDA cannot represent the full data model. A database dump or CSV export of all tables would be more appropriate for a true (b)(10) export.
- **Reconstructability:** A third party could reconstruct a basic clinical summary from this export, but could not reconstruct the full patient record as it exists in eHana — the behavioral health service notes, billing history, program enrollment, scheduling, and scanned documents would all be lost.

### Documentation Quality

- **Readability:** The PDF is clearly organized with a table of contents and consistent section structure. Each section has an overview, UI screenshot, and XML example.
- **Data dictionary:** There is no formal data dictionary. The documentation shows XML element names and sample values, but does not provide field-level definitions, data types, cardinality, optionality, or value set bindings. You see that `<raceCode>` uses code system "2.16.840.1.113883.6.238" from the example, but this is implicit — not formally documented.
- **Sample data:** The XML snippets serve as worked examples with synthetic data, which is useful. However, these are fragments, not a complete sample export file.
- **Developer usability:** A developer familiar with C-CDA could implement an import, but would need to reference external C-CDA specifications — the document alone doesn't fully specify the export format. It shows "what XML elements appear" but not "what is the complete document structure."

### Structure & Completeness

- **Granularity:** Section-level with XML element examples. No formal field listing — the XML snippets are the specification.
- **Value sets:** Referenced implicitly via OIDs in examples (e.g., SNOMED-CT codes) but not enumerated or documented.
- **Relationships:** Not documented. C-CDA's inherent document structure provides some implicit relationships (e.g., encounters contain entries).
- **Versioning:** The PDF was created May 10, 2023. No version history or change log.
- **Completeness:** The 18 sections cover standard C-CDA clinical summary content. There is no documentation of how to request the export, what triggers it, how it's delivered to the patient, or any operational details of the export process.

### Overall Assessment

eHana's EHI export documentation is a **minimal compliance effort**. The vendor has documented a C-CDA clinical summary export that covers standard USCDI-adjacent clinical data — essentially the same data that their (g)(10) FHIR API would expose. This conflates the (b)(10) requirement ("all electronic health information") with a clinical summary export.

For a behavioral health EHR that is primarily a documentation and billing platform — where the core value is in service notes, program management, and behavioral health-specific workflows — exporting only a C-CDA clinical summary misses the majority of the data the system stores. The billing data alone (837 claims, 835 remittances, eligibility records) represents a significant data domain with no export path documented. The 600,000+ clinical service notes generated monthly are the primary clinical record, and they appear to have no structured export path beyond what fits into C-CDA "Assessment and Plan" or "Instructions" sections.

The documentation itself is reasonably clear for what it covers — the section-by-section format with UI screenshots and XML examples is easy to follow. But it lacks a formal data dictionary, complete sample files, operational instructions, and any acknowledgment of data domains beyond the clinical summary.

## Access Summary
- Final URL (after redirects): https://www.ehana.com/certification-documentation
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (EHI Export PDF linked directly from the certification page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The EHI Export PDF contains scanned/image-based content — `pdftotext` returned empty output. All text had to be extracted by rendering pages as images.
- No obstacles accessing the page or downloading the PDF. The Squarespace-hosted page loaded cleanly and all links worked.
- The FHIR API documentation and FHIR base URLs are for the (g)(10) API, not the (b)(10) export — downloaded for completeness but they are separate systems.
