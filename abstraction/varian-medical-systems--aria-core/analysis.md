# EHI Export Analysis: Varian Medical Systems

**Product**: ARIA CORE v18.3
**Analysis date**: 2026-02-16
**CHPL IDs**: 11719 (15.04.04.2496.ARIA.18.08.1.251126)

## 1. Product Context

ARIA CORE is an oncology-specific electronic health record (EHR) and information system developed by Varian Medical Systems (now part of Siemens Healthineers). It is the leading best-of-breed oncology information system in the U.S., used by approximately 369 organizations including major academic medical centers and health systems. ARIA CORE is not a general-purpose EHR — it manages radiation oncology, medical oncology, and surgical oncology workflows, and is designed to integrate with a hospital's enterprise EHR (e.g., Epic, Cerner) for general clinical data.

**Data domains ARIA CORE stores** (relevant to export completeness):

- **Clinical documentation**: Consultation reports, weekly treatment check notes, treatment summaries, review of systems, physical exams, e-signatures
- **Radiation therapy management**: RT prescriptions, treatment plans, dose distributions, beam parameters, daily treatment fraction logs, on-treatment image review (MV, kV, CBCT, CT, MR, PET)
- **Medical oncology / systemic therapy**: Chemotherapy orders with 300+ disease-specific regimens, drug interaction checking, medication administration records
- **Cancer staging**: Automated AJCC staging, disease response tracking
- **Lab results and vital signs**: With trend graphing
- **Toxicity/adverse event records**: Using oncology-standard grading scales
- **Medical images**: DICOM images from multiple modalities
- **Billing/charge data**: RVU-based charge capture, technical/professional charge splits, charge export to billing systems
- **Scheduling**: Patient, staff, and resource scheduling
- **Patient demographics, allergies, medications, problem lists**
- **QA data**: Quality assurance reports, chart checks, treatment plan verification

The core value proposition of ARIA is its oncology-specific data — radiation therapy plans, treatment delivery records, chemotherapy regimen management, cancer staging, and DICOM imaging. A genuine (b)(10) export should include these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/fhir-api-documentation.html` (678 KB) | Full HTML of the Varian DynamicFHIR portal documenting the FHIR R4 (g)(10) API. Contains USCDI-to-FHIR resource mapping table (29 mappings across 87 rows), bulk export instructions, OAuth 2.0 flows, and example FHIR JSON responses. **This is (g)(10) documentation, not (b)(10).** | Most informative — but only documents the FHIR API, not the EHI export |
| `downloads/fhir-capability-statement.json` (25 KB) | FHIR R4 CapabilityStatement listing 27 resource types with search parameters. Standard US Core resources only. | Confirms API scope is standard USCDI |
| `downloads/fhir-smart-configuration.json` (9 KB) | SMART on FHIR configuration listing 233 OAuth scopes across 33 resource types. | Confirms standard SMART capabilities |
| `downloads/ARIACOREv16.1_18.1_18.2_ONC_Certification.pdf` (91 KB, 2 pages) | ONC certification certificate. Lists certified criteria including (b)(10). Notes "Dynamic Health IT" as additional software. | Confirms certification; no EHI export detail |
| `downloads/ARIA_Interoperability_Brochure_RAD10787_Nov2020.pdf` (1.6 MB, 5 pages) | Marketing brochure about ARIA + Epic HL7 integration via Varian Professional Services. | Not relevant to EHI export |
| `downloads/chpl-b10-details.png` (208 KB) | Screenshot of CHPL listing's (b)(10) criteria. Shows: Relied Upon Software = Winzip, Conformance Method = Attestation, Export Documentation = https://varian.com/aria/ehi (dead URL). | Critical metadata about the (b)(10) certification |
| `downloads/fhir-api-documentation-fullpage.png` (15 MB) | Full-page screenshot of the FHIR API documentation. | Visual confirmation of HTML content |

**No (b)(10)-specific documentation was found.** The registered EHI documentation URL (`https://varian.com/aria/ehi`) redirects to `https://cancercare.siemens-healthineers.com/aria/ehi`, which returns HTTP 404. I verified this directly — the URL is still dead as of this analysis.

## 3. Export Mechanics

**Format(s)**: Unknown. No (b)(10) export documentation exists to describe the format. The only documented export mechanism is FHIR Bulk Data (NDJSON) via the (g)(10) API. The CHPL listing notes "Winzip" as relied-upon software for (b)(10), suggesting a ZIP-based file archive, but no documentation describes what it contains.

