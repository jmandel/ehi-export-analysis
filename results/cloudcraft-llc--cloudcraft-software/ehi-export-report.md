# CloudCraft, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://cloudcraftsoftware.com/certification/B10.html
- CHPL IDs: 11150 (15.04.04.3071.Clou.09.01.1.221227)
- Product: CloudCraft Software v9.0
- Certified: 2022-12-27

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```
   curl -sI -L "https://cloudcraftsoftware.com/certification/B10.html" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `Content-Type: text/html`, 6525 bytes. Served via CloudFront/S3. No redirects. Last-Modified: 2023-12-14.

2. **Fetched the page** and examined the HTML source directly. The page is a static HTML file with no JavaScript navigation or SPA behavior. It includes a "Download as PDF" button implemented via `html2pdf.js` (client-side PDF generation from the rendered HTML — not a separate PDF artifact on the server).

3. **Downloaded all referenced assets**: The page references 5 workflow diagram images (`img1.gif` through `img5.gif`), an arrow graphic (`arrow1.png`), the CloudCraft logo (`CloudCraft.png`), a favicon, and a CSS stylesheet. All were downloaded from `cloudcraftsoftware.com/Images/` and `/Css/styles.css`.

4. **Searched for additional documentation**: Checked for downloadable files (PDF, ZIP, CSV, JSON, etc.) linked from the page — found none. The B10.html page contains no outbound links to other documentation.

5. **Explored the certification site** at `cloudcraftsoftware.com/certification/`:
   - The certification index is a separate SPA-style site with navigation links to: Home, Listing Information, Certification Criteria, Clinical Quality Measures, Safety Enhanced Design, G1/G2 Measures, Compliance Activities, Real World Testing, Case Studies.
   - None of these navigation items link to the B10.html page — it is only accessible via its direct URL (as registered on CHPL).
   - Checked `certificationcriteria.html`, `feature.html`, and others — all render the same generic "Welcome to CloudCraft" landing page with no criteria-specific content. These are placeholder pages.
   - The mandatory disclosures URL (`cloudcraftsoftware.com/certificationdisclosurestatements`) also returns the generic landing page.

6. **Probed for variant URLs**: Tested `b10.html`, `ehi.html`, `EHI.html`, `export.html`, `bulk-data.html` — all return the generic 30KB landing page. Only `B10.html` (capital B, exact match) serves the 6.5KB EHI export documentation.

7. **Checked FHIR endpoint**: Attempted to reach `fhirapitest.naiacorp.net/metadata` (referenced in product research) — connection timed out. This endpoint is not publicly accessible without authentication or network access.

8. **Rendered the page in a browser** and took a full-page screenshot to capture the visual workflow diagram.

## What Was Found

The B10.html page is a single, self-contained HTML page that constitutes the entirety of CloudCraft's EHI export documentation. It is divided into two sections:

### Provider Export

Describes a "secure, one-time bulk export of all primary care provider patient data." The workflow is illustrated with 5 icons:
1. Patient(s) submit requests
2. Access Bulk Download from Admin Console
3. Select patients requesting primary care provider access
4. User selects secure download location
5. User gives provider secure access

The "Bulk Data" section lists what the export includes:
- C-CDA USCDI v3
- PDF documents, including scanned paper and digital records of faxes
- Image files (JPEG, GIF, TIF)
- Word documents
- Internal correspondence such as tasks, notes

### Patient Export Requests

Describes a FHIR-based export pathway: "CloudCraft FHIR supports the FHIR R4 DocumentReference resource. This resource can be used with any document format with a recognized mime type." Lists the same bulk data types as above, and mentions FHIR App Connections via "MyLinks, Apple Health, etc."

### Key Observations

- The page has a typo: "including meme document types" (should be "MIME document types")
- There is **no data dictionary** — no table definitions, no field listings, no schema
- There is **no export format specification** beyond "C-CDA USCDI v3" and file types
- There are **no sample data files or examples**
- There are **no schema files** (no XSD, JSON Schema, OpenAPI spec)
- There are **no API endpoint specifications** — the FHIR section mentions DocumentReference but gives no URLs, authentication details, or parameters
- The "Download as PDF" button generates a client-side PDF from the HTML via html2pdf.js — there is no separate PDF artifact to download
- The documentation has not been updated since December 2023 (per Last-Modified header)

## Export Coverage Assessment

### Data Domain Coverage

The documentation describes an export that includes:
- **C-CDA USCDI v3 documents** — this covers the standard clinical data subset: demographics, problems, medications, allergies, lab results, vitals, immunizations, procedures, clinical notes, care plans, goals, and implantable devices
- **PDF/image/Word documents** — scanned paper records, faxes, and other document attachments
- **Internal correspondence** — tasks and notes

Based on the product research, CloudCraft stores data in these domains. Assessment of coverage:

| Domain | Covered? | Notes |
|--------|----------|-------|
| Demographics | Likely (via C-CDA) | USCDI v3 includes demographics |
| Problems/diagnoses | Likely (via C-CDA) | Standard USCDI data class |
| Medications | Likely (via C-CDA) | Standard USCDI data class |
| Allergies | Likely (via C-CDA) | Standard USCDI data class |
| Lab results | Likely (via C-CDA) | Standard USCDI data class |
| Vitals | Likely (via C-CDA) | Standard USCDI data class |
| Immunizations | Likely (via C-CDA) | Standard USCDI data class |
| Procedures | Likely (via C-CDA) | Standard USCDI data class |
| Clinical notes | Likely (via C-CDA) | Standard USCDI data class |
| Care plans/goals | Likely (via C-CDA) | Standard USCDI data class |
| Implantable devices | Likely (via C-CDA) | Standard USCDI data class |
| Family health history | Likely (via C-CDA) | Standard USCDI data class |
| Scanned documents/images | **Yes** | Explicitly listed (PDF, JPEG, GIF, TIF) |
| Word documents | **Yes** | Explicitly listed |
| Internal correspondence | **Yes** | Tasks and notes explicitly listed |
| **Billing data** | **Not mentioned** | CloudCraft advertises billing as a core module; no mention of billing data in the export |
| **Practice management data** | **Not mentioned** | No mention of scheduling, encounters, or PM data |
| **Sliding fee/financial data** | **Not mentioned** | FQHC-specific financial data not addressed |
| **Referrals** | **Unknown** | Not mentioned in export docs |
| **Clinical quality measure data** | **Unknown** | Not mentioned in export docs |
| **Order details beyond C-CDA** | **Unknown** | CPOE data structure not documented |

**Critical gap: billing data.** CloudCraft advertises "billing" as one of its four core modules (EHR, practice management, billing, HR). Billing records are squarely within the designated record set, yet the export documentation makes no mention of billing data whatsoever. The C-CDA USCDI v3 format does not comprehensively capture billing information (charges, claims, payments, adjustments, EOBs).

**The C-CDA limitation.** By describing the clinical data export as "C-CDA USCDI v3," the documentation implicitly limits the structured clinical export to what C-CDA can represent. This is essentially the (g)(10) data subset. While the inclusion of documents and internal correspondence goes beyond pure (g)(10), the structured clinical data appears to be only the USCDI slice — not a comprehensive dump of everything in the database.

### Export Format & Standards

- **Primary clinical format**: C-CDA (Consolidated Clinical Document Architecture) conforming to USCDI v3. This is a well-established standard, but it represents the patient summary/transitions-of-care data subset, not a comprehensive database export.
- **Document formats**: Raw files in their original formats (PDF, JPEG, GIF, TIF, DOC/DOCX). This is appropriate for document-type data.
- **Patient-facing pathway**: FHIR R4 DocumentReference resource — documents can be retrieved via FHIR API with appropriate MIME types.
- **No proprietary database dump**: There is no indication of a CSV, SQL, or proprietary format export that would capture all data tables. The export appears to be a curated document package, not a comprehensive data extraction.

A third party receiving this export would get a C-CDA document (providing a structured clinical summary) plus attached files. This is more of a "patient record transfer" package than a comprehensive EHI export. The absence of a data dictionary or schema means the recipient must rely entirely on C-CDA and FHIR standards documentation to interpret the structured data.

### Documentation Quality

**Very poor.** The entire EHI export documentation is a single HTML page with approximately 150 words of prose content. Specific deficiencies:

- **No data dictionary**: Zero field-level documentation. No table definitions, no column listings, no data type specifications.
- **No schema files**: No XSD, JSON Schema, or any machine-readable format definition.
- **No API documentation**: The FHIR section mentions DocumentReference but provides no endpoint URLs, authentication requirements, query parameters, or response examples.
- **No sample data**: No example C-CDA documents, no example export packages, no sample files.
- **No user guide**: The 5-icon workflow provides only the highest-level overview. There are no step-by-step instructions, no screenshots of the actual admin console, no explanation of options or settings.
- **No versioning or change history**: The page appears to have been created in late 2023 and not updated since.
- **Vague language**: "meme document types" (typo for MIME), "one-time bulk export" (is it truly one-time? can it be repeated?), "secure Download location" (what does this mean technically?).

A developer attempting to import data from this export would need to rely entirely on knowledge of C-CDA and FHIR standards. The documentation tells you almost nothing about what specific data CloudCraft puts into the C-CDA or how their export is structured beyond the broadest categories.

### Structure & Completeness

- **Granularity**: Category-level only. Five bullet points listing data types. No table-level, entity-level, or field-level detail whatsoever.
- **Coded fields**: Not documented. No value sets, no code systems, no terminology bindings.
- **Relationships**: Not documented.
- **Cardinality**: Not documented.
- **Versioning**: None apparent.

This is among the most minimal EHI export documentation possible — essentially a statement that "we export C-CDA documents plus some files." It meets the bare minimum of having a publicly accessible page at the registered URL, but provides almost no actionable technical detail about the export content, structure, or process.

## Access Summary
- Final URL (after redirects): https://cloudcraftsoftware.com/certification/B10.html
- Status: found
- Required browser: no (static HTML, though browser needed to view workflow images)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The FHIR endpoint at `fhirapitest.naiacorp.net` timed out and appears inaccessible from the public internet.
- All other URLs on the certification site (`certificationcriteria.html`, `feature.html`, etc.) serve the same generic landing page with no criteria-specific content — these are essentially placeholder pages.
- The mandatory disclosures URL (`cloudcraftsoftware.com/certificationdisclosurestatements`) also serves the generic landing page.
- No downloadable PDF, ZIP, CSV, or other artifact files were found anywhere on the site.
- The "Download as PDF" button on B10.html generates a client-side PDF via JavaScript (html2pdf.js), not a server-hosted file.
