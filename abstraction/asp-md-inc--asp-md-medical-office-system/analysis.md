# EHI Export Analysis: ASP.MD Inc.

**Product**: ASP.MD Medical Office System (AMOS), Version 92
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.1026.ASPM.01.01.0.220203

## 1. Product Context

ASP.MD Medical Office System is a fully integrated, web-based EHR and Practice Management (PM) platform targeting small, independent ambulatory practices — primarily internal medicine and family medicine. The company (~14–19 employees) is based in Cambridge, MA and offers the software alongside professional billing and compliance services.

Key data domains the product stores, relevant to EHI export completeness:

- **Clinical records**: problem lists, medications, allergies, vitals, clinical notes, encounter documentation, lab results (with LabCorp/Quest connectivity), imaging/radiology, immunizations, procedures, family health history, care plans
- **E-prescribing**: medication orders, drug interaction checks
- **Billing and claims**: electronic coding with payer-specific rules, automated claims submission, claims scrubbing, adjudication tracking, electronic remittance/payment posting, HCC optimization
- **Insurance**: patient insurance/eligibility, real-time electronic eligibility checking
- **Patient portal**: secure messaging, lab results viewing, clinical summary download
- **Scheduling**: appointment scheduling with automated reminders
- **Quality reporting**: MIPS analytics, 48 certified clinical quality measures
- **Public health reporting**: immunization registry, syndromic surveillance
- **Transitions of care**: C-CDA generation and reconciliation

This is a single integrated platform — all data lives within AMOS, with no separate modules or third-party components required.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informative? |
|---|---|---|---|---|
| `export-page.html` | HTML | 76,272 bytes | Full HTML of the EHI export documentation page at `https://www.asp.md/export/`. Actual content is 5 sentences amid WordPress theme boilerplate. | **Most informative** — this is the entirety of the vendor's export documentation |
| `export-page-wp-api.json` | JSON | 7,298 bytes | WordPress REST API representation of the export page. Confirms page published 2023-11-14 and never modified since. | Useful for metadata (publication date, revision history) |
| `export-page-screenshot.png` | PNG | 105,245 bytes | Full-page browser screenshot confirming visual layout: heading, 5 lines of text, footer. No hidden content, collapsed sections, or JS-loaded elements. | Useful for visual verification |
| `disclosures-page.html` | HTML | 83,891 bytes | Mandatory disclosures page at `https://www.asp.md/disclosures-2/`. Confirms 170.315(b)(10) certification but contains no additional export documentation or links. | Low informative value for this analysis |

