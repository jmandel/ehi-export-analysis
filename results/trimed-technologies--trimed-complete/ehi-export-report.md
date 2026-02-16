# TriMed Technologies — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.trimedtech.com/EHRDisclosureV10
- CHPL IDs: 10076
- CHPL Product Number: 15.05.05.3103.TRIC.01.00.1.190820
- Certification Date: 2019-08-20

## Navigation Journal

### Step 1: Initial probe of the registered URL

```bash
curl -sI -L "https://www.trimedtech.com/EHRDisclosureV10" -H 'User-Agent: Mozilla/5.0'
# Returns HTTP 405 for HEAD, but GET returns 200
curl -sL "https://www.trimedtech.com/EHRDisclosureV10" -H 'User-Agent: Mozilla/5.0' -o page.html
```

The page is a mandatory disclosures page titled "Certification COSTS of TriMed Complete Version 1." It contains vendor information, a full list of certified criteria (including 170.315(b)(10) Electronic Health Information export), clinical quality measures, leveraged software, and cost disclosures. The entire EHI export documentation on this page is a single sentence:

> **Electronic Health Information Export:** Electronic patient health information may be exported in XML format in CCDA architecture. TriMed Complete regularly updates the CCDA format to meet the current HL7 Clinical Document Architecture standards as set forth at: https://www.hl7.org/implement/standards/

### Step 2: Explored the /certifications page

From the main disclosure page, the `/certifications` page was discovered. It links to:
- "Cost for EHR Certification, TriMed Complete Version 1" → /ehrdisclosurev10 (same page)
- "TriMed Patient Data API" → https://patientapi.trimedtech.com/
- "Real World Testing" → /rwtplan
- "TriMed Complete FHIR API" → /fhirapi

### Step 3: Investigated the Patient Data API (SOAP)

```bash
curl -sL "https://patientapi.trimedtech.com/" \
  -H 'User-Agent: Mozilla/5.0' \
  -H 'Referer: https://patientapi.trimedtech.com/' \
  -o patientapi-homepage.html
```

This is a single-page application (all content loaded via anchor navigation) documenting a **SOAP-based Patient Data API (v1.3)**. The site requires `Referer: https://patientapi.trimedtech.com/` header for resource access (images, XML files). It contains:

- **Authentication** documentation (practice-generated keys)
- **LookupPatientId** method (find patient by demographics)
- **GetPatientData** method (comprehensive C-CDA export with 25+ boolean flags controlling which data types to include)
- **8 individual data-type methods**: GetPatientAllergy, GetPatientProblemList, GetPatientMedication, GetPatientImmunization, GetPatientLabResult, GetPatientEncounter, GetPatientEncompassingEncounter, GetPatientVitals
- Sample SOAP request/response XML for each method
- Request parameter tables, response parameter tables, response codes
- **Underlying SQL queries** in hidden "Internal Use Only" sections revealing Oracle database table names and column structures

### Step 4: Investigated the FHIR API

```bash
curl -sL "https://www.trimedtech.com/fhirapi" -H 'User-Agent: Mozilla/5.0' -o fhirapi-page.html
```

