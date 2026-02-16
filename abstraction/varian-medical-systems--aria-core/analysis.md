# EHI Export Analysis: Varian Medical Systems

**Product**: ARIA CORE v18.3
**Analysis date**: 2026-02-16
**CHPL IDs**: 11719 (15.04.04.2496.ARIA.18.08.1.251126)

## 1. Product Context

ARIA CORE is Varian Medical Systems' (now Siemens Healthineers) flagship **oncology information system** — a specialty EHR purpose-built for radiation oncology, medical oncology, and surgical oncology. It is the leading best-of-breed oncology information system in the US market, used by approximately 369 organizations including major academic medical centers and health systems.

ARIA CORE manages extensive oncology-specific data that would be part of a patient's designated record set:

- **Patient demographics and registration**
- **Clinical notes** — consultation reports, weekly treatment checks, treatment summaries, H&P, progress notes
- **Radiation therapy data** — treatment prescriptions, treatment plans, beam parameters, dose distributions, daily fraction delivery logs, on-treatment images (MV, kV, CBCT, CT, MR, PET)
- **Medical oncology / chemotherapy** — drug orders, 300+ disease-specific regimens, medication administration records, drug interaction data
- **Cancer staging** — automated AJCC staging
- **Lab results and vital signs** — with trend tracking
- **Medications, allergies, immunizations**
- **Problem lists and diagnoses**
- **Toxicity/adverse event records** — using oncology-standard grading scales
- **Disease response tracking** — treatment outcome documentation
- **Billing/charge data** — RVU-based charge capture, technical/professional charge splits
- **QA data** — physics quality assurance reports, chart checks
- **Patient-reported outcomes** — via Noona integration
- **Medical images** — DICOM-compliant oncology imaging

ARIA is designed to coexist with hospital enterprise EHRs (like Epic or Cerner), handling oncology-specific workflows and data while the enterprise system handles general clinical data. This makes the specialty data in ARIA — particularly radiation therapy plans, fraction logs, and physics data — uniquely important since it may not exist anywhere else.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `fhir-api-documentation.html` (678 KB) | Full HTML of Varian's FHIR R4 API documentation from DynamicFHIR portal. Contains USCDI-to-FHIR mapping table (29 categories → 18 FHIR resources), bulk export instructions, OAuth 2.0 flows, example responses. This is (g)(10) documentation, NOT (b)(10). | **Most informative** — but for the wrong criterion |
| `fhir-capability-statement.json` (25 KB) | FHIR R4 CapabilityStatement listing 27 resource types with search parameters and interactions. Machine-readable. | Moderately informative |
| `fhir-smart-configuration.json` (9 KB) | SMART on FHIR configuration with 233 scopes across 34 resource types. | Moderately informative |
| `ARIACOREv16.1_18.1_18.2_ONC_Certification.pdf` (91 KB, 2 pages) | ONC Certification certificate showing ARIA CORE v18.3 certified 2025-11-26. Lists Dynamic Health IT as additional software. | Low — confirms certification only |
| `ARIA_Interoperability_Brochure_RAD10787_Nov2020.pdf` (1.6 MB, 5 pages) | Marketing brochure about ARIA + Epic integration via HL7 interfaces. TriHealth case study. No EHI export content. | Not informative for EHI |
| `chpl-b10-details.png` (208 KB) | Screenshot of CHPL listing's (b)(10) details showing Relied Upon Software = Winzip, Conformance Method = Attestation, Export Documentation = `https://varian.com/aria/ehi` (dead URL). | **Critical evidence** — confirms documentation is missing |
| `fhir-api-documentation-fullpage.png` (15 MB) | Full-page screenshot of FHIR API documentation. Confirms HTML content. | Redundant with HTML |

**No artifact in the downloads folder constitutes (b)(10) EHI export documentation.** The FHIR API documentation is explicitly (g)(10) USCDI-scoped. No data dictionary, no export schema, no sample export data, and no native database model documentation was found.

