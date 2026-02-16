# EHI Export Analysis: ASP.MD Inc.

**Product**: ASP.MD Medical Office System (AMOS)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.02.05.1026.ASPM.01.01.0.220203

## 1. Product Context

ASP.MD Medical Office System is a fully web-based, cloud-hosted, integrated EHR and Practice Management system developed by ASP.MD Inc., a small (~14–19 employees) Cambridge, MA-based company founded in 2001. The product targets small independent ambulatory practices, primarily in internal medicine and family medicine.

AMOS is a single integrated platform covering:
- **Clinical documentation**: problem lists, medications, allergies, clinical notes, encounter documentation, clinical decision support
- **E-prescribing**: electronic prescribing with drug interaction checking
- **Lab management**: lab ordering and result management with connectivity to external labs (LabCorp, Quest)
- **Scheduling**: appointment scheduling with automated reminders, eligibility checking
- **Billing and claims**: electronic coding, claims generation/submission, scrubbing, remittance posting, HCC optimization — plus billing-as-a-service
- **Patient portal**: lab results viewing, secure messaging, clinical summary access
- **Quality reporting**: MIPS analytics, 48 certified clinical quality measures
- **Public health reporting**: immunization registry, syndromic surveillance
- **Transitions of care**: C-CDA generation and reconciliation

The product is certified across 36 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, and multiple clinical criteria. All data lives in a single integrated system with no third-party software dependencies (per mandatory disclosures).

For a (b)(10) export to be comprehensive, it should cover clinical records, billing/claims data, scheduling, patient portal communications, prescriptions, lab results, documents/images, and quality reporting data stored in AMOS.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `export-page.html` / `export-page-wp-api.json` (76KB / 7KB) | The vendor's entire EHI export documentation page at `https://www.asp.md/export/`. Contains **66 words** of content: a heading, a list of three export formats, a link to an external HL7 document, and a folder naming convention. Published 2023-11-14, never modified. | **Most informative** (it's the only export documentation) |
| `export-page-screenshot.png` (105KB) | Full-page screenshot confirming the export page contains exactly 5 lines of text between the header and footer. | Confirmatory |
| `disclosures-page.html` (84KB) | Mandatory disclosures page at `https://www.asp.md/disclosures-2/`. Confirms (b)(10) certification. States "no additional fees beyond quoted monthly fees." No additional export documentation. | Minor — confirms certification and pricing only |

**No data dictionary, schema, sample data, field definitions, or machine-readable artifacts of any kind were found.** The entire export documentation is 66 words.

## 3. Export Mechanics

- **Format(s)**: Three formats listed: C-CDA, text files ("industry standard"), PDF files ("industry standard")
- **Mechanism**: Not documented. No description of how to initiate an export (UI button, API call, vendor-assisted, or otherwise).
- **Single-patient vs bulk**: Not documented. The folder naming convention (`LASTNAME_FIRSTNAME_DOB_MRN`) implies per-patient organization, but no process is described.
- **Access constraints or fees**: Disclosures page states "no additional fees beyond quoted monthly fees." No other constraints documented.
- **External documentation reference**: The only technical reference is a link to the HL7 C-CDA Companion Guide (`http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf`), which is a generic industry specification — not product-specific documentation.

## 4. Export Content: What's In It

### What the documentation says

The export documentation consists of this single paragraph (66 words, verbatim):

> Health Information Export
>
> The electronic health information export will include data in the following formats:
>
> C-CDA Documentation can be found here http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf
>
> Text files (industry standard)
>
> PDF files (industry standard)
>
> Files relevant to each patient will be stored in folders with name format LASTNAME_FIRSTNAME_DOB_MRN where DOB is Date of Birth formatted YYYYMMDD and MRN is medical record number, an integer linking to the MRN in C-CDA.

### What this tells us

