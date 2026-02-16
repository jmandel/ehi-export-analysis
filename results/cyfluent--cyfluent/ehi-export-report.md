# Cyfluent — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.cyfluent.com/onc-certified-hit-2015-edition
- Final URL (after 301 redirect): https://www.cyfluent.com/onc-certified-health-it
- CHPL IDs: 10072 (v3.2, certified 2019-08-13), 11546 (v3.3, certified 2024-12-11)
- Developer: Cyfluent (Planned Systems International)

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://www.cyfluent.com/onc-certified-hit-2015-edition" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 301 redirect to `https://www.cyfluent.com/onc-certified-health-it`, which returns HTTP 200. The site is hosted on Wix (Pepyaka server). Content-Type: text/html.

### Step 2: Examine the page (Wix SPA, requires browser)
The page is a Wix-hosted site that renders content via JavaScript. Used Chrome DevTools to navigate and take a snapshot. The page displays:

1. Cyfluent EHR v3.3 certification announcement (December 11, 2024)
2. Drummond Group certification details
3. A "View Certificate" button (opens a dialog)
4. A link to `https://www.cyfluentphr.com/_Files/CURES/` for Real World Testing plans
5. A §170.315(b)(10) attestation section with:
   - Attestation text about single-patient and bulk export capabilities
   - Instructions for both single-patient and bulk export
   - A link to the export format: `https://build.fhir.org/ig/HL7/cda-ccda-2.2/` (C-CDA 2.2 specification)

### Step 3: Explore the CURES directory
```bash
curl -sL "https://www.cyfluentphr.com/_Files/CURES/" -H 'User-Agent: Mozilla/5.0'
```
IIS directory listing revealed:
- `b10 EHI Attestation Information.docx` (45,605 bytes, 2024-01-04)
- `Cyfluent Service Based URL Endpoints.docx` (14,335 bytes, 2024-10-28)
- Several "Real World Test Plans/Results" directories (2022-2026)

Downloaded both .docx files.

### Step 4: Examine the b10 EHI Attestation document
Extracted text from `b10 EHI Attestation Information.docx`. Contains:
- The same attestation text visible on the web page
- **Step-by-step export instructions** for bulk and single-patient export
- Reference to C-CDA 2.2 as the export format
- Document dated 11/7/2023, version reference "3.2.00.3"

### Step 5: Examine the Service Based URL Endpoints document
Contains FHIR API service-base-url endpoints for 7 facilities:
- `cyfluentphr.com/fhirapi/{facilityCode}/service-base-url` (AKMD, HBSH, HUMFA, PGP, PPEET, RCLAYTON, STEIN)
- Reference to SwaggerHub API docs: `https://app.swaggerhub.com/apis-docs/Cyfluent/ProviderPortalApi/3.3#/FHIR/fhir`

### Step 6: Explore SwaggerHub API documentation
Navigated to SwaggerHub in browser. The ProviderPortalApi v3.3 spec includes:
- **FHIR** section: FHIR v4.0.1 service-base-url with dynamic user registration and bulk exporting
- **Security** section: Login/logout process (non-FHIR) with sample code
- **oData** section: Database CRUD operations with full data model access
- **REST (non-FHIR)** section: Endpoints for pulling files, C-CDA documents, prescriptions, and orders

Downloaded the OpenAPI spec:
```bash
curl -sL "https://app.swaggerhub.com/apiproxy/registry/Cyfluent/ProviderPortalApi/3.3" -H 'Accept: application/json'
```

### Step 7: Download referenced artifacts
The Swagger docs reference two ZIP files:
- `https://www.cyfluentchart.com/_Files/Desktop.zip` (69KB) — Contains OData metadata XML and service reference
- `https://www.cyfluentchart.com/_Files/API.zip` (24MB) — Contains C# API client with full OData model and CDA extraction code

Both downloaded successfully. The FhirUnitTests.txt file referenced in the Swagger docs returns 404 (no longer available).

### Step 8: Extract and analyze OData metadata
Extracted `OdataMetadata.xml` (796KB) from Desktop.zip. This is a full EDMX schema of the Cyfluent database model:
- **296 entity types** with **3,159 properties** and **876 navigation properties**
- **438 associations** defining relationships between entities
- Namespace: `CfChartOpModel`

Also extracted C# source files from API.zip, including `Program.cs` which shows a working CDA extraction utility.

## What Was Found

Cyfluent provides EHI export documentation across several artifacts:

