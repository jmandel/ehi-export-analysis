# Objective Medical Systems, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://objectivemedicalsystems.com/wp-content/uploads/2025/09/EHI-Export-Data-Format.pdf
- CHPL ID: 11751
- Product: OMS EHR Version 6, certified 2026-01-08

## Navigation Journal

The registered URL is a direct PDF download hosted on WordPress (Cloudflare CDN).

```bash
# Probe headers — confirmed direct PDF download
curl -sI -L "https://objectivemedicalsystems.com/wp-content/uploads/2025/09/EHI-Export-Data-Format.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# → HTTP/2 200, content-type: application/pdf, content-length: 133402

# Download the PDF
curl -sL "https://objectivemedicalsystems.com/wp-content/uploads/2025/09/EHI-Export-Data-Format.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/EHI-Export-Data-Format.pdf

# Verified: file(1) confirms "PDF document, version 1.7, 2 page(s)"
```

The disclosures page at https://objectivemedicalsystems.com/disclosures/ links to an HTML version at https://objectivemedicalsystems.com/ehi-export-data-format/ — but this URL serves the identical PDF file (same 133,402 bytes). No additional EHI export documentation was found on the disclosures page or elsewhere on the site.

The PDF was authored by Anand Aravind using Microsoft Word for Microsoft 365, created 2023-11-16 and never modified since.

No embedded URLs, attachments, or links to additional documents were found in the PDF.

## What Was Found

The entire EHI export documentation is a 2-page PDF:

- **Page 1**: Title page — "§170.315(b)(10) Electronic Health Information Export Data Format" with company logo and address.
- **Page 2**: A single table listing 9 "functionalities" and their export file format:

| Function | Doc Type |
|---|---|
| CCDA | XML, HTML |
| Notes | HTML |
| C3 Notes | HTML |
| Labs | XML, HTML |
| Labs Scanned | PDF |
| Diagnostics | Discrete fields, PDF |
| Scanned documents | PDF |
| Smart Forms | HTML |
| Messages | Discrete fields |

A note states: "Documents sourced from outside will be exported in the same format it was received."

That is the entirety of the documentation. There is no data dictionary, no field-level definitions, no schema, no sample data, no export instructions, no API specification, and no description of how the export is initiated or delivered.

## Export Coverage Assessment

### Data Domain Coverage

OMS EHR is a cardiology-specific EHR with an integrated cardiovascular information system (CVIS) that stores an unusually rich and deep set of specialty clinical data: 16 structured diagnostic reporting modules covering echocardiography, EKG, stress testing, nuclear imaging, catheterization lab, vascular studies, and Holter monitoring, plus chronic care coordination (C3), remote patient monitoring data, AI-assisted diagnosis detection, and revenue cycle data.

The export documentation lists 9 high-level categories. Mapping these against what the product actually stores:

**Likely covered (at least partially):**
- **Clinical notes** → "Notes" (HTML) and "C3 Notes" (HTML) likely cover progress notes and chronic care coordination notes
- **CCDA summary data** → "CCDA" (XML, HTML) likely covers demographics, problems, medications, allergies, immunizations, vitals — the standard clinical summary
- **Lab results** → "Labs" (XML, HTML) and "Labs Scanned" (PDF)
- **Cardiovascular diagnostics** → "Diagnostics" (Discrete fields, PDF) — this is the product's core differentiator, but "discrete fields" is undefined
- **Forms** → "Smart Forms" (HTML) covers custom form data
- **Messages** → "Messages" (Discrete fields) covers internal messaging
- **Scanned/external documents** → "Scanned documents" (PDF) and the note about external documents

