# EHI Export Analysis: agilon health inc.

**Product**: Minerva V4
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3082.Mine.04.01.0.210609 (CHPL #10649)

## 1. Product Context

Minerva is a **FHIR-native healthcare data aggregation and patient engagement platform**, originally built by MphRx and acquired by agilon health in March 2023 for $45M. It is **not a traditional EHR** — it is a data interoperability platform that aggregates clinical data *from* EHRs and other clinical systems (EMRs, HIS, PACS) rather than serving as a system of record for clinical documentation.

Minerva's two primary functional areas are:
1. **Interoperability Platform**: Integrates and aggregates data from disparate healthcare IT systems into a unified FHIR-based patient record, providing SMART on FHIR APIs for third-party application integration.
2. **Patient Engagement**: Web and mobile applications for patients/family members to access health data, book appointments, securely message providers, and share information.

Additional capabilities include care coordination (including surgical coordination workflows), virtual care/telemedicine, clinical viewer for providers, and analytics. Minerva has been deployed at scale — managing 460M+ patient records across 20+ countries with 52M+ active patient accounts (per Frost & Sullivan, 2020).

**Data the product stores** (relevant to export completeness assessment):
- **Aggregated clinical data** from connected systems (demographics, conditions, medications, labs, notes, etc.) — stored as FHIR resources
- **Claims data** (explicitly mentioned in vendor materials: "brings together clinical and claims data")
- **Natively generated data**: patient-reported outcomes, appointment/scheduling data (16M+ appointments booked), secure messages, patient engagement activity, care coordination tasks/documents/alerts, user accounts
- **Imaging references** (PACS integration)

The certified criteria are limited: primarily (b)(10) for EHI export, (e)(1)/(e)(3) for patient access, and (g) criteria for FHIR APIs. Notably absent are all clinical criteria (a)(1)–(a)(14), consistent with Minerva being a data aggregation platform.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `Mphrx-EHI-export-documentation.pdf` | Core EHI export documentation with UI screenshots and API instructions | 12 pages, 638 KB | **Most informative** — lists supported FHIR resources, shows export UI, documents bulk API workflow |
| `Mandatory-Disclosures-Letter_MphRx.pdf` | ONC mandatory disclosures with cost/fee information | 5 pages, 630 KB | Low — standard disclosure letter, confirms subscription pricing model |
| `FHIR-Data-Elements-mphrX.pdf` *(from disclosures page, not in downloads)* | Documents FHIR complex and primitive data types | 8 pages, 277 KB | Low — documents generic FHIR data types (Coding, Address, etc.), **not** resource-specific field schemas |
| `FHIR-Search-Guide-mphrX.pdf` *(from disclosures page, not in downloads)* | FHIR R4 search parameter documentation | 10 pages, 266 KB | Low — search API guide, no export-specific content |
| agilonhealth.com/onc-health-it-disclosures/ *(live web page)* | ONC disclosures page with links to all documentation | Active as of analysis date | Useful for discovering the FHIR Data Elements and Search Guide PDFs |

**Note**: The original `downloads/` folder contained only the two PDFs (EHI export doc and mandatory disclosures). The FHIR Data Elements and FHIR Search Guide PDFs were discovered by examining the live ONC disclosures web page, which links to them. Neither provides a data dictionary for the export.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON (Newline Delimited JSON). One file per FHIR resource type, split into multiple files at 10,000 records per file (e.g., `patient_file_1.ndjson`, `patient_file_2.ndjson`).
- **Mechanism**:
  - **Single-patient**: UI-based export from the Minerva portal. Clinical Admin/Admin selects a patient → Action → Export EHI → receives a ZIP download notification containing NDJSON files and a readme.txt.
  - **Bulk (all patients)**: FHIR Bulk Data Export API (`Patient/$export`) using SMART Backend Services Authorization. Requires contacting MphRx team (techsvc@mphrx.com) to obtain a Client ID. Uses async polling pattern (status URL → download URLs).
- **Access constraints**: Requires Clinical Admin/Admin role for UI export. Bulk API requires pre-registration with MphRx team. Download URLs expire after 48 hours.
- **Bulk export**: Yes, supported via API.
- **Fees**: Platform requires one-time implementation fee and monthly subscription based on active patient records (tiered pricing). No separate EHI export fee documented.

## 4. Export Content: What's In It

### FHIR Resource Types

The export is a standard FHIR Bulk Data Export. The documentation lists **20 supported FHIR resource types** for the bulk API (Section 3.2.1, page 8 of the EHI export documentation):

AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance

The single-patient UI export ZIP screenshot (page 6) shows **14 NDJSON files** plus a readme.txt:

allergyintolerance, careteam, clinicalimpression, diagnosticreport, documentreference, encounter, location, medication, medicationrequest, observation, patient, practitioner, procedure, provenance

**Discrepancy**: ClinicalImpression appears in the UI export ZIP but is **not listed** in the bulk API's supported resources. Conversely, CarePlan, Condition, Device, Goal, Immunization, Organization, and PractitionerRole are listed for the bulk API but do not appear in the ZIP screenshot. The ZIP screenshot likely reflects a specific patient's actual data (empty resources omitted from the ZIP) rather than a true capability difference. The union is **21 distinct FHIR resource types**.

### No Data Dictionary

**There is no data dictionary or resource-specific field documentation.** The vendor provides:
- A list of supported FHIR resource types (names only, no field enumeration)
- Generic FHIR complex data type definitions (Coding, CodeableConcept, Address, etc. — 18 types with 95 fields total) in the FHIR Data Elements PDF
- 19 FHIR primitive type definitions
- A readme.txt in the export ZIP that links to the HL7 NDJSON specification

The implicit expectation is that consumers understand FHIR R4 resource structures. No vendor-specific extensions, custom fields, or data dictionary mapping from the Minerva internal model to FHIR resources is provided.

### Vendor's own content organization

The vendor does not organize the export by clinical domains. The only structure is the flat list of FHIR resource types. Based on the documentation:

| FHIR Resource | In Bulk API | In UI Export ZIP | EHI Domain |
|---|---|---|---|
| AllergyIntolerance | ✅ | ✅ | Allergies |
| CarePlan | ✅ | — | Care plans / goals |
| CareTeam | ✅ | ✅ | Care plans / goals |
| ClinicalImpression | — | ✅ | Clinical notes / documents |
| Condition | ✅ | — | Problems / conditions / diagnoses |
| Device | ✅ | — | Procedures |
| DiagnosticReport | ✅ | ✅ | Lab results / diagnostic reports |
| DocumentReference | ✅ | ✅ | Clinical notes / documents |
| Encounter | ✅ | ✅ | Encounters / visits |
| Goal | ✅ | — | Care plans / goals |
| Immunization | ✅ | — | Immunizations |
| Location | ✅ | ✅ | Encounters (supporting) |
| Medication | ✅ | ✅ | Medications / prescriptions |
| MedicationRequest | ✅ | ✅ | Medications / prescriptions |
| Observation | ✅ | ✅ | Vitals / lab results / observations |
| Organization | ✅ | — | Demographics (supporting) |
| Patient | ✅ | ✅ | Demographics |
| Practitioner | ✅ | ✅ | Encounters (supporting) |
| PractitionerRole | ✅ | — | Encounters (supporting) |
| Procedure | ✅ | ✅ | Procedures |
| Provenance | ✅ | ✅ | Data provenance |

**No field counts, descriptions, or types are provided per resource.** The vendor documents only the existence of these resource types, not their internal structure or which elements are populated.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a standard set of **USCDI / US Core-aligned FHIR resources**. The 20–21 resource types map to the core clinical data categories (demographics, conditions, medications, allergies, immunizations, vitals/labs, encounters, procedures, care plans, clinical notes via DocumentReference, and provenance). This is essentially the same set of resources one would expect from a FHIR R4 patient access API or Bulk FHIR export — it is not a deep or customized export.

There are no resources for:
- Billing, claims, or financial data (no Coverage, Claim, ExplanationOfBenefit, Invoice)
- Patient communications or messages (no Communication resource)
- Appointments or scheduling (no Appointment, Schedule, Slot)
- Consent or directives (no Consent resource)
- Orders or referrals beyond MedicationRequest (no ServiceRequest, ReferralRequest)
- Patient-reported outcomes (no QuestionnaireResponse)
- Care coordination task data (no Task resource)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient, Organization resources | Standard FHIR Patient resource |
| Encounters / visits | ✅ Covered | Encounter, Location, Practitioner, PractitionerRole | Standard FHIR Encounter |
| Problems / conditions / diagnoses | ✅ Covered | Condition resource | Standard FHIR Condition |
| Medications / prescriptions | ✅ Covered | Medication, MedicationRequest resources | Standard FHIR medication resources |
| Allergies | ✅ Covered | AllergyIntolerance resource | Standard FHIR AllergyIntolerance |
| Immunizations | ✅ Covered | Immunization resource | Standard FHIR Immunization |
| Vitals | ⚠️ Partial | Observation resource (covers vitals, labs, and other observations) | Single resource for all observation types; no documentation on which observation categories are populated |
| Lab results | ⚠️ Partial | DiagnosticReport, Observation resources | Present but no documentation on which lab types are included |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport resource | Product integrates with PACS; unclear if imaging data/references are actually in export |
| Procedures | ✅ Covered | Procedure, Device resources | Standard FHIR Procedure |
| Clinical notes / documents | ✅ Covered | DocumentReference, ClinicalImpression resources | DocumentReference can carry note content; depth unknown |
| Care plans / goals | ✅ Covered | CarePlan, CareTeam, Goal resources | Standard FHIR care plan resources |
| Orders / referrals | ⚠️ Partial | MedicationRequest only | No ServiceRequest for non-medication orders or referrals — **gap** given care coordination is a core feature |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resources | Minerva aggregates data including insurance info; this is a gap |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or Invoice resources | Product "brings together clinical and claims data" per vendor materials; **significant gap** |
| Payments | ❌ Not covered | No PaymentNotice or PaymentReconciliation resources | N/A — platform is not a billing system |
| Consents / directives | ❌ Not covered | No Consent resource | May store consent-related data; minor gap |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product provides secure messaging as a core feature (16M+ appointments, messaging); **significant gap** for natively-generated data |
| Scheduling / appointments | ❌ Not covered | No Appointment, Schedule, or Slot resources | Product's patient engagement module handles appointment booking (16M+ appointments booked); **significant gap** for natively-generated data |
| Patient-reported outcomes | ❌ Not covered | No QuestionnaireResponse resource | Product collects patient-reported data; **gap** |
| Care coordination tasks | ❌ Not covered | No Task resource | Product has care/surgery coordination with task management; **gap** for natively-generated data |

## 6. Documentation Quality

The documentation quality is **thin**:

- **No data dictionary**: No field-level documentation for any FHIR resource. The FHIR Data Elements PDF documents only generic FHIR data types (Coding, Address, HumanName, etc.), not the specific elements within each resource type.
- **No sample data**: No sample NDJSON files, no example FHIR resources. The screenshot shows only file names in a ZIP, not content.
- **No schema documentation**: No indication of which FHIR profiles are used, which elements are populated, or whether there are any vendor extensions.
- **No value sets**: No documentation of code systems or terminology used.
- **No relationships**: No documentation of how resources reference each other beyond standard FHIR references.

What IS documented:
- The export **process** is clearly documented with step-by-step screenshots (UI) and API call sequences (bulk).
- The **list of supported FHIR resource types** is explicitly stated.
- The **bulk API** mechanics (authentication, polling, download) are adequately documented.
- A **readme.txt** in the export links to the HL7 NDJSON specification.

A developer familiar with FHIR R4 could use the bulk export API, but would have to inspect the actual exported data to understand what fields are populated, what codes are used, and how resources relate to each other. A developer unfamiliar with FHIR would have insufficient documentation to build an import.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The EHI export is a standard FHIR Bulk Data Export. It projects Minerva's internal data model (which aggregates clinical data from multiple sources into FHIR resources) into standard FHIR R4 NDJSON output. The 20–21 resource types are a typical USCDI/US Core-aligned set that covers core clinical domains but omits billing/claims, patient communications, scheduling, and other natively-generated data that the platform stores.

### Key Findings

1. **Export is FHIR Bulk Data repackaged as (b)(10)**: The export mechanism is indistinguishable from the standard FHIR Bulk Data Export API that the platform already provides for (g)(10) certification. The same 20 FHIR resource types serve both purposes. There is no evidence of additional data beyond what the FHIR API provides.

2. **No data dictionary or field-level documentation**: Despite exporting 20+ FHIR resource types, the vendor provides zero resource-specific field documentation. The "FHIR Data Elements" PDF only documents generic FHIR data types (Coding, Address, etc.), not the structure of any exported resource.

3. **Significant gaps in natively-generated data**: Minerva generates its own data through patient engagement (messaging, scheduling, patient-reported outcomes) and care coordination (tasks, surgical workflows). None of this natively-generated data appears in the export — only aggregated clinical data mapped to standard FHIR resources.

4. **Claims data gap**: Vendor materials explicitly state Minerva "brings together clinical and claims data," but no claims/billing resources (Coverage, Claim, ExplanationOfBenefit) appear in the export.

5. **Documentation dates from 2021**: All artifacts (EHI export doc, data elements, search guide, mandatory disclosures) date from May–June 2021 and have not been updated, despite the product continuing to evolve under agilon health's ownership.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 NDJSON
Model type:      Standard projection (FHIR Bulk Data Export)
Entities:        20–21 FHIR resource types
Fields:          N/A (no field-level documentation provided)
Descriptions:    N/A (no resource-specific documentation)
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data API)
Domains covered: 11 of 20 applicable domains (with several partial)
```

### Bottom Line

Minerva's EHI export is its standard FHIR Bulk Data Export relabeled as (b)(10). It covers core clinical domains through 20 standard FHIR resource types but misses data the platform natively generates — patient messages, appointments, care coordination tasks, and patient-reported outcomes — as well as claims data it explicitly aggregates. The complete absence of a data dictionary makes it impossible to assess field-level completeness from documentation alone.
