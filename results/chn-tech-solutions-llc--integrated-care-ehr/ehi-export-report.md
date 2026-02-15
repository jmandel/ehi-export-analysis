# CHN Tech Solutions LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://onc.chntechsolutions.com/integrated-care-ehr-electronic-health-information-export-cures/
- CHPL IDs: 11067
- Product: Integrated Care EHR, Version 3
- Certification Date: 2022-12-13

## Navigation Journal

1. **Initial probe of registered URL:**
   ```bash
   curl -sI -L "https://onc.chntechsolutions.com/integrated-care-ehr-electronic-health-information-export-cures/" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html. WordPress site with Kadence theme, cache-enabled.

2. **Fetched and examined page content:**
   ```bash
   curl -sL "https://onc.chntechsolutions.com/integrated-care-ehr-electronic-health-information-export-cures/" -H 'User-Agent: Mozilla/5.0' -o /tmp/chn-page.html
   ```
   47,333 bytes. The page is titled "Integrated Care EHR – Electronic Health Information Export" and contains a brief description of the EHI export mechanism, citing C-CDA as the export format. Links to IHE Technical Framework, HL7 C-CDA IG standards, and two locally-hosted C-CDA IG PDFs (Vol 1 and Vol 2).

3. **Searched for downloadable files on the page:**
   Found two PDFs hosted on the vendor's site:
   - `CDAR2_IG_CCDA_CLINNOTES_R1_DSTU2.1_2015AUG_Vol1_2022SEPwith_errata.pdf` (986 KB)
   - `CDAR2_IG_CCDA_CLINNOTES_R1_DSTU2.1_2015AUG_Vol2_2022SEPwith_errata.pdf` (7.2 MB, 913 pages)

   These are **standard HL7 C-CDA Implementation Guide documents**, not vendor-specific documentation. They are the official Consolidated CDA Clinical Notes IG with September 2022 errata.

4. **Explored the site navigation.** The site header has these nav items:
   - IC-EHR API Reference (the home/hub page)
   - IC-EHR FHIR API
   - IC-EHR REST API Documentation
   - IC-EHR Standard API
   - Instructions – CCD Operation in FHIR

5. **Fetched the "Instructions – CCD Operation in FHIR" page:**
   ```bash
   curl -sL "https://onc.chntechsolutions.com/instructions-ccd-operation-in-fhir/" -H 'User-Agent: Mozilla/5.0'
   ```
   This is the most relevant page for the (b)(10) export. It provides a step-by-step walkthrough (with screenshots) of how to generate a CCD using the FHIR `$docref` operation via Swagger. Steps include: registering a client, setting scopes (including DocumentReference and Document scopes), authenticating, selecting a patient, calling the `$docref` endpoint with optional date parameters, and downloading the resulting C-CDA document.

6. **Fetched the FHIR API page:**
   ```bash
   curl -sL "https://onc.chntechsolutions.com/ic-ehr-fhir-api/" -H 'User-Agent: Mozilla/5.0'
   ```
   Comprehensive FHIR R4 / US Core 3.1 API documentation. Covers BULK FHIR exports (system, group, and patient export), Provenance resources, the `$docref` CCD generation operation, SMART on FHIR app support, and scope definitions. Includes API endpoint examples using the testing base URL `https://chntech.from-tx.com/ic_ehr_onc_public/apis/default/fhir`.

7. **Fetched the REST API page and Standard API page:**
   Both pages contain the same content: OpenEMR-based REST API documentation with OIDC authorization, scope listings (FHIR scopes + OpenEMR native scopes including dental_issue, soap_note, surgery, insurance, etc.), and client registration examples.

8. **Checked the home/hub page:**
   ```bash
   curl -sL "https://onc.chntechsolutions.com/home/" -H 'User-Agent: Mozilla/5.0'
   ```
   Lists FHIR API docs, Standard API docs, CCD Operation instructions, terms of use (GNU GPL3), and Service Base URL listing. The only listed production endpoint is "(will be added when available)" — only a testing endpoint is published: `https://chntech.from-tx.com/ic_ehr_onc_public/apis/default/fhir`.

