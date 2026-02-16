# EHI Export Analysis: Strateq Health, Inc.

**Product**: StrateqEHR Version 5
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.3097.STRQ.01.00.1.220105

## 1. Product Context

StrateqEHR is a cloud-based Hospital Information System (HIS) targeting critical access hospitals, rural hospitals, and freestanding emergency rooms. It is developed by Strateq Health, Inc. (Plano, TX), a subsidiary of Malaysia-based Strateq Group. The product is certified across 30+ ONC criteria including (b)(10) EHI export.

StrateqEHR is marketed as a **comprehensive, fully integrated HIS** — not just an EHR module. It covers:

- **Clinical**: H&P, assessments, care plans, nursing documentation, dictation notes, operative notes via a "Dynamic Form Engine"; CPOE for medications, labs, radiology, nursing, and procedures; eMAR; medication reconciliation; ED tracking board
- **Revenue Cycle**: Charges, claims, remittance, eligibility checking, denial management, GL journal entries, patient statements (integrated with Waystar and 3M CRS)
- **Ancillary**: Pharmacy (FDB integration), perioperative scheduling and documentation, HIM (document scanning, deficiency tracking, ROI)
- **Patient Administration**: Registration, ADT, bed management, insurance verification, scheduling
- **Interoperability**: C-CDA, e-prescribing (SureScripts/NewCrop), FHIR API, immunization registry, syndromic surveillance

