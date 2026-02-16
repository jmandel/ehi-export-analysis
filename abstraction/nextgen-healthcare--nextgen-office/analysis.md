# EHI Export Analysis: NextGen Healthcare

**Product**: NextGen Office  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 9372 (15.04.04.2054.Medi.05.00.1.180220)

## 1. Product Context

NextGen Office is a cloud-based, integrated EHR and practice management platform for small ambulatory practices (1–10 providers). Originally built as MediTouch EHR by HealthFusion (acquired by NextGen Healthcare in 2016 for $165M), it is a separate product from the larger NextGen Enterprise platform, with its own cloud-native technology stack.

The product is a full-featured all-in-one platform encompassing:

- **Clinical EHR**: charting, problem lists, medication lists, allergy lists, vitals, immunizations, labs, imaging orders, clinical notes (including AI-generated SOAP notes via Ambient Assist), e-prescribing with EPCS, clinical decision support, CPOE
- **Practice management**: scheduling, patient registration, insurance eligibility verification, referral management
- **Billing & revenue cycle**: electronic claims submission (via Office Ally clearinghouse), EDI, charge capture, CPT/ICD-10 coding, collections, denial management, A/R, electronic statements, online bill pay
- **Patient engagement**: patient portal (NextGen PxP) with secure messaging, self-scheduling, digital intake forms, medication refill requests, telehealth
- **Specialty support**: specialty-specific clinical templates ("blueprints") for 40+ specialties
- **Reporting**: MIPS/MACRA quality reporting, financial analytics
- **Public health**: immunization registry submission, electronic case reporting

