# Sequel Systems, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.sequelmed.com/data-export/
- CHPL ID: 11143
- Product: SequelMed EHR V12
- Certification date: 2022-12-27

## Navigation Journal

1. Probed the registered URL with curl:
   ```bash
   curl -sI -L "https://www.sequelmed.com/data-export/" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html, served by Microsoft-IIS/8.5.

2. Fetched the HTML page. It is a minimal static page with a single heading "Data Export" and one bullet-pointed link:
   - "Electronic Health Information Export Documentation" → `https://sequelmed.com/images/SequelMed EHR B10-Electronic Health Information Export.pdf`

3. Downloaded the PDF:
   ```bash
   curl -sL "https://sequelmed.com/images/SequelMed%20EHR%20B10-Electronic%20Health%20Information%20Export.pdf" -o SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf
   ```
   Confirmed: PDF document, version 1.7, 4 pages, 96,891 bytes. Created 2023-11-22 with Microsoft Word for Microsoft 365.

4. Took a screenshot of the data-export page in browser (saved as `data-export-page-screenshot.png`).

5. Checked the vendor's mandatory disclosure statement page (`/ehr/2015edition/disclosurestatement.aspx`) for any additional EHI export references — none found.

6. Checked the site's sitemap page (`/sitemap.html`) for any other EHI-related pages — none found.

No additional documentation links, data dictionaries, schema files, sample exports, or downloadable artifacts exist on this site beyond the single PDF.

## What Was Found

The entire EHI export documentation is a single 4-page PDF titled "170.315(b)(10) Electronic Health Information Export — Electronic data Export Documentation, Version 1.0." The document describes:

**Export modes:**
- Single patient export — users can export EHI for one patient at any time without developer assistance.
- Multi-patient export — users can export EHI for multiple patients at any time without developer assistance.

**Export structure:**
Data is exported as a single compressed ZIP file per patient containing:

1. **Clinical folder** — Contains one XML-based C-CDA file for the patient. The documentation states this is "standard based which comply to US Core Data for Interoperability (USCD), Version 1 requirements." Three HL7 specification references are provided for the C-CDA format (CDA R2 IHE Health Story Consolidation DSTU 1.1, Consolidated CDA Templates R2.1, and C-CDA R2.1 Companion Guide R2).

2. **Documents folder** — Contains patient documents exported in their original upload/scan format. The document lists six types:
   - Signed progress notes
   - Available lab results
   - Radiology reports
   - Scanned documents
   - Imported documents
   - "Iploaded" [sic — typo for "Uploaded"] documents

   Supported file formats: .jpg, .gif, .bmp, .png, .pdf, .txt

3. **Patient Documents Detail.xls** — An Excel file described only by its name; no further explanation of its contents is provided.

That is the entirety of the documentation. There is no data dictionary, no field-level documentation, no schema files, no sample exports, no screenshots of the export interface, and no explanation of what data is included in or excluded from the C-CDA.

## Export Coverage Assessment

### Data Domain Coverage

This is where the documentation has its most significant shortcoming. The product research identifies SequelMed as an integrated EHR + Practice Management platform storing clinical, financial, scheduling, and administrative data across 24+ specialties. The export documentation describes exporting only two things:

**Clearly covered (via C-CDA):**
- Demographics (standard C-CDA section)
- Problem lists, conditions
- Medications, allergies
- Immunizations
- Vital signs
- Lab results (to the extent they are in the C-CDA)
- Clinical notes (to the extent captured in the C-CDA)

**Partially covered (via Documents folder):**
- Signed progress notes (as document files)
- Lab results (as document files)
- Radiology reports (as document files)
- Scanned/imported/uploaded documents

