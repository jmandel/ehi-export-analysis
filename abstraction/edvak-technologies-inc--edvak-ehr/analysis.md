# EHI Export Analysis: Edvak Technologies Inc

**Product**: Edvak EHR v1
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.3230.Edva.0v.00.1.250613 (Listing #11656)

## 1. Product Context

Edvak EHR is a cloud-based ambulatory EHR and practice management platform targeting solo practitioners and small-to-mid-sized group practices. Certified on June 13, 2025 with 33 ONC criteria, the product is marketed as an "all-in-one" platform with five integrated modules:

1. **Advanced EHR (Clinical)**: AI-powered clinical documentation, e-prescribing (Surescripts), CPOE for meds/labs/imaging, drug-allergy interaction checks (Medi-Span), structured clinical notes with speech-to-text/AI scribe, telehealth
2. **Practice Management**: Scheduling, task management, referral management, document management, fax management
3. **Patient Engagement**: Patient portal, two-way SMS, phone calls, patient intake forms with auto-charting, automated care reminders, online scheduling
4. **Revenue Cycle Management / Billing**: ICD/CPT code capture, insurance eligibility verification, claims submission and processing, denial prediction, patient payment processing
5. **Analytics & Reporting**: Practice insights, CQM reporting, revenue/billing analytics

This product stores clinical, billing, practice management, and patient engagement data. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|
| `ehi-export-page.html` | HTML | 50,380 bytes | Main EHI export documentation page at edvak.com/ehi-export | **Primary** — sole source of export documentation |
| `screenshots/SP_!A.png` through `SP_3.png` | PNG | 4 files, 393 KB total | Single-patient export workflow screenshots | Supporting — confirms UI mechanism |
| `screenshots/MP_1A.png` through `MP_7.png` | PNG | 6 files, 429 KB total | Population export workflow screenshots | Supporting — confirms bulk export and ZIP output |
| `screenshots/ehi-export-page-full.png` | PNG | 1.17 MB | Full-page browser capture of EHI export page | Redundant with HTML |
| `ccda-api-introduction-1018024m0.html` | HTML (Apidog) | 92,640 bytes | CCDA API introduction: describes C-CDA format and document types | Secondary — confirms C-CDA scope |
| `ccda-api-ccda-retrieval-16935528e0.html` | HTML (Apidog) | 122,532 bytes | CCDA retrieval endpoint docs with truncated XML example | **Most informative API artifact** — confirms CCD template and header-only sample |
| `ccda-api-generate-token-16915497e0.html` | HTML (Apidog) | 116,997 bytes | Token generation endpoint | Low — authentication mechanics only |
| `ccda-api-authentication-access-1019424m0.html` | HTML (Apidog) | 84,356 bytes | OAuth 2.0 authentication description | Low |
| `ccda-api-errors-1019029m0.html` | HTML (Apidog) | 80,943 bytes | Error response codes | Low |
| `ccda-api-apis-3752591f0.html` | HTML (Apidog) | 78,331 bytes | API overview listing endpoints | Low |

**Key observation**: There is no data dictionary, no JSON/XML schema, no sample export file, no field-level documentation of any kind. The entire EHI export documentation consists of a single HTML page with step-by-step screenshots and one paragraph describing data domains at a category level.

## 3. Export Mechanics

- **Format**: C-CDA XML (Consolidated Clinical Document Architecture), specifically a Continuity of Care Document (CCD) using template `2.16.840.1.113883.10.20.22.1.1` (2015-08-01 extension), LOINC code `34133-9` ("Summarization of Episode Note")
- **Single-patient export**: UI button labeled "Export CCDA" on the patient Facesheet page. Downloads a single XML file named `PATIENTNAME-TIMESTAMP` (e.g., `ALICE_NOMEN-1747301459482`)
- **Bulk/population export**: Via Analytics → CCDA tab → Export icon → select patients (with "Select All" option) → Export. Downloads a ZIP file (e.g., `ccda-bulk-1747301769867`) containing individual C-CDA files per patient. Sample ZIP in screenshot shows 4 files, 14–33 KB each.
- **Programmatic API**: REST API at `https://darwinapi.edvak.com/ccda/ccda/patient_data` with OAuth 2.0 ROPC authentication. Accepts `patient_token` (required) and optional date range filters (`date`, `start_date`, `end_date`). Returns C-CDA XML.
- **Access constraints**: Requires "authorized users with appropriate system permissions." API requires client credentials. No mention of fees for export.
- **Bulk capability**: Yes — population-level export available through UI and implicitly through API (one patient at a time via API).

## 4. Export Content: What's In It

### No data dictionary exists

There is **no data dictionary, schema, field-level documentation, or structured specification** of the export content. The entirety of the content description is this single sentence from the EHI export page:

> "This option is accessible directly from the patient's Facesheet section and includes data such as demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, and clinical notes."

This is a category-level list with no field names, no types, no descriptions, no coded value sets, no relationships, and no mapping to C-CDA sections or templates.

### Sample data analysis

The only sample data available is a truncated XML example embedded in the CCDA API retrieval endpoint documentation (`ccda-api-ccda-retrieval-16935528e0.html`). The API docs page itself labels this as a "Trimmed Clinical Document (CCD Summary) — This schema includes only the document header and patient demographic information from a full Continuity of Care Document (CCD)."

The sample XML (1,893 bytes, saved to `analysis/sample-ccda-from-api-docs.xml`) contains only:
- Document header: realmCode, typeId, templateId, id, code, title, effectiveTime, confidentialityCode, languageCode
- recordTarget/patientRole: patient ID (MRN), address, phone, email, name, gender, birth date, race, language

**No clinical sections are present** — no structuredBody, no medications, no problems, no allergies, no vitals, no lab results, nothing beyond the CDA header and demographics. The sample is explicitly labeled as truncated.

No complete sample C-CDA export file is provided anywhere in the documentation.

### C-CDA document type

The export uses the standard CCD template (`2.16.840.1.113883.10.20.22.1.1`), which is the same document type used for transitions of care under §170.315(b)(1). The LOINC code `34133-9` ("Summarization of Episode Note") confirms this is a clinical summary document, not a comprehensive data export format.

The CCDA API Introduction page lists these as example CCDA document types: CCD, Discharge Summary, Referral Note, Consultation Note, and Progress Note — all standard C-CDA document types. No vendor-specific extensions or custom sections are mentioned.

### Vendor's own content organization

Since no data dictionary exists, the only content information available is the 10-item domain list. Mapped to what's standard in a CCD:

| Data Domain (vendor's list) | Likely C-CDA Section | Fields | Described | Types |
|---|---|---|---|---|
| Demographics | recordTarget/patientRole | Unknown | No | No |
| Medications | Medications Section | Unknown | No | No |
| Problems | Problem List Section | Unknown | No | No |
| Allergies | Allergies Section | Unknown | No | No |
| Vitals | Vital Signs Section | Unknown | No | No |
| Immunizations | Immunizations Section | Unknown | No | No |
| Lab results | Results Section | Unknown | No | No |
| Procedures | Procedures Section | Unknown | No | No |
| Care plans | Plan of Treatment Section | Unknown | No | No |
| Clinical notes | Notes / Encounter Section | Unknown | No | No |

Field counts, types, and descriptions are all unknown because no data dictionary or sample data is provided. The section-to-C-CDA mapping is inferred from standard C-CDA structure, not documented by the vendor.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor claims 10 data domains, all of which are standard USCDI/C-CDA clinical summary categories. This is precisely the same scope as a transitions-of-care C-CDA document — the data you'd get from a §170.315(b)(1) export or a FHIR US Core API response.

There is no indication of any vendor-specific extensions, custom data, billing data, or practice management data in the export. The vendor does not organize the export into custom categories — they list the same clinical domain names used universally across C-CDA implementations.

The CCDA API introduction explicitly states the API "conforms to the G9 certification standard for electronic health information access," referencing §170.315(g)(9) (application access — all data request), not §170.315(b)(10). This suggests the vendor may be reusing the same C-CDA generation for both (g)(9) and (b)(10) purposes.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Listed in claimed domains; truncated sample shows basic demographics (name, DOB, gender, race, address, phone, email). No evidence of full demographic detail. | No field-level documentation to verify completeness |
| Encounters / visits | ⚠️ Partial | Not explicitly listed but "clinical notes" may include encounter context. Facesheet has "Encounter Notes" tab. | Product stores encounters; coverage uncertain |
| Problems / conditions | ⚠️ Partial | "Problems" listed in claimed domains | Claimed but no verification possible without sample data |
| Medications / prescriptions | ⚠️ Partial | "Medications" listed in claimed domains | Claimed but no field-level detail; e-prescribing history likely not included |
| Allergies | ⚠️ Partial | "Allergies" listed in claimed domains | Claimed but unverifiable |
| Immunizations | ⚠️ Partial | "Immunizations" listed in claimed domains | Claimed but unverifiable |
| Vitals | ⚠️ Partial | "Vitals" listed in claimed domains | Claimed but unverifiable |
| Lab results | ⚠️ Partial | "Lab results" listed in claimed domains | Claimed; unclear if includes full order history and discrete results |
| Imaging / diagnostic reports | ❌ Not covered | Not listed in claimed domains despite "Labs & Imaging" being a combined Facesheet section | Product has electronic imaging ordering; gap |
| Procedures | ⚠️ Partial | "Procedures" listed in claimed domains | Claimed but unverifiable |
| Clinical notes / documents | ⚠️ Partial | "Clinical notes" listed; Facesheet shows "Assessments" and "Interventions" sections | AI-generated notes, structured notes may not fully render in C-CDA |
| Care plans / goals | ⚠️ Partial | "Care plans" listed; Facesheet shows "Goals" section | Goals may or may not be included; unverifiable |
| Orders / referrals | ❌ Not covered | Not listed in claimed domains. Facesheet has "Referrals" tab. | Product has referral management; gap |
| Insurance / coverage | ❌ Not covered | Not mentioned in export | Product does real-time eligibility checks and stores insurance data; significant gap |
| Claims / billing | ❌ Not covered | Not mentioned in export. Facesheet has "Billing" tab. | Product has full RCM/billing module with claims, coding, payments; **major gap** |
| Payments | ❌ Not covered | Not mentioned in export | Product processes patient payments; gap |
| Consents / directives | ❌ Not covered | Not mentioned | Likely stored given patient portal and intake forms |
| Patient communications | ❌ Not covered | Not mentioned | Product has 2-way SMS, phone calls, portal messages; gap |
| Patient-reported data | ❌ Not covered | Not mentioned | Product has patient intake forms with AI auto-charting; gap |

**Summary**: Of the domains listed above relevant to this product, 10 are claimed as covered (but all unverifiable without sample data) and at least 7 are clearly not covered despite the product storing data in those domains.

## 6. Documentation Quality

The export documentation is **extremely thin**:

- **No data dictionary**: Zero field-level documentation exists. A developer cannot determine what fields are in the export, what coded values are used, how data is structured within C-CDA sections, or what entry-level templates are employed.
- **No sample files**: The only XML sample is explicitly truncated to the document header. No complete C-CDA export is available for inspection.
- **No schema files**: No XSD, Schematron, or other machine-readable specification is provided.
- **No value set documentation**: No indication of what code systems, terminologies, or value sets are used in the export.
- **No relationship documentation**: No mapping between Edvak's internal data model and C-CDA structures.
- **Step-by-step workflow is clear**: The screenshots effectively demonstrate how to trigger the export. This is the only well-documented aspect.
- **API documentation exists but is shallow**: The CCDA API has endpoint documentation but no response body specification beyond the truncated header example.

A developer attempting to build an import for Edvak EHI exports would have no specification to work from. They would need to obtain a sample file and reverse-engineer the structure entirely.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The Edvak EHI export is a C-CDA Continuity of Care Document — the same standardized clinical summary format used for transitions of care. The 10 claimed data domains (demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, clinical notes) are exactly the USCDI clinical data classes, which is the same data available through the FHIR (g)(10) API, just delivered in C-CDA format.

This is not a native database export. It does not expose Edvak's internal data model. It projects a subset of clinical data into a standard format that inherently cannot represent billing, insurance, claims, referrals, patient communications, documents, or other non-clinical data that the product stores.

### Key Findings

1. **The (b)(10) export is functionally identical to the transitions-of-care C-CDA.** The template ID (`2.16.840.1.113883.10.20.22.1.1`), LOINC code (`34133-9`), and data domains match a standard CCD document. The vendor's own API documentation references §170.315(g)(9) compliance, not (b)(10), suggesting this C-CDA generation was built for interoperability and repurposed as the "EHI export."

2. **No billing, insurance, claims, or payment data is exported despite the product having a full RCM module.** Edvak markets billing and revenue cycle management as a core product feature with ICD/CPT capture, claims submission, denial tracking, and payment processing. None of this data appears in the export. The Facesheet screenshot itself shows a "Billing" tab that is not covered by the "Export CCDA" button.

3. **No data dictionary or sample data exists.** The entire content specification is a 10-item bullet list of domain names. There are zero documented fields, zero documented types, zero documented value sets. The only XML sample is explicitly truncated to the document header.

4. **Multiple product data domains visible in the UI are absent from the export.** The patient Facesheet screenshot (SP_2.png) shows tabs for Documents, Encounter Notes, Billing, and Referrals — none of which are listed in the export's claimed data domains. Facesheet sections for "Assessments," "Interventions," "Goals," and "Past History" are also visible but not explicitly called out in the export specification.

5. **The documentation reads as a compliance checkbox.** The EHI export page exists to satisfy the (b)(10) certification requirement. It demonstrates the feature exists and can be triggered but provides no technical depth about what data is actually exported or how it maps to the product's full data model.

### Summary Stats

```
Classification:  Standard-based projection (C-CDA repackaging)
Export format:   C-CDA XML (Continuity of Care Document)
Model type:      Standard projection (CCD, not native database)
Entities:        N/A (no data dictionary; C-CDA is a single document per patient)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No (only truncated header example in API docs)
Bulk export:     Yes (ZIP of individual C-CDA files via UI; API is per-patient)
Domains covered: 10 claimed of 17+ applicable domains (but all unverifiable)
```

### Bottom Line

The Edvak EHI export is a standard C-CDA clinical summary repackaged as a (b)(10) export. It covers roughly the same clinical data available through any FHIR or C-CDA interoperability endpoint — demographics and standard clinical domains — while entirely omitting billing, insurance, claims, referrals, documents, patient communications, and other data the product stores. With no data dictionary, no sample data, and no field-level documentation, even the claimed coverage cannot be independently verified. The single biggest gap is the complete absence of the product's billing/RCM data from the export, despite billing being a core marketed feature of the platform.
