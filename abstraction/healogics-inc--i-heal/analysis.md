# EHI Export Analysis: Healogics, Inc.

**Product**: i-heal 2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1575.ihea.02.00.1.191007

## 1. Product Context

i-heal 2.0 is a proprietary, web-based EMR designed specifically for wound care, built and used internally by Healogics, Inc. — the nation's largest wound care services company, operating 600+ hospital-based outpatient Wound Care Centers. It is not a general-purpose EHR; its clinical domain is highly specialized around wound assessment, treatment, and healing outcomes.

**Key data domains the product stores:**
- **Wound care clinical data**: wound assessments, wound measurements/photographs, treatment plans, healing progress, wound etiologies, debridement records, negative pressure wound therapy (NPWT), dermal matrix substitutes, compression therapy, topical growth factors, total contact casts, skin perfusion pressure measurements
- **Hyperbaric oxygen therapy (HBO)**: treatment courses, pre-treatment evaluations, safety checklists, screening checklists
- **Ostomy/stoma care**: stoma assessments, treatment notes, pre-operative documentation
- **General clinical data**: demographics, problem lists, allergies, immunizations, vital signs, medications/prescriptions, physician orders, test results, progress notes, physical exams, HPI, chief complaints
- **Specialty assessments**: neuropathy, lower extremity, fall risk, pressure ulcer risk, nutrition risk, pain assessment, conservative patient assessment
- **Care plans and education**: multidisciplinary care plans, patient/caregiver education
- **Billing**: SuperBill documentation (E&M coding, CPT codes)
- **Documents and media**: custom scanned documents, wound photographs, patient communications
- **Custom forms**: 9 configurable custom form types (CustomForm1-3, 5-10; no CustomForm4)

**What the export should cover**: All wound care clinical documentation, HBO therapy records, specialty assessments, billing/superbill data, patient communications, prescriptions, orders, test results, and demographic data. This is a specialty-focused product, so the data universe is narrower than a full hospital EHR but deep within its wound care domain.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `EHIExport-iheal-2.pdf` | 237 KB, 10 pages | Primary (b)(10) EHI export documentation. Describes proprietary XML export format, lists 69 document types, explains relationships, signatures, and file references. References an unpublished companion Data Dictionary. | **Most informative** — defines the export structure and document types |
| `Healogics-FHIR-g10-Documentation.pdf` | 999 KB, ~40 pages | FHIR R4 (g)(10) API docs covering standard US Core profiles. Separate system from (b)(10) export. | Useful for comparison — confirms (b)(10) is distinct from (g)(10) |
| `RegistrationHelpv1.pdf` | 774 KB, 51 pages | Integration API registration guide | Low — administrative, not EHI-relevant |
| `AuthenticationHelpv1.pdf` | 595 KB, 28 pages | Integration API authentication guide | Low — administrative |
| `PatientSearchHelpv1.pdf` | 556 KB, 22 pages | Integration API patient search guide | Low — administrative |
| `DataRequestHelpv1.pdf` | 431 KB, 8 pages | C-CDA data request API guide | Low — separate from (b)(10) |
| `certified-ehr-technology.html` | 52 KB | Main certification page HTML | Low — link hub only |
| `certified-ehr-technology-screenshot.png` | 1.4 MB | Screenshot of certification page | Low — visual record |

## 3. Export Mechanics

- **Format**: Proprietary XML documents packaged in a ZIP archive. Each clinical record is a separate XML file named `<documentType>_<documentId>.xml`, organized into patient folders (`<patientId>/`).
- **Mechanism**: UI feature within i-heal 2.0, accessible to users with Facility Administration or Emergency Access roles.
- **Single-patient**: Yes — export can be requested for a single patient.
- **Bulk capability**: Yes — export can be requested for all patients within a facility.
- **Processing time**: Usually within 48 hours after request.
- **Photo/file access**: External photos and files are accessed via secure URLs included in the XML (Azure Blob Storage SAS tokens). These URLs expire 90 days after export.
- **Access constraints**: Requires Facility Administration or Emergency Access user role. No fee information documented.

## 4. Export Content: What's In It

### Structure overview

