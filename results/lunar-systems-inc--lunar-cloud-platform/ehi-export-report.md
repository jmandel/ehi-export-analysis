# Lunar Systems, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://golunar.com/ehi-export
- Final URL (after redirect): https://www.golunar.com/ehi-export
- CHPL IDs: 11698
- Product: Lunar Cloud Platform v2.6
- Certification date: 2025-09-17

## Navigation Journal

1. **Initial probe** — HTTP HEAD request:
   ```bash
   curl -sI -L "https://golunar.com/ehi-export" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: 301 redirect from `golunar.com` → `www.golunar.com/ehi-export`, then HTTP 200. Content-Type: `text/html; charset=utf-8`. Served via Cloudflare with Webflow backend (surrogate keys indicate Webflow CMS).

2. **Page examination** — Downloaded the HTML page (6,699 bytes). The page is a minimal Webflow page with a single `<iframe>` element embedding a PDF from the Webflow CDN:
   ```html
   <iframe src="https://cdn.prod.website-files.com/61e750daa55a671737f07639/698254d7eef1bab54364c4ef_fea8fdb838b7c4e6075f27875ff811fb_EHI%20Export%2C%20Jan%202026.pdf"
       width="100%" height="1000px" style="border: none;">
   </iframe>
   ```
   No other links, navigation elements, or download buttons on the page — just the embedded PDF viewer.

3. **PDF download**:
   ```bash
   curl -sL 'https://cdn.prod.website-files.com/61e750daa55a671737f07639/698254d7eef1bab54364c4ef_fea8fdb838b7c4e6075f27875ff811fb_EHI%20Export%2C%20Jan%202026.pdf' \
     -H 'User-Agent: Mozilla/5.0' \
     -o EHI_Export_Jan_2026.pdf
   ```
   Verified: `file` reports "PDF document, version 1.4", 54 pages, 1,145,714 bytes. Produced by Google Docs Renderer.

4. **PDF content inspection** — Extracted full text via `pdftotext`. 54-page document titled "Lunar Cloud Platform 2.6 — Electronic Health Information Export", dated January 2026, © 2026 Lunar Systems, Inc. Contains: overview, C-CDA format guide, 18 detailed section specifications with XML examples and element tables, and supplemental data dictionary for CSV files.

5. **URL extraction from PDF** — Only one URL found: `https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447` (external HL7 C-CDA standard reference — not a vendor artifact). No embedded files/attachments.

6. **Checked /certified page** — `https://www.golunar.com/certified` embeds a separate "Mandatory Disclosures" PDF. Not directly relevant to EHI export documentation (different ONC requirement), so not downloaded.

## What Was Found

Lunar provides a single, comprehensive 54-page PDF documenting their EHI export mechanism. The documentation is well-structured and directly addresses the (b)(10) requirement.

### Export Format

The export is delivered as a **ZIP file** containing:
1. **C-CDA XML files** — one per patient, using CDA Release 4.1 (Consolidated Clinical Document Architecture). These contain the majority of clinical data.
2. **Supplemental CSV files** — for data that doesn't fit into C-CDA format, organized into three categories: documents, orders, and charges. The CSV files contain "well formatted JSON columns" for complex nested data.

The platform supports both single-patient and bulk-patient export.

### C-CDA Sections Documented (18 total)

Each section includes: a description, metadata (template ID, LOINC code), a complete XML example with sample data, a human-readable text example, coded entry examples, and a key elements table mapping XML elements to descriptions.

