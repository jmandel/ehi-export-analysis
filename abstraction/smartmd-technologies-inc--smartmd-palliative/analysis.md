# EHI Export Analysis: SMARTMD Technologies, Inc.

**Product**: SMARTMD Palliative  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.11.09.3194.SMDP.06.00.1.240531

## 1. Product Context

SMARTMD Palliative is a specialty EHR and practice management system designed exclusively for palliative care programs, typically operated alongside hospice organizations. Version 6, certified 2024-05-31. The company (founded 1999, ~30-37 employees) originally focused on medical transcription and expanded into healthcare IT with a focus on hospice, palliative care, and PACE markets.

**Data the product stores (based on product-research.md and vendor materials):**
- **Patient demographics** — name, DOB, address, contacts, service line
- **Clinical encounter notes** — palliative-specific templates with structured assessments (PPS, FAST, ESAS)
- **Medications** — active medication lists
- **Allergies** — drug, food, environmental
- **Problems/diagnoses** — ICD-10 coded problem lists
- **Quality measure data** — acuity scores, PPS scores, pain levels, trend graphs
- **Billing/charge data** — time-based chronic care billing (PCM, TCM, CCM), CPT codes, Medicare Part B
- **Scheduling** — provider schedules, appointments
- **Secure messages** — HIPAA-compliant team messaging
- **Scanned documents/images** — consent forms, scanned documents
- **Care plans** — implied by palliative workflows and CMS GUIDE model support
- **CRM/referral data** — via Accelerate CRM module
- **Audio dictation recordings** — voice documentation with transcription

The product is certified for 28 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, (b)(1) Transitions of Care, and (h)(1) Direct messaging. It relies on EMR Direct Interoperability Engine v2023 for (b)(1) and (h)(1).

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `170.315b10-Electronic-Health-Information-Export.pdf` (10 pages, 173 KB) | Primary (b)(10) documentation. Contains a data dictionary with 5 documented sections (Patient, KinList, Meds, Allergies, Problems) with field-level detail, plus a complete sample JSON export that reveals an additional undocumented CaseList section. | **Most informative** — this is the sole (b)(10) documentation |
| `SMARTMD-ONC-Disclosure-Statement-2024-Leidos-b10.pdf` (2 pages, 137 KB) | ONC disclosure statement listing all 28 certified criteria and CQMs. Confirms (b)(10) certification. Updated Jan 2025. | Moderately informative — confirms scope |
| `SMARTMD-FHIR-API-Documentation-v1.pdf` (58 pages, 587 KB) | FHIR R4 API documentation for (g)(10). Covers standard USCDI resources (Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, etc.). Separate from (b)(10) export. | Context only — documents the separate (g)(10) API |
| `API.json` (4 KB) | FHIR R4 Bundle with Direct messaging Endpoint and Organization resources for (h)(1). | Not relevant to (b)(10) |
| `compliance-page-screenshot.png` (292 KB) | Screenshot of SMARTMD compliance page with documentation links. | Minimal — confirms layout |

## 3. Export Mechanics

- **Format**: JSON (single file per patient)
- **Mechanism**: UI-based — accessed from the "Patients" tab by selecting one or more patients and tapping the "Export" button
- **Single-patient vs bulk**: Documentation says "selecting one or more patients," suggesting both single and multi-patient export, though each patient is a separate record in the output JSON array
- **Access constraints**: Available to "credentialed and authorized users"
- **Fees**: Not mentioned in documentation
- **Output structure**: A JSON file with a top-level `PracticeName` and `PatientList` array, where each patient contains nested sections (Patient, KinList, CaseList, Meds, Allergies, ClinicalSummaryProblemDetailsList)

## 4. Export Content: What's In It

The export documentation defines **5 named sections** with field-level data dictionaries totaling **48 documented fields** across those sections. The sample JSON export reveals a 6th section (CaseList) with approximately **30 additional fields** that are **not documented** in the data dictionary.

### Data Dictionary Quality

- **48 documented fields** across 5 sections — all have field name, type, and prose description
- **30 undocumented fields** visible only in the sample JSON (CaseList section, including nested CaseProvider object)
- **2 undocumented fields** in the Meds section (RxNtCode, IsDiscontinued) present in sample but absent from dictionary
- Types are simple (string, date, bool, Int) — no value sets, no foreign key documentation, no nullable annotations
- One apparent typo: KinList.LastName has type "Date" instead of "string"
- No machine-readable schema (no JSON Schema, no OpenAPI spec)

### Vendor's own content organization

| Entity/Section | Documented Fields | Undocumented Fields (from sample) | Types | Category |
|---|---|---|---|---|
| Patient | 14 | 0 | Yes | Demographics |
| KinList | 10 | 0 | Yes | Demographics |
| Meds | 13 | 2 (RxNtCode, IsDiscontinued) | Yes | Medications |
| Allergies | 4 | 0 | Yes | Clinical |
| Problems (ClinicalSummaryProblemDetailsList) | 7 | 0 | Yes | Clinical |
| CaseList | 0 | 30 | No | Case/Encounter (undocumented) |
| ExportWrapper | 0 | 2 | No | Metadata |
| **Totals** | **48** | **34** | — | — |

