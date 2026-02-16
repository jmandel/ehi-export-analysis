# EHI Export Analysis: OT EMR, Inc.

**Product**: OneTouch EMR, Version 3
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.05.2821.OTEM.01.00.1.250224 (CHPL ID 11599)

## 1. Product Context

OneTouch EMR is a cloud-based ambulatory EHR and practice management system built by OT EMR, Inc. (Dallas, TX), targeting small to mid-size primary care practices. Founded in 2010 by Dr. Robert Abbate, D.O., it is a small-vendor product with a modest user base.

The product is a single integrated platform combining:

- **EHR / Clinical Documentation**: Patient charting with templates, voice dictation (Dragon), vital signs, clinical assessments, iPad photo capture with annotation (Free Draw tool), ICD-10 coding, E&M coding helper
- **E-Prescribing**: Electronic prescribing including EPCS (controlled substances), drug interaction checks
- **Lab Integration**: Electronic lab orders and results with nationwide labs
- **Practice Management / Scheduling**: Appointment scheduling, reminders (text/email), patient demographics
- **Patient Portal**: Secure messaging, telemedicine, online billing/payments, online scheduling, medical summary viewing, patient check-in forms
- **Medical Billing & Revenue Cycle**: Integrated billing, unlimited eClaims, claim scrubbing, clearinghouse integration, ERA processing, eligibility verification, denial management, payment processing, patient billing
- **Interoperability**: HL7 interfaces, FHIR R4 API, Direct messaging, C-CDA document exchange, integrated fax

