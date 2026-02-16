# EHI Export Analysis: Systemedx Inc

**Product**: Systemedx Clinical Navigator  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2857.Syst.24.02.1.241126 (CHPL ID 11536)

## 1. Product Context

Systemedx Clinical Navigator is an all-in-one ambulatory EHR and practice management system from a small Alabama-based vendor (11–50 employees). It targets ambulatory physician practices, with a notable presence in orthopedic and sports medicine practices.

The product is a single integrated platform combining:

- **EHR / Clinical Documentation**: AI-assisted office visits ("AI Office Visit"), one-click ordering ("Touch Orders"), medication management with PDMP/EPCS, drug interaction checking, customizable templates and workflows
- **Practice Management**: Scheduling, patient registration, AI-assisted coding (CPT/ICD), claims submission, auto-posting remittances, eligibility verification, claim scrubbing, financial dashboards
- **Patient Portal**: Self-registration, appointment requests, medication refills, secure messaging, bill pay, clinical summaries
- **Surgical Pathways**: Surgical case tracking, AI-driven billing recovery ("rogue surgery detection"), automated CPT suggestion, pre/post-op workflow management, mobile integration
- **Quality Reporting**: MIPS/QPP measure calculation and submission
- **Interfaces**: HL7 lab interfaces (LabCorp, Quest, hospitals), imaging, PT, DME, dictation integrations
- **FHIR API**: OAuth 2.0 API via "Systemedx XNet" for (g)(10) compliance

The product is certified for 37 ONC criteria, a broad footprint for a small vendor. The data the product stores spans demographics, encounters, medications, problems, labs, allergies, vitals, immunizations, orders, billing/claims, surgical case data, portal messages, documents, quality measures, and public health reporting — all relevant to assessing export completeness.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `dataExport.html` (19,629 bytes) | The sole (b)(10) export documentation page. A static HTML page with ~236 words of substantive content describing the CDAEXPORT module, three export modes, and the output format (CDA XML + HTML + PDF). Contains zero field-level detail, no data dictionary, no schema, no sample data, no download links. Last modified May 2022 per HTTP headers. | **Primary source but extremely thin** |
| `dataExport-screenshot.png` (752 KB) | Full-page screenshot of the export documentation page, confirming the page content visually. | Confirmatory |
| `Mandatory-Disclosures-2022.pdf` (772 KB, 2 pages) | ONC cost transparency disclosures listing fees for e-prescribing, patient portal, lab interfaces, API access ($10,000/year/app). Does not mention the (b)(10) data export module or any associated costs. | **No export-relevant content** |

**Most informative**: `dataExport.html` — but it provides only a high-level description of how to trigger the export, not what it contains.  
**Least informative**: The mandatory disclosures PDF, which is unrelated to export content.

No data dictionary, schema, sample export files, or field-level documentation exists in any artifact.

## 3. Export Mechanics

- **Format**: CDA XML files + human-readable HTML copies ("CDA.html") + PDF chart documents
- **Mechanism**: UI-based — accessed via a job stream called "CDAEXPORT" within the application, appearing as "Data Export"
- **Patient scope**:
  - All Patients (bulk, with date range filter and output directory selection)
  - Select Patients (subset by manual selection or appointment date range)
  - Single Patient
- **Options**: Configurable date range, directory selection, checkboxes to include chart documents and human-readable HTML
- **Output structure**: Patient folders named `LastName_FirstName_DOB_PatientID`, with a "Documents" subfolder organized by document type
- **Access constraints**: No fees documented for the export module (the mandatory disclosures PDF does not mention it)
- **Bulk capability**: Yes — the "All Patients" mode supports bulk export

## 4. Export Content: What's In It

### What the documentation says

The export documentation describes exactly four types of content:

1. **CDA XML files** containing "patient demographics and distinct chart data (medications, problems, etc.)"
2. **CDA.html files** — human-readable HTML versions of the CDA documents
3. **PDF documents** — patient chart documents organized by document type in a "Documents" folder
4. **Folder structure** — patient-level organization by name, DOB, and patient ID

### What is NOT documented

