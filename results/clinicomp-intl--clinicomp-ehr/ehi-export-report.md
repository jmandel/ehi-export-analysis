# CliniComp, Intl. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://clinicomp.com/ehr-data-export-details/
- CHPL ID: 10998
- Product: CliniComp|EHR v213.03
- Certification date: 2022-10-13

## Navigation Journal

### Step 1: Initial probe of the registered URL

```bash
curl -sI -L "https://clinicomp.com/ehr-data-export-details/" -H 'User-Agent: Mozilla/5.0'
```

Response: HTTP/2 200, Content-Type: text/html; charset=UTF-8, 43,254 bytes. WordPress site hosted on WP Engine. No redirects.

### Step 2: Fetch and examine the page

```bash
curl -sL "https://clinicomp.com/ehr-data-export-details/" -H 'User-Agent: Mozilla/5.0' -o ehi-data-export-details.html
```

The page is a single static WordPress page titled "EHI Data Export Details." It contains only text — no downloadable files (PDFs, ZIPs, schemas, etc.) are linked from this page. No accordion sections or hidden content. The page is rendered with Elementor page builder but all content is in the initial HTML.

### Step 3: Search for downloadable files

```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json|xml|xsd)[^"]*"' ehi-data-export-details.html
```

Result: No downloadable file links found on the EHI export page.

### Step 4: Check the Certified EHR Technology disclosures page

The footer of the EHI export page and the CHPL metadata both link to: https://clinicomp.com/certified-ehr-technology/

```bash
curl -sL "https://clinicomp.com/certified-ehr-technology/" -H 'User-Agent: Mozilla/5.0' -o certified-ehr-technology.html
```

This page contains a section: "CliniComp|EHR API, FHIR, and EHI Export Documentation" with three "here" links:
1. **FHIR documentation**: `http://clinicomp.com/wp-content/uploads/2023/11/FHIR_Api_2_Merged_20231110_01.pdf`
2. **EHI export (b)(10) documentation**: links back to `https://clinicomp.com/ehr-data-export-details/` (the registered URL)
3. **API documentation**: `http://clinicomp.com/wp-content/uploads/2024/02/250-70079_CliniComp_EHR_ONC-API_USCDI.pdf`

### Step 5: Download the linked PDFs

```bash
curl -sL "http://clinicomp.com/wp-content/uploads/2023/11/FHIR_Api_2_Merged_20231110_01.pdf" -H 'User-Agent: Mozilla/5.0' -o FHIR_Api_2_Merged_20231110_01.pdf
curl -sL "http://clinicomp.com/wp-content/uploads/2024/02/250-70079_CliniComp_EHR_ONC-API_USCDI.pdf" -H 'User-Agent: Mozilla/5.0' -o 250-70079_CliniComp_EHR_ONC-API_USCDI.pdf
```

Both confirmed as valid PDFs via `file` command.

### Step 6: Examine the PDFs

**FHIR_Api_2_Merged_20231110_01.pdf** (2,155 pages, 13.1 MB):
- Title: "Terms and conditions Rev 1.0 DRAFT"
- This is a massive auto-generated HAPI FHIR Server API reference. It documents every standard FHIR R4 resource endpoint (Account, ActivityDefinition, AdverseEvent, AllergyIntolerance, Appointment, etc.) with generic CRUD operations. It includes `$export` endpoints at system, Patient, and Group levels. The document reads as a full Swagger/OpenAPI dump of the HAPI FHIR server — it is not EHI-export-specific documentation but rather a comprehensive FHIR R4 API reference for CliniComp's FHIR server.

**250-70079_CliniComp_EHR_ONC-API_USCDI.pdf** (42 pages, 846 KB):
- Title: "CliniComp: Web API & USCDI Dataset — Adaptive Interoperability Platform"
- P/N: 250-70079, Rev D, dated 11 Jan 2024
- This is CliniComp's proprietary REST API documentation for querying USCDI data objects. It defines a custom (non-FHIR, non-standard) web API that returns JSON or XML/HTML responses. The API uses a proprietary naming convention (CCDS.Patient_Name, CCDS.Medications, CCDS.Laboratory_Values, etc.) mapped to internal EHR "Major IT" field identifiers. It includes field-level data dictionaries for 20 USCDI objects, sample API queries, sample JSON responses, and error handling. Pages 28-42 cover Terms of Use.

### Step 7: Screenshots

Took full-page screenshots of both the EHI export page and the Certified EHR Technology disclosures page in Chrome.