Key data domains the product stores: patient demographics, clinical encounter notes, clinical images/annotations, prescriptions/medications, lab orders/results, documents/faxes, appointments, patient portal messages, patient-submitted forms, billing/claims/ERA/payment data, CQM data, and care transition documents.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf` | 159-page PDF (1.1 MB). FHIR R4 API documentation covering 18 US Core resource types with attribute tables, search parameters, worked JSON examples, FHIR Bulk Data API, OAuth 2.0 security, and a dedicated EHI Export section (pp. 153–157). Produced via Google Docs (Skia/PDF m120 renderer). **This is the sole artifact — the entire EHI export documentation.** | Primary source |

Only one artifact was collected; the registered (b)(10) documentation URL points directly to this single PDF. No additional data dictionaries, sample data files, schemas, or supplementary documentation exist.

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON files packaged in a ZIP archive, with a README.txt listing US Core profile URLs for each resource type
- **Mechanism**: UI-based export via Administration > General > Single Patient Export. Users with Office Manager, Practice Administrator, or System Administrator roles can trigger exports through the admin panel. The user searches for a patient by name (autocomplete), clicks "Export," monitors job status on the same page, and receives the ZIP file as an attachment in the internal Messaging system inbox.
- **Single-patient**: Yes, via the UI described above
- **Bulk/All-patient**: Available but only via support request to OneTouch EMR ("due to the large volume of data that needs to be processed, this can only be requested through support by contacting OneTouch EMR")
- **Access constraints**: Requires Office Manager, Practice Administrator, or System Administrator role. API access is free for paid-plan clients; free-tier clients must pay an additional fee.
- **Underlying technology**: The EHI export section states explicitly: "OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data." The export produces the same 18 US Core resource types as the (g)(10) FHIR Bulk Data API.

## 4. Export Content: What's In It

The export consists of exactly 18 NDJSON files (one per FHIR resource type) plus a README.txt, delivered as a ZIP archive. This is confirmed by the screenshot on p. 156 of the PDF showing the ZIP contents:

| File | Size (from screenshot) |
|---|---|
| README.txt | 3.5 kB |
| Provenance-306.ndjson | 745 bytes |
| Procedure-305.ndjson | 978 bytes |
| Practitioner-304.ndjson | 824 bytes |
| Patient-303.ndjson | 1.9 kB |
| Organization-302.ndjson | 738 bytes |
| Observation-301.ndjson | 10.4 kB |
| MedicationRequest-300.ndjson | 3.3 kB |
| Location-299.ndjson | 480 bytes |
| Immunization-298.ndjson | 1.2 kB |
| Goal-297.ndjson | 696 bytes |
| Encounter-296.ndjson | 1.3 kB |
| DocumentReference-295.ndjson | 64.9 kB |
| DiagnosticReport-294.ndjson | 5.1 kB |
| Device-293.ndjson | 775 bytes |
| Condition-292.ndjson | 6.0 kB |
| CareTeam-291.ndjson | 1.1 kB |
| CarePlan-290.ndjson | 3.7 kB |
| AllergyIntolerance-289.ndjson | 1.6 kB |

Total: 19 objects (109.2 kB). All files dated 23 October 2023.

### Data Dictionary

The PDF documents "supported attributes" for each of the 18 FHIR resources in two-column tables (Name | Comments). These are standard FHIR element names with brief descriptions — not a proprietary data dictionary mapping internal database fields. No data types, cardinality, or value set enumerations are provided beyond what's inherent in the US Core profiles referenced.

**Parsed totals** (from `analysis/entity-inventory-full.json`):

- **18 entities** (FHIR resource types)
- **126 total fields** documented across all resources
- **126 fields (100%)** have descriptions (brief comments)
- No data types specified beyond implicit FHIR types
- No foreign key / relationship documentation beyond FHIR references
- No value set enumerations (just references to standard code systems)

### Vendor's own content organization

The vendor does not organize the export into domain categories — it is presented as a flat list of 18 FHIR resources conforming to US Core STU3.1.1. The README.txt in the export ZIP lists each resource with its US Core profile URL.

| Entity (FHIR Resource) | Fields | Described | Types | US Core Profile |
|---|---|---|---|---|
| AllergyIntolerance | 8 | 8 | No (implicit) | us-core-allergyintolerance |
| CarePlan | 6 | 6 | No | us-core-careplan |
| CareTeam | 6 | 6 | No | us-core-careteam |
| Condition | 6 | 6 | No | us-core-condition |
| Device | 10 | 10 | No | us-core-implantable-device |
| DiagnosticReport | 10 | 10 | No | us-core-diagnosticreport-note, us-core-diagnosticreport-lab |
| DocumentReference | 10 | 10 | No | us-core-documentreference |
| Encounter | 11 | 11 | No | us-core-encounter |
| Goal | 4 | 4 | No | us-core-goal |
| Immunization | 6 | 6 | No | us-core-immunization |
| Location | 5 | 5 | No | us-core-location |
| MedicationRequest | 9 | 9 | No | us-core-medicationrequest |
| Observation | 8 | 8 | No | us-core-smokingstatus, us-core-observation-lab, vital signs, pediatric profiles, pulse-oximetry |
| Organization | 6 | 6 | No | us-core-organization |
| Patient | 11 | 11 | No | us-core-patient |
| Practitioner | 3 | 3 | No | us-core-practitioner |
| Procedure | 4 | 4 | No | us-core-procedure |
| Provenance | 3 | 3 | No | us-core-provenance |
| **Total** | **126** | **126** | | |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor covers exactly the US Core STU3.1.1 resource set — 18 FHIR resource types that map to USCDI v1 data classes. The export is explicitly built on FHIR Bulk Data Access (the same mechanism as their (g)(10) API). The documentation states the API "permits users, developers and other health IT applications to request data for patient health information that is part of the requirements of U.S. Core Data for Interoperability (USCDI) v1" (p. 3).

The export provides reasonable coverage of standard clinical data: demographics, allergies, conditions/problems, medications, lab results, vitals, immunizations, procedures, encounters, care plans, goals, care teams, devices, clinical notes/documents, and provenance. DocumentReference is the largest file in the sample export (64.9 kB), suggesting clinical documents are included. DiagnosticReport covers both clinical notes and lab results via two profiles.

However, the export is bounded exactly at USCDI v1 — there is nothing beyond the standard US Core resource set. No vendor extensions, no custom mappings, no additional resource types. The README.txt in the ZIP lists only standard US Core profile URLs.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (11 fields: identifier, name, telecom, gender, birthdate, address, maritalStatus, communication, race, ethnicity, birthsex) | Covers USCDI demographics; limited to US Core Must Support elements |
| Encounters / visits | ✅ Covered | `Encounter` (11 fields) | Basic encounter data present |
| Problems / conditions / diagnoses | ✅ Covered | `Condition` (6 fields: clinicalStatus, verificationStatus, category, encounter, code, subject) | Covers problem-list-item, encounter-diagnosis, health-concern categories |
| Medications / prescriptions | ⚠️ Partial | `MedicationRequest` (9 fields) | Prescription orders present, but no MedicationDispense (fill status), no EPCS workflow details, no pharmacy routing data. Product has full e-prescribing with EPCS. |
| Allergies | ✅ Covered | `AllergyIntolerance` (8 fields including reaction details) | Adequate |
| Immunizations | ✅ Covered | `Immunization` (6 fields) | Basic immunization data |
| Vitals | ✅ Covered | `Observation` (vital-signs category, 8 fields) | Standard vital signs |
| Lab results | ✅ Covered | `Observation` (laboratory category), `DiagnosticReport` (lab profile) | Lab results and reports present |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` (note profile), `DocumentReference` | Report metadata present; unclear if actual DICOM/image data is exported. Clinical images from iPad capture and Free Draw annotations are likely not covered. |
| Procedures | ✅ Covered | `Procedure` (4 fields: status, code, performedDateTime, encounter) | Basic procedure records; very thin (4 fields) |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (10 fields), `DiagnosticReport` (10 fields) | Notes present; base64-encoded content noted. Covers 7 note types per DocumentReference type list (discharge summary, consult, H&P, progress, procedure, lab, imaging). |
| Care plans / goals | ✅ Covered | `CarePlan` (6 fields), `Goal` (4 fields) | Present but thin |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral-specific resources | Product likely supports referrals via its HL7/interoperability features; not in export |
| Insurance / coverage | ❌ Not covered | No Coverage, InsurancePlan, or related resources | Product stores insurance information (demographics, billing); significant gap |
| Claims / billing | ❌ Not covered | No Claim, ClaimResponse, ExplanationOfBenefit, or billing resources | Product has **integrated medical billing**, eClaims, claim scrubbing, clearinghouse integration, ERA processing, denial management. **Major gap.** |
| Payments | ❌ Not covered | No payment-related resources | Product has integrated POS payment processing, patient billing, ERA auto-processing. Significant gap. |
| Consents / directives | ❌ Not covered | No Consent resources | Unknown if product stores formal consent records |
| Patient communications / portal messages | ❌ Not covered | No Communication resources | Product has secure patient-provider messaging, telemedicine. Gap. |
| Specialty-specific | N/A | No specialty-specific data | Product targets primary care; no specialty modules identified |