| # | Section | Template ID | LOINC |
|---|---------|-------------|-------|
| 1 | Patient Summary | (recordTarget) | — |
| 2 | Allergies and Intolerances | 2.16.840.1.113883.10.20.22.2.6.1 | 48765-2 |
| 3 | Problem List | 2.16.840.1.113883.10.20.22.2.5.1 | 11450-4 |
| 4 | History of Medication Use | 2.16.840.1.113883.10.20.22.2.1.1 | 10160-0 |
| 5 | Laboratory/Diagnostic Results | 2.16.840.1.113883.10.20.22.2.3.1 | 30954-2 |
| 6 | Procedures | 2.16.840.1.113883.10.20.22.2.7.1 | 47519-4 |
| 7 | Social History | 2.16.840.1.113883.10.20.22.2.17 | 29762-2 |
| 8 | Functional Status | 2.16.840.1.113883.10.20.22.2.14 | 47420-5 |
| 9 | Mental/Cognitive Status | 2.16.840.1.113883.10.20.22.2.56 | 10190-7 |
| 10 | Vital Signs | 2.16.840.1.113883.10.20.22.2.4.1 | 8716-3 |
| 11 | History of Encounters | 2.16.840.1.113883.10.20.22.2.22.1 | 46240-8 |
| 12 | History of Immunizations | 2.16.840.1.113883.10.20.22.2.2.1 | 11369-6 |
| 13 | Care Team | 2.16.840.1.113883.10.20.22.2.500 | 85847-2 |
| 14 | Assessments | 2.16.840.1.113883.10.20.22.2.8 | 51848-0 |
| 15 | Treatment Plan | 2.16.840.1.113883.10.20.22.2.10 | 18776-5 |
| 16 | Clinical Notes | 2.16.840.1.113883.10.20.22.2.65 | 11506-3 |
| 17 | Payers (Insurance) | 2.16.840.1.113883.10.20.22.2.18 | 48768-6 |
| 18 | Participant (Relationships) | 2.16.840.1.113883.10.20.22.5.8 | — |

### Supplemental CSV Data Dictionary

The supplemental data covers three categories beyond what C-CDA captures:

- **Documents** (12 fields): class, type, awaiting_signature, timestamp, added_at, source, desc, loinc_id, text_data, json_data, application_data, visit
- **Orders** (14 fields): name, label, serial_number, data, status, urgency, reason, start_time, end_time, details, fully_signed_at, ixp_start_time, ixp_end_time, visit
- **Charges** (16 fields): rate, revenue_code, procedure_code, modifier, pos_code, dept, quantity, total, recorded_at, service_date, is_emg, is_epsdt, is_verified, ndc, deleted_at, diagnosis_ids

### Notable Design Choices

- The export explicitly mentions being configurable based on platform suites: "Lunar Clinical Suite, Lunar Revenue Suite, Lunar Lab Suite, Lunar IT Suite, Lunar Operations Suite, Lunar Analytics Suite, and Lunar Patient Suite."
- C-CDA is used for structured clinical data; CSV with JSON columns is used for supplemental data.
- The supplemental data includes charges (billing) and orders — these are genuinely beyond standard C-CDA and represent a real attempt at (b)(10) completeness.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered in C-CDA:**
- Demographics, contacts, identifiers (Patient Summary)
- Allergies and adverse reactions
- Problem list / diagnoses
- Medications (history of use)
- Lab/diagnostic results
- Procedures
- Social history (smoking, tribal affiliation, etc.)
- Functional status
- Mental/cognitive status
- Vital signs
- Encounters (visit history with diagnoses)
- Immunizations
- Care team members
- Clinical assessments
- Treatment plans / care plans
- Clinical notes (progress notes, discharge summaries, etc.)
- Insurance/payer information
- Participant relationships (family/legal contacts)

**Covered in supplemental CSV:**
- **Documents** — appears to capture documents, images, scanned materials, and multimedia that don't map to C-CDA. The `json_data` and `application_data` dict fields suggest this is a catch-all for structured data that doesn't fit the C-CDA model. This is a good sign for (b)(10) completeness.
- **Orders** — all clinical orders beyond what's in the procedures/medications sections. Includes investigation times, urgency, and linked visit data.
- **Charges/billing** — revenue codes, procedure codes, modifiers, NDC codes, quantities, rates, totals, diagnosis linkages. This is genuine billing data, not just insurance information. This is a critical (b)(10) domain and Lunar has documented it.

**Potentially missing or unclear:**
- **Medication administration records (MAR)** — The C-CDA section covers "History of Medication Use" but the examples show medication orders rather than detailed administration events (when exactly each dose was given by a nurse). MARs may be captured via the supplemental Orders or Documents CSV, but this isn't explicitly stated.
- **Implantable device data** — Lunar is certified for (a)(14) implantable device list, but there is no dedicated C-CDA section or supplemental CSV for device records. Devices may be included under the Procedures section or the supplemental Documents CSV, but this is not documented.
- **Referrals** — Care plans mention referral-like content, but there's no explicit referral section.
- **Supply chain data** — The product research identifies supply chain staff as users, but no supply chain data appears in the export. This is likely NOT EHI (operational data), so this is not a gap.
- **Images and attachments as binary files** — The overview mentions "images, scanned documents, and multimedia files" are included as supplemental CSV data. However, the CSV schema only has text-based fields (text_data, json_data, application_data). It's unclear whether actual image binaries (DICOM, JPEG, etc.) are exported or only metadata about them.
- **Family health history** — Certified for (a)(12), but no dedicated section in the export. May be under Social History or Participant sections but not clearly documented.

