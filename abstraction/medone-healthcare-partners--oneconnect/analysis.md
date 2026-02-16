# EHI Export Analysis: MedOne Healthcare Partners

**Product**: OneConnect Version 0  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3182.Onec.00.00.1.231227 (CHPL ID 11426)

## 1. Product Context

OneConnect is a **custom clinical documentation tool** built by MedOne Healthcare Partners, a physician-owned hospital medicine practice in Columbus, Ohio (~100 physicians, 75+ APCs). It is **not a commercial EHR** sold to external customers — it is an internal tool used by MedOne's clinicians to document patient encounters across ~150 post-acute care facilities (skilled nursing, assisted living, long-term acute care, and rehab hospitals) in Ohio.

OneConnect is a **documentation overlay** designed to integrate with a facility's existing EMR, not a standalone full-featured EHR. Its certified capabilities are narrow: CPOE for medications (a)(1), demographics (a)(5), implantable device list (a)(14), transitions of care (b)(1), FHIR APIs (g)(10), and Direct messaging (h)(1). Notably **absent** from certification: medication lists (a)(6), allergy lists (a)(8), problem lists (a)(7), vital signs (a)(4), lab results (a)(2)/(a)(3), clinical decision support (a)(9), e-prescribing, and patient portal.

The product's core function is **streamlined clinical note creation** for providers rounding in post-acute settings. It uses e-prescribing via third-party RXNT. A related product (BOLT, by the same founder) includes billing/CPT code capture, but it is unclear whether OneConnect shares this capability.

Given its narrow scope as a documentation overlay for post-acute care, the designated record set for OneConnect would primarily include: clinical notes/documentation, patient demographics, medication orders, implantable device records, transitions of care documents, and any attached documents (PDFs, images).

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `EHI-Export.pdf` | 282 KB, 1 page | **The entire (b)(10) export documentation.** 111 words, 6 sentences. Describes export as ZIP of C-CDAs per encounter. No data dictionary, no schema, no sample data, no instructions. | **Primary but extremely thin** |
| `FHIR-API-Specifications.pdf` | 1.3 MB, 58 pages | (g)(10) FHIR API documentation. Smart on FHIR OAuth2, 16 US Core resource types, search/retrieve operations, terms of use. **Not (b)(10) documentation.** | Contextual — shows what FHIR API covers |
| `FHIR_Valid_URLs.json` | 2.2 KB | FHIR Bundle with Endpoint (pointing to `qafhir.medonehp.com:9443`) and Organization resource. Infrastructure metadata. | Minimal |
| `certifications-page-screenshot.png` | 367 KB | Screenshot of MedOne certifications/mandatory disclosures page at `medonehp.com/certifications`. Shows document links in footer. | Contextual |

The EHI Export PDF is the only artifact directly relevant to (b)(10). The FHIR API documentation provides context about the product's clinical data capabilities but documents a separate system ((g)(10) API, not the EHI export).

## 3. Export Mechanics

- **Format**: ZIP archive containing C-CDA documents, one per patient encounter
- **Mechanism**: Not documented. No instructions for how a user or administrator initiates the export. No UI screenshots, no API endpoint, no command-line tool described.
- **Single-patient vs bulk**: Not documented. The documentation says "the patient EHI export" (singular patient), suggesting single-patient export.
- **Access constraints or fees**: Not documented. MedOne's certifications page mentions no fees for EHI export specifically. The FHIR API terms of use mention API subscription agreements, but these apply to the (g)(10) API, not the (b)(10) export.
- **Completeness**: The documentation explicitly states the export is **incomplete**: "It contains zip files of C-CDAs for now and other files attached to the patient's chart will be added later (e.g. PDF and images)." This was written 2023-11-07 — over two years ago.

## 4. Export Content: What's In It

### What the documentation says

The entire content specification is one sentence: "The patient EHI export contains data from the patient's chart." The export delivers C-CDA documents per encounter.

**There is no data dictionary.** There is no schema. There is no sample data. There is no field-level documentation. There is no description of which C-CDA sections are populated, which templates are used, or what coded values appear.

### What can be inferred

