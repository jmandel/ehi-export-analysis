# Perk Medical Systems LLC (PCB Apps LLC) — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://penn-clinical.com/ehi-export
- CHPL IDs: 11237 (15.07.04.2154.Ezpr.15.01.1.230208)
- Product: ezPractice V15.1
- Certification date: 2023-02-08

## Navigation Journal

The registered URL https://penn-clinical.com/ehi-export loads directly (HTTP 200) as a GoDaddy-hosted page on the PennClinical website. The page is simple: a "Download PDF" link at the top and an embedded PDF viewer showing the 7-page EHI Export documentation. The nav bar has an "ONC" dropdown with sub-links including EHI-export, API Documentation, FHIR Base Url, and ezPractice-fhir-service.

```bash
# Initial probe
curl -sI -L "https://penn-clinical.com/ehi-export" -H 'User-Agent: Mozilla/5.0'
# Returns HTTP 200, Content-Type: text/html;charset=utf-8

# Download the EHI Export PDF (linked from page)
curl -sL "https://img1.wsimg.com/blobby/go/6df195d6-1497-405a-bdde-4de17c7e19a1/EHI%20Export.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o "EHI Export.pdf"
# 289,017 bytes, PDF document, 7 pages

# FHIR base URLs CSV (linked from ONC nav dropdown)
curl -sL "https://pcbapps.com/wp-content/uploads/2022/11/fhir-base-urls.csv" \
  -H 'User-Agent: Mozilla/5.0' -o "fhir-base-urls.csv"
# 263 bytes, lists test/prod FHIR endpoints
```

