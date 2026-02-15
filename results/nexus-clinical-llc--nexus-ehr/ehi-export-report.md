# Nexus Clinical LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.nexusclinical.com/costs-and-limitations/
- CHPL IDs: 11130
- Product: Nexus EHR V 7.3
- Certification date: 2022-12-27

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```bash
   curl -sI -L "https://www.nexusclinical.com/costs-and-limitations/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `text/html; charset=UTF-8`, WordPress site on Apache. No redirects.

2. **Page fetch and examination:**
   ```bash
   curl -sL "https://www.nexusclinical.com/costs-and-limitations/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
   ```
   The page is the vendor's "Costs and Considerations" compliance page (WordPress + Elementor). It contains:
   - ONC certification information (version, CHPL number, criteria list)
   - A link to a Costs and Considerations PDF
   - Multi-factor authentication use cases
   - An **"EHI Export Documentation"** section at the bottom with a link to a PDF

3. **Identified downloadable files:**
   ```bash
   grep -oiE 'href="[^"]*\.pdf[^"]*"' /tmp/page.html
   ```
   Found two PDFs:
   - `https://www.nexusclinical.com/wp-content/uploads/2023/11/EHI-Export-Documentation.pdf`
   - `https://www.nexusclinical.com/wp-content/uploads/2024/08/Nexus_EHR_Costs_And_Considerations.pdf`

4. **Downloaded the EHI Export Documentation PDF:**
   ```bash
   curl -sL "https://www.nexusclinical.com/wp-content/uploads/2023/11/EHI-Export-Documentation.pdf" -o EHI-Export-Documentation.pdf
   ```
   Verified: `file` confirms PDF document, version 1.5, 2 pages, 774 KB. Created 2023-11-30, author "Francis Carlo Hofilena", produced in Microsoft Word 2010. No embedded attachments.

5. **Downloaded the Costs and Considerations PDF:**
   ```bash
   curl -sL "https://www.nexusclinical.com/wp-content/uploads/2024/08/Nexus_EHR_Costs_And_Considerations.pdf" -o Nexus_EHR_Costs_And_Considerations.pdf
   ```
   Verified: PDF document, version 1.7, 2 pages, 178 KB.

6. **Checked for additional documentation:**
   - Searched page for links to data dictionaries, schemas, API docs — none found.
   - Checked `/resources/` page — no EHI-related content.
   - Attempted `/?page_id=6165` (linked twice from the page) — redirects to homepage (draft/private page).
   - Checked for `/interoperability/` and `/fhir/` paths — both return 406 (blocked by ModSecurity).
   - Google search for `site:nexusclinical.com EHI export` — no additional results beyond the costs-and-limitations page.
   - No FHIR API documentation is publicly accessible (the Costs PDF notes FHIR API requires a subscription).

7. **Took full-page screenshot** of the costs-and-limitations page in browser for visual record.

8. **Examined PDF embedded URLs:** Only external standards references (hl7.org C-CDA search, healthit.gov USCDI) — not followed per instructions.

## What Was Found

The entire EHI export documentation is a **single 2-page PDF** (`EHI-Export-Documentation.pdf`). It describes the export format for both individual patient and population-level exports under 170.315(b)(10).

### Export Format

The export is a **ZIP file** containing a mix of formats:

**Individual Patient Export includes:**
1. **Clinical Data** — C-CDA R2.1 format, compliant with USCDI V1
2. **Patient Billing Information** — CSV files for:
   - Claims
   - Insurance payment details
   - Patient payment details
3. **Patient Documents** — exported in original format (PDF, DOC, HTML, JPG, etc.) as individual files:
   - Chart Notes (PDF per encounter)
   - Scanned Documents (PDF)
   - Imported Faxes (PDF from eFax module)
   - Software-generated Documents and Forms (PDF)
   - PE Images (image format)
   - Other imported documents (original format)
4. **Future Appointments** — CSV format
5. **Patient Demographics and Insurance** — CSV format (contact details, address, emergency contact, primary/secondary insurance, responsible party)

**Population Data Export includes:**
Same data categories as individual export with one difference:
- Documents are replaced by a **Patient Documents Index** (CSV) containing document ID, patient identification details, document classification, name, and created date. Nexus provides a separate "document export utility program" to export actual documents offline based on this index file.

### What Is NOT Documented
- No data dictionary — no field names, data types, or value sets for the CSV files
- No C-CDA template constraints or customizations beyond "C-CDA R2.1 compliant with USCDI V1"
- No sample export files or examples
- No schema files (no XSD for C-CDA customizations, no CSV column headers listed)
- No API documentation (the export is a UI-driven process, not API-based)
- No detailed export instructions or screenshots of the export interface
- Admin users access the "export module" — no further detail provided

The Costs and Considerations PDF is a standard ONC-required disclosure document listing pricing for certified functionality. Relevant finding: the FHIR API (g(10)) requires a separate paid subscription ("One time setup fee and annual subscription fees"), meaning EHI export and FHIR API are separate systems.

## Export Coverage Assessment

### Data Domain Coverage

Nexus EHR is a comprehensive ambulatory EHR with clinical documentation, practice management, medical billing, patient portal, telehealth, and e-prescribing. The product research identifies extensive data domains stored in the system.

**Clearly covered by the export:**
- **Core clinical data** (via C-CDA): problems, medications, allergies, immunizations, vital signs, lab results, clinical notes — but only the USCDI V1 subset
- **Billing data** (via CSV): claims, insurance payments, patient payments
- **Patient documents**: chart notes, scanned documents, faxes, software-generated forms, images
- **Demographics and insurance**: contact info, addresses, emergency contacts, insurance details
- **Future appointments**: scheduled appointments

