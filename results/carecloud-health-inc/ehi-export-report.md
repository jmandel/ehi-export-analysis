# CareCloud Health, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://carecloud.box.com/s/hbcwnjut45ck1gp99so3v4p7tjncmxo4
- CHPL IDs: 11173
- Product: CareCloud Charts v3.0
- Developer: CareCloud Health, Inc.

## Navigation Journal

1. Initial probe with `curl -sI -L` returned HTTP 404 from `carecloud.box.com`. The URL uses Box's shared link format.

2. Despite the 404 to curl, the HTML response contained OpenGraph metadata revealing the file: `<meta property="og:title" content="CareCloud Charts Certification - §170.315(b)(10) Electronic Health Information Export - Documentation.pdf | Powered by Box">` and a thumbnail image URL. Box shared links require JavaScript rendering.

3. Navigated to the URL in a browser. The page redirected to `https://carecloud.app.box.com/s/hbcwnjut45ck1gp99so3v4p7tjncmxo4` and rendered successfully, showing an 11-page PDF viewer with page thumbnails, a Download button, and the CareCloud company logo.

4. Clicking the Download button in the browser initiated a download. The PDF was also retrievable via Box's download endpoint:
   ```
   curl -sL "https://carecloud.app.box.com/index.php?rm=box_download_shared_file&shared_name=hbcwnjut45ck1gp99so3v4p7tjncmxo4&file_id=f_1363401764765" -H 'User-Agent: Mozilla/5.0' -o ehi-export-documentation.pdf
   ```

5. Verified the download: `file ehi-export-documentation.pdf` confirms "PDF document, version 1.7, 11 page(s)", 457,681 bytes.

6. Checked the mandatory disclosures page at `https://www.carecloud.com/meaningful-use-certified-ehr/` — it does not reference EHI export or link to this Box URL. The Box shared link is a standalone artifact.

7. Checked the Wayback Machine — no archived snapshots found for this URL.

## What Was Found

A single 11-page PDF document titled **"CareCloud Charts Certification - §170.315(b)(10) Electronic Health Information Export - Documentation"**, authored by Rico Lopez, created November 14, 2023 in Microsoft Word.

The document describes CareCloud Charts v3.0's approach to EHI export using a **multi-format, multi-mechanism strategy**:

### Export Mechanisms

1. **Clinical Data — Single Patient Export**: Users open a patient's account, click the Print icon, and select "Clinical Summary CCD" to download a C-CDA XML file for that patient.

2. **Clinical Data — Bulk Patient Export**: Via the Analytics Application, users navigate to Clinical > Patient List, apply filter settings, select "Render Format" as CDA, and run a report. A ZIP file of C-CDA XML files is generated.

3. **Non-clinical data in PDF format**: Patient demographics/insurance, advance directives, appointments, provider-to-patient messages, and billing data (claims with CPT, ICD, Modifier) are exported as PDF files via the Analytics Application.

4. **Documents in PDF format**: Signed encounter notes (progress notes), lab results, radiology reports, and any scanned/uploaded documents are exported as PDFs, organized by document type.

5. **FHIR Data Export**: The document mentions that CareCloud Charts' FHIR Server creates a single-patient FHIR resource DocumentReference and supports FHIR Bulk Data EHI Export for the patient population as described in §170.315(b)(10)(ii).

### CCD Output Format (Data Dictionary)

Pages 6–10 provide a detailed data dictionary for the C-CDA export, mapping data elements to CDA XPATHs and code systems. The CCD sections documented include:

| CCD Section | Key Data Elements | Code Systems |
|---|---|---|
| Patient Demographics | Name, Sex, DOB, Race, Ethnicity, Language | AdminGender, CDC Race/Ethnicity |
| Provider Information | Name, contact, address | — |
| Date/Location of Visit | Time, address | — |
| Chief Complaint | Visit details/complaints | — |
| Encounters | Code, diagnosis, location, date | CPT, SNOMED, ICD-10 |
| Immunizations | Vaccine, date, status, route, site, manufacturer, dose, lot, notes | CVX, CPT-4, NCI, SNOMED |
| Instructions | Patient instructions, follow-up reasons | — |
| Treatment Plan | Planned observations, dates | LOINC, SNOMED |
| Social History | Observation description, dates | — |
| Problems | Problem, status, active date | SNOMED, ICD-10 |
| Medications | Medication, directions, start/end date, status | RxNorm, NDC |
| Medication Allergies | Substance, reaction, severity, status | RxNorm, SNOMED |
| Laboratory Tests | Test code, name, date | LOINC |
| Laboratory Results | Result type, value, reference range, interpretation, date | LOINC |
| Vitals | Observation, date/time | LOINC |
| Goals | Goal, value, date | — |
| Procedures | Procedure, date | CPT-4, SNOMED, HCPCS |
| Care Team Members | Name, specialty, date | — |
| Reason for Referral | Reason | SNOMED |
| Medical Equipment | Implanted device, UDI, GMDN description | SNOMED |
| Mental Status | Assessment, date, results, comments | SNOMED |
| Functional Status | Assessment, date, results, comments | SNOMED |
| Health Concerns | Concern/observation, status, date | SNOMED |

