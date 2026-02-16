# CareCloud, Inc. — talkEHR — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.talkehr.com/cost-and-fees-information
- CHPL IDs: 9799
- Certification Number: 15.04.04.2790.Talk.01.01.1.181217
- Certification Date: 2018-12-17

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```bash
   curl -sI -L "https://www.talkehr.com/cost-and-fees-information" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `text/html; charset=utf-8`, served via Cloudflare CDN. No redirects.

2. **Page fetch and examination** — Downloaded the full HTML page (61,274 bytes). The page is CareCloud/talkEHR's ONC mandatory disclosures page listing all 45+ certified criteria, CQMs, software dependencies, and compliance links.

3. **Link extraction** — Searched for document links on the page:
   ```bash
   grep -oiE 'href="[^"]*"' /tmp/talkehr-page.html | sort -u
   ```
   Found one EHI-relevant PDF link in the footer under "Legal & Compliance":
   - `§170.315(b)(10) Electronic Health Information export - Documentation` → `https://cdn.prod.website-files.com/6040fac6832b627ac2ffc9ad/6553a43229cacaf138511818_talkEHR%20Certification%20-%20%C2%A7170.315(b)(10)%20Electronic%20Health%20Information%20Export%20-%20Documentation.pdf`

   Other PDFs on the page are Real World Testing Plans/Results (2022–2025) — not EHI export documentation.

4. **PDF download and verification**:
   ```bash
   curl -sL "https://cdn.prod.website-files.com/6040fac6832b627ac2ffc9ad/6553a43229cacaf138511818_talkEHR%20Certification%20-%20%C2%A7170.315(b)(10)%20Electronic%20Health%20Information%20Export%20-%20Documentation.pdf" -H 'User-Agent: Mozilla/5.0' -o talkEHR-b10-EHI-Export-Documentation.pdf
   ```
   Verified: `file` reports "PDF document, version 1.5, 12 page(s)" — 1,129,138 bytes. Created 2023-11-14 by Jahanzaib Nisar using Microsoft Word 2013.

5. **PDF analysis** — Extracted full text via `pdftotext`, checked for embedded URLs (none found), checked for embedded file attachments (0 found), rendered key pages as images for visual inspection (screenshots of UI on pages 4–5).

6. **Browser verification** — Navigated to the URL in Chrome, confirmed the page renders correctly and the b(10) link is visible in the footer under "Legal & Compliance". Took screenshots.

## What Was Found

The sole EHI export documentation is a 12-page PDF titled "§170.315(b)(10) Electronic Health Information Export – Documentation." It describes talkEHR's approach to EHI export using a combination of two output formats:

### Export Format 1: C-CDA XML (Clinical Data)

For structured clinical data, talkEHR uses CCD (Continuity of Care Document) export conforming to the HL7 C-CDA R2.1 standard (§ 170.205(a)(4)). Two modes are available:

- **Single Patient Export**: Navigate to CCDA Report → CCDA Export tab → select patient → Generate → Download as XML. A screenshot in the PDF shows the UI with tabs for "CCDA Import", "CCDA Export", "Data Portability", and "Summary of Care Request."
- **Bulk Patient Export (Data Portability)**: Navigate to CCDA Report → Data Portability tab → select date range → Export. A ZIP file is downloaded containing CCDA XML files. A screenshot shows the export yielding a ZIP file (e.g., `WebEHR_Documents2_111_talkEHR_TempA...zip`, 54.1 KB).

The CCD output contains these sections (documented with XPATHs and code systems on pages 6–10):

| Section | Code Systems |
|---------|-------------|
| Patient Demographics | AdministrativeGender, CDC Race & Ethnicity |
| Provider Info | — |
| Date and Location of visit | — |
| Chief Complaint and Reason for Visit | — |
| Encounters | CPT, SNOMED, ICD-10 |
| Immunizations | CVX, CPT-4, NCI Thesaurus, SNOMED |
| Instructions | — |
| Treatment Plan (Planned Observations) | LOINC |
| Social History | LOINC, SNOMED |
| Problems | SNOMED, ICD-10 |
| Medications | RxNorm, NDC |
| Medication Allergies | RxNorm, SNOMED |
| Laboratory Tests & Results | LOINC |
| Vitals | LOINC |
| Goals | — |
| Procedures | CPT-4, SNOMED, HCPCS |
| Care Team Members | — |
| Reason for Referral | SNOMED |
| Medical Equipment (Implantable Devices) | SNOMED, GMDN |
| Mental Status | SNOMED |
| Functional Status | SNOMED |
| Health Concern | SNOMED |