This breadth means a genuine (b)(10) EHI export should cover clinical, billing, administrative, and patient engagement data across all these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-data-dictionary-page.html` (175,648 bytes) | Full HTML source of the registered EHI documentation page at nextgen.com. Contains sections for four products: Enterprise EHR, Office, Direct Messaging, Mirth Connect. The NextGen Office section is 85 words of prose listing four file types — no data dictionary, no schema, no field definitions. | **Primary source** for Office; extremely thin |
| `downloads/screenshot-office-section.png` | Screenshot visually confirming the Office section has only a bullet list of file types (C-CDA, CSV, binary, HTML) with no dictionary link. | Confirms HTML analysis |
| `downloads/screenshot-database-dictionaries.png` | Screenshot showing all four product sections; Enterprise has a "Database dictionary" download link, Office does not. | Confirms asymmetry |
| `downloads/screenshot-ehi-section-top.png` | Screenshot of page header and "Key Information About the Exported Data" introduction. | Context |
| `downloads/screenshot-page-top.png` | Screenshot of page navigation header. | Minimal value |
| `downloads/DD_Complete_EHI_20250627.pdf` (29.2 MB, 10,875 pages) | NextGen **Enterprise** EHR data dictionary — SQL Server database schema with ~2,097 tables. Title page explicitly reads "for NextGen® Enterprise." **Not applicable to NextGen Office** — different product, different technology stack, different database architecture. Downloaded for reference only. | Not applicable to Office |

## 3. Export Mechanics

Based on the documentation page, the export produces a **ZIP archive** containing:

1. **C-CDA Format** — XML files following the C-CDA specification
2. **CSV** — comma-separated text files with one or more fields per record
3. **Binary files** — images and PDFs
4. **HTML files** — purpose not described

- **Format**: Mixed (C-CDA XML + CSV + binary + HTML) in a ZIP archive
- **Mechanism**: Not documented. No instructions for how to trigger or perform the export.
- **Single-patient vs bulk**: Not documented. The phrase "EHI exports for patients" (singular context) suggests single-patient.
- **Access constraints or fees**: Not documented.

No export guide, user manual, API documentation, or workflow instructions are provided.

## 4. Export Content: What's In It

### The core problem: no data dictionary exists

The entire NextGen Office EHI export documentation consists of **85 words** describing four file types. There is:

- **No data dictionary** — zero tables, zero fields, zero schemas documented
- **No field definitions** — no column names, data types, value sets, or descriptions
- **No sample export data** — no example ZIP, CSV, or C-CDA files
- **No relationship documentation** — no foreign keys, no entity-relationship model
- **No export instructions** — no guide on how to trigger the export
- **No machine-readable schema** — no JSON schema, XSD, or DDL

The page promises "database dictionaries that define the schema of the EHI data exports for each of NextGen Healthcare's certified health IT products: NextGen® Enterprise EHR, NextGen® Office, and NextGen® Direct Messaging, and Mirth Connect." However, only Enterprise has an actual dictionary link. The Office section has only format descriptions.

### Vendor's own content organization

There is no vendor-provided content organization to present. The vendor does not enumerate any tables, entities, categories, or fields for NextGen Office.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### What can be inferred (but not confirmed)

The mention of **C-CDA** implies standard clinical summary data would be included (demographics, problems, medications, allergies, vitals, procedures, results, immunizations, clinical notes). However, C-CDA is a clinical document exchange standard — it does not cover billing, specialty-specific structured data, practice management, or patient portal interactions.

The mention of **CSV** files is potentially significant — CSV could carry structured data beyond what C-CDA supports (billing records, custom forms, specialty data). However, without any documentation of what CSV files are produced, their column headers, or their content, this is entirely speculative.

**Binary files** likely include scanned documents, images, and PDF attachments from the patient record.

**HTML files** are unexplained — they could be rendered clinical documents, reports, or patient portal content.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no structured documentation from which to assess coverage. The only information is that the export includes four file types. No categories, modules, or data domains are described. No entity names, field counts, or content descriptions are provided.

The contrast with the sibling product is stark: NextGen Enterprise has a 10,875-page data dictionary covering ~2,097 database tables. NextGen Office has 85 words and zero tables documented.

### 5b. Standardized domain coverage (top-down)

Because no data dictionary exists, coverage cannot be verified for any domain. The C-CDA component provides *probable* coverage of standard USCDI clinical domains, but even this is unconfirmed without sample data or documentation. The CSV component *could* cover additional domains, but there is zero evidence either way.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (probable) | C-CDA likely includes basic demographics | Product stores extensive demographics; C-CDA covers basics but depth unknown |
| Encounters / visits | ⚠️ Partial (probable) | C-CDA may include encounter data | Product stores scheduling, visit details; C-CDA coverage limited |
| Problems / conditions | ⚠️ Partial (probable) | C-CDA typically includes problem list | Standard C-CDA section; depth unknown |
| Medications / prescriptions | ⚠️ Partial (probable) | C-CDA typically includes medications | Product has full e-prescribing with EPCS; C-CDA covers basics |
| Allergies | ⚠️ Partial (probable) | C-CDA typically includes allergies | Standard C-CDA section |
| Immunizations | ⚠️ Partial (probable) | C-CDA may include immunizations | Product has registry integration; C-CDA may cover basics |
| Vitals | ⚠️ Partial (probable) | C-CDA typically includes vital signs | Standard C-CDA section |
| Lab results | ⚠️ Partial (probable) | C-CDA typically includes results | Product integrates with lab networks; depth unknown |
| Imaging / diagnostic reports | ⚠️ Partial (probable) | C-CDA may include imaging narratives | Depth unknown |
| Procedures | ⚠️ Partial (probable) | C-CDA typically includes procedures | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial (probable) | C-CDA includes notes; binary files may include scanned docs | Product generates AI SOAP notes, specialty templates; completeness unknown |
| Care plans / goals | ⚠️ Partial (probable) | C-CDA may include care plan section | Product has care management tools |
| Orders / referrals | ❌ Not confirmed | No evidence | Product has CPOE, referral management; no documentation of export |
| Insurance / coverage | ❌ Not confirmed | No evidence | Product stores insurance info, eligibility verification data; not in C-CDA |
| Claims / billing | ❌ Not confirmed | No evidence | Product has full billing/RCM with EDI claims, charge capture, denial mgmt; C-CDA does not cover billing |
| Payments | ❌ Not confirmed | No evidence | Product processes payments, A/R, collections; no documentation |
| Consents / directives | ❌ Not confirmed | No evidence | Product has digital intake forms; no documentation |
| Patient communications / portal messages | ❌ Not confirmed | No evidence | Product has patient portal with secure messaging; not in C-CDA |
| Specialty-specific (40+ specialties) | ❌ Not confirmed | No evidence | Product has specialty-specific clinical templates; not in standard C-CDA |

**Critical caveat**: Every "⚠️ Partial (probable)" rating above is based on the *assumption* that the C-CDA component follows standard C-CDA sections. This has not been verified with sample data or documentation. Every "❌ Not confirmed" domain is one where the CSV files *might* provide coverage, but there is zero documentation to support or refute this.

## 6. Documentation Quality

**Rating: Essentially absent**

The NextGen Office EHI export documentation is 85 words describing four file types. It is among the most minimal documentation possible while technically having *something* on the page.

- **Can a developer understand and use the export?** No. A developer receiving a ZIP archive of CSV files with no column headers documented, no schema, no sample data, and no relationship information would have to reverse-engineer the entire data model.
- **What's well-documented?** Nothing. The only documented facts are that the export is a ZIP containing four file types.
- **Machine-readable artifacts?** None. No JSON schema, XSD, DDL, or any other machine-readable format specification.
- **Human-readable documentation?** 85 words of prose.

The documentation fails the most basic test of utility: could someone who receives this export understand what they have? The answer is clearly no.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

Documentation is too thin to assess what the export actually contains. The 85-word description provides no field-level information, no entity enumeration, and no content specification. While the mention of CSV files alongside C-CDA *hints* that the export might go beyond standard clinical summaries, there is zero evidence to confirm this. The vendor's own page promises "database dictionaries that define the schema of the EHI data exports" for NextGen Office but delivers only a paragraph listing file types. The sibling product (Enterprise) has a 10,875-page data dictionary on the same page, making the absence for Office conspicuous and deliberate.

**Axis 2 — Export approach: Unclear/undetermined**

It is impossible to determine whether this is a purpose-built EHI export or a repackaged existing export. The presence of CSV files in addition to C-CDA suggests the vendor *may* have built something beyond a standard clinical exchange — CSV files would not be needed if the export were purely C-CDA. However, without any documentation of what the CSV files contain, this is speculation. The C-CDA component alone would be a repackaged clinical exchange export; if the CSV files carry billing, specialty, and administrative data with meaningful coverage, the export could be purpose-built. The documentation simply does not provide enough information to make this determination.

### Key Findings

1. **No data dictionary exists for NextGen Office.** The registered EHI documentation URL contains only 85 words describing four export file types (C-CDA, CSV, binary, HTML). No tables, fields, types, descriptions, schemas, or sample data are provided. This is verified from the HTML source and screenshot (`downloads/ehi-data-dictionary-page.html`, `downloads/screenshot-office-section.png`).

2. **The same page provides a 10,875-page data dictionary for sibling product NextGen Enterprise** (`downloads/DD_Complete_EHI_20250627.pdf`), documenting ~2,097 SQL Server tables. This demonstrates NextGen Healthcare is capable of producing detailed EHI documentation but chose not to for Office.

3. **The CSV component is a black box.** CSV files alongside C-CDA could indicate the export goes beyond clinical summaries, but without any documentation of CSV file names, column headers, or content, this cannot be evaluated. The entire assessment hinges on what these undocumented CSV files contain.

4. **No export instructions are provided.** There is no user guide, API documentation, or workflow description for how to trigger or perform the EHI export in NextGen Office. A patient or provider would not know how to request their data.

5. **The page copyright is © 2023**, and the Office section shows no evidence of updates since initial publication, while the Enterprise dictionary was updated June 27, 2025. This suggests the Office documentation has been neglected.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   ZIP archive (C-CDA XML, CSV, binary, HTML)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 19 confirmed (up to ~12 probable via C-CDA, unverified)
```

### Bottom Line

NextGen Office's EHI export documentation is functionally absent — 85 words listing file types with no data dictionary, no schema, no sample data, and no export instructions. While the export *may* include meaningful data via its undocumented CSV files, there is no way to evaluate coverage, completeness, or usability from what the vendor has published. A patient or developer receiving this export would have to reverse-engineer the entire data model with no guidance. This represents one of the weakest (b)(10) documentation efforts possible while technically having a page at the registered URL.
