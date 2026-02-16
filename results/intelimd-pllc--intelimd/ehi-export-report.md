# inteliMD PLLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.intelimd.com/assets/docs/b10-ehi-export.pdf
- CHPL ID: 11555
- Certificate number: 15.05.05.3211.INTL.01.00.1.241127
- Certification date: 2024-11-27

## Navigation Journal

The registered URL is a direct PDF download. No navigation required.

```bash
# Probe URL — returns 200 with Content-Type: application/pdf, 432456 bytes
curl -sI -L "https://www.intelimd.com/assets/docs/b10-ehi-export.pdf" -H 'User-Agent: Mozilla/5.0'

# Download
curl -sL "https://www.intelimd.com/assets/docs/b10-ehi-export.pdf" -H 'User-Agent: Mozilla/5.0' \
  -o downloads/b10-ehi-export.pdf
```

Verified the download: `file` confirms "PDF document, version 1.4, 5 page(s)".

Also checked the ONC certification page (https://www.intelimd.com/onc-certification) — it is a SPA that renders a C-CDA viewer interface but contains no additional EHI export documentation links or downloadable files. Probed several alternative document paths under `/assets/docs/` (data-dictionary.pdf, ehi-export.pdf, etc.) — all return the SPA's index.html (text/html, 85219 bytes), confirming the b10-ehi-export.pdf is the only real document hosted there.

## What Was Found

A single 5-page PDF titled "170.315(b)(10) Electronic Health Information export" produced with Google Docs Renderer. The document covers:

### Structure of the PDF

1. **Overview (page 1)**: Boilerplate description of the (b)(10) criterion. States that inteliMD's EHR system is designed in alignment with 170.315(b)(10).

2. **Purpose and Scope (page 1)**: States the EHI export feature provides "system level user (superadmin)" with the ability to export "all patient's health information in a standardized format." Mentions data types including "demographics, clinical notes, medications, lab results etc." Specifies that the feature applies to both individual patient exports and bulk exports for a population.

3. **Single Patient Export (pages 2-3)**: Step-by-step instructions with screenshots:
   - Log in to the inteliMD portal with Superadmin credentials
   - Verify OTP sent to registered mobile number
   - Navigate to Patient List page
   - Select a patient and click the eye icon under the Action column
   - A popup shows "Patient Chart Summary" with two download buttons: **PDF** and **C-CDA**
   - Screenshots show the Patient List view (with sample patient data — names, contact details, MRN, SSN, registered dates) and the Profile Summary popup (showing patient demographics, contact info, patient IDs, document ID, performer/author)

4. **Bulk Export (page 4)**: Instructions for bulk export:
   - Click "Download Records" button
   - Server generates C-CDA XML files for all patients
   - Countdown timer shows progress
   - Files are automatically downloaded as a .zip file

5. **Patient EHI C-CDA XML (page 4)**: Brief description that the exported C-CDA XML contains "comprehensive health data such as medical history, test results, treatment plans, and other relevant health records."

6. **Error Codes (page 4)**: Three HTTP error codes: 400 (Invalid search parameter), 500 (Internal Server Error), 401 (Unauthorized access).

7. **Product Info (page 5)**: Developer name, product name, version v1.1, certificate number, certification date, and criteria certified.

### Export Format

The export format is **C-CDA XML** for structured data, with an additional **PDF** option for individual patient exports. Bulk export produces a ZIP file of C-CDA XML files. There is no data dictionary, no schema documentation, no field-level specification, no sample export files, and no description of what specific C-CDA document type or sections are included.

## Export Coverage Assessment

### Data Domain Coverage

The documentation is extremely vague about what data domains are included. The only concrete mentions are:
- "demographics, clinical notes, medications, lab results etc" (in the Purpose and Scope section)
- "medical history, test results, treatment plans, and other relevant health records" (in the C-CDA XML section)

Based on the product research, inteliMD stores:
- **Clinical data**: Demographics, medications/prescriptions, lab orders, imaging orders, drug allergies, family health history, implantable devices, clinical notes/consultation documentation, immunization records, vital signs, problems
- **Telemedicine data**: Video consultation records, secure messages
- **Financial/billing data**: Insurance information, electronic claims, patient billing, payment processing
- **Patient-generated data**: Registration info, portal-captured health info

**Clearly covered**: Demographics (visible in the screenshot), clinical notes, medications, lab results (mentioned in text)

**Unclear/ambiguous**: The documentation says "all patient's health information" but provides no data dictionary or field mapping. There's no way to verify what C-CDA sections are generated or what data elements they contain. The phrase "etc" does a lot of heavy lifting.

**Likely missing or undocumented**:
- **Billing data** — No mention of billing records, claims, charges, or financial data in the export. C-CDA is not a natural format for billing data.
- **E-prescribing records** — No specific mention of whether prescription history is fully represented.
- **Telemedicine session data** — Video consultation records and messaging history are not mentioned.
- **Imaging orders** — Listed as a certified capability but not mentioned in the export.
- **Family health history** — Certified under (a)(12) but not mentioned in export.
- **Implantable device list** — Certified under (a)(14) but not mentioned.
- **Specialty-specific data** — The product targets skilled nursing facilities and home health; any specialty assessments or care plans specific to those settings are not documented.

This appears to be a case where the vendor uses C-CDA as the export format, which inherently constrains coverage to the clinical data that fits within C-CDA's document models. Data domains that don't map well to C-CDA (billing, telemedicine, administrative) are almost certainly not exported.

### Export Format & Standards

The export uses **C-CDA XML**, which is a recognized healthcare interoperability standard (HL7 Consolidated CDA). This is a reasonable choice for clinical data but has significant limitations for a (b)(10) "export everything" requirement:

- C-CDA covers clinical summaries well (problems, medications, allergies, labs, vitals, procedures, immunizations)
- C-CDA does **not** naturally represent billing records, claims, financial data, telemedicine session data, or administrative records
- The documentation does not specify which C-CDA document type is generated (CCD, Discharge Summary, Continuity of Care, etc.)
- No C-CDA template OIDs or section identifiers are provided
- No indication of which C-CDA implementation guide version is followed
- No sample export is provided

The PDF download option for single patients is a secondary format — its content and structure are not described at all.

A third party receiving this export would get C-CDA XML files but would have no documentation to understand inteliMD-specific mappings, extensions, or data representations. They would need to reverse-engineer the XML.

### Documentation Quality

The documentation is **minimal and procedural**. It is essentially a "how to click the button" guide with screenshots, not technical documentation of the export format. Specific gaps:

- **No data dictionary**: No table/field definitions, no C-CDA section mappings, no element descriptions
- **No schema documentation**: No reference to C-CDA templates, OIDs, or profiles used
- **No sample data**: No example export files or representative records
- **No field-level specifications**: No data types, value sets, or constraints
- **No completeness documentation**: No list of what data domains are included or excluded
- **No technical API documentation**: The error codes (400, 500, 401) suggest there's an API behind the UI, but no API endpoint, request/response format, or authentication details are documented
- **No versioning or change history**: Version is listed as v1.1 but no changelog

A developer could not implement an import of this data based on this documentation. They would need to obtain a sample export and reverse-engineer the C-CDA structure.

### Structure & Completeness

The documentation is 5 pages long and consists almost entirely of:
1. Boilerplate regulatory text (1 page)
2. Step-by-step UI instructions with screenshots (2 pages)
3. Brief description of bulk export (1 page)
4. Product identification info (1 page)

There is no data dictionary at any level of granularity — not even table names or broad data categories. The documentation does not describe the internal structure of the C-CDA export. Relationships between entities are not documented. No coded fields or value sets are described.

This is a **compliance checkbox document**, not genuine technical documentation. It demonstrates that an export button exists in the UI but provides no information about what the export contains at a field level.

### (b)(10) vs (g)(10) Assessment

This is **not** the classic (b)(10)/(g)(10) confusion — the vendor is not pointing to a FHIR Bulk Data API. Instead, they provide a UI-based export generating C-CDA XML. However, C-CDA typically covers the same clinical summary data as USCDI/US Core (problems, medications, allergies, labs, vitals, etc.), which means the practical coverage may be similar to a (g)(10) FHIR export — a clinical summary subset rather than "all electronic health information."

The critical question is whether the C-CDA export includes data beyond what's in a typical clinical summary: billing records, telemedicine-specific data, administrative records, and specialty-specific assessments for post-acute/SNF/home health settings. The documentation provides no evidence that it does.

## Access Summary
- Final URL (after redirects): https://www.intelimd.com/assets/docs/b10-ehi-export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The `/assets/docs/` directory listing is forbidden (403)
- The ONC certification page (https://www.intelimd.com/onc-certification) is a SPA that does not contain additional downloadable documentation
- Several alternative document paths all return the SPA's index.html rather than PDFs (the server returns 200 for all paths, making it impossible to distinguish real files from catch-all routes without checking Content-Type headers)
- No data dictionary, schema files, or sample exports are available anywhere on the site
