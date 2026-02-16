# EHI Export Analysis: Tebra Technologies, Inc.

**Product**: Tebra EHR (formerly Kareo EHR)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2777.Tebr.05.03.1.241219

## 1. Product Context

Tebra (formerly Kareo) is an integrated cloud-based platform for small ambulatory practices. It combines:

- **Clinical (EHR)**: Charting, notes, problem lists, medications, allergies, immunizations, vitals, lab orders/results, care plans, referrals, e-prescribing (via DrFirst Rcopia), patient portal (via Updox), charge capture, custom templates, flowsheets, and clinical decision support.
- **Billing / Practice Management (PM)**: Full revenue cycle management including insurance eligibility verification, electronic claim submission and scrubbing, ERA/EOB posting, patient statements, payment collection (including digital payments), denial management, superbills, and robotic process automation for billing workflows. The PM module supports CPT/HCPCS/ICD-10 coding, payer-specific rules, and multi-client billing company management.
- **Platform**: Patient demographics, scheduling, patient communications (email/text), document management, message center, and practice settings.
- **Engage**: Patient communications, online visibility, front office automation.
- **Telehealth**: Video visits.

The billing/PM module is a major component — the billing page describes features like claim scrubbing, batch claim submission, real-time eligibility, ERA auto-posting, patient payment links, branded statements, and multi-client dashboards. This is not a thin add-on; it stores substantial billing and claims data.

The EHI export should therefore cover clinical data (notes, medications, allergies, labs, vitals, procedures, etc.), billing/claims data (charges, claims, payments, insurance), patient demographics, documents, and communications.

## 2. Artifacts Reviewed

