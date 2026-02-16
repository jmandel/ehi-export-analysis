# Azalea Health — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.azaleahealth.com/resources/onc-certification/
- CHPL IDs: 11151 (15.04.04.2688.Azal.04.02.1.221227)
- Certification date: 2022-12-27

## Navigation Journal

1. **Initial probe** of registered URL:
   ```bash
   curl -sI -L "https://www.azaleahealth.com/resources/onc-certification/" -H 'User-Agent: Mozilla/5.0'
   ```
   HTTP 200, text/html, WordPress site on Cloudflare/Kinsta hosting.

2. **Fetched and examined the page** — a compliance/certification hub page. Searched for EHI-related links:
   ```bash
   curl -sL "https://www.azaleahealth.com/resources/onc-certification/" -H 'User-Agent: Mozilla/5.0' -o /tmp/azalea-page.html
   ```
   Found two mentions of "EHI Export Documentation" in the page text, both pointing to: `https://dev.azaleahealth.com/compliance/b10`

3. **Fetched the b(10) compliance page** at `https://dev.azaleahealth.com/compliance/b10`:
   ```bash
   curl -sL "https://dev.azaleahealth.com/compliance/b10" -H 'User-Agent: Mozilla/5.0' -o b10-main.html
   ```
   This is the main EHI export overview. It describes the export format (NDJSON), file naming convention, and links to platform-specific export guides.

4. **Downloaded platform-specific export guides**:
   - Ambulatory EHI Export Guide: `https://dev.azaleahealth.com/ambulatory/export`
   - Hospital EHI Export Guide: `https://dev.azaleahealth.com/hospital/export`

5. **Downloaded supporting documentation** from the developer portal:
   - Ambulatory resources, profiles, extensions, overview pages
   - Hospital resources, overview pages
   - Bulk Data Export implementation guide
   - US Core Mappings page

6. **Downloaded FHIR CapabilityStatements** (machine-readable):
   ```bash
   curl -sL "https://app.azaleahealth.com/fhir/R4/CapabilityStatement/metadata" -H 'Accept: application/fhir+json' -o ambulatory-capability-statement.json
   curl -sL "https://hospital.azaleahealth.com/api/fhir/R4/CapabilityStatement/metadata" -H 'Accept: application/fhir+json' -o hospital-capability-statement.json
   ```

## What Was Found

Azalea Health provides dedicated (b)(10) EHI export documentation on their developer portal at `dev.azaleahealth.com`. The documentation is well-structured and explicitly addresses the (b)(10) requirement separately from (g)(10).

### Export Format

The export uses **NDJSON (Newline Delimited JSON)** formatted as FHIR R4 resources. Files are named `{ResourceType}_{identifier}.ndjson` (e.g., `Patient_24r0sadf098230.ndjson`). Each file contains resources of a single FHIR resource type, one per line.

### Export Scope

The export includes:
- All data from the **FHIR R4 Patient Compartment**
- Supporting administrative resources: **Location** and **Practitioner**
- **Binary resources** for unstructured data (images, documents, medical notes) — encoded as base64 in `Binary.data`
- **DocumentReference** resources that may contain embedded clinical notes as base64 in `DocumentReference.content.attachment.data`

### Two Platforms, Two Export Guides

Azalea has two separate EHR platforms with separate export guides:

