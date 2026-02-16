# EHI Export Analysis: Axxess

**Product**: Axxess Palliative
**Analysis date**: 2026-02-15
**CHPL IDs**: 11620 (15.99.04.3134.AXXE.02.03.1.250313)

## 1. Product Context

Axxess Palliative is a cloud-based EHR and practice management system designed specifically for palliative care delivery, serving physicians and nurse practitioners in home-based palliative care settings. It is part of the broader Axxess platform (9,000+ organizations, 800,000+ users). The product was certified in March 2025 (Version 3.0.2022) across 27 ONC criteria.

Based on vendor materials and help center documentation, the product stores data across these functional areas:

- **Clinical documentation**: Visit notes, vital signs, symptom assessments, diagnoses, medications (with eMAR), allergies, infectious disease tracking, implantable devices, family health history, advance directives, comprehensive plan of care, physician communications
- **Orders management**: Medication orders, DME orders, supply orders, order workflows with read-back verification
- **IDG (Interdisciplinary Group) Center**: Meeting scheduling, agendas, summaries, sign-in sheets, patient review documentation
- **Billing**: Medicare Part B billing, multi-payer claims via Axxess Revenue Cycle Management integration, CPT codes, ERA processing
- **Intake/scheduling**: Patient intake from referral through admission, scheduling with calendar views, insurance eligibility checking
- **Administration**: Referral tracking, payer/insurance management, authorized contacts, pharmacy and DME vendor management

This establishes the baseline: a complete EHI export should cover clinical records, specialty palliative care data (symptom assessments, IDG records, comprehensive plans of care), billing/claims, orders, and administrative patient data.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Informativeness |
|---|---|---|---|
| `b10-electronic-health-information-export.pdf` | EHI export documentation | 1 page, 148 KB | **Primary artifact** — describes export format and process; no data dictionary |
| `Axxess-CEHRT-Disclosures-V3.0.2022.pdf` | CEHRT transparency disclosures | 3 pages, 210 KB | **Low** — one-sentence description of (b)(10) capability among 27 criteria |
| `cehrt-page-screenshot.png` | Screenshot of CEHRT page | 2.5 MB | **Minimal** — shows page layout and document links |

All three artifacts were directly examined. The b10 PDF text was extracted with `pdftotext -layout` and verified against the prior report's claims. The CEHRT disclosures PDF was similarly extracted. Both PDFs' metadata was verified with `pdfinfo`.

**Total documentation for the (b)(10) export: 1 page of substantive content.** No data dictionary, no schema, no sample data, no machine-readable artifacts of any kind.

## 3. Export Mechanics

- **Format**: C-CDA 2.1 XML and PDF, packaged in a ZIP archive. Each patient's data is in a subfolder labeled `LASTNAME_FIRSTNAME`.
- **Mechanism**: UI-driven. Navigate to Patients → Download Patient Chart → select Branch, date range, patient(s), and file format → click "Request Documents" (enters processing queue) → when status shows "Ready," click "Export" to download the ZIP.
- **Single-patient vs bulk**: Both. The UI allows selection of single or multiple patients.
- **Access constraints**: Per the CEHRT disclosures PDF, "All costs are included within software license fees according to contract terms and conditions." No additional fees documented.
- **Process maturity indicator**: The b10 PDF (created 2023-12-15) ends with an internal note: *"This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking."* This sentence was left in the publicly-facing document and strongly suggests the export was developed as a minimal compliance measure rather than a thorough implementation.

## 4. Export Content: What's In It

### What the documentation tells us

The b10 PDF provides **zero detail** about what data is included in the export. The entire description of content is:

> "XML: Comprehensive patient data, conforming to the C-CDA version 2.1 specification."
> "PDF: A widely accepted industry standard."

There is:
- **No data dictionary** — not at any level (entity, table, field, section)
- **No enumeration of C-CDA sections or templates** used
- **No field-level documentation** of any kind
- **No sample export files**
- **No schema or machine-readable specification** beyond referencing "C-CDA version 2.1"
- **No description of what the PDF export contains** (rendered clinical documents? Full chart? Selected forms?)

### Vendor's own content organization

The vendor provides no content organization. There is no breakdown of data categories, tables, entities, or sections. The entire content documentation is the two bullet points quoted above.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | 0 | 0 | N/A | N/A |

### What we can infer

The export format is C-CDA 2.1. Standard C-CDA documents include sections for demographics, problems, medications, allergies, procedures, results, vital signs, immunizations, encounters, plan of care, social history, and functional status. However, without sample data or template documentation, we cannot confirm which C-CDA sections Axxess actually populates.

C-CDA 2.1 does **not** have standard sections for billing records, claims, CPT codes, ERA data, palliative-specific symptom assessments, IDG meeting records, DME/supply orders, or many other data types that Axxess Palliative stores.

The PDF format component could theoretically contain additional data (rendered documents, forms, notes), but there is no documentation of what it includes.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categorization or detail about export content. The only statement is that the export produces "comprehensive patient data" in C-CDA 2.1 format. Without a data dictionary, sample data, or even a list of C-CDA sections, it is impossible to assess coverage from the vendor's documentation alone.