### Export Format & Standards

The choice of **C-CDA XML** as the primary format is well-established and interoperable. C-CDA is a recognized industry standard backed by HL7, and the document references CDA Release 4.1. The template IDs and LOINC codes for each section are standard C-CDA identifiers — this is not a proprietary format masquerading as C-CDA.

The **supplemental CSV** approach for data beyond C-CDA is pragmatic. CSV with JSON columns is not a formal standard, but it's computable and accessible. The three categories (documents, orders, charges) represent a genuine attempt to capture data that C-CDA was never designed to hold — particularly billing charges with revenue codes, modifiers, and NDC codes.

**This is NOT a (g)(10) FHIR API repackaged as (b)(10).** The export uses C-CDA (not FHIR), includes billing/charges data far beyond USCDI, and has a separate supplemental CSV mechanism for non-clinical data. This is clearly a dedicated (b)(10) implementation, not a cosmetic relabeling of a FHIR Bulk Data endpoint.

The format is appropriate for the data. A third party could reconstruct a meaningful patient record from the C-CDA plus supplemental CSVs, though the JSON-in-CSV pattern for the supplemental data would require documentation of the JSON schemas (which are not provided — the `json_data`, `application_data`, and `data` fields are described only as "dict" type without schema details).

### Documentation Quality

**Strengths:**
- Well-organized 54-page PDF with clear table of contents
- Every C-CDA section has: description, metadata, complete XML example, human-readable text example, coded entry example, and key elements table
- Sample data is realistic (patient names, addresses, clinical scenarios)
- Template IDs, LOINC codes, and code systems are correctly specified
- The document explicitly addresses the (b)(10) requirement and references the designated record set (45 CFR 164.502)

**Weaknesses:**
- **No sample export files** — there are XML examples in the PDF, but no downloadable sample C-CDA file or sample CSV files that a developer could test against
- **Supplemental CSV schemas are sparse** — the three CSV tables have field names and data types, but fields like `json_data`, `application_data`, and `data` are typed as "dict" with no documentation of their internal structure. What keys does `json_data` contain for a document? What structure does `data` have for an order? This is a significant gap for implementability.
- **No complete C-CDA example** — while each section has an XML snippet, there is no full sample C-CDA document showing how all sections compose together
- **No export instructions** — the document describes the format but not how to trigger the export. There's no user guide for performing the export (which button to click, which API endpoint to call, what permissions are needed)
- **No schema files** — no XSD, no formal schema definition for the supplemental CSVs
- **Single document** — all documentation is in one PDF with no machine-readable artifacts (no schema files, no sample data files, no OpenAPI specs)

### Structure & Completeness

**Field-level documentation granularity:**
- C-CDA sections: element names + descriptions (moderate granularity). No data types or cardinality specified beyond what's implicit in C-CDA.
- Supplemental CSV: field names + descriptions + data types (good granularity for flat fields, but "dict" and "array" fields lack internal structure documentation).

**Coded fields:** The C-CDA sections reference standard code systems (SNOMED-CT, LOINC, RxNorm, CVX, NCI Thesaurus, NUCC Taxonomy) with example codes. Value sets are not explicitly enumerated but can be inferred from C-CDA standard constraints.

**Relationships between entities:** The C-CDA structure inherently defines relationships through nesting (entries within sections, observations within organizers). The supplemental CSVs link to visits via UUID fields, but there's no documentation of how the CSV `visit` UUIDs correspond to encounters in the C-CDA.

**Versioning:** The document is dated "Jan 2026" and tagged to platform version 2.6. No change history or prior versions are available.

## Access Summary
- Final URL: https://www.golunar.com/ehi-export
- Status: found
- Required browser: no (PDF is directly downloadable from CDN, page just embeds it in an iframe)
- Navigation complexity: direct_link (single page with embedded PDF)
- Anti-bot issues: none (Cloudflare serves the page, but no challenges encountered)

## Obstacles & Dead Ends

None. The documentation was immediately accessible. The URL resolved cleanly, the PDF embedded in the page was directly downloadable from the Webflow CDN, and the content was text-based (not scanned) so `pdftotext` extracted it cleanly.