### What's in the sample JSON that's NOT in the data dictionary

The sample JSON (pages 7-9 of the PDF) includes a `CaseList` array with rich case/encounter data:
- Case metadata: CaseId, CaseDescription ("Hospice"), CaseClosedFlag, CreatedOn
- Provider info: nested CaseProvider object with ProviderId, ProviderName, FirstName, LastName
- Patient location: PatientLocationId, Address, City, State, Zip
- Diagnosis: Diagnosis1 field (empty in sample)
- Score field (numeric, possibly acuity score — value is 0 in sample)
- Three empty arrays: InsuranceList, ExternalContactList, InternalContactList — these suggest the system *could* export insurance and contact data, but the sample shows them empty

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a narrow subset of the product's data in 5+1 sections:

1. **Demographics** (Patient + KinList): 24 fields covering basic patient info and caregiver/kin contacts. Reasonably complete for basic demographics but missing race, ethnicity, language, sex/gender — fields the product likely stores given its (a)(5) Demographics certification.

2. **Medications** (Meds): 13 documented fields covering the active medication list with drug name, strength, form, dosing, and status. Includes RxNorm code (undocumented). No prescriber info, no pharmacy, no dispense data.

3. **Clinical** (Allergies + Problems): 11 fields total. Allergies are minimal (4 fields: allergen, reaction, text, status). Problems are better (7 fields with ICD-10 codes, onset dates, resolution status, primary diagnosis flag).

4. **Case/Encounter Management** (CaseList, undocumented): 30 fields visible in sample JSON but entirely absent from the data dictionary. Contains case metadata, provider assignments, and placeholder arrays for insurance and contacts.