**Not mentioned or clearly missing:**
- **Patient demographics** — not listed as a separate export category (may be in CCDA but unclear if full demographic record is exported)
- **Medications and prescriptions** — not listed separately; Surescripts e-prescribing data may only appear in CCDA summary
- **Billing and revenue cycle data** — completely absent from the export documentation. OMS mentions revenue cycle management on their homepage and uses CPT/ICD coding; none of this appears in the export.
- **Remote patient monitoring data** — the C3 platform captures blood pressure and heart rate readings from Bluetooth devices. "C3 Notes" may cover coordinator notes but RPM device readings/time-series data are not addressed.
- **Referral data** — OMS is certified for CMS50 (closing the referral loop) but referrals are not mentioned in the export.
- **Care plans and goals** — not mentioned.
- **Immunizations** — not mentioned separately (may be in CCDA).
- **Procedures and surgical data** — catheterization lab data implies procedural records, but procedures are not mentioned as an export category.
- **Insurance/coverage information** — not mentioned.
- **Patient portal data** — not mentioned.

The fundamental issue is that the CCDA export (which follows the C-CDA standard) covers only the USCDI/US Core clinical summary subset. The remaining categories are document-oriented exports (HTML, PDF) that capture rendered content but may not preserve the underlying discrete data in a computably useful form. The "Diagnostics" and "Messages" categories mention "discrete fields" but provide zero detail about what those fields are.

### Export Format & Standards

The export uses a mix of formats:
- **C-CDA XML/HTML** for clinical summaries — this is a recognized standard but covers only the (g)(10) clinical data subset
- **HTML** for notes, C3 notes, and smart forms — rendered documents, not structured data
- **PDF** for scanned documents and lab scans — essentially image exports
- **"Discrete fields"** for diagnostics and messages — completely undefined; no schema, no field listing, no format specification

The term "discrete fields" is the most intriguing and the least documented. For a cardiology CVIS that stores structured echocardiography measurements, catheterization data, and other numeric/coded diagnostic data, "discrete fields" could represent genuinely valuable structured export — but without any specification of what fields, what format, or what structure, it is impossible to assess.

There is no mention of FHIR, NDJSON, CSV, SQL dump, or any bulk data format. The export appears to be a document-level export (one document per category per patient) rather than a database-level export.

### Documentation Quality

This is among the most minimal EHI export documentation possible. The entire substantive content fits in a single table with 9 rows and 2 columns. There is:

- **No data dictionary** — not a single field name is defined
- **No schema or format specification** — "discrete fields" is not defined
- **No sample data or examples**
- **No export instructions** — how does a user initiate an export? Is it per-patient? Bulk?
- **No field-level definitions** — for any category
- **No value sets or coded field documentation**
- **No relationship documentation** — how do the exported pieces relate to each other?
- **No worked examples**

A developer could not implement an import of this data based on this documentation. A patient or provider receiving this export would have no specification to interpret the "discrete fields" exports.

The document was created in November 2023 and has not been updated since, despite the product being certified in January 2026. The certification is very recent (5 weeks ago), which may partially explain the sparse documentation, though the PDF predates the certification by over 2 years.

### Structure & Completeness

The documentation provides only category-level granularity (9 categories). There is no field-level documentation whatsoever. This is essentially a list of export file types, not a data dictionary or format specification.

**What's critically missing for a cardiology CVIS:**
- The 16 structured diagnostic reporting modules (echo, EKG, stress, nuclear, cath lab, vascular, Holter) are collapsed into a single "Diagnostics" row with "Discrete fields, PDF" — no information about what discrete fields are exported for any modality
- Remote patient monitoring time-series data (blood pressure, heart rate readings) from the C3/Cardio@Home platform — not addressed
- Billing/claims data — absent entirely
- The claim of processing "6,000+ data points per patient" on the vendor homepage vs. 9 export categories with no field documentation is a stark contrast

## Access Summary
- Final URL: https://objectivemedicalsystems.com/wp-content/uploads/2025/09/EHI-Export-Data-Format.pdf (no redirect)
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare present but did not block curl)

## Obstacles & Dead Ends

None. The URL worked perfectly and the download was straightforward. The obstacle is the content itself — there is almost nothing to download. The disclosures page was checked for additional documentation links but none were found beyond the same PDF.
