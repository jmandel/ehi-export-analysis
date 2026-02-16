# EHI Export Analysis: iCare.com, Inc.

**Product**: iCare EHR Version 2
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2617.iCar.02.00.1.200220 (Listing ID 10314)

## 1. Product Context

iCare EHR is a cloud-native enterprise EHR marketed to hospitals, multi-hospital systems, and ambulatory clinics. The CHPL certification SED lists intended user settings as "Inpatient, Ambulatory, and Behavioral." The product is developed by iCare.com, Inc., a small company (~11–200 employees) based in Fort Lauderdale, Florida, with ONC certification since 2020.

The product includes modules for:
- **Clinical documentation**: charting, notes, problem/medication/allergy lists, CPOE for medications and labs, vital signs, immunizations, care plans
- **E-prescribing**: EPCS, drug interaction checking, Surescripts integration
- **Revenue Cycle Management (RCM)**: insurance verification, claims, billing, payments, denial management, E/M coding
- **Patient portal**: secure messaging, appointment scheduling, bill payment, health record access
- **Scheduling**: appointment, procedure, and surgery scheduling
- **Lab/imaging integration**: lab results and radiology results flowing into patient records
- **Public health reporting**: syndromic surveillance, reportable lab results

This broad feature set means a compliant (b)(10) export should cover clinical data, billing/RCM data, e-prescribing records, portal communications, and scheduling data — not just the USCDI clinical summary subset.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.html` (15 KB) | Clean HTML of the EHI export documentation page at https://icare.com/developers/ehi_export/. Lists 3 export methods and 13 FHIR resource types with example URIs. | **Primary** — the vendor's (b)(10) documentation |
| `iCare-API-Guide.pdf` (67 pages, 355 KB) | Proprietary REST API guide (Copyright 2020). Documents 16 clinical data categories with example JSON outputs. | **Most informative** — provides field-level detail via sample outputs |
| `fhir-capability-statement.json` (3 KB) | FHIR R4 CapabilityStatement from sandbox server (EMR Direct Interoperability Engine). Declares US Core Server and Bulk Data conformance. | **Supplementary** — confirms third-party infrastructure |
| `ehi-export-page-wp-json.json` (18 KB) | WordPress API response for the EHI page. Confirms page last modified 2025-10-18. | **Metadata only** |
| `screenshot-ehi-export-page.png` (903 KB) | Full-page screenshot of the EHI export page. | **Visual confirmation** |

No data dictionary, schema files, or sample export files were provided in any artifact. The API Guide PDF's example JSON outputs are the closest thing to field-level documentation.

## 3. Export Mechanics

The EHI export page describes three methods:

### Method 1: CCD/HIM Export (In-App, Single Patient)
- **Format**: C-CDA XML (CCD) and HIM documents
- **Mechanism**: UI — within patient chart, navigate to Reports > Clinical Summary > Continuity of Care and Referral Notes (for CCD), or Patient Info > HIM Request (for assessments/notes)
- **Scope**: Single patient only
- **Documentation**: Two sentences; no detail on content or format

### Method 2: CSC Request (Bulk Export)
- **Format**: Unknown — described as "files" delivered via SFTP
- **Mechanism**: Vendor-assisted — make a "CSC request" to iCare
- **Scope**: Organization's entire clinical data (population)
- **Documentation**: One sentence. States a data dictionary will be included with the delivered files, but **no data dictionary, format specification, or any other documentation is publicly available** for this method.
- **Fees**: Not mentioned; the certification page says EHI export is "Included with iCare subscription fee"

### Method 3: FHIR REST API (Single/Population/Group)
- **Format**: FHIR R4 JSON via Bulk Data ($export)
- **Mechanism**: API — OAuth2 token then GET Patient/$export, Group/$export, or resource-specific queries
- **Scope**: Single patient, population, or group
- **Endpoint**: `https://sandbox-r4.interopengine.com/fhir/r4/icare/`
- **Infrastructure**: Third-party — powered by "EMR Direct Interoperability Engine" (not iCare's own system)

### Method 4 (Undocumented on EHI page): Proprietary REST API
- **Format**: FHIR R4 JSON per category; C-CDA XML for all-criteria request
- **Mechanism**: API — session token then GET /rest/extApp/Clinical?category=X
- **Scope**: Single patient
- **Documentation**: 67-page API guide with example inputs/outputs (Copyright 2020)
- **Endpoint**: `<URL>/iCareEHRWeb/rest/extApp/Clinical`
- **Note**: This older API is documented in the separately-linked API Guide PDF but is not directly referenced on the EHI export page itself.

## 4. Export Content: What's In It

### No data dictionary provided

There is **no data dictionary** for any export method. No schema files, no field definitions, no table structures, no value sets, no relationship documentation. The only field-level information comes from example JSON responses in the 2020 API Guide PDF.

### FHIR resource types on the EHI export page

The EHI export page lists 13 FHIR R4 resource types with example query URIs:

| # | Resource Type | Example URI Correct? |
|---|---|---|
| 1 | CarePlan | ✅ Yes |
| 2 | AllergyIntolerance | ✅ Yes |
| 3 | CareTeam | ✅ Yes |
| 4 | Condition | ✅ Yes |
| 5 | Device | ✅ Yes |
| 6 | DiagnosticReport | ✅ Yes (LAB category only) |
| 7 | DocumentReference | ✅ Yes |
| 8 | Goal | ✅ Yes |
| 9 | Immunization | ✅ Yes |
| 10 | MedicationRequest | ✅ Yes |
| 11 | Observation | ⚠️ Example hardcodes LOINC 2708-6 only |
| 12 | Procedure | ❌ Example URI points to Patient endpoint |
| 13 | Encounter | ❌ Example URI points to Procedure endpoint |

**Copy-paste errors**: The Procedure and Encounter sections have their example URIs swapped — Procedure's example is `Patient?_id=MRN.XXXXXX` and Encounter's example is `Procedure?patient=MRN.XXXXXX`. Additionally, every resource section redundantly lists the generic `Patient/id/$export` URI, suggesting the documentation was quickly templated rather than carefully authored.

No field-level documentation is provided for any of these 13 resource types. Each section follows the same template: URI pattern, "Or can use Patient/id/$export", request parameters, method GET, example URL. No descriptions of what fields each resource will contain, what coded values to expect, or how vendor-specific data maps to standard FHIR elements.

### Proprietary API categories (from API Guide PDF)

The 67-page API Guide (2020) documents 16 clinical data categories via the proprietary REST API. Each category includes a description, example input, and example JSON output showing the FHIR resource structure returned. From these examples, 85 total fields are visible across all categories:

| Category | Description | FHIR Resource | Fields in Example |
|---|---|---|---|
| patient | Demographics (name, sex, DOB, race, ethnicity, language) | Patient | 18 |
| smokingStatus | Smoking status with onset date | Composition | 4 |
| problem | Problems with SNOMED codes, status, onset/resolution | Condition | 6 |
| medication | Medications with RxNorm codes, dosage, directions | MedicationStatement | 7 |
| medAllergy | Medication allergies with reactions and severity | AllergyIntolerance | 7 |
| labTest | Planned lab tests | DiagnosticReport | 3 |
| labResult | Lab results with values and reference ranges | Observation | 4 |
| vital | Vital signs with LOINC codes | Observation | 4 |
| procedure | Procedures with SNOMED codes and dates | Procedure | 6 |
| careTeam | Care team members with roles | CareTeam | 2 |
| immunization | Immunizations with CVX codes and lot numbers | Immunization | 4 |
| device | Implanted devices with UDI identifiers | Device | 4 |
| planOfTreatment | Care plan activities (medication/lab/procedure/task) | CarePlan | 4 |
| assessment | Clinical assessment narrative | RiskAssessment | 1 |
| goal | Discharge goals (free-text) | Goal | 3 |
| healthConcern | Health concerns — complaints and observations | Composition | 8 |
| **Total** | | | **85** |

Of the 85 fields visible in examples, 79 have descriptions (either from the API guide text or inferable from the JSON structure and context). No formal field-level data dictionary exists — these fields are only documented implicitly through the example JSON responses.

### All Criteria Data Request

The API Guide also documents a combined endpoint (`/rest/extApp/ClinicalCCDA`) that returns a C-CDA compliant XML document containing all 16 categories' data for a patient. No sample output is provided for this endpoint.

### What's notably absent

The export documentation — across all methods — covers **only clinical data mapped to standard FHIR resources or C-CDA sections**. The following data domains known to exist in iCare EHR are not represented in any export method:

- **Revenue Cycle Management / Billing**: No claims, charges, payments, insurance verification, denial records, or E/M codes
- **Scheduling**: No appointments, procedure schedules, surgery schedules
- **E-prescribing transactions**: No prescription tracking, EPCS audit trails, Surescripts transaction records
- **Patient portal data**: No secure messages, portal interactions, patient-submitted forms, online payment records
- **Document management**: DocumentReference is listed but described only as "assessments, notes, and documents" — unclear if this includes the broader document vault (scanned forms, correspondence, images)
- **Orders**: CPOE orders beyond what maps to MedicationRequest are not represented
- **Behavioral health**: Explicitly excluded — the page states "items related to psychotherapy will not be included in any data export"

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes their export around a single category: **clinical data**. There is no separate billing, administrative, or scheduling category. All 16 API categories and all 13 FHIR resource types fall within the USCDI/US Core clinical data class:

- **Demographics**: Patient resource with name, gender, DOB, race, ethnicity, language, address, phone (18 fields in example)
- **Clinical conditions**: Problems (Condition), allergies (AllergyIntolerance), smoking status
- **Medications**: Active medications (MedicationStatement/MedicationRequest) with RxNorm codes and dosing
- **Diagnostics**: Lab tests (DiagnosticReport), lab results (Observation), vital signs (Observation)
- **Procedures & devices**: Procedures with SNOMED codes, implanted devices with UDI
- **Care planning**: CarePlan activities, goals, assessments (RiskAssessment), health concerns
- **Care team**: Team members with roles
- **Documents**: DocumentReference (assessments, notes, documents)
- **Encounters**: Visit dates (minimal — only period.start in the example)
- **Immunizations**: Vaccine records with CVX codes

This is a reasonable coverage of US Core / USCDI clinical data elements, but it represents only the subset of data that would also be available through the (g)(10) FHIR API — not the full designated record set that (b)(10) requires.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` category (18 fields): name, gender, DOB, race, ethnicity, language, address, phone | Adequate for USCDI; no SSN, emergency contacts, or preferred pharmacy |
| Encounters / visits | ⚠️ Partial | `Encounter` resource on EHI page; API guide Encounter shows only `period.start` | Only visit date — no encounter type, location, provider, disposition, or diagnosis |
| Problems / conditions | ✅ Covered | `problem` category: SNOMED codes, clinical status, onset/resolution dates | Well-structured with coded data |
| Medications / prescriptions | ✅ Covered | `medication` category: RxNorm codes, dosage, directions, start/end dates | Covers ordered medications; unclear if MAR or dispensing data is included |
| Allergies | ✅ Covered | `medAllergy` category: RxNorm codes, reactions, severity, onset dates | Only medication allergies — unclear if food/environmental allergies are captured |
| Immunizations | ✅ Covered | `immunization` category: CVX codes, dates, lot numbers | Standard coverage |
| Vitals | ✅ Covered | `vital` category: LOINC codes, values, units, components | Standard coverage |
| Lab results | ✅ Covered | `labResult`/`labTest` categories: LOINC codes, values, reference ranges | Standard coverage |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport listed but example shows `category=LAB` only | No evidence of radiology reports despite PACS integration |
| Procedures | ✅ Covered | `procedure` category: SNOMED codes, status, dates | Standard coverage |
| Clinical notes / documents | ⚠️ Partial | `assessment` (narrative text), `healthConcern`, DocumentReference | DocumentReference scope unclear; assessment is free text only |
| Care plans / goals | ✅ Covered | `planOfTreatment` and `goal` categories: activities, scheduled dates, descriptions | Includes planned medications/labs/procedures and discharge goals |
| Orders / referrals | ⚠️ Partial | `planOfTreatment` shows ServiceRequest activities for planned items | No dedicated orders resource; CPOE orders likely incomplete |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in any export method | Product does insurance verification (RCM module); **significant gap** |
| Claims / billing | ❌ Not covered | No claims, charges, or billing entities in any export method | Product has full RCM module (claims, billing, coding); **significant gap** |
| Payments | ❌ Not covered | No payment entities in any export method | Product tracks payments and A/R; **significant gap** |
| Consents / directives | ❌ Not covered | No consent or advance directive entities | Unknown if product stores these |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal interaction data | Product has patient portal with secure messaging; **gap** |
| Specialty-specific (Behavioral) | ❌ Not covered | Explicitly excluded: "items related to psychotherapy will not be included" | Product targets behavioral health settings per CHPL SED; psychotherapy notes are carved out of EHI per §171.102, but behavioral health diagnoses, treatment plans, session dates, and medications ARE still EHI |

**Covered**: 8 of 18 applicable domains
**Partially covered**: 4 domains
**Not covered**: 6 domains (of which at least 4 represent confirmed product capabilities)

## 6. Documentation Quality

**Overall: Poor.**

- **No data dictionary**: None of the artifacts provide a formal data dictionary — no field definitions, no types, no value sets, no relationships between entities
- **No schema files**: No JSON Schema, FHIR StructureDefinitions, or any machine-readable format specification
- **No sample export data**: No sample files showing what an actual export looks like
- **Field documentation via example only**: The only field-level information comes from example JSON responses in the 6-year-old API Guide PDF (Copyright 2020). A developer would have to reverse-engineer the data model from these examples
- **Copy-paste errors**: The EHI export page has at least 2 incorrect example URIs (Procedure and Encounter sections are swapped) and a repetitive template structure where every section redundantly lists the `Patient/id/$export` URI
- **Stale documentation**: The API Guide documents a proprietary REST API at `ehr.icare.com/iCareEHRWeb/rest/` while the EHI page documents a FHIR API at `sandbox-r4.interopengine.com`. The relationship between these two APIs is unexplained
- **CSC bulk export undocumented**: The most promising export method (vendor-provided data dump with data dictionary) has zero public documentation — the data dictionary is only delivered with the actual export

A developer attempting to build an import from this documentation would:
1. Know the 13 FHIR resource types available but have no field-level specification
2. Have example JSON from a 2020 API guide that may not match current output
3. Have no documentation whatsoever for the bulk data export format
4. Need to contact iCare directly ("CSC request") to get the actual data and its documentation

## 7. Overall Assessment

### Classification

**Standard-based projection**

The documented EHI export is fundamentally the vendor's (g)(10) FHIR API repackaged as a (b)(10) export. The 13 FHIR resource types on the EHI page map directly to US Core resources. The third-party infrastructure (EMR Direct Interoperability Engine) is a standard interoperability middleware platform, not a custom export tool. The proprietary REST API (from the 2020 PDF) covers the same clinical data domains. Neither API surfaces any data beyond what USCDI/US Core defines — no billing, no scheduling, no portal data, no vendor-specific internal model.

The vendor-assisted "CSC request" for bulk data could potentially constitute a native export, but it is entirely undocumented and unassessable from the public artifacts.

### Key Findings

1. **The export is a FHIR/C-CDA clinical summary, not a full EHI export.** All documented export methods produce standard FHIR R4 resources or C-CDA documents covering only USCDI clinical data classes — approximately 13 resource types. The vendor's native data model (database tables, billing records, scheduling data, portal messages) is not exported.

2. **Revenue Cycle Management data is entirely absent.** iCare EHR has an integrated RCM module with insurance verification, claims management, billing, payment tracking, and denial management. None of this data appears in any export method — a clear (b)(10) gap since billing records are explicitly part of the HIPAA designated record set.

3. **No data dictionary exists.** Across all artifacts, there is no formal data dictionary, no schema, no field definitions. The only field-level information is implicit in 6-year-old API guide examples. The CSC bulk export allegedly includes a data dictionary "with the files," but none is publicly available.

4. **The FHIR API is third-party infrastructure.** The export endpoint (`sandbox-r4.interopengine.com`) is powered by EMR Direct Interoperability Engine, a third-party interoperability platform. The CapabilityStatement only declares `Group/$export` — even the individual resource queries documented on the EHI page are not reflected in the CapabilityStatement.

5. **Copy-paste errors indicate minimal effort.** The EHI export page contains swapped example URIs (Procedure/Encounter), a repetitive template structure, and inconsistencies suggesting the documentation was hastily assembled rather than carefully authored.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 JSON, C-CDA XML
Model type:      Standard projection (US Core / USCDI)
Entities:        13 FHIR resource types (EHI page) / 16 API categories (API guide)
Fields:          ~85 (visible in sample outputs only; no formal dictionary)
Descriptions:    ~93% (79/85 fields in samples have implicit descriptions; 0% formally documented)
Sample data:     No (example JSON in API guide only)
Bulk export:     Yes (FHIR Bulk Data $export; also vendor-assisted CSC request)
Domains covered: 8 of 18 applicable domains (4 partial, 6 not covered)
```

### Bottom Line

iCare's (b)(10) export is their (g)(10) FHIR API relabeled. It covers the standard USCDI clinical data classes (demographics, problems, medications, labs, vitals, procedures, immunizations, care plans) but entirely omits billing/RCM data, scheduling, patient portal communications, and e-prescribing transaction history — all of which the product stores and which are part of the HIPAA designated record set. The single biggest gap is the complete absence of revenue cycle and billing data despite iCare having an integrated RCM module. A patient or provider receiving this export would get a clinical summary, not their complete health record.
