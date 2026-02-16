# EHI Export Analysis: eDerm Systems LLC

**Product**: eDerm Systems v2.8.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2592.eDer.28.00.1.191025

## 1. Product Context

eDerm Systems is a dermatology-specific EHR, practice management, and revenue cycle management (RCM) platform built by eDerm Systems LLC (Boca Raton, FL). It targets dermatology practices (1–50 physicians) including cosmetic dermatology, Mohs surgery, and dermatopathology. The EHR runs as a native iPad application; practice management and RCM modules run as browser-based web apps, all against a shared cloud backend.

Key data domains the product stores:

- **Clinical charting**: "One-Touch Charting" with 3D anatomical maps, dermatology-specific exam templates, structured clinical notes
- **Clinical photography**: Unlimited photos linked to encounters — a core dermatology feature
- **Pathology lifecycle**: Biopsy orders, requisitions, pathology results, status tracking, biopsy logs — a distinctive specialty feature
- **Cancer tracking**: Follow-up tracking for patients with cancer diagnoses
- **Demographics and patient registration**
- **Practice management**: Scheduling, insurance verification, phone messages, multi-location support
- **Revenue cycle management**: Smart Coder (automated CPT/ICD-10 coding), claims (primary/secondary/tertiary), payment posting, collections, financial reporting
- **Patient portal** (via Updox integration): Secure messaging, record access
- **Document management**: Scanned documents, consent forms, prescriptions, lab requisitions

The product was ONC certified on 2019-10-25 for criteria including (b)(10) EHI export, along with (g)(9)/(g)(10) FHIR/API, and (b)(1)/(b)(2) transitions of care.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `eDerm-API-Documentation-G8-G9.pdf` (584 KB, 26 pages) | Proprietary REST API documentation covering OAuth authentication, patient search, encounter listing, and patient data retrieval via C-CDA. Documents the (g)(9)/(g)(10) API. Created 2022-08-08 by Juan Benedit. | **Most informative** — the only technical documentation available |
| `ValidURLs.json` (4 KB) | FHIR Endpoint Bundle with two Organization/Endpoint pairs registering the FHIR service base URL. A (g)(10) registration artifact. | Low — infrastructure only |
| `ederm-onc-certified.html` (61 KB) | eDerm's ONC certification/mandatory disclosures page. Contains Drummond Group letter, API doc link, ValidURLs link, Real World Testing links. | Moderate — confirms no (b)(10) documentation exists on this page |
| `ederm-onc-certified-page.png` (478 KB) | Full-page screenshot of the ONC certification page. | Low — visual backup |
| `fhir-endpoint-cert-expired.png` (74 KB) | Screenshot showing SSL certificate expiry error for the FHIR endpoint. | Low — documents endpoint failure |

**No data dictionary, export schema, sample export files, or (b)(10)-specific documentation exists among the artifacts.**

## 3. Export Mechanics

**No dedicated EHI export mechanism is documented.** The only documented data access mechanism is a proprietary REST API (not FHIR) described in `eDerm-API-Documentation-G8-G9.pdf`:

- **Format**: C-CDA 2.1 XML (also JSON and HTML options via `returnformat` parameter)
- **Mechanism**: REST API with OAuth-style authentication (username/password grant) — requires programmatic access
- **Scope**: Single-patient at a time via `GetPatientData` endpoint; no bulk export capability documented
- **Access constraints**: Requires valid credentials; sample URLs reference an internal hostname (`remotedev-5`), not a production endpoint
- **Fees**: Unknown — "Terms of Use: TBD: Link will be added here" in the documentation, suggesting terms were never finalized

