# EHI Export Analysis: MDFlow EHR, LLC DBA: MDFlow Systems

**Product**: MDFlow EHR and Patient Care Workflow Management System
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.11.09.3190.MDEP.08.00.1.240402 (CHPL ID 11459)

## 1. Product Context

MDFlow Systems is a small, Miami-based healthcare IT company targeting **value-based care provider groups** — particularly staff-model medical groups operating under capitation contracts in South Florida. Their largest referenced customer, Community Medical Group, operates 18 medical centers with over 70,000 patients.

The certified product (MDFlow EHR v8.0) is a web-based EHR with the following capabilities relevant to EHI scope:

- **Clinical documentation & charting**: encounter documentation, clinical decision support, CPOE for medications
- **Medication management**: e-prescribing, medication reconciliation, drug interaction checking, PBM history
- **Lab integration**: automatic retrieval and incorporation of lab results
- **Immunization tracking**: immunization registry submission (certified (h)(1))
- **Quality/risk adjustment**: HCC/MRA scoring, Star Ratings, HEDIS measures, MIPS/PQRS — a core differentiator for this value-based care product
- **Patient engagement**: patient portal, integrated telemedicine (sessions recorded and stored in patient records), secure messaging
- **Scheduling**: appointment scheduling with transportation management
- **Document management**: referenced in product materials
- **Health information exchange**: HL7, CCD, CCR, C-CDA formats; FHIR API (certified (g)(7), (g)(9), (g)(10))

**Billing status is ambiguous.** The EHR product page does not explicitly list billing, claims submission, or revenue cycle management. The separate Hospitalist Management System product explicitly includes billing/RCM, suggesting the EHR may rely on external billing systems. The product promises "revenue enhancement" but this may refer to risk adjustment coding rather than claims processing.

**Baseline expectation**: A complete EHI export should cover demographics, encounters, medications, labs, immunizations, vitals, allergies, procedures, clinical notes, quality/risk adjustment data, documents, and telemedicine records. If billing data is stored in the EHR, it should also be included.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informative? |
|---|---|---|---|
| `EHIExport.pdf` | 442 KB, 1 page | Primary (b)(10) EHI export documentation (v8.0). Five bullet points describing export format and capabilities. No data dictionary, schema, field definitions, or sample data. | **Low** — nearly zero technical content |
| `EHI-B10-Export.pdf` | 40 KB, 1 page | Supplemental (b)(10) documentation (v8.1). Five statements clarifying the export structure as a ZIP of per-encounter C-CDA ZIPs. No data dictionary. | **Low** — marginally more specific than v8.0 PDF |
| `API-Documentation-g7910.pdf` | 509 KB, 58 pages | FHIR (g)(7)/(g)(9)/(g)(10) API documentation. Covers SMART on FHIR auth and 16 FHIR resource type endpoints. **Not (b)(10) documentation** but provides context on clinical data the system exposes. | **Medium** — useful context, not EHI export |
| `ValidURLs.json` | 4 KB | FHIR Bundle with 2 Endpoint and 2 Organization resources listing FHIR server URLs. (g)(10) Service Base URL artifact. | **None** — not related to EHI export |
| `mandatory-disclosures-page.png` | 2.1 MB | Screenshot of MDFlow's mandatory disclosures page showing links to all artifacts. | **Low** — confirms link structure only |

**Verification notes:**
- Both EHI export PDF URLs remain accessible (HTTP 200 confirmed 2026-02-16).
- `EHIExport.pdf` was created 2024-03-20 by author "Harold Tong"; `EHI-B10-Export.pdf` was created 2025-02-26 by author "Mahesh."
- The mandatory disclosures page link text contains a typo ("EHI Export Iinformation") and garbled text ("Multi-Factor Authentication IJson URLEHI Export Iinformation"), confirming sloppy HTML editing.
- The prior report's claims about file sizes, page counts, and content are verified as accurate.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) is the **primary** format. CSV and PDF are described as available for "special and customized requests" but are entirely undocumented.
- **Structure**: A ZIP file containing per-encounter ZIP archives, each containing a C-CDA document (per `EHI-B10-Export.pdf`).
- **Mechanism**: Not documented. No screenshots, procedural instructions, or UI descriptions. The documentation does not describe how a user initiates an export.
- **Single-patient vs bulk**: The v8.0 document states the system "can export single patient's EHI or a group of patients' EHI."
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### The fundamental problem: no documentation of content

