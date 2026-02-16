# EHI Export Analysis: CloudCraft, LLC

**Product**: CloudCraft Software v9.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11150 (15.04.04.3071.Clou.09.01.1.221227)

## 1. Product Context

CloudCraft Software is a cloud-hosted EHR system built by NAIA Corporation (Birmingham, AL), described as "your all-in-one solution for electronic health records, practice management, billing, and human resources." It targets small ambulatory practices and FQHCs — its only confirmed customer is Goshen Medical Center, a 38-site FQHC in North Carolina. The product holds a broad ONC certification covering 36 criteria including CPOE (medications, lab, imaging), clinical decision support, demographics, family health history, implantable devices, transitions of care, clinical information reconciliation, FHIR API (g)(10), and EHI export (b)(10).

**What the product stores (relevant to export completeness):**
- **Clinical data**: Demographics, problem lists, medication lists, allergies, lab results (implied by CPOE lab certification), vitals, immunizations, procedures, clinical notes, care plans, family health history, implantable devices
- **Documents**: Scanned paper records, digital faxes, images, Word documents
- **Internal correspondence**: Tasks, notes
- **Billing**: Listed as a core module on the homepage; includes a sliding fee schedule module for FQHC financial workflows
- **Practice management**: Listed as a core module; details unspecified but typically includes scheduling and encounter management
- **HR**: Listed as a core module; no details available

The product's four advertised pillars — EHR, practice management, billing, and HR — set the baseline for what a comprehensive (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10.html` (6,525 bytes) | The complete EHI export documentation — a single static HTML page with ~150 words of prose content. Two sections: Provider Export (bulk workflow) and Patient Export Requests (FHIR DocumentReference). Lists 5 exported data types. | **Primary source** — this is the entirety of the documentation |
| `downloads/B10-page-screenshot.png` (150 KB) | Full-page screenshot showing the rendered workflow diagram with 5 icons | Confirms visual layout; no additional information beyond HTML |
| `downloads/certification-index-screenshot.png` (262 KB) | Screenshot of certification site landing page | Shows B10.html is not linked from main navigation |
| `downloads/styles.css` (34 KB) | CSS stylesheet for the page | Not informative for content analysis |
| `downloads/Images/` (7 files, ~63 KB total) | Workflow diagram icons and logo | Not informative for content analysis |

**Most informative**: `B10.html` — the only artifact with export-relevant content.
**Least informative**: CSS, images — purely presentational.

**Notable absence**: No data dictionary, no schema files, no sample data, no API documentation, no downloadable artifacts of any kind. The entire documentation corpus is one HTML page.

## 3. Export Mechanics

- **Format(s)**: C-CDA (USCDI v3) for structured clinical data; raw files (PDF, JPEG, GIF, TIF, DOC/DOCX) for documents; FHIR R4 DocumentReference for patient-facing access
- **Mechanism**:
  - *Provider pathway*: Admin Console bulk download — 5-step workflow (patient requests → admin console → select patients → download location → secure access)
  - *Patient pathway*: FHIR R4 DocumentReference resource via FHIR apps (MyLinks, Apple Health mentioned)
- **Single-patient vs bulk**: The provider pathway supports bulk export (multiple patients). The patient pathway appears to be single-patient via FHIR apps.
- **Access constraints**: No fees mentioned. The provider export requires Admin Console access. The FHIR endpoint (`fhirapitest.naiacorp.net`) is not publicly accessible. No API authentication details are documented.

## 4. Export Content: What's In It

The B10.html page lists exactly 5 categories of exported data:

1. **C-CDA USCDI v3** — structured clinical data conforming to the USCDI v3 standard
2. **PDF documents** — including scanned paper records and digital faxes
3. **Image files** — JPEG, GIF, TIF format
4. **Word documents** — DOC/DOCX format
5. **Internal correspondence** — tasks and notes

There is **no data dictionary**. Zero fields are documented. No entity definitions, no table structures, no column names, no data types, no value sets, no relationships, no schemas, no sample data.

The structured clinical data is described solely as "C-CDA USCDI v3," which by reference to the standard would include approximately 17 C-CDA sections covering USCDI data classes (demographics, allergies, problems, medications, labs, vitals, immunizations, procedures, clinical notes, care plans, goals, encounters, family history, implantable devices, health insurance, health concerns, and assessment/plan). However, no vendor-specific mapping, extensions, or customizations are documented.

### Vendor's own content organization

