# CloudCraft, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://cloudcraftsoftware.com/certification/B10.html
- CHPL ID: 11150
- CHPL Product Number: 15.04.04.3071.Clou.09.01.1.221227
- Product: CloudCraft Software v9.0
- Certification date: 2022-12-27

## Navigation Journal

**Step 1: Probe the registered URL.**
```bash
curl -sI -L "https://cloudcraftsoftware.com/certification/B10.html" -H 'User-Agent: Mozilla/5.0'
```
HTTP/2 200, Content-Type: text/html, 6525 bytes. Hosted on S3 behind CloudFront. Last-Modified: 2023-12-14.

**Step 2: Download and examine the page.**
```bash
curl -sL "https://cloudcraftsoftware.com/certification/B10.html" -H 'User-Agent: Mozilla/5.0' -o B10.html
```
Static HTML page, no JavaScript SPA. Contains two sections ("Provider Export" and "Patient Export Requests"), five workflow diagram images, and a client-side "Download as PDF" button (html2pdf.js — generates PDF from the DOM, no server-side PDF).

**Step 3: Download all referenced images.**
```bash
for img in img1.gif img2.png img3.gif img4.gif img5.gif arrow1.png CloudCraft.png; do
  curl -sL "https://cloudcraftsoftware.com/Images/$img" -H 'User-Agent: Mozilla/5.0' -o "$img"
done
```
All 7 images downloaded and verified as valid image files (GIF/PNG).

**Step 4: Take browser screenshot.**
Navigated to the page in Chrome and took a full-page screenshot for visual reference.

**Step 5: Search for additional documentation.**
Checked:
- Homepage (cloudcraftsoftware.com) — links to certificationcriteria.html, feature.html, complianceactivities.html, realworldtesting.html, clinicalqualitymeasures.html, ggmeasures.html, safetyenhanced.html, casestudies.html. None link to B10 or additional EHI export documentation.
- certificationcriteria.html — mentions "Electronic Health Information Export" as a line item but no link to additional docs.
- Mandatory disclosures URL (certificationdisclosurestatements) — same navigation links as homepage, no EHI-specific content.
- Probed /certification/ directory for other pages (data-dictionary.html, ehi.html, export.html, schema.html, G10.html) — all return the homepage (30028 bytes, S3 default error document). Only B10.html (6525 bytes) is a distinct page.
- Probed for downloadable files (certification/B10.pdf, certification/data-dictionary.pdf, etc.) — all return 30028 bytes of HTML (the homepage), not actual PDFs.
- No links to external documentation, FHIR API specs, data dictionaries, or downloadable schema files anywhere on the site.

**Conclusion: The B10.html page is the entirety of CloudCraft's public (b)(10) EHI export documentation.**

## What Was Found

The B10 page is a single-page HTML document (~6.5 KB) with two sections:

### Provider Export
Describes a "secure, one-time bulk export of all primary care provider patient data, including meme [sic — likely 'MIME'] document types for PDF, TIF, PNG, and WORD." A five-step workflow is shown with icons:
1. Patient(s) submit requests
2. Access Bulk Download From Admin Console
3. Select Patients requesting Primary care provider Access
4. User selects secure Download location
5. User give provider Secure access

The exported "Bulk Data" consists of:
- C-CDA USCDI v3
- PDF documents, including scanned paper and digital records of faxes
- Image files (JPEG, GIF, TIF)
- Word documents
- Internal correspondence such as tasks, notes

### Patient Export Requests
States that "CloudCraft FHIR supports the FHIR R4 DocumentReference resource" which "can be used with any document format with a recognized mime type." Mentions connections to FHIR apps (MyLinks, Apple Health, etc.) and lists the same bulk data items.

### Key observations
- There is **no data dictionary** — no table/field definitions, no schema, no column listings.
- There is **no export format specification** beyond naming C-CDA USCDI v3 and listing document types.
- There is **no API documentation** — the FHIR DocumentReference mention is a single sentence.
- There are **no sample files** or worked examples.
- There are **no machine-readable schema files** (XSD, JSON Schema, OpenAPI, etc.).
- The "Download as PDF" button uses client-side html2pdf.js to render the page as a PDF — there is no server-hosted PDF version.
- The page was last modified 2023-12-14, about a year after certification (2022-12-27).

## Export Coverage Assessment

### Data Domain Coverage

CloudCraft is described as an "all-in-one solution for electronic health records, practice management, billing, and human resources" targeting FQHCs and community health centers. Based on the product research, it stores:

**Clearly covered by the documented export:**
- Clinical document summaries (via C-CDA USCDI v3) — this covers demographics, problems, medications, allergies, lab results, vitals, immunizations, procedures, and other USCDI data classes
- Scanned documents and faxes (PDF)
- Image files (JPEG, GIF, TIF)
- Word documents
- Internal correspondence (tasks, notes)

