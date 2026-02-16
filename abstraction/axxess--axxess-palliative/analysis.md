# EHI Export Analysis: Axxess

**Product**: Axxess Palliative  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 11620 (15.99.04.3134.AXXE.02.03.1.250313)

## 1. Product Context

Axxess Palliative is a cloud-based EHR and practice management system designed specifically for palliative care delivery. It is part of the broader Axxess platform (serving 9,000+ home-based care organizations) and was certified in March 2025 (Version 3.0.2022).

The product stores a rich set of data across these functional areas:

- **Clinical**: Visit notes, vital signs, symptom assessments/ratings, diagnoses, medications (with eMAR), allergies, infectious disease tracking, implantable devices, family health history, advance directives, comprehensive plan of care, physician communications
- **Orders**: Medication orders, DME orders, supply orders, order workflows with read-back/verification
- **IDG (Interdisciplinary Group)**: Meeting schedules, agendas, summaries, sign-in sheets, team assignments, patient review documentation
- **Billing**: Direct Medicare Part B billing, multi-payer claims via Axxess Revenue Cycle Management, CPT codes, ERA processing, insurance eligibility
- **Administration**: Patient intake, referral tracking, scheduling, payer/insurance management, pharmacy/DME vendor management

This establishes the baseline: a compliant EHI export should cover clinical documentation, palliative-specific assessments, orders, IDG records, and billing/claims data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10-electronic-health-information-export.pdf` | 1-page PDF (148 KB). Primary EHI export documentation. Describes export as C-CDA 2.1 XML and PDF in ZIP format. Contains a 4-step export process. No data dictionary, no schema, no sample data. Created 2023-12-15 by Charles Daprix. Contains an internal note left in the public document. | **Primary but extremely thin** |
| `Axxess-CEHRT-Disclosures-V3.0.2022.pdf` | 3-page PDF (210 KB). CEHRT transparency disclosures listing all 27 certified criteria with brief descriptions. (b)(10) entry states export covers "all of a single patient's or population of patient's electronic health information." Created 2025-06-20. | **Secondary — confirms (b)(10) claim but adds no technical detail** |
| `cehrt-page-screenshot.png` | Full-page screenshot of the CEHRT compliance hub at `axxess.com/cehrt/`. Shows two-column layout with links to certification documents. | **Minimal — confirms page structure** |

**Verification**: The CEHRT page at `https://www.axxess.com/cehrt/` is live (HTTP 200 as of 2026-02-16). The same two PDFs and no additional EHI export documentation are linked. No data dictionary, schema, sample export, or help article about the "Download Patient Chart" feature was found on the site.

## 3. Export Mechanics

- **Format**: C-CDA 2.1 XML and PDF, packaged in a ZIP file. Each patient's data is in a subfolder named `LASTNAME_FIRSTNAME`.
- **Mechanism**: UI-based. Navigate to Patients → Download Patient Chart → specify parameters (branch, date range, patients, format) → Request Documents → wait for "Ready" status → click Export to download ZIP.
- **Single-patient**: Yes
- **Bulk/population**: Yes (multiple patients can be selected)
- **Access constraints**: Requires "appropriate permissions" (no further detail)
- **Fees**: "All costs are included within software license fees according to contract terms and conditions" (per CEHRT Disclosures PDF, page 1)

## 4. Export Content: What's In It

### What the documentation tells us

The b10 PDF provides **zero detail** about what data is included in the export. It states only:
- XML files contain "comprehensive patient data, conforming to the C-CDA version 2.1 specification"
- PDF files are in "a widely accepted industry standard"

There is no data dictionary. There are:
- **0 entities/tables** documented
- **0 fields** documented
- **0 field descriptions**, types, value sets, or relationships
- **No sample data** or machine-readable schema
- **No specification** of which C-CDA sections or templates are populated
- **No documentation** of what the PDF export contains

### Vendor's own content organization

The vendor provides no content organization whatsoever. There is no breakdown by category, module, section, or data type. The entire technical specification is: "C-CDA version 2.1 XML" and "PDF."

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

### What can be inferred from C-CDA 2.1