MDFlow provides **zero field-level, table-level, or section-level documentation** of what the EHI export contains. The entire (b)(10) documentation consists of:

- **v8.0 (EHIExport.pdf)**: 1 page, 5 bullet points, 76 words of substance
- **v8.1 (EHI-B10-Export.pdf)**: 1 page, 5 statements, 59 words of substance

Combined, the two documents provide **135 words** of technical content about the export. There is:

- **No data dictionary** — zero documentation of what data elements are exported
- **No field definitions** — no field names, types, constraints, or value sets
- **No C-CDA template documentation** — no specification of which C-CDA sections or templates are populated
- **No sample data** — no example export files
- **No schema** — no machine-readable format description
- **No export instructions** — no description of how to perform an export

### What can be inferred

The export is C-CDA-based, meaning it is constrained to what the C-CDA standard supports. Standard C-CDA sections include:

| Standard C-CDA Section | Likely Present? | Basis |
|---|---|---|
| Patient demographics | Yes | C-CDA header always includes demographics |
| Problems / conditions | Likely | Standard C-CDA section; also in FHIR API |
| Medications | Likely | Standard C-CDA section; e-prescribing is a core feature |
| Allergies | Likely | Standard C-CDA section; drug-allergy checking is certified ((a)(5)) |
| Immunizations | Likely | Standard C-CDA section; immunization registry is certified ((h)(1)) |
| Vital signs | Likely | Standard C-CDA section; in FHIR API |
| Procedures | Likely | Standard C-CDA section; in FHIR API |
| Lab results | Likely | Standard C-CDA section; lab integration is a product feature |
| Clinical notes (narrative) | Likely | C-CDA supports narrative sections |
| Care plans / goals | Possible | In FHIR API; C-CDA supports this section |

**However, "likely" is not "documented."** MDFlow does not confirm which C-CDA sections their exports actually contain, nor what level of detail is included in each section. The above is inference from what C-CDA supports, not evidence from MDFlow's documentation.

### Vendor's own content organization

MDFlow provides no entity/table/field inventory. There is nothing to tabulate.

**The vendor's documentation provides 0 entities, 0 fields, and 0 descriptions.**

### What the FHIR API documentation reveals (for context only)

The 58-page FHIR API documentation ((g)(7)/(g)(9)/(g)(10), not (b)(10)) documents 16 FHIR resource type endpoints:

1. Patient
2. AllergyIntolerance
3. CarePlan
4. CareTeam
5. Condition (Problems / Health Concern)
6. ImplantableDevice
7. DiagnosticReport / Clinical Notes / DocumentReference
8. Observation (Laboratory Results)
9. Goal
10. Immunization
11. Medication
12. Observation (Smoking Status)
13. Procedure
14. Provenance
15. Observation (Vital Signs)
16. Complete Patient Summary (CCDA)

This is the standard USCDI v1 / US Core resource set — exactly what (g)(10) requires. It provides context on what clinical data MDFlow stores, but the (b)(10) EHI export could contain more or less than this depending on their C-CDA implementation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categorization, no entity listing, and no field inventory. The only content claim is that the export "contains data stored in the patient's chart in the SQL database" (EHIExport.pdf) or "contains data from the patient's chart" (EHI-B10-Export.pdf).

