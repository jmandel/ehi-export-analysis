# EHI Export Analysis: Edvak Technologies Inc

**Product**: Edvak EHR v1  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3230.Edva.0v.00.1.250613 (CHPL #11656)

## 1. Product Context

Edvak EHR is a cloud-based ambulatory EHR and practice management platform from Edvak Technologies Inc (Houston, TX), targeting solo practitioners and small-to-mid-sized clinics. It was certified June 13, 2025, with 33 ONC criteria including (b)(10).

The product has five integrated modules relevant to assessing export completeness:

1. **Advanced EHR (Clinical)**: AI-powered documentation, e-prescribing (Surescripts), CPOE for meds/labs/imaging, drug interaction checks (Medi-Span), clinical decision support, comprehensive charting.
2. **Practice Management**: Scheduling, task management, referral management, document management, fax management.
3. **Patient Engagement**: Patient portal, two-way SMS, phone calls, patient intake forms, automated care reminders, telehealth.
4. **Revenue Cycle Management / Billing**: ICD/CPT code capture, real-time insurance eligibility, claims submission, denial analytics, payment processing.
5. **Analytics & Reporting**: Practice insights, standard and advanced reports, CQM reporting.

The Facesheet screenshot (SP_2.png) confirms the product stores data across tabs: **Facesheet, Demographics, Documents, Encounter Notes, Billing, Referrals**, with Facesheet sections for Medications, Problems, Vitals, Allergies, Labs & Imaging, Past History, Immunizations, Goals, Assessments, and Interventions. Additional UI buttons visible: Forms & Letters, Patient Education, Tasks, Notes.

A genuine (b)(10) export for this product should cover clinical data, billing/claims, insurance, referrals, documents, patient communications, and intake forms — all data domains the product stores about patients.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `ehi-export-page.html` (50 KB) | Main EHI export documentation page. Single HTML page describing single-patient and population-level C-CDA export workflows with embedded screenshot references. Lists 10 data domains. | **Primary source** — but very thin |
| `screenshots/SP_2.png` (64 KB) | Facesheet view showing "Export CCDA" button and patient data tabs (Facesheet, Demographics, Documents, Encounter Notes, Billing, Referrals) | **Key evidence** — reveals product stores more than export covers |
| `screenshots/MP_1.png` (66 KB) | Analytics screen showing CCDA tab for bulk export. Tabs: My Collection, Reports Library, Meaningful Use, Quality, Promoting Interoperability, CCDA, Audit, Activity, Downloads | Confirms bulk export mechanism |
| `screenshots/MP_7A.png`, `MP_4.png` (114 KB, 79 KB) | Patient selection panel for bulk export with checkboxes and Select All | Confirms bulk capability |
| `screenshots/MP_7.png` (36 KB) | ZIP file contents showing 4 individual C-CDA files (14–33 KB each) | Confirms per-patient C-CDA files in ZIP |
| `screenshots/SP_1.png` (128 KB) | Patient list with 40 patients | UI context |
| `screenshots/SP_3.png`, `MP_6.png` (26–27 KB) | File save dialogs | Confirms download mechanism |
| `screenshots/SP_!A.png`, `MP_1A.png` (176 KB, 108 KB) | Dashboard navigation screenshots | UI context |
| `ccda-api-introduction-1018024m0.html` (93 KB) | CCDA API introduction. Lists 5 C-CDA document types (CCD, Discharge Summary, Referral Note, Consultation Note, Progress Note). References "G9 certification standard." | Useful — confirms C-CDA scope |
| `ccda-api-ccda-retrieval-16935528e0.html` (123 KB) | CCDA Retrieval endpoint. Shows truncated CCD XML example with header and demographics only (patientRole with name, gender, DOB, race, address, telecom, language). | Useful — only sample of export content |
| `ccda-api-generate-token-16915497e0.html` (117 KB) | OAuth token generation endpoint | Confirms API access mechanism |
| `ccda-api-authentication-access-1019424m0.html` (84 KB) | OAuth 2.0 bearer token auth description | Access mechanism |
| `ccda-api-errors-1019029m0.html` (81 KB) | Error codes documentation | Minimal relevance |
| `ccda-api-apis-3752591f0.html` (78 KB) | API overview listing Generate Token and CCDA Retrieval endpoints | Minimal relevance |
| `screenshots/ehi-export-page-full.png` (1.2 MB) | Full-page browser screenshot of EHI export documentation | Visual confirmation |

**Most informative**: `ehi-export-page.html` (the only export documentation), `SP_2.png` (reveals product scope), and `ccda-api-ccda-retrieval-16935528e0.html` (only sample data).  
**Least informative**: Error codes page, API overview page, navigation screenshots.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) — specifically a Continuity of Care Document (CCD) using templateId `2.16.840.1.113883.10.20.22.1.1` (extension 2015-08-01). This is the same CCD template used for transitions of care under §170.315(b)(1).
- **Mechanism**:
  - **UI (single patient)**: Navigate to patient Facesheet → click "Export CCDA" → file downloads (named `PATIENTNAME-TIMESTAMP`).
  - **UI (bulk)**: Analytics → CCDA tab → click Export icon → select patients → Export → ZIP file downloads containing individual C-CDA files.
  - **API**: GET `/ccda/ccda/patient_data` with bearer token and `patient_token` parameter. Optional date range filtering. Returns C-CDA XML.