This is a product that stores substantial clinical, billing, operational, and administrative data. A credible (b)(10) export would need to cover well beyond clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Strateq-Export.pdf` | The **sole** EHI export documentation artifact. A single-page PDF (282 KB, A4, created 2023-12-06 from Word via "Print to PDF"). Contains 6 sentences totaling ~105 words. Three sentences define common file formats (ZIP, PDF, C-CDA); three describe the export. No data dictionary, no field definitions, no sample data, no export instructions. | **Primary but extremely thin** — this is the entire (b)(10) documentation |
| `product-research.md` | Research on StrateqEHR's capabilities, modules, and data domains. Used to establish baseline of what the product stores. | Useful for gap analysis |
| `chpl-metadata.json` | CHPL certification details including 30+ certified criteria. | Confirms product scope |
| `ehi-export-report.md` | Prior agent's collection report. Confirmed that no additional export documentation exists beyond the single PDF. The mandatory disclosures page links to the same PDF. | Confirmed completeness of collection |

## 3. Export Mechanics

- **Format**: ZIP archive containing per-encounter C-CDA documents (themselves in ZIP archives) and attached files (PDFs, images)
- **Mechanism**: Not documented. No instructions for how a user initiates the export, what parameters are available, or what the workflow looks like.
- **Single-patient vs bulk**: Not specified. The documentation says "the patient EHI export" (singular), suggesting single-patient, but this is not confirmed.
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### What the documentation says

The complete substantive content of the export documentation is three sentences:

1. "The patient EHI export contains data from the patient's chart."
2. "The export file itself is a zip file. It contains zip files of C-CDAs and other files attached to the patient's chart (e.g. PDF and images)"
3. "Information for each patient encounter is available C-CDA format in zip archive."

### What is NOT provided

- **No data dictionary**: Zero entities, zero fields, zero descriptions
- **No C-CDA template specification**: No indication of which C-CDA document types are generated (CCD, Discharge Summary, Progress Note, Consultation Note, etc.)
- **No C-CDA section listing**: No indication of which sections are populated (Problems, Medications, Allergies, Results, Vitals, Procedures, etc.)
- **No field-level documentation**: No listing of data elements within C-CDA sections or extensions
- **No sample data**: No example exports
- **No schema**: No machine-readable artifacts
- **No export instructions**: No UI screenshots, API documentation, or workflow description

### Vendor's own content organization

There is no vendor-provided content organization. The vendor does not enumerate any entities, tables, or fields. The entire documentation is format-level ("it's a ZIP of C-CDAs") with no content-level detail.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | 0 | 0 | N/A | N/A |

The full inventory is saved to `analysis/entity-inventory-full.json`. Since there is no data dictionary, it contains zero entities and zero fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no content-level documentation. The only information is:
- The export uses **C-CDA format** — a clinical document standard designed for health information exchange and transitions of care
- **Attached files** (PDFs, images) from the patient's chart are included

C-CDA is a standardized clinical summary format. At best, it covers a subset of clinical data: problems, medications, allergies, lab results, vitals, immunizations, procedures, clinical notes, and patient demographics. It does **not** naturally represent billing data, detailed order lifecycle data, eMAR records, ED tracking metrics, custom dynamic form data, HIM records, or revenue cycle information.

Without knowing which C-CDA templates and sections are populated, we cannot even confirm which clinical domains are covered.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA typically includes patient demographics in the header, but no vendor documentation confirms this | Product stores extensive registration data; C-CDA header would carry basics only |
| Encounters / visits | ⚠️ Partial | Documentation says "per encounter" C-CDAs; encounter context likely present as document metadata | Product has full ADT; C-CDA would capture encounter dates but not ADT workflow details |
| Problems / conditions | ⚠️ Partial | C-CDA standard includes Problems section, but no confirmation it's populated | Product stores problem lists; likely included if standard C-CDA sections are used |
| Medications / prescriptions | ⚠️ Partial | C-CDA standard includes Medications section | Product has extensive medication management, eMAR, reconciliation; C-CDA would carry summary only |
| Allergies | ⚠️ Partial | C-CDA standard includes Allergies section | Likely included in standard C-CDA |
| Immunizations | ⚠️ Partial | C-CDA standard includes Immunizations section | Product stores immunization data; likely included |
| Vitals | ⚠️ Partial | C-CDA standard includes Vital Signs section | Likely included in standard C-CDA |
| Lab results | ⚠️ Partial | C-CDA standard includes Results section | Product integrates with Aspyra CyberLAB; unclear what flows into StrateqEHR vs stays in LIS |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA can include Diagnostic Results | Product orders radiology via CPOE; results depend on integration |
| Procedures | ⚠️ Partial | C-CDA standard includes Procedures section | Product has perioperative module; C-CDA would carry procedure names, not full operative detail |
| Clinical notes / documents | ⚠️ Partial | C-CDA can carry note content; attached PDFs/images included | Product has H&P, nursing notes, dictation, operative notes via Dynamic Form Engine; unclear if structured form data survives C-CDA serialization |
| Care plans / goals | ⚠️ Partial | C-CDA can include Care Plan section | Product stores nursing care plans |
| Orders / referrals | ⚠️ Partial | C-CDA has limited order representation | Product has close-loop CPOE across medications, labs, radiology, nursing, procedures; order detail and lifecycle would be lost in C-CDA |
| Insurance / coverage | ❌ Not covered | No evidence; C-CDA does not naturally carry insurance data | Product stores insurance, pre-auth, eligibility data; **significant gap** |
| Claims / billing | ❌ Not covered | No evidence; C-CDA cannot represent billing data | Product has extensive revenue cycle (Waystar integration, charges, claims, remittance, denial management, GL entries); **major gap** |
| Payments | ❌ Not covered | No evidence | Product processes payments (credit card, check authorization, patient portal payments); **gap** |
| eMAR | ❌ Not covered | No evidence; C-CDA Medications section is a summary, not administration records | Product has eMAR; **gap** |
| ED tracking data | ❌ Not covered | No evidence; C-CDA cannot represent ESI levels, turnaround times, disposition tracking | Product has ED tracking board; **gap** |
| Scanned documents | ⚠️ Partial | Documentation mentions "PDFs and images" as attachments | Product has HIM document scanning; attachments may partially cover this |
| Dynamic Form Engine data | ❌ Not covered | No evidence structured form data is exported | Product's Dynamic Form Engine renders custom clinical forms; structured data from these forms likely lost in C-CDA serialization; **gap** |
| Perioperative data | ❌ Not covered | No evidence beyond what C-CDA Procedures section carries | Product has perioperative scheduling, checklists, documentation; **gap** |
| Implantable devices | ⚠️ Partial | C-CDA can carry UDI data | Product is certified for (a)(14) UDI tracking; unclear if included |
| Consents / directives | ❌ Not covered | No evidence | Unknown if product stores these |

**Summary**: Every clinical domain is rated ⚠️ Partial rather than ✅ Covered because the vendor provides no confirmation that any specific C-CDA section is populated. All non-clinical domains (billing, payments, insurance, eMAR, ED tracking, dynamic forms, perioperative data) are ❌ Not covered — C-CDA is structurally incapable of representing this data, and the vendor documents no supplementary export mechanism.

## 6. Documentation Quality

The export documentation is **functionally nonexistent**. Key failures:

- **105 words total**, of which ~45 are definitions of ZIP, PDF, and C-CDA file formats
- **Zero data elements** documented — no tables, no fields, no types, no descriptions
- **No export instructions** — a user cannot determine how to initiate an export
- **No C-CDA specifics** — which document types, which sections, which templates
- **No sample data** — no example exports to inspect
- **No schema or machine-readable artifacts**
- **Created 2023-12-06, never updated** — produced from a Word document ("Export.docx") printed to PDF

A developer could not build an import from this documentation. They would know to expect "a ZIP of C-CDAs" but would have no information about the content, structure, or completeness of those C-CDAs. They would need to obtain an actual export and reverse-engineer it.

This is among the thinnest (b)(10) documentation that can exist while technically having a document at the registered URL.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess coverage with any confidence. What we can determine structurally is that C-CDA is a clinical summary format that cannot represent billing, revenue cycle, eMAR, ED operations, dynamic form data, or perioperative detail — all data domains that StrateqEHR stores. Even within clinical domains, we cannot confirm which C-CDA sections are populated. The export appears to be a clinical summary format applied to a comprehensive HIS, with no supplementary mechanism for non-clinical data.

**Axis 2 — Export approach: Repackaged existing export**

The export is described as per-encounter C-CDA documents — this is the same format StrateqEHR uses for transitions of care (the product is certified for (b)(1) transitions of care and generates C-CDA documents as part of that workflow). There is no evidence of any purpose-built (b)(10) export mechanism: no additional data formats, no data dictionary mapping EHR-internal data to export fields, no coverage of billing or operational data. The telltale signs are all present: C-CDA format (designed for clinical exchange, not EHI export), no product-specific data dictionary, and no coverage of non-clinical domains despite the product having extensive revenue cycle capabilities.

### Key Findings

1. **The entire (b)(10) documentation is 6 sentences on one page**, three of which define common file formats. This is among the weakest export documentation reviewed — it provides essentially no actionable information about what data is exported.

2. **The export appears to be repackaged C-CDA** — the same clinical document format used for transitions of care, relabeled as (b)(10) EHI export. No supplementary export mechanism exists for the substantial non-clinical data StrateqEHR stores.

3. **Major data domains are structurally excluded**: StrateqEHR has an extensive revenue cycle module (charges, claims, remittance, eligibility, denial management, GL entries via Waystar). C-CDA cannot represent any of this. Similarly, eMAR records, ED tracking data, Dynamic Form Engine structured data, and perioperative detail cannot be expressed in C-CDA.

4. **No data dictionary exists** — zero entities, zero fields documented. A recipient of this export would have no way to know what's included or missing without obtaining and reverse-engineering an actual export file.

5. **The documentation has not been updated since December 2023**, suggesting no ongoing investment in the (b)(10) compliance effort.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (in ZIP archives), plus attached PDFs/images
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 confirmed of 17+ applicable domains (up to ~12 partial via C-CDA assumption)
```

### Bottom Line

StrateqEHR's (b)(10) export is a one-page PDF describing per-encounter C-CDA documents with no data dictionary, no field definitions, and no coverage of billing or operational data. For a comprehensive hospital information system with revenue cycle management, ED operations, pharmacy, perioperative care, and custom clinical forms, this export represents a compliance checkbox — not a genuine effort to make all electronic health information available to patients. The single biggest gap is the complete absence of documentation: without knowing what's in the C-CDAs or how to obtain the export, neither patients nor developers can assess or use it.