The choice of C-CDA 2.1 as the sole structured format is itself informative: C-CDA is a clinical summary exchange standard, not a native data model export. It is designed for transitions of care, not for exporting "all electronic health information." This strongly suggests the export covers only the clinical summary slice of the patient record.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Likely in C-CDA header, but no confirmation | Product stores demographics (certified under (a)(5)); C-CDA typically includes basic demographics |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections | Product stores visit notes; C-CDA encounter sections are typically thin |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA typically includes problem list | Product stores diagnoses; likely present but unconfirmed |
| Medications / prescriptions | ⚠️ Partial | C-CDA typically includes medications section | Product stores medication profiles with eMAR; C-CDA unlikely to capture full eMAR detail |
| Allergies | ⚠️ Partial | C-CDA typically includes allergies section | Product stores allergies; likely present but unconfirmed |
| Immunizations | ⚠️ Partial | C-CDA has immunizations section | Unclear if palliative care product stores immunizations significantly |
| Vitals | ⚠️ Partial | C-CDA typically includes vital signs | Product stores vitals; likely present but unconfirmed |
| Lab results | N/A | Product does not appear to have lab ordering/results | No lab certification criteria; not a gap |
| Imaging / diagnostic reports | N/A | No evidence product stores imaging data | Not a gap |
| Procedures | ⚠️ Partial | C-CDA has procedures section | Likely present but unconfirmed |
| Clinical notes / documents | ⚠️ Partial | PDF component may contain rendered notes; C-CDA may include notes as unstructured text | Product stores extensive visit documentation; coverage depth unknown |
| Care plans / goals | ⚠️ Partial | C-CDA has plan of care section | Product stores comprehensive palliative plan of care; C-CDA section unlikely to capture full specialty detail |
| Orders / referrals | ❌ Not covered | No evidence in C-CDA standard sections for DME, supply, or medication orders as managed in the product | Product stores medication, DME, and supply orders with workflow data; significant gap |
| Insurance / coverage | ❌ Not covered | C-CDA does not have insurance/payer sections | Product stores insurance/payer information and eligibility data; significant gap |
| Claims / billing | ❌ Not covered | C-CDA has no billing sections | Product handles Medicare Part B billing, multi-payer claims, CPT codes, ERA; significant gap |
| Payments | ❌ Not covered | C-CDA has no payment sections | Product processes ERA and payment data; significant gap |
| Consents / directives | ⚠️ Partial | C-CDA has advance directives section | Product stores advance directives; may be partially covered |
| Specialty-specific (Palliative Care) | ❌ Not covered | C-CDA has no standard sections for palliative-specific data | Product stores symptom ratings/assessments, IDG meeting records, palliative-specific plan of care detail, physician communications; **critical gap** |

**Note on coverage ratings**: All domains marked "⚠️ Partial" are assessed based on what C-CDA 2.1 *typically* includes, not on confirmed evidence from this vendor. Without sample data or section-level documentation, we cannot confirm any domain is actually covered. Every clinical domain could equally be rated "❌ Not covered" given the absence of evidence.

## 6. Documentation Quality

The export documentation quality is **extremely poor** — among the worst possible for a certified product:

- **Total substantive documentation**: 1 page (~150 words of actual content)
- **Data dictionary**: None
- **Field-level documentation**: None (0 fields documented)
- **C-CDA template/section specification**: None
- **Sample data**: None
- **Schema or machine-readable artifacts**: None
- **Value sets or code systems**: None
- **Relationship documentation**: None
- **PDF export content description**: None

A developer attempting to build an import from this documentation would know only that the export is "C-CDA 2.1 XML" and "PDF" in a ZIP file. They would need to obtain actual export files and reverse-engineer the structure entirely.

The internal note left in the public document — *"This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking"* — indicates the documentation was drafted as an interim compliance artifact. The b10 PDF was created 2023-12-15, yet the product was not certified until 2025-03-13. There is no evidence the documentation was updated between initial drafting and certification, and the internal note was never removed.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export documentation is too thin to assess actual content, and the export format (C-CDA 2.1) is structurally incapable of representing the full scope of data a palliative care EHR stores. The internal note in the documentation confirms this was treated as a compliance checkbox. There is no data dictionary, no schema, no sample data, and no evidence of effort to document or export data beyond what a standard clinical summary provides.

### Key Findings

1. **The entire (b)(10) export documentation is a single page with ~150 words of content** — no data dictionary, no field documentation, no sample data, no schema. This is among the most minimal export documentation possible for a certified product. (`b10-electronic-health-information-export.pdf`, 1 page)

2. **The export uses C-CDA 2.1 as its sole structured format**, which is a clinical summary exchange standard — not a native data model export. C-CDA cannot represent billing records, palliative-specific assessments, IDG meeting data, orders workflows, or insurance information that the product stores. This is functionally a (b)(1) Transitions of Care export repackaged as (b)(10).

3. **An internal note was left in the public document**: *"This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking."* This confirms the export was developed as a minimal compliance measure. (`b10-electronic-health-information-export.pdf`, final line)

4. **Palliative care specialty data is entirely unaddressed.** The product's core differentiator — symptom assessments, IDG meeting records, comprehensive palliative plans of care, physician communications — has no representation in C-CDA and is not documented in the export.

5. **Billing and financial data is absent.** The product handles Medicare Part B billing, multi-payer claims, CPT codes, and ERA processing. C-CDA has no billing sections, and the documentation provides no indication that billing data is exported in any format.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA 2.1 XML + PDF, in ZIP
Model type:      Standard projection (C-CDA clinical summary)
Entities:        N/A (no data dictionary)
Fields:          N/A (no fields documented)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient selection supported)
Domains covered: 0 confirmed of 13 applicable (up to ~9 inferred from C-CDA, 0 verified)
```

### Bottom Line

This is a textbook case of a vendor repackaging their existing C-CDA/Transitions of Care export as a (b)(10) "all EHI" export. A patient or provider would receive a clinical summary — likely demographics, problem lists, medications, allergies, and vitals — but would almost certainly not receive billing records, palliative-specific clinical assessments, IDG documentation, orders, or insurance data. The internal note left in the documentation confirms this was a compliance shortcut, not a genuine effort to enable comprehensive health information export.