## 3. Export Mechanics

**No (b)(10) EHI export mechanism is documented.** Based on the available evidence:

- **Format**: Unknown. The CHPL listing's "Relied Upon Software" is Winzip, suggesting the export produces a compressed archive — but the contents and format of that archive are undocumented.
- **Mechanism**: Unknown. No UI instructions, API endpoints, or vendor-assisted process descriptions were found.
- **Single-patient vs bulk**: Unknown.
- **Access constraints**: Unknown.
- **Conformance method**: **Attestation** — meaning the vendor self-attested to (b)(10) compliance without testing by an ONC-ACB testing lab.

The only documented export capability is the **FHIR Bulk Data Access API** (for (g)(10)), which:
- Produces NDJSON bundles of standard FHIR R4 US Core resources
- Is scoped to USCDI data only (explicitly stated: "Available data via the API interface is limited by the data defined by the USCDI")
- Operates as a **C-CDA pass-through**: "Varian FHIR API assumes the use of a cumulative C-CDA with patient data"
- Supports `Patient/$export` and `Group/[id]/$export` endpoints
- Uses backend service authorization (client credentials with JWT)

## 4. Export Content: What's In It

### What can be determined

There is **no (b)(10) data dictionary or export documentation** to analyze. The registered EHI documentation URL (`https://varian.com/aria/ehi`) redirects to `https://cancercare.siemens-healthineers.com/aria/ehi`, which returns HTTP 404. This was verified directly during this analysis. No alternative URL or documentation location was found through:
- Probing 8+ alternative URL paths on `cancercare.siemens-healthineers.com`
- Checking the vendor's interoperability page
- Examining the CHPL listing

### FHIR API coverage (g)(10) only — not (b)(10)

The only export-related documentation available describes the FHIR R4 API, which exposes:

**CapabilityStatement: 27 resource types, 86 total search parameters**

| FHIR Resource | Search Params | Interactions |
|---|---|---|
| AllergyIntolerance | 3 | read, search-type |
| Binary | 2 | read, search-type |
| CarePlan | 4 | read, search-type |
| CareTeam | 2 | read, search-type |
| ClinicalImpression | 2 | search-type, read |
| Condition | 4 | search-type, read |
| Coverage | 1 | search-type, read |
| Device | 2 | read, search-type |
| DiagnosticReport | 4 | read, search-type |
| DocumentReference | 7 | read, search-type |
| Encounter | 5 | search-type, read |
| Goal | 3 | read, search-type |
| Group | 0 | (bulk export grouping) |
| Immunization | 2 | search-type, read |
| Location | 2 | search-type, read |
| MedicationDispense | 3 | search-type, read |
| MedicationRequest | 5 | search-type, read |
| Observation | 4 | search-type, read |
| Organization | 7 | search-type, read |
| Patient | 8 | search-type, read |
| Practitioner | 2 | search-type, read |
| PractitionerRole | 2 | search-type, read |
| Procedure | 2 | search-type, read |
| Provenance | 0 | search-type, read |
| RelatedPerson | 2 | search-type, read |
| ServiceRequest | 6 | read |
| Specimen | 2 | search-type, read |

**USCDI mapping: 29 USCDI categories → 18 FHIR resource types**

The mapping covers standard USCDI clinical data classes (Patient Demographics, Allergies, Conditions, Medications, Labs, Vitals, Immunizations, Procedures, Encounters, Goals, Care Plans, Clinical Notes, Devices, Smoking Status) plus clinical note subtypes (Consultation Note, Discharge Summary, H&P, Progress Note, Procedure Note, Pathology Report, Radiology Report, Cardiology Report).

**Critical limitation**: The FHIR API documentation explicitly states the API reads from C-CDA documents, not the native ARIA database. This means even the USCDI data exposed via the API is filtered through C-CDA, and any oncology-specific data that doesn't fit in a standard C-CDA section would be lost.

### Vendor's own content organization

