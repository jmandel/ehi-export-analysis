# EHI Export Analysis: QRS, Inc.

**Product**: PARADIGM® (EHR + Practice Management)  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2838.PARA.22.01.1.221227

## 1. Product Context

PARADIGM® is an integrated ambulatory EHR and Practice Management (PM) suite developed by QRS, Inc. (Knoxville, TN, est. 1983; acquired by Harris Computer / Constellation Software in May 2024). The product consists of two tightly integrated modules sharing a single database:

- **PARADIGM EHR**: Clinical documentation with customizable templates, e-prescribing (FDA drug database), speech recognition/dictation (.wav files stored per encounter), scanning/document management (PDF/PNG/etc.), patient flow, work lists, fax integration, recalls, and a patient portal.
- **PARADIGM PM (PARADIGM+)**: Appointment scheduling, charge posting (single-screen charges/payments/adjustments), claims management with clearinghouse integration, ERA processing, insurance eligibility, patient/guarantor billing, E/M coding assistance, and inventory management.

The product targets small to mid-size ambulatory practices across 50+ specialties. Optional modules include HL7 interfaces (lab, radiology), insurance contract management, referral management, claims tracking, and specialty-specific modules (radiology, allergy, chiropractic, ambulance billing).

The product is certified for 37 ONC criteria including (b)(10) EHI export, (g)(10) FHIR API, clinical documentation, e-prescribing, care coordination, clinical quality measures, public health reporting (immunization, syndromic surveillance, cancer case), and direct messaging.

**Baseline expectation for (b)(10)**: Given the integrated EHR+PM architecture, a genuine EHI export should cover clinical data (demographics, problems, medications, allergies, immunizations, vitals, labs, notes, procedures, encounters) AND billing/PM data (charges, claims, payments, insurance, appointments linked to care).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `PARADIGM_EHI_Export_Documentation.pdf` (163 KB, 6 pages) | Core (b)(10) EHI export documentation. 4 pages of Terms & Conditions boilerplate, 2 pages of technical content describing export structure and API endpoints. **No data dictionary, no schema, no sample data.** | **Primary artifact — extremely thin** |
| `PARADIGM_FHIR_API_Documentation.pdf` (279 KB, 27 pages) | (g)(10) FHIR R4 API documentation. OAuth 2.0/PKCE auth, 15 US Core resource types with request/response parameters. Standard FHIR API — separate from EHI export. | Reference only — documents (g)(10), not (b)(10) |
| `PARADIGM_Patient_API_Documentation.pdf` (160 KB, 6 pages) | Non-FHIR REST API for patient search and C-CDA retrieval. Same 4 pages T&C, 2 pages technical. Same endpoints referenced in EHI export doc. | Low — duplicates EHI export doc endpoints |
| `qrshs-info-main-page.html` (29 KB) | QRS Disclosures page listing all compliance documents, RWT plans/results, and API documentation links. | Orientation only |

**Most informative**: `PARADIGM_EHI_Export_Documentation.pdf` — the sole (b)(10) document, though it contains only 2 pages of technical substance.

**Least informative**: The FHIR API and Patient API docs are standard interoperability documentation and do not describe (b)(10) export content.

## 3. Export Mechanics

- **Format**: ZIP file containing:
  1. **C-CDA XML** (CCD) — one per patient, named by patient code (e.g., `10000.xml`)
  2. **Supplemental JSON** — additional data files named by type and patient code (e.g., `10000_invoice history.json`)
  3. **Attached files** — files imported into the EHR in original format (PDF, PNG, etc.), placed in a `_addt_files` subdirectory per patient (e.g., `10000_addt_files/`)

- **Mechanism**:
  - **UI**: Via EHR System Reports, authorized users access the "Data Portability module." A checkbox labeled "include all Electronic Healthcare Information (EHI) for each patient in the set" must be checked.
  - **API**: REST API at `api.qrshs.com/v1/` with Basic authentication for patient search (`/patient/search`) and C-CDA retrieval (`/patient/ccda`). The API documentation only describes C-CDA retrieval; it's unclear whether the API also returns the supplemental JSON and attached files that the UI export includes.

