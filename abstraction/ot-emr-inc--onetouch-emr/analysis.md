# EHI Export Analysis: OT EMR, Inc.

**Product**: OneTouch EMR, Version 3
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.05.2821.OTEM.01.00.1.250224 (Listing #11599)

## 1. Product Context

OneTouch EMR is a cloud-based ambulatory EHR and practice management system built by OT EMR, Inc. (Dallas, TX), a small company founded in 2010 by Dr. Robert Abbate. The product targets small to mid-size primary care practices (internal medicine, family medicine) and is accessible via web browser, iPad, and Android tablets.

OneTouch EMR is a **single integrated platform** combining:

- **EHR/Clinical documentation**: Patient charting with customizable templates, touch/voice dictation input, vital signs, clinical assessments, drawing/annotation tools for clinical images, iPad photo capture
- **E-Prescribing**: Full eRx including EPCS (Electronic Prescribing for Controlled Substances), drug interaction checks
- **Lab integration**: Electronic lab orders and results with national labs
- **Practice management**: Appointment scheduling, patient demographics, reminders
- **Patient portal**: Secure messaging, telemedicine, online billing/payment, form completion, medical summaries
- **Medical billing & revenue cycle**: Integrated billing, unlimited eClaims submission, claim scrubbing, clearinghouse integration (ERAs), eligibility verification, denial management, POS payment processing, patient billing

The product is certified across a broad range of ONC criteria including (b)(10) EHI export. The billing and revenue cycle capabilities mean the product stores significant financial data beyond clinical records — claims, remittance, eligibility, denials, and payments.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf` (1.1 MB, 159 pages) | The sole artifact. A FHIR R4 API reference document produced via Google Docs (Skia/PDF m120 renderer). Contains documentation for 18 US Core FHIR resources (pp. 4–137), FHIR Bulk Data Access API (pp. 139–145), OAuth 2.0 security (pp. 148–152), a dedicated EHI Export section (pp. 153–157), and Terms and Conditions (pp. 158–159). | **Primary source.** The EHI export section (5 pages) is the only documentation of the (b)(10) export. The FHIR resource sections define what data is included. |

Only one artifact was collected. No additional data dictionaries, sample data files, database schemas, or supplementary documentation exist beyond this single PDF.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON files packaged in a ZIP archive. Each resource type gets its own `.ndjson` file (e.g., `AllergyIntolerance-289.ndjson`). A `README.txt` lists exported FHIR resource types with their US Core profile URLs.
- **Mechanism**: UI-based. Users with Office Manager, Practice Administrator, or System Administrator roles access **Administration → General → Single Patient Export** in the web UI. The user searches for a patient by name (with autocomplete), clicks "Export," and monitors the job status on the same page. The completed export is delivered as a ZIP attachment via the internal Messaging system (p. 155 screenshot shows a message with subject "FHIR Data Export Completed" and attachment `fhir_export_17_24_65361680a3eec.zip`).
- **Single-patient**: Yes, via the UI workflow described above.
- **Bulk/all-patient**: Available in the same format, but "due to the large volume of data that needs to be processed, this can only be requested through support by contacting OneTouch EMR" (p. 158). This is vendor-assisted, not self-service.
- **Access constraints**: Requires administrative role (Office Manager, Practice Administrator, or System Administrator). The API is free for paid-plan clients; free-tier clients must pay a monthly fee.
- **Notable**: The Administration panel screenshot (p. 154) shows a separate "Export Data" option that exports "Patient Summaries in CCDA Format," distinct from the "Single Patient Export" (EHI) option. The EHI export is explicitly based on FHIR, not C-CDA.

## 4. Export Content: What's In It

### What the export contains

The EHI export produces exactly 18 FHIR R4 resources conforming to US Core STU3 Release 3.1.1 profiles. The PDF states: *"OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data"* (p. 153). The README.txt screenshot (p. 157) confirms the export contains only these US Core resources and no vendor extensions.

The sample export ZIP shown in the PDF (p. 156) contains 19 files totaling 109.2 kB:
- `README.txt` (3.5 kB)
- 18 NDJSON files, one per resource type

### Field-level documentation

The PDF documents 171 supported attributes across the 18 resources, with 155 (90.6%) having descriptions. Attributes are documented in two-column tables (Name | Comments) — these are standard FHIR element names with brief descriptions, not a proprietary data dictionary. No data types, cardinality, or value set enumerations are documented beyond what the US Core profile names imply.

There are no foreign key/relationship diagrams. Relationships are expressed through standard FHIR references (e.g., `patient` references in clinical resources).

### Vendor's own content organization

The vendor does not organize the export into custom categories. The content is organized strictly by FHIR resource type, following the US Core Implementation Guide:

| FHIR Resource | Attributes | Described | Search Params | US Core Profiles |
|---|---|---|---|---|
| AllergyIntolerance | 8 | 7 | 2 | us-core-allergyintolerance |
| CarePlan | 6 | 6 | 3 | us-core-careplan |
| CareTeam | 14 | 11 | 3 | us-core-careteam |
| Condition | 13 | 11 | 2 | us-core-condition |
| Device | 17 | 15 | 2 | us-core-implantable-device |
| DiagnosticReport | 17 | 15 | 5 | us-core-diagnosticreport-note, us-core-diagnosticreport-lab |
| DocumentReference | 17 | 15 | 5 | us-core-documentreference |
| Encounter | 18 | 16 | 3 | us-core-encounter |
| Goal | 4 | 4 | 2 | us-core-goal |
| Immunization | 6 | 6 | 2 | us-core-immunization |
| Location | 7 | 5 | 1 | us-core-location |
| MedicationRequest | 9 | 9 | 5 | us-core-medicationrequest, us-core-medication |
| Observation | 8 | 8 | 4 | us-core-smokingstatus, us-core-observation-lab, pediatric-weight-for-height, pediatric-bmi-for-age, us-core-pulse-oximetry, head-occipital-frontal-circumference-percentile |
| Organization | 6 | 6 | 1 | us-core-organization |
| Patient | 11 | 11 | 3 | us-core-patient (+ race, ethnicity, birthsex extensions) |
| Practitioner | 3 | 3 | 2 | us-core-practitioner |
| Procedure | 4 | 4 | 3 | us-core-procedure |
| Provenance | 3 | 3 | 0 | us-core-provenance |
| **Total** | **171** | **155 (90.6%)** | **48** | |

The full entity inventory with all parsed attributes is available in `analysis/full-entity-inventory.json`.

**No vendor-specific extensions.** The README.txt in the export ZIP (p. 157) lists exclusively US Core profile URLs. The PDF documentation references only standard FHIR elements. There is no evidence of custom extensions, vendor-specific data fields, or proprietary data structures in the export.

**PresentedForm and attachments.** The documentation notes that "PresentedForm Data for DiagnosticReport and Content Attachment Data for DocumentReference resources are base64-encoded" — this means clinical documents and lab reports include inline binary content, not just metadata references.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor covers exactly the USCDI v1 data classes via US Core FHIR R4 resources. There is no vendor-specific layering, no custom categories, and no proprietary extensions. The content is:

- **Patient identity**: Patient resource with demographics, race, ethnicity, birthsex (11 attributes)
- **Clinical observations**: Observation resource covering vitals, smoking status, lab results, and pediatric growth profiles (8 attributes shared across 6 US Core profiles)
- **Conditions/diagnoses**: Condition resource with problem-list-item, encounter-diagnosis, and health-concern categories (13 attributes)
- **Medications**: MedicationRequest for prescriptions (9 attributes) — no MedicationDispense or MedicationAdministration
- **Allergies**: AllergyIntolerance with substance, reaction, and severity (8 attributes)
- **Encounters**: Encounter with type, period, participants, diagnoses, location, and discharge disposition (18 attributes — the richest resource)
- **Procedures**: Procedure with code, date, status (4 attributes — quite thin)
- **Care planning**: CarePlan (6 attrs), CareTeam (14 attrs), Goal (4 attrs)
- **Documents**: DocumentReference (17 attrs) and DiagnosticReport (17 attrs) — these may include base64-encoded clinical documents
- **Immunizations**: Immunization (6 attrs)
- **Devices**: Device (17 attrs) — implantable devices only
- **Reference entities**: Organization (6), Practitioner (3), Location (7), Provenance (3)

The export is strictly a **US Core / USCDI v1 clinical data projection**. It contains no billing, financial, scheduling, portal communication, or specialty data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (11 fields): name, DOB, gender, address, telecom, race, ethnicity, birthsex, marital status, language | Reasonable for US Core; missing insurance/coverage info stored elsewhere in the product |
| Encounters / visits | ✅ Covered | Encounter resource (18 fields): type, period, participants, discharge disposition | Covers visit records |
| Problems / conditions / diagnoses | ✅ Covered | Condition resource (13 fields): code, category, onset, clinical/verification status | Covers problem list and encounter diagnoses |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest (9 fields): medication, dosage, requester, status | Only prescription orders; no MedicationDispense (fill status), no EPCS workflow data, no MedicationAdministration. Product has full e-prescribing with EPCS — significant data missing |
| Allergies | ✅ Covered | AllergyIntolerance (8 fields): substance, reaction, severity, status | Adequate |
| Immunizations | ✅ Covered | Immunization (6 fields): vaccine code, date, status, patient | Adequate |
| Vitals | ✅ Covered | Observation (vital-signs category): via US Core profiles | Covered through Observation resource |
| Lab results | ✅ Covered | Observation (laboratory category) + DiagnosticReport (lab profile) | Lab results and reports included |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (note profile) + DocumentReference with base64 attachments | Reports likely included but clinical images from iPad photo capture and Free Draw annotations are unclear |
| Procedures | ✅ Covered | Procedure (4 fields): code, date, status, encounter | Thin but present |
| Clinical notes / documents | ✅ Covered | DocumentReference (17 fields) with base64-encoded content + DiagnosticReport (note exchange) | Documents included with inline content |
| Care plans / goals | ✅ Covered | CarePlan (6 fields), Goal (4 fields), CareTeam (14 fields) | Present via US Core |
| Orders / referrals | ❌ Not covered | No ServiceRequest, ReferralRequest, or equivalent | Product likely stores lab orders; not in export |
| Insurance / coverage | ❌ Not covered | No Coverage, InsurancePlan, or equivalent resources | Product stores insurance/eligibility data; significant gap |
| Claims / billing | ❌ Not covered | No Claim, ClaimResponse, ExplanationOfBenefit, or financial resources | **Major gap.** Product has integrated billing, eClaims, claim scrubbing, ERA processing, denial management. None exported. |
| Payments | ❌ Not covered | No payment-related resources | Product has integrated payment processing (POS, online); not exported |
| Consents / directives | ❌ Not covered | No Consent resource | Unknown if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No Communication resources | Product has patient portal with secure messaging and telemedicine; not exported |
| Specialty-specific data | N/A | Product targets primary care; no specialty modules identified | No specialty gap expected |

**Summary**: Of 16 applicable domains (excluding specialty), 9 are covered or partially covered and 7 are not covered. The most significant gaps are billing/claims (the product has a full billing and revenue cycle suite), insurance/coverage, patient portal communications, and payments.

## 6. Documentation Quality

**Strengths:**
- Well-organized 159-page PDF with clear table of contents and consistent formatting
- Every FHIR resource has a supported attributes table, HTTP operations, search parameters, and worked examples with full JSON request/response bodies
- The EHI Export section includes 6 screenshots showing the complete UI workflow from menu navigation through export completion and file delivery
- Sufficient for a developer to consume the FHIR API

**Weaknesses:**
- **No proprietary data dictionary.** The "data dictionary" is just FHIR element names with brief comments — it documents the standard, not the vendor's internal data model. A developer could reconstruct the same information from the US Core IG alone.
- **No data types documented.** The attribute tables provide Name and Comments columns but no Type, Cardinality, or Required/Optional indicators beyond what's implicit in the US Core profiles.
- **No value set enumerations.** Coded fields reference terminology systems (SNOMED CT, RXNORM) by name but don't enumerate the vendor's actually-used codes or value sets.
- **No sample export data.** The ZIP contents screenshot (p. 156) shows file names and sizes but the actual NDJSON content is not provided as sample data.
- **No schema or machine-readable definition.** No JSON Schema, FHIR CapabilityStatement export, or other machine-readable artifact beyond the PDF.
- **No relationship documentation.** No ER diagram or formal relationship mapping.

A developer could build a FHIR R4 client to consume this API based on the PDF, but would learn nothing about vendor-specific data structures or data that doesn't map to US Core. The documentation describes the standard, not the product.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The EHI export is explicitly and unambiguously a repackaging of the FHIR Bulk Data Access API ((g)(10)) as the (b)(10) EHI export. The vendor states this directly: *"OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data"* (p. 153). The export produces exactly the same 18 US Core resource types that the (g)(10) API serves. The README.txt in the export ZIP lists only US Core profile URLs. There are no vendor extensions, no additional data beyond USCDI v1, and no native data model exposure.

### Key Findings

1. **Textbook (g)(10)→(b)(10) conflation.** The EHI export is literally the FHIR Bulk Data export wrapped in a UI. The vendor built a nice admin panel (patient search, job monitoring, message delivery) but the underlying data scope is USCDI v1 / US Core — approximately 40-50% of the designated record set for a product with integrated billing.

2. **Billing and financial data completely absent.** OneTouch EMR has a full billing suite (eClaims, ERAs, eligibility verification, denial management, payment processing). None of this data — claims, remittance, coverage, payments — appears in the export. There are no FHIR financial resources (Claim, ClaimResponse, ExplanationOfBenefit, Coverage) and no proprietary billing tables.

3. **Patient portal communications not exported.** The product has secure patient-provider messaging and telemedicine. No Communication or equivalent resources are in the export.

4. **Single artifact, no native data model exposure.** The entire (b)(10) documentation is one PDF that is primarily a FHIR API reference guide. There is no proprietary data dictionary, no database schema, no indication of what data structures exist beyond what maps to US Core. The vendor's internal data model is completely opaque.

5. **Well-executed UI wrapper.** Despite the scope limitations, the export mechanism itself is well-designed: clear admin UI, async job processing, delivery via internal messaging, clear README in the ZIP. The documentation quality for what it covers (FHIR API) is above average.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 NDJSON (ZIP)
Model type:      Standard projection (US Core STU3.1.1)
Entities:        18 FHIR resource types
Fields:          171 attributes documented
Descriptions:    90.6% of fields have descriptions
Sample data:     No (screenshot of ZIP contents only)
Bulk export:     Yes (vendor-assisted; single-patient is self-service)
Domains covered: 9 of 16 applicable domains (with 2 partial)
```

### Bottom Line

OneTouch EMR's EHI export is a FHIR Bulk Data export rebranded as (b)(10). It covers standard clinical data (demographics, conditions, meds, labs, vitals, encounters, documents) but entirely omits the billing, claims, insurance, payment, and patient communication data that the product stores. For a product with an integrated billing and revenue cycle suite, the most significant gap is the complete absence of financial data from the export — a patient or provider would receive a clinical summary, not a complete copy of their electronic health information.
