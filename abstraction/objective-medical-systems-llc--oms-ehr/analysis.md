# EHI Export Analysis: Objective Medical Systems, LLC

**Product**: OMS EHR (Version 6)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2086.OMSE.06.07.1.260108 (CHPL ID 11751)

## 1. Product Context

OMS EHR is a **cardiology-specific EHR with an integrated cardiovascular information system (CVIS)**, built by cardiologists for cardiologists. The vendor, based in Houma, Louisiana (~17 employees), serves mid-size to large cardiology practices including the Cardiovascular Institute of the South.

**Key capabilities relevant to export completeness:**

- **Core EHR**: Demographics, problem lists, medications, allergies, vitals, clinical notes, care plans, immunizations
- **Cardiovascular diagnostics (CVIS)**: 16 structured reporting modules covering echocardiography, EKG, stress testing, nuclear imaging, catheterization lab, vascular studies, and Holter monitoring — this is the product's core differentiator, with the vendor claiming "6,000+ data points per patient"
- **e-Prescribing**: Surescripts integration with formulary/benefits checking
- **C3 (Chronic Care Coordinator)**: Remote patient monitoring (RPM) via Bluetooth devices (blood pressure, heart rate), chronic care management (CCM), transitional care management (TCM)
- **Lab integration**: Lab results and scanned lab documents
- **Smart Forms**: Custom questionnaires/forms
- **Patient portal**: View-download-transmit capabilities
- **Revenue cycle**: Mentioned on vendor homepage; CPT and ICD coding support (IMO integration) — depth of billing functionality unclear
- **Referrals**: Certified for CMS50 (closing the referral loop)
- **AI features**: Diagnosis detection, clinical trial matching, patient no-show prediction