Since the export is described as C-CDA 2.1, the following sections are *implied* by the standard (but not confirmed by the vendor):

- Demographics (recordTarget)
- Problems/Conditions
- Medications
- Allergies and Intolerances
- Vital Signs
- Immunizations
- Procedures
- Results (lab/diagnostic)
- Encounters
- Plan of Treatment
- Social History
- Advance Directives

However, C-CDA 2.1 is a clinical summary standard. It does **not** have standard sections for billing records, palliative-specific assessments, IDG meeting documentation, DME/supply orders, or insurance/claims data. None of these domains are addressed or even mentioned in the export documentation.

### Internal note

The b10 PDF ends with the sentence: *"This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking."* This internal note, left in the public-facing document, explicitly indicates the documentation (and potentially the export itself) was created as an interim compliance artifact.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation is so thin that there is essentially nothing to describe bottom-up. The export is characterized in a single sentence as "comprehensive patient data, conforming to the C-CDA version 2.1 specification." No categories, no modules, no sections, no entities are enumerated.

The only content organization comes from the C-CDA standard itself, not from the vendor. If the export genuinely produces valid C-CDA 2.1 documents, it would contain standard clinical summary sections — but even this cannot be confirmed without sample data or section-level documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied by C-CDA 2.1 recordTarget; not confirmed by vendor | Product stores demographics (Section 1); C-CDA likely includes basic demographics but vendor doesn't specify which fields |
| Encounters / visits | ⚠️ Partial | Implied by C-CDA 2.1 Encounters section; not confirmed | Product has visit documentation; C-CDA may include encounter summaries but not full visit notes with palliative-specific detail |
| Problems / conditions / diagnoses | ⚠️ Partial | Implied by C-CDA 2.1 Problems section; not confirmed | Product stores diagnoses; likely partially covered by C-CDA |
| Medications / prescriptions | ⚠️ Partial | Implied by C-CDA 2.1 Medications section; not confirmed | Product has eMAR and medication profiles; C-CDA may include medication list but not administration records |
| Allergies | ⚠️ Partial | Implied by C-CDA 2.1 Allergies section; not confirmed | Likely partially covered |
| Immunizations | ⚠️ Partial | Implied by C-CDA 2.1 Immunizations section; not confirmed | May or may not be applicable to palliative care product |
| Vitals | ⚠️ Partial | Implied by C-CDA 2.1 Vital Signs section; not confirmed | Product records vitals; likely partially covered |
| Lab results | N/A | Product does not appear to include lab ordering/results management | No lab certification criteria |
| Imaging / diagnostic reports | N/A | No evidence product stores imaging data | Not part of product scope |
| Procedures | ⚠️ Partial | Implied by C-CDA 2.1 Procedures section; not confirmed | May be partially covered |
| Clinical notes / documents | ⚠️ Partial | PDF format may capture rendered notes; C-CDA may include notes as unstructured text | Product stores extensive visit notes; depth of coverage unknown |
| Care plans / goals | ⚠️ Partial | Implied by C-CDA 2.1 Plan of Treatment section; not confirmed | Product has palliative-specific Comprehensive Plan of Care; C-CDA Plan of Treatment section is generic and likely misses palliative-specific detail |
| Orders / referrals | ❌ Not covered | No evidence in documentation; C-CDA has no standard orders section | Product stores medication, DME, and supply orders; **significant gap** |
| Insurance / coverage | ❌ Not covered | No evidence in documentation; C-CDA does not cover insurance | Product stores insurance/payer data; **significant gap** |
| Claims / billing | ❌ Not covered | No evidence in documentation; C-CDA does not cover billing | Product does Medicare Part B billing and multi-payer claims; **significant gap** |
| Payments | ❌ Not covered | No evidence in documentation; C-CDA does not cover payments | Product processes ERA; **significant gap** |
| Consents / directives | ⚠️ Partial | Implied by C-CDA 2.1 Advance Directives section; not confirmed | Product stores advance directives; may be partially covered |
| Patient communications | ❌ Not covered | No evidence; C-CDA has no communications section | Product has physician communications; gap |
| Specialty-specific (palliative care) | ❌ Not covered | No evidence; C-CDA has no palliative-specific sections | Product stores symptom ratings/assessments, IDG meeting records, palliative-specific care plans; **critical gap** — this is the product's core differentiating data |

