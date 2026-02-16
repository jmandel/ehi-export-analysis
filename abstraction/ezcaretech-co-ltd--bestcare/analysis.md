# EHI Export Analysis: ezCaretech Co., Ltd.

**Product**: BESTCare 2.0B
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2610.BEST.02.00.1.180423 (CHPL listing #9665)

## 1. Product Context

BESTCare is a comprehensive hospital information system (HIS) built by ezCaretech Co., Ltd., a publicly traded South Korean healthcare IT company (KOSDAQ: 099750) originally spun off from Seoul National University Hospital's IT department. The product was co-developed with Seoul National University Bundang Hospital (SNUBH) — the first hospital outside North America to achieve HIMSS EMRAM Stage 7.

BESTCare is designed for large hospitals and university tertiary medical centers. In the US market, it is deployed primarily at Aurora Behavioral Healthcare's 14 psychiatric hospitals as a behavioral-health-specialized variant.

The system is a full-scope HIS with broad data coverage relevant to EHI completeness assessment:

- **Clinical modules**: EMR (3,000+ templates), CPOE (medications, labs, imaging, procedures), CDSS (drug interactions, dosing alerts), closed-loop medication administration (barcode/RFID), nursing documentation, pharmacy, radiology, clinical pathways
- **Administrative/billing modules**: Billing, patient services, inpatient management, social services, CRM, activity-based costing
- **Data/analytics**: Clinical data warehouse (290 indicators), business intelligence
- **Integration**: HIE (HL7 V2.X, CDA), FHIR API (g)(10) certified

The product holds one of the broadest ONC certifications possible (33 criteria), including CPOE for medications, labs, and imaging; transitions of care; CQMs; public health reporting; and FHIR APIs. This is consistent with a system that stores extensive clinical, administrative, and billing data about patients.

## 2. Artifacts Reviewed

| # | Artifact | Size | Description | Informativeness |
|---|---------|------|-------------|-----------------|
| 1 | `b.10_EHI_Export.pdf` | 24.8 KB, 1 page | Primary (b)(10) documentation. Names CSV and Oracle DMP formats; contains no data dictionary, schema, or field definitions. Links to FHIR portal. | **Most critical** — this is the entire (b)(10) documentation |
| 2 | `BESTCare2.0B_Certified_Health_IT_v3.0.pdf` | 138.8 KB, 3 pages | List of 33 certified criteria and 13 CQMs. No technical EHI export detail. | Low — confirms certification only |
| 3 | `fhir-capability-statement.json` | 33.3 KB | FHIR R4 CapabilityStatement from ezFHIRStation. 26 resource types (standard US Core). Named "ezfhirstation-us-core-usa-aurora". | Moderate — documents the (g)(10) FHIR API scope |
| 4 | `single-patient-api.html` | 1.87 MB | Single Patient API Guide. Documents 30 US Core FHIR R4 profiles with must-have/must-support fields and search parameters. | Moderate — documents FHIR API, not (b)(10) |
| 5 | `multi-patient-api.html` | 87.0 KB | Multi Patient API Guide. Documents FHIR Bulk Data Export ($export) with NDJSON output. | Moderate — documents (g)(10) bulk API |
| 6 | `base-urls.html` | 41.6 KB | Service Base URLs for ezFHIRStation portal (authorization, APIs, testing). | Low |
| 7 | `screenshot-onc-disclosures-page.png` | 171.3 KB | Screenshot of ONC mandatory disclosures page. Confirms EHI Export PDF is the sole (b)(10) documentation link. | Low |
| 8 | `screenshot-single-patient-api.png` | 257.2 KB | Screenshot of Single Patient API page showing US Core resource documentation. | Low |
| 9 | `screenshot-multi-patient-api.png` | 273.3 KB | Screenshot of Multi Patient API page showing Bulk Data Export endpoints. | Low |

Additionally verified by fetching from the live ONC disclosures page:
- **Mandatory Disclosures Letter** (fetched live): Describes (b)(10) in one sentence — "This capacity allows to export electronic health information (EHI)." Mentions license fee, implementation fee, and recurring maintenance fee. No technical detail.
- **Real World Testing Results 2025** (fetched live): Confirms 128 single-patient EHI exports were initiated in the reporting period with a 98.4% success rate (126 completed) and 3.5-minute average completion time. Population-level exports were tested in a production-mirrored environment only. No detail on what data elements were included.

## 3. Export Mechanics

The (b)(10) PDF (`b.10_EHI_Export.pdf`) describes two export capabilities:

- **Single Patient Export**: Allows a user to export EHI for a single patient "at any time without developer assistance." No UI screenshots, workflow description, or access instructions are provided.
- **Multi-Patient Export**: Can export "all the data for a patient population." No further detail on how this is initiated or scoped.

**Format(s):**
- **CSV**: Comma-separated values files. No documentation of file structure (one file per table? one per domain? column headers?).
- **Oracle DMP**: Oracle binary database dump files. Proprietary format requiring Oracle tools to read.

**FHIR API** (linked from PDF Section II via "Click Here"):
- The FHIR portal at `portal.ezcaretech.com:30112` documents a standard (g)(10) FHIR API — not a separate (b)(10) mechanism. This is the ezFHIRStation US Core implementation supporting both single-patient (SMART on FHIR) and multi-patient (Bulk Data Export via $export) access.

**Access constraints**: The mandatory disclosures letter states a one-time software license fee, implementation service fee, and recurring maintenance fee are required. License fee is per-facility based on bed or provider count.

**Bulk export**: The RWT results report notes population-level exports were restricted to a production-mirrored environment "to avoid system performance impact," suggesting bulk export has operational constraints in production.

## 4. Export Content: What's In It

### 4a. Native Export (CSV / Oracle DMP) — Undocumented

The (b)(10) PDF provides **zero documentation** of what the CSV or Oracle DMP exports contain. There is:
- No data dictionary
- No table listing
- No field/column definitions
- No schema documentation
- No sample data
- No description of how tables relate to each other
- No description of how CSV files are organized (naming convention, one per table, etc.)

The only content-related claim is that the multi-patient export can export "all the data for a patient population." The RWT report states exports "included all required EHI data elements" but does not specify what those elements are.

An Oracle DMP *could* theoretically contain the entire database — making it potentially the most comprehensive possible export. But without any documentation, this is unknowable and unusable.

### 4b. FHIR API — Standard US Core (Not Native)

The FHIR API is documented but is a **(g)(10) implementation**, not a native (b)(10) export. It covers the standard US Core profile set:

| # | Resource Type | Category | Interactions | Search Params |
|---|--------------|----------|-------------|---------------|
| 1 | AllergyIntolerance | Clinical | read, search-type | 4 |
| 2 | CarePlan | Clinical | read, search-type | 3 |
| 3 | CareTeam | Clinical | read, search-type | 2 |
| 4 | Condition | Clinical | read, search-type | 4 |
| 5 | Device | Clinical | read, search-type | 2 |
| 6 | DiagnosticReport | Diagnostics | read, search-type | 5 |
| 7 | DocumentReference | Documents | read, search-type | 5 |
| 8 | Encounter | Clinical | read, search-type | 4 |
| 9 | Goal | Clinical | read, search-type | 3 |
| 10 | Immunization | Clinical | read, search-type | 3 |
| 11 | Medication | Medications | read, search-type | 0 |
| 12 | MedicationRequest | Medications | read, search-type | 4 |
| 13 | Observation | Diagnostics | read, search-type | 5 |
| 14 | Patient | Demographics | read, search-type | 7 |
| 15 | Procedure | Clinical | read, search-type | 3 |
| 16 | Provenance | Administrative | read, search-type | 0 |

Plus supporting/infrastructure types: Binary, CodeSystem, Endpoint, Group, Location, Medication, OperationDefinition, Organization, Practitioner, PractitionerRole, ValueSet.

The Single Patient API documents 30 US Core profiles (including vital signs sub-profiles: Blood Pressure, Body Height, Body Weight, Body Temperature, Heart Rate, Respiratory Rate, Pulse Oximetry, Pediatric BMI for Age, Pediatric Weight for Height, and Smoking Status).

The FHIR CapabilityStatement is named "ezfhirstation-us-core-usa-aurora" — explicitly referencing the Aurora Behavioral Healthcare deployment and confirming this is a standard US Core implementation with no vendor extensions for behavioral health or other specialty data.

### Vendor's own content organization

The vendor does not organize content into categories. The (b)(10) PDF has no data dictionary at all. The FHIR API follows the standard US Core profile organization. There is no vendor-specific content organization to present.

**Since there is no data dictionary, no entity/field inventory table can be generated.** The full-entity-inventory.json in the analysis directory captures what is available from the FHIR CapabilityStatement and API documentation — 26 resource types with their search parameters and profile references — but this documents the (g)(10) API, not the (b)(10) native export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) documentation describes two components:

