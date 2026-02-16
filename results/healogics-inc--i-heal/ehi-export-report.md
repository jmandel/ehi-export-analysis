# Healogics, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.healogics.com/certified-ehr-technology/
- CHPL IDs: 10140
- Product: i-heal 2.0
- Developer: Healogics, Inc. (software built by Net Health)
- Certification date: 2019-10-07

## Navigation Journal

### Step 1: Probed the registered URL
```bash
curl -sI -L "https://www.healogics.com/certified-ehr-technology/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, `text/html; charset=UTF-8`, WordPress site served by nginx/PHP 8.3.

### Step 2: Downloaded and examined the page
```bash
curl -sL "https://www.healogics.com/certified-ehr-technology/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```
The page is a simple certification compliance hub (single WordPress page, no accordion or SPA). It contains three sections:
1. **API Documentation** — links to four integration API PDFs (Registration, Authentication, PatientSearch, DataRequest), plus FHIR g(10) documentation PDF, a FHIR base URL, and the (b)(10) EHI Export PDF.
2. **Mandatory Disclosure** — links to disclosure form and compliance certificate.
3. **Real World Test Plan** — links to RWT plans and results for 2022-2025.

### Step 3: Extracted all file links
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
```
Found 16 PDF links. The EHI export-specific link:
- `https://www.healogics.com/wp-content/uploads/2023/11/EHIExport-iheal-2.pdf` — linked with text "§170.315(b)(10) Electronic Health Information Export Documentation"

### Step 4: Downloaded EHI-relevant PDFs
```bash
curl -sL "https://www.healogics.com/wp-content/uploads/2023/11/EHIExport-iheal-2.pdf" -o EHIExport-iheal-2.pdf
curl -sL "https://www.healogics.com/wp-content/uploads/2023/01/Healogics-FHIR-g10-Documentation.pdf" -o Healogics-FHIR-g10-Documentation.pdf
curl -sL "https://www.healogics.com/wp-content/uploads/2019/10/RegistrationHelpv1.pdf" -o RegistrationHelpv1.pdf
curl -sL "https://www.healogics.com/wp-content/uploads/2019/10/AuthenticationHelpv1.pdf" -o AuthenticationHelpv1.pdf
curl -sL "https://www.healogics.com/wp-content/uploads/2019/10/PatientSearchHelpv1.pdf" -o PatientSearchHelpv1.pdf
curl -sL "https://www.healogics.com/wp-content/uploads/2019/10/DataRequestHelpv1.pdf" -o DataRequestHelpv1.pdf
```
All returned valid PDF documents (confirmed with `file` command).

### Step 5: Searched for companion Data Dictionary
The EHI Export PDF references a companion document: "EHIExport – Data Dictionary." This document is **not linked on the page** and could not be found:
- Probed dozens of URL variations on healogics.com/wp-content/uploads/ (multiple date directories and filename patterns) — all returned 404
- Searched nethealth.com (the software partner) — 404
- Web search for `"EHIExport" "Data Dictionary" site:healogics.com OR site:nethealth.com` — only found the main EHI Export PDF itself
- The data dictionary is referenced but not publicly accessible

### Step 6: Checked FHIR base URL endpoint
```bash
curl -sL "https://sfp-g10fhirproxy.azurewebsites.net/fhir/base-url" -H 'Accept: application/json'
```
Empty response — the endpoint appears to be a landing page for the FHIR server base URL, not a direct FHIR endpoint itself.

### Step 7: Took screenshot of the certification page
Navigated in browser and captured a full-page screenshot for reference.

## What Was Found

### Primary Document: EHI Export Documentation (EHIExport-iheal-2.pdf)

This 10-page PDF (dated November 16, 2023, authored by Amanda Quinones at Net Health) provides a solid description of the (b)(10) EHI export mechanism. Key findings:

**Export mechanism:** The EHI export is a feature built into i-heal 2.0, accessible to users with Facility Administration or Emergency Access roles. It supports export of a single patient or all patients at a facility. The export is generated asynchronously ("usually within 48 hours") and downloaded as a ZIP file from within i-heal.

