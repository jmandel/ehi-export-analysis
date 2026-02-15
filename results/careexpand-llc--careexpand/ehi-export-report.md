# Careexpand LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda
- CHPL IDs: 11625 (15.04.04.3226.Care.24.00.1.250422)
- Certification date: 2025-04-22
- Product: Careexpand v2024.11.0

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL returned HTTP 200 with `Content-Type: text/html; charset=UTF-8`. The server runs nginx with PHP 8.3.12, powered by BookStack v24.05.4 (a wiki platform). No redirects.

```bash
curl -sI -L "https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda" -H 'User-Agent: Mozilla/5.0'
```

2. **Fetched the main page** — The page is a single BookStack wiki page titled "b10 EHI Export - CCDA". The content rendered fully in curl (no JavaScript required). The page contains text documentation of the EHI export API plus one embedded image containing a data dictionary table.

```bash
curl -sL "https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda" -H 'User-Agent: Mozilla/5.0' -o /tmp/careexpand-main.html
```

3. **Checked the parent book** — The BookStack book "TECHDOC - ONC - Patient EHI Export - b.10" contains exactly one page: this CCDA export page. No additional chapters or pages.

```bash
curl -sL "https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10" -H 'User-Agent: Mozilla/5.0'
```

4. **Searched the entire BookStack instance** — The instance contains ~80+ books across 6 paginated result pages plus 11 shelves. This is clearly an internal development wiki. The only EHI/ONC-related book is the "techdoc-onc-patient-ehi-export-b10" book already found. Other books cover internal development epics (SAAS features, Dapper Care platform, DSP device monitoring, etc.), user manuals, SOPs, and third-party integrations. None contain additional EHI export documentation.

Notable: The shelves page publicly exposes internal infrastructure details (RDS database hostnames, schema names for dev/staging/production environments). This is an internal wiki that was made publicly accessible — likely for ONC compliance purposes — without restricting access to only the relevant EHI export documentation.

5. **Downloaded all export formats** — BookStack provides built-in HTML, PDF, Markdown, and plaintext exports. Downloaded HTML, PDF, and Markdown versions.

```bash
curl -sL "https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda/export/html" -H 'User-Agent: Mozilla/5.0' -o b10-ehi-export-ccda.html
curl -sL "https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda/export/pdf" -H 'User-Agent: Mozilla/5.0' -o b10-ehi-export-ccda.pdf
curl -sL "https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda/export/markdown" -H 'User-Agent: Mozilla/5.0' -o b10-ehi-export-ccda.md
```

6. **Downloaded the data dictionary image** — The data dictionary table is embedded as a PNG image (not HTML table). Downloaded the full-resolution version.

```bash
curl -sL "https://bookstack.careexpandcloud.com/uploads/images/gallery/2025-02/Qvqimage.png" -H 'User-Agent: Mozilla/5.0' -o data-dictionary-table.png
```

7. **Took full-page browser screenshot** for visual reference.

## What Was Found

The entire EHI export documentation consists of a **single wiki page** describing a C-CDA 2.1 XML export via an authenticated API endpoint. Here is what the documentation covers:

### Export Mechanism
- **Format**: XML conforming to C-CDA 2.1 (Consolidated Clinical Document Architecture)
- **Endpoint**: `POST /patient/:idPatient/getPatientCCDAData`
- **Authentication**: JWT Bearer Token with JwtAuthGuard
- **Request body**: `PatientCCDADTO` (not further defined)
- **Output**: A JSON response containing `patientData` with `demographics`, `clinicalData`, and `monitors` sub-objects, plus a link to download a `.xml` C-CDA file

### Data Dictionary (from embedded image)
The data dictionary table lists 17 fields:

| Field | Description | Data Type | Required |
|-------|-------------|-----------|----------|
| patient_name | Full name of the patient | String | Yes |
| dob | Date of birth of the patient | Date (YYYY-MM-DD) | Yes |
| gender | Patient's gender | String (M/F/Other) | Yes |
| race | Race of the patient | String | No |
| ethnicity | Ethnicity of the patient | String | No |
| language | Preferred language of communication | String | No |
| address | Patient's home address | String | No |
| phone | Contact number | String | No |
| emergency_contact | Emergency contact name and phone | String | No |
| smoking_status | Patient's smoking habits | String | No |
| problem_list | List of active and past medical problems | Array (Structured) | Yes |
| medications | Active and past medications | Array (Structured) | Yes |
| allergies | Patient allergies | Array (Structured) | Yes |
| lab_results | Laboratory test results | Array (Structured) | No |
| procedures | Medical procedures performed | Array (Structured) | No |
| encounters | Clinical encounters and visits | Array (Structured) | Yes |
| vital_signs | Blood pressure, heart rate, temperature, etc. | Array (Structured) | No |

The note states: "Additional fields may be included depending on the data available for the patient."

### Response Structure
The JSON response has three top-level objects: `demographics`, `clinicalData`, and `monitors`. The documentation shows only placeholder comments (`// ... other demographic fields`, `// Clinical information`, `// Patient monitoring data`) — no actual field definitions for `clinicalData` or `monitors`.

### Access Instructions
Four steps: authenticate with JWT, call the POST endpoint, download the returned CCDA .xml file, open in a CCDA viewer or XML library.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes what is essentially a **standard C-CDA clinical summary** — the same kind of document you'd see in a (b)(1) Transitions of Care export. It covers a narrow slice of the data Careexpand stores:

**Clearly covered (by the data dictionary):**
- Demographics (name, DOB, gender, race, ethnicity, language, address, phone, emergency contact)
- Problem lists
- Medications
- Allergies
- Lab results
- Procedures
- Encounters
- Vital signs
- Smoking status

