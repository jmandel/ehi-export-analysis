# MEDENT (Community Computer Service, Inc.) — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.medent.com/onc/
- CHPL IDs: 11347
- Product: MEDENT v23.7
- Certification date: 2023-09-18

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://www.medent.com/onc/"` returned HTTP 200, Content-Type: text/html. WordPress site (Apache/Debian, PHPSESSID cookie, wp-json API link).

2. **Fetched page** — 162KB HTML. Extracted visible text and searched for download links:
   ```bash
   curl -sL "https://www.medent.com/onc/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)[^"]*"' /tmp/page.html
   grep -oiE 'href="[^"]*"' /tmp/page.html | grep -iE 'ehi|export|data.dictionary|b.10'
   ```

3. **Found dedicated EHI section** — The ONC certification page contains a clearly labeled section **"Electronic Health Information Specification"** (at line 239 of the HTML source). Below the heading are 33 PDF links under the `/ehi_pdfs/` path on the vendor's domain. The section is distinct from the FHIR API documentation section above it.

4. **Downloaded all 33 EHI PDFs** — All files downloaded successfully as genuine PDF documents (verified with `file` command). URLs required URL-encoding for spaces:
   ```bash
   curl -sL "https://www.medent.com/ehi_pdfs/Allergy%20File%20Specification.pdf" -o Allergy_File_Specification.pdf
   ```

5. **Found Financial Field List reference** — The Financial File Specification PDF states: "Fields available can be reviewed and selected in the MEDENT manual here: https://www.medent.com/htmlmanual/html/v237/asciifieldlistinter.html". This is a JavaScript SPA (Help & Manual WebHelp) containing a comprehensive table of 750 configurable financial/billing data export fields.

6. **Downloaded and extracted the ASCII Field List** — Navigated in browser, extracted the full 750-row table via JavaScript DOM evaluation, saved as structured JSON. Also saved the raw HTML page.

7. **Took screenshots** of the EHI section on the ONC page and the full ASCII Field List page.

## What Was Found

MEDENT has implemented a **purpose-built EHI export system** that is clearly distinct from their FHIR API. This is one of the better (b)(10) implementations encountered: it is not a repurposed FHIR endpoint but a dedicated export module with its own documentation, field-level specifications, and configurable export settings.

### Export Architecture

The EHI export is accessed via: **Medical Records > Data Export/Import/Connection Table > Electronic Health Information Export**. It has four operational areas:

1. **Setup** — Configure export settings: patient population filters (by provider, location, age, insurance, race, ethnicity, sex, status), data feeds to include, optional financial data, and optional document/triage/todo exports. Supports autorun scheduling for overnight batch processing.

2. **Create** — Review settings and trigger data generation for a specific date range. Can be further narrowed to specific patients.

3. **Send** — Completed exports are queued for transmission to external destinations or download to local PC.

4. **Control File** — Configures output format:
   - **Delimiters**: PIPE (with/without quotes), CSV (with/without quotes)
   - **Filename format**: Configurable with create date, practice ID, process ID, date ranges
   - **ZIP compression**: Optional
   - **Connection**: Can route to configured destinations or local PC download

### Export Format

The export produces **delimited text files** (CSV or pipe-delimited). Each data domain has its own file with a documented field specification. Documents, triages, and todos are exported as **HL7 C-CDA 2.1 Unstructured Documents** containing Base64-encoded PDFs, zipped together.

### Documentation Corpus

33 PDF file specifications covering these data domains:

| File | Description | Fields |
|------|-------------|--------|
| EHI Setup and File Format Specification | Master document — export configuration, workflow, and architecture | (setup doc) |
| Patient File Specification | Demographics, contacts, insurance, social determinants, birth info | ~80 |
| Allergy File Specification | Allergies with SNOMED codes, reactions, severity, criticality | ~21 |
| Appointment File Specification | Appointments with providers, types, statuses | ~15 |
| CareTeam and Resources File Specification | Care team members and community resources | ~8 |
| Diagnosis File Specification | Encounter diagnoses with ICD codes | ~13 |
| Document Listing File Specification | Document metadata with LOINC codes | ~12 |
| Encounter File Specification | E-Superbill encounters with providers, NPIs, locations | ~14 |
| Exchanged Patient Level Files | Records of data exchanges (sent packages) | ~13 |
| Eye/Contact Script File Specification | Ophthalmology/optometry prescriptions — keratometry, sphere, cylinder, axis, etc. | ~56 |
| Financial File Specification | Financial export (references 750-field ASCII Field List) | configurable |
| Goals File Specification | Patient goals with short-term/long-term tracking | ~19 |
| HIPAA File Specification | HIPAA consent and communication preferences | ~21 |
| Immunization File Specification | Immunizations with CVX, CPT, lots, manufacturers, VIS | ~29 |
| Info File Specification | Export metadata — criteria used, statistics | (metadata) |
| InsurancePlan File Specification | Insurance plan master data | ~6 |
| Location File Specification | Practice locations | ~9 |
| MedicalHistory File Specification | Past medical history with SNOMED codes | ~9 |
| Medication File Specification | Prescriptions with NDC, RxNorm, SIG, refills, administration | ~43 |
| OBEpisode File Specification | OB/prenatal episodes with EDD, gestational age, risk | ~12 |
| OBOutcome File Specification | Delivery outcomes with birthweight, type | ~11 |
| Order File Specification | Lab, DI, and general orders with facility, LOINC, fasting | ~31 |
| PatientPlan File Specification | Patient insurance enrollment with policy details | ~9 |
| ProblemList File Specification | Problem list with SNOMED codes, onset, resolution | ~14 |
| Procedures File Specification | Procedures with CPT, SNOMED, modifiers, body site, status | ~30 |
| Progress Note Listing File Specification | Progress note metadata with LOINC codes, signatures | ~13 |
| Provider File Specification | Provider demographics, NPI, taxonomy, specialty | ~18 |
| Referral File Specification | Referral tracking with dates, providers, types | ~26 |
| Result File Specification | Lab/diagnostic results with reference ranges, status | ~39 |
| Screening and Assessment Specification | Screenings, assessments, risk scores, tobacco use, SDOH | ~43 |
| SocialHistory File Specification | Social history with SNOMED codes | ~9 |
| SurgicalHistory File Specification | Surgical history with SNOMED codes | ~9 |
| Vital File Specification | Vital signs with LOINC codes, remote monitoring flags | ~15 |

Additionally, the **ASCII Field List** (750 fields across 17 data areas) provides granular financial/billing export configuration covering: charges, payments, adjustments, denial codes, insurance details, referring doctor info, scheduling, surgical booking, and more.

### Field-Level Quality

Each specification PDF follows a consistent format:
- **Field Name** — snake_case identifiers matching the actual export column names
- **Field Description** — Plain English description of what the field contains and where in MEDENT it comes from (e.g., "SNOMED code for the reaction listed, if any. If multiple exist, they are comma separated.")
- **Example Output** — Sample data showing actual output format with realistic values

Coded fields reference standard terminologies: SNOMED CT, LOINC, RxNorm, CVX, NDC, CPT/HCPCS, ICD-10, UNII. UUIDs are used as record identifiers throughout.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains:**
- Patient demographics (extensive — 80 fields including SDOH, gender identity, sexual orientation, pronouns, birth location/time, multiple birth, education level, employment, income, homelessness/migrant/veteran status)
- Allergies (with coded reactions, severity, criticality)
- Diagnoses (encounter-level and problem list)
- Medications (prescriptions with full SIG, NDC, RxNorm, administration records)
- Immunizations (with CVX, lot numbers, manufacturers, VIS dates)
- Vital signs (with remote monitoring flag)
- Lab results and orders (with reference ranges, LOINC codes)
- Diagnostic imaging orders
- General orders
- Procedures (with CPT, SNOMED, body site, outcomes, complications)
- Progress notes (metadata + documents as C-CDA wrapped PDFs)
- Documents (metadata + actual documents as C-CDA wrapped PDFs)
- Medical history and surgical history
- Social history
- Goals (short-term and long-term with status tracking)
- Care team and community resources
- Referrals (comprehensive tracking with dates, reasons, providers)
- Screenings and assessments (tobacco, SDOH, risk scores, questionnaires)
- Insurance/enrollment data (patient plans with policy numbers, effective dates)
- Insurance plan master data
- Financial/billing data (750 configurable fields covering charges, payments, adjustments, denials, claims)
- HIPAA consent preferences
- Encounter data (E-Superbill based)
- Provider/referring doctor data
- Location data
- Eye/contact lens prescriptions (specialty ophthalmology/optometry data)
- OB/prenatal episodes and delivery outcomes (specialty OB/GYN data)
- Exchanged patient-level records (data disclosure tracking)

**Domains potentially missing or unclear:**
- **Triages (messages)**: The setup document mentions including triages and todos in the export as C-CDA documents, but there is no dedicated field specification for these. They appear to be exported as unstructured PDFs rather than structured data.
- **Patient portal messages**: No explicit specification for portal message content (though they may be captured under documents/triages).
- **Telehealth encounter data**: No dedicated telehealth-specific fields beyond standard encounter data, though the appointment spec does include an "E-Visit" status.
- **Clinical note content**: Progress notes and documents export metadata and the document itself as a C-CDA-wrapped PDF. The actual text/structured content of notes is not broken into discrete fields — but this is reasonable since clinical notes are inherently unstructured.
- **Scanned images**: The document listing includes document metadata but the actual image/scan content export is handled through the C-CDA document wrapping mechanism.