**Export format:** The export uses a **proprietary XML format** — not FHIR, not C-CDA, not CSV. Each patient's data is organized into individual XML files named `<documentType>_<documentId>.xml`, grouped in folders by patient ID. The XML includes common structural elements for document properties, relationships, signatures, and file references.

**Document types (70+ forms):** The export covers an impressively broad range of wound care-specific data:

- **Patient information:** PatientDocument (demographics, care team, emergency contact, insurance)
- **Treatment courses / conditions:** HBOTreatmentCourseDocument, NonWoundConditionDocument, StomaDocument, WoundDocument
- **Encounter documentation (55+ types):** AllergyListDocument, AncillaryServiceDocument, BiopsyDocument, ChiefComplaintDocument, CompressionTherapyDocument, CustomForm1-10Documents, DebridementDocument, DermalMatrixSubstituteDocument, DischargeInfoDocument, FallRiskDocument, GeneralVisitNotesDocument, HBODocument, HBOPreTreatmentEvaluationDocument, HBOSafetyChecklistDocument, HPIDocument, HROSDocument, ImmunizationsDocument, IncisionAndDrainageDocument, LowerExtremityDocument, MultiDisciplinaryCarePlanDocument, NeuropathyDocument, NH_EducationAssessmentDocument, NPWTApplicationDocument/MaintenanceDocument, NutritionRiskDocument, OstomyPreOperativeDocument, PainAssessmentDocument, PhysicalExamDocument, PhysicianOrdersDocument, PrescriptionDocument, PressureUlcerRiskDocument, ProblemListDocument, ProgressNoteDocument, SkinPerfusionPressureDocument, SuperBillDocument, TCOMDocument, TopicalGrowthFactorDocument, TotalContactCastDocument, VitalSignsDocument, WoundAssessmentDocument, WoundTreatmentNotesDocument, and more
- **Non-encounter documentation:** CustomScanDocument, PatientCommunicationDocument, TestResultDocument

**Document relationships:** The PDF documents a well-structured parent-child relationship model using PatientID, VisitID, and ParentDocumentID, allowing reconstruction of: patient → encounter → condition/treatment course → clinical observations and procedures.

**Photos and files:** Wound photos and scanned documents are exported via time-limited Azure Blob Storage URLs (valid 90 days from export), referenced within the XML via `<FileReferences>` elements.

**Critical gap — companion Data Dictionary not available:** The PDF explicitly states: "A companion document, EHIExport – Data Dictionary, provides a data dictionary and identifies the elements within each document." This document is not linked on the certification page and could not be found publicly. Without it, there is no field-level documentation for any of the 70+ document types. The main PDF describes only the common structural elements (DocumentProperties, relationships, signatures, file references) — not the specific clinical content fields within each document type.

### Secondary: FHIR g(10) Documentation (40 pages)

The FHIR API documentation covers the standard US Core / USCDI data classes (g(10) compliance): AllergyIntolerance, CarePlan, CareTeam, DocumentReference, Encounter, Goal, Condition, Immunization, Laboratory results, Medication/MedicationRequest, Patient demographics, Procedure, Provenance, Observation, ImplantableDevice, Location, Organization, Practitioner, VitalSigns. It also supports querying all patient data as a C-CDA document.

This is clearly a **separate system from the b(10) export** — the g(10) uses standard FHIR R4 with US Core profiles, while the b(10) uses proprietary XML. The two are not conflated, which is a positive sign.

### Secondary: Integration API Documentation (4 PDFs, 2019-era)

These older PDFs document a pre-FHIR integration API for i-heal:
- **RegistrationHelpv1.pdf** (51 pages) — vendor registration process for API access
- **AuthenticationHelpv1.pdf** (28 pages) — user auth, password management, facility authorization
- **PatientSearchHelpv1.pdf** (22 pages) — patient search and demographics access
- **DataRequestHelpv1.pdf** (8 pages) — C-CDA retrieval API (Common Clinical Data Set per visit)