Not applicable — no vendor-provided data dictionary or export content documentation exists.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**The vendor has not documented any (b)(10) EHI export content.** The EHI documentation URL is dead (404), the conformance method is attestation (not tested), and no alternative documentation was found.

The only documented data access is the FHIR R4 API, which covers standard USCDI clinical summary data — the same content any certified EHR would expose via (g)(10). This API is explicitly not intended for (b)(10) and covers only a small fraction of the data ARIA stores about patients.

The FHIR API is provided by **Dynamic Health IT** (a third-party platform listed in the certification as additional software), not by Varian/Siemens directly. It operates as a C-CDA intermediary layer, not a native database query interface.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource (via g(10) API only; no b(10) documentation) | FHIR covers basic demographics; ARIA stores oncology-specific registration data that is undocumented |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource | Standard encounters only; oncology treatment sessions (radiation fractions) not mapped |
| Problems / conditions / diagnoses | ⚠️ Partial | FHIR Condition resource | Standard problem list; ARIA's automated AJCC cancer staging data not mapped |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest, MedicationDispense | Standard medications; ARIA manages 300+ oncology-specific chemotherapy regimens — unclear if these are fully represented |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance | Basic allergy data via FHIR; no b(10) documentation |
| Immunizations | ⚠️ Partial | FHIR Immunization | Basic immunization data via FHIR; no b(10) documentation |
| Vitals | ⚠️ Partial | FHIR Observation | Standard vitals via FHIR; no b(10) documentation |
| Lab results | ⚠️ Partial | FHIR DiagnosticReport, Observation | Standard labs via FHIR; ARIA's oncology-specific lab trending data not documented |
| Imaging / diagnostic reports | ❌ Not covered | FHIR DiagnosticReport covers text reports only | ARIA stores extensive DICOM images (MV, kV, CBCT, CT, MR, PET) — none documented in any export |
| Procedures | ⚠️ Partial | FHIR Procedure | Standard procedures; radiation therapy procedures and treatment delivery not mapped |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference (7 note types mapped) | C-CDA clinical notes covered; oncology-specific note types and structured templates unclear |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, Goal | Standard care plans; oncology treatment plans with beam parameters, dose distributions not mapped |
| Orders / referrals | ⚠️ Partial | FHIR ServiceRequest | Standard orders; radiation therapy orders and chemotherapy protocol orders not specifically documented |
| Insurance / coverage | ⚠️ Partial | FHIR Coverage resource (1 search param) | Minimal coverage data; ARIA stores insurance information for billing |
| Claims / billing | ❌ Not covered | No billing entities in any documentation | ARIA has charge capture, RVU tracking, tech/professional charge splits — completely absent |
| Payments | ❌ Not covered | No payment entities | ARIA exports charges to billing systems; payment data not documented |
| Consents / directives | ❌ Not covered | No consent resources documented | No evidence |
| Patient communications | ❌ Not covered | No communication resources | Noona patient engagement platform data not included |
| **Radiation therapy** (specialty) | ❌ Not covered | No radiation therapy data in any documentation | **Critical gap**: ARIA's primary purpose is radiation therapy management. RT prescriptions, treatment plans, beam parameters, dose distributions, daily fraction logs, image-guided therapy data — none documented in any export |
| **Cancer staging** (specialty) | ❌ Not covered | No staging data documented | ARIA automates AJCC cancer staging — not in any export |
| **Toxicity/adverse events** (specialty) | ❌ Not covered | No toxicity data documented | ARIA tracks treatment toxicity with oncology grading scales — not documented |
| **Disease response** (specialty) | ❌ Not covered | No response data documented | Treatment outcome tracking — not documented |

**Summary**: Of 22 applicable domains, 0 are fully covered by documented (b)(10) export, 12 have partial evidence (via the g(10) FHIR API only), and 10 have no coverage at all. The uncovered domains include the most important specialty data that constitutes ARIA's core value proposition: radiation therapy management, cancer staging, toxicity tracking, and oncology billing.