The product runs on Windows/SQL Server on-premises. It is certified for (b)(10) as of January 8, 2026.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHI-Export-Data-Format.pdf` (133 KB, 2 pages) | The **sole artifact**: a title page and a single table listing 9 export categories with their file formats. Created 2023-11-16 in Microsoft Word, never modified. Author: Anand Aravind. | **Minimally informative** — provides category names and output formats only; zero field-level detail |

No other artifacts were found. There is no data dictionary, no schema, no sample data, no export instructions, and no supplementary documentation on the vendor's website or disclosures page.

## 3. Export Mechanics

- **Format(s)**: Mixed — C-CDA XML/HTML, HTML documents, PDF scans, and undefined "discrete fields"
- **Mechanism**: Not documented. No instructions on how to initiate an export, whether via UI, API, or vendor-assisted process.
- **Single-patient vs bulk**: Not documented.
- **Access constraints or fees**: Not documented.

The documentation provides no information about how the export is triggered, delivered, or consumed. A user reading this PDF would not know how to request or receive an EHI export.

## 4. Export Content: What's In It

### What the documentation says

The entire data specification is a single table with 9 rows and 2 columns:

| Entity/Category | Export Format(s) | Fields Documented | Types Documented | Descriptions |
|---|---|---|---|---|
| CCDA | XML, HTML | 0 | No | No |
| Notes | HTML | 0 | No | No |
| C3 Notes | HTML | 0 | No | No |
| Labs | XML, HTML | 0 | No | No |
| Labs Scanned | PDF | 0 | No | No |
| Diagnostics | Discrete fields, PDF | 0 | No | No |
| Scanned documents | PDF | 0 | No | No |
| Smart Forms | HTML | 0 | No | No |
| Messages | Discrete fields | 0 | No | No |

**Totals: 9 categories, 0 fields documented, 0 descriptions, 0 type definitions.**

An additional note states: "Documents sourced from outside will be exported in the same format it was received."

### What the documentation doesn't say

- **No field names are defined for any category.** The term "discrete fields" appears for Diagnostics and Messages but is never defined — no field listing, no data types, no format specification (CSV? JSON? XML? proprietary?).
- **No data dictionary exists.** Not a single field in the product is documented.
- **No schema or format specification** for any export category.
- **No sample data or examples.**
- **No relationship documentation** between exported categories.
- **No value sets, code systems, or coded field documentation.**

### Vendor's own content organization

The vendor organizes their export into 9 "functionalities." The format breakdown:

| Format | Categories Using It |
|---|---|
| XML | CCDA, Labs |
| HTML | CCDA, Notes, C3 Notes, Labs, Smart Forms |
| PDF | Labs Scanned, Diagnostics, Scanned documents |
| "Discrete fields" (undefined) | Diagnostics, Messages |

The CCDA category likely maps to the standard C-CDA clinical summary (demographics, problems, medications, allergies, immunizations, vitals) — this is the existing clinical exchange surface, not a purpose-built EHI export.

The HTML exports (Notes, C3 Notes, Smart Forms) are rendered document exports that preserve readable content but may not preserve discrete structured data in a computably useful form.

The PDF exports (Labs Scanned, Scanned documents, Diagnostics) are image-level exports.

The "discrete fields" exports (Diagnostics, Messages) are the only categories that might contain structured data beyond C-CDA, but they are completely undocumented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes 9 export categories, none with any depth. The categories can be grouped:

- **Clinical summary (CCDA)**: 1 category — the standard C-CDA document, covering USCDI-scope data
- **Clinical notes**: 2 categories (Notes, C3 Notes) — HTML rendered documents
- **Lab data**: 2 categories (Labs as XML/HTML, Labs Scanned as PDF)
- **Diagnostics**: 1 category — "discrete fields" and PDF, with zero specification
- **Documents**: 1 category (Scanned documents as PDF)
- **Forms**: 1 category (Smart Forms as HTML)
- **Messaging**: 1 category (Messages as "discrete fields", undefined)

The richest category by potential is "Diagnostics" — for a cardiology CVIS with 16 structured reporting modules, "discrete fields" could contain echocardiography measurements, catheterization data, and other structured cardiovascular data. But without any field documentation, this is speculation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in CCDA XML, but not listed separately | C-CDA includes basic demographics; full record (contacts, preferences, employment) unknown |
| Encounters / visits | ⚠️ Partial | Not listed; may be implicit in Notes/CCDA | No dedicated encounter export; visit structure undocumented |
| Problems / conditions / diagnoses | ⚠️ Partial | Likely in CCDA XML | C-CDA scope only; ICD-10 coding detail unclear |
| Medications / prescriptions | ⚠️ Partial | Likely in CCDA XML | C-CDA scope only; e-prescribing detail (Surescripts data, formulary checks) likely missing |
| Allergies | ⚠️ Partial | Likely in CCDA XML | C-CDA scope only |
| Immunizations | ⚠️ Partial | Likely in CCDA XML | C-CDA scope only |
| Vitals | ⚠️ Partial | Likely in CCDA XML | C-CDA scope only; RPM device readings (C3 platform) not separately addressed |
| Lab results | ✅ Covered | "Labs" (XML, HTML) and "Labs Scanned" (PDF) | Two dedicated categories; likely adequate for lab data |
| Imaging / diagnostic reports | ⚠️ Partial | "Diagnostics" (Discrete fields, PDF) | Category exists but completely undocumented; unclear if all 16 CVIS modules are covered |
| Procedures | ❌ Not covered | No procedure-specific category | Product stores cath lab procedural data; not addressed in export |
| Clinical notes / documents | ✅ Covered | "Notes" (HTML), "C3 Notes" (HTML), "Scanned documents" (PDF) | Three categories cover notes and documents |
| Care plans / goals | ❌ Not covered | Not mentioned | Product likely stores care plans; not in export |
| Orders / referrals | ❌ Not covered | Not mentioned | Product certified for CMS50 (closing referral loop); referrals absent |
| Insurance / coverage | ❌ Not covered | Not mentioned | Unknown if product stores insurance data |
| Claims / billing | ❌ Not covered | Not mentioned | Product has revenue cycle and CPT/ICD coding; billing absent from export |
| Payments | ❌ Not covered | Not mentioned | N/A if billing is external |
| Consents / directives | ❌ Not covered | Not mentioned | May be in Smart Forms but unverifiable |
| Patient communications / portal | ⚠️ Partial | "Messages" (Discrete fields) | Category exists but undocumented; portal messages vs secure messaging unclear |
| Specialty — Cardiovascular diagnostics | ⚠️ Partial | "Diagnostics" (Discrete fields, PDF) | This is the product's **core differentiator** (16 CVIS modules, "6,000+ data points") yet it gets a single row with no field documentation — the most significant gap |
| Specialty — Remote patient monitoring | ⚠️ Partial | "C3 Notes" (HTML) may cover coordinator notes | RPM time-series data (BP, HR readings from Bluetooth devices) not addressed |
| Smart Forms / custom assessments | ⚠️ Partial | "Smart Forms" (HTML) | Category exists; HTML rendering may not preserve discrete form data |

**Summary**: Of 21 assessed domains, 2 appear covered, 11 are partial (meaning a category exists but documentation is too thin to confirm actual coverage), and 8 are not covered at all. Critically, the product's core specialty — cardiovascular diagnostic data — is only partially documented despite being the most data-rich area of the product.

## 6. Documentation Quality

**The documentation is functionally absent.** The entire specification is a 9-row, 2-column table on a single page. There is:

- ❌ No data dictionary
- ❌ No field names, types, or definitions for any export category
- ❌ No schema or machine-readable format specification
- ❌ No sample data or examples
- ❌ No export instructions or user guide
- ❌ No API specification
- ❌ No relationship documentation between exported categories
- ❌ No value sets or terminology references

**Could a developer build an import from this documentation?** No. A developer would know only that the export produces some combination of XML, HTML, PDF, and undefined "discrete fields" across 9 categories. They would have no specification for parsing any of it.

**Could a patient interpret the export?** A patient could read the HTML notes and PDF documents, but would have no context for the "discrete fields" exports and no specification to understand the CCDA XML.

The PDF was created in November 2023 using Microsoft Word and has never been updated, despite the product being certified in January 2026 — over 2 years later.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to determine actual export coverage. What's documented amounts to a C-CDA clinical summary plus rendered documents (HTML notes, PDF scans) and two undefined "discrete fields" exports. This is a category listing, not a data specification. For a product that claims "6,000+ data points per patient" and has 16 structured cardiovascular diagnostic modules, the export documentation lists 9 categories with 0 fields defined. Major product domains — billing/revenue cycle, procedures, care plans, referrals, RPM time-series data — are entirely absent from the documentation.

The CCDA component covers only USCDI-scope data (the clinical exchange floor). The HTML/PDF exports are document-level rather than data-level. The "discrete fields" exports for Diagnostics and Messages could contain meaningful structured data, but without any specification, this cannot be assessed.

**Axis 2 — Export approach: Repackaged existing export**

The export is structured around the C-CDA clinical summary (the existing (g)(10)/(b)(1) exchange surface) supplemented by rendered document exports (HTML, PDF). This is the pattern of a vendor assembling their existing document exchange capabilities — C-CDA generation, note rendering, PDF storage — and listing them as a (b)(10) export. The "discrete fields" for Diagnostics and Messages are the only potentially novel elements, but they are entirely undefined, suggesting they may not represent a deliberate purpose-built EHI export design.

Key signals:
- The CCDA category is listed first and is the only structured data export with a recognized standard
- The remaining categories are document-level exports (HTML, PDF) that mirror existing clinical exchange capabilities
- No native database export, no comprehensive schema, no evidence of mapping internal tables to export format
- The document predates certification by over 2 years and was never updated — suggesting minimal ongoing investment in (b)(10) compliance

### Key Findings

1. **The entire EHI export documentation is 9 rows in a table on a single page** — zero fields defined across all categories, making this one of the thinnest (b)(10) documentation artifacts possible (`downloads/EHI-Export-Data-Format.pdf`, page 2).

2. **The product's core differentiator — cardiovascular diagnostics — is barely documented**: 16 structured reporting modules covering echo, EKG, stress, cath lab, and more are collapsed into a single "Diagnostics" row with "Discrete fields, PDF" and no further specification.

3. **Major data domains are absent from the export**: billing/revenue cycle, procedures, care plans, referrals, insurance, and RPM time-series data are not mentioned despite the product storing this data.

4. **The export appears to be the vendor's existing clinical exchange surface repackaged**: CCDA for clinical summary, HTML for rendered notes, PDF for scans — these are standard document exchange capabilities, not a purpose-built EHI export.

5. **The documentation is 2+ years old and never updated**: Created November 2023, never modified, with certification obtained January 2026 — suggesting minimal investment in (b)(10) documentation.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML, HTML, PDF, undefined "discrete fields"
Entities:        9 (high-level categories only)
Fields:          0 (no field-level documentation)
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Unclear (not documented)
Domains covered: 2 of 21 assessed domains clearly covered; 11 partial/unverifiable
```

### Bottom Line

A patient or provider would receive a C-CDA clinical summary, rendered HTML notes, scanned PDFs, and undefined "discrete fields" — with no specification to interpret the structured data. The export documentation is a stub: it names 9 categories but defines zero fields, and it omits major data domains (billing, procedures, referrals, RPM data) that the product stores. For a cardiology CVIS that claims 6,000+ data points per patient, a 9-row table with no field definitions does not constitute meaningful (b)(10) compliance.