### Export Format 2: PDF (Non-Clinical Data)

For data that doesn't fit the C-CDA structure, talkEHR exports in PDF format:

- **Patient Demographic/Insurance** — "a comprehensive view of demographics and insurance details"
- **Advance Directive** — "a comprehensive view of Advance Directive"
- **Appointments** — "a comprehensive view of appointments"
- **Provider-to-Patient Messages** — "a comprehensive view of messages"
- **Billing Data (Claim)** — "a comprehensive view of billing data (CPT, ICD, Modifier)"
- **Documents** — "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" in PDF format

These are accessed via the application's "Reports" section.

### Organizational Structure

The documentation states: "The files created by the export are saved to a folder specified by the user. Documents can be sorted and categorized as per their Type, e.g., Lab Reports and Imaging etc."

### FHIR Data Export

The final page mentions: "talkEHR FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)." No further details are provided about the FHIR export — no endpoint URLs, resource types, profiles, or API documentation.

### Timeliness

"A user of the Product can perform an electronic health information (EHI) export for at any time the user chooses without developer assistance and that the export files are created in a timely fashion."

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, talkEHR stores clinical data, e-prescribing data, practice management data, billing/financial data, patient engagement data, public health reporting data, document/imaging data, and audit/security data.

**Clearly covered in the export:**
- **Demographics and insurance** — via both C-CDA and dedicated PDF export
- **Diagnoses/problems** — in C-CDA (SNOMED, ICD-10)
- **Medications and prescriptions** — in C-CDA (RxNorm, NDC)
- **Allergies** — in C-CDA (medication allergies with reactions/severity)
- **Immunizations** — in C-CDA (CVX codes)
- **Lab results** — in C-CDA (LOINC) and as PDF documents
- **Vitals** — in C-CDA (LOINC)
- **Procedures** — in C-CDA (CPT-4, SNOMED, HCPCS)
- **Encounters** — in C-CDA (CPT, SNOMED, ICD-10)
- **Social history** — in C-CDA (LOINC, SNOMED)
- **Mental/functional status** — in C-CDA (SNOMED)
- **Care plans and goals** — in C-CDA
- **Care team members** — in C-CDA
- **Referrals** — in C-CDA (reason for referral)
- **Implantable devices** — in C-CDA (medical equipment section)
- **Advance directives** — dedicated PDF export
- **Appointments** — dedicated PDF export
- **Billing data (claims)** — dedicated PDF export with CPT, ICD, Modifier
- **Provider-to-patient messages** — dedicated PDF export
- **Clinical documents** — progress notes, lab results, radiology reports, scanned/uploaded documents exported as PDFs

**Potentially missing or unclear:**
- **E-prescribing details** — prescription records appear in the C-CDA medications section, but refill request management, drug interaction alert history, pharmacy information, and controlled substance prescription details may not be fully captured. The medications section maps to RxNorm/NDC but doesn't mention prescription workflow data.
- **Family health history** — the product is certified for (a)(12) Family Health History but this section does not appear in the documented CCD output sections.
- **Patient portal activity** — the product has talkPHR (patient health records portal) with features like self-service appointment scheduling, secure messaging, demographic updates, and claims/statements review. The export includes provider-to-patient messages, but patient-initiated portal activity (demographic update requests, appointment requests, patient-entered data) is not explicitly mentioned.
- **Telehealth visit records** — the product supports HIPAA-compliant video visits integrated with the EHR, but telehealth-specific data (session recordings, virtual visit metadata) is not mentioned in the export.
- **Care plan details** — while the C-CDA includes a care plan section (b)(9), the granularity is unclear beyond what standard C-CDA supports.

### Export Format & Standards

The export uses a **dual-format approach**:

1. **C-CDA R2.1 XML** for structured clinical data — a well-established, recognized standard. The documentation provides a detailed field-level mapping with XPATHs and code systems for each section. This is the strongest part of the documentation.

2. **PDF** for non-clinical data (demographics/insurance, appointments, billing, messages, documents) — this is a human-readable format but **not machine-processable**. A third party receiving billing data as PDF could read it visually but would have significant difficulty importing it into another system. PDF export of structured data like billing claims (CPT, ICD, modifier codes) represents a loss of computability compared to what the system stores internally.

