# EHI Export Analysis: BroadStreet Health LLC

**Product**: BroadStreet v1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3161.BRDS.01.00.1.231222

## 1. Product Context

BroadStreet is an ONC-certified EHR developed by BroadStreet Health LLC (affiliated with Arsana Health / WashSense Inc.) for **post-acute and community-based care** — specifically skilled nursing facilities (SNFs), assisted living communities, residential care, and home-based settings. It is described as a "mobile physician platform" for providers caring for elderly and psychosocially vulnerable individuals.

**Certified clinical capabilities** include: CPOE for medications, lab orders, and diagnostic imaging; demographics; family health history; implantable device tracking; social/psychological/behavioral data (SDOH); transitions of care (C-CDA); clinical information reconciliation; care plans; patient-generated health data; clinical quality measures (depression screening, BMI, tobacco, falls, dementia cognitive assessment, kidney health); FHIR API access (g)(10); and direct secure messaging.

**What data should the export cover**: Given the post-acute care focus, the product should store patient demographics, encounters/visits, problem lists, medications (including administration records/eMAR for facility-based care), allergies, immunizations, vitals, lab results, clinical notes, care plans, nursing assessments (potentially MDS for SNFs), imaging orders, procedures, device records, social history, and advance directives. The product research indicates billing is likely handled externally — no billing module was identified. The company is very early-stage (1–10 employees, minimal market presence), so the breadth of stored data may be narrower than a mature post-acute EHR.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page-rendered.html` (9,698 bytes) | **Primary artifact.** Rendered HTML of the EHI Export documentation page from `broadstreetcare.com/docs/ehi-export`. Describes three export formats: CDA 2.1, FHIR R4, and BroadStreet Notes (HTML). | **Most informative** — sole source of (b)(10) documentation |
| `downloads/ehi-export-page.png` (674 KB) | Full-page screenshot of the EHI Export page, confirming content matches the rendered HTML. | Corroborative |
| `downloads/ehi-export-page-raw.html` (4,194 bytes) | Server-rendered HTML shell (SvelteKit SPA). Contains only a spinner — no content without JavaScript. | Not informative (confirms SPA architecture) |
| `downloads/fhir-resources-page.png` (127 KB) | Screenshot of the FHIR Resources index page at `/docs/fhir/resources`, listing 12 clinical resources and 11 reference resources for the (g)(10) API. | **Informative** — confirms FHIR export aligns with (g)(10) API |
| `downloads/BST-2025-RWT-Plan.pdf` (184 KB, 15 pages) | 2025 Real World Testing Plan. Contains Test Case 4 for (b)(10) describing testing methodology at assisted living facilities. | Moderately informative — confirms export exists but adds no content detail |

**No data dictionary, schema, sample data, or machine-readable artifacts were provided.** The entire (b)(10) documentation consists of a single HTML page with generic standard descriptions plus 22 fields for the Notes format.

## 3. Export Mechanics

- **Formats**: Three formats claimed: CDA 2.1, FHIR R4, and BroadStreet Notes (HTML)
- **Mechanism**: Not documented. The RWT Plan mentions "export requests" tracked via logs and references both individual and population-level exports, but no UI screenshots, API endpoints, or step-by-step instructions are provided for the (b)(10) export.
- **Single-patient vs bulk**: The RWT Plan Test Case 4 states "Test cases will simulate both individual and population-level EHI exports," indicating both are supported.
- **Access constraints**: Not documented. No mention of fees, authorization requirements, or turnaround time.

## 4. Export Content: What's In It

The EHI export documentation page provides three categories of content, but almost no product-specific detail:

### CDA 2.1
The page provides a generic description of the CDA 2.1 standard (header/body structure, human-readability, machine-processability). It states "Our system exports patient data in the form of CDA documents that adhere to the CDA 2.1 standard" and links to the external HL7 CDA specification. **No BroadStreet-specific CDA template, section list, or field inventory is provided.** It is impossible to determine which CDA sections are populated or how complete the documents are.

### FHIR R4
The page lists 15 FHIR resource types with one-sentence descriptions:

| FHIR Resource | Description (from vendor) |
|---|---|
| Patient | Information about an individual receiving care |
| Observation | Measurements or simple assertions made about a patient |
| Medication | Details about a medication that can be prescribed |
| Practitioner | Individual with a formal responsibility in the healthcare process |
| Encounter | Interaction between a patient and the healthcare provider |
| Procedure | Clinical activity or intervention performed on or for a patient |
| Condition | Clinical condition, problem, or diagnosis about a patient |
| Immunization | Record of an immunization given to a patient |
| AllergyIntolerance | Adverse reaction or allergy a patient has to substances |
| MedicationRequest | Request for a medication to be administered or dispensed |
| CarePlan | Plan or protocol established to manage health concerns |
| Device | Medical device used on or for a patient |
| DiagnosticReport | Findings and interpretation of diagnostic tests |
| Appointment | Scheduled interaction between patient and provider |
| Organization | Organization involved in the care of a patient |

The separate FHIR API documentation at `/docs/fhir/resources` (visible in `fhir-resources-page.png`) lists 23 resources total (12 clinical + 11 reference), all using US Core STU 5.0.1 profiles. This is clearly the (g)(10) standardized API. The EHI export page's FHIR resource list is a subset of this (g)(10) list, with no vendor extensions, custom profiles, or additional resources documented. **No field-level documentation is provided for any FHIR resource.**

### BroadStreet Notes (HTML)
This is the only product-specific documentation. It describes 22 fields organized into 10 sections:

| Field | Section | Description |
|---|---|---|
| Physician Name | Physician Information | The name of the physician who provided the service |
| Sent by | Physician Information | The individual who sent the documentation |
| Date | Physician Information | The timestamp when the documentation was sent |
| Date of Service | Visit and Patient Details | The date when the service was provided |
| Type | Visit and Patient Details | The type of service provided (e.g., H&P) |
| Patient Name | Visit and Patient Details | The full name of the patient |
| Date of Birth | Visit and Patient Details | The birthdate of the patient |
| Gender | Visit and Patient Details | The gender of the patient |
| Advance Directive Code | Visit and Patient Details | Any code related to advance directives |
| Allergies | Medical Concerns | Any known allergies |
| Primary Concern | Medical Concerns | The main reason for the patient's visit |
| Smoking Status | Social History | The patient's smoking habits |
| Blood Pressure | Vital Examination | Systolic/Diastolic blood pressure measurement |
| Pulse | Vital Examination | Heart rate measured in beats per minute |
| Weight | Vital Examination | Patient's weight |
| Diagnosis Code | Assessment Plan | The ICD code for the diagnosis |
| Assessment | Assessment Plan | The physician's findings and recommendations |
| Next Appointment | Visit Details | Details of the next scheduled appointment |
| Reason for Next Visit | Visit Details | The purpose for the upcoming visit |
| Electronically Signed By | Signature | Confirmation of who signed electronically |
| Treatment Review Content | Treatment Review | Past and ongoing treatments (section described but not itemized) |
| Additional Notes Content | Additional Notes | Additional physician remarks |

No data types, constraints, value sets, or relationships are documented for any field. No sample data is provided.

### Vendor's Own Content Organization

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| CDA 2.1 Document | 2 (Header, Body) | 2 | No | Clinical Document |
| FHIR Patient | 0 | 0 | N/A | FHIR Resource |
| FHIR Observation | 0 | 0 | N/A | FHIR Resource |
| FHIR Medication | 0 | 0 | N/A | FHIR Resource |
| FHIR Practitioner | 0 | 0 | N/A | FHIR Resource |
| FHIR Encounter | 0 | 0 | N/A | FHIR Resource |
| FHIR Procedure | 0 | 0 | N/A | FHIR Resource |
| FHIR Condition | 0 | 0 | N/A | FHIR Resource |
| FHIR Immunization | 0 | 0 | N/A | FHIR Resource |
| FHIR AllergyIntolerance | 0 | 0 | N/A | FHIR Resource |
| FHIR MedicationRequest | 0 | 0 | N/A | FHIR Resource |
| FHIR CarePlan | 0 | 0 | N/A | FHIR Resource |
| FHIR Device | 0 | 0 | N/A | FHIR Resource |
| FHIR DiagnosticReport | 0 | 0 | N/A | FHIR Resource |
| FHIR Appointment | 0 | 0 | N/A | FHIR Resource |
| FHIR Organization | 0 | 0 | N/A | FHIR Resource |
| BroadStreet Notes (HTML) | 22 | 22 | No | Clinical Notes |

**Total: 17 entities, 24 fields documented (22 in Notes + 2 generic CDA). 0 fields with data types.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes three export formats but provides almost no product-specific detail:

1. **CDA 2.1**: Generic standard description. No indication of which CDA sections BroadStreet populates. Likely produces standard C-CDA documents (given (b)(1) Transitions of Care certification), covering basic clinical summary data.

2. **FHIR R4**: Lists 15 standard FHIR resources that map directly to US Core / USCDI data classes. The resource list matches the (g)(10) API. No evidence of any FHIR resources or extensions beyond the standard clinical exchange set. No billing resources (Claim, ExplanationOfBenefit), no specialty resources.

3. **BroadStreet Notes (HTML)**: The most specific section, documenting a 22-field clinical note structure. This is a single-entity export format for physician notes — not a comprehensive data export.

The documentation does not describe how these three formats work together, whether they're exported simultaneously, or whether the combination constitutes the complete (b)(10) export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient (no field detail); Notes has Patient Name, DOB, Gender | Only 3 demographic fields in Notes; FHIR Patient has no documented fields beyond standard US Core |
| Encounters / visits | ⚠️ Partial | FHIR Encounter (no field detail); Notes has Date of Service, Type | Encounter resource listed but no field detail |
| Problems / conditions | ⚠️ Partial | FHIR Condition (no field detail); Notes has Diagnosis Code | Only ICD code in Notes; FHIR Condition undocumented |
| Medications / prescriptions | ⚠️ Partial | FHIR Medication + MedicationRequest (no field detail) | Resource names only; no eMAR documentation despite post-acute focus |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance (no field detail); Notes has Allergies field | Single text field in Notes; FHIR resource undocumented |
| Immunizations | ⚠️ Partial | FHIR Immunization (no field detail) | Resource name only |
| Vitals | ⚠️ Partial | FHIR Observation (no field detail); Notes has BP, Pulse, Weight | 3 vitals in Notes; no SpO2, temp, height, RR, BMI |
| Lab results | ⚠️ Partial | FHIR Observation, DiagnosticReport (no field detail) | Resource names only; certified for lab CPOE but no lab-specific documentation |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport (no field detail) | Certified for imaging CPOE but no detail |
| Procedures | ⚠️ Partial | FHIR Procedure (no field detail) | Resource name only |
| Clinical notes / documents | ✅ Covered | BroadStreet Notes (HTML) with 22 fields | Best-documented domain; still lacks data types and value sets |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan (no field detail) | Resource name only; certified for (b)(11) care plan |
| Orders / referrals | ❌ Not covered | No ServiceRequest or order-related entities in EHI export docs | FHIR API has ServiceRequest but it's not listed on the EHI export page |
| Insurance / coverage | ❌ Not covered | No insurance or coverage entities | Unclear if product stores this data |
| Claims / billing | ❌ Not covered | No billing entities | Product likely doesn't do billing (external) — likely N/A |
| Payments | ❌ Not covered | No payment entities | Likely N/A |
| Consents / directives | ⚠️ Partial | Notes has "Advance Directive Code" field | Single code field, no directive documents |
| Patient communications | ❌ Not covered | No messaging or portal communication entities | Product has patient portal (e)(1) but no comm data in export |
| Family health history | ❌ Not covered | Not listed in FHIR resources or Notes | Certified for (a)(12) family health history — genuine gap |
| Social/behavioral/SDOH | ⚠️ Partial | Notes has Smoking Status; certified for (a)(15) | Only smoking status documented; (a)(15) covers broader SDOH data |
| Specialty: post-acute assessments | ❌ Not covered | No nursing assessments, MDS, or facility-specific entities | If product stores MDS/nursing assessments, this is a significant gap |
| Implantable devices | ⚠️ Partial | FHIR Device (no field detail) | Certified for (a)(14) implantable devices but no detail |

## 6. Documentation Quality

**Very poor.** The EHI export documentation is inadequate for any practical use:

- **No data dictionary**: No field-level documentation for CDA or FHIR exports. The Notes format has field names and descriptions but no types, constraints, or value sets.
- **No export instructions**: No user guide explaining how to initiate an export, what options are available, or what files are produced.
- **No sample data**: No example exports, test files, or demonstration bundles.
- **No machine-readable artifacts**: No JSON Schema, XSD, OpenAPI spec, or other computable format.
- **No relationship documentation**: How entities relate to each other is not described.
- **Generic standard descriptions dominate**: The CDA and FHIR sections are textbook descriptions of the standards, not documentation of BroadStreet's implementation. A developer reading this page learns about CDA and FHIR in general but nothing about what BroadStreet specifically exports.

A developer could not build an import from this documentation alone. They would need to obtain sample exports and reverse-engineer the structure.

The RWT Plan (Test Case 4) confirms the export is being tested in production at assisted living facilities, but provides no additional detail about what data is exported — only that the system should "consistently generate and export EHI for both individual patients and populations."

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to determine what the export actually covers. The FHIR resource list is the standard US Core set (15 resources), identical to what the (g)(10) API serves. The CDA format is described generically with no product-specific detail. The only product-specific documentation is the 22-field HTML Notes structure, which covers a single entity type (clinical notes). There is no evidence the export goes beyond USCDI-scope data.

Even accounting for this being an early-stage product with potentially limited data breadth, the documentation fails to describe what's actually exported. Key domains certified by the product — family health history (a)(12), social/behavioral data (a)(15), implantable devices (a)(14) — are not addressed in the export documentation or are listed only as bare FHIR resource names.

**Axis 2 — Export approach: Repackaged existing export**

The evidence strongly suggests the (b)(10) export is the vendor's existing clinical exchange capabilities relabeled:

1. The FHIR resource list on the EHI export page is a subset of the (g)(10) API resources (15 of 23). No vendor-specific FHIR extensions, custom resources, or non-USCDI resources are documented.
2. The CDA export is almost certainly the same C-CDA used for (b)(1) Transitions of Care.
3. The documentation links to external HL7 standard specifications rather than providing a product-specific data dictionary.
4. No billing, specialty post-acute, or operational data domains are represented.
5. The only product-specific addition is the HTML Notes format, which is a single clinical note structure — not a comprehensive EHI export mechanism.

### Key Findings

1. **Documentation is a generic standards tutorial, not an EHI data dictionary.** The EHI export page spends ~80% of its content explaining what CDA and FHIR are, with almost no product-specific information. (Source: `ehi-export-page-rendered.html`)

2. **FHIR export appears identical to the (g)(10) API.** The 15 FHIR resources listed on the EHI export page are a subset of the 23 resources in the (g)(10) API documentation (`fhir-resources-page.png`), all using standard US Core STU 5.0.1 profiles. No extensions or non-USCDI resources.

3. **Only 22 product-specific fields documented total**, all in the HTML Notes format. Zero product-specific fields documented for CDA or FHIR exports.

4. **No data dictionary, schema, sample data, or export instructions exist.** The entire (b)(10) documentation is a single HTML page.

5. **Domains the product is certified for are missing from the export.** Family health history (a)(12) and social/behavioral data (a)(15) are certified capabilities with no representation in the export documentation. Medication administration records (eMAR), critical for post-acute care, are not mentioned.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   CDA 2.1 + FHIR R4 + HTML (Notes)
    Entities:        17 (1 CDA + 15 FHIR resources + 1 HTML Notes)
    Fields:          24 (22 in Notes + 2 generic CDA; 0 for FHIR)
    Descriptions:    100% of documented fields (24/24), but only 22 are meaningful
    Sample data:     No
    Bulk export:     Yes (per RWT Plan, individual and population-level)
    Domains covered: ~0 of 15+ applicable domains with adequate documentation

### Bottom Line

BroadStreet's EHI export documentation is among the thinnest possible — a single HTML page that mostly explains what CDA and FHIR standards are, rather than what the product actually exports. A patient or provider would receive standard clinical exchange documents (C-CDA and/or FHIR bundle) covering USCDI-scope data, plus HTML-formatted clinical notes. There is no evidence of a purpose-built (b)(10) export that covers the designated record set beyond what the existing (g)(10) API and (b)(1) transitions of care already provide.
