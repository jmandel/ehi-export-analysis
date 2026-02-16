# EHI Export Analysis: First Insight Corporation

**Product**: MaximEyes.com v1.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2729.Maxi.01.00.1.201014 (CHPL ID 10470)

## 1. Product Context

MaximEyes.com is a cloud-based (Microsoft Azure) EHR and practice management platform built exclusively for ophthalmology and optometry practices. Developed by First Insight Corporation (founded 1994, ~50 employees, Hillsboro, OR), it serves thousands of practices from solo providers to large corporate chains (e.g., U.S. Vision with 600+ locations).

The product is a comprehensive eye care suite with modules spanning:

- **Clinical EHR**: Structured ophthalmic/optometric exam documentation (visual acuity, IOP, slit lamp, fundus exam, refraction), SOAP notes, AI-assisted scribe (EVAA), coding triggers, clinical decision support, problem lists, medication lists, allergy lists, family health history, implantable device tracking (IOLs)
- **Practice Management**: Patient scheduling, registration, demographics, insurance verification, recall scheduling
- **Revenue Cycle / Billing**: End-to-end claims management, electronic claims submission, claim scrubbing, ERA/EOB auto-posting, accounts receivable, VSP claims integration
- **Optical Point-of-Sale**: Frame catalog, barcode scanning, inventory tracking, lab order management, spectacle and contact lens dashboards
- **Patient Engagement (EyeClinic.net)**: Patient portal, online intake forms, automated reminders, secure messaging, telehealth
- **Image Management**: OCT scans, fundus photographs, visual field results, autorefractor data — cloud-based HIPAA-compliant storage
- **E-Prescribing**: Two-way e-prescribing via DrFirst Rcopia, including eyeglass and contact lens prescriptions
- **Quality Reporting**: PQRS/MIPS, AAO IRIS Registry, AOA MORE Registry

This establishes a very broad baseline for what the EHI export should cover — clinical exam data, billing/claims, optical retail, specialty prescriptions, diagnostic images, and patient portal data are all patient-specific data used for decision-making.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `MaximEyes-EHI-Export-Documentation.pdf` (293 KB, 4 pages) | Brief EHI export instructions with screenshots, API endpoint details, query parameters, and "Scope of EHI" listing 15 data categories. Created 2025-03-17. | **Moderate** — establishes the export mechanism and scope but has no field-level detail |
| `MaximEyes-FHIR-API-Documentation.pdf` (572 KB, 40 pages) | Comprehensive FHIR R4 API reference covering SMART App Launch authorization, Bulk Data 1.0.1, and 20 FHIR resource types with search parameters and USCDI data class mappings. Created 2025-03-17. | **Most informative** — provides the most detail about what resources are available, though it is a (g)(10) FHIR API document, not a (b)(10) data dictionary |
| `swagger-v1.json` (448 KB) | OpenAPI 3.0.1 specification for the MaximEyes FHIR API. Contains endpoint definitions for 20 resource types (including 3 billing resources not in the PDF), plus export/status/download endpoints. Example responses embedded as strings. | **Moderate** — reveals billing resources (Account, ChargeItem, Coverage) not documented in the PDF; example responses show actual field content but no formal schemas |

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON, delivered as a ZIP file containing one NDJSON file per patient per resource type (naming pattern: `PatientID_Date_ResourceType.json`)
- **Mechanism**: Dual-mode:
  - **UI**: Navigate to Reports → Incentive Programs → Electronic Health Information in MaximEyes.com. Select single patient or "All Patients" checkbox, click Download.
  - **API**: HTTP GET to `GET /api/{customerName}/R4/Patient/Export` with JWK token authentication (system-level SMART Backend Services flow). Query parameters: `_since` (incremental), `_type` (resource filter). This is the standard FHIR Bulk Data 1.0.1 protocol.
- **Single-patient and bulk**: Both supported via UI and API
- **Access constraints**: Requires user permissions in MaximEyes.com (UI) or registered backend service with JWK credentials (API). FHIR API access is free of charge per the documentation.
- **Fees**: No fees mentioned for API access or export

## 4. Export Content: What's In It

### No Data Dictionary

There is **no data dictionary** in any of the artifacts. The export documentation consists of:
- A 15-item bulleted list of data categories ("Scope of EHI") on page 4 of the EHI export PDF
- FHIR resource types with search parameters in the FHIR API PDF
- Example JSON responses in the Swagger spec

There are no field-level definitions, no value sets, no relationship documentation, no sample export files, and no machine-readable data schemas. The Swagger spec defines all response schemas as `type: string` with embedded JSON example strings — there are zero structured component schemas.

### FHIR Resource Types

