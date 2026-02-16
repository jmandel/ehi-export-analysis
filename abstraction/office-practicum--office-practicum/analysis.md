# EHI Export Analysis: Office Practicum

**Product**: Office Practicum (Version 21)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.3048.Offi.21.02.1.221121

## 1. Product Context

Office Practicum (OP) is a pediatric-specialty EHR, practice management, and revenue cycle management platform developed by Connexin Software, Inc. It serves over 9,000 pediatricians across 48–49 states and is described as the only EHR "built by pediatricians for pediatricians."

The product is an end-to-end platform combining:

- **Clinical / EHR**: SOAP note-based documentation, pediatric growth charts (including specialty curves for Down Syndrome and preemie patients), VacLogic immunization forecasting, 175+ school/camp form templates, developmental assessments, behavioral health monitoring (PHQ-9, GAD-7), allergy tracking, medication management, clinical decision support
- **e-Prescribing**: EPCS support, Surescripts integration
- **Lab integration**: Electronic ordering, result receiving, in-house device connectivity
- **Practice management**: Scheduling, patient flow tracking, well-visit recalls, insurance eligibility verification
- **Billing & RCM**: Electronic superbills, claims processing, payment posting, denial tracking, clearinghouse integration, revenue analysis
- **Patient portal**: Secure messaging, self-registration, lab result access, prescription refill requests
- **Telehealth**: Video-based virtual care (via RemedyConnect acquisition)
- **Document management**: Scanning, bi-directional eFax, referral workflows

This is a feature-rich product that stores extensive clinical, billing, scheduling, and patient engagement data. A complete EHI export would need to cover demographics (with pediatric family/guardian relationships), clinical documentation, growth data, immunizations, behavioral health screenings, medications, allergies, labs, billing/claims, scanned documents, referrals, school/camp forms, insurance data, and patient communications.

## 2. Artifacts Reviewed

| # | Artifact | Type | Size | What It Tells Us | Value |
|---|---|---|---|---|---|
| 1 | `onc-certification-page.html` | HTML | 407 KB | Registered ONC certification URL. Contains the EHI export section: 3 paragraphs (~130 words) describing CSV export via built-in SQL query. No data dictionary, no downloadable files. | **Primary** |
| 2 | `onc-certification-info-disclosures.html` | HTML | 414 KB | Mandatory disclosures page with accordion sections. EHI export section text is **identical** to artifact #1. | Duplicate |
| 3 | `OP_RWT_Results_Report_2025.pdf` | PDF | 965 KB, 10 pages | 2025 Real World Testing Results. Page 7: EHI Export section reports 2,861 single-patient exports and 20 bulk exports across 5 practices in Q4 2025. No technical detail about export contents. | Supplementary |
| 4–7 | Screenshots (4 files) | PNG | 318–789 KB each | Visual captures of the HTML pages confirming the content. | Corroborative |

**Most informative**: Artifact #1 (the certification page HTML) — it contains 100% of the available EHI export documentation. **Least informative**: The screenshots, which simply visually confirm what the HTML source already shows.