The export contains 69 distinct XML document types organized into 4 categories. Every document shares a common `<DocumentProperties>` element with 25 structural fields (patient identifiers, visit identifiers, provider information, timestamps, facility references). Most documents also include `<ElectronicSignatures>` (5 additional fields) and some include `<FileReferences>` (1 field for photo/file URLs).

**Critical limitation**: The PDF explicitly references a companion document — "EHIExport – Data Dictionary" — that "provides a data dictionary and identifies the elements within each document." This companion document is **not publicly available**. Without it, we can only document the 25 common structural fields and the 69 document type names; the actual clinical data fields within each document type are unknown.

### What's documented (common fields only)

The PDF documents 25 common fields present across all/most documents, plus 5 electronic signature fields and 1 file reference field — **31 total fields documented with descriptions and types**. All 31 have descriptions (100%).

### Vendor's own content organization

| Category | Doc Types | Description |
|---|---|---|
| **Patient Information** | 1 | PatientDocument — demographics, care team, emergency contact, insurance |
| **Treatment Course / Conditions** | 4 | HBO treatment courses, non-wound conditions, stoma/ostomy conditions, wound conditions |
| **Encounter Documentation** | 61 | Clinical documentation per visit: assessments, procedures, orders, prescriptions, vitals, billing, custom forms, care plans, etc. |
| **Non-Encounter Documentation** | 3 | Custom scanned documents, patient communications, test results |

### Document types by clinical domain

| Domain | Document Types | Count |
|---|---|---|
| Wound care | WoundDocument, WoundAssessmentDocument, WoundTreatmentNotesDocument, DebridementDocument, DermalMatrixSubstituteDocument, NPWTApplicationDocument, NPWTMaintenanceDocument, TopicalGrowthFactorDocument, CompressionTherapyDocument, TotalContactCastDocument, MultiWoundChartNotesDocument, SkinPerfusionPressureDocument | 12 |
| HBO therapy | HBOTreatmentCourseDocument, HBODocument, HBOPreTreatmentEvaluationDocument, HBOSafetyChecklistDocument, HBOScreeningChecklistDocument | 5 |
| Stoma/ostomy | StomaDocument, StomaAssessmentDocument, StomaTreatmentNotesDocument, OstomyPreOperativeDocument | 4 |
| Non-wound conditions | NonWoundConditionDocument, NonWoundConditionAssessmentDocument, NonWoundTreatmentNotesDocument | 3 |
| General clinical | AllergyListDocument, ImmunizationsDocument, ProblemListDocument, VitalSignsDocument, PhysicalExamDocument, HPIDocument, ChiefComplaintDocument, ProgressNoteDocument, GeneralVisitNotesDocument | 9 |
| Orders & prescriptions | PhysicianOrdersDocument, PrescriptionDocument, TestResultDocument | 3 |
| Assessments & risk | PainAssessmentDocument, FallRiskDocument, PressureUlcerRiskDocument, NutritionRiskDocument, NeuropathyDocument, LowerExtremityDocument, ConservativePatientAssessmentDocument, HROSDocument | 8 |
| Care plans & education | MultiDisciplinaryCarePlanDocument, NH_EducationAssessmentDocument, NH_PatientCaregiverEducationDocument | 3 |
| Billing | SuperBillDocument | 1 |
| Procedures | BiopsyDocument, IncisionAndDrainageDocument, OtherProcedureDocument | 3 |
| Encounter admin | ArrivalInfoDocument, DischargeInfoDocument, DischargeInstructionsDocument, ClinicLevelOfCareDocument, AncillaryServiceDocument, TCOMDocument | 6 |
| Custom forms | CustomForm1-3, 5-10 Document (9 types) | 9 |
| Documents & communications | CustomScanDocument, PatientCommunicationDocument | 2 |
| Demographics | PatientDocument | 1 |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The i-heal EHI export is clearly purpose-built for (b)(10) compliance and is distinct from the vendor's FHIR (g)(10) API. Key evidence:

1. **Deep wound care specialization**: 12 document types dedicated to wound care workflows alone — wound assessments, treatment notes, debridement, NPWT, dermal substitutes, compression therapy, growth factors, casts, skin perfusion pressure. This goes far beyond what any standard clinical exchange format covers.

2. **HBO therapy coverage**: 5 dedicated document types for hyperbaric oxygen therapy, a core Healogics service with no USCDI/FHIR equivalent.