### 1. EHI Export Mechanism (b10 Attestation)
The export works through two methods:
- **Single Patient**: Navigate to patient chart → scroll bar shortcut → "Export Patient Data to CCD" → downloads CDA-format file
- **Bulk Export**: Utilities → Files → CDA Extract Configuration → set date range → "Extract now" → downloads CDA-format files

The export format is **C-CDA 2.2** (Consolidated Clinical Document Architecture). The vendor points to the HL7 C-CDA 2.2 specification at `https://build.fhir.org/ig/HL7/cda-ccda-2.2/` as the format documentation.

### 2. Provider Portal API (SwaggerHub)
A comprehensive API with four sections:
- **FHIR v4.0.1** endpoint at `cyfluentphr.com/fhirapi/{facilityCode}/service-base-url` — Inferno-compliant, supports dynamic registration and bulk exporting
- **oData** endpoint at `.../Secure/oData.svc` — Full database CRUD, exposing 296 entity types (the entire data model)
- **REST** endpoints for pulling files (`File.ashx`), C-CDA documents, prescriptions, and orders

### 3. OData Database Schema (Data Dictionary)
The OData metadata XML is effectively a full data dictionary, documenting 296 entity types with field names, data types, nullability, max lengths, and all relationships. Key patient-data entity categories include:

**Patient entities (36)**: Patient, PatientAllergy, PatientAllergyReaction, PatientPrescription, PatientProblem, PatientVital, PatientBodyMeasurement, PatientContact, PatientDiet, PatientFamilyHistory, PatientInsurance, PatientMedication, PatientNote, PatientObGyn, PatientPainHistory, PatientSocialHistory, PatientVision, PatientAdvanceDirective, PatientBloodGlucose, PatientDiabete, PatientEligibilityRequest, PatientPulseOximetry, PatientRace, PatientEthnicity, PatientIdentifier, PatientCarePlan (seen in API code), PatientImplantableDevice (seen in API code), etc.

**Encounter entities (43)**: Encounter (43 properties, 51 nav props), EncounterDiagnosi, EncounterPrescription, EncounterExam, EncounterHpi, EncounterChiefComplaint, EncounterEducation, EncounterPainDescription, EncounterObGyn, EncounterPregnancy, EncounterDsm, EncounterRiskFactor, etc.

**Orders/Actions (25)**: ActionItem (49 properties, 16 nav props — includes lab orders, procedure orders, results, and care plans), ActionItemResult, ActionItemResultValue, etc.

**Code sets (36)**: Full coded terminology tables for ICD, CPT, LOINC, SNOMED, allergies, medications, reactions, diets, advance directives, etc.

### 4. API Client Source Code
The C# `Program.cs` from API.zip demonstrates a working CDA extraction utility that:
- Logs in via API
- Queries patients with encounters in a date range via oData
- Calls `File.ashx?mode=dataccd` to pull C-CDA for each patient
- Also queries individual data tables (allergies, problems, medications, vitals, prescriptions, social history, care plans, goals, health concerns, implantable devices, etc.) via oData

## Export Coverage Assessment

### Data Domain Coverage

The Cyfluent EHI export presents a complex picture. There are actually **two export pathways** documented:

**Pathway 1: C-CDA Export (the certified b(10) mechanism)**
This exports patient data in C-CDA 2.2 format. C-CDA covers a defined set of clinical data sections. Based on the API client code's comments, the CDA export includes:
- Patient demographics (name, sex, DOB, race, ethnicity, preferred language)
- Smoking status
- Problems
- Medications
- Medication allergies
- Laboratory tests and values/results
- Vital signs
- Procedures
- Care team members
- Immunizations
- Unique Device Identifiers (implantable devices)
- Assessment and Plan of Treatment
- Goals
- Health concerns

This is essentially the **USCDI v1 data set** — the same content required for (g)(10) FHIR API certification. It does NOT cover:

- **Billing data**: No claims, charges, payments, A/R, or insurance billing records are included in C-CDA. The product's CyMED/CyCLAIMS modules store extensive billing data (charge ledger, claims, electronic remittance, payer status).
- **Encounter documentation beyond clinical summary**: The rich encounter documentation (43 entity types including HPI, chief complaints, exam sections with nested groups/items, pain descriptions, risk factors, DSM assessments, OB/GYN data, pregnancy tracking) is far more detailed than what C-CDA captures.
- **Custom forms**: The product supports a custom forms builder (DDO — "Dynamic Data Objects") with 9 template entity types. This custom clinical data is not represented in C-CDA.
- **Scanned documents**: The scanning module (ScanPage, ScanPredocument, ScanSegment, ScanSession) stores document images.
- **Patient notes**: PatientNote entity (12 properties) — clinical notes beyond encounter documentation.
- **Occupational health data**: Work-related injuries, OSHA compliance records, hearing exams.
- **Health services management data**: Medical evacuation records, travel clearance, travel immunizations, mental health/substance abuse evaluations.
- **Pharmacy fulfillment data**: Inventory, shipping, barcode tracking.
- **Secure messages**: Patient-provider secure messaging (23 properties per message).
- **Fax records**: Incoming and outgoing faxes with file associations.