1. **C-CDA**: The export includes C-CDA documents. The only documentation provided is a link to the generic HL7 C-CDA Companion Guide — there is no product-specific mapping, no description of which C-CDA sections are populated, no indication of what data elements are included beyond what the C-CDA standard defines.

2. **Text files**: Described only as "industry standard." No specification of what data these contain, what format they use (CSV, TSV, fixed-width, free-text), what fields are included, or what "industry standard" refers to.

3. **PDF files**: Described only as "industry standard." No specification of content. These could be rendered clinical notes, reports, scanned documents, or something else entirely.

4. **Folder structure**: Patient folders use `LASTNAME_FIRSTNAME_DOB_MRN` naming, with MRN linking to the C-CDA. This is the only structural detail provided.

### Vendor's own content organization

There is no content organization. No entities, tables, categories, or data domains are defined. The vendor provides no data dictionary whatsoever.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not describe what data is exported at the field level. The only concrete statement is that the export includes C-CDA, text files, and PDF files organized in per-patient folders. With no data dictionary, no schema, and no field-level documentation, it is impossible to determine from the documentation alone what data domains are covered.

The C-CDA component, by definition, would cover standard USCDI clinical data classes (demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, clinical notes). However, the vendor provides no indication of whether their C-CDA includes all standard sections or a subset, and no information about what the "text files" and "PDF files" contribute beyond the C-CDA.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA would contain basic demographics; no field-level detail provided | Product stores demographics; C-CDA covers basics but depth unknown |
| Encounters / visits | ⚠️ Partial | C-CDA encounters section (assumed, not documented) | Product manages encounters; no documentation of export depth |
| Problems / conditions | ⚠️ Partial | C-CDA problems section (assumed, not documented) | Product stores problem lists; no documentation of export depth |
| Medications / prescriptions | ⚠️ Partial | C-CDA medications section (assumed, not documented) | Product has e-prescribing; no documentation of Rx history depth |
| Allergies | ⚠️ Partial | C-CDA allergies section (assumed, not documented) | Product stores allergies; no documentation of export depth |
| Immunizations | ⚠️ Partial | C-CDA immunizations section (assumed, not documented) | Product stores immunizations (certified (h)(1)); depth unknown |
| Vitals | ⚠️ Partial | C-CDA vitals section (assumed, not documented) | Product stores vitals; depth unknown |
| Lab results | ⚠️ Partial | C-CDA results section (assumed, not documented) | Product has lab connectivity; depth unknown |
| Imaging / diagnostic reports | ❌ Not covered | No mention in documentation | Product has imaging/document management; not addressed |
| Procedures | ⚠️ Partial | C-CDA procedures section (assumed, not documented) | Product stores procedures; depth unknown |
| Clinical notes / documents | ⚠️ Partial | PDF files may contain notes; no specification | Product generates clinical notes; format/completeness unknown |
| Care plans / goals | ❌ Not covered | No mention beyond C-CDA | No evidence of dedicated export |
| Orders / referrals | ❌ Not covered | No mention in documentation | Product has CPOE (certified (a)(1)–(a)(3)); not addressed |
| Insurance / coverage | ❌ Not covered | No mention in documentation | Product does eligibility checking and insurance management; **significant gap** |
| Claims / billing | ❌ Not covered | No mention in documentation | Product has full billing/claims capability; **significant gap** |
| Payments | ❌ Not covered | No mention in documentation | Product does remittance/payment posting; **significant gap** |
| Consents / directives | ❌ Not covered | No mention in documentation | Unknown if product stores these |
| Patient communications | ❌ Not covered | No mention in documentation | Product has patient portal with secure messaging; **gap** |
| Specialty-specific data | N/A | — | Product is general ambulatory; no deep specialty modules known |

**Key gaps**: The product is an integrated EHR/PM with robust billing capabilities (claims generation, scrubbing, remittance posting, HCC optimization). None of this billing/financial data is documented as part of the export. Similarly, patient portal communications, scheduling data, and quality reporting data are not addressed. The C-CDA component — even if fully populated — covers only USCDI-scope clinical data, which is a fraction of what this integrated system stores.