**Not mentioned or clearly missing:**
- **Billing data** — charges, claims, payments, patient A/R, collections, denials, eligibility — the entire Practice Management financial dataset is absent from the export description
- **Scheduling data** — appointments, visit history
- **Orders** — lab orders, pharmacy orders, imaging orders (only results are mentioned, not the orders themselves)
- **E-prescribing history** — prescription records beyond what's in the C-CDA medication list
- **Clinical decision support alerts** — alert history
- **Patient portal data** — messages, patient-submitted information
- **Specialty-specific clinical data** — the product claims to serve 24+ specialties with customizable templates; none of that specialty-specific data structure is described
- **Custom clinical templates** — data captured via specialty templates that may not map to standard C-CDA sections
- **Referral data**
- **Quality management / outcomes data** (to the extent it's patient-specific)
- **Insurance/enrollment information** beyond what's in the C-CDA demographics

The export is essentially a C-CDA clinical summary plus any attached document files. This is a textbook example of the (b)(10) vs (g)(10) confusion: the clinical data portion of the export is a C-CDA — a transitions-of-care document format that covers the USCDI/US Core clinical summary — not a comprehensive export of everything in the system. The C-CDA format inherently cannot represent billing records, scheduling data, custom specialty templates, or the full breadth of data a combined EHR+PM system stores.

The "Patient Documents Detail.xls" file is intriguing but completely undocumented — it could potentially contain a manifest or metadata about the documents, but its structure and content are not described.

### Export Format & Standards

- **Format:** ZIP archive per patient containing a C-CDA XML file, document files in original format, and an Excel spreadsheet.
- **Standard:** C-CDA (HL7 CDA R2, Consolidated CDA Templates R2.1) for clinical data. USCDI V1 compliance claimed.
- **Concern:** C-CDA is a clinical summary standard designed for transitions of care. It is appropriate for the clinical data it covers (problems, meds, allergies, labs, vitals, immunizations) but structurally cannot represent billing records, scheduling data, or arbitrary custom clinical forms. Using C-CDA as the sole structured export format for a (b)(10) export means the export is inherently limited to what C-CDA can express.
- **Document files** are exported in their original upload format, which is reasonable for unstructured content but means no structured metadata about those documents is provided (beyond whatever is in the unexplained XLS file).
- A third party receiving this export would get a standard clinical summary plus a folder of document files, but would have no way to reconstruct billing history, scheduling records, or specialty-specific clinical data.

### Documentation Quality

The documentation is extremely minimal:
- **4 pages total**, including a cover page. Approximately 1.5 pages of actual content.
- **No data dictionary** — no field-level documentation whatsoever.
- **No schema** — the C-CDA format is referenced by external HL7 specs, but there are no SequelMed-specific profiles, constraints, or mappings documented.
- **No sample data** — no example exports or worked examples.
- **No screenshots** — no illustration of the export interface or workflow.
- **No explanation of the XLS file** — the "Patient Documents Detail.xls" is listed but not described.
- **No explanation of scope** — the document never states what data is or isn't included, or why.
- **Typo present** — "Iploaded" instead of "Uploaded" on page 4, suggesting minimal review.
- A developer could not implement an import of this data based solely on this documentation. They would need to rely entirely on the external C-CDA specifications to parse the clinical data, and would have no guidance on the document files or the XLS.

### Structure & Completeness

- **Granularity:** The documentation operates at the folder/file level only (Clinical folder, Documents folder, XLS file). There is zero field-level documentation.
- **Coded fields:** Not addressed. The C-CDA will contain coded data (ICD-10, SNOMED, RxNorm, etc.) but the documentation doesn't describe which code systems are used or how.
- **Relationships:** Not documented. The relationship between the C-CDA data, the document files, and the XLS manifest is not explained.
- **Versioning:** "Version 1.0" — no change history, no dates within the document (though the PDF metadata shows creation date of 2023-11-22).
- **Value sets:** Not documented.

### Overall Assessment

SequelMed's EHI export documentation is among the most minimal possible while still technically existing. The export itself appears to be a C-CDA clinical summary packaged with attached document files — essentially the same as a transitions-of-care export, not a true (b)(10) comprehensive export. The documentation provides no data dictionary, no field definitions, no sample data, and no explanation of scope or completeness.

The fundamental gap is that SequelMed is a combined EHR + Practice Management platform with billing, scheduling, and 24+ specialty-specific clinical templates, but the export only describes a C-CDA (which covers a clinical summary subset) plus document attachments. Everything outside the C-CDA's scope — billing, scheduling, custom clinical forms, orders, e-prescribing history — appears to be excluded from the export entirely, or at least is not documented.

This is a clear case of conflating (b)(10) with transitions-of-care export functionality: the C-CDA satisfies clinical summary exchange requirements, but it does not constitute an export of "all electronic health information" as required by 170.315(b)(10).

## Access Summary
- Final URL (after redirects): https://www.sequelmed.com/data-export/
- Status: found
- Required browser: no (static HTML, direct PDF link)
- Navigation complexity: direct_link (single page with one PDF link)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly and the PDF downloaded without issues.
- The disclosure statement page was checked but contained no additional EHI export information.
- The sitemap was checked but contained no additional EHI-related pages.