### Export Format & Standards

The export uses **delimited text files** (CSV or pipe-delimited) for structured data and **HL7 C-CDA 2.1 Unstructured Documents** for documents, triages, and todos. This is a pragmatic, well-designed approach:

- The delimited text format is universally readable and doesn't force clinical data into a standard that may not fit well
- Coded fields use standard terminologies (SNOMED, LOINC, RxNorm, CVX, NDC, CPT, ICD-10)
- UUIDs provide stable record identifiers
- Documents are wrapped in C-CDA for interoperability while preserving the original content as PDF

Relationships between entities are expressed through shared identifiers:
- `patient_mrn` and `MEDENT_id` link records to patients
- `encounter_id` (E-Superbill number) links records to encounters
- `provider_id` links to the Provider file
- `location_id` links to the Location file
- `plan_id` links patient insurance to the InsurancePlan file

This is **not** a FHIR-based export (the FHIR API is documented separately for g(10) compliance). The EHI export is a purpose-built, configurable data extraction system that exports directly from MEDENT's internal data structures.

### Documentation Quality

**Excellent.** This is among the best-documented EHI exports:

- Every data file has its own PDF specification with field names, descriptions, and example output
- Field names are consistent (snake_case), matching actual export column headers
- Descriptions reference specific MEDENT UI screens and data sources, making the mapping traceable
- Standard code systems are explicitly called out (SNOMED, LOINC, RxNorm, etc.)
- The main Setup document provides clear workflow instructions with navigation paths
- The financial export leverages a pre-existing, comprehensive 750-field configuration system
- The Info File provides export metadata including criteria used and record counts per file

Areas for improvement:
- Data types are not formally specified (no explicit "string", "date", "integer" declarations), though example output makes types inferrable
- Value sets for coded fields are not enumerated in the specifications (e.g., what are the valid `status` values for appointments?) — though some are documented inline (e.g., verification_status: "Confirmed, Unconfirmed, Refuted")
- No formal schema file (XSD, JSON Schema, etc.) — field specs are only in PDF
- Cardinality is not formally specified (which fields are required vs optional)
- The financial export documentation requires navigating to the separate ASCII Field List HTML manual page

### Structure & Completeness

**Granularity**: Field-level documentation with names, descriptions, and examples for all 33 data files. The Patient file alone has ~80 fields. Total structured fields across all EHI specs: ~648, plus 750 configurable financial fields.

**Coded fields**: Standard terminologies are documented (SNOMED, LOINC, RxNorm, CVX, NDC, CPT/HCPCS, ICD-10, UNII). However, proprietary value sets (appointment types, document codes, etc.) are not enumerated.

**Relationships**: Cross-file relationships are implied through shared field names (patient_mrn, MEDENT_id, encounter_id, provider_id, location_id, plan_id) rather than formally documented with a relationship diagram.

**Specialty coverage**: Notably includes ophthalmology/optometry data (Eye/Contact Script with keratometry, sphere, cylinder, axis, etc.) and OB/GYN data (antepartum records, delivery outcomes, birth weights). This demonstrates real (b)(10) thinking — exporting specialty clinical data that would never appear in a standard FHIR US Core export.

**Versioning**: No explicit version number or change history on the specifications. The main Setup PDF title includes "Part1Img3912SUPPROGC" in its metadata, suggesting it was created from the MEDENT documentation system. PDF creation date is November 30, 2023, roughly contemporaneous with the September 2023 certification.

## Access Summary
- Final URL (after redirects): https://www.medent.com/onc/
- Status: found
- Required browser: no (PDFs downloadable via curl; ASCII Field List page needed browser for JS rendering but content is also in HTML source)
- Navigation complexity: direct_link (EHI section clearly labeled on the ONC page)
- Anti-bot issues: none (standard User-Agent header sufficient)

## Obstacles & Dead Ends

- **Spaces in PDF URLs**: The PDF filenames contain spaces (e.g., "Allergy File Specification.pdf"), requiring URL-encoding (`%20`) for successful download via curl. Direct copy-paste of href values from HTML source works in browsers but not in curl without encoding.
- **ASCII Field List is a JS SPA**: The financial field list at `asciifieldlistinter.html` is a Help & Manual WebHelp 3 application that requires JavaScript execution. The 750-field table is embedded in the HTML source but rendered by JS. Used browser automation to extract the table data.
- **Financial File Specification indirection**: The Financial File Specification PDF doesn't contain its own field list — it says "Fields available can be reviewed and selected in the MEDENT manual" and links to the ASCII Field List. This is the only spec that delegates its content to an external reference.

No dead ends, no login walls, no Cloudflare blocks. Documentation was fully accessible and well-organized.