**Missing or unclear from the export documentation:**
- **Medication orders / prescriptions** — C-CDA may include medication lists, but the prescribing data (CPOE orders, EPCS details, NewCrop e-prescribing records, PDMP queries) is not explicitly mentioned as exported
- **Laboratory and imaging orders** — CPOE certified under (a)(2) and (a)(3), but no mention of order-level export; C-CDA only captures results, not the full ordering workflow
- **Problem list / diagnosis codes** — likely in C-CDA, but not explicitly confirmed beyond "USCDI V1"
- **Family health history** — certified under (a)(12), likely in C-CDA but not confirmed
- **Implantable device list** — certified under (a)(14), may be in C-CDA
- **Patient-generated data** — portal-submitted demographics updates, health questionnaires, appointment requests, secure messages, post-visit surveys — none mentioned
- **Inventory management data** — in-house medication/supply tracking, not mentioned
- **Practice management data** — task management, scheduling history, recall lists — not mentioned
- **Quality measure data** — CQM/MIPS tracking data, not mentioned
- **Communication records** — Direct messages, secure portal messages, eFax logs (as metadata rather than document content)
- **Care plan / referral data** — not explicitly mentioned
- **Fee schedules and billing configuration** — only claims/payments are exported, not the underlying billing setup

**Key concern:** The clinical data export relies entirely on C-CDA R2.1 with USCDI V1 compliance. USCDI V1 is a narrow subset of clinical data — it covers demographics, problems, medications, allergies, immunizations, lab results, vital signs, clinical notes, and a few other categories. It does **not** cover specialty-specific clinical data, detailed encounter documentation beyond progress notes, or the full depth of clinical observations that a 25+ specialty EHR might store. For example, a cardiology practice using Nexus EHR may have EKG interpretations, echocardiogram reports, or cardiac risk assessments that don't map to standard C-CDA templates.

The billing CSV export (claims, insurance payments, patient payments) is a positive sign — this goes beyond what a g(10) FHIR API would provide. However, the lack of field-level documentation for these CSV files means we can't assess their completeness.

### Export Format & Standards

The export uses a **hybrid format**: C-CDA R2.1 for clinical data plus CSV files for billing and administrative data, plus raw document files. This is a reasonable approach for b(10) — it doesn't try to force all data into FHIR or C-CDA.

However:
- C-CDA R2.1 with USCDI V1 is inherently limited to a subset of clinical data
- The CSV format is completely undocumented — no column names, data types, or encoding specified
- No documentation of how relationships between entities are expressed (e.g., how a claim CSV row links to a patient or encounter)
- A third party receiving this export would need to reverse-engineer the CSV structure

### Documentation Quality

**Very poor.** The documentation is a 2-page PDF with:
- High-level description of export categories (5 bullet points per export type)
- No data dictionary whatsoever
- No field-level definitions for CSV files
- No C-CDA template documentation or constraints
- No sample files or worked examples
- No export instructions or interface screenshots
- No information about character encoding, date formats, or delimiter handling
- No error handling or edge case documentation

A developer receiving this export would have no way to programmatically parse the CSV files without first examining sample data. The C-CDA portion would be interpretable using standard C-CDA tooling, but any Nexus-specific extensions or conventions are undocumented.

The document was created in November 2023 (about 11 months after certification in December 2022). It reads as a minimal compliance checkbox rather than genuine technical documentation.

### Structure & Completeness

- **Granularity**: Category-level only (e.g., "Claims" as a CSV file). No field names, no column headers, no data types, no cardinality.
- **Value sets**: Not documented for any field.
- **Relationships**: Not documented. No explanation of how a billing CSV relates to clinical records or patient demographics.
- **Versioning**: None. The PDF has no version number or change history.
- **Population export distinction**: The only documented difference is that documents are replaced by a document index CSV, and actual document export requires a separate offline utility.

### Overall Assessment

Nexus Clinical's EHI export documentation represents a **minimal compliance effort**. The export itself appears to be a genuine attempt at b(10) compliance — it goes beyond just g(10) FHIR data by including billing CSVs, raw documents, and demographic/insurance data in a downloadable ZIP. This is better than vendors who simply point to their FHIR Bulk Data endpoint.

However, the documentation is severely inadequate:
1. **No data dictionary** — the single most critical piece of export documentation is entirely absent
2. **No field definitions** for the CSV files that constitute the non-clinical portion of the export
3. **Probable coverage gaps** — patient-generated data (portal activity, questionnaires, secure messages), specialty clinical data beyond USCDI V1, prescription/order details, and practice management data are not mentioned
4. **No sample data** — impossible to validate the export format without access to the system

The FHIR API being a separate paid module confirms that this is genuinely a b(10)-specific export mechanism, not a repackaged g(10) endpoint — which is architecturally correct. But the documentation needs substantial improvement to be useful to anyone receiving or importing this data.

## Access Summary
- Final URL (after redirects): https://www.nexusclinical.com/costs-and-limitations/
- Status: found
- Required browser: no (PDFs directly downloadable via curl)
- Navigation complexity: one_click (PDF linked from "Click Here" on the page)
- Anti-bot issues: Site has right-click/copy protection JavaScript (`jh_disabled_options_data` disabling click, Ctrl+U, F12, Ctrl+Shift+I/J/C, Ctrl+S, image dragging) and ModSecurity on some paths, but PDF downloads work fine with standard User-Agent

## Obstacles & Dead Ends
- `/?page_id=6165` (linked twice on the page) redirects to homepage — appears to be a draft/private page
- `/interoperability/` and `/fhir/` paths return 406 (blocked by ModSecurity)
- No directory listing available for `/wp-content/uploads/`
- Google search found no additional EHI documentation beyond what's on the costs-and-limitations page
- The site's JavaScript copy protection is irrelevant since the documentation is in downloadable PDFs