The export format is C-CDA, which is a clinical summary standard. By choosing C-CDA as the primary format, the vendor has implicitly limited the export to what C-CDA can represent — which is clinical summary data. C-CDA does not naturally accommodate billing records, risk adjustment scores, quality measures, scheduling data, portal messages, or custom vendor-specific data structures.

The v8.0 document mentions CSV and PDF as alternative formats, but provides no documentation of what they contain or how to request them.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header includes demographics, but no documentation of which fields | Likely present in C-CDA but undocumented; cannot confirm completeness |
| Encounters / visits | ⚠️ Partial | Export is per-encounter (each encounter gets a C-CDA), but encounter metadata detail is undocumented | Structure implies encounters exist; content undocumented |
| Problems / conditions | ⚠️ Partial | Standard C-CDA section; in FHIR API; but not confirmed in (b)(10) docs | Likely present but undocumented |
| Medications / prescriptions | ⚠️ Partial | Standard C-CDA section; e-prescribing is a core feature; but not confirmed | Likely present but undocumented |
| Allergies | ⚠️ Partial | Standard C-CDA section; drug-allergy checking certified ((a)(5)); but not confirmed | Likely present but undocumented |
| Immunizations | ⚠️ Partial | Standard C-CDA section; immunization registry certified ((h)(1)); but not confirmed | Likely present but undocumented |
| Vitals | ⚠️ Partial | Standard C-CDA section; in FHIR API; but not confirmed | Likely present but undocumented |
| Lab results | ⚠️ Partial | Standard C-CDA section; lab integration is a feature; but not confirmed | Likely present but undocumented |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA supports diagnostic reports; in FHIR API; product doesn't explicitly mention imaging | Unclear if product stores imaging data; cannot assess |
| Procedures | ⚠️ Partial | Standard C-CDA section; in FHIR API; but not confirmed | Likely present but undocumented |
| Clinical notes / documents | ⚠️ Partial | C-CDA supports narrative sections; document management is a product feature | Likely present as narrative; structured detail undocumented |
| Care plans / goals | ⚠️ Partial | C-CDA supports care plans; in FHIR API; but not confirmed in (b)(10) | Likely present but undocumented |
| Orders / referrals | ❌ Not covered | CPOE for medications is certified ((a)(1)); no evidence orders are in C-CDA export | Product does CPOE; C-CDA may not capture order details beyond medications |
| Insurance / coverage | ❌ Not covered | Not a standard C-CDA section | Product likely stores insurance info; not exportable via C-CDA |
| Claims / billing | ❌ Not covered | Not a standard C-CDA section | Billing status ambiguous (may be external); if stored, this is a gap |
| Payments | ❌ Not covered | Not a standard C-CDA section | Same as billing — unclear if product stores payment data |
| Consents / directives | ❌ Not covered | C-CDA has an advance directives section, but not confirmed | Possibly present in C-CDA if implemented |
| Patient communications / portal messages | ❌ Not covered | Not a standard C-CDA section; product has patient portal and secure messaging | Product stores portal messages; significant gap |
| Quality/risk adjustment (HCC, HEDIS, Star) | ❌ Not covered | Not a standard C-CDA section | **Major gap**: HCC/MRA scoring, HEDIS, Star Ratings are core product features and part of the designated record set; completely absent from C-CDA export |
| Telemedicine session records | ❌ Not covered | Not a standard C-CDA section; vendor states sessions are "recorded and stored in patient's medical record" | Product explicitly stores telemedicine data; significant gap |

**Note**: All "⚠️ Partial" ratings above reflect that standard C-CDA sections *probably* contain this data, but MDFlow's documentation does not confirm it. Without sample data or C-CDA template documentation, this is inference, not evidence. If MDFlow's C-CDA implementation is complete, these would be "✅ Covered" for the clinical data C-CDA can represent. The rating reflects the documentation gap, not necessarily an export gap.

## 6. Documentation Quality

The documentation quality is **among the worst possible for a certified product**:

- **Usability**: A developer could not build an import from this documentation. The two EHI export PDFs provide no technical specifications whatsoever — no data elements, no field names, no C-CDA template identifiers, no XML structure, no sample data.
- **What's documented**: Only the high-level format (C-CDA in ZIP) and the claim that it contains "data from the patient's chart."
- **What requires guesswork**: Everything else — which C-CDA sections are populated, what data elements are included, how to initiate an export, what the CSV/PDF alternatives contain, and whether any non-C-CDA data is included.
- **Machine-readable artifacts**: None. No schemas, no sample data, no structured documentation.
- **Contrast with FHIR API docs**: The 58-page FHIR API documentation is reasonably detailed with endpoint descriptions, request/response examples, and OAuth2 flow documentation. The disparity (58 pages for (g)(10) vs. 2 pages for (b)(10)) strongly suggests the vendor invested effort in the FHIR API and treated (b)(10) as a compliance checkbox.

**A developer receiving this documentation would know only that they will get C-CDA files in a ZIP.** They would need to examine actual export files (not provided) and have independent knowledge of C-CDA to understand the data structure.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The EHI export is documented as C-CDA, which is a clinical summary standard that covers a subset of what the product stores. The vendor has chosen to repackage their existing C-CDA capability (also used for transitions of care (b)(1)) as the (b)(10) EHI export. This covers standard clinical domains but structurally cannot include billing, risk adjustment, quality measures, telemedicine records, portal messages, or other vendor-specific data that MDFlow stores.

The classification borders on **Minimal/stub** due to the extreme lack of documentation (2 pages, 135 words, no data dictionary, no sample data), but the export itself appears to be a defined deliverable (C-CDA per encounter in ZIP) rather than a stub.

### Key Findings

1. **The export is C-CDA repackaged as (b)(10)**: The primary format is per-encounter C-CDA documents in a ZIP archive — the same format used for transitions of care. This covers standard clinical summary data but cannot represent the full designated record set. (`EHI-B10-Export.pdf`)

2. **Documentation is critically deficient**: The entire (b)(10) documentation is 2 pages containing 135 words of substance, with zero field-level detail, zero C-CDA section specification, zero sample data, and zero export instructions. (`EHIExport.pdf`, `EHI-B10-Export.pdf`)

3. **Quality/risk adjustment data is a major gap**: HCC/MRA scoring, Star Ratings, HEDIS measures, and MIPS/PQRS metrics are core differentiators of this value-based care product and part of the designated record set. C-CDA cannot represent this data, and no alternative export mechanism is documented. (`product-research.md` vs. export artifacts)

4. **Telemedicine and portal data are unexportable**: The vendor explicitly states telemedicine sessions are "recorded and stored in the patient's medical record," and the product includes a patient portal with secure messaging. Neither can be represented in C-CDA. (`product-research.md`)

5. **CSV/PDF alternatives are mentioned but undocumented**: The v8.0 document mentions CSV and PDF formats for "special and customized requests," which could theoretically address some gaps, but there is no documentation of what these contain, how to request them, or whether they cover non-clinical data. (`EHIExport.pdf`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA (per-encounter, in ZIP archive)
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary provided)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (group of patients supported per documentation)
Domains covered: ~8-10 of 19 applicable domains (inferred from C-CDA capabilities; none confirmed by vendor documentation)
```

### Bottom Line

MDFlow's (b)(10) EHI export is a C-CDA clinical summary repackaged as an EHI export, documented in just 2 pages with no data dictionary, no field definitions, and no sample data. A patient would likely receive standard clinical data (demographics, medications, labs, allergies, vitals, etc.) but would miss quality/risk adjustment scores, telemedicine records, portal messages, and potentially billing data — all of which the product stores as part of the designated record set. The single biggest gap is the complete absence of documentation: even for the data that C-CDA does cover, there is no way to verify what is actually exported without examining real export files.
