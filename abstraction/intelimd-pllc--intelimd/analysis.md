# EHI Export Analysis: inteliMD PLLC

**Product**: inteliMD
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3211.INTL.01.00.1.241127

## 1. Product Context

inteliMD is a cloud-based, integrated EHR platform developed by inteliMD PLLC, a small Phoenix-based vendor. The product combines electronic medical records, telemedicine/telehealth, e-prescribing, scheduling, billing, and a patient portal into a single platform. Per ONC certification documentation, it is "specifically designed for the post-acute and primary segment of care" and optimized for skilled nursing facilities, home health settings, and primary care physicians. The company also operates InteliPsych, a telepsychiatry service that appears to be a primary user of the platform.

**Data domains the product stores** (based on certified criteria, features, and documentation):
- **Clinical**: Patient demographics, medications/prescriptions (CPOE + e-prescribe), lab orders (CPOE), imaging orders (CPOE), drug allergies, family health history, implantable devices, clinical notes/dictation, immunizations, vitals, problems, care plans
- **Telemedicine**: Video consultation records, secure messages (provider-patient and provider-provider)
- **Financial/billing**: Credit card processing, patient electronic billing, electronic claims, insurance eligibility verification, payment processing
- **Patient portal**: Registration, patient-captured health information
- **Administrative**: Provider scheduling, patient scheduling, form templates, specialty illness lists, CDS rules

