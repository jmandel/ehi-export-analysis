# EHI Export Analysis: Radysans, Inc

**Product**: Radysans EHR v5.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2912.Rady.05.00.1.191231 (CHPL #10253)

## 1. Product Context

Radysans EHR is an integrated ambulatory EHR and practice management platform targeting small outpatient clinics and physician practices. It is a cloud-hosted SaaS product (ehr.cutecharts.com) developed by Radysans, Inc, a very small vendor based in Apex, NC. The only identifiable customer is Mann ENT, an otolaryngology practice in the Raleigh-Durham area.

The product comprises several integrated modules relevant to EHI scope:

- **EMR**: Clinical documentation including problems, medications, allergies, vitals, lab results, immunizations, procedures, implantable devices, social/behavioral data, clinical notes, and care plans. Certified across CPOE (a)(1)–(a)(4), CDS (a)(9), demographics (a)(5), and other clinical criteria.
- **Practice Management (PMS)**: Enterprise scheduling, patient registration (including scanned photos/insurance cards), referral management, message routing, and business intelligence reports.
- **e-Billing**: Charge capture, claim scrubbing, electronic claim submission to 2,500+ payers, denial tracking, EOB/ERA processing, payment posting, and patient statement generation.
- **Patient Portal**: Patient and caregiver access to health information, certified for View/Download/Transmit (e)(1).
- **Transcription Services**: Medical transcription with long-term storage.

This baseline establishes that a complete EHI export should cover clinical data, billing/claims records, insurance information, referral tracking, and patient-generated data — not just USCDI clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `B-10-Documentation.pdf` | Primary (b)(10) EHI export documentation | 1 page, 61 KB, created 2023-11-27 | **Most informative for (b)(10) scope** — but extremely thin |
| `G10ApplicationAccessTermsandCondition.pdf` | FHIR R4 API documentation for (g)(10) | 41 pages, 311 KB, last modified 2025-06-25 | Detailed API docs with 18 FHIR resource endpoints and sample JSON |
| `RadysansEHRCostsandLimitations.pdf` | Mandatory Disclosure Statement | 2 pages, 582 KB | Confirms data portability fee; minimal detail |
| `fhir-endpoint-bundle.json` | FHIR Endpoint/Organization bundle | 1.2 KB | Confirms API base URL at ehrwebapi.cutecharts.com/radywebapi |
| `screenshot-onc-certification-page.png` | Screenshot of ONC certification page | 275 KB | Shows page layout and link structure |

The B-10 document is the only artifact that directly addresses (b)(10) compliance. The G10 document provides the most technical detail but is (g)(10) API documentation that the B-10 document simply references.

## 3. Export Mechanics

- **Formats**: C-CDA XML and FHIR R4 JSON
- **Mechanism**: The B-10 document says the application provides export "for a single patient as well as for patient population." The FHIR path uses Bulk Data export via the (g)(10) API at `https://ehrwebapi.cutecharts.com/radywebapi/`. The C-CDA mechanism is not detailed — no instructions are provided for how to initiate or receive the C-CDA bulk export.
- **Single-patient vs bulk**: The document claims both ("single patient as well as for patient population"), but no operational details are provided for either path.
- **Access constraints**: The Mandatory Disclosure Statement lists data portability as requiring a "one-time fee per provider upon request of data extraction," suggesting this is a vendor-assisted process rather than a self-service feature.
- **No worked examples**: There are no instructions, screenshots, or process documentation showing how to actually trigger or receive an export.

## 4. Export Content: What's In It

### Overview

The (b)(10) export documentation describes two standard clinical data formats — C-CDA and FHIR — that together cover only the USCDI v1 data classes. There is **no data dictionary, no field-level documentation, no schema, and no sample export files** beyond the FHIR sample JSON responses embedded in the (g)(10) API document.

### C-CDA Export

The B-10 document lists 22 C-CDA sections:

| # | C-CDA Section |
|---|---|
| 1 | Allergies, Adverse Reactions, Alerts |
| 2 | Assessment Plan |
| 3 | Chief Complaint |
| 4 | Cognitive Status |
| 5 | Demographics |
| 6 | Reason for Visit / Encounters |
| 7 | Family History |
| 8 | Functional Status |
| 9 | Goals |
| 10 | Health Concerns |
| 11 | Immunizations |
| 12 | Instructions |
| 13 | Lab Results |
| 14 | Medical Equipment UDI |
| 15 | Medications |
| 16 | Plan of Care |
| 17 | Problem List |
| 18 | Procedures |
| 19 | Reason for Referral |
| 20 | Social History |
| 21 | Plan of Treatment |
| 22 | Vitals |

These are standard C-CDA sections corresponding to USCDI v1 requirements. No field-level detail, no sample files, and no documentation of what fields within each section are populated.

### FHIR Export

The (g)(10) document describes 18 FHIR R4 resource types, all conforming to US Core STU 3.1.1 profiles:

| # | FHIR Resource | Parameters Documented | Sample Output Provided |
|---|---|---|---|
| 1 | AllergyIntolerance | Clinical-Status, Patient | Yes |
| 2 | CarePlan | Category, Date, Patient, Status | Yes |
| 3 | CareTeam | Patient, Status | Yes |
| 4 | Condition | Category, Clinical-Status, Patient, Onset-Date | Yes |
| 5 | Device | Patient, Type | Yes |
| 6 | DiagnosticReport | Status, Patient, Category, Code, Date | Yes |
| 7 | DocumentReference | _id, Status, Patient, Category, Type, Date, Period | Yes |
| 8 | Encounter | _id, Class, Date, Identifier, Patient, Status, Type | Yes |
| 9 | Goal | Lifecycle-status, Patient, Target-date | Yes |
| 10 | Immunization | Patient, Status, Date | Yes |
| 11 | MedicationRequest | Status, Intent, Patient, Encounter, Authoredon | Yes |
| 12 | Observation | Status, Category, Code, Date, Patient | Yes |
| 13 | Organization | Name, Address | Yes |
| 14 | Patient | _id, Birthdate, Family, Gender, Given, Identifier, Name | Yes |
| 15 | Practitioner | Name, Identifier | Yes |
| 16 | PractitionerRole | Specialty, Practitioner | Yes |
| 17 | Procedure | Status, Patient, Date, Code | Yes |
| 18 | Provenance | Patient, Id | Yes |

These 18 resources are exactly the US Core required resource types — no vendor extensions, no non-US-Core resources, no custom profiles. The sample outputs use standard terminologies (SNOMED CT, LOINC, RxNorm, CVX) and contain synthetic test data (e.g., patient "ALICE NEWMAN," practitioner "Albert Davis" at "RADYSANS MU STAGE THREE PRACTICE").

### What's Missing

There is **no native data model export**. The vendor does not expose any internal database tables, proprietary data structures, or vendor-specific fields. The entire export is a projection of internal data into two interoperability standards (C-CDA and FHIR) that were designed for clinical summary exchange, not comprehensive data export.

Absent from the export:
- Billing records (claims, charges, payments, EOBs, ERAs, denial logs)
- Insurance/coverage data
- Appointment/scheduling data
- Referral management records (administrative tracking, pre-authorizations)
- Patient registration documents (scanned photos, insurance cards)
- Transcription records
- Portal activity and patient communications
- Custom forms or specialty-specific assessments

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor does not organize the export into custom categories — they simply list C-CDA sections and FHIR US Core resources. The two formats overlap substantially: both cover the same USCDI v1 clinical data classes (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, care plans, goals, clinical notes via DocumentReference, devices/UDI, social history, and provenance).

The export coverage is a 1:1 match with the US Core / USCDI v1 specification. There is no evidence of any data beyond what's required by the (g)(10) certification criterion. The (b)(10) export is functionally identical to the (g)(10) API output.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | C-CDA Demographics section; FHIR Patient resource (7 search params) | Standard US Core coverage only |
| Encounters / visits | ✅ Covered | C-CDA Reason for Visit / Encounters; FHIR Encounter resource | Basic encounter data; no scheduling detail |
| Problems / conditions | ✅ Covered | C-CDA Problem List; FHIR Condition resource | Standard coverage |
| Medications / prescriptions | ✅ Covered | C-CDA Medications; FHIR MedicationRequest resource | Prescription orders covered; no MAR or dispensing data |
| Allergies | ✅ Covered | C-CDA Allergies section; FHIR AllergyIntolerance resource | Standard coverage |
| Immunizations | ✅ Covered | C-CDA Immunizations; FHIR Immunization resource | Standard coverage |
| Vitals | ✅ Covered | C-CDA Vitals; FHIR Observation resource | Standard coverage |
| Lab results | ✅ Covered | C-CDA Lab Results; FHIR DiagnosticReport + Observation | Standard coverage |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport resource could include imaging; no dedicated imaging entity | Product supports CPOE for diagnostic imaging (a)(3); imaging orders/results may be thin |
| Procedures | ✅ Covered | C-CDA Procedures; FHIR Procedure resource | Standard coverage |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference resource; C-CDA sections for Chief Complaint, Assessment Plan | No evidence of transcription records being included; DocumentReference may not cover all note types |
| Care plans / goals | ✅ Covered | C-CDA Plan of Care/Treatment, Goals; FHIR CarePlan, Goal, CareTeam | Standard coverage |
| Orders / referrals | ⚠️ Partial | C-CDA Reason for Referral section | Clinical referral reason only; no administrative referral tracking, no pre-auth records |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product captures insurance data in PMS registration module; **significant gap** |
| Claims / billing | ❌ Not covered | No billing entities in export | Product has full e-Billing module (charge capture, claims, denials, EOBs/ERAs); **major gap** |
| Payments | ❌ Not covered | No payment entities in export | Product handles payment posting and reconciliation; **significant gap** |
| Consents / directives | ❌ Not covered | No consent entities in export | Product scans regulatory documents; may store consent records; gap if present |
| Patient communications / portal messages | ❌ Not covered | No messaging entities in export | Product has patient portal and Message Manager; gap for patient-facing communications |
| Specialty-specific (ENT) | ❌ Not covered | No specialty entities in export | Known customer is ENT practice; any specialty clinical data is absent |

**Summary**: 10 of 19 domains have standard clinical coverage via C-CDA/FHIR. 3 domains have partial coverage. 6 domains have no coverage at all. The missing domains include the product's entire billing/financial stack (claims, payments, insurance), which represents a substantial portion of patient-related EHI.

## 6. Documentation Quality

The (b)(10) documentation is **exceptionally thin**:

- **1 page** of documentation for the entire EHI export
- **No data dictionary** — not even a list of fields within C-CDA sections or FHIR resources
- **No schema files** — no XSD for C-CDA output, no FHIR StructureDefinitions, no proprietary schemas
- **No sample export files** — the only sample data is in the (g)(10) API document's inline JSON examples
- **No export instructions** — no UI screenshots, no step-by-step process, no API call sequences for bulk export
- **No relationship documentation** — no ERD, no foreign key descriptions
- **No value set documentation** — beyond what's implicit in FHIR sample outputs (SNOMED, LOINC, RxNorm)

The (g)(10) document (41 pages) provides meaningful technical detail for FHIR API access — OAuth2 flow, endpoint URLs, search parameters, and sample JSON for all 18 resource types. A developer could build a FHIR client from it. However, this is API documentation, not EHI export documentation. It tells you how to query the FHIR API, not what comprehensive EHI is available or how to obtain a full patient record.

A developer attempting to build an import system from these documents would:
- Know the FHIR resource types and their search parameters (from the g10 doc)
- Know the C-CDA section names (from the b10 doc)
- **Not know** what fields are populated within each resource/section
- **Not know** how to initiate the actual export process
- **Not know** what data is excluded from the export
- **Not know** anything about the internal data model

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is entirely composed of two interoperability standards (C-CDA and FHIR R4 US Core) that were designed for clinical data exchange, not comprehensive data export. There is no native data model exposure and no data beyond what the (g)(10) FHIR API already provides. The (b)(10) documentation is a 1-page reference to the existing (g)(10) infrastructure, not an independent export capability.

### Key Findings

1. **The (b)(10) export is the (g)(10) API repackaged.** The entire 1-page B-10 document lists C-CDA sections (standard clinical summary sections) and then refers the reader to the (g)(10) API documentation. The 18 FHIR resources are exactly the US Core required set with no extensions. This is a textbook example of repurposing existing clinical interoperability infrastructure as an "EHI export."

2. **The product's entire billing/financial module is absent from the export.** Radysans EHR includes a full e-Billing suite (charge capture, claim submission to 2,500+ payers, denial tracking, EOB/ERA processing, payment posting), yet zero billing entities appear in the export. This is a significant EHI gap — billing records about patients are squarely within the designated record set.

3. **No data dictionary exists.** There is no field-level documentation of any kind — no table definitions, no field descriptions, no types, no value sets, no relationships. The only technical detail comes from the (g)(10) FHIR sample outputs, which are example-based rather than formal specifications.

4. **Export may require vendor assistance and a fee.** The Mandatory Disclosure Statement lists data portability as requiring a "one-time fee per provider upon request of data extraction," suggesting this is not a self-service capability.

5. **Documentation is among the thinnest possible while still existing.** A single page listing C-CDA section names and a pointer to the FHIR API docs meets the bare minimum of having "documentation" for (b)(10) but provides almost no actionable information about the export's scope, content, or process.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + FHIR R4 JSON
Model type:      Standard projection (US Core / USCDI v1)
Entities:        22 C-CDA sections + 18 FHIR resources (overlapping; ~18 unique data categories)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     Inline FHIR examples only (no standalone sample files)
Bulk export:     Claimed but not detailed
Domains covered: 10 of 16 applicable domains (with 3 partial)
```

### Bottom Line

Radysans EHR's (b)(10) export is a clinical summary repackaged as comprehensive EHI. A patient or provider would receive standard USCDI clinical data (problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, notes, care plans) but would get none of their billing history, insurance records, claims, payments, referral tracking, or any specialty-specific data. The single biggest gap is the complete absence of the product's billing and financial data — a core module that generates patient-specific records clearly within the EHI designated record set.
