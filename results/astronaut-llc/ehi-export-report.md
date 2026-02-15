# Astronaut, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://astronautehr.com/index.php/disclosures/export-format-documentation/
- CHPL IDs: 10809
- Product: Astronaut (version 1709, certified 2022-02-01)

## Navigation Journal

1. Probed the registered URL with curl — returned HTTP 200, Content-Type: text/html, served via Cloudflare.

```bash
curl -sI -L "https://astronautehr.com/index.php/disclosures/export-format-documentation/" -H 'User-Agent: Mozilla/5.0'
```

2. Fetched the page HTML (47,355 bytes). It's a simple WordPress page titled "Export Format Documentation" with a single embedded PDF viewer and download link.

3. Found one downloadable file:
```
href="https://astronautehr.com/wp-content/uploads/2025/08/Astronaut-EHR-Export-Format-Documentation.pdf"
```
The PDF is embedded via a `<object>` tag with a PDF preview and a "Download" button.

4. Downloaded the PDF:
```bash
curl -sL "https://astronautehr.com/wp-content/uploads/2025/08/Astronaut-EHR-Export-Format-Documentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o Astronaut-EHR-Export-Format-Documentation.pdf
```
Verified: `file` reports "PDF document, version 1.4, 10 page(s)" (pdfinfo says 10 pages), 222,805 bytes. Produced with Google Docs Renderer.

5. Took a full-page screenshot of the documentation page in a browser.

