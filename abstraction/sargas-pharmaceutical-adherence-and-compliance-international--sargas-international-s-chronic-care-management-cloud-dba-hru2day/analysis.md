# EHI Export Analysis: Sargas Pharmaceutical Adherence and Compliance International

**Product**: Sargas International's Chronic Care Management Cloud dba hru2day  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.05.05.2306.SPAC.01.00.0.211014 (CHPL #10702)

## 1. Product Context

Sargas International's Chronic Care Management Cloud (branded "hru2day") is a **cloud-based chronic care management platform** — not a full EHR. It received ONC Modular EHR certification in October 2021. The product serves physician practices, hospitals, ACOs, and FQHCs, primarily managing Medicare patients with chronic conditions under CMS CCM (CPT 99490 etc.), PCM, and RPM programs. SPAC International also operates a 24/7 clinical call center that performs care coordination services on behalf of contracting practices.

**Key data the product stores** (relevant to export completeness):

- **Care plans**: Comprehensive, structured care plans addressing physical, mental, cognitive, psychosocial, functional, and environmental domains — the product's core function
- **Care coordination logs**: 200,000+ logged interactions documenting CCM services (≥20 min/month per patient)
- **RPM device data**: Physiological readings from glucose monitors, BP cuffs, pulse oximeters, weight scales, heart rate monitors
- **Medication adherence records**: The company's founding use case — tracking adherence, side effects, and drug interactions for cancer/chronic disease patients
- **Patient demographics, problems, medications, allergies**: Standard clinical data (certified for (a)(1)–(a)(3), (a)(5))
- **Secure messages**: Communication between patients, care teams, and providers
- **CCM/PCM/RPM time tracking**: Service documentation supporting Medicare billing (CPT-linked time records)
- **Patient consent records**: Required for CCM billing enrollment