The DataRequest API provides C-CDA exports filtered by date range and selectable data parts (allergies, encounters, immunizations, medications, problems, procedures, vitals, etc.). This is a predecessor/complement to the g(10) FHIR API and covers the same clinical summary scope — it is not a substitute for the broader b(10) export.

## Export Coverage Assessment

### Data Domain Coverage

The b(10) export documentation describes an export that appears to cover the **full breadth of data stored in i-heal**, not just USCDI. This is one of the better (b)(10) implementations in terms of scope.

**Clearly covered (based on document type names):**
- Patient demographics (PatientDocument)
- Wound assessments and wound data (WoundDocument, WoundAssessmentDocument, WoundTreatmentNotesDocument)
- Wound photographs (via FileReferences in WoundAssessmentDocument and others)
- HBO (hyperbaric oxygen) therapy data (HBODocument, HBOTreatmentCourseDocument, HBOPreTreatmentEvaluationDocument, HBOSafetyChecklistDocument, HBOScreeningChecklistDocument)
- Non-wound conditions and treatment (NonWoundConditionDocument, NonWoundConditionAssessmentDocument, NonWoundTreatmentNotesDocument)
- Ostomy/stoma care (StomaDocument, StomaAssessmentDocument, StomaTreatmentNotesDocument, OstomyPreOperativeDocument)
- Vital signs (VitalSignsDocument)
- Allergies (AllergyListDocument)
- Problem list (ProblemListDocument)
- Immunizations (ImmunizationsDocument)
- Prescriptions (PrescriptionDocument)
- Physician orders (PhysicianOrdersDocument)
- Lab/test results (TestResultDocument)
- Progress notes (ProgressNoteDocument)
- Physical exam (PhysicalExamDocument)
- History of present illness (HPIDocument)
- Chief complaint (ChiefComplaintDocument)
- Discharge information and instructions (DischargeInfoDocument, DischargeInstructionsDocument)
- Care plans (MultiDisciplinaryCarePlanDocument)
- Patient education (NH_EducationAssessmentDocument, NH_PatientCaregiverEducationDocument)
- Fall risk and pressure ulcer risk assessments (FallRiskDocument, PressureUlcerRiskDocument)
- Nutrition risk assessment (NutritionRiskDocument)
- Pain assessment (PainAssessmentDocument)
- Neuropathy assessment (NeuropathyDocument)
- Lower extremity assessment (LowerExtremityDocument)
- Skin perfusion pressure (SkinPerfusionPressureDocument)
- Biopsy records (BiopsyDocument)
- Debridement records (DebridementDocument)
- Compression therapy (CompressionTherapyDocument)
- Negative pressure wound therapy (NPWTApplicationDocument, NPWTMaintenanceDocument)
- Dermal matrix/skin substitute (DermalMatrixSubstituteDocument)
- Topical growth factor (TopicalGrowthFactorDocument)
- Total contact cast (TotalContactCastDocument)
- Incision and drainage (IncisionAndDrainageDocument)
- Other procedures (OtherProcedureDocument)
- Custom forms (CustomForm1-10Documents — up to 10 facility-customizable forms)
- Scanned documents (CustomScanDocument)
- Patient communications (PatientCommunicationDocument)
- Billing/superbill (SuperBillDocument)
- Electronic signatures on all signable documents
- Insurance information (within PatientDocument)
- Clinic level of care (ClinicLevelOfCareDocument)
- TCOM (TCOMDocument — likely a standardized wound healing outcome measure)
- Ancillary services (AncillaryServiceDocument)
- HROS (HROSDocument — likely a healing rate/outcome score)

**Potentially missing or unclear:**
- **Detailed billing/claims data beyond the superbill:** The SuperBillDocument is included, but it's unclear whether detailed charge records, payment postings, and claims adjudication data are exported. Given that i-heal operates within hospital systems (billing likely handled by the host hospital's system), this may not be stored in i-heal at all.
- **Scheduling/appointment data:** No document type for appointment scheduling. This is classified as operational data and is not an EHI gap.
- **Patient portal messages and patient-generated health data:** PatientCommunicationDocument may cover this, but unclear if patient-submitted data from the portal is included.
- **Referral data:** No explicit referral document type, though this information may be embedded in discharge or care plan documents.