1. **CSV / Oracle DMP export**: Claims to export "all the data" but provides zero documentation of content. Coverage is unknowable from the available documentation.

2. **FHIR API** (cross-referenced from (b)(10) PDF): Covers the standard US Core clinical data subset — 16 patient-facing resource types and 10 supporting types. This is the standard USCDI v1 clinical summary data set, with no vendor-specific extensions or additional behavioral health content.

The FHIR API is adequately documented for its own purpose (a (g)(10) API), but it represents only a clinical summary subset — demographics, conditions, medications, allergies, labs, vitals, immunizations, procedures, care plans, encounters, and clinical notes. It does not cover billing, orders beyond medication requests, specialty assessments, nursing documentation, or administrative data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource (US Core); native export undocumented | FHIR covers basic demographics; product likely stores richer registration data (insurance at registration, emergency contacts, etc.) |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource (US Core); native export undocumented | FHIR has basic encounters; product manages full inpatient workflows, bed management — likely much richer natively |
| Problems / conditions | ⚠️ Partial | FHIR Condition resource (US Core); native export undocumented | Standard problem list via FHIR; product's 3,000+ templates likely capture richer diagnostic context |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest + Medication (US Core); native export undocumented | Prescription data via FHIR; product has closed-loop medication administration (barcode/RFID verification records) not in FHIR |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance (US Core); native export undocumented | Standard allergy data via FHIR |
| Immunizations | ⚠️ Partial | FHIR Immunization (US Core); native export undocumented | Standard immunization records via FHIR |
| Vitals | ⚠️ Partial | FHIR Observation (vital signs profiles: BP, height, weight, temp, heart rate, resp rate, pulse ox); native export undocumented | Standard vitals via FHIR |
| Lab results | ⚠️ Partial | FHIR DiagnosticReport + Observation (lab profiles); native export undocumented | Standard lab results via FHIR; product's full lab workflow may include more |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (report/note exchange profile); native export undocumented | Basic report data via FHIR; product has dedicated radiology module likely with richer data |
| Procedures | ⚠️ Partial | FHIR Procedure (US Core); native export undocumented | Basic procedure records via FHIR |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference (US Core); native export undocumented | Document references via FHIR; product has 3,000+ templates — likely much richer native documentation model |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan + CareTeam + Goal (US Core); native export undocumented | Standard care plan data via FHIR; product has clinical pathways with variance tracking not in FHIR |
| Orders / referrals | ❌ Not covered | No order resources in FHIR beyond MedicationRequest; native export undocumented | Product has full CPOE (meds, labs, imaging, procedures). Only medication orders appear in FHIR. Significant gap. |
| Insurance / coverage | ❌ Not covered | No insurance resources in FHIR; native export undocumented | Product stores patient insurance/enrollment data. No evidence in documented export. |
| Claims / billing | ❌ Not covered | No billing resources in FHIR; native export undocumented | Product has billing module. No evidence in documented export. Significant gap. |
| Payments | ❌ Not covered | No payment resources in FHIR; native export undocumented | Product likely handles payment processing. No evidence in documented export. |
| Consents / directives | ❌ Not covered | No consent resources in FHIR; native export undocumented | Product has electronic consent (iPad/PC signature). Not in documented export. |
| Patient communications | ❌ Not covered | No communication resources in FHIR; native export undocumented | N/A — no strong evidence of patient portal/messaging capabilities in US deployment |
| Specialty-specific (behavioral health) | ❌ Not covered | No behavioral health extensions in FHIR; native export undocumented | US deployment is at psychiatric hospitals (Aurora). FHIR API has zero behavioral health-specific content. **Major gap.** |

