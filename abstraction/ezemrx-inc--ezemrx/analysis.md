# EHI Export Analysis: ezEMRx Inc

**Product**: ezEMRx  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 10779 (15.02.05.2886.EZEM.01.01.1.220105)

## 1. Product Context

ezEMRx is a certified ambulatory EHR with integrated practice management, billing, inventory management, and patient portal. It serves two markets: **public health departments** (via exclusive partner Custom Data Processing, Inc., deployed in 1,000+ locations) and **private ambulatory clinics** across specialties including primary care, OB/GYN, behavioral health, substance abuse, cardiology, neurology, and urgent care.

The product stores substantial data across multiple domains:

- **Clinical**: charting, medical/social/behavioral/substance abuse history, problem lists, medications, allergies, vitals, lab results, immunizations, treatment plans, clinical notes, e-prescribing, clinical decision support alerts
- **Administrative**: demographics, registration, scheduling, household/family relationships
- **Billing/financial**: electronic claims, claims scrubbing, eligibility verification, sliding fee schedules, payment posting, denial tracking, patient statements, merchant services transactions, RCM records
- **Inventory**: medication/supply tracking with barcodes, vaccine batch records, distribution logs
- **Patient engagement**: portal data, appointment reminders, self-registration
- **Public health reporting**: immunization registry submissions, syndromic surveillance, cancer case reports, quality measures

The product has broad ONC certification (40+ criteria) and was certified in January 2022. A (b)(10) export from this product should cover all these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/ehi-export-page-text.txt` (2,144 bytes) | Extracted text from the rendered EHI export page. Contains regulatory definitions and (b)(10) requirements paraphrased from 45 CFR, plus introductory text promising documentation "about the resulting files from the EHI Export." | Low — no technical content |
| `downloads/ehi-export-page-full.png` (821 KB) | Full-page screenshot of `https://www.ezemrx.com/ehi-export`. Shows header with EHI definition, (b)(10) bullet points, a large (~1,100px tall) blank area where a PDF Viewer Pro widget is embedded but empty, and footer text promising documentation. | Low — confirms absence of content |
| `downloads/ehi-export-page-blank-area.png` (90 KB) | Focused screenshot of the blank PDF Viewer Pro widget area. | Low — confirms empty widget |
| Live website verification (2026-02-16) | Fetched `https://www.ezemrx.com/ehi-export` via web_fetch. Page still returns only regulatory text; no data dictionary, schema, or technical documentation present. | Confirms no change since collection |

**No artifact contained any technical export documentation.** There are no data dictionaries, schemas, sample data files, format specifications, or any description of what the export contains or how it works.

## 3. Export Mechanics

- **Format**: Unknown. No format is specified anywhere in the documentation.
- **Mechanism**: Unknown. The page states the user should be "familiar with the functions and features within ezEMRx to access and execute the EHI export capability," implying a UI-based export exists, but no instructions are provided.
- **Single-patient vs bulk**: The page claims support for both single-patient and patient-population export (listing regulatory requirements for each), but provides no details on how either works.
- **Access constraints or fees**: Unknown. No information provided.

## 4. Export Content: What's In It

**Cannot be determined.** The vendor's EHI export page provides zero information about what the export contains.

The page at `https://www.ezemrx.com/ehi-export` has:
1. A definition of EHI quoting 45 CFR 160.103 and 164.501
2. Bullet points paraphrasing (b)(10) regulatory requirements (e.g., "Must include all EHI for a single patient," "Must be electronic and in a computable format")
3. An **empty PDF Viewer Pro widget** — a Wix-hosted placeholder where a document (presumably a data dictionary or format specification) was intended to be embedded but was never uploaded
4. Introductory text stating: "The documentation listed on this page is intended to provide the user an understanding of the resulting files from the EHI Export. It will explain how to read the files, understand the meaning behind fields, and offer other insight to properly make use of this extensive amount of information."