**Conspicuously absent**: Clinical notes, encounter documentation, care plans, vital signs, assessments (PPS, FAST, ESAS), billing/charges, quality measures, scanned documents, secure messages, scheduling data, dictation records, CQM data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` (14 fields), `KinList` (10 fields) | Basic name/address/phone but missing race, ethnicity, language, sex/gender — product stores these per (a)(5) certification |
| Encounters / visits | ⚠️ Partial | `CaseList` (undocumented, 30 fields) has case metadata | Cases ≠ encounters. No visit dates, visit types, or encounter documentation |
| Problems / conditions / diagnoses | ✅ Covered | `Problems` (7 fields) with ICD-10 codes | Reasonable for problem list |
| Medications / prescriptions | ⚠️ Partial | `Meds` (13 fields) with drug details | Active med list only; no prescriber, pharmacy, MAR, or prescription history |
| Allergies | ⚠️ Partial | `Allergies` (4 fields) | Very thin — no severity, no onset date, no allergy type coding |
| Immunizations | ❌ Not covered | No immunization data in export | Product has FHIR Immunization endpoint; may store immunization data |
| Vitals | ❌ Not covered | No vital signs in export | Product's FHIR API documents vital signs endpoints; likely stored |
| Lab results | ❌ Not covered | No lab data in export | Product has FHIR DiagnosticReport/Lab endpoints; may store some lab data |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data in export | Likely N/A for palliative care specialty |
| Procedures | ❌ Not covered | No procedure data in export | Product has FHIR Procedure endpoint; likely stores some procedure data |
| Clinical notes / documents | ❌ Not covered | No clinical notes in export | **Major gap** — clinical documentation is a core product feature (palliative-specific templates, PPS/FAST/ESAS assessments, dictation) |
| Care plans / goals | ❌ Not covered | No care plan data in export | Product has FHIR CarePlan/Goal endpoints; palliative care plans are core to the product |
| Orders / referrals | ❌ Not covered | No order data in export | Product is certified for CPOE ((a)(1) medications, (a)(2) labs) |
| Insurance / coverage | ❌ Not covered | `InsuranceList` exists in sample JSON but is empty array | Product handles Medicare Part B billing; insurance data likely stored |
| Claims / billing | ❌ Not covered | No billing data in export | **Major gap** — product has time-based chronic care billing, CPT codes, monthly billing; none exported |
| Payments | ❌ Not covered | No payment data | Product does billing/collections; payments likely stored |
| Consents / directives | ❌ Not covered | No consent data | Product handles scanned consent forms |
| Patient communications | ❌ Not covered | No messaging data | Product has HIPAA-compliant secure messaging |
| Specialty-specific (palliative care) | ❌ Not covered | No palliative assessments in export | **Major gap** — PPS, FAST, ESAS assessments, acuity scores, trend data are core product features; none exported |

**Summary**: Of ~18 applicable domains, the export covers 1 fully (problems), 3 partially (demographics, medications, allergies), and omits 14 entirely — including clinical notes, billing, and specialty-specific palliative care assessments, which are the product's core differentiators.

## 6. Documentation Quality

**Strengths:**
- Field-level data dictionary with name, type, and prose description for each field in 5 sections
- Complete sample JSON export showing real data structure
- Clear description of export mechanism (UI-based, Patients tab → Export button)

**Weaknesses:**
- No machine-readable schema (no JSON Schema, no OpenAPI specification)
- CaseList section (30 fields) appears in sample JSON but has zero documentation
- Two Meds fields (RxNtCode, IsDiscontinued) in sample but not in dictionary
- No value sets or coded value documentation
- No relationship/foreign key documentation
- No description of what the export does NOT include
- Type error: KinList.LastName listed as "Date" type
- Only 10 pages total, including 3 pages of sample JSON and boilerplate

**Could a developer build an import?** Partially. The documented sections are clear enough to parse, but the undocumented CaseList section and missing fields would require guesswork. The export is simple enough (flat JSON with nested arrays) that parsing is straightforward, but understanding the data semantics is limited by thin descriptions.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only 5 documented data sections (Patient, KinList, Meds, Allergies, Problems) totaling 48 documented fields. This is essentially a clinical summary — demographics, active medication list, allergies, and problem list — which maps almost exactly to a C-CDA CCD or USCDI core data. The product stores substantially more: clinical encounter notes with specialty-specific palliative care assessments (PPS, FAST, ESAS), billing data (chronic care billing, CPT codes, Medicare Part B), care plans, vital signs, quality measures, scanned documents, secure messages, and dictation recordings. None of these are in the export. The export represents perhaps 10-15% of what the product stores about patients.

**Axis 2 — Export approach: Purpose-built EHI export (but severely incomplete)**

The export is technically purpose-built: it uses a custom JSON format with the product's native data model (not FHIR, not C-CDA), has its own data dictionary, and is accessed through a dedicated Export button. It is not a repackaging of the (g)(10) FHIR API or C-CDA transitions of care. However, despite being purpose-built, it exports so little data that it fails to achieve the purpose of (b)(10). It appears to be a minimal effort to meet the certification requirement rather than a genuine attempt to export all EHI.

### Key Findings

1. **The export omits clinical notes entirely** — the product's primary value proposition is palliative-care-specific clinical documentation with structured assessments (PPS, FAST, ESAS), voice dictation, and trend analysis. None of this appears in the export. This is the single largest gap. (Source: `170.315b10-Electronic-Health-Information-Export.pdf`, all 10 pages — no notes/encounters section exists)

2. **Only 48 documented fields across 5 sections** — an extremely small export for a certified EHR. By comparison, even the product's own FHIR (g)(10) API exposes more resource types (Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Goal, Immunization, Medication, Procedure, Vital Signs, Provenance) than the (b)(10) export covers. (Source: `SMARTMD-FHIR-API-Documentation-v1.pdf`)

3. **Billing data completely absent despite product capability** — the product supports chronic care billing (PCM, TCM, CCM), Medicare Part B, CPT code recommendations, and time-based billing reports. None of this financial data is in the export. (Source: product-research.md billing features vs. `170.315b10-Electronic-Health-Information-Export.pdf`)

4. **Undocumented CaseList section suggests incomplete implementation** — the sample JSON contains a CaseList with 30 fields including InsuranceList, ExternalContactList, and InternalContactList arrays that are all empty. This suggests the export structure was designed to include more data but was never fully implemented. (Source: sample JSON on pages 7-9 of the b10 PDF)

5. **The (g)(10) FHIR API actually covers more data than the (b)(10) export** — the FHIR API documents endpoints for CarePlan, CareTeam, Goal, Immunization, Procedure, Vital Signs, and Provenance, none of which appear in the (b)(10) JSON export. This is an unusual situation where the clinical exchange API provides broader coverage than the supposedly comprehensive EHI export. (Source: comparing `SMARTMD-FHIR-API-Documentation-v1.pdf` table of contents vs. `170.315b10-Electronic-Health-Information-Export.pdf`)

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Purpose-built EHI export (but severely incomplete)
Export format:   JSON
Entities:        7 (5 documented + 1 undocumented CaseList + 1 wrapper)
Fields:          80 total (48 documented, 32 undocumented from sample)
Descriptions:    62.5% of fields (48 of 80; 100% of documented fields)
Sample data:     Yes (embedded in PDF)
Bulk export:     Yes (multi-patient selection)
Domains covered: 4 of 18 applicable domains (1 full, 3 partial)
```

### Bottom Line

The SMARTMD Palliative (b)(10) export provides a bare-minimum clinical summary (demographics, medications, allergies, problems) in a custom JSON format — roughly equivalent to what a C-CDA CCD would contain, but with fewer fields. A patient or provider would **not** get a usable or complete copy of their data: clinical notes, palliative care assessments, billing records, care plans, vital signs, and all specialty-specific data are entirely missing. The single biggest gap is the complete absence of clinical documentation — the product's core function.