The product's data footprint is specialized but deep in its niche. It is **not** a point-of-care EHR — it supplements practices' existing EHRs with CCM/RPM/MTM capabilities.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/SPAC-Export.pdf` | 1-page PDF (379,759 bytes, 109 words). The **entire** EHI export documentation. Describes the export as a ZIP containing per-encounter C-CDA XML files and PDF chart attachments. No data dictionary, no field definitions, no sample data, no export instructions. | **Primary artifact** — extremely thin |
| `downloads/screenshot-certification-page.png` | Screenshot of vendor's Certified EHR Technology webpage. Contains certification boilerplate only; no additional export documentation. | Minimal |
| `product-research.md` | Prior research on the product's capabilities and data model. | Useful for context (Section 1) |
| `ehi-export-report.md` | Prior agent's collection narrative. Confirmed: no additional documentation found on vendor site despite checking ~100 PDFs in the `/pdf/` directory, the mandatory disclosures page, and common alternative URL paths. | Confirmed no missed artifacts |

**Verification of prior report claims**: The prior report stated the PDF is 1 page with 6 sentences. Verified: 1 page, 109 words. The text extraction matches the rendered PDF exactly (confirmed via `pdftoppm` rendering). The claim about ~100 PDFs in the vendor's `/pdf/` directory and the absence of additional EHI documentation was not independently re-verified via web access, but is consistent with the artifact set.

## 3. Export Mechanics

- **Format**: ZIP archive containing nested ZIP files of C-CDA XML documents and PDF attachments
- **Mechanism**: Not documented. The PDF provides no instructions for initiating an export — no UI screenshots, no API endpoint, no workflow description.
- **Single-patient vs bulk**: Not documented. The language ("the patient EHI export") suggests single-patient, but this is inference.
- **Access constraints or fees**: Not documented.

The documentation says nothing about who can initiate the export, how long it takes, whether it requires vendor assistance, or whether there are any costs.

## 4. Export Content: What's In It

### What the documentation says

The entire documentation consists of 6 substantive sentences (109 words total). Verbatim:

1. "The patient EHI export contains data from the patient's chart."
2. "Multiple file formats are used to store this information."
3. "ZIP is an archive file format."
4. "PDF or Portable Document Format is a file format that is used to present text or image based documents."
5. "C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange."
6. "The export file itself is a zip file. It contains zip files of C-CDAs and PDF files attached to the patient's chart (machine readable PDF)"
7. "Information for each patient encounter is available C-CDA format in zip archive."

Three of these sentences (3–5) simply define file format acronyms. The remaining sentences describe the export structure at the highest possible level: it's a ZIP of C-CDAs and PDFs.

### What is NOT documented

- **Zero entities/tables** are described
- **Zero fields** are described
- **Zero C-CDA sections** are specified — it is unknown which of the ~60+ possible C-CDA sections are populated
- **Zero C-CDA templates or profiles** are referenced
- **No data dictionary** exists
- **No schema** or machine-readable specification exists
- **No sample data** is provided
- **No value sets, code systems, or terminologies** are specified
- **No relationship or foreign key documentation** exists

### Vendor's own content organization

There is no vendor-defined content organization. The documentation does not categorize, enumerate, or describe any data elements.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### What can be inferred

Based on the export using C-CDA format, the export likely contains standard C-CDA sections (demographics, problems, medications, allergies, possibly care plans), but this is inference from the format choice, not from the vendor's documentation. The product's most distinctive data — RPM device readings, care coordination logs, medication adherence tracking, CCM time records — has no standard C-CDA representation and is likely absent from the export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no content categorization**. The documentation describes only a container format (ZIP) and two content formats (C-CDA, PDF) without specifying what data populates either format. There is no way to assess coverage depth from the documentation alone.

The only substantive claim is: "The patient EHI export contains data from the patient's chart" — a tautological statement that provides no insight into what "data from the patient's chart" actually includes.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA standard sections, but not confirmed | Product stores demographics (certified (a)(5)); C-CDA typically includes this, but no documentation confirms |
| Encounters / visits | ⚠️ Partial | C-CDAs are "per encounter," implying encounter data exists | Structure implies encounters are represented, but no section-level detail |
| Problems / conditions | ⚠️ Partial | Likely in C-CDA, but not confirmed | Product stores problem lists (certified (a)(3)); C-CDA typically includes this |
| Medications / prescriptions | ⚠️ Partial | Likely in C-CDA, but not confirmed | Product stores medication lists (certified (a)(1)); C-CDA typically includes this |
| Allergies | ⚠️ Partial | Likely in C-CDA, but not confirmed | Product stores allergies; C-CDA typically includes this |
| Vitals | ⚠️ Partial | Possibly in C-CDA | Product captures RPM vitals (BP, HR, SpO2, glucose, weight); unknown if these appear in C-CDA |
| Lab results | ❌ Not covered | No evidence | Product has CPOE for labs (certified (a)(2)) but no lab storage is described; may be N/A |
| Procedures | N/A | — | Not a core function of this CCM platform |
| Clinical notes / documents | ⚠️ Partial | PDF attachments described as "files attached to the patient's chart" | PDFs may contain some clinical documents, but content is unspecified |
| Care plans / goals | ❌ Not covered | No evidence beyond standard C-CDA care plan section | **Major gap**: Care plans are the product's core function — comprehensive plans addressing 6 domains. C-CDA's care plan section is unlikely to capture this richness. No vendor-specific mapping documented. |
| RPM device data | ❌ Not covered | No evidence | **Major gap**: RPM telemetry (glucose, BP, HR, SpO2, weight time-series) is a core product capability. C-CDA has no standard representation for device time-series data. |
| Medication adherence | ❌ Not covered | No evidence | **Major gap**: Medication adherence tracking and side effect reporting is the company's founding use case. No C-CDA section exists for adherence data. |
| Care coordination logs | ❌ Not covered | No evidence | **Major gap**: 200,000+ logged interactions documenting CCM services. These workflow/interaction records have no C-CDA analog. |
| CCM/PCM/RPM time tracking | ❌ Not covered | No evidence | **Gap**: Time-based service documentation linked to CPT codes, supporting Medicare billing. No C-CDA representation. |
| Insurance / coverage | ❌ Not covered | No evidence | Product likely stores patient insurance information for CCM enrollment |
| Patient communications | ❌ Not covered | No evidence | Secure messaging between patients and care teams is a product feature |
| Consent records | ❌ Not covered | No evidence | CCM requires patient consent; product stores consent records |
| Imaging / diagnostic reports | N/A | — | Not a core function |
| Immunizations | N/A | — | Not a core function |
| Claims / billing | N/A | — | Actual billing done by physician practice, not this product |

**Summary**: Of 13 applicable domains, 0 are confirmed covered, 5 are partially/likely covered (inferred from C-CDA format choice), and 8 are not covered or have no evidence. The 4 domains most central to the product's purpose — care plans, RPM device data, medication adherence, and care coordination logs — all appear absent.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the worst possible while still technically existing.

- **Comprehensibility**: A developer given this PDF could not build an import. They would know only that the export is a ZIP containing C-CDA and PDF files. They would not know which C-CDA sections to expect, what data elements are present, what templates are used, or what the PDFs contain.
- **Machine-readable artifacts**: None. No schema, no sample data, no JSON/XML specification.
- **Field-level detail**: None. Zero fields are documented.
- **Value sets/terminologies**: None specified.
- **Relationships**: None documented.
- **Instructions**: None. No UI guide, no API reference, no workflow description.

The 109-word document reads as a bare-minimum compliance artifact. Three of its sentences simply define common file format acronyms (ZIP, PDF, C-CDA) — information that would be obvious to any technical reader.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to definitively assess coverage, but strong signals point to minimal coverage. The export uses C-CDA as its sole structured format — a clinical document standard designed for health information exchange, not for comprehensive data export. The product's most valuable and distinctive data domains (care coordination logs, RPM device time-series, medication adherence records, CCM time tracking) have no standard C-CDA representation. The documentation provides zero field-level detail, zero entity enumeration, and zero C-CDA section specification. Even if the C-CDA is well-populated, it would capture at best the clinical summary layer (demographics, problems, medications, allergies) while missing the product's core operational data.

**Axis 2 — Export approach: Repackaged existing export**

The export is a C-CDA clinical document export — the same format the product would use for clinical information reconciliation ((e)(2) certified criterion) and general health information exchange. There is no evidence of any purpose-built export mechanism. No vendor-specific data dictionary, no mapping of product-specific concepts (care coordination logs, RPM readings, adherence tracking) to any export format, no extensions to C-CDA for non-standard data. The documentation defines C-CDA as "a file format used for health information exchange" — language that describes the standard's clinical exchange purpose, not a comprehensive EHI export. The inclusion of "PDF files attached to the patient's chart" alongside the C-CDAs is the only non-standard element, but this is a trivial addition (bundling existing chart attachments) rather than a purpose-built export of structured data.

### Key Findings

1. **Documentation is 109 words on 1 page** — among the thinnest EHI export documentation possible. Zero entities, zero fields, zero C-CDA sections are specified. (`downloads/SPAC-Export.pdf`)

2. **C-CDA format is fundamentally mismatched with the product's data model.** This is a chronic care management platform whose core data — care coordination logs, RPM device telemetry, medication adherence tracking, CCM time records — has no standard C-CDA representation. Using C-CDA as the sole export format likely means the majority of the product's distinctive patient data is excluded.

3. **The product's 4 most important data domains appear unaddressed.** Care plans (the core function), RPM device data, medication adherence records, and care coordination interaction logs are not mentioned in the documentation and have no C-CDA analog. These represent the primary reason patients are enrolled in this system.

4. **No export instructions exist.** The documentation does not describe how to initiate an export, who can do it, what parameters are available, or how long it takes. A user or administrator would need to contact the vendor to learn how to use the feature.

5. **This appears to be a repackaged clinical exchange export.** The C-CDA + PDF bundle is consistent with a standard clinical document exchange capability relabeled as (b)(10), not a purpose-built EHI export.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + PDF (in ZIP archive)
Entities:        0 (no data dictionary)
Fields:          0 (no field documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear
Domains covered: 0 of 13 confirmed; 5 of 13 likely partial (inferred from C-CDA)
```

### Bottom Line

A patient or provider would receive C-CDA clinical summaries and PDF chart attachments — likely capturing basic demographics, problems, medications, and allergies. But the product's most important data — the comprehensive care plans, RPM device readings, medication adherence history, and 200,000+ care coordination interaction logs that constitute the actual chronic care management record — would almost certainly be absent. The 109-word documentation provides no evidence that the vendor engaged meaningfully with (b)(10) requirements; this appears to be a clinical exchange export relabeled as an EHI export with the absolute minimum documentation needed to check the certification box.