The export covers FHIR R4 resources conforming to US Core 3.1.1 profiles. Based on the FHIR API PDF and Swagger spec combined:

**Documented in the FHIR API PDF (20 resource types):**

| Resource Type | USCDI Data Class | Category | PDF Pages |
|---|---|---|---|
| AllergyIntolerance | Allergies and Intolerances | Clinical | 12–13 |
| CarePlan | Assessment and Plan of Treatment | Clinical | 13–14 |
| CareTeam | Care Team Member(s) | Clinical | 15 |
| Condition | Health Concerns, Problems | Clinical | 15–16 |
| Device | Implantable Devices (UDI) | Clinical | 17 |
| DiagnosticReport | Laboratory, Clinical Notes | Clinical | 17–18 |
| DocumentReference | Clinical Notes | Clinical | 19–20 |
| Encounter | Encounter Information | Clinical | 20–21 |
| Goal | Goals | Clinical | 21 |
| Immunization | Immunizations | Clinical | 22 |
| Location | — | Administrative | 23 |
| Medication | Medications | Clinical | 23–24 |
| MedicationRequest | Medications | Clinical | 23–24 |
| Observation | Laboratory, Vital Signs, Social History | Clinical | 25–35 |
| Organization | — | Administrative | 35–36 |
| Patient | Patient Demographics/Information | Demographics | 36–37 |
| Practitioner | — | Administrative | 37–38 |
| PractitionerRole | — | Administrative | 38 |
| Procedure | Procedures | Clinical | 38–39 |
| Provenance | Provenance | Infrastructure | 39–40 |

**Additional resources in Swagger but NOT documented in the FHIR API PDF (3 resource types):**

| Resource Type | Category | Notes |
|---|---|---|
| Account | Billing | Billing account with coverage, guarantor, service period |
| ChargeItem | Billing | Individual billing charges with codes, quantities, performers |
| Coverage | Billing/Insurance | Insurance coverage with subscriber, beneficiary, class |

**Total**: 23 FHIR resource types (20 documented + 3 undocumented billing resources)

### Vendor's Scope of EHI Categories

From page 4 of the EHI Export Documentation PDF (verified from rendered image), the vendor lists exactly 15 data categories:

1. Patient Demographic
2. Social History
3. Problems
4. Medications
5. Allergies and Reactions
6. Diagnostic Results
7. Vital signs
8. Encounter Diagnoses
9. Procedures
10. Care team members
11. Immunizations
12. Assessment and plan of treatment
13. Goals
14. Insurance Providers
15. Accounts

These map directly to USCDI v3.1.1 data classes. The last two items (Insurance Providers, Accounts) correspond to the undocumented Coverage and Account resources in the Swagger spec.

### Example Data from Swagger

The Swagger spec contains embedded JSON examples for 20 resource types. Analysis of these examples shows field counts per resource (from `analysis/swagger-field-analysis.json`):

| Resource | Example Fields | Notable Top-Level Keys |
|---|---|---|
| Patient | 41 | active, address, birthDate, communication, extension, gender, identifier, name, telecom |
| Encounter | 29 | class, hospitalization, identifier, location, participant, period, reasonCode, status, subject, type |
| DocumentReference | 27 | author, category, content, context, custodian, date, identifier, status, subject, type |
| ChargeItem | 19 | code, context, enteredDate, performer, quantity, reason, status, subject |
| Account | 17 | coverage, description, guarantor, name, owner, servicePeriod, status, subject, type |
| AllergyIntolerance | 17 | asserter, clinicalStatus, code, encounter, identifier, patient, reaction, type |
| DiagnosticReport | 17 | category, code, effectiveDateTime, encounter, performer, result, status, subject |
| Condition | 16 | category, clinicalStatus, code, encounter, subject, verificationStatus |
| Device | 15 | deviceName, distinctIdentifier, expirationDate, lotNumber, serialNumber, udiCarrier |
| MedicationRequest | 15 | authoredOn, category, dosageInstruction, encounter, intent, medicationReference, requester, status |
| Organization | 13 | active, address, identifier, name, telecom |
| Practitioner | 13 | active, address, identifier, name, telecom |
| Coverage | 12 | beneficiary, class, dependent, identifier, relationship, status, subscriber, type |
| Immunization | 12 | encounter, occurrenceDateTime, patient, primarySource, status, vaccineCode |
| CareTeam | 11 | managingOrganization, participant, status, subject |
| Procedure | 11 | code, encounter, identifier, performedPeriod, status, subject |
| CarePlan | 9 | category, encounter, intent, status, subject |
| Goal | 5 | description, lifecycleStatus, subject, target |