- Which CDA template or standard is used (C-CDA R2.1? Custom CDA? Proprietary XML?)
- What "distinct chart data" means — which specific data elements beyond the parenthetical examples of "medications, problems, etc."
- What CDA sections are included (allergies? vitals? immunizations? procedures? results?)
- What "document types" exist in the Documents folder
- What fields are in each CDA section
- Data types, value sets, coded terminologies
- Relationships between records
- Whether billing, claims, surgical pathway, insurance, or practice management data is included

### Vendor's own content organization

There is no data dictionary, no entity listing, and no field-level documentation. The vendor's "organization" consists of three bullet points of prose. There are zero entities and zero fields documented:

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

The only concrete data concepts mentioned are "patient demographics," "medications," "problems," and "chart documents (PDF)." The phrase "etc." is the vendor's sole acknowledgment that other data may exist in the export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes one export mechanism producing two output types:

1. **CDA XML**: Contains "patient demographics and distinct chart data." The phrase "distinct chart data" is undefined. If this follows C-CDA conventions, it likely includes standard clinical summary sections (allergies, medications, problems, procedures, results, vital signs, immunizations). However, this is inference — the vendor does not enumerate any sections.

2. **PDF chart documents**: Unstructured documents from the patient chart, organized by document type. Document types are not listed.

The documentation is so sparse that no meaningful depth assessment is possible. There is no evidence of any coverage beyond the three explicitly named data concepts (demographics, medications, problems) and PDF documents.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Mentioned: "patient demographics" in CDA XML | Mentioned but no field-level detail; product stores registration data including insurance — unclear what's included |
| Encounters / visits | ❌ Not covered | Not mentioned in documentation | Product stores encounter documentation; likely in CDA but not confirmed |
| Problems / conditions | ⚠️ Partial | Mentioned parenthetically: "problems" | Listed as example but no detail on fields or coding |
| Medications / prescriptions | ⚠️ Partial | Mentioned parenthetically: "medications" | Listed as example but no detail; product has PDMP/EPCS — unclear if that data is included |
| Allergies | ❌ Not covered | Not mentioned | Product is certified for (a)(8) medication allergy list; likely in CDA but not documented |
| Immunizations | ❌ Not covered | Not mentioned | Product is certified for (f)(1) immunization registry; not mentioned in export |
| Vitals | ❌ Not covered | Not mentioned | Implied by clinical certification criteria; not mentioned in export |
| Lab results | ❌ Not covered | Not mentioned | Product has HL7 lab interfaces (LabCorp, Quest); not mentioned in export |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned | Product has imaging interfaces; not mentioned in export |
| Procedures | ❌ Not covered | Not mentioned | Product is certified for procedure documentation; not mentioned |
| Clinical notes / documents | ⚠️ Partial | PDF chart documents exported by document type | Documents included as PDFs; unstructured, no metadata documented |
| Care plans / goals | ❌ Not covered | Not mentioned | Not mentioned; may or may not be in CDA |
| Orders / referrals | ❌ Not covered | Not mentioned | Product has "Touch Orders" feature; not mentioned in export |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product stores insurance/enrollment data; not mentioned |
| Claims / billing | ❌ Not covered | Not mentioned | **Significant gap**: Product has full practice management with AI-assisted coding, claims submission, remittance posting. No mention of billing data in export |
| Payments | ❌ Not covered | Not mentioned | Product handles bill pay and statements; not mentioned |
| Consents / directives | ❌ Not covered | Not mentioned | Not mentioned |
| Patient communications | ❌ Not covered | Not mentioned | Product has portal secure messaging; not mentioned |
| Surgical pathways (specialty) | ❌ Not covered | Not mentioned | **Significant gap**: Product's differentiating feature with case tracking, billing recovery, pre/post-op workflows. Entirely absent from export documentation |

**Key gaps**: The product's two most distinctive capabilities — **practice management/billing** and **surgical pathways** — have zero representation in the export documentation. These are core data domains squarely within the designated record set.