**Key finding**: Every domain is rated at best "Partial" because the only documented export mechanism is the FHIR API, which provides only the US Core clinical summary. The native CSV/Oracle DMP export *may* cover additional domains but is completely undocumented, so coverage cannot be assessed. The behavioral health gap is particularly notable given the US deployment at 14 psychiatric hospitals.

## 6. Documentation Quality

**Overall quality: Very poor.**

- **Data dictionary**: None. Zero tables, columns, or fields are defined for the native CSV/Oracle DMP export.
- **Schema**: None for the native export. A FHIR CapabilityStatement exists but documents the (g)(10) API, not the (b)(10) export.
- **Field descriptions**: None for native export. FHIR profiles provide standard US Core field semantics.
- **Value sets / code systems**: None for native export. FHIR uses standard US Core terminologies.
- **Relationships / foreign keys**: Not documented.
- **Sample data**: None.
- **Export instructions**: None. No screenshots, no step-by-step workflow, no description of how a user initiates an export.
- **Machine-readable artifacts**: The FHIR CapabilityStatement is machine-readable but documents the API, not the (b)(10) export.

**Could a developer build an import?** Not from this documentation. A developer would know the export produces CSV files and Oracle DMP files but would have no idea what columns the CSVs contain, how files are named, how tables relate, or how to interpret any of the data. The Oracle DMP format is a proprietary binary that requires Oracle database tools — a significant portability barrier.