**Verification notes**:
- The live export page at `https://www.asp.md/export/` was fetched during this analysis (2026-02-16) and returns HTTP 200 with content identical to the downloaded artifact.
- No additional export documentation was found elsewhere on the site (confirmed by the prior agent's WordPress API enumeration and path probing, which I verified via the live site response headers showing the same WordPress installation).

## 3. Export Mechanics

- **Format(s)**: Three formats mentioned — C-CDA, "text files (industry standard)", "PDF files (industry standard)"
- **Mechanism**: Not documented. No instructions for how a provider, administrator, or patient would initiate an export.
- **Single-patient vs bulk**: Not documented. The folder naming convention (`LASTNAME_FIRSTNAME_DOB_MRN`) implies per-patient organization, but whether single-patient or bulk export is supported is not stated.
- **Access constraints or fees**: Not documented.

The documentation provides zero procedural information about obtaining an export.

## 4. Export Content: What's In It

### What the documentation states

The entire export documentation is the following text from the export page (`export-page-wp-api.json`, published 2023-11-14):

> Health Information Export
> The electronic health information export will include data in the following formats:
>
> C-CDA Documentation can be found here http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf
>
> Text files (industry standard)
>
> PDF files (industry standard)
>
> Files relevant to each patient will be stored in folders with name format LASTNAME_FIRSTNAME_DOB_MRN where DOB is Date of Birth formatted YYYYMMDD and MRN is medical record number, an integer linking to the MRN in C-CDA.

That is the complete documentation. There is:
- **No data dictionary** — zero tables, fields, columns, data types, or schemas
- **No export format specification** beyond naming three formats
- **No field-level documentation** of any kind
- **No sample exports or examples**
- **No schema files** (XSD, JSON Schema, etc.)
- **No API documentation**
- **No description of what data is included** in each format

### Vendor's own content organization

There is no vendor-defined content organization. The vendor does not enumerate entities, tables, categories, or data domains. The only structural information is:

| Format | Description (vendor's) | Fields documented | Specification detail |
|---|---|---|---|
| C-CDA | "Documentation can be found here" + external HL7 link | 0 | External standard reference only; no vendor-specific section list, mapping, or customization |
| Text files | "industry standard" | 0 | Completely undefined — no format, encoding, delimiter, or content specification |
| PDF files | "industry standard" | 0 | Completely undefined — no content specification |

**Total entities documented: 0. Total fields documented: 0.**

The phrase "industry standard" applied to text and PDF files is meaningless without further specification — there is no single "industry standard" format for either.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides no categorization of export content. The only structure is three output formats:

1. **C-CDA**: By the nature of the standard, C-CDA documents typically carry demographics, problems, medications, allergies, lab results, vitals, immunizations, procedures, and some clinical notes. However, ASP.MD does not specify which C-CDA document type(s) they produce (CCD, Referral Note, etc.) or which sections they populate. The link to the external HL7 Companion Guide is a general reference, not a vendor-specific mapping.

2. **Text files**: Completely unspecified. Could contain clinical notes, billing data, or anything — there is no way to determine scope from the documentation.

3. **PDF files**: Completely unspecified. Could be rendered clinical documents, billing statements, lab reports, or other content.

The vendor does not describe any domain-specific content in the export. There is no mention of billing, claims, insurance, prescriptions, scheduling, portal messages, quality measures, or any specific clinical data type.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied by C-CDA; not explicitly documented | Product stores demographics; C-CDA likely includes basic demographics, but vendor doesn't confirm which fields |
| Encounters / visits | ⚠️ Partial | Implied by C-CDA | Product stores encounters; likely in C-CDA but unconfirmed |
| Problems / conditions | ⚠️ Partial | Implied by C-CDA | Product stores problem lists; likely in C-CDA but unconfirmed |
| Medications / prescriptions | ⚠️ Partial | Implied by C-CDA | Product has e-prescribing; C-CDA likely includes med list but prescription history depth is unknown |
| Allergies | ⚠️ Partial | Implied by C-CDA | Likely in C-CDA but unconfirmed |
| Immunizations | ⚠️ Partial | Implied by C-CDA | Likely in C-CDA but unconfirmed |
| Vitals | ⚠️ Partial | Implied by C-CDA | Likely in C-CDA but unconfirmed |
| Lab results | ⚠️ Partial | Implied by C-CDA | Product has lab connectivity; likely in C-CDA but depth unknown |
| Imaging / diagnostic reports | ⚠️ Partial | Possibly in text/PDF files | Product stores images/documents; no confirmation of export inclusion |
| Procedures | ⚠️ Partial | Implied by C-CDA | Likely in C-CDA but unconfirmed |
| Clinical notes / documents | ⚠️ Partial | Possibly in text/PDF files | Product stores clinical notes; may be in text/PDF but unspecified |
| Care plans / goals | ⚠️ Partial | Implied by C-CDA | Unconfirmed |
| Orders / referrals | ⚠️ Partial | Possibly in C-CDA | Product supports CPOE; unconfirmed |
| Insurance / coverage | ❌ Not covered | No mention in documentation | Product stores insurance/eligibility data; **significant gap** |
| Claims / billing | ❌ Not covered | No mention in documentation | Product has deep billing — claims submission, adjudication, remittance posting, HCC coding; **major gap** |
| Payments | ❌ Not covered | No mention in documentation | Product handles electronic remittance/payment posting; **significant gap** |
| Consents / directives | ❌ Not covered | No mention in documentation | Unknown if product stores; cannot confirm gap |
| Patient communications / portal messages | ❌ Not covered | No mention in documentation | Product has patient portal with secure messaging; **gap** |

**Key finding**: Every clinical domain is marked "Partial" rather than "Covered" because the vendor does not actually confirm any C-CDA sections or data elements — coverage is inferred entirely from the C-CDA standard itself, not from vendor documentation. All billing-related domains are explicitly absent from the documentation, despite the product being a deeply integrated billing system.

## 6. Documentation Quality

The export documentation is among the most minimal possible for a certified EHR product:

- **5 sentences** on a single web page — the entirety of the vendor's EHI export documentation
- **No data dictionary, schema, or field definitions** of any kind
- **No sample data or worked examples**
- **No machine-readable artifacts** (no JSON schema, XSD, CSV templates)
- **No procedural documentation** for initiating an export
- **No version history** — page published 2023-11-14 (20 months after certification), never updated

A developer receiving this export would be able to parse the C-CDA files (using the C-CDA standard, not vendor documentation), but the text and PDF files would be completely opaque. Building an automated import system from this documentation alone is not feasible.

The documentation reads as a compliance checkbox — the minimum text needed to have a page at the registered URL.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what the export actually contains. Five sentences naming three output formats (C-CDA, text, PDF) with no data dictionary, no field-level detail, no sample data, and no specification of what data domains are covered. The vendor appears to have created the minimum possible page to satisfy the certification requirement of having a registered URL.

### Key Findings

1. **The export documentation is 5 sentences with zero field-level detail.** The entire (b)(10) documentation at `https://www.asp.md/export/` is a heading and four sentences naming three output formats and a folder naming convention. No data dictionary, schema, sample data, or content specification exists. (Source: `export-page-wp-api.json`, verified against live page 2026-02-16)

2. **Billing data is entirely absent from the documentation despite being a core product capability.** ASP.MD is an integrated EHR/PM system with deep billing functionality (claims submission, adjudication tracking, electronic remittance, HCC coding). C-CDA does not naturally carry billing data, and neither text files nor PDF files are documented to include it. This represents a probable major gap in EHI coverage. (Source: product capabilities from `product-research.md`; absence verified in `export-page-wp-api.json`)

3. **Clinical data coverage relies entirely on C-CDA standard inference, not vendor documentation.** The vendor does not specify which C-CDA document types or sections they produce. All clinical domain coverage assessments are based on what C-CDA *typically* includes, not what ASP.MD *confirms* it includes. (Source: `export-page-wp-api.json` — the only C-CDA reference is an external HL7 Companion Guide link)

4. **"Text files" and "PDF files" are completely undefined.** These are described only as "industry standard" with no specification of content, structure, encoding, or what data they contain. These could significantly expand export coverage — or they could be trivial — but the documentation makes it impossible to assess. (Source: `export-page-wp-api.json`)

5. **Documentation has not been updated since initial publication.** Published 2023-11-14 (20 months after the 2022-02-03 certification date) and never modified. (Source: `export-page-wp-api.json`, `date` and `modified` fields are identical)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA + undefined text + undefined PDF
Model type:      Standard projection (C-CDA) + unspecified
Entities:        0 (no data dictionary)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 15 confirmed; ~9 of 15 inferred via C-CDA standard
```

### Bottom Line

A patient or provider requesting an EHI export from ASP.MD would receive C-CDA files (parseable via the standard) alongside undefined text and PDF files with no documentation explaining their contents. The vendor provides no data dictionary, no field definitions, and no specification of what data domains are exported. Most critically, billing and claims data — a core function of this integrated EHR/PM product — appears entirely absent from the export, representing a significant gap in EHI coverage under 170.315(b)(10).
