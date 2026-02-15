# Meridian Medical Management — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://vertexdr.com
- Final URL: https://vertexdr.com/ (no redirect)
- CHPL IDs: 11002
- Product: VertexDr v9.1
- Certification date: 2022-10-24

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://vertexdr.com"` returned HTTP 200, WordPress site with JSON API. Content-Type: text/html.

2. **Main page examination** — Downloaded full HTML (137KB). Scanned for links containing `ehi`, `export`, `data.dictionary`, `b.10`, `bulk`, `fhir`. Found one directly relevant file:
   ```
   href="https://vertexdr.com/wp-content/uploads/2023/11/VertexDr-Certification-§170.315b10-Electronic-Health-Information-Export-Documentation.pdf"
   ```

3. **Downloaded the PDF** — 11-page PDF (716KB), confirmed with `file` command. Text-based PDF, fully extractable with `pdftotext`.

4. **Searched for FHIR/API documentation** — The PDF's final page mentions "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)." However:
   - No FHIR API documentation, endpoint URLs, or developer docs were found anywhere on the site.
   - Searched all links on homepage, practice-suite page, document-library page.
   - Checked WordPress sitemap (`/page-sitemap.xml`) — only 11 pages total on the site. None are API/FHIR docs.
   - Web search for "vertexdr FHIR API documentation" and "meridian medical management FHIR bulk data server endpoint" returned no results.
   - A Box.com link (`carecloud.box.com/s/gqaxygaynv3qt6ozvr16n999zu1sd8uv`) for "Real World Testing Results 2023" returned HTTP 404.

5. **Checked Mandatory Disclosures** — Two PDFs available. Both are identical single-page documents listing costs for MedFusion patient portal and DataMotion secure messaging. Not relevant to EHI export.

6. **Browser verification** — Navigated to vertexdr.com in Chrome. The page is a single long page with distinct sections. The EHI export documentation appears under a clear "Electronic Health Information Export" heading (h2), with a single link to the PDF. No accordion, no hidden content, no JavaScript-dependent rendering.

## What Was Found

### The EHI Export Documentation PDF (11 pages)

VertexDr's EHI export consists of **two complementary mechanisms**:

**1. CCD/C-CDA Export (Clinical Data)**
- Single patient export: File → Export CCD from patient chart. User selects which C-CDA sections to include.
- Bulk patient export: File → Export CCD(s) for Patients. Generates a ZIP file with CCDA documents in XML format.
- The C-CDA conforms to HL7 CDA R2 Consolidated CDA Templates for Clinical Notes (US Realm), DSTU R2.1, August 2015 — i.e., the standard referenced by § 170.205(a)(4).

**The PDF documents these C-CDA sections in detail** (pages 6–10), listing each data element with its XPATH/entry path, code system OID, and code system name. Sections documented:
- Patient Demographics/Information (name, sex, DOB, race, ethnicity, language)
- Provider info (name, contact, address)
- Date and Location of visit
- Chief Complaint and Reason for visit
- Encounters (code, diagnosis, location, date)
- Immunizations (vaccine, date, status, route, site, manufacturer, dose, lot, notes)
- Instructions (patient instructions/follow-up reasons)
- Treatment Plan (planned observations, planned dates)
- Social History
- Problems (SNOMED + ICD-10 translation)
- Medications (RxNorm + NDC translation)
- Medication Allergies (substance, reaction, severity, status)
- Laboratory Tests and Results (LOINC-coded)
- Vitals (LOINC-coded)
- Goals
- Procedures (CPT-4, SNOMED, or HCPCS)
- Care team members
- Reason for Referral
- Medical Equipment / Implanted Devices
- Mental Status assessments
- Functional Status assessments
- Health Concerns

**2. PDF Exports (Non-Clinical Data)**
For data that doesn't fit into the C-CDA standard, VertexDr exports in PDF format:
- **Patient Demographic/Insurance** — "comprehensive view of demographics and insurance details"
- **Advance Directives**
- **Appointments**
- **Provider-to-Patient Messages**
- **Billing Data (Claims)** — CPT, ICD, Modifier data
- **Documents** — signed progress notes, lab results, radiology reports, scanned/uploaded documents

These non-CCD exports are accessible via the application's 'Reports' section. Files are saved to a user-specified folder and can be organized by document type and sub-type.

**3. FHIR Data Export (mentioned but undocumented)**
Page 11 states: "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)."

No further FHIR documentation exists — no endpoint URLs, no resource types, no authentication details, no sample payloads.

## Export Coverage Assessment

### Data Domain Coverage

**Covered by C-CDA export:**
- Demographics (name, sex, DOB, race, ethnicity, language) ✓
- Problems/diagnoses (SNOMED + ICD-10) ✓
- Medications (RxNorm + NDC) ✓
- Medication allergies (substance, reaction, severity) ✓
- Lab results (LOINC-coded) ✓
- Vital signs (LOINC-coded) ✓
- Immunizations (CVX + CPT-4) ✓
- Procedures (CPT-4, SNOMED, HCPCS) ✓
- Encounters ✓
- Goals ✓
- Social history ✓
- Care team members ✓
- Mental/functional status assessments ✓
- Health concerns ✓
- Treatment plans ✓
- Medical equipment / implanted devices ✓
- Referrals (reason for referral) ✓

**Covered by PDF export:**
- Insurance information ✓
- Billing/claims data (CPT, ICD, Modifier) ✓
- Advance directives ✓
- Appointments ✓
- Provider-to-patient messages ✓
- Documents (progress notes, lab results, radiology reports, scanned documents) ✓