- **Single-patient vs. bulk**: The UI appears to support "a patient or set of patients." The API retrieves data one patient at a time.

- **Access constraints**: API access requires a Developer Account established "through direct consultation and permission of a QRS Client." Terms include whitelisting, registration, and a dually-executed agreement with the QRS client.

## 4. Export Content: What's In It

### What we know

The EHI export documentation provides **no data dictionary whatsoever**. There is no enumeration of fields, tables, entities, or data elements. There is no schema for the JSON files. There is no sample data. The entire technical description of the export content is captured in a single paragraph:

> "Data is exported in a zip format (.zip) and contains standard CCDA (.xml) as well as other available information for each patient included. Additional information is included in a JSON (.json) while information imported into the EHR will be included in the format in which it was received (ex PDF/PNG/etc)."

The only concrete data type mentioned by name is **"invoice history"** as an example of what might appear in supplemental JSON files. No schema, no field list, no indication of what other JSON files might be included.

### Vendor's own content organization

The vendor does not organize or categorize their export content. The only structure provided is format-based:

| Component | Fields Documented | Field Descriptions | Types Documented | Category (vendor's) |
|---|---|---|---|---|
| C-CDA XML (CCD) | 0 | N/A | N/A | "standard CCDA" |
| Supplemental JSON | 0 | N/A | N/A | "other available information" |
| Attached files | 0 | N/A | N/A | "format in which it was received" |

**Total documented entities**: 3 (by format type only)  
**Total documented fields**: 0  
**Fields with descriptions**: 0  

### What we can infer (but cannot confirm)

1. **C-CDA content**: As a "standard CCDA" CCD, it would contain the typical C-CDA sections: demographics, problems, medications, allergies, immunizations, vitals, procedures, results, encounters, care plans. This is USCDI-scope clinical data — the same content available through the (g)(10) FHIR API.

2. **Supplemental JSON**: The "invoice history" example suggests some billing data may be included. But we don't know:
   - What other JSON files are generated
   - What fields the invoice history JSON contains
   - Whether it includes charges, payments, adjustments, insurance details, or just a summary
   - Whether there are JSON files for other data domains (scheduling, referrals, insurance, etc.)

3. **Attached files**: Documents and images that were imported/scanned into the EHR are included in original format. This is good for completeness of the document record.

### FHIR API (g)(10) — for reference

The separate FHIR API documentation covers 15 US Core resource types with 88 total response fields:

| Resource | Response Fields |
|---|---|
| Patient | 3 |
| AllergyIntolerance | 1 |
| CarePlan | 5 |
| CareTeam | 3 |
| Condition | 6 |
| Device | 13 |
| DiagnosticReport | 8 |
| DocumentReference | 2 |
| Goal | 5 |
| Immunization | 7 |
| MedicationRequest | 11 |
| Observation | 7 |
| Procedure | 5 |
| Encounter | 9 |
| Provenance | 3 |

These are standard US Core profiles — the regulatory floor for clinical exchange.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides almost no detail about what data the EHI export covers. The documentation describes **how** the export is structured (C-CDA + JSON + files in a ZIP) but not **what** is in it.

The only evidence of content beyond standard C-CDA is:
1. The mention of **"invoice history"** as a supplemental JSON file — suggesting some billing/financial data
2. The **attached files** inclusion — suggesting scanned documents and imported files
3. The **"include all EHI" checkbox** — suggesting the system has a broader vs. narrower export mode

The vendor does not categorize, list, or describe their export content in any meaningful way. There are no "sections," "modules," or "categories" of data described.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (inferred) | C-CDA CCD would include standard demographics | Product stores demographics (certified (a)(3)); C-CDA covers basics but depth unknown |
| Encounters / visits | ⚠️ Partial (inferred) | C-CDA encounter sections | Product stores encounter data; C-CDA covers basics |
| Problems / conditions | ⚠️ Partial (inferred) | C-CDA problem list section | Product has problem list (certified (a)(5)); C-CDA covers basics |
| Medications / prescriptions | ⚠️ Partial (inferred) | C-CDA medications section | Product has e-prescribing with FDA drug database; C-CDA covers basics but MAR depth unknown |
| Allergies | ⚠️ Partial (inferred) | C-CDA allergies section | Product stores allergies (certified (a)(2)); C-CDA covers basics |
| Immunizations | ⚠️ Partial (inferred) | C-CDA immunizations section | Product stores immunizations (certified (f)(1)); C-CDA covers basics |
| Vitals | ⚠️ Partial (inferred) | C-CDA vitals section | Likely covered at basic level via C-CDA |
| Lab results | ⚠️ Partial (inferred) | C-CDA results section | Product has optional HL7 lab interfaces; C-CDA covers basics if labs are present |
| Imaging / diagnostic reports | ⚠️ Partial (inferred) | C-CDA diagnostic reports section, possible attached files | Unclear depth; optional radiology module exists |
| Procedures | ⚠️ Partial (inferred) | C-CDA procedures section | C-CDA covers basics |
| Clinical notes / documents | ⚠️ Partial | C-CDA clinical notes sections + attached files in `_addt_files` | Product stores notes, scanned docs, voice recordings (.wav), faxes; attached files may capture some of this |
| Care plans / goals | ⚠️ Partial (inferred) | C-CDA care plan section | C-CDA covers basics |
| Family health history | ⚠️ Partial (inferred) | C-CDA family history section | Product certified for (a)(12); C-CDA covers basics |
| Orders / referrals | ❌ Not confirmed | No evidence in documentation | Product has optional referral management module; no export documentation |
| Insurance / coverage | ❌ Not confirmed | No evidence beyond possible inclusion in supplemental JSON | Product manages insurance eligibility and verification; not documented in export |
| Claims / billing | ⚠️ Unclear | "invoice history" mentioned as supplemental JSON example | Product has full billing/claims/ERA capability; only evidence is an undocumented JSON file name |
| Payments | ❌ Not confirmed | No evidence in documentation | Product manages payments and adjustments; not documented in export |
| Consents / directives | ❌ Not confirmed | No evidence in documentation | Unknown if product stores advance directives |
| Patient communications / portal | ❌ Not confirmed | No evidence in documentation | Product has patient portal; no evidence portal messages are exported |
| Specialty-specific data | ❌ Not confirmed | No evidence in documentation | Product supports 50+ specialties with optional modules; no export documentation |
| Implantable devices | ⚠️ Partial (inferred) | C-CDA device section, FHIR Device resource | Product certified for (a)(14); C-CDA covers basics |

**Key observation**: Nearly every domain is marked "inferred" because the documentation provides no explicit enumeration of export content. We are inferring C-CDA section coverage based on the C-CDA standard, not based on anything the vendor documented. The only domain with any non-C-CDA evidence is billing (via the "invoice history" JSON mention).

## 6. Documentation Quality

The EHI export documentation is **critically deficient**:

- **No data dictionary**: Zero fields documented for any export component
- **No schema**: No JSON schema for supplemental files, no C-CDA template specification
- **No sample data**: No examples of what the export output looks like
- **No field-level detail**: Not even a list of what C-CDA sections are included
- **No relationship documentation**: No foreign keys, no entity relationships
- **No value sets**: No code systems or coded values documented

**What is documented**: The export ZIP structure (3 types of files), the UI access path (System Reports > Data Portability), the API endpoints (patient search + C-CDA retrieval), and the naming convention for files.

**Could a developer build an import from these docs?** No. A developer would receive a ZIP file and have to reverse-engineer its contents. The C-CDA portion is at least a recognized standard, but the supplemental JSON files are entirely undocumented — no schema, no field list, no examples. The developer would have no way to know what JSON files to expect, what they contain, or how to parse them.

**Positive note**: The documentation does clearly describe the mechanism for triggering the export and the high-level file structure, which is more than some vendors provide. The mention of an "include all EHI" checkbox suggests awareness of the (b)(10) requirement.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess the actual breadth of the export. The core clinical data is almost certainly present via C-CDA (this is standard), but the depth within those domains and the coverage of non-clinical domains (billing, PM, specialty data) is entirely undocumented. The single mention of "invoice history" as a JSON file suggests the vendor may have included some billing data, but without any field documentation, schema, or sample data, it's impossible to verify what's actually exported or how complete it is. Given that PARADIGM is a full EHR+PM system with billing, claims, scheduling, and multi-specialty features, the lack of documentation for any of these domains is a significant concern.

**Axis 2 — Export approach: Partially purpose-built, but documentation is too thin to fully assess**

The export structure — C-CDA plus supplemental JSON files plus attached documents — indicates that QRS built something beyond just a standard C-CDA export. The supplemental JSON layer (e.g., "invoice history") and the attached files directory are purpose-specific additions that go beyond what a standard C-CDA or FHIR (g)(10) export would include. The "include all EHI" checkbox in the UI also suggests a deliberate (b)(10) effort. However, the C-CDA component is the same C-CDA retrievable through the Patient API, and the supplemental JSON layer is so undocumented that it's impossible to assess its actual depth. This is a partially purpose-built export with elements of repackaging (the C-CDA core) and genuinely new export capability (supplemental JSON, attached files) — but the documentation failure makes it impossible to confirm the actual scope.

### Key Findings

1. **Documentation is critically thin**: The entire EHI export is described in 2 pages of technical content (out of a 6-page PDF that is 67% legal boilerplate). Zero fields are documented. No data dictionary, no schema, no sample data. This is one of the thinnest (b)(10) documentation packages we could encounter.

2. **Export structure suggests partial effort beyond C-CDA**: The ZIP format with C-CDA + supplemental JSON + attached files indicates the vendor built more than just a C-CDA export. The "invoice history" JSON example and the "include all EHI" checkbox suggest some awareness of covering billing data beyond clinical summaries.

3. **Billing/PM data coverage is almost entirely undocumented**: PARADIGM has a full practice management suite (charges, claims, ERA, insurance, payments), but the only evidence of billing data in the export is the mention of an "invoice history" JSON file name. No fields, no schema, no indication of coverage depth.

4. **API-based retrieval appears to only return C-CDA**: The Patient API's `/patient/ccda` endpoint returns an XML document (C-CDA). It's unclear whether the supplemental JSON and attached files are accessible via API or only through the UI export.

5. **The (g)(10) FHIR API is a separate, better-documented system**: The FHIR API documentation (27 pages, 15 resources, 88 fields) is substantially more detailed than the EHI export documentation. This makes the (b)(10) documentation look even more neglected by comparison.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Unclear (elements of purpose-built, but documentation too thin to confirm)
    Export format:   ZIP (C-CDA XML + JSON + attached files in original format)
    Entities:        3 (by format type only; no entity-level documentation)
    Fields:          0 documented
    Descriptions:    N/A (0 fields)
    Sample data:     No
    Bulk export:     Yes (UI supports "set of patients")
    Domains covered: ~1 confirmed (clinical via C-CDA), 1 hinted (billing via "invoice history"), rest unknown

### Bottom Line

A patient or provider requesting their EHI from PARADIGM would receive a ZIP file containing a standard C-CDA clinical summary, some undocumented JSON files (possibly including invoice history), and any scanned/imported documents. The clinical summary portion would cover basic USCDI-scope data, but there is no way to know from the documentation whether billing, insurance, specialty-specific, or practice management data is meaningfully included. The single biggest gap is the complete absence of a data dictionary — with zero fields documented, this (b)(10) implementation cannot be independently verified or used by a developer to build a data import.
