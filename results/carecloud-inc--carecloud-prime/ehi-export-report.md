# CareCloud, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.carecloud.com/cc-prime/
- CHPL IDs: 11504
- Product: CareCloud Prime v2.0
- Certification date: 2024-08-21

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to https://www.carecloud.com/cc-prime/:
   ```
   curl -sI -L "https://www.carecloud.com/cc-prime/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: 301 redirect from `www.carecloud.com` to `carecloud.com/cc-prime/`, then 200 OK. Content-Type: text/html. WordPress site with WP Rocket caching.

2. **Page examination** — Fetched full HTML (476KB). The page is a marketing/product page for CareCloud Prime ("Empower Your Practice with CareCloud PRIME: The Future Of EHR Solutions"). The main body contains product marketing, feature descriptions, testimonials, FAQ accordions, and a demo request form. No EHI export content in the main body.

3. **Link search** — Searched the HTML for downloadable files and EHI-related links:
   ```
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json)[^"]*"' /tmp/page.html
   ```
   Found three PDFs:
   - `certification_-___170.315_b__10__electronic_health_information_export_-_documentation-1-1-1.pdf` — **the EHI export documentation**
   - `CareCloud_Prime_CY-2025-Plan-1.pdf` — Real World Testing Plan 2025
   - `CareCloudPrime-Real-World-Testing-Result-2025.pdf` — Real World Testing Result 2025

4. **Location of link** — The EHI export PDF link is in the site footer, under a "Real World Testing Plan" heading (misnomer — the b(10) doc is not a real-world testing plan). The link text reads "$170.315(b)(10) Electronic Health Information Export – Documentation" (note: uses dollar sign instead of section symbol).

5. **Downloaded the PDF**:
   ```
   curl -sL "https://carecloud.com/wp-content/uploads/2014/08/certification_-___170.315_b__10__electronic_health_information_export_-_documentation-1-1-1.pdf" -o certification_b10_ehi_export_documentation.pdf
   ```
   Verified: PDF document, 12 pages, 1.15MB, created 2024-09-12, author "JAHANZAIB NISAR", created with Microsoft Word 2016.

6. **Checked for additional FHIR/API documentation** — The PDF mentions "FHIR Bulk Data EHI Export" on page 12, and the page HTML contained a reference to `aptivio.azure-api.net`, but that endpoint returns 404. No additional FHIR API documentation was found on the site.

7. **Checked mandatory disclosures page** (https://carecloud.com/cost-and-fees-information/) — Lists (b)(10) among certified criteria but contains no additional EHI export documentation.

## What Was Found

The sole EHI export documentation is a 12-page PDF titled "§170.315(b)(10) Electronic Health Information Export – Documentation" (Version V2.0). It describes a **multi-format export approach** combining:

### Export Components

**1. Clinical Data via C-CDA (pages 3–10)**
- **Single Patient Export**: Navigate to CCDA Report > CCDA Export Tab, select CCDA type, search for patient, generate and download as XML. Screenshot of the interface is included showing a "Patient Chart Summary" with demographics.
- **Bulk Patient Export**: Navigate to CCDA Report > Data Portability Tab, select date range, click Export. Downloads a ZIP of CCDA XML files. Screenshot shows the interface with pagination (1–10 of 93 patients) and a download dialog.
- **CCD output format**: References §170.205(a)(4) HL7 CDA R2 C-CDA templates (US Realm, Draft Standard for Trial Use Release 2.1, August 2015).

**CCD Sections documented** (pages 6–10): A detailed data dictionary maps each CDA section to XPATH entries, code systems, and code system names:
- Patient Demographics/Information (name, sex, DOB, race, ethnicity, preferred language)
- Provider information (name, contact, address)
- Date and Location of Visit
- Chief Complaint and Reason for Visit
- Encounters (CPT codes, SNOMED/ICD10 diagnoses, location, date)
- Immunizations (CVX/CPT-4, route, site, manufacturer, dose, lot, notes)
- Instructions (patient instructions/followup reasons)
- Treatment Plan (planned observations, LOINC codes, planned dates)
- Social History (LOINC observations)
- Problems (SNOMED/ICD10, status, active date)
- Medications (RxNorm/NDC, directions, dates, status)
- Medication Allergies (RxNorm substance, SNOMED reaction/severity/status)
- Laboratory Tests and Results (LOINC, reference ranges, interpretation)
- Vitals (LOINC observations)
- Goals
- Procedures (CPT-4/SNOMED/HCPCS)
- Care Team Members
- Reason for Referral (SNOMED)
- Medical Equipment / Implanted Devices (GMDN)
- Mental Status (SNOMED assessments)
- Functional Status (SNOMED assessments)
- Health Concerns (SNOMED observations)

**2. Non-clinical Data via PDF (page 11)**
Brief one-sentence descriptions for each, all exported in PDF format:
- Patient Demographic/Insurance
- Advance Directive
- Appointments
- Provider-to-Patient Messages
- Billing Data (Claim) — includes CPT, ICD, Modifier
- Documents (signed progress notes, lab results, radiology reports, scanned/uploaded documents)

**3. Organizational Structure (page 11)**
Files are saved to a user-specified folder, sorted/categorized by type (e.g., Lab Reports, Imaging) with sub-types.

**4. FHIR Data Export (page 12)**
A single sentence: "CareCloud PRIME FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in §170.315(b)(10)(ii)." No further detail — no FHIR resource list, no endpoint documentation, no profile information.

**5. Timeliness (page 12)**
States that practice administrators can grant access for EHI export, users can export at any time without developer assistance, and exports are created in a timely fashion.

## Export Coverage Assessment

### Data Domain Coverage

CareCloud Prime's EHI export documentation describes a **hybrid approach** that covers clinical data more thoroughly than non-clinical data, but leaves significant gaps relative to everything the product stores.

**Clearly covered (via C-CDA):**
- Patient demographics (name, sex, DOB, race, ethnicity, language)
- Problems/diagnoses (SNOMED + ICD10)
- Medications (RxNorm + NDC)
- Allergies (substance, reaction, severity)
- Lab results (LOINC codes, values, reference ranges)
- Vitals (LOINC)
- Immunizations (CVX/CPT-4)
- Procedures (CPT-4/SNOMED/HCPCS)
- Encounters
- Care plans, goals, health concerns
- Social history
- Mental and functional status assessments
- Care team members
- Implantable devices
- Referrals

**Nominally covered but poorly documented (via PDF export):**
- Insurance information — mentioned but no field-level documentation
- Appointments — mentioned but no field-level documentation
- Billing data (claims) — described only as "CPT, ICD, Modifier" with no field-level detail
- Provider-to-patient messages — mentioned but no format documentation
- Advance directives — mentioned but no format documentation
- Documents (progress notes, lab results, radiology reports, scanned documents) — exported as PDFs

**Clearly missing or not mentioned:**
- **Scheduling and workflow data** — calendars, check-in status, task assignments, staff communications (the product has extensive scheduling via CareCloud Central)
- **Revenue cycle management data** — denial records, appeal records, payment processing, patient statements, contract rates, underpayment/overpayment analysis (the product offers full RCM services)
- **Insurance eligibility verification records**
- **Claims scrubbing results** (CollectiveIQ feature)
- **Patient portal data** — intake forms, consent forms (e-signatures), prescription refill requests, patient payment methods
- **Telehealth session data**
- **Clinical decision support alerts and interaction records**
- **Prescription history and e-prescribing records** (the C-CDA covers medication lists but not detailed prescribing workflows, controlled substance records, or Surescripts transaction history)
- **Public health reports** (immunization registry, syndromic surveillance, cancer case reports)
- **Quality measure calculations** (CQMs)
- **Population health analytics**
- **Practice performance metrics and dashboards**
- **Direct messaging records** (sent/received via EMR Direct)
- **Audit logs**
- **AI-generated content** (cirrusAI Notes ambient documentation, cirrusAI Chat interactions, cirrusAI Guide recommendations)
- **Staff communications** (real-time chat via Community feature)
- **Medical coding and transcription data**

### Export Format & Standards

The export uses a **two-format approach**:

1. **C-CDA XML** for clinical data — based on HL7 CDA R2 C-CDA 2.1 (August 2015). This is a well-defined, recognized standard. The data dictionary in pages 6–10 maps sections to XPATHs and code systems, providing reasonable field-level documentation for the clinical portion.

2. **PDF** for non-clinical data (demographics/insurance, appointments, billing, messages, documents). This is a **significant limitation** — PDF is essentially a print format with no computable structure. A third party cannot programmatically import or process PDF-exported billing claims, appointments, or messages. There is no schema, no field mapping, no data types documented for any of the PDF exports.

3. **FHIR** is mentioned on page 12 as a third option ("FHIR Bulk Data EHI Export") but is entirely undocumented — no resource types, no endpoint URLs, no profiles, no examples. It appears to be a reference to their (g)(10) FHIR API repackaged as a (b)(10) component, but this cannot be confirmed from the documentation.

The C-CDA format is appropriate for the clinical data it covers (it maps well to standard clinical concepts). However, the PDF format for billing, scheduling, and administrative data means that critical operational data would be exported in a non-computable, non-interoperable format with no documented structure.

### Documentation Quality

**Strengths:**
- The C-CDA data dictionary (pages 6–10) is reasonably detailed, with XPATH entries, OID-identified code systems, and code system names for each data element.
- Screenshots of the export interface for both single-patient and bulk export are included, showing the actual UI.
- The document is organized with a clear table of contents.

**Weaknesses:**
- The non-clinical exports (page 11) receive one sentence each with no field-level documentation. "PDF format - This file offers a comprehensive view of billing data (CPT, ICD, Modifier), structured for clarity and ease of access" tells a developer essentially nothing about what fields are included, how they're structured, or what data is represented.
- The FHIR section (page 12) is a single sentence with no actionable documentation.
- No sample export files or example data are provided.
- No version history or change tracking.
- No documentation of relationships between exported components (e.g., how does the C-CDA XML relate to the PDF billing data? Are they linked by patient ID?).
- The document reads like a compliance checkbox — the clinical data dictionary was likely copied from existing C-CDA implementation documentation, while the non-clinical sections were written minimally.

### Structure & Completeness

- **Clinical data (C-CDA)**: Moderate granularity. Table/section names, field names (via XPATH), and code systems are provided. Data types and cardinality are not explicitly documented (these are implicit in the C-CDA standard). Value sets are identified by OID but not enumerated. This is adequate for someone familiar with C-CDA but relies heavily on knowledge of the underlying standard.
- **Non-clinical data (PDF)**: No granularity. Just category names with no field-level detail.
- **FHIR export**: No granularity. A single sentence claiming FHIR Bulk Data support with no specifics.
- Relationships between entities are not documented.
- No versioning or change history beyond "Version: V2.0" on the cover.

## Access Summary
- Final URL (after redirects): https://carecloud.com/cc-prime/
- Status: found
- Required browser: no (direct PDF download via curl)
- Navigation complexity: one_click (PDF link in footer of the registered URL)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered URL (https://www.carecloud.com/cc-prime/) is a product marketing page, not a dedicated EHI documentation page. The EHI export PDF is buried in the footer under a "Real World Testing Plan" heading alongside unrelated regulatory documents.
- The link text uses a dollar sign ($170.315) instead of the section symbol (§170.315).
- The page title is "CareCloud Medical Transcription Services" which doesn't match the page content (it's the CareCloud Prime product page) — suggesting the page may have been repurposed or the title metadata is wrong.
- The FHIR API reference (`aptivio.azure-api.net`) found in the page source returns 404 — no usable FHIR documentation was accessible.
- No additional EHI export documentation was found on the mandatory disclosures page or elsewhere on the site.