**Summary**: 10 of 18 applicable domains have at least partial coverage. 8 domains are not covered at all, including billing/claims (the product's most significant non-USCDI capability) and patient communications.

## 6. Documentation Quality

- **Structure**: Well-organized 159-page PDF with clear table of contents and consistent formatting per resource.
- **Field documentation**: Each resource has a brief attributes table mapping FHIR element names to one-line descriptions. Descriptions are functional but shallow — they typically restate the FHIR element definition with USCDI data element cross-references. No data types, cardinality, or nullability are specified beyond what's inherent in the US Core profile.
- **Examples**: Strong. Every resource type has complete worked examples with full JSON request/response pairs. The EHI Export section includes 4 UI screenshots showing the export workflow end-to-end.
- **Machine-readable artifacts**: None. No downloadable schema, sample export data, or FHIR CapabilityStatement beyond what's in the PDF.
- **Implementability**: A developer could consume the FHIR API based on this documentation. However, there is no product-specific data dictionary — a developer would need to rely entirely on the standard US Core profiles to understand the data model. The documentation adds minimal vendor-specific insight.
- **What's missing**: No mapping of internal database fields to FHIR elements. No documentation of what data in the product is NOT exported. No data dictionary for billing, scheduling, portal, or other non-USCDI data domains. No ER diagram or relationship documentation.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers the standard USCDI v1 clinical data classes via 18 US Core FHIR resources (126 documented fields). This provides reasonable coverage of core clinical domains — demographics, conditions, medications, labs, vitals, immunizations, procedures, encounters, clinical notes, care plans, goals, care teams, and devices. However, the product includes **integrated medical billing and revenue cycle management** (eClaims, claim scrubbing, ERA processing, denial management, payment processing, eligibility verification) — none of which appears in the export. Patient portal communications (secure messaging, telemedicine records) and patient-submitted forms are also absent. The billing gap is particularly significant because OneTouch EMR explicitly markets itself as an integrated EHR + PM + billing platform, and billing/claims data is squarely within the HIPAA Designated Record Set.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of (g)(10) repackaged as (b)(10). The EHI Export section of the documentation (p. 153) states plainly: "OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data." The export produces exactly the same 18 US Core resource types as the Bulk Data API. The README.txt in the export ZIP lists only standard US Core profile URLs — no vendor extensions, no custom resources, no non-USCDI data. The implementation instructions (p. 3) explicitly scope the API to "USCDI v1." The vendor has built a thoughtful UI wrapper (admin panel with patient search, job monitoring, and messaging delivery), but the underlying data scope is identical to the (g)(10) FHIR Bulk Data export.

### Key Findings

1. **The EHI export is the (g)(10) FHIR Bulk Data API repackaged with a UI.** The documentation explicitly states "OneTouch EMR leverages FHIR Bulk Data Access to enable users to export patient data" (p. 153). The same 18 US Core resources are exported.

2. **Billing and revenue cycle data is entirely absent.** OneTouch EMR has integrated billing, eClaims, ERA processing, denial management, and payment processing. None of this appears in the export. No Claim, Coverage, ExplanationOfBenefit, or payment resources are present.

3. **No product-specific data dictionary exists.** The documentation maps only standard FHIR element names with brief comments — there is no mapping from internal database fields to export fields, and no documentation of what data is excluded.

4. **126 fields across 18 resources is thin for a full-featured EHR+PM product.** Many resources have very few fields (Practitioner: 3, Provenance: 3, Procedure: 4, Goal: 4), suggesting only Must Support elements from US Core are populated.

5. **The UI export workflow is well-designed.** Single-patient export via admin panel with autocomplete search, job monitoring, and message delivery is user-friendly. All-patient export requires contacting support, which is a limitation.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   FHIR R4 NDJSON (ZIP)
Entities:        18 (FHIR resource types)
Fields:          126
Descriptions:    100% (brief comments, no types/cardinality)
Sample data:     Yes (screenshot of sample export ZIP in documentation)
Bulk export:     Yes (via support request only)
Domains covered: 10 of 18 applicable domains
```

### Bottom Line

OneTouch EMR's (b)(10) EHI export is its (g)(10) FHIR Bulk Data API with a UI wrapper — it exports only the 18 US Core resource types covering USCDI v1 clinical data. For a product that includes integrated medical billing, claims processing, patient portal messaging, and e-prescribing with EPCS, the export omits entire categories of designated record set data, most critically billing and financial records. A patient would receive a reasonable clinical summary but would be missing their billing history, insurance interactions, portal messages, and any data stored beyond standard US Core elements.
