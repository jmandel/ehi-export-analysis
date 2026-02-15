# GeniusDoc, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.geniusdoc.com/DataExport/GeniusDoc_Data_Export.pdf
- CHPL IDs: 10745
- Developer: GeniusDoc, Inc.
- Product: GeniusDoc 12.0 (certified 2021-12-09)

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
# Probe the URL
curl -sI -L "https://www.geniusdoc.com/DataExport/GeniusDoc_Data_Export.pdf" -H 'User-Agent: Mozilla/5.0'
# Returns: HTTP/2 200, content-type: application/pdf, content-length: 159078

# Download the PDF
curl -sL "https://www.geniusdoc.com/DataExport/GeniusDoc_Data_Export.pdf" -H 'User-Agent: Mozilla/5.0' \
  -o downloads/GeniusDoc_Data_Export.pdf

# Verify it's a real PDF
file downloads/GeniusDoc_Data_Export.pdf
# PDF document, version 1.7, 2 page(s)
```

I also checked:
- `/DataExport/` directory — 403 Forbidden (no directory listing)
- Common alternative paths (`/ehi`, `/ehi-export`, `/b10`, `/data-export`) — all 404
- `API.php` — this is their FHIR API page for (g)(10), separate from the EHI export. Notes "There are currently no GeniusDoc customers integrated with the API."
- `ONC_Certification_Costs.php` — mandatory disclosures page, no EHI export references
- Main page (`index.php`) — no links to EHI export documentation beyond the standard navigation

The single PDF is the entirety of their publicly available EHI export documentation.

## What Was Found

The PDF is a 2-page document (page 2 is blank) titled "Data Export Details" with the GeniusDoc logo. It was created in Microsoft Word on November 17, 2023 (author field: "exotic").

The document describes six categories of data that can be exported under 170.315(b)(10):

1. **Demographics and Insurance** — exported in Excel format; "comprehensive patient demographics and insurance details"
2. **Medications and Allergies** — exported in Excel format; "patient medications and allergies details"
3. **Problems** — exported in Excel format; "the active patient diagnosis"
4. **Lab Results** — exported in Excel format; "structured patient lab results"
5. **Visit Summaries** — exported in PDF format and CDA format (per HL7 CDA standards); a "reference link document" is provided in Excel format
6. **Documents** — all scanned or imported documents in the patient chart; a reference file provides "document index, file information, folder names and patient details"

The document ends with a brief paragraph about data privacy, encryption, and safe transmission, and encourages clients to check the website for updates.

There is no data dictionary, no field-level documentation, no schema, no sample data, and no instructions for how to request or perform the export. The descriptions are purely categorical — they name the broad data types but provide zero detail about what fields are included, what the Excel columns are, how relationships between files are expressed, or what the CDA documents contain beyond being "per HL7 CDA standards."

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes six categories that cover a narrow slice of what GeniusDoc stores. Based on the product research, GeniusDoc is a comprehensive ambulatory EHR with deep oncology/hematology capabilities, integrated billing, scheduling, document management, quality reporting, and public health reporting. Here is how the documented export maps to the product's data domains:

**Clearly covered (at least mentioned):**
- Patient demographics and insurance
- Medications
- Allergies
- Problems/diagnoses (active only — not resolved or historical)
- Lab results
- Visit summaries (encounter documentation)
- Scanned/imported documents

**Clearly absent — not mentioned at all:**
- **Chemotherapy/oncology data** — This is GeniusDoc's flagship specialty feature. Chemo regimens, dose calculations (BSA, AUC, ANC), cumulative dose tracking, cancer staging (TNM), tumor markers, chemo administration records, oncology nurse assessments — none of this is mentioned. For an oncology-focused EHR, this is the most significant gap.
- **Prescribing data** — E-prescribing transactions, drug interaction screening results, prescription history beyond the current medication list
- **Billing and financial data** — Charges, claims, CPT/ICD codes, EOB data, remittance advice, payment records, accounts receivable. The billing module is a major component of GeniusDoc.
- **Scheduling data** — Appointments, treatment calendars, wave scheduling
- **Orders/CPOE** — Computerized provider order entry records, imaging orders
- **Vital signs** — Not mentioned as a separate export category (may be embedded in visit summaries, but not documented)
- **Immunization records** — Not mentioned (the product is certified for immunization registry reporting)
- **Clinical decision support data** — Alerts, health maintenance records
- **Quality reporting data** — MIPS measures, PQRS data, QOPI measures
- **Public health reporting data** — Syndromic surveillance, cancer registry submissions
- **Care coordination data** — CCM module data, care plans, referrals, medication reconciliation
- **Audit logs** — Access logs, security audit trails
- **Patient portal data** — Patient engagement records, portal activity
- **Correspondence** — Referral letters, discharge summaries (unless included under "Documents")
- **Audio/video files** — The product stores these in patient charts

The export description reads more like a **patient clinical summary** than a comprehensive EHI export. It covers the core USCDI-equivalent data classes (demographics, meds, allergies, problems, labs, encounters) plus documents — essentially what you'd find in a C-CDA patient summary. This strongly resembles what would satisfy (g)(10) rather than (b)(10).

The explicit mention that Problems covers only "active patient diagnosis" is a red flag — a true (b)(10) export should include resolved/historical diagnoses as well, since they are electronic health information the system stores.

### Export Format & Standards

The export uses a mix of formats:
- **Excel** for structured data (demographics, insurance, medications, allergies, problems, labs, document index)
- **PDF** for visit summaries
- **CDA (HL7 CDA)** for visit summaries
- **Original file formats** for scanned/imported documents (implied)

This is a reasonable approach for a small vendor — Excel is universally readable and can preserve tabular structure. However, without any documentation of what columns the Excel files contain, the format is essentially undefined. A recipient would have to reverse-engineer the column meanings.

The CDA format for visit summaries is a standardized choice, but no profile or template is specified — "per HL7 CDA standards" could mean anything from a minimal CDA header to a full C-CDA Continuity of Care Document.

The lack of any schema, data dictionary, or sample file means that the export format is effectively opaque. A third party could not implement an import based on this documentation alone.

### Documentation Quality

This is among the thinnest EHI export documentation possible while technically existing. Key deficiencies:

- **No data dictionary** — Not a single field name, column heading, or data type is documented
- **No schema or structure definition** — No description of what the Excel files contain
- **No sample data** — No example files or records
- **No instructions** — No description of how to request or perform an export (who initiates it? Is it self-service or vendor-mediated? What parameters are available?)
- **No export process documentation** — No mention of timelines, formats, delivery mechanisms
- **No field-level detail** — Only category-level descriptions (e.g., "patient medications and allergies details")
- **No relationship documentation** — No description of how the exported files relate to each other (e.g., how to link a document reference to a visit summary)

The document is 1 page of actual content. It reads as a compliance checkbox — the minimum conceivable effort to have a publicly accessible URL that mentions (b)(10).

A developer receiving this export would have no documentation to work from. They would need to examine the Excel files themselves to understand the schema, infer column meanings, and hope that the data is self-documenting.

### Structure & Completeness

- **Granularity**: Category-level only. No table names, no field names, no data types, no value sets, no constraints, no cardinality.
- **Coded fields**: Not documented at all. No mention of coding systems, value sets, or terminology.
- **Relationships**: Not documented. No description of how files relate to each other or how to reconstruct a complete patient record.
- **Versioning**: The PDF was created November 17, 2023. No version number, no change history.

## Access Summary
- Final URL (after redirects): https://www.geniusdoc.com/DataExport/GeniusDoc_Data_Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None — the URL worked on the first try with a simple curl request. The obstacle is not access but substance: the documentation that exists is extraordinarily thin.

The `/DataExport/` directory returns 403 (no listing), and no other EHI-related paths exist on the site. The `API.php` page documents their FHIR API (a separate system for g(10)), which notably states "There are currently no GeniusDoc customers integrated with the API."