**Clearly missing or not mentioned:**
- **Billing data** — No mention of charges, claims, payments, superbills, or any financial data. The product research indicates Careexpand has billing/practice management capabilities (at the $249/mo tier) including a billing dashboard and superbills. None of this appears in the export.
- **Care plans** — Despite being certified for (b)(11) care plans, the export data dictionary does not include care plan data.
- **Prescriptions / e-prescribing data** — The export lists "medications" but not prescription details (prescriber, pharmacy, fill status, SIG). The product supports AI-assisted e-prescribing.
- **Referrals** — The product has automated referral management, but referral data is absent from the export.
- **Clinical notes / encounter documentation** — The product markets "clinical documentation with AI-assisted automated coding" but the export has no note text, progress notes, H&P, or narrative documentation fields.
- **Telemedicine records** — Video/phone consultation records, virtual visit data. The product's core offering is telemedicine. None of this appears.
- **Remote Patient Monitoring (RPM) data** — The response JSON hints at a `monitors` array, but the data dictionary doesn't document what it contains. RPM is a significant product feature (device readings for diabetes, hypertension, heart disease).
- **Patient portal communications** — Messages between providers and patients.
- **Immunization records** — Not mentioned.
- **Implantable devices** — Despite being certified for (a)(14) implantable device lists, this data is absent from the export.
- **Images/documents/attachments** — Not mentioned.
- **Intake forms** — The product has customizable intake forms; none appear in the export.
- **Custom/specialty clinical data** — AI-generated metatags, protocol data, gaps-in-care assessments.

**This is a classic (b)(10) vs (g)(10) confusion.** The export is a C-CDA document — the same format used for transitions of care under (b)(1) and the same clinical data classes available through the FHIR API under (g)(10). It covers roughly the USCDI core data elements and nothing more. A true (b)(10) export should include *all* electronic health information in the designated record set, which for Careexpand would include billing records, telemedicine session data, RPM readings, care plans, referrals, clinical notes, e-prescribing details, and any other patient-specific data stored in the system.

### Export Format & Standards

- **Format**: C-CDA 2.1 XML — a well-established HL7 standard
- **Appropriateness**: C-CDA is appropriate for clinical summary data (the subset it covers). However, C-CDA cannot represent billing data, RPM device readings, telemedicine session metadata, or many of the other data types Careexpand stores. A true (b)(10) export would need a supplementary format (CSV, JSON, database dump) for data that doesn't fit C-CDA.
- **The "Array (Structured)" data types** in the dictionary are not further defined. There is no documentation of the internal structure of problem_list entries, medication entries, encounter entries, etc. A developer receiving a C-CDA file could parse it using standard C-CDA tooling, but the documentation itself doesn't explain what template IDs, code systems, or value sets Careexpand uses.

### Documentation Quality

**Very poor.** This is minimal, compliance-checkbox documentation:

- **Single page**: The entire EHI export documentation is one wiki page (~4 printed pages in PDF).
- **Data dictionary is an image**: The key data dictionary table is embedded as a PNG screenshot, not as structured text. This is not machine-readable and cannot be queried.
- **No field-level detail for structured arrays**: The 7 "Array (Structured)" fields (problem_list, medications, allergies, lab_results, procedures, encounters, vital_signs) have no sub-field documentation. What fields does a medication entry contain? What coding systems are used? Unknown.
- **Response structure is a placeholder**: The JSON example uses comments (`// Clinical information`) instead of actual field definitions.
- **PatientCCDADTO is undefined**: The request body type is referenced but never documented.
- **No sample data or example files**: No example C-CDA output, no sample XML.
- **No schema files**: No XSD, no Schematron, no profile definitions.
- **No worked examples**: No step-by-step walkthrough of making an actual export request.
- **Ambiguous output format**: The documentation describes a JSON response structure but says the export format is C-CDA XML. It's unclear whether the JSON response *contains* the C-CDA data inline, returns a download link, or wraps the C-CDA in a JSON envelope.

A developer could not implement an import of this data based solely on this documentation. They would need to call the API and reverse-engineer the actual output.

### Structure & Completeness

- **Granularity**: Table-name level at best. The 17 fields listed are top-level data categories, not a true field-level dictionary. No column data types beyond "String" and "Array (Structured)".
- **Value sets**: No coded fields are documented with value sets. Gender is listed as "String (M/F/Other)" but no code system. No ICD, SNOMED, RxNorm, LOINC, or CPT references.
- **Relationships**: No entity relationships documented.
- **Versioning**: Document says "Version: v1.0". BookStack shows Revision #5, created/updated 1 year ago by "Ameya" (matches the CHPL contact Ameya Parab, Chief Software Strategist).

## Access Summary
- Final URL (after redirects): https://bookstack.careexpandcloud.com/books/techdoc-onc-patient-ehi-export-b10/page/b10-ehi-export-ccda
- Status: found
- Required browser: no (content renders via curl; browser used for screenshot only)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

- **No obstacles** — the URL worked immediately, no authentication required, no JavaScript rendering needed.
- **Data dictionary as image** — The data dictionary table is embedded as a PNG image rather than an HTML table, making it non-machine-readable. The BookStack Markdown export includes the image link but not the table data as text.
- **Internal wiki exposure** — The BookStack instance is an internal development wiki with ~80+ books covering internal development, infrastructure credentials, and other sensitive information all publicly accessible. This suggests the vendor made their entire internal wiki public rather than creating a dedicated public-facing documentation page for EHI export compliance.