3. **Stoma/ostomy care**: 4 document types for ostomy-specific documentation.

4. **Specialty risk assessments**: 8 document types covering wound-care-relevant assessments (fall risk, pressure ulcer risk, neuropathy, nutrition risk, lower extremity, pain).

5. **Billing**: SuperBillDocument is included, covering the E&M/CPT coding documentation that the product generates.

6. **Custom forms**: 9 configurable custom form types, ensuring facility-specific data is captured.

7. **Patient communications**: Dedicated PatientCommunicationDocument type.

8. **Breadth**: 69 document types total vs. ~18 FHIR resource types in the (g)(10) API.

**Weaknesses**: The companion Data Dictionary is not publicly available, so we cannot assess field-level depth within each document type. We know the 69 document types exist but not how many fields each contains or what specific data elements they capture.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PatientDocument — demographics, care team, emergency contact, insurance | Described as comprehensive in PDF |
| Encounters / visits | ✅ Covered | VisitID in DocumentProperties; encounter-level documents; ArrivalInfoDocument, DischargeInfoDocument | Visit structure is the organizing principle of the export |
| Problems / conditions | ✅ Covered | ProblemListDocument, NonWoundConditionDocument, WoundDocument | Wound conditions are deeply covered; general problems via ProblemListDocument |
| Medications / prescriptions | ✅ Covered | PrescriptionDocument (child of PhysicianOrdersDocument) | Present; field-level depth unknown |
| Allergies | ✅ Covered | AllergyListDocument | Present; field-level depth unknown |
| Immunizations | ✅ Covered | ImmunizationsDocument | Present; field-level depth unknown |
| Vitals | ✅ Covered | VitalSignsDocument | Present; field-level depth unknown |
| Lab results | ✅ Covered | TestResultDocument (child of PhysicianOrdersDocument), with file attachment support | Covers test results linked to orders |
| Procedures | ✅ Covered | BiopsyDocument, DebridementDocument, IncisionAndDrainageDocument, OtherProcedureDocument, plus numerous wound-specific procedure types (NPWT, dermal matrix, compression therapy, etc.) | Deeply covered for wound care procedures |
| Clinical notes / documents | ✅ Covered | ProgressNoteDocument, GeneralVisitNotesDocument, MultiWoundChartNotesDocument, HPIDocument, ChiefComplaintDocument, CustomScanDocument | Multiple note types covered |
| Care plans / goals | ✅ Covered | MultiDisciplinaryCarePlanDocument | Present |
| Orders / referrals | ⚠️ Partial | PhysicianOrdersDocument covers orders; no dedicated referral document type | Orders are present; referral tracking unclear |
| Insurance / coverage | ✅ Covered | PatientDocument includes insurance information per PDF description | Part of PatientDocument; depth unknown |
| Claims / billing | ✅ Covered | SuperBillDocument | SuperBill is the billing artifact for outpatient wound care; appropriate for this product's scope |
| Patient communications | ✅ Covered | PatientCommunicationDocument | Dedicated document type |
| Specialty — wound care | ✅ Covered | 12 wound-specific document types covering assessments, treatments, procedures | This is the product's core domain — deeply covered |
| Specialty — HBO therapy | ✅ Covered | 5 HBO-specific document types | Core Healogics service — well covered |
| Specialty — stoma/ostomy | ✅ Covered | 4 stoma-specific document types | Covered |
| Specialty — risk assessments | ✅ Covered | 8 assessment document types (fall risk, pressure ulcer risk, neuropathy, nutrition, pain, etc.) | Wound-care-relevant assessments covered |
| Imaging / diagnostic reports | ⚠️ Partial | Wound photographs via FileReferences in assessment documents; no dedicated diagnostic imaging document type | Wound photos are covered; general diagnostic imaging may not be applicable to this product |
| Consents / directives | ❌ Not covered | No consent or advance directive document type visible | Unclear if product stores these; may be handled by host hospital |
| Payments | ❌ Not covered | No payment/remittance document type | Unclear if i-heal processes payments or if billing goes through the host hospital's system; may be N/A |

## 6. Documentation Quality