**Ambulatory Platform** (CHPL 11151 — the one we're evaluating):
57 EHR concept → FHIR resource mappings, including:
- Clinical: Allergies, Care Plans, Goals, Care Teams, Conditions (encounter diagnoses, health concerns, problems), Encounters, Family History, Immunizations, Implantable Devices, Lab Orders/Reports/Results, Medications, Prescriptions, Procedures, Radiology, Vital Signs, Smoking Status, Social History, Sexual Orientation
- Documents: Chart notes (Plan, Procedure, Subjective/PMH), Documents, Patient Handouts, Patient URLs
- Questionnaires: Chart Evaluation Tables (QuestionnaireResponse), Social Questions
- Financial/Billing: Encounter Billing (Claim), Encounter Financial Account (Account), Patient Financial Account, Patient Statements (Invoice), Payments (PaymentReconciliation), Pre-Certifications (Claim with use=preauthorization), Insurance (Coverage)
- Patient context: Demographics, Emergency Contact, Employer, Employment Status, Guarantor, Next of Kin, Power of Attorney, Portal Messages, Comments, Popup Comments, Travel History, Patient Classes (Group), Recalls
- Administrative: Locations, Providers

**Hospital Platform** (CHPL 11140 — different product, documented for reference):
45 EHR concept → FHIR resource mappings, including additional hospital-specific concepts like Admissions, EMAR (MedicationAdministration), Dietary (NutritionOrder), Nursing Orders, Cardiology Orders/Execution, Therapy Orders/Execution, Supplies, Care Level, Flowsheets, Patient Death Report, Lactating Status, Pregnancy Status, Amendments, Patient Memo, Preferred Pharmacy.

### Export Mechanisms

1. **Single Patient Export (b)(10)(i)**: In-app UI for requesting single patient export, runs in background. Also available via Bulk Data Export API with `_typeFilter=Patient?_id=1234`.
2. **Patient Population Export (b)(10)(ii)**: Users contact support to initiate. Also available via Bulk Data Export API (All Patient or Group of Patients endpoints). No charge for this export type.

### API Details

The Bulk Data Export API follows the FHIR Bulk Data Access specification:
- Kick-off: `GET [base]/Patient/$export` with `Accept: application/fhir+json` and `Prefer: respond-async`
- Returns 202 Accepted with Content-Location for polling
- Status polling returns 200 OK with manifest of NDJSON file URLs
- Supports delete for cancellation

### CapabilityStatements

The ambulatory CapabilityStatement declares 50 FHIR resource types with full interaction/operation/search parameter details. The hospital CapabilityStatement declares 36 resource types.

## Export Coverage Assessment

### Data Domain Coverage

**Well-covered domains** (based on product research comparison):

| Product Domain | Export Coverage |
|---|---|
| Demographics | ✅ Patient resource with contacts (emergency, employer, NOK, POA, guarantor) |
| Problem lists | ✅ Condition (patient-problem-list, encounter-diagnosis, health-concern categories) |
| Medications | ✅ MedicationStatement + MedicationRequest (prescriptions) |
| Allergies | ✅ AllergyIntolerance |
| Lab results | ✅ Observation + DiagnosticReport + ServiceRequest |
| Vital signs | ✅ Observation (vital-signs category) |
| Immunizations | ✅ Immunization |
| Procedures | ✅ Procedure |
| Clinical notes | ✅ DocumentReference (Plan, Procedure, Subjective/PMH, all documents) |
| Care plans | ✅ CarePlan + Goal |
| Care teams | ✅ CareTeam |
| Family history | ✅ FamilyMemberHistory |
| Implantable devices | ✅ Device |
| Social history | ✅ Observation (social-history, smoking status, sexual orientation, employment, travel) |
| Radiology | ✅ ServiceRequest + DiagnosticReport + Observation |
| Insurance | ✅ Coverage |
| Billing/claims | ✅ Claim (with use=claim), Account (financial-account, charge-group) |
| Payments | ✅ PaymentReconciliation (applied + unapplied) |
| Patient statements | ✅ Invoice |
| Pre-certifications | ✅ Claim (use=preauthorization) |
| Patient portal messages | ✅ Communication |
| Documents/images | ✅ Binary (base64 encoded) + DocumentReference |
| Questionnaires | ✅ QuestionnaireResponse (chart evaluation tables, social questions) |
| Appointments | ✅ Appointment |
| Recalls | ✅ CarePlan (category=recall) |

**Potentially missing or unclear domains:**

- **E-prescribing details (EPCS)**: MedicationRequest covers prescriptions, but controlled substance–specific metadata (DEA schedule, EPCS workflow status) may not be fully captured.
- **Telehealth sessions**: No explicit mapping for telehealth visit records. These may be captured within Encounter resources, but the documentation doesn't specifically address telehealth data.
- **AI Clinical Assistant (Suki) notes**: No mention of AI-generated notes as a distinct data type. These may be included in DocumentReference, but it's unspecified.
- **Analytics/reporting data**: Not included — but this is operational/aggregate data, not EHI, so this is correctly scoped.
- **Audit logs**: AuditEvent is in the CapabilityStatement but not in the export mapping table. This is correctly excluded from EHI export.

### Export Format & Standards

The export format is **FHIR R4 NDJSON** — a recognized standard. This is a genuine (b)(10) implementation that goes well beyond the (g)(10) USCDI minimum:

- The export includes **57 distinct EHR concepts** mapped to FHIR resources (ambulatory), far exceeding the ~20 USCDI data classes.
- It includes **billing data** (Claim, Account, Invoice, PaymentReconciliation, Coverage) — a clear indicator this is real (b)(10) work, not just repackaged (g)(10).
- It includes **non-US Core resources** like Account, Invoice, Claim, PaymentReconciliation, Flag, Communication, Group — resources that don't appear in the US Core profile set.
- The Patient Compartment approach ensures broad coverage rather than cherry-picking specific resource types.

The choice of FHIR R4 for EHI export is well-suited to this product. Azalea has extended beyond standard FHIR patterns with custom category codes and resource usage patterns to capture EHR-specific concepts (e.g., `Flag` for patient comments/popups, `Group` for patient classes, `CarePlan` for recalls).

### Documentation Quality

**Strengths:**
- Clear separation of (b)(10) from (g)(10) documentation
- Explicit EHR concept → FHIR resource mapping tables with filter notes
- Machine-readable CapabilityStatements with full interaction, operation, and search parameter details
- Separate documentation for ambulatory vs. hospital platforms
- Bulk Data Export API implementation guide with request/response examples

**Weaknesses:**
- No field-level data dictionary beyond what the FHIR resource definitions provide
- No sample export files or example NDJSON records
- No documentation of custom extensions used in export (the extensions page exists but isn't export-specific)
- No explicit list of coded value sets for vendor-specific codes (e.g., what are all possible `Flag.category.text` values?)
- The profiles page documents FHIR profiles but doesn't tie them explicitly to the export
- Population export requires contacting support — no self-service for this

### Structure & Completeness

The documentation is structured at the **EHR concept level**, mapping each internal data concept to its FHIR resource representation. This is more informative than a raw resource list but less detailed than a field-level data dictionary.

- **Resource-type granularity**: Good — 57 concepts mapped to ~25 distinct FHIR resource types
- **Filter/query notes**: Provided where needed (e.g., which Condition category distinguishes encounter-diagnoses from health-concerns)
- **Field-level documentation**: Not provided — you'd need to infer field semantics from FHIR R4 base definitions plus the profiles/extensions pages
- **Value sets**: Not documented for vendor-specific coded values
- **Relationships**: Implicit via FHIR references; not separately documented
- **Versioning**: CapabilityStatement version is "43608" (ambulatory), suggesting it's auto-versioned

Overall, Azalea Health has done **genuine (b)(10) work** — not just repackaged (g)(10). The export covers clinical, financial, demographic, and administrative data. The documentation is above average for the industry, with clear concept-to-resource mappings and machine-readable CapabilityStatements. The main gaps are the lack of field-level data dictionaries, sample files, and value set documentation.

## Access Summary
- Final URL (after redirects): https://dev.azaleahealth.com/compliance/b10
- Status: found
- Required browser: no
- Navigation complexity: one_click (link from ONC certification page to dev portal)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The documentation was straightforward to find and access.
- The registered URL (azaleahealth.com/resources/onc-certification/) contains a direct link to the b(10) documentation page.
- All documentation is publicly accessible without authentication.
- CapabilityStatements are served from live FHIR endpoints without requiring auth tokens.