### Export Format & Standards

The export uses a **proprietary XML format** with a well-defined structural convention. This is an appropriate and honest approach for a (b)(10) export:

- It is **not FHIR** — it does not pretend that wound care specialty data fits neatly into US Core profiles. This is correct; much of i-heal's wound-specific data (HBO treatments, wound measurements, compression therapy, debridement details, etc.) has no standard FHIR representation.
- The XML files are **machine-readable** and parseable, with consistent naming and relationship conventions.
- **File references** (for photos/scanned documents) use time-limited Azure Blob Storage URLs, which means exported archives are not fully self-contained — photo access expires after 90 days.
- Relationships between documents are expressed through common IDs (PatientID, VisitID, ParentDocumentID), which would allow a third party to reconstruct the clinical record hierarchy.

However, without the companion Data Dictionary, it is impossible to know the exact XML schema for each document type — what fields are present, what their data types are, and what values they can take.

### Documentation Quality

**Strengths:**
- The EHI Export documentation is clearly written and focused on the (b)(10) requirement specifically — it is not a repackaged FHIR API doc.
- The structural conventions (document properties, relationships, signatures, file references) are well-documented with XML examples.
- The parent-child relationship hierarchy is clearly diagrammed.
- The document types are enumerated with brief descriptions indicating their clinical purpose.
- The distinction between encounter documentation and non-encounter documentation is clear.
- The FHIR g(10) API is documented separately and clearly, avoiding the common (b)(10)/(g)(10) conflation.

**Weaknesses:**
- The **companion Data Dictionary is missing** — it is referenced as providing "a data dictionary and identifies the elements within each document" but is not publicly available. This is a critical gap. Without it, a third party cannot implement an import of this data.
- There are **no field-level definitions** for any of the 70+ document types in the available documentation. We know a WoundAssessmentDocument exists but not what fields it contains (wound dimensions? etiology codes? healing status? measurement method?).
- There are **no sample export files** or example XML content for individual document types (only the DocumentProperties wrapper is shown).
- There is **no XSD or schema definition** for the XML format.
- There are **no value set definitions** for coded fields.
- The 90-day expiration on photo/file URLs is a significant limitation for long-term archival, and this is disclosed but not mitigated.

### Structure & Completeness

- **Entity-level:** Excellent — 70+ document types covering the full breadth of wound care clinical data, billing, and specialty-specific assessments.
- **Field-level:** Unknown — entirely dependent on the missing companion Data Dictionary.
- **Relationship documentation:** Good — parent-child relationships are clearly mapped.
- **Value sets:** Unknown — no coded field documentation available.
- **Versioning:** None evident. The PDF is dated November 2023 with no version history.

## Assessment Summary

Healogics/Net Health has done **genuinely thoughtful work on b(10) compliance**. The export is clearly a real, purpose-built mechanism — not a repackaged FHIR API or C-CDA export. It covers 70+ wound care-specific document types in a proprietary XML format, which is the right approach for specialty clinical data that doesn't map to standard FHIR resources.

However, the **companion Data Dictionary is the missing critical piece**. The available documentation describes the envelope (how files are structured, named, and related) but not the content (what clinical fields are in each document type). Without field-level definitions, a third party cannot meaningfully use or import the exported data.

**Grade: B-** — Strong architectural approach and impressive scope of document types, significantly undermined by the missing field-level documentation that would make the export actually usable by a recipient.

## Access Summary
- Final URL (after redirects): https://www.healogics.com/certified-ehr-technology/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (all files linked from a single flat page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The companion "EHIExport – Data Dictionary" document referenced in the main PDF is not linked on the certification page and could not be found via URL probing, web search, or Wayback Machine. This is the most significant gap.
- The FHIR base URL endpoint (sfp-g10fhirproxy.azurewebsites.net/fhir/base-url) returned an empty response — appears to be informational, not a functional FHIR server endpoint.
- No other pages on healogics.com appeared to contain additional EHI export documentation.