**Strengths:**
- The export format documentation (EHIExport-iheal-2.pdf) is well-structured and clearly written
- Common data elements (DocumentProperties, ElectronicSignatures, FileReferences) are fully documented with XML examples
- Document relationships (parent-child) are clearly defined
- The export mechanism is clearly described (UI feature, roles required, processing time)
- Both single-patient and bulk export are supported

**Weaknesses:**
- **The companion Data Dictionary is not publicly available.** This is a significant gap. The PDF states: "Refer to the companion EHIExport – Data Dictionary document for a detailed definition of each document archive type." Without this document, a developer cannot understand the specific fields within any of the 69 document types beyond the shared structural fields.
- No sample data is provided
- No machine-readable schema (XSD, JSON Schema) is published
- No value sets or code systems are documented
- A developer could understand the overall structure and relationships from the public PDF but would need the unpublished Data Dictionary to actually parse the clinical content of any document

**Could a developer build an import from this documentation alone?** No. The public documentation tells you how to navigate the ZIP structure, identify patients and visits, and relate documents to each other — but the actual clinical fields within each document type are undocumented without the companion Data Dictionary.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive** (relative to what this specialty product stores)

The export covers 69 document types spanning virtually every data domain this wound-care-focused EMR manages: wound assessments, HBO therapy, stoma/ostomy care, prescriptions, orders, test results, billing (SuperBill), patient communications, custom forms, risk assessments, care plans, and patient demographics/insurance. The export goes far beyond USCDI clinical summary data — it includes 12 wound-specific document types, 5 HBO therapy types, 8 specialty risk assessment types, 9 custom form types, and a SuperBillDocument for billing. This represents the full breadth of what a wound care EMR stores about patients. The few potentially missing domains (consents, payments) are plausibly handled by the host hospital's systems rather than i-heal itself, since Healogics operates within hospital facilities.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. Key evidence:
1. The export uses a proprietary XML format designed specifically for this purpose — it is not C-CDA, not FHIR, not a repackaging of the (g)(10) API
2. It covers 69 document types vs. ~18 FHIR resource types in the separate (g)(10) API
3. It includes wound-care-specific data types (NPWT, dermal matrix, compression therapy, HBO) that have no representation in standard clinical exchange formats
4. It includes SuperBillDocument (billing) and PatientCommunicationDocument, which are outside USCDI scope
5. The PDF is authored by Net Health (the development partner), dated November 2023, and describes a dedicated UI feature — not a documentation afterthought
6. The export supports both single-patient and bulk (facility-wide) export

### Key Findings

1. **Purpose-built, wound-care-deep export**: The 69 XML document types demonstrate a genuine effort to export all clinical documentation stored in i-heal, including deep specialty data (wound care, HBO, stoma) that has no standard exchange equivalent. This is not a repackaged C-CDA or FHIR API.

2. **Critical gap: Data Dictionary not publicly available**: The PDF explicitly references a companion "EHIExport – Data Dictionary" that defines the fields within each document type. Without it, only the 25 common structural fields are documented. The actual clinical content of each document type is opaque to external review.

3. **Billing included via SuperBillDocument**: The presence of a dedicated billing document type is notable — many vendors omit billing entirely from their (b)(10) exports.

4. **Custom forms captured**: 9 custom form types (CustomForm1-3, 5-10) ensure facility-specific questionnaires and assessments are exported, not just standard clinical data.

5. **Photo/file access has a 90-day expiration**: External file references (wound photographs, scanned documents, test result files) expire 90 days after export. This is a practical limitation — if a patient or provider doesn't download these within that window, the linked media becomes inaccessible.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   Proprietary XML in ZIP archive
Entities:        69 document types
Fields:          31 documented (common fields only; companion Data Dictionary not public)
Descriptions:    100% of documented fields have descriptions
Sample data:     No
Bulk export:     Yes (single-patient and facility-wide)
Domains covered: 16 of 18 applicable domains (consents and payments unclear/N/A)
```

### Bottom Line

Healogics built a genuine, purpose-specific EHI export that covers the full breadth of its wound care EMR — 69 XML document types spanning clinical assessments, specialty procedures, HBO therapy, billing, communications, and custom forms. The single most significant gap is the unpublished companion Data Dictionary: without it, external reviewers cannot verify the depth of field-level coverage within each document type, and developers cannot build an import without requesting the document from Healogics/Net Health directly.