## What Was Found

CliniComp's EHI export documentation consists of three components:

### 1. The EHI Data Export Details Web Page (registered URL)

A single-page description of the EHI export mechanism. Key statements:
- The export uses **C-CDA (Consolidated Clinical Document Architecture)** format
- C-CDA files are XML documents using the **CCD (Continuity of Care Document)** template
- The C-CDA sections listed are: Admission Diagnosis, Encounter Data, Implantable Devices, Problems, Social History, Allergies, Discharge Medications, Immunization, Procedures, Smoking Status, Assessment, Hospital Discharge Instructions, Functional Status, Plan of Care, Reason for Referral, Care Team, Health Concerns, Medications, Vital Signs, Cognitive Status, Goals, Results, Laboratory Tests, Payers
- **Export scope**: "Customers can choose to export EHI datasets for a single patient, or all patients within the selected time range"
- **Export formats**:
  - C-CDA v1.0 XML (computable and human-readable)
  - HTML / web page format
  - FHIR DocumentReference for single patients
  - FHIR Bulk Data EHI Export for patient populations per §170.315(b)(10)(ii), with downloads in **C-CDA 2.1 XML** format

The page was published 2023-11-07 and last modified 2023-11-09.

### 2. FHIR Server API Reference (2,155-page PDF)

A comprehensive auto-generated HAPI FHIR R4 server API reference. It documents standard FHIR endpoints for all R4 resource types including `$export` bulk data operations. This is the (g)(10) FHIR API documentation — it is generic FHIR R4, not specific to EHI export content or data coverage.

### 3. Web API & USCDI Dataset (42-page PDF)

CliniComp's proprietary REST API documentation that defines 20 USCDI data objects queryable through a custom web service. Each object has a field-level data dictionary with NAME, TYPE, NULLABLE, DESCRIPTION, and EHR MAJOR IT (internal field identifiers). The objects are:
- Patient_Name, Sex, Date_of_Birth, Race, Ethnicity, Preferred_Language
- Smoking_Status, Problems, Medications, Medication_Allergies
- Laboratory_Tests, Laboratory_Values, Vital_Signs
- Implantable_Device, Procedures, Care_Team_Members
- Immunizations, Health_Concerns, Assessment_Treatment, Goals

A "Full Patient Query" mode (object=ccds.AllData) returns all data for a patient, with output available as XML document or HTML page.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation describes what is essentially a **USCDI/clinical summary export**, not a comprehensive export of all electronic health information. Comparing against the product research:

**Clearly covered (via C-CDA sections and USCDI API objects):**
- Demographics (patient name, sex, DOB, race, ethnicity, preferred language)
- Problems / diagnoses
- Medications
- Allergies (medication allergies only — not food/environmental)
- Laboratory results and tests
- Vital signs
- Procedures
- Immunizations
- Implantable devices
- Care team members
- Smoking status / social history
- Assessment and treatment plans
- Goals
- Health concerns
- Encounter data
- Payers (in C-CDA sections only — no API object for this)

**Notably absent from the export documentation:**
- **Revenue cycle / billing data** — CliniComp|EHR has a full RCM suite (charges, claims, payments, eligibility, authorization, coding). None of this is mentioned in the export.
- **Clinical notes / documentation** — The product stores flowsheets, progress notes, H&P, discharge summaries, consult notes, and multidisciplinary charting. The export mentions "Assessment" and "Hospital Discharge Instructions" as C-CDA sections but does not cover free-text clinical notes, flowsheet data, or specialty documentation.
- **Orders / CPOE data** — The product has a fully integrated CPOE system. No orders are exported.
- **Pharmacy data** — Drug dispensing records, compounding records, BCMA verification logs. Not mentioned.
- **Medical device integration data** — The product captures waveforms, parameters, and settings from bedside devices. Not mentioned.
- **Radiology/imaging** — The product has integrated RIS/PACS. No imaging data or radiology reports in the export.
- **Perinatal/neonatal data** — Fetal monitoring, growth curves, specialized neonatal records. Not mentioned.
- **ED-specific documentation** — Not mentioned.
- **Perioperative/PACU records** — Pre-op, intra-op, post-op documentation. Not mentioned.
- **Behavioral health records** — Not mentioned.
- **Documents and attachments** — External documents incorporated into the patient chart. Not mentioned.
- **Patient portal data** — Not mentioned.