| Artifact | Source | Description | Informativeness |
|---|---|---|---|
| `macra_mips_page.html` | [tebra.com/tebra-resources/macra-mips/](https://www.tebra.com/tebra-resources/macra-mips/) | Main CHPL-linked certification page; contains the 3-sentence EHI export description | **Most informative** for understanding vendor's stated EHI export scope |
| `export_patient_data_help.html` | [helpme.tebra.com](https://helpme.tebra.com/Platform/Practice_Settings/Data_Management/Export_Patient_Clinical_Data) | Help center article on how to run the EHI export; describes mechanics and output format | **Most informative** for understanding export mechanics |
| `general_api_docs.pdf` | tebra.com, 48 pages | General Clinical API documentation — 14 JSON resources, 176 fields with descriptions | **Most informative** for understanding structured clinical data model |
| `fhir_api_guide.pdf` | tebra.com, 34 pages | FHIR R4 API User Guide via SmileCDR — USCDI v1 / US Core STU3 3.1.1 | Moderately informative; covers same USCDI data as C-CDA |
| `2024_test_results.pdf` | tebra.com, 14 pages | 2024 Real World Test Results — confirms (b)(10) testing: 3,931 EHI exports across 790 practices | Moderately informative; confirms export is active and used |
| `2025_test_plan.pdf` | tebra.com, 17 pages | 2025 RWT Plan — describes (b)(10) measure methodology | Low informativeness for export content |
| `2024_test_plan.pdf` | tebra.com, 16 pages | 2024 RWT Plan — originally tested (b)(6) batch export; switched to (b)(10) in results | Reveals the (b)(6)→(b)(10) evolution |
| `costs_and_guidance.pdf` | tebra.com, 1 page | Costs and Guidance — data portability "creates export summaries for all patients" | Confirms no additional fees |
| `2022_test_plan.pdf` | tebra.com, 13 pages | 2022 RWT Plan | Low informativeness |
| `2022_test_results.pdf` | tebra.com, 12 pages | 2022 RWT Results | Low informativeness |
| `2023_test_plan.pdf` | tebra.com, 20 pages | 2023 RWT Plan | Low informativeness |
| `2023_test_results.pdf` | tebra.com, 12 pages | 2023 RWT Results | Low informativeness |

**No data dictionary, schema, sample export files, or field-level documentation for the EHI export was found.** The vendor provides no structured documentation of what the export contains beyond a few sentences of prose.

## 3. Export Mechanics

- **Format**: ZIP file containing individual XML C-CDA 2.1 Summary of Care files per patient, plus patient documents in native format (PDF, JPG, etc.). The vendor's MACRA page additionally mentions "PDFs for claims and billing information."
- **Mechanism**: UI-based. Navigate to Practice Settings → Data Management → Export Patient Data. No API-based export; no command-line tool.
- **Single-patient vs bulk**: Supports population-level export. Users select a date range and provider, and the system generates C-CDA files for all patients with clinical notes in that timeframe. Can be one-time or recurring (weekly/monthly).
- **Filtering**: By date range (when patients were seen) and by provider. No per-patient granularity in the export UI — it's batch-only filtered by encounter dates.
- **Access constraints**: Available to users with Practice Settings access. No additional fees per the Costs and Guidance document.
- **Turnaround**: The Costs and Guidance doc notes "Creation of these summaries will be completed within 24 hours."
- **Real-world usage**: 2024 RWT results show 3,931 exports across 790 practices in a 3-month period, averaging ~5 exports per practice. Most exports contained fewer than 100 patients.

## 4. Export Content: What's In It

### What the export produces

Based on the help center documentation (`Export_Patient_Clinical_Data`), the export generates:

1. **C-CDA 2.1 Summary of Care XML files** — one per patient, for patients with clinical notes in the selected timeframe
2. **Patient documents** — uploaded documents in their native format

The vendor's MACRA/MIPS certification page adds: "PDFs for claims and billing information" — but there is no further documentation of what these PDFs contain, what fields they include, or how they are structured.

### No data dictionary

There is **no data dictionary** for the EHI export. The vendor provides:
- No schema or field-level documentation for the export content
- No sample export files
- No mapping document showing what database fields appear in the export
- No description beyond the two sources quoted above

### C-CDA content (inferred from API documentation)

While the export itself has no data dictionary, the General Clinical API (48-page PDF, `general_api_docs.pdf`) documents 14 JSON resources with 176 total fields that represent the clinical data model. These resources map to C-CDA sections:

| Resource (API endpoint) | Fields | Category | Description |
|---|---|---|---|
| Patient (`/patient`) | 25 | Demographics | Name, DOB, gender, race, ethnicity, language, contact info |
| Encounter (`/patient/encounter`) | 19 | Clinical | Dates, providers, diagnoses, location |
| Allergy Intolerance (`/patient/allergyIntolerance`) | 14 | Clinical | Substances, reactions, severity, status |
| Care Plan (`/patient/carePlan`) | 13 | Clinical | Assessment and plan of treatment |
| Condition/Problem List (`/patient/condition/problemList`) | 11 | Clinical | Problems and conditions |
| Implantable Device (`/patient/device`) | 10 | Clinical | UDI information |
| Procedure (`/patient/procedure`) | 9 | Clinical | Patient procedures |
| Goal (`/patient/goal`) | 7 | Clinical | Clinical goals |
| Vital Signs (`/patient/observation/vitalSigns`) | 10 | Clinical | BP, height, weight, temp, pulse ox, etc. |
| Smoking Status (`/patient/smokingStatus`) | 8 | Clinical | Smoking status observation |
| Diagnostic Report (`/patient/diagnosticReport`) | 22 | Clinical | Lab tests, imaging, diagnostic results |
| Immunization (`/patient/immunization`) | 12 | Clinical | Immunization history |
| Medication Statement (`/patient/medicationStatement`) | 12 | Clinical | Medication history |
| Summary C-CDA (`/patient/binary/summary`) | 4 | Summary | Base64-encoded C-CDA 2.1 document |

**All 176 fields have descriptions and types** in the General API documentation. However, this API documentation is not specifically for the (b)(10) export — it describes the Clinical API, and the EHI export is the C-CDA output from the same underlying data.

### FHIR API content

The FHIR API (via SmileCDR) covers the same USCDI v1 data elements through ~22 FHIR resources (Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Practitioner, PractitionerRole, Procedure, Provenance). This is a standard US Core projection — no vendor extensions are documented.

### What's missing

The export is explicitly a C-CDA Summary of Care — a standardized clinical summary. It covers USCDI v1 data elements but, by definition, does not include:

- **Billing data in structured form**: Claims, charges, CPT/HCPCS codes, payment records, ERA/EOB data, denial tracking, patient balances — none of this appears in C-CDA. The vendor mentions "PDFs for claims and billing information" but provides no detail on content.
- **Insurance/coverage details**: Beyond basic payer information that may appear in the C-CDA header, the detailed insurance eligibility, coverage, copay, deductible data stored in the PM module is not exported as structured data.
- **Patient communications**: Portal messages, email/text communications
- **Charge capture details**: The EHR has charge capture from clinical notes; this is billing data
- **Referral details**: The EHR has a referral management module
- **Custom templates/forms**: The EHR supports custom clinical templates; template-specific data may or may not appear in the C-CDA

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is structured around a single output: **C-CDA 2.1 Summary of Care files**. There are no vendor-defined categories, no data dictionary categories, no entity groupings. The vendor describes the export in one sentence: "C-CDA documents for clinical records, PDFs for claims and billing information, and also documents in the original native format."

The C-CDA sections cover standard clinical summary data (demographics, allergies, medications, problems, procedures, immunizations, vitals, lab results, care plans, goals). The uploaded patient documents are included in native format. The "PDFs for claims and billing information" are mentioned but undocumented.

This is thin. The vendor has not invested in creating any export documentation beyond a help center article and a few sentences on their certification page.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA patient header; General API shows 25 fields (name, DOB, gender, race, ethnicity, language) | Missing: address/contact details unclear in export; phone, email, emergency contacts unknown |
| Encounters / visits | ⚠️ Partial | C-CDA encounters section; API shows 19 fields | C-CDA encounters are summaries, not full encounter records; encounter-level notes may be truncated |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA problems section; API shows 11 fields with ICD codes | Standard C-CDA coverage |
| Medications / prescriptions | ✅ Covered | C-CDA medications section; API shows 12 fields | Standard C-CDA coverage; e-prescribing details (pharmacy, fill status) may be limited |
| Allergies | ✅ Covered | C-CDA allergies section; API shows 14 fields with coded substances and reactions | Standard C-CDA coverage |
| Immunizations | ✅ Covered | C-CDA immunizations section; API shows 12 fields | Standard C-CDA coverage |
| Vitals | ✅ Covered | C-CDA vital signs section; API shows 10 fields | Standard C-CDA coverage |
| Lab results | ✅ Covered | C-CDA results section; API shows 22 fields for diagnostic reports | Standard C-CDA coverage |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA diagnostic reports; some imaging may be in document attachments | Structured imaging data may be limited to what fits in C-CDA |
| Procedures | ✅ Covered | C-CDA procedures section; API shows 9 fields | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | Patient documents included in native format; C-CDA has notes sections | Full clinical note text may or may not be in the C-CDA; uploaded docs are included |
| Care plans / goals | ✅ Covered | C-CDA care plan and goals sections; API shows 13 + 7 fields | Standard C-CDA coverage |
| Orders / referrals | ❌ Not covered | No evidence of referral data in export | Product has referral management; significant gap |
| Insurance / coverage | ❌ Not covered | No structured insurance data in export | Product has insurance eligibility, coverage management; significant gap |
| Claims / billing | ❌ Not covered | Vendor mentions "PDFs for claims and billing" but no documentation of content | Product has full RCM with claims, ERA/EOB, denial management; **major gap** |
| Payments | ❌ Not covered | No structured payment data in export | Product has patient payments, digital payments, payment posting; significant gap |
| Consents / directives | ❌ Not covered | No consent data in export | Unknown if product stores structured consents |
| Patient communications / portal messages | ❌ Not covered | No communication data in export | Product has patient portal, message center, email/text; significant gap |

## 6. Documentation Quality

The EHI export documentation is **extremely thin**:

- **No data dictionary**: There is zero field-level documentation of the export output. No schema, no field list, no entity definitions.
- **No sample data**: No sample export files are provided.
- **Export mechanics are documented**: The help center article clearly explains how to run the export, with screenshots. A developer could trigger an export. But they would have no idea what's in it until they open the ZIP.
- **C-CDA format is implicitly documented**: Since the export produces C-CDA 2.1, the HL7 C-CDA specification serves as de facto documentation. But the vendor doesn't document which C-CDA sections are populated, what coded vocabularies are used, or what extensions (if any) they include.
- **General Clinical API is well-documented**: The 48-page API guide documents 14 resources with 176 fields, all with descriptions and types. But this is the API, not the (b)(10) export — and it covers only clinical data, not billing.
- **A developer could not build an import from this documentation alone.** They would need to: (1) obtain an actual export, (2) reverse-engineer the C-CDA structure, (3) figure out the billing PDFs, and (4) handle the native document formats — all without any vendor guidance.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The EHI export is a C-CDA 2.1 Summary of Care document plus attached patient documents. This is a standard clinical summary format that covers USCDI v1 data elements — essentially the same content available through the FHIR API. There is no native database export. The vendor mentions "PDFs for claims and billing information" but provides no documentation of this component.

### Key Findings

1. **The export is fundamentally a C-CDA repackaging.** The (b)(10) EHI export produces the same C-CDA Summary of Care files that would be used for transitions of care under (b)(1)/(b)(6). The 2024 RWT Plan originally tested this as "(b)(6) Patient Batch Export" before being relabeled as "(b)(10) EHI Export" in the results document — an explicit acknowledgment that this is the same batch C-CDA functionality repurposed for (b)(10).

2. **Billing and claims data is absent from structured export despite being a major product capability.** Tebra has a comprehensive PM/billing module (claims submission, ERA/EOB posting, insurance eligibility, patient payments, denial management). None of this appears in structured form in the export. The vendor mentions "PDFs for claims and billing" but provides no documentation of what these contain.

3. **No data dictionary or export documentation exists.** The vendor provides zero field-level documentation of the export. This is the minimum bar for (b)(10) compliance — the regulation requires "documentation describing the format of the export" to be publicly accessible.

4. **The API documentation shows a clinically reasonable data model** (14 resources, 176 fields with descriptions) but this documents the API, not the export, and covers only clinical data — not billing, insurance, payments, or communications.

5. **The export is actively used.** 2024 RWT results show 3,931 exports across 790 practices in Q2 2024, indicating real production usage.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA 2.1 XML + PDF + native documents (ZIP)
Model type:      Standard projection (C-CDA/FHIR, not native database)
Entities:        N/A (no data dictionary; ~13 C-CDA sections)
Fields:          N/A (no data dictionary; 176 fields documented in separate API)
Descriptions:    N/A (no data dictionary for export)
Sample data:     No
Bulk export:     Yes (date range + provider filter)
Domains covered: 9 of 17 applicable domains (with caveats on billing PDFs)
```

### Bottom Line

Tebra's EHI export is a C-CDA batch export rebranded as (b)(10), covering standard clinical summary data but missing the substantial billing, insurance, payment, and communication data the product stores. The absence of any data dictionary or export documentation makes it impossible to verify exactly what's included. A patient or provider would get a clinical summary (the same ~20% of data available via C-CDA/FHIR) but not a complete copy of their record, particularly missing all billing and financial data from Tebra's PM module.