The CHPL-registered EHI documentation URL (`https://fhir.ederm.io:9443/fhir-server/api/v4/metadata`) is non-functional:
- SSL certificate expired 2026-02-10 (Let's Encrypt)
- Server returns HTTP 404 on all FHIR paths (Tomcat running but FHIR application undeployed)
- Verified independently on 2026-02-16: `curl -sk` returns HTTP 404 with SSL verify result 20

The `GetPatientEncounters` endpoint is also documented but only returns encounter metadata (PatientId, VisitBeginDateTime, ProviderFullName), not clinical content.

## 4. Export Content: What's In It

### What the API documentation describes

The `GetPatientData` endpoint accepts 20 boolean toggle parameters (plus `patientid`, `ccdafromdate`, `ccdatodate`, `returnformat`). Each toggle controls inclusion of one C-CDA section. The documentation states: "All values are options, if you donot give any paratemer it will return complete record."

The 20 toggleable C-CDA data sections are:

| Parameter | CCDA Element | Category |
|---|---|---|
| `patientname` | Patient Name | Demographics |
| `patientgender` | Sex | Demographics |
| `patientdob` | Date of Birth | Demographics |
| `patientrace` | Race | Demographics |
| `patientethnicity` | Ethnicity | Demographics |
| `patientpreferredlanguage` | Preferred Language | Demographics |
| `smokingstatus` | Smoking Status | Social History |
| `problems` | Problems | Clinical |
| `medications` | Medications | Clinical |
| `medicationallergies` | Medication Allergies | Clinical |
| `labtest` | Laboratory Tests | Clinical |
| `labresults` | Laboratory Values Results | Clinical |
| `vitalsigns` | Vital Signs | Clinical |
| `procedures` | Procedures | Clinical |
| `careteammembers` | Care Team Members | Clinical |
| `immunizations` | Immunizations | Clinical |
| `udiforpatientdevices` | Unique Device Identifiers (procedures) | Clinical |
| `assessment` | Assessment and Plan | Clinical |
| `goals` | Goals | Clinical |
| `healthconcerns` | Health Concerns | Clinical |

### What the sample C-CDA response contains

The embedded sample C-CDA response (pages 5–25 of the PDF) contains 18 sections:

1. Chief Complaint
2. Allergies, Adverse Reactions
3. Immunizations
4. Medications
5. Medications Administered During Visit
6. Care Plan
7. Assessments
8. Health Concerns Section
9. Goals Section
10. Procedures
11. Social History
12. Vital Signs
13. Encounter Diagnosis
14. Results
15. Problems
16. Functional Status
17. Referrals
18. Summarization of episode note (document header)

The sample data uses test patient data (non-PHI). The C-CDA conforms to the standard CCD template structure with SNOMED CT and LOINC coding.

### What is NOT documented

- **No data dictionary**: Zero field-level definitions, no data types, no cardinalities, no value sets
- **No schema**: No machine-readable schema for the C-CDA content or the native data model
- **No sample export files**: Only the inline C-CDA sample in the PDF
- **No relationship documentation**: No foreign keys, no entity relationships
- **No native data model exposure**: The API only outputs C-CDA projections, not the underlying database tables

**Total documented entities: 20 C-CDA section toggles (not database tables)**
**Total documented fields: 0 (no field-level documentation)**
**Fields with descriptions: 0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides exactly one data access mechanism: a C-CDA-based API with 20 section toggles corresponding to standard USCDI v1 data classes. This is the standard clinical summary content required for transitions of care — demographics, problems, medications, allergies, lab results, vitals, procedures, immunizations, care team, goals, and health concerns.

The vendor does not organize this as an "EHI export" — there is no (b)(10)-specific documentation, no data dictionary, and no acknowledgment that the export should cover all EHI. The documentation is explicitly labeled for (g)(8)/(g)(9) criteria.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 API parameters (name, gender, DOB, race, ethnicity, language) | Basic USCDI demographics only; no address, phone, email, emergency contacts, insurance info |
| Encounters / visits | ⚠️ Partial | `GetPatientEncounters` returns date + provider name only | No encounter detail, no visit types, no linked clinical data per encounter |
| Problems / conditions | ✅ Covered | `problems` parameter; sample shows SNOMED-coded problem list | Standard C-CDA problem list |
| Medications / prescriptions | ✅ Covered | `medications` parameter; sample shows medication section | Standard C-CDA medications; no prescription details or e-prescribing data |
| Allergies | ✅ Covered | `medicationallergies` parameter; sample shows allergy section | Standard C-CDA allergies |
| Immunizations | ✅ Covered | `immunizations` parameter; sample shows immunization section | Standard C-CDA immunizations |
| Vitals | ✅ Covered | `vitalsigns` parameter; sample shows vitals section | Standard C-CDA vitals |
| Lab results | ✅ Covered | `labtest` + `labresults` parameters; sample shows results section | Standard C-CDA lab results |
| Imaging / diagnostic reports | ❌ Not covered | No imaging parameters or sections | Product stores clinical photography (unlimited, core feature); significant gap |
| Procedures | ✅ Covered | `procedures` parameter; sample shows procedures section | Standard C-CDA procedures |
| Clinical notes / documents | ⚠️ Partial | Assessment/plan section only; no full note export | Product has structured dermatology charting with 3D anatomical maps; C-CDA cannot represent this specialty-specific content |
| Care plans / goals | ✅ Covered | `assessment`, `goals`, `healthconcerns` parameters | Standard C-CDA care plan sections |
| Orders / referrals | ⚠️ Partial | Referrals section present in sample C-CDA | Lab orders (certified (a)(2) CPOE) not separately documented for export |
| Insurance / coverage | ❌ Not covered | No insurance parameters or sections | Product has insurance verification module; gap |
| Claims / billing | ❌ Not covered | No billing entities in API | Product has full RCM module (Smart Coder, claims filing, payment posting); major gap |
| Payments | ❌ Not covered | No payment data in API | Product processes electronic payments; gap |
| Consents / directives | ❌ Not covered | No consent parameters or sections | Product generates automated consent forms; gap |
| Patient communications | ❌ Not covered | No messaging data in API | Portal via Updox integration; may be in separate system |
| Specialty: Dermatology charting | ❌ Not covered | No dermatology-specific data in C-CDA | Product's core "One-Touch Charting" with 3D anatomical maps, dermatology exam templates; major gap |
| Specialty: Clinical photography | ❌ Not covered | No photo/image export | Unlimited photos linked to encounters; product's key differentiator; major gap |
| Specialty: Pathology lifecycle | ❌ Not covered | No biopsy/pathology data in API | Biopsy orders, requisitions, results, status tracking; distinctive feature; major gap |
| Specialty: Cancer tracking | ❌ Not covered | No cancer tracking data | Product has cancer patient follow-up module; gap |
| Implantable devices | ✅ Covered | `udiforpatientdevices` parameter | Standard C-CDA UDI section |

**Summary: 9 of 22 applicable domains are covered (all via standard C-CDA sections). 7 domains are not covered at all. 3 domains are partially covered. The 3 most distinctive features of the product — dermatology charting, clinical photography, and pathology lifecycle tracking — are entirely absent from the export.**

## 6. Documentation Quality

The API documentation (`eDerm-API-Documentation-G8-G9.pdf`) is rudimentary and clearly unfinished:

- **No table of contents** or structured navigation
- **Internal hostnames**: Sample URLs reference `remotedev-5`, not any production server
- **No field-level documentation**: The 20 boolean toggles are named but have no documentation of what data elements each section contains
- **Inline C-CDA sample**: The sample response is embedded as escaped XML directly in the PDF (pages 5–25), making it difficult to review
- **Unfinished**: "Terms of Use: TBD: Link will be added here" (page 26) — the documentation was never completed
- **Mislabeled**: The certification page labels the link as "G9-G10.pdf" but the actual file is "G8-G9.pdf"
- **No error handling detail**: Error section lists HTTP status codes (401, 403, 400, 200) with generic descriptions

A developer could not build a meaningful import from this documentation. The API structure is documented (endpoint URLs, authentication flow, request/response format), but there is no field-level specification of what the C-CDA sections contain, no value sets, no data type documentation, and no information about the native data model.

**No machine-readable artifacts**: No JSON Schema, no OpenAPI spec, no FHIR CapabilityStatement (the registered URL is dead), no sample export files beyond the inline C-CDA.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The vendor has no (b)(10) EHI export documentation or mechanism. The only documented data access is a (g)(9)/(g)(10) C-CDA API that covers standard USCDI clinical summary data — approximately 9 of 22 applicable data domains. The C-CDA API is clearly designed for transitions of care, not for comprehensive EHI export. The registered EHI documentation URL is non-functional (expired SSL, undeployed application). No data dictionary exists.

### Key Findings

1. **No (b)(10) documentation exists.** The vendor's certification page contains only (g)(9)/(g)(10) API documentation. There is no EHI export page, no data dictionary, and no mention of (b)(10) anywhere on the vendor's website. The CHPL-registered URL points to a dead FHIR endpoint.

2. **The only documented export is a C-CDA clinical summary API.** The `GetPatientData` endpoint returns standard C-CDA documents with 20 toggleable USCDI sections. This is a transitions-of-care API, not an EHI export.

3. **All dermatology-specific data is missing from the export.** The product's three most distinctive features — One-Touch Charting with 3D anatomical maps, unlimited clinical photography, and pathology lifecycle tracking — have no export mechanism. C-CDA cannot represent this data.

4. **The entire billing/RCM module is absent.** Despite the product having a full revenue cycle management module (Smart Coder, claims filing, electronic payment posting), no billing data appears in the export.

5. **The FHIR endpoint is non-functional.** The registered endpoint at `fhir.ederm.io:9443` has an expired SSL certificate (Feb 10, 2026) and returns 404 on all paths — the FHIR application has been undeployed from the Tomcat server.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA 2.1 (XML), JSON, or HTML (via API)
Model type:      Standard projection (C-CDA)
Entities:        20 C-CDA section toggles (not database tables)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     Inline C-CDA only (in PDF)
Bulk export:     No
Domains covered: 9 of 22 applicable domains (all via standard C-CDA)
```

### Bottom Line

eDerm Systems has not implemented a (b)(10) EHI export. What exists is a C-CDA API for clinical summaries that covers basic USCDI data classes but misses the product's most valuable and unique data: dermatology-specific charting, clinical photography, pathology lifecycle tracking, and the entire billing/RCM module. A patient requesting their complete health information from this system would receive a clinical summary covering roughly 30–40% of their data, with no dermatology-specific content and no billing records.