These are example data only — they demonstrate the resource structure but are not a substitute for a data dictionary.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's "Scope of EHI" exactly tracks the USCDI v3.1.1 data classes. The 15 listed categories correspond to standard clinical data elements that are required for the (g)(10) Standardized API criterion:

- **Strongest coverage**: Patient demographics (12 USCDI elements explicitly listed in the PDF), vital signs (11 observation profiles documented across pages 26–35), laboratory results, clinical notes (4 note types), medications
- **Thinnest coverage**: Social History (only Smoking Status is documented), Goals (minimal search parameters)
- **Undocumented additions**: Account, ChargeItem, and Coverage appear in the Swagger API only. These are the sole acknowledgment that the product handles billing — but they are not documented in the FHIR API PDF, have no field-level documentation, and no search parameters are specified. It is unclear whether they are included in the EHI bulk export or only available via individual API calls.

The fundamental limitation is that this is a USCDI/US Core projection of what the product stores, not a native data model export. The vendor's most distinctive data — structured ophthalmic exam findings, optical retail data, specialty prescriptions — has no representation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (12 USCDI elements documented: name, DOB, sex, race, ethnicity, language, address, phone, identifiers) | Adequate for standard demographics |
| Encounters / visits | ✅ Covered | Encounter resource (class, type, period, participants, location, reasonCode) | Covers visit metadata but not specialty exam content |
| Problems / conditions / diagnoses | ✅ Covered | Condition resource (health concerns, problems, encounter diagnoses with SNOMED/ICD coding) | Standard problem list; likely misses specialty-specific diagnostic categorizations |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest + Medication resources (medication orders with intent, dosage, dates) | Pharmaceutical Rx covered, but **eyeglass and contact lens prescriptions (CLX/Rx scripts) are not represented** — these are specialty clinical data with no FHIR US Core equivalent |
| Allergies | ✅ Covered | AllergyIntolerance resource (substance, drug class, reactions) | Adequate |
| Immunizations | ✅ Covered | Immunization resource (vaccine code, occurrence, status) | Adequate |
| Vitals | ✅ Covered | Observation resource with 11 vital sign profiles (BP, HR, RR, temp, height, weight, BMI, SpO2, head circumference) | Adequate; general vitals are covered |
| Lab results | ✅ Covered | Observation (laboratory category) + DiagnosticReport (LAB category) | Standard lab results; unclear if ophthalmic diagnostic test results (OCT metrics, visual field indices) are included |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (imaging narrative, pathology narrative) + DocumentReference | Report narratives may be included, but **diagnostic images themselves (OCT scans, fundus photos, visual field plots) are not addressed**. No discussion of binary/attachment export. |
| Procedures | ✅ Covered | Procedure resource (code, date, status) | Standard procedure codes; likely covers surgical procedures but not optical dispensing workflows |
| Clinical notes / documents | ✅ Covered | DocumentReference (Consultation Note, Discharge Summary, H&P, Progress Note) | Standard clinical note types; **structured ophthalmic exam data is NOT captured** — it may be embedded as unstructured text in notes but the structured findings (VA, IOP, slit lamp, fundus exam, refraction) are not exported as discrete data |
| Care plans / goals | ✅ Covered | CarePlan + Goal resources | Adequate for standard care plans |
| Orders / referrals | ⚠️ Partial | MedicationRequest covers medication orders; **no representation of referrals, optical lab orders, or diagnostic test orders** | The product manages optical lab orders and diagnostic test orders — these are patient-specific data gaps |
| Insurance / coverage | ⚠️ Partial | Coverage resource (in Swagger only, undocumented) | Resource exists but is not documented in the FHIR API PDF, has no search parameters, and its inclusion in bulk export is unconfirmed |
| Claims / billing | ⚠️ Partial | Account + ChargeItem resources (in Swagger only, undocumented) | Two billing resources exist but are undocumented. The product has full claims management, ERA/EOB, AR tracking — none of this is represented beyond basic Account and ChargeItem |
| Payments | ❌ Not covered | No payment resources in export | Product handles ERA/EOB auto-posting and payment tracking; this is a gap |
| Consents / directives | ❌ Not covered | No Consent resource | No evidence of consent document export |
| Patient communications / portal | ❌ Not covered | No messaging resources | EyeClinic.net patient portal handles secure messaging, intake forms, and care summary access; none exported |
| Specialty-specific (ophthalmology/optometry) | ❌ Not covered | No specialty resources | **Critical gap.** MaximEyes stores structured ophthalmic exam data (visual acuity, intraocular pressure, slit lamp findings, dilated fundus exam, refraction, etc.), optical retail data (frames, contact lens orders, lab orders, spectacle prescriptions), and diagnostic imaging data (OCT, visual fields, fundus photos). None of this has any representation in the FHIR R4 export. This is the product's most clinically distinctive data. |