**Mechanism**: Unknown for (b)(10). The FHIR API supports standard Bulk Data Access operations (`Patient/$export`, `Group/[id]/$export`) via the DynamicFHIR third-party platform.

**Single-patient vs bulk**: The FHIR API supports both individual and group/bulk export, but this is (g)(10), not (b)(10).

**Access constraints**: Unknown. No documentation describes how to initiate or receive a (b)(10) EHI export.

**Critical architectural detail**: The FHIR API documentation explicitly states: *"Varian FHIR API assumes the use of a cumulative C-CDA with patient data. For filtering C-CDA data by section, it will use the latest cumulative C-CDA document (by the document EffectiveDateTime) per patient."* This means the FHIR API is a **C-CDA pass-through** — it does not query ARIA's native database. It consumes C-CDA documents and re-exposes them as FHIR resources. This is significant because C-CDA is inherently USCDI-scoped and cannot represent radiation therapy physics data, DICOM images, or other oncology-specific content.

## 4. Export Content: What's In It

**There is no (b)(10) EHI export documentation to analyze.** The only available documentation describes the FHIR (g)(10) API.

### What the FHIR (g)(10) API provides

The CapabilityStatement lists 27 FHIR R4 resource types, all standard US Core:

| FHIR Resource | USCDI Category | Search Params | Interactions |
|---|---|---|---|
| Patient | Patient Demographics | 8 | read, search |
| Condition | Problem List, Health Concerns | 4 | read, search |
| Procedure | Procedures | 2 | read, search |
| Observation | Smoking Status, Vital Signs, Lab Results | 4 | read, search |
| DiagnosticReport | Laboratory Tests | 4 | read, search |
| MedicationRequest | Medications | 5 | read, search |
| MedicationDispense | Medications | 3 | read, search |
| AllergyIntolerance | Allergies and Intolerances | 3 | read, search |
| Immunization | Immunizations | 2 | read, search |
| CarePlan | Assessment and Plan of Treatment | 4 | read, search |
| CareTeam | Care Team Members | 2 | read, search |
| Goal | Goals | 3 | read, search |
| Encounter | Encounter | 5 | read, search |
| DocumentReference | Clinical Notes (8 types) | 7 | read, search |
| Device | Implantable Devices | 2 | read, search |
| Coverage | Insurance | 1 | read, search |
| ServiceRequest | (not mapped in USCDI table) | 6 | read |
| Specimen | (not mapped in USCDI table) | 2 | read, search |
| ClinicalImpression | (not mapped in USCDI table) | 2 | read, search |
| Location | Location | 2 | read, search |
| Organization | Organization | 7 | read, search |
| Practitioner | Practitioner | 2 | read, search |
| PractitionerRole | PractitionerRole | 2 | read, search |
| RelatedPerson | (supporting) | 2 | read, search |
| Provenance | (supporting) | 0 | read, search |
| Binary | (supporting) | 2 | read, search |
| Group | (bulk export) | 0 | — |

This is a standard US Core FHIR surface. There are **no vendor extensions**, no oncology-specific resource profiles, no custom FHIR resources mapping to ARIA's native data model. The FHIR API is provided by a third party (Dynamic Health IT), not built by Varian against ARIA's database.

### Vendor's own content organization

There is no vendor-specific data dictionary or content organization. The only structure is the USCDI-to-FHIR mapping table from the DynamicFHIR documentation, which maps 29 USCDI data elements to standard FHIR resources. No field-level documentation exists beyond the standard FHIR resource definitions.

### What is NOT in the FHIR API (and critical for an oncology system)

The FHIR API documentation contains zero references to:
- Radiation therapy prescriptions, plans, dose distributions, beam parameters
- Treatment delivery records (fraction logs)
- Cancer staging (AJCC)
- Chemotherapy-specific regimen details (beyond generic MedicationRequest)
- Toxicity/adverse event grading
- Disease response tracking
- QA reports / chart checks
- DICOM images
- Charge/billing data (beyond Coverage)
- Patient-reported outcomes

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides **no (b)(10)-specific documentation**. The only available documentation is the FHIR (g)(10) API from DynamicFHIR, which covers standard USCDI data classes:
- Patient demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, encounters, clinical notes, goals, care plans, care team, implantable devices, and coverage.
- All 29 USCDI mappings point to standard US Core FHIR profiles with no vendor-specific extensions.
- The API is a C-CDA pass-through, meaning it can only expose data that exists in C-CDA documents — it cannot access ARIA's native database.