The FHIR API page documents a RESTful API conforming to FHIR R4 (4.0.1), US Core IG v6.1.0, USCDI Version 3, and SMART on FHIR. Key endpoints discovered:
- **CapabilityStatement**: https://fhir.trimed.cloud/metadata (downloaded successfully)
- **SMART config**: https://fhir.trimed.cloud/.well-known/smart-configuration (downloaded)
- **Swagger docs**: https://fhir.trimed.cloud/swagger/index.html (OpenAPI spec downloaded)
- **FHIR Documentation PDF**: 54-page PDF with sample JSON responses for all resource types (downloaded via https://www.trimedtech.com/a/uploads/122667)
- **Developer Portal**: https://fhir-developer.trimed.cloud

### Step 5: Downloaded the SOAP API WSDL

```bash
curl -sL "https://svcs-ccd.trimed.cloud/PatientAPI.asmx?WSDL" -H 'User-Agent: Mozilla/5.0' -o PatientAPI-WSDL.xml
```

Downloaded successfully. The WSDL defines all 10 SOAP methods with full XML Schema type definitions.

### Step 6: Downloaded XML sample responses with Referer header

```bash
for f in GetPatientAllergy GetPatientData GetPatientEncounter GetPatientImmunization \
         GetPatientLabResult GetPatientMedication GetPatientProblemList GetPatientVitals LookupPatientId; do
  curl -sL "https://patientapi.trimedtech.com/Xml%20Files/${f}.xml" \
    -H 'User-Agent: Mozilla/5.0' -H 'Referer: https://patientapi.trimedtech.com/' \
    -o "xml-samples/${f}.xml"
done
```

All 9 files downloaded successfully (680 bytes to 36KB). The GetPatientData.xml is a complete C-CDA document with 16 sections.

### Step 7: Downloaded Postman screenshot images

```bash
for img in LookupPatientIdRequest PatientLookupResponse PatientDataRequest \
           PatientDataResponse AllergyRequest PatientAllergyResponse; do
  curl -sL "https://patientapi.trimedtech.com/Image/${img}.png" \
    -H 'User-Agent: Mozilla/5.0' -H 'Referer: https://patientapi.trimedtech.com/' \
    -o "patientapi-images/${img}.png"
done
```

### Step 8: Attempted S3-hosted CCDA sample

```bash
curl -sL "https://trimed-public-docs.s3.amazonaws.com/18180.xml" -H 'User-Agent: Mozilla/5.0'
# Returns 403 Forbidden — access denied
```

This S3-hosted XML file (linked from the Patient API page) is not publicly accessible.

## What Was Found

TriMed Technologies provides two separate API systems for accessing patient data, plus a minimal one-sentence description of EHI export on their mandatory disclosure page.

### 1. Mandatory Disclosure Statement (EHI Export)

The registered URL is a mandatory disclosure page. The EHI export documentation consists of a single sentence stating that patient data "may be exported in XML format in CCDA architecture." There is no data dictionary, no field-level documentation, no export instructions, and no mention of how to actually trigger an export or what data it includes beyond "electronic patient health information."

### 2. TriMed Patient Data API (SOAP, v1.3)

This is the more substantial documentation. It describes a SOAP-based API at `https://svcs-ccd.trimed.cloud/PatientAPI.asmx` that:

- Returns patient data as **C-CDA (Consolidated Clinical Document Architecture)** XML documents
- Requires authentication via practice-generated keys
- Supports 10 methods: LookupPatientId, GetPatientData (comprehensive), and 8 individual data-type methods
- The **GetPatientData** method accepts 25+ boolean parameters controlling which data types to include:
  - `bAllergies`, `bProbs`, `bMeds`, `bImmunizations`, `bAdvDirectives`
  - `bResults`, `bNoteData`, `bVitals`, `bSmokingStatus`, `bProcedure`
  - `bCareTeamMembers`, `bUDI`, `bAssessmentPlan`, `bGoals`, `bHealthConcerns`
  - `bLabTests`, `bConfid` (confidential items)
  - Demographics: `bPatientName`, `bDOB`, `bGender`, `bRace`, `bEthnicity`, `bPreferredLang`
  - `bLimitPage` (all demographics)
- Supports date filtering via `dStartDate`, `dEndDate`, `lRelativeDays`

The C-CDA sample response (GetPatientData.xml) contains these sections:
- Encounters
- Allergies and Adverse Reactions
- Conditions or Problems
- Medications
- Immunizations
- Reason For Visit / Chief Complaint
- Functional and Cognitive Status
- Instructions
- Reason for Referral
- Procedures
- Medical Devices
- Assessment and Plan of Treatment
- Diagnostic Results (Lab)
- Social History
- Vital Signs

The hidden "Internal Use Only" SQL queries reveal an Oracle database with tables prefixed `pr1_` (inherited from the e-Medsys product), including: `PR1_View_Patient`, `pr1_allergies`, `pr1_problem_list`, `pr1_patient_drug`, `pr1_patient_immunization`, `pr1_lab_result_req/set/item/value`, `pr1_patient_note`, `pr1_patient_note_control`, `pr1_view_doctor`, `pr1_view_department`, `pr1_template`, `pr1_template_field`, `pr1_lookups`.

### 3. TriMed FHIR API (R4)

A separate FHIR R4 API conforming to US Core IG v6.1.0 and USCDI v3. The CapabilityStatement lists 26 resources:
AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen.

The CapabilityStatement declares `http://hl7.org/fhir/uv/bulkdata/CapabilityStatement/bulk-data` as an instantiation, and the OpenAPI spec includes bulk export endpoints (`/Group/{id}/$export`, `/Patient/$export`), indicating FHIR Bulk Data support.

A 54-page FHIR Documentation PDF provides sample JSON responses for each resource type.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered** (via the SOAP API/C-CDA export):
- Demographics (name, DOB, gender, race, ethnicity, preferred language)
- Allergies and adverse reactions
- Problem list / conditions (with SNOMED coding)
- Medications (name, strength, route, frequency, dates)
- Immunizations (vaccine, date, status, manufacturer, lot number)
- Lab results (LOINC-coded, with values, units, ranges, flags)
- Vital signs
- Encounters (type, provider, location, date, diagnosis)
- Clinical notes (via encounter data and note_datetime)
- Procedures
- Medical devices (UDI)
- Assessment/plan of treatment
- Goals
- Health concerns
- Care team members
- Social history (smoking status)
- Advance directives

**Covered via FHIR API but not the SOAP/C-CDA system:**
- Coverage (insurance) — FHIR resource present but no SOAP method for it
- ServiceRequest — FHIR resource present
- Specimen — FHIR resource present
- DocumentReference — FHIR resource present
- MedicationDispense — FHIR resource present

**Absent from both APIs — significant gaps for b(10):**
- **Billing data** — No billing records, claims, charges, payments, or financial data exposed through either API. The product stores billing/RCM data (claims management, collections, EDI transactions, consolidated family balances), but none of this is available in the export.
- **Prescription history / e-prescribing records** — Only active medications are exported via the SOAP API. E-prescribing transaction history (Surescripts interactions, EPCS records) is not included.
- **Patient-generated data** — Portal messages, self-reported demographics, electronic form submissions, digital check-in data
- **Scanned documents and images** — OCR-processed documents, scanned insurance cards, referral documents, handwritten notes. The FHIR API includes DocumentReference but it's unclear if the b(10) export mechanism surfaces these.
- **Family account linkages** — Guarantor information, consolidated family balances (pediatric-specific feature)
- **Referral and authorization tracking** — Authorization records for referrals and treatment
- **Telemedicine session records**
- **AI-generated documentation** — Amazon HealthScribe summaries, AI-generated HPI/assessment/plan

### Export Format & Standards

The product uses **two distinct export formats**:

1. **C-CDA XML** (via SOAP Patient Data API) — This is the export mechanism referenced in the mandatory disclosure. It produces HL7 C-CDA 2.1 documents that cover the clinical data domains listed above. This is a recognized standard and well-suited for clinical summaries.

2. **FHIR R4 JSON** (via FHIR API) — Conforming to US Core v6.1.0/USCDI v3. This is the g(10) certified API. It supports bulk data export.

**Critical assessment**: Neither mechanism provides a true b(10) export of **all electronic health information**. The C-CDA export covers the clinical data that maps neatly to CDA sections but omits billing, financial, and administrative data. The FHIR API covers US Core resources — a defined subset of clinical data. The disclosure page makes no distinction between b(10) and g(10), and there is no documentation of a separate mechanism for exporting the full designated record set.

The SOAP API is the more honest b(10) mechanism — it at least provides a dedicated per-patient data retrieval system with configurable data types. But it still doesn't export billing records, documents/images, or other non-clinical EHI.

A third party could reconstruct much of the clinical record from the C-CDA export, but would be missing billing data, scanned documents, e-prescribing history, and practice management data.

### Documentation Quality

**Patient Data API (SOAP)**: Good quality for what it covers. The documentation includes:
- Clear API method descriptions with request/response parameter tables
- Sample SOAP XML for each method
- Sample C-CDA responses demonstrating actual data structure
- Response codes and error handling
- Authentication workflow with step-by-step Postman examples
- Date filtering capabilities documented
- Hidden underlying SQL (labeled "Internal Use Only") revealing database schema

**FHIR API**: Adequate. The documentation includes:
- CapabilityStatement (machine-readable)
- OpenAPI/Swagger spec (machine-readable, but schemas are empty `{}` objects)
- 54-page PDF with sample JSON responses for each resource
- SMART on FHIR authentication flow
- Developer portal and sandbox access

**Mandatory Disclosure Page**: Extremely poor. A single sentence about C-CDA export with no actionable detail.

**Overall**: The technical API documentation is functional but neither system documents a comprehensive b(10) export. There's no data dictionary mapping internal database fields to export fields. There's no export user guide for practice administrators. The documentation reads as g(10)/API compliance documentation, not b(10) EHI export documentation.

### Structure & Completeness

**Field-level documentation**: The SOAP API provides parameter-level documentation (parameter name, type, required, description) for requests and responses. The response field descriptions are brief but usable (e.g., "Drug Strength (e.g., '5mg', '200mg/5mL')").

**Coded fields**: SNOMED is used for diagnoses/problems, LOINC for lab results, CVX for immunizations. Value set documentation is by reference to external standards only — no vendor-specific value sets are documented.

**Relationships**: Implicitly documented through the SQL queries (foreign keys visible in JOIN conditions) but not formally documented.

**Versioning**: The Patient Data API is version 1.3. No change history is provided. The FHIR API declares v1.0.0.

**Missing**: No ERD or schema diagram. No data dictionary document. No mapping between API fields and database fields. No documentation of custom or specialty-specific data models (pediatric growth charts, specialty templates, etc.).

## Access Summary
- Final URL (after redirects): https://www.trimedtech.com/ehrdisclosurev10
- Status: found
- Required browser: no (curl works, but Referer header required for Patient API resources)
- Navigation complexity: multi_page (disclosure → certifications → API docs across 3 sites)
- Anti-bot issues: Referer header required for patientapi.trimedtech.com resources; S3-hosted file returns 403

## Obstacles & Dead Ends
- HEAD requests to trimedtech.com return HTTP 405 (Method Not Allowed) — GET works fine
- All resources on `patientapi.trimedtech.com` (images, XML files, sub-pages) require `Referer: https://patientapi.trimedtech.com/` header or they return 403
- The Patient API site is a single-page app — sub-page URLs like `/Authentication.html` return 404; all content is in the main page, toggled via JavaScript
- S3-hosted sample CCDA (`https://trimed-public-docs.s3.amazonaws.com/18180.xml`) returns 403 Forbidden
- The "Underlying SQL" sections in the Patient API docs are in hidden divs labeled "Internal Use Only" — not visible without JavaScript manipulation to show all sections
- The FHIR Swagger spec has empty schema objects (`{}`) for request/response bodies, limiting machine-readability
- The FHIR Documentation PDF was discovered on a separate page (`/FHIR_Documentation`) linked from the `/fhirapi` page as "Response Examples" — not directly findable from the disclosure URL