All claims from the prior agent report about artifact contents were verified and found accurate. The PDF does produce text via `pdftotext` (contrary to the prior report's note about "image-based PDF"), though the output is minimal; visual inspection of rendered pages confirmed the content.

## 3. Export Mechanics

- **Format**: CSV (comma-separated values)
- **Mechanism**: Built-in SQL query accessible through the application's "Database Viewer" feature
  - Single-patient: A stored SQL query named "Single patient EHI export" — user runs it without developer assistance
  - Multi-patient: Described as "export all the data for a patient population" in CSV format
- **Single-patient**: Yes — explicitly documented
- **Bulk/multi-patient**: Yes — explicitly documented
- **Access constraints**: The documentation states the export can be performed "without developer assistance," implying it is a user-accessible feature within the application UI
- **Fees**: Not mentioned in any artifact

The reference to a "Database Viewer stored SQL query" suggests the export runs directly against the database, which *could* indicate comprehensive coverage — but without seeing the query definition or its output, this cannot be confirmed.

## 4. Export Content: What's In It

### What the documentation provides

The entire publicly available EHI export documentation consists of **three paragraphs totaling approximately 130 words** (verified by script; see `analysis/full-entity-inventory.json`). The complete text is:

> **Single Patient Export**
> Office Practicum allows a user to export electronic health information (EHI) for a single patient at any time via a Database Viewer stored SQL query built into OP named "Single patient EHI export" without developer assistance. The exported files are in .csv file format explained below
>
> **Multi-Patient Export**
> Office Practicum can export all the data for a patient population in .csv file format explained below:
>
> **CSV**
> A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values. Each line of the file is a data record. Each record consists of one or more fields, separated by commas. The use of the comma as a field separator is the source of the name for this file format.

### What is absent

- **No data dictionary**: Zero tables, entities, or fields are documented
- **No schema**: No entity-relationship diagrams, no table definitions, no field specifications
- **No sample data**: No example CSV files showing what the output looks like
- **No field-level documentation**: No column names, data types, value sets, or descriptions
- **No export instructions**: Beyond naming the SQL query, no step-by-step procedure
- **No content inventory**: No list of what data domains, tables, or categories are included
- **No downloadable files**: The entire documentation is inline HTML text
- **No machine-readable artifacts**: No JSON schemas, no XML definitions, no CSV templates

The third paragraph ("CSV") is entirely generic — it defines what a CSV file is. This contributes zero information about the export itself and reads as filler content.

### Vendor's own content organization

There is no vendor-provided content organization. No entities, tables, or fields are documented at all.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | 0 | 0 | N/A | N/A |

**Total entities documented: 0. Total fields documented: 0.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation provides **no information** about what data is included in the export. The only substantive claims are:

1. The export produces CSV files
2. It is driven by a "Database Viewer stored SQL query"
3. Both single-patient and multi-patient modes exist

The phrase "export electronic health information (EHI) for a single patient" and "export all the data for a patient population" implies comprehensive coverage, but without any table listing, field inventory, or sample data, there is zero evidence to evaluate this claim.

The Real World Testing report (page 7 of `OP_RWT_Results_Report_2025.pdf`) confirms the feature is functional — 2,861 single-patient exports and 20 bulk exports were performed across 5 practices in Q4 2025 — but adds no information about what data these exports contain.

### 5b. Standardized domain coverage (top-down)

Because no data dictionary, schema, or sample data exists, **no domain can be confirmed as covered**. Every domain is assessed based solely on the product's known capabilities (Section 1) and the absence of any evidence in the export documentation.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores demographics incl. family/guardian links; cannot confirm coverage |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounter data; cannot confirm coverage |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation | Product stores problem lists; cannot confirm coverage |
| Medications / prescriptions | ❓ Unknown | No documentation | Product stores medications and EPCS data; cannot confirm coverage |
| Allergies | ❓ Unknown | No documentation | Product stores allergy data; cannot confirm coverage |
| Immunizations | ❓ Unknown | No documentation | Product stores immunization records (VacLogic); cannot confirm coverage |
| Vitals | ❓ Unknown | No documentation | Product stores vitals and growth charts; cannot confirm coverage |
| Lab results | ❓ Unknown | No documentation | Product stores lab orders and results; cannot confirm coverage |
| Imaging / diagnostic reports | ❓ Unknown | No documentation | Product likely stores some diagnostic data; cannot confirm coverage |
| Procedures | ❓ Unknown | No documentation | Product stores procedure data; cannot confirm coverage |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores SOAP notes, visit notes, templates; cannot confirm coverage |
| Care plans / goals | ❓ Unknown | No documentation | Product may store care plans; cannot confirm coverage |
| Orders / referrals | ❓ Unknown | No documentation | Product stores referral workflows; cannot confirm coverage |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance and eligibility data; cannot confirm coverage |
| Claims / billing | ❓ Unknown | No documentation | Product has full billing/RCM capability; cannot confirm coverage |
| Payments | ❓ Unknown | No documentation | Product stores payment records; cannot confirm coverage |
| Patient communications / portal messages | ❓ Unknown | No documentation | Product has patient portal with secure messaging; cannot confirm coverage |
| Specialty-specific (pediatric) | ❓ Unknown | No documentation | Product stores growth charts, developmental assessments, school/camp forms, behavioral health screenings; cannot confirm coverage |

**It is impossible to assess coverage because the documentation does not describe what data is exported.** This is not a case of partial documentation — it is a near-total absence of documentation. The export *may* be comprehensive (the "Database Viewer stored SQL query" mechanism suggests it could pull from the full database), but there is no public evidence to support or refute this.

## 6. Documentation Quality

The export documentation is **critically deficient**:

- **Completeness**: The documentation describes the existence of the export and its output format (CSV). It provides no information about what data is exported — zero tables, zero fields, zero data types, zero value sets, zero relationships.
- **Developer usability**: A developer receiving CSV files from this export would have no documentation to work from. They would need to reverse-engineer the meaning of every column header. There are no schemas, no sample data, no field descriptions, no import guides.
- **Machine-readable artifacts**: None. No JSON schemas, XML definitions, CSV templates, or any other structured artifact.
- **Accessibility**: The documentation is inline HTML on two web pages (which contain identical text). No downloadable files exist.
- **Generic filler**: One-third of the documentation (the "CSV" paragraph) is a generic definition of the CSV format that provides zero information about the actual export. This reads as padding to fill the documentation section.

A developer tasked with integrating data from this export would be operating entirely blind. The documentation is insufficient to build an import, to validate data completeness, or even to understand what tables or fields to expect.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to assess what the export contains. The three paragraphs (~130 words) describe only that an export exists, it produces CSV files, and there are single-patient and multi-patient modes. No data dictionary, no schema, no sample data, no field definitions, and no content inventory are provided. While the export mechanism (a "Database Viewer stored SQL query") suggests it *may* provide database-level access, the complete absence of documentation makes it impossible to verify this or assess coverage.

### Key Findings

1. **Near-total documentation absence**: The entire publicly available EHI export documentation is ~130 words across 3 paragraphs. One-third of that text is a generic definition of CSV files. Zero tables, zero fields, and zero data types are documented. (Source: `onc-certification-page.html`, verified by `analysis/extract_ehi_documentation.py`)

2. **Export mechanism suggests potential**: The reference to a "Database Viewer stored SQL query built into OP" implies the export runs against the database directly, which *could* mean comprehensive data coverage. However, without the query definition or output schema being public, this remains unverifiable. (Source: `onc-certification-page.html`)

3. **Feature is actively used**: The 2025 RWT report documents 2,861 single-patient exports and 20 bulk exports across 5 practices in Q4 2025, confirming the feature exists and functions in production. (Source: `OP_RWT_Results_Report_2025.pdf`, page 7)

4. **No downloadable technical artifacts**: Unlike vendors who provide data dictionaries, schema documents, or sample files, Office Practicum provides zero downloadable artifacts related to the EHI export. All documentation is inline HTML text.

5. **Product is data-rich but export is undocumented**: Office Practicum stores extensive pediatric-specific data across clinical, billing, scheduling, and patient engagement domains. The gap between the product's data richness and the export documentation's emptiness is stark.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   CSV
Model type:      Unknown (likely native database via SQL query, but undocumented)
Entities:        0 documented
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes
Domains covered: 0 of 18 confirmable (documentation insufficient to assess any domain)
```

### Bottom Line

Office Practicum's EHI export documentation is among the most minimal possible while technically existing. The ~130 words of public documentation tell a reader only that the export exists and produces CSV files — nothing about what data is included, how it's structured, or how to interpret it. While the "Database Viewer stored SQL query" mechanism hints that the underlying export *may* be comprehensive, the complete absence of a data dictionary, schema, sample data, or content inventory means a patient, provider, or developer cannot determine what they would actually receive. The single biggest gap is the total lack of transparency about export contents.
