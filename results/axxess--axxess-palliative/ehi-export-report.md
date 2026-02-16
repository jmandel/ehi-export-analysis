# Axxess — EHI Export Documentation (Axxess Palliative)

Collected: 2026-02-15

## Source
- Registered URL: https://www.axxess.com/cehrt/
- CHPL IDs: 11620
- Product: Axxess Palliative, Version 3.0.2022
- Certification date: 2025-03-13

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://www.axxess.com/cehrt/"` returned HTTP 200, Content-Type: text/html, served by nginx/PHP. No redirects.

2. **Page fetch and examination** — `curl -sL "https://www.axxess.com/cehrt/" -o /tmp/page.html` returned a 165KB HTML page titled "CEHRT | Axxess". The page is a static compliance/certification hub with a "What is CEHRT?" heading and two columns of document links.

3. **Document links found** — Searched for downloadable files:
   ```
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)[^"]*"' /tmp/page.html
   ```
   Relevant results:
   - `/assets/pdf/b10-electronic-health-information-export.pdf` — **Primary EHI export document**
   - `/assets/pdf/Axxess-CEHRT-Disclosures-V3.0.2022.pdf` — CEHRT disclosures (includes b(10) capability description)
   - `/assets/pdf/Compliance-Certificate-Axxess-Palliative-Version-3.0.2022-040825.pdf` — Compliance certificate (not downloaded; not technical)
   - Real-World Testing Plans/Reports for 2024 and 2025 (not downloaded; not EHI export docs)

4. **Downloaded the b10 PDF**:
   ```bash
   curl -sL "https://www.axxess.com/assets/pdf/b10-electronic-health-information-export.pdf" -o downloads/b10-electronic-health-information-export.pdf
   ```
   Verified: `file` confirms PDF document, version 1.6, 148,257 bytes, 1 page.

5. **Downloaded the CEHRT Disclosures PDF**:
   ```bash
   curl -sL "https://www.axxess.com/assets/pdf/Axxess-CEHRT-Disclosures-V3.0.2022.pdf" -o downloads/Axxess-CEHRT-Disclosures-V3.0.2022.pdf
   ```
   Verified: PDF document, version 1.7, 3 pages, 210,127 bytes.

6. **Checked for additional documentation** — Searched the CEHRT page for links to FHIR API docs, help pages, and other potential EHI export resources:
   - `https://engage.axxess.com/api.html` — Partner API specifications (marketing/lead-gen page, not EHI export)
   - `https://fhirpresentationdev.axxessweb.com/fhir/r4/endpoints` — FHIR endpoint listing (g)(10), not (b)(10)
   - `https://r4dev.dynamicfhirsandbox.com/dhit/practicetwo/r4/Home/ApiDocumentation` — FHIR API sandbox docs (timed out; irrelevant to b(10))
   - `https://www.axxess.com/help/axxess-palliative-care/` — Help center with ~40+ articles covering clinical, billing, admin features. No article specifically about "Download Patient Chart" or EHI export was found in the listing.

7. **Took full-page screenshot** of the CEHRT page using browser automation.

8. **Examined b10 PDF content** — Used `pdftotext` to extract text. The entire document is a single page with overview, file formats, and export process instructions. No embedded URLs, no attachments. Notable: the closing sentence reads "This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking" — an internal note that was apparently left in the public-facing document.

9. **Examined CEHRT Disclosures PDF** — 3-page document listing all certified criteria with brief descriptions. The (b)(10) entry states: "Axxess Palliative enables a user to timely create an export file(s) with all of a single patient's or population of patient's electronic health information that can be stored." No additional technical detail.

## What Was Found

The EHI export documentation consists of a **single 1-page PDF** (`b10-electronic-health-information-export.pdf`) that provides a brief overview of the export functionality. Here is the entirety of the substantive content:

**Export Format:**
- **XML**: Patient data conforming to C-CDA version 2.1 specification
- **PDF**: Rendered patient documents

**Export Mechanism:**
- Navigate to Patients → Download Patient Chart
- Select Branch, date range, patient(s), and desired file format
- Click "Request Documents" (enters a processing queue)
- When status shows "Ready", click "Export" to download a ZIP file
- Each patient's data is organized in individual ZIP folders labeled `LASTNAME_FIRSTNAME`

**Scope:** Single patient or population (multiple patients)

**No data dictionary is provided.** There is no documentation of:
- What specific data elements are included in the C-CDA export
- Which C-CDA sections/templates are populated
- Whether the export covers data beyond standard C-CDA sections
- How billing data, palliative-care-specific assessments, or specialty clinical data are represented
- Sample export files or example output
- Any schema or machine-readable format specification beyond "C-CDA 2.1"

The internal-sounding closing sentence — "This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking" — suggests this documentation was drafted as an interim compliance artifact rather than a thorough technical specification.

## Export Coverage Assessment

### Data Domain Coverage

