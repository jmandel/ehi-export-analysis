# EHI Export Analysis: inteliMD PLLC

**Product**: inteliMD
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.3211.INTL.01.00.1.241127

## 1. Product Context

inteliMD is a cloud-based integrated healthcare platform combining EHR, telemedicine, e-prescribing, scheduling, billing, and patient portal capabilities. Per the ONC certification page, it is "specifically designed for the post-acute and primary segment of care," optimized for skilled nursing facilities, home health settings, and primary care physicians. The company (inteliMD PLLC) also operates InteliPsych, a telepsychiatry clinical services arm, suggesting the platform may also be used internally for behavioral health workflows.

The product was ONC-certified on November 27, 2024 (version 1), with 30+ certified criteria. Key data domains the product stores:

- **Clinical**: Demographics, medications/prescriptions (e-prescribing), lab orders, imaging orders, drug allergies, family health history, implantable devices, clinical notes (with voice dictation), immunizations, vital signs, problems/conditions
- **Telemedicine**: Video consultation records, secure messaging
- **Billing/Financial**: Insurance verification, electronic claims, patient billing/statements, credit card processing
- **Administrative**: Provider scheduling, patient scheduling, multi-site management
- **Patient portal**: Patient-generated health information, registration data

The sidebar menu visible in the PDF screenshots (page 3) reveals additional modules: Form Template, Inquiries, Global Speciality Illness, Manage Medication, Courses, Manage CSR, Billed Inactive, Deactivated Business, Medication Improvement, Manage Tickets, CDS Rules — indicating the product has more functional depth than the marketing website suggests.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b10-ehi-export.pdf` (432 KB, 5 pages) | The sole EHI export documentation artifact. A Google Docs-produced PDF titled "170.315(b)(10) Electronic Health Information export." Contains regulatory boilerplate (p1), UI login/export instructions with screenshots (pp2-3), bulk export description (p4), error codes table (p4), and product identification (p5). **No data dictionary, no schema, no sample data, no C-CDA section mapping.** | Low — documents only that an export button exists, not what it exports |

This is the **only artifact** available. There is no data dictionary, no schema documentation, no sample export files, no C-CDA template specifications, and no supplementary documentation of any kind. The `files.json` manifest confirms only this single PDF was found and downloaded.

## 3. Export Mechanics

- **Format**: C-CDA XML (primary), PDF (secondary, single-patient only). Bulk export produces a ZIP of C-CDA XML files.
- **Mechanism**: UI-based. Requires superadmin login with OTP verification to registered mobile number.
  - *Single patient*: Navigate to Patient List → click eye icon on patient row → "Patient Chart Summary" popup → click "C-CDA" or "PDF" button to download.
  - *Bulk*: Click "Download Records" button on Patient List page → server generates C-CDA XML files with countdown timer → ZIP auto-downloads.
- **Single-patient**: Yes (C-CDA or PDF)
- **Bulk**: Yes (ZIP of C-CDA XML files for all patients)
- **Access constraints**: Restricted to "system level user (superadmin)" only. OTP-based two-factor authentication required.
- **Fees**: Not mentioned in documentation.

## 4. Export Content: What's In It

### What the documentation says

The documentation provides only vague, high-level descriptions of export content:

1. **Purpose and Scope** (p1): "export all patient's health information in a standardized format" with data types including "demographics, clinical notes, medications, lab results etc"
2. **Patient EHI C-CDA XML** (p4): "comprehensive health data such as medical history, test results, treatment plans, and other relevant health records"

These are the **only two statements** about content in the entire document. There is no enumeration of C-CDA sections, no listing of data elements, no template OIDs, no field mappings, and no indication of which C-CDA document type (CCD, Discharge Summary, etc.) is generated.

### What the screenshots reveal

The Patient Chart Summary popup (page 3, bottom screenshot) shows these fields for a sample patient:

| Field | Sample Value |
|---|---|
| Patient | Reyansh Saini |
| Date Of Birth | November 9, 1972 |
| Sex | Male |
| Race | (empty) |
| Ethnicity | (empty) |
| Contact Info | Primary Home: A 5 Evontech IT Park, Dehardun, AK 24800, US |
| Patient IDs | 0000001142 1.3.6.1.4.1365711 |
| Document Id | PatientSummary-Header-0000001142 |
| Document Created | November 23, 2023, 10:11:00 -0530 |
| Performer | Abhinav Mishra |
| Author | Abhinav Mishra, Mean Healthcare |

The patient list shows columns: S.No, Patient Name, Contact Details, MRN, SSN, Registered Date — with 6 sample patients visible.

This is the extent of verifiable content information. The Document Id format ("PatientSummary-Header-0000001142") suggests the C-CDA document type may be a Patient Summary / CCD, but this is inferential.

### Vendor's own content organization

The vendor provides **no content organization** — no categories, no entity list, no field inventory. The only structured information is the vague mention of data types in prose:

| Data Type Mentioned | Source | Detail Level |
|---|---|---|
| Demographics | Purpose and Scope (p1) | None — no fields listed |
| Clinical notes | Purpose and Scope (p1) | None |
| Medications | Purpose and Scope (p1) | None |
| Lab results | Purpose and Scope (p1) | None |
| Medical history | C-CDA XML section (p4) | None |
| Test results | C-CDA XML section (p4) | None |
| Treatment plans | C-CDA XML section (p4) | None |

**No data dictionary exists.** There are zero entities/tables documented, zero fields with descriptions, zero type definitions, zero relationships, zero value sets. The documentation provides no machine-readable artifacts whatsoever.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor claims the export contains "all patient's health information" but provides no evidence to support this claim. The documentation names 7 vague data categories in prose (demographics, clinical notes, medications, lab results, medical history, test results, treatment plans) with no field-level detail.

The export format is C-CDA XML, which has well-known structural limitations. A standard C-CDA CCD document supports sections for: allergies, medications, problems, procedures, results (labs), vital signs, immunizations, encounters, functional status, plan of care, and social history. It does **not** natively represent billing records, insurance claims, telemedicine session data, appointment scheduling, custom forms, or specialty assessments.

Without sample export files or C-CDA section enumeration, it is impossible to verify which C-CDA sections are actually populated. The vendor's documentation gives no indication they've extended C-CDA beyond standard sections to cover their full data model.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Mentioned in prose; Patient Chart Summary screenshot shows name, DOB, sex, race, ethnicity, address | Likely present in C-CDA header, but no field-level detail documented |
| Encounters / visits | ⚠️ Partial | Not mentioned, but standard C-CDA may include encounters section | Product stores visit/encounter data; unclear if exported |
| Problems / conditions / diagnoses | ⚠️ Partial | "Medical history" mentioned in prose | Likely present as standard C-CDA section but unverified |
| Medications / prescriptions | ⚠️ Partial | "Medications" mentioned in prose | Likely present as standard C-CDA section; product has full e-prescribing — unclear if Rx history is complete |
| Allergies | ⚠️ Partial | Not explicitly mentioned; standard C-CDA section | Product certified for drug-allergy checks (a)(4); allergy data likely in C-CDA but unconfirmed |
| Immunizations | ⚠️ Partial | Not mentioned; standard C-CDA section | Product certified for immunization registry reporting (f)(1); likely in C-CDA but unconfirmed |
| Vitals | ⚠️ Partial | Not mentioned; standard C-CDA section | Likely present but unconfirmed |
| Lab results | ⚠️ Partial | "Lab results" and "test results" mentioned in prose | Likely present as C-CDA results section but no detail |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned | Product has CPOE imaging (a)(3); no evidence imaging reports are exported |
| Procedures | ⚠️ Partial | Not mentioned; standard C-CDA section | May be present in C-CDA but unconfirmed |
| Clinical notes / documents | ⚠️ Partial | "Clinical notes" mentioned in prose | Product has voice dictation notes; unclear if full note text is in C-CDA or just structured data |
| Care plans / goals | ⚠️ Partial | "Treatment plans" mentioned in prose | May map to C-CDA plan of care section; post-acute focus suggests care plans are significant |
| Orders / referrals | ❌ Not covered | Not mentioned | Product has CPOE for meds, labs, imaging; no evidence orders are exported |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product does insurance eligibility verification; not a natural C-CDA domain — likely missing |
| Claims / billing | ❌ Not covered | Not mentioned | Product does electronic claims and patient billing; C-CDA cannot represent this — significant gap |
| Payments | ❌ Not covered | Not mentioned | Product has credit card processing; not in C-CDA — likely missing |
| Consents / directives | ❌ Not covered | Not mentioned | No evidence |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Product has secure messaging and patient portal; C-CDA cannot represent this — likely missing |
| Specialty-specific (post-acute/SNF/home health) | ❌ Not covered | Not mentioned | Product is "specifically designed for post-acute and primary care" per ONC page; any SNF assessments, home health plans, or specialty forms are likely not in C-CDA — significant gap |
| Specialty-specific (psychiatry/telepsychiatry) | ❌ Not covered | Not mentioned | InteliPsych arm suggests psychiatric assessment data; not in C-CDA — likely missing |
| Family health history | ❌ Not covered | Not mentioned | Product certified under (a)(12); no evidence it's in export |
| Implantable devices | ❌ Not covered | Not mentioned | Product certified under (a)(14); no evidence it's in export |

**Summary**: Of 20 applicable domains, 0 are confirmed as fully covered. 8 are assessed as partially/likely covered (based on C-CDA standard sections and vague prose mentions, not verified evidence). 12 domains have no evidence of coverage, including billing, insurance, specialty clinical data, and patient communications — all of which the product stores.

## 6. Documentation Quality

The documentation is **critically deficient** for its intended purpose:

- **No data dictionary**: Zero entities, tables, or fields documented
- **No C-CDA specifications**: No document type identified, no sections enumerated, no template OIDs, no implementation guide version referenced
- **No schema or sample data**: No machine-readable artifacts of any kind
- **No field-level mapping**: Impossible to determine what data elements are included in the export
- **No completeness statement**: No mapping of product data domains to export coverage
- **No API documentation**: Error codes (400, 500, 401) hint at an API but no endpoints, request formats, or authentication details are documented

The document is essentially a **5-page screenshot walkthrough** showing how to click an export button. A developer receiving a C-CDA export from inteliMD would need to reverse-engineer the XML structure entirely. There is no documentation that would enable building an import pipeline.

The PDF was produced with Google Docs Renderer, suggesting it was created quickly as a compliance artifact rather than as genuine technical documentation.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The documentation is too thin to meaningfully assess the export's completeness. The vendor provides a single 5-page PDF that documents only the existence of an export button, with no data dictionary, no schema, no sample data, and no specification of what C-CDA sections or data elements are included. The export format (C-CDA XML) inherently limits coverage to clinical summary data, leaving billing, insurance, telemedicine, specialty assessments, and other significant data domains unaddressed.

### Key Findings

1. **Export is C-CDA XML only — a standard clinical summary format, not a native data export.** C-CDA is structurally incapable of representing billing records, insurance claims, telemedicine session data, secure messages, custom forms, or specialty assessments. For a product with billing, e-prescribing, telemedicine, and post-acute care capabilities, this represents a fundamental coverage limitation. (Source: `b10-ehi-export.pdf`, pp1-4)

2. **Documentation contains zero field-level detail.** The entire specification of export content is two vague sentences mentioning "demographics, clinical notes, medications, lab results etc" and "medical history, test results, treatment plans." No C-CDA sections, template OIDs, or data elements are identified. (Source: `b10-ehi-export.pdf`, pp1, 4)

3. **No data dictionary, schema, or sample data exists.** This is the only artifact available for the entire (b)(10) certification. A developer could not build an import from this documentation. (Source: `files.json` — single file downloaded; no additional documentation found on vendor website)

4. **Bulk export is supported.** The "Download Records" button generates a ZIP of C-CDA XML files for all patients, which at least provides a population-level export mechanism. This is better than many vendors who only support single-patient export. (Source: `b10-ehi-export.pdf`, p4)

5. **The product has significantly more depth than the export covers.** The sidebar navigation visible in screenshots shows 17 modules (Form Template, Global Speciality Illness, Manage Medication, CDS Rules, etc.), and the product is certified for 30+ criteria. The C-CDA export almost certainly captures only a fraction of the product's data model. (Source: `b10-ehi-export.pdf`, p3 screenshot)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA XML (single), ZIP of C-CDA XML (bulk), PDF (single patient only)
Model type:      Standard projection (C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes
Domains covered: 0 of 20 confirmed; 8 of 20 likely partial (unverifiable)
```

### Bottom Line

inteliMD's EHI export is a C-CDA clinical summary repackaged as a (b)(10) export, with documentation so thin it amounts to a screenshot walkthrough of an export button. A patient or provider would receive a C-CDA XML file containing standard clinical summary data but would almost certainly miss billing records, insurance information, telemedicine session data, specialty assessments (post-acute, psychiatric), and any custom data the product stores beyond what fits in a standard C-CDA document. The single biggest gap is the complete absence of documentation — without a data dictionary or sample data, it is impossible to verify what the export actually contains.