## 6. Documentation Quality

**Can a developer use the export from these docs?** A developer could build a FHIR Bulk Data client to retrieve NDJSON files — the SMART Backend Services auth flow and Bulk Data protocol are adequately documented. However:

- **No data dictionary**: There is no field-level documentation. A developer would need to rely entirely on US Core 3.1.1 profile definitions and the example responses in the Swagger spec.
- **No sample export data**: No actual NDJSON export files are provided. The Swagger examples show individual resource instances, not bulk export output.
- **No value sets or code systems**: While the PDF mentions SNOMED, LOINC, and ICD codes in search examples, there is no documentation of which code systems are used for which fields, or what vendor-specific coded values might appear.
- **No relationships documentation**: Beyond FHIR's built-in references, there is no documentation of how resources relate to each other in the MaximEyes data model.
- **Undocumented billing resources**: Account, ChargeItem, and Coverage exist in the Swagger API but have zero documentation in the PDF — no USCDI mappings, no search parameters, no field descriptions.
- **Machine-readable artifacts**: The Swagger spec is machine-readable but contains no actual response schemas (all responses are `type: string`). Zero component schemas are defined.
- **The FHIR API PDF is a (g)(10) document, not a (b)(10) document**: Its footer reads "MaximEyes FHIR API Documentation" on all 40 pages. It was written for the FHIR API certification requirement, not for EHI export. The EHI export PDF simply references it for "format details."

## 7. Overall Assessment

### Classification

**Standard-based projection**

The EHI export is the FHIR Bulk Data API repackaged as a (b)(10) export. The evidence is unambiguous:

1. The export uses the exact same FHIR R4 NDJSON / Bulk Data 1.0.1 endpoint as the (g)(10) API
2. The documented FHIR resources match the US Core 3.1.1 resource set required for (g)(10)
3. The supported scopes are US Core scopes
4. The "Scope of EHI" lists USCDI data classes, not the product's full data domains
5. The FHIR API PDF is explicitly a FHIR API document (per its title and footer)
6. The 3 billing resources (Account, ChargeItem, Coverage) in the Swagger spec are undocumented and represent a modest attempt to extend beyond US Core, but they are not mentioned in the EHI export PDF's Scope of EHI (though "Insurance Providers" and "Accounts" are listed)

### Key Findings

1. **The export is a (g)(10) FHIR API relabeled as (b)(10).** The same endpoint, the same resources, the same documentation. The three undocumented billing resources in the Swagger spec are the only evidence of effort beyond (g)(10).

2. **The product's most clinically distinctive data — structured ophthalmic exam findings — is entirely absent.** MaximEyes stores detailed structured data for visual acuity, intraocular pressure, slit lamp findings, fundus exams, and refraction. FHIR US Core has no profiles for this data, and the vendor has not created extensions or custom resources to export it. This is the most significant EHI gap.

3. **Optical retail data is missing.** Frame orders, contact lens orders, spectacle/CLX prescriptions, lab orders, and point-of-sale data are patient-specific billing and clinical data with no representation in the export.

4. **Diagnostic images are not addressed.** The product stores OCT scans, fundus photographs, and visual field results — clinically critical ophthalmic data. The export documentation does not mention binary/attachment handling.

5. **Billing coverage is token at best.** The product has full claims management, ERA/EOB auto-posting, and AR tracking. Three undocumented FHIR resources (Account, ChargeItem, Coverage) cover a fraction of this data.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 NDJSON (Bulk Data 1.0.1)
Model type:      Standard projection (US Core 3.1.1)
Entities:        23 FHIR resource types (20 documented + 3 undocumented billing)
Fields:          N/A (no field-level documentation; FHIR profiles define fields)
Descriptions:    N/A (no data dictionary)
Sample data:     No (Swagger examples only, no actual export samples)
Bulk export:     Yes (single-patient and all-patient)
Domains covered: 9 of 17 applicable domains (5 partial, 3 not covered)
```

### Bottom Line

MaximEyes.com's EHI export is its FHIR (g)(10) API rebranded as a (b)(10) export. A patient or provider would receive a standard USCDI clinical summary — demographics, problems, medications, allergies, vitals, labs, notes, immunizations, and procedures — but would **not** receive the specialty ophthalmology/optometry data that is the core clinical value of this EHR: structured exam findings, optical prescriptions, diagnostic images, optical retail data, or most billing records. For an eye care-specific EHR, the absence of eye care-specific data from the export is the single most significant gap.
