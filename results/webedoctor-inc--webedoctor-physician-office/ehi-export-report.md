# WEBeDoctor, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://new.webedoctor.com/certification/
- CHPL ID: 11748
- Product: WEBeDoctor Physician Office v6.0
- Certification Date: 2026-01-13
- Certification Body: SLI Compliance

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://new.webedoctor.com/certification/"` returned HTTP 200, Content-Type: text/html. This is a WordPress site (Elementor-based) hosted on Bluehost with Apache.

2. **Fetched and examined the page** — 132KB HTML page titled "Certification and Costs." The page is a compliance hub listing mandatory disclosures, Real World Testing (RWT) plans/results for 2022–2025, and one EHI export entry.

3. **Searched for downloadable file links:**
   ```
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/webedoctor-cert.html
   ```
   Found 9 PDF links:
   - Mandatory Disclosures (2026-01 signed)
   - RWT Plans/Results for 2022, 2023, 2024, 2025
   - **WEBeDoctor_EHI_Export.pdf** — the only EHI-relevant document

4. **Downloaded the EHI Export PDF:**
   ```
   curl -sL "https://new.webedoctor.com/wp-content/uploads/2025/06/WEBeDoctor_EHI_Export.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o downloads/WEBeDoctor_EHI_Export.pdf
   ```
   Verified: `file` confirms PDF document, 3 pages, 859,649 bytes. Created 2023-10-27 by Syed Imran Ali using Microsoft Word 2007.

5. **Extracted PDF text** with `pdftotext` and rendered all 3 pages as images with `pdftoppm` for visual inspection. The PDF contains:
   - A brief introduction stating WEBeDoctor uses C-CDA 2.1 for (b)(10) export
   - A screenshot of the User Configuration page showing "Enable EHI Export" buttons
   - A screenshot of the single-patient export interface (Hub > EHI Export > One Time)
   - A screenshot of the CCDA List showing generated exports with Download buttons
   - A screenshot of the all-patients export interface with "All Patients" checkbox

6. **Checked for embedded URLs and attachments** in the PDF:
   - One URL: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447 (external C-CDA spec — not our concern)
   - No embedded file attachments

7. **Searched for additional EHI documentation** across the entire WordPress site:
   - Queried WP REST API for pages (`/wp-json/wp/v2/pages`) — 28 pages found, none related to EHI/export/data dictionary/FHIR API
   - Searched WP media library for "ehi", "export", "data dictionary", "schema" — only the single PDF exists
   - Searched WP posts for "ehi" — no results
   - Probed common documentation paths (/interoperability/, /fhir/, /api/, /ehi/, /developer/, /api-docs/) — all returned 406

8. **Captured full-page screenshot** of the certification page showing the page layout and the EHI Export card at the bottom.

## What Was Found

WEBeDoctor's entire EHI export documentation consists of a single 3-page PDF dated October 2023. The document states:

> "WEBeDoctor is compliant with §170.315(b)(10) Electronic Health Information Export by generating C-CDA 2.1 electronic documents."

The export mechanism works as follows:
- **Access control:** A facility admin must enable EHI Export for each user via Administration > User Configuration > "Enable EHI Export" button
- **Single patient export:** Hub > EHI Export > One Time > Select Patient > Save. A C-CDA file is generated and available for download from Hub > EHI Export > CCDA List > Download
- **Population export:** Hub > EHI Export > One Time > Check "All Patients" checkbox > Save. A ZIP file of all C-CDA files for all patients is generated and available from Hub > EHI Export > CCDA List > Download
- **Output format:** C-CDA 2.1 XML documents, one per patient, delivered as individual files or bundled in a ZIP

There is no data dictionary, no field mapping, no schema documentation, no sample export files, and no description of what data elements are included in the C-CDA documents beyond the standard reference link to hl7.org.

## Export Coverage Assessment

### Data Domain Coverage

This is a textbook case of the (b)(10) vs (g)(10) confusion. WEBeDoctor's EHI export produces C-CDA 2.1 documents, which is an HL7 standard designed for clinical document exchange (transitions of care). C-CDA covers a defined set of clinical data — essentially the USCDI data classes — but not the full designated record set.

Based on the product research, WEBeDoctor Physician Office stores extensive data across these domains:

**Likely covered by C-CDA 2.1 (standard clinical summary data):**
- Patient demographics
- Problem lists / diagnoses
- Medication lists and prescriptions
- Allergies
- Lab results
- Vital signs
- Immunizations
- Procedures
- Clinical notes (to some degree — C-CDA supports notes but implementations vary)
- Care plans
- Family health history

**Almost certainly missing from C-CDA export:**
- **Billing and claims data** — electronic claims, payment records, adjustments, EDI transaction data, patient statements. C-CDA has no billing sections.
- **Practice management data** — insurance verification records, scheduling data tied to encounters
- **E-prescribing details** — full prescription history with pharmacy routing, controlled substance records, refill management history. C-CDA includes a medication list but not the complete e-prescribing workflow data.
- **Patient portal communications** — secure messages between patients and office staff, appointment requests, refill requests
- **Remote patient monitoring data** — blood pressure readings, weight measurements, glucose readings from RPM devices
- **Telehealth visit records** — virtual visit metadata and encounter specifics
- **Electronic fax records** — sent/received faxes that are part of the patient record
- **Clinical images with annotations** — the vendor supports image annotation tools; C-CDA XML cannot carry full image data with annotations
- **Transcription records** — if stored within the system
- **Chronic care management / RTM documentation**
- **Custom specialty templates** — the vendor supports specialty-specific templates (cardiology, ophthalmology, podiatry, pediatrics, etc.); custom template fields likely don't map to C-CDA sections

The documentation provides no indication that WEBeDoctor has considered these gaps. There is no mention of supplementary export mechanisms, no discussion of data that falls outside C-CDA, and no acknowledgment that C-CDA represents a subset of the data the system stores.

### Export Format & Standards

- **Format:** C-CDA 2.1 (XML)
- **Standard:** HL7 Consolidated Clinical Document Architecture Release 2.1
- **Appropriateness:** C-CDA is a recognized clinical document standard, but it is designed for transitions of care — clinical summaries exchanged between providers. It was not designed to be a complete database export format. Using C-CDA as the sole (b)(10) export mechanism means the export will contain only the clinical data that maps to C-CDA templates and sections.
- **Reconstruction capability:** A third party could reconstruct a clinical summary from the C-CDA, but could not reconstruct the full patient record including billing, communications, specialty assessments, and monitoring data.

### Documentation Quality

The documentation is **minimal**. The entire EHI export documentation is 3 pages consisting of:
- One paragraph of introduction
- Four screenshots of the WEBeDoctor interface
- Brief navigation instructions for each screenshot

**What's missing:**
- No data dictionary or field mapping
- No description of which C-CDA sections are populated or what data elements are included
- No C-CDA template/profile constraints (which templateIds, which optional sections are included)
- No sample export file
- No data type specifications
- No value set documentation for coded fields
- No description of how WEBeDoctor-specific data maps to C-CDA elements
- No information about export completeness or data scope
- No error handling or troubleshooting guidance
- No versioning or change history

A developer receiving a C-CDA file from this export would need to reverse-engineer the content by examining actual export files. The documentation tells you only *how to click the buttons*, not *what data you'll get*.

### Structure & Completeness

- **Granularity:** Zero field-level documentation. Not even table-level. The document mentions "C-CDA 2.1" and links to the HL7 spec, implying "it's standard C-CDA, go read the spec."
- **Coded fields:** Not documented
- **Relationships:** Not documented
- **Value sets:** Not documented
- **Versioning:** No version number or change history. PDF creation date is October 2023; the upload path suggests it was uploaded to the WordPress site in June 2025.

## Access Summary
- Final URL (after redirects): https://new.webedoctor.com/certification/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (certification page → PDF download link)
- Anti-bot issues: none (standard User-Agent header sufficient; ModSecurity blocks some paths but not the relevant ones)

## Obstacles & Dead Ends
- The WordPress site has ModSecurity enabled, which returned 406 errors for arbitrary path probes. This did not affect access to the actual documentation.
- The WP REST API is accessible and confirmed that no additional EHI-related pages, posts, or media exist beyond the single PDF.
- No sitemap.xml was accessible (ModSecurity blocked it).
- The PDF was created in October 2023 and appears unchanged since then, despite the product being re-certified in January 2026 (version 6.0). The documentation may be stale relative to the current product version.