This represents the absolute minimum clinical exchange surface. For a radiation oncology system like ARIA, whose primary purpose is managing treatment plans, daily treatment delivery, imaging, staging, and chemotherapy regimens, the USCDI surface covers perhaps 10-15% of the clinically significant patient data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient resource via FHIR API (USCDI fields only) | Only standard USCDI demographics; ARIA likely stores oncology-specific registration data |
| Encounters / visits | ⚠️ Partial | Encounter resource via FHIR API | Standard encounters only; radiation treatment sessions not represented |
| Problems / conditions / diagnoses | ⚠️ Partial | Condition resource via FHIR API | Standard problem list; ARIA's cancer staging data (AJCC) not included |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest, MedicationDispense via FHIR API | Generic medication data only; 300+ oncology-specific chemotherapy regimens not mapped |
| Allergies | ✅ Covered | AllergyIntolerance via FHIR API | Standard USCDI coverage |
| Immunizations | ✅ Covered | Immunization via FHIR API | Standard USCDI coverage |
| Vitals | ✅ Covered | Observation via FHIR API | Standard USCDI coverage |
| Lab results | ✅ Covered | Observation, DiagnosticReport via FHIR API | Standard USCDI coverage |
| Imaging / diagnostic reports | ⚠️ Partial | DocumentReference (Radiology Report, Cardiology Report, Pathology Report) | Text reports only; DICOM images (MV, kV, CBCT, CT, MR, PET) not included |
| Procedures | ⚠️ Partial | Procedure via FHIR API | Standard procedures; radiation treatment delivery details not included |
| Clinical notes / documents | ⚠️ Partial | DocumentReference (8 note types) via FHIR API | C-CDA clinical notes only; oncology-specific note templates not documented |
| Care plans / goals | ⚠️ Partial | CarePlan, Goal via FHIR API | Standard care plans; radiation therapy treatment plans not included |
| Orders / referrals | ⚠️ Partial | ServiceRequest via FHIR API (read only) | Limited; chemotherapy orders, RT orders not specifically mapped |
| Insurance / coverage | ⚠️ Partial | Coverage via FHIR API (1 search param) | Minimal — single search parameter, likely basic coverage only |
| Claims / billing | ❌ Not covered | No billing entities | ARIA has RVU-based charge capture; significant gap |
| Payments | ❌ Not covered | No payment entities | N/A if charges exported to separate billing system, but charge data itself is missing |
| Consents / directives | ❌ Not covered | No consent entities | Unknown if ARIA stores consent data |
| Patient communications | ❌ Not covered | No communication entities | Patient portal exists (Noona integration) |
| **Radiation therapy plans** | ❌ Not covered | No RT-specific entities | **Critical gap** — core ARIA data: prescriptions, dose distributions, beam parameters |
| **Treatment delivery records** | ❌ Not covered | No fraction log entities | **Critical gap** — daily treatment delivery logs are primary ARIA data |
| **Cancer staging** | ❌ Not covered | No staging entities | **Critical gap** — ARIA automates AJCC staging |
| **Chemotherapy regimens** | ❌ Not covered | No regimen-specific entities | **Critical gap** — 300+ regimens managed in ARIA |
| **Toxicity / adverse events** | ❌ Not covered | No toxicity entities | **Critical gap** — oncology-standard grading scales |
| **Disease response** | ❌ Not covered | No response entities | **Critical gap** — treatment outcome tracking |
| **QA / chart checks** | N/A | Not EHI (operational) | Physics QA is operational, not patient decision-making |
| **DICOM images** | ❌ Not covered | No image entities | **Significant gap** — treatment verification images are part of patient record |
| **Patient-reported outcomes** | ❌ Not covered | No PRO entities | Noona integration data not in export |

**Summary**: Of ~19 applicable EHI domains, 4 have standard USCDI coverage (allergies, immunizations, vitals, labs), 9 have partial coverage (standard FHIR only, missing oncology-specific depth), and 6+ critical oncology-specific domains are completely absent.

## 6. Documentation Quality

**For (b)(10) EHI export: No documentation exists.** The registered URL is dead (404). No alternative documentation was found on any Varian/Siemens property, via web search, or via the Wayback Machine.