The introductory text (#4) strongly implies that a data dictionary or format guide was planned — it references "resulting files," "meaning behind fields," and "extensive amount of information." This document was never published. The empty PDF viewer widget confirms a document was intended to be placed there.

### Vendor's own content organization

No content exists to organize. There are:
- 0 entities/tables documented
- 0 fields documented
- 0 data types specified
- 0 relationships described
- 0 sample data files
- 0 machine-readable schemas

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Nothing is documented.** The vendor provides no information about what data the export includes. The only content on the EHI export page is regulatory boilerplate and an empty document placeholder.

### 5b. Standardized domain coverage (top-down)

Because no export documentation exists, every domain must be assessed as "unclear." We cannot determine whether the actual export (which presumably exists in the software, given it was certified) covers any of these domains.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores demographics; cannot assess export |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounter data; cannot assess export |
| Problems / conditions | ❓ Unknown | No documentation | Product stores problem lists; cannot assess export |
| Medications / prescriptions | ❓ Unknown | No documentation | Product has e-prescribing; cannot assess export |
| Allergies | ❓ Unknown | No documentation | Product stores allergies; cannot assess export |
| Immunizations | ❓ Unknown | No documentation | Product stores immunization records; cannot assess export |
| Vitals | ❓ Unknown | No documentation | Product stores vitals; cannot assess export |
| Lab results | ❓ Unknown | No documentation | Product stores lab results; cannot assess export |
| Procedures | ❓ Unknown | No documentation | Product stores procedures; cannot assess export |
| Clinical notes / documents | ❓ Unknown | No documentation | Product stores clinical notes; cannot assess export |
| Care plans / goals | ❓ Unknown | No documentation | Product stores treatment plans; cannot assess export |
| Orders / referrals | ❓ Unknown | No documentation | Product likely stores orders; cannot assess export |
| Insurance / coverage | ❓ Unknown | No documentation | Product stores insurance/eligibility data; cannot assess export |
| Claims / billing | ❓ Unknown | No documentation | Product has full billing/RCM; cannot assess export |
| Payments | ❓ Unknown | No documentation | Product tracks payments/adjustments; cannot assess export |
| Consents / directives | ❓ Unknown | No documentation | Cannot determine if product stores these |
| Patient communications | ❓ Unknown | No documentation | Product has patient portal; cannot assess export |
| Specialty-specific (behavioral health, substance abuse, public health) | ❓ Unknown | No documentation | Product has specialty templates; cannot assess export |
| Inventory | ❓ Unknown | No documentation | Product has inventory management; cannot assess export |

## 6. Documentation Quality

The EHI export documentation is **effectively nonexistent**. Assessment:

- **Can a developer understand and use the export?** No. There is no information about the export format, structure, content, or how to interpret the data.
- **What's well-documented?** Nothing. The page contains only regulatory definitions copied from 45 CFR.
- **Machine-readable artifacts?** None. No schemas, no sample data, no JSON/XML/CSV specifications.
- **Could someone build an import from this?** No. A recipient of an ezEMRx EHI export would have no public documentation to help interpret the data.

The presence of the empty PDF viewer widget and the introductory text ("It will explain how to read the files, understand the meaning behind fields") indicates the vendor planned to publish documentation but never completed or uploaded it. The product was certified in January 2022 — over 4 years ago — so this is not a temporary gap.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is entirely empty. There is literally no information about what the export contains — no data dictionary, no entity list, no field inventory, no sample data. It is impossible to assess coverage because nothing is documented. The page is a compliance shell: it exists at the registered URL and contains regulatory language, but provides zero technical content about the actual export.

**Axis 2 — Export approach: Unclear/undetermined**

With no documentation of any kind, it is impossible to determine whether ezEMRx built a purpose-built EHI export or repackaged an existing clinical exchange export. The page does not reference C-CDA, FHIR, or any specific standard, which means it doesn't have the telltale signs of a repackaged (g)(10) export — but it also doesn't show any evidence of a purpose-built solution. The introductory text's reference to "resulting files" and "meaning behind fields" suggests some export mechanism exists in the software, but its nature is completely undocumented.

### Key Findings

1. **Empty documentation page**: The EHI export page (`ehi-export-page-full.png`) contains an empty PDF Viewer Pro widget where documentation was clearly intended to be displayed. The introductory text promises to "explain how to read the files, understand the meaning behind fields" — but no such document was ever uploaded. This is the single most telling artifact.

2. **Zero technical content**: Across all artifacts examined, there are 0 entities, 0 fields, 0 data types, 0 relationships, and 0 sample data files documented. The only text content is regulatory definitions from 45 CFR and paraphrased (b)(10) requirements.

3. **Long-standing gap**: The product was certified in January 2022. The absence of export documentation has persisted for over 4 years, indicating this is not a temporary oversight.

4. **Significant product scope**: ezEMRx is a full-featured EHR with billing, inventory, public health reporting, and specialty-specific templates deployed across 1,000+ public health locations. The breadth of data that should be covered by a (b)(10) export is substantial, making the documentation gap more consequential.

5. **No alternative documentation found**: Web searches, Wayback Machine checks, and partner site (CDP) examination revealed no EHI export documentation published anywhere else.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   Unknown
Entities:        0 (no data dictionary)
Fields:          0
Descriptions:    N/A
Sample data:     No
Bulk export:     Claimed but undocumented
Domains covered: 0 of 19 verifiable (all unknown due to absent documentation)
```

### Bottom Line

ezEMRx's EHI export documentation page is an empty shell — it contains regulatory boilerplate and an unfilled PDF viewer placeholder where a data dictionary was clearly intended but never published. Despite being certified for over 4 years and deployed across 1,000+ public health locations, the vendor provides zero information about what the export contains, what format it uses, or how to interpret the data. A patient or provider receiving this export would have no public documentation to help them understand or use it.