## 6. Documentation Quality

The export documentation is among the thinnest possible:

- **66 words total** — the entire EHI export documentation fits in a tweet
- **No data dictionary** — zero entities, zero fields, zero descriptions
- **No schema** — no machine-readable format definition of any kind
- **No sample data** — no examples of export output
- **No process documentation** — no instructions on how to request or initiate an export
- **No product-specific technical detail** — the only technical reference is a link to the generic HL7 C-CDA Companion Guide, which describes the C-CDA standard generally, not ASP.MD's implementation of it
- **"Text files (industry standard)" and "PDF files (industry standard)"** — these descriptions are content-free; "industry standard" is not defined or referenced

A developer receiving this documentation could not build an import system. A patient receiving this export would have no way to understand what data they received or whether it was complete. The documentation provides no basis for verifying export completeness.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess what the export actually contains. The 66-word page provides no data dictionary, no field definitions, and no enumeration of data domains covered. The only concrete format mentioned is C-CDA, which by its nature covers USCDI-scope clinical data — a small fraction of what this integrated EHR/PM stores. The product has extensive billing, claims, scheduling, patient portal, and quality reporting capabilities, none of which are documented as part of the export. Even the C-CDA component is undocumented at the product level — the vendor simply links to the generic HL7 specification.

**Axis 2 — Export approach: Repackaged existing export**

The strongest signal is that C-CDA is listed first and is the only format with any technical reference (the HL7 Companion Guide). C-CDA is the same format used for transitions of care (certified criteria (b)(1)–(b)(3)), strongly suggesting the (b)(10) export reuses the existing C-CDA generation capability. The "text files" and "PDF files" may supplement this, but without any documentation of their content, they could be anything from rendered notes to patient summaries. There is no evidence of a purpose-built export mechanism that reaches beyond the existing clinical exchange surface to cover billing, administrative, or operational data.

### Key Findings

1. **Documentation is essentially empty**: The entire EHI export documentation is 66 words — a heading, three format names, a link to an external specification, and a folder naming convention. This is among the thinnest (b)(10) documentation possible. (Source: `export-page-wp-api.json`)

2. **No data dictionary exists**: Zero entities, zero fields, zero descriptions. There is no way to determine from the documentation what data elements are included in the export. (Source: `export-page.html`, confirmed by screenshot)

3. **C-CDA is the primary documented format**: The only format with any technical reference is C-CDA, linked to the generic HL7 Companion Guide rather than a product-specific implementation guide. This strongly suggests the export is the vendor's existing transitions-of-care C-CDA repurposed for (b)(10). (Source: `export-page-wp-api.json`)

4. **Billing/PM data not addressed**: AMOS is an integrated EHR/PM with full billing capabilities (claims, scrubbing, remittance, HCC optimization). None of this data is documented as part of the export, representing a significant gap. (Source: product-research.md vs. export documentation)

5. **Page has never been updated**: The WordPress API confirms the export page was published 2023-11-14 and has never been modified, suggesting it was created once for certification compliance and never revisited. (Source: `export-page-wp-api.json`, `modified` field matches `published` field)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA, text files, PDF files
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 15 confirmed; ~9 of 15 assumed via C-CDA (undocumented)
```

### Bottom Line

ASP.MD's (b)(10) EHI export documentation is a 66-word stub with no data dictionary, no schema, no sample data, and no product-specific technical detail. The export appears to be the vendor's existing C-CDA transitions-of-care output relabeled as an EHI export, supplemented by undefined "text files" and "PDF files." A patient or provider receiving this export would have no way to know what data they received, whether it was complete, or how to interpret the non-C-CDA files — and the product's extensive billing, scheduling, patient portal, and quality reporting data is almost certainly not included.