This is a clear case of the **(b)(10) vs (g)(10) confusion**. The export covers the USCDI v1 data classes — the exact same data set required for (g)(10) certification — and nothing more. The 20 CCDS objects in the proprietary API map precisely to USCDI v1 data elements. The C-CDA sections are standard clinical summary sections. There is no evidence of any mechanism to export the vast amount of data a full hospital EHR stores beyond this clinical summary subset.

### Export Format & Standards

CliniComp describes **four** export formats, which is unusually complex:

1. **C-CDA v1.0 XML** — Standard clinical document format. The page says "CCDA version 1.0" which is somewhat ambiguous (C-CDA 1.1 was the first published version in 2012).
2. **HTML** — Web page format for human-readable viewing.
3. **FHIR DocumentReference** — Single-patient export via FHIR, presumably wrapping a C-CDA document.
4. **FHIR Bulk Data Export** — Population-level export per (b)(10)(ii), downloading C-CDA 2.1 XML files. This is notable: the bulk data export produces C-CDA documents, not FHIR NDJSON.

Additionally, the **proprietary Web API** (documented in the 42-page PDF) returns data in a **custom JSON format** — not FHIR JSON, not any standard. The field names are internal identifiers (e.g., "nit", "tkey", "LOINC Code", "MRN") and the response structure is a simple `{success, total, data:[...]}` wrapper.

The presence of a proprietary JSON API alongside standard C-CDA and FHIR mechanisms suggests historical layering of interoperability capabilities, with the proprietary API predating the FHIR adoption.

For a product that stores ICU waveform data, pharmacy compounding records, perioperative documentation, and complex billing — none of which map cleanly to C-CDA sections or USCDI objects — the format choice limits what can be exported. A database dump or CSV export of all tables would be far more appropriate for true (b)(10) compliance.

### Documentation Quality

**Strengths:**
- The proprietary API documentation (250-70079) is well-structured with field-level data dictionaries, including data types, nullability, descriptions, and internal EHR field identifiers.
- Sample API requests, sample JSON responses, and error handling are documented.
- The architecture diagram (Figure 1) showing CCDS → Adapters → Native Data layers demonstrates CliniComp's data normalization approach.
- The document includes screenshots of the EHR interface showing lab results alongside the API output.

**Weaknesses:**
- The EHI export details web page is extremely brief — about 150 words of substance, with no examples, no schema, no detailed field descriptions.
- There is no data dictionary for the C-CDA export. The page lists section names (Allergies, Procedures, etc.) but does not specify which C-CDA templates are used, what coded value sets are applied, or what optional elements are included.
- The FHIR API PDF is a 2,155-page auto-generated API dump that provides no EHI-specific context. It documents every FHIR R4 resource type even though the product likely only populates a subset.
- There is no documentation of the FHIR Bulk Data Export workflow — no instructions for initiating a bulk export, no description of the polling mechanism, no sample requests or responses.
- There are no sample C-CDA files or sample bulk export outputs.
- The "C-CDA version 1.0" designation is unclear and potentially refers to an outdated version (the page elsewhere mentions C-CDA 2.1 for bulk data).

### Structure & Completeness

- **Field-level documentation exists** only for the proprietary USCDI API (20 objects, ~5-10 fields each). The C-CDA and FHIR bulk data export have no field-level documentation.
- **Value sets** are not documented for any export format. Coded fields (e.g., SNOMED-CT for problems, LOINC for labs, CVX for immunizations) are referenced by column name but no value set bindings are specified.
- **Relationships** between entities are implicitly defined by the C-CDA document structure but not explicitly documented.
- **No versioning or change history** is provided for the export format.
- The proprietary API's internal "EHR MAJOR IT" identifiers (e.g., "14074 labresult_ID", "0518 PatientSSN.adm") provide a partial window into the database schema but are not a substitute for comprehensive field documentation.

## Access Summary
- Final URL (after redirects): https://clinicomp.com/ehr-data-export-details/
- Status: found
- Required browser: no (static HTML, no JavaScript required for content)
- Navigation complexity: direct_link (one click to additional PDFs from disclosures page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The registered URL returned HTTP 200 with all content visible.
- The only documentation beyond the web page required navigating to the separate Certified EHR Technology disclosures page (https://clinicomp.com/certified-ehr-technology/) to find the PDF links. The EHI export page itself contains no downloadable files.
- The FHIR API PDF is 2,155 pages but is a generic HAPI FHIR R4 API reference, not EHI-specific documentation. It was included because it documents the FHIR server that supports the bulk data export, but its size is disproportionate to its EHI-specific value.
