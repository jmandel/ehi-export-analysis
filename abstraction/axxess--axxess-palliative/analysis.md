# EHI Export Analysis: Axxess

**Product**: Axxess Palliative (Version 3.0.2022)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.99.04.3134.AXXE.02.03.1.250313 (CHPL ID 11620)

## 1. Product Context

Axxess Palliative is a cloud-based EHR and practice management system built specifically for palliative care delivery, serving physicians, nurse practitioners, and administrative staff at palliative care organizations. Axxess as a company serves 9,000+ organizations with 800,000+ users across home health, hospice, home care, and palliative care.

The product stores data across several clinical and operational domains relevant to EHI export assessment:

- **Patient demographics** — contacts, MRN, code status, insurance/payer info, authorized contacts, advance directives
- **Clinical documentation** — visit notes, vital signs, symptom ratings/assessments, diagnoses, medication profiles with eMAR, allergies, infectious disease tracking, implantable devices, family health history, physician communications
- **Plan of care** — comprehensive palliative plan of care management
- **Orders** — medication orders, DME orders, supply orders, order workflows with verification
- **IDG (Interdisciplinary Group)** — meeting records, agendas, summaries, sign-in sheets, patient review documentation
- **Billing** — Medicare Part B billing, multi-payer claims via Revenue Cycle Management integration, CPT codes, ERA processing
- **Scheduling** — patient/employee schedules, task assignments, visit history