6. Checked the parent disclosures page (https://astronautehr.com/index.php/disclosures/) for additional EHI-specific content — it links to the export format documentation page, an APIs page, FHIR base URLs, and real-world testing docs, but no additional EHI export documentation beyond the PDF already downloaded.

No other files, data dictionaries, schemas, or sample exports were found.

## What Was Found

The entire EHI export documentation consists of a single 10-page PDF titled "Astronaut EHR Export Format Documentation" (Copyright 2023).

### Export Format

The export uses a **dual format**:

1. **C-CDA (XML)** for the majority of clinical data — the document describes this as the primary export format.
2. **Proprietary CSV** for "advanced demographics and remaining EHI" — data that doesn't fit into the C-CDA structure.

### How Data Is Accessed

The documentation states that data is stored on a **FHIR server** where patient information is continuously uploaded and updated. To export:
- An authorized user must be granted permission by Astronaut EHR IT staff.
- IT staff walk the user through the extraction process.
- Users can perform **Single Patient Export** or **Bulk Patient Export** through the FHIR server's capabilities.

This is notable: the export requires IT staff involvement rather than being a self-service function.

### C-CDA Sections Documented

The PDF lists 16 C-CDA sections with brief summaries of each (largely paraphrased from HL7's C-CDA documentation):

1. Allergies
2. Immunizations
3. Medications
4. Plan of Treatment
5. Goals
6. Problems (diagnoses)
7. Results (Lab) — including hematology, chemistry, serology, virology, toxicology, microbiology, imaging, pathology
8. Vitals
9. Procedures
10. Social History
11. Encounters
12. Functional Status
13. Medical Equipment
14. Assessments
15. Header section (demographics, author info, timestamps)
16. "Advanced Demographics and Remaining EHI" (CSV supplement)

### CSV Supplement

For data not fitting C-CDA, the vendor provides a proprietary CSV format. The documentation describes this as name-value pairs:

> `Place of Birth, USA, Mother's Maiden Name, Annabelle, Spouse's Employer Name, Astronaut LLC, Date of Retirement, 10/31/2023…(etc)`

Categories with no data are excluded. The documentation claims this covers "all available data."

### Documentation Depth

The PDF provides:
- A brief XML structural overview of C-CDA (header, body sections, entry elements) with code snippets
- A one-paragraph summary of each C-CDA section
- A single fictional example of the CSV format
- A reference to HL7's C-CDA documentation for syntax specifics

It does **not** provide:
- A data dictionary or field-level definitions
- Schema files (XSD, JSON Schema, etc.)
- Sample export files
- Value set definitions
- Mapping between Astronaut EHR's internal data model and C-CDA/CSV output
- Specifics on which VistA FileMan files/fields are exported

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered (via C-CDA):**
- Demographics (header)
- Problem/diagnosis lists
- Medications
- Allergies
- Lab results (broad scope — pathology, imaging, microbiology, etc.)
- Vital signs
- Immunizations
- Procedures
- Clinical notes/assessments
- Encounters
- Goals and plan of treatment
- Functional status
- Medical equipment / implantable devices
- Social history

**Claimed covered via CSV supplement:**
- "Advanced demographics" — the example shows place of birth, mother's maiden name, spouse's employer, date of retirement
- "Remaining EHI" — described as everything not in the C-CDA

**Apparently missing or not mentioned:**
- **Billing data** — no mention of charges, claims, payments, billing codes, or financial records. The product research indicates Astronaut has some billing capabilities ("Rocket Note" for billing, "billers" on staff), but the export documentation is silent on billing data.
- **Scheduling data** — appointments, visit scheduling information are not mentioned beyond encounter records.
- **E-prescribing details** — Newcrop/Surescripts prescription transmission records are not specifically addressed. Medications are covered via C-CDA, but the integration-specific data (EPCS records, prescription transmission status) is not discussed.
- **Clinical orders (CPOE)** — the C-CDA "Plan of Treatment" covers pending orders, but historical completed orders beyond what's captured in results/procedures/medications are not specifically addressed.
- **Consult requests/notes** — while "Encounters" and "Assessments" may partially cover this, dedicated consult tracking isn't mentioned.
- **Clinical Decision Support data** — drug interaction alerts, CDS triggers.
- **Documents and images** — no mention of scanned documents, attached images, or external records incorporated into the chart.

**Ambiguous:**
- The CSV "remaining EHI" supplement is described vaguely enough that it *could* cover many of these gaps, but without a data dictionary or field listing, it's impossible to verify. The only example given is demographic data (place of birth, maiden name, etc.), not clinical or billing data.
- The documentation references "the designated record set defined in 45 CFR 164.502, excluding psychotherapy notes," which suggests awareness of the (b)(10) scope, but doesn't enumerate what's actually included.

### Export Format & Standards

The C-CDA portion uses a recognized healthcare standard (HL7 C-CDA XML), which is appropriate for the clinical data it covers. The vendor refers users to HL7's official C-CDA documentation for syntax details rather than providing their own field-level specification.

The CSV supplement uses a non-standard, proprietary name-value pair format. The lack of a formal schema or field listing makes it difficult to assess what data is actually included. A name-value pair format without a header row or defined structure would be challenging for a third party to reliably parse and import.

The export format is **not FHIR** despite data being stored on a FHIR server — they export as C-CDA + CSV, not FHIR resources. This is a reasonable approach for (b)(10), since C-CDA covers the clinical core and the CSV supplement can (in theory) capture everything else.

### Documentation Quality

The documentation is minimal and high-level:

- **No data dictionary** — there is no field-level specification for either the C-CDA content or the CSV supplement.
- **No schema files** — no XSD, JSON Schema, or other machine-readable artifact.
- **No sample exports** — no example C-CDA document or example CSV file beyond the single fictional demographic snippet.
- **No value set documentation** — coded fields are not enumerated.
- **Reliance on external standards** — the document essentially says "our C-CDA follows HL7's C-CDA spec" and points users to HL7's website for details.
- **Minimal CSV documentation** — a single example line of demographic name-value pairs is the entire specification for the proprietary format.

A developer attempting to build an import for this data would not have enough information from this documentation alone. They would need to work from the HL7 C-CDA specification for the XML portion and reverse-engineer the CSV format from actual export files.

The documentation reads as a compliance checkbox — it establishes that the export exists and uses C-CDA, but doesn't provide the technical detail needed to actually work with the exported data.

### Structure & Completeness

- **Granularity:** Section-level descriptions only. No field names, data types, cardinality, or constraints.
- **Value sets:** Not documented.
- **Relationships:** Not documented (the C-CDA standard implicitly defines these, but vendor-specific mappings are absent).
- **Versioning:** The PDF is dated 2023, hosted in a 2025/08 upload path, suggesting it was re-uploaded or updated in August 2025. No version history or changelog.

### (b)(10) vs (g)(10) Assessment

This vendor shows awareness of the distinction. The documentation explicitly references C-CDA (not FHIR resources) as the export format, mentions "remaining EHI" in a separate CSV supplement, and cites the designated record set definition from 45 CFR 164.502. The approach of C-CDA + proprietary CSV for everything else is conceptually sound for (b)(10) compliance.

However, the **lack of specificity about what "remaining EHI" includes** is the key weakness. The only example of CSV data is demographic fields (place of birth, maiden name). Whether billing records, scheduling data, e-prescribing logs, and other non-clinical EHI are actually exported is unknown from this documentation. The documentation promises completeness ("all available data will be present upon exportation") but doesn't enumerate what that means.

## Access Summary
- Final URL (after redirects): https://astronautehr.com/index.php/disclosures/export-format-documentation/
- Status: found
- Required browser: no (curl works fine; PDF direct-linked)
- Navigation complexity: direct_link (single PDF download on the registered page)
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends

None. The page loaded cleanly, the PDF downloaded without issues, and no special headers or authentication were required. The simplicity of the page (one embedded PDF) meant there was nothing to navigate or expand.
