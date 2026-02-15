# EHI Export Analysis: iCare.com, Inc.

**Product**: iCare EHR Version 2
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2617.iCar.02.00.1.200220 (CHPL #10314)

## 1. Product Context

iCare EHR is a cloud-native enterprise EHR platform from iCare.com, Inc. (Fort Lauderdale, FL), marketed to hospitals, clinics, and physician practices in both inpatient and ambulatory settings. The CHPL SED description lists intended users as "Inpatient, Ambulatory, and Behavioral." The product was certified in February 2020 via Drummond Group ONC-ACB.

Based on the vendor's website and certification criteria, iCare EHR manages data across these domains relevant to EHI completeness:

- **Clinical documentation**: Patient charting, notes, problem lists, medication lists, allergy lists, vitals, immunizations, care plans, clinical decision support
- **E-prescribing**: EPCS, drug interaction checks, prescription tracking via Surescripts
- **Lab and imaging**: Lab orders/results, radiology integration, PACS integration
- **Revenue cycle management (RCM)**: Insurance verification, billing, claims, payments, denial management, E/M coding — described as an integrated module
- **Scheduling**: Appointment, procedure, and surgery scheduling
- **Patient portal**: Secure messaging, appointment scheduling, bill payment, health information access
- **CPOE**: Computerized provider order entry for medications and labs
- **Document management**: Centralized vault for charts, forms, images, correspondence

This breadth of functionality — particularly the integrated RCM/billing module and inpatient capabilities — sets the baseline for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.html` (15 KB) | Clean HTML extraction of the EHI Export documentation page at `https://icare.com/developers/ehi_export/`. Describes 3 export methods and lists 13 FHIR resource types. Verified against live site on 2026-02-15 — content matches. | **Primary source** — defines the export |
| `screenshot-ehi-export-page.png` (903 KB) | Full-page screenshot of the EHI export page. Confirms the rendered content matches the HTML extraction. | Corroborative |
| `ehi-export-page-wp-json.json` (18 KB) | WordPress REST API response for page ID 1286. Shows page last modified 2025-10-18. | Metadata only |
| `iCare-API-Guide.pdf` (355 KB, 67 pages) | Proprietary REST API guide (Copyright 2020) documenting login, patient search, encounters, and 16 clinical data categories with FHIR R4 JSON examples. Also documents a C-CDA "All Criteria Data Request." | **Secondary source** — older API, more detailed |
| `fhir-capability-statement.json` (3 KB) | FHIR R4 CapabilityStatement from sandbox at `sandbox-r4.interopengine.com`. Powered by "EMR Direct Interoperability Engine" (third-party middleware). Declares US Core Server and Bulk Data conformance. Only declares Group/$export and SearchParameter — no individual resource interactions. | Reveals third-party infrastructure |

## 3. Export Mechanics

iCare describes three export methods on the EHI export page:

**Method 1: CCD/HIM Export (In-App, Single Patient)**
- Generate a CCD via: Reports > Clinical Summary > Continuity of Care and Referral Notes
- Export Clinical Assessments and Notes via: Patient Info > HIM Request
- Format: C-CDA (implied by "CCD")
- No further detail on scope, fields, or output format

**Method 2: CSC Request for Full Data Export (Population, Vendor-Assisted)**
- Quote: "You may make a CSC request for export of the entirety of your organization's clinical data. The files will be provided via SFTP or other requested means and will include a description of the data file formats and data dictionary."
- This is vendor-assisted (contact CSC = Customer Service Center), not self-service
- **No data dictionary, format specification, or any documentation is publicly available** for this method. The data dictionary is apparently delivered only with the actual export files.
- Cannot be assessed for coverage or format

**Method 3: FHIR REST API (Single Patient, Population, Group)**
- Single patient: `Patient/id/$export` or resource-specific queries
- Population: `Patient/$export` (Bulk Data)
- Group: `Group/GroupID/$export` (Bulk Data)
- Authorization: OAuth2 via `sandbox-r4.interopengine.com/oauth/icare/token`
- Hosted on third-party infrastructure: EMR Direct Interoperability Engine
- Format: FHIR R4 JSON (via Bulk Data ndjson)
- Requires Admin role or PHI Export permission

**Access**: Method 1 is self-service via UI. Method 2 requires vendor engagement. Method 3 is API-based, requiring technical implementation. The certification page states: "Included with iCare subscription fee."

**Bulk export**: Yes, via Methods 2 and 3.

## 4. Export Content: What's In It

### FHIR API Export (Method 3) — 13 Resource Types

The EHI export page lists 13 FHIR resource types under "Data Elements." Each section follows an identical copy-paste template with a resource-specific query URI and a generic `Patient/id/$export` URI. There is no field-level documentation, no data dictionary, no schemas, and no sample data.

| FHIR Resource | Query Example | Notes |
|---|---|---|
| CarePlan | `CarePlan?category=assess-plan&patient=<id>` | |
| AllergyIntolerance | `AllergyIntolerance?patient=<id>` | |
| CareTeam | `CareTeam?patient=<id>&status=active` | |
| Condition | `Condition?patient=<id>` | |
| Device | `Device?patient=<id>` | |
| DiagnosticReport | `DiagnosticReport?category=LAB&patient=<id>` | LAB category only |
| DocumentReference | `DocumentReference?patient=<id>` | "Contains all info about Assessment, Notes and Documents tabs" |
| Goal | `Goal?patient=<id>` | |
| Immunization | `Immunization?patient=<id>` | |
| MedicationRequest | `MedicationRequest?intent=proposal&patient=<id>` | |
| Observation | `Observation?code=2708-6&patient=<id>` | Example hardcodes LOINC 2708-6 (oxygen saturation) |
| Procedure | `Procedure?patient=<id>` | Example URI incorrectly links to `Patient?_id=` |
| Encounter | `Patient?_id=<id>` | URI is wrong (says Patient, not Encounter); example links to `Procedure?patient=` |

**Copy-paste errors**: The generic `Patient/id/$export` URI appears 28 times across the page — pasted identically into every resource section. The Encounter section's URI says `Patient?_id=<id>` instead of `Encounter?patient=<id>`, and its example links to `Procedure?patient=MRN.XXXXXX`.

### Proprietary API (API Guide PDF) — 16 Data Categories

The 67-page API Guide (2020) documents an older proprietary REST API at `ehr.icare.com/iCareEHRWeb/rest/`. It covers 16 clinical data categories with JSON request/response examples containing ~62 unique field names across all categories:

| Category | Description | Fields in Example |
|---|---|---|
| patient | Name, sex, DOB, race, ethnicity, preferred language | 24 |
| careTeam | Care team members | 6 |
| smokingStatus | Smoking status | 9 |
| problem | Problems | 13 |
| medication | Medications | 15 |
| medAllergy | Medication allergies | 15 |
| labTest | Planned lab tests | 10 |
| labResult | Lab test results | 21 |
| vital | Vital measurements | 13 |
| procedure | Procedures | 17 |
| immunization | Immunizations | 15 |
| device | Implanted devices | 9 |
| planOfTreatment | Care plan | 10 |
| assessment | Assessment | 3 |
| goal | Discharge goals | 7 |
| healthConcern | Health concerns (complaints and observations) | 5 |

An "All Criteria Data Request" endpoint (`/rest/extApp/ClinicalCCDA?id=<id>`) returns all categories combined as a C-CDA XML document.

Both the FHIR API and the proprietary API cover essentially the same clinical data domains — standard USCDI data classes. Neither includes billing, scheduling, insurance, or administrative data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation (across all three methods) covers **standard USCDI clinical data only**. There is no vendor-specific categorization — the data is organized entirely around standard FHIR resource types and C-CDA sections.

The 13 FHIR resources on the EHI page and 16 API categories in the PDF map to the same core clinical domains:
- **Demographics**: Patient resource / `patient` category (24 fields in API examples: name, gender, birthDate, race, ethnicity, language, address, telecom, contacts)
- **Problems/conditions**: Condition resource / `problem` category (13 fields: clinicalStatus, code, onsetDateTime, abatementString)
- **Medications**: MedicationRequest / `medication` category (15 fields: medicationCodeableConcept, dosage, effectiveDateTime)
- **Allergies**: AllergyIntolerance / `medAllergy` category (15 fields: clinicalStatus, reaction, severity, onsetDateTime)
- **Labs**: DiagnosticReport + Observation / `labTest` + `labResult` categories (31 combined fields)
- **Vitals**: Observation / `vital` category (13 fields)
- **Immunizations**: Immunization / `immunization` category (15 fields: vaccineCode, occurrenceDateTime, status)
- **Procedures**: Procedure / `procedure` category (17 fields: bodySite, performedDateTime, performer)
- **Care plans/goals**: CarePlan + Goal / `planOfTreatment` + `goal` categories (17 combined fields)
- **Clinical notes**: DocumentReference / `assessment` category (3 fields in assessment; DocumentReference described as containing "Assessment, Notes and Documents tabs")
- **Care team**: CareTeam / `careTeam` category (6 fields: member, participant)
- **Devices**: Device / `device` category (9 fields: udiCarrier, deviceIdentifier)
- **Encounters**: Encounter resource (period.start only in API examples)
- **Smoking status**: Observation / `smokingStatus` category (9 fields)
- **Health concerns**: `healthConcern` category (5 fields)

The thinnest data elements are assessment (3 fields), healthConcern (5 fields), and careTeam (6 fields). The richest are patient (24 fields), labResult (21 fields), and procedure (17 fields) — though these counts come from example JSON, not a formal schema.

**Notable absence**: The entire billing/RCM side of the product — insurance verification, claims, payments, denial management, E/M coding — has zero representation in any export method. Scheduling data is also entirely absent. These are integrated modules in the product, not third-party systems.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (13 FHIR resources); `patient` API category with 24 fields (name, gender, DOB, race, ethnicity, language, address, telecom, contacts) | Adequate for standard demographics |
| Encounters / visits | ⚠️ Partial | Encounter resource listed on EHI page; API Guide Encounter endpoint returns only `period.start` | Encounters are listed but extremely thin — only start date/time, no type, location, provider, or discharge info |
| Problems / conditions / diagnoses | ✅ Covered | Condition resource; `problem` API category with 13 fields | Adequate |
| Medications / prescriptions | ✅ Covered | MedicationRequest resource; `medication` API category with 15 fields | Covers prescriptions; no medication administration records (MAR) for inpatient |
| Allergies | ✅ Covered | AllergyIntolerance resource; `medAllergy` API category with 15 fields | Adequate |
| Immunizations | ✅ Covered | Immunization resource; `immunization` API category with 15 fields | Adequate |
| Vitals | ✅ Covered | Observation resource; `vital` API category with 13 fields | Adequate |
| Lab results | ✅ Covered | DiagnosticReport (LAB only) + Observation resources; `labTest` + `labResult` API categories with 31 combined fields | Limited to LAB category in DiagnosticReport |
| Imaging / diagnostic reports | ❌ Not covered | DiagnosticReport filtered to `category=LAB` only; no radiology/imaging resources | Product has PACS integration and radiology results — gap |
| Procedures | ✅ Covered | Procedure resource; `procedure` API category with 17 fields | Adequate |
| Clinical notes / documents | ⚠️ Partial | DocumentReference resource; `assessment` API category (3 fields); page says DocumentReference contains "Assessment, Notes and Documents tabs" | DocumentReference may contain notes, but no field-level detail; clinical note depth unclear |
| Care plans / goals | ✅ Covered | CarePlan + Goal resources; `planOfTreatment` + `goal` API categories | Adequate |
| Orders / referrals | ❌ Not covered | No ServiceRequest, no order resources beyond MedicationRequest | Product has CPOE for meds and labs — lab orders not in export |
| Insurance / coverage | ❌ Not covered | No Coverage or insurance-related resources in any export method | Product has integrated insurance verification — significant gap |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing entities in any export method | Product has full RCM module with claims, coding, denials — **major gap** |
| Payments | ❌ Not covered | No payment or financial transaction data in any export method | Product tracks payments and A/R — significant gap |
| Consents / directives | ❌ Not covered | No Consent resources | Unknown if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No Communication resources; no portal message export | Product has portal with secure messaging — gap |
| Specialty-specific (Behavioral Health) | ❌ Not covered | Page explicitly states: "Items related to psychotherapy will not be included in any data export" | Product is used in behavioral health settings per CHPL SED description; psychotherapy notes are excluded from EHI by statute, but behavioral health assessments, treatment plans, and diagnoses ARE EHI |

**Covered**: 10 of 19 applicable domains (with 2 partial)

## 6. Documentation Quality

**Quality: Poor.** The EHI export documentation is insufficient for a developer to understand, reproduce, or verify the export.

**What exists:**
- A single web page (last modified 2025-10-18) listing 13 FHIR resource types with query URIs
- A 67-page API Guide PDF (2020) documenting an older proprietary REST API with JSON examples for 16 clinical categories
- A FHIR CapabilityStatement from a third-party sandbox server

**What's missing:**
- **No data dictionary** — no field-level definitions for any export method
- **No schema files** — no JSON Schema, FHIR StructureDefinitions, or XML schemas
- **No sample data** — no example export files
- **No value sets** — no documentation of coded values, code systems, or enumerations
- **No relationships** — no entity relationship diagrams or foreign key documentation
- **No format specification for Method 2** (CSC bulk export) — the allegedly most complete export method has zero public documentation
- **No field types** — the API Guide shows JSON examples but never formally specifies types or cardinality

**Documentation errors:**
- The Encounter section's URI says `Patient?_id=<id>` instead of `Encounter?patient=<id>`
- The Encounter section's example links to `Procedure?patient=MRN.XXXXXX`
- Every resource section pastes the identical generic `Patient/id/$export` URI (28 times) instead of resource-specific URIs
- The introduction mentions "USCIS" instead of "USCDI" (appears to be a typo for US Core Implementation Guides or USCDI)

**Could a developer build an import from this documentation?** Only for the FHIR API path, and only if they already know FHIR R4 / US Core. The documentation provides no vendor-specific guidance. The CSC bulk export method — which is the only path described as covering "the entirety of your organization's clinical data" — has no public documentation at all.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The documented EHI export is the vendor's (g)(10) FHIR API relabeled as (b)(10). The 13 FHIR resource types map directly to US Core / USCDI data classes. No native database model is exposed. No vendor-specific entities, custom FHIR profiles, or non-standard data formats are documented. The FHIR infrastructure is third-party (EMR Direct Interoperability Engine), not iCare's own. The undocumented CSC bulk export method *might* be a genuine native export, but without any public documentation it cannot be assessed.

### Key Findings

1. **FHIR/(g)(10) repackaged as (b)(10)**: The 13 FHIR resource types listed on the EHI export page are standard US Core resources. This is the classic pattern of pointing the (g)(10) standardized API at (b)(10) and calling it done. The third-party FHIR server (EMR Direct Interoperability Engine) confirms this is interoperability middleware, not a custom EHI export tool.

2. **Entire billing/RCM module absent**: iCare markets an integrated Revenue Cycle Management module with insurance verification, claims, payments, denial management, and E/M coding. None of this data appears in any documented export method. This is a significant EHI gap — billing records about individuals are part of the designated record set.

3. **CSC bulk export is undocumented**: The most promising export method — a vendor-assisted full data dump described as covering "the entirety of your organization's clinical data" — has zero public documentation. No data dictionary, no format specification, no sample files. It cannot be independently assessed.

4. **Copy-paste errors throughout**: The EHI export page contains multiple copy-paste errors (wrong URIs, wrong resource types in examples, the same generic `$export` URI pasted 28 times). This suggests minimal quality review of the documentation.

5. **No sample data or machine-readable artifacts**: Unlike vendors with strong (b)(10) implementations, iCare provides no sample export files, JSON schemas, data dictionaries, or any machine-readable documentation that would let a developer verify or build against the export.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 JSON (API), C-CDA XML (HIM/CCD), unknown (CSC bulk)
Model type:      Standard projection (US Core FHIR resources)
Entities:        13 FHIR resource types (EHI page); 16 API categories (PDF)
Fields:          ~62 unique field names across API JSON examples; no formal field inventory
Descriptions:    N/A (no data dictionary)
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data + vendor-assisted CSC)
Domains covered: 10 of 19 applicable domains (2 partial)
```

### Bottom Line

iCare's EHI export is a FHIR/C-CDA clinical summary repackaged as a (b)(10) export. It covers standard USCDI clinical data (~10 domains) but omits billing, insurance, payments, scheduling, portal messages, imaging, and orders — all of which the product stores. The single biggest gap is the complete absence of billing/RCM data from the documented export despite the product having an integrated revenue cycle management module. A patient or provider requesting their complete EHI would receive clinical data but miss significant portions of their designated record set.
