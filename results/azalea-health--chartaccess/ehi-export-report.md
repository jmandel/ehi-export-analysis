# Azalea Health — EHI Export Documentation (ChartAccess)

Collected: 2026-02-16

## Source
- Registered URL: https://www.azaleahealth.com/resources/onc-certification/
- CHPL ID: 11140 (ChartAccess ® 7.0)
- Developer: Azalea Health

## Navigation Journal

1. **Initial probe** of registered URL:
   ```bash
   curl -sI -L "https://www.azaleahealth.com/resources/onc-certification/" -H 'User-Agent: Mozilla/5.0'
   ```
   HTTP/2 200, Content-Type: text/html (WordPress site on Cloudflare/Kinsta).

2. **Fetched and examined the ONC certification page.** Found downloadable PDFs for compliance certificates, cost disclosures, and MFA use cases — none specific to EHI export. Found a key link: `https://dev.azaleahealth.com/compliance/b10` — the (b)(10) EHI Export documentation on Azalea's developer portal.

3. **Fetched the b(10) compliance page:**
   ```bash
   curl -sL "https://dev.azaleahealth.com/compliance/b10" -H 'User-Agent: Mozilla/5.0'
   ```
   This is the main EHI Export overview. It links to two platform-specific export guides:
   - Ambulatory EHI Export Guide: `https://dev.azaleahealth.com/ambulatory/export` (for Azalea EHR, CHPL 11151 — not our target)
   - **Hospital EHI Export Guide: `https://dev.azaleahealth.com/hospital/export`** (for ChartAccess, CHPL 11140 — our target)

4. **Downloaded the Hospital EHI Export Guide:**
   ```bash
   curl -sL "https://dev.azaleahealth.com/hospital/export" -H 'User-Agent: Mozilla/5.0' -o hospital_export.html
   ```
   Contains a detailed table of 45 EHR concept → FHIR resource mappings.

5. **Downloaded supporting pages:**
   - Hospital Overview: `https://dev.azaleahealth.com/hospital/overview`
   - Hospital Resources: `https://dev.azaleahealth.com/hospital/resources` (lists all 36 supported FHIR resource types)
   - Bulk Data Export implementation guide: `https://dev.azaleahealth.com/implementation/bulk-data-export`
   - Bulk Data Access implementation guide: `https://dev.azaleahealth.com/implementation/bulk-data-access`

6. **Downloaded the Hospital CapabilityStatement (machine-readable):**
   ```bash
   curl -sL "https://hospital.azaleahealth.com/api/fhir/R4/CapabilityStatement/metadata" \
     -H 'Accept: application/fhir+json' -o capability-statement-hospital.json
   ```
   92KB JSON file listing 36 resource types, confirming Bulk Data export support.

7. **Took browser screenshots** of the b(10) overview page and the Hospital EHI Export Guide page.

## What Was Found

### Export Mechanism

Azalea Health uses **FHIR R4 Bulk Data Export** (NDJSON format) as its EHI export mechanism. The export is performed via the `Patient/$export` operation on the Hospital FHIR API (`hospital.azaleahealth.com`). The export covers:

- **All resources in the FHIR R4 Patient compartment** (as defined by HL7)
- **Additional administrative resources:** Location, Practitioner
- **Binary resources** for unstructured data (images, documents, notes) with base64-encoded content
- **DocumentReference** resources that may contain inline base64 data for clinical notes

### File Format

- **Format:** NDJSON (Newline Delimited JSON)
- **File naming:** `{resource}_{identifier}.ndjson` (e.g., `Patient_24r0sadf098230.ndjson`)
- **Structure:** Each file contains only one FHIR resource type; each line is one resource instance

### Data Mappings (Hospital EHI Export Guide)

The export guide maps 45 distinct EHR concepts to FHIR resources:

| EHR Concept | FHIR Resource |
|---|---|
| Admissions | Encounter |
| Allergies | AllergyIntolerance |
| Amendments | Communication |
| Appointments | Appointment |
| Cardiology Execution | Procedure |
| Cardiology Order | ServiceRequest |
| Care Level | Condition |
| Chart Notes (All) | DocumentReference |
| Diagnoses | Condition |
| Dietary | NutritionOrder |
| EMAR (medication admin) | MedicationAdministration |
| Files | DocumentReference |
| Financial Account | Account |
| Flowsheets | Observation |
| Immunizations | Immunization |
| Implantable Devices | Device |
| Laboratory Orders | ServiceRequest |
| Laboratory Reports | DiagnosticReport |
| Laboratory Results | Observation |
| Locations | Location |
| Medication History | MedicationStatement |
| Medication Orders | MedicationRequest |
| Nursing Orders | ServiceRequest |
| Patient Death Report | Observation |
| Patient Demographics | Patient |
| Patient Emergency Contact | Patient |
| Patient Lactating Status | Condition |
| Patient Memo | Flag |
| Patient Portal Messages | Communication |
| Patient Preferred Pharmacy | HealthcareService |
| Patient Pregnancy Status | Condition |
| Payments | PaymentReconciliation |
| Problem History | Condition |
| Procedure History | Procedure |
| Providers | Practitioner |
| Radiology Orders | ServiceRequest |
| Radiology Reports | DiagnosticReport |
| Radiology Results | Observation |
| Sexual Orientation | Observation |
| Smoking Status | Observation |
| Social History | Observation |
| Supplies | SupplyRequest |
| Therapy Execution | Procedure |
| Therapy Order | ServiceRequest |
| Vital Signs | Observation |

### Single Patient vs. Population Export

- **Single Patient (b)(10)(i):** Available via in-app UI or API using `_typeFilter=Patient?_id=1234`
- **Population Export (b)(10)(ii):** Users must contact Azalea support to initiate; alternatively available via Bulk Data API (`Patient/$export` or `Group/$export`). No charge.

### API Access (Bulk Data)

- Backend Services authorization via OAuth 2.0 `client_credentials` grant
- Supports both confidential clients (client_secret) and public clients (client assertion with JWK)
- Apps must be registered on the Developer Portal and pre-authorized per tenant
- Query parameters: `_outputFormat`, `_since`, `_type`, `_typeFilter`

## Export Coverage Assessment

### Data Domain Coverage

The export documentation is notably comprehensive for a hospital EHR. The 45 EHR concept mappings cover a wide range of clinical and some administrative/financial data:

**Well-covered domains:**
- **Clinical core:** Demographics, allergies, conditions/diagnoses, medications (orders, history, administration/EMAR), lab orders/results/reports, radiology orders/results/reports, vital signs, immunizations, procedures, implantable devices — all covered
- **Hospital-specific:** Admissions (Encounter), care levels, dietary orders (NutritionOrder), nursing orders, therapy orders/execution, cardiology orders/execution, flowsheets, supplies — all covered
- **Clinical notes:** Chart Notes (All) via DocumentReference — comprehensive
- **Documents/images:** Files via DocumentReference + Binary resources for unstructured data
- **Social determinants:** Sexual orientation, smoking status, social history — covered
- **Specialty status:** Pregnancy status, lactating status, patient death report — covered
- **Patient portal:** Portal messages via Communication — covered
- **Some financial data:** Financial Account (Account), Payments (PaymentReconciliation) — a meaningful attempt at billing coverage

**Domains with gaps or concerns:**
- **Billing claims/charges:** While "Financial Account" and "Payments" are mapped, there is no mention of claims (Claim resource), charge items (ChargeItem), or explanation of benefits (ExplanationOfBenefit). For a product with integrated billing/RCM as a core feature, the absence of detailed claims and charges data is a notable gap.
- **Insurance/coverage data:** Coverage and InsurancePlan are in the CapabilityStatement but NOT mapped in the export guide. Patient insurance information may not be exported.
- **Care plans and goals:** CarePlan and Goal are in the CapabilityStatement but not in the export mappings. These may not be part of the export.
- **Questionnaire responses:** QuestionnaireResponse is in the CS but not mapped — custom forms and assessments may be missed.
- **E-prescribing data:** MedicationDispense is in the CS but not mapped to an export concept.
- **Scheduling details:** Appointment is mapped but may be limited to basic scheduling data.
- **Analytics/quality data:** Not included, which is expected — these are operational, not patient-level EHI.

