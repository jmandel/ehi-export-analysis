# EHI Export Analysis: Healogics, Inc.

**Product**: i-heal 2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1575.ihea.02.00.1.191007

## 1. Product Context

Healogics, Inc. is the nation's largest provider of advanced wound care services, operating over 600 hospital-based outpatient Wound Care Centers. i-heal 2.0 is their proprietary, internal-use EMR designed specifically for wound care. It is not sold externally — it is used across Healogics' managed network. The software is built by Net Health.

**Data the product stores (relevant to export completeness):**
- **Core wound care clinical data**: wound assessments, wound photographs/measurements, treatment plans, healing progress tracking, debridement documentation, compression therapy, negative pressure wound therapy (NPWT), skin substitutes, topical growth factor treatments
- **Hyperbaric oxygen (HBO) therapy**: treatment courses, pre-treatment evaluations, safety checklists, screening
- **Ostomy/stoma care**: stoma assessments, treatment notes, pre-operative documentation
- **Standard clinical data**: demographics, problem lists, medication lists, allergy lists, immunizations, vital signs, lab results, prescriptions, physician orders, progress notes, physical exams
- **Specialty assessments**: neuropathy, lower extremity, nutrition risk, fall risk, pressure ulcer risk, pain, skin perfusion pressure
- **Billing/documentation support**: superbill documentation, E&M coding support (though full claims may be handled by host hospital systems)
- **Patient portal**: view/download/transmit, patient-generated health data
- **Care coordination**: C-CDA send/receive, clinical reconciliation, FHIR API
- **Custom forms**: up to 10 facility-customizable forms
- **Scanned documents and wound photographs**: stored in Azure Blob Storage

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHIExport-iheal-2.pdf` (10 pages, 237 KB) | Primary (b)(10) EHI Export documentation. Describes proprietary XML export format, 69 document types, parent-child relationships, common structural elements. Dated 2023-11-16, authored by Amanda Quinones at Net Health. | **Most informative** — sole source of (b)(10) export details |
| `Healogics-FHIR-g10-Documentation.pdf` (40 pages, 999 KB) | FHIR R4 API documentation for (g)(10). Covers 21 US Core profiles. Separate system from b(10) export. | Informative for understanding what FHIR covers vs. what b(10) adds |
| `DataRequestHelpv1.pdf` (8 pages, 431 KB) | Pre-FHIR C-CDA retrieval API. Covers standard clinical summary data only. | Low — narrower scope than b(10) export |
| `RegistrationHelpv1.pdf` (51 pages, 774 KB) | Integration API vendor registration guide. | Low — process documentation, not data content |
| `AuthenticationHelpv1.pdf` (28 pages, 595 KB) | Integration API authentication guide. | Low — auth mechanics only |
| `PatientSearchHelpv1.pdf` (22 pages, 556 KB) | Patient search and demographics API guide. | Low — search mechanics only |
| `certified-ehr-technology.html` (52 KB) | Saved HTML of certification page with all documentation links. | Orientation — confirms what docs are linked |
| `certified-ehr-technology-screenshot.png` (1.4 MB) | Full-page screenshot of certification page. | Low — visual confirmation only |

**Companion Data Dictionary**: The EHI Export PDF references "EHIExport – Data Dictionary" as a companion document that provides field-level definitions for each document type. This document is **not publicly available** — not linked on the certification page, not found via URL probing (dozens of patterns tested, all return 404), and not found via web search. This is the most significant documentation gap.

## 3. Export Mechanics

- **Format**: Proprietary XML. Each patient's data is organized into individual XML files named `<documentType>_<documentId>.xml`.
- **Delivery**: ZIP file download from within i-heal 2.0. Processed asynchronously, "usually within 48 hours."
- **Access**: Available to users with Facility Administration or Emergency Access roles.
- **Single-patient vs bulk**: Supports export of either a single patient or all patients at a facility.
- **Photos/files**: Wound photos and scanned documents are referenced via time-limited Azure Blob Storage URLs that expire 90 days after export. The archive is not fully self-contained.
- **Cost**: No explicit export fee mentioned. Mandatory disclosure mentions only a $250/year fee for Direct messaging via Secure Exchange Solutions.

The export is **not** FHIR or C-CDA — it is a purpose-built, proprietary XML format distinct from the (g)(10) FHIR API. This separation is a positive sign that the vendor did not simply repackage their FHIR/C-CDA capabilities.

## 4. Export Content: What's In It

### Document type inventory

The EHI Export PDF enumerates **69 document types** organized into 4 categories. The PDF provides brief descriptions for 5 entities (PatientDocument and the 4 Treatment Course/Condition types) but no field-level detail for any document type.

**Critical limitation**: The companion Data Dictionary — which would provide field-level definitions — is not publicly available. Without it, we know *what types* of documents are exported but not *what fields* each document contains.

### Common structural elements (documented)

Every document XML file contains a `<DocumentProperties>` block with **25 common fields** (see `analysis/full-entity-inventory.json`), including:
- Patient identifiers (ID, name, MRN, DOB)
- Visit/encounter identifiers
- Parent document relationships
- Provider and clinician identifiers
- Timestamps (date added, last updated)
- Facility identifiers

Most documents also support **electronic signatures** (5 fields per signature: UserID, name, date signed, credentials).

Documents supporting photos/files include `<FileReferences>` with Azure Blob Storage URLs.

### Vendor's own content organization

| Category | Document Types | Descriptions Available | Field-Level Detail |
|---|---|---|---|
| Patient Information | 1 | 1 (brief) | No — requires missing Data Dictionary |
| Treatment Course / Conditions | 4 | 4 (brief) | No — requires missing Data Dictionary |
| Encounter Documentation | 61 | 0 | No — requires missing Data Dictionary |
| Non-Encounter Documentation | 3 | 0 | No — requires missing Data Dictionary |
| **Total** | **69** | **5** | **0** |

### Representative document types by clinical domain

**Wound care (core specialty)**:
- WoundDocument, WoundAssessmentDocument, WoundTreatmentNotesDocument
- DebridementDocument, CompressionTherapyDocument, DermalMatrixSubstituteDocument
- NPWTApplicationDocument, NPWTMaintenanceDocument
- TopicalGrowthFactorDocument, TotalContactCastDocument
- SkinPerfusionPressureDocument, BiopsyDocument, IncisionAndDrainageDocument

**HBO therapy**:
- HBOTreatmentCourseDocument, HBODocument, HBOPreTreatmentEvaluationDocument
- HBOSafetyChecklistDocument, HBOScreeningChecklistDocument

**Ostomy/stoma**:
- StomaDocument, StomaAssessmentDocument, StomaTreatmentNotesDocument, OstomyPreOperativeDocument

**Standard clinical**:
- AllergyListDocument, ImmunizationsDocument, ProblemListDocument, VitalSignsDocument
- PrescriptionDocument, PhysicianOrdersDocument, TestResultDocument
- ProgressNoteDocument, PhysicalExamDocument, HPIDocument, ChiefComplaintDocument

**Risk assessments**:
- FallRiskDocument, NutritionRiskDocument, PainAssessmentDocument
- PressureUlcerRiskDocument, NeuropathyDocument, LowerExtremityDocument

**Billing/administrative**:
- SuperBillDocument
- DischargeInfoDocument, DischargeInstructionsDocument
- ArrivalInfoDocument, ClinicLevelOfCareDocument, AncillaryServiceDocument

**Patient communications & custom**:
- PatientCommunicationDocument, CustomScanDocument
- CustomForm1-10Documents (9 of 10 slots present: 1,2,3,5,6,7,8,9,10 — CustomForm4Document is absent)

**Outcome measures**:
- TCOMDocument, HROSDocument

### Parent-child relationship structure

The export has a well-documented hierarchical structure:

- **WoundDocument** → 11 child document types (wound assessments, debridement, treatments, etc.)
- **NonWoundConditionDocument** → 7 child document types
- **StomaDocument** → 3 child document types
- **HBOTreatmentCourseDocument** → HBODocument
- **PhysicianOrdersDocument** → PrescriptionDocument, TestResultDocument
- **NPWTApplicationDocument** → NPWTMaintenanceDocument

This allows full reconstruction of the clinical hierarchy: Patient → Condition/Treatment Course → Encounter observations and procedures.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes their export into 4 categories:

1. **Patient Information** (1 type): Demographics, care team, emergency contact, insurance. Brief description provided but no field list.

2. **Treatment Course / Conditions** (4 types): Wound, HBO treatment course, non-wound condition, and stoma/ostomy conditions. Each has brief descriptions mentioning key data elements (etiologies, location, status). These are parent documents that span multiple encounters.

3. **Encounter Documentation** (61 types): The bulk of the export. Covers an impressively wide range of wound care-specific clinical data — from standard items (allergies, vitals, problem list) to highly specialty-specific (HBO safety checklists, NPWT maintenance, dermal matrix substitutes, compression therapy). Also includes billing (SuperBillDocument), care planning, discharge documentation, patient education, risk assessments, and up to 10 custom forms. No descriptions provided for any encounter document type.

4. **Non-Encounter Documentation** (3 types): Scanned documents, patient communications, and test results.

**Strongest coverage**: Wound care specialty data — with 14+ wound/procedure-specific document types plus 5 HBO-specific types and 4 ostomy/stoma types, this is genuinely deep specialty coverage.

**Thinnest area**: Billing — only SuperBillDocument is present. This may reflect the reality that detailed billing/claims processing is handled by host hospital systems, not i-heal itself.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PatientDocument (demographics, care team, emergency contact, insurance) | Product stores this; export includes it |
| Encounters / visits | ✅ Covered | 61 encounter document types with VisitID linking; ArrivalInfoDocument | Encounters are the core organizational unit of the export |
| Problems / conditions / diagnoses | ✅ Covered | ProblemListDocument, WoundDocument, NonWoundConditionDocument, StomaDocument | Covered through both standard and specialty-specific document types |
| Medications / prescriptions | ✅ Covered | PrescriptionDocument (child of PhysicianOrdersDocument) | Present in export |
| Allergies | ✅ Covered | AllergyListDocument | Present in export |
| Immunizations | ✅ Covered | ImmunizationsDocument | Present in export |
| Vitals | ✅ Covered | VitalSignsDocument | Present in export |
| Lab results | ✅ Covered | TestResultDocument (child of PhysicianOrdersDocument); supports file attachment | Present in export |
| Imaging / diagnostic reports | ⚠️ Partial | Wound photos via FileReferences in WoundAssessmentDocument and others; no dedicated radiology/imaging document type | Wound photography is well-covered; no evidence of diagnostic imaging reports beyond wound photos |
| Procedures | ✅ Covered | DebridementDocument, BiopsyDocument, IncisionAndDrainageDocument, NPWTApplicationDocument, OtherProcedureDocument, DermalMatrixSubstituteDocument, CompressionTherapyDocument, TopicalGrowthFactorDocument, TotalContactCastDocument | Exceptionally deep specialty procedure coverage |
| Clinical notes / documents | ✅ Covered | ProgressNoteDocument, GeneralVisitNotesDocument, HPIDocument, ChiefComplaintDocument, PhysicalExamDocument, MultiWoundChartNotesDocument, CustomScanDocument | Multiple note types plus scanned document support |
| Care plans / goals | ✅ Covered | MultiDisciplinaryCarePlanDocument, DischargeInfoDocument, DischargeInstructionsDocument | Present in export |
| Orders / referrals | ⚠️ Partial | PhysicianOrdersDocument present; no explicit referral document type | Orders covered; referrals may be embedded in discharge/care plan documents but no dedicated type |
| Insurance / coverage | ✅ Covered | Insurance information within PatientDocument | Present per document description |
| Claims / billing | ⚠️ Partial | SuperBillDocument only | Product supports billing documentation for "accurate claims and maximum reimbursements" but detailed charge/payment/claim data may be handled by host hospital systems. SuperBillDocument captures encounter-level billing documentation but likely not full claims lifecycle. |
| Payments | ❌ Not covered | No payment-related document type | If payment processing is handled by hospital systems rather than i-heal, this may be N/A |
| Consents / directives | ❌ Not covered | No consent or advance directive document type | Unclear if i-heal stores this data; may be handled by host hospital EHR |
| Patient communications / portal messages | ✅ Covered | PatientCommunicationDocument | Present in export |
| Specialty-specific (wound care) | ✅ Covered | 14+ wound procedure types, 5 HBO types, 4 ostomy/stoma types, 6 risk assessment types, outcome measures (TCOMDocument, HROSDocument) | This is the product's core strength — exceptional specialty data coverage |
| Patient education | ✅ Covered | NH_EducationAssessmentDocument, NH_PatientCaregiverEducationDocument | Present in export |

**Gap Analysis Summary**: The export covers all major clinical data domains that i-heal stores. The main gaps are:
- **Payments**: Likely N/A — payment processing appears to be handled by host hospital systems, not i-heal
- **Consents/directives**: Unclear if stored in i-heal; may be handled by hospital EHR
- **Referrals**: No dedicated document type, but may be embedded in other documents
- **Detailed claims data**: Only superbill documentation; full claims lifecycle likely outside i-heal's scope

These gaps are mostly attributable to i-heal's role as a specialty EMR operating within hospital facilities, where billing, payments, and administrative functions are handled by the hospital's own systems.

## 6. Documentation Quality

**What's well-documented:**
- The overall export architecture (XML format, ZIP delivery, folder structure) is clearly explained
- Parent-child document relationships are explicitly diagrammed
- Common structural elements (DocumentProperties, ElectronicSignatures, FileReferences) include XML examples
- All 69 document types are enumerated with clear categorization
- The export mechanism (roles, timing, single vs bulk) is clearly described
- The FHIR (g)(10) API is documented separately and clearly — no conflation with b(10)

**What's missing or inadequate:**
- **No field-level documentation**: The companion Data Dictionary is referenced but not publicly available. Without it, there are zero field definitions for any of the 69 document types. We know a WoundAssessmentDocument exists but not what fields it contains (wound dimensions? etiology codes? healing stage? measurement method?).
- **No sample data**: No example XML content for any individual document type (only the common DocumentProperties wrapper is shown)
- **No XSD or schema definition**: No machine-readable schema for the XML format
- **No value set definitions**: No coded field documentation
- **No field counts**: Impossible to determine total fields across all document types

**Could a developer build an import?** No — not from the available documentation alone. A developer could parse the ZIP structure and common elements, but would have to reverse-engineer the content of each document type from sample exports. The missing Data Dictionary is the critical blocker.

## 7. Overall Assessment

### Classification

**Partial native export** — The export is clearly a purpose-built, proprietary XML format covering the product's native data model across 69 document types. The scope is impressively broad, covering wound care specialty data, standard clinical data, billing documentation, and more. However, the missing companion Data Dictionary means the documentation is fundamentally incomplete — it describes the envelope but not the content. The architecture is right; the documentation isn't there yet.

### Key Findings

1. **Purpose-built (b)(10) export, not a FHIR/C-CDA repackage**: The export uses proprietary XML with 69 wound care-specific document types — clearly a genuine effort to export the product's native data model. The (g)(10) FHIR API exists separately and is not conflated with the (b)(10) export. (`EHIExport-iheal-2.pdf`)

2. **Exceptionally deep wound care specialty coverage**: 14+ wound procedure types, 5 HBO therapy types, 4 ostomy/stoma types, 6 risk assessment types, and outcome measures. This captures specialty clinical workflows that no standard (FHIR/C-CDA) would cover. (`EHIExport-iheal-2.pdf`, pages 4-6)

3. **Missing companion Data Dictionary is a critical gap**: The PDF explicitly references "EHIExport – Data Dictionary" for field-level definitions, but this document is not publicly available. Without it, there are zero field definitions for any document type. Probing dozens of URL variants on healogics.com all returned 404. (Verified 2026-02-16)

4. **Well-structured document hierarchy**: Parent-child relationships (e.g., WoundDocument → WoundAssessmentDocument, DebridementDocument, etc.) are explicitly documented, enabling reconstruction of the clinical record. (`EHIExport-iheal-2.pdf`, pages 7-8)

5. **Photo/file URLs expire after 90 days**: Wound photos and scanned documents are referenced via Azure Blob Storage URLs that become inaccessible 90 days after export, making the archive not fully self-contained for archival purposes. (`EHIExport-iheal-2.pdf`, page 9)

### Summary Stats

    Classification:  Partial native export
    Export format:   Proprietary XML (ZIP archive)
    Model type:      Native document model
    Entities:        69 document types
    Fields:          N/A (companion Data Dictionary not publicly available)
    Descriptions:    5 of 69 entities have brief descriptions; 0 field-level descriptions
    Sample data:     No
    Bulk export:     Yes (single patient or all patients at facility)
    Domains covered: 13 of 17 applicable domains (fully or partially)

### Bottom Line

Healogics/Net Health built a genuinely thoughtful (b)(10) export mechanism — 69 document types in proprietary XML covering the full breadth of wound care clinical data, with a clear document hierarchy and well-documented structural conventions. However, the publicly available documentation is only half the story: the companion Data Dictionary containing field-level definitions for all document types is not accessible. Without it, a recipient cannot meaningfully interpret or import the exported data. Making the Data Dictionary publicly available would elevate this from a partial to a potentially comprehensive native export.