**For the (g)(10) FHIR API** (not the EHI export, but the only documentation available):
- The DynamicFHIR portal provides adequate (g)(10) API documentation: USCDI-to-FHIR mapping table, search parameter syntax, OAuth 2.0 authorization flows, bulk export instructions, and example JSON responses.
- **No field-level data dictionary** — the documentation references standard US Core profiles on HL7.org rather than providing ARIA-specific field mappings.
- **No value sets or code system documentation** beyond US Core defaults.
- **No product-specific extensions** — no evidence of custom FHIR profiles for oncology data.
- **C-CDA intermediary architecture** — the API's reliance on C-CDA documents as an intermediary means it structurally cannot access data that doesn't exist in C-CDA.

A developer could implement a standard FHIR client against this API but would get only USCDI clinical summary data — no oncology-specific information.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The registered (b)(10) EHI documentation URL returns 404. No alternative documentation was found. The only available documentation is the FHIR (g)(10) API, which is explicitly USCDI-scoped and provided by a third-party (Dynamic Health IT). For a radiation oncology system whose entire purpose is managing treatment plans, delivery records, imaging, staging, and chemotherapy, the USCDI surface misses the overwhelming majority of clinically significant patient data. The Winzip reference in the CHPL listing hints that some kind of file-based export may exist, but with no documentation, it's impossible to assess its content.

**Axis 2 — Export approach: Repackaged existing export**

Every indicator points to the (g)(10) FHIR Bulk Data API being presented as the (b)(10) mechanism:
1. The FHIR API documentation explicitly states data is "limited by the data defined by the USCDI."
2. The API operates as a C-CDA pass-through, not a native database export.
3. Dynamic Health IT (a third-party FHIR platform) provides the API — Varian didn't build an ARIA-specific export.
4. There are zero vendor extensions, zero oncology-specific resource profiles, and zero mappings to ARIA's native data model.
5. The conformance method is "Attestation" (not tested), and the documentation URL is dead.

The Winzip reference creates some ambiguity — there may be a separate file-based export mechanism — but without any documentation, this cannot be verified. The available evidence strongly suggests the vendor attested to (b)(10) compliance without building or documenting a purpose-built EHI export.

### Key Findings

1. **Dead documentation URL**: The registered (b)(10) EHI export documentation URL (`https://varian.com/aria/ehi`) returns 404. It has never been captured by the Wayback Machine. No alternative location was found. This is the most fundamental finding — a certified product with no accessible export documentation.

2. **C-CDA pass-through architecture**: The FHIR API explicitly processes C-CDA documents, not ARIA's native database. This structurally limits the API to USCDI-scope data and makes it incapable of exporting oncology-specific content (RT plans, fraction logs, DICOM images, staging, regimens).

3. **Third-party FHIR platform**: The API is provided by Dynamic Health IT, not built by Varian. The 27 FHIR resource types are standard US Core with zero vendor extensions — no evidence of any ARIA-specific mapping.

4. **Critical oncology data gap**: ARIA's core data — radiation therapy plans, treatment delivery records, cancer staging, chemotherapy regimen management, toxicity grading, disease response tracking, and DICOM images — is completely absent from the documented export surface.

5. **Attestation-only certification**: The (b)(10) criteria was certified via attestation, not tested by an ONC-ACB testing lab. Combined with the dead URL and lack of documentation, this suggests minimal vendor engagement with the (b)(10) requirement.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   FHIR R4 NDJSON (g)(10) API; possibly ZIP files (undocumented)
    Entities:        27 FHIR resource types (standard US Core, no oncology-specific)
    Fields:          N/A (no field-level data dictionary)
    Descriptions:    N/A
    Sample data:     No (example FHIR responses are generic US Core examples, not ARIA-specific)
    Bulk export:     Yes (FHIR Bulk Data via g(10), but not b(10)-specific)
    Domains covered: 4 of 19 applicable domains fully; 9 partial (USCDI only); 6+ oncology-specific domains missing

### Bottom Line

A patient treated with ARIA CORE would receive, at best, a standard USCDI clinical summary through the FHIR API — basic demographics, problem list, medications, allergies, labs, and vitals. The core oncology record — radiation therapy plans, daily treatment delivery logs, cancer staging, chemotherapy regimen details, toxicity assessments, treatment response data, and diagnostic images — would be entirely missing. For a product whose primary purpose is managing radiation and medical oncology workflows, this represents a near-total failure to export the designated record set. The dead documentation URL and attestation-only certification suggest the vendor has not meaningfully engaged with the (b)(10) requirement.