C-CDA is a clinical summary standard. A standard C-CDA document may contain sections such as:
- Allergies & Intolerances
- Medications
- Problem List
- Procedures
- Results (lab/diagnostic)
- Vital Signs
- Immunizations
- Plan of Treatment
- Goals
- Social History
- Encounters
- Medical Equipment (implantable devices)
- Assessment
- Functional/Mental Status

However, **which of these sections OneConnect actually populates is unknown**. Given that OneConnect is not certified for allergy lists (a)(8), problem lists (a)(7), vital signs (a)(4), or lab results (a)(2)/(a)(3)), many of these standard C-CDA sections may be empty or absent.

The FHIR API documentation (separate from the EHI export) shows the system can serve: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Observation (labs, vitals, smoking status), Goal, Immunization, Medication, Procedure, and Provenance via FHIR. This suggests the underlying system stores these data types — but there is no documentation confirming the C-CDA export includes equivalent coverage.

### Vendor's own content organization

There is **no vendor-provided content organization**. The vendor provides no entities, tables, fields, categories, or any structured description of export content. The table below cannot be populated:

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes a single export type: **C-CDA documents per encounter, packaged in a ZIP archive**. There is no categorization, no module breakdown, no entity listing. The documentation is 111 words on a single page.

The vendor explicitly acknowledges incompleteness: additional file types (PDFs, images) are promised for future addition. The current export appears to be limited to whatever C-CDA sections the system populates for each encounter.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header includes patient demographics | C-CDA patient header has limited demographic fields vs. what an EHR stores |
| Encounters / visits | ⚠️ Partial | One C-CDA per encounter implies encounter data present | Encounter metadata likely in C-CDA header, but depth unknown |
| Problems / conditions | ❌ Not confirmed | No documentation; product not certified for (a)(7) | May or may not be in C-CDA; cannot determine |
| Medications / prescriptions | ⚠️ Partial | Certified for CPOE (a)(1); C-CDA has medication section | Medication orders likely present; e-prescribing data from RXNT integration unclear |
| Allergies | ❌ Not confirmed | Not certified for (a)(8); C-CDA has allergy section | Section may exist but may be empty; cannot determine |
| Immunizations | ❌ Not confirmed | FHIR API supports Immunization; C-CDA has section | Not confirmed for export |
| Vitals | ❌ Not confirmed | Not certified for (a)(4); FHIR API supports Vital Signs | Section may exist but product may not collect vitals |
| Lab results | ❌ Not confirmed | Not certified for (a)(2)/(a)(3); FHIR API supports Lab Observation | Product likely doesn't generate lab results (post-acute documentation overlay) |
| Imaging / diagnostic reports | ❌ Not confirmed | FHIR API has DiagnosticReport | Not confirmed for export |
| Procedures | ❌ Not confirmed | FHIR API supports Procedure | Not confirmed for export |
| Clinical notes / documents | ⚠️ Partial | Core product function is documentation; C-CDA likely contains notes | Clinical notes are OneConnect's primary data — C-CDA's narrative sections may capture them, but custom templates/shorthand formats may not translate faithfully |
| Care plans / goals | ❌ Not confirmed | FHIR API supports CarePlan, Goal | Not confirmed for export |
| Orders / referrals | ❌ Not confirmed | CPOE certified but order details in export unknown | Cannot determine |
| Insurance / coverage | ❌ Not covered | No evidence | N/A — product likely doesn't manage insurance |
| Claims / billing | ❌ Not covered | No evidence; C-CDA has no billing sections | Related BOLT product may do billing; unclear if OneConnect does. If it does, significant gap. |
| Payments | ❌ Not covered | No evidence | N/A — product likely doesn't process payments |
| Consents / directives | ❌ Not covered | No evidence | Unclear if product stores consents |
| Patient communications | ❌ Not covered | No patient portal (e)(1) not certified | N/A — no portal functionality |
| Attached documents (PDFs, images) | ❌ Not covered (planned) | Documentation explicitly says "will be added later" | Gap — vendor acknowledges these are part of the patient chart but are not currently exported |

## 6. Documentation Quality

**Extremely poor — among the worst possible for a certified product.**