The product was certified on November 27, 2024 (version 1), covering 30 ONC criteria. It is priced at $49–$299/physician/month, targeting small practices and individual providers. Very limited market presence — no third-party reviews exist.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/b10-ehi-export.pdf` | 5-page PDF titled "170.315(b)(10) Electronic Health Information export." Generated via Google Docs. Contains procedural instructions with screenshots for single-patient and bulk export, brief description of C-CDA output, 3 HTTP error codes, and product identification. **No data dictionary, no schema, no sample data, no C-CDA section mapping.** | Low — demonstrates export button exists but provides no detail on content |

This is the **only artifact** available. No additional documentation, sample exports, schemas, or data dictionaries were found at the vendor's site.

## 3. Export Mechanics

- **Format**: C-CDA XML for structured data; PDF as an alternative for single patients. Bulk export produces a ZIP of C-CDA XML files.
- **Mechanism**: UI-based. Superadmin logs into the inteliMD portal, authenticates via OTP, navigates to the Patient List, and either (a) clicks the eye icon for a single patient then downloads C-CDA or PDF, or (b) clicks "Download Records" for bulk export.
- **Single-patient**: Yes — via Patient List → eye icon → "C-CDA" or "PDF" button.
- **Bulk export**: Yes — "Download Records" button generates C-CDA XML for all patients, downloaded as ZIP. A countdown timer indicates progress.
- **Access constraints**: Requires "system level user (superadmin)" credentials with OTP verification.
- **Fees**: Not mentioned in documentation.
- **C-CDA document type**: Not specified. No template OIDs, implementation guide version, or section identifiers are provided.

## 4. Export Content: What's In It

### What the documentation says

The PDF provides only vague prose descriptions of export content:

1. **Purpose and Scope section**: "export all patient's health information in a standardized format" including "demographics, clinical notes, medications, lab results etc"
2. **Patient EHI C-CDA XML section**: "comprehensive health data such as medical history, test results, treatment plans, and other relevant health records"

These are the **only** content descriptions in the entire document. No C-CDA sections are enumerated. No field mappings are provided. No data dictionary exists at any level of granularity.

### What screenshots reveal

The Profile Summary popup (PDF page 3) shows 12 fields, all demographic/metadata:

| Field | Example Value |
|---|---|
| Patient | Reyansh Saini |
| Date Of Birth | November 9, 1972 |
| Sex | Male |
| Race | (empty) |
| Ethnicity | (empty) |
| Contact Info | Primary Home: A S Eventech IT Pahe, Dehardun, AK 24800, US |
| Patient IDs | 0000001142 1.3.6.1.4.1.36517.1|
| Document Id | PatientSummary-Header-0000001142 |
| Document Created | November 23, 2023, 10:11:00 +0530 |
| Performer | Abhinav Mishra |
| Author | Abhinav Mishra, Mean Healthcare |
| Contact Info (Work) | Work Place: A S Eventech IT Park |

This is just the C-CDA header/demographic section preview. The clinical content of the C-CDA document is not shown or described anywhere.

### Vendor's own content organization

There is **no vendor-provided content organization**. No tables, no entities, no field lists, no data dictionary. The vendor provides zero field-level documentation for the export.

The sidebar navigation visible in the screenshot hints at the application's data domains (Registered Patients, Form Template, Global Specialty Illness, Manage Medication, Billed Inactive, CDS Rules, etc.), but none of these are mapped to export content.

### What's actually unknown

Because no data dictionary, sample export, or C-CDA section mapping is provided, it is impossible to determine:
- Which C-CDA sections are included (Problems? Medications? Allergies? Procedures? Immunizations? Results?)
- Whether any vendor-specific extensions or custom sections exist
- Whether the C-CDA includes data beyond standard clinical summary sections
- What level of detail each section contains
- Whether billing, telemedicine, or specialty data is represented in any form

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes their export in the broadest possible terms: "all patient's health information" including "demographics, clinical notes, medications, lab results etc." No further detail is provided. The word "etc" is doing enormous work — there is no way to verify what it encompasses.

The export format is C-CDA XML, which is a clinical document standard. Standard C-CDA documents (CCD, Continuity of Care Document) typically include: patient demographics, problems/conditions, medications, allergies, immunizations, procedures, results/labs, vital signs, and clinical notes. C-CDA does **not** naturally represent billing records, claims, telemedicine session data, secure messages, form templates, or administrative data.

Without a sample export or section mapping, we can only assume the C-CDA contains standard clinical summary sections. There is no evidence of any data beyond what a standard C-CDA document would contain.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 12 fields visible in Profile Summary screenshot; likely in C-CDA header | Probably included but no field-level verification possible |
| Encounters / visits | ⚠️ Partial | Not mentioned; may be in C-CDA if using CCD template | Product stores encounters; coverage unknown |
| Problems / conditions | ⚠️ Partial | Not mentioned; standard C-CDA section | Likely in C-CDA but unverified |
| Medications / prescriptions | ⚠️ Partial | "medications" mentioned in prose | Product has CPOE + e-prescribe; C-CDA may include med list but not full Rx history |
| Allergies | ⚠️ Partial | Not mentioned; standard C-CDA section | Likely in C-CDA but unverified |
| Immunizations | ⚠️ Partial | Not mentioned; standard C-CDA section | Product certified for (f)(1) immunization reporting; C-CDA may include but unverified |
| Vitals | ⚠️ Partial | Not mentioned; standard C-CDA section | Likely in C-CDA but unverified |
| Lab results | ⚠️ Partial | "lab results" mentioned in prose | Product has CPOE for labs + LIMS integration; coverage depth unknown |
| Imaging / diagnostic reports | ⚠️ Partial | Not mentioned | Product has CPOE for imaging (a)(3); coverage unknown |
| Procedures | ⚠️ Partial | Not mentioned; standard C-CDA section | Likely in C-CDA but unverified |
| Clinical notes / documents | ⚠️ Partial | "clinical notes" mentioned in prose | Product has dictation; coverage depth unknown |
| Care plans / goals | ⚠️ Partial | "treatment plans" mentioned in prose | Product targets post-acute care where care plans are central; coverage unknown |
| Orders / referrals | ❌ Not covered | No mention | Product has CPOE for meds/labs/imaging; no evidence orders are in export |
| Insurance / coverage | ❌ Not covered | No mention | Product has eligibility verification; not in export |
| Claims / billing | ❌ Not covered | No mention | Product has electronic claims, patient billing, credit card processing; significant gap |
| Payments | ❌ Not covered | No mention | Product processes payments; not in export |
| Consents / directives | ❌ Not covered | No mention | "Legal Documents" in sidebar suggests product stores these; not in export |
| Patient communications / portal messages | ❌ Not covered | No mention | Product has secure messaging and patient portal; not in export |
| Specialty-specific (post-acute/SNF/home health) | ❌ Not covered | No mention | Product specifically targets SNF/home health; "Global Specialty Illness" and "Form Template" visible in sidebar suggest specialty data exists; not in export |

**Note**: Almost every "Partial" rating above is speculative — based on the assumption that the C-CDA follows standard templates. There is no direct evidence from the documentation for any specific clinical domain coverage. A more honest assessment would rate nearly every domain as "Unclear."

## 6. Documentation Quality

The documentation is a **5-page procedural guide** — essentially a "how to click the export button" document with screenshots. It is not technical documentation.

**What exists**:
- Step-by-step UI instructions with 4 screenshots (2 pages)
- One paragraph describing C-CDA content in vague terms (1 paragraph)
- 3 HTTP error codes (400, 500, 401)
- Product identification (version, certificate number)

**What's missing**:
- Data dictionary at any level of granularity
- C-CDA section/template mapping
- Field-level specifications (types, constraints, value sets)
- Sample export files
- API documentation (despite error codes implying an API exists)
- Relationship documentation
- Completeness inventory (what's in vs. what's out)
- Any machine-readable artifacts (schemas, sample data)

**Could a developer build an import from this documentation?** No. A developer would receive C-CDA XML files with zero context about what sections or custom elements to expect. They would need to reverse-engineer the XML structure entirely. The documentation does not even specify which C-CDA document type (CCD, Discharge Summary, etc.) is generated.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The entire content specification is two vague prose sentences mentioning "demographics, clinical notes, medications, lab results etc" and "medical history, test results, treatment plans, and other relevant health records." No data dictionary, no field list, no section mapping. The use of C-CDA as the export format inherently limits coverage to clinical summary data — C-CDA cannot naturally represent billing records, claims, telemedicine sessions, secure messages, form templates, or the post-acute/SNF-specific data that this product is specifically designed to store. The sidebar navigation reveals at least 17 application modules including "Billed Inactive," "Form Template," "Global Specialty Illness," "Legal Documents," and "Manage Medication" — none of which are addressed in the export documentation. This product has billing capabilities (electronic claims, patient billing, credit card processing, eligibility verification) that are almost certainly absent from the C-CDA export.

**Axis 2 — Export approach: Repackaged existing export**

The export is standard C-CDA XML — the same format used for transitions of care under (b)(1)/(b)(2), which inteliMD is also certified for (using the EMR Direct Interoperability Engine). The documentation provides no evidence that the (b)(10) export includes anything beyond what their existing C-CDA transitions-of-care exchange already produces. There is no product-specific data dictionary, no custom C-CDA extensions, no non-clinical data, and no indication that the vendor built anything purpose-specific for (b)(10). The document title references "PatientSummary-Header" in the screenshot, consistent with a standard CCD/patient summary document. This appears to be the vendor's existing C-CDA capability relabeled as (b)(10).

### Key Findings

1. **No data dictionary exists.** The entire (b)(10) documentation is a 5-page how-to guide with screenshots. There are zero field-level specifications, zero C-CDA section mappings, and zero sample exports. This is the thinnest possible documentation that could be filed for certification.

2. **Export is standard C-CDA XML — likely the same as transitions of care.** inteliMD is certified for (b)(1)/(b)(2) transitions of care using EMR Direct's C-CDA engine. The (b)(10) export uses the same C-CDA format with no documented extensions or additional content. The "PatientSummary-Header" document ID in the screenshot is consistent with a standard patient summary document.

3. **Billing and financial data are almost certainly excluded.** The product has electronic claims, patient billing, credit card processing, and eligibility verification. C-CDA does not represent billing data, and no alternative format is offered for non-clinical data. This is a significant gap for a product that lists billing as a core feature.

4. **Post-acute and specialty data are unaddressed.** The product is specifically designed for SNF and home health settings, which require care plans, functional assessments, and specialty documentation. The sidebar shows "Global Specialty Illness" and "Form Template" modules, but the export documentation makes no mention of specialty-specific or post-acute data.

5. **The documentation is a compliance checkbox.** The PDF demonstrates that an export button exists in the UI. It provides no technical content. A receiving system could not use this documentation to understand, validate, or import the exported data.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML (single patient or ZIP for bulk); PDF (single patient)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (ZIP of C-CDA XML files)
Domains covered: 0 confirmed; ~9 assumed from standard C-CDA of 19 applicable
```

### Bottom Line

inteliMD's (b)(10) export is a standard C-CDA clinical summary with no data dictionary, no schema documentation, and no evidence of content beyond what their existing transitions-of-care exchange provides. For a product that stores billing data, telemedicine records, specialty assessments, and administrative data for post-acute care settings, exporting only a C-CDA summary represents a small fraction of the designated record set. The documentation is the bare minimum needed to claim a checkbox — a patient or provider receiving this export would get a clinical summary, not their complete health record.