9. **Attempted to access the Swagger endpoint** at `https://chntech.from-tx.com/ic_ehr_onc_public/swagger/` — DNS resolution failed (host not resolvable).

10. **Screenshots taken:**
    - Full page screenshot of the EHI export page
    - Full page screenshot of the CCD Operation in FHIR instructions (includes step-by-step screenshots of the Swagger UI)

## What Was Found

The EHI export mechanism for Integrated Care EHR is the generation of a **C-CDA (Consolidated Clinical Document Architecture) Clinical Summary of Care Document (CCD)** via the FHIR `$docref` operation. This is an on-demand document generation process, not a bulk database export.

### Export Format
The export produces a single C-CDA XML document per patient. The CCD is generated dynamically and can be filtered by date range. The document is accessed through the FHIR DocumentReference resource and downloaded via the Binary endpoint.

### CCD Sections Documented
The FHIR API page documents the following CCD sections, noting that date-filtered sections only include encounters within the specified date range:

**Date-filterable sections:**
- History of Procedures
- Relevant DX Tests / LAB Data
- Functional Status
- Progress Notes
- Procedure Notes
- Laboratory Report Narrative
- Encounters
- Assessments
- Treatment Plan
- Goals
- Health Concerns
- Document Reason for Referral
- Mental Status

**Full medical record sections (always include complete history):**
- Demographics
- Allergies, Adverse Reactions, Alerts
- History of Medication Use
- Problem List
- Immunizations
- Social History
- Medical Equipment
- Vital Signs (latest recorded)

### Additional API Capabilities
The site also documents:
- **FHIR Bulk Data Export** supporting System, Group, and Patient export operations (this is the (g)(10) mechanism, not the (b)(10) export)
- **OpenEMR native REST API** with endpoints covering: allergies, appointments, dental issues, documents, drugs, encounters, facilities, immunizations, insurance, medical problems, medications, messages, patients, practitioners, prescriptions, procedures, SOAP notes, surgeries, transactions, and vitals

## Export Coverage Assessment

### Data Domain Coverage

The (b)(10) EHI export is a **C-CDA CCD document**, which by its nature covers a defined set of clinical summary data. Based on the product research, here is the coverage analysis:

**Clearly covered by the CCD export:**
- Demographics (CCD section)
- Allergies and adverse reactions (CCD section)
- Medications / medication history (CCD section)
- Problem list / diagnoses (CCD section)
- Immunizations (CCD section)
- Vital signs (CCD section, latest only)
- Procedures (CCD section)
- Lab results (CCD section)
- Social history (CCD section)
- Encounters (CCD section)
- Goals and care plans (CCD sections)
- Mental status (CCD section)
- Medical equipment / implantable devices (CCD section)
- Progress notes (CCD section)
- Assessment and treatment plans (CCD sections)