- The entire EHI export documentation is **111 words on 1 page** (6 sentences).
- Three of those sentences define what ZIP, PDF, and C-CDA are — adding no product-specific value.
- **No data dictionary** of any kind.
- **No schema** or machine-readable artifacts.
- **No sample data** or example exports.
- **No instructions** for how to perform or request an export.
- **No description** of which C-CDA sections are populated or what templates are used.
- **No field-level detail** whatsoever.

A developer could not build an import from this documentation. They would receive a ZIP of C-CDA files with no guidance on what sections to expect, what coded values appear, or how the data maps to OneConnect's internal model.

The documentation explicitly acknowledges the export is incomplete ("will be added later"), written in November 2023 — over two years before this analysis. There is no evidence this promise was fulfilled.

By contrast, the (g)(10) FHIR API documentation is 58 pages with OAuth2 flows, resource examples, search parameters, and error handling. The disparity between the (g)(10) and (b)(10) documentation quality is stark: the FHIR API documentation is functional; the EHI export documentation is a compliance placeholder.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The vendor provides no data dictionary, no schema, no sample data, and no description of what C-CDA sections are populated. The export is explicitly acknowledged as incomplete ("other files will be added later"). Even if the C-CDA documents contain all standard sections, C-CDA is structurally incapable of representing the full designated record set (e.g., custom documentation templates, billing codes if applicable, order metadata). The 111-word document reads as the absolute minimum compliance artifact — a statement that an export exists, not a documentation of what it contains.

**Axis 2 — Export approach: Repackaged existing export**

The export is C-CDA documents per encounter — the same format used for transitions of care (b)(1), which OneConnect is separately certified for. The FHIR API documentation shows the system already supports C-CDA retrieval via the "Complete Patient Summary (CCDA)" endpoint. The (b)(10) export appears to be a repackaging of these existing C-CDA documents into a ZIP archive, with no additional data beyond what the transitions of care / FHIR API already provides. There is no vendor-specific data dictionary, no additional data domains beyond C-CDA's standard clinical sections, and no evidence of any purpose-built export infrastructure.

### Key Findings

1. **The EHI export documentation is 111 words on a single page** — one of the thinnest (b)(10) documents possible. It defines file formats (ZIP, PDF, C-CDA) but provides zero product-specific information about what data is exported. (`EHI-Export.pdf`)

2. **The export is explicitly incomplete.** The documentation states "other files attached to the patient's chart will be added later (e.g. PDF and images)." This was written November 2023; there is no evidence the export has been updated since. (`EHI-Export.pdf`)

3. **The export is C-CDA per encounter** — the same format used for transitions of care (b)(1). This is a repackaged clinical exchange export, not a purpose-built EHI export. C-CDA cannot represent billing data, custom form data, or the full depth of the system's internal data model.

4. **Stark contrast between (g)(10) and (b)(10) documentation.** The FHIR API has 58 pages of detailed documentation with examples; the EHI export has 1 page with no detail. This suggests the (b)(10) requirement was treated as a compliance checkbox. (`FHIR-API-Specifications.pdf` vs `EHI-Export.pdf`)

5. **Mitigating context:** OneConnect is a narrow-scope documentation overlay used internally by a single physician practice, not a commercial EHR. Its designated record set is likely smaller than a full-featured EHR's. However, even for a focused product, the documentation is inadequate — a recipient of the export would have no way to understand or use the data without reverse-engineering the C-CDA files.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (ZIP archive, one per encounter)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (documentation says "patient EHI export" — implies single-patient)
Domains covered: 0 confirmed of ~8 applicable domains (demographics, encounters, medications, notes, devices, orders, care plans, attached documents)
```

### Bottom Line

OneConnect's (b)(10) EHI export documentation is a 111-word, single-page PDF that describes a ZIP of C-CDA files per encounter with no data dictionary, no schema, no sample data, and an explicit admission of incompleteness. This is a repackaged transitions-of-care export relabeled as (b)(10), with documentation that is a compliance placeholder rather than a usable specification. The single biggest gap is the complete absence of any structured description of what data is actually exported — a patient or provider receiving this export would have no way to verify its completeness or interpret its contents beyond standard C-CDA parsing.
