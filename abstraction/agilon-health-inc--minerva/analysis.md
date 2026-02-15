# EHI Export Analysis: agilon health inc.

**Product**: Minerva V4
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.3082.Mine.04.01.0.210609 (CHPL #10649)

## 1. Product Context

Minerva is a **FHIR-native healthcare data aggregation and patient engagement platform**, originally built by MphRx (My Personal Health Records Express Inc.) and acquired by agilon health in March 2023 for $45 million. It is **not a traditional EHR** — it is an interoperability platform that ingests and unifies clinical data from disparate EHRs, HIS, and PACS systems into a consolidated FHIR-based patient record.

The product has two primary functional areas per its ONC mandatory disclosures:

1. **Interoperability Platform**: Integrates and aggregates data from disparate healthcare IT systems to create a unified FHIR-based patient record. Provides SMART on FHIR APIs for third-party application integration.
2. **Patient Engagement**: Web and mobile applications for patients and family members to access their data, book appointments, securely message their health systems, and share information. Also provides clinical and administrative access for care coordination.

**Data the product stores** (relevant for completeness assessment):
- **Aggregated clinical data** from connected EHRs (demographics, problems, medications, allergies, labs, notes, etc.)
- **Aggregated claims data** ("brings together clinical and claims data" per vendor materials)
- **Natively generated data**: patient-reported outcomes, appointment/scheduling data (16M+ appointments booked historically), secure patient-provider messages, care coordination tasks/documents/alerts, patient engagement activity, and user accounts (52M+ patient accounts, 350K+ clinical users)

The certified criteria are limited: (b)(10) for EHI export, (e)(1)/(e)(3) for patient access, (g)(1)/(g)(7)/(g)(9)/(g)(10) for FHIR APIs, and various (d) criteria. No clinical criteria (a)(1)–(a)(14) are certified, consistent with Minerva being a data aggregation platform rather than a primary clinical documentation system.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Mphrx-EHI-export-documentation.pdf` (12 pages, 624 KB) | Primary EHI export documentation. Describes single-patient UI export and bulk FHIR API export. Contains screenshots of the export workflow and ZIP file contents. Created June 4, 2021 with Microsoft Word. | **Primary source** — the only artifact describing the (b)(10) export |
| `Mandatory-Disclosures-Letter_MphRx.pdf` (5 pages, 615 KB) | ONC mandatory disclosure letter from MphRx dated May 24, 2021. Describes two capabilities (Interoperability Platform, Patient Engagement) with cost/fee info and multi-factor authentication approach. | Contextual — confirms product scope |
| ONC Health IT Disclosures webpage (`agilonhealth.com/onc-health-it-disclosures/`) | Web page with certification details, cost information, and links to mandatory disclosures. | Contextual — confirms certification status |
| `product-research.md` | Prior agent research on agilon health and Minerva. Describes company, product capabilities, modules, and data types. | Orientation — claims verified against artifacts |

**No additional artifacts were found**: no data dictionary, no schema files, no sample data files, no field-level documentation. The `downloads/` directory was empty at the start of analysis; the PDF was downloaded directly from the CHPL-listed URL.

## 3. Export Mechanics

- **Format**: NDJSON (Newline Delimited JSON) — one file per FHIR resource type
- **Standard**: FHIR R4 Bulk Data Export (`$export` operation)
- **Single-patient export**: Via Minerva portal UI. Admin/Clinical Admin navigates to Patient List → selects patient → Action → Export EHI. A notification with a download link appears; the download is a ZIP file containing NDJSON files plus a readme.txt.
- **Bulk export (all patients)**: Via FHIR Bulk Data API at `<base-url>/minerva/fhir-export/r4/bulkExport/Patient/$export`. Requires SMART Backend Services Authorization (RS384/ES384). Users must contact MphRx (techsvc@mphrx.com) to obtain a Client ID.
- **File splitting**: A new NDJSON file is created per resource type after 10,000 records (e.g., `patient_file_1.ndjson`, `patient_file_2.ndjson`).
- **Download expiry**: URLs expire 48 hours after generation; files are auto-deleted.
- **Access constraints**: Clinical Admin or Admin role required for UI export. Bulk API requires pre-registration with MphRx team.
- **Fees**: No explicit export fee mentioned; platform usage is subscription-based per active patient record.
- **Query parameters**: `_outputFormat`, `_since` (incremental export by modification date), `_type` (filter by resource type).

## 4. Export Content: What's In It

The export is a **standard FHIR Bulk Data Export** producing NDJSON files containing FHIR R4 resources. There is **no vendor-specific data dictionary**, **no field-level documentation**, **no sample data content**, and **no vendor extensions documented**. The only documentation of what's exported is the list of supported FHIR resource types and a screenshot of a ZIP file.

### Supported FHIR Resource Types

The PDF documentation lists **20 supported resource types** for the bulk API (PDF page 8):

AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance

### ZIP File Contents (Single-Patient Export Screenshot)

The screenshot on PDF page 6 shows the ZIP file for a single-patient export containing **14 NDJSON files** plus a readme.txt:

| File | FHIR Resource |
|---|---|
| `allergyintolerance_file_1.ndjson` | AllergyIntolerance |
| `careteam_file_1.ndjson` | CareTeam |
| `clinicalimpression_file_1.ndjson` | ClinicalImpression |
| `diagnosticreport_file_1.ndjson` | DiagnosticReport |
| `documentreference_file_1.ndjson` | DocumentReference |
| `encounter_file_1.ndjson` | Encounter |
| `location_file_1.ndjson` | Location |
| `medication_file_1.ndjson` | Medication |
| `medicationrequest_file_1.ndjson` | MedicationRequest |
| `observation_file_1.ndjson` | Observation |
| `patient_file_1.ndjson` | Patient |
| `practitioner_file_1.ndjson` | Practitioner |
| `procedure_file_1.ndjson` | Procedure |
| `provenance_file_1.ndjson` | Provenance |
| `readme.txt` | Format documentation link |

### Discrepancies Between API List and ZIP Screenshot

**7 resources in the API list but absent from the ZIP screenshot**: CarePlan, Condition, Device, Goal, Immunization, Organization, PractitionerRole. These may simply not have data for the sample patient.

**1 resource in the ZIP but NOT in the API supported list**: **ClinicalImpression** — this resource appears in the single-patient export screenshot but is not listed among the 20 supported resources for the bulk API. This is a minor inconsistency in the documentation.

### Documentation Depth

The export documentation provides **zero field-level detail**. There is:
- No data dictionary
- No field names, types, or descriptions
- No relationship documentation
- No value set or code system specifications
- No sample NDJSON content (only file names are shown)
- No vendor-specific extension documentation

The readme.txt included in the ZIP simply links to the HL7 FHIR NDJSON specification page for format details. The consumer is expected to understand standard FHIR R4 resource schemas.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers **standard FHIR clinical resources** — effectively the US Core / USCDI resource set. The 20 supported resources map cleanly to core clinical data domains: demographics (Patient), encounters, conditions, medications, allergies, immunizations, vitals/labs (Observation), procedures, diagnostic reports, clinical documents (DocumentReference), care plans, goals, and care teams.

This is a **FHIR Bulk Data Export** that reflects exactly what the FHIR API already exposes. The vendor has not organized the export into custom categories — it uses FHIR resource types as the sole organizational structure.

The export is notably thin for a product that aggregates data from multiple sources and generates its own patient engagement, messaging, and care coordination data. The 20 FHIR resources cover the clinical summary data that would typically flow through FHIR APIs, but miss the platform's natively generated data entirely.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` resource | Standard FHIR Patient resource |
| Encounters / visits | ✅ Covered | `Encounter` resource | Standard FHIR Encounter |
| Problems / conditions / diagnoses | ✅ Covered | `Condition`, `ClinicalImpression` resources | Standard FHIR resources |
| Medications / prescriptions | ✅ Covered | `Medication`, `MedicationRequest` resources | No MedicationAdministration |
| Allergies | ✅ Covered | `AllergyIntolerance` resource | Standard FHIR resource |
| Immunizations | ✅ Covered | `Immunization` resource | Standard FHIR resource |
| Vitals | ✅ Covered | `Observation` resource (includes vitals) | Standard FHIR Observation |
| Lab results | ✅ Covered | `Observation`, `DiagnosticReport` resources | Standard FHIR resources |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport`, `DocumentReference` (no actual images) | Product integrates with PACS; no ImagingStudy resource |
| Procedures | ✅ Covered | `Procedure` resource | Standard FHIR Procedure |
| Clinical notes / documents | ✅ Covered | `DocumentReference` resource | Standard; unclear if document content (attachments) is included or just references |
| Care plans / goals | ✅ Covered | `CarePlan`, `Goal`, `CareTeam` resources | Standard FHIR resources |
| Orders / referrals | ❌ Not covered | No ServiceRequest or ReferralRequest resource | Product may handle referrals via care coordination; gap if data exists |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resource | Product aggregates claims data which implies insurance information; **significant gap** |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing resources | Product explicitly "brings together clinical and claims data"; **significant gap** — claims data the platform stores is not exported |
| Payments | ❌ Not covered | No payment-related resources | N/A if platform doesn't process payments directly |
| Consents / directives | ❌ Not covered | No Consent resource | Gap if patient consents are managed in the platform |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has secure messaging as a core feature (patient engagement module); **significant gap** — messages are natively generated EHI |
| Specialty-specific (care coordination) | ❌ Not covered | No custom resources for surgical coordination, care pathways, task management | Product has surgery coordination, care pathway management, and task allocation as core features; **significant gap** |

**Summary**: 11 of 18 applicable domains have at least partial coverage. However, coverage is limited to standard FHIR clinical resources. The product's natively generated data — secure messages, appointment scheduling, care coordination workflows, patient-reported data, and aggregated claims — is entirely absent from the export.

## 6. Documentation Quality

The documentation quality is **poor**:

- **12 pages total**, of which ~3 pages are title/TOC/copyright, ~3 pages are UI screenshots, and ~6 pages describe the FHIR Bulk Data API mechanics (authentication, request/response format, error codes).
- **No data dictionary at all**: The documentation never describes what fields are in the exported FHIR resources or whether any vendor-specific extensions are included. The only content documentation is a list of 20 FHIR resource type names and a link to the HL7 FHIR NDJSON specification.
- **No sample data**: The ZIP screenshot shows file names but no content. The "sample format" section on page 7 just shows an ndjson file icon with no content.
- **No schema artifacts**: No JSON schemas, FHIR StructureDefinitions, or CapabilityStatements are provided.
- **Outdated contact information**: The documentation references techsvc@mphrx.com for API access, but mphrx.com appears to be offline since the agilon acquisition.
- **Created in 2021, never updated**: The document is dated June 2021, coinciding with initial certification. No evidence of updates since.

A developer trying to consume this export would need to:
1. Understand FHIR R4 resource schemas independently
2. Guess whether any vendor extensions exist in the data
3. Hope that the standard FHIR Patient $export API behavior applies
4. Contact an email address at a defunct domain for API credentials

The FHIR Bulk Data API documentation itself is reasonably clear (token acquisition, export initiation, status polling, download) — but this is just standard FHIR Bulk Data Export behavior, not vendor-specific documentation.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The Minerva (b)(10) EHI export is a FHIR Bulk Data Export repackaged as the EHI export. It exports 20 standard FHIR R4 resource types in NDJSON format — this is functionally identical to the (g)(10) Standardized API (FHIR Bulk Data) capability. There is no evidence that the (b)(10) export provides any data beyond what the FHIR API already exposes. The product's natively generated data (secure messages, appointments, care coordination tasks, patient-reported outcomes, claims data) is not represented in any of the 20 exported resource types.

### Key Findings

1. **The (b)(10) export is identical to the FHIR Bulk Data API**: The export produces the same 20 FHIR R4 resource types available through the standardized API. There is no additional data, no native database export, and no vendor-specific content. This is a clear case of FHIR repackaging — the vendor certified the same capability twice under different criteria.

2. **Claims data is explicitly missing despite being a core product capability**: Product materials state Minerva "brings together clinical and claims data," yet no Claim, ExplanationOfBenefit, or Coverage resources are included in the export. This is a significant gap given claims data is squarely within the designated record set.

3. **Natively generated patient engagement data is completely absent**: Minerva's patient engagement module generates secure messages, appointment records, care coordination tasks, and patient-reported data — all of which constitute EHI. None of these are exported. No Communication, Appointment, Task, or QuestionnaireResponse resources are supported.

4. **No data dictionary exists**: The documentation provides zero field-level detail. The only documentation of export content is a list of 20 FHIR resource type names and a reference to the HL7 FHIR specification. A consumer cannot determine from the documentation alone what data they would receive.

5. **Documentation is frozen at 2021 certification date**: The 12-page PDF was created in June 2021 and shows no signs of updates. Contact references point to mphrx.com, which is offline following agilon's 2023 acquisition.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   NDJSON (FHIR R4 Bulk Data Export)
Model type:      Standard projection (FHIR R4 resources)
Entities:        20 FHIR resource types (API list); 14 visible in sample ZIP
Fields:          N/A (no data dictionary; standard FHIR resource schemas apply)
Descriptions:    N/A (no field-level documentation provided)
Sample data:     No (screenshot shows file names only, no content)
Bulk export:     Yes (FHIR $export API with SMART Backend Services auth)
Domains covered: 11 of 18 applicable domains (clinical summary only)
```

### Bottom Line

Minerva's EHI export is a FHIR Bulk Data API relabeled as the (b)(10) export. It covers standard clinical summary data (demographics, conditions, medications, labs, etc.) but entirely omits the platform's natively generated data — secure messages, appointments, care coordination workflows, patient-reported outcomes — and the aggregated claims data the product explicitly stores. A patient would get a clinical data summary but not a complete copy of all their data in the system. The single biggest gap is the absence of claims data and patient engagement data that the product explicitly manages.