The entire (b)(10) documentation is approximately **150 words** on a single page. Created September 30, 2023, in Microsoft Word 2013, by Eunsol Lee.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The (b)(10) documentation is a single-page PDF that names two export formats (CSV and Oracle DMP) but provides no data dictionary, no schema, no field definitions, no sample data, and no user instructions. The FHIR API documentation linked from the PDF is a (g)(10) implementation that covers only the US Core clinical summary subset.

While the native CSV/Oracle DMP export could theoretically be comprehensive (an Oracle DMP could contain the entire database), the documentation is so thin that the export's content and usability cannot be assessed. A stub classification is warranted because the documentation fails to demonstrate that the export covers "all electronic health information."

### Key Findings

1. **The (b)(10) documentation is ~150 words with zero data content specification.** The single-page PDF (`b.10_EHI_Export.pdf`, created 2023-09-30) names CSV and Oracle DMP as export formats but provides no data dictionary, no table listing, no field definitions, no schema, and no sample data.

2. **The FHIR API is explicitly conflated with (b)(10).** The PDF's "API documentation" section links directly to the (g)(10) FHIR portal (`portal.ezcaretech.com:30112`). The FHIR server is named "ezfhirstation-us-core-usa-aurora" and implements exactly the standard US Core profile set (26 resource types, 30 profiles) with no vendor extensions.

3. **Behavioral health data — the core US use case — is absent from documented exports.** BESTCare's US deployment is at Aurora Behavioral Healthcare's 14 psychiatric hospitals. The FHIR API contains zero behavioral health-specific content (no psychiatric assessments, no behavioral health forms, no PHQ-9/GAD-7 structured data beyond what's in US Core). The native export is undocumented.

4. **Oracle DMP format raises portability concerns.** The proprietary binary format requires Oracle database tools to import. Combined with zero schema documentation, a recipient would need to reverse-engineer the entire data model.

5. **Real-world testing confirms the export mechanism exists and functions** (128 single-patient exports, 98.4% success rate, 3.5-min average in the 2025 RWT report) but provides no detail on what data elements were included.

### Summary Stats

    Classification:  Minimal/stub
    Export format:   CSV, Oracle DMP (native); FHIR R4 NDJSON (API)
    Model type:      Undocumented native + standard projection (FHIR US Core)
    Entities:        0 (native export); 26 resource types (FHIR API)
    Fields:          0 (native export); ~52 search parameters (FHIR API)
    Descriptions:    N/A (no data dictionary)
    Sample data:     No
    Bulk export:     Yes (FHIR $export); unclear for native CSV/DMP
    Domains covered: 0 of 15 confirmed; up to 12 of 15 partial via FHIR (clinical only)

### Bottom Line

ezCaretech's (b)(10) documentation is among the thinnest possible — a single page naming two file formats with no content specification whatsoever. A patient or provider receiving this export would get CSV files and/or an Oracle binary dump with no way to interpret what the data means. The most significant gap is the complete absence of behavioral health documentation from the export of a system deployed at 14 US psychiatric hospitals. The FHIR API, while functional, is a standard US Core implementation that covers perhaps 20% of what a full hospital information system stores.