**Not mentioned or clearly missing:**
- **Billing data** — CloudCraft has a distinct billing module (cloudcraft-billing.naiacorp.net), but the export documentation makes no mention of billing records, claims, charges, payments, or financial data
- **Sliding fee scale data** — a dedicated FQHC module exists but is absent from the export
- **Practice management data** — scheduling, registration, and administrative workflows are not mentioned
- **Medication administration records** — C-CDA USCDI v3 may include medication lists, but detailed prescribing/administration records are not specifically addressed
- **Lab interface data** — orders and results beyond what's in C-CDA summaries
- **Diagnostic imaging orders** — certified for CPOE under (a)(3), but imaging data beyond what's in C-CDA is unaddressed
- **Family health history** — certified under (a)(12), unclear if captured in C-CDA exports
- **Clinical decision support data** — rules, alerts, and their outcomes
- **Care plans and goals** — may be in C-CDA but not explicitly documented
- **Patient portal data** — amendment requests, portal messages
- **Custom/specialty clinical data** — behavioral health assessments, FQHC-specific screening tools

The fundamental problem is that the export is described as "C-CDA USCDI v3 + documents." C-CDA USCDI v3 covers a well-defined subset of clinical data (the USCDI v3 data classes), but an EHR that also does billing, practice management, sliding fee calculations, and HR stores substantially more data than what USCDI covers. The export documentation does not address how any of that non-USCDI data is exported — or whether it is exported at all.

### Export Format & Standards

The export uses two formats:
1. **C-CDA USCDI v3** — a well-established standard for clinical document exchange. This is a reasonable choice for clinical summary data.
2. **Raw documents** — PDF, images, Word files, and other MIME-typed documents delivered via FHIR R4 DocumentReference.

This is essentially a (g)(10)-style approach repackaged as (b)(10). C-CDA USCDI v3 covers the same data domains as the USCDI/US Core requirement — it does not inherently include billing, practice management, or other non-clinical data. The documentation makes no mention of how structured data beyond USCDI is exported (e.g., as database dumps, CSV files, or additional FHIR resources).

A third party could reconstruct a clinical summary from C-CDA documents and view attached documents, but could not reconstruct a complete patient record including billing history, appointment history, sliding fee calculations, or other practice management data.

### Documentation Quality

The documentation is extremely sparse:
- **No data dictionary** — there are zero field-level definitions anywhere
- **No schema documentation** — no description of the C-CDA templates used, constraints applied, or extensions
- **No API documentation** — the FHIR DocumentReference mention is a single sentence with no endpoint, authentication, or request/response details
- **No sample files** — no example C-CDA document, no sample export package
- **No export instructions** — the workflow diagram shows five high-level steps with icons but no detailed user guide
- **No error handling or edge cases** — what happens with large records, special characters, incomplete data?
- A developer could not implement an import of this data based solely on the documentation. They would know to expect C-CDA documents and various document types, but nothing about the specific structure, packaging, delivery mechanism, or API details.

The documentation reads as a compliance checkbox — the minimum needed to have something at the registered URL.

### Structure & Completeness

- **Granularity**: The documentation operates at the "format name" level only. It says "C-CDA USCDI v3" without specifying which C-CDA document types, which sections, or which data elements. It lists document types (PDF, JPEG, etc.) without describing how they're organized or packaged.
- **Coded fields**: Not documented at all.
- **Relationships**: Not documented.
- **Value sets**: Not documented.
- **Versioning**: No version history. The page was last modified 2023-12-14.

### Overall Assessment

CloudCraft's (b)(10) documentation is among the most minimal possible. It amounts to: "we export C-CDA documents and attached files." There is no evidence that the export covers the full breadth of data the product stores — particularly billing, practice management, and FQHC-specific modules. The documentation provides no technical detail that would allow a recipient to understand, validate, or import the exported data beyond recognizing standard C-CDA format. This appears to be a (g)(10)-equivalent export relabeled as (b)(10), with no effort to address the broader EHI scope that (b)(10) requires.

## Access Summary
- Final URL: https://cloudcraftsoftware.com/certification/B10.html
- Status: found
- Required browser: no (static HTML, no JavaScript required for content)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- S3 bucket serves the homepage (30028 bytes) as the default error document for all unrecognized paths, making it impossible to distinguish real 404s from the default response without checking content size.
- No additional EHI documentation exists on the site beyond the single B10.html page.
- The "Download as PDF" button is client-side only (html2pdf.js), producing a rendering of the same page content.
- Checked G10.html — returns the homepage, not a real page.
- No downloadable files (PDF, ZIP, etc.) were found at any probed paths.