This product is certified for 27 ONC criteria including (b)(10) EHI Export. The breadth of stored data — spanning clinical documentation, specialty palliative assessments, orders management, IDG workflows, and billing — establishes the baseline against which export completeness should be measured.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10-electronic-health-information-export.pdf` | 1-page PDF (148 KB, created 2023-12-15). Sole (b)(10) documentation. Describes export format (C-CDA 2.1 XML + PDF in ZIP) and 4-step export process. No data dictionary, no schema, no sample data. Contains an inadvertent internal note. | **Primary but extremely thin** — the only technical artifact for the (b)(10) export |
| `Axxess-CEHRT-Disclosures-V3.0.2022.pdf` | 3-page PDF (210 KB, created 2025-06-20). Transparency disclosures listing all 27 certified criteria with brief descriptions and cost info. (b)(10) entry confirms export of "all of a single patient's or population of patient's electronic health information." | **Supplementary** — confirms export claim and pricing but adds no technical detail |
| `cehrt-page-screenshot.png` | Full-page screenshot (2.5 MB) of the CEHRT compliance hub at axxess.com/cehrt/. Shows document links layout. | **Minimal** — confirms page structure only |

Total documentation pages: 4 (1 + 3). No machine-readable artifacts. No sample data. No data dictionary.

## 3. Export Mechanics

- **Format**: C-CDA 2.1 XML and PDF, packaged in a ZIP archive. Each patient's data is in a subfolder labeled `LASTNAME_FIRSTNAME`.
- **Mechanism**: UI-based. Navigate to Patients → Download Patient Chart → set parameters (branch, date range, patients, file format) → click "Request Documents" → download ZIP when status shows "Ready."
- **Single-patient vs bulk**: Supports both single patient and "population of patients" (multiple patients).
- **Access constraints**: Available to "users with appropriate permissions." No additional fees beyond license — "All costs are included within software licenses fees according to contract terms and conditions."

## 4. Export Content: What's In It

### No data dictionary exists

The vendor provides **zero documentation** about what data elements are included in the export. The entire technical specification is:

> "XML: Comprehensive patient data, conforming to the C-CDA version 2.1 specification."
> "PDF: A widely accepted industry standard."

There is no:
- Data dictionary or field inventory
- List of C-CDA sections or templates used
- Schema or machine-readable specification
- Sample export files
- Field names, types, descriptions, or value sets
- Entity or table documentation of any kind

### Vendor's own content organization

The vendor does not organize or categorize the export content at all. The only content description is the single sentence about "comprehensive patient data" in C-CDA 2.1 format.

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

**Total entities documented: 0. Total fields documented: 0.**

### What can be inferred

The export format is C-CDA 2.1, which is a clinical document exchange standard. Standard C-CDA sections typically include: allergies, encounters, immunizations, medications, problems, procedures, results, vital signs, plan of treatment, social history, and assessment. However, the vendor does not confirm which sections are populated or whether any extensions are used.

The PDF export format is undefined — it likely renders patient documents but there is no documentation of what documents or data are included.

### The internal note

The b10 PDF contains this sentence at the end: *"This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking."* This internal memo language, left in the public-facing document, suggests the C-CDA export was implemented as an interim compliance measure rather than a purpose-built EHI export, and that a more complete solution was intended but may not have been delivered (the document dates from December 2023 and has not been updated).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no structured coverage information. The only claim is that the export contains "comprehensive patient data" in C-CDA 2.1 format and "all of a single patient's or population of patient's electronic health information."

Because C-CDA 2.1 is a clinical summary standard, the export almost certainly covers standard clinical summary data (demographics, problems, medications, allergies, vitals, immunizations, procedures, encounters). However, without documentation, sample data, or a data dictionary, it is impossible to verify what is actually exported.

C-CDA 2.1 does not have standard sections for billing records, palliative care-specific symptom assessments, IDG meeting documentation, DME/supply orders, insurance eligibility details, ERA data, or other specialty/operational data that Axxess Palliative stores.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (likely) | C-CDA typically includes demographics | Likely present but unverifiable; no field-level detail |
| Encounters / visits | ⚠️ Partial (likely) | C-CDA encounters section | Likely present but depth unknown |
| Problems / conditions / diagnoses | ⚠️ Partial (likely) | C-CDA problems section | Likely present but depth unknown |
| Medications / prescriptions | ⚠️ Partial (likely) | C-CDA medications section | Basic meds likely present; eMAR detail almost certainly absent from C-CDA |
| Allergies | ⚠️ Partial (likely) | C-CDA allergies section | Likely present |
| Immunizations | ⚠️ Partial (likely) | C-CDA immunizations section | Likely present |
| Vitals | ⚠️ Partial (likely) | C-CDA vital signs section | Likely present |
| Lab results | N/A | Product does not appear to include lab ordering/results | Not a gap — product lacks lab certification |
| Imaging / diagnostic reports | N/A | No evidence product stores imaging data | Not a gap |
| Procedures | ⚠️ Partial (likely) | C-CDA procedures section | Likely present but depth unknown |
| Clinical notes / documents | ⚠️ Partial (likely) | C-CDA may include notes; PDF export may include rendered documents | Possibly covered via PDF format; no confirmation |
| Care plans / goals | ⚠️ Partial (likely) | C-CDA plan of treatment section | Basic plan likely present; palliative-specific comprehensive plan of care depth unknown |
| Orders / referrals | ❌ Not covered (likely) | C-CDA has no standard section for DME/supply orders | Product has rich orders management (meds, DME, supplies); likely not fully captured in C-CDA |
| Insurance / coverage | ❌ Not covered (likely) | C-CDA does not have insurance/payer detail sections | Product stores insurance/payer info; likely absent from export |
| Claims / billing | ❌ Not covered (likely) | C-CDA has no billing sections | Product does Medicare Part B billing, multi-payer claims, CPT codes, ERA; almost certainly absent |
| Payments | ❌ Not covered (likely) | C-CDA has no payment sections | Product processes ERA/payments; almost certainly absent |
| Consents / directives | ⚠️ Partial (likely) | C-CDA advance directives section | May be partially present |
| Patient communications | ❌ Not covered (likely) | C-CDA has no communications section | Physician communications stored in product; likely absent |
| Specialty-specific (palliative care) | ❌ Not covered (likely) | C-CDA has no palliative-specific sections | Product stores symptom ratings, IDG meeting records, palliative-specific assessments; almost certainly absent from C-CDA |

**Critical caveat**: Every coverage assessment above is inferential. The vendor provides no documentation confirming what is or isn't in the export. Assessments are based on what C-CDA 2.1 standard sections can and cannot represent.

## 6. Documentation Quality

The documentation quality is **extremely poor** — among the weakest possible for a certified product:

- **No data dictionary at all** — not even a list of what's exported
- **No field-level definitions** — no names, types, descriptions, value sets, or constraints
- **No machine-readable artifacts** — no schemas, no sample data, no JSON/XML specifications
- **No C-CDA template or section detail** — doesn't even list which C-CDA sections are populated
- **1 page total** for the technical documentation
- **Contains an internal note** that was inadvertently left in the public document, undermining credibility
- **No help center article** for the "Download Patient Chart" feature found in the public help center

A developer could not build an import from this documentation. They would know only that the export is "C-CDA 2.1 XML" in a ZIP and would need to reverse-engineer the structure from actual exports.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is far too thin to assess coverage. However, the choice of C-CDA 2.1 as the sole structured format is a strong signal that coverage is limited to clinical summary data. C-CDA 2.1 has no standard representation for billing records, palliative-specific symptom assessments, IDG meeting documentation, DME/supply orders, insurance details, ERA data, or other specialty data that Axxess Palliative stores. The vendor makes no claim of extending C-CDA beyond standard sections and provides no evidence of custom sections or extensions. The internal note — "This should comply with what we need and buy us time to finish the feature" — explicitly frames this as an interim compliance measure rather than a comprehensive EHI export.

**Axis 2 — Export approach: Repackaged existing export**

The export is C-CDA 2.1 — the same format used for (b)(1) Transitions of Care and (g)(6) CDA creation, both of which Axxess Palliative is also certified for. The disclosures PDF confirms the product creates CDA documents conforming to "USCDI V1 requirements and the approved templates" for (g)(6). The (b)(10) export appears to be the same C-CDA clinical summary capability relabeled as "electronic health information export." There is no evidence of any purpose-built export mechanism, no native database dump, no additional data domains beyond what C-CDA covers, and no data dictionary showing product-specific fields. The internal note confirms this was designed as a compliance checkbox.

### Key Findings

1. **The export is a C-CDA clinical summary relabeled as (b)(10).** The same C-CDA 2.1 format is used for (b)(1) Transitions of Care and (g)(6) CDA creation. No evidence exists that the (b)(10) export includes any data beyond standard C-CDA sections. (`b10-electronic-health-information-export.pdf`)

2. **The internal note is a smoking gun.** The sentence "This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking" explicitly acknowledges this is an interim compliance artifact, not a complete EHI export. (`b10-electronic-health-information-export.pdf`)

3. **Zero documentation of export content.** No data dictionary, no field inventory, no schema, no sample data — just one sentence saying the XML is "comprehensive patient data, conforming to the C-CDA version 2.1 specification." This is among the thinnest (b)(10) documentation possible. (`b10-electronic-health-information-export.pdf`)

4. **Major data domains are almost certainly missing.** Axxess Palliative stores Medicare Part B billing data, CPT codes, ERA data, palliative-specific symptom assessments, IDG meeting records, DME/supply orders, and insurance details — none of which map to standard C-CDA sections. (`product-research.md`, `b10-electronic-health-information-export.pdf`)

5. **The b10 PDF has not been updated since December 2023**, despite the product being certified in March 2025 and the disclosures document being updated in June 2025. The promised feature improvement has not materialized in the documentation. (`pdfinfo` metadata)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA 2.1 XML + PDF in ZIP
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (single or multiple patients)
Domains covered: 0 of 14 confirmed (up to ~9 of 14 inferred from C-CDA standard sections, but unverifiable)
```

### Bottom Line

Axxess Palliative's (b)(10) export is a standard C-CDA clinical summary repackaged as an EHI export, with the thinnest possible documentation — a single page with no data dictionary, no schema, and an inadvertent internal note acknowledging it as an interim compliance measure. A patient or provider would likely receive only a clinical summary (demographics, problems, meds, allergies, vitals) while billing records, palliative-specific assessments, IDG documentation, and orders data are almost certainly excluded. The single biggest gap is the complete absence of documentation making it impossible to verify any coverage claims, compounded by the strong evidence that this is a relabeled clinical exchange export rather than a genuine "all EHI" export.