Axxess Palliative stores a rich set of data as documented in the product research: patient demographics, clinical visit notes, vital signs, symptom assessments, diagnoses, medications (with eMAR), allergies, infectious disease tracking, implantable devices, family health history, advance directives, comprehensive plan of care, physician communications, orders (medications, DME, supplies), IDG meeting records, Medicare Part B billing/claims, CPT codes, ERA data, payroll, insurance eligibility, and more.

The export documentation provides **no specifics whatsoever** about which data domains are included. It states only that the export produces "comprehensive patient data" in C-CDA 2.1 format.

**Critical concern: C-CDA 2.1 is structurally insufficient for "all electronic health information."** C-CDA is designed for clinical summary exchange (transitions of care, discharge summaries, referral notes). It has standardized sections for:
- Demographics, problems, medications, allergies, procedures, results, vital signs, immunizations, plan of care, social history, encounters, functional status

It does **not** have standard sections for:
- **Billing records** (claims, CPT codes, ERA data, payer information, financial transactions)
- **Palliative care-specific assessments** (symptom ratings, IDG meeting documentation, comprehensive plan of care details)
- **Orders management** (DME orders, supply orders, order workflows)
- **Scheduling data** (though this is borderline EHI)
- **Payroll and financial data** related to patient billing

This means the C-CDA export likely covers only the clinical summary slice of the patient record — analogous to a (b)(1) Transition of Care export — and misses significant portions of the designated record set. Without a data dictionary or detailed documentation, it's impossible to confirm, but the choice of C-CDA 2.1 as the sole structured format strongly suggests this is a (g)(10)-adjacent clinical summary, not a true (b)(10) "all EHI" export.

The alternative PDF format likely captures rendered versions of documents and notes, which could theoretically include more data, but PDFs are not computable and there's no documentation of what the PDF export contains.

**Domains likely covered** (by virtue of C-CDA 2.1):
- Demographics
- Diagnoses/problems
- Medications
- Allergies
- Vital signs
- Immunizations
- Procedures
- Lab/diagnostic results (if applicable)
- Encounters
- Clinical notes (as unstructured text in C-CDA sections)

**Domains likely missing or unverifiable:**
- Billing records (claims, charges, payments, CPT codes, ERA)
- Insurance/payer details
- Palliative-specific clinical assessments and symptom ratings
- IDG meeting records and documentation
- Orders (DME, supplies)
- Comprehensive plan of care (palliative-specific detail beyond C-CDA's generic plan of care section)
- Advance directives (may be partially in C-CDA)
- Physician communications
- Emergency preparedness documentation
- Referral tracking data

### Export Format & Standards

- **Format**: C-CDA 2.1 XML and PDF, delivered in a ZIP archive
- **Standard**: C-CDA (Consolidated Clinical Document Architecture) version 2.1 is a recognized HL7 standard for clinical document exchange
- **Appropriateness**: C-CDA is appropriate for clinical summaries but is a poor fit for exporting "all electronic health information" from a palliative care EHR. A palliative care product stores specialty-specific data (symptom assessments, IDG records, comprehensive plans of care, billing) that doesn't map to C-CDA sections.
- **Reconstruction**: A third party could reconstruct a basic clinical summary from the C-CDA export but almost certainly could not reconstruct the full patient record, especially billing, palliative-specific assessments, and administrative data.

### Documentation Quality

The documentation quality is **extremely poor**:
- A single page with no technical depth
- No data dictionary at all
- No field-level definitions
- No data types, value sets, or constraints
- No sample exports or worked examples
- No schema files or machine-readable specifications
- No description of which C-CDA templates or sections are used
- Contains an internal note ("This should comply with what we need and buy us time to finish the feature") that was not removed before publication
- The documentation reads as an internal memo rather than a technical specification

A developer could not implement an import of this data based on this documentation alone. They would know only that the export is "C-CDA 2.1 XML" in a ZIP — they'd need to reverse-engineer the actual structure from sample exports.

### Structure & Completeness

- **Granularity**: Zero field-level documentation. Not even table-level or section-level documentation.
- **Value sets**: Not documented
- **Relationships**: Not documented
- **Versioning**: The PDF was created December 15, 2023. No change history.
- **Machine-readable artifacts**: None provided

## Access Summary
- Final URL (after redirects): https://www.axxess.com/cehrt/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (PDF linked directly from CEHRT page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The FHIR API sandbox documentation (`r4dev.dynamicfhirsandbox.com`) timed out but was determined to be (g)(10) documentation, not relevant to the (b)(10) export.
- The partner API page (`engage.axxess.com/api.html`) is a marketing/lead-gen page, not technical documentation.
- The help center (`axxess.com/help/axxess-palliative-care/`) has ~40+ articles but none specifically about the "Download Patient Chart" EHI export feature. This is a gap — users have no publicly accessible guide for performing the export.
- No enrichment was performed because the documentation corpus consists of only two PDFs (one 1-page, one 3-page) with no structured data to extract.