**Interesting discrepancy:** Four resources appear in the export mappings but NOT in the CapabilityStatement: Appointment, Account, Flag, PaymentReconciliation. This suggests the export may include data types beyond what the standard FHIR API exposes, which is a positive sign for (b)(10) completeness — but it also means these resources can't be independently verified via the API.

### Export Format & Standards

The export uses **FHIR R4 in NDJSON format via Bulk Data Export** — this is the same mechanism as (g)(10) but with broader scope. This is a well-chosen format:

- FHIR R4 is a recognized standard
- NDJSON is efficient for bulk transfer
- The Patient compartment approach ensures comprehensive coverage of patient-linked data
- Binary resources handle unstructured content (images, scanned documents)

However, this approach has limitations for truly complete EHI export:
- Not all data stored in a hospital EHR fits cleanly into standard FHIR R4 resources
- The mapping from proprietary EHR concepts to FHIR may lose some specificity (e.g., "Care Level" → Condition is semantically imprecise)
- Billing data beyond basic accounts/payments doesn't have natural FHIR R4 mappings in the standard spec

### Documentation Quality

**Strengths:**
- Clear EHR concept → FHIR resource mapping table with 45 entries
- FHIR path-level notes for disambiguating resources (e.g., `Condition.where(category.coding.code = "encounter-diagnosis")`)
- Machine-readable CapabilityStatement available
- Bulk Data API documentation with concrete request/response examples
- Both UI and API export methods documented

**Weaknesses:**
- No sample export files or worked examples
- No data dictionary with field-level definitions — the mapping table shows resource types but not which fields are populated
- No value set documentation for coded fields
- No schema or profile definitions specific to the Hospital platform (CapabilityStatement references US Core but no custom profiles)
- No documentation of data types, cardinality, or constraints beyond standard FHIR
- Typo in documentation: "attachemnt" instead of "attachment"

### Structure & Completeness

- **Granularity:** Resource-type level (which EHR concept maps to which FHIR resource), but NOT field level. We know that "Allergies" → AllergyIntolerance, but not which fields of AllergyIntolerance are populated.
- **Value sets:** Not documented beyond FHIR path expressions for category disambiguation
- **Relationships:** Implicit through FHIR resource references; not explicitly documented
- **Versioning:** CapabilityStatement shows version "debug" with date 2025-01-10; no formal versioning or change history

Overall, this is a **moderately well-documented EHI export** that goes beyond the bare minimum. The 45 EHR concept mappings show genuine thought about what data the hospital stores and how it maps to FHIR. The inclusion of financial data (Account, PaymentReconciliation) and hospital-specific concepts (EMAR, flowsheets, dietary orders, cardiology, therapy) demonstrates awareness of the (b)(10) requirement to export more than just US Core data. However, the lack of field-level documentation, sample data, and incomplete billing coverage prevent this from being a fully comprehensive export specification.

## Access Summary
- Final URL (after redirects): https://www.azaleahealth.com/resources/onc-certification/ (unchanged)
- b(10) documentation URL: https://dev.azaleahealth.com/compliance/b10
- Hospital EHI Export Guide: https://dev.azaleahealth.com/hospital/export
- Status: found
- Required browser: no (all content server-rendered HTML)
- Navigation complexity: one_click (link from ONC certification page to dev portal)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. All pages loaded without issues.
- The ONC certification page itself contains no direct EHI export documentation — it links to the developer portal.
- No PDFs, ZIPs, or downloadable data dictionaries were found — all documentation is web-based HTML.
- No login required for any of the documentation pages.