Many clinical domains (labs, allergies, vitals, immunizations) are "not mentioned" but might be present if the CDA follows standard C-CDA conventions. However, the vendor does not confirm this, and the documentation provides no basis for assuming any specific CDA sections are included.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **Total documentation**: ~236 words of prose on a single HTML page — shorter than a typical patient discharge instruction
- **Data dictionary**: None
- **Schema/specification**: None — no XSD, no JSON Schema, no CDA template identification
- **Field-level detail**: Zero fields documented across all artifacts
- **Sample data**: None
- **Value sets/terminologies**: None
- **Relationships**: None
- **Machine-readable artifacts**: None
- **Last updated**: May 2022 (per HTTP headers), predating the November 2024 certification by over 2 years
- **Developer usability**: A developer could not build an import from this documentation alone. They would need to obtain a sample export and reverse-engineer the CDA structure, with no guarantee of understanding vendor-specific content.

The documentation describes only *how to trigger* the export (three modes, directory selection, checkboxes). It does not describe *what the export contains* at any level of detail beyond three parenthetical examples.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. Only three data concepts are explicitly named (demographics, medications, problems), plus PDF documents. The product stores data across at least 15 clinical and administrative domains — billing/claims, surgical pathways, lab results, orders, portal messages, insurance, immunizations, and more. There is no evidence any of these are in the export. The CDA format inherently limits what can be exported (CDA does not naturally carry billing, claims, or surgical pathway data). The "etc." in "medications, problems, etc." is not a substitute for documentation.

**Axis 2 — Export approach: Repackaged existing export**

The export is clearly the vendor's existing CDA clinical summary generation relabeled as (b)(10). Key evidence:

1. The module is called "CDAEXPORT" — it's a CDA export, not an EHI export
2. The output is CDA XML + HTML + PDF — standard clinical document exchange formats, not a comprehensive data dump
3. CDA is a clinical summary format that cannot carry billing, claims, surgical pathway, or practice management data
4. The documentation mentions "distinct chart data" (a clinical summary concept) rather than "all electronic health information"
5. No billing, insurance, claims, surgical pathway, portal message, or administrative data is mentioned
6. The page was last modified in May 2022, likely predating serious (b)(10) compliance effort
7. The vendor has separate (g)(10) FHIR API documentation under `/API/` — the (b)(10) export is a different, simpler mechanism that covers no more (and likely less) than the FHIR API

This is a clinical summary export — likely a C-CDA or similar CDA document — that was pointed at to satisfy the (b)(10) certification checkbox. There is no evidence of a purpose-built effort to export all electronic health information.

### Key Findings

1. **Documentation is a stub**: The entire (b)(10) export documentation is ~236 words with zero field-level detail, no data dictionary, no schema, and no sample data. This is among the thinnest export documentation possible (`dataExport.html`).

2. **Export is CDA-based clinical summary**: The "CDAEXPORT" module produces CDA XML documents — a clinical document exchange format that is structurally incapable of carrying billing, claims, or operational data. This is a repackaged clinical summary, not a comprehensive EHI export.

3. **Major data domains missing**: The product's practice management module (scheduling, billing, claims, remittances, eligibility) and surgical pathways module (case tracking, billing recovery, pre/post-op workflows) — both core product capabilities — have no representation in the export.

4. **No costs disclosed**: The mandatory disclosures document lists fees for e-prescribing, patient portal, lab interfaces, and API access, but does not mention the (b)(10) export — suggesting it may not be a separately priced feature, or it was overlooked in disclosure.

5. **Unchanged since 2022**: The export documentation page has not been modified since May 2022, over two years before the November 2024 certification date, suggesting no substantive update was made for certification.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   CDA XML + HTML + PDF
Entities:        N/A (no data dictionary)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (All Patients mode)
Domains covered: 3 of 18 applicable domains mentioned (demographics, medications, problems) — none confirmed with detail
```

### Bottom Line

A patient or provider requesting their data from Systemedx Clinical Navigator would receive CDA XML documents and PDF chart documents, but there is no way to determine from the documentation what those documents actually contain. The export almost certainly excludes billing/claims data, surgical pathway data, and other practice management records that are part of the designated record set. This is a clinical summary export rebranded as (b)(10), with the thinnest possible documentation — a compliance checkbox, not a genuine EHI export effort.