The brief mention of FHIR Bulk Data export on page 12 is essentially a one-sentence assertion with no technical details — no endpoint documentation, no resource type list, no profile specifications.

**Could a third party reconstruct the patient record?** Partially. The C-CDA clinical data is in a standard format that any C-CDA-compliant system could ingest. However, the PDF portions (billing, appointments, messages, documents) would require manual data entry or OCR to import into another system. The billing data in particular — which is structured, coded data internally — loses significant value when exported as PDF rather than as a computable format (CSV, 837 claims, or FHIR resources).

### Documentation Quality

- **Readability**: The PDF is reasonably well-organized with a table of contents, clear section headings, and screenshots of the export UI.
- **Data dictionary**: The CCD output section (pages 6–10) provides a useful field-level mapping with XPATHs, code system OIDs, and code system names. This is a genuine data dictionary for the C-CDA portion.
- **Missing detail for PDF exports**: The non-C-CDA sections (page 11) are extremely terse — each gets a single sentence saying it's exported in PDF format with no field-level detail. For billing data, knowing the format includes "CPT, ICD, Modifier" is helpful but there's no specification of what a billing PDF actually contains (claim number? date of service? amounts? payer info? adjustments?).
- **No sample data or examples**: No example C-CDA XML files, no sample PDF exports, no worked examples of what the output looks like beyond the UI screenshots.
- **FHIR documentation gap**: The FHIR Bulk Data mention on page 12 has zero technical detail. A developer would have no idea how to interact with this endpoint.
- **Could a developer implement an import?** For C-CDA: yes, using the standard. For PDF exports: no — the field-level structure is undocumented.

### Structure & Completeness

- **C-CDA mapping granularity**: Good — field names, XPATHs, code system OIDs, and code system names are specified for each data element across ~20 clinical sections.
- **Value sets**: Code system OIDs are listed (SNOMED, ICD-10, RxNorm, LOINC, CVX, etc.) but specific value set bindings within those code systems are not detailed.
- **Relationships between entities**: Implicitly captured by the C-CDA structure (e.g., encounters contain diagnoses, medications have routes/doses). Not separately documented.
- **Versioning**: The PDF is version V1.0, dated November 2023. No change history.
- **PDF export field specifications**: Absent. These sections have boilerplate descriptions without any field-level documentation.

### Overall Assessment

talkEHR's EHI export documentation represents a **reasonable but incomplete** attempt at (b)(10) compliance. The strongest aspect is the detailed C-CDA field mapping, which goes beyond what many vendors provide. The weakest aspects are:

1. **PDF as an export format for structured data** — Exporting billing claims, appointment schedules, and demographic/insurance data as PDF rather than a computable format (CSV, JSON, FHIR) means this data is effectively trapped. A recipient can read it but cannot efficiently import it. This is a significant limitation for true data portability.

2. **Minimal documentation for non-CDA exports** — The PDF export sections each get one generic sentence. There's no way to know what fields or structure to expect in a billing PDF, for example.

3. **FHIR Bulk Data claim without documentation** — Page 12 asserts FHIR Bulk Data support for (b)(10)(ii) but provides zero technical details. If this endpoint exists and works, it could potentially address many of the coverage gaps (since FHIR resources could represent billing, scheduling, and other data). But without documentation, it's impossible to assess.

4. **Family health history gap** — Certified for (a)(12) but not included in the documented export sections.

The documentation reads like a compliance document rather than an engineering specification. It demonstrates awareness of the requirement and describes a multi-format export approach that attempts to cover data beyond C-CDA's scope. But the heavy reliance on PDF output for structured data, combined with the lack of detail on what those PDFs contain, significantly limits the practical utility of the export.

## Access Summary
- Final URL (after redirects): https://www.talkehr.com/cost-and-fees-information
- Status: found
- Required browser: no (direct PDF link accessible via curl)
- Navigation complexity: one_click (PDF linked from footer of the registered URL page)
- Anti-bot issues: none (Cloudflare CDN but no blocking)

## Obstacles & Dead Ends
- None. The registered URL is live, the page loads correctly, and the PDF link works without authentication or special headers.
- The page is hosted on Webflow (Cloudflare CDN) and loads without JavaScript requirement for the key link.
- No additional EHI export documentation was found on the site beyond the single PDF.