**Missing or not addressed by the CCD export:**
- **Billing data** — FQHC facility billing, fee-for-service claims, payment records, patient ledgers, payor aging. The CCD format does not carry billing data, and no separate billing export mechanism is documented.
- **Screening/assessment data** — The product stores extensive screening results (SDOH, substance abuse, depression, fall risk, human trafficking, lead poisoning, vision, TB, smoking, dental, Zika). While some of these might map to Observations in the CCD, the documentation does not describe how these screenings are represented in the export, and most would not fit standard CCD templates.
- **Scheduling data** — Appointments, no-show tracking. Not included in CCD.
- **Insurance/coverage data** — While the REST API has insurance scopes, the CCD does not carry insurance enrollment details.
- **Patient portal communications** — Secure messages between patients and providers. Not included in CCD.
- **E-prescribing records** — Detailed prescription transmission records (VeraDigm/NewCrop). The CCD includes medication lists but not prescription routing history.
- **Chronic care management data** — Tracking, reporting, and billing data for CCM programs.
- **Dental records** — The REST API includes `dental_issue` scopes, but the CCD does not have a dental section.
- **Specialty clinical notes** — While progress notes are included, the CCD may not capture the full richness of specialty modules (psychiatry, therapy, MAT documentation, women's health).
- **Documents and attachments** — External documents incorporated into the chart. The CCD is a generated summary, not an archive of all attached documents.

**Ambiguous:**
- **Lab/imaging reports** — The CCD includes lab results, but it's unclear whether all results from 20+ interfaced labs are fully represented, or whether imaging reports (from radiology interfaces) are included beyond diagnostic report narratives.
- **Clinical quality measure data** — Not typically part of a CCD.

### Export Format & Standards

The export uses C-CDA R2.1 (the standard clinical document format), generated via the FHIR `$docref` operation. This is a recognized, widely-used standard — but it is a **clinical summary format**, not a comprehensive data dump.

The fundamental problem: **a CCD is designed to summarize a patient's clinical state for transitions of care, not to export all electronic health information.** It covers a well-defined set of clinical domains but structurally cannot carry billing data, scheduling data, messaging history, or much of the specialty-specific data that this FQHC product stores.

The vendor has essentially pointed their (b)(10) certification at their (g)(10) FHIR API's `$docref` operation. The FHIR Bulk Data Export (also documented on the site) exports standard FHIR US Core resources, which would have similar coverage limitations. Neither mechanism addresses the full "designated record set" requirement of (b)(10).

The REST API scope list is actually more revealing than the CCD about what data the system stores. It includes scopes for dental issues, SOAP notes, surgeries, insurance, prescriptions, and transactions — data types that are not represented in the CCD export.

### Documentation Quality

- **Readability**: The documentation is clear and well-organized across several WordPress pages. The CCD generation tutorial with Swagger screenshots is practical and followable.
- **Data dictionary**: There is **no data dictionary**. There are no field-level definitions, no schema documentation, no description of what data elements appear in each CCD section.
- **Format specification**: The vendor relies entirely on the C-CDA standard (linking to the HL7 C-CDA IG PDFs hosted on their site) rather than documenting any vendor-specific customizations or constraints.
- **Sample data**: No sample export files or example CCDs are provided.
- **Developer usability**: A developer could follow the Swagger tutorial to generate a CCD, but would have no vendor-specific documentation to understand the structure or content of the resulting document. They would need to rely entirely on the generic C-CDA IG (913 pages for Volume 2 alone).

### Structure & Completeness

- **Granularity**: The documentation lists CCD section names but provides no field-level detail. There is no mapping between EHR data fields and CCD elements.
- **Value sets**: Not documented. The vendor relies on the C-CDA standard's value set bindings.
- **Relationships**: Not applicable — the CCD is a flat document, not a relational export.
- **Versioning**: No version history or change log for the documentation.

### Overall Assessment

CHN Tech Solutions has taken the common approach of equating their EHI export with their FHIR API's CCD generation capability. The documentation is functional for understanding *how* to generate a CCD, but it does not address the fundamental (b)(10) question: how does a patient (or their representative) obtain *all* of their electronic health information from this system?

The product is built on OpenEMR, an open-source EHR with a well-documented database schema. The REST API scope list reveals data domains (dental issues, insurance, transactions, SOAP notes, surgeries) that go well beyond what the CCD export covers. A more complete (b)(10) approach would either export from the underlying OpenEMR database or use the native REST API to retrieve all data types — but neither is documented as the EHI export mechanism.

This is a small vendor (possibly single-site deployment at an FQHC) that appears to have met the letter of certification by pointing to CCD generation, but the export covers perhaps 40-50% of the patient data domains the product stores. Billing, scheduling, dental, screening tools, and messaging are the most significant gaps.

## Access Summary
- Final URL (after redirects): https://onc.chntechsolutions.com/integrated-care-ehr-electronic-health-information-export-cures/
- Status: found
- Required browser: no (static WordPress pages, though screenshots in the CCD tutorial require viewing)
- Navigation complexity: one_click (EHI page is directly accessible; CCD instructions are one nav click away)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The Swagger API endpoint at `chntech.from-tx.com` could not be resolved via DNS, so the interactive API documentation could not be accessed.
- The "Standard API" page and "REST API Documentation" page contain identical content.
- The two C-CDA IG PDFs hosted on the site are standard HL7 documents, not vendor-specific — they provide no information about how this vendor's specific implementation generates CCDs.
- No production FHIR endpoint is listed — only a testing endpoint that is not DNS-resolvable.