The vendor organizes content into exactly 5 bullet points with no further structure:

| Entity/Category | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA USCDI v3 | 0 | 0 | N/A | Bulk Data |
| PDF documents | 0 | 0 | N/A | Bulk Data |
| Image files | 0 | 0 | N/A | Bulk Data |
| Word documents | 0 | 0 | N/A | Bulk Data |
| Internal correspondence | 0 | 0 | N/A | Bulk Data |

Total entities with field-level documentation: **0**
Total fields documented: **0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes their export in a single flat list under "Bulk Data." There are no modules, sections, or categories beyond this list. The export consists of:

1. **A C-CDA document** covering USCDI v3 clinical data classes — this is the standard clinical summary format used for transitions of care and patient access, identical to what would be produced for (g)(10) FHIR API or (b)(1) transitions of care.

2. **Document attachments** in their original formats (PDF, images, Word) — this goes slightly beyond a pure C-CDA exchange by including non-structured documents like scanned records and faxes.

3. **Internal correspondence** (tasks, notes) — this is the one element that goes beyond typical clinical exchange, though no details are given about format or content.

The clinical data coverage is entirely bounded by what C-CDA USCDI v3 defines. There is no evidence of any data beyond the standard C-CDA sections. The document/attachment inclusion adds some breadth, but no billing, practice management, scheduling, financial, or HR data is mentioned anywhere.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Inferred via C-CDA USCDI v3 `recordTarget` | Only USCDI-scope fields; product likely stores more (e.g., sliding fee eligibility, FQHC-specific demographics) |
| Encounters / visits | ⚠️ Partial | Inferred via C-CDA Encounters Section | C-CDA encounter data is summary-level; practice management encounter details not included |
| Problems / conditions | ⚠️ Partial | Inferred via C-CDA Problem List Section | USCDI-scope only; no vendor-specific extensions documented |
| Medications / prescriptions | ⚠️ Partial | Inferred via C-CDA Medications Section | USCDI-scope only |
| Allergies | ⚠️ Partial | Inferred via C-CDA Allergies Section | USCDI-scope only |
| Immunizations | ⚠️ Partial | Inferred via C-CDA Immunizations Section | USCDI-scope only |
| Vitals | ⚠️ Partial | Inferred via C-CDA Vital Signs Section | USCDI-scope only |
| Lab results | ⚠️ Partial | Inferred via C-CDA Results Section | USCDI-scope only; product certified for CPOE lab, likely stores more detail |
| Imaging / diagnostic reports | ⚠️ Partial | Inferred via C-CDA; images explicitly listed | Product certified for CPOE imaging; C-CDA has limited imaging support |
| Procedures | ⚠️ Partial | Inferred via C-CDA Procedures Section | USCDI-scope only |
| Clinical notes / documents | ✅ Covered | C-CDA Notes Section + PDF/image/Word attachments | Best-covered domain due to explicit document inclusion |
| Care plans / goals | ⚠️ Partial | Inferred via C-CDA Goals/Assessment Section | USCDI-scope only |
| Orders / referrals | ⚠️ Partial | Inferred via C-CDA (limited order representation) | Product has CPOE for meds, labs, imaging — order details likely exceed C-CDA scope |
| Insurance / coverage | ⚠️ Partial | Inferred via C-CDA Payers Section | C-CDA payer section is minimal; FQHC sliding fee data not addressed |
| Claims / billing | ❌ Not covered | No billing entities in export | **Significant gap**: Product advertises billing as a core module; billing records are part of the designated record set |
| Payments | ❌ Not covered | No payment data mentioned | Gap if product processes payments (likely, given billing module) |
| Consents / directives | ❌ Not covered | Not mentioned | Unknown if product stores advance directives |
| Patient communications / portal | ❌ Not covered | Not mentioned | Product has a patient portal (ehrpatientportal.naiacorp.net); portal messages not in export |
| Internal correspondence | ✅ Covered | Explicitly listed: "tasks, notes" | One of the few items beyond standard clinical exchange |
| Sliding fee / FQHC financial | ❌ Not covered | Not mentioned | Product has a dedicated sliding fee module; this data is part of patient financial records |

**Summary**: Of 20 applicable domains, 2 are covered (clinical notes/documents, internal correspondence), 12 are partially covered (via C-CDA inference only), and 6 are not covered at all. The partial coverage is all inferred from the "C-CDA USCDI v3" label — no vendor-specific content detail is provided.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the most minimal possible while still having a publicly accessible page.