**Summary**: Of 15 applicable domains, 0 are confirmed covered, 9 are partially implied (by the C-CDA standard, not by vendor documentation), and 6 are not covered at all. The uncovered domains include the product's core specialty data (palliative-specific assessments, IDG records) and all billing/financial data.

## 6. Documentation Quality

The export documentation quality is **extremely poor** — among the worst possible:

- **Completeness**: A single page with no technical content beyond format names (C-CDA 2.1, PDF) and a 4-step export procedure
- **Data dictionary**: None
- **Field definitions**: None (0 fields documented)
- **Types/constraints**: None
- **Value sets/code systems**: None
- **Relationships/foreign keys**: None
- **Sample data**: None
- **Machine-readable schema**: None
- **C-CDA template/section specification**: None — the vendor doesn't even list which C-CDA sections are populated
- **PDF export specification**: None — no documentation of what the PDF export contains

A developer could not build an import from this documentation. They would know only that the output is "C-CDA 2.1 XML in a ZIP" and would need to reverse-engineer everything from actual exports.

The internal note left in the document — *"This should comply with what we need and buy us time to finish the feature"* — is a candid indicator that this was treated as a compliance checkbox, not a genuine data portability effort.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is explicitly described as C-CDA 2.1 XML (plus rendered PDFs). C-CDA is a clinical document standard designed for transitions of care, not a comprehensive data export format. This is functionally equivalent to the vendor's (b)(1) Transitions of Care capability repackaged as (b)(10). The documentation provides no evidence of any content beyond what C-CDA covers — no native database tables, no billing data, no specialty-specific palliative care data.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The export uses C-CDA 2.1, a clinical summary standard, as its sole structured format. C-CDA structurally cannot represent billing records, palliative-specific assessments, IDG meeting data, or orders management — all core data domains this product stores. This is the classic failure mode of pointing an existing clinical document export at the (b)(10) requirement. *(Source: `b10-electronic-health-information-export.pdf`)*

2. **Zero documentation depth**: There is no data dictionary, no field definitions, no schema, no sample data, and no specification of which C-CDA sections or templates are populated. The entire technical specification fits in four sentences. *(Source: `b10-electronic-health-information-export.pdf`, 1 page, 148 KB)*

3. **Internal note left in public document**: The b10 PDF ends with "This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking" — an internal planning note that was not removed before publication. This explicitly acknowledges the export was a placeholder compliance artifact. *(Source: `b10-electronic-health-information-export.pdf`, last line)*

4. **Critical specialty data gaps**: Axxess Palliative's core differentiating data — palliative-specific symptom assessments, IDG meeting records, comprehensive palliative care plans — has no representation in C-CDA and no evidence of inclusion in the export. This is the product's reason for existing, and it appears to be absent from the export. *(Based on product research vs. export documentation)*

5. **Billing/financial data absent**: The product handles Medicare Part B billing, multi-payer claims, CPT codes, and ERA processing. None of this has any representation in C-CDA, and the export documentation makes no mention of billing data. *(Based on product research vs. C-CDA 2.1 standard scope)*

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaging)
Export format:   C-CDA 2.1 XML + PDF in ZIP
Model type:      Standard projection (C-CDA)
Entities:        0 documented (N/A — no data dictionary)
Fields:          0 documented (N/A — no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multiple patients)
Domains covered: 0 of 15 confirmed; 9 of 15 implied by C-CDA standard
```

### Bottom Line

This is a textbook case of C-CDA/FHIR repackaging: the vendor points to their existing clinical document export and calls it "(b)(10)." The export documentation consists of a single page with no data dictionary and an internal note acknowledging it was a placeholder. A patient or provider requesting their complete EHI would receive a clinical summary that likely omits billing records, palliative-specific assessments, IDG meeting documentation, and orders — the very data that makes this product specialized for palliative care.