**Potentially missing or ambiguous:**
- **Prescription history / e-prescribing data**: The C-CDA covers medications, but detailed e-prescribing transaction history (EPCS data, pharmacy transmissions) is unclear. May be subsumed under the medication section or document exports.
- **Clinical notes beyond progress notes**: The documents export covers "signed progress notes" — what about H&P notes, consult notes, discharge summaries, other note types? These may be captured as "any other scanned or uploaded document" but this is ambiguous.
- **Family health history**: VertexDr is certified for (a)(12) family health history, but the C-CDA section list doesn't explicitly include a Family Health History section. It may be embedded in Social History.
- **Patient-generated health data**: The product is certified for (e)(3) patient health information capture, but this doesn't appear explicitly in the export documentation.
- **Analytics/reporting data (PrecisionBI)**: Not included, but this is likely operational/aggregate data (not EHI).

**Appropriately excluded** (not EHI):
- Audit logs, system configuration, quality metrics aggregates — correctly absent.

### Export Format & Standards

The export uses a **dual-format approach**:

1. **C-CDA XML** for structured clinical data — a well-recognized standard. The CDA R2 Consolidated CDA DSTU R2.1 is the exact standard required by ONC certification.
2. **PDF** for billing, demographics, insurance, appointments, messages, and documents.

This is a reasonable approach but has significant limitations:

- **The PDF exports are not machine-readable.** Billing data (claims with CPT, ICD, modifier codes) in PDF format cannot be programmatically consumed. A CSV, NDJSON, or database dump of billing records would be far more useful for data portability. PDF is effectively a dead end for computable reuse.
- **The C-CDA portion is limited to standard US Core / USCDI clinical data.** The sections documented map cleanly to what a standard C-CDA covers, which overlaps heavily with what (g)(10) FHIR APIs expose. There's no indication of VertexDr exporting data beyond standard C-CDA sections.
- **The FHIR export is a black box.** A single sentence mentions it, with zero technical detail. It's unclear whether the FHIR Bulk Data endpoint adds coverage beyond the C-CDA (unlikely, given the mention of "Document Reference" suggests it may just wrap C-CDA documents as FHIR DocumentReference resources).

A third party could reconstruct a clinical summary from the C-CDA export. They could read the PDF exports visually. They could **not** programmatically import billing data, appointment history, or insurance information.

### Documentation Quality

- **Moderate for C-CDA clinical data.** The data element mapping table (pages 6–10) is useful — it lists each field, its XPATH, code system OID, and code system name. A developer could validate a C-CDA against this mapping.
- **Minimal for non-CCD data.** The PDF export categories are described in a single sentence each, with no field definitions, no sample outputs, and no schema. "A comprehensive view of billing data (CPT, ICD, Modifier)" is the only description of billing export content.
- **No FHIR documentation at all.** A single sentence claiming FHIR Bulk Data support without any endpoint, authentication, resource type, or format details.
- **Screenshots included** show the export interfaces — useful for understanding how to trigger exports, but not for understanding output format or content.
- **No sample data or worked examples** are provided.
- **No data dictionary** beyond the C-CDA element mapping.

### Structure & Completeness

- **C-CDA field documentation**: Granular — includes element names, XPATHs, code system OIDs, and code system names. Missing: cardinality, data types, optionality, value set specifics (beyond naming the code system).
- **Non-CCD categories**: Only category-level descriptions, no field-level detail whatsoever.
- **No relationship documentation**: How entities relate to each other is not described.
- **No versioning or change history**: The document is undated (file timestamp: November 16, 2023).
- **Single document**: Everything is in one 11-page PDF. No supplementary schema files, no sample exports, no API specs.

### Overall Assessment

VertexDr's (b)(10) documentation represents a **genuine but minimal effort** at EHI export. The vendor correctly identified that clinical data alone (via C-CDA) is insufficient for full EHI export and added PDF exports for billing, demographics, insurance, appointments, and messages. This shows awareness of the broader (b)(10) scope beyond (g)(10)'s clinical data subset.

However, the execution has significant weaknesses:
1. **PDF format for structured data** (billing, demographics, insurance) defeats the purpose of data portability. These are inherently tabular/structured data domains being exported in a non-computable format.
2. **The FHIR export is documented in a single sentence** with no technical detail — it's essentially an unverifiable claim.
3. **The non-CCD documentation is boilerplate** — identical sentence structures repeated for each category with no field-level specificity.
4. **No sample data, no schema files, no machine-readable artifacts** beyond the C-CDA XML itself.

The C-CDA portion is the strongest part and would enable a developer to understand the clinical data export. Everything else would require experimentation or vendor contact to actually implement an import.

## Access Summary
- Final URL (after redirects): https://vertexdr.com/
- Status: found
- Required browser: no (direct PDF download via curl)
- Navigation complexity: one_click (scroll to "Electronic Health Information Export" section, click PDF link)
- Anti-bot issues: none

## Obstacles & Dead Ends
- Box.com link for "Real World Testing Results 2023" returned HTTP 404 (not relevant to EHI export, but noted).
- No FHIR API documentation exists anywhere on the site despite the PDF claiming FHIR Bulk Data support.
- Web searches for VertexDr FHIR documentation returned no results.
- The WordPress site has only 11 pages total — a very minimal web presence. No developer portal, no API docs, no knowledge base.