### Non-CCD Exports (PDF Format)

The final page briefly describes additional data exported as PDFs:
- **Patient Demographic/Insurance** — demographics and insurance details
- **Advance Directive** — advance directive information
- **Appointments** — patient appointments
- **Provider-to-Patient Messages** — secure messages
- **Billing Data (Claim)** — CPT, ICD, Modifier billing data
- **Documents** — signed progress notes, lab results, radiology reports, scanned/uploaded documents

These PDFs can be generated from the Analytics Application and organized into folders by document type.

## Export Coverage Assessment

### Data Domain Coverage

CareCloud Charts is a comprehensive ambulatory EHR with integrated practice management (Central), patient portal (Breeze), telehealth (Live), and analytics. The product research identifies extensive data domains including clinical documentation, e-prescribing, lab/imaging, scheduling, billing/claims, patient portal data, telehealth, and AI-generated documentation.

**Domains clearly covered by the export:**
- Patient demographics (CCD + PDF)
- Insurance information (PDF)
- Problem lists/diagnoses (CCD with SNOMED/ICD-10)
- Medications and prescriptions (CCD with RxNorm/NDC)
- Allergies (CCD with RxNorm/SNOMED)
- Lab results (CCD with LOINC)
- Vital signs (CCD with LOINC)
- Immunizations (CCD with CVX/CPT-4)
- Procedures (CCD with CPT-4/SNOMED/HCPCS)
- Care plans/goals (CCD)
- Social history (CCD)
- Mental/functional status (CCD)
- Health concerns (CCD)
- Medical equipment/implants (CCD)
- Encounters (CCD with CPT)
- Referrals (CCD)
- Signed encounter notes/progress notes (PDF documents)
- Lab results (PDF documents)
- Radiology reports (PDF documents)
- Scanned/uploaded documents (PDF documents)
- Appointments (PDF)
- Provider-to-patient messages (PDF)
- Billing data — claims with CPT, ICD, Modifier (PDF)
- Advance directives (PDF)

**Domains with potential gaps or ambiguity:**
- **Prescription history detail**: The CCD exports medications with RxNorm/NDC codes, directions, and dates, which is good. But e-prescribing transaction details (pharmacy sent to, fill status, refill history) may not be fully captured in the C-CDA format.
- **Claims adjudication detail**: Billing is exported as PDF with CPT/ICD/Modifier, but the product research describes extensive RCM features including claims tracking, denial management, payment records, collections data. A PDF of claim data likely captures charges but may lose the detail of claim lifecycle (submission, denial, appeal, payment posting).
- **Patient portal activity**: Check-in records, intake form submissions, and appointment request history from Breeze are not specifically mentioned.
- **Telehealth session data**: Virtual visit records from CareCloud Live are not specifically mentioned — they may be captured as encounter notes, but it's unclear.
- **Custom templates/order sets**: The product has configurable specialty templates and order sets. The clinical data captured via these templates should flow into the CCD, but custom fields that don't map to standard CCD sections could be lost.
- **AI-generated documentation**: cirrusAI Notes produces ambient clinical documentation. These presumably become signed encounter notes and would be exported as documents, but it's not explicitly addressed.
- **Quality measure data**: MIPS/CQM data is not mentioned in the export.
- **Payment records**: Patient payments (online bill pay, payment plans from Breeze) are not specifically mentioned.

**Overall assessment**: CareCloud has made a genuine effort to address (b)(10) beyond just the (g)(10) FHIR API. The export combines C-CDA for structured clinical data with PDF exports for administrative/financial data and documents. This is a thoughtful approach that recognizes the C-CDA alone doesn't cover everything. The inclusion of billing data, appointments, messages, advance directives, and all document types as separate PDF exports demonstrates awareness that EHI extends beyond clinical summaries.