## 6. Documentation Quality

**There is no (b)(10) EHI export documentation to assess.** The registered URL returns 404. The conformance method is attestation.

The FHIR API documentation (for g(10), not b(10)) is reasonably well-structured:
- It includes USCDI-to-FHIR resource mappings with search parameters
- It provides example JSON responses for each resource type
- It documents OAuth 2.0/SMART authorization flows
- It includes a machine-readable CapabilityStatement
- A developer could implement a FHIR client from this documentation

However, even the FHIR API documentation lacks:
- Field-level data dictionaries (no documentation of what fields each resource contains beyond the FHIR standard)
- Value set definitions (relies on US Core defaults)
- Documentation of any vendor extensions or oncology-specific data elements
- Any relationship to the native ARIA data model

**A developer could not build an EHI import from the available documentation** because no (b)(10) export format, schema, or content specification exists.

## 7. Overall Assessment

### Classification

**Minimal/stub** — The registered EHI documentation URL is dead (404), no alternative documentation exists, and the only export documentation available is a FHIR API explicitly scoped to USCDI/(g)(10). For a radiation oncology information system where the vast majority of clinically significant data (treatment plans, fraction logs, physics data, cancer staging, chemotherapy protocols, oncology imaging) falls outside USCDI scope, this represents a near-total absence of (b)(10) compliance documentation.

### Key Findings

1. **Dead documentation URL**: The registered EHI export documentation URL (`https://varian.com/aria/ehi`) returns HTTP 404 after redirecting to the Siemens Healthineers Cancer Care domain. No alternative documentation location was found. (Verified: `chpl-b10-details.png`, direct HTTP request)

2. **Attestation-only conformance**: The (b)(10) certification was achieved through self-attestation, not ONC-ACB testing. Combined with the dead URL, this raises serious questions about whether a functional (b)(10) export exists. (Source: CHPL listing screenshot)

3. **FHIR API is a C-CDA pass-through, not a native data export**: The FHIR documentation states "Varian FHIR API assumes the use of a cumulative C-CDA with patient data" — meaning the API re-projects C-CDA content into FHIR resources rather than querying the native ARIA database. This inherently limits the data to what fits in a C-CDA clinical summary. (Source: `fhir-api-documentation.html`)

4. **Core oncology data has no export path**: ARIA's primary value — radiation therapy plans, daily treatment delivery logs, beam parameters, dose distributions, DICOM imaging, AJCC cancer staging, treatment toxicity grading, disease response tracking — has no documented export mechanism whatsoever. These are the data elements most critical to a patient's designated record set in an oncology context.

5. **Winzip dependency hints at undocumented export**: The CHPL listing mentions Winzip as relied-upon software, suggesting a zip-based export mechanism may exist somewhere in the product. However, without documentation of what that archive contains, its existence cannot be confirmed or evaluated.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (Winzip listed as relied-upon software; FHIR NDJSON for g(10) only)
Model type:      Unknown (no b(10) documentation; g(10) is standard FHIR projection via C-CDA)
Entities:        N/A (no data dictionary)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Unclear (FHIR Bulk Data exists for g(10); b(10) mechanism undocumented)
Domains covered: 0 of 22 confirmed via b(10) documentation (12 partial via g(10) FHIR API only)
```

### Bottom Line

Varian Medical Systems has **no publicly accessible (b)(10) EHI export documentation** for ARIA CORE. The registered URL is dead, the conformance was achieved through attestation alone, and the only documented export is a FHIR API explicitly limited to USCDI scope. For a radiation oncology system where the most critical patient data — treatment plans, fraction delivery logs, physics QA, cancer staging, chemotherapy protocols, and DICOM imaging — falls entirely outside USCDI, this represents a fundamental failure to meet the spirit of the (b)(10) requirement. A patient or provider requesting their complete oncology record from ARIA would have no documented mechanism to obtain it.