**Pathway 2: oData API (indirect access to full data)**
The oData API exposes all 296 entity types — the entire database model. However, this is documented as a general-purpose API for database CRUD, not specifically as the EHI export mechanism. The b(10) attestation specifically describes the C-CDA export as the EHI export format.

This is a classic case where the vendor has the technical capability to export everything (via oData) but has certified the C-CDA export as the b(10) mechanism, which only covers the clinical summary subset.

### Export Format & Standards

- **Primary export format**: C-CDA 2.2 (XML)
- **Standard**: HL7 Consolidated Clinical Document Architecture Release 2.2
- **Appropriateness**: C-CDA is a recognized clinical document standard, but it is a **clinical summary format** designed for care transitions. It is not designed to carry the full breadth of an EHR's data — particularly billing records, custom assessment forms, occupational health data, or pharmacy operations data. For Cyfluent's product scope (comprehensive EHR + PM + occupational health + pharmacy), C-CDA is a significant mismatch.
- **Reconstructability**: A third party could reconstruct a clinical summary from the C-CDA export. They could NOT reconstruct the full patient record — billing history, encounter-level detail, custom forms, scanned documents, and specialty modules would be missing.

### Documentation Quality

**Strengths:**
- The oData metadata XML is an exceptional artifact — a machine-readable, complete schema of 296 entities with typed properties, nullability, max lengths, and relationships. This is unusually detailed compared to most vendors.
- The SwaggerHub API documentation is well-organized with working examples, including JSON response samples and C# client code.
- The API.zip provides a runnable code sample demonstrating the full extraction flow.
- Export instructions are clear and step-by-step.

**Weaknesses:**
- The b(10) attestation document is minimal — a one-page Word document with export instructions and a link to the C-CDA spec. It does not describe what data sections are included in the export or acknowledge any limitations.
- No data dictionary specific to the C-CDA export content (e.g., mapping EHR fields to C-CDA sections/templates).
- No sample export files provided.
- The oData metadata is from 2017 (based on Desktop.zip timestamp). The 2018 API client has ~41 more entities, suggesting the schema has evolved. The current production schema likely has additional entities.
- The FhirUnitTests.txt file referenced in the SwaggerHub docs returns 404.

### Structure & Completeness

**OData schema (de facto data dictionary):**
- Granularity: Excellent. Field-level documentation with names, data types (Edm.String, Edm.DateTime, Edm.Boolean, Edm.Int32, Edm.Guid, etc.), max lengths, nullability, and precision.
- Relationships: Fully documented via 438 associations with referential constraints.
- Code sets: 36 entity types for coded terminology, though actual value set contents are not included (they're data, not schema).
- No field-level descriptions or business logic documentation.

**C-CDA export documentation:**
- Points to the external C-CDA 2.2 specification — no Cyfluent-specific mapping guide.
- No documentation of which C-CDA templates are populated or which optional sections are included.
- No sample export files.

## Access Summary
- Registered URL: https://www.cyfluent.com/onc-certified-hit-2015-edition
- Final URL (after redirect): https://www.cyfluent.com/onc-certified-health-it
- Status: found
- Required browser: yes (Wix SPA for initial page, but linked documents accessible via curl)
- Navigation complexity: one_click (main page has direct links to CURES directory)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered URL redirects (301) to a slightly different path (`/onc-certified-health-it` instead of `/onc-certified-hit-2015-edition`)
- The Wix-hosted page requires JavaScript to render content (curl returns empty-looking HTML)
- `FhirUnitTests.txt` referenced in SwaggerHub docs returns 404 at `https://www.cyfluentphr.com/_files/CURES/FhirUnitTests.txt`
- The EULA PDF referenced in the SwaggerHub license field also returns 404
- Parent directory `https://www.cyfluentphr.com/_Files/` returns 403 Forbidden
- The oData metadata XML (Desktop.zip) dates from 2017, pre-dating the current version 3.3. The C# connected reference from 2018 has ~41 additional entity classes, suggesting schema evolution.