The API Documentation page (https://penn-clinical.com/api-documentation) hosts a separate 58-page PDF titled "SmartOnFHIR API Documentation template (g7910)" covering the (g)(10) FHIR API. This was examined but not downloaded because it documents the standardized FHIR API, not the (b)(10) EHI export mechanism. The EHI export document itself describes a completely different export mechanism (ZIP files with C-CDA + CSV), confirming these are separate systems.

## What Was Found

The EHI Export documentation is a single 7-page PDF. After 2 pages of cover matter, copyright notices, and legal boilerplate, the substantive content spans roughly 3 pages. Here is what it describes:

### Export Mechanism
The export produces one or more ZIP files containing patient data. A single patient or a full collection of patients can be exported. The ZIP file contains:

1. **Patient Demographics and Clinical Data** — HL7 C-CDA R2.1 formatted XML files, each paired with an HTML rendering. These follow the standard C-CDA specification.

2. **Adhoc Patient Notes** — CSV files containing telephone calls, adhoc notes, and other patient notes. Filename includes a "patNotes" TYPE indicator. The CSV has 6 columns:
   - PID (Patient ID)
   - Patient Notes ID
   - Username (who documented the note)
   - Subject (may be blank)
   - Patient Notes Category (user-defined, from a pick list)
   - Patient Notes Date
   - Patient Notes (the actual note content)

3. **Scanned Records** — HL7 CDA formatted XML files containing Base64-encoded scanned/uploaded documents. Filename includes an "Echart" TYPE indicator. Can be large depending on volume of scanned data.

### File Naming Convention
Files follow the pattern: `PID_INTERNALNUMBERING.EXT` or `PID_INTERNALNUMBERING_TYPE.EXT`
- PID = Patient ID (unique number)
- INTERNALNUMBERING = internal control number (can be ignored)
- TYPE = content descriptor (e.g., "Claim Data", "Echart", "patNotes")
- EXT = file extension (XML, HTML, CSV)

### Fees
No fees for self-service export. If ezPractice performs the export on the user's behalf, fees may apply based on time and effort.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes three categories of exported data: C-CDA clinical data, adhoc patient notes (CSV), and scanned records (CDA). Notably, the file naming convention mentions "Claim Data" as one of the TYPE values, suggesting billing/claims data is part of the export even though it is not described in detail in the documentation.

**Likely covered (via C-CDA R2.1):**
- Patient demographics
- Medications
- Allergies
- Problems/diagnoses
- Lab results
- Vital signs
- Immunizations
- Procedures
- Clinical notes (to the extent included in C-CDA sections)

**Covered via separate files:**
- Adhoc patient notes (CSV) — telephone calls, miscellaneous notes
- Scanned/uploaded documents (CDA with Base64 encoding)
- Claim data (mentioned in filename convention as a TYPE, but not described further)

**Unclear or potentially missing:**
- **Billing records** — "Claim Data" is mentioned as a TYPE value in the filename convention, suggesting it's exported, but the documentation provides no detail on its format, fields, or structure. This is a significant gap in the documentation, not necessarily in the export itself.
- **CPOE orders** — Medication orders, lab orders, and imaging orders are key certified features. These may be represented within C-CDA documents, but the documentation doesn't explicitly confirm this.
- **Family health history** — Certified for (a)(12), likely in C-CDA but not explicitly mentioned.
- **Implantable devices** — Certified for (a)(14), likely in C-CDA but not explicitly mentioned.
- **Clinical decision support data** — Alerts and rules are system configuration, not EHI, but CDS-triggered data entries would be EHI.
- **E-prescribing data** — Via DrFirst Rcopia integration. Whether prescriptions are fully captured in the C-CDA export or whether they remain in DrFirst's system is unclear.
- **Direct messaging content** — Certified for (h)(1), but whether exchanged Direct messages are included in the export is not stated.
- **Patient-submitted health information** — Certified for (e)(3), not mentioned in export docs.

**Key observation:** The documentation mentions the product portfolio includes "Practice Management" and "Revenue Cycle Management" services, and the filename TYPE values include "Claim Data" — suggesting billing data IS part of the export. However, there is zero documentation of the claim data format, fields, or structure. Someone receiving claim data files would have no documentation to interpret them.

### Export Format & Standards

The export uses a mixed format approach:
- **C-CDA R2.1** for clinical data — a well-established healthcare standard. This is appropriate for demographics and clinical summaries but inherently limited to what C-CDA sections cover. C-CDA is a clinical document standard, not a complete database export format.
- **CSV** for adhoc patient notes — simple and interpretable, with column descriptions provided.
- **CDA with Base64** for scanned records — standard approach for encoded document attachments.

The C-CDA format means clinical data export is constrained to what C-CDA sections support. Data that doesn't map well to C-CDA (specialty-specific fields, custom forms, billing line items, scheduling) either gets omitted or squeezed into generic sections. The documentation simply points to the C-CDA R2.1 specification rather than documenting which C-CDA sections are populated or how ezPractice-specific data maps to C-CDA elements.

A third party could reasonably process the C-CDA files (since C-CDA is a well-known standard) and the patient notes CSV (since column descriptions are provided). However, the claim data format is undocumented, and the scanned records would require understanding CDA + Base64 decoding with no guidance on the types of documents encoded.

### Documentation Quality

The documentation is minimal but functional for its scope:
- **Readable:** The 7-page PDF is straightforward and easy to follow.
- **Data dictionary:** Only the patient notes CSV has field-level descriptions (6 columns). Clinical data defers entirely to the C-CDA R2.1 specification with no ezPractice-specific mapping.
- **No examples:** No sample export files, no worked examples, no sample C-CDA with annotations.
- **No schema files:** No XSD, JSON Schema, or any machine-readable format specification.
- **No import guidance:** A developer would need to know C-CDA R2.1 to process the clinical files and would be on their own for claim data.
- **Compliance checkbox feel:** The document reads like a minimal compliance document — it covers just enough to describe the export mechanism but doesn't provide the depth needed for practical data interchange.

### Structure & Completeness

- File naming convention is documented
- Three file categories are described at a high level
- Only the CSV (patient notes) has field-level documentation
- C-CDA content defers entirely to external spec references
- Claim data is mentioned but completely undocumented
- No value sets, coded field documentation, or relationship descriptions
- No versioning or change history

## Access Summary
- Final URL (after redirects): https://penn-clinical.com/ehi-export
- Status: found
- Required browser: no (PDF downloadable via direct curl)
- Navigation complexity: direct_link (PDF link on the registered page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The URL loaded cleanly and the PDF downloaded without issues.
- The API Documentation page was checked and confirmed to be (g)(10) FHIR API documentation, separate from the EHI export.
- The FHIR base URLs CSV (linked from nav) contains only endpoint URLs — not EHI export-related, but downloaded for completeness.
