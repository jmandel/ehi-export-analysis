# EHI Export Analysis: Lunar Systems, Inc.

**Product**: Lunar Cloud Platform v2.6
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.3241.Luna.02.00.1.250917 (CHPL #11698)

## 1. Product Context

Lunar Systems, Inc. is an early-stage startup (founded 2020, 11–50 employees) building an "AI-native hospital information system" targeting smaller hospitals. The Lunar Cloud Platform is a comprehensive, cloud-hosted HIS covering inpatient, ED, and ambulatory settings. It was certified on 2025-09-17 with 30+ ONC criteria, consistent with a full-featured EHR.

**What the product stores** (based on certifications, job listings, and marketing):

- **Clinical data**: Demographics, medication lists, allergy lists, problem lists, vital signs, lab orders/results, diagnostic imaging orders, implantable device records, family health history, clinical notes, CPOE across medications/labs/imaging, drug interaction checks.
- **Revenue cycle / billing**: Job listings for Revenue Cycle Specialist, and "coders" and "billers" are explicitly listed as platform users. The product describes seven suites including a "Lunar Revenue Suite."
- **Pharmacy**: Pharmacists listed as users; CPOE for medications and drug interaction checks certified.
- **Lab**: Lab technicians listed as users; CPOE for lab orders certified.
- **Supply chain**: Supply chain staff listed as users (operational, likely not EHI).
- **Patient access**: Patient portal with view/download/transmit ((e)(1) certified).
- **Interoperability**: FHIR R4 API (via EMR Direct), Direct messaging, transitions of care.

This is a broad product. An EHI export should cover clinical data across all settings, billing/charges, orders, clinical documentation, insurance, and patient-generated data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_Export_Jan_2026.pdf` (54 pages, 1.1 MB) | Primary and sole documentation artifact. Contains overview, C-CDA format guide, 18 C-CDA section specifications with XML examples and key element tables, and supplemental CSV data dictionary for 3 categories (documents, orders, charges). | **Most informative** — this is the entire documentation |
| `ehi-export-page.html` (6.7 KB) | Webflow-hosted page containing a single iframe that embeds the PDF. No other content, links, or instructions. | Low — confirms delivery mechanism only |
| `ehi-export-page-screenshot.png` (1.4 MB) | Browser screenshot of the EHI export page showing the embedded PDF viewer. | Minimal |
| `enrichment/ehi-export-sections.json` (29.6 KB) | Prior agent's extraction of 18 C-CDA sections with 146 key element definitions. | High — verified against PDF text; accurate |
| `enrichment/ehi-export-supplemental.json` (6.5 KB) | Prior agent's extraction of 3 supplemental CSV categories with 42 fields. | High — verified against PDF text; accurate |
| `enrichment/extraction-stats.json` (185 bytes) | Parse accounting: 54 pages, 18/18 sections, 3 supplemental categories, 42 fields, 146 key elements, 0 parse failures. | Useful for cross-check |
| `enrichment/extract-sections.ts` (10.8 KB) | Bun TypeScript script that performed the PDF extraction. | Reference for methodology |

**Verification notes**: I independently extracted the PDF text via `pdftotext -layout` (2,269 lines) and verified all section names, element counts, and supplemental field counts against the enrichment JSON. The prior agent's extraction is accurate. The PDF is 54 pages as reported, produced by Google Docs Renderer, PDF version 1.4.

## 3. Export Mechanics

- **Format**: ZIP file containing (1) C-CDA XML files (one per patient) and (2) supplemental CSV files for data not captured in C-CDA
- **C-CDA version**: CDA Release 4.1
- **Mechanism**: The PDF describes the export format but provides no instructions on how to trigger it. There is no user guide for performing the export — no button names, no API endpoints, no permission requirements documented.
- **Single-patient vs bulk**: Both single-patient and bulk-patient export are explicitly supported (per the overview: "The platform supports single-patient and bulk-patient data extraction").
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

The export has two components: (1) C-CDA XML containing structured clinical data across 18 sections, and (2) supplemental CSV files covering 3 categories of data that don't fit the C-CDA standard.

### C-CDA Component

18 sections with a total of 146 key elements documented. Every element has a description. Each section includes:
- A narrative description of what the section covers
- Metadata (template ID, LOINC code where applicable)
- A complete XML example with realistic sample data
- A human-readable text example
- Coded entry examples
- A key elements table mapping XML elements to descriptions

| Section | Key Elements | Template ID | LOINC Code | Pages |
|---|---|---|---|---|
| Patient Summary | 15 | (recordTarget) | — | 6–7 |
| Allergies and Intolerances | 7 | 2.16.840.1.113883.10.20.22.2.6.1 | 48765-2 | 8–10 |
| Problem List | 9 | 2.16.840.1.113883.10.20.22.2.5.1 | 11450-4 | 11–13 |
| History of Medication Use | 10 | 2.16.840.1.113883.10.20.22.2.1.1 | 10160-0 | 14–16 |
| Laboratory/Diagnostic Results | 7 | 2.16.840.1.113883.10.20.22.2.3.1 | 30954-2 | 17–19 |
| Procedures | 6 | 2.16.840.1.113883.10.20.22.2.7.1 | 47519-4 | 20–21 |
| Social History | 5 | 2.16.840.1.113883.10.20.22.2.17 | 29762-2 | 22–23 |
| Functional Status | 6 | 2.16.840.1.113883.10.20.22.2.14 | — | 24–25 |
| Mental/Cognitive Status | 6 | 2.16.840.1.113883.10.20.22.2.56 | — | 26–27 |
| Vital Signs | 8 | 2.16.840.1.113883.10.20.22.2.4.1 | 8716-3 | 28–30 |
| History of Encounters | 10 | 2.16.840.1.113883.10.20.22.2.22.1 | 46240-8 | 31–33 |
| History of Immunizations | 7 | 2.16.840.1.113883.10.20.22.2.2.1 | 11369-6 | 34–35 |
| Care Team | 10 | 2.16.840.1.113883.10.20.22.2.500 | 85847-2 | 36–38 |
| Assessments | 7 | 2.16.840.1.113883.10.20.22.2.8 | — | 39–40 |
| Treatment Plan | 9 | 2.16.840.1.113883.10.20.22.2.10 | — | 41–43 |
| Clinical Notes | 9 | 2.16.840.1.113883.10.20.22.2.65 | 11506-3 | 44–46 |
| Payers (Insurance) | 10 | 2.16.840.1.113883.10.20.22.2.18 | 48768-6 | 47–49 |
| Participant (Relationships) | 5 | 2.16.840.1.113883.10.20.22.5.8 | — | 50–51 |

The C-CDA sections use standard template IDs and LOINC codes. This is genuine C-CDA with proper HL7 template references, not a proprietary format. The XML examples reference standard code systems: SNOMED-CT, LOINC, RxNorm, CVX, NCI Thesaurus, NUCC Health Care Provider Taxonomy, CDC race/ethnicity codes, and Source of Payment Typology.

### Supplemental CSV Component

3 categories with 42 total fields. Every field has a name, description, and data type documented.

| Category | Fields | Opaque (dict/array) | Purpose |
|---|---|---|---|
| Documents | 12 | 2 (`json_data`, `application_data`) | Documents, images, scanned materials, multimedia |
| Orders | 14 | 1 (`data`) | Clinical orders beyond C-CDA (all order types) |
| Charges | 16 | 1 (`diagnosis_ids`) | Billing charges with revenue codes, procedure codes, NDC |

**Documents CSV** (12 fields): `class`, `type`, `awaiting_signature`, `timestamp`, `added_at`, `source`, `desc`, `loinc_id`, `text_data`, `json_data` (dict), `application_data` (dict), `visit` (uuid)

**Orders CSV** (14 fields): `name`, `label`, `serial_number`, `data` (dict), `status`, `urgency`, `reason`, `start_time`, `end_time`, `details`, `fully_signed_at`, `ixp_start_time`, `ixp_end_time`, `visit` (uuid)

**Charges CSV** (16 fields): `rate`, `revenue_code`, `procedure_code`, `modifier`, `pos_code`, `dept`, `quantity`, `total`, `recorded_at`, `service_date`, `is_emg`, `is_epsdt`, `is_verified`, `ndc`, `deleted_at`, `diagnosis_ids` (array)

**Critical gap in supplemental documentation**: 4 fields are typed as `dict` or `array` with no documentation of their internal structure. The `json_data` and `application_data` fields in Documents, and the `data` field in Orders, are described generically ("JSON data associated with the document," "Data associated with the order"). A developer would have no way to know what keys or values these dictionaries contain without sample data, which is not provided.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized into two components using the vendor's own framing:

**C-CDA XML** (18 sections): Covers the standard clinical data you'd expect from a C-CDA document — demographics, allergies, problems, medications, labs, procedures, social history, functional/cognitive status, vitals, encounters, immunizations, care team, assessments, treatment plans, clinical notes, insurance/payers, and patient relationships. This is broader than a minimal C-CDA; the inclusion of functional status, cognitive status, assessments, care team, and treatment plan sections goes beyond what many vendors include. The 18-section coverage is genuinely comprehensive for C-CDA.

**Supplemental CSV** (3 categories): This is where Lunar goes beyond standard C-CDA to address (b)(10) completeness:
- **Documents**: A catch-all for non-C-CDA documents, images, and multimedia. The `text_data`, `json_data`, and `application_data` fields suggest this can hold arbitrary structured and unstructured content. However, the opaque `dict` fields make it impossible to assess what's actually captured without sample data.
- **Orders**: All clinical orders (medications, labs, imaging, etc.) with status, urgency, timing, and investigation windows. This supplements the C-CDA medication and procedure sections with the full order lifecycle.
- **Charges**: Genuine billing data — revenue codes, procedure codes, modifiers, place-of-service codes, NDC codes, quantities, rates, and totals linked to diagnoses. This is not just insurance information (which is in the C-CDA Payers section) but actual charge/billing records.

The vendor explicitly mentions the export content varies by which suites are implemented (Clinical, Revenue, Lab, IT, Operations, Analytics, Patient). This suggests the export is configurable and may include more or less data depending on the deployment.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Summary section: 15 elements including name, DOB, gender, address, phone, MRN, SSN, race, ethnicity, language, marital status, deceased status | Thorough |
| Encounters / visits | ✅ Covered | History of Encounters section: 10 elements including encounter type, dates, performer, diagnoses | Adequate |
| Problems / conditions | ✅ Covered | Problem List section: 9 elements with SNOMED-CT coding, status, dates | Thorough |
| Medications / prescriptions | ✅ Covered | History of Medication Use section: 10 elements with RxNorm coding, dose, route, rate; supplemental Orders CSV may contain additional medication orders | Good; MAR (medication administration records) coverage unclear |
| Allergies | ✅ Covered | Allergies and Intolerances section: 7 elements with coded allergens, reactions, severity | Thorough |
| Immunizations | ✅ Covered | History of Immunizations section: 7 elements with CVX coding | Adequate |
| Vitals | ✅ Covered | Vital Signs section: 8 elements with LOINC coding | Thorough |
| Lab results | ✅ Covered | Laboratory/Diagnostic Results section: 7 elements with LOINC coding, values, units, reference ranges | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | Lab/Diagnostic Results section covers some; supplemental Documents CSV may contain imaging data in opaque `json_data`/`application_data` fields, but this is not explicitly documented | Product is certified for (a)(3) CPOE for diagnostic imaging; imaging results may be in supplemental Documents but evidence is indirect |
| Procedures | ✅ Covered | Procedures section: 6 elements with SNOMED-CT coding | Adequate |
| Clinical notes / documents | ✅ Covered | Clinical Notes section: 9 elements including note type, text, author; supplemental Documents CSV provides additional document capture | Good |
| Care plans / goals | ✅ Covered | Treatment Plan section: 9 elements with SNOMED-CT coding for planned procedures; Assessments section: 7 elements | Adequate |
| Orders / referrals | ✅ Covered | Supplemental Orders CSV: 14 fields covering order lifecycle | No explicit referral entity, but orders may capture referrals |
| Insurance / coverage | ✅ Covered | Payers section: 10 elements including payer org, plan name, member ID, coverage type, effective dates | Good |
| Claims / billing | ✅ Covered | Supplemental Charges CSV: 16 fields including revenue codes, procedure codes, modifiers, NDC, quantities, rates, totals, diagnosis linkages | Genuine billing data — a strength |
| Payments | ❌ Not covered | No payment entity in C-CDA or supplemental CSV | Product likely handles revenue cycle (Revenue Suite); payment records may be a gap |
| Consents / directives | ❌ Not covered | No advance directives or consent section in C-CDA; no supplemental CSV for consents | Not explicitly documented as a product capability, so unclear if this is a gap |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal communication entity | Product has patient portal ((e)(1) certified); portal messages are likely stored but not exported |
| Family health history | ⚠️ Partial | Certified for (a)(12) family health history, but no dedicated section. May be partially captured under Social History or Participant sections | Likely a gap — the product stores this data per its certification, but the export doesn't explicitly address it |
| Implantable devices | ⚠️ Partial | Certified for (a)(14), but no dedicated section or CSV. May be captured under Procedures section | Likely a gap — product is certified to store this data but the export doesn't explicitly include it |

**Key gaps**:
- **Payments**: The product has a Revenue Suite and explicitly lists billers as users. Charges are exported, but payment/remittance records are not.
- **Patient portal messages**: The product has a patient portal but no communication data appears in the export.
- **Family health history and implantable devices**: Both are certified capabilities with no clear export coverage.
- **Imaging results as files**: The overview mentions "images, scanned documents, and multimedia files" are included, but the CSV schema only has text/dict fields — it's unclear whether actual binary files (DICOM, JPEG) are exported or just metadata.

## 6. Documentation Quality

**Strengths**:
- Well-organized 54-page PDF with clear structure: overview → C-CDA format guide → 18 section specifications → supplemental data dictionary
- Every C-CDA section has consistent documentation: description, metadata (template ID, LOINC), XML example, human-readable text example, coded entry example, key elements table
- All 188 documented elements (146 C-CDA + 42 CSV) have descriptions — 100% description coverage
- XML examples use realistic sample data (patient names, addresses, clinical scenarios)
- Template IDs and code systems are correctly specified and reference real HL7/LOINC/SNOMED standards
- The document explicitly addresses the (b)(10) requirement and references the designated record set (45 CFR 164.502)

**Weaknesses**:
- **No sample export files**: No downloadable sample C-CDA file, no sample CSV files, no sample ZIP package. A developer cannot test against real output.
- **No machine-readable schemas**: No XSD, no JSON Schema, no OpenAPI spec. The entire specification is a single PDF.
- **Opaque dict/array fields**: 4 supplemental CSV fields (`json_data`, `application_data`, `data`, `diagnosis_ids`) have no internal structure documentation. These could contain significant data that is effectively undocumented.
- **No export trigger documentation**: How does a user actually perform the export? No UI guide, no API endpoint, no permissions documentation.
- **No relationship documentation between C-CDA and CSV**: The supplemental CSVs reference visits by UUID, but there's no documentation of how these UUIDs map to encounters in the C-CDA XML.
- **C-CDA element descriptions are generic**: The key elements tables describe standard C-CDA XML elements (e.g., "`<entry>` — Represents the allergy or adverse reaction entry"). These describe the C-CDA structure, not Lunar-specific data content. A developer familiar with C-CDA already knows what `<entry>` does.
- **Single artifact**: All documentation is in one PDF with no supporting machine-readable files.

**Implementability assessment**: A developer familiar with C-CDA could parse the XML using standard C-CDA libraries. The supplemental CSV fields are simple enough to parse, but the opaque `dict` fields would require reverse-engineering from actual data. Overall, the documentation is adequate for a C-CDA-literate developer but insufficient for a complete, reliable import — primarily due to the undocumented dict fields and lack of sample data.

## 7. Overall Assessment

### Classification

**Standard-based projection with supplemental native data**

The export is primarily a C-CDA document (a standard clinical data projection) supplemented with proprietary CSV files for data that doesn't fit C-CDA (documents, orders, charges). This is not a native database export — it's a C-CDA export extended with 3 supplemental CSV tables. The C-CDA covers standard clinical domains well, and the supplemental CSV adds genuine value for billing charges and orders. However, the export does not expose the vendor's native data model (no database tables, no internal schema), and the 18 C-CDA sections + 3 CSV categories (totaling ~21 entities) are far fewer than what a full database export would reveal from a comprehensive hospital information system.

### Key Findings

1. **Genuine (b)(10) effort, not a repackaged FHIR or minimal C-CDA**: The export uses C-CDA (not FHIR) and includes a supplemental Charges CSV with revenue codes, procedure codes, modifiers, and NDC codes. This is billing data beyond what a standard API or clinical summary would include. This is clearly a dedicated (b)(10) implementation.

2. **C-CDA is inherently limited as an "all EHI" vehicle**: C-CDA was designed for clinical summaries and transitions of care, not for exporting a complete database. 18 C-CDA sections capture standard clinical data well, but they cannot represent the full data model of a comprehensive HIS. The supplemental CSV approach partially addresses this, but only for 3 categories.

3. **Opaque dict fields hide unknown data depth**: 4 fields (`json_data`, `application_data`, `data`, `diagnosis_ids`) are typed as `dict` or `array` with no schema documentation. These could contain significant clinical or operational data that is effectively invisible in the documentation.

4. **No sample data or machine-readable schemas**: The entire specification is a single PDF. No sample export files, no XSD, no JSON Schema. A developer must rely entirely on XML snippets embedded in the document.

5. **Several certified domains lack explicit export coverage**: Family health history ((a)(12)), implantable devices ((a)(14)), and patient portal data ((e)(1)) are certified product capabilities with no clear representation in the export. Payment records are absent despite a Revenue Suite.

### Summary Stats

```
Classification:  Standard-based projection with supplemental native data
Export format:   C-CDA XML + supplemental CSV (in ZIP)
Model type:      Standard projection (C-CDA) + proprietary CSV supplement
Entities:        21 (18 C-CDA sections + 3 CSV categories)
Fields:          188 (146 C-CDA key elements + 42 CSV fields)
Descriptions:    100% (188/188 elements have descriptions)
Sample data:     No (XML examples in PDF only; no downloadable sample files)
Bulk export:     Yes
Domains covered: 13 of 19 applicable domains (3 partial, 3 not covered)
```

### Bottom Line

Lunar provides a well-documented, thoughtful (b)(10) export that goes beyond a minimal C-CDA by adding supplemental CSV files for charges, orders, and documents. This is a genuine effort from a young company, not a compliance checkbox. However, C-CDA is fundamentally a clinical summary format — it cannot represent the full data model of a comprehensive HIS — and the 3 supplemental CSV categories, while valuable, cover only a fraction of what a native database export would reveal. A patient would get a good clinical record and basic billing charges, but may miss payment data, portal messages, family health history, and device records. The biggest structural limitation is the choice of C-CDA as the primary vehicle: it ensures interoperability but caps the depth and breadth of what can be exported.