- **Total documentation**: 1 HTML page, ~150 words of prose, 6,525 bytes
- **Data dictionary**: None
- **Field-level documentation**: None — zero fields documented
- **Schema files**: None (no XSD, JSON Schema, OpenAPI)
- **Sample data**: None
- **API documentation**: The FHIR section mentions DocumentReference but provides no endpoints, authentication details, query parameters, or response examples
- **User guide**: 5-icon workflow diagram with one-line captions; no screenshots, no step-by-step instructions
- **Versioning**: No change history; page last modified December 2023

A developer could not build an import from this documentation. They would need to rely entirely on the C-CDA and FHIR R4 standards specifications, with no guidance on what CloudCraft-specific data elements are included or how the export is structured. The documentation contains a typo ("meme document types" for "MIME document types") and vague language ("one-time bulk export," "secure Download location") with no technical precision.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation describes a C-CDA USCDI v3 document plus file attachments. This is the standard clinical summary used for transitions of care — identical in scope to what would be produced for (g)(10) FHIR API access. While the inclusion of document attachments (PDFs, images, Word files) and internal correspondence goes marginally beyond pure USCDI clinical exchange, the export omits entire core modules the product advertises: billing, practice management, and HR. The documentation is too thin to determine whether any additional data beyond standard C-CDA content is included in the structured clinical export. There is no data dictionary to assess depth within covered domains.

**Axis 2 — Export approach: Repackaged existing export**

The telltale signs are clear:
1. The structured clinical data is described solely as "C-CDA USCDI v3" — the same format used for (b)(1) transitions of care and accessible via (g)(10) FHIR API
2. No product-specific data dictionary exists — the vendor relies entirely on the C-CDA standard specification
3. No vendor extensions, custom mappings, or proprietary data elements are documented
4. The patient pathway explicitly references FHIR R4 DocumentReference, which is the (g)(10) mechanism
5. The FHIR app connections listed (MyLinks, Apple Health) are standard (g)(10) consumer apps

The only elements that go beyond standard clinical exchange are document attachments and "internal correspondence," which appear to be added to the existing C-CDA/FHIR export rather than representing a purpose-built EHI export system.

### Key Findings

1. **The export is a repackaged C-CDA clinical summary**: The entire structured data export is described as "C-CDA USCDI v3" with no vendor-specific data dictionary, schema, or field documentation. This is functionally identical to the product's transitions-of-care export. (`downloads/B10.html`, lines 75–76)

2. **Billing data is entirely absent despite being a core product module**: CloudCraft advertises billing as one of its four main modules and has a sliding fee schedule system for FQHCs. No billing, claims, charges, payments, or financial data appear in the export documentation. (`downloads/B10.html` — billing not mentioned; `product-research.md` — billing listed as core module)

3. **Zero fields are documented**: The entire EHI export documentation is ~150 words on a single HTML page. There is no data dictionary, no schema, no sample data, and no field-level documentation of any kind. (`downloads/B10.html`, 6,525 bytes total including HTML markup)

4. **Document attachments provide some breadth beyond USCDI**: The explicit inclusion of PDFs, images, Word documents, and internal correspondence (tasks/notes) goes beyond a pure C-CDA exchange. This is the one area where the export exceeds the standard clinical summary. (`downloads/B10.html`, lines 77–81)

5. **Patient portal data is not exported**: Despite having a patient portal (confirmed at `ehrpatientportal.naiacorp.net`), portal messages and patient-submitted data are not mentioned in the export.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (USCDI v3) + raw document files (PDF, JPEG, GIF, TIF, DOC/DOCX)
Entities:        0 (no data dictionary; ~17 C-CDA sections inferred)
Fields:          0 (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (provider pathway supports multiple patients)
Domains covered: 2 of 20 applicable domains fully covered; 12 partial (C-CDA inference only)
```

### Bottom Line

CloudCraft's (b)(10) export is a repackaged C-CDA clinical summary with document attachments — it provides no data beyond what the vendor's existing transitions-of-care and FHIR API capabilities already deliver, except for file attachments and internal correspondence. The complete absence of a data dictionary (zero fields documented across ~150 words of total documentation) makes it impossible to verify what is actually exported, and the omission of billing data — a core product module — represents a significant gap in designated record set coverage. A patient or provider receiving this export would get a clinical summary and their scanned documents, but not their billing records, financial data, or any structured data beyond the USCDI floor.