However, the PDF format for billing and administrative data is a significant limitation — it preserves the data for human reading but makes it essentially non-computable. A CSV or structured export of billing data would be far more useful for data portability.

### Export Format & Standards

The export uses two formats:

1. **C-CDA (HL7 CDA R2, Consolidated CDA 2.1)**: For structured clinical data. This is a well-established standard. The document references § 170.205(a)(4), the specific ONC-referenced version. The data dictionary on pages 6–10 maps each section to CDA XPaths and standard code systems (SNOMED, ICD-10, LOINC, RxNorm, CVX, CPT-4, HCPCS, NDC). This is the same format used for (b)(1)/(b)(2)/(b)(3) transitions of care, so it's well-tested.

2. **PDF**: For demographics/insurance, appointments, messages, billing, advance directives, and documents. PDF is human-readable but non-computable. For documents (scanned records, signed notes), PDF is appropriate. For structured data like billing claims, it's a significant limitation.

3. **FHIR**: Mentioned briefly on the last page — CareCloud's FHIR Server creates DocumentReference resources and supports FHIR Bulk Data EHI Export. This appears to be an additional mechanism, possibly the (g)(10) API repurposed for (b)(10)(ii) bulk export. No detail is provided about which FHIR resources are included beyond DocumentReference.

A third party could reconstruct the core clinical record from the C-CDA export. The billing PDFs would require OCR or manual review to extract structured data. The document export preserves clinical notes and reports but in a non-queryable format.

### Documentation Quality

**Strengths:**
- The document is clearly structured with a table of contents
- The CCD data dictionary (pages 6–10) is reasonably detailed, mapping data elements to CDA XPaths and code systems
- The export process is described with step-by-step instructions for both single-patient and bulk export
- The document explicitly addresses (b)(10) and demonstrates awareness that it requires more than just clinical data

**Weaknesses:**
- The PDF-format exports (billing, demographics, appointments, messages) are described in only 1-2 sentences each with no field-level documentation
- No sample export files or examples are provided
- No schema files (XSD, JSON Schema) are included — only the PDF description
- The FHIR export section is a single paragraph with no detail about resources, profiles, or endpoints
- No documentation of the organizational structure of the export package (folder naming, file naming conventions)
- The document was created in November 2023 (product certified December 2022) and there's no version history or update log
- No value set documentation beyond code system OIDs
- No cardinality or optionality information for data elements

A developer could implement a C-CDA importer based on the data dictionary and the referenced standard, but would need additional documentation for the PDF exports and FHIR endpoint.

### Structure & Completeness

- **Granularity**: The CCD section provides field-level documentation with XPaths and code systems, which is moderately detailed. The PDF export sections have no field-level documentation at all.
- **Code systems**: Standard code system OIDs are documented (SNOMED, ICD-10, LOINC, RxNorm, etc.), but specific value sets within those systems are not.
- **Relationships**: Relationships between entities are implicit in the CDA structure (e.g., encounters contain diagnoses) but not explicitly documented.
- **Data types**: Not specified beyond what's inherent in the CDA standard.
- **Versioning**: No version history. Single creation date of November 2023.

## Access Summary
- Final URL (after redirects): https://carecloud.app.box.com/s/hbcwnjut45ck1gp99so3v4p7tjncmxo4
- Status: found
- Required browser: yes (Box shared links return 404 to curl but render in browser; download possible via Box API endpoint)
- Navigation complexity: direct_link (single PDF file on Box)
- Anti-bot issues: Box shared links require JavaScript rendering; direct curl gets 404. Download URL requires constructing the Box download endpoint with the file ID extracted from page source.

## Obstacles & Dead Ends
- The registered URL `https://carecloud.box.com/s/hbcwnjut45ck1gp99so3v4p7tjncmxo4` returns HTTP 404 to curl. However, the HTML response body contains valid OpenGraph metadata and the Box JavaScript application loads the PDF correctly in a browser. This is a Box platform behavior, not a dead link.
- The Box API content URL (used for in-browser preview) returns empty content when accessed directly via curl, likely due to token expiration or referrer checking.
- The successful download method was via Box's download endpoint: `https://carecloud.app.box.com/index.php?rm=box_download_shared_file&shared_name=hbcwnjut45ck1gp99so3v4p7tjncmxo4&file_id=f_1363401764765`
- The Wayback Machine had no archived snapshots of this URL.
- The mandatory disclosures page (`https://www.carecloud.com/meaningful-use-certified-ehr/`) does not reference EHI export documentation.