- **Single-patient**: Yes, via Facesheet button or API.
- **Bulk**: Yes, via Analytics CCDA tab (select multiple patients, get ZIP).
- **Access constraints**: Requires "appropriate system permissions." API requires OAuth 2.0 token (client_id, client_secret, username, password). No fees mentioned.

## 4. Export Content: What's In It

### No data dictionary

Edvak provides **no data dictionary, no schema, no field-level documentation, and no sample export files**. The only content specification is a single sentence on the EHI export page:

> "includes data such as demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, and clinical notes"

The CCDA API retrieval documentation provides one truncated XML example that shows only the CCD header and patient demographics (patientRole with id, address, telecom, name, gender, birthTime, raceCode, languageCommunication). The response body sections are not documented at all.

### Vendor's own content organization

Since no data dictionary exists, the only vendor-provided content description is the 10 domain names listed above. These map to standard C-CDA CCD sections:

| Domain (vendor's term) | C-CDA Section | Fields | Described | Types | Category |
|---|---|---|---|---|---|
| demographics | recordTarget/patientRole (header) | ~7 standard | 0 | No | Claimed |
| medications | Medications Section | ~6 standard | 0 | No | Claimed |
| problems | Problem Section | ~4 standard | 0 | No | Claimed |
| allergies | Allergies Section | ~5 standard | 0 | No | Claimed |
| vitals | Vital Signs Section | ~5 standard | 0 | No | Claimed |
| immunizations | Immunizations Section | ~5 standard | 0 | No | Claimed |
| lab results | Results Section | ~6 standard | 0 | No | Claimed |
| procedures | Procedures Section | ~4 standard | 0 | No | Claimed |
| care plans | Plan of Treatment Section | ~3 standard | 0 | No | Claimed |
| clinical notes | Notes / narrative | ~4 standard | 0 | No | Claimed |

**Total**: 10 claimed domains, ~57 inferred standard C-CDA fields, **0 fields documented by the vendor**, 0% description coverage.

The field counts above are estimates based on standard C-CDA section templates — the vendor provides no indication of which specific data elements within each section are populated. Without a sample export file, it is impossible to verify what the C-CDA actually contains.

### What's visible in the UI but absent from export documentation

The Facesheet screenshot (SP_2.png) shows sections that are **not** listed in the export documentation:
- **Past History** — visible on Facesheet
- **Goals** — visible on Facesheet (may be included under "care plans")
- **Assessments** — visible on Facesheet
- **Interventions** — visible on Facesheet

Additionally, the patient view shows tabs for **Documents**, **Billing**, and **Referrals** — none of which are mentioned in the export content.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export covers exactly one category: **clinical summary data delivered as a C-CDA CCD**. The 10 listed domains (demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, clinical notes) are precisely the standard C-CDA CCD sections — the same content used for transitions of care, clinical summaries, and USCDI exchange.

There is no evidence of any export content beyond what a standard CCD provides. The CCDA API introduction page explicitly states the API "conforms to the G9 certification standard for electronic health information access" — confirming this is the same data surface as the (g)(9) API, delivered in C-CDA format rather than FHIR.

The vendor has a single export mechanism (C-CDA CCD) that appears to serve multiple certification criteria: (b)(1) transitions of care, (b)(10) EHI export, and (g)(9) application access. No purpose-built (b)(10) functionality is evident.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Listed in export; API example shows name, gender, DOB, race, address, phone, email, language | Standard CCD demographics; may miss product-specific fields |
| Encounters / visits | ❌ Not covered | Not listed; "Encounter Notes" tab visible on Facesheet but not in export list | Product has encounters (Encounter Notes tab); gap |
| Problems / conditions | ✅ Covered | "problems" listed in export | Standard C-CDA section |
| Medications / prescriptions | ✅ Covered | "medications" listed in export | Standard C-CDA section; e-prescribing history likely not included |
| Allergies | ✅ Covered | "allergies" listed in export | Standard C-CDA section |
| Immunizations | ✅ Covered | "immunizations" listed in export | Standard C-CDA section |
| Vitals | ✅ Covered | "vitals" listed in export | Standard C-CDA section |
| Lab results | ✅ Covered | "lab results" listed in export | Standard C-CDA section |
| Imaging / diagnostic reports | ⚠️ Partial | Facesheet shows "Labs & Imaging" combined; export lists only "lab results" | Product has imaging orders/results; unclear if included |
| Procedures | ✅ Covered | "procedures" listed in export | Standard C-CDA section |
| Clinical notes / documents | ⚠️ Partial | "clinical notes" listed; but "Documents" tab (scanned docs, faxes) not mentioned | Notes likely included as C-CDA narrative; uploaded documents/faxes likely excluded |
| Care plans / goals | ⚠️ Partial | "care plans" listed; "Goals" visible on Facesheet but not listed separately | Goals section may or may not be in the C-CDA |
| Orders / referrals | ❌ Not covered | "Referrals" tab visible on Facesheet; not in export | Product has referral management; gap |
| Insurance / coverage | ❌ Not covered | Not mentioned; product has real-time insurance eligibility checks | Product stores insurance data; gap |
| Claims / billing | ❌ Not covered | "Billing" tab visible on Facesheet; not in export | Product has full RCM module (claims, ICD/CPT codes, denial tracking); **significant gap** |
| Payments | ❌ Not covered | Not mentioned; product has payment processing | Product stores payment data; gap |
| Consents / directives | ❌ Not covered | Not mentioned | May store consent forms; unclear |
| Patient communications | ❌ Not covered | Not mentioned; product has 2-way SMS, phone calls, portal messages | Product stores communications; gap |
| Specialty-specific data | N/A | No specialty-specific sections | Product claims "all specialties" but no specialty data is evident |

**Summary**: Of 18 applicable standard domains, **7 are covered** (standard C-CDA sections), **4 are partially covered** (incomplete or ambiguous), and **7 are not covered at all** — including billing, insurance, payments, referrals, documents, encounters, and patient communications, all of which the product stores.

## 6. Documentation Quality

The EHI export documentation is **extremely thin**:

- **No data dictionary**: Zero field-level documentation. A developer examining this export would have to rely entirely on the C-CDA standard spec to interpret the output.
- **No schema**: No XSD, Schematron, or implementation guide is provided or referenced.
- **No sample data**: The API docs show a truncated XML example (header + demographics only). No complete sample C-CDA file is available. The ZIP file screenshot shows files of 14–33 KB each, suggesting minimal content.
- **No vendor-specific mapping**: No documentation of how Edvak's internal data model maps to C-CDA sections — no indication of which coded value sets are used, which optional C-CDA elements are populated, or what vendor extensions (if any) exist.
- **No content specification beyond a sentence**: The entire content description is one sentence listing 10 domain names.
- **Procedural clarity**: The step-by-step screenshots effectively show *how* to trigger the export (click a button, save a file). The *what* (content) is undocumented.

A developer trying to build an import for Edvak's EHI export would have nothing vendor-specific to work from — they would need to obtain actual C-CDA files and reverse-engineer the structure.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only the 10 standard C-CDA CCD clinical summary domains — demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, and clinical notes. These are exactly the USCDI clinical data classes, representing the regulatory floor for clinical exchange. The product demonstrably stores substantially more: billing/claims data (full RCM module with claims submission, denial tracking, payment processing), insurance eligibility data, referral management data, documents/faxes, patient communications (SMS, phone, portal messages), patient intake forms, and encounter-level data. None of these appear in the export. The Facesheet screenshot directly confirms Billing, Documents, and Referrals tabs exist in the product but are absent from the export. Without a sample export file or data dictionary, even the claimed clinical domains cannot be verified for depth.

**Axis 2 — Export approach: Repackaged existing export**

Multiple signals confirm this is a standard C-CDA CCD export relabeled as (b)(10):

1. **Same template**: The CCD templateId `2.16.840.1.113883.10.20.22.1.1` (2015-08-01) is the standard Continuity of Care Document used for transitions of care under (b)(1).
2. **Same data**: The 10 listed domains exactly match USCDI clinical data classes / standard CCD sections.
3. **API cross-references (g)(9)**: The CCDA API introduction page states it "conforms to the G9 certification standard" — explicitly linking this to the existing clinical exchange API.
4. **No product-specific content**: Zero vendor-specific data mapping, extensions, or billing/operational data.
5. **Shared mechanism**: The "Export CCDA" button on the Facesheet and the CCDA tab under Analytics appear to serve both transitions-of-care and EHI export purposes.

### Key Findings

1. **The (b)(10) export is a standard C-CDA CCD — the same transitions-of-care document used for (b)(1) and referenced by the (g)(9) API.** The vendor's own API documentation links it to "G9 certification standard," confirming it is a repackaged clinical exchange export, not a purpose-built EHI export.

2. **Billing/RCM data is entirely absent despite the product having a full billing module** with claims submission, denial analytics, ICD/CPT code capture, insurance eligibility, and payment processing. The "Billing" tab is visible on the patient Facesheet (SP_2.png) but is not included in the export.

3. **No data dictionary, schema, or sample export exists.** The entire content specification is a single sentence listing 10 data domain names. Zero fields are documented by the vendor.

4. **Multiple product data domains are missing**: referrals, uploaded documents/faxes, patient communications (SMS, phone, portal messages), patient intake forms, insurance data, and encounter-level records are all stored by the product but absent from the export.

5. **Bulk export is supported**, which is a positive feature — users can export C-CDA files for multiple patients simultaneously via the Analytics CCDA tab, delivered as a ZIP file.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA (CCD)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No (truncated XML header only in API docs)
Bulk export:     Yes
Domains covered: 7 of 18 applicable domains (+ 4 partial)
```

### Bottom Line

Edvak's (b)(10) export is a standard C-CDA Continuity of Care Document — the same clinical summary used for transitions of care — relabeled as an EHI export. A patient receiving this export would get a clinical summary (medications, problems, allergies, vitals, labs, immunizations, procedures, care plans, notes) but would be missing their billing history, insurance data, referrals, uploaded documents, patient communications, and intake forms. The single biggest gap is the complete absence of billing/RCM data despite the product having a full revenue cycle management module.
