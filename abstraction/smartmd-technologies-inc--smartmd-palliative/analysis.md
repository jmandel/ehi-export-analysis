# EHI Export Analysis: SMARTMD Technologies, Inc.

**Product**: SMARTMD Palliative  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.11.09.3194.SMDP.06.00.1.240531 (CHPL listing #11476)

## 1. Product Context

SMARTMD Palliative is a palliative care-specific EHR and practice management system designed for hospice organizations adding palliative care programs. Certified in May 2024 as Version 6, it serves palliative care providers, social workers, chaplains, and billing staff.

**Key data-generating capabilities:**
- **Clinical documentation**: Palliative-specific encounter notes with structured assessments (PPS, FAST, ESAS), voice dictation with transcription, mobile documentation
- **Billing & reimbursement**: Chronic care billing (PCM, TCM, CCM), time-tracking for billable minutes, CPT code recommendations, Medicare Part B billing, month-end billing generation
- **Patient management**: Demographics, next of kin/caregivers, scheduling, patient boards
- **Care coordination**: HIPAA-compliant secure messaging, care plans, CMS GUIDE model documentation
- **Documents**: Scanned consent forms, images, attachments
- **Integrations**: Axxess Palliative Care integration (demographics, admissions, discharges, diagnoses), C-CDA receive/display, FHIR API
- **Quality/compliance**: MIPS/MACRA registry, clinical quality measures, acuity/PPS trend tracking

This product stores substantial clinical, billing, and specialty-specific data. A complete EHI export should cover clinical notes, structured palliative assessments, billing/charge data, care plans, documents, and secure messages — in addition to the standard demographics, medications, allergies, and problems.

## 2. Artifacts Reviewed

| Artifact | Description | Size | Informativeness |
|---|---|---|---|
| `170.315b10-Electronic-Health-Information-Export.pdf` | Primary b(10) EHI export documentation. 10-page PDF with field-level data dictionary for 5 sections and sample JSON | 173 KB, 10 pages | **Primary** — most informative artifact |
| `SMARTMD-ONC-Disclosure-Statement-2024-Leidos-b10.pdf` | ONC Disclosure Statement listing all certified criteria | 137 KB, 2 pages | Confirmatory — validates certification scope |
| `SMARTMD-FHIR-API-Documentation-v1.pdf` | FHIR API documentation for g(10) — 16 FHIR resource types | 587 KB, 58 pages | Context — shows g(10) scope separate from b(10) |
| `API.json` | FHIR Bundle with Direct messaging Endpoints and Organizations for h(1) | 4 KB | Irrelevant — Direct messaging config, not EHI export |
| `compliance-page-screenshot.png` | Screenshot of smartmd.com/compliance page | 292 KB | Confirmatory — shows all available documentation links |

The EHI export PDF is the only artifact relevant to b(10). No sample export files, no machine-readable schemas, no data dictionaries in HTML/JSON/CSV format were provided.

## 3. Export Mechanics

- **Format**: Proprietary JSON (not FHIR, not C-CDA)
- **Mechanism**: UI-driven — users navigate to the Patients tab, select one or more patients, and tap "Export"
- **Scope**: One patient per export file
- **Bulk capability**: Multiple patients can be selected and exported, but each produces a separate JSON file
- **Access constraints**: Requires "credentialed and authorized user" access; no separate API endpoint for export
- **Fees**: Not specified in documentation; the ONC Disclosure Statement notes additional annual subscription fees for relied-upon software (EMR Direct), but this applies to b(1)/h(1), not b(10)

## 4. Export Content: What's In It

The export produces a JSON file per patient containing 5 documented sections and 1 undocumented section (CaseList, visible only in the sample JSON). Based on parsing the PDF data dictionary and the embedded sample JSON (see `analysis/full-entity-inventory.json`):

### Summary Statistics

| Metric | Value |
|---|---|
| Total entities (sections) | 8 (5 documented + 3 undocumented) |
| Total fields | 91 |
| Fields with descriptions | 48 (52.7%) |
| Fields with types | 91 (100%) |
| Value sets documented | 0 |
| Foreign keys documented | 0 |
| Relationships | Implicit via PatientId only |
| Sample data | Yes (1 complete patient record in PDF) |

### Vendor's own content organization

The vendor documents 5 sections explicitly. The CaseList section and its nested CaseProvider sub-object are present in the sample JSON but have zero documentation (no field descriptions).

| Entity/Table | Fields | Described | Types | Documented? |
|---|---|---|---|---|
| ExportRoot | 2 | 0 | yes | No (inferred from sample) |
| Patient | 15 | 14 | yes | Yes — demographics |
| KinList | 11 | 10 | yes | Yes — caregivers/relatives |
| Meds | 16 | 13 | yes | Yes — medications |
| Allergies | 4 | 4 | yes | Yes — drug/food/environmental allergies |
| ClinicalSummaryProblemDetailsList | 7 | 7 | yes | Yes — diagnoses/problems |
| CaseList | 30 | 0 | yes | **No** — found only in sample JSON |
| CaseList.CaseProvider | 6 | 0 | yes | **No** — nested within CaseList |

**Notable observations:**

1. **CaseList is entirely undocumented** but contains 30 fields including provider assignments, patient location, case status, diagnosis, insurance list, external/internal contact lists, and creation timestamps. This is the richest section in the export but has zero descriptions.

2. **Meds section has 3 undocumented fields** visible in the sample: `RxNtCode` (appears to be an RxNorm code — "209964"), `IsDiscontinued` (boolean), and `DoseQuanity` (note the typo — differs from documented `DoseQuantity`). The `DoseQuanity` / `DoseQuantity` mismatch suggests a documentation-vs-implementation discrepancy.

3. **Patient section has 1 undocumented field**: `AccountId` (integer, value 99 in sample).

4. **KinList has 1 undocumented field**: `AccountId` (integer).

5. **KinList.LastName is documented as type "date"** — clearly a typo in the PDF; the sample shows it as a string ("Smith").

6. **InsuranceList, ExternalContactList, InternalContactList** appear as empty arrays in the CaseList sample — their field structures are unknown.

7. **No clinical notes, assessments, care plans, billing data, documents, or secure messages** appear anywhere in the export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's b(10) export covers a narrow slice of patient data organized into 5 explicitly documented sections:

- **Patient demographics** (14 documented fields): Name, DOB, address, phone numbers, email, chart ID, service line. Standard but thorough for basic demographics.
- **KinList** (10 documented fields): Caregiver/relative contacts with relationship, decisional authority, and deceased flag. Useful for palliative care workflows.
- **Medications** (13 documented fields): Drug name, strength, form, dosing, start/end dates, instructions, status. Reasonable medication list with RxNorm codes in sample (but undocumented).
- **Allergies** (4 documented fields): Allergen, reaction, status. Minimal but complete for basic allergy list.
- **Problems** (7 documented fields): ICD-10 coded diagnoses with onset/resolution dates, primary diagnosis flag. Good structured problem list.

The undocumented **CaseList** section (30 fields) adds case/service line context, provider assignments, and placeholder arrays for insurance and contacts — but with zero documentation, its contents are interpretable only from the sample.

This is essentially **a patient clinical summary** — the same information available through a C-CDA CCD or FHIR USCDI export. The vendor's FHIR API (g(10)) actually covers *more* resource types (16 FHIR resources including CarePlan, CareTeam, Goal, Immunization, Procedure, VitalSigns, DiagnosticReport, DocumentReference, Provenance) than the b(10) export's 5-6 sections.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (15 fields), `KinList` (11 fields) | Thorough for basic demographics |
| Encounters / visits | ⚠️ Partial | `CaseList` has case-level data (undocumented, 30 fields) but no encounter-level clinical content | Product documents clinical encounters; only case metadata is exported |
| Problems / conditions / diagnoses | ✅ Covered | `ClinicalSummaryProblemDetailsList` (7 fields, ICD-10 coded) | Adequate |
| Medications / prescriptions | ✅ Covered | `Meds` (16 fields incl. undocumented RxNorm) | Adequate for medication list |
| Allergies | ✅ Covered | `Allergies` (4 fields) | Minimal but complete |
| Immunizations | ❌ Not covered | No immunization data in export | FHIR API supports Immunization; unclear if product stores this routinely for palliative care — possible minor gap |
| Vitals | ❌ Not covered | No vitals data in export | FHIR API supports VitalSigns; palliative care tracks vitals — gap |
| Lab results | ❌ Not covered | No lab data in export | Palliative care may rely on external systems — possible N/A |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data in export | Likely N/A for palliative care specialty |
| Procedures | ❌ Not covered | No procedure data in export | FHIR API supports Procedure; possible gap |
| Clinical notes / documents | ❌ Not covered | No notes, dictation transcripts, or documents in export | **Critical gap** — clinical documentation is the product's primary function |
| Care plans / goals | ❌ Not covered | No care plan or goal data in export | FHIR API supports CarePlan and Goal; **significant gap** for palliative care |
| Orders / referrals | ❌ Not covered | No order data in export | Product supports CPOE (a)(1), (a)(2) — gap |
| Insurance / coverage | ⚠️ Partial | `CaseList.InsuranceList` array exists but is empty in sample; no field documentation | Structure present but content unknown |
| Claims / billing | ❌ Not covered | No billing, charges, CPT codes, or time-tracking data in export | **Critical gap** — product has detailed chronic care billing (PCM, TCM, CCM) |
| Payments | ❌ Not covered | No payment data in export | Product does Medicare Part B billing — gap |
| Consents / directives | ❌ Not covered | No consent or advance directive data in export | Product handles scanned consent forms — gap |
| Patient communications / portal messages | ❌ Not covered | No secure messages in export | Product has HIPAA-compliant team messaging — gap |
| Specialty-specific (palliative care assessments) | ❌ Not covered | No PPS, FAST, ESAS, acuity scores, or specialty assessments in export | **Critical gap** — these are the product's defining clinical instruments |

**Summary**: The export covers 4 of 19 standard domains fully, 2 partially, and 13 not at all. Of those 13, at least 6 represent data the product clearly stores (clinical notes, palliative assessments, billing, care plans, orders, secure messages), making them genuine gaps rather than N/A.

## 6. Documentation Quality

**Strengths:**
- Dedicated b(10) PDF document (not just a link to the FHIR API)
- Field-level documentation with names, types, and descriptions for 5 sections
- Complete sample JSON showing a realistic patient record
- Clear description of the export mechanism (UI workflow)

**Weaknesses:**
- **CaseList section (30 fields, 40% of fields in sample) is entirely undocumented** — no field names, types, or descriptions in the data dictionary tables despite being present in the sample output
- **No machine-readable schema** — no JSON Schema, no OpenAPI spec; only a PDF
- **No value sets** — fields like `Case`, `Status`, `RelationshipList` have no enumerated valid values
- **No foreign key documentation** — relationships between entities are only implicit via `PatientId`
- **No cardinality** — arrays have no min/max documentation
- **Typos and inconsistencies** — `KinList.LastName` documented as type "date"; `DoseQuanity` vs `DoseQuantity` mismatch between sample and documentation; `ChartID` vs `ChartId` casing inconsistency
- **No versioning strategy** beyond "2024v1"

**Could a developer build an import?** For the documented 5 sections — yes, with some guesswork on value sets. For the undocumented CaseList — only by reverse-engineering the sample JSON. For the product's full clinical data — no, because notes, assessments, billing, and documents are not in the export at all.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The export covers only basic patient summary data (demographics, meds, allergies, problems) — approximately the same scope as a C-CDA CCD or USCDI core data set. For a palliative care EHR whose primary value is clinical documentation, structured assessments (PPS, FAST, ESAS), and specialty billing, the export omits the vast majority of patient-specific EHI the product stores. The 91 fields across 8 entities represent a fraction of the product's data model.

### Key Findings

1. **The b(10) export is functionally a clinical summary, not an "all EHI" export.** It covers demographics, medications, allergies, and problems — the same data already available through the vendor's g(10) FHIR API, which actually exposes *more* resource types (16 FHIR resources vs. 5 JSON sections). The b(10) export adds less coverage than the g(10) API.

2. **Clinical notes — the product's core function — are entirely absent from the export.** SMARTMD Palliative is fundamentally a palliative care documentation system with specialty templates, voice dictation, and mobile documentation. No encounter notes, dictation transcripts, or clinical documents appear in the export. (Source: `170.315b10-Electronic-Health-Information-Export.pdf`, all 10 pages reviewed.)

3. **Specialty palliative care assessments (PPS, FAST, ESAS) are missing.** These structured clinical instruments track patient trajectory toward hospice and are central to the product's clinical value. Their absence is a major gap for a palliative care-specific EHR. (Source: product-research.md documents these as key features; not present in export PDF.)

4. **Billing and charge data are completely absent.** The product has detailed time-based chronic care billing (PCM, TCM, CCM) with CPT code recommendations and Medicare Part B support. No billing entities appear in the export. (Source: product-research.md vs. `170.315b10-Electronic-Health-Information-Export.pdf`.)

5. **40% of the export's fields (CaseList, 30 fields) are undocumented.** The CaseList section appears in the sample JSON with provider assignments, location data, insurance arrays, and contact lists, but has zero documentation in the field-level tables — meaning even the data that *is* exported is incompletely documented. (Source: comparison of PDF data dictionary tables pp. 3-6 vs. sample JSON pp. 7-9.)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Proprietary JSON (per-patient)
Model type:      Custom projection (not native database, not standard)
Entities:        8 (5 documented, 3 undocumented)
Fields:          91 (48 with descriptions, 52.7%)
Descriptions:    52.7% of fields have descriptions
Sample data:     Yes (1 patient in PDF)
Bulk export:     Per-patient files; multi-select available
Domains covered: 4 of 15 applicable domains (+ 2 partial)
```

### Bottom Line

SMARTMD Palliative's b(10) export is a patient demographic summary with medication, allergy, and problem lists — roughly equivalent to what their FHIR API already provides under g(10). For a palliative care EHR whose defining value is clinical documentation, specialty assessments, and chronic care billing, the export omits the majority of patient-specific EHI the product stores. A patient or provider requesting their complete record would receive only a fraction of the data held by the system.
